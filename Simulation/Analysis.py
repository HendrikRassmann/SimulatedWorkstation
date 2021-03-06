import Simulation
import DBConnector

from typing import cast, List, Union, Optional, Callable, Tuple, Text, TypeVar, Generic, Type, Dict

import matplotlib.pyplot as plt
import numpy as np

from more_itertools import intersperse, pairwise
import itertools


startAt0 = False
min_data_points = 1

def show():
	fixed = figure_3

	sfXY = {}
	dbConnector = DBConnector.DBConnector()
	xAxis = "seqR"
	yAxis = "avgFlowTime"
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
		"fifo_optimistic",
		"fifo_backfill_lpt",
		"fifo_optimistic_lpt",
		#"lpt_backfill_fifo",
		#"lpt_optimistic_fifo"
		"fifo_backfill_spt"

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
				if (numberOfValues >= min_data_points):
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
		"lpt_backfill":"X",
		"lpt_backfill_fifo" : "o",
		"lpt_optimistic_fifo" : "o"

	}

	for sf in schedulers:
		lsf = list(map(list, zip(*sorted(sfXY[sf], key=lambda x:x[0]))))
		#print (lsf)
		xValues = lsf[0]
		yValues = lsf[1]
		print("Area under curve " + str(sf) + " : " + str(integral(xValues,yValues)))
		
		plt.plot(xValues,yValues,label= sf,marker=algoRep.get(sf, "."))
		plt.xlabel(xAxis)
		plt.ylabel(yAxis)
	if startAt0:
		plt.ylim(ymin=0)
	plt.legend()
	plt.show()



'''
#all methods static
#what the list has multiple runs with same config
results get plottet
'''

def integral(xVals: List[Union[float,int]],yVals: List[float])->float:
	#assume correlate, x is sorted low->hi
	#assume at least 2 xvalues
	#assume no two x values same
	beginnIntegral, endIntegral = xVals[0], xVals[-1]
	numberOfBars = len(xVals)-1
	bars = zip(xVals,yVals)
	area = sum(map(lambda pair: ( ((pair[0][1]+pair[1][1])/2) *abs(pair[0][0]-pair[1][0]) ),pairwise(bars) ) )
	return area


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

def complexityOfRun(jobs: List[Simulation.Job]) -> int:
	nodes = len(set(list(itertools.chain.from_iterable(list( map(lambda j:j.runningOn,jobs))))))
	return len(jobs) + len(list(filter(lambda j: j.queueingT != 0, jobs) )) + nodes

def run2String(jobs: List[Simulation.Job])->str:

	#assumption: complete Run
	#assumption: starts at 0 #whoops
	#assumption: 0 <= id < 10
	#assumption: ids unique
	firstQ: int = min(jobs,key=(lambda j:j.queueingT)).queueingT
	lastCompletion: int = max(jobs,key=(lambda j:j.realCompletionT)).realCompletionT

	#legende:
	#id,qtime,paral

	legend: string =  "queueintT, processingT, realProcessingT, degreeOfParallelism\n" + "".join(list(map(lambda j: "id: %d, qT: %d, pT: %d, rPT: %d, doP: %d\n" % (j.id, j.queueingT,j.processingT,j.realProcessingT, j.degreeOP ), list(sorted(jobs,key=lambda j: j.id)) )))

	#nodes: #QTimes später
	#make a dict of all the nodes running works
	#add a reduced form of all the jobs to that id
	#------------------------------start,end,id
	nodesInRun: Dict[int,List[Tuple[int,int,int]]] = {}
	for j in jobs:
		for n in j.runningOn:
			if n.id in nodesInRun:
				nodesInRun[n.id].append( (j.startRunning, j.realCompletionT, j.id) )
			else:
				nodesInRun[n.id]=[(j.startRunning, j.realCompletionT, j.id)]

	for l in nodesInRun:
		nodesInRun[l].sort(key=lambda x:x[0]) #sorted by start
	#store the strings for each node here:
	nodeStrings:Dict[int,str] = {}
	for l in nodesInRun:
		nodeStrings[l]=['-']*(lastCompletion)#how does last completion become float??

		for j in nodesInRun[l]:
			nodeStrings[l][j[0]:j[1]] = [str(j[2])]*(j[1]-j[0])
		nodeStrings[l] = ["[",str(l),"]",":"] + list(intersperse("|",nodeStrings[l], n=3 )) + ['\n']


	return legend + "".join(list(map(lambda x:"".join(x), list(sorted(nodeStrings.values())))))

def idleTime(jobs: List[Simulation.Job])->Optional[float]:
	if jobs is None:
		return None
	end: int = max(jobs, key=lambda j:j.realCompletionT).realCompletionT
	nodes: int = len(set(list(itertools.chain.from_iterable(list( map(lambda j:j.runningOn,jobs))))))
	potentialPT:int = end*nodes
	totalT = potentialPT

	for j in jobs:
		potentialPT -= (j.realCompletionT-j.startRunning)*j.degreeOP

	return potentialPT /  totalT


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
	"Params.errorRate" : 1
	#"Params.maxError" : [ [x/100 for x in range(0,501,20) ] ]
}
