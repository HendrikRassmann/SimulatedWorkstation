def nice (tupJobsNodes):
	jobList = tupJobsNodes[0]
	nrNodes = tupJobsNodes[1]
	nrJobs = len(jobList)
	jobIDs = list(range(0,nrJobs))
	for j in jobList:
		j.id = jobIDs.pop()

	return lambda scheduler: Simulation.System(jobList.copy(),nrNodes,scheduler)



from hypothesis import given, settings, note, strategies as st
from hypothesis.strategies import builds
import Simulation
import Analysis
from Simulation import Job
#int: id, queueingT, processingT, nodes

generate_id = st.integers(0,100)
generate_queueingTime = st.integers(0,100)
generate_runtime = st.integers(1,100)
generate_nodes2run = st.integers(1,20)

generate_node = builds(Simulation.Node, st.integers(0,50))

generate_job = builds(\
Simulation.Job,\
generate_id,\
generate_queueingTime,\
generate_runtime,\
generate_nodes2run)

generate_id_small = st.integers(0,0)
generate_queueingTime_small = st.integers(0,10)
generate_runtime_small = st.integers(1,10)
generate_nodes2run_small = st.integers(1,5)


generate_list_jobs = st.lists(generate_job, min_size=0, max_size=50)

generate_job_small = builds(\
Simulation.Job,\
generate_id_small,\
generate_queueingTime_small,\
generate_runtime_small,\
generate_nodes2run_small)

#here important to work,
def generate_job_params(maxNodes, maxRuntime, maxQT):
	return builds(Simulation.Job,\
	 st.integers(0,0),\
	 st.integers(0,maxQT),\
	 st.integers(1,maxRuntime),\
	 st.integers(1,maxNodes) )

def generate_System_and_Jobs(maxNodes, maxNumberOfJobs, maxRuntime, maxQT):#give scheduler, return system ready2run
	#unique ids: set later in Test!
	#flatmap:
	ids = list(range(0,maxNumberOfJobs))
	return st.integers(1,maxNodes).flatmap(lambda x:\
		st.tuples(st.lists(generate_job_params(x,maxRuntime,maxQT),min_size=2,max_size=maxNumberOfJobs), st.integers(x,x)) ).map(nice)

generate_list_jobs_small = st.lists(generate_job_small, min_size=2, max_size=5, unique_by=(lambda x: x.queueingT) )

generate_list_nodes = st.lists(generate_node, min_size=0, max_size=50 )

#####################
# Testing Schedulers#
# ( ) backfilling
# (X) fifo
# (X) firstfit
# (X) lpt
# (X) spt
# (X) rand
#####################

@settings(max_examples=300)
@given(generate_list_jobs_small)#unique ids
def test_backfilling(q):
	#small list has id 0
	sysFiFo: Simulation.System = Simulation.System(q.copy(),5,Simulation.fifo)
	sysBackfilling: Simulation.System = Simulation.System(q.copy(),5,Simulation.backfilling)

	fifoTrace = sysFiFo.run()
	backfillingTrace = sysBackfilling.run()

	fifoTraceStart = sorted(list(map(lambda j: j.startRunning, fifoTrace )))
	backfillingTraceStart = sorted(list(map(lambda j: j.startRunning,backfillingTrace )))

	note("".join(map(str,q)) )
	note("#OfNodes: "+str(5) )

	note("fifoTrace:")
	note("".join(map(str,fifoTrace)))
	note("backfillingTrace:")
	note("".join(map(str,backfillingTrace)))

	for f,b in zip(fifoTraceStart, backfillingTraceStart):
		assert b <= f
	'''
	#fifoRun = list(map(lambda j: j.startRunning, sysFiFo.run())).sort()#
	print(len(fifoRun))
	backfillingRun = list(map(lambda j: j.startRunning, sysBackfilling.run())).sort()

	print(len(fifoRun))
	for f,b in zip(fifoRun,backfillingRun):#len 0?
		assert b.queueingT <= f.queueingT'''


@given(generate_list_jobs, generate_list_nodes)
def test_random(q,n):
	nextJob = Simulation.rand(q,n)
	if not (q and n): assert nextJob is None
	else:
		if nextJob is not None:
			assert nextJob[0] in q
			for node in nextJob[1]: assert node in n
		else:
			assert max( map(lambda j: j.degreeOP,q)) > len(n)
		#one not runnable job

@given(generate_list_jobs, generate_list_nodes)
def test_lpt(q,n):
	# picks a job with the longest processingT
	# found one -> no other job longer
	# none	-> either no job runnable
	#	-> or one of the longest not runnable

	nextJob = Simulation.lpt(q,n)

	#q or nodes empty
	if not (q and n):
		assert nextJob is None
	else:
		if nextJob is None: #only runs the longest job

			maxPT = max( map(lambda j: j.processingT,q) ) #max processingT in q
			nodesAvl = len(n)
			assert max(filter(lambda j: j.processingT == maxPT, q), key=lambda j: j.degreeOP).degreeOP > nodesAvl

		else:
			for j in q: assert j.processingT <= nextJob[0].processingT

