print("importing Ressources.py")
import simpy

class Node:
    inUse = False
    speed = 1
    def __init__(self,x):
        print("resource created")
        Node.speed = x

class Nodes:
    
    def __init__(self,nodeSpeed):
        self.nodes = []
        #map
        for x in nodeSpeed:
            self.nodes.append(Node(x))
            

    def getIdleNodes(self):
        return list(filter((lambda x : x.inUse),self.nodes))