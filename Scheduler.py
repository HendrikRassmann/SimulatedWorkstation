import simpy
import Ressources

class Scheduler:
   
    def __init__(self,env,nodes):
        print("Scheduler created")
        self.Q = []
        self.env = env
        self.nodes = nodes
        #locking RessourceManger
        #could be regular Mutex, but prob nicer to keep everything in simpy
        self.modifyNodes = simpy.Resource(env, capacity=1)

    def addJob(self,newJob):
        self.Q.append(newJob)

    def runJob(self,job,nodes):

        with self.modifyNodes.request() as req:
            yield req
            
            

            for x in nodes:
                x.inUse()
        




    def runScheduler(self):
        while True:
            yield self.env.timeout(1)           
            if self.Q:
                ##FiFo:
                #if Kann laufen:
                if self.Q[0].nrRessources <= len(self.nodes.getIdleNodes()):#make thread safe
                    print("list not empty, %d jobs" % len(self.Q))
                    self.Q.pop(0).run()
