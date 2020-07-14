#from hypothesis.strategies import integers

#assert 0 == 1

from hypothesis import given, settings, note, strategies as st
from hypothesis.strategies import builds
import Simulation
import Analysis
from Simulation import Job
#int: id, enterQ, runtime, nodes

generate_id = st.integers(0,100)
generate_enterQ = st.integers(0,100)
generate_runtime = st.integers(1,100)
generate_nodes2run = st.integers(1,20)

generate_node = builds(Simulation.Node, st.integers(0,50))

generate_job = builds(\
Simulation.Job,\
generate_id,\
generate_enterQ,\
generate_runtime,\
generate_nodes2run)

generate_id_small = st.integers(0,0)
generate_enterQ_small = st.integers(0,10)
generate_runtime_small = st.integers(1,10)
generate_nodes2run_small = st.integers(1,5)


generate_list_jobs = st.lists(generate_job, min_size=0, max_size=50)

generate_job_small = builds(\
Simulation.Job,\
generate_id_small,\
generate_enterQ_small,\
generate_runtime_small,\
generate_nodes2run_small)

#st.lists(twoints, unique_by=(lambda x: x[0], lambda x: x[1]))
generate_list_jobs_small = st.lists(generate_job_small, min_size=2, max_size=5, unique_by=(lambda x: x.enterQ) )

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

@settings(max_examples=30001)
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
		assert b.enterQ <= f.enterQ'''


@given(generate_list_jobs, generate_list_nodes)
def test_random(q,n):
	nextJob = Simulation.rand(q,n)
	if not (q and n): assert nextJob is None
	else:
		if nextJob is not None: 
			assert nextJob[0] in q
			for node in nextJob[1]: assert node in n
		else:
			assert max( map(lambda j: j.nodes2run,q)) > len(n)
		#one not runnable job

@given(generate_list_jobs, generate_list_nodes)
def test_lpt(q,n):
	# picks a job with the longest runtime
	# found one -> no other job longer
	# none	-> either no job runnable
	#	-> or one of the longest not runnable
	
	nextJob = Simulation.lpt(q,n)

	#q or nodes empty
	if not (q and n):
		assert nextJob is None
	else:	
		if nextJob is None: #only runs the longest job

			maxPT = max( map(lambda j: j.runtime,q) ) #max runtime in q			
			nodesAvl = len(n)
			assert max(filter(lambda j: j.runtime == maxPT, q), key=lambda j: j.nodes2run).nodes2run > nodesAvl
						
		else:
			for j in q: assert j.runtime <= nextJob[0].runtime

#some cool shit with inverting runtimes maybe?
@given(generate_list_jobs, generate_list_nodes)
def test_spt(q,n):
	nextJob = Simulation.spt(q,n)
	note("".join(map(str,q)) )
	note("number of nodesAvl: %d" %len(n))
	#q or nodes empty
	if not (q and n):
		assert nextJob is None
	else:	
		if nextJob is None: #only runs the longest job

			minPT = min( map(lambda j: j.runtime,q) ) #max runtime in q			
			nodesAvl = len(n)
			assert max(filter(lambda j: j.runtime == minPT, q), key=lambda j: j.nodes2run).nodes2run > nodesAvl#fails
						
		else:
			for j in q: assert j.runtime >= nextJob[0].runtime


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
#int: id, enterQ, runtime, nodes
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
		assert pair[0].nodes2run <= len(pair[1])

@given(generate_list_jobs)
def test_ffEQfifo_allRunnable(q):
	nodes1k = list(map(Simulation.Node, list(range(50)) ) )#should be max nodes needed
	assert Simulation.fifo(q, nodes1k) == Simulation.firstFit(q, nodes1k)
	#doesnt have to be, you know, there might be many right answers

'''
@settings(max_examples=10000)
@given(generate_list_jobs_small)
def test_whenFiFoFirstFitFlowTime(q):

	sysFiFo: Simulation.System = Simulation.System(q.copy(),5,Simulation.fifo)
	sysFirstFit: Simulation.System = Simulation.System(q.copy(),5,Simulation.firstFit)
	
	fifoRun = sysFiFo.run()
	flowTimeFifo =  Analysis.makespan(fifoRun)
	firstFitRun = sysFirstFit.run()
	flowTimeFirstFit = Analysis.makespan(firstFitRun)
	note("".join(map(str,firstFitRun)))
	note("".join(map(str,q)) )
	note("#OfNodes: "+str(5) )
	
	#print(len(q))
	#print(*q,sep = "\n")
	#print ("fifoFlowTime %d, FirstFitFlowtime %d" %(flowTimeFifo,flowTimeFirstFit) )
	assert flowTimeFifo <= flowTimeFirstFit 
'''
