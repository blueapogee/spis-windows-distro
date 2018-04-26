"""
Tasks calling th 2D analysis module (y=f(x) plots).

**File name:**    TaskBuildPlot2D.py

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
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.common         import ask_value
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.common         import create_internal_frame

import sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from javax.swing              import JComboBox, JButton, JPanel
from java.awt                 import BorderLayout
from java.awt.event           import ItemEvent

from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH

try:
    from Bin.BuildPlot2D import BuildPlot2D
except:
    loadingLogger.warn("Error in TaskBuildPlot2D: Impossible to load BuildPlot2D.")
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    loadingLogger.debug(repr(traceback.format_tb(exceptionTraceback)))
    loadingLogger.debug("       "+ repr( exceptionValue))

class TaskBuildPlot2D(Task):
    """
    Tasks calling the 2D analysis module (y=f(x) plots).
    """
    desc = "Build Plot2D"
       
    def setEnv(self):

        self.localLogger = LoggerFactory.getLogger("TaskBuildPlot2D")
        self.localLogger.info("Starting TaskBuildPlot2D...")
    
        self.dataField=sharedData['AllDataField']
        self.meshfield=sharedData['AllMeshField']
        
        self.flagPos = 0
        self.positionFrame = [0,0, 300,120]
        self.ctrWindowGeom = [0,0, 300,120]
        self.initXshift = 301
        self.initYshift  = 0
       
        self.DFName = "No data"
        
    def run_task(self):
        '''
        performs the tasks.
        '''
        self.setEnv()
        self.DataChooser()
        
    def setShapeCrtWin(self, x, y, l, h):
        self.ctrWindowGeom = [x, y, l, h]
        
    def getShapeCrtWin(self):
        return(self.ctrWindowGeom)
        
    def setShapeInitialPlotWin(self, x, y, l, h):
        self.positionFrame = [x, y, l, h]
        
    def setInitShift(self, xShift, yShift):
        self.initXshift = xShift
        self.initYshit  = yShift
        
        
    def displayPlot(self):
        '''
        Displays the chosen DataField.
        '''
        # creation of the 2D plot tool
        self.plot2D = BuildPlot2D()
        
        if self.flagPos == 0: 
            self.positionFrame[0] = self.positionFrame[0] + self.initXshift
            self.positionFrame[1] = self.positionFrame[1] + self.initYshift
            self.positionFrame[2] = 400
            self.positionFrame[3] = 300
            self.flagPos = 1
        else:
            self.positionFrame[0] = self.positionFrame[0] + 30
            self.positionFrame[1] = self.positionFrame[1] + 30
        self.plot2D.setShape(self.positionFrame[0], self.positionFrame[1], self.positionFrame[2], self.positionFrame[3])
       
        if ( self.DFName == "No data"):
            self.localLogger.error("Please select a data") # "Error_01-_No_data_displayed_in_y_f_x_plot") 
        elif ( self.DFName == "Default Test Data"):
            self.plot2D.buildDefaultData()   
        else:      
	    # identification of the corresponding DataField	in AllDataField
            if ( sharedData['AllDataField'] != None):
                if ( sharedData['AllDataField'].Dic[self.DFName] != None):
                   # identification of the corresponding MeshField via the MeshId
                   MFIndex = sharedData['AllMeshField'].IdList.index(sharedData['AllDataField'].Dic[self.DFName].MeshFieldId)
                   #the good one             
                   #print sharedData['AllDataField'].Dic[self.DFName]
                   #print sharedData['AllMeshField'].List[MFIndex]
                   self.plot2D.setDataFromDfAnMF( sharedData['AllDataField'].Dic[self.DFName], sharedData['AllMeshField'].List[MFIndex])

        self.plot2D.buildPlot()
        self.plot2D.run()

        
    def FieldComboBox(self):
        '''
        building and management of the GUI of DataField chooser.
        '''
        self.jComboBox1 = JComboBox()
        self.jComboBox1.addItem("No Data")
        
        if self.dataField != None:
            for data in self.dataField.List:
                # here we select (filter) y = f(x) like DF only. 
                if ( data.Local == 4):
                    self.jComboBox1.addItem(data.Name)
                    
        self.jComboBox1.addItem("Default Test Data");
        self.jComboBox1.itemStateChanged = self.eventListener
        

    def eventListener(self,e):
        if e.getStateChange() == e.SELECTED:
            self.DFName = self.jComboBox1.getSelectedItem()
            
    def showPlot(self, a):
        self.localLogger.info("Show plot")
        self.displayPlot()
        

    def DataChooser(self):
        
        self.internalChooser = create_internal_frame("2D Data Analysis Module",sharedFrames["gui"].getCurrentDesktop())
        self.internalChooser.reshape( self.ctrWindowGeom[0], 
                                      self.ctrWindowGeom[1], 
                                      self.ctrWindowGeom[2], 
                                      self.ctrWindowGeom[3])
        
        self.internalChooser.setResizable(1)
        self.FieldComboBox()
        self.internalChooser.getContentPane().add(self.jComboBox1, BorderLayout.NORTH)
        self.runButton = JButton( "Show Plots", actionPerformed=self.showPlot)
        tmpBottomPanel = JPanel()
        tmpBottomPanel.add(self.runButton)
        
        self.internalChooser.getContentPane().add(tmpBottomPanel, BorderLayout.SOUTH)
        #self.internalChooser.pack()
        #sharedFrames["desktop_pane"].add(self.internalChooser)
        self.internalChooser.setClosable(1)
        self.internalChooser.show()
        
        
        
