"""
Module of visualisation of the mesh structure. This module will 
generate the VTK unstructured grid corresponding to the mesh structure.

**File name:**    ViewPipeLine2.py

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

import os
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH

try:
    #if(1):
    from com.artenum.free.mesh.vtk import VtkGridBuilder
except:
    print "Error in ViewPipeLine2: impossible to load VtkGridBuilder from com.artenum.free.mesh.vtk"

try:
    #if(1):
    from Modules.InOut.vtkIO import vtkIO
    from vtk import vtkDataSetMapper
    from vtk import vtkActor
except:
    print "Impossible to load VTK modules in ViewPipeLine2"

class ViewPipeLine2:
  '''
  Class of visualisation of the mesh structure. This class will
  generate the VTK unstructured grid corresponding to the mesh structure.
  '''

  def __init__(self):
        print "Viewing pipeline 2 loaded: mesh grid visualisation"

        
  def run(self, mesh):

        print"Lib and modules loading"
        try:
            from Modules.PostProcessing.Include.vtkGridBuilder import vtkGridBuilder
            from Modules.PostProcessing.Modules.Color import Color
            
            import Modules.InOut.vtkIO
            from Modules.InOut.vtkIO import vtkIO
            print "modules loaded"
        except:
            print "impossible to load the VTK modules"

        
        self.myColor=Color(12)
        self.myColor.ContiniousColors()          
          
        # output as wireFrame 
        self.grdBuilder = VtkGridBuilder(mesh, 3)
        self.grdBuilder.buildVtkUnstructuredGrid()
        
        self.grdMp = vtkDataSetMapper()
        self.grdMp.SetInput(self.grdBuilder.getVtkDataSet())
        self.grdAct = vtkActor()
        self.grdAct.SetMapper(self.grdMp)

        self.colorIndex=5
        self.grdAct.GetProperty().SetDiffuseColor(self.myColor.Color[self.colorIndex][0], self.myColor.Color[self.colorIndex][1], self.myColor.Color[self.colorIndex][2])
             
        #sharedVTK['VTKDataSet'].append(self.grdBuilder.getVtkDataSet())
        #sharedVTK['VTKListActor'].append(["3D Mesh", self.grdAct])
        #sharedVTK['VTKObjectType'].append("VTK_UGRID")
        print "Done"
        
        
  def writeOutputFile(self):
        self.fileNameRoot = os.path.join(GL_DATA_PATH,"Vtk","mesh")
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
