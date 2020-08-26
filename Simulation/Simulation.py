#Testing TypeSistem FiFo :D
import random
import math
from typing import List, Optional, Callable, Tuple
from functools import partial, update_wrapper

def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func

class Node:
	def __init__(self, ID: int, speed: int=1)-> None:
		self.id = ID
		self.speed = speed
	def __str__(self):  # type: () -> str
		return "id: %d" % self.id

class Job:
	def __init__(self, id: int, queueingT : int, processingT: int, degreeOP: int, realProcessingT: int) -> None:
		self.id = id
		self.queueingT = queueingT
		self.processingT = processingT
		self.startRunning: Optional[int] = None
		self.completionT: Optional[int] = None
		self.realProcessingT: Optional[int] = realProcessingT
		self.realCompletionT: Optional[int] = None
		self.degreeOP = degreeOP
		self.runningOn: List[Node] = []


	#def schedule(self,)
	#print star,end,running on, also
	def __str__(self):  # type: () -> str
		return "id: %d, queueingT: %d, processingT: %d, degreeOP: %d, startRunning: %d, completionT: %d\n" % (self.id, self.queueingT,self.processingT, self.degreeOP, self.startRunning, self.completionT)


class System:

############
#Schedulers#
############
	def fit(self, f: Callable[[List[Job]],Optional[Job]], q:[List[Job]]  ) -> Optional[Job]:
		filteredList: List[Job] = list(filter(lambda j: j.degreeOP <= len(self.nodesAvl),q))
		return f(filteredList)
	#use (wrapped_partial (f,))(q)

	def backfilling (self, f: Callable[[List[Job]],Optional[Job] ],q: List[Job])  -> Optional[Job]:

		fPick: Optional[Job] = f(q)
		if fPick is None:
			return None #q empty
		if len(self.nodesAvl) >= fPick.degreeOP:
			return fPick
		else:
			nodesNeeded: int = fPick.degreeOP
			nodesFreeNow: int = len(self.nodesAvl)
			runningByCompletionTime = sorted(self.running, key =lambda j: j.completionT)
			time2runF: int = None
			for r in runningByCompletionTime:
				if (nodesFreeNow < nodesNeeded or r.completionT == time2runF):
					nodesFreeNow += r.degreeOP
					time2runF = r.completionT
				else:
					break #bug potential: what if multiple nodes get free at same time => more surplus than calculated!

			filteredList: List[Job] = list(filter(lambda j:j.processingT <= (time2runF - self.time),q))
			return f(filteredList)

	def optimisticBackfill (self, f: Callable[[List[Job]],Optional[Job] ],q: List[Job])  -> Optional[Job]:
		fPick: Optional[Job] = f(self,q)
		if fPick is None:
			return None #q empty
		if self.nodesAvl >= fPick.degreeOP:
			return fPick
		else:
			nodesNeeded: int = fPick.degreeOP
			nodesFreeNow: int = len(nodesAvl)
			runningByCompletionTime = sorted(self.running, key =lambda j: j.completionT)
			time2runF: int = None
			for r in runningByCompletionTime:
				if (nodesFreeNow < nodesNeeded or r.completionT == time2runF):
					nodesFreeNow += r.degreeOP
					time2runF = r.completionT
				else:
					break #bug potential: what if multiple nodes get free at same time => more surplus than calculated!

					#the second or claus makes it optimistic
			return f(filter(q, lambda j:j.processingT <= (time2runF - self.time) or j.degreeOP <= (nodesFreeNow - nodesNeeded)))

	#note: self is just spam
	#self is not necessary
	#but fit, fill expect self (state)
	#=> when calling a scheduler, it might expect self
	#would be nice, if you could check, wether or not function expects self, and only give if necessary
	def fifo(self,q: List[Job]) -> Optional[Job]:
		return min(q, key=lambda j: (j.queueingT, j.id)) if q else None

	def lpt(self,q: List[Job]) -> Optional[Job]:
		return max(q,key=lambda j: (j.processingT,j.id)) if q else None

	def spt(self,q: List[Job]) -> Optional[Job]:
		return min(q,key=lambda j: (j.processingT,j.id)) if q else None

	def random(sefl,q: List[Job]) -> Optional[Job]:
		return random.choice(q) if q else None
