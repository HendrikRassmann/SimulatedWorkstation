import Simulation
import DBConnector

from typing import cast, List, Union, Optional, Callable, Tuple, Text, TypeVar, Generic, Type, Dict

import matplotlib.pyplot as plt
import numpy as np

fixed = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : 10,
	#"Params.seqR" : 1,
	"Params.largeR" : 0.3,
	"Params.timespan" : 10000,
	"Params.minSeq" : 1000,
	"Params.maxSeq" : 50000,
	"Params.minPar" : 10000,
	"Params.maxPar" : 400000,
	"Params.errorRate" : 0,
	#"Params.maxError" : 1
}


def show():

	sfXY = {}
	dbConnector = DBConnector.DBConnector()
	xAxis = "seqR"
	yAxis = "makespan"
	schedulers = [
		"fifo",
		"fifo_fit",
		"fifo_backfill",
		"spt",
		#"spt_fit",
		#"spt_backfill",
		"lpt",
		#"lpt_fit",
		#"lpt_backfill"
	]
	for sf in schedulers:
		sfXY[sf] = [] #pair of x,ys
		##x,y list für jeden scheduler
	print (sfXY["fifo"])
	docs = dbConnector.find(fixed)

	for item in docs:

		for sf in schedulers:
			xVaried = item["Params"][xAxis]
			values = item["Evals"].get(sf)
			if values is not None:
				numberOfValues = len(values)
				yAvg = sum(map (lambda x: x[yAxis], (item["Evals"][sf]) ) ) / numberOfValues
				sfXY[sf].append((xVaried,yAvg))
				print (xVaried,yAvg)
		#print (item)
	#plot tse grapf!
	#map(list, zip(*[(1, 2), (3, 4), (5, 6)]))

	algoRep = {
		"fifo":"^",
		"fifo_fit":"<",
		"fifo_backfill": ">",
		"spt":"2",
		"spt_fit":"3",
		"spt_backfill":"4",
		"lpt":"*",
		"lpt_fit":"x",
		"lpt_backfill":"X"
	}

	for sf in schedulers:
		lsf = list(map(list, zip(*sorted(sfXY[sf], key=lambda x:x[0]))))
		print (lsf)
		xValues = lsf[0]
		yValues = lsf[1]
		plt.plot(xValues,yValues,label= sf,marker=algoRep.get(sf, "."))
		plt.xlabel(xAxis)
		plt.ylabel(yAxis)
	plt.ylim(ymin=0)
	plt.legend()
	plt.show()



'''
#all methods static
#what the list has multiple runs with same config
results get plottet
'''


def makespan(jobs: List[Simulation.Job])->int:
	#how does this handle None? idk
	firstEnter: int = min(jobs, key=lambda j : j.queueingT).queueingT
	lastFinished: int = max(jobs, key=lambda j : j.realCompletionT).realCompletionT
	return lastFinished - firstEnter

def flowTime(jobs: List[Simulation.Job])->int:
	#how does this handle Nonde? idk
	return sum(map(lambda j: (j.realCompletionT - j.queueingT), jobs ) )

def avgFlowTime(jobs: List[Simulation.Job])->float:
	return flowTime(jobs) / len(jobs)

def maximumLateness(jobs: List[Simulation.Job]) ->int:
	return max(map(lambda j: j.startRunning - j.queueingT, jobs) )

def standardAnalysis(jobs: List[Simulation.Job])->Dict[str,Union[float,int]]:
	resultDict: Dict[str,Union[float,int]] = {
		"makespan": makespan(jobs),
  		"flowTime": flowTime(jobs),
  		"avgFlowTime": avgFlowTime(jobs),
  		"maximumLateness": maximumLateness(jobs)
	}
	return resultDict

def run2String(jobs: List[Simulation.Job])->str:

	#assumption: complete Run
	#assumption: starts at 0
	#assumption: 0 <= id < 10
	lastCompletion: int = max(jobs,key=(lambda j:j.realCompletionT)).realCompletionT

	#legende:
	#id,qtime,paral
	legend: str = "".join(list(map(lambda j: "id: %d, queueingT: %d, processingTime: %d, realProcessingT: %d, degreeOfParallelism: %d\n" % (j.id, j.queueingT,j.processingT,j.realProcessingT, j.degreeOP ), list(sorted(jobs,key=lambda j: j.id)) )))
	#nodes: #QTimes später
	#start,end,id
	nodesInRun: Dict[int,List[Tuple[int,int,int]]] = {}
	for j in jobs:
		for n in j.runningOn:
			if n.id in nodesInRun:
				nodesInRun[n.id].append( (j.startRunning, j.realCompletionT, j.id) )
			else:
				nodesInRun[n.id]=[(j.startRunning, j.realCompletionT, j.id)]

	for l in nodesInRun:
		nodesInRun[l].sort(key=lambda x:x[0]) #sorted by start
	nodeStrings:Dict[int,str] = {}
	for l in nodesInRun:
		nodeStrings[l]=['-']*lastCompletion#how does last completion become float??
		for j in nodesInRun[l]:
			nodeStrings[l][j[0]:j[1]] = [str(j[2])]*(j[1]-j[0])
		nodeStrings[l] = ["[",str(l),"]",":"] + nodeStrings[l] + ['\n']

	return legend + "".join(list(map(lambda x:"".join(x), list(nodeStrings.values()))))
'''Figure 2
fixed = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : 10,
	"Params.seqR" : 1,
	#"Params.largeR" : 0.5,
	#"Params.timespan" : 0,
	"Params.minSeq" : 1000,
	"Params.maxSeq" : 50000,
	#"Params.minPar" : 1000,
	#"Params.maxPar" : 100000,
	"Params.errorRate" : 0,
	#"Params.maxError" : 1
}
'''
