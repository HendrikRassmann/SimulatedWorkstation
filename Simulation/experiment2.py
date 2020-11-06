experiment = {
	"numberOfJobs" : [250],
	"numberOfNodes" : [[100,100,100,100,100,100,100,100,100,100]],
	"seqR" : [1],
	"largeR" : [0],
	"timespan" : list(range(0,10000+1, 500)),
	"minSeq" : [1000],
	"maxSeq" : [50000],
	"minPar" : [0],
	"maxPar" : [0],
	"errorRate" : [0],
        "maxError" : [0],
        "schedulers" : ["fifo", "spt", "lpt"],
        "x-axis" : ["timespan"]
    }

print ("experiment loaded")

