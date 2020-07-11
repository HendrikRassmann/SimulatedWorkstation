import Simulation

from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type

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
	
def standardAnalysis(jobs: List[Simulation.Job])->None:
	print ("Standard Analysis")
	print ("makespan: %d", makespan(jobs) )
	print ("flowtime: %d", flowTime(jobs) )
	print ("avg flowtime: %d", avgFlowTime(jobs))
	print ("maximum lateness: %d", maximumLateness(jobs))
	
