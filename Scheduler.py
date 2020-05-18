import simpy
import Ressources

class Scheduler:
   
    def __init__(self,env,nodes):
        self.log = []
        print("Scheduler created")
        self.waitingJobs = []
        self.completedJobs = []
        self.env = env
        self.nodes = nodes
        #locking RessourceManger
        #could be regular Mutex, but prob nicer to keep everything in simpy
        self.modifyNodes = simpy.Resource(env, capacity=1)

    def addJob(self,newJob):
        print("job added to Q at t: %d" % self.env.now)
        newJob.enterQTime = self.env.now
        self.waitingJobs.append(newJob)

    def runJob(self,job,nodes):

        

        print("running Job %d at t: %d" % (job.id,self.env.now))
        print("number of ressources assinged: %d" % len(nodes))

        with self.modifyNodes.request() as req:
            #modifie nodes
            yield req       
            for x in nodes:
                x.use()
        #run tse job
        job.startTime = self.env.now
        print("should yield for: %d" % job.run())
        yield self.env.timeout(job.run())
        #unUse Nodes
        job.endTime = self.env.now
        self.completedJobs.append(job)
        with self.modifyNodes.request() as req:
            yield req
            for x in nodes:
                x.release()

        print("Job %d finished at: %d" % (job.id,self.env.now))
    

    def runScheduler(self):
        while True:
            yield self.env.timeout(1)        
            if self.waitingJobs:
                ##FiFo:
                #if Kann laufen:
                print("Q size: %d, %d free resources" % (len(self.waitingJobs),len(self.nodes.getIdleNodes()) ) )
                with self.modifyNodes.request() as req:
                    yield req
                    if self.waitingJobs[0].nrRessources <= len(self.nodes.getIdleNodes()):#make thread safe
                        print("enough ressources!!!!!!")
                        jobToRun = self.waitingJobs.pop(0) 
                        self.env.process(self.runJob(jobToRun, self.nodes.getIdleNodes()[0:jobToRun.nrRessources]) )
                    else:
                        print("not enough ressources!!!!!!!!!!!!!!!")
