import Simulation
from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type

def jobs100() -> List[Simulation.Job]:
	jobs: List[Simulation.Job] = []
	# 10s between jobs
	# job1 = 1 + id % 10 * 2
	#def __init__(self, id: int, enterQ : int, runtime: int, nodes2run: int
	for i in range(100):
		jobs.append(Simulation.Job(id= i, enterQ= i*10, runtime= 1 +((i%15)*5), nodes2run= 1+(i%10) ) )
	return jobs

#next up: good generation
	#number of jobs
	#set of nodes
	#percentage of sequential
	#percentage of large parallel jobs (>=50%)
	#time span of q time
	#seq min/max runtime	uniform
	#parralel min/max runtime	uniform
