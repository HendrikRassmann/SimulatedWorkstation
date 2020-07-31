'''
MONGO DB STUFF:

'''

'''QUESTIONS:
run from main with string args, and start dbs and typecheck and stuff
or make a shell script, that does that stuff? ++++<3+++++++
'''

'''TODO:

	2DAY:
	(O)-add runs to Mongo DB, find BSON represantation
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
	
	(O)-performance gains
	(X)-label axis, analysis selector comprehandable :D
	(X)-find examples when one scheduler better than other
	(X)-Draw some cool Graphs
'''
'''
"Params" : {
		"numberOfJobs": _,
  		"numberOfNodes: _,
  		"seqR": _,
  		"largeR":_,
  		"timespan":_,
  		"minSeq": _,
  		"maxSeq": _,
  		"minPar": _,
  		"maxPar": _,
  		"evals": []
  		
}
"Eval" : {
		"makespan": _,
  		"flowTime": _,
  		"avgFlowTime": _,
  		"maximumLateness": _
}

'''
import sys, getopt

import Simulation
import Generator
import Analysis

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
	numberOfIterations = range(3)
	numberOfJobs = list(range(250,1000 +1,200))
	numberOfNodes = list(range(20,20 +1))
	seqR = [0.5] #part of sequential jobs (between 0 and 1)
	largeR = [1] #part of large jobs (50% of nodes or more) of Parallel jobs
	timespan = [0]#offline
	minSeq = [1000] #minimal runtime of sequential jobs
	maxSeq = list(range(1000,1000+1, 1000))#[1000] #max runtime of sequential jobs
	minPar = [10] #min runtime of parallel jobs
	maxPar = [100] #max runtime of parallel jobs
	
	results = []
	
	#addTryCatch
	client = MongoClient('localhost',27017)

	database = client['pastRunns']
	collection = database['run1']
	
	for conf in itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):
		#print(*conf)
		for i in numberOfIterations:
			jobs: List[Simulation.Job] = Generator.generate(*conf)
			print (typeOf(*conf))
			for sf in schedulers:
				#acc = (0,0,0,0)
				sys: Simulation.System = Simulation.System(jobs.copy(),20,sf)
				finishedJobs: List[Simulation.Job] = sys.run()
				#multiple anylsis => multiple lists
				#append
				#results.append( (conf , Analysis.standardAnalysis(finishedJobs) ,sf) )

	stop = timeit.default_timer()

	plotSelect = {
		"numberOfJobs": lambda p: p[0][0],
  		"numberOfNodes": lambda p: p[0][1],
  		"seqR": lambda p: p[0][2],
  		"largeR": lambda p: p[0][3],
  		"timespan": lambda p: p[0][4],
  		"minSeq": lambda p: p[0][5],
  		"maxSeq": lambda p: p[0][6],
  		"minPar": lambda p: p[0][7],
  		"maxPar": lambda p: p[0][8],
  		"makespan": lambda p: p[1][0],
  		"flowTime": lambda p: p[1][1],
  		"avgFlowTime": lambda p: p[1][2],
  		"maximumLateness": lambda p: p[1][3]	
	}
	
	'''analysis
	x="numberOfJobs"
	y="flowTime"
		

	for sf in schedulers:
		#results now has multiple runs with same params
		
		sfData =list(filter(lambda t: t[2] is sf, results))
		xs = list(map(plotSelect[x], sfData))
		ys = list(map(plotSelect[y], sfData))
		plt.plot(xs,ys,label= sf.__name__)
		plt.xlabel(x)
		plt.ylabel(y)

	plt.legend()
	plt.show()
	'''

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
		#try opening db
		client = MongoClient('localhost',27017)

		database = client['pastRunns']
		collection = database['run1']
		'''
		"Params" : {
		"numberOfJobs": _,
  		"numberOfNodes: _,
  		"seqR": _,
  		"largeR":_,
  		"timespan":_,
  		"minSeq": _,
  		"maxSeq": _,
  		"minPar": _,
  		"maxPar": _,
  		"evals": []
  		
}
"Eval" : {
		"makespan": _,
  		"flowTime": _,
  		"avgFlowTime": _,
  		"maximumLateness": _
}'''
		post = {
			"Params" : {
			"numberOfJobs": 100,
  			"numberOfNodes": 10,
  			"seqR": 0.5,
  			"largeR": 0.5,
  			"timespan": 123,
  			"minSeq": 1,
  			"maxSeq": 10,
  			"minPar": 5,
  			"maxPar": 50}
  			,
  			"evals": [{
  				"makespan": 4,
  				"flowTime": 4,
  				"avgFlowTime": 0.4,
  				"maximumLateness": 12}
  			]
		}
		#post_id = collection.insert_one(post).inserted_id
		collection.find_one_and_update(
		{"Params.numberOfJobs": 100}, {'$push': {"evals": {
				"makespan": 1,
  				"flowTime": 2,
  				"avgFlowTime": 0.74,
  				"maximumLateness": 14
  				}
			}
		}
		)
		#make stuff safe:
			#make sure you find at max 1 entry to add to

		print ((collection.find({})))
		print (collection.find_one({"Params.numberOfJobs": 100})["evals"])
		lenOfRuns = len(collection.find_one({"Params.numberOfJobs": 100})["evals"])
		avgAvgFlowTime = (sum(map(lambda x: x["avgFlowTime"]/lenOfRuns, collection.find_one({"Params.numberOfJobs": 100})["evals"])))
		print (avgAvgFlowTime)
		
		print (database.list_collection_names())
		
		#for post in collection.find({"Params.numberOfJobs": 100}):
		#	pprint.pprint(post)		
		
		
		print ("now showing stuff, maybe asking for what to show")
		client.close()
		sys.exit()
	else :
		print ("run with argument halp for help")
		sys.exit()

def show():
	pass
	#talk to db
	#plot what you want
