"""
**File name:**    dedouble.py

**Creation:**     2004/07/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.1.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 3.1.0   | Arsene Lupin                         | Modif                      |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+

PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

import sys
import math
import copy
import Bin.Tasks.shared

from Bin.Tasks.shared                         import shared
from Bin.Tasks.shared                         import sharedGroups
from Bin.Tasks.shared                         import sharedData
from Bin.Tasks.shared                         import sharedSplitElm

from Modules.Groups.MeshGroup        import MeshGroup
from Modules.Groups.GeoGroup         import GeoGroup
from Modules.Meshing.MeshElement     import MeshElement
from Modules.Meshing.SkeletonElement import SkeletonElement
from Modules.Meshing.Node            import Node
from Modules.Meshing.Edge            import Edge
from Modules.Meshing.Face            import Face
from Modules.Meshing.NodeList        import NodeList
from Modules.Field.DataField         import DataField
from Modules.Field.MeshField         import MeshField
from Modules.Field.MeshFieldList     import MeshFieldList
from Modules.Field.DataFieldList     import DataFieldList


from Modules.Utils.CorresTable       import CorresTable

try: 
    from Modules.PostProcessing.Include.vtkGridBuilder import vtkGridBuilder
except:
    print "Error in MeshSplitter: Impossible to load VTK modules."

from Bin.config import GL_DATA_PATH

class MeshSplitter:

     def __init__(self):
         print "initialisation of the mesh splitter"
                
         ### Creation of correspondance lists

         # global correspondance table
         self.skelCorTab = CorresTable()
         self.skelCorTab.setElmList(shared['MeshElmtList'][2].List)
         
         self.nodeCorTab = CorresTable()
         self.nodeCorTab.setElmList(shared['MeshElmtList'][0].List)
         
         self.edgeCorTab = CorresTable()
         self.edgeCorTab.setElmList(shared['MeshElmtList'][1].List)
         
         self.faceCorTab = CorresTable()
         self.faceCorTab.setElmList(shared['MeshElmtList'][2].List)
         
         
         # correspondance table for the surface S
         self.edgeOnSCorTab = CorresTable()
         self.edgeOnSCorTab.setElmList(shared['MeshElmtList'][1].List)
         
         self.faceOnSCorTab = CorresTable()
         self.faceOnSCorTab.setElmList(shared['MeshElmtList'][2].List)
         
         # correspondance table for the border B
         self.skelOnBCorTab = CorresTable()
         self.skelOnBCorTab.setElmList(shared['MeshElmtList'][1].List)
         
         
         # correspondance table for the cracking border K
         self.nodeCorOnKTab = CorresTable()
         self.nodeCorOnKTab.setElmList(shared['MeshElmtList'][0].List)
         
         self.edgeCorOnKTab = CorresTable()
         self.edgeCorOnKTab.setElmList(shared['MeshElmtList'][1].List)
         
         self.faceCorOnKTab = CorresTable()
         self.faceCorOnKTab.setElmList(shared['MeshElmtList'][2].List)           
     
     
            
     def CrackMeshGrp(self, oldGrpId, kBorderGrpId, inflate):
         print oldGrpId, kBorderGrpId, inflate
      
         print "#########################"
         print "Group to be duplicated"
         print "#########################"      
         indexGrp = shared['MeshGroupList'].IdList.index(oldGrpId)
         print "index grp = ", indexGrp
         
         indexKGrp = shared['MeshGroupList'].IdList.index(kBorderGrpId)
         print "index K grp = ", indexKGrp
      
         lenSkElList = len(shared['SkeletonElmtList'].List)
         print "length of skeleton elm list= ", lenSkElList
      
         print "#########################"
         print "Building of new geo and mesh group"
         print "#########################"
         newGrpId = -1
         for grpId in shared['MeshGroupList'].IdList:
             if grpId > newGrpId:
                newGrpId = grpId
         newGrpId = newGrpId + 1
      
         newGeoGrp = GeoGroup()
         newGeoGrp.Id = newGrpId
         newGeoGrp.Name = "new face ( Side B )"
         newGeoGrp.Type = "SURFACE GROUP"
         newGeoGrp.IsDuplicated = 1 # is duplicated
         sharedGroups['GeoGroupList'].Add_Group(newGeoGrp)

         # new MeshGroup building
         newMeshGrp = MeshGroup()
         newMeshGrp.Id = newGrpId
         newMeshGrp.Name = "new face group ( Side B )"
         newMeshGrp.Type = "SURFACE GROUP"
         shared['MeshGroupList'].Add_Group(newMeshGrp)
         newGrpId = newGrpId + 1
         
         
         # for the border
         newGeoGrpForB = GeoGroup()
         newGeoGrpForB.Id = newGrpId
         newGeoGrpForB.Name = "new border ( Side B)"
         newGeoGrpForB.Type = "CURVE GROUP"
         newGeoGrpForB.IsDuplicated = 1 # is duplicated
         sharedGroups['GeoGroupList'].Add_Group(newGeoGrpForB)
      
         # new MeshGroup building
         newMeshGrpForB = MeshGroup()
         newMeshGrpForB.Id = newGrpId
         newMeshGrpForB.Name = "New border ( Side B )"
         newMeshGrpForB.Type = "CURVE GROUP"
         shared['MeshGroupList'].Add_Group(newMeshGrpForB)
 
         ####################################################################
         ##                 Building of cracking border                  ####
         ####################################################################
         print "BUILDING OF THE SPLITTING BORDER"
         self.borderNodeList = []
         self.borderEdgeList = []
         self.surfEdgeList = []
         surfFaceList = []
         surfNodeList = []
         
         for borderSkel in shared['MeshGroupList'].List[indexKGrp].SkeletonElementList.List:
             for node in borderSkel.SkeletonNodeList.List:
                 if node not in self.borderNodeList:
                    self.borderNodeList.append(node)
         print "step 1"
         
         for borderSkel in shared['MeshGroupList'].List[indexKGrp].SkeletonElementList.List:
             for edge in borderSkel.SkeletonEdgeList.List:
                 if (edge not in self.borderEdgeList):
                    self.borderEdgeList.append(edge)
         print "step 2"
         
         for surfSkel in shared['MeshGroupList'].List[indexGrp].SkeletonElementList.List:
             for edge in surfSkel.SkeletonEdgeList.List:
                 if (edge not in self.surfEdgeList):
                     self.surfEdgeList.append(edge)
             
             for face in surfSkel.SkeletonFaceList.List:
                 if (face not in surfFaceList):
                    surfFaceList.append(face)
                    
             for node in surfSkel.SkeletonNodeList.List:
                 if (node not in surfNodeList):
                    surfNodeList.append(node)
         
         print "computation of local normals"
         tmpList = []
         for skelm in shared['MeshGroupList'].List[indexGrp].SkeletonElementList.List:
             tmpList.append(skelm.SkeletonMeshElement)
         
         
         localNormalIndexList = []
         localNormalList = []
         for node in surfNodeList:
             localNormalIndexList.append(node)
             localNormalList.append(self.GetLocalNormale(node, tmpList))

         
         print "Detection of up/down cells"
         # Detection of up-down cells
         self.downCellList = []
         self.upCellList = []
         self.downFaceList = []
         self.upFaceList = []
         
         for node in surfNodeList:
             for cellId in node.CellOnNode:
                 cell = shared['MeshElmtList'][3].GetElementById(cellId)

                 localNormal = localNormalList[localNormalIndexList.index(node)]
                 
                 if self.UpDownTest(node, localNormal, cell.GetIsoBaryCenter()) < 0.0:
                     #print "Cell Id", cell.Id, "normal", localNormal, "bary", cell.GetIsoBaryCenter(), "test", self.UpDownTest(node, localNormal, cell.GetIsoBaryCenter())
                     if cell not in self.downCellList:
                         self.downCellList.append(cell)
                         for face in cell.Connection:
                             if (face not in self.downFaceList and face not in surfFaceList):
                                 self.downFaceList.append(face)
                 else: 
                     if cell not in self.upCellList:
                         self.upCellList.append(cell)
                         for face in cell.Connection:
                             if (face not in self.upFaceList and face not in surfFaceList):
                                 self.upFaceList.append(face)
 
         
         print "Building of the cracking border K"
         #### For the surfaces #####
         
         # List of additionnal faces to be splitted due to the cracking
         self.crackingBorderFaceList = []
         for node in self.borderNodeList:
             for faceId in node.FaceOnNode:
                 face = shared['MeshElmtList'][2].GetElementById(faceId)
                 
                 #For each edge we check if this edge is between an Up and a Down face. 
                 upFlag = 0
                 downFlag = 0
                 for cellId in face.CellOnFace:
                     cellOnEdge = shared['MeshElmtList'][3].GetElementById(cellId)
                     
                     # detection if the face is on the up-side of edges
                     localNormal = localNormalList[localNormalIndexList.index(node)]
                     if self.UpDownTest(node, localNormal, cellOnEdge.GetIsoBaryCenter()) < 0.0:
                        downFlag = -1
                     else:
                        upFlag = 1
                 
                 if (downFlag*upFlag) < 0 : 
                     if (     face not in self.crackingBorderFaceList 
                          and face not in surfFaceList): 
                         self.crackingBorderFaceList.append(face)
                         if face in self.downFaceList:
                             self.downFaceList.remove(face)
                         if face in self.upFaceList:
                             self.upFaceList.remove(face)
                 
            
         #### FOR the edges
         # List of additionnal edges to be splitted due to the cracking
         self.crackingBorderEdgeList = []
         for face in self.crackingBorderFaceList:
             for edge in face.Connection:
                 if ( edge not in self.crackingBorderEdgeList and edge not in self.surfEdgeList):
                    self.crackingBorderEdgeList.append(edge)
 
         crackingBorderNodeList = []           
         for face in self.crackingBorderFaceList:
             for node in face.MeshElementNodeList:
                 crackingBorderNodeList.append(node.Id)
         
         
         #############################################################################
         ####                  Duplication of elements ON the surface             ####
         #############################################################################
         print 
         print "########## Duplication of skeleton elements #######"
      
         # here we duplicate the skeletons and add them at the end of the list of skeletons
         #shift = lenSkElList
         #count = shift + 1
         
         # looking for last Id
         print "Looking for the last Ids"
         #meshElmId = -1
         #for face in shared['MeshElmtList'][2].List:
         #    if face.Id != shared['MeshElmtList'][2].IdList[shared['MeshElmtList'][2].List.index(face)]:
         #        print "Warning : face Id mismatching!"
         #    if face.Id > meshElmId:
         #        meshElmId = face.Id
         #meshElmId = 1 + meshElmId     #len(shared['MeshElmtList'][2].List) 
                  
         meshFaceId = -1
         FaceId = -1
         for face in shared['MeshElmtList'][2].List:
             #if face.Id != shared['MeshElmtList'][2].IdList[shared['MeshElmtList'][2].List.index(face)]:
             #    print "Warning : face Id mismatching!"
             if face.Id > meshFaceId:
                meshFaceId = face.Id
             if face.FaceId > FaceId:
                FaceId = face.FaceId
         meshFaceId = meshFaceId + 1
         print "Last Id for mesh element of type face is :",  meshFaceId
         
         meshEdgeId = -1
         for edge in shared['MeshElmtList'][1].List:
             #if edge.Id != shared['MeshElmtList'][1].IdList[shared['MeshElmtList'][1].List.index(edge)]:
             #    print "Warning : edge Id mismatching!"
             if edge.Id > meshEdgeId:
                meshEdgeId = edge.Id
         meshEdgeId = meshEdgeId + 1
         print "Last Id for mesh element of type edge is :",  meshEdgeId
         
         meshNodeId = -1
         for node in shared['MeshElmtList'][0].List:
             #if node.Id != shared['MeshElmtList'][1].IdList[shared['MeshElmtList'][1].List.index(node)]:
             #    print "Warning : node Id mismatching!"
             if node.Id > meshNodeId:
                meshNodeId = node.Id
         meshNodeId = meshNodeId + 1
         print "Last Id for mesh element of type node is :",  meshNodeId
         
         seklElmId = -1
         for skel in shared["SkeletonElmtList"].List:
             #if skel.Id != shared["SkeletonElmtList"].IdList[shared["SkeletonElmtList"].List.index(skel)]:
             #    print "Warning : skel Id mismatching!"
             if skel.Id > seklElmId:
                 seklElmId = skel.Id
         seklElmId = 1 + seklElmId
         print "Last Id for skel elements of type node is:",  seklElmId
         
         
         correspondanceTable = []
         # we scan all skeletons element of the original group and duplicate them
         for skelm in shared['MeshGroupList'].List[indexGrp].SkeletonElementList.List:
             
             newSkElm = SkeletonElement( seklElmId, skelm.Type, NodeList())

             newSkElm.GeoGroup = newGeoGrp           # on attribut au nouveau group
             newSkElm.GeoElement = skelm.GeoElement  #mais on garde la ref a l object de geo
             newSkElm.NodeNumber = skelm.NodeNumber
             newSkElm.Comments = "Duplicated skel"
             
             
             #we add the new skeleton element to the list of the new MeshGrp
             newMeshGrp.SkeletonElementList.Add_Element(newSkElm)
             
             # we add the corresponding mesh element, in the presente case a FACE
             newSkeletonMeshElement = Face(meshFaceId, FaceId, 'TRIANGLE')
             FaceId = FaceId + 1
             meshFaceId = meshFaceId + 1
             
             newSkElm.SkeletonMeshElement = newSkeletonMeshElement
             if newSkElm.Id not in newSkeletonMeshElement.SkeletonId:
                 newSkeletonMeshElement.SkeletonId.append(newSkElm.Id)
             
             shared['MeshElmtList'][2].List.append(newSkeletonMeshElement)
             shared['MeshElmtList'][2].IdList.append(newSkeletonMeshElement.Id)
             shared['MeshElmtList'][2].NbFace = len(shared['MeshElmtList'][2].List)
             
             self.skelCorTab.addCoupleByElm( skelm.SkeletonMeshElement, newSkeletonMeshElement)
             self.faceCorTab.addCoupleByElm( skelm.SkeletonMeshElement, newSkeletonMeshElement)
             self.faceOnSCorTab.addCoupleByElm( skelm.SkeletonMeshElement, newSkeletonMeshElement)
           
             #we add the element to the common and shared Skeleton Elemt list
             shared['SkeletonElmtList'].Add_Element(newSkElm)
             newSkElm.SkeletonFaceList.Add_Face(newSkeletonMeshElement) #i.e itself
             correspondanceTable.append( ( shared['SkeletonElmtList'].List.index(skelm), 
                                           shared['SkeletonElmtList'].List.index(newSkElm)) )
             seklElmId = seklElmId + 1
         # until now, the faces are only declared. The corresponding nodes are not built.
         
         
         #############################################################
         #                  Nodes duplication                        #
         #############################################################
         
         print "Duplication of nodes on S surface"
         #newId = shared['MeshElmtList'][0].List[len(shared['MeshElmtList'][0].List)-1].Id + 1
         newNodeId = shared['MeshElmtList'][0].List[len(shared['MeshElmtList'][0].List)-1].NodeId + 1
         
         
         indexSkel = 0
         for couple in correspondanceTable:
             skelm = shared['SkeletonElmtList'].List[couple[0]]
             newSkElm = shared['SkeletonElmtList'].List[couple[1]]
      
             for node in skelm.SkeletonNodeList.List:        
                 indexOldNode = shared['MeshElmtList'][0].List.index(node)
                 
                 
                 tmpList = []
                 for indexFace in self.faceOnSCorTab.duplicatedElmList:
                     tmpList.append(shared['MeshElmtList'][2].List[indexFace])
         
                 if ( indexOldNode in self.nodeCorTab.duplicatedElmList):
                     newNode = self.nodeCorTab.getNewElmByIndex(indexOldNode)
                     newSkElm.SkeletonNodeList.Add_Node(newNode)
                     newSkElm.SkeletonMeshElement.MeshElementNodeList.append(newNode)
                 else:
                     newNode = Node()
      
                     newNode.Id = meshNodeId
                     meshNodeId = meshNodeId + 1
                     newNode.NodeId =  newNodeId
                     newNodeId = newNodeId + 1
                     newNode.ElmtNum = 1010  #FIX ME
      
                     newNode.Coord = [node.Coord[0], node.Coord[1], node.Coord[2]]
      
                     shared['MeshElmtList'][0].List.append(newNode)
                     shared['MeshElmtList'][0].IdList.append(newNode.Id)
                     shared['MeshElmtList'][0].NbNode = len(shared['MeshElmtList'][0].List)
                     newSkElm.SkeletonNodeList.Add_Node(newNode)
 
                     self.nodeCorTab.addCoupleByIndex( indexOldNode, shared['MeshElmtList'][0].List.index(newNode))
              
                     # now, we must add this node the SkeletonMeshElement, i.e. the face
                     newSkElm.SkeletonMeshElement.MeshElementNodeList.append(newNode)
         
         
 
         #############################################################
         #               Edges duplication                           #
         # Here we duplicate edges included into the skel, i.e in    #
         # the surface to be duplicated                              #
         #############################################################           
         
         sys.stdout.write("Duplication of edges on S: ")
         #newId = shared['MeshElmtList'][1].List[len(shared['MeshElmtList'][1].List)-1].Id + 1
         newEdgeId = shared['MeshElmtList'][1].List[len(shared['MeshElmtList'][1].List)-1].EdgeId + 1
         
         
         for couple in correspondanceTable:
             skelm = shared['SkeletonElmtList'].List[couple[0]]
             newSkElm = shared['SkeletonElmtList'].List[couple[1]]
 
             for edge in skelm.SkeletonEdgeList.List:
      
                 indexOldEdge = shared['MeshElmtList'][1].List.index(edge)
      
                 if ( indexOldEdge in self.edgeCorTab.duplicatedElmList):
                     sys.stdout.write(".")
                 else:
                     sys.stdout.write("+")
                     # we create a new edge 
                     newEdge = Edge()
                     newEdge.Id = meshEdgeId
                     meshEdgeId = meshEdgeId + 1
                     newEdge.EdgeId = newEdgeId
                     newEdgeId = newEdgeId + 1
      
                     newEdge.ElmtNum = 2010 #FIX ME
      
                     # we link the corresponding duplicated start node
                     #indexNewNode = self.nodeCorTab.getNewElmIndex(edge.StartNode)
                     #newEdge.StartNode = shared['MeshElmtList'][0].List[indexNewNode]
                     newNode = self.nodeCorTab.getNewElm(edge.StartNode)
                     newEdge.StartNode = newNode
                     
                     newEdge.StartNode.EdgeOnNode.append(newEdge.Id)
                     #newEdge.MeshElementNodeList.append(shared['MeshElmtList'][0].List[indexNewNode])
                     newEdge.MeshElementNodeList.append(newNode)
      
                     # idem for end node
                     #indexNewNode = self.nodeCorTab.getNewElmIndex(edge.EndNode)
                     #newEdge.EndNode = shared['MeshElmtList'][0].List[indexNewNode]
                     newNode = self.nodeCorTab.getNewElm(edge.EndNode)
                     newEdge.EndNode = newNode
                     newEdge.EndNode.EdgeOnNode.append(newEdge.Id)
                     #newEdge.MeshElementNodeList.append(shared['MeshElmtList'][0].List[indexNewNode])
                     newEdge.MeshElementNodeList.append(newNode)
                     
                     shared['MeshElmtList'][1].List.append(newEdge)
                     shared['MeshElmtList'][1].IdList.append(newEdge.Id)
                     shared['MeshElmtList'][1].NbEdge = len(shared['MeshElmtList'][1].List)
                     
                     newSkElm.SkeletonEdgeList.Add_Edge(newEdge)
                     
                     # Lists of old to new edges for already duplicated edges
                     self.edgeCorTab.addCoupleByIndex(indexOldEdge, shared['MeshElmtList'][1].List.index(newEdge))
                     self.edgeOnSCorTab.addCoupleByIndex(indexOldEdge, shared['MeshElmtList'][1].List.index(newEdge))
      
                        
         # now, we must add  this node the SkeletonMeshElement
         for oldFaceIndex in self.faceCorTab.duplicatedElmList:
             oldFace = shared['MeshElmtList'][2].List[oldFaceIndex]
             newFace = self.faceCorTab.getNewElmByIndex(oldFaceIndex)
             for oldEdge in oldFace.Connection:
                 newEdge = self.edgeCorTab.getNewElm(oldEdge)
                 newFace.Connection.append(newEdge)
         print " "            
                     
                     
         print "########## Duplication of skeleton elements on the B border #######"
         # we scan all skeletons element of the original group and duplicate them         
         print "Group",  indexKGrp
         for skelm in shared['MeshGroupList'].List[indexKGrp].SkeletonElementList.List:
             
             newSkElm = SkeletonElement( seklElmId, skelm.Type, NodeList())
             newSkElm.GeoGroup = newGeoGrpForB       # on attribut au nouveau group
             newSkElm.GeoElement = skelm.GeoElement  #mais on garde la ref a l object de geo
             newSkElm.NodeNumber = skelm.NodeNumber
             newSkElm.Comments = "Duplicated skel on the b border"
             
             # we add the corresponding mesh element, in the presente case a LINE
             for edge in skelm.SkeletonEdgeList.List:
                 newSkElm.SkeletonEdgeList.Add_Edge(self.edgeOnSCorTab.getNewElm(edge))
                  
             for node in skelm.SkeletonNodeList.List:
                 newSkElm.SkeletonNodeList.Add_Node(self.nodeCorTab.getNewElm(node))
                  
             newSkElm.SkeletonMeshElement = self.edgeOnSCorTab.getNewElm(skelm.SkeletonMeshElement)
             print skelm.SkeletonMeshElement
             
             #we add the new skeleton element to the list of the new MeshGrp
             newMeshGrpForB.SkeletonElementList.Add_Element(newSkElm)
             
             #we add the element to the common and shared Skeleton Elemt list
             shared['SkeletonElmtList'].Add_Element(newSkElm)
             seklElmId = seklElmId + 1
        
        
        
        
        #-------------------------------------------------------------------------#
        
        
        
        
         #########################################################
         ####   Duplication of elements on the cracking border    
         #########################################################
         print "Duplication of elements of the cracking border K"
                     
         ################################################
         ### Management of edges on the cracking border
         ################################################
         sys.stdout.write("Duplication of edges of K: ")
         self.kBorderEdgeSideB = []
         for edge in self.crackingBorderEdgeList:
             #in this case we must really duplicate the edge and create a new one
                               
             indexOldEdge = shared['MeshElmtList'][1].List.index(edge)
             #we choose one node
             startNode = edge.StartNode
                               
             if ( indexOldEdge in self.edgeCorTab.duplicatedElmList):   # VERIFIER SI TEST NECESSAIRE
                 sys.stdout.write(".")
                 print "Edge already duplicated in cracking border list"
             else:
                 sys.stdout.write("+")
                 # we create a new edge 
                 newEdge = Edge()
                 newEdge.Id = meshEdgeId
                 meshEdgeId = meshEdgeId + 1
 
                 newEdge.EdgeId = newEdgeId
                 newEdgeId = newEdgeId + 1
      
                 newEdge.ElmtNum = 5010 #FIX ME
 
                 # we link the corresponding duplicated start and end node
                 # being on the border
                 
                 # apparently can miss some nodes on the border if Gmsh makes 
                 # error in the skeleton attribution
                 if (startNode in surfNodeList):
 
                    # we split the start node
                    newEdge.StartNode = self.nodeCorTab.getNewElm(edge.StartNode)
                    newEdge.StartNode.EdgeOnNode.append(newEdge.Id)
                    newEdge.MeshElementNodeList.append(newEdge.StartNode)
                                                       
                    # and keep the end one
                    newEdge.EndNode = edge.EndNode
                    newEdge.MeshElementNodeList.append(newEdge.EndNode)
                    
                    shared['MeshElmtList'][1].List.append(newEdge)
                    shared['MeshElmtList'][1].IdList.append(newEdge.Id)
                    shared['MeshElmtList'][1].NbEdge = len(shared['MeshElmtList'][1].List)
                    
                    #TO DO : TBC
                    self.edgeCorOnKTab.addCoupleByIndex(indexOldEdge, shared['MeshElmtList'][1].List.index(newEdge))

                    
                    #FIX ME : pb de groupe
                 elif (edge.EndNode in self.borderNodeList):    #because some of the cracking edge have no node on the border
                      #we split the end node                                 
                      newEdge.EndNode = self.nodeCorTab.getNewElm(edge.EndNode)
                      newEdge.EndNode.EdgeOnNode.append(newEdge.Id)
                      newEdge.MeshElementNodeList.append(newEdge.EndNode)
                                 
                      #and keep the start one
                      newEdge.StartNode = edge.StartNode
                      newEdge.MeshElementNodeList.append(newEdge.StartNode)
                   
                      shared['MeshElmtList'][1].Add_Edge(newEdge)
                      self.edgeCorOnKTab.addCoupleByIndex(indexOldEdge, shared['MeshElmtList'][1].List.index(newEdge)) 
                 self.kBorderEdgeSideB.append(newEdge)     
             
             
             # attribution to the same groups than the initial face (i.e at leat the volume)
             for sklId in edge.SkeletonId:
                 indexOldSkel = shared["SkeletonElmtList"].IdList.index(sklId)
                 oldSkelm     = shared["SkeletonElmtList"].List[indexOldSkel]
                 volGeoGrp    = shared["SkeletonElmtList"].List[indexOldSkel].GeoGroup
                 meshGrpIndex = shared["MeshGroupList"].IdList.index(volGeoGrp.Id)
                 volMeshGrp   = shared["MeshGroupList"].List[meshGrpIndex]
    
                 # we assume that mesh and geo groups ahve the same order
                 newSkElm = SkeletonElement( seklElmId, oldSkelm.Type, NodeList())   #FIX ME
                 newSkElm.GeoGroup = volGeoGrp           # on attribut au nouveau group
                 newSkElm.GeoElement = oldSkelm.GeoElement  #mais on garde la ref a l object de geo
                 newSkElm.NodeNumber = oldSkelm.NodeNumber
                 newSkElm.Comments = "Duplicated skel on K"
                 
                 if newEdge.Id not in newSkeletonMeshElement.SkeletonId:
                     newFace.SkeletonId.append(newEdge.Id)
                 
                 #we add the new skeleton element to the list of the new MeshGrp
                 volMeshGrp.SkeletonElementList.Add_Element(newSkElm)
                 
                 newSkElm.SkeletonEdgeList.Add_Edge(newEdge) #i.e itself
                 
                 #TBC
                 for node in newEdge.MeshElementNodeList:
                     newSkElm.SkeletonNodeList.Add_Node(node)
                 
                 # we add the corresponding mesh element, in the presente case a FACE
                 newSkElm.SkeletonMeshElement = newEdge
                 
                 #we add the element to the common and shared Skeleton Elemt list
                 shared['SkeletonElmtList'].Add_Element(newSkElm)
                 seklElmId = seklElmId + 1
         print" "
         
         ###################################################
         ####  Management of faces on the cracking border
         ###################################################
         sys.stdout.write("Duplication of faces of K: ")
         newFaceId = shared['MeshElmtList'][2].List[len(shared['MeshElmtList'][1].List)-1].FaceId + 1
         
         # here we duplicate the skeletons and add them at the end of the list of skeletons
         #shift = len(shared['SkeletonElmtList'].List)
         #count = shift + 1
         
         controlList = []
         self.kborderFaceSideB = []
         for face in self.crackingBorderFaceList:
             #in this case we must really duplicate the face and create a new one
 
             indexOldFace = shared['MeshElmtList'][2].List.index(face)
                               
             #if ( indexOldEdge in self.faceCorTab.duplicatedElmList):   # VERIFIER SI TEST NECESSAIRE
             #    sys.stdout.write(".")
             #else:
             sys.stdout.write("+")
             # we create a new face 
             newFace = Face()
             newFace.Id = meshFaceId
             meshFaceId = meshFaceId + 1

             newFace.FaceId = newFaceId
             newFaceId = newFaceId + 1
             newFace.FaceType = "TRIANGLE"
             newFace.ElmtNum = 7010 #FIX ME
             
             tmpNodeOnFaceList =[]
             for oldNode in face.MeshElementNodeList:
                 tmpNodeOnFaceList.append(oldNode)
                    
             for oldNode in tmpNodeOnFaceList:
                 oldNodeIndex = shared['MeshElmtList'][0].List.index(oldNode)

                 #old version       
                 # apparently miss some nodes when Gmsh make mistakes in the skeletons
                 # attribution 
                 
                 # FIX ME : groupe a revoir
                 if oldNode in surfNodeList:

                    controlList.append(oldNode.Id)
                    #then it should be splitted.
                    newNode = self.nodeCorTab.getNewElmByIndex(oldNodeIndex)
                    newNode.FaceOnNode.append(newFace.Id)
                    
                    newFace.MeshElementNodeList.append(newNode)
                 else:
                    newFace.MeshElementNodeList.append(oldNode)
                    
             self.kborderFaceSideB.append(newFace)  
             
             
             # attribution to the same groups than the initial face (i.e at leat the volume)
             
             for sklId in face.SkeletonId:
                 indexOldSkel = shared["SkeletonElmtList"].IdList.index(sklId)
                 oldSkelm     = shared["SkeletonElmtList"].List[indexOldSkel]
                 volGeoGrp    = shared["SkeletonElmtList"].List[indexOldSkel].GeoGroup
                 meshGrpIndex = shared["MeshGroupList"].IdList.index(volGeoGrp.Id)
                 volMeshGrp   = shared["MeshGroupList"].List[meshGrpIndex]
    
                 # we assume that mesh and geo groups ahve the same order
                 newSkElm = SkeletonElement( seklElmId, oldSkelm.Type, NodeList())   #FIX ME
                 newSkElm.GeoGroup = volGeoGrp           
                 newSkElm.GeoElement = oldSkelm.GeoElement  
                 newSkElm.NodeNumber = oldSkelm.NodeNumber
                 newSkElm.Comments = "Duplicated skel from K border"
                 
                 if newFace.Id not in newSkeletonMeshElement.SkeletonId:
                     newFace.SkeletonId.append(newFace.Id)
                 
                 #we add the new skeleton element to the list of the new MeshGrp
                 volMeshGrp.SkeletonElementList.Add_Element(newSkElm)
                 
                 # we add the corresponding mesh element, in the presente case a FACE
                 newSkElm.SkeletonMeshElement = newFace
                 
                 #TBC
                 for node in newFace.MeshElementNodeList:
                     newSkElm.SkeletonNodeList.Add_Node(node)
             
                 #we add the element to the common and shared Skeleton Elemt list
                 shared['SkeletonElmtList'].Add_Element(newSkElm)
                 newSkElm.SkeletonFaceList.Add_Face(newFace) #i.e itself
                 seklElmId = seklElmId + 1
             
             
             
             # 2) Edges attribution
             tmpEdgeOnFaceList =[]
             for oldEdge in face.Connection:
                 tmpEdgeOnFaceList.append(oldEdge)
                    
             for oldEdge in tmpEdgeOnFaceList:
                 oldEdgeIndex = shared['MeshElmtList'][1].List.index(oldEdge)
                 if (oldEdgeIndex in self.edgeCorOnKTab.duplicatedElmList):
                     #then it should be splitted.
                     newEdge = self.edgeCorOnKTab.getNewElmByIndex(oldEdgeIndex)
                     newEdge.FaceOnEdge.append(newFace.Id)                        
                     newFace.Connection.append(newEdge)
                 else:
                     newFace.Connection.append(oldEdge)
                     oldEdge.FaceOnEdge.append(newFace.Id)
                    
             #don't forget to add the new face to the list
             shared['MeshElmtList'][2].Add_Face(newFace)
             
             #FIX ME 
             #splitedFaceIndexList.append(faceIndex)
             self.faceCorTab.addCoupleByElm( face, newFace)
             self.faceCorOnKTab.addCoupleByElm(face, newFace)
                 
         print " "
 
         
         ############################################################################################
         #  At this level, all elements ON the surface S and on the cracking border are duplicated. #
         ############################################################################################
 
 
                 
         ####################################################
         #     connection and splitting of Cells on Face    #
         #     and related sub-components.
         #     Version 2.0: bottom to up conectivity        #
         ####################################################
        
         print "Attribution of connected elements"
               
         # first we scan all node of the surface S in order to identify the elements on Node
         splitedCellIndexList = []
         correspondingCellIndexList =[]
         splitedFaceIndexList = []
         splitedEdgeIndexList = []
         
         print "Scanning nodes"
         #for nodeIndex in duplicatedNodesList:
         for nodeIndex in self.nodeCorTab.duplicatedElmList:
             node = shared['MeshElmtList'][0].List[nodeIndex]

             print "Attribution of element on node = ", node.Id

             #we translate the old nodes along the +normal in order to see something
             n = localNormalList[localNormalIndexList.index(node)]
             node.Coord[0] = node.Coord[0] - inflate * n[0]
             node.Coord[1] = node.Coord[1] - inflate * n[1]
             node.Coord[2] = node.Coord[2] - inflate * n[2]

             #node "conversion", i.e. attribution
             indexNewNode = self.nodeCorTab.getNewElmIndex(node)
             newNode = shared['MeshElmtList'][0].List[indexNewNode]       
             
             # We translate the new old along the -normal in order to see something
             newNode.Coord[0] = newNode.Coord[0] + inflate * n[0]
             newNode.Coord[1] = newNode.Coord[1] + inflate * n[1]
             newNode.Coord[2] = newNode.Coord[2] + inflate * n[2]
             
         
             
             # First, we manage the edges having at least one foot on the surface S
             sys.stdout.write("    Edges: ")
             for edgeId in node.EdgeOnNode:
                 edgeIndex = shared['MeshElmtList'][1].IdList.index(edgeId)
                 edge = shared['MeshElmtList'][1].List[edgeIndex]
                 indexInNodeList = node.EdgeOnNode.index(edgeId)
 
                 if ( edgeIndex not in splitedEdgeIndexList):
                    #Case A and B: the edge is include in S, then must be
                    #DUPLICATED it and attribute the new edge to the new node
                    indexStartNode = shared['MeshElmtList'][0].List.index(edge.StartNode)
                    indexEndNode = shared['MeshElmtList'][0].List.index(edge.EndNode)
                    
                    #FIX ME TBC
                    if ( edge in skelm.SkeletonEdgeList.List
                         or (    (indexStartNode in self.nodeCorTab.duplicatedElmList) 
                             and (indexEndNode in self.nodeCorTab.duplicatedElmList))
                         or edge in self.crackingBorderEdgeList):    #test fonctionnel mais a verifier  
                       sys.stdout.write(".")
                    else:
                        sys.stdout.write("+")
                        tmpList =[]
                        for tmpNode in edge.MeshElementNodeList:
                            tmpList.append(tmpNode.Id)

                        # test de la position relative for the edge having at lest one foot on the surface
                        localNormal = localNormalList[localNormalIndexList.index(node)]
                        if ( self.UpDownTest(node, localNormal, edge.GetIsoBaryCenter()) > 0.0 ):
                                    
                            #in this case, we have just to re-atribute it to the new node
                            if (node == edge.StartNode):
                                  edge.StartNode = newNode  
                            elif (node == edge.EndNode):
                                  edge.EndNode = newNode
                       
                            #c'est ce qui fait de fait le splitting topologique
                            tmpIndex = edge.MeshElementNodeList.index(node)
                            edge.MeshElementNodeList[tmpIndex] = newNode
                    
                    splitedEdgeIndexList.append(edgeIndex)
                    
                 tmpList =[]
                 for tmpNode in edge.MeshElementNodeList:
                     tmpList.append(tmpNode.Id) 
             print " "
             # END OF EDGES SPLITTING 
      
      
             
             #### FACES SPLITTING  
             #Second, we manage the faces having or one top or one side on the surface
             sys.stdout.write("    Faces: ")
             tmpFaceList=[]
             controlFaceList = []
             for faceOnNodeId in node.FaceOnNode:
                 tmpFaceList.append(faceOnNodeId)
             
             for faceOnNodeId in tmpFaceList:                              #node.FaceOnNode: Because otherwise it jump some elements when the previous has been removed
                 faceIndex = shared['MeshElmtList'][2].IdList.index(faceOnNodeId)
                 faceOnNode = shared['MeshElmtList'][2].List[faceIndex]
 
                 if ( faceIndex not in splitedFaceIndexList):                      
                    if faceOnNode not in controlFaceList:
                        controlFaceList.append(faceOnNode)
                    #Case A : the face is included in S, then must be
                    #DUPLICATED it and attribute the new face to the new nodes
                    
                    if (faceOnNode in self.upFaceList):
                        sys.stdout.write("+")
                        '''
                        if faceOnNode in self.crackingBorderFaceList:
                            print "XXXXXX ERROR IN FACE SIDE A"
                        if faceOnNode in self.kborderFaceSideB:
                            print "XXXXXX ERROR IN FACE SIDE B"
                        '''
                        
                        # detection of sub-elements ON the surface S
                        # 1) nodes
                        tmpNodeOnFaceList =[]
                        for oldNode in faceOnNode.MeshElementNodeList:
                            tmpNodeOnFaceList.append(oldNode)
                        
                        for oldNode in tmpNodeOnFaceList:
                            oldNodeIndex = shared['MeshElmtList'][0].List.index(oldNode)
                            if (oldNodeIndex in self.nodeCorTab.duplicatedElmList):
                                                   
                                #then it should be splitted.
                                newNode = self.nodeCorTab.getNewElmByIndex(oldNodeIndex)
                                
                                oldNode.FaceOnNode.remove(faceOnNode.Id)
                                newNode.FaceOnNode.append(faceOnNode.Id)
                            
                                faceOnNode.MeshElementNodeList.remove(oldNode)
                                faceOnNode.MeshElementNodeList.append(newNode)
                                
                        # 2) Edges
                        tmpEdgeOnFaceList =[]
                        for oldEdge in faceOnNode.Connection:
                            tmpEdgeOnFaceList.append(oldEdge)
                        
                        for oldEdge in tmpEdgeOnFaceList:
                            oldEdgeIndex = shared['MeshElmtList'][1].List.index(oldEdge)
                            if (oldEdgeIndex in self.edgeCorTab.duplicatedElmList):
                                                   
                                #then it should be splitted.
                                newEdge = self.edgeCorTab.getNewElmByIndex(oldEdgeIndex)
 
                                oldEdge.FaceOnEdge.remove(faceOnNode.Id)
                                newEdge.FaceOnEdge.append(faceOnNode.Id)
                            
                                faceOnNode.Connection.remove(oldEdge)
                                faceOnNode.Connection.append(newEdge)      
                    
                    splitedFaceIndexList.append(faceIndex)
                    
             print " " 
             ### END OF FACE SPLITTING
             
             
             
             #### CELLS SPLiTTING
             #Third, we manage the cells having or one top or one edge or one side on the surface
             sys.stdout.write("    Cells: ")
             tmpCellList=[]
             for cellOnNodeId in node.CellOnNode:
                 tmpCellList.append(cellOnNodeId)
             
             for cellOnNodeId in tmpCellList:                              #node.FaceOnNode: Because otherwise it jump some elements when the previous has been removed
                 cellIndex = shared['MeshElmtList'][3].IdList.index(cellOnNodeId)
                 upCell = shared['MeshElmtList'][3].List[cellIndex]
                 
                 if ( cellIndex not in  splitedCellIndexList):
                    # dectection if the face is on the up-side of S
                    if upCell in self.upCellList:
                        sys.stdout.write("+")
                        # detection of sub-elements ON the surface S
                        # 1) nodes
                        tmpNodeOnCellList =[]
                        for oldNode in upCell.MeshElementNodeList:
                            tmpNodeOnCellList.append(oldNode)
                            
                        for oldNode in tmpNodeOnCellList:
                            oldNodeIndex = shared['MeshElmtList'][0].List.index(oldNode)
                            if (oldNodeIndex in self.nodeCorTab.duplicatedElmList):
                                
                                newNode = self.nodeCorTab.getNewElmByIndex(oldNodeIndex)
                                
                                oldNode.CellOnNode.remove(upCell.Id)
                                newNode.CellOnNode.append(upCell.Id)
                               
                                upCell.MeshElementNodeList.remove(oldNode)
                                upCell.MeshElementNodeList.append(newNode)
                                               
                                             
                        # 2) Faces (for cells the connection is defined on toward the faces)
                        tmpFaceOnCellList =[]
                        tmpIdList=[]
                        for faceOnCell in upCell.Connection:
                            tmpFaceOnCellList.append(faceOnCell)
                            tmpIdList.append(faceOnCell.Id)
                                             
                        
                        #version 2
                        # for the cells connected to S
                        for faceOnCell in tmpFaceOnCellList:
                            oldFaceIndex = shared['MeshElmtList'][2].List.index(faceOnCell)
                            if (   oldFaceIndex in self.skelCorTab.duplicatedElmList):                       
                                #then it should be splitted.
                                newFace = self.skelCorTab.getNewElmByIndex(oldFaceIndex)
                                
                                faceOnCell.CellOnFace.remove(upCell.Id)
                                newFace.CellOnFace.append(upCell.Id)
                                
                                upCell.Connection.remove(faceOnCell)
                                upCell.Connection.append(newFace)
                                
                        # for the cells connected to the K border        
                        for faceOnCell in tmpFaceOnCellList:
                            oldFaceIndex = shared['MeshElmtList'][2].List.index(faceOnCell)
                            if ( faceOnCell in self.crackingBorderFaceList):                       
                                #then it should be splitted.
                                newFace = self.faceCorTab.getNewElmByIndex(oldFaceIndex)
                                
                                faceOnCell.CellOnFace.remove(upCell.Id)
                                newFace.CellOnFace.append(upCell.Id)
                                
                                upCell.Connection.remove(faceOnCell)
                                upCell.Connection.append(newFace)
                        
                        
                    splitedCellIndexList.append(cellIndex)
             print " " 
             ### END OF CELL SPLITTING
         
         print "end of splitting"
         
         
     
     def UpDownTest(self, nodeIn, normalIn, baryIn): 
         '''
         returns 1 if the barycentre is on the same side than the normal with
         respect to the node.
         '''
         vect = [0.0, 0.0, 0.0]
         vect[0] = baryIn[0] - nodeIn.Coord[0] 
         vect[1] = baryIn[1] - nodeIn.Coord[1] 
         vect[2] = baryIn[2] - nodeIn.Coord[2]
         value = vect[0]*normalIn[0] + vect[1]*normalIn[1] + vect[2]*normalIn[2]
         value = value/math.fabs(value)
         return(value)
         
     def GetLocalNormale(self, nodeIn, surfListIn):
         
         localNormal = [0.0, 0.0, 0.0]
         nbNormal = 0
         
         for faceId in nodeIn.FaceOnNode:
             face = shared['MeshElmtList'][2].GetElementById(faceId)
             if face in surfListIn:
                nodeList = face.MeshElementNodeList
                A = nodeIn.Coord
                indexA = face.MeshElementNodeList.index(nodeIn)
                indexB = (indexA+1) % 3
                B = face.MeshElementNodeList[indexB].Coord
                indexC = (indexA+2) % 3
                C = face.MeshElementNodeList[indexC].Coord
   
                vect1 = [0.0, 0.0, 0.0]
                vect1[0] = B[0] - A[0]
                vect1[1] = B[1] - A[1]
                vect1[2] = B[2] - A[2]
                
                vect2 = [0.0, 0.0, 0.0]
                vect2[0] = C[0] - A[0]
                vect2[1] = C[1] - A[1]
                vect2[2] = C[2] - A[2]
                
                tmpNormal = [0.0, 0.0, 0.0]
                tmpNormal[0] = vect1[1]*vect2[2] - vect2[1]*vect1[2]
                tmpNormal[1] = vect2[0]*vect1[2] - vect1[0]*vect2[2]
                tmpNormal[2] = vect1[0]*vect2[1] - vect2[0]*vect1[1]
                
                normalisation = math.sqrt(tmpNormal[0]*tmpNormal[0] + tmpNormal[1]*tmpNormal[1] + tmpNormal[2]*tmpNormal[2])
                tmpNormal[0] = tmpNormal[0]/normalisation
                tmpNormal[1] = tmpNormal[1]/normalisation
                tmpNormal[2] = tmpNormal[2]/normalisation
                
                localNormal[0] = localNormal[0] + tmpNormal[0]
                localNormal[1] = localNormal[1] + tmpNormal[1]
                localNormal[2] = localNormal[2] + tmpNormal[2]
                nbNormal = nbNormal + 1
                
         if nbNormal != 0.0:
             localNormal[0] = localNormal[0]/nbNormal
             localNormal[1] = localNormal[1]/nbNormal
             localNormal[2] = localNormal[2]/nbNormal
         
         return(localNormal)
         
         
     def GetFields(self):
         #####################################################################
         # Creation of correspondance meshfields and data fields
         #####################################################################
         
         MFId = 100001 #FIX ME
         DFId = 100001 #FIX ME
         
         
         #############################################################
         # real correspondance tables on spacecraft
         #############################################################
         
         # for nodes on SC
         sys.stdout.write("Mapping of correspondance DF for nodes on SC: ")
         nodeCorresMF = MeshField()
         nodeCorresMF.Id = MFId
         MFId = MFId + 1
         nodeCorresMF.Name = "duplicatedNodesParityS_MF"
         nodeCorresMF.Local = 0
         nodeCorresMF.Type = "int"
 
         for nodeIndex in self.nodeCorTab.duplicatedElmList:
              node = shared['MeshElmtList'][0].List[nodeIndex]
              nodeCorresMF.MeshElementIdList.append(node.Id)
              nodeCorresMF.MeshElementList.append(node)
         
         for nodeIndex in self.nodeCorTab.correspondingElmList:
              node = shared['MeshElmtList'][0].List[nodeIndex]
              nodeCorresMF.MeshElementIdList.append(node.Id)
              nodeCorresMF.MeshElementList.append(node)
         
         nodeCorresDF = DataField()
         nodeCorresDF.Id = DFId
         DFId = DFId + 1
         nodeCorresDF.Name = "duplicatedNodesParityS"
         nodeCorresDF.Local = 0
         nodeCorresDF.MeshFieldId = nodeCorresMF.Id
         nodeCorresDF.Category = "meshSplitting"
 
         for nodeIndexOnFaceDown in self.nodeCorTab.duplicatedElmList:
              nodeCorresDF.ValueList.append(self.nodeCorTab.getNewElmByIndex(nodeIndexOnFaceDown).Id)
         
         for nodeIndexOnFaceUp in self.nodeCorTab.correspondingElmList:
              nodeCorresDF.ValueList.append(self.nodeCorTab.getOldElmByIndex(nodeIndexOnFaceUp).Id)
         
         sharedData['AllDataField'].Add_DataField(nodeCorresDF)
         sharedData['AllMeshField'].Add_MeshField(nodeCorresMF)
         print "Done"

         # for edges on SC
         sys.stdout.write("Mapping of correspondance DF for edges on SC: ")
         edgeCorresMF = MeshField()
         edgeCorresMF.Id = MFId
         MFId = MFId + 1
         edgeCorresMF.Name = "duplicatedEdgesParityS_MF"
         edgeCorresMF.Local = 1
         edgeCorresMF.Type = "int"
         
         for edgeIndex in self.edgeOnSCorTab.duplicatedElmList:
             edge = shared['MeshElmtList'][1].List[edgeIndex]
             edgeCorresMF.MeshElementIdList.append(edge.Id)
             edgeCorresMF.MeshElementList.append(edge)
         
         for edgeIndex in self.edgeOnSCorTab.correspondingElmList:
             edge = shared['MeshElmtList'][1].List[edgeIndex]
             edgeCorresMF.MeshElementIdList.append(edge.Id)
             edgeCorresMF.MeshElementList.append(edge)   
          
         edgeCorresDF = DataField()
         edgeCorresDF.Id = DFId
         DFId = DFId + 1
         edgeCorresDF.Name = "duplicatedEdgesParityS"
         edgeCorresDF.Local = 1
         edgeCorresDF.MeshFieldId = edgeCorresMF.Id
         edgeCorresDF.Category = "meshSplitting"
         
         for edgeIndexOnFaceDown in self.edgeOnSCorTab.duplicatedElmList:
              edgeCorresDF.ValueList.append(self.edgeOnSCorTab.getNewElmByIndex(edgeIndexOnFaceDown).Id)
        
         for edgeIndexOnFaceUp in self.edgeOnSCorTab.correspondingElmList:
              edgeCorresDF.ValueList.append(self.edgeOnSCorTab.getOldElmByIndex(edgeIndexOnFaceUp).Id)
                 
         sharedData['AllDataField'].Add_DataField(edgeCorresDF)
         sharedData['AllMeshField'].Add_MeshField(edgeCorresMF)
         print "Done"
         
         # for faces on SC
         sys.stdout.write("Mapping of correspondance DF for faces: ")
         faceCorresMF = MeshField()
         faceCorresMF.Id = MFId
         MFId = MFId + 1
         faceCorresMF.Name = "duplicatedFacesParityS_MF"
         faceCorresMF.Local = 2
         faceCorresMF.Type = "int"
         
         for faceIndex in self.faceOnSCorTab.duplicatedElmList:
              face = shared['MeshElmtList'][2].List[faceIndex]
              faceCorresMF.MeshElementIdList.append(face.Id)
              faceCorresMF.MeshElementList.append(face)
         
         for faceIndex in self.faceOnSCorTab.correspondingElmList:
              face = shared['MeshElmtList'][2].List[faceIndex]
              faceCorresMF.MeshElementIdList.append(face.Id)
              faceCorresMF.MeshElementList.append(face)   
         
         faceCorresDF = DataField()
         faceCorresDF.Id = DFId
         DFId = DFId + 1
         faceCorresDF.Name = "duplicatedFacesParityS"
         faceCorresDF.Local = 2
         faceCorresDF.MeshFieldId = faceCorresMF.Id
         faceCorresDF.Category = "meshSplitting"
         
         print 
         for faceIndexOnFaceDown in self.faceOnSCorTab.duplicatedElmList:
              faceCorresDF.ValueList.append(self.faceOnSCorTab.getNewElmByIndex(faceIndexOnFaceDown).Id)
              print shared['MeshElmtList'][2].List[faceIndexOnFaceDown].Id,"(",faceIndexOnFaceDown,")", self.faceOnSCorTab.getNewElmByIndex(faceIndexOnFaceDown).Id
         print "----"
         for faceIndexOnFaceUp in self.faceOnSCorTab.correspondingElmList:
              faceCorresDF.ValueList.append(self.faceOnSCorTab.getOldElmByIndex(faceIndexOnFaceUp).Id)
              print shared['MeshElmtList'][2].List[faceIndexOnFaceUp].Id,"(",faceIndexOnFaceUp,")", self.faceOnSCorTab.getOldElmByIndex(faceIndexOnFaceUp).Id
          
         sharedData['AllDataField'].Add_DataField(faceCorresDF)
         sharedData['AllMeshField'].Add_MeshField(faceCorresMF)
         print "Done"  
         
         
         #############################################################
         # correspondance tables on volume
         #############################################################
         # for nodes
         sys.stdout.write("Mapping of correspondance DF for nodes: ")
         nodeCorresMF = MeshField()
         nodeCorresMF.Id = MFId
         MFId = MFId + 1
         nodeCorresMF.Name = "duplicatedNodesParity_MF"
         nodeCorresMF.Local = 0
         nodeCorresMF.Type = "int"
         for node in shared['MeshElmtList'][0].List:
             nodeCorresMF.MeshElementIdList.append(node.Id)
             nodeCorresMF.MeshElementList.append(node)
 
         
         nodeCorresDF = DataField()
         nodeCorresDF.Id = DFId
         DFId = DFId + 1
         nodeCorresDF.Name = "duplicatedNodesParity"
         nodeCorresDF.Local = 0
         nodeCorresDF.MeshFieldId = nodeCorresMF.Id
         nodeCorresDF.Category = "meshSplitting"
         
         # new and fast version
         for node in shared['MeshElmtList'][0].List:
             nodeCorresDF.ValueList.append(0)
             
         for nodeIndexOnFaceDown in self.nodeCorTab.duplicatedElmList:
             nodeCorresDF.ValueList[nodeIndexOnFaceDown] = self.nodeCorTab.getNewElmByIndex(nodeIndexOnFaceDown).Id
          
         for nodeIndexOnFaceUp in self.nodeCorTab.correspondingElmList:
             nodeCorresDF.ValueList[nodeIndexOnFaceUp] = self.nodeCorTab.getOldElmByIndex(nodeIndexOnFaceUp).Id
       
         
         # for edges
         sys.stdout.write("Mapping of correspondance DF for edges: ")
         edgeCorresMF = MeshField()
         edgeCorresMF.Id = MFId
         MFId = MFId + 1
         edgeCorresMF.Name = "duplicatedEdgesParity_MF"
         edgeCorresMF.Local = 1
         edgeCorresMF.Type = "int"
         for edge in shared['MeshElmtList'][1].List:
             edgeCorresMF.MeshElementIdList.append(edge.Id)
             edgeCorresMF.MeshElementList.append(edge)
             
         
         edgeCorresDF = DataField()
         edgeCorresDF.Id = DFId
         DFId = DFId + 1
         edgeCorresDF.Name = "duplicatedEdgesParity"
         edgeCorresDF.Local = 1
         edgeCorresDF.MeshFieldId = edgeCorresMF.Id
         edgeCorresDF.Category = "meshSplitting"
         
         # new and fast version
         for edge in shared['MeshElmtList'][1].List:
             edgeCorresDF.ValueList.append(0)
             
             
         # for the S surface    
         for edgeIndexOnFaceDown in self.edgeCorTab.duplicatedElmList:
             edgeCorresDF.ValueList[edgeIndexOnFaceDown] = self.edgeCorTab.getNewElmByIndex(edgeIndexOnFaceDown).Id
             
         for edgeIndexOnFaceUp in self.edgeCorTab.correspondingElmList:
             edgeCorresDF.ValueList[edgeIndexOnFaceUp] =  self.edgeCorTab.getOldElmByIndex(edgeIndexOnFaceUp).Id
             
         
         # for the K border
         self.edgeCorOnKTab
         for edgeIndexOnFaceDown in self.edgeCorOnKTab.duplicatedElmList:
             edgeCorresDF.ValueList[edgeIndexOnFaceDown] = self.edgeCorOnKTab.getNewElmByIndex(edgeIndexOnFaceDown).Id
             
         for edgeIndexOnFaceUp in self.edgeCorOnKTab.correspondingElmList:
             edgeCorresDF.ValueList[edgeIndexOnFaceUp] =  self.edgeCorOnKTab.getOldElmByIndex(edgeIndexOnFaceUp).Id
         
         
         sharedData['AllDataField'].Add_DataField(edgeCorresDF)
         sharedData['AllMeshField'].Add_MeshField(edgeCorresMF)
         print "Done"
         
         
         # for faces
         sys.stdout.write("Mapping of correspondance DF for faces: ")
         faceCorresMF = MeshField()
         faceCorresMF.Id = MFId
         MFId = MFId + 1
         faceCorresMF.Name = "duplicatedFacesParity_MF"
         faceCorresMF.Local = 2
         faceCorresMF.Type = "int"
         for face in shared['MeshElmtList'][2].List:
             faceCorresMF.MeshElementIdList.append(face.Id)
             faceCorresMF.MeshElementList.append(face)
         
         
         faceCorresDF = DataField()
         faceCorresDF.Id = DFId
         DFId = DFId + 1
         faceCorresDF.Name = "duplicatedFacesParity"
         faceCorresDF.Local = 2
         faceCorresDF.MeshFieldId = faceCorresMF.Id
         faceCorresDF.Category = "meshSplitting"
          
         faceCorresDF.ValueList = []
         # new and fast version
         for face in shared['MeshElmtList'][2].List:
             faceCorresDF.ValueList.append(0)
             
         print     
         print self.faceOnSCorTab.duplicatedElmList
         print self.faceOnSCorTab.correspondingElmList

         
         for faceIndexOnFaceDown in self.faceOnSCorTab.duplicatedElmList:
             indexOpposedFace = self.faceOnSCorTab.getNewElmIndexByIndex(faceIndexOnFaceDown)
             faceCorresDF.ValueList[faceIndexOnFaceDown] =  shared['MeshElmtList'][2].List[indexOpposedFace].Id
             faceCorresDF.ValueList[indexOpposedFace] = shared['MeshElmtList'][2].List[faceIndexOnFaceDown].Id
             print "face A(", faceIndexOnFaceDown,") of Id", shared['MeshElmtList'][2].List[faceIndexOnFaceDown].Id," =",faceCorresDF.ValueList[faceIndexOnFaceDown], "face B(",indexOpposedFace,") of Id", shared['MeshElmtList'][2].List[indexOpposedFace].Id,"=", faceCorresDF.ValueList[indexOpposedFace]
             
         sharedData['AllDataField'].Add_DataField(nodeCorresDF)
         sharedData['AllMeshField'].Add_MeshField(nodeCorresMF)
         print "Done"
         
         # for the K border
         for faceIndexOnFaceDown in self.faceCorOnKTab.duplicatedElmList:
             faceCorresDF.ValueList[faceIndexOnFaceDown] = self.faceCorOnKTab.getNewElmByIndex(faceIndexOnFaceDown).Id
             
         for faceIndexOnFaceUp in self.faceCorOnKTab.correspondingElmList:
             faceCorresDF.ValueList[faceIndexOnFaceUp] = self.faceCorOnKTab.getOldElmByIndex(faceIndexOnFaceUp).Id
          
          
         sharedData['AllDataField'].Add_DataField(faceCorresDF)
         sharedData['AllMeshField'].Add_MeshField(faceCorresMF)
         print "Done"   
         

     def GetControls(self):
     
         #############################
         
         MFId = 200001 #FIX ME
         DFId = 200001 #FIX ME
         
         nodeCorresMF = MeshField()
         nodeCorresMF.Id = MFId
         MFId = MFId + 1
         nodeCorresMF.Name = "correspondanceSCNodeGlyph_MF"
         nodeCorresMF.Local = 0
         nodeCorresMF.Type = "int*3"
 
         for nodeIndex in self.nodeCorTab.duplicatedElmList:
              node = shared['MeshElmtList'][0].List[nodeIndex]
              nodeCorresMF.MeshElementIdList.append(node.Id)
              nodeCorresMF.MeshElementList.append(node)
         
         for nodeIndex in self.nodeCorTab.correspondingElmList:
              node = shared['MeshElmtList'][0].List[nodeIndex]
              nodeCorresMF.MeshElementIdList.append(node.Id)
              nodeCorresMF.MeshElementList.append(node)
              
         sys.stdout.write("Glyph controle mapping of correspondance DF for nodes on SC: ")         
         nodeCorresDF = DataField()
         nodeCorresDF.Id = DFId
         DFId = DFId + 1
         nodeCorresDF.Name = "correspondanceSCNodeGlyph"
         nodeCorresDF.Local = 0
         nodeCorresDF.MeshFieldId = nodeCorresMF.Id
         nodeCorresDF.Category = "meshSplitting"
 
         
         for nodeIndexOnFaceDown in self.nodeCorTab.duplicatedElmList:
              nodeA = shared['MeshElmtList'][0].List[nodeIndexOnFaceDown]
              nodeB = self.nodeCorTab.getNewElmByIndex(nodeIndexOnFaceDown)
              u = [0.0, 0.0, 0.0]
              u[0] = nodeB.Coord[0]-nodeA.Coord[0]
              u[1] = nodeB.Coord[1]-nodeA.Coord[1]
              u[2] = nodeB.Coord[2]-nodeA.Coord[2]
              nodeCorresDF.ValueList.append(u)
         
         for nodeIndexOnFaceUp in self.nodeCorTab.correspondingElmList:
              #nodeCorresDF.ValueList.append(self.nodeCorTab.getOldElmByIndex(nodeIndexOnFaceUp).Id)
              nodeA = shared['MeshElmtList'][0].List[nodeIndexOnFaceUp]
              nodeB = self.nodeCorTab.getOldElmByIndex(nodeIndexOnFaceUp)
              u = [0.0,0.0, 0.0]
              u[0] = nodeB.Coord[0]-nodeA.Coord[0]
              u[1] = nodeB.Coord[1]-nodeA.Coord[1]
              u[2] = nodeB.Coord[2]-nodeA.Coord[2]
              nodeCorresDF.ValueList.append(u)
         
         sharedData['AllDataField'].Add_DataField(nodeCorresDF)
         sharedData['AllMeshField'].Add_MeshField(nodeCorresMF)
         
         
         #fro the edges
         sys.stdout.write("Mapping of correspondance DF for edges on SC: ")
         edgeCorresMF = MeshField()
         edgeCorresMF.Id = MFId
         MFId = MFId + 1
         edgeCorresMF.Name = "correspondanceSCEdgesGlyph_MF"
         edgeCorresMF.Local = 1
         edgeCorresMF.Type = "int"
         
         for edgeIndex in self.edgeOnSCorTab.duplicatedElmList:
             edge = shared['MeshElmtList'][1].List[edgeIndex]
             edgeCorresMF.MeshElementIdList.append(edge.Id)
             edgeCorresMF.MeshElementList.append(edge)
         
         for edgeIndex in self.edgeOnSCorTab.correspondingElmList:
             edge = shared['MeshElmtList'][1].List[edgeIndex]
             edgeCorresMF.MeshElementIdList.append(edge.Id)
             edgeCorresMF.MeshElementList.append(edge)   
          
         edgeCorresDF = DataField()
         edgeCorresDF.Id = DFId
         DFId = DFId + 1
         edgeCorresDF.Name = "correspondanceSCEdgesGlyph"
         edgeCorresDF.Local = 1
         edgeCorresDF.MeshFieldId = edgeCorresMF.Id
         edgeCorresDF.Category = "meshSplitting"
         
         
         for edgeIndexOnFaceDown in self.edgeOnSCorTab.duplicatedElmList:
              #edgeCorresDF.ValueList.append(self.edgeOnSCorTab.getNewElmByIndex(edgeIndexOnFaceDown).Id)  
              nodeA = shared['MeshElmtList'][1].List[edgeIndexOnFaceDown].GetIsoBaryCenter()
              nodeB = self.edgeOnSCorTab.getNewElmByIndex(edgeIndexOnFaceDown).GetIsoBaryCenter()
              u = [0.0, 0.0, 0.0]
              u[0] = nodeB[0]-nodeA[0]
              u[1] = nodeB[1]-nodeA[1]
              u[2] = nodeB[2]-nodeA[2]
              edgeCorresDF.ValueList.append(u)
        
         for edgeIndexOnFaceUp in self.edgeOnSCorTab.correspondingElmList:
              #edgeCorresDF.ValueList.append(self.edgeOnSCorTab.getOldElmByIndex(edgeIndexOnFaceUp).Id)
              nodeA = shared['MeshElmtList'][1].List[edgeIndexOnFaceUp].GetIsoBaryCenter()
              nodeB = self.edgeOnSCorTab.getOldElmByIndex(edgeIndexOnFaceUp).GetIsoBaryCenter()
              u = [0.0,0.0, 0.0]
              u[0] = nodeB[0]-nodeA[0]
              u[1] = nodeB[1]-nodeA[1]
              u[2] = nodeB[2]-nodeA[2]
              edgeCorresDF.ValueList.append(u)
         
         sharedData['AllDataField'].Add_DataField(edgeCorresDF)
         sharedData['AllMeshField'].Add_MeshField(edgeCorresMF)
         print "Done"
         
         # for faces
         sys.stdout.write("Mapping of correspondance DF for faces: ")
         faceCorresMF = MeshField()
         faceCorresMF.Id = MFId
         MFId = MFId + 1
         faceCorresMF.Name = "duplicatedFacesParitySGlyph_MF"
         faceCorresMF.Local = 0
         faceCorresMF.Type = "int"
         
         #for faceIndex in self.faceOnSCorTab.duplicatedElmList:
         #     face = shared['MeshElmtList'][2].List[faceIndex]
         #     faceCorresMF.MeshElementIdList.append(face.Id)
         #     faceCorresMF.MeshElementList.append(face)
         
         #for faceIndex in self.faceOnSCorTab.correspondingElmList:
         #     face = shared['MeshElmtList'][2].List[faceIndex]
         #     faceCorresMF.MeshElementIdList.append(face.Id)
         #     faceCorresMF.MeshElementList.append(face)   
         
         faceCorresDF = DataField()
         faceCorresDF.Id = DFId
         DFId = DFId + 1
         faceCorresDF.Name = "duplicatedFacesParitySGlyph"
         faceCorresDF.Local = 2
         faceCorresDF.MeshFieldId = faceCorresMF.Id
         faceCorresDF.Category = "meshSplitting"
         
         for faceIndexOnFaceDown in self.faceOnSCorTab.duplicatedElmList:
              #faceCorresDF.ValueList.append(self.faceOnSCorTab.getNewElmByIndex(faceIndexOnFaceDown).Id)
              nodeA = shared['MeshElmtList'][2].List[faceIndexOnFaceDown].GetIsoBaryCenter()
              nodeB = self.faceOnSCorTab.getNewElmByIndex(faceIndexOnFaceDown).GetIsoBaryCenter()
              u = [0.0, 0.0, 0.0]
              u[0] = nodeB[0]-nodeA[0]
              u[1] = nodeB[1]-nodeA[1]
              u[2] = nodeB[2]-nodeA[2]
              faceCorresDF.ValueList.append(u)
         
         for faceIndexOnFaceUp in self.faceOnSCorTab.correspondingElmList:
              #faceCorresDF.ValueList.append(self.faceOnSCorTab.getOldElmByIndex(faceIndexOnFaceUp).Id)
              nodeA = shared['MeshElmtList'][2].List[faceIndexOnFaceUp].GetIsoBaryCenter()
              nodeB = self.faceOnSCorTab.getOldElmByIndex(faceIndexOnFaceUp).GetIsoBaryCenter()
              u = [0.0,0.0, 0.0]
              u[0] = nodeB[0]-nodeA[0]
              u[1] = nodeB[1]-nodeA[1]
              u[2] = nodeB[2]-nodeA[2]
              faceCorresDF.ValueList.append(u)
          
         sharedData['AllDataField'].Add_DataField(faceCorresDF)
         sharedData['AllMeshField'].Add_MeshField(faceCorresMF)
         print "Done"  
         

     def GetVtkDataSet(self):
                     
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.crackingBorderEdgeList, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/kBorderEdgeSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.kBorderEdgeSideB, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/kBorderEdgeSideB.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.borderEdgeList, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/bBorderEdgeListSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         gBuilder = vtkGridBuilder(self.borderNodeList, self.borderNodeList, 1)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/bBorderNodesSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.crackingBorderFaceList, 5)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/kBorderFaceSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)
 
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.kborderFaceSideB, 5)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/kBorderFaceSideB.vtk"
         gBuilder.writeToFile(pathVtkFile)
 
 
 
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.upFaceList, 5)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/connectedFaceSideB.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         sharedSplitElm["faceSideB"] = self.downFaceList
 
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.downFaceList, 5)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/connectedFaceSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)   
         
         sharedSplitElm["faceSideA"] = self.upFaceList
         
 
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, shared['MeshElmtList'][1].List, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/edgeGrid.vtk"
         gBuilder.writeToFile(pathVtkFile)
                        
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.surfEdgeList, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/EdgeSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, shared['MeshElmtList'][3].List, 10)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/cellGrid.vtk"
         gBuilder.writeToFile(pathVtkFile)
 
 
 
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.downCellList, 10)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/cellSideA.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, self.upCellList, 10)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/cellSideB.vtk"
         gBuilder.writeToFile(pathVtkFile)
 
 
 
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, shared['MeshElmtList'][2].List, 5)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/surfGrid.vtk"
         gBuilder.writeToFile(pathVtkFile)
 
         tmpList = []
         for indexTmp in self.edgeCorTab.correspondingElmList:
             tmpList.append(shared['MeshElmtList'][1].List[indexTmp])
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, tmpList, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/duplicatedCrackingBorderEdge.vtk"
         gBuilder.writeToFile(pathVtkFile)
                  
         tmpList = []
         for indexTmp in self.edgeOnSCorTab.correspondingElmList:
             tmpList.append(shared['MeshElmtList'][1].List[indexTmp])
         
         gBuilder = vtkGridBuilder(shared['MeshElmtList'][0].List, tmpList, 3)
         gBuilder.buildGrid()
         pathVtkFile = GL_DATA_PATH+"Vtk/edgeOnSCorTab.vtk"
         gBuilder.writeToFile(pathVtkFile)
         
