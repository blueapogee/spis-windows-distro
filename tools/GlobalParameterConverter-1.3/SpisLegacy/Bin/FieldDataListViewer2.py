"""
DataField management and conversion module. This module allows the visualisation
and the edition of DataFields, their convertion into VTK format. 
It allows also perform the "transtyping" of cell type, e.g display on cell data initially
localised on nodes. 

**File name:**    FieldDataListViewer.py

**Creation:**     2004/05/31

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


from threading import Thread
import traceback

from Bin.Tasks.shared             import sharedData
from Bin.Tasks.shared             import shared
from Bin.Tasks.shared             import sharedVTK
from Bin.Tasks.shared             import sharedFrames
from Bin.Tasks.shared             import sharedFiles
from Bin.Tasks.shared             import sharedFlags
 
from Bin.Tasks.common             import create_internal_frame # deprecated
from Bin.FrameManager             import FrameManager

from org.spis.imp.ui.util         import DirectoryDialog

from org.slf4j                    import Logger
from org.slf4j                    import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

# must be removed for epydoc
import javax.swing
from javax.swing                  import JPanel
from javax.swing                  import JLabel
from javax.swing                  import JTextField
from java.awt.event               import ItemEvent
from java.awt                     import BorderLayout
from java.awt                     import GridLayout

#----

import sys, time, os, string
from config import GL_SPISUIROOT_PATH
from Bin.config import GL_DATA_PATH, GL_CMD_GMSH, GL_CMD_TETGEN, GL_CMD_MEDIT, GL_GMSH_OUT_PATH, GL_VTK_EXCHANGE

#VTK stuff
try:
    import vtk
    import Modules.PostProcessing.Lib.JavaLib
    import Modules.PostProcessing.Include.DataMeshViewer
    from Modules.PostProcessing.Include.DataMeshViewer import DataMeshViewer
    import Modules.PostProcessing.Include.vtkParticleTrajectoryBuilder
    from Modules.PostProcessing.Include.vtkParticleTrajectoryBuilder import vtkParticleTrajectoryBuilder
except:
    # FIX ME
    loadingLogger.warn("Warning in FieldDataListViewer2: Impossible to load VTK components. VTK export impossible.")
    loadingLogger.debug(traceback.format_tb(exceptionTraceback))
    
    
#Java stuff    
import Bin.Tasks.FileChooserSwing
#from Bin.Tasks.FileChooserSwing import *

from org.spis.imp.ui import FieldManager
from java.awt.event import ActionEvent
from java.awt.event import ActionListener

try:
    from Bin.CassandraCaller import CassandraCaller
except:
    loadingLogger.warn("Impossible to load the Cassandra controler")
    loadingLogger.debug(traceback.format_tb(exceptionTraceback))
   
try:
    import Bin.DataExporter.ExporterControler
except:
    loadingLogger.warn("Impossible to load the Data ASCII exporter")
    loadingLogger.debug(traceback.format_tb(exceptionTraceback))
   


class FieldDataListViewer2(ActionListener):
    '''
    Module of management and conversion of DataField. This modules allows to visualise
    and edit DataFields and convert them into VTK format for their 3D visualisation.
    It allows also the "transtyping" of cell type, e.g display on cell data initially
    localised on node.
    '''
    
    def __init__(self):
        '''
        constructor and creation of the GUI
        '''
        
        self.frameManager = FrameManager()
        self.frameManager.setGuicontext(sharedFlags['guiMode'])
        self.frame = self.frameManager.getNewFrame("DataField Manager")
        
        self.DataFieldGrid = None
        self.allDataField=sharedData['AllDataField']
        self.allMeshField=sharedData['AllMeshField']
        self.currentDataField = None
        self.flip = 0
        self.exportControler = None
        self.cassandraCaller = None

        # building of the related logger
        self.logger = LoggerFactory.getLogger("FieldDataListViewer2")
        self.logger.info("FieldDataListViewer2 initialised")

        #self.frame = create_internal_frame("DataField Manager 2", sharedFrames["gui"].getCurrentDesktop())
        
        self.controlPanel = FieldManager()
        self.controlPanel.setActionListener(self)
        self.frame.contentPane.add( self.controlPanel, BorderLayout.CENTER)
        size = self.frame.getParent().getSize()
        self.deskTopSize = size
        self.frame.setSize(size.width/3, size.height)
        
        self.currentVtkDataSet = None
        self.currentOutVtkDataSetList = None
        self.BUILD_DATA_PATH = 'ON'
        index = 0
        if self.allDataField != None:
            for dataField in self.allDataField.List:
                outputText = "Name of the Data Field:  "+str(dataField.Name)+"\n" \
                +"Id of the Data Field:  "+str(dataField.Id)+"\n" \
                +"Type of the Data Field:  "+str(dataField.Type)+"\n" \
                +"Description of the Data Field:  "+str(dataField.Description)+"\n" \
                +"Unit:  "+str(dataField.Unit)+"\n" \
                +"Local:  "+str(dataField.Local)+"\n" \
                +"LockedValue:  "+str(dataField.LockedValue)+"\n" \
                +"MeshFieldId:  "+str(dataField.MeshFieldId)

                viewAvailable = [1,1,1,1]
            
                if (dataField.Local == 0):
                    viewAvailable = [1,1,1,1]
                elif (dataField.Local == 1):
                    viewAvailable = [0,1,0,0]
                elif (dataField.Local == 2):
                    viewAvailable = [0,0,1,0]
                elif (dataField.Local == 3):
                    viewAvailable = [0,0,0,1]
                elif (dataField.Local == 4):
                    viewAvailable = [0,0,0,0]
                elif (dataField.Local == 5):
                    viewAvailable = [0,0,0,0]

                self.controlPanel.registerDataField( dataField.Category, dataField.Name, 
				                     outputText, index, dataField.MeshFieldId, 
						     dataField.Unit, dataField.Local,viewAvailable)
                index = index + 1
        else:
            outputText = "No DataField to process... "
            self.controlPanel.registerDataField("", "", outputText, index, 0, "", 0, [1,1,1,1])
            index = index + 1
        self.frame.setVisible(1)


        
    def actionPerformed(self, ae):
        """
        handle the action for the GUI.
        """
        actionName = ae.getActionCommand()
        if self.allDataField != None:
            self.currentDataField = self.allDataField.List[self.controlPanel.getSelectedDataField().getId()]
            self.currentMeshField =  self.allMeshField.GetMeshFieldById(self.currentDataField.MeshFieldId)
        else:
            self.logger.error("No data field selected")
           
        self.viewType = self.controlPanel.getSelectedView()
        
        if (actionName == 'EDIT'):
            self.editDataField()
        if (actionName == 'SHOW'):
            self.ShowValueList()
        if (actionName == 'REMOVE'):
            self.delDataField()
        if (actionName == 'MAP'):
            self.DataFieldMapping()
        if (actionName == 'SAVE'):
            self.SaveDataField()
        if (actionName == 'EXPORT'):
            self.ExportToASCII()
        if (actionName == 'BUILD_VTK_GRID'):
            self.BuildGrid(None)
        if (actionName == 'SAVE_VTK_FILE'): # deprecated not used
            print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            self.ExportToCassandra()
        if (actionName == 'CALL_2D_VIEWER'):
            self.call2DViewer()
        if (actionName == 'CALL_3D_VIEWER'):
            self.ExportToCassandra()
          
    def call2DViewer(self):
        '''
        Call the SPIS 2D data post-processing module.
        '''
        # for a dynamic reloading
        from Bin.Tasks.Task            import Task
        from Bin.Tasks.TaskBuildPlot2D import TaskBuildPlot2D
        
        viewer2D = TaskBuildPlot2D(Task)
        viewer2D.setEnv()
        viewer2D.setShapeCrtWin( (self.deskTopSize.width/3), 0, 300,120)
        viewer2D.setShapeInitialPlotWin( (self.deskTopSize.width/3), 120, 300,120)
        viewer2D.setInitShift( 0, 0)
        viewer2D.DataChooser()
    
    
    def call3DViewer(self):
        '''
        call the 3D viewer.
        '''
        self.logger.info("Calling Cassandra viewer")
        if self.cassandraCaller == None:
            self.logger.debug("New viewer built")
            self.cassandraCaller = CassandraCaller()
            self.cassandraCaller.show()
        else:
            self.logger.debug("re-show viewer")
            self.cassandraCaller.reShow()
        
                      
    def BuildGrid(self, viewer):
        '''
        builds the VTK grids corresponding to the selected DataField.
        '''
        
        
        if self.currentDataField == None:
            self.logger.error("Not data field selected")
        else:
            self.logger.info("Building VTK grid")
            self.logger.info("Localisation:"+`self.currentDataField.Local`)
            self.logger.info("View type:"+`self.viewType`)
        
            self.currentOutVtkDataSetList = []
            if (self.currentDataField.Local == 0):
                self.logger.info("Data Localised on Node and displayed on:")
                if self.viewType > -1 :
                    if (self.viewType == 0):
                       self.logger.info("          Node")
                       return(self.transtypeGrid(0, 0, viewer))           
                    if (self.viewType == 1):
                       self.logger.info("          Edge")
                       return(self.transtypeGrid(0, 1, viewer))
                    if (self.viewType == 2):
                       self.logger.info("          Face")
                       return(self.transtypeGrid(0, 2, viewer))
                    if (self.viewType == 3):
                       self.logger.info("          Cell")
                       return(self.transtypeGrid(0, 3, viewer))
                else:
                   self.logger.error("Type of visualisation grid not set. Please, select a type of visualisation grid.")
                                  
            elif (self.currentDataField.Local == 1):
               if self.viewType > -1 : 
                   self.logger.info("Data Localised on Edge and diplayed on:")
                   if (self.viewType == 0):
                       self.logger.info("          Node")
                       self.logger.erro("This conversion is not authorised")
                   if (self.viewType == 1):
                       self.logger.info("          Edge")
                       return(self.transtypeGrid(1, 1, viewer))
                   if (self.viewType == 2):
                       self.logger.info("          Face")
                       return(self.transtypeGrid(1, 2, viewer))                 
                   if (self.viewType == 3):
                       self.logger.info("          Cell")
                       return(self.transtypeGrid(1, 3, viewer))                  
               else:
                   self.logger.error("Type of visualisation grid not set. Please, select a type of visualisation grid.")
               
            elif (self.currentDataField.Local == 2):
               if self.viewType > -1 : 
                   self.logger.info("Data Localised on Face and displayed on:")
                   if (self.viewType == 0):
                       self.logger.info("          Node")
                       self.logger.error("This conversion is not authorised")
                   if (self.viewType == 1):
                       self.logger.info("          Edge")
                       self.logger.error("This conversion is not authorised")
                   if (self.viewType == 2):
                       self.logger.info("          Face")
                       return(self.transtypeGrid(2, 2, viewer))
                   if (self.viewType == 3):
                       self.logger.info("          Cell")
                       return(self.transtypeGrid(2, 3, viewer))
               else:
                   self.logger.error("Error in cell transtyping. No visualisation cell type selected! Please select one before.")
                   
            elif (self.currentDataField.Local == 3):
               if self.viewType > -1 : 
                   self.logger.info("Data Localised on Cell and displayed on:")
                   if (self.viewType == 0):
                       self.logger.info("          Node")
                       self.logger.error("This conversion is not authorised")
                   if (self.viewType == 1):
                       self.logger.info("          Edge")
                       self.logger.info("This conversion is not authorised")
                   if (self.viewType == 2):
                       self.logger.info("          Face")
                       self.logger.error("This conversion is not authorised")
                   if (self.viewType == 3):
                       self.logger.info("          Cell")
                       return(self.transtypeGrid(3, 3, viewer))
               else:
                   self.logger.error("Error in cell trans-typing. No visualisation cell type selected! Please select one before.")
                   
            elif (self.currentDataField.Local == 5):
                   traj = vtkParticleTrajectoryBuilder(self.currentMeshField.MeshElementList)
                   traj.buildGrid()
                   outputName = self.currentDataField.Name+"Traj.vtk"         
                   if self.BUILD_DATA_PATH == 'ON':
                       fileName = os.path.join(GL_VTK_EXCHANGE, outputName)
                   else:
                       fileName = outputName
                   traj.writeToFile(fileName)
                   return(None)       
            else:
               self.logger.error("Data not localised. Conversion not possible.")
               return(None)
        
        
    def transtypeGrid(self, dimIn, dimOut, viewer):
        '''
        Transtype the cells of the mesh (e.g. transform a cloud of nodes into 
        the corresponding volumic cells) and call the DataField to vtkDataSet converter. 
        return the corresponding output vtkDataSet. 
        '''
        filePostfix = "NotSet"
        
        if dimOut == 0:
            filePostfix = "onNode"
        elif dimOut == 1:
            filePostfix = "onEdge"
        elif dimOut == 2:
            filePostfix = "onFace"
        elif dimOut == 3:
            filePostfix = "onCell"
        else: 
            self.logger.error("Output cell dimension not supported")

        converter = DataFieldToVtkDataSetThread()
        converter.setCassandraViewer(viewer)
        converter.setOutputFileName(self.currentDataField.Name + filePostfix)
        converter.setOutVtkDataSetList(self.currentOutVtkDataSetList)
        converter.setDataFieldIn(self.currentDataField)
        converter.setMeshFieldIn(self.currentMeshField)
        converter.setMesh(shared['Mesh'])
        converter.dimInOut( dimIn, dimOut)
        return(converter.start())

            
    def showErrorDialogue(self):
            self.logger.error("Error in cell transtyping. No visualisation cell type selected! Please select one before.")
 

    def showErrorDialogue(self, errorMessage):
            self.logger.error(errorMessage)

    def ExportToASCII(self):    
        if self.currentDataField != None:
            if self.exportControler == None:
                self.exportControler = Bin.DataExporter.ExporterControler.Controler()
            self.exportControler.setDataFieldName(self.currentDataField.Name)
            self.exportControler.showControlPanel()
        else:
            self.showErrorDialogue("No data to convert. Please select one dataField")
    
    def Export(self):
        '''
        Export as ASCII raw format (DFValue, MFId, Coords of NodesOnMeshElement.
        '''
        print "Export as ASCII raw format (DFValue, MFId, Coords of NodesOnMeshElement"

        self.fileNameOut = str(choose_save(sharedFiles["project_directory"])).strip()
        if (self.fileNameOut and self.allDataField and self.allDataField.List):
           self.fileNameOut = self.fileNameOut+".dat"
           fileOut =  open(self.fileNameOut, 'w')
           index = 0
           if (self.currentDataField.Local < 4):
               fileOut.write("# DataField export for volumic DataField \n")
               fileOut.write("# DataValue MeshElmId Xnode1 Ynode1 Znode1 Xnode2 Ynode2 Znode2... \n")
               for value in self.currentDataField.ValueList:
                   elmId = self.currentMeshField.MeshElementIdList[index]
                   MElmt = self.currentMeshField.MeshElementList[index]
                   index = index + 1
                   tmpLine = `value`+" "+`elmId`+" "
                   coordList = ''
                   if (MElmt.getSize() == 1): #(MElmt.Type == "NODE"):
                       Coord = MElmt.getCoord()
                       coordList = `Coord[0]` +" "+ `Coord[1]` +" "+ `Coord[2]`+" "
                   else:
                       for node in MElmt.MeshElementNodeList:
                           coordList = coordList + `node.Coord[0]` +" "+ `node.Coord[1]` +" "+ `node.Coord[2]`+" "
                   tmpLine = tmpLine + coordList + "\n"
                   fileOut.write(tmpLine)   
           elif self.currentDataField.Local == 4:
               fileOut.write("# DataField export for y=f(x) type \n")
               fileOut.write("# MeshElm DataValue \n")
               for index in xrange(len(self.currentDataField.ValueList)):
                   value = self.currentDataField.ValueList[index]
                   MElmt = self.currentMeshField.MeshElementList[index]
                   tmpLine = `MElmt`+" "+`value` + "\n"           
                   fileOut.write(tmpLine)
           elif self.currentDataField.Local == 5:
               fileOut.write("# DataField export for trajectories type \n")
               fileOut.write("# X Y Z DataValue \n")
               for index in xrange(len(self.currentDataField.ValueList)):
                   value = self.currentDataField.ValueList[index]
                   MElmt = self.currentMeshField.MeshElementList[index]
                   tmpLine = `MElmt[0]`+" "+`MElmt[1]`+" "+`MElmt[2]`+" "+`value`+"\n"           
                   fileOut.write(tmpLine)
           else: 
               print "Impossible to convert this dataField."
           fileOut.close()
           self.logger.info("Done")
               
                
                
    def DataFieldMapping(self):
        '''
        Performs the DataField mapping for the groups definition. 
        '''
        from Bin.FieldManager import FieldManager
        
        myFields = FieldManager()
        myFields.CreateDataField(shared['MeshGroupList'])
        myFields.FillFields(shared['MeshGroupList'], shared['MeshElmtList'])
        
        # defined data and corresponding fields are stoked in the
        # sharedData common dictionnary
        sharedData['AllDataField'] = myFields.GetAllDataField()
        sharedData['AllMeshField'] = myFields.GetAllMeshField()
        self.logger.info("Fields mapping done.")
                
        
    def delDataField(self):
        ''' 
        remove the current DataField
        '''
        if self.allDataField and self.allDataField.List:
            self.allDataField.Del_DataField(self.currentDataField)
            self.controlPanel.getSelectedDataField().removeItem(self.controlPanel.getSelectedDataField().getId())
            self.controlPanel.repaint()
            self.updatePanel()
        else:
            self.logger.error("No more DataField to remove")
   
   
    def SaveDataField(self):
        '''
        Saves the selected DataField by Jython serialisation. 
        '''
        self.logger.info("Save DataField")
        dialog = DirectoryDialog(sharedFiles["project_directory"])
        if (dialog.showDialog(None)):
            if (self.allDataField and self.allDataField.List):
                outputDir = dialog.getFileToSave().getAbsolutePath()                    
                try:                
                    print "Saving of", self.currentDataField.Name
                    dfpw = DataFieldPyWriter(self.currentDataField)
                    dfpw.setOutputDirPath(outputDir)
                    dfpw.write()
                except:
                    self.logger.warn("No dataField to save")
            

    def ExportToVTK(self):
        '''
        export to the VTK file format.
        '''
        self.logger.info("export to VTK file")
    
        if self.currentOutVtkDataSetList != None:
            for vtkDS in self.currentOutVtkDataSetList:
                self.vtkWriter = vtk.vtkDataSetWriter()
                self.vtkWriter.SetInput(vtkDS[1])
                self.vtkWriter.SetFileTypeToBinary()
                self.fileNameRoot = vtkDS[0]+".vtk"
                if self.BUILD_DATA_PATH == 'ON':
                    self.fileName = os.path.join(GL_VTK_EXCHANGE, self.fileNameRoot)
                else:
                    self.fileName = self.fileNameRoot
                print "vtk file name=", self.fileName
                self.vtkWriter.SetFileName(self.fileName)
                self.vtkWriter.Write()
            self.logger.info("export VTK done")
            return(vtkDS[1])
        else:
            self.logger.error("No vtkDataSet defined. Please build one before.")
        return(None)
           
    def ExportToCassandra(self):
        self.logger.info("Export data set to Cassandra")
        #if self.cassandraCaller == None:
        self.call3DViewer()
        self.BuildGrid(self.cassandraCaller.viewer)
                    
            
    def ShowValueList(self):
                
        print "Display the Value List"
        print "For the DataField of name", self.currentDataField.Name, " and Id ", self.currentDataField.Id
        print "The list of Values is:"
        print self.currentDataField.ValueList
        print "The corresponding mesh elements are:"
        print self.currentMeshField.MeshElementIdList         
            
    def editDataField(self):
        '''
        edit the current dataField
        '''
        if ( self.allDataField and self.allDataField.List):
            print "edition of the current dataField"
            
            
            #self.editDia = editDialog(create_internal_frame("Global View Settings",
            #                              sharedFrames["desktop_pane"]),
            #                              self.currentDataField)
            
            
            self.editDia = editDialog(self.frameManager.getNewFrame("Global View Settings"),self.currentDataField)

                                          
class DataFieldToVtkDataSetThread(Thread):
    """
    Threaded DataField to vtkDataSet exporter.
    """

    def __init__(self):
         Thread.__init__(self)
         
         # building of the related logger
         self.logger = LoggerFactory.getLogger("DataFieldToVtkDataSetThread")         
         self.BUILD_DATA_PATH = 'ON'
         self.isFileTypeToBinary = 1         
         self.viewer = None

    def setOutputFileName(self, outputName):
        self.outputName = outputName
         
    def setOutVtkDataSetList(self, OutVtkDataSetList):
        self.currentOutVtkDataSetList = OutVtkDataSetList
     
    def setDataFieldIn(self, dataFieldIn):
        self.dataFieldIn = dataFieldIn
      
    def setMeshFieldIn(self, meshFieldIn):
        self.meshFieldIn = meshFieldIn
     
    def setMesh(self, meshIn):
        self.mesh = meshIn
         
    def dimInOut(self, dimIn, dimOut):
        self.dimIn = dimIn
        self.dimOut = dimOut
     
    def setCassandraViewer(self, viewer):
        """
        set the linked Cassandra viewer for the export
        """
        self.viewer = viewer
              
    def run(self):
        # FIX ME
        #self.logger.info("Conversion pending, Please wait...")
        self.DFViewer = DataMeshViewer( self.dataFieldIn,  self.meshFieldIn, self.mesh, self.dimIn, self.dimOut)
        self.DFViewer.convertData()
        self.DFViewer.buildVtkDataSet()
        # FIX ME
        self.logger.info("                "+self.outputName+" built")
        self.currentOutVtkDataSetList.append([self.outputName, self.DFViewer.getVtkDataSet()])
        #FIX ME : should be done in JFreeMesh in place of here
        #DFViewer.getVtkDataSet().GetPointData().GetArray(0).SetName(self.dataFieldIn.Name+" "+self.dataFieldIn.Unit)
        #FIX ME
        #self.logger.info("Grid conversion done.")
         
        self.logger.info("Export to the Cassandra Pipeline Manager...")
        if self.viewer != None:
            self.viewer.getPipeLineManager().addDataSetAndBuildPipeline( self.DFViewer.getVtkDataSet(), self.dataFieldIn.Name)
        self.logger.info("    DONE")
            
        # saving of the corresponding VTK file
        self.logger.info("Saving of the corresponding vtkDataSet")
        self.writeVTKFile(self.DFViewer.getVtkDataSet())
         
         
         
    def getOutputVtkDataSet(self):
        return(self.DFViewer.getVtkDataSet)
         
         
    def writeVTKFile(self, vtkDataSetIn):
        vtkWriter = vtk.vtkDataSetWriter()
        vtkWriter.SetInput(vtkDataSetIn)
        if self.isFileTypeToBinary == 1:
            vtkWriter.SetFileTypeToBinary()
        else:
            vtkWriter.SetFileTypeToASCII()
        fileNameRoot = self.outputName+".vtk"
        if self.BUILD_DATA_PATH == 'ON':
            fileName = os.path.join(GL_VTK_EXCHANGE, fileNameRoot)
        else:
            fileName = fileNameRoot
        #FIX ME    
        #self.logger.info("vtk file name="+fileName)
        vtkWriter.SetFileName(fileName)
        vtkWriter.Write()
        #FIX ME
        #self.logger.info("VTK export done")
                                          
class editDialog:
    '''
    Edit the parameters (Name, Id...) of the DataField set in input.
    A JInternal frame shoudl be given in input. 
    '''
    def __init__(self, frame, theDataField):

        #self.frameManager = FrameManager()
        #self.frameManager.setGuicontext(sharedFlags['guiMode'])

        self.dataField = theDataField
        self.frame = frame
        
        self.dataPanel = JPanel()
        self.dataPanel.setLayout(GridLayout(4,2))
        self.frame.getContentPane().add(self.dataPanel, BorderLayout.CENTER)


        # to have something at the middle of the desktop
        #size = sharedFrames["desktop_pane"].getSize()
        # FIX ME:No clean at all 
        size = sharedFrames["gui"].getCurrentDesktop().getSize()
        dialogueWidth = 400
        dialogueHeight = 250
        self.frame.setSize(dialogueWidth, dialogueHeight)
        self.frame.reshape((int)(size.getWidth()/2 - dialogueWidth/2),
                           (int)(size.getHeight()/3 - dialogueHeight/2),
                           dialogueWidth, dialogueHeight)
        #self.frame.toFront()
        self.frame.setClosable(1)

        self.label = JLabel("Edition of the DataFileds properties")
        self.dataPanel.add(self.label)

        self.label2 = JLabel("")
        self.dataPanel.add(self.label2)

        self.label3 = JLabel("DataField Name")
        self.dataPanel.add(self.label3)


        self.annot0 = JTextField()
        self.annot0.setText(self.dataField.Name)
        self.dataPanel.add(self.annot0)

        self.label4 = JLabel("Description")
        self.dataPanel.add(self.label4)

        self.annot1 = JTextField()
        self.annot1.setText(self.dataField.Description)
        self.dataPanel.add(self.annot1)

        #FIX ME
        #self.exitBut = pawt.swing.JButton('Save and Exit')
        #self.dataPanel.add(self.exitBut)
        #elf.exitBut.actionPerformed = self.saveAndExit

        self.frame.show()
        self.frame.validate()
  
