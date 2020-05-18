import matplotlib.pyplot as plt
import simpy
import Job
import JobCreator
import Ressources
import Scheduler




print("Starting env")

env = simpy.Environment()

res = Ressources.RessourceManager([1,1,1,1,1])

scheduler = Scheduler.Scheduler(env,res)

jobCreator = JobCreator.JobCreator(env,scheduler) 

env.process(scheduler.runScheduler())

env.process(jobCreator.runCreator())

print("------------running---------------")

env.run(until=20)
print("time:")
print(env.now)