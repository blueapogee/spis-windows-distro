"""
**File name:**    vtkGridBuilder.py

**Creation:**     2004/11/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      1.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Arsene Lupin                         | Creation                   |
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

import os

import java

# import the vtk stuff and its corresponding Java wrapping 
try:
   import vtk
   from vtk import vtkPoints
   from vtk import vtkUnstructuredGrid
   from vtk import vtkIdList
   from vtk import vtkDataSetWriter
except:
   print "Error in vtkGridBuilder: impossible to load the VTK stuff"
   
try:
#if(1):
    import Modules.PostProcessing.Lib.JavaLib
except:
   #print "Error in vtkGridBuilder: impossible to load the java VTK stuff"
   silenciousError = 1


class vtkGridBuilder:
    '''
    Builds a vtk unstructured grid from the SPIS-UI mesh structure.
    '''
        
    def __init__(self, nodeList, cellList, cellType = 10):
       '''
       This build a vtk grid builder. nodeList is the list of SPIS nodes
       (i.e shared['MeshElmtList'][0].List for the whole grid) and cellList is 
       the list of cells (i.e shared['MeshElmtList'][3].List for the whole grid
       built on tehraedrons).  The cell type is an integer and defined the 
       corresponding VTK cell type (e.g. 10 = tethraedron). The table below gives 
       the most classic combinaisons:
       
       nodeList = shared['MeshElmtList'][0].List
       edgeList = shared['MeshElmtList'][1].List
       faceList = shared['MeshElmtList'][2].List
       cellList = shared['MeshElmtList']["].List
       
       +---------------------+----------+----------+----------+
       | Type of output grid | nodeList | cellList | cellType |
       +---------------------+----------+----------+----------+
       + edges               | nodeList | edgeList |    3     |
       +---------------------+----------+----------+----------+
       + faces               | nodeList | faceList |    5     |
       +---------------------+----------+----------+----------+
       + cells               | nodeList | cellList |   10     |
       +---------------------+----------+----------+----------+
       '''
      
       self.cellTypes ={}
       self.cellTypes['VTK_EMPTY_CELL'] = 0
       self.cellTypes['VTK_VERTEX'] = 1
       self.cellTypes['VTK_POLY_VERTEX'] = 2
       self.cellTypes['VTK_LINE'] = 3
       self.cellTypes['VTK_POLY_LINE'] = 4
       self.cellTypes['VTK_TRIANGLE'] = 5
       self.cellTypes['VTK_TRIANGLE_STRIP'] = 6
       self.cellTypes['VTK_POLYGON'] = 7
       self.cellTypes['VTK_PIXEL'] = 8
       self.cellTypes['VTK_QUAD'] = 9
       self.cellTypes['VTK_TETRA'] = 10
       self.cellTypes['VTK_VOXEL'] = 11
       self.cellTypes['VTK_HEXAHEDRON'] = 12
       self.cellTypes['VTK_WEDGE'] = 13
       self.cellTypes['VTK_PYRAMID'] = 14
       
       self.pts = vtkPoints()
       self.gd = vtkUnstructuredGrid()

       self.nodeList = nodeList
       self.cellList = cellList
       
       self.NbNode = len(self.nodeList)
       print "NbNode = ", self.NbNode
       self.NbCell = len(self.cellList)
       print "NbCell = ", self.NbCell
       
       self.gd.Allocate( self.NbCell, self.NbNode)
       
       self.cellType = cellType
       
    def buildGrid(self):
        '''
        Generate the grid.
        '''
        #print "node generation"
        # node building
        self.Size = 0
        for self.node in self.nodeList:
            #print "nodeId", self.node.Id
            if self.Size < self.node.Id: self.Size = self.node.Id
        invCorrList = range(self.Size+1)                #range(len(self.nodeList)+1)
        vtkIndex = 0
        for self.node in self.nodeList:
            #print "Node Id in build", self.node.Id
            invCorrList[self.node.Id] = vtkIndex
            self.pts.InsertPoint( vtkIndex, self.node.Coord[0], self.node.Coord[1], self.node.Coord[2])
            vtkIndex = vtkIndex + 1
        
        self.gd.SetPoints(self.pts)

        print "cell generation"
        # we build the cells using the vtkIdList
        if (self.cellType==1 or self.cellType==2):   #special case if data localised on node and displayed on node
            for self.cell in self.cellList:
                self.IdList = vtkIdList()
                self.IdList.InsertNextId(invCorrList[self.cell.Id])

                self.gd.InsertNextCell( self.cellType, self.IdList) #10 corresponds to cell of type tethraedron
        else:
            for self.cell in self.cellList:
                self.IdList = vtkIdList()
                for self.node in self.cell.MeshElementNodeList:
                    self.IdList.InsertNextId(invCorrList[self.node.Id])
                
                self.gd.InsertNextCell( self.cellType, self.IdList) #10 corresponds to cell of type tethraedron

        invCorrList = None
        print "end of cell generation"
         
    def listCellTypes(self):
        '''
        Lists the available cell types and the corresponding number (i.e. tetrahedron = 10)
        '''
        for self.typeKey in self.cellTypes.keys():
            print self.typeKey, self.cellTypes[self.typeKey]
        
    def getVtkDataSet(self):
        '''
        returns the vtkDataSet corresponding to the grid.
        '''
        return (self.gd)
        
        
    def writeToFile(self, fileName):
        '''
        write a binary vtk file correspoding to the grid.
        '''
        vtkWriter = vtkDataSetWriter()
        vtkWriter.SetInput(self.gd)
        vtkWriter.SetFileTypeToBinary()
        vtkWriter.SetFileName(fileName)
        vtkWriter.Write()
