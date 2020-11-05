import Simulation

experiment = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [[100,100,100,100,100,100,100,100,100,100]],
	"seqR" : [1],
	"largeR" : [0],
	"timespan" : [0],
	"minSeq" : [1000],
	"maxSeq" : list(range(1000,10000+1, 1000)),
	"minPar" : [0],
	"maxPar" : [0],
	"errorRate" : [0],
        "maxError" : [0],
        "schedulers" : [Simulation.System.fifo, Simulation.System.spt,Simulation.System.lpt],
        "x-axis" : ["maxSeq"]
    }

print ("experiment loaded")

