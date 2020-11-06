'''
python 3.6
'''

import sys

import Simulation
import Generator
import Analysis

import itertools
import functools
import operator

import timeit

import matplotlib.pyplot as plt
import numpy as np

import math

#importers
import importlib.util

#fakeDB
import csv
import os.path
from pathlib import Path


xValueConverter = {
        "numberOfJobs":0,
        "numberOfNodes":1,
        "seqR":2,
        "largeR":3,
        "timespan":4,
        "minSeq":5,
        "maxSeq":6,
        "minPar":7,
        "maxPar":8,
        "errorRate":9,
        "maxError":10
}
schedulerConverter = {
		"fifo" : Simulation.System.fifo,
		"spt" : Simulation.System.spt,
		"lpt" : Simulation.System.lpt,
		"fifo_fit" : Simulation.System.fifo_fit,
		"fifo_backfill" : Simulation.System.fifo_backfill,
		"fifo_optimistic" :Simulation.System.fifo_optimistic,
		"lpt_fit" : Simulation.System.lpt_fit,
		"lpt_backfill" :Simulation.System.lpt_backfill,
		"lpt_optimistic" : Simulation.System.lpt_optimistic,
		"spt_fit" :Simulation.System.spt_fit,
		"spt_backfill" :Simulation.System.spt_backfill,
		"spt_optimistic" : Simulation.System.spt_optimistic,
		"fifo_optimistic_lpt" : Simulation.System.fifo_optimistic_lpt,
		"fifo_backfill_lpt" : Simulation.System.fifo_backfill_lpt,
		"fifo_backfill_spt": Simulation.System.fifo_backfill_spt,
		"lpt_backfill_fifo": Simulation.System.lpt_backfill_fifo,
		"lpt_optimistic_fifo" : Simulation.System.lpt_optimistic_fifo	
	}
#from collections import defaultdict

def main(experiment,experimentName,n=1):
        
        print ("Started Runs")
        start: float = timeit.default_timer()

        finishedRuns = []
        numberOfIterations = list(range(n))    

        byTarget = {
                "makespan":{},
                "avgFlowTime":{},
                "maximumLateness":{}
        }
        for target in byTarget:
                for sf in experiment["schedulers"]:
                        byTarget[target][sf]=[]

        if Path(experimentName + ".csv").is_file():
                with open(experimentName + ".csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter = ";")
                        for row in reader:
                                byTarget[row[0]][row[1]].append((float(row[2]), float(row[3])))
                                #print(", ".join(row))
        
        product = itertools.product( *(list(experiment.values()))[:-2] )
        for conf in product:#itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):

                      
                for i in numberOfIterations:
                        jobs: List[Simulation.Job] = Generator.generate(*conf)
                        for sf in experiment["schedulers"]:
                                sys: Simulation.System = Simulation.System(jobs.copy(),conf[1],schedulerConverter[sf])
                                finished: List[Simulation.Job] = sys.run()
                                analysis = Analysis.standardAnalysis(finished)
                                for target in byTarget:
                                        byTarget[target][sf].append((conf[xValueConverter[experiment["x-axis"][0]]],analysis[target]))


        #print (byTarget)
        #sortieren nach x
        #dbCopy = {**bySchedulers}

        #save to file:
        with open(experimentName + ".csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=";")
                for target in byTarget:
                        for sf in byTarget[target]:
                                for valuePair in byTarget[target][sf]:
                                        writer.writerow([target]+[sf]+list(valuePair))
        
        fig, axs  = plt.subplots(3)
        i = 0
        for targetFunktion in ["makespan","avgFlowTime","maximumLateness"]:
                #setup
                xLabel = experiment["x-axis"][0]
                yLabel = targetFunktion

                for sf in byTarget[targetFunktion]:
                        xs = []
                        ys = []
                        pairs = sorted(byTarget[targetFunktion][sf],key=lambda x: x[0])
                        grouped= itertools.groupby(pairs,lambda x:x[0])
                        for key, group in grouped:
                                vals = list(group)
                                xs.append(key)
                                ys.append(sum(map(lambda x: x[1],vals))/len(vals) )

                        axs[i].plot(xs,ys,label=sf)
                axs[i].set_ylabel(targetFunktion)
                axs[i].set_ylim(ymin=0)
                axs[i].legend(bbox_to_anchor=(1.0,1),loc = "upper left",fontsize ="xx-small")
                i+=1
        
        plt.xlabel(experiment["x-axis"][0])
        plt.show()
                        

if __name__ == "__main__":
        if len (sys.argv) == 0:
                print ("run MainNoDB.py experiment1.py")
                sys.exit()
        if sys.argv[1].endswith(".py"):
                iterations = 5
                if len(sys.argv) > 2:
                        iterations = abs(int(sys.argv[2]))
                
                file_path = sys.argv[1]
                module_name = sys.argv[1][:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                main(module.experiment,module_name,iterations)
                #print (module.experiment)
                print(iterations)
                sys.exit()

        else:
                print ("run with argument halp for help")
                sys.exit()
