"""
**File name:**    TaskGroupManager.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
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
from Bin.Tasks.shared         import sharedProp

import sys
from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH

from org.slf4j                import Logger
from org.slf4j                import LoggerFactory

class TaskGroupManager(Task):
    """Task of management of groups."""
    desc = "Task of management of groups"
    
    def run_task(self):
        
        
        from Bin.GroupManager import GroupManager

        # we recover the common task logger
        self.logger = LoggerFactory.getLogger("Task")

        self.logger.info("Start GeoGroupManager")
        myBoss = GroupManager()
        
        myBoss.setGUI(self.mycond)
        myBoss.PrintWarning()
        

        self.logger.debug(sharedProp.keys())
        self.logger.debug(sharedProp['defaultMaterialList'].List[0].PrintMaterial())

        
        for tmp in sharedGroups['GeoGroupList'].List:
            self.logger.debug(tmp.Material.Id)

        #definition of groups (this part is input file dependent)
        myBoss.DefineGeoGroups( sharedGroups['GeoGroupList'].List, sharedProp)

        #conversion from geo to mesh groups
        myBoss.ConvertGeoToMeshGroup(sharedGroups['GeoGroupList'].List, shared['MeshGroupList'], shared['SkeletonElmtList'])
