"""
Call the GEOM to Mesh groups converter. 
 
**File name:**    TaskConvertGroup.py

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
| 4.1.0   | Julien Forest                       | Modif                      |
|         | contact@artenum.com                 |                            |
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
from Bin.Tasks.shared         import sharedProp
from Bin.Tasks.common         import ask_value
from Bin.Tasks.shared         import sharedGroups
from Modules.Groups.MeshGroupList import MeshGroupList

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH


class TaskConvertGroup(Task):
    '''Performs the geo to mesh groups conversion.'''
    desc = "Conversion of groups"
    
    def run_task(self):
        '''
        Performs the task.
        '''
        self.logger = LoggerFactory.getLogger("Task")
        
        # for dynamical re-loading
        import Bin.GroupManager
        reload(Bin.GroupManager)
        from Bin.GroupManager import GroupManager

        self.logger.info(" Converting groups from Geo to Mesh...")

        try:
            myBoss = GroupManager()
            myBoss.setGUI(self.mycond)

            #conversion from geo to mesh groups
            if shared['MeshGroupList'] == None:
                self.logger.warn("No mesh groups defined !")
                shared['MeshGroupList'] = MeshGroupList()
            
            shared['MeshGroupList'].clearList()
            self.logger.debug("MeshGroups list cleared.")
            myBoss.ConvertGeoToMeshGroup( sharedGroups['GeoGroupList'], shared['MeshGroupList'], shared['Mesh'])

            self.logger.info("Conversion done.")
        
        except:
            self.logger.error(  "Error in TaskConvertGroup: It seems that your group definition is corrupted.\n"
                             + "Are you sure to have loaded a CAD file, the properties library \n"
                             + "and defined all needed groups ?")
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
            self.logger.debug("       "+ repr( exceptionValue))
