#Testing TypeSistem FiFo :D

import functools
import random
from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type
print("starting")


class Node:
	def __init__(self, ID: int, speed: int=1)-> None:
		self.id = ID
		self.speed = speed
	def __str__(self):  # type: () -> str
		return "id: %d" % self.id
		
class Job:
	def __init__(self, id: int, enterQ : int, runtime: int, nodes2run: int) -> None:
		self.id = id
		self.enterQ = enterQ
		self.runtime = runtime
		self.startRunning: Optional[int] = -1
		self.endRunning: Optional[int] = -1
		self.nodes2run = nodes2run
		self.runningOn: List[Node] = []
		
	#print star,end,running on, also
	def __str__(self):  # type: () -> str
		return "id: %d, enterQ: %d, runtime: %d, nodes2run: %d, startRunning: %d, endRunning: %d\n" % (self.id, self.enterQ,self.runtime, self.nodes2run, self.startRunning, self.endRunning)

def backfilling (q: List[Job], nodes: List[Node], running: List[Job], clock: int) -> Optional[Tuple[Job, List[Node]] ]:

	#scheduling assumes all jobs are theoreticly runnable
	
	#edgecases:
	
	if not running: #nothing running ->fifo
		return fifo(q,nodes,running,clock)	
	if not q or len(nodes) == 0:#noting to run (with) -> None
		return None
	
	fifoJob: Optional[Tuple[Job, List[Node]]] = fifo(q,nodes,running)
	if fifoJob is not None:
		return fifoJob
	else:
		
		#longestWaitingJob:
		nextJob: Job = min(q, key=lambda j: j.enterQ)
		
		nodesNeeded: int = nextJob.nodes2run
		#nodes currently free (and future free)
		nodesFreeNow: int = len(nodes)
		#when would fifo Job run next?
		time2runFifo: int = None
		#how many nodes will be left when wouldfifojob runs?
		surplus: int = None
		assert nodesFreeNow < nodesNeeded
					
		#sort running < by point in time, when they will be finished
		runningByNextDone: List[Job] = sorted(running, key=lambda j: j.startRunning + j.runtime) #sort copy by next to be finished
		#find point when there will be enough free nodes 2 run fifo job
		
		#pop only on non empty list
		for r in running:
			nodesFreeNow += r.nodes2run
			time2runFifo = r.startRunning + r.runtime - clock
			if (nodesFreeNow >= nodesNeeded):
				break
		
		surplus = nodesFreeNow - nodesNeeded
			
		#while nodesFreeNow < nodesNeeded:
			#print ("ping")
			#if running
			#jobNextFinished: Job = running.pop(0) #popping schlägt fehl? pop von lehr?
			
			#nodesFreeNow += jobNextFinished.nodes2run
			#time2runFifo = jobNextFinished.startRunning + jobNextFinished.runtime - clock #how to get clock?~= remaining time
			#when this job finishes in time2runFifo seconds, there will be nodesFreeNow free nodes 
		
		
		
		#extra nodes, that backfill job might us
		#surplus = nodesFreeNow - nodesNeeded
		
		#get oldest waiting job, that doesn't change the startrunning of fifo job
		#either would be finished befor fifo job runs
		#or there would still be enough nodes, if this one runs
		return firstFit(list(filter(lambda j: j.runtime <= time2runFifo or j.nodes2run <= surplus,q)), nodes)

