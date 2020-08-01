import Simulation
import DBConnector

from typing import cast, List, Union, Optional, Callable, Tuple, Text, TypeVar, Generic, Type, Dict

import matplotlib.pyplot as plt
import numpy as np

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
fixed = {
	"Params.numberOfNodes" : 20,
	"Params.seqR" : 0.5,
	"Params.largeR" : 1,
	"Params.timespan" : 0,
	"Params.minSeq" : 1000,
	"Params.maxSeq" : 1000,
	"Params.minPar" : 10,
	"Params.maxPar" : 100
}


def show():
	
	sfXY = {}
	dbConnector = DBConnector.DBConnector()
	xAxis = "numberOfJobs"
	yAxis = "makespan"
	schedulers = ["fifo","lpt","spt"]
	for sf in schedulers:
		sfXY[sf] = [] #pair of x,ys
		##x,y list für jeden scheduler
	print ("next: NewLine")
	print (sfXY["fifo"])
	docs = dbConnector.find(fixed)
	print ("not dead yead, plz b4 deleting")
	#nur ein doc?
	for item in docs:
		for sf in schedulers:
			xVaried = item["Params"][xAxis]
			values = item["Evals"].get(sf)
			if values is not None:
				numberOfValues = len(values)
				yAvg = sum(map (lambda x: x[yAxis], (item["Evals"][sf]) ) ) / numberOfValues
				sfXY[sf].append((xVaried,yAvg))
				print (xVaried,yAvg)
		print (item)
	
	

'''
#all methods static
#what the list has multiple runs with same config
results get plottet
'''


def makespan(jobs: List[Simulation.Job])->int:
	#how does this handle None? idk
	firstEnter: int = min(jobs, key=lambda j : j.enterQ).enterQ
	lastFinished: int = max(jobs, key=lambda j : j.endRunning).endRunning
	return lastFinished - firstEnter
	
def flowTime(jobs: List[Simulation.Job])->int:
	#how does this handle Nonde? idk
	return sum(map(lambda j: (j.endRunning - j.enterQ), jobs ) )
	
def avgFlowTime(jobs: List[Simulation.Job])->float:
	return flowTime(jobs) / len(jobs)
	
def maximumLateness(jobs: List[Simulation.Job]) ->int:
	return max(map(lambda j: j.startRunning - j.enterQ, jobs) )
	
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
	#print ("avg flowtime: %d", avgFlowTime(jobs))
	#print ("maximum lateness: %d", maximumLateness(jobs))
	return resultDict
#def conf2Dict()
	
	
