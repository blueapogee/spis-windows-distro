"""
**File name:**    SpisNumCaller.py

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

import os
from Bin.JyTop4                import JyTop4
from Bin.Tasks.shared          import sharedSolver

from Bin.ProjectWriter2        import ProjectWriter2
from Bin.DeamonWriter          import DeamonWriter
from Bin.FrameManager          import FrameManager
from Bin.Tasks.shared          import sharedFlags, sharedFiles
from Bin.Tasks.shared          import sharedData
from Bin.Tasks.shared          import sharedProp

from Bin.DataExporter.ExporterControler import Controler

import java
from javax.swing import JPanel, BoxLayout, BorderFactory, JLabel, JTextField, JRadioButton, JButton, JFileChooser
from java.awt import FlowLayout, BorderLayout

import string
from threading import Thread

from Bin.config import GL_SPISUIROOT_PATH

from Modules.SolverInterfaces.SpisNum.SpisNumSimulationDataExtractor import SpisNumSimulationDataExtractor

#from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory
from Modules.Utils.LoggingUtilities     import LoggingUtilities

class  SpisNumCaller:
    '''
    control module of the numerical solver.
    '''
    
    def __init__(self, spisNumMesh, allDataFields, allMeshFields, materialModel, globalParam, selectedNascapMaterialList, nascapMaterialCatalog):
        
        self.logger = LoggerFactory.getLogger("SpisNumCaller")
        #self.logger.info("TrackManager initialised")
        #self.loggingUtilities = LoggingUtilities(self.logger)
        
        #import Bin.JyTop4
        #reload(Bin.JyTop4)
        #from Bin.JyTop4 import JyTop4
        
        # pass the incoming SPIS-NUM mesh data structure
        self.spisNumMesh = spisNumMesh
        sharedSolver['jytop'] = None
        
        self.allDataFields = allDataFields
        self.allMeshFields = allMeshFields
        
        self.materialModel = materialModel
        self.globalParam = globalParam
        
        self.selectedNascapMaterialList = selectedNascapMaterialList
        self.nascapMaterialCatalog = nascapMaterialCatalog
        
        # set the outcoming (if any) SPIS-NUM 'JyTop' instance
        self.simulationKernel = None
        sharedSolver['jytop'] = self.simulationKernel
        
        self.frameManager = FrameManager()
        self.frameManager.setGuicontext(sharedFlags['guiMode'])
        
        #data extractor
        self.extractor = SpisNumSimulationDataExtractor()
      
        
    def runAsInternalTaks(self):
        '''
        run the simulation job as internal SPIS Task. Useful for interacting mode. 
        '''
        # to force the dynamic reloading
        import Bin.JyTop4
        reload(Bin.JyTop4)
        from Bin.JyTop4 import JyTop4

        print '###################################'
        print '# SpisNum caller as internal task #'
        print '###################################'
        self.simulationKernel = JyTop4(self.spisNumMesh, self.allDataFields, self.allMeshFields)
        
        # If we find NASCAP based material, we convert them otherwise, we just 
        # set the model type. 
        if sharedProp['selectedNascapMaterialList'] != None:
            self.simulationKernel.buildNascapParameterSetList(self.materialModel, self.selectedNascapMaterialList, self.nascapMaterialCatalog)
        else:
            self.simulationKernel.setSharedMaterialModel(self.materialModel)
        
        self.simulationKernel.setGlobalParameters(self.globalParam)
        
        #sharedSolver['jytop'] = self.simulationKernel

        
    def BuildSim(self):
        '''
        Initializes the simulation and build the numerical model. See, JyTop4
        file and the SPIS-NUM documentation for more detail.
        '''
        #if sharedSolver['jytop'] != None:
        self.simulationKernel.BuildSim() #(AllMeshField, AllDataField)

    def Run(self):
        '''
        performs the simulation.
        '''
        #if sharedSolver['jytop'] != None:
        self.simulationKernel.Run()

    def ExtractData(self, allMeshField, allDataField, simulationKernel=None):
        '''
        extracts output data from the simulation kernel.
        '''
        
        # if we do not use the default simulation kernel        
        if simulationKernel != None:
            self.simulationKernel = simulationKernel
            
        if self.simulationKernel != None:         
            self.extractor.setInput(self.simulationKernel.simu)
            self.extractor.setOutputDataBus( allMeshField, allDataField)
            
            self.extractor.setDefaultSimulationId()
            print "***********************************************************"
            self.extractor.readVolumeData()
            print "***********************************************************"
            self.extractor.readSCSurfaceData()
            print "***********************************************************"
            self.extractor.readBoundarySurfaceData()
            print "***********************************************************"
            self.extractor.readTimeDependentData()
            print "***********************************************************"
            self.extractor.readParticleTrajectories()
            print "***********************  END  *****************************"
        
        
    def exportDataToASCII(self, list):
        """
        Exported the listed data fields into the ASCII format described in CETP study.
        """
        #self.simulationKernel.exportDataToASCII(list)
        self.extractor.exportDataToControledFormat( Controler(), list)


        
        
        
    def runAsExternalJob(self):
        '''
        run job as an external job. Useful for large jobs in non-interactive mode.
        '''        
        self.deamon = DeamonWriter()
        self.deamon.setTemplateFileName( os.path.join( GL_SPISUIROOT_PATH, "Templates", "Tracks", "simulationDeamon_template_compliante_spis_4_3.py"))
        
        self.settingFrame = self.frameManager.getNewFrame("Simulation run type selection")
        
        mainPanel = JPanel()
        mainLayout = BoxLayout(mainPanel, BoxLayout.PAGE_AXIS)
        mainPanel.setLayout(mainLayout)
        mainPanel.setBorder(BorderFactory.createTitledBorder("Simulation Settings"))


        subPanel1 = JPanel()
        subPanel1.setLayout(BorderLayout())
        simLabel = JLabel("Simulation Name")
        simLabel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
        subPanel1.add(simLabel, BorderLayout.WEST)
        self.simulationTextField = JTextField()
        self.simulationTextField.setSize(20, 80)
        subPanel1.add(self.simulationTextField, BorderLayout.CENTER)
        mainPanel.add(subPanel1)
        
        subPanel2 = JPanel()
        subPanel2.setLayout(BorderLayout())
        runLabel = JLabel("Run Id (integer)  ")
        runLabel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
        subPanel2.add(runLabel, BorderLayout.WEST)
        self.runIdTextField = JTextField()
        self.runIdTextField.setSize(20, 80)
        subPanel2.add(self.runIdTextField, BorderLayout.CENTER)
        mainPanel.add(subPanel2)
                
                
        templateSubPanel = JPanel()
        templateSubPanel.setLayout(BorderLayout())
        cmdLabel = JLabel("Track template  ")
        cmdLabel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
        templateSubPanel.add(cmdLabel, BorderLayout.WEST)
        self.templateFileName = JTextField()
        self.templateFileName.setText(self.deamon.getTemplateFileName())
        self.templateFileName.setSize(20, 80)
        templateSubPanel.add(self.templateFileName, BorderLayout.CENTER)
        self.selectTemplateButton = JButton("select", actionPerformed = self.selectButtonAction)
        templateSubPanel.add(self.selectTemplateButton, BorderLayout.EAST)
        mainPanel.add(templateSubPanel)
        
        
        subPanel3 = JPanel()
        subPanel3.setLayout(BorderLayout())
        cmdLabel = JLabel("Batch command ")
        cmdLabel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
        subPanel3.add(cmdLabel, BorderLayout.WEST)
        self.deamonCmd = JTextField()
        self.deamonCmd.setText(self.deamon.getDeamonBaseCmd())
        self.deamonCmd.setSize(20, 80)
        subPanel3.add(self.deamonCmd, BorderLayout.CENTER)
        mainPanel.add(subPanel3)
        
        subPanel4 = JPanel()
        subPanel4.setLayout(BorderLayout())
        self.runRadioButton = JRadioButton("Launch (run) the daemon now!")
        subPanel4.add(self.runRadioButton)
        mainPanel.add(subPanel4)
        
        subPanel5 = JPanel(FlowLayout(java.awt.FlowLayout.RIGHT))
        self.selectionOkButton = JButton("OK", actionPerformed = self.selectionOkButton)
        subPanel5.add(self.selectionOkButton)
        mainPanel.add(subPanel5)
        
        self.settingFrame.getContentPane().add(mainPanel)
        width = 650
        height = 250
        size = self.settingFrame.getParent().getSize()
        self.settingFrame.reshape( (size.width-width)/2, (size.height-height)/2, width, height)
        self.settingFrame.show()
        
        
    def selectButtonAction(self, dummy):
        chooser = JFileChooser(os.path.join( GL_SPISUIROOT_PATH, "Templates", "Tracks"))
        chooser.showDialog(None, None)
        if (chooser.getSelectedFile() != None):
            selectedTrackFile = chooser.getSelectedFile().absolutePath
            #print selectedTrackFile
            self.deamon.setTemplateFileName(selectedTrackFile)
            self.templateFileName.setText(self.deamon.getTemplateFileName())
            self.templateFileName.repaint()

                
    def selectionOkButton(self, dummy):
         
        runId = 0
        try:
            runId = string.atoi(self.runIdTextField.getText())
        except:
            self.logger.error("Run Id not supported. Please enter an integer")
            return()
        
        self.settingFrame.dispose()
        self.settingFrame = None
        
        dialogFrame = self.frameManager.getNewFrame("Daemon under preparation")
        text = "<html> <center>Deamon (i.e Track) under preparation. <br>\
                        Full project saving needed. This may be long. Please wait...<br><br> </center> </html>"
        dialogPanel = JPanel()
        dialogPanel.add(JLabel(text))
        dialogFrame.getContentPane().add(dialogPanel)
        width = 450
        height = 100
        size = dialogFrame.getParent().getSize()
        dialogFrame.reshape( (size.width-width)/2, (size.height-height)/2, width, height)
        dialogFrame.setVisible(1)
        
        #self.writeDemon(self.simulationTextField.getText(), runId)
        saver = ThreadedDeamonSaver( self.deamon, self.simulationTextField.getText(), runId, self.runRadioButton.isSelected(), dialogFrame)
        saver.start()
        
        #dialogFrame.dispose()
        #dialogFrame = None
        
class ThreadedDeamonSaver(Thread):
    """
    """

    def __init__(self, deamon, simulationName, runId, runDeamonFlag, dialogFrame):
        Thread.__init__(self)
         
        self.deamon = deamon
        self.simulationName = simulationName
        self.runId = runId
        self.runDeamonFlag = runDeamonFlag
        self.dialogFrame = dialogFrame
        
    def run(self):
        self.writeDemon(self.simulationName, self.runId)
        if (self.dialogFrame != None):
            self.dialogFrame.dispose()
            self.dialogFrame = None
        
    def writeDemon(self, simulationName, runId):
        #save the input datafields
        # To put into a separated thread
        writer = ProjectWriter2()
        writer.setOuputDirectory(sharedFiles["project_directory"])
        writer.createNewProject()
        writer.write()
        
        # generation of the daemon
        print "Generation of the track"
        self.deamon.loadTemplate()
        self.deamon.setParameters(simulationName, runId, ".", ".")
        if sharedFiles["project_directory"] != None:
            self.deamon.writeDeamon(sharedFiles["project_directory"])
            if self.runDeamonFlag:
                self.deamon.runDeamon(sharedFiles["project_directory"], self.deamon.getDeamonName())
        else:
            print "Error in SpisNumCaller: Impossible to launch the daemon because no project defined."
        print "Track generated"
        


