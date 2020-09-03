import Simulation
import DBConnector

from typing import cast, List, Union, Optional, Callable, Tuple, Text, TypeVar, Generic, Type, Dict

import matplotlib.pyplot as plt
import numpy as np





def show():
	fixed = figure_8
	print("showing")
	print(fixed)

	sfXY = {}
	dbConnector = DBConnector.DBConnector()
	xAxis = "timespan"
	yAxis = "makespan"
	schedulers = [
		"fifo",
		"fifo_fit",
		"fifo_backfill",
		"spt",
		"spt_fit",
		"spt_backfill",
		"lpt",
		"lpt_fit",
		"lpt_backfill",
		"fifo_optimistic"
	]
	for sf in schedulers:
		sfXY[sf] = [] #pair of x,ys
		##x,y list für jeden scheduler
	docs = dbConnector.find(fixed)

	for item in docs:

		for sf in schedulers:
			xVaried = item["Params"][xAxis]
			values = item["Evals"].get(sf)
			if values is not None:
				numberOfValues = len(values)
				yAvg = sum(map (lambda x: x[yAxis], (item["Evals"][sf]) ) ) / numberOfValues
				sfXY[sf].append((xVaried,yAvg))
				#print (xVaried,yAvg)

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
		#print (lsf)
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

figure_1 = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : [100,100,100,100,100,100,100,100,100,100],
	"Params.seqR" : 1,
	"Params.largeR" : 0,
	"Params.timespan" : 0,
	"Params.minSeq" : 1000,
	#"Params.maxSeq" : [list(range())100000],
	#"Params.minPar" : [0],
	#"Params.maxPar" : [0],
	"Params.errorRate" : 0
	#"Params.maxError" : [0]
}
figure_2 = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : [100,100,100,100,100,100,100,100,100,100],
	"Params.seqR" : 1,
	#"Params.largeR" : 0
	#"Params.timespan" : list(range(0,10000+1, 200)),
	"Params.minSeq" : 1000,
	"Params.maxSeq" : 50000,
	#"Params.minPar" : [0],
	#"Params.maxPar" : [0],
	"Params.errorRate" : 0
	#"Params.maxError" : 0
}
figure_3 = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : [100,100,100,100,100,100,100,100,100,100],
	#"Params.seqR" : list(map (lambda x: x/100), range(20,100+1, 4))
	"Params.largeR" : 0.3,
	"Params.timespan" : 10000,
	"Params.minSeq" : 1000,
	"Params.maxSeq" : 50000,
	"Params.minPar" : 10000,
	"Params.maxPar" : 400000,
	"Params.errorRate" : 0,
	#"Params.maxError" : 0
}

figure_4 = {
	"Params.numberOfJobs" : 250,
	#"numberOfNodes" : [[ (totalCompute/2)/(slowerR*100) if (x+1)/100 < slowerR else (totalCompute/2)/(100*(1-slowerR)) for x in range (100)]],
	"Params.numberOfNodes" : [275 if (x+1)/22 < 0.75 else 825 for x in range (22)],
	#"seqR" :  [ x/100 for x in range(50, 101, 8)],
	"Params.largeR" : 0.3,
	"Params.timespan" : 4000,
	"Params.minSeq" : 2000,
	"Params.maxSeq" : 100000,
	"Params.minPar" : 20000,
	"Params.maxPar" : 800000,
	"Params.errorRate" : 0
	#"maxError" : 0
}

figure_5 = {
	"Params.numberOfJobs" : 500,
	"Params.numberOfNodes" : [275 if (x+1)/100 < 0.75 else 825 for x in range (100)],
	#"Params.seqR" :  [ x/100 for x in range(50,101, 4)],
	"Params.largeR" : 0.3,
	"Params.timespan" : 2000,
	"Params.minSeq" : 2000,
	"Params.maxSeq" : 100000,
	"Params.minPar" : 20000,
	"Params.maxPar" : 800000,
	"Params.errorRate" : 0
	#"Params.maxError" : [0]
}
figure_6 = {
	"Params.numberOfJobs" : 250,
	#Params."numberOfNodes" : [[ (totalCompute/2)/(slowerR*100) if (x+1)/100 < slowerR else (totalCompute/2)/(100*(1-slowerR)) for x in range (100)]],
	"Params.numberOfNodes" : [275 if (x+1)/22 < 0.75 else 825 for x in range (22)],
	"Params.seqR" :  0.7,
	#"Params.largeR" : [x/100 for x in range(0, 101,2)],
	"Params.timespan" : 3500,
	"Params.minSeq" : 2000,
	"Params.maxSeq" : 100000,
	"Params.minPar" : 20000,
	"Params.maxPar" : 800000,
	"Params.errorRate" : 0
	#"Params.maxError" : [0]
}
figure_7 = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : [275 if (x+1)/22 < 0.75 else 825 for x in range (22)],
	"Params.seqR" :  0.7,
	"Params.largeR" : 0.3,
	#"Params.timespan" : [x for x in range (0,10000+1, 100)],
	"Params.minSeq" : 2000,
	"Params.maxSeq" : 100000,
	"Params.minPar" : 20000,
	"Params.maxPar" : 800000,
	"Params.errorRate" : 0
	#"Params.maxError" : [0]
}
figure_8 = {
	"Params.numberOfJobs" : 250,
	"Params.numberOfNodes" : [275 if (x+1)/22 < 0.75 else 825 for x in range (22)],
	"Params.seqR" :  0.7,
	"Params.largeR" : 0.3,
	"Params.timespan" : 4000,
	"Params.minSeq" : 2000,
	"Params.maxSeq" : 100000,
	"Params.minPar" : 20000,
	"Params.maxPar" : 800000,
	"Params.errorRate" : 1,
	#"Params.maxError" : [ [x/100 for x in range(0,501,20) ] ]
}
