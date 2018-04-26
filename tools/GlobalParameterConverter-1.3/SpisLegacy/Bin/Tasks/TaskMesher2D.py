"""
**File name:**    TaskMesher2D.py

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

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedControls
from Bin.Tasks.common         import ask_value

import sys
from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH

from org.slf4j                import Logger
from org.slf4j                import LoggerFactory

class TaskMesher2D(Task):
    """Call the 2D mesher."""
    desc = "Meshing module"
    def run_task(self):
        
        self.logger = LoggerFactory.getLogger("Task")
        from Bin.Mesher import Mesher

        self.logger.info("2D mesher loaded")
        
        TheMesher = Mesher()

	# temporary
	sharedControls['dimMesh'] = '1'

	self.control = sharedControls['dimMesh']

	#2D meshing
        TheMeshFile='tmp.msh'
       	TheMesher.mesh2D(sharedFiles['TheCADFileOut'], TheMeshFile)

	# import of the 2D mesh into the Spismesh structure
        #FileName3_msh = os.path.join(GL_DATA_PATH, TheMeshFile)
        FileName4 = TheMesher.getMeshFileOut() #to recover the right file if self.BUILD_DATA_PATH =='ON'
	print "meshing file=", FileName4


	################################################################
	#                     Import of the Mesh                       #
	################################################################

        print 'XXX  ',FileName4,' IS BEING IMPORTED XXX'
        print

        shared['MeshElmtList'], shared['OldNodeNumList'],\
        shared['SkeletonElmtList'], \
        shared['OldSkeletonElmtNumList'], \
        shared['MeshGroupList'] = Cv_Gmsh2MeshStruct([FileName4], \
        shared['cadimport'].GeoElementList, shared['cadimport'].GeoGroupList)


