#from hypothesis.strategies import integers

#assert 0 == 1

from hypothesis import given, settings, note, strategies as st
from hypothesis.strategies import builds
import Simulation
from Simulation import Job
#int: id, enterQ, runtime, nodes

generate_id = st.integers(0,1000)
generate_enterQ = st.integers(0,1000)
generate_runtime = st.integers(1,1000)
generate_nodes2run = st.integers(1,50)

generate_node = builds(Simulation.Node, st.integers(0,50))

generate_job = builds(\
Simulation.Job,\
generate_id,\
generate_enterQ,\
generate_runtime,\
generate_nodes2run)


generate_list_jobs = st.lists(generate_job, min_size=0, max_size=50)

generate_list_nodes = st.lists(generate_node, min_size=0, max_size=50 )  


#no examples?


#@given
def test_list_diff():
	pass

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
	

#@given(st.integers)
@given(generate_list_jobs, generate_list_nodes)
def test_fifo(q,nodes):
	pair = Simulation.fifo(q, nodes)
	if pair != None:
		assert len(pair[1]) >=1
		assert pair[0].nodes2run <= len(pair[1])


'''
This should hold for any 2 scheduling strategies

@given(generate_list_jobs, generate_nodes)
@settings(max_examples=100)
def test_firstFitEQfifoL1(q,n):
	if (len(q) > 0):
		firstElem = q[:1]
		assert Simulation.fifo(firstElem,n) == Simulation.firstFit(firstElem,n)
'''

@given(generate_list_jobs)
def test_ffEQfifo_allRunnable(q):
	nodes1k = list(map(Simulation.Node, list(range(50)) ) )#should be max nodes needed
	assert Simulation.fifo(q, nodes1k) == Simulation.firstFit(q, nodes1k)
	#doesnt have to be, you know, there might be many right answers


#generate List of jobs
#sort by enterQ
#ids: random
#enterQ +y
#runntime = generate
#nodes ? generate 


#test fifo

#print ("hello, my name is")
#generate_job.example()

#Jobs generator
@given(st.integers(0,1000), st.integers(0,1000), st.integers(0,1000), st.integers(1,100) )
def test_test(ids,enterQ,runtime,nodes):
	j = Simulation.Job(ids,enterQ,runtime,nodes)
	assert j.runtime >= 0
	assert 1 == 1
	
#generate list of jobs?