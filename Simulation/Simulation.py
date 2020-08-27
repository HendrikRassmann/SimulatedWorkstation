#Testing TypeSistem FiFo :D
import random
import math
from typing import List, Optional, Callable, Tuple

class Node:
    def __init__(self, ID: int, speed: int=100)-> None:
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
        if len(self.nodesAvl) >= fPick.degreeOP:#job can be started
            #print(len(self.nodesAvl)) #immer 10 ?
            return fPick#start it
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

        #teilweise nur eine gap größer 1000 im ganzen run!
            #entweder: gap zu klein berechnet
            #parameter falsch (aber rest richtig => unwahrscheinlich)
        #print("qlen-filterL-gap(at least 1000)----------------------")
        #print(len(q))

'''
Es oist: j.processingT / (sum( map(sorted(self.nodesAvl), lambda j:j.speed)[0:j.degreeOfParallelism])
'''


        #es werden nicht genug gestartet(berechnung falsch?)
        filteredList: List[Job] = list(filter(lambda j: j.processingT <= time2runF - self.time ,q ) )#now fit
        #print(len(filteredList))
        if (time2runF - self.time >= 1000):
             print(time2runF - self.time)
        #filteredList: List[Job] = list(filter(lambda j:j.processingT <= (time2runF - self.time) ,q))
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
                    break #bug potential: what if multiple nodes get free at same time => more surplus than calculated! => OR

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
        finishedJobs: List[Job] = list(filter(lambda j : j.realCompletionT <= self.time, self.running)) #saves done jobs
        self.running = list(filter(lambda j : j.realCompletionT > self.time, self.running)) #removes done jobs
        for j in finishedJobs:
            self.nodesAvl += j.runningOn
            self.finished.append(j) #give nodes back
        #print ("jobs finished: %d" % len(finishedJobs)
            #self.finished = self.finished + finishedJobs #extra jobs?

    def jobsEnterQ(self):
        self.q +=  list(filter(lambda j : j.queueingT <= self.time, self.futureJobs))
        self.futureJobs = list(filter(lambda j : j.queueingT > self.time, self.futureJobs))

    def tick(self):
        nextQ: Optional[int] = None
        nextC: Optional[int] = None
        for j in self.futureJobs:
            if nextQ is None:
                nextQ = j.queueingT
            else:
                nextQ = min(nextQ, j.queueingT)

        for j in self.running:
            if nextQ is None:
                nextQ = j.realCompletionT
            else:
                nextQ = min(nextQ, j.realCompletionT)

        if nextQ is None and nextC is None:
            self.time += 1 #error state
        elif nextQ is None:
            self.time = nextC
        elif nextC is None:
            self.time = nextQ
        else:
            self.time = min (nextQ, nextC)

        #self.time += 1

    def scheduleNextJob(self)->bool:
        nextJob: Optional[Job] = self.scheduler(self,self.q)
        if nextJob is None or nextJob.degreeOP > len(self.nodesAvl):
            return False
        else:
            self.q.remove(nextJob)
            self.nodesAvl.sort(key=lambda n:n.speed,reverse = True)
            nextJob.startRunning = self.time
            nextJob.runningOn = self.nodesAvl[:nextJob.degreeOP]
            self.nodesAvl = self.nodesAvl[nextJob.degreeOP:]
            nextJob.completionT = self.time + round(nextJob.processingT / sum(map(lambda j:j.speed, nextJob.runningOn))) #nodespeed
            nextJob.realCompletionT = self.time + round(nextJob.realProcessingT / sum(map(lambda j:j.speed, nextJob.runningOn)))
            self.running.append(nextJob)
            return True

    def run(self)->List[Job]:

        assert (self.assertNodes == len(self.nodesAvl) + sum (map(lambda j: j.runningOn, self.running)))
        while self.q or self.futureJobs or self.running:

            self.finishJobs()
            self.jobsEnterQ()

            while self.scheduleNextJob():
                pass#this is dumb, but atom removes "useless" spaces while saving -> breakes the loop ;( -> pass)
            self.tick()
        assert len(self.finished) == self.assertNumberOfJobs
        return self.finished
