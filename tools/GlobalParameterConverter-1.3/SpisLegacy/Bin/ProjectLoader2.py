"""
Project loader mdoule of SPIS-UI project in format 2 (default format).

**Project ref:**  Spis/SpisUI

**File name:**    ProjectLoader2.py

:status:          Implemented

**Creation:**     10/01/2006

**Modification:** 22/05/2006  validation

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

from Bin.Tasks.shared                   import *
from Bin.Tasks.common                   import *
from Bin.Tasks.TaskBuiltins             import *
from Bin.Tasks.FileChooserSwing         import *

from javax.swing                        import JPanel, BorderFactory, JProgressBar

import traceback
import sys, shutil, os, time, glob

from Bin.config                         import GL_DATA_PATH
from Bin.config                         import GL_SPISUIROOT_PATH
from Bin.config                         import GL_CMD_EDITOR
from Bin.config                         import GL_EXCHANGE
from Bin.config                         import GL_KERNEL_EXCHANGE
from Bin.config                         import GL_BLOCK_SIZE
from Bin.config                         import GL_SPIS_VERSION

from Bin.Tasks.Task                     import Task

#from Modules.Field                      import DataFieldReader
import Modules.Field.DataField
import Modules.Field.MeshField

from Modules.Field.DataFieldReader      import DataFieldReader
from Modules.Field.DataField            import DataField
from Modules.Field.MeshField            import MeshField
from Bin.Tasks.shared                   import sharedData
from Bin.Tasks.shared                   import sharedGroups
from Bin.Tasks.shared                   import sharedProp

from Modules.Field.DataFieldList        import DataFieldList
from Modules.Field.MeshField            import MeshField
from Modules.Field.MeshFieldList        import MeshFieldList
#from Modules.Groups.MeshGroup           import MeshGroup
#from Modules.Groups.GeoGroupList        import GeoGroupList

#from Modules.Properties.PlasmaList      import PlasmaList
#from Modules.Properties.MaterialList    import MaterialList
#from Modules.Properties.ElecNodeList    import ElecNodeList
#from Modules.Properties.Material        import Material

#from Modules.InOut.NascapMaterialsCatalogReader import NascapMaterialsCatalogReader

#from org.spis.imp.ui.util               import DirectoryDialog
#from com.artenum.free.mesh.io           import GmshLoader
#from com.artenum.free.mesh              import Mesh
from Modules.Groups.MeshGroupList       import MeshGroupList

from Bin.ProjectLoader                  import ProjectLoader
#from Bin.FrameManager                   import FrameManager

from threading                          import Thread
from Bin.config                         import GL_MAX_THREADS_STACK

#from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory
from Modules.Utils.LoggingUtilities     import LoggingUtilities
from org.slf4j.profiler       import Profiler
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

class ProjectLoader2(ProjectLoader):
    '''
    Project loader class of SPIS-UI project in format 2 (default format).
    For further information regarding the file format, please see the SPIS-UI 
    User Manual and/or the corresponding Technical Note. 
    '''

    def __init__(self):
        ProjectLoader.__init__(self)
        
        # building of the related logger
        self.logger = LoggerFactory.getLogger("ProjectLoader")
        self.logger.info("ProjectLoader2 initialised")
        self.loggingUtilities = LoggingUtilities(self.logger)

    def setLoadingList( self, loadingList):
        
        self.keysList = loadingList
        print self.keysList
        
    def buildProgresBarFrame(self, frameManagerIn):
        '''
        build a progress frame. 
        '''
        self.prgBarFrame = frameManagerIn.getNewFrame("Project loading")
        if self.prgBarFrame != None:
            self.prgBar = JProgressBar()
            empty = BorderFactory.createEmptyBorder()
            prgPanel = JPanel()
            prgPanel.setBorder( empty )
            self.prgBar.setMinimum(0)
            self.prgBar.setMaximum(10)
            prgPanel.add(self.prgBar)
            self.prgBarFrame.getContentPane().add(prgPanel)
            self.prgBarFrame.reshape(40, 40, 256, 70)
            self.prgBarFrame.show()
        
    def setPrgBarValue(self, value):
        if self.prgBarFrame != None:
            self.prgBar.setValue(value)

    def setPrgBarMaxValue(self):
        if self.prgBarFrame != None:
            self.setPrgBarValue(self.prgBar.getMaximum()) 

    def closeProgresBarFrame(self):
        if self.prgBarFrame != None:
            self.prgBarFrame.dispose()
            self.prgBarFrame = None
        
    def load(self, projectPathIn):
        '''
        Load the project.
        '''
    
        #frameManager = FrameManager()
        #frameManager.setGuicontext(0) #sharedFlags['guiMode'])
        #self.buildProgresBarFrame(frameManager)
        
        #######################################################################
        dir1 = projectPathIn   #sharedFiles["project_directory"]    
        if (dir1 != None and dir1 !="" and dir1 !="None"):
            
            dir = str(dir1).strip()
            
            # we add the dir path to the path for the python modules loading
            sys.path.append(dir)
            materialDir = dir+os.sep+"Properties"+os.sep+"Materials"
            sys.path.append(materialDir)
            elecNodeDir = dir+os.sep+"Properties"+os.sep+"ElecNodes"
            sys.path.append(elecNodeDir)
            plasmaDir = dir+os.sep+"Properties"+os.sep+"Plasmas"
            sys.path.append(plasmaDir)
            dataFieldDir = dir+os.sep+"DataFields"
            sys.path.append(dataFieldDir)
            meshFieldDir = dir+os.sep+"DataFields"+os.sep+"MeshFields"
            sys.path.append(meshFieldDir)
            grpDir = dir+os.sep+"Groups"
            sys.path.append(grpDir)
            geomDir = dir+os.sep+"Geom"
            sys.path.append(geomDir)
            
            numKernelParamInDir = dir+os.sep+"NumKernel"+os.sep+"Input"
            numKernelParamOutDir = dir+os.sep+"NumKernel"+os.sep+"InOutput"
            
            nascapPropertiesDir = os.path.join(materialDir, "NascapProperties")
            
            filename = os.path.join(dir, "spis")

            project_file = os.path.join(dir,"project")
            if not os.path.isfile(project_file):
                self.logger.error("SPIS project reference file not found. Invalid project")
                self.closeProgresBarFrame()
                return(-1)
                
            sharedFiles["project_directory"] = dir1
            self.logger.info(sharedFiles["project_directory"])

            if self.logger.isDebugEnabled():
                timeProfiler = Profiler("ProjectLoader")
                timeProfiler.start("DataFields manager initialisation")
                
            ################################# 
            # project informations loading
            #################################
            if "projectInfo" in self.keysList:
                self.logger.info("Loading project's informations")
                try:
                #if(1):
                    load_dict(sharedProjectInfos, project_file)
                    self.logger.info("Done")
                except:                    #print >> sys.stderr, "No project file. Probably invalid directory."
                    self.logger.warn("No project file. Probably invalid directory.")
                    
                # check the version compliance
                if sharedProjectInfos.has_key("projectVersion"):
                    if (sharedProjectInfos["projectVersion"] < GL_SPIS_VERSION):
                        self.logger.warn("The project version is older than the current SPIS'one:"+str(sharedProjectInfos["projectVersion"])+" versus "+GL_SPIS_VERSION+"/n"
                                         +"The compliance with the current version cannot be guaranty! \n"
                                         + "Please check your data and update your project format !!!")
                    elif (sharedProjectInfos["projectVersion"] > GL_SPIS_VERSION):
                        self.logger.warn("The project version is higher than the current SPIS'one:"+str(sharedProjectInfos["projectVersion"])+" versus "+GL_SPIS_VERSION+"/n"
                                         +"The compliance with the current version cannot be guaranty! \n")
                else:
                    self.logger.warn("The project has no version number defined ! \n"
                                     + "The compliance with the current version cannot be guaranty! \n"
                                     + "Please check your data and update your project format !!!")
                    

                # names and files ref
                self.logger.info("Loading files names and references")
                tmpName = filename + "-names"
                if (os.path.isfile(tmpName)):
                    tmpDic = {}
                    try:
                        load_dict(tmpDic, tmpName)
                        for key in tmpDic.keys():
                            sharedFiles[key] = tmpDic[key]
                        self.logger.info("Done")
                    except:
                        self.logger.error("Error in files names and reference")
                else:
                    self.logger.error("Impossible to load ", tmpName)
                sharedFiles["project_directory"] = dir
                self.logger.info("project directory updated: ", sharedFiles["project_directory"])
            #self.setPrgBarValue(1)
                
            self.logger.info("keyList at CAD loading", self.keysList)
            
            #################################
            # load CAD file reference loading
            #################################
            '''
            if "geomFile" in self.keysList:
                try:
                    self.logger.debug("loading of workSpaceDescription.py")
                    tmpCmd = "import workSpaceDescription"
                    exec(tmpCmd)
                    tmpCmd = "self.tmpGeomFileName = workSpaceDescription.workSpaceDescription.nameMainFile"
                    exec(tmpCmd) 
                    tmpCmd = "sharedFiles['TheCADFileIn'] = os.path.join(dir,'Geom', self.tmpGeomFileName)"
                    exec(tmpCmd)                
                    self.logger.debug(sharedFiles['TheCADFileIn'])
                    
                    fileList = os.listdir(geomDir)
                    os.path.join(GL_EXCHANGE, "Geom")
                    if ( fileList != []):
                        for file in fileList:
                            if file != "workSpaceDescription.py" and file != "workSpaceDescription$py.class":
                                fileNameIn = os.path.join(geomDir, file)
                                fileNameOut = os.path.join(GL_EXCHANGE, "Geom", file)
                                shutil.copyfile(fileNameIn, fileNameOut)
                except:
                    self.logger.warn("No GEOM workspace defined./n Try to load the old format of GEOM.")
                    InfileList = os.listdir(dir)
                    if ("cad_sav.geo" in InfileList):
                        self.logger.info("Ok, there is a unrolled CAD file previously saved. Let's go with it.")
                        sharedFiles['TheCADFileIn'] = os.path.join(dir,"cad_sav.geo")
                        self.logger.info("Reference CAD file:"+sharedFiles['TheCADFileIn'])
                    else:
                        self.logger.warn( "Humm... This is quite strange. Apparently you have no CAD file in your project. \n"
                                           +"Only the reference to the initial file has been saved. I recommend you to check \n"
                                           +"what you are currently doing.")
            self.setPrgBarValue(2)
            '''

            #########################        
            # Properties loading
            #########################
            '''
            self.logger.info("Loading materials and properties")

            ###############################   
            # Material Properties loading  
            ###############################     
            if "materials" in self.keysList:                   
                self.logger.info("Loading material modules")
                sharedProp['defaultMaterialList'] = MaterialList()
                try:
                    selectedList = glob.glob(os.path.join(materialDir, "material*.py"))
                    #print "*****> ", selectedList
                    for pls in selectedList:
                        #print "+++++++++++++++> ", pls.split(os.sep)[-1]
                        tmpName = pls.split(os.sep)[-1][:-3]
                        #print "----------------------> ", tmpName
                        try:
                            self.logger.debug("loading of ", tmpName)
                            tmpCmd = "import "+tmpName
                            self.logger.debug(tmpCmd)
                            exec(tmpCmd)
                            tmpCmd = "sharedProp['defaultMaterialList'].Add_Material("+tmpName+".material)"
                            self.logger.debug(tmpCmd)
                            exec(tmpCmd)
                        except:
                            self.logger.warn("Impossible to load "+ tmpName)
                            self.loggingUtilities.printStackTrace()
                               
                except: 
                    self.logger.warn("No material to load.")
                    #self.loggingUtilities.printStackTrace()
                
                # loading  extra parameters for NASCAP based materials
                self.logger.info("    Loading NASCAP material extra parameters... ")
                try:
                    #if(1):
                    tmpName = "selectedNascapMaterialList"
                    tmpCmd = "import "+tmpName
                    self.logger.debug(tmpCmd)
                    exec(tmpCmd)
                    
                    tmpCmd = "sharedProp['materialModel'] = "+tmpName+".materialModel"
                    self.logger.debug(tmpCmd)
                    exec(tmpCmd)
                    
                    tmpCmd = "sharedProp['selectedNascapMaterialList'] = "+tmpName+".selectedNascapMaterialList"
                    self.logger.debug(tmpCmd)
                    exec(tmpCmd)
                    self.logger.info("         DONE")
                except:
                    self.logger.warn("Impossible to load "+ tmpName)
                    self.loggingUtilities.printStackTrace()
                    
                    
                self.logger.info("    Loading NASCAP material catalog... ")
                try:
                #if(1):               
                    # loading of the related NASCAP properties if needed
                    nascapLoadingFlag = 0
                    for mat in sharedProp['defaultMaterialList'].List:
                        if (mat.Type == Material.NASCAP_2K_MATERIAL or mat.Type == Material.NASCAP_MATERIAL):
                            nascapLoadingFlag= 1
                    if (nascapLoadingFlag == 1):
                        nascapReader = NascapMaterialsCatalogReader()
                        nascapReader.read(nascapPropertiesDir)
                    self.logger.info("         DONE")
                except: 
                    self.logger.warn("No NASCAP material to load.")

            '''
                  
            ###########################
            # loading of electrical Node
            ###########################
            '''
            if "elecNodes" in self.keysList:
                self.logger.info("Loading electrical nodes modules")
                selectedList=[]
                sharedProp['defaultElecNodeList'] = ElecNodeList()
                try:
                    fileList = os.listdir(elecNodeDir)
                    for elm in fileList:
                        if(elm[-3:]==".py"):
                            selectedList.append(elm)
                    for pls in selectedList:
                        tmpName = pls[:-3]
                        try:
                            self.logger.debug("loading of ", pls)
                            tmpCmd = "import "+tmpName
                            exec(tmpCmd)
                            tmpCmd = "sharedProp['defaultElecNodeList'].Add_ElecNode("+tmpName+".elecNode)"
                            exec(tmpCmd)
                        except:
                            self.logger.warn("Impossible to load " + tmpName +"\n")
                            self.loggingUtilities.printStackTrace()
                except:
                    self.logger.warn("No elecNodes to load.")
            '''        
                   
            ##########################
            # loading of plasma
            ##########################	
            '''
            if "plamas" in self.keysList: 
                self.logger.info("Loading plasma modules")
                selectedList = []
                sharedProp['defaultPlasmaList'] = PlasmaList()
                try:
                    fileList = os.listdir(plasmaDir)
                    for elm in fileList:
                        if(elm[-3:]==".py"):
                            selectedList.append(elm)
                    for pls in selectedList:
                        tmpName = pls[:-3]
                        try:
                            self.logger.debug("loading "+ pls)
                            tmpCmd = "import "+tmpName
                            exec(tmpCmd)
                            tmpCmd = "sharedProp['defaultPlasmaList'].Add_Plasma("+tmpName+".plasma)"
                            exec(tmpCmd)                                
                        except:
                            self.logger.warn("Impossible to load "+tmpName)
                            self.loggingUtilities.printStackTrace()
                except:
                    self.logger.warn("No plasma to load.")
            
            if (sharedProp['defaultPlasmaList'] != None):                
                self.validatePlasma()
            else:
                self.logger.info("No plasma loaded. Validation tests by-passed")
    
            self.setPrgBarValue(3)
            '''
                
            ############################   
            # load groups 
            ############################
            '''
            if "groups" in self.keysList:                  
                    self.logger.info("Loading groups")
                    tmpName = filename + "-groups"
                    if (os.path.isfile(tmpName)):
                        try: 
                            self.logger.debug("Try to load group in the old format")
                            load_dict(sharedGroups, tmpName)
                        except:
                            self.logger.error("Impossible to load " + tmpName + " probably problem of data consistency")
                    else:
                        self.logger.debug("loading the new format")
                        selectedList = []
                        sharedGroups['GeoGroupList'] = GeoGroupList()
                        try:
                            fileList = os.listdir(grpDir)
                            for elm in fileList:
                                if (elm[-3:]==".py"):
                                    selectedList.append(elm)
                                   
                            # re-ordering according to the priority list
                            self.logger.debug("loading groupsPriorityList")
                            try:
                                tmpCmd = "import groupsPriorityList.py"+tmpName
                                exec("import groupsPriorityList")
                                tmpList = []
                                for Id in groupsPriorityList.prioList:
                                    try:
                                        tmpList.append(selectedList[selectedList.index("geoGroup"+`Id`+".py")])
                                    except:
                                        self.logger.warn("Group"+`Id`+" not found in the file list, skipped.")
                                selectedList = tmpList
                            except:
                                self.logger.warn("Impossible to load the priority list (probably missing). Please check groups priority!")
                          
                            # loading of meta-groups (if any)
                            self.logger.debug("loading of meta-groups (if any)")
                            try:
                                exec("import metaGroupsDic")
                                sharedGroups["metaGrpDic"] = metaGroupsDic.metaGrpDic
                            except:
                                self.logger.info("No meta group found")                           
                          
                            for pls in selectedList:
                                tmpName = pls[:-3]
                                try:
                                    self.logger.debug("loading "+ pls)
                                    tmpCmd = "import "+tmpName
                                    exec(tmpCmd)
                                    tmpCmd = "sharedGroups['GeoGroupList'].Add_Group("+tmpName+".group)"
                                    exec(tmpCmd)
                                    tmpCmd = "self.tmpGrpId = "+tmpName+".group.Id"
                                    exec(tmpCmd)
                                    tmp = sharedGroups['GeoGroupList'].GetElmById(self.tmpGrpId)
                                    
                                    if tmp == None:
                                        self.logger.warn("Error to recover current Geo group")
                                    else:
                                        self.tmpGrp = tmp
                                    
                                    tmp = sharedProp["defaultPlasmaList"].GetElmById(self.tmpGrp.Plasma.Id)
                                    if tmp == None:
                                        self.logger.warn("Warning in Plasma property re-connection")
                                    else:
                                        self.tmpGrp.Plasma = tmp
                                        
                                    tmp = sharedProp["defaultMaterialList"].GetElmById(self.tmpGrp.Material.Id)
                                    if tmp == None:
                                        self.logger.warn("Warning in Material property re-connection")
                                    else:
                                        self.tmpGrp.Material = tmp
                                    
                                    tmp = sharedProp["defaultElecNodeList"].GetElmById(self.tmpGrp.ElecNode.Id)
                                    if tmp == None:
                                        self.logger.warn("Warning in ElectNode property re-connection")
                                    else:
                                        self.tmpGrp.ElecNode = tmp
                                except:
                                    self.logger.warn("Impossible to load "+ tmpName)
                                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                                    self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                                    self.logger.debug("       "+ repr( exceptionValue))
                            sharedControls['groupLoadingFlag'] = 1
                        except:
                            self.logger.warn("No groups defined")
                            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                            self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                            self.logger.debug("       "+ repr( exceptionValue))
            '''

            
            ############################   
            # load globals 
            ############################
            
            if "globals" in self.keysList:  
                self.logger.info("Loading global parameters")
                tmpName = filename + "-globals"
                if (os.path.isfile(tmpName)):
                    load_dict(sharedGlobals, tmpName)
                else:
                    self.logger.error("Impossible to load " +tmpName)
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                    self.logger.debug("       "+ repr( exceptionValue))
            
            
            ############################   
            # load additional parameters of numerical kernel 
            ############################
            '''
            if "numKernelParam" in self.keysList:
                self.logger.info("Loading of additional parameters of the numerical kernel")
                try: 
                    fileList = os.listdir(numKernelParamInDir)
                    if ( fileList != []):
                        for file in fileList:
                            shutil.copyfile(os.path.join(numKernelParamInDir, file), os.path.join(GL_KERNEL_EXCHANGE, file))
                    else:
                        self.logger.warn("No numerical parameters for kernel to load")
                except:
                    self.logger.error("Error in numKernelParam. See log console for further informations.")
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                    self.logger.debug("       "+ repr( exceptionValue))
            
            sharedFiles["projectLoadingFlag"] = 1
            sharedFiles["projectSavingFlag"] = 1
            
            self.logger.info("Pre-processing phase 2")
            self.setPrgBarValue(4)
            '''

            
            ##############################    
            # load CAD into the framework
            ##############################
            '''
            if "geomLoading" in self.keysList:
                self.logger.info("CAD import")
                sharedTasks["context"] = 0
                sharedTasks['manager'].run_tasks('CADImporter')
                sharedTasks["manager"].set_done_task("CADImporter")
            self.setPrgBarValue(5)
            '''
            
            ###############################  
            # Mesh loading
            ###############################
            '''
            if "meshLoading" in self.keysList:   
                sys.stdout.write("Loading mesh... ")
                mesh = Mesh()
                try:
                    print "Mesh Importing. Please wait..."
                    fileNameIn = os.path.join(dir, "Tmp3D.msh")
                    print "Selected file: ", fileNameIn
                    fileNameOut = os.path.join(GL_EXCHANGE, "Tmp3D.msh")
                    
                    try:
                        shutil.copyfile(fileNameIn, fileNameOut)
                    except:
                        self.logger.warn("Mesh file missing")
               
                    print "Loading file (exchange copy of selected file): ", fileNameOut
                    mesh.load(GmshLoader(fileNameOut))
                    shared['Mesh'] = mesh
                    print "Nb cell in loaded mesh", mesh.getNbCell()
                    shared['MeshGroupList'] = MeshGroupList()
                except:
                    self.logger.error("Impossible to import mesh file: " + fileNameOut+ "/n"
                                      + "Please, check if your mesh file is not corrupted or missing!"
                                      + "If this one remains impossible to reload, try to re-mesh it \n by calling the mesher.")
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                    self.logger.debug("       "+ repr( exceptionValue))

                # to avoid to re_mesh the mesh 
                sharedTasks["manager"].set_done_task("Mesher3D")
                self.logger.info("Done")
            self.setPrgBarValue(6)
            '''
            
            ##################################
            # load DataFields and MeshFields
            ##################################
            '''
            if "preproDFLoading" in self.keysList:   
                self.logger.info("Loading of DataFields and MeshFields")
                if (sharedData['AllDataField'] == None):
                    self.logger.debug("No pre-existing DataFields")
                    sharedData['AllDataField'] = DataFieldList()
                if (sharedData['AllMeshField'] == None):
                    self.logger.debug("No pre-existing MeshFields")
                    sharedData['AllMeshField'] = MeshFieldList()
                
                #selectedList=[]
                fileList = os.listdir(os.path.join(dir, "DataFields"))
                # to extract only the right files
                fileList = [elem for elem in fileList if elem[:3] == "df_"]
                 
                
                threadManager = ThreadPoolManager()
                sizeListOfData = len(fileList)

                # for test purpose (only)
                #threadManager.nbMaxThreads=1

                for thrId in xrange(threadManager.nbMaxThreads):
                    indexStart = (thrId*sizeListOfData)/threadManager.nbMaxThreads
                    if thrId*(sizeListOfData+1)/threadManager.nbMaxThreads < sizeListOfData:
                        indexEnd = (thrId+1)*sizeListOfData/threadManager.nbMaxThreads
                    else:
                        indexEnd = sizeListOfData
                    tmpList = fileList[indexStart:indexEnd]
                    #print "tmp List ----------------->", tmpList
                    readData = DataFieldMultiReader(threadManager)
                    readData.setList(tmpList)

                    #print threadManager.NbRunningThreads
                    #print tmpList

                    #readData.setThreadCont(NbRunningThreads)
                 
                    # in multi-threaded mode
                    readData.start()
                    # in direct mode (for test purpose)
                    #readData.run()
                
                # we stop until all threads are finished
                threadManager.globalLock()
                
                
                # FIXME : divergence with the old version
                if shared['Mesh'] != None:
                    
                    for meshField in sharedData['AllMeshField'].List:
                        try:
                            self.logger.info("Re-building connectivity for "+meshField.Name+"... ")
                            if meshField.Local == 0:
                                meshField.MeshElementList = shared['Mesh'].getNodesByIds(meshField.MeshElementIdList)
                            if meshField.Local == 1:
                                meshField.MeshElementList = shared['Mesh'].getEdgesByIds(meshField.MeshElementIdList)
                            if meshField.Local == 2:
                                meshField.MeshElementList = shared['Mesh'].getFacesByIds(meshField.MeshElementIdList)
                            if meshField.Local == 3:
                                meshField.MeshElementList = shared['Mesh'].getCellsByIds(meshField.MeshElementIdList)
                            if meshField.Local == 4:
                                meshField.MeshElementList = meshField.MeshElementIdList    #this is not clean but...
                            self.logger.info("Done")
                        except:
                            self.logger.warn("Impossible to rebuild connectivity for "+ meshField.Name)
                            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                            self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                            self.logger.debug("       "+ repr( exceptionValue))
                else:
                    self.logger.error("Impossible to rebuild connectivity because no mesh loaded")
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
                    self.logger.debug("       "+ repr( exceptionValue))
                
                sharedTasks["manager"].set_done_task("InitFields")
                sharedTasks["manager"].set_done_task("FieldManager")
            self.setPrgBarValue(7)    
            '''
            
            # to declare to the whole framework that we are starting from a 
            # project (useful for the group definition)
            sharedControls['projetLoadingFlag'] = 2
            

            '''
            self.setPrgBarMaxValue()
                           
            # just to see that everything is done before to close the window
            time.sleep(0.2)
            self.closeProgresBarFrame()
            # to print the time cost
            if self.logger.isDebugEnabled():
                timeProfiler.stop().print()
            '''

    def validatePlasma(self):
        """
        Validates the compliance of the loaded plasma with the current version of SPIS
        """
        self.logger.debug("Validation of the loaded plasma")
        for plasma in sharedProp["defaultPlasmaList"].List:
            foundData = plasma.DataList.GetElmsByName('EdgeRadiusS')
            for data in foundData:
                if (data.Type == "Int*1"):
                    data.Type = 'FLOAT'
                    self.logger.warn( "Deprecated type for EdgeRadiusS in "+plasma.Name+"\n"
                                      +"automatically corrected to FLOAT. We recommend to save your project to update the disk data.")
           
class ThreadPoolManager:
    def __init__(self):
        self.logger = LoggerFactory.getLogger("DataFieldMultiReader")
        self.loggingUtilities = LoggingUtilities(self.logger)
        
        self.nbMaxThreads = GL_MAX_THREADS_STACK
        self.NbRunningThreads = 0

    def setThreadCont(self, cont):
        self.NbRunningThreads = cont

    def decreasesThreadsCont(self):
        self.NbRunningThreads = self.NbRunningThreads - 1

    def increasesThreadsCont(self):
        self.NbRunningThreads = self.NbRunningThreads + 1

    def globalLock(self):
        while self.NbRunningThreads > 0:
            self.logger.debug("waiting: Nb threads still alive: "+`self.NbRunningThreads`)
            time.sleep(5)

    def escape(self):
        self.NbRunningThreads = 0

    def printTest(self):
        print "XXXXXXXXXXXX TEST XXXXXXXXXXXX"
        
    def setPath(self, path):
        self.path = path


class DataFieldMultiReader(Thread):
    
    def __init__(self, threadPoolManager):
        Thread.__init__(self)
        self.list = None
        self.threadsCont = 1
        #self.threadId = 0
        self.threadPoolManager = threadPoolManager
        #self.threadPoolManager.printTest()
        self.threadPoolManager.increasesThreadsCont()
          
        # building of the related logger
        self.logger = LoggerFactory.getLogger("DataFieldMultiReader")
        self.loggingUtilities = LoggingUtilities(self.logger)
        
    def setThreadPoolManager(self, threadPoolManager):
        self.threadPoolManager = threadPoolManager

    def setList(self, list):
        self.list = list

        #def setThreadCont(self, cont):
        #    self.threadsCont = cont
         
        #def decreasesThreadsCont(self):
        #    self.threadsCont = self.threadsCont - 1

    def run(self):
        #print "list in runner--->", self.list
        for dfName in self.list:
            print "loading :", dfName
            try:
            #if(1):
                tmpCmd = "import "+dfName+".data_field"
                #print "cmd ---->", tmpCmd
                exec(tmpCmd)
                
                tmpCmd = "sharedData['AllDataField'].Add_DataField("+dfName+".data_field.savedData )"
                #print "cmd --------->", tmpCmd
                exec(tmpCmd)
                
                tmpCmd = "self.IdTmp = "+dfName+".data_field.savedData.MeshFieldId"
                #print "cmd -------------->", tmpCmd
                exec(tmpCmd)

                tmpCmd = "import "+dfName+".meshfield"+`self.IdTmp`
                #print "cmd ------------------->", tmpCmd
                exec(tmpCmd)
                  
                tmpCmd = "sharedData['AllMeshField'].Add_MeshField("+dfName+".meshfield"+`self.IdTmp`+".savedData )"
                #print "cmd ------------------------->", tmpCmd
                exec(tmpCmd)
            except:
                self.logger.warn("Data Field not supported ! \n"
                                 +"      Impossible to load "+dfName)
                self.loggingUtilities.printStackTrace()

        #print "list in runner done"          
        self.threadPoolManager.decreasesThreadsCont()
        print "Thread free"
