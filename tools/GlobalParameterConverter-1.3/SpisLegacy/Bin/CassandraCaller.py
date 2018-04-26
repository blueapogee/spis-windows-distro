"""
Call the Java based 3D VTK viewer Cassandra for post-processing and 3D visualisation.

**Project ref:**  Spis/SpisUI

**File name:**    CAD_Importer.py

:status:          Implemented

**Creation:**     10/06/2005

**Modification:** 22/11/2005  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest, Sebastien Jourdain

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | J.Forest                             | Creation                   |
|                | j.fores@atenum.com                   |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | Sebastian Jourdain                   | Bug correction             |
|                | jourdain@artenum.com                 |                            |
+----------------+--------------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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

import sys, os
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.common         import ask_value
from Bin.Tasks.common         import create_internal_frame

from Bin.Tasks.shared         import sharedFrames

from pawt                     import swing, colors
from java.lang                import Thread, System
from java.awt                 import BorderLayout
from java.io                  import File
from java.awt.event           import ItemEvent
import javax.swing.WindowConstants.HIDE_ON_CLOSE

try:
#if(1):
    from com.artenum.cassandra        import Cassandra
    from com.artenum.cassandra.action import CassandraActionListener
    from com.artenum.cassandra.ui     import CassandraGUI
except:
    loadingLogger.warn("Error in CassandraCaller: Impossible to load Cassandra.")
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    loadingLogger.debug(repr(traceback.format_tb(exceptionTraceback)))
    loadingLogger.debug("       "+ repr( exceptionValue))

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE, GL_CASSANDRA_PLUGINS, GL_IMAGES_EXCHANGE

class CassandraCaller(Task):
    """Call the Java based 3D VTK viewer Cassandra for post-processing and 3D visualisation."""
    desc="Build vtk frame"
    
    def __init__(self):
        '''
        Default constructor. 
        '''

        #from com.artenum.cassandra        import Cassandra
        #from com.artenum.cassandra.action import CassandraActionListener
        #from com.artenum.cassandra.ui     import CassandraGUI


        self.size = None
        self.viewer = Cassandra()
        self.InitFrame()

    def InitFrame(self):
        self.InternalFrame = create_internal_frame("Cassandra VTK viewer",sharedFrames["gui"].getCurrentDesktop())
        self.InternalFrame.setFrameIcon( javax.swing.ImageIcon(self.InternalFrame.getClass().getResource("/cassandraIcone27x27.png")))
        self.InternalFrame.setVisible(0);
        #self.InternalFrame.reshape( 507, 0, 489, 473)
        self.size = self.InternalFrame.getParent().getSize()
        self.InternalFrame.reshape(self.size.width/3-2,0, (self.size.width*2)/3+2, self.size.height)
        self.InternalFrame.getContentPane().setLayout(BorderLayout())
        self.InternalFrame.setJMenuBar(self.viewer.getDefaultMenu())              
        self.InternalFrame.getContentPane().add(self.viewer.getDefaultUI(),BorderLayout.CENTER)
        self.InternalFrame.getContentPane().add(self.viewer.getDefaultToolBar(),BorderLayout.NORTH)
        
    def reshape(self, xMin, yMin, xMax, yMax):
        self.InternalFrame.reshape( xMin, yMin, xMax, yMax)
        
    def selectControlPanel(self, panelIndex):
        self.viewer.getDefaultUI().setPreferedControlPanel(panelIndex)
        self.viewer.getDefaultUI().update()
        
    def setControlPanelSize(self, size):
        self.viewer.getDefaultUI().setPipeLineRendererDividerLocation(size)
        self.viewer.getDefaultUI().update()


    def show(self, deskPanel=None):
        '''
        Display the viewer in an internal frame of SPIS-UI. Cassandra and its JyConsole will shared the 
        whole context and data (dataBus) of SPIS-UI. 
        ''' 
        print "Cassandra Plug-Ins directory:", GL_CASSANDRA_PLUGINS
        self.viewer.loadPluginInDirectory(File(GL_CASSANDRA_PLUGINS))
        self.viewer.getDefaultUI().getPyConsole().getPythonInterpreter().setLocals(globals())
        self.viewer.getDefaultUI().getPyConsole().getPythonInterpreter().set("cassandra", self.viewer);
        
        self.viewer.setPreference(CassandraActionListener.PREF_IMAGE_SAVE_DIR, File(GL_IMAGES_EXCHANGE));
        
        #self.viewer.setPreference(CassandraActionListener.PREF_PLUGIN_OPEN_DIR, new File(localDir, "plugin"));

        self.viewer.setPreference(CassandraActionListener.PREF_VTK_FILE_OPEN_DIR, File(GL_VTK_EXCHANGE));
        self.viewer.setPreference(CassandraGUI.PREF_SCRIPT_DIR, File(GL_SPISUIROOT_PATH, "Scripts"))
        
        from com.artenum.cassandra.action import JInternalFrameDispose
        self.viewer.getActionManager().setExitAction(JInternalFrameDispose(self.InternalFrame))
        self.InternalFrame.setVisible(1)
        print "Done"
    
    def reShow(self):
        if (not self.InternalFrame.isVisible()):
            self.InternalFrame.setSize(self.size)
            #self.InternalFrame.show()
        
            sharedFrames["gui"].getCurrentDesktop().add(self.InternalFrame)
            #size = self.InternalFrame.getParent().getSize()
            self.InternalFrame.reshape(self.size.width/3-2,0, (self.size.width*2)/3+2, self.size.height)
            self.InternalFrame.show()
        
