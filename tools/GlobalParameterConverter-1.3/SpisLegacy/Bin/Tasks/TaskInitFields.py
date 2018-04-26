"""
**File name:**    TaskFieldManager.py

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

import sys, time
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.Task           import Task

# import of shared data and objects i
# (see shared.y file for more informations)
from Bin.Tasks.shared                          import shared
from Bin.Tasks.shared                          import sharedFiles
from Bin.Tasks.shared                          import sharedProp
from Bin.Tasks.shared                          import sharedData
from Bin.Tasks.common                          import ask_value
from Modules.Field.DataFieldList    import DataFieldList
from Modules.Field.MeshFieldList    import MeshFieldList

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH


class TaskInitFields(Task):
    """Reinitisalise all DataFields and MeshField."""
    desc = "Task of management of FieldManager"

    
    def run_task(self):
        self.logger = LoggerFactory.getLogger("Task")

        StartTime = time.time()
        # defined data and corresponding fields are stored in the
        # sharedData common dictionary
        sharedData['AllDataField'] = DataFieldList()
        sharedData['AllMeshField'] = MeshFieldList()
 
        EndTime = time.time()
        Min = int((EndTime-StartTime)/60)
        Sec = (((EndTime-StartTime)/60)-Min)*60
        self.logger.debug('Initialisation DF and MF List Task Time =' + `Min`+'Mn'+ `Sec` +'S')

