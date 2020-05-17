print("importing Job.py")
import simpy




class Job:

    def __init__(self,env,xTime,nrRessources):
        self.expectedTime = xTime
        self.env = env
        self.nrRessources = nrRessources
    
    def createProcess(self):
        print("job started at: %d, expected Time : %d" % (self.env.now, self.expectedTime) )
        yield self.env.timeout(self.expectedTime)
        print("job finished at: %d" % self.env.now)
    
    def run(self):
        print("run invoked")
        self.env.process( self.createProcess() )

    