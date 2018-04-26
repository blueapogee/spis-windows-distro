"""
**File name:**    TaskSaveProj.py

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
import sys

from Bin.Tasks.shared           import *
from Bin.Tasks.TaskBuiltins     import *
from Bin.Tasks.FileChooserSwing import *
import shutil

from Bin.Tasks.shared import sharedData
import Modules.Field
import Modules.Field.DataField
import Modules.Field.MeshField

from Modules.Field.DataFieldWriter import DataFieldWriter
from Modules.Field.DataFieldReader import DataFieldReader
from Modules.Field.DataField import DataField
from Modules.Field.MeshField import MeshField

sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, GL_VTK_EXCHANGE, GL_EXCHANGE
sys.path.append(GL_SPISUIROOT_PATH)
from Bin.Tasks.Task           import Task

from Modules.InOut.ReadWriteManager import ReadWriteManager
from Modules.InOut import PlasmaPyWriter
from Modules.InOut.PlasmaPyWriter import PlasmaPyWriter

from Modules.InOut import ElecNodePyWriter
from Modules.InOut.ElecNodePyWriter import ElecNodePyWriter

import Modules.InOut.MaterialPyWriter
from Modules.InOut.MaterialPyWriter import MaterialPyWriter


#FIX ME
#import Modules.InOut.GlobalParamWriter
#from Modules.InOut.GlobalParamWriter import GlobalParamWriter


class TaskSaveProjSeb(Task):
    """Under testing."""
    desc = "Saving of the current project"
    def run_task(self):
        print "Save current project"
        ioManager = ReadWriteManager()
        
        #if the project path is not defined, we open a file browser
        #otherwise, we save in the default directory
        print "Project path ", sharedFiles["project_directory"]
        if (sharedFiles["project_directory"] == "" or sharedFiles["project_directory"] == None or sharedFiles["project_directory"] == "None"):
             dir = str(choose_dir(sharedFiles["project_directory"])).strip()
        else:
             dir = sharedFiles["project_directory"]

        ################################################
        # Try to Save project info: sharedProjectInfos
        ## sharedTasks["event_queue"].append("SaveProjSeb"); sharedTasks["event_cond"].broadcast();  reload_task("TaskSaveProjSeb")
        ################################################

        if sharedProjectInfos != None:
            print 'Save project info'
            subdir = os.path.join(dir, "infos")
            ioManager.createDirectory(subdir)
            ioManager.saveObject(sharedProjectInfos,
                                 os.path.join(subdir, "project_infos.py"))
        else:
            print >> sys.stderr,"ERROR 202 (TaskSaveProj): Strange! No project to save."

        ################################################
        # Try to Save The Properties
        ################################################
        
        if sharedProp != None:
            print "Export of materials as Jython modules"
            try:
                ioManager.saveMaterialListToDir(os.path.join(dir, "Properties", "Materials"), sharedProp['defaultMaterialList'].List)
            except:
                print "No material to save"
                 
            print "Export of electical nodes as Jython modules"
            try:
                ioManager.saveElectricalNodeListToDir(os.path.join(dir, "Properties", "ElecNodes"), sharedProp['defaultElecNodeList'].List)
            except:
                 print "No elecNode to save"
        
            print "Export of plasmas as Jython modules"
            try:
                ioManager.saveElectricalNodeListToDir(os.path.join(dir, "Properties", "Plasmas"), sharedProp['defaultPlasmaList'].List)
            except:
                print "No plasma to save"
        else:
            print >> sys.stdwarn,"WARNNING 203 (TaskSaveProj): No properties to save."      

        ################################################
        # Try to save groups
        # TODO
        ################################################
        
        print "Saving of the groups"
        if sharedGroups != None:
            subdir = os.path.join(dir, "inputs", "groups")
            ioManager.createDirectory(subdir)
            #tmpName = filename + "-groups"
            #save_obj(sharedGroups, tmpName)
            pass
        else:
            print >> sys.stdwarn,"WARNNING 204 (TaskSaveProj): No groups to save."
            
            
        ################################################
        # Try to save datafield
        # TODO
        ################################################
        
        if sharedData['AllDataField'] != None:
            print "Saving of the DataFields and MeshFields"
            for dataTmp in sharedData['AllDataField'].List:
              print "saving of", dataTmp.Name
              tmpName = dataTmp.Name + ".fld"
              fileNameOut = os.path.join(dir, "DataFields", tmpName)
              indexMF = sharedData['AllMeshField'].IdList.index(dataTmp.MeshFieldId)
              w = DataFieldWriter(dataTmp, sharedData['AllMeshField'].List[indexMF], fileNameOut)
              w.write()
        else:
            print >> sys.stdwarn,"WARNNING 205 (TaskSaveProj): No DataFields to save"
        
        ################################################
        # Try to save global parameter
        ################################################
        
        print "Saving of global parameters"
        subdir = os.path.join(dir, "inputs", "sim_param")
        ioManager.createDirectory(subdir)
        ioManager.saveObject(sharedGlobals,
                             os.path.join(subdir, "project_parameters.py"))
        print "Export of global parameters as Jython modules"
            
        ################################################
        # Try to save CAD file
        ################################################
        
        print "copy of the CAD file"
        try:
            subdir = os.path.join(dir, "inputs", "geo")
            ioManager.createDirectory(subdir)
            fileNameIn = os.path.join(GL_EXCHANGE, sharedFiles['TheCADFileOut'])
            fileNameOut = os.path.join(subdir, "cad_sav.geo")
            print "copy", fileNameIn, " to", fileNameOut
            shutil.copyfile(fileNameIn, fileNameOut)
            print "Update of the CAD file shared reference"
            sharedFiles['TheCADFileIn'] = fileNameOut
        except: 
            print >> sys.stdwarn, "No CAD file to save. This is quite strange. Please check."

        ################################################
        # Try to save linked files
        ################################################
        
        print "Saving of the files names and references"
        subdir = os.path.join(dir, "inputs", "links")
        ioManager.createDirectory(subdir)
        ioManager.saveObject(sharedFiles,
                             os.path.join(subdir, "linked_files.py"))
        
       
        ################################################
        # Try to save VTK files
        ################################################
        
        print "Copy of the VTK files"
        fileList = os.listdir(GL_VTK_EXCHANGE)
        if ( fileList != []):
           for file in fileList:
               subdir = os.path.join(dir, "outputs", "vtk")
               ioManager.createDirectory(subdir)
               fileNameIn = GL_VTK_EXCHANGE+file
               fileNameOut = os.path.join(subdir, file)
               print fileNameIn
               print fileNameOut
               shutil.copyfile(fileNameIn, fileNameOut)
        else:
           print "No VTK files to save"
               
        ################################################
        # Try to save log files
        ################################################
               
        print "Copy of the log files"        
        fileList = os.listdir(GL_EXCHANGE)
        for fileName in fileList:
            splittedName = fileName.split(".")
            if (len(splittedName) > 1):
                if (splittedName[1] == "log"):
                    subdir = os.path.join(dir, "logs")
                    ioManager.createDirectory(subdir)
                    fileNameIn = os.path.join(GL_EXCHANGE, fileName)
                    fileNameOut = os.path.join(subdir, fileName)
                    print fileNameIn, " saved as ", fileNameOut
                    shutil.copyfile(fileNameIn, fileNameOut)
        print "Project saved"
