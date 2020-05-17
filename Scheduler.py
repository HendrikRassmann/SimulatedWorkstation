import simpy
import Ressources

class Scheduler:
   
    def __init__(self,env,nodes):
        print("Scheduler created")
        self.Q = []
        self.env = env
        self.nodes = nodes

    def addJob(self,newJob):
        self.Q.append(newJob)

    def runScheduler(self):
        while True:
            yield self.env.timeout(1)           
            if self.Q:
                ##FiFo:
                if self.Q[0].nrRessources > len(self.nodes.getIdleNodes()):
                    print("list not empty, %d jobs" % len(self.Q))
                    self.Q.pop(0).run()
