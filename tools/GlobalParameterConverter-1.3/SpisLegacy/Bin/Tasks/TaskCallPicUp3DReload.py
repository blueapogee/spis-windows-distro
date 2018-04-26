"""
Task re-loading the current simulation done with the Picup3D 
simulation kernel.

**Project ref:**  Spis/SpisUI

**File name:**    TaskCallPicUp3DReload.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Sebastien Jourdain        | Definition/Creation        |
|                | jourdain@artenum.com      |                            |
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

import java.awt
import pawt
from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedGlobalsPicUp
from Bin.Tasks.common         import create_internal_frame

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE, GL_CASSANDRA_PLUGINS

class TaskCallPicUp3DReload(Task):
    """Relead the current simulation done with Java based 3D simulation kernel PicUp3D."""
    desc="Load PicUp3D simulation kernel from previous simulation"
    def run_task(self):
        from org.spis.picup3d                  import PicUp3DGUI
        from org.spis.imp.ui.util              import FileDialog

        self.fileToLoad = None
        self.dialog = FileDialog(".")
        self.dialog.addFileType(".picup", "PicUp Simulation")
        if (self.dialog.showOpenDialog(None)):
            self.fileToLoad = self.dialog.getFileToSave().getAbsolutePath()
        
        self.fis = FileInputStream(self.fileToLoad)
        self.ois = ObjectInputStream(self.fis)
        self.picUp3d = self.ois.readObject()
        self.fis.close()
        self.glassPane = InfiniteProgressPanel();
        self.glassPane.setVisible(0);
        self.gui = PicUp3DGUI(self.picUp3d,sharedFrames["gui"].getCurrentDesktop());
        self.gui.setWaitWindows(self.glassPane);      
        
        self.InternalFrame = create_internal_frame("PicUp3D",sharedFrames["gui"].getCurrentDesktop())
        self.InternalFrame.setVisible(0);
        self.InternalFrame.addInternalFrameListener(InternalCloser(self.picUp3d))
        self.InternalFrame.reshape( 0, 0, 400, 300)
        self.InternalFrame.getContentPane().setLayout(java.awt.BorderLayout())
        self.InternalFrame.getContentPane().add(self.gui,java.awt.BorderLayout.CENTER)
        self.InternalFrame.setGlassPane(self.glassPane);
        self.InternalFrame.setVisible(1);
                     
class InternalCloser(pawt.swing.event.InternalFrameAdapter):
    def __init__(self,picUp):
        self.picUp = picUp
        
    def internalFrameClosing(self,internalFrameEvent):
        self.picUp.stopSimulation()
