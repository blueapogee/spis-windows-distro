"""
**File name:**    TaskSaveProj.py

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


from Bin.Tasks.shared           import *
from Bin.Tasks.TaskBuiltins     import *
from Bin.Tasks.FileChooserSwing import *

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, GL_VTK_EXCHANGE, GL_EXCHANGE
from Bin.config         import GL_SPIS_VERSION
#sys.path.append(GL_SPISUIROOT_PATH)

from Bin.Tasks.Task           import Task
from Bin.Tasks.TaskSaveProjAs import PersistenceManager

from org.slf4j                     import LoggerFactory

#from Bin.ProjectWriter2 import ProjectWriter2
#from Bin.ProjectWriter3 import ProjectWriter3

#from org.spis.imp.ui.util import DirectoryDialog

class TaskSaveProj(Task):
    """Project saving task"""
    desc = "Saving of the current project"
    def run_task(self):
        
        # building of the related logger
        logger = LoggerFactory.getLogger("TaskSaveProj")
        logger.info("TaskSaveProj launched")
        
        
        #import Bin.ProjectWriter3
        #from Bin.ProjectWriter3 import ProjectWriter3
        #reload(Bin.ProjectWriter3)
        #from Bin.ProjectWriter3 import ProjectWriter3
        
        #import Bin.ProjectWriter2
        #from Bin.ProjectWriter2 import ProjectWriter2
        #reload(Bin.ProjectWriter2)
        #from Bin.ProjectWriter2 import ProjectWriter2
        
        #if the project path is not defined, we open a file browser
        #otherwise, we save in the default directory
        logger.info( "Project path ", sharedFiles["project_directory"])
        logger.info( "projectSavingFlag =", sharedFiles["projectSavingFlag"])
        
        # we use the persistence manager in the SaveAs task to perform the job
        savingTask =  PersistenceManager()
        
        # we manage the case if the project is not already saved
        if sharedFiles["projectSavingFlag"] == None or sharedFiles["projectSavingFlag"] == 0:   
                     
            # initialisation of the project info data
            if sharedFiles["project_directory"] == None:
                sharedFiles["project_directory"] = ""
              
            savingTask.saveAs()
        else:
            savingTask.save()
               

               
