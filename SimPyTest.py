import matplotlib.pyplot as plt
import numpy as np
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

env.run(until=200)
print("time:")
print(env.now)
print(*scheduler.completedJobs, sep = "\n")


print("----------analize------------------")
jobs =sorted(scheduler.completedJobs, key=lambda x: x.id, reverse=True)
ids = list(map(lambda x : x.id,jobs))
expectedTimes = list(map (lambda x : x.expectedTime, jobs))
timeInQ = list (map (lambda x : x.startTime - x.enterQTime, jobs))
nrOfNodes = list (map (lambda x : x.nrRessources, jobs))


plt.subplot(2,1,1)
plt.plot( ids,expectedTimes,'o-' )
plt.ylabel('expectedTimes of Job')
plt.plot( ids,nrOfNodes,label="nr of nodes")
plt.ylabel('expected Time in s\n nr of nodes used')


plt.subplot(2,1,2)
plt.plot( ids,timeInQ,'.-')
plt.ylabel('time waiting in Q')

plt.show()
#matplotlib stuff