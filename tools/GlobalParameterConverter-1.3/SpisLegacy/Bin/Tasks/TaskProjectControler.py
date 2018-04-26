"""
**File name:**    TaskLoadCAD.py

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

from Bin.Tasks.shared             import *
from TaskBuiltins       import *
from FileChooserSwing   import choose
from Bin.Tasks.Task               import Task
from org.spis.imp.ui.util import FileDialog


from Bin.Tasks.shared              import *
from Bin.Tasks.common              import *
from Bin.Tasks.TaskBuiltins        import *
from Bin.Tasks.FileChooserSwing    import *


import java
import pawt
import javax.swing
from java.awt.event                     import ItemEvent
from java.awt                           import BorderLayout, GridLayout
from java.awt.event                     import ActionEvent
from java.awt.event                     import ActionListener

import sys, shutil, os

sys.path.append("..")
from Bin.config                         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, GL_EXCHANGE
sys.path.append(GL_SPISUIROOT_PATH)
from Bin.Tasks.Task                     import Task

from org.spis.imp.ui.shared             import ProjetLoaderControler
from org.spis.imp.ui.util               import DirectoryDialog



class TaskProjectControler(Task, ActionListener):
    '''
    Call the project controler. 
    '''
    desc = "Load the  CAD structure"
    
    def run_task(self):
        dir1 = sharedFiles["project_directory"]    
        if (dir1 != None and dir1 !="" and dir1 !="None"):
            self.showControler()
        
        
    def showControler(self):    
        
        self.ctr = ProjetLoaderControler()

        if sharedFlags['guiMode'] == 1:
            self.frame = create_internal_frame("Project Loader", sharedFrames["gui"].getCurrentDesktop())
            self.ctr.setActionListener(self)
            self.frame.contentPane.add( self.ctr, BorderLayout.CENTER)
        
            self.ctr.registerShared("Pre-processing (Phase 1)", "Project", "projectInfo", "Project Infos")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Geometry", "geomFile", "Geometry File Setting")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Properties", "materials", "Material Properties")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Properties", "elecNodes", "Electrical Nodes")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Properties", "plamas", "Plasma Properties")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Initial & Boundary Conditions", "groups", "Groups")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Initial & Boundary Conditions", "globals", "Global Parameters")
            self.ctr.registerShared("Pre-processing (Phase 1)", "Numerical kernel settings", "numKernelParam", "Additionnal Parameters")
    
            self.ctr.registerShared("Pre-processing (Phase 2)", "Geometry", "geomLoading", "Geometry loading")
            self.ctr.registerShared("Pre-processing (Phase 2)", "Mesh", "meshLoading", "Mesh loading")
            self.ctr.registerShared("Pre-processing (Phase 2)", "Pre-processing Data Fields", "preproDFLoading", "Data Fields loading")
    
            self.ctr.selectAll("Pre-processing (Phase 1)",1)
        
            self.frame.pack()
            self.frame.reshape(0,0,self.frame.getWidth() + 50, self.frame.getHeight()+10)
            self.frame.setVisible(1)
        else:
            sharedTasks["context"] = [ "projectInfo", 
                                       "geomFile", 
                                       "materials", 
                                       "elecNodes", 
                                       "plamas", 
                                       "groups", 
                                       "globals", 
                                       "geomLoading", 
                                       "meshLoading"] 
            sharedTasks["manager"].set_todo_task("ProjectLoaderFormat2")
            sharedTasks["manager"].run_tasks("ProjectLoaderFormat2")

        
    def setLoadingList( self, loadingList):
        self.keysList = loadingList
    
    def actionPerformed(self, ae):
            
        actionName = ae.getActionCommand() 
        
        if (actionName == "LOAD"):
           self.keysList = self.ctr.getSelectedKeys()
           print "Keys: ",self.keysList
           sharedTasks["context"] = self.keysList
           self.frame.dispose()
        
           sharedTasks["manager"].set_todo_task("ProjectLoaderFormat2")
           sharedTasks["manager"].run_tasks("ProjectLoaderFormat2")
           self = None
        else:
           print "Cancel"
           self.frame.dispose()
           self  = None
           return
        
