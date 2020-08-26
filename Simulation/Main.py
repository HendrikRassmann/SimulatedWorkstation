'''
python 3.6
sudo Mongod : starts mongoDB
python3 -m pytest
'''

'''TODO:

	2DAY:

	(O) false times
	(0) refactor Schedulers to be nice (Agnostic to state (Nodes, Running, etc))
	(0)-find flakeness (min/max)

	(O)-Testing!!!!!
		#generator
		#run
		#backFilling

	(O)-non deterministic execution (4example:
		*finish,schedule,run in random sequence each second)
		*tick random time (1..10)
	(O)-find nice invariants to check
	(O)-build state full testing in hypothesis (compare to vary input lists)

	(O)-fix Random. once a job is choosen, it should stay choosen until it is started (Prob.)

	(O)-performance gains
	(X)-add runs to Mongo DB, find BSON represantation
	(X)-label axis, analysis selector comprehandable :D
	(X)-find examples when one scheduler better than other
	(X)-Draw some cool Graphs
	(X) different machine speed
'''
import sys

import Simulation
import Generator
import Analysis
import DBConnector

from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type

import itertools

import timeit

import matplotlib.pyplot as plt
import numpy as np

import pymongo
from pymongo import MongoClient
import pprint


#from collections import defaultdict

def main():

	start: float = timeit.default_timer()

	# graph: of gridsearch

	#numberOfJobs: int, numberOfNodes: int, seqR: float, largeR: float, timespan: int,minSeq: int, maxSeq: int ,minPar: int, maxPar: int)

	schedulers = [\
		Simulation.System.fifo,\
		Simulation.System.fifo_fit,\
		Simulation.System.fifo_backfill,\
		Simulation.System.lpt,\
		Simulation.System.lpt_fit,\
		Simulation.System.lpt_backfill,\
		Simulation.System.spt,\
		Simulation.System.spt_fit,\
		Simulation.System.spt_backfill,\
		]

	numberOfIterations = list(range(1))
	numberOfJobs = list(range(5,5 +1,10))
	numberOfNodes = list(range(5,5 +1))
	seqR = [0.5] #part of sequential jobs (between 0 and 1).
	largeR = [1] #part of large jobs (50% of nodes or more) of Parallel jobs
	timespan = [0]# 0 <==> offline
	minSeq = [5] #minimal processingT of sequential jobs
	maxSeq = list(range(10,10+1, 10000))#[1000] #max processingT of sequential jobs
	minPar = [30] #min processingT of parallel jobs
	maxPar = [60] #max processingT of parallel jobs
	errorRate = [0,1]
	maxError = [1]

	dbConnector = DBConnector.DBConnector()
	print ("DB connection open, start running")
	doneRuns = 0
	product = itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar, errorRate, maxError)
	numberOfRuns =\
	 len(numberOfIterations)*len(numberOfJobs)*len(numberOfNodes)*\
	 len(seqR)*len(largeR)*len(timespan)*len(minSeq)*len(maxSeq)*\
	 len(minPar)*len(maxPar)*len(numberOfIterations)*len(schedulers)*\
	 len(errorRate)*len(maxError)
	print (numberOfRuns)

	for conf in product:#itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):

		for i in numberOfIterations:
			jobs: List[Simulation.Job] = Generator.generate(*conf)
			for sf in schedulers:

				sys: Simulation.System = Simulation.System(jobs.copy(),conf[1],sf)
				finishedJobs: List[Simulation.Job] = sys.run()
				dbConnector.add(*conf, Analysis.standardAnalysis(finishedJobs), sf)
				doneRuns += 1
				print ("%d Procent done" % (doneRuns/numberOfRuns*100))
				print(sf.__name__)
				print (Analysis.run2String(finishedJobs))

	del dbConnector

	stop = timeit.default_timer()
	print('Time: ', stop - start)

if __name__ == "__main__":
	if len (sys.argv) == 0 or sys.argv[1] == "halp":
		print ("halp string, now exiting")
		sys.exit()
	if sys.argv[1] == "run":
		#main and to db
		print ("now running stuff, maybe asking for arguments n stuff")
		main()
		sys.exit()

	if sys.argv[1] == "show":
		Analysis.show()

	else :
		print ("run with argument halp for help")
		sys.exit()

def show():
	pass
	#talk to db
	#plot what you want
