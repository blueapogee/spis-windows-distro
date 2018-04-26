'''
Created on Sep 6, 2010

@author: juju
'''
import os, string 
from threading import Thread

from Bin.config         import GL_DEFAULT_WIZARD_PATH
from Bin.config         import GL_CURRENT_WIZARD_PATH
from Bin.config         import GL_SPISUIROOT_PATH
from Bin.config         import GL_EXCHANGE
from Bin.config         import GL_KERNEL_EXCHANGE

import java
from javax.swing import JFileChooser
from java.awt.event import ActionListener

from Bin.GeomManager          import GeomManager
from Bin.Tasks.Task           import Task
from Bin.Tasks.common         import create_internal_frame
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedTasks
from Bin.Tasks.shared         import sharedGlobals
from Bin.Tasks.shared         import sharedFlags
from Bin.Tasks.shared         import sharedProp
from Bin.Tasks.shared         import sharedGroups
from Bin.Tasks.shared         import sharedData

from Bin.ProjectLoader2       import ProjectLoader2

from Modules.Utils.LoggingUtilities     import LoggingUtilities
from Modules.InOut.ExtendedProjectManager import ExtendedProjectManager

from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from com.artenum.shaman.event import ShamanListener
from com.artenum.shaman.event import ShamanEvent
from com.artenum.shaman.event import ShamanEventType

from org.spis.imp.ui.wizard import WizardManager  

