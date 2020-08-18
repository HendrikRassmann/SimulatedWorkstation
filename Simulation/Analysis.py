import Simulation
import DBConnector

from typing import cast, List, Union, Optional, Callable, Tuple, Text, TypeVar, Generic, Type, Dict

import matplotlib.pyplot as plt
import numpy as np

fixed = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : 10,
	"Params.seqR" : 1,
	#"Params.largeR" : 1,
	"Params.timespan" : 0,
	"Params.minSeq" : 1000,
	#"Params.maxSeq" : 1000, vary
	#"Params.minPar" : 100,
	#"Params.maxPar" : 1000
}


def show():
	
	sfXY = {}
	dbConnector = DBConnector.DBConnector()
	xAxis = "maxSeq"
	yAxis = "makespan"
	schedulers = ["fifo","spt","lpt"]
	for sf in schedulers:
		sfXY[sf] = [] #pair of x,ys
		##x,y list für jeden scheduler
	print ("next: NewLine")
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
		"fifo":"+",
		"spt":"x",
		"lpt":"*"}
	
	for sf in schedulers:
		lsf = list(map(list, zip(*sorted(sfXY[sf], key=lambda x:x[0]))))
		print (lsf)
		xValues = lsf[0]
		yValues = lsf[1]
		plt.plot(xValues,yValues,label= sf,marker=algoRep.get(sf, "."))
		plt.xlabel(xAxis)
		plt.ylabel(yAxis)
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
	lastFinished: int = max(jobs, key=lambda j : j.completionT).completionT
	return lastFinished - firstEnter
	
def flowTime(jobs: List[Simulation.Job])->int:
	#how does this handle Nonde? idk
	return sum(map(lambda j: (j.completionT - j.queueingT), jobs ) )
	
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
	#print ("Standard Analysis")
	#print ("makespan: %d", makespan(jobs) )
	#print ("flowtime: %d", flowTime(jobs) )
	#print ("avgflowtime: %d", avgFlowTime(jobs))
	#print ("maximum lateness: %d", maximumLateness(jobs))
	return resultDict

def run2String(jobs: List[Simulation.Job])->str:
	
	#assumption: complete Run
	#assumption: starts at 0
	#assumption: 0 <= id < 10
	lastCompletion: int = max(jobs,key=(lambda j:j.completionT)).completionT
	
	#legende:
	#id,qtime,paral
	legend: str = "".join(list(map(lambda j: "id: %d, queueingT: %d, processingTime: %d, degreeOfParallelism: %d\n" % (j.id, j.queueingT,j.processingT, j.degreeOP ), list(sorted(jobs,key=lambda j: j.id)) )))
	#nodes: #QTimes später
	#start,end,id
	nodesInRun: Dict[int,List[Tuple[int,int,int]]] = {}
	for j in jobs:
		for n in j.runningOn:
			if n.id in nodesInRun:
				nodesInRun[n.id].append( (j.startRunning, j.completionT, j.id) )
			else:
				nodesInRun[n.id]=[(j.startRunning, j.completionT, j.id)]
	
	for l in nodesInRun:
		nodesInRun[l].sort(key=lambda x:x[0]) #sorted by start
	nodeStrings:Dict[int,str] = {}
	for l in nodesInRun:
		nodeStrings[l]=['-']*lastCompletion
		for j in nodesInRun[l]:
			nodeStrings[l][j[0]:j[1]] = [str(j[2])]*(j[1]-j[0])
		nodeStrings[l] = ["[",str(l),"]",":"] + nodeStrings[l] + ['\n']

	return legend + "".join(list(map(lambda x:"".join(x), list(nodeStrings.values()))))

		
	
	
	
