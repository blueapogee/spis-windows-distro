"""
**File name:**    TaskLoadProj.py

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

from Bin.Tasks.Task                import Task
from Bin.Tasks.shared              import sharedFiles
from Bin.Tasks.shared              import sharedTasks

#from org.slf4j                     import Logger
from org.slf4j                     import LoggerFactory

from Bin.config                         import GL_SPIS_VERSION

from org.spis.imp.ui.util import DirectoryDialog
from Bin.ProjectLoader2 import ProjectLoader2

class TaskLoadProj(Task):
    """Load a SPIS-UI project. See the corresponding Technical Note for further informations."""
    desc = "Load a SPIS-UI project."
    
    def run_task(self):
        '''
        Performs the task.
        '''
        # building of the related logger
        logger = LoggerFactory.getLogger("TaskLoadProj")
        logger.info("TaskLoadProj launched")
        
        #default project format
        sharedFiles["projectSavingFormat"] = "V2"

        if sharedFiles["projectLoadingFlag"] == None or sharedFiles["projectLoadingFlag"] == 0:            
            if sharedFiles["project_directory"] == None:
                sharedFiles["project_directory"] = ""
            dialog = DirectoryDialog(sharedFiles["project_directory"])
            dialog.addFileType(".v1", "Version 1.0")
            dialog.addFileType(".v3", "Version 3.0")
            dialog.addFileType(".v2", "Version 2.0")
            dialog.addFileType(".current", "Version "+str(GL_SPIS_VERSION))
        
        # FIX ME
        
            if (dialog.showDialog(None)):
                if (dialog.getSelectedFileTypeDescription() == 'Version 1.0'):
                    logger.info("Format version 1.0 selected")
                    sharedFiles["projectSavingFormat"] = "V1"
                elif (dialog.getSelectedFileTypeDescription() == 'Version 2.0'):
                    logger.info("Format version 2.0 selected")
                    sharedFiles["projectSavingFormat"] = "V2"
                elif (dialog.getSelectedFileTypeDescription() == 'Version 3.0'):
                    logger.info("Format version 3.0 selected")
                    sharedFiles["projectSavingFormat"] = "V3"
                else:
                    logger.info("Format version 2.0 selected")
                    sharedFiles["projectSavingFormat"] = "V2"  
                
                sharedFiles["project_directory"] = dialog.getFileToSave().getAbsolutePath()
                
        if sharedFiles["projectSavingFormat"] == "V1":
            logger.error("Deprecated format. Select another format.")
        elif sharedFiles["projectSavingFormat"] == "V2":
            sharedTasks["manager"].set_todo_task("ProjectControler")
            sharedTasks["manager"].run_tasks("ProjectControler")
        elif sharedFiles["projectSavingFormat"] == "V3":
            print "Not supported yet."
            logger.error("Format not supported yet. Select another format.")
        else:
            logger.error("Format not supported. Select another format.")
        
        
