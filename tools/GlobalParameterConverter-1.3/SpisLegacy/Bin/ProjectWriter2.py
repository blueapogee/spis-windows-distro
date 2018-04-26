"""
Saving module of SPIS-UI project into the format 2.0 (default), updated for version 4.3 of SPIS-UI.

**File name:**    ProjectWriter2.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      4.3.1

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 4.3.0   | Julien Forest                        | Modif                      |
|         | j.forest@artenum.com                 |                            |
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

import java

import os, sys, string, shutil

from Bin.Tasks.shared           import *
from Bin.Tasks.TaskBuiltins     import *
from Bin.Tasks.FileChooserSwing import *
import shutil

#from Bin.Tasks.shared import sharedData
import Modules.Field
import Modules.Field.DataField
import Modules.Field.MeshField

from Modules.Field.DataField import DataField
from Modules.Field.MeshField import MeshField
from Modules.Properties.Material import Material

from Modules.InOut.ObjectPyWriter import ObjectPyWriter
from Modules.InOut.DataFieldPyWriter import DataFieldPyWriter
from Modules.InOut.NascapMaterialsCatalogWriter import NascapMaterialsCatalogWriter

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, GL_VTK_EXCHANGE, GL_EXCHANGE, GL_KERNEL_EXCHANGE, GL_IMAGES_EXCHANGE, GL_BLOCK_SIZE, GL_MESH_STUDY, GL_SPIS_VERSION

from Bin.Tasks.Task           import Task

from Modules.InOut import PlasmaPyWriter
from Modules.InOut.PlasmaPyWriter import PlasmaPyWriter

from Modules.InOut import ElecNodePyWriter
from Modules.InOut.ElecNodePyWriter import ElecNodePyWriter

import Modules.InOut.MaterialPyWriter
from Modules.InOut.MaterialPyWriter import MaterialPyWriter

import Modules.InOut.GeoGroupPyWriter
from Modules.InOut.GeoGroupPyWriter import GeoGroupPyWriter

import Modules.InOut.GeomWorkSpaceDescriptor
from Modules.InOut.GeomWorkSpaceDescriptor import GeomWorkSpaceDescriptor

#FIX ME
#import Modules.InOut.GlobalParamWriter
#from Modules.InOut.GlobalParamWriter import GlobalParamWriter

from Bin.ProjectWriter import ProjectWriter

import com.artenum.free.mesh.io.exporter.GmshExporter

from Modules.Utils.LoggingUtilities     import LoggingUtilities
from org.slf4j                import LoggerFactory
from org.slf4j.profiler       import Profiler
#loadingLogger = LoggerFactory.getLogger("CoreLogger")


class ProjectWriter2(ProjectWriter):
    """Project saving class of SPIS-UI project into 2.0 format (default). 
    Please see the corresponding Technical Note for further information regarding the
    file format."""
    desc = "Saving of the current project"
    
    def setOuputDirectory(self, dirName=""):
        '''
        Defines the path and name of the output directory.
        '''
        self.dirName = dirName
    
    def createNewProject(self):
        '''
        create the directories structure of the project. This method must 
        be called at least one time before the write method. This method 
        detects if each directory is already built or not. If not, the 
        directory is built.
        '''
        
        if not os.path.isdir(self.dirName):
            os.makedirs(self.dirName)
        
        self.fileName = self.dirName+os.sep+"__init__.py"
        fileOut = open(self.fileName, 'w')
        fileOut.write("")
        fileOut.close()
        
        if not os.path.isdir(self.dirName+os.sep+"vtk"):
            os.makedirs(self.dirName+os.sep+"vtk")
        if not os.path.isdir(self.dirName+os.sep+"DataFields"):
            os.makedirs(self.dirName+os.sep+"DataFields")
        #if not os.path.isdir(self.dirName+os.sep+"DataFields"+os.sep+"MeshFields"):
        #    os.makedirs(self.dirName+os.sep+"DataFields"+os.sep+"MeshFields")
        
        if not os.path.isdir(self.dirName+os.sep+"Properties"):
            os.makedirs(self.dirName+os.sep+"Properties")
        if not os.path.isdir(self.dirName+os.sep+"Properties"+os.sep+"Materials"):
            os.makedirs(self.dirName+os.sep+"Properties"+os.sep+"Materials")
        if not os.path.isdir(self.dirName+os.sep+"Geom"):
            os.makedirs(self.dirName+os.sep+"Geom")
        if not os.path.isdir(self.dirName+os.sep+"Properties"+os.sep+"ElecNodes"):
            os.makedirs(self.dirName+os.sep+"Properties"+os.sep+"ElecNodes")
        if not os.path.isdir(self.dirName+os.sep+"Properties"+os.sep+"Plasmas"):
            os.makedirs(self.dirName+os.sep+"Properties"+os.sep+"Plasmas")
        if not os.path.isdir(self.dirName+os.sep+"NumKernel"):
            os.makedirs(self.dirName+os.sep+"NumKernel")
        if not os.path.isdir(self.dirName+os.sep+"NumKernel"+os.sep+"Input"):
            os.makedirs(self.dirName+os.sep+"NumKernel"+os.sep+"Input")
        if not os.path.isdir(self.dirName+os.sep+"NumKernel"+os.sep+"Output"):
            os.makedirs(self.dirName+os.sep+"NumKernel"+os.sep+"Output")
        if not os.path.isdir(self.dirName+os.sep+"Groups"):
            os.makedirs(self.dirName+os.sep+"Groups")
        if not os.path.isdir(self.dirName+os.sep+"Reporting"):
            os.makedirs(self.dirName+os.sep+"Reporting")
        if not os.path.isdir(self.dirName+os.sep+"Images"):
            os.makedirs(self.dirName+os.sep+"Images")
        if not os.path.isdir(self.dirName+os.sep+"MeshStudy"):
            os.makedirs(self.dirName+os.sep+"MeshStudy")
    
    
    def write(self):
        '''
        write (i.e save) the data currently loaded in the framework.
        '''
        
        self.logger = LoggerFactory.getLogger("Task")
        self.loggingUtilities = LoggingUtilities(self.logger)
        
        if self.logger.isDebugEnabled():
            timeProfiler = Profiler("ProjectWriter")
            timeProfiler.start("DataFields manager initialisation")

        if sharedProjectInfos != None:
            
            # for version tracking and projet/SPIS compliance
            sharedProjectInfos["projectVersion"] = GL_SPIS_VERSION
            
            project_file = os.path.join(self.dirName, "project")
            print type(project_file), " -", project_file
            save_obj(sharedProjectInfos, project_file)
            filename = os.path.join(self.dirName, "spis")
            
            '''
            descp = ProjectDescriptor()
            descp.setSharedFiles( sharedFiles)
            ow = ObjectPyWriter( descp)
            ow.setInstanceName("projectDescription")
            ow.readPatern()
            descriptionList = ow.saveToList()
            print "step 1"
            #try:
            fileOut = open(os.path.join(self.dirName, "projectDescription.py"), 'w')
            fileOut.write("# PROJECT DESCRIPTION")

            for line in descriptionList:
                fileOut.write(line+"\n")
                        
            fileOut.close()
            #except:
            #   print >> sys.stderr, "error: impossible to export the module"
            '''
        else:
            self.logger.error("ERROR 202 (TaskSaveProj): Strange! No project to save.")
        
        print "Saving of the materials and properties"
        if sharedProp != None:
            tmpName = filename + "-props"

            print "Export of material properties as Jython modules"
            ctrList = []
            try:
            #if(1):
                #for mat in sharedProp['defaultMaterialList'].List:
                for grp in sharedGroups['GeoGroupList'].List:
                    mat = grp.Material
                    if mat not in ctrList: 
                        if mat.Id > -1:
                            tmpName = "material"+`mat.Id`+".py"
                            self.logger.info("Saving: "+tmpName)
                            fileNameOut = os.path.join(self.dirName, "Properties", "Materials", tmpName)
                            wr = MaterialPyWriter(mat)
                            wr.setOutputFileName(fileNameOut)
                            wr.readStructure()
                            wr.write()
                            wr = None
                            ctrList.append(mat)
                             
                # saving of the related NASCAP properties if at least one group as a NASCAP property set                
                nascapSavingFlag = 0
                for grp in sharedGroups['GeoGroupList'].List:
                    # print grp.Material.Type
                    if (grp.Material.Type == Material.NASCAP_2K_MATERIAL or grp.Material.Type == Material.NASCAP_MATERIAL):
                        nascapSavingFlag= 1
                if (nascapSavingFlag == 1):
                    print "NASCAP properties detected and saved"
                    writer = NascapMaterialsCatalogWriter( sharedProp["defaultNascapMaterialList"].List)
                    writer.buildCatalog() 
                    nascapPropertiesDir = os.path.join(self.dirName, "Properties", "Materials", "NascapProperties")
                    print nascapPropertiesDir
                    if not os.path.isdir(nascapPropertiesDir):
                        os.makedirs(nascapPropertiesDir)
                    writer.write( nascapPropertiesDir+os.sep+"NascapMaterialCatalog.xml")
                    writer.writePythonInitFile(nascapPropertiesDir)
                    writer.writeCorrespondanceList(nascapPropertiesDir+os.sep+"materialCorrespondanceList.py")
                else: 
                    self.logger.info("No NASCAP properties detected")
            except:
                self.logger.warn("No material to save")
                self.loggingUtilities.printStackTrace()
            ctrlList = None    
            
            # saving of extra parameters for NASCAP based materials
            try:
                fileNameOut = os.path.join(self.dirName, "Properties", "Materials", "selectedNascapMaterialList.py")
                fileOut = open(fileNameOut, 'w')
                fileOut.write("# selected Nascap material list \n")
                
                # saving of the material model type
                fileOut.write("materialModel = '"+ sharedProp["materialModel"]+"'\n")
                
                #saving of the lsit itself
                prioListLine = "selectedNascapMaterialList = ["
                for mat in sharedProp["selectedNascapMaterialList"]:
                    prioListLine = prioListLine + str(mat)+","
                prioListLine = prioListLine[:-1] + "] \n"
                        
                fileOut.write(prioListLine)
                        
                fileOut.close()
            except:
                self.logger.warn("Impossible to write the selected Nascap material list")
                
            self.logger.info("Saving of electrical nodes properties as Jython modules")
            ctrList=[]
            try:
            #if(1):
                #for elec in sharedProp['defaultElecNodeList'].List:
                for grp in sharedGroups['GeoGroupList'].List:
                    elec = grp.ElecNode
                    if elec not in ctrList:
                        if elec.Id > -1:
                            tmpName = "elecNode"+str(elec.Id)+".py"
                            fileNameOut = os.path.join(self.dirName, "Properties", "ElecNodes", tmpName)
                            wr = ElecNodePyWriter(grp.ElecNode)
                            wr.setOutputFileName(fileNameOut)
                            wr.readStructure()
                            wr.write()
                            wr = None
                            ctrList.append(elec)
                            self.logger.info("  "+tmpName + " saved")
            except:
                self.logger.warn("No elecNode to save")
                self.loggingUtilities.printStackTrace()
            ctrList = None
            # need by some JVM (e.g SUN) under some OS, to avoid a "java.lang.OutOfMemoryError: PermGen space"
            java.lang.System.gc()
        
            self.logger.info("Saving of plasma properties as Jython modules")
            ctrList=[]
            try:
                #for plasma in sharedProp['defaultPlasmaList'].List:
                for grp in sharedGroups['GeoGroupList'].List:
                    plasma= grp.Plasma
                    if plasma not in ctrList: 
                        if plasma.Id > -1:
                            tmpName = "plasma"+`plasma.Id`+".py"
                            print "saving of "+ tmpName
                            fileNameOut = os.path.join(self.dirName, "Properties", "Plasmas", tmpName)
                            wr = PlasmaPyWriter(plasma)
                            wr.setOutputFileName(fileNameOut)
                            wr.readStructure()
                            wr.write()
                            wr = None
                            ctrList.append(plasma)
            except:
                self.logger.warn("No plasma to save")
            ctrList = None
            # need by some JVM (e.g SUN) under some OS, to avoid a "java.lang.OutOfMemoryError: PermGen space"
            java.lang.System.gc()
        else:
            self.logger.warn("WARNNING 203 (TaskSaveProj): No properties to save.")
             
        self.logger.info("Groups saving")
        if sharedGroups != None:
           #remove old files to clean up the project
           fileList = os.listdir(os.path.join(self.dirName, "Groups"))
           if ( fileList != []):
               for file in fileList:
                   tmpName = os.path.join(self.dirName, "Groups", file)
                   os.remove(tmpName)
                   
               # write the priority list of the Geom groups
               try:
                   fileNameOut = os.path.join(self.dirName, "Groups", "groupsPriorityList.py")
                   fileOut = open(fileNameOut, 'w')
                   fileOut.write("# groups list priority \n")
    
                   prioListLine = "prioList = ["
                   for grp in sharedGroups['GeoGroupList'].List:
                       prioListLine = prioListLine + `grp.Id`+","
                   prioListLine = prioListLine[:-1] + "] \n"
                        
                   fileOut.write(prioListLine)
                        
                   fileOut.close()
               except:
                   self.logger.warn("Impossible to write the groups priority list")
           
           #write the new groups   
           if sharedGroups['GeoGroupList'] != None:
               for grp in sharedGroups['GeoGroupList'].List:
                    tmpName = "geoGroup"+`grp.Id`+".py"
                    print "saving of "+ tmpName
                    fileNameOut = os.path.join(self.dirName, "Groups", tmpName)
                    try:
                    #if(1):
                        wr = GeoGroupPyWriter(grp)
                        wr.setOutputFileName(fileNameOut)
                        wr.readStructure()
                        wr.write()
                        wr = None
                    except:
                        self.logger.error("Impossible to save group"+grp.Name)
                        self.loggingUtilities.printStackTrace()
           # need by some JVM (e.g SUN) under some OS, to avoid a "java.lang.OutOfMemoryError: PermGen space"
           java.lang.System.gc()

        else:
            self.logger.warn("WARNNING 204 (TaskSaveProj): No groups to save.")

               
        ##############################################################
        # DataFields saving 
        ##############################################################             
        print "Saving of DataFields and MeshFields as Jython modules"
        #badCharList = " ()[].:,;!~<>#-="

        if sharedData['AllDataField'] == None:
            self.logger.warn("WARNNING 205 (TaskSaveProj): No dataField to save")
        else:
            dfDirPath = os.path.join(self.dirName, "DataFields")
            # moving of the previously saved DF to back
            if os.path.isdir(dfDirPath):
                if os.path.isdir(dfDirPath+".bak"):
                    shutil.rmtree(dfDirPath+".bak")
                shutil.move(dfDirPath, dfDirPath+".bak")
                self.logger.warn("Previous DataFields found. Moved to "+dfDirPath+".bak")
            
            # saving of the data fields
            for dataField in sharedData['AllDataField'].List:
                try : 
                    sys.stdout.write("Saving of "+ dataField.Name+"... ")
                    dfpw = DataFieldPyWriter(dataField)
                    dfpw.setOutputDirPath(dfDirPath)
                    dfpw.setBlockSize(GL_BLOCK_SIZE)
                    dfpw.write()                
                    # to help the garbage collector
                    dfpw = None 
                except:
                    self.logger.warn("WARNING 205 (TaskSaveProj): Impossible to save DataField "+dataField.Name)
            # need by some JVM (e.g SUN) under some OS, to avoid a "java.lang.OutOfMemoryError: PermGen space"
            java.lang.System.gc()


        self.logger.info("Solver related numerical elements saving")
        fileList = os.listdir(GL_KERNEL_EXCHANGE)
        if ( fileList != []):
            for file in fileList:
                fileNameIn = os.path.join(GL_KERNEL_EXCHANGE, file)
                fileNameOut = os.path.join(self.dirName, "NumKernel", "Input", file)
                shutil.copyfile(fileNameIn, fileNameOut)
        else:
            self.logger.warn("No numerical param for kernel to save")
        
        
        self.logger.info("Global parameters saving (python serialisation)")
        tmpName = filename + "-globals"    
        save_obj(sharedGlobals, tmpName)
        


        self.logger.info("Saving (copy) of the CAD files and workspace information")
        try:
            fileList = os.listdir(os.path.join(GL_EXCHANGE, "Geom"))
            if ( fileList != []):
                for file in fileList:
                    fileNameIn = os.path.join(GL_EXCHANGE, "Geom", file)
                    fileNameOut = os.path.join(self.dirName, "Geom", file)
                    shutil.copyfile(fileNameIn, fileNameOut)
                   
            self.logger.debug("Update of the CAD file shared reference")
            tmpPath = sharedFiles['TheCADFileIn']
            splittedTmpPath = tmpPath.split(os.sep)            
            sharedFiles['TheCADFileIn'] = os.path.join(self.dirName,  "Geom", splittedTmpPath[-1])
            self.logger.debug(sharedFiles['TheCADFileIn']) 
            
            self.logger.info("Generation of the workspace descriptor")
            descp = GeomWorkSpaceDescriptor()
            descp.setCanonicalPath(os.path.join(self.dirName, "Geom"))
            descp.updateListFiles()
            descp.setMainFile(splittedTmpPath[-1])
            self.logger.debug("Reference to main CAD file"+descp.nameMainFile)
            
            ow = ObjectPyWriter( descp)
            ow.setInstanceName("workSpaceDescription")
            ow.readPatern()
            descriptionList = ow.saveToList()
            
            try:
                fileOut = open(os.path.join(self.dirName, "Geom", "workSpaceDescription.py"), 'w')
                fileOut.write("# PROJECT DESCRIPTION")
                for line in descriptionList:
                    fileOut.write(line+"\n")
                fileOut.close()
            except:
                self.logger.warn("error: impossible to export the module")
        except: 
            self.logger.warn("No main CAD files to save. This is quite strange. Please check.")
            
        #FIX ME : a virer a termes
        self.logger.debug("Copy of the temporary CAD file")
        try:
            fileNameIn = os.path.join(GL_EXCHANGE, sharedFiles['TheCADFileOut'])
            fileNameOut = os.path.join(self.dirName, "cad_sav.geo")
            shutil.copyfile(fileNameIn, fileNameOut)
        except: 
            self.logger.warn("No main CAD file to save. This is quite strange. Please check.")
            

        
        
        self.logger.info("Saving of the mesh structure...")
        try:
            fileNameOut = os.path.join(self.dirName, "Tmp3D.msh")
            gmshExporter = com.artenum.free.mesh.io.exporter.GmshExporter(shared['Mesh'])
            gmshExporter.setOutputFile(fileNameOut)
            gmshExporter.exportAll()
        except: 
            self.logger.warn("No mesh to save.")

        self.logger.info("Saving of the files names and references")
        tmpName = filename + "-names"
        save_obj(sharedFiles, tmpName)
        
        self.logger.info("Copy of the VTK and posprocessing files")
        fileList = os.listdir(GL_VTK_EXCHANGE)
        if ( fileList != []):
            for file in fileList:
                fileNameIn = os.path.join(GL_VTK_EXCHANGE,file)
                fileNameOut = os.path.join(self.dirName, "vtk", file)
                shutil.copyfile(fileNameIn, fileNameOut)
        else:
            self.logger.warn("No VTK files to save")
              
              
        self.logger.info("Copy of the images files")
        try:
            fileList = os.listdir(GL_IMAGES_EXCHANGE)
        except:
            self.logger.warn("Deprecated exchange structure. No Images to copy.")
            fileList = []
        if ( fileList != []):
            for file in fileList:
                fileNameIn = os.path.join(GL_IMAGES_EXCHANGE,file)
                fileNameOut = os.path.join(self.dirName, "Images", file)
                shutil.copyfile(fileNameIn, fileNameOut)
        else:
            self.logger.warn("No images files to save")
               
        self.logger.info("Copy of the log files")      
        fileList = os.listdir(GL_EXCHANGE)
        for fileName in fileList:
            splittedName = fileName.split(".")
            if (len(splittedName) > 1):
                if (splittedName[1] == "log"):
                    fileNameIn = os.path.join(GL_EXCHANGE, fileName)
                    fileNameOut = os.path.join(self.dirName, fileName)
                    self.logger.debug(fileNameIn + " saved as " +fileNameOut)
                    shutil.copyfile(fileNameIn, fileNameOut)
        
        self.logger.info("Copy the mesh study (if any)... ")
        try:
            fileList = os.listdir(GL_MESH_STUDY)
        except:
            self.logger.warn("Deprecated exchange structure. No mesh study to copy.")
            fileList = []
        if ( fileList != []):
            for file in fileList:
                fileNameIn = os.path.join(GL_MESH_STUDY,file)
                fileNameOut = os.path.join(self.dirName, "MeshStudy", file)
                shutil.copyfile(fileNameIn, fileNameOut)
        else:
            self.logger.warn("No mesh study to save")                      
        
        # need by some JVM (e.g SUN) under some OS, to avoid a "java.lang.OutOfMemoryError: PermGen space"
        java.lang.System.gc()

        self.logger.info("Project saved")
        # to print the time cost
        if self.logger.isDebugEnabled():
            timeProfiler.stop().print()
