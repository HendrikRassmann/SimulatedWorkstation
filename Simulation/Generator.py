import Simulation
from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type, Dict, Union
import random

def jobs100() -> List[Simulation.Job]:
	jobs: List[Simulation.Job] = []
	# 10s between jobs
	# job1 = 1 + id % 10 * 2
	#def __init__(self, id: int, queueingT : int, processingT: int, degreeOP: int
	for i in range(100):
		jobs.append(Simulation.Job(id= i, queueingT= i*10, processingT= 1 +((i%15)*5), degreeOP= 1+(i%10) ) )
	return jobs



def generate(numberOfJobs: int, numberOfNodes: List[int], seqR: float, largeR: float, timespan: int,
minSeq: int, maxSeq: int ,minPar: int, maxPar: int, errorRate :int = 0, maxError :int = 0)->List[Simulation.Job]:


	#shuffle ids:
	idList = list(range(numberOfJobs))
	random.shuffle(idList)
	#ids go seq, small par, big par
	assert 0 <= errorRate <= 1
	assert 0 <= maxError
	assert numberOfJobs >= 1
	assert len(numberOfNodes) >= 1
	assert 0 <= seqR <= 1
	assert 0 <= largeR <= 1
	assert timespan >= 0
	assert maxSeq >= minSeq >= 0
	assert maxPar >= minPar >= 0
	#remember: // is integer division

	#approach: make multiple lists, shuffle list, zip
	jobs: List[Simulation.Job] = []
	for i in range(numberOfJobs):

	#a if condition else b
	#d: int, queueingT : int, processingT: int, degreeOP
		pTime = random.randint(minSeq,maxSeq) if (i < seqR*numberOfJobs) else random.randint(minPar, maxPar)
		jobs.append(Simulation.Job(\
		id=idList.pop(0),\
		queueingT= random.randint(0,timespan),\
		processingT= (round(pTime*(1+ maxError*random.random()) ) if False else  round(pTime/(1 + maxError*random.random()) ) )  if random.random() <= errorRate else pTime,\
		degreeOP= 1 if (i < seqR*numberOfJobs) else (random.randint(2,len(numberOfNodes)//2) if i < (numberOfJobs*(1 - largeR + seqR*largeR)) else (random.randint( (len(numberOfNodes)+1)//2, len(numberOfNodes)) ))\
		,realProcessingT = pTime
		  ))

	random.shuffle(jobs)
	assert len(jobs) == numberOfJobs
	return jobs