#some cool shit with inverting runtimes maybe?
@given(generate_list_jobs, generate_list_nodes)
def test_spt(q,n):
	nextJob = Simulation.spt(q,n)

	#q or nodes empty
	if not (q and n):
		assert nextJob is None
	else:
		if nextJob is None: #only runs the longest job

			minPT = min( map(lambda j: j.processingT,q) ) #max processingT in q
			nodesAvl = len(n)
			assert max(filter(lambda j: j.processingT == minPT, q), key=lambda j: j.degreeOP).degreeOP > nodesAvl#fails

		else:
			for j in q: assert j.processingT >= nextJob[0].processingT


def test_fifo_unit():
	emptyJobList = []
	emptyNodeList = []
	onePool = [3]
	twoPool = [2,1]
	tenPool = [1,2,3,4,5,6,7,8,9,10]
	oneJob = Simulation.Job(1,1,1,1)
	twoJob = Simulation.Job(2,2,2,2)
	threeJob = Simulation.Job(3,3,3,3)
	forOneJob = Simulation.Job(4,1,4,4)

	assert Simulation.fifo(emptyJobList, tenPool) == None
	assert Simulation.fifo([threeJob], emptyNodeList) == None
	assert Simulation.fifo(emptyJobList, emptyNodeList) == None

	pair1 = Simulation.fifo([oneJob],onePool)
	assert pair1[0] == oneJob and pair1[1] == onePool

	pair2 = Simulation.fifo([twoJob, oneJob], [1])
	assert pair2[0] == oneJob and pair2[1] == [1]

	pair3 = Simulation.fifo([twoJob, threeJob], twoPool) # 3 :two many nodes
	assert pair3[0] == twoJob and (pair3[1] == [1,2] or pair3[1] == [2,1])

	pair4 = Simulation.fifo([forOneJob, twoJob],twoPool)
	assert pair4 == None


def test_firstFit_unit():
#int: id, queueingT, processingT, nodes
	emptyJobList = []
	emptyNodeList = []
	onePool = [3]
	twoPool = [2,1]
	tenPool = [1,2,3,4,5,6,7,8,9,10]
	oneJob = Simulation.Job(1,1,1,1)
	twoJob = Simulation.Job(2,2,2,2)
	threeJob = Simulation.Job(3,3,3,3)
	forOneJob = Simulation.Job(4,1,4,4)

	assert Simulation.firstFit(emptyJobList, tenPool) == None
	assert Simulation.firstFit([threeJob], emptyNodeList) == None
	assert Simulation.firstFit(emptyJobList, emptyNodeList) == None

	pair1 = Simulation.firstFit([threeJob,forOneJob], onePool)
	assert pair1 == None
	pair2 = Simulation.firstFit([forOneJob, threeJob], tenPool)
	assert pair2[0] == forOneJob

@given(st.integers(), st.integers())
def test_firstFit(q,nodes):
	assert True


@given(generate_list_jobs, generate_list_nodes)
def test_fifo(q,nodes):
	pair = Simulation.fifo(q, nodes)
	if pair != None:
		assert len(pair[1]) >=1
		assert pair[0].degreeOP <= len(pair[1])

@given(generate_list_jobs)
def test_ffEQfifo_allRunnable(q):
	nodes1k = list(map(Simulation.Node, list(range(50)) ) )#should be max nodes needed
	assert Simulation.fifo(q, nodes1k) == Simulation.firstFit(q, nodes1k)
	#doesnt have to be, you know, there might be many right answers

### lets do some statefull testing next

###

@settings(max_examples=10000)
@given(generate_System_and_Jobs(maxNodes=5, maxNumberOfJobs=5, maxRuntime=10, maxQT=10))
def test_whenFiFoFirstFitFlowTime(listANDnodes):

	sysFiFo: Simulation.System = listANDnodes(Simulation.fifo)
	sysFirstFit: Simulation.System = listANDnodes(Simulation.firstFit)


	fifoRun = sysFiFo.run()
	flowTimeFifo =  Analysis.makespan(fifoRun)
	note(flowTimeFifo)
	note(Analysis.run2String(fifoRun))
	"""---------------------------------------"""
	firstFitRun = sysFirstFit.run()
	flowTimeFirstFit = Analysis.makespan(firstFitRun)
	note(flowTimeFirstFit)
	note(Analysis.run2String(fifoRun))
	note("XXXXXXXXXXXXXXXXXXXXXXXXXXX")
	assert flowTimeFifo <= flowTimeFirstFit
