'''TODO:

	(O)-find examples when one scheduler better than other

	(O)-Testing!!!!!
		#generator
		#run
		#backFilling

	(O)-multiple runs per point
	(O)-non deterministic execution (4example: 
		*finish,schedule,run in random sequence each second)
		*tick random time (1..10)
	(O)-find nice invariants to check
	(O)-build state full testing in hypothesis (compare to vary input lists)
	
	(O)-performance gains
	(X)-Draw some cool Graphs
'''

import Simulation
import Generator
import Analysis

from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type

import itertools

import timeit

import matplotlib.pyplot as plt
import numpy as np

#from collections import defaultdict

def main():
	
	start: float = timeit.default_timer()

	# graph: of gridsearch
	
	#numberOfJobs: int, numberOfNodes: int, seqR: float, largeR: float, timespan: int,minSeq: int, maxSeq: int ,minPar: int, maxPar: int)
	
	schedulers = [Simulation.fifo,Simulation.lpt,Simulation.spt]
	
	#times per point(accuracy)
	numberOfIterations = 1
	
	numberOfJobs = list(range(250,250 +1,5000))
	numberOfNodes = list(range(20,20 +1))
	seqR = [1] #part of sequential jobs (between 0 and 1)
	largeR = [1] #part of large jobs (50% of nodes or more) of Parallel jobs
	timespan = [0]#offline
	minSeq = [1000] #minimal runtime of sequential jobs
	maxSeq = list(range(1000,10000+1, 1000))#[1000] #max runtime of sequential jobs
	minPar = [10] #min runtime of parallel jobs
	maxPar = [100] #max runtime of parallel jobs
	
	results = []
	
	for conf in itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):
		#print(*conf)
		jobs: List[Simulation.Job] = Generator.generate(*conf)
		for sf in schedulers:
			#acc = (0,0,0,0)
			sys: Simulation.System = Simulation.System(jobs.copy(),20,sf)
			finishedJobs: List[Simulation.Job] = sys.run()
			#multiple anylsis => multiple lists
			results.append( (conf , Analysis.standardAnalysis(finishedJobs) ,sf) )

		#print (conf)	
	#print (*results, sep = "\n")

	stop = timeit.default_timer()
	#selector (allways for scheduler in schedulers:)
	# p of conf=0, analysis=1,scheduler=2
	#conf 0f numberOfJobs=0, numberOfNodes=1,seqR=2, largeR=3, timespan=4,minSeq=5,maxSeq=6,minPar=7,maxPar=8
	#analysis of makespan=0,flowTime=1,avgFlowTime2,maximumLateness=3
	x=lambda p: p[0][6] 
	y=lambda p: p[1][1] 
		

	for sf in schedulers:
		sfData =list(filter(lambda t: t[2] is sf, results))
		xs = list(map(x, sfData))
		ys = list(map(y, sfData))
		plt.plot(xs,ys,label= sf.__name__)

	plt.legend()
	plt.show()

	print('Time: ', stop - start) 

if __name__ == "__main__":
	print("main...")
	main()
