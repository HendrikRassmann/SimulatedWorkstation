import Simulation
import Generator
import Analysis

from typing import cast, List, Optional, Callable, Tuple, Text, TypeVar, Generic, Type

def main():
	
	
	jobList: List[Simulation.Job] = Generator.jobs100()
	
	print ("#jobs2do: %d", len(jobList))
	print("FIFI")
	sys: Simulation.System = Simulation.System(jobList.copy(),20,Simulation.fifo)
	finishedFifo: List[Job] = sys.run()
	Analysis.standardAnalysis(finishedFifo)
	
	print("firstFit")
	sys1: Simulation.System = Simulation.System(jobList.copy(),20,Simulation.firstFit)
	finishedFirstFit: List[Job] = sys1.run()	
	Analysis.standardAnalysis(finishedFirstFit)
	
	print("backfilling")
	sys2: Simulation.System = Simulation.System(jobList.copy(),20,Simulation.backfilling)
	finishedBackFilling: List[Job] = sys2.run()	
	Analysis.standardAnalysis(finishedBackFilling)
	################################
	#try different
	################################
	
if __name__ == "__main__":
	print("main...")
	main()