################higher Order
	def fifo_fit(self,q:List[Job]) -> Optional[Job]:
		return self.fit(self.fifo,q)

	def fifo_backfill(self,q:List[Job])->Optional[Job]:
		return self.backfilling(self.fifo,q)

	def lpt_fit(self,q:List[Job]) -> Optional[Job]:
		return self.fit(self.lpt,q)

	def lpt_backfill(self,q:List[Job])->Optional[Job]:
		return self.backfilling(self.lpt,q)

	def spt_fit(self,q:List[Job]) -> Optional[Job]:
		return self.fit(self.spt,q)

	def spt_backfill(self,q:List[Job])->Optional[Job]:
		return self.backfilling(self.spt,q)

	#dis nice, but name of function after workarround would be fit => fit of what?
	#fifo_fit: Callable[[List[Job]],Optional[Job]] = wrapped_partial(fit,fifo)
	#fifo_backfill: Callable[[List[Job]],Optional[Job]] = wrapped_partial(backfilling, fifo)





	def __init__(self,jobs: List[Job], nodesAvl: int, scheduler:\
	Callable[ [List[Job], List[Node], List[Job],int ], Optional[Tuple[Job, List[Node]]]  ] ) -> None:


		#online, finished list inside System or reference?

		#list nodes with name 0..n(odess)
		self.assertNodes = nodesAvl
		self.assertNumberOfJobs = len(jobs)
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
		finishedJobs: List[Job] = list(filter(lambda j : j.completionT <= self.time, self.running)) #saves done jobs
		self.running = list(filter(lambda j : j.completionT > self.time, self.running)) #removes done jobs
		for j in finishedJobs:
			self.nodesAvl += j.runningOn #give nodes back
		#print ("jobs finished: %d" % len(finishedJobs)
		self.finished = self.finished + finishedJobs #transfaire to finished list

	def jobsEnterQ(self):
		self.q +=  list(filter(lambda j : j.queueingT <= self.time, self.futureJobs))
		self.futureJobs = list(filter(lambda j : j.queueingT > self.time, self.futureJobs))

	def tick(self):
		self.time += 1

	def scheduleNextJob(self)->bool:
		nextJob: Optional[Job] = self.scheduler(self,self.q)
		if nextJob is None or nextJob.degreeOP > len(self.nodesAvl):
			return False
		else:
			self.q.remove(nextJob)
			#get free node
			self.nodesAvl.sort(key=lambda n:n.speed,reverse = True)
			nextJob.startRunning = self.time
			nextJob.runningOn = self.nodesAvl[:nextJob.degreeOP]
			self.nodesAvl = self.nodesAvl[nextJob.degreeOP:]
			nextJob.completionT = self.time + nextJob.processingT
			self.running.append(nextJob)#appends NoneType?

			return True

	def run(self)->List[Job]:

		assert (self.assertNodes == len(self.nodesAvl) + sum (map(lambda j: j.runningOn, self.running)))
		while self.q or self.futureJobs or self.running:

			self.finishJobs()
			self.jobsEnterQ()

			while self.scheduleNextJob():
				'''print(self.time)
				print ("q: %d", len(self.q))
				print ("nodesAvl: %d", len(self.nodesAvl))
				print ("running: %d", len(self.running))
				print ("finished: %d", len(self.finished))'''

			self.tick()
		assert len(self.finished) == self.assertNumberOfJobs
		return self.finished
'''
def backfillnodesAvling (q: List[Job], nodes: List[Node], running: List[Job], clock: int) -> Optional[Tuple[Job, List[Node]] ]:


	if not running: #nothing running ->fifo
		return fifo(q,nodes,running,clock)

	if not q or len(nodes) == 0:#noting to run (with) -> None
		return None

	fifoJob: Optional[Tuple[Job, List[Node]]] = fifo(q,nodes,running)

	if fifoJob is not None:
		return fifoJob
	else:
		#longestWaitingJob:
		nextJob: Job = min(q, key=lambda j: j.queueingT)

		nodesNeeded: int = nextJob.degreeOP
		#nodes currently free (and future free)
		nodesFreeNow: int = len(nodes)
		#when would fifo Job run next?
		time2runFifo: int = None
		#how many nodes will be left when wouldfifojob runs?
		surplus: int = None
		assert nodesFreeNow < nodesNeeded

		#sort running < by point in time, when they will be finished
		#can be used for "optimistic" backfilling
		#runningByNextDone: List[Job] = sorted(running, key=lambda j: j.startRunning + j.processingT) #sort copy by next to be finished
		#find point when there will be enough free nodes 2 run fifo job

		#pop only on non empty list
		for r in running:
			nodesFreeNow += r.degreeOP
			time2runFifo = r.startRunning + r.processingT - clock
			if (nodesFreeNow >= nodesNeeded):
				break

		surplus = nodesFreeNow - nodesNeeded

		return firstFit(list(filter(lambda j: j.processingT <= time2runFifo or j.degreeOP <= surplus,q)), nodes)

def fifo(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if len(q) > 0 and len(nodes) > 0:
		#min doesn't work with types :(
		firstEnterQ: Job = min(q, key=lambda j : j.queueingT)#smalles element

		if (firstEnterQ.degreeOP <= len(nodes) ):
			return (firstEnterQ, nodes[:firstEnterQ.degreeOP])

	return None

def firstFit(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if len(q) > 0 and len(nodes) > 0:
		#min doesn't work with types :(
		#only runnable Jobs
		runnableJobs: List[Job] = list( filter(lambda x: (x.degreeOP <= len(nodes)),q) )
		return fifo(runnableJobs, nodes)

	return None
#plz Test
def lpt(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if not q or not nodes: return None

	nextJob: Job = (max(q,key=lambda x: x.processingT))
	return (nextJob,nodes[:nextJob.degreeOP]) if nextJob.degreeOP <= len (nodes) else None

def spt(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	#nodes will be selected randomly
	if not q or not nodes: return None

	nextJob: Job = (min(q,key=lambda x: x.processingT))
	return (nextJob,nodes[:nextJob.degreeOP]) if nextJob.degreeOP <= len (nodes) else None

def rand(q: List[Job], nodes: List[Node], running: List[Job]=[], clock:int=None ) -> Optional[Tuple[Job, List[Node]]]:
	if not q or not nodes: return None
	nextJob: Job = random.choice(q)
	return (nextJob,nodes[:nextJob.degreeOP]) if nextJob.degreeOP <= len (nodes) else None

'''
'''
def scheduleNextJob(self) -> bool: #returns true if job was scheduled
	nextJob: Optional[Tuple[Job, List[Node]]] = self.scheduler(self.q, self.nodesAvl, self.running, self.time)
	if nextJob is None:
		return False
	else:
		#remove scheduled job
		self.q.remove(nextJob[0])
		nextJob[0].startRunning = self.time
		nextJob[0].runningOn = nextJob[1]
		nextJob[0].completionT = self.time + math.ceil(nextJob[0].processingT / sum(map(lambda j: j.speed, nextJob[1])))
		#print (nextJob[0].completionT)
		#remove now used nodes form avl
		for n in nextJob[1]:
			self.nodesAvl.remove(n)

		self.running.append(nextJob[0])


		return True
'''
