print("importing Job.py")
import simpy




class Job:

    def __init__(self,id,xTime,nrRessources):
        self.id = id
        self.expectedTime = xTime
        self.nrRessources = nrRessources
        self.enterQTime = -1
        self.startTime = -1
        self.endTime = -1
        
        
    
    def run(self):
        return self.expectedTime

    #def __repr__(self):
     #   return "a"

    def __repr__(self):
        return {'id':self.id
        ,'enterQ':self.enterQTime
        ,'startTime':self.startTime
        ,'endTime':self.endTime
        ,'nodes':self.nrRessources
        ,'expectedTime':self.expectedTime}
    def __str__(self):
        return '{id:'+str(self.id)\
        +',enterQ:'+str(self.enterQTime)\
        +',startTime:'+str(self.startTime)\
        +',endTime:'+str(self.endTime)\
        +',nodes:'+str(self.nrRessources)\
        +',expectedTime:'+str(self.expectedTime)+'}'