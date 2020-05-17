print("importing Ressources.py")
import simpy

class Node:
    inUse = False
    speed = 1
    def __init__(self,x):
        print("resource created")
        Node.speed = x
    def use(self):
        self.inUse = True
    def release(self):
        self.inUse = False

class RessourceManager:
    
    def __init__(self,env,nodeSpeed):
        
        self.nodes = []
        #map
        for x in nodeSpeed:
            self.nodes.append(Node(x))
            

    def getIdleNodes(self):
        return list(filter((lambda x : x.inUse),self.nodes))