print("importing Job.py")
import simpy




class Job:

    def __init__(self,id,xTime,nrRessources):
        self.id = id
        self.expectedTime = xTime
        self.nrRessources = nrRessources
    
    def run(self):
        return self.expectedTime