"""
Call the mesh viewer and Cassandra to display the mesh structure.

**File name:**    TaskViewPipeline2.py

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

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.common         import ask_value
from Bin.Tasks.shared         import shared, sharedFrames, sharedProp, sharedGroups, sharedTasks
from Bin.Tasks.shared         import sharedFlags
from Bin.Tasks.common         import create_internal_frame

import sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from javax.swing              import JOptionPane
from Bin.ViewPipeLine2        import ViewPipeLine2

try: 
    from Bin.CassandraCaller      import CassandraCaller
except:
    print "XXXXXXXXXXXXXXXXXXXXXXXX"
    #loadingLogger.warn("Impossible to load CassandraCaller!")
    #exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    #loadingLogger.debug(repr(traceback.format_tb(exceptionTraceback)))

from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH

class TaskViewPipeline2(Task):
    """
    Call the mesh viewer and Cassandra to display the mesh structure. 
    """
    desc = "Mesh viewer (Pipeline2)"
    
    import Bin.ViewPipeLine2
    reload(Bin.ViewPipeLine2)
    from Bin.ViewPipeLine2 import ViewPipeLine2

    def run_task(self):
        
        # we recover the common task logger
        self.logger = LoggerFactory.getLogger("Task")
        if shared['Mesh'] != None :   
            self.logger.info("Creation of the data set")
            dataSetName = "mesh grid"
            Viewer2 = ViewPipeLine2()
            
            self.logger.debug("Calling Cassandra")
            caller = CassandraCaller()
            caller.viewer.getDefaultUI().hidePipeLine();
            caller.show()
            caller.viewer.getDefaultUI().hidePipeLine();
            
            self.logger.debug("Building of the visualisation pipelines")
            
            #Set default pipeline
            Viewer2.run(shared['Mesh'])
            dataSet = Viewer2.getDataSet()
            mapper = Viewer2.getMapper()
            actor = Viewer2.getActor()
        
            # Register vtkObject in pipeline
            caller.viewer.getPipeLineManager().addDataSet(dataSet, dataSetName)
            caller.viewer.getPipeLineManager().addMapper(mapper, dataSetName);

            #caller.viewer.getPipeLineManager().addActor(actor, dataSetName)
            caller.viewer.getPipeLineManager().setActorVisible(caller.viewer.getPipeLineManager().addActor(actor, dataSetName), 1)
            
            # to automatically update the view
            caller.viewer.getPipeLineManager().getCassandraView().resetCamera()
            caller.viewer.getPipeLineManager().validateViewAndGo()
            
            # Show actors
            #caller.viewer.getPipeLineManager().setActorVisible(caller.viewer.getPipeLineManager().addActor(actor, dataSetName), 1)
            Viewer2.writeOutputFile()
        else:
            self.logger.error("No mesh to display! Please load a mesh file before to call the mesh viewer!")
            #if sharedFlags['guiMode'] == 1:
            #    InternalFrame = create_internal_frame("Error",sharedFrames["gui"].getCurrentDesktop())
            #    errorMessage = "<html>No mesh to display! Please load a mesh file before.</html>"
            #    toto = JOptionPane.showMessageDialog( InternalFrame, errorMessage, "Error in MeshViewer", JOptionPane.ERROR_MESSAGE)
            #else: 
            #    print >> sys.stderr, "Error in TaskViewPipeline2: No mesh to display! Please load a mesh file before."
        
