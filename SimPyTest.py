import simpy
import Job
import JobCreator
import Ressources
import Scheduler


ressources = [False,False,False,False]
q = []

print("Starting env")

env = simpy.Environment()

res = Ressources.Nodes([1,1,1,1,1])

scheduler = Scheduler.Scheduler(env,res)

jobCreator = JobCreator.JobCreator(env,scheduler) 

env.process(scheduler.runScheduler())

env.process(jobCreator.runCreator())

env.run(until=20)
print("time:")
print(env.now)