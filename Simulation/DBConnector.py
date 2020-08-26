'''
TODO:
don't clear buffer, if update to db doesn't succeed
'''

import pymongo
from pymongo import MongoClient
import pprint

class DBConnector:
	def __init__(self):
		self.client = MongoClient('localhost',27017)
		self.database = self.client['pastRunns']
		self.collection = self.database['run1']

		self.itemBuffer = []

	def flush(self):
		print ("STAAAAAAAAAAAAART FLUSH")
		for item in self.itemBuffer:
			#print (item)
			for key in item.get("Evals"): #key == should be name of scheduler

				self.collection.find_one_and_update(
					{"Params" : item["Params"]},
					{'$push': {("Evals."+key) : item["Evals"][key]}	},
					upsert = True
				)

		#if no found => create (2DO?)
		#"".join(["Evals",])
		'''
			collection.find_one_and_update(
			{"Params" : item["Params"]},
			#{'$push': {"Evals" : item["Evals"]}	}
			upsert = True
			)'''
		self.itemBuffer.clear()


	def add(self, numberOfJobs, numberOfNodes, seqR, largeR, timespan,
minSeq, maxSeq ,minPar, maxPar, errorRate, maxError, evals, sf):
		dataPoint = {
		"Params": {
			"numberOfJobs": numberOfJobs,
			"numberOfNodes": numberOfNodes,
			"seqR": seqR,
			"largeR": largeR,
			"timespan": timespan,
			"minSeq" : minSeq,
			"maxSeq" : maxSeq,
			"minPar" : minPar,
			"maxPar": maxPar,
			"errorRate" : errorRate,
			"maxError" : maxError
			},
		"Evals": {
			sf.__name__ : evals
			}
		}
		self.itemBuffer.append(dataPoint)
		if len(self.itemBuffer) >= 100:
			self.flush()

	def find(self,params):
		return self.collection.find(params) #would be cool, if this would work with parameters not in dict form? Maybe

	def __del__(self):
		print ("deleting DBConnector")
		self.flush()
		self.client.close()
