
import java

from com.artenum.spis.module.mesh import Node

#class nodeAdapter(com.artenum.spis.module.mesh.Node):
 
class nodeAdapter(Node):
        
     def __init__(self, nodeIn):
         self(nodeIn.Id, nodeIn.NodeId)
         self.node = nodeIn
         
         print "toto"
             
     def getNodeId(self):
          return (self.node.NodeId)
          
     def getCellOnNode(self):
          return (self.node.CellOnNode)
              
     def getEdgeOnNode(self):
          return (self.node.EdgeOnNode)           
          
             
     def getFaceOnNode(self):
          return (self.node.FaceOnNode)