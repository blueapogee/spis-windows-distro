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

from Bin.ProjectWriter2 import ProjectWriter2
from Bin.ProjectWriter3 import ProjectWriter3
from Bin.Tasks.FileChooserSwing import *
from Bin.Tasks.Task import Task
from Bin.Tasks.TaskBuiltins import *
from Bin.Tasks.common import ask_value
from Bin.Tasks.shared import *
from Bin.config import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, \
    GL_VTK_EXCHANGE, GL_EXCHANGE, GL_SPIS_VERSION
from org.spis.imp.ui.util import DirectoryDialog
import Modules.Field

import os

#import javax.swing
from javax.swing import JOptionPane


class TaskSaveProjAs(Task):
    """Project saving task"""
    desc = "Saving of the current project"
    def run_task(self):
        print "Saving the project as... "
       
        self.manager = PersistenceManager()
        self.manager.saveAs()


class PersistenceManager:
    
    def __init__(self):
        """
        Persistence manager.
        """
    def saveAs(self):
        
        if sharedFiles["project_directory"] != None:
            dialog = DirectoryDialog(sharedFiles["project_directory"])
        else:
            dialog = DirectoryDialog(".")
        dialog.addFileType(".v1", "Version 1.0")
        dialog.addFileType(".v3", "Version 3.0")
        dialog.addFileType(".v2", "Version 2.0")
        dialog.addFileType(".current", "Version "+str(GL_SPIS_VERSION))


        sharedFiles["projectSavingFlag"] = 1
    
        if (dialog.showSaveDialog(None)):
            projectPath = dialog.getFileToSave().getAbsolutePath()
            # just to have the right extension
            splitPath = projectPath.split(".")
            extension = splitPath[-1]
            if ( extension != "spis" ):
                cleanedProjectPath=""
                if (len(splitPath) > 1):      
                    for elm in splitPath[:-1]:
                        cleanedProjectPath = cleanedProjectPath +"_"+ elm
                else:
                    cleanedProjectPath = splitPath[0]
                cleanedProjectPath = cleanedProjectPath +".spis"
            else:
                cleanedProjectPath = projectPath
            sharedFiles["project_directory"] = cleanedProjectPath
            
            ctrPanAns = 0
            if os.path.isdir(sharedFiles["project_directory"]):
                ctrPanAns = JOptionPane.showConfirmDialog(None, "Project already existing, do want to continue?", "Error in save as", JOptionPane.YES_NO_OPTION)
                
            if ctrPanAns == 0:
                if (dialog.getSelectedFileTypeDescription() == 'Version 1.0'):
                    sharedFiles["projectSavingFormat"] = "V1"
                    print "Deprecated format"
                elif (dialog.getSelectedFileTypeDescription() == 'Version 2.0'):
                    print "V2"
                    sharedFiles["projectSavingFormat"] = "V2"
                elif (dialog.getSelectedFileTypeDescription() == 'Version 3.0'):
                    print "V3"
                else:
                    print "Current Spis version"
                    sharedFiles["projectSavingFormat"] = str(GL_SPIS_VERSION)
            
            self.save()
            
            
    def save(self):
        """
        Save the project with the right version
        """
        if sharedFiles["projectSavingFormat"] == "V1":
            print "Deprecated format"
        elif sharedFiles["projectSavingFormat"] == "V2":
            writer = ProjectWriter2()
            writer.setOuputDirectory(sharedFiles["project_directory"])
            writer.createNewProject()
            writer.write()
        elif sharedFiles["projectSavingFormat"] == "V3":
            writer = ProjectWriter3()
            writer.setOuputDirectory(sharedFiles["project_directory"])
            writer.write()
        else: # default value
            writer = ProjectWriter2()
            writer.setOuputDirectory(sharedFiles["project_directory"])
            writer.createNewProject()
            writer.write()
       
        print "Project saved"
