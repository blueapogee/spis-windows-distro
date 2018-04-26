"""
**File name:**    vtkIO.py

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


from shared                                             import sharedData
from shared                                             import shared
from shared                                             import sharedFrames

from vtk import vtkDataSetWriter
import Modules.PostProcessing.Lib.JavaLib

import sys, os, string
from Bin.config import GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)
from Bin.config import GL_DATA_PATH, GL_CMD_GMSH, GL_CMD_TETGEN, GL_CMD_MEDIT, GL_GMSH_OUT_PATH, GL_VTK_EXCHANGE


class vtkIO:
        """  Class of vtk file I/O """

        def __init__(self):
            print "Export to VTK format module"
            self.BUILD_DATA_PATH = 'ON'

          
        def setOutputFileNameRoot(self, fileNameRootIn):
            self.fileNameRoot = fileNameRootIn
                  

        ##############################################################
        #  method of export to the VTK file format                   #
        ##############################################################
        def exportVTK(self, vtkDataSetIn):
 
                self.currentVtkDataSet = vtkDataSetIn

                if self.currentVtkDataSet != None:
                    self.vtkWriter = vtkDataSetWriter()
                    self.vtkWriter.SetInput(self.currentVtkDataSet)
                    self.vtkWriter.SetFileTypeToBinary()
                    self.fileNameRoot = self.fileNameRoot+".vtk"
                    if self.BUILD_DATA_PATH == 'ON':
                       self.fileName = os.path.join(GL_VTK_EXCHANGE, self.fileNameRoot)
                    else:
                       self.fileName = self.fileNameRoot
                    print self.fileName
                    self.vtkWriter.SetFileName(self.fileName)
                    self.vtkWriter.Write()
                    print "export VTK done"
                else:
                    print "Error: No vtkDataSet defined. Please build one before."
