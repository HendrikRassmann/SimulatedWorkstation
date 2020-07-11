import Simulation
from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type
import random

def jobs100() -> List[Simulation.Job]:
	jobs: List[Simulation.Job] = []
	# 10s between jobs
	# job1 = 1 + id % 10 * 2
	#def __init__(self, id: int, enterQ : int, runtime: int, nodes2run: int
	for i in range(100):
		jobs.append(Simulation.Job(id= i, enterQ= i*10, runtime= 1 +((i%15)*5), nodes2run= 1+(i%10) ) )
	return jobs

def generate(numberOfJobs: int, numberOfNodes: int, sequentialR: float, largeR: float, timespan: int,
minSeq: int, maxSeq: int ,minPar: int, maxPar: int)->List[Simulation.Job]:

	assert numberOfJobs >= 1
	assert numberOfNodes >= 1
	assert 0 <= sequentialR <= 1
	assert 0 <= largeR <= 1 
	assert timespan >= 0
	assert minSeq >= 0
	assert maxSeq >= minSeq
	assert minPar >= 0
	assert maxPar >= minPar
	#remember: // is integer division

	#approach: make multiple lists, shuffle list, zip
	jobs: Simulation.Job = []
	for i in range(numberJobs):
		
	#a if condition else b
	#d: int, enterQ : int, runtime: int, nodes2run
		jobs.append(Simulation.Job(\
		\id=i,
		\enterQ= random.randint(minSeq,maxSeq) if (i/numberNodes < sequentialR) else random.randint(minPar, maxPar),
		\nodes2run= 1 if (i/numberNodes < sequentialR) else ( random.randint(2,nodes//2) if (i/numberNodes) <((1-sequentialR))
		))
	#seq,par, bigPar list
	#fill list seq=>1, par=>random(2,nodes/2), bigPar random (nodes+1/2, nodes )
	
	return []

#next up: good generation
	#number of jobs
	#set of nodes
	#percentage of sequential
	#percentage of large parallel jobs (>=50%)
	#time span of q time
	#seq min/max runtime	uniform
	#parralel min/max runtime	uniform
