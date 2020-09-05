def nice (tupJobsNodes):
	jobList = tupJobsNodes[0]
	nrNodes = tupJobsNodes[1]
	nrJobs = len(jobList)
	jobIDs = list(range(0,nrJobs))
	for j in jobList:
		j.id = jobIDs.pop()

	return lambda scheduler: Simulation.System(jobList.copy(),[1]*nrNodes,scheduler)


from hypothesis import given, settings, note, strategies as st
from hypothesis.strategies import builds
import Simulation
import Analysis
from Simulation import Job
#int: id, queueingT, processingT, nodes
'''
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
'''

#keep
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


@settings(max_examples=1)
@given(generate_System_and_Jobs(maxNodes=5, maxNumberOfJobs=5, maxRuntime=10, maxQT=10))
def test_whenFiFoFirstFitFlowTime(listANDnodes):
	
	
	sysFiFo: Simulation.System = listANDnodes(Simulation.System.fifo_backfill)
	sysFirstFit: Simulation.System = listANDnodes(Simulation.System.fifo_optimistic)
	
	fifoRun = sysFiFo.run()
	flowTimeFifo =  Analysis.makespan(fifoRun)
	
	print(Analysis.makespan(fifoRun))
	note(Analysis.run2String(fifoRun))
	"""---------------------------------------"""
	
	firstFitRun = sysFirstFit.run()
	flowTimeFirstFit = Analysis.makespan(firstFitRun)
	note(flowTimeFirstFit)
	note(Analysis.run2String(fifoRun))
	note("XXXXXXXXXXXXXXXXXXXXXXXXXXX")
	assert False
	assert flowTimeFifo <= flowTimeFirstFit
