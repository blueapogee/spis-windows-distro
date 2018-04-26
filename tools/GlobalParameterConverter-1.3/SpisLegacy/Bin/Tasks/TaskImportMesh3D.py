"""
**File name:**    TaskMesher3D.py

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
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedControls

#from Bin.Tasks.shared         import *
#from FileChooserSwing         import choose
from org.spis.imp.ui.util import FileDialog

from Bin.config         import GL_EXCHANGE, GL_DATA_PATH, GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)


class TaskMesher3D(Task):
    """Call the default 3D mesher."""
    desc = "Meshing module"

    def run_task(self):
        '''
        Performs the task.        
        '''
        self.logger = LoggerFactory.getLogger("Task")
        dir = sharedFiles["project_directory"]
        
        dialog = FileDialog(dir)
        if (dialog.showOpenDialog(None)):
           fileNameIn = dialog.getFileToSave().getAbsolutePath()
        self.logger.debug("Loading Geom file: "+ fileNameIn)
        
        ###############################  
        # Mesh loading
        ###############################

        mesh = Mesh()
        try:
            self.logger.info("Mesh Importing. Please wait...")
            #fileNameIn = os.path.join(dir, "Tmp3D.msh")
            fileNameOut = os.path.join(GL_EXCHANGE, "Tmp3D.msh")
            shutil.copyfile(fileNameIn, fileNameOut)
                
            mesh.load(GmshLoader(fileNameOut))
            shared['Mesh'] = mesh
            shared['MeshGroupList'] = MeshGroupList()
        except:
            self.logger.error("Error in TaskImportMesh3D: Impossible to import mesh file" + fileNameOut)
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            loadingLogger.debug(repr(traceback.format_tb(exceptionTraceback)))
            loadingLogger.debug("       "+ repr( exceptionValue))   

        # to avoid to re_mesh the mesh 
        sharedTasks["manager"].set_done_task("Mesher3D")
    
        #print "memory clean"
        #import java.lang.System
        #java.lang.System.gc()
        #java.lang.System.runFinalization()
