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
   print "Error: impossible to load the VTK stuff"
   
try:
    import PostProcessing.Lib.JavaLib
except:
   #print "Error: impossible to load the java VTK stuff"
   SilenciousERror = 1

class vtkParticleTrajectoryBuilder:
    '''
    Builds a vtk unstructured grid from the SPIS-UI mesh structure.
    '''
        
    def __init__(self, nodeList):
       '''
       This build a vtk grid builder. 
       '''
      
       self.cellTypes ={}
       self.cellTypes['VTK_EMPTY_CELL'] = 0
       self.cellTypes['VTK_VERTEX'] = 1
       self.cellTypes['VTK_POLY_VERTEX'] = 2
       self.cellTypes['VTK_LINE'] = 3
       self.cellTypes['VTK_POLY_LINE'] = 4
       
       
       self.pts = vtkPoints()
       self.gd = vtkUnstructuredGrid()

       self.nodeList = nodeList
       
       self.cellList= []
       for node in self.nodeList[0:-1]:
           tmpIndex = self.nodeList.index(node)
           self.cellList.append((tmpIndex, tmpIndex+1))
       
       self.NbNode = len(self.nodeList)
       print "NbNode = ", self.NbNode
       self.NbCell = len(self.cellList)
       print "NbCell = ", self.NbCell
       
       self.gd.Allocate( self.NbCell, self.NbNode)
       
       self.cellType = 4
       
    def buildGrid(self):
        '''
        Generate the grid.
        '''
        
        # node building
        #self.Size = 0
        #for node in self.nodeList:
        #    if self.Size < self.node.Id: self.Size = self.node.Id
        #invCorrList = range(self.Size+1)                #range(len(self.nodeList)+1)
        
        vtkIndex = 0
        for node in self.nodeList:
            #print "Node Id in build", self.node.Id
            #invCorrList[self.node.Id] = vtkIndex
            self.pts.InsertPoint( vtkIndex, node[0], node[1], node[2])
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
            for cell in self.cellList:
                IdList = vtkIdList()
                for node in cell:
                    IdList.InsertNextId(node)
                
                self.gd.InsertNextCell( self.cellType, IdList) #10 corresponds to cell of type tethraedron

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
