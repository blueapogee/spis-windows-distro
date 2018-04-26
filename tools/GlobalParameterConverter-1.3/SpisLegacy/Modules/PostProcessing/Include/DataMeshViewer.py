"""
Converts a given DataField and its related MeshField to an unstructured vtkDataSet. Various
conversions are possible dependingon the initial localisation of teh data and the final
type of viewing cell type.

**File name:**    DataMeshViewer.py

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

         
import time, java
         
from Bin.Tasks.shared import shared
from Bin.Tasks.shared import sharedData


from com.artenum.free.mesh.vtk    import *
from com.artenum.free.mesh.util   import NodeData
from com.artenum.free.mesh.util   import CountBasicMeshObjectAndFilter
from Modules.Utils.ListCleaner     import ListCleaner
from Modules.Utils.pyIterator      import pyIterator


class DataMeshViewer:
    '''
    Converts a given DataField and its related MeshField to an unstructured vtkDataSet. Various 
    conversions are possible depending on the initial localisation of the data and the final 
    type of visualisation cell.
    
    For data localised in the computational volume:
            
    Data on Node (local = 0):
            
         to Node (localOut = 0), for discrete representation of node loacated data (e.g flags)

         to Edge (localOut = 1), wireframe representation with linear interpolation between nodes

         to Surface (localOut = 2), face representation with linear interpolation between nodes

         to Cell (localOut = 3), cell repsentation with linear interpolation 
         between nodes, typically for volumicc representation of continuous data.

    Data on Edge (localIn = 1):
            
         to Edge (localOut = 1), discrete (edge by edge) wireframe representation (e.g flags)
         
    Data on Face (localIn = 2):
            
         to Face (localOut = 2), discrete (face by face) face representation (e.g flags)
            
    Data on Edge (localIn = 3):
            
         to Cell (localOut = 3), discrete (edge by edge) edge representation (e.g flags)
            
    For data localised on a surface (e.g the surface of the spacecraft)
    
    Data on Node (local = 0):
            
         to Node (localOut = 0), for discrete representation of node loacated data (e.g flags)

         to Edge (localOut = 1), wireframe representation with linear interpolation between nodes

         to Surface (localOut = 2), face representation with linear interpolation between nodes
            
    Data on Edge (localIn = 1):
            
         to Edge (localOut = 1), discrete (edge by edge) wireframe representation (e.g flags)
         
    Data on Face (localIn = 2):
            
         to Face (localOut = 2), discrete (face by face) face representation (e.g flags)
            
    '''
    
    def __init__(self, dataField, meshField, mesh, localIn, localOut):
        '''
        Main constructor. localIn should correspond to the localisation of the data on the 
        computational grid. localOut in the localisation (i.e type of cell) on the visualisation
        grid. 
        '''
        
        self.dataField = dataField
        self.meshField = meshField
        self.mesh = mesh
        self.localIn = localIn
        self.localOut = localOut
        self.cellType = (1, 3, 5, 10)
        self.filter = CountBasicMeshObjectAndFilter(self.localOut + 1) #ATTENTION: works only if node, line, tri, tetra
        if self.dataField.Name == None:
            self.name = "Data"
        else:
            self.name = self.dataField.Name + "(" + self.dataField.Unit + ")"
        print self.name
        
        self.VERBOSE = 1
        
    def convertData(self):
        '''
        Convert the data set and extract the filtered data. Should be called before buildVtkDataSet(). 
        '''
        
        if self.VERBOSE > 2:
            print "Time of cell and node identification" 
            StartTime = time.time()
        
        if (self.localIn == 0): 
            if (self.localOut == 0): # From node to node
                self.ptsList = self.meshField.MeshElementList
                if self.VERBOSE > 2:
                    print "Number of Nodes= ", len(self.ptsList)
                self.targetedCells = self.meshField.MeshElementList
                if self.VERBOSE > 1:
                    print "Conversion done"   
            else:    
                if self.localOut == 1: # From node to edge
                    self.targetedCells = self.mesh.getEdgeOnNodes(pyIterator(self.meshField.MeshElementList))
                if self.localOut == 2: # From node to face
                    self.targetedCells = self.mesh.getFaceOnNodes(pyIterator(self.meshField.MeshElementList))
                if self.localOut == 3:  # From node to cell
                    self.targetedCells = self.mesh.getCellOnNodes(pyIterator(self.meshField.MeshElementList))
                
                # definition of the cell type
                self.magic = self.localOut   
                self.ptsList = self.meshField.MeshElementList
                if self.VERBOSE > 1:
                    print "Conversion ", self.localIn, " to ", self.localOut, " done"
            
        elif(self.localIn == 3):     # From cell to cell (we can map volumic data only on cell)
            self.localOut = 3
            self.filter = CountBasicMeshObjectAndFilter(1)
            
            filteredList = java.util.ArrayList()
            for cell in self.meshField.MeshElementList:
                for node in cell.getNodes():
                    filteredList.add(node)

            # Filter data
            self.filter.setDataToFilter(filteredList, self.mesh.getLastNodeId())

            self.ptsList = self.filter.getFilteredData()
            self.targetedCells = self.meshField.MeshElementList
            if self.VERBOSE > 1:
                print "Conversion done"   

        elif(self.localIn == 2): 
            if (self.localOut == 2): # From face to face
                self.filter = CountBasicMeshObjectAndFilter(1)
                
                filteredList = java.util.ArrayList()
                for face in self.meshField.MeshElementList:
                   for i in xrange(face.getSize()):
                      filteredList.add(face.getNode(i))

                # Filter data
                self.filter.setDataToFilter(filteredList, self.mesh.getLastNodeId())

                self.ptsList = self.filter.getFilteredData()
                self.targetedCells = self.meshField.MeshElementList
                if self.VERBOSE > 1:
                    print "Conversion done"

            else: # From face to cell...
                print "conversion not implemented yet"
                    
        
        elif(self.localIn == 1):
            if (self.localOut == 1): # From edge to edge
                self.filter = CountBasicMeshObjectAndFilter(1)
                
                filteredList = java.util.ArrayList()
                for edge in self.meshField.MeshElementList:
                    filteredList.add(edge.getNode(0))
                    filteredList.add(edge.getNode(1))

                # Filter data
                self.filter.setDataToFilter(filteredList, self.mesh.getLastNodeId())

                self.ptsList = self.filter.getFilteredData()
                self.targetedCells = self.meshField.MeshElementList
                if self.VERBOSE > 1:
                    print "Conversion done"

            else:
                print "conversion not implemented yet"
                
        if self.VERBOSE > 2:
            EndTime = time.time()
            Min = int((EndTime - StartTime) / 60)
            Sec = (((EndTime - StartTime) / 60) - Min) * 60
            print ' Time =', Min, 'Mn', Sec, 'S'        

 
    def buildVtkDataSet(self):
        '''
        Builds the vtkDataSet itself ( i.e the vtkGrid and add the values to it). 
        '''
        print "In buildVtkDataSet "
        
        
        if self.VERBOSE > 2:
            print "Duration of vtkDataSetBuilder initialisation"
            StartTime = time.time()
        
        data = java.util.ArrayList()
        # detection if the data is a scalar or a vector
        try:
            dataSize = len(self.dataField.ValueList[0])
        except:
            dataSize = 1

        if dataSize == 1:
            print "data are scalars"
            for localData in self.dataField.ValueList:
                #print "In DataMeshViewer.buildVtkDataSet, value of local data ----->", localData       
                data.add(NodeData([localData]))
        else:
            "data are vectors"
            for localData in self.dataField.ValueList:
                #print "In DataMeshViewer.buildVtkDataSet, value of local data ----->", localData 
                data.add(NodeData(localData))
            print "In DataMeshViewer.buildVtkDataSet, value of local data ----->", localData

        print "Building of the vtkDataSet"    
        #self.builder = VtkDataSetBuilder( data , pyIterator(self.ptsList), pyIterator(self.targetedCells), len(self.ptsList), self.mesh.getLastNodeId(),len(self.targetedCells), self.cellType[self.localOut])
        self.builder = VtkDataSetBuilder(data , pyIterator(self.ptsList), pyIterator(self.targetedCells), self.mesh.getLastNodeId(), self.cellType[self.localOut])
        if self.VERBOSE > 1:
            print "cellType= ", self.cellType[self.localOut]
        # FIX ME
        #self.builder.setName(self.name)
        print "Data name= ", self.name

        if self.VERBOSE > 2:
            EndTime = time.time()
            Min = int((EndTime - StartTime) / 60)
            Sec = (((EndTime - StartTime) / 60) - Min) * 60
            print ' Time =', Min, 'Mn', Sec, 'S'   
        
            print "Duration of buildGrid()"
            StartTime = time.time()
            
        self.builder.buildVtkUnstructuredGrid()
        
        if self.VERBOSE > 2:
            EndTime = time.time()
            Min = int((EndTime - StartTime) / 60)
            Sec = (((EndTime - StartTime) / 60) - Min) * 60
            print ' Time =', Min, 'Mn', Sec, 'S'
        
        if (self.localIn == 0):
           self.builder.setValueToPoint()
           print "data centered on nodes"
        else:
           self.builder.setValueToCell()
           print "data centered on cell"
        print "vtkDataSet generated."
        
    def getVtkDataSet(self):
        '''
        returns the built vtkDataSet.
        '''
        return (self.builder.getVtkDataSet())

