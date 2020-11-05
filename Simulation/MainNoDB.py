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
import json


xValueConverter = {
        "numberOfJobs":0,
        "numberOfNodes":1,
        "seqR":2,
        "largeR":3,
        "timespan":4,
        "minSeq":5,
        "maxSeq":6,
        "minPar":7,
        "maxPar":8
}
#from collections import defaultdict

def main(experiment):
        print ("Started Runs")
        start: float = timeit.default_timer()

        finishedRuns = []
        numberOfIterations = list(range(2))    

        byTarget = {
                "makespan":{},
                "avgFlowTime":{},
                "maximumLateness":{}
        }
        for target in byTarget:
                for sf in experiment["schedulers"]:
                        byTarget[target][sf]=[]
        
        product = itertools.product( *(list(experiment.values()))[:-2] )
        for conf in product:#itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):

                      
                for i in numberOfIterations:
                        jobs: List[Simulation.Job] = Generator.generate(*conf)
                        for sf in experiment["schedulers"]:
                                sys: Simulation.System = Simulation.System(jobs.copy(),conf[1],sf)
                                finished: List[Simulation.Job] = sys.run()
                                analysis = Analysis.standardAnalysis(finished)
                                for target in byTarget:
                                        byTarget[target][sf].append((conf[xValueConverter[experiment["x-axis"][0]]],analysis[target]))


        print (byTarget)
        '''dbCopy = {**bySchedulers}
        for targetFunktion in ["makespan","avgFlowTime","maxiumumLateness"]:
                #setup
                xLabel = experiment["x-axis"][0]
                yLabel = targetFunktion
                for sf in experiment["schedulers"]:
                        confs = dbCopy[sf]#confs : {(*conf):[{Analysis1},{Analysis} ]}
                        #avg out
                        #fetch and plot
                        xs = []
                        ys = []
                        for conf in confs:
                                xs.append()
                                acc = sum(map(lambda x : x[targetFunktion], confs[conf]))
                        confs'''

if __name__ == "__main__":
        if len (sys.argv) == 0:
                print ("run MainNoDB.py experiment1.py")
                sys.exit()
        if sys.argv[1].endswith(".py"):
                file_path = sys.argv[1]
                module_name = sys.argv[1][:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                main(module.experiment)
                #print (module.experiment)
                sys.exit()

        else:
                print ("run with argument halp for help")
                sys.exit()
