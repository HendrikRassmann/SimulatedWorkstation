

'''
python 3.6
sudo Mongod : starts mongoDB
$: mongo opens mongoshell in terminal
--use pastRunns
--db.run1.drop()
python3 -m pytest
'''

'''TODO:

	2DAY:

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

	# Fuck Random (O)-fix Random. once a job is choosen, it should stay choosen until it is started (Prob.)
	(X) refactor Schedulers to be nice (Agnostic to state (Nodes, Running, etc)) #but !this! sucks
	(X) false times
	(X)-performance gains
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
import functools
import operator

import timeit

import matplotlib.pyplot as plt
import numpy as np

import pymongo
from pymongo import MongoClient
import pprint

import math


#from collections import defaultdict

def main():

	start: float = timeit.default_timer()


	schedulers = [\
		Simulation.System.fifo,\
		Simulation.System.fifo_fit,\
		Simulation.System.fifo_backfill,\
		Simulation.System.lpt,\
		#Simulation.System.lpt_fit,\
		#Simulation.System.lpt_backfill,\
		Simulation.System.spt,\
		#Simulation.System.spt_fit,\
		#Simulation.System.spt_backfill,\
		]

	numberOfIterations = list(range(5))

	dbConnector = DBConnector.DBConnector()
	print ("DB connection open, start running")
	doneRuns = 0

	experiment = figure_4

	product = itertools.product( *experiment.values())
	numberOfRuns = functools.reduce(operator.mul, map(len, list(experiment.values())), 1)
	#product = itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar, errorRate, maxError)

	runCounter = 0
	for conf in product:#itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):

		for i in numberOfIterations:
			jobs: List[Simulation.Job] = Generator.generate(*conf)
			for sf in schedulers:
				sys: Simulation.System = Simulation.System(jobs.copy(),conf[1],sf)
				finishedJobs: List[Simulation.Job] = sys.run()
				dbConnector.add(*conf, Analysis.standardAnalysis(finishedJobs), sf)

		runCounter+=1
		print(runCounter/numberOfRuns)

	del dbConnector

	stop = timeit.default_timer()
	print('Time: ', stop - start)



def show():
	pass
	#talk to db
	#plot what you want
figure_1 = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [[100,100,100,100,100,100,100,100,100,100]],
	"seqR" : [1],
	"largeR" : [0],
	"timespan" : [0],
	"minSeq" : [1000],
	"maxSeq" : list(range(1000,100000+1, 2000)),
	"minPar" : [0],
	"maxPar" : [0],
	"errorRate" : [0],
	"maxError" : [0]
}
figure_2 = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [100,100,100,100,100,100,100,100,100,100],
	"seqR" : [1],
	"largeR" : [0],
	"timespan" : list(range(0,10000+1, 200)),
	"minSeq" : [1000],
	"maxSeq" : [50000],
	"minPar" : [0],
	"maxPar" : [0],
	"errorRate" : [0],
	"maxError" : [0]
}
figure_3 = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [[100,100,100,100,100,100,100,100,100,100]],
	"seqR" :  [ x/100 for x in range(20,101, 4)],
	"largeR" : [0.3],
	"timespan" : [10000],
	"minSeq" : [1000],
	"maxSeq" : [50000],
	"minPar" : [10000],
	"maxPar" : [400000],
	"errorRate" : [0],
	"maxError" : [0]
}
slowerR = 0.75
figure_4 = {
	"numberOfJobs" : [500],
	"numberOfNodes" : [[ 666 if x/21 < slowerR else 4700 for x in range (22)]],
	"seqR" :  [ x/100 for x in range(50,101, 25)],
	"largeR" : [0.3],
	"timespan" : [2000],
	"minSeq" : [2000],
	"maxSeq" : [100000],
	"minPar" : [20000],
	"maxPar" : [800000],
	"errorRate" : [0],
	"maxError" : [0]
}

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
