"""
Performs the MeshGroup visualisation and call Cassandre to display them.

**File name:**    TaskViewPipeline1.py

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

import sys, time
from threading import Thread

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared, sharedFrames
from Bin.Tasks.shared         import sharedGroups
from Bin.Tasks.common         import ask_value

from Bin.Tasks.shared         import sharedFlags
from Bin.Tasks.common         import create_internal_frame

from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from javax.swing import JOptionPane

try:
    from Bin.CassandraCaller import CassandraCaller
except:
    print "Warning: impossible to load CassandraCaller"
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    loadingLogger.debug(repr(traceback.format_tb(exceptionTraceback)))
    loadingLogger.debug("       "+ repr( exceptionValue))

from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_MAX_THREADS_STACK
from Bin.ViewPipeLine1        import ViewPipeLine1

class TaskViewPipeline1(Task):
    """
    Performs the MeshGroup visualisation and call Cassandre to display them.
    """
    desc = "Geo groups viewer (Pipeline 1)"
    
    
    def run_task(self):
        
        NbRunningThreads = 0 
        
        if shared["MeshGroupList"] != None:
            print"Calling Cassandra"
            caller = CassandraCaller()
            #size = caller.InternalFrame.getParent().getSize()
            caller.selectControlPanel(0)
            caller.setControlPanelSize(200)
            caller.show()
            
            for grp in shared["MeshGroupList"].List: #sharedGroups['GeoGroupList'].List:
                
                grpIndex = shared["MeshGroupList"].List.index(grp) #sharedGroups['GeoGroupList'].List.index(grp)
                
                dataSetName = grp.Name
                print "Building of the visualisation pipelines for Grp", dataSetName
                
                print "NbRunningThreads =", `NbRunningThreads`
                pipelineBuilder = buildPipeline()
                pipelineBuilder.setGrpIndex(grpIndex)
                pipelineBuilder.setDataSetName(dataSetName)
                pipelineBuilder.setcassandraViewer(caller)
                NbRunningThreads = NbRunningThreads +1
                pipelineBuilder.setThreadCont(NbRunningThreads)
                if NbRunningThreads <= GL_MAX_THREADS_STACK:
                    pipelineBuilder.start()
                else:
                    time.sleep(5)
                    pipelineBuilder.start() 
        else:
            if sharedFlags['guiMode'] == 1:
                InternalFrame = create_internal_frame("Error",sharedFrames["gui"].getCurrentDesktop())
                errorMessage = "<html>No mesh groups to display! Please convert geo groups to mesh groups before.</html>"
                toto = JOptionPane.showMessageDialog( InternalFrame, errorMessage, "Group Viewer", JOptionPane.ERROR_MESSAGE)
            else: 
                print >> sys.stderr, "Error in TaskViewPipeline1: No mesh groups to display! Please convert geo groups to mesh groups before."   
            
class buildPipeline(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        
        self.pipeline = ViewPipeLine1()
        
    def setGrpIndex(self, grpIndex):
        self.grpIndex = grpIndex
        
    def setDataSetName(self, dataSetName):
        self.dataSetName = dataSetName
        
    def setcassandraViewer(self, cassandraViewer):
        self.cassandraViewer = cassandraViewer
        
    def setThreadCont(self, cont):
        self.threadsCont = cont
        
    def decreasesThreadsCont(self):
        self.threadsCont = self.threadsCont - 1
         
    def run(self):
        self.pipeline.run(self.grpIndex)
        dataSet = self.pipeline.getDataSet()
        mapper = self.pipeline.getMapper()
        actor = self.pipeline.getActor()
        
        # Register vtkObject in pipeline
        self.cassandraViewer.viewer.getPipeLineManager().addDataSet(dataSet, self.dataSetName)
        self.cassandraViewer.viewer.getPipeLineManager().addMapper(mapper, self.dataSetName);
        self.cassandraViewer.viewer.getPipeLineManager().addActor(actor, self.dataSetName)
        
        self.decreasesThreadsCont()