class TaskWizardManager(Task, ShamanListener):
    '''
    Call and control the Modelling Wizard manager based on Artenum Shaman. 
    This is used, for instance, for the ESD modelling wizard.
    '''
        
    def run_task(self):
        
        self.logger = LoggerFactory.getLogger("Task")
        self.loggingUtilities = LoggingUtilities(self.logger)
        
        # to simplify the identification of each panel
        self.PROJECT_PANEL = "element 1"
        self.GEOMETRY_PANEL = "element 2"
        self.MATERIAL_PANEL = "element 4"
        self.SPACE_ENV_PANEL = "element 5"
        self.SIM_SETTINGS_PANEL = "element 6"
        self.SIM_RUN_DASHBOARD_PANEL = "element 7"
        self.POST_PRO_PANEL = "element 8"
        
        self.isPanelSet = 0

        self.logger.debug(GL_DEFAULT_WIZARD_PATH)
        chooser = JFileChooser(GL_DEFAULT_WIZARD_PATH) 
        chooser.showDialog(None, None)
        scenario = chooser.getSelectedFile()
                
        # in UI context
        if sharedFlags['guiMode'] == 1:            
            self.internalFrame = create_internal_frame("Modelling Wizard",sharedFrames["gui"].getCurrentDesktop())
            size = self.internalFrame.getParent().getSize()
            
            self.manager = WizardManager()
            self.manager.setScenarioName(scenario.getAbsolutePath())
            self.manager.setInternalFrame(self.internalFrame)
            self.manager.run()            
            self.manager.addActionListener(self)

            self.initPanelsConnection()            
            
            # set the visibility of the frame
            self.internalFrame.reshape(0,0,2*size.width/3,size.height)
            self.internalFrame.setVisible(1)
            
    def initPanelsConnection(self):
        
            # setting of the models inputs
            sharedFrames["esdPanelsList"]= self.manager.getShamanables()
            
            ####################################################
            # model setting for the project panel
            ###############################
            self.projectPanel = self.manager.getShamanable(self.PROJECT_PANEL)
            sharedFrames["projectPanel"] = self.projectPanel
            self.projectPanelModel = java.util.HashMap()
            self.projectPanel.setModel(self.projectPanelModel)
            tmpPath = os.path.join(GL_SPISUIROOT_PATH, "..", "Data", "TemplateProjects", "ESD", "TP_ESD_RC1.spis")
            self.projectPanel.getGui().setTemplatePath(tmpPath )
            self.projectPanel.getGui().setfromTemplateSelected(0)
            
            #################################################
            # Model setting for the geometry panel
            #################################################
            self.geomPanel = self.manager.getShamanable(self.GEOMETRY_PANEL)
            self.geomPanelModel = java.util.HashMap()
            self.geomManager = GeomManager()
            
            #################################################
            # Material settings panel
            #################################################
            self.materialPanel = self.manager.getShamanable(self.MATERIAL_PANEL)
            self.materialPanelModel = java.util.HashMap()
            
            #################################################
            # model setting for the space environment panel
            #################################################
            self.spaceEnvPanel = self.manager.getShamanable(self.SPACE_ENV_PANEL)
            self.spaceEnvModel = java.util.HashMap()
            
            #################################################
            # simulation settings panel
            #################################################
            self.simSettingPanel = self.manager.getShamanable(self.SIM_SETTINGS_PANEL)
            self.simSettingModel = java.util.HashMap()
            
            # model setting for the run Simulation panel
            simulationRunPanel = self.manager.getShamanable(self.SIM_RUN_DASHBOARD_PANEL)
            self.simulationControlModel = java.util.HashMap()
            simulationRunPanel.getGui().setModel(self.simulationControlModel)
            
            #################################################
            # post-processing panel
            #################################################
            self.postProPanel = self.manager.getShamanable(self.POST_PRO_PANEL)
            self.postProModel = java.util.HashMap()
            self.postProPanel.getGui().setModel(self.postProModel)
            actionListener = PostprocessingActionListener()
            actionListener.addActionCmdCouple( self.postProPanel.getGui().SAVE_PROJECT_ACTION, "SaveProj")
            actionListener.addActionCmdCouple( self.postProPanel.getGui().CALL_DATAFIELD_MANAGER_ACTION, "BuildDataFieldChooser")
            actionListener.addActionCmdCouple( self.postProPanel.getGui().EXPORT_TO_ASCII_ACTION, "ExportAllDF")
            self.postProPanel.getGui().addActionListenerToSaveProjectButton(actionListener)
        
        
    def onShamanEvent(self, event ):
        """
        this method should be implemented to respect the API of the ShamanListener interface.
        """        
        currentShamanable = self.manager.getCurrentShamanable()        
        eventType = event.getType() 
        if (eventType == ShamanEventType.CANCEL):
            self.internalFrame.setVisible(0)
            self.InternalFrame = None
            self.logger.info("End of the wizard")
        elif(eventType == ShamanEventType.NEXT_REQUESTED):
            self.logger.debug("NEXT_REQUESTED")
            
            #####################################################
            # Handling of the project setting phase (i.e panel)
            #####################################################
            if ( currentShamanable.getId() == self.PROJECT_PANEL):
                projectValidFlag = 0
                self.projectPanel.getGui().updateModel()
                                
                projectPath  = currentShamanable.getModel().get("projectPath")
                if ( projectPath != None):
                    if (currentShamanable.getModel().get("generateFromTemplate")):
                        templatePath = currentShamanable.getModel().get("templatePath")
                        if ( templatePath != None ):
                            self.logger.info("Project creation")
                            self.logger.info("    from template path: " + templatePath)
                            self.logger.info("    to project path: " + projectPath)
                            #self.makeProjectFromTemplate( templatePath, projectPath)
                            projectManager = ExtendedProjectManager()
                            projectValidFlag = projectManager.makeProjectFromTemplate( templatePath, projectPath)
                    else:
                        # update of the project informations
                        sharedFiles["project_directory"] = projectPath
                        sharedFiles["projectSavingFlag"] = 1
                        projectValidFlag = 1
                else: 
                    self.logger.error("The project path seems invalid. Please select a valid project path.")
                
                if (projectValidFlag):
                    # loading of the project
                    self.logger.info("Project loading... ")
                    loadingList = [ "projectInfo", "geomFile", "elecNodes", "plamas", "groups", "globals", "meshLoading", "numKernelParam", "materials"]
                    loader = ProjectLoader2()
                    loader.setLoadingList(loadingList)
                    loader.load()
                    self.logger.info("Project loaded")
            
            #####################################################
            # Handling of the geometric settings
            #####################################################
            elif ( currentShamanable.getId() == self.GEOMETRY_PANEL):
                
                #safer
                self.geomPanel.getGui().updateModel()
                
                #FIXME: gerer le cas ou changmeent de fichiers de geom.
                 
                # more robust approach
                tmpDic = {}
                keyList = []
                keyList.append(self.geomPanel.getGui().L_BOX_X)
                keyList.append(self.geomPanel.getGui().L_BOX_Y)
                keyList.append(self.geomPanel.getGui().L_BOX_Z)
                keyList.append(self.geomPanel.getGui().L_DIELEC_X)
                keyList.append(self.geomPanel.getGui().L_DIELEC_Z)
                keyList.append(self.geomPanel.getGui().ALPHA)
                for key in keyList: 
                    tmpDic[ key ] = self.geomPanelModel.get( key )
                    
                self.geomManager.writeGeomParametersFile(os.path.join(GL_EXCHANGE, "Geom", "GEOM_PARAM_1.geo"), tmpDic)
                self.geomManager.updateProject(None)
                                
            #####################################################
            # Handling of the simulation settings
            #####################################################
            elif ( currentShamanable.getId() == self.SIM_SETTINGS_PANEL):
                
                self.simSettingPanel.getGui().updateModel()
                sharedGlobals["scenarioParameter11"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().INITIAL_SC_POTENTIAL)
                sharedGlobals["scenarioParameter2"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().INITIAL_DDP )
                sharedGlobals["scenarioParameter3"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().FINAL_DDP)
                sharedGlobals["scenarioParameter1"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().POTENTIAL_STEPS_NUMBER)
                sharedGlobals["scenarioParameter8"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().FIRST_STEP_DURATION)
                sharedGlobals["scenarioParameter9"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().NEXT_STEP_DURATION)
                sharedGlobals["scenarioParameter7"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().TIP_LENGTH)
                sharedGlobals["scenarioParameter5"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().INITIAL_BETA)
                sharedGlobals["scenarioParameter6"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().FINAL_BETA)
                sharedGlobals["scenarioParameter4"][4]  = self.simSettingModel.get(self.simSettingPanel.getGui().BETA_STEPS_NUMBER)
                sharedGlobals["scenarioParameter10"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().END_SCENARIO_FLAG)
                sharedGlobals["sourceTrajFlag1"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().ELEC_TRAJ_FLAG)
                sharedGlobals["electronSecondaryEmissionTrajFlag"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().SECOND_ELEC_TRAJ_FLAG)
                sharedGlobals["photoElectronTrajFlag"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().PHOTO_ELEC_TRAJ_FLAG)
                sharedGlobals["particleTrajectoriesNb"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().NUMBER_PARTICLE_TRAJECTORIES)
                sharedGlobals["particleTrajectoriesPeriod"][4] = self.simSettingModel.get(self.simSettingPanel.getGui().MONITORING_FREQUENCY)                
                
            #####################################################
            # Handling of the materials settings
            #####################################################
            elif ( currentShamanable.getId() == self.MATERIAL_PANEL):
                
                # re-atribution of materials to the groups
                for key in sharedGroups["metaGrpDic"].keys():
                    #print "scanning groups for meta-group ", key
                    for grpId in sharedGroups["metaGrpDic"][key]:
                        selectedMaterialId = string.atoi(self.materialPanelModel.get( key+"."+self.materialPanel.getGui().SELECTED_MATERIAL).split(":")[0])
                        sharedGroups["GeoGroupList"].GetElmById(grpId).Material = sharedProp["defaultMaterialList"].GetElmById(selectedMaterialId)
                    
            #####################################################
            # Handling of the space environment setting
            #####################################################
            elif ( currentShamanable.getId() == self.SPACE_ENV_PANEL):
                self.logger.info("Space environment settings")
                
                # update of the SPIS-UI model (i.e sharedGlobals)
                sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_TEMP_1 ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().ELEC_TEMP_1 )
                sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_DENS_1 ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().ELEC_DENS_1 )
                sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_TEMP_2 ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().ELEC_TEMP_2 )
                sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_DENS_2 ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().ELEC_DENS_2 )
                sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_SECOND_EMIS_FLAG ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().ELEC_SECOND_EMIS_FLAG )
                sharedGlobals[ self.spaceEnvPanel.getGui().SOLAR_FLUX ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().SOLAR_FLUX )
                sharedGlobals[ self.spaceEnvPanel.getGui().SUN_X ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().SUN_X )
                sharedGlobals[ self.spaceEnvPanel.getGui().SUN_Y ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().SUN_Y )
                sharedGlobals[ self.spaceEnvPanel.getGui().SUN_Z ][4] = self.spaceEnvModel.get( self.spaceEnvPanel.getGui().SUN_Z )
            else:
                self.logger.debug("Nothing to do")
        elif(eventType == ShamanEventType.BACK_REQUESTED):
            print "BACK_REQUESTED"
            
        elif(eventType == ShamanEventType.NEXT_DONE):
            
            #####################################################
            # Action for the simulation running phase
            #####################################################  
            if ( currentShamanable.getId() == self.SIM_RUN_DASHBOARD_PANEL):
                self.logger.info("Simulation run")
                ctrThread = SimulationThreadedControler()
                ctrThread.byPassSimulation = self.simSettingModel.get(self.simSettingPanel.getGui().BY_PASS_SIMULATION_FLAG)
                ctrThread.setCurrentShamanable(currentShamanable)
                ctrThread.start()     
                
            #####################################################
            # Handling of the geometry settings
            #####################################################
            elif ( currentShamanable.getId() == self.GEOMETRY_PANEL):              
                geomFileList, paramFileList = self.geomManager.readParametrisedGeometricalModel( os.path.join(GL_EXCHANGE, "Geom"))                
                indexTmp = 0
                tmpArray = self.geomPanel.getGui().getGeomModelArray( len(geomFileList.keys()))
                for elm in geomFileList.keys():
                    tmpArray[indexTmp] = elm
                    indexTmp = indexTmp + 1
                self.geomPanelModel.put(self.geomPanel.getGui().GEOM_FILE_LIST, tmpArray)
                
                for key in paramFileList.keys():
                    paramFile = paramFileList[key]
                    # more robust approach
                    keyList = []
                    keyList.append(self.geomPanel.getGui().L_BOX_X)
                    keyList.append(self.geomPanel.getGui().L_BOX_Y)
                    keyList.append(self.geomPanel.getGui().L_BOX_Z)
                    keyList.append(self.geomPanel.getGui().L_DIELEC_X)
                    keyList.append(self.geomPanel.getGui().L_DIELEC_Z)
                    keyList.append(self.geomPanel.getGui().ALPHA)
                    for key in keyList: 
                        try:
                            #print key , paramFile[key]
                            self.geomPanelModel.put( key , paramFile[key])
                        except:
                            print"parameter "+key+" not found"
                self.geomPanel.setModel(self.geomPanelModel)
                
            #####################################################
            # setting of the simulation run
            #####################################################
            elif (currentShamanable.getId() == self.SIM_SETTINGS_PANEL ):
                
                self.simSettingModel.put(self.simSettingPanel.getGui().INITIAL_SC_POTENTIAL, sharedGlobals["scenarioParameter11"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().INITIAL_DDP, sharedGlobals["scenarioParameter2"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().FINAL_DDP, sharedGlobals["scenarioParameter3"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().POTENTIAL_STEPS_NUMBER, sharedGlobals["scenarioParameter1"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().FIRST_STEP_DURATION, sharedGlobals["scenarioParameter8"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().NEXT_STEP_DURATION, sharedGlobals["scenarioParameter9"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().TIP_LENGTH, sharedGlobals["scenarioParameter7"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().INITIAL_BETA, sharedGlobals["scenarioParameter5"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().FINAL_BETA, sharedGlobals["scenarioParameter6"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().BETA_STEPS_NUMBER, sharedGlobals["scenarioParameter4"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().END_SCENARIO_FLAG, sharedGlobals["scenarioParameter10"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().ELEC_TRAJ_FLAG, sharedGlobals["sourceTrajFlag1"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().SECOND_ELEC_TRAJ_FLAG, sharedGlobals["electronSecondaryEmissionTrajFlag"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().PHOTO_ELEC_TRAJ_FLAG, sharedGlobals["photoElectronTrajFlag"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().NUMBER_PARTICLE_TRAJECTORIES, sharedGlobals["particleTrajectoriesNb"][4])
                self.simSettingModel.put(self.simSettingPanel.getGui().MONITORING_FREQUENCY, sharedGlobals["particleTrajectoriesPeriod"][4])       
                self.simSettingModel.put(self.simSettingPanel.getGui().BY_PASS_SIMULATION_FLAG, 0)
                self.simSettingPanel.getGui().setModel(self.simSettingModel)
            
            #####################################################
            # setting of the material properties panel
            #####################################################
            elif (currentShamanable.getId() == self.MATERIAL_PANEL ):
                
                self.logger.info("Material panel start setting")
                if (self.isPanelSet == 0): # this a trick to avoid to add groups 2 times if we come back with the wizard
                    # first we set the handler to the exchange model
                    self.materialPanel.setModel(self.materialPanelModel)
                    
                    if ( sharedGroups.has_key("metaGrpDic") and len(sharedGroups["metaGrpDic"].values()) > 0):
                        # we scan all meta groups
                        for key in sharedGroups["metaGrpDic"].keys():
                            # we set the corresponding combo box
                            materialComboArray = self.materialPanel.getGui().getComboModelArray( sharedProp['defaultMaterialList'].NbMaterial)
                            indexTmp = 0
                            for mat in sharedProp['defaultMaterialList'].List:
                                materialComboArray[indexTmp] = str(mat.Id) + ": "+ mat.Name
                                indexTmp = indexTmp + 1
                            self.materialPanelModel.put( key+"."+self.materialPanel.getGui().MATERIALS_LIST, materialComboArray)
                    
                            # we generate a new tab
                            self.materialPanelModel.put(key, sharedGroups["metaGrpDic"][key])
                            self.materialPanel.getGui().addPropertySubPanel(key, "Please select a material type for meta-group "+key)
                    else: 
                        print "No meta-group found, we do it by groups..."
                        for group in sharedGroups["GeoGroupList"].List:
                            # we set the corresponding combo box
                            materialComboArray = self.materialPanel.getGui().getComboModelArray( sharedProp['defaultMaterialList'].NbMaterial)
                            indexTmp = 0
                            for mat in sharedProp['defaultMaterialList'].List:
                                materialComboArray[indexTmp] = str(mat.Id) + ": "+ mat.Name
                                indexTmp = indexTmp + 1
                            self.materialPanelModel.put( "group."+str(group.Id)+"."+self.materialPanel.getGui().MATERIALS_LIST, materialComboArray)
                    
                            # we generate a new tab
                            self.materialPanelModel.put("group."+str(group.Id), group)
                            self.materialPanel.getGui().addPropertySubPanel("group."+str(group.Id), "Please select a material type for group "+str(group.Id))

                    for mat in sharedProp['defaultMaterialList'].List:
                        detailedDescription =  mat.Description+"\n" + str(mat.PrintMaterial)
                        self.materialPanelModel.put( str(mat.Id) + ": "+ mat.Name, detailedDescription)
                
                    # the update view should be done in last
                    self.materialPanel.getGui().updateView() 
                    self.isPanelSet = 1
                self.logger.info("Material panel set")
                
            #####################################################
            # 
            #####################################################
            elif (currentShamanable.getId() == self.SPACE_ENV_PANEL ):
                
                # NB: the view is dynamically set in order to start from the data provided by the project/template
                # this one being loaded before ( see panel project).
                self.logger.debug("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                #self.spaceEnvModel.put( sharedGlobals[])            
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().ELEC_TEMP_1, sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_TEMP_1 ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().ELEC_TEMP_1 + str(sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_TEMP_1 ][4]))
                
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().ELEC_DENS_1, sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_DENS_1 ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().ELEC_DENS_1 + str(sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_DENS_1 ][4]))
                
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().ELEC_TEMP_2, sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_TEMP_2 ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().ELEC_TEMP_2 + str(sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_TEMP_2 ][4]))
                
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().ELEC_DENS_2, sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_DENS_2 ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().ELEC_DENS_2 +str(sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_DENS_2 ][4]))
                
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().ELEC_SECOND_EMIS_FLAG, sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_SECOND_EMIS_FLAG ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().ELEC_SECOND_EMIS_FLAG  +str(sharedGlobals[ self.spaceEnvPanel.getGui().ELEC_SECOND_EMIS_FLAG ][4]))
                
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().SOLAR_FLUX, sharedGlobals[ self.spaceEnvPanel.getGui().SOLAR_FLUX ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().SOLAR_FLUX +str( sharedGlobals[ self.spaceEnvPanel.getGui().SOLAR_FLUX ][4]))
                
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().SUN_X, sharedGlobals[ self.spaceEnvPanel.getGui().SUN_X ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().SUN_X +str( sharedGlobals[ self.spaceEnvPanel.getGui().SUN_X ][4]))
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().SUN_Y, sharedGlobals[ self.spaceEnvPanel.getGui().SUN_Y ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().SUN_Y +str( sharedGlobals[ self.spaceEnvPanel.getGui().SUN_Y ][4]))
                self.spaceEnvModel.put( self.spaceEnvPanel.getGui().SUN_Z, sharedGlobals[ self.spaceEnvPanel.getGui().SUN_Z ][4])
                self.logger.debug( self.spaceEnvPanel.getGui().SUN_Z +str( sharedGlobals[ self.spaceEnvPanel.getGui().SUN_Z ][4]))                
                self.spaceEnvPanel.setModel( self.spaceEnvModel )
        
            #####################################################
            # Post processing panel
            #####################################################
            elif (currentShamanable.getId() == self.POST_PRO_PANEL ):
                
                # first index
                leftSideDataField = sharedData["AllDataField"].Dic["Barrier potential value"]
                MFIndex = sharedData['AllMeshField'].IdList.index(leftSideDataField.MeshFieldId)
                leftSideMeshField = sharedData['AllMeshField'].List[MFIndex]
                tmpPlot = self.postProPanel.getGui().addPlotPanel("ESD results", leftSideDataField.Name, leftSideMeshField.MeshElementList, leftSideDataField.ValueList, 0)
                
                # adding of the right side value
                rightSideDataField = sharedData["AllDataField"].Dic["Emitted current [A] versus time [s]: all interactions, all nodes, "]
                MFIndex = sharedData['AllMeshField'].IdList.index(rightSideDataField.MeshFieldId)
                rightSideMeshField = sharedData['AllMeshField'].List[MFIndex]
                tmpPlot.addRightSidePlot(rightSideDataField.Name, rightSideMeshField.MeshElementList, rightSideDataField.ValueList, 1)          

                # second index
                leftSideDataField = sharedData["AllDataField"].Dic["Collected current [A] versus time [s]: all populations, all nodes, "]
                MFIndex = sharedData['AllMeshField'].IdList.index(leftSideDataField.MeshFieldId)
                leftSideMeshField = sharedData['AllMeshField'].List[MFIndex]
                tmpPlot = self.postProPanel.getGui().addPlotPanel("Collected current", leftSideDataField.Name, leftSideMeshField.MeshElementList, leftSideDataField.ValueList, 1)      
                
                # Adding the third panel with the report
                try: 
                    print os.path.join( GL_EXCHANGE, "ESDRiskScenarioReport.txt")
                    reportFile = open( os.path.join( GL_EXCHANGE, "ESDRiskScenarioReport.txt"))
                    report = string.join(reportFile.readlines())
                except:
                    report = "No report found..."
                self.postProPanel.getGui().addReportPanel(report)
        else:
            self.logger.debug("not supported")
        
        
        #SHAMANABLE_CHANGED,
        #NEXT_REQUESTED,
        #NEXT_DONE,
        #CANCEL,
        #BACK_REQUESTED,
        #BACK_DONE;
                  
        
class PostprocessingActionListener(ActionListener):
    
    def __init__(self):
        self.actionToCmdTranslator = {}
        
    def addActionCmdCouple(self, actionName, cmdName):
        self.actionToCmdTranslator[actionName] = cmdName
        
    
    def actionPerformed(self, ae):
        actionName = ae.getActionCommand()
        sharedTasks["manager"].run_tasks( self.actionToCmdTranslator[actionName] )
                
         
class SimulationThreadedControler(Thread):
    """
    Performs the action corresponding to the simulation run control and monitoring. This class
    is threaded to do not freeze the whole application. The Next button is validated at the end 
    of the action only (i.e when the simulation is done). 
    """
    
    def __init__(self):
        Thread.__init__(self)
        self.currentShamanable = None
        self.logger = LoggerFactory.getLogger("Wizard Thread")
        self.loggingUtilities = LoggingUtilities(self.logger)
        self.byPassSimulation = 0
        
    def setCurrentShamanable(self, currentShamanable):
        self.currentShamanable = currentShamanable
                 
    def run(self):
        """
        Perform the simulation in a separated thread
        """        
        self.logger.info("Performing pre-processing")
        self.currentShamanable.getGui().getPreprocessingProgressBar().setIndeterminate(1)
        sharedTasks["manager"].set_done_task("ParamsEditor")
        if self.byPassSimulation !=1:
            sharedTasks["manager"].run_tasks("SpisNumInterface")
        self.logger.info("Pre-processing done")
        self.currentShamanable.getGui().getPreprocessingProgressBar().setIndeterminate(0)
        self.currentShamanable.getGui().getPreprocessingProgressBar().setValue(100)
        self.currentShamanable.getGui().getPreprocessingProgressBar().setStringPainted(1)
                    
        self.logger.info("Running the simulation (i.e running JyTop4)")
        self.currentShamanable.getGui().getSimulationRunProgressBar().setIndeterminate(1)
        
        #sharedTasks["manager"].run_tasks("JyTop")
        
        if self.byPassSimulation !=1:
            # I know this is crap, but this is to by pass the threaded approach of the SPIS-NUM caller
            for task in sharedTasks["tasks"]:
                if task[1] == "JyTop":
                    #print task 
                    break
            task[0].initCaller()
            task[0].action.runAction()
        
        self.currentShamanable.getGui().getSimulationRunProgressBar().setIndeterminate(0)
        #self.currentShamanable.getGui().getSimulationRunProgressBar().setValue(100)
        self.currentShamanable.getGui().getSimulationRunProgressBar().setStringPainted(1);

        # just to allow the NEXT button of the current panel. 
        self.currentShamanable.setOutputStatus(1)
        self.currentShamanable.fireShamanableChangedEvent( );
        
        

