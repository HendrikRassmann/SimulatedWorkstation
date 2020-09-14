def nice (tupJobsNodes):
	#handles stuf thats easier this way:
	#unique ids
	#earliest jobs starts at 0
	jobList = tupJobsNodes[0].copy() #copy Job list to not modify it in other tests
	nrNodes = tupJobsNodes[1]
	minQT = min(jobList, key=lambda j:j.queueingT).queueingT
	nrJobs = len(jobList)
	jobIDs = list(range(0,nrJobs))
	for j in jobList:
		j.id = jobIDs.pop()
		j.queueingT -= minQT

	return lambda scheduler: Simulation.System(jobList.copy(),[1]*nrNodes,scheduler)


from hypothesis import given, settings, Verbosity, note, assume, target, strategies as st
from hypothesis.strategies import builds
import Simulation
import Analysis
from Simulation import Job

#keep
#here important to work,
def generate_job_params(maxNodes, maxRuntime, maxQT):
	return builds(Simulation.Job,\
	 st.integers(0,0),\
	 st.integers(0,maxQT),\
	 st.integers(1,maxRuntime),\
	 st.integers(1,maxNodes) )

def generate_System_and_Jobs(maxNodes, maxNumberOfJobs, maxRuntime, maxQT, perm=False):#give scheduler, return system ready2run
	return st.integers(1,maxNodes).flatmap(lambda x:\
		st.tuples(st.lists(generate_job_params(x,maxRuntime,maxQT),min_size=2,max_size=maxNumberOfJobs), st.integers(x,x)) ).map(nice)

def generate_System_and_Jobs_ID_Permutation(maxNodes, maxNumberOfJobs, maxRuntime, maxQT):
	return st.integers(1,maxNodes).flatmap(lambda x:\
		st.tuples(st.lists(generate_job_params(x,maxRuntime,maxQT),min_size=2,max_size=maxNumberOfJobs),st.integers(x,x)) ).flatmap(lambda x:\
			st.tuples(st.just(x) , st.tuples(st.permutations(x[0]) ,st.just(x[1]) ) )    ) #list of systems

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
	complexityA = Analysis.complexityOfRun(runA)
	note( str(metric) + " of " + str(a_scheduler) + " : " + str(metricA) )
	note(Analysis.run2String(runA))
	note(complexityA)

	######################################################

	runB = sysB.run()
	metricB = metric(runB)
	complexityB = Analysis.complexityOfRun(runB)

	note( str(metric) + " of " + str(b_scheduler) + " : " + str(metricB) )
	note(Analysis.run2String(runB))
	note(complexityB)

	#target( (metricA-metricB)*1.0, label="difference") #größere minimalfälle, dafür schneller gefunden
	#target( 1.0*max(complexityA, complexityB), label="complexity" )# sometimes one run doesnt use a node
	return metricA <= metricB

'''
@settings(max_examples=50000)
@given(generate_System_and_Jobs(maxNodes=3, maxNumberOfJobs=6, maxRuntime=10, maxQT=10))
def test_backfill_better_fifo_and_optimistic_makespan_lateness(listAndNodes):
	assert compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.maximumLateness, True) or compareA2BonC(Simulation.System.fifo, Simulation.System.fifo_backfill, listAndNodes, Analysis.maximumLateness, True) or compareA2BonC(Simulation.System.fifo_optimistic, Simulation.System.fifo_backfill, listAndNodes, Analysis.makespan, True) or compareA2BonC(Simulation.System.fifo, Simulation.System.fifo_backfill, listAndNodes, Analysis.makespan, True)
'''
@settings(max_examples=100000, deadline=None)
@given(generate_System_and_Jobs(maxNodes=10, maxNumberOfJobs=10, maxRuntime=10, maxQT=10))
def test_compareXY12a2exas211aasda111111(listAndNodes):
	#loser +winner
	assert compareA2BonC(Simulation.System.spt_backfill, Simulation.System.spt, listAndNodes, Analysis.makespan, False)
'''
@settings(max_examples=100)
@given(generate_System_and_Jobs_ID_Permutation(maxNodes=10, maxNumberOfJobs=10, maxRuntime=10, maxQT=10))
def test_smallest_difference(listAndNodes):#tuple
	sysA = nice(listAndNodes[0])(Simulation.System.firstID)
	run_a = sysA.run()
	makespan_a = Analysis.makespan(run_a)
	note(makespan_a)
	note (Analysis.run2String(run_a))


	sysB = nice(listAndNodes[1])(Simulation.System.firstID)
	run_b = sysB.run()
	makespan_b = Analysis.makespan(run_b)
	note(makespan_b)
	note (Analysis.run2String(run_b))


	assert (makespan_a == makespan_b)
'''