def fifo(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if len(q) > 0 and len(nodes) > 0:		
		#min doesn't work with types :(
		firstEnterQ: Job = min(q, key=lambda j : j.enterQ)#smalles element
		
		#firstEnterQ: Job = q[0]
		#for job in q:
		#	if job.enterQ < firstEnterQ.enterQ:
		#		firstEnterQ = job

		#assert isinstance(nodes, List[Node])
		if (firstEnterQ.nodes2run <= len(nodes) ):	
			return (firstEnterQ, nodes[:firstEnterQ.nodes2run])
			
	return None

def firstFit(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if len(q) > 0 and len(nodes) > 0:
		#min doesn't work with types :(
		#only runnable Jobs
		runnableJobs: List[Job] = list( filter(lambda x: (x.nodes2run <= len(nodes)),q) )
		return fifo(runnableJobs, nodes)
			
	return None
#plz Test
def lpt(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if not q or not nodes: return None

	nextJob: Job = (max(q,key=lambda x: x.runtime))
	return (nextJob,nodes[:nextJob.nodes2run]) if nextJob.nodes2run <= len (nodes) else None

def spt(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if not q or not nodes: return None
	
	nextJob: Job = (min(q,key=lambda x: x.runtime))
	return (nextJob,nodes[:nextJob.nodes2run]) if nextJob.nodes2run <= len (nodes) else None

def rand(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	if not q or not nodes: return None
	nextJob: Job = random.choice(q)
	return (nextJob,nodes[:nextJob.nodes2run]) if nextJob.nodes2run <= len (nodes) else None
	
class System:
	def __init__(self,jobs: List[Job], nodesAvl: int, scheduler:\
	Callable[ [List[Job], List[Node], List[Job],int ], Optional[Tuple[Job, List[Node]]]  ] ) -> None:
		
		
		#online, finished list inside System or reference?
		
		#list nodes with name 0..n(odess)
		self.time: int = 0
		self.nodesAvl: List[Node] = [] #("free nodes")
		for i in range(nodesAvl):
			self.nodesAvl.append(Node(i)) #all nodes speed 1 
		#scheduling function
		self.scheduler = scheduler
		#Job q
		self.futureJobs = jobs
		self.q :List[Job] = []
		self.running :List[Job] = []
		self.finished :List[Job] = []
		
	
	def finishJobs(self):
	#newly finished Jobs:
		finishedJobs: List[Job] = list(filter(lambda j : j.runtime + j.startRunning <= self.time, self.running)) #saves done jobs
		self.running = list(filter(lambda j : j.startRunning + j.runtime > self.time, self.running)) #removes done jobs
		for j in finishedJobs:
			j.endRunning = self.time #safe time
			self.nodesAvl += j.runningOn #give nodes back
		#print ("jobs finished: %d" % len(finishedJobs)
		self.finished = self.finished + finishedJobs #transfaire to finished list
		
	def jobsEnterQ(self):
		self.q =  self.q + list(filter(lambda j : j.enterQ <= self.time, self.futureJobs))
		self.futureJobs = list(filter(lambda j : j.enterQ > self.time, self.futureJobs))
				
	def tick(self):
		self.time += 1
		
	def scheduleNextJob(self) -> bool: #returns true if job was scheduled
		nextJob: Optional[Tuple[Job, List[Node]]] = self.scheduler(self.q, self.nodesAvl, self.running, self.time)
		if nextJob is None:
			return False
		else:
			#remove scheduled job
			self.q.remove(nextJob[0])
			nextJob[0].startRunning = self.time
			nextJob[0].runningOn = nextJob[1]	
			#remove now used nodes form avl
			for n in nextJob[1]:
				self.nodesAvl.remove(n)
			
			self.running.append(nextJob[0])
			#self.nodesAvl = cast(List[Node],list_diff(self.nodesAvl, nextJob[1]))
			#job to running
			#set start running time
			#use nodes
			return True
		
	def run(self)->List[Job]:
		while self.q or self.futureJobs or self.running:
		
			self.finishJobs()#doesn't work?
			self.jobsEnterQ()
			
			while self.scheduleNextJob():
				'''print(self.time)
				print ("q: %d", len(self.q))
				print ("nodesAvl: %d", len(self.nodesAvl))
				print ("running: %d", len(self.running))
				print ("finished: %d", len(self.finished))'''
			
			self.tick()
		return self.finished
