print("importing Ressources.py")
import simpy

class Node:
    inUse = False
    speed = 1
    def __init__(self,x):
        print("resource created")
        Node.speed = x
    def use(self):
        #print("using node")
        self.inUse = True
    def release(self):
        #print("releasing node")
        self.inUse = False

class RessourceManager:
    
    def __init__(self,nodeSpeed):
        
        self.nodes = []
        #map
        for x in nodeSpeed:
            self.nodes.append(Node(x))
            

    def getIdleNodes(self):
        return list(filter((lambda x : not x.inUse),self.nodes))