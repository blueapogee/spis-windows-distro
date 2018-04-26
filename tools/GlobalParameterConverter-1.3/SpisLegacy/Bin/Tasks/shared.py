"""
Central and shared Data bus of SPIS-UI.

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

from org.slf4j            import Logger
from org.slf4j            import LoggerFactory

dataBusLogger = LoggerFactory.getLogger("dataBusLogger")

# Share data between tasks and console

shared = {
    # Cannot be unpickled
    'MeshElmtList': None,
    'OldNodeNumList': None,
    # Cannot be unpickled
    'SkeletonElmtList': None,
    'OldSkeletonElmtNumList': None,
    'cadimport': None,
    'MeshGroupList': None, 
    'Mesh': None
    }
'''
Mesh structure dictionary. This dictionary contains all data related to the mesh 
description. 
'''


sharedProjectInfos = {
    "Name": "default",
    "projectVersion": None,
    "description": None
    }
'''
General project informations dictionary.
'''


sharedFiles = {
    'TheProjectFileIn': 'proj.spis',
    'TheProjectFileOut': 'proj.spis',
    'TheCADFileIn': None,
    'TheCADFileOut': None,
    'TheMeshFileIn': None,
    'TheMeshFileOut': None,
    'ThePrintFileOut': None,
    'project_directory': None,
    'projectSavingFlag' : None,
    'projectSavingFormat': None,
    'projectLoadingFlag': None,
    'projectNumElmFlag' : None
    }
'''
References of all IN/OUT, sharing and temporary files.
'''


sharedProp = {
    'defaultMaterialList': None,
    'defaultPlasmaList': None,
    'defaultNascapMaterialList': None,
    'materialModel': None,
    'selectedNascapMaterialList': None       #'uiToNumNascapMaterialCorresponcanceDic': None
    }
'''
Material and numerical properties dictionary.
'''

sharedGroups = {
    'GeoGroupList': None
    }
'''
CAD groups list.
'''

sharedFlags = {
    'importFlag': 0,
    'guiMode': 1
    }

# Used to reload tasks in console mode
sharedTasks = {
    "tasks": None,
    "manager": None,
    "event_queue": None,
    "event_cond": None,
    "context": None,
    "caller":None
    }

sharedFrames = {
    'VTK': None,
    'esdPanelsList': None
    }

sharedVTK = {
    'VTKMeshElmtList': None,
    'VTKOldNodeNumList': None,
    'VTKSkeletonElmtList': None,
    'VTKOldSkeletonElmtNumList': None,
    'VTKMeshGroupList': None,
    'VTKcadimport': None,
    'VTKListActor': [],
    'VTKListScalarBarActor': [],
    'VTKMeshFieldUgrid':None,
    'VTKMeshFieldUgrid_Node':None,
    'VTKCutterActor':None,
    'VTKCutterVisibleActor':None,
    'RenderWindows':None,   		#deprecated
    'VTKColorBar':None,
    'VTKMin':None,
    'VTKMax':None,
    'VTKContour':None,
    'VTKIsoPlane':None,
    'VTKPlaneContour':None,
    'VTKAxes':None,
    'VTKMeshFieldUGridActor':None,
    'VTKDataName': None,
    'VTKDataUnit': None,
    'VTKMeshGridActor':None,
    'VTKCuttingPlane':None,
    'VTKLabel':None,
    'VTKMeshGridTestData':None,
    'VTKIsoSurface':None,
    'VTKObjectType':[],
    'VTKJavaRender':None,		 #this is the vtk panel for java based viewin (includes vtkRenderWindow, vtkRenderer, vtkCamera, vtkLight...)
    'VTKGridList':[],
    'VTKPlaneList':[],
    'VTKListMinMax':[],
    'VTKLookUpTable':None,
    'VTKDataSet':[]
    }

sharedData = {
    'AllDataField': None,
    'AllMeshField': None
    }
'''
All shared DataFields and related MeshFields.
'''

sharedNum = {
    'SNVolList':  None,
    'SNSurfList': None,
    'SNBndList': None,
    'SNIdList': None,
    'uiToNumNascapMaterialCorresponcanceDic': None
    #'materialProp': None,
    #'materialModel': None
    }
"""
Specifique data relative to the Spis-NUM integration, interface
and control. May depend on the version of SPIS-NUM. 
"""

sharedControls = {
    'dimMesh': None,
    'projetLoadingFlag': 0,
    'groupLoadingFlag': 0
    }
"""
Framework extra-control flags and meta-data. 
"""

#CAD and groups stuff
cadimport = None

#solvers stuff
sharedSolver = {
    'solver' : None
    }
"""
Registered solvers. 
"""

sharedGlobals = {
    }
'''
Shared global parameters.
'''

sharedGlobalsPicUp = {
    }
'''
Shared global parameters for PicUp
'''

sharedCharScales = {
    }

sharedSplitElm = {
    }


def addElementToSharedList(rootList=None, appendedList=None):
    """
    append a list of object to an existing one (e.g shared dictionaries). Check if the 
    list is pre-existing or not. If not, the list is created. 
    """    
    if rootList == None:
        dataBusLogger.info("No pre-existing shared list. List created.")
        rootList = appendedList
    else:
        dataBusLogger.info("Pre-existing shared list. List appended.")
        for elm in appendedList.List:
            rootList.Add(elm)
    return(rootList)
        