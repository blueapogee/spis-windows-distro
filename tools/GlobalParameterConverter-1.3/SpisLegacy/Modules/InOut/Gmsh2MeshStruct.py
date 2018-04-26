"""
**Module Name:**  Gmsh2MeshStruct

**Project ref:**  Spis/SpisUI

**File name:**    Gmsh2MeshStruct.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:** Moduel of conversion from the mesh GMSH mesh format to the
the mesh structure.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Pascal Seng

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                | Definition/Creation        |
|                | Franck Warmont@artenum.com    |                            |
+----------------+-------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet               | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com   | Validation                 |
+----------------+-------------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

import os
import string
import time

from Modules.Meshing.EdgeList            import EdgeList
from Modules.Meshing.FaceList            import FaceList
from Modules.Meshing.CellList            import CellList
from Modules.Meshing.Edge                import Edge
from Modules.Meshing.NodeList            import NodeList
from Modules.Meshing.SkeletonElementList import SkeletonElementList
from Modules.Meshing.Node                import Node
from Modules.Meshing.SkeletonElement     import SkeletonElement
from Modules.Meshing.Face                import Face
from Modules.Meshing.Cell                import Cell
from Modules.Groups.MeshGroupList        import MeshGroupList

ListOfNode = NodeList()
ListOfEdge = EdgeList()
ListOfFace = FaceList()
ListOfCell = CellList()
ListOfNodeId = []
ListOfSkeletonElement = SkeletonElementList()
ListOfMeshGroup = MeshGroupList()
ListOfMeshElement = []
ListOfMeshElementNum = []
ListOfOldNodeNum = []
ListOfNewNodeNum = []
ListOfOldSkeletonElmtNum = []
ListOfNewSkeletonElmtNum = []
NbMeshElement = 1

LineCounter = 1
Field = []
FileIn = None

Convert_Type = {}
Convert_Type['1'] = 'LINE'
Convert_Type['2'] = 'TRIANGLE'
Convert_Type['3'] = 'QUADRANGLE'
Convert_Type['4'] = 'TETRAHEDRON'
Convert_Type['5'] = 'HEXAHEDRON'
Convert_Type['6'] = 'PRISM'
Convert_Type['7'] = 'PYRAMID'
Convert_Type['15'] = 'POINT'

def Convert_Point(Skeleton):
   Skeleton.SkeletonNodeList.List[0].SkeletonId.append(Skeleton.Id)
   return Skeleton.SkeletonNodeList.List[0]

def Convert_Line(Skeleton):
   global ListOfEdge,NbMeshElement,ListOfMeshElementNum
   for TempNode in Skeleton.SkeletonNodeList.List:
      TempNode.SkeletonId.append(Skeleton.Id)
   # Warning Edge should have an independent id management and should not use NbMeshElement as argument
   # Check first if Line already exist
   EdgeFound = 0
   for EdgeNum in Skeleton.SkeletonNodeList.List[0].EdgeOnNode: # Go throuh the list of Edge that live on first Node
       # If Edge has already been identified as an edge living on first node one get it back
       if (EdgeNum in Skeleton.SkeletonNodeList.List[1].EdgeOnNode):
           EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
           EdgeFound = 1
           break
   if EdgeFound == 0: # if Edge is not found, Edge created
       EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1])
       NbMeshElement = NbMeshElement+1
       ListOfEdge.Add_Edge(EdgeElmt)
       ListOfMeshElementNum.append(ListOfEdge.NbEdge)
       EdgeElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List 
   Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)
   EdgeElmt.SkeletonId.append(Skeleton.Id)
   return EdgeElmt





def Convert_Triangle(Skeleton):
   global ListOfEdge,ListOfFace,NbMeshElement,ListOfMeshElementNum

   # TempNode is the List of node used to define skeleton
   for TempNode in Skeleton.SkeletonNodeList.List:
       TempNode.SkeletonId.append(Skeleton.Id)

   # initiate face corresponding to triangle, if it does not exist yet
   FaceFound = 0
   for FaceNum in Skeleton.SkeletonNodeList.List[0].FaceOnNode: # loop over face ids associated with first node of the list of three nodes
        if ((FaceNum in Skeleton.SkeletonNodeList.List[1].FaceOnNode) and (FaceNum in Skeleton.SkeletonNodeList.List[2].FaceOnNode)):
            FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
            FaceFound = 1
            break
   if FaceFound == 0: # If face not found 
       FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'TRIANGLE')
       ListOfFace.Add_Face(FaceElmt) # can it be defined now ?!
       NbMeshElement = NbMeshElement + 1
       ListOfMeshElementNum.append(ListOfFace.NbFace) # Add FaceId in MeshElementNum list
       FaceElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List 

   #TempList is the temporary list of Edge that live on the triangle
   TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]     # First Edge
   TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2]]) # Second Edge
   TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]]) # Third Edge

   FoundEdgeList = []
   for EdgeList in TempEdgeList: # Go through the list of edge
       EdgeFound = 0
       for EdgeNum in EdgeList[0].EdgeOnNode: # Go throuh the list of Edge that live on first Node
         # If Edge has already been identified as an edge living on first node one get it back
           if ((EdgeNum in EdgeList[1].EdgeOnNode) and (EdgeNum not in FoundEdgeList)):
               EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
               EdgeFound = 1
               break
       if EdgeFound == 0: # if Edge on Triangle is not found, Edge created
           EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,EdgeList[0],EdgeList[1])
           # ERROR EdgeElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List
           EdgeElmt.MeshElementNodeList = [EdgeList[0],EdgeList[1]] 
           NbMeshElement = NbMeshElement+1
           ListOfEdge.Add_Edge(EdgeElmt)
           ListOfMeshElementNum.append(ListOfEdge.NbEdge)
       FoundEdgeList.append(EdgeElmt.Id)
       FaceElmt.Add_Edge(EdgeElmt)
       Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)

   for TempEdge in FaceElmt.Connection:
      TempEdge.SkeletonId.append(Skeleton.Id)

   Skeleton.SkeletonFaceList.Add_Face(FaceElmt)
   FaceElmt.SkeletonId.append(Skeleton.Id)
   FaceElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List
   return FaceElmt






def Convert_Quadrangle(Skeleton):
   global ListOfEdge,ListOfEdgeNode,ListOfFace,ListeOfFaceNode,NbMeshElement,ListOfMeshElementNum
   for TempNode in Skeleton.SkeletonNodeList.List:
      TempNode.SkeletonId.append(Skeleton.Id)
   # To be updated
   TempList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
   TempList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3]])
   TempList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
   TempList.append([Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
   Elmt = Face(NbMeshElement,ListOfFace.NbFace+1,'QUADRANGLE')
   FoundEdgeList = []
   for List in TempList:
      EdgeFound = 0
      for EdgeNum in List[0].EdgeOnNode:
         if ((EdgeNum in List[1].EdgeOnNode) and (EdgeNum not in FoundEdgeList)):
            EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
            EdgeFound = 1
            break
      if EdgeFound == 0:
         EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,List[0],List[1])
         NbMeshElement = NbMeshElement+1
         ListOfEdge.Add_Edge(EdgeElmt)
         ListOfMeshElementNum.append(ListOfEdge.NbEdge)
      FoundEdgeList.append(EdgeElmt.Id)
      Elmt.Add_Edge(EdgeElmt)
      Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)
   for TempEdge in Elmt.Connection:
      TempEdge.SkeletonId.append(Skeleton.Id)
   Elmt.Modify_Id(NbMeshElement)
   NbMeshElement = NbMeshElement+1
   ListOfFace.Add_Face(Elmt)
   Skeleton.SkeletonFaceList.Add_Face(Elmt)
   ListOfMeshElementNum.append(ListOfFace.NbFace)
   Elmt.SkeletonId.append(Skeleton.Id)
   Elmt.Init_NodeList(Skeleton.SkeletonNodeList.List)
   return Elmt

def Convert_Tetrahedron(Skeleton):
   global ListOfEdge,ListOfFace,ListOfCell,NbMeshElement,ListOfMeshElementNum
   for TempNode in Skeleton.SkeletonNodeList.List:
      TempNode.SkeletonId.append(Skeleton.Id)
   TempFaceList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[3]]]
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[1]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3],Skeleton.SkeletonNodeList.List[2]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
   #XXX
   CellElmt = Cell(NbMeshElement,ListOfCell.NbCell+1,'TETRAHEDRON')
   CellElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List
   NbMeshElement = NbMeshElement + 1
   # Since cell is created it has to be added in the list of cells which live on the 4 corresponding nodes
   for NodeElmt in Skeleton.SkeletonNodeList.List:
      NodeElmt.CellOnNode.append(CellElmt.Id)
   ListOfCell.Add_Cell(CellElmt)
   ListOfMeshElementNum.append(ListOfCell.NbCell)
   # we do not have to check duplication of cell element
   FoundFaceList = []
   for FaceList in TempFaceList: # loop over face associated with cell, describe by list of three nodes
      FaceFound = 0
      for FaceNum in FaceList[0].FaceOnNode: # loop over face ids associated with first node of the list of three nodes
         if ((FaceNum in FaceList[1].FaceOnNode) and (FaceNum in FaceList[2].FaceOnNode) and (FaceNum not in FoundFaceList)):
            FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
            FaceFound = 1 
            # If Face of Id FaceNum is in the list of FaceOnNode for the three node of Face "List"
            # then this face has already been referenced (as a mesh element or a skeleton) 
            # since there is only one triangle based on three nodes 
            # XXX constraint on FoundFaceList
            break
      if FaceFound == 0: # If face not found ?!
         # XXX
         FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'TRIANGLE')
         # ERROR FaceElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List
         FaceElmt.MeshElementNodeList = [FaceList[0], FaceList[1], FaceList[2]] 
         ListOfFace.Add_Face(FaceElmt) # can it be defined now ?!
         NbMeshElement = NbMeshElement + 1
         ListOfMeshElementNum.append(ListOfFace.NbFace) # Add FaceId in MeshElementNum list
         # create new face and check existence of associated edge
         # XXX created with same NbMeshElement =  MeshElementId
         #TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
         #TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2]])
         #TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
         # XXX why the list reduce to 3 specifics edges  different from FaceList ?
         TempEdgeList = [[FaceList[0],FaceList[1]]]
         TempEdgeList.append([FaceList[0],FaceList[2]])
         TempEdgeList.append([FaceList[1],FaceList[2]])
         FoundEdgeList = []
         for EdgeList in TempEdgeList:
            EdgeFound = 0
            for EdgeNum in EdgeList[0].EdgeOnNode:
               if ((EdgeNum in EdgeList[1].EdgeOnNode) and (EdgeNum not in FoundEdgeList)):
                  EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
                  EdgeFound = 1
                  break
            if EdgeFound == 0:
               #If Edge not found, create new edge
               #EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,List[0],List[1])
               # XXX why should it related ti List[0] and List[1]
               # and  not EdgeList ?!
               EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,EdgeList[0],EdgeList[1])
               NbMeshElement = NbMeshElement+1
               ListOfEdge.Add_Edge(EdgeElmt) # Add new edge to the list of edge (automatically incremente NbEdge)
               ListOfMeshElementNum.append(ListOfEdge.NbEdge) # Add EdgeId in MeshElementNum list
               # EdgeElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List
               EdgeElmt.MeshElementNodeList = [EdgeList[0], EdgeList[1]]
               # XXX Now NbMeshElement is increased by one ...
            FoundEdgeList.append(EdgeElmt.Id)
            FaceElmt.Add_Edge(EdgeElmt)
            # XXX avoid redondant item in the list
            if EdgeElmt not in Skeleton.SkeletonEdgeList.List:
               Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)
         for TempEdge in FaceElmt.Connection:
            TempEdge.SkeletonId.append(Skeleton.Id)
         #FaceElmt.Modify_Id(NbMeshElement)
         #NbMeshElement = NbMeshElement+1
         #ListOfFace.Add_Face(FaceElmt)
         #ListOfMeshElementNum.append(ListOfFace.NbFace)
      # At this point, Face has been found or created
      FoundFaceList.append(FaceElmt.Id)
      CellElmt.Add_Face(FaceElmt)
      # XXX avoid redondant item in the list
      if FaceElmt not in Skeleton.SkeletonFaceList.List:
         Skeleton.SkeletonFaceList.Add_Face(FaceElmt)
      # If faceFound = 1 then one checklist of associated edge
      if FaceFound == 1:
         for EdgeElmt in FaceElmt.Connection:
            if EdgeElmt.Id not in Skeleton.SkeletonEdgeList.IdList:
               Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt) 
   for TempFace in CellElmt.Connection:
      TempFace.SkeletonId.append(Skeleton.Id)
   #Elmt.Modify_Id(NbMeshElement)
   #NbMeshElement = NbMeshElement+1
   #ListOfCell.Add_Cell(Elmt)
   # XXX avoid redondant item in the list
   if CellElmt not in  Skeleton.SkeletonCellList.List:
      Skeleton.SkeletonCellList.Add_Cell(CellElmt)
   #ListOfMeshElementNum.append(ListOfCell.NbCell)
   CellElmt.SkeletonId.append(Skeleton.Id) # list of skeleton Id to which it belong
   CellElmt.MeshElementNodeList = Skeleton.SkeletonNodeList.List # Node list associated with Cell defined (4 nodes)
   return CellElmt

def Convert_Hexahedron(Skeleton):
   global ListOfEdge,ListOfFace,ListOfCell,NbMeshElement,ListOfMeshElementNum
   for TempNode in Skeleton.SkeletonNodeList.List:
      TempNode.SkeletonId.append(Skeleton.Id)
   TempFaceList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[5],Skeleton.SkeletonNodeList.List[4]]]
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[1]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[4],Skeleton.SkeletonNodeList.List[7],Skeleton.SkeletonNodeList.List[3]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[6],Skeleton.SkeletonNodeList.List[5]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[4],Skeleton.SkeletonNodeList.List[7],Skeleton.SkeletonNodeList.List[6]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[4],Skeleton.SkeletonNodeList.List[5],Skeleton.SkeletonNodeList.List[6],Skeleton.SkeletonNodeList.List[7]])
   Elmt = Cell(NbMeshElement,ListOfCell.NbCell+1,'HEXAHEDRON')
   FoundFaceList = []
   for List in TempFaceList:
      FaceFound = 0
      for FaceNum in List[0].FaceOnNode:
         if ((FaceNum in List[1].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum not in FoundFaceList)):
            FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
            FaceFound = 1
            break
      if FaceFound == 0:
         TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
         TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3]])
         TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
         TempEdgeList.append([Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
         FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'QUADRANGLE')
         FoundEdgeList = []
         for EdgeList in TempEdgeList:
            EdgeFound = 0
            for EdgeNum in EdgeList[0].EdgeOnNode:
               if ((EdgeNum in EdgeList[1].EdgeOnNode) and (EdgeNum not in FoundEdgeList)):
                  EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
                  EdgeFound = 1
                  break
            if EdgeFound == 0:
               EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,List[0],List[1])
               NbMeshElement = NbMeshElement+1
               ListOfEdge.Add_Edge(EdgeElmt)
               ListOfMeshElementNum.append(ListOfEdge.NbEdge)
            FoundEdgeList.append(EdgeElmt.Id)
            FaceElmt.Add_Edge(EdgeElmt)
            Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)
         for TempEdge in FaceElmt.Connection:
            TempEdge.SkeletonId.append(Skeleton.Id)
         FaceElmt.Modify_Id(NbMeshElement)
         NbMeshElement = NbMeshElement+1
         ListOfFace.Add_Face(FaceElmt)
         ListOfMeshElementNum.append(ListOfFace.NbFace)
      FoundFaceList.append(FaceElmt.Id)
      Elmt.Add_Face(FaceElmt)
      Skeleton.SkeletonFaceList.Add_Face(FaceElmt)
   for TempFace in Elmt.Connection:
      TempFace.SkeletonId.append(Skeleton.Id)
   Elmt.Modify_Id(NbMeshElement)
   NbMeshElement = NbMeshElement+1
   ListOfCell.Add_Cell(Elmt)
   Skeleton.SkeletonCellList.Add_Cell(Elmt)
   ListOfMeshElementNum.append(ListOfCell.NbCell)
   Elmt.SkeletonId.append(Skeleton.Id)
   Elmt.Init_NodeList(Skeleton.SkeletonNodeList.List)
   return Elmt

def Convert_Prism(Skeleton):
   global ListOfEdge,ListOfFace,ListOfCell,NbMeshElement,ListOfMeshElementNum
   for TempNode in Skeleton.SkeletonNodeList.List:
      TempNode.SkeletonId.append(Skeleton.Id)
   TempFaceList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[3]]]
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[1]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3],Skeleton.SkeletonNodeList.List[2]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
   Elmt = Cell(NbMeshElement,ListOfCell.NbCell+1,'PRISM')
   FoundFaceList = []
   for List in TempFaceList:
      FaceFound = 0
      for FaceNum in List[0].FaceOnNode:
         if len(List) == 3:
            if ((FaceNum in List[1].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum not in FoundFaceList)):
               FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
               FaceFound = 1
               break
         else:
            if ((FaceNum in List[1].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum not in FoundFaceList)):
               FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
               FaceFound = 1
               break
      if FaceFound == 0:
         if len(List) > 3:
            TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3]])
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
            FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'QUADRANGLE')
         else:
            TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2]])
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
            FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'TRIANGLE')
         FoundEdgeList = []
         for EdgeList in TempEdgeList:
            EdgeFound = 0
            for EdgeNum in EdgeList[0].EdgeOnNode:
               if ((EdgeNum in EdgeList[1].EdgeOnNode) and (EdgeNum not in FoundEdgeList)):
                  EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
                  EdgeFound = 1
                  break
            if EdgeFound == 0:
               EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,List[0],List[1])
               NbMeshElement = NbMeshElement+1
               ListOfEdge.Add_Edge(EdgeElmt)
               ListOfMeshElementNum.append(ListOfEdge.NbEdge)
            FoundEdgeList.append(EdgeElmt.Id)
            FaceElmt.Add_Edge(EdgeElmt)
            Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)
         for TempEdge in FaceElmt.Connection:
            TempEdge.SkeletonId.append(Skeleton.Id)
         FaceElmt.Modify_Id(NbMeshElement)
         NbMeshElement = NbMeshElement+1
         ListOfFace.Add_Face(FaceElmt)
         ListOfMeshElementNum.append(ListOfFace.NbFace)
      FoundFaceList.append(FaceElmt.Id)
      Elmt.Add_Face(FaceElmt)
      Skeleton.SkeletonFaceList.Add_Face(FaceElmt)
   for TempFace in Elmt.Connection:
      TempFace.SkeletonId.append(Skeleton.Id)
   Elmt.Modify_Id(NbMeshElement)
   NbMeshElement = NbMeshElement+1
   ListOfCell.Add_Cell(Elmt)
   Skeleton.SkeletonCellList.Add_Cell(Elmt)
   ListOfMeshElementNum.append(ListOfCell.NbCell)
   Elmt.SkeletonId.append(Skeleton.Id)
   Elmt.Init_NodeList(Skeleton.SkeletonNodeList.List)
   return Elmt

def Convert_Pyramid(Skeleton):
   global ListOfEdge,ListOfFace,ListOfCell,NbMeshElement,ListOfMeshElementNum
   for TempNode in Skeleton.SkeletonNodeList.List:
      TempNode.SkeletonId.append(Skeleton.Id)
   TempFaceList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[3]]]
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[1]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3],Skeleton.SkeletonNodeList.List[2]])
   TempFaceList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
   Elmt = Cell(NbMeshElement,ListOfCell.NbCell+1,'PYRAMID')
   FoundFaceList = []
   for List in TempFaceList:
      FaceFound = 0
      for FaceNum in List[0].FaceOnNode:
         if len(List) == 3:
            if ((FaceNum in List[1].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum not in FoundFaceList)):
               FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
               FaceFound = 1
               break
         else:
            if ((FaceNum in List[1].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum in List[2].FaceOnNode) and (FaceNum not in FoundFaceList)):
               FaceElmt = ListOfFace.List[ListOfMeshElementNum[FaceNum-1]-1]
               FaceFound = 1
               break
      if FaceFound == 0:
         if len(List) > 3:
            TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[3]])
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[2],Skeleton.SkeletonNodeList.List[3]])
            FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'QUADRANGLE')
         else:
            TempEdgeList = [[Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[1]]]
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[0],Skeleton.SkeletonNodeList.List[2]])
            TempEdgeList.append([Skeleton.SkeletonNodeList.List[1],Skeleton.SkeletonNodeList.List[2]])
            FaceElmt = Face(NbMeshElement,ListOfFace.NbFace+1,'TRIANGLE')
         FoundEdgeList = []
         for EdgeList in TempEdgeList:
            EdgeFound = 0
            for EdgeNum in EdgeList[0].EdgeOnNode:
               if ((EdgeNum in EdgeList[1].EdgeOnNode) and (EdgeNum not in FoundEdgeList)):
                  EdgeElmt = ListOfEdge.List[ListOfMeshElementNum[EdgeNum-1]-1]
                  EdgeFound = 1
                  break
            if EdgeFound == 0:
               EdgeElmt = Edge(NbMeshElement,ListOfEdge.NbEdge+1,List[0],List[1])
               NbMeshElement = NbMeshElement+1
               ListOfEdge.Add_Edge(EdgeElmt)
               ListOfMeshElementNum.append(ListOfEdge.NbEdge)
            FoundEdgeList.append(EdgeElmt.Id)
            FaceElmt.Add_Edge(EdgeElmt)
            Skeleton.SkeletonEdgeList.Add_Edge(EdgeElmt)
         for TempEdge in FaceElmt.Connection:
            TempEdge.SkeletonId.append(Skeleton.Id)
         FaceElmt.Modify_Id(NbMeshElement)
         NbMeshElement = NbMeshElement+1
         ListOfFace.Add_Face(FaceElmt)
         ListOfMeshElementNum.append(ListOfFace.NbFace)
      FoundFaceList.append(FaceElmt.Id)
      Elmt.Add_Face(FaceElmt)
      Skeleton.SkeletonFaceList.Add_Face(FaceElmt)
   for TempFace in Elmt.Connection:
      TempFace.SkeletonId.append(Skeleton.Id)
   Elmt.Modify_Id(NbMeshElement)
   NbMeshElement = NbMeshElement+1
   ListOfCell.Add_Cell(Elmt)
   Skeleton.SkeletonCellList.Add_Cell(Elmt)
   ListOfMeshElementNum.append(ListOfCell.NbCell)
   Elmt.SkeletonId.append(Skeleton.Id)
   Elmt.Init_NodeList(Skeleton.SkeletonNodeList.List)
   return Elmt

Convert_Skeleton2Mesh = {}
Convert_Skeleton2Mesh['1'] = Convert_Line
Convert_Skeleton2Mesh['2'] = Convert_Triangle
Convert_Skeleton2Mesh['3'] = Convert_Quadrangle
Convert_Skeleton2Mesh['4'] = Convert_Tetrahedron
Convert_Skeleton2Mesh['5'] = Convert_Hexahedron
Convert_Skeleton2Mesh['6'] = Convert_Prism
Convert_Skeleton2Mesh['7'] = Convert_Pyramid
Convert_Skeleton2Mesh['15'] = Convert_Point

def Reset_Variables():
   global ListOfNode,ListOfSkeletonElement,ListOfMeshGroup,ListOfOldNodeNum,ListOfNewNodeNum,ListOfOldSkeletonElmtNum,ListOfNewSkeletonElmtNum,ListOfMeshElementNum,ListOfEdge,ListOfFace,ListOfCell,ListOfMeshElement,NbMeshElement,ListOfNodeId

   ListOfNode = NodeList()
   ListOfEdge = EdgeList()
   ListOfFace = FaceList()
   ListOfCell = CellList()
   ListOfNodeId = []
   ListOfSkeletonElement = SkeletonElementList()
   ListOfMeshGroup = MeshGroupList()
   ListOfMeshElement = []
   ListOfMeshElementNum = []
   ListOfOldNodeNum = []
   ListOfNewNodeNum = []
   ListOfOldSkeletonElmtNum = []
   ListOfNewSkeletonElmtNum = []
   NbMeshElement = 1

def Convert(InputList,ListOfGeoElement,ListOfGeoGroup):
   global FileIn,ListOfNode,ListOfEdge,ListOfFace,ListOfCell,ListOfMeshElement,ListOfMeshGroup,ListOfSkeletonElement,ListOfOldNodeNum,ListOfOldSkeletonElmtNum,ListOfNewNodeNum,ListOfNewSkeletonElmtNum,NbMeshElement,LineCounter,ListOfMeshElementNum,ListOfNodeId
   Reset_Variables()
   for FileNameIn in InputList:
      if not os.path.isfile(FileNameIn):
         print ' No such file ',FileNameIn,',check the path'
         break
      print ' Read the input file:',FileNameIn
      FileIn = open(FileNameIn,"r")
      while 1:
         NextLine = FileIn.readline()
         LineCounter = LineCounter+1
         if NextLine[0:4]=='$NOD':
            break
      FileIn.readline()
      LineCounter = LineCounter+1
      while 1:
         NextLine = FileIn.readline()
         LineCounter = LineCounter+1
         if NextLine[0:7] == '$ENDNOD':
            break
         Field = string.split(NextLine)
         ListOfOldNodeNum.append(string.atoi(Field[0]))
         ListOfNewNodeNum.append(NbMeshElement)
         for i in range(string.atoi(Field[0])-len(ListOfNodeId)-1):
            ListOfNodeId.append(-1)
         ListOfNodeId.append(NbMeshElement)
         TempNode = Node(NbMeshElement,string.atoi(Field[0]),string.atof(Field[1]),string.atof(Field[2]),string.atof(Field[3]))
         NbMeshElement = NbMeshElement+1
         ListOfNode.Add_Node(TempNode)
         ListOfMeshElementNum.append(ListOfNode.NbNode-1)
      while 1:
         NextLine = FileIn.readline()
         LineCounter = LineCounter+1
         if NextLine[0:4]=='$ELM':
            break
      FileIn.readline()
      LineCounter = LineCounter+1
      Counter = 1

###########################################################################
#                                                                         #
#                            TEMPORARY                                    #
#                                                                         #
###########################################################################
                                                                          #
      print ' Start'                                                      #
      StartTime = time.time()                                             #
                                                                          #
###########################################################################

      while 1:
         NextLine = FileIn.readline()
         LineCounter = LineCounter+1
         if NextLine[0:7] == '$ENDELM':
            break
         Field = string.split(NextLine)
         TempNodeList = NodeList()
         for NodeNumber in Field[5:]:
            TempNum = ListOfNodeId[string.atoi(NodeNumber)-1]
            TempNodeList.Add_Node(ListOfNode.List[TempNum-1])
         ListOfOldSkeletonElmtNum.append(string.atoi(Field[0])) # keep old Id from msh file
         ListOfNewSkeletonElmtNum.append(Counter)               # Set new Id
         SkeletonElmt = SkeletonElement(Counter, Convert_Type[Field[1]], TempNodeList) # Set Skeleton Elmt and node list

         Counter = Counter+1
         SkeletonElmt.GeoGroup = ListOfGeoGroup.List[ListOfGeoGroup.IdList.index(string.atoi(Field[2]))]
         SkeletonElmt.GeoElement = ListOfGeoElement.List[ListOfGeoElement.IdList.index(string.atoi(Field[3]))]

         ListOfSkeletonElement.Add_Element(SkeletonElmt)
         #XXX print  'First ',SkeletonElmt.SkeletonEdgeList.IdList

         MeshElmt = Convert_Skeleton2Mesh[Field[1]](SkeletonElmt)
         #XXX problem if Elmt already defined in mesh element list ?

         #print 'Last',SkeletonElmt.SkeletonEdgeList.IdList
         #XXX control = raw_input()
         SkeletonElmt.SkeletonMeshElement = MeshElmt

###########################################################################
#                                                                         #
#                            TEMPORARY                                    #
#                                                                         #
###########################################################################
                                                                          #
      EndTime = time.time()                                               #
      Min = int((EndTime-StartTime)/60)                                   #
      Sec = (((EndTime-StartTime)/60)-Min)*60                             #
      print ' Time =',Min,'Mn',Sec,'S'                                    #
                                                                          #
###########################################################################

      FileIn.close()
   ListOfNodeNum = [ListOfOldNodeNum,ListOfNewNodeNum]
   ListOfSkeletonElmtNum = [ListOfOldSkeletonElmtNum,ListOfNewSkeletonElmtNum]
   ListOfMeshElement = [ListOfNode,ListOfEdge,ListOfFace,ListOfCell]
   return ListOfMeshElement,ListOfNodeNum,ListOfSkeletonElement,ListOfSkeletonElmtNum,ListOfMeshGroup,

