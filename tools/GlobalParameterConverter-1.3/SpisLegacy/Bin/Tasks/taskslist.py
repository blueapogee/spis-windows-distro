"""
**File name:**    taskslist.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
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

import sys

print "Please wait..."
sys.stdout.write("Tasks loading")
from Bin.Tasks.TaskCADImporter            import TaskCADImporter; sys.stdout.write(".")
from Bin.Tasks.TaskMesher                 import TaskMesher; sys.stdout.write(".")
from Bin.Tasks.TaskMaterial               import TaskMaterial; sys.stdout.write(".")
from Bin.Tasks.TaskGroupManager           import TaskGroupManager; sys.stdout.write(".")
from Bin.Tasks.TaskFieldManager           import TaskFieldManager; sys.stdout.write(".")
from Bin.Tasks.TaskSpisNumInterface       import TaskSpisNumInterface; sys.stdout.write(".")

from Bin.Tasks.TaskViewPipeline1          import TaskViewPipeline1; sys.stdout.write(".")

from Bin.Tasks.TaskViewPipeline2          import TaskViewPipeline2; sys.stdout.write(".")
from Bin.Tasks.TaskToolCaller             import TaskToolCaller; sys.stdout.write(".")
from Bin.Tasks.TaskEditIni                import TaskEditIni; sys.stdout.write(".")
from Bin.Tasks.TaskPrompt                 import TaskPrompt; sys.stdout.write(".")
from Bin.Tasks.TaskFileChooser            import TaskFileChooser; sys.stdout.write(".")
from Bin.Tasks.TaskJyTop                  import TaskJyTop; sys.stdout.write(".")
from Bin.Tasks.TaskMesher2D               import TaskMesher2D; sys.stdout.write(".")
from Bin.Tasks.TaskMesher3D               import TaskMesher3D; sys.stdout.write(".")
from Bin.Tasks.TaskBuildDataFieldChooser  import TaskBuildDataFieldChooser; sys.stdout.write(".")
from Bin.Tasks.TaskBuildPlot2D            import TaskBuildPlot2D; sys.stdout.write(".")
from Bin.Tasks.TaskEditNumSettings        import TaskEditNumSettings; sys.stdout.write(".")
from Bin.Tasks.TaskGroupEditor            import TaskGroupEditor; sys.stdout.write(".")
from Bin.Tasks.TaskReloadSolver           import TaskReloadSolver; sys.stdout.write(".")
from Bin.Tasks.TaskSaveProj               import TaskSaveProj; sys.stdout.write(".")
from Bin.Tasks.TaskSaveProjAs             import TaskSaveProjAs; sys.stdout.write(".")
from Bin.Tasks.TaskLoadProj               import TaskLoadProj; sys.stdout.write(".")


from Bin.Tasks.TaskMaterialEditor         import TaskMaterialEditor; sys.stdout.write(".")
from Bin.Tasks.TaskElecNodeEditor         import TaskElecNodeEditor; sys.stdout.write(".")
from Bin.Tasks.TaskPlasmaEditor           import TaskPlasmaEditor; sys.stdout.write(".")
from Bin.Tasks.TaskDataEditor             import TaskDataEditor; sys.stdout.write(".")
from Bin.Tasks.TaskReload                 import TaskReload; sys.stdout.write(".")
from Bin.Tasks.TaskInitGroup              import TaskInitGroup; sys.stdout.write(".")
try:
    from Bin.Tasks.TaskConvertGroup           import TaskConvertGroup; sys.stdout.write(".")
except:
    print "Error: impossible to load Bin.Tasks.TaskConvertGroup."
from Bin.Tasks.TaskSaveCAD                import TaskSaveCAD; sys.stdout.write(".")
from Bin.Tasks.TaskLoadCAD                import TaskLoadCAD; sys.stdout.write(".")
from Bin.Tasks.TaskSaveProperties         import TaskSaveProperties; sys.stdout.write(".")
from Bin.Tasks.TaskLoadProperties         import TaskLoadProperties; sys.stdout.write(".")
from Bin.Tasks.TaskNewProject             import TaskNewProject; sys.stdout.write(".")
from Bin.Tasks.TaskSolverInit             import TaskSolverInit; sys.stdout.write(".")
from Bin.Tasks.TaskSolverBuildSim         import TaskSolverBuildSim; sys.stdout.write(".")
from Bin.Tasks.TaskSolverRun              import TaskSolverRun; sys.stdout.write(".")
from Bin.Tasks.TaskSolverReadSim          import TaskSolverReadSim; sys.stdout.write(".")
from Bin.Tasks.TaskParaview               import TaskParaview; sys.stdout.write(".")
from Bin.Tasks.TaskParamsEditor           import TaskParamsEditor; sys.stdout.write(".")
from Bin.Tasks.TaskSaveGroups             import TaskSaveGroups; sys.stdout.write(".")
from Bin.Tasks.TaskLoadGroups             import TaskLoadGroups; sys.stdout.write(".")
from Bin.Tasks.TaskDocCaller              import TaskDocCaller; sys.stdout.write(".")
from Bin.Tasks.TaskCallCassandra          import TaskCallCassandra; sys.stdout.write(".")
from Bin.Tasks.TaskCallJyConsole          import TaskCallJyConsole; sys.stdout.write(".")
from Bin.Tasks.TaskCallMemoryMonitor      import TaskCallMemoryMonitor; sys.stdout.write(".")
from Bin.Tasks.TaskCallJSynoptic          import TaskCallJSynoptic; sys.stdout.write(".")
from Bin.Tasks.TaskMeshSplitter           import TaskMeshSplitter; sys.stdout.write(".")
from Bin.Tasks.TaskInitFields             import TaskInitFields; sys.stdout.write(".")
from Bin.Tasks.TaskExit                   import TaskExit; sys.stdout.write(".")
from Bin.Tasks.TaskExportToGmshMesh       import TaskExportToGmshMesh; sys.stdout.write(".")
from Bin.Tasks.TaskMeshImporter           import TaskMeshImporter; sys.stdout.write(".")
from Bin.Tasks.TaskDataBusCleaner         import TaskDataBusCleaner; sys.stdout.write(".")
from Bin.Tasks.TaskCallNumParamEditor     import TaskCallNumParamEditor; sys.stdout.write(".")

try:
    from Bin.Tasks.TaskEditCharScales         import TaskEditCharScales; sys.stdout.write(".")
except:
    print "Error: impossible to load Bin.Tasks.TaskEditCharScales"

from Bin.Tasks.TaskPicUpParamsEditor      import TaskPicUpParamsEditor; sys.stdout.write(".")
from Bin.Tasks.TaskExportToPicUp          import TaskExportToPicUp; sys.stdout.write(".")
from Bin.Tasks.TaskCallPicUp3D            import TaskCallPicUp3D; sys.stdout.write(".")
from Bin.Tasks.TaskCallPicUp3DReload      import TaskCallPicUp3DReload; sys.stdout.write(".")

from Bin.Tasks.TaskProjectControler       import TaskProjectControler; sys.stdout.write(".")
from Bin.Tasks.TaskProjectLoaderFormat2   import TaskProjectLoaderFormat2; sys.stdout.write(".")
from Bin.Tasks.TaskGeomManager            import TaskGeomManager; sys.stdout.write(".")
from Bin.Tasks.TaskExecuteCmdAsDemaon     import TaskExecuteCmdAsDemaon; sys.stdout.write(".")
from Bin.Tasks.TaskAbout                  import TaskAbout; sys.stdout.write(".")
#try: 
from Bin.Tasks.TaskExportAllDF            import TaskExportAllDF; sys.stdout.write(".")
#except: print "Error: impossible to load Bin.Tasks.TaskExportAllDF"
from Bin.Tasks.TaskPreferencesEditor       import TaskPreferencesEditor; sys.stdout.write(".")
from Bin.Tasks.TaskImportNascapMaterial    import TaskImportNascapMaterial; sys.stdout.write(".")
from Bin.Tasks.TaskMeshInspector           import TaskMeshInspector; sys.stdout.write(".")
from Bin.Tasks.TaskExportNascapMaterial    import TaskExportNascapMaterial; sys.stdout.write(".")
from Bin.Tasks.TaskLoadTrack               import TaskLoadTrack; sys.stdout.write(".")
from Bin.Tasks.TaskWizardManager           import TaskWizardManager; sys.stdout.write(".")
from Bin.Tasks.TaskExportAllDFToVtk        import TaskExportAllDFToVtk; sys.stdout.write(".")
print ""


class TasksList:
    '''
    Define the dependence tree of all Tasks defined in the SPIS-UI framework.
    If you whish add de new Tasks, you must:

    1) Add it import in this module, as follow:

       from Bin.Tasks.TaskMyTask                  import TaskMyTask; sys.stdout.write(".")

    2) Add it in the tasklist self.tasks, as follow:

        (TaskMesher("iMyTask", 0, "Other")                                  , "MyTask")

        The 0 flag means that this task must be run in forground mode.

        "Other" is the name of the Task on whish one your task is dependent on. 
 
        The last field "MyTask" is the string corresponding the celling message used 
        by the TaskManager to perform the task. Typically, this string is returned by the 
        main SPIs-UI GUI. 

    Please see the SPIS-UI Developer Guide for further informations. 
    '''
    
    def __init__(self):
        
        #print "Tasks list intantiation"
        self.isDeamon = 1
        self.tasks = []

        
    def initTasksList(self):
        '''
        initialises the dependence tree (tasklist).
        '''

        # dependency tree between tasks.
	
        print "Building of the dependence tree..."
        #print "isDeamon", self.isDeamon
        self.tasks = [(TaskFileChooser("FileChooser")                                        , "FileChooser"),
                    (TaskCADImporter("CADImporter", 0)                        , "CADImporter"),
                    (TaskMesher("Mesher", 0, "CADImporter")                                  , "Mesher"),
                    (TaskViewPipeline1("ViewPipeline1", 0, "ConvertGroup")                   , "ViewPipeline1"),
                    (TaskMaterial("Material")                                                , "Material"),
                    (TaskGroupManager("GroupManager", 0, "Material")                         , "GroupManager"),
                    (TaskFieldManager("FieldManager", 0, "ConvertGroup", \
                                                               "InitFields")                 , "FieldManager"),
                    (TaskSpisNumInterface("SpisNumInterface", 0, \
                                                               "FieldManager", \
                                                               "ParamsEditor")               , "SpisNumInterface"),
                    (TaskViewPipeline2("ViewPipeline2", self.isDeamon)                       , "ViewPipeline2"),
                    (TaskJyTop("JyTop", self.isDeamon)                                       , "JyTop"),
                    (TaskToolCaller("ToolCaller", self.isDeamon)                                , "ToolCaller"),
                    (TaskEditIni("EditIni", self.isDeamon)                                   , "EditIni"),
                    (TaskPrompt("Prompt", self.isDeamon)                                     , "Prompt"),
                    (TaskMesher2D("Mesher2D", 0, "CADImporter")                              , "Mesher2D"),
                    (TaskMesher3D("Mesher3D", 0, "CADImporter")                              , "Mesher3D"),
                    (TaskBuildDataFieldChooser("BuildDataFieldChooser", self.isDeamon)       , "BuildDataFieldChooser"), 
                    (TaskBuildPlot2D("BuildPlot2D",self.isDeamon)                            , "BuildPlot2D"),
                    (TaskGroupEditor("GroupEditor", 0)                                       , "GroupEditor"),
                    (TaskReloadSolver("ReloadSolver")                                        , "ReloadSolver"),
                    (TaskSaveProj("SaveProj", self.isDeamon)                                 , "SaveProj"),
                    (TaskSaveProjAs("SaveProjAs",self.isDeamon)                              , "SaveProjAs"),
                    (TaskLoadProj("LoadProj")                                                , "LoadProj"),
                    (TaskMaterialEditor("MaterialEditor", self.isDeamon)                     , "MaterialEditor"),
                    (TaskElecNodeEditor("ElecNodeEditor", self.isDeamon)                     , "ElecNodeEditor"),
                    (TaskPlasmaEditor("PlasmaEditor", self.isDeamon)                         , "PlasmaEditor"),
                    (TaskDataEditor("DataEditor", self.isDeamon)                             , "DataEditor"),
                    (TaskReload("Reload")                                                    , "Reload"),
                    (TaskInitGroup("InitGroup")                                              , "InitGroup"),
                    (TaskConvertGroup("ConvertGroup", 0, "Mesher3D")                         , "ConvertGroup"),
                    (TaskSaveCAD("SaveCAD", self.isDeamon)                                   , "SaveCAD"),
                    (TaskLoadCAD("LoadCAD")                                                  , "LoadCAD"),
                    (TaskSaveProperties("SaveProperties", self.isDeamon)                     , "SaveProperties"),
                    (TaskLoadProperties("LoadProperties")                                    , "LoadProperties"),
                    (TaskNewProject("NewProject")                                            , "NewProject"),
                    (TaskSolverInit("SolverInit", 0)                                         , "SolverInit"),
                    (TaskSolverBuildSim("SolverBuildSim")                                    , "SolverBuildSim"),
                    (TaskSolverRun("SolverRun", self.isDeamon)                               , "SolverRun"),
                    (TaskSolverReadSim("SolverReadSim")                                      , "SolverReadSim"),
                    (TaskParaview("Paraview", self.isDeamon)                                 , "Paraview"),
                    (TaskParamsEditor("ParamsEditor", 0)                                     , "ParamsEditor"),
                    (TaskSaveGroups("SaveGroups")                                            , "SaveGroups"),
                    (TaskLoadGroups("LoadGroups")                                            , "LoadGroups"),
                    (TaskDocCaller("DocCaller", self.isDeamon)                               , "DocCaller"),
                    (TaskCallCassandra("CallCassandra", self.isDeamon)                       , "CallCassandra"),
                    (TaskCallJyConsole("CallJyConsole", self.isDeamon)                       , "CallJyConsole"),
                    (TaskCallMemoryMonitor("CallMemoryMonitor", self.isDeamon)               , "CallMemoryMonitor"),
                    (TaskCallJSynoptic("CallJSynoptic", self.isDeamon)                       , "CallJSynoptic"),
                    (TaskMeshSplitter("MeshSplitter", 0, "InitFields")                       , "MeshSplitter"),
                    (TaskInitFields("InitFields",0, "ConvertGroup")                          , "InitFields"),
                    (TaskExit("Exit")                                                        , "Exit"),
                    (TaskExportToGmshMesh("ExportToGmshMesh", self.isDeamon)                 , "ExportToGmshMesh"),
                    (TaskMeshImporter("MeshImporter")                                        , "MeshImporter"),
                    (TaskCallNumParamEditor("CallNumParamEditor")                            , "CallNumParamEditor"),
                    (TaskDataBusCleaner("DataBusCleaner")                                    , "DataBusCleaner"),
                    (TaskEditCharScales("EditCharScales")                                    , "EditCharScales"),
                    (TaskPicUpParamsEditor("PicUpParamsEditor")                                      , "PicUpParamsEditor"),
                    (TaskExportToPicUp("ExportToPicUp",0,"EditCharScales","PicUpParamsEditor")       , "ExportToPicUp"),
                    (TaskCallPicUp3D("CallPicUp3D",0,"PicUpParamsEditor","ExportToPicUp")            , "CallPicUp3D"),
                    (TaskCallPicUp3DReload("CallPicUp3DReload")                              , "CallPicUp3DReload"),
                    (TaskProjectControler("ProjectControler")                                , "ProjectControler"),
                    (TaskProjectLoaderFormat2("ProjectLoaderFormat2",self.isDeamon)          , "ProjectLoaderFormat2"),
                    (TaskGeomManager("GeomManager", self.isDeamon)                           , "GeomManager"), 
                    (TaskExecuteCmdAsDemaon("ExecuteCmdAsDemaon", self.isDeamon)             , "ExecuteCmdAsDemaon"),
                    (TaskAbout("About",  self.isDeamon)                                      , "About"),
                    (TaskExportAllDF("ExportAllDF", self.isDeamon)                           , "ExportAllDF"),
                    (TaskPreferencesEditor("PreferencesEditor", self.isDeamon)               , "PreferencesEditor"),
                    (TaskImportNascapMaterial("ImportNascapMaterial", self.isDeamon)         , "ImportNascapMaterial"),
                    (TaskMeshInspector("MeshInspector",  self.isDeamon)                      , "MeshInspector"),
                    (TaskExportNascapMaterial("ExportNascapMaterial", self.isDeamon)         , "ExportNascapMaterial"),
                    (TaskLoadTrack("LoadTrack", self.isDeamon)                               , "LoadTrack"),
                    (TaskWizardManager("WizardManager", self.isDeamon)                       , "WizardManager"),
                    (TaskExportAllDFToVtk("ExportAllDFToVtk", self.isDeamon)                 , "ExportAllDFToVtk")
                    ]

    def setAllAlive(self):
        '''
        Forces all tasks to be in forground mode. Usefull in script or batch mode.
        '''
        self.isDeamon = 0
    
    
