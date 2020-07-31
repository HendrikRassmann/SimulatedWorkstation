import pymongo
from pymongo import MongoClient

import sys, getopt

'''
client = MongoClient('localhost',27017)

database = client['pastRunns']
collection = database['run']

testdata = {"Params" :
	{
	"numberOfNodes" : 5,
	"numberOfJobs" : 100
	}
}

collection.insert_one(testdata)

client.close()
'''
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ("use -a <inputfile> -o <outputfile> for analysis")
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ('Input file is "', inputfile)
   print ('Output file is "', outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
