print("importing JobCreator.py")
import simpy
import Job


class JobCreator:

    def __init__(self,env,scheduler):
        self.timeBetween = 5
        self.env = env
        self.scheduler = scheduler

    def runCreator(self):
        while True:
            yield self.env.timeout(self.timeBetween)
            print("new job")
            newJob = Job.Job(self.env,3,2)
            self.scheduler.addJob(newJob)
            #self.scheduler.