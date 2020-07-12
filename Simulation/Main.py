'''TODO:
	-Draw some cool Graphs
	-Testing!!!!!
		#generator
		#run
		#backFilling
'''

import Simulation
import Generator
import Analysis

from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type

import itertools

import timeit

import matplotlib.pyplot as plt
import numpy as np


def main():
	
	start: float = timeit.default_timer()

	# graph: of gridsearch
	
	#numberOfJobs: int, numberOfNodes: int, seqR: float, largeR: float, timespan: int,minSeq: int, maxSeq: int ,minPar: int, maxPar: int)
	
	schedulers = [Simulation.fifo, Simulation.firstFit, Simulation.backfilling]
	
	numberOfJobs = list(range(250,250 +1,5000))
	numberOfNodes = list(range(20,20 +1))
	seqR = [1]
	largeR = [0]
	timespan = [0]#offline
	minSeq = [1000]
	maxSeq = list(range(1000,10000+1,1000))#[1000]
	minPar = [10]
	maxPar = [100]
	
	for conf in itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):
		print(*conf)
		jobs: List[Simulation.Job] = Generator.generate(*conf)
		for sf in schedulers:
			sys: Simulation.System = Simulation.System(jobs.copy(),20,sf)
			finishedJobs: List[Simulation.Job] = sys.run()
			Analysis.standardAnalysis(finishedJobs)
		#print (conf)	
	
	#Your statements here

	stop = timeit.default_timer()

	'''plt.subplot(2,1,1)
plt.plot( ids,expectedTimes,'o-' )
plt.ylabel('expectedTimes of Job')
plt.plot( ids,nrOfNodes,label="nr of nodes")
plt.ylabel('expected Time in s\n nr of nodes used')


plt.subplot(2,1,2)
plt.plot( ids,timeInQ,'.-')
plt.ylabel('time waiting in Q')
plt.savefig('graphs.png')
plt.show()'''

	print('Time: ', stop - start) 

if __name__ == "__main__":
	print("main...")
	main()
