"""
groups visualisation pipeline. Must be used to visualise groups.

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 3.1.0   | Yves Le Rumeur                       | Modif                      |
|         | lerumeur@artenum.com                 |                            |
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
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks                  import common 
from Bin.Tasks.common           import ask_value
from Bin.Tasks.shared           import sharedGroups
from Bin.Tasks.shared           import shared

from Bin.config                 import GL_DATA_PATH, GL_SPISUIROOT_PATH

try:
    from com.artenum.free.mesh.vtk import VtkGridBuilder
except:
    loadingLogger.warn("Error in ViewPipeLine1: impossible to properly VtkGridBuilder from com.artenum.free.mesh.vtk \n"
                       +"Please check, if the path to JfreeMesh is properly set.")

try:
    import Modules.PostProcessing.Include
    from Modules.PostProcessing.Modules.Color import Color
    from vtk                 import vtkDataSetMapper
    from vtk                 import vtkActor
    from Modules.InOut.vtkIO import vtkIO
except:
    loadingLogger.warn(  "Error in ViewPipeLine1: Impossible to load the VTK modules \n"
                       + "Module ViewPipeLine1 of groups visualisation not operational")


class ViewPipeLine1:
   """
   Physical and properties groups visualisation.
   """
   def __init__(self):
       
       self.logger = LoggerFactory.getLogger("PostProcessingLogger")
       self.logger.info("Groups visualisation")
       
       self.colorSet = Color(len(shared["MeshGroupList"].List))
       self.colorSet.ColorsBySteps()
       self.colorIndex = 0 

   def run(self, geoGroupIndex):
       
        grp = shared["MeshGroupList"].List[geoGroupIndex]
        self.grpName = grp.Name
        currentMeshGroup = grp.jMeshGroup
     
        self.colorIndex = geoGroupIndex
     
        print "Generation of elements set"
        
        # Init VTK builder params
        nodeIterator = currentMeshGroup.getNodeIterator()
        meshElementIterator = None
        nbNode = currentMeshGroup.getNbNode()
        nbMeshElement = -1

        # setting of the grid type
        if grp.Type == "SURFACE GROUP":       # ameliorer cette procedure en cas de mismatching entre
            gridType = 5                       # type de groupe et de cellules.
            meshElementIterator = currentMeshGroup.getFaceIterator()
            nbMeshElement = currentMeshGroup.getNbFace()
        elif grp.Type == "CURVE GROUP":
            gridType = 3
            meshElementIterator = currentMeshGroup.getEdgeIterator()
            nbMeshElement = currentMeshGroup.getNbEdge()
        elif grp.Type == "POINT GROUP":
            gridType = 1
            meshElementIterator = currentMeshGroup.getNodeIterator()
            nbMeshElement = currentMeshGroup.getNbNode()
        else:
            gridType = 10
            meshElementIterator = currentMeshGroup.getCellIterator()
            nbMeshElement = currentMeshGroup.getNbCell()

        print grp.Name, " - grid type: ",gridType, " - Nb node: ", nbNode," - Nb Element: ", nbMeshElement

        self.grdBuilder = VtkGridBuilder(nodeIterator, meshElementIterator, shared["Mesh"].getLastNodeId(), gridType)
        self.grdBuilder.buildVtkUnstructuredGrid()
        
        self.grdMp = vtkDataSetMapper()
        self.grdMp.SetScalarVisibility(0) # in order to see the colorisation
        self.grdMp.SetInput(self.grdBuilder.getVtkDataSet())
        self.grdAct = vtkActor()
        self.grdAct.SetMapper(self.grdMp)
        
        self.grdAct.GetProperty().SetDiffuseColor(self.colorSet.Color[self.colorIndex][0], self.colorSet.Color[self.colorIndex][1], self.colorSet.Color[self.colorIndex][2])
        self.logger.info("Done")
        
        
   def writeOutputFile(self):
        self.fileNameRoot = self.grpName
        self.vtkExporter = vtkIO()
        self.vtkExporter.setOutputFileNameRoot(self.fileNameRoot)
        self.vtkExporter.exportVTK(self.grdBuilder.getVtkDataSet())
        
        
   def getDataSet(self):
        return(self.grdBuilder.getVtkDataSet())
        
   def getMapper(self):
        return(self.grdMp)
        
   def getActor(self):
        return(self.grdAct)
  
   def getOutputFileNameRoot(self):
        return(self.fileNameRoot)
         
