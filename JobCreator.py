print("importing JobCreator.py")
import simpy
import Job
import random

class JobCreator:

    def __init__(self,env,scheduler):
        self.jobID = 1
        self.timeBetween = 3
        self.env = env
        self.scheduler = scheduler

    def runCreator(self):
        while True:
            yield self.env.timeout(self.timeBetween)
            #print("new job")
            newJob = Job.Job(self.jobID,random.randint(1,10),random.randint(1,4))
            self.scheduler.addJob(newJob)
            self.jobID += 1