"""
**File name:**    TaskJyTop.py

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

from threading                import Thread

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedNum
from Bin.Tasks.common         import ask_value
from Bin.Tasks.shared         import sharedSolver
from Bin.Tasks.shared         import sharedGlobals
from Bin.Tasks.shared         import sharedFlags
from Bin.Tasks.shared         import sharedProp



import javax.swing 
from javax.swing import JFrame
from javax.swing import JDialog
from javax.swing import JLabel
from javax.swing import JButton
from javax.swing import JPanel
from javax.swing import BorderFactory
from javax.swing import JRadioButton

from java.awt                  import BorderLayout

import sys
from Bin.config                import GL_DATA_PATH, GL_SPISUIROOT_PATH

from Bin.FrameManager          import FrameManager

import traceback
from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory

from Bin.SpisNumCaller import SpisNumCaller

class TaskJyTop(Task):
    """Task JyTop: Jython wrapping of SPIS-NUM. See technical information 
    for more details.
    """
    desc = "Solver wrapping module (JyTop for SpisNum)"
    
    def run_task(self):
                
        if self.initCaller() :
                self.frameManager = FrameManager()
                self.frameManager.setGuicontext(sharedFlags['guiMode'])
                self.selectionDialogBox()  
        else:
            self.logger.error( "Numerical Model Mesh not defined or inconsistent! \n"
                              +"Please perform the pre-processing phase before to call the \n"
                              + "solver (i.e at least load a project and perform UI2Num task.\n"
                              + "If this is already done, clean all mesh and data fields using "
                              + "the DataBus Manager and re-run the pre-processing phase.")
    

            
    def initCaller(self):
        """
        init the SPIS-NUM caller
        """
        
        # flag used to by-pass the simulation thread and exception handling 
        # for debug purpose (equal 1). The default value is 0 (normal behavior).
        self.DEEP_DEBUG = 0    
        self.logger = LoggerFactory.getLogger("Task")
        
        # for a dynamic reloading
        import Bin.SpisNumCaller
        reload(Bin.SpisNumCaller)
        from Bin.SpisNumCaller import SpisNumCaller
        
        if ("SNMesh" in sharedNum.keys()) and (sharedNum['SNMesh'] != None): 
            
                #self.spisNumCaller = SpisNumCaller(sharedNum['SNMesh'], 
                #                                   sharedData['AllDataField'], 
                #                                   sharedData['AllMeshField'], 
                #                                   sharedProp['materialModel'], 
                #                                   sharedGlobals, 
                #                                   sharedNum['nascapParameterSetList'])
                self.spisNumCaller = SpisNumCaller(sharedNum['SNMesh'], 
                                                   sharedData['AllDataField'], 
                                                   sharedData['AllMeshField'], 
                                                   sharedProp['materialModel'], 
                                                   sharedGlobals,
                                                   sharedProp['selectedNascapMaterialList'],
                                                   sharedProp['defaultNascapMaterialList'])
                
        
                sharedSolver['SpisNumCaller'] = self.spisNumCaller
                
                # specific thread that rally call SPIS-NUM (i.e JyTop) and run the simulation
                self.action = Action(self.spisNumCaller)
                self.action.setDebugLevel(self.DEEP_DEBUG)
                
                return(1)
        else:
            return(0)      
               
    def selectionDialogBox(self):
        '''
        Selection internal frame to select the type of job (spis daemon or system daemon) for 
        the simulation kernel.
        '''
        
        self.selectionFrame = self.frameManager.getNewFrame("Simulation run type selection")
        mainPanel = JPanel()
        mainPanel.setLayout( javax.swing.BoxLayout( mainPanel, javax.swing.BoxLayout.PAGE_AXIS))
        
        self.internalTaskRadioButton = JRadioButton("Internal task (spis daemon)",  actionPerformed = self.actionOnInternalTaskButton)
        self.internalTaskRadioButton.setSelected(1)
        mainPanel.add(self.internalTaskRadioButton)
        self.externalJobRadioButton = JRadioButton("External job (system daemon)",  actionPerformed = self.actionOnExternalTaskButton)
        mainPanel.add(self.externalJobRadioButton)
        
        okButton = JButton("OK", actionPerformed = self.okAction)
        mainPanel.add(okButton)
        self.selectionFrame.getContentPane().add(mainPanel)
        size = self.selectionFrame.getParent().getSize()
        self.selectionFrame.reshape(size.width/2-150, size.height/2-100, 300, 120)
        self.selectionFrame.show()
        
        
    def okAction(self, dummy):
        self.selectionFrame.dispose()
        self.selectionFrame.setVisible(0)
        
        if self.internalTaskRadioButton.isSelected():
            self.action.actionKey = "internal"
        else:
            self.action.actionKey = "external"
         
        if (self.DEEP_DEBUG == 0):    
            # standard behavior in a separated thread
            self.action.start()
        else:
            # for deep debug
            self.action.run()
            
    def actionOnInternalTaskButton(self, dummy):
        self.logger.info("internal task")
        if self.internalTaskRadioButton.isSelected():
            self.externalJobRadioButton.setSelected(0)

    def actionOnExternalTaskButton(self, dummy):
        self.logger.info("external task")
        if self.externalJobRadioButton.isSelected():
            self.internalTaskRadioButton.setSelected(0)   
     
     
     
     
     
     
class Action(Thread):
    '''
    Action thread (for a better GUI updating). Please set the actionKey
    before to start the thread.
    '''
    
    def __init__(self, simulationKernel):
        Thread.__init__(self)
        self.DEEP_DEBUG = 0
        self.simulationKernel = simulationKernel
        self.actionKey = "internal"
        self.logger = LoggerFactory.getLogger("Task")
        self.frameManager = FrameManager()
        self.frameManager.setGuicontext(sharedFlags['guiMode'])
        
        
    def setDebugLevel(self, deepDebug):
        self.DEEP_DEBUG = deepDebug
        
    def run(self):
        '''
        perform the simulation loop and the data extraction phase.
        '''
        print self.actionKey
        if self.actionKey == "internal":
            if (self.DEEP_DEBUG): 
                # run the simulation
                self.runAction()
                    
                # export
                if "exportAllDataFields" in sharedGlobals:     # to manage the legacy
                    self.exportData()           
                else:
                    self.logger.info("Deprecated project: exportAllDataFields key is missing in the Global Parameters \n \
                                      Missing parameters added to the Global Parameters list.\n \
                                      Please set exportAllDataFields, exportPotential, exportDensity and re-run the data extraction phase to export DF and Ms to ASCII formats.")
                    sharedGlobals["exportAllDataFields"] = ['Outputs', 'Select the export mode for all data fields (None=no export, ASCII=ASCII multi-files)', 'string', 'None', 'None']
                    sharedGlobals["exportPotential"] = ['Outputs', 'Select the export mode for potential data fields (None=no export, ASCII=ASCII multi-files)', 'string', 'None', 'None']
                    sharedGlobals["exportDensity"] = ['Outputs', 'Select the export mode for density data fields (None=no export, ASCII=ASCII multi-files)', 'string', 'None', 'None']            
            else:
                try:
                    
                    # run the simulation
                    self.runAction()
                    
                    # export
                    if "exportAllDataFields" in sharedGlobals:     # to manage the legacy
                        self.exportData()           
                    else:
                        self.logger.info("Deprecated project: exportAllDataFields key is missing in the Global Parameters \n \
                                      Missing parameters added to the Global Parameters list.\n \
                                      Please set exportAllDataFields, exportPotential, exportDensity and re-run the data extraction phase to export DF and Ms to ASCII formats.")
                        sharedGlobals["exportAllDataFields"] = ['Outputs', 'Select the export mode for all data fields (None=no export, ASCII=ASCII multi-files)', 'string', 'None', 'None']
                        sharedGlobals["exportPotential"] = ['Outputs', 'Select the export mode for potential data fields (None=no export, ASCII=ASCII multi-files)', 'string', 'None', 'None']
                        sharedGlobals["exportDensity"] = ['Outputs', 'Select the export mode for density data fields (None=no export, ASCII=ASCII multi-files)', 'string', 'None', 'None']
    
                    # closing dialogue box
                    text = "<html> <center>Simulation run done.<br> </center></html>"
                    self.showDialog("Numerical Kernel", text)  
                    self.logger.info("Simulation done.")
    
                except:
                    # recover the stack trace from SPIS-NUM layer.
                    print "XXXXXXXXXXXXXXXXXXXXX ERROR IN SIMULATION THREAD  XXXXXXXXXXXXXXXXXXXXXX"
                    sys.exc_info()
                    print" ----"
                    traceback.print_exc()
                    print" ----"
                    traceback.print_stack()
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    try: 
                        exc_value.printStackTrace()
                    except:
                        self.logger.warn("No java exception")
                    print exc_value
                    #self.logger.error(exc_value.printStackTrace())
                    print "XXXXXXXXXXXXXXXXXXXXX ERROR IN SIMULATION THREAD  XXXXXXXXXXXXXXXXXXXXXX"

        else:
            print "Run as external Job"
            self.simulationKernel.runAsExternalJob()
            
            
        
    def runAction(self):
        self.simulationKernel.runAsInternalTaks()
                 
        self.simulationKernel.BuildSim()
  
        text = "<html> <center>Numerical kernel (SPIS-NUM) is running in daemon mode.<br>\
                        Please see the standard log for more details.<br><br> </center> </html>"
        self.showDialog("Numerical Kernel Message", text)
            
        self.simulationKernel.Run()
        self.simulationKernel.ExtractData(sharedData['AllMeshField'], sharedData['AllDataField'])

    def exportData(self):
        # export
        if sharedGlobals["exportAllDataFields"][4] == 'ASCII':
            self.logger.info("Export all dataFields to ASCII...")
            self.simulationKernel.exportDataToASCII(sharedData['AllDataField'].Dic.keys())
        else :
            if sharedGlobals["exportPotential"][4] == 'ASCII':
                self.logger.info("Export electric potential to ASCII...")
                dataNameList = []
                for key in sharedData['AllDataField'].Dic.keys():
                    if "pot" in key: 
                        dataNameList.append(key)
                        self.spisNumCaller.exportDataToASCII(dataNameList)
        
            if sharedGlobals["exportDensity"][4] == 'ASCII':
                self.logger.info("Export densities to ASCII...")
                dataNameList = []
                for key in sharedData['AllDataField'].Dic.keys():
                    if "dens" in key:
                        dataNameList.append(key)
                        self.spisNumCaller.exportDataToASCII(dataNameList)     
        
        
    def showDialog(self, frameName, dialogueMessage):
        
        frame = JFrame()
        self.dia = JDialog( frame, frameName, 0)
        self.dia.getContentPane().setLayout(BorderLayout())
        textLabel = JLabel(dialogueMessage)
        textLabel.setBorder(BorderFactory.createEmptyBorder(20,20,10,10))
        tmpBottomPanel = JPanel()
        closeButton = JButton("OK", actionPerformed = self.closeAction)
        tmpBottomPanel.add(closeButton)
        self.dia.getContentPane().add(textLabel, BorderLayout.CENTER)
        self.dia.getContentPane().add(tmpBottomPanel, BorderLayout.SOUTH)
        self.dia.setSize(400, 150)
        self.dia.setLocationRelativeTo(None)
        self.dia.show()
        
    def closeAction(self, dummy):
        self.dia.dispose()
        self.dia = None   
      

            
            
