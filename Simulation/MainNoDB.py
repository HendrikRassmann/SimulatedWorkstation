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

#from collections import defaultdict

def main(experiment):
        start: float = timeit.default_timer()
        finishedRuns = []
        numberOfIterations = list(range(1))
        product = itertools.product( *(list(experiment.values()))[:-1] )
        for conf in product:#itertools.product(numberOfJobs,numberOfNodes,seqR,largeR,timespan,minSeq,maxSeq,minPar,maxPar):

                for i in numberOfIterations:
                        jobs: List[Simulation.Job] = Generator.generate(*conf[:-1])
                        sys: Simulation.System = Simulation.System(jobs.copy(),conf[1],conf[-1])
                        finished: List[Simulation.Job] = sys.run()
                        finishedRuns.append(finished)
                        print (Analysis.standardAnalysis(finished))
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        
def show():
	pass
	#talk to db
	#plot what you want

if __name__ == "__main__":
        if len (sys.argv) == 0:
                print ("run MainNoDB.py experiment1.py")
                sys.exit()
        if sys.argv[1].endswith(".py"):
                file_path = sys.argv[1]
                module_name = sys.argv[1][:-3]
                #import experiment1
                #print ("testy")
                #print ("imported file :D")
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                main(module.experiment)
                #print (module.experiment)
                sys.exit()

        if sys.argv[1] == "show":
                Analysis.show()

        else:
                print ("run with argument halp for help")
                sys.exit()
