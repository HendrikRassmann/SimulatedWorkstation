experiment = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [[275 if (x+1)/22 < 0.75 else 825 for x in range (22)]],
	"seqR" :  [ x/100 for x in range(0, 101, 5)],
	"largeR" : [0.3],
	"timespan" : [4000],
	"minSeq" : [2000],
	"maxSeq" : [100000],
	"minPar" : [20000],
	"maxPar" : [800000],
	"errorRate" : [0],
	"maxError" : [0],
        "schedulers" : ["fifo", "spt", "lpt","fifo_fit","fifo_backfill"],
        "x-axis" : ["seqR"]
    }

print ("experiment loaded")

