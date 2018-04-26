"""

**Project ref:**  Spis/SpisUI

**File name:**    TaskPreferencesEditor.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**Modification:**

**Use:**

**Description:**  This Task is used to call the visualization module.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Julien Forest             | Definition/Creation        |
+----------------+---------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.common         import create_internal_frame

import org.spis.imp.ui.PropertiesEditorPanel

import java
from javax.swing import JFrame
from java.awt.event import ActionEvent
from java.awt.event import ActionListener

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH

class TaskPreferencesEditor(Task):
    """Call the preferences panel"""
    desc="Preferences editor"

    def run_task(self):
        '''
        Performs the Task.
        '''
        editor = Editor()
        
class Editor(ActionListener):
    
    def __init__(self):
        self.frame = create_internal_frame("Preferences", sharedFrames["gui"].getCurrentDesktop())
        self.controlPanel = org.spis.imp.ui.PropertiesEditorPanel()
        self.controlPanel.setActionListener(self)
        self.frame.getContentPane().add(self.controlPanel);
        self.frame.setSize(400, 250);
        self.frame.setVisible(1);   
        
        
    def actionPerformed(self, ae):
        actionName = ae.getActionCommand()
        print "Action=", actionName
        print self.controlPanel.getConsoleLoginLevel()
        if (actionName == "QUITE"):
            self.frame.dispose()
            self.frame = None
            self = None 
            
            
            
            
