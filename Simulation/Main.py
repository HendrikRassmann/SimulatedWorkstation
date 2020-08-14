'''
sudo Mongod : starts mongoDB
'''

'''TODO:

	2DAY:
	(O) different machine speed
	(O) false times
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
	
	schedulers = [Simulation.fifo,Simulation.lpt,Simulation.spt]
	
	#times per point(accuracy)
	numberOfIterations = list(range(1))
	numberOfJobs = list(range(250,250 +1,10))
	numberOfNodes = list(range(10,10 +1))
	seqR = [1] #part of sequential jobs (between 0 and 1).
	largeR = [1] #part of large jobs (50% of nodes or more) of Parallel jobs
	timespan = [0]# 0 <==> offline
	minSeq = [1000] #minimal processingT of sequential jobs
	maxSeq = list(range(1000,100000+1, 1000))#[1000] #max processingT of sequential jobs
	minPar = [100] #min processingT of parallel jobs
	maxPar = [1000] #max processingT of parallel jobs
	

	dbConnector = DBConnector.DBConnector()
	print ("DB connection open, start running")
	doneRuns = 0
	product = itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar)
	numberOfRuns =\
	 len(numberOfIterations)*len(numberOfJobs)*len(numberOfNodes)*\
	 len(seqR)*len(largeR)*len(timespan)*len(minSeq)*len(maxSeq)*\
	 len(minPar)*len(maxPar)*len(numberOfIterations)*len(schedulers)
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
