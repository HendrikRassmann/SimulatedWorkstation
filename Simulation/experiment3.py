experiment = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [[100,100,100,100,100,100,100,100,100,100]],
	"seqR" :  [ x/100 for x in range(20,101, 4)],
	"largeR" : [0.3],
	"timespan" : [10000],
	"minSeq" : [1000],
	"maxSeq" : [50000],
	"minPar" : [10000],
	"maxPar" : [400000],
	"errorRate" : [0],
	"maxError" : [0],
        "schedulers" : ["fifo", "spt", "lpt","fifo_fit","fifo_backfill"],
        "x-axis" : ["seqR"]
    }

print ("experiment loaded")

