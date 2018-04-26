"""

**Project ref:**  Spis/SpisUI

**File name:**    TaskBuildAllVTKPipeline.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**Modification:**

**Use:**

**Description:**  This Task is used to build all the vtk pipeline of
		  visualization.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Arsene Lupin              | Definition/Creation        |
|                | lupin@artenum.com         |                            |
+----------------+---------------------------+----------------------------+

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

import sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared

import com.artenum.free.mesh.io.exporter.GmshExporter


sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE, GL_CASSANDRA_PLUGINS
sys.path.append(GL_SPISUIROOT_PATH)

import FileChooserSwing

class TaskExportToGmshMesh(Task):
    """exports to the Gmsh mesh format the loaded mesh structure"""
    desc="exports to the Gmsh mesh format the loaded mesh structure"
    
    def run_task(self):
        '''
        performs the task.
        '''
        self.logger = LoggerFactory.getLogger("Task")

        if  shared["Mesh"] != None:
             
            FileNameOut = str(FileChooserSwing.choose_save()).strip()
            self.logger.info("Export mesh to " + FileNameOut)
            exporter =  com.artenum.free.mesh.io.exporter.GmshExporter( shared["Mesh"], FileNameOut)
            exporter.exportAll()
        else:
            self.logger.error("Error in TaskExportToGmshMesh: No mesh loaded in the Data Bus. Impossible to export it.")
            
            
            
            
