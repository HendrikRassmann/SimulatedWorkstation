def nice (tupJobsNodes):
	#handles stuf thats easier this way:
	#unique ids
	#earliest jobs starts at 0
	jobList = tupJobsNodes[0]
	nrNodes = tupJobsNodes[1]
	minQT = min(jobList, key=lambda j:j.queueingT).queueingT
	nrJobs = len(jobList)
	jobIDs = list(range(0,nrJobs))
	for j in jobList:
		j.id = jobIDs.pop()
		j.queueingT -= minQT

	return lambda scheduler: Simulation.System(jobList.copy(),[1]*nrNodes,scheduler)


from hypothesis import given, settings, note, assume, strategies as st
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


def compareA2BonC(a_scheduler, b_scheduler, listAndNodes, metric, unique = False):

	note("Is " + str(a_scheduler) + " allways better than " + str(b_scheduler) + " by " + str(metric) + " ?")
	note("No! counterexample:")
	sysA = listAndNodes(a_scheduler)
	sysB = listAndNodes(b_scheduler)
	
	if unique:
		for j in sysA.futureJobs:
			j.queueingT = j.id
		for j in sysA.futureJobs:
			j.queueingT = j.id
		#assume(len(sysA.futureJobs) == len(set(map(lambda j:j.queueingT, sysA.futureJobs))) )
			
	runA = sysA.run()	
	metricA = metric(runA)
		
	note( str(metric) + " of " + str(a_scheduler) + " : " + str(metricA) ) 
	note(Analysis.run2String(runA))
	
	######################################################
	
	runB = sysB.run()
	metricB = metric(runB)
	
	note( str(metric) + " of " + str(b_scheduler) + " : " + str(metricB) )
	note(Analysis.run2String(runB))
	
	return metricA <= metricB

'''
@settings(max_examples=100000)
@given(generate_System_and_Jobs(maxNodes=5, maxNumberOfJobs=5, maxRuntime=10, maxQT=10))
def test_optimisticBetter(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_backfill, Simulation.System.fifo_optimistic, listAndNodes, Analysis.makespan)

@settings(max_examples=100000)
@given(generate_System_and_Jobs(maxNodes=5, maxNumberOfJobs=5, maxRuntime=10, maxQT=10))
def test_optimisticWorse(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.makespan)
	
@settings(max_examples=100000)
@given(generate_System_and_Jobs(maxNodes=5, maxNumberOfJobs=5, maxRuntime=10, maxQT=10))
def test_optimisticBetter_Lateness(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_backfill, Simulation.System.fifo_optimistic, listAndNodes, Analysis.maximumLateness)

@settings(max_examples=100000)
@given(generate_System_and_Jobs(maxNodes=5, maxNumberOfJobs=5, maxRuntime=10, maxQT=10))
def test_optimisticWorse_LateNess(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.maximumLateness, False)
'''

@settings(max_examples=50000)
@given(generate_System_and_Jobs(maxNodes=3, maxNumberOfJobs=5, maxRuntime=10, maxQT=0))
def test_optimisticWorse_LateNess1(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.maximumLateness, True) or compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.makespan, True)

@settings(max_examples=50000)
@given(generate_System_and_Jobs(maxNodes=10, maxNumberOfJobs=5, maxRuntime=10, maxQT=0))
def test_backfill_better_fifo_and_optimistic(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.makespan, False) or compareA2BonC(Simulation.System.fifo, Simulation.System.fifo_backfill, listAndNodes, Analysis.makespan, False)
