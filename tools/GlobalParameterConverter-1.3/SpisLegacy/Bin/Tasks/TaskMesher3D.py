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
sys.path.append("..")

from Bin.Tasks.Task                    import Task
from Bin.Tasks.shared                  import shared
from Bin.Tasks.shared                  import sharedFiles
from Bin.Tasks.shared                  import sharedControls
from Bin.Tasks.shared                  import sharedFlags
from Bin.Tasks.shared                  import sharedFrames

from Bin.config                        import GL_DATA_PATH, GL_SPISUIROOT_PATH

from com.artenum.free.mesh.io          import GmshLoader
from com.artenum.free.mesh             import Mesh
from Modules.Groups.MeshGroupList      import MeshGroupList
from Bin.Mesher import Mesher

from org.slf4j                         import Logger
from org.slf4j                         import LoggerFactory

class TaskMesher3D(Task):
    """Call the 3D Mesher."""
    desc = "Meshing module"
    
    
    def run_task(self):

        self.logger = LoggerFactory.getLogger("Task")
        TheMesher = Mesher()

        # temporary
        sharedControls['dimMesh'] = '2'
        self.control = sharedControls['dimMesh']

        if (   sharedFiles['TheCADFileOut'] == "None" 
            or sharedFiles['TheCADFileOut'] == None 
            or sharedFiles['TheCADFileOut'] == ""):
               self.logger.error("No main input GEOM file defined in the geometrical model. Please use the GEOM manager, set you root file 'as main' and re-process the modelling chain.")
        else:
            if self.control == '1':
                #2D meshing
                TheMeshFile='tmp.msh'
                TheMesher.mesh2D(sharedFiles['TheCADFileOut'], TheMeshFile)
    
                # import of the 2D mesh into the Spismesh structure
                #FileName3_msh = os.path.join(GL_DATA_PATH, TheMeshFile)
                FileName4 = TheMeshFile
                print "meshing file=", FileName4
            elif self.control == '2':
                TheMeshFile='tmp.msh'
                #3D meshing
                TheMesher.mesh3DwithGmsh(sharedFiles['TheCADFileOut'], TheMeshFile)
                FileName4 = TheMesher.getMeshFileOut() #to recover the right file if self.BUILD_DATA_PATH =='ON'
                self.logger.info("Meshing file: "+FileName4)
            else:
                self.logger.error("Please choose your meshing dimension or type.")
    
            ################################################################
            #                     Import of the Mesh                       #
            ################################################################    
            mesh = Mesh()
            try:
                self.logger.info("Mesh "+FileName4+" Importing. Please wait...")
                mesh.load(GmshLoader(FileName4))
                shared['Mesh'] = mesh
                shared['MeshGroupList'] = MeshGroupList()
            except:
                self.logger.error("Impossible to import "+FileName4+" ! Maybe the file is corrupted or Gmsh is missing. Please check.")
    
            #import gc
            #gc.collect()
            self.logger.debug("Memory cleaning.")
            import java.lang.System
            java.lang.System.gc()
            java.lang.System.runFinalization()
