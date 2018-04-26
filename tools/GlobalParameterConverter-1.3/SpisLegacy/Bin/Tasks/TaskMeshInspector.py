"""

**Project ref:**  Spis/SpisUI

**File name:**    TaskCallCassandra.py

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
| 0.1.0          | Arsene Lupin              | Definition/Creation        |
|                | lupin@artenum.com         |                            |
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

try:
#if(1):
    from com.artenum.free.mesh.inspector.core import Context
    from com.artenum.free.mesh.inspector.core import Inspector
except:
    print "Impossible to load the Mesh Inspector Context"
    
from Bin.Tasks.common         import create_internal_frame
from Bin.Tasks.shared         import sharedFrames


from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE, GL_CASSANDRA_PLUGINS, GL_MESH_STUDY


class TaskMeshInspector(Task):
    """Call the Java based mesh inspector."""
    desc="Call the mesh inspector"

    def run_task(self):
        '''
        Performs the Task.
        '''        
        
        # setting of the shared context
        Context.getInstance().setCASSANDRA_CONTEXT(1)
        
        Context.getInstance().setGUI_CONTEXT(Context.GRAPHICAL)
        Context.getInstance().setVTK_CONTEXT(1)
        Context.getInstance().setPlotContext(1)
        Context.getInstance().setKERIDWEN_CONTEXT(1)
        Context.getInstance().setKeridwenMesh(shared["Mesh"])
        
        
        Context.getInstance().setStudyPath(GL_MESH_STUDY);
        
        inspector = Inspector()
        
        self.InternalFrame = create_internal_frame("Mesh Inspector",sharedFrames["gui"].getCurrentDesktop())
        #self.InternalFrame.setFrameIcon( javax.swing.ImageIcon(self.InternalFrame.getClass().getResource("/cassandraIcone27x27.png")))
        self.InternalFrame.setVisible(0);
        size = self.InternalFrame.getParent().getSize()
        self.InternalFrame.reshape(0, 0, size.width, size.height)
                
        if (Context.getInstance().isCASSANDRA_CONTEXT()):
            inspector.setCassandraPlugInsPath(GL_CASSANDRA_PLUGINS);
            inspector.initCassandraPanel(self.InternalFrame.getContentPane())
        else:
            self.InternalFrame.getContentPane().add(inspector.getGui())

        #from com.artenum.cassandra.action import JInternalFrameDispose
        #self.InternalFrame.getActionManager().setExitAction(JInternalFrameDispose(self.InternalFrame))
        
        self.InternalFrame.show()
        
