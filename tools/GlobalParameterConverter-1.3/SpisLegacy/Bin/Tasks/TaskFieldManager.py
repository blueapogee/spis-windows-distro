"""
**File name:**    TaskFieldManager.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest, Maxime Biais

:version:      4.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 4.0.0   | Julien Forest                        | Update improvment          |
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

import sys
import traceback

#from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
from org.slf4j.profiler       import Profiler
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Modules.Utils.LoggingUtilities import LoggingUtilities

from Bin.Tasks.Task           import Task

# import of shared data and objects 
# (see shared.y file for more informations)
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedProp
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedNum #FIX ME: not clean to use shareNum

import Bin.FieldManager
from Bin.FieldManager         import FieldManager

class TaskFieldManager(Task):
    """Map (deploy) the DataFields on mesh."""
    desc = "Task of management of FieldManager"
    
    def run_task(self):
        
        self.logger = LoggerFactory.getLogger("Task")
        # to simplify the various (Jython and Java stack printing)
        loggingUtilities = LoggingUtilities(self.logger)
        if self.logger.isDebugEnabled():
            timeProfiler = Profiler("TaskFieldManager")
            timeProfiler.start("DataFields manager initialisation")
        
        # for dynamic reloading of sub-modules
        reload(Bin.FieldManager)
        from Bin.FieldManager import FieldManager
                
        # Initialisation of the Data Field Manager
        mappedDataFields = sharedData["AllDataField"]
        mappedMeshFields = sharedData["AllMeshField"]
        preproDataFieldManager = FieldManager(mappedDataFields, mappedMeshFields)
        
        # Materials properties conversion (e.g for NASCAP based properties)
        #sharedNum['nascapParameterSetList'] should be passed to the simulation model in JyTop

        if self.logger.isDebugEnabled():
            timeProfiler.start("Material properties conversion")
            
        #sharedNum['nascapParameterSetList'] = preproDataFieldManager.convertMaterialProperties( shared["MeshGroupList"], sharedProp['defaultNascapMaterialList'])
        sharedProp['selectedNascapMaterialList'] = preproDataFieldManager.extractSelectedNascapMaterialsList( shared["MeshGroupList"], sharedProp['defaultNascapMaterialList'])
        self.logger.info("Conversion of NASCAP based material properties done.")
     
        sharedProp['materialModel'] = preproDataFieldManager.getMaterialModel()
        self.logger.info("Material model recovered successfully.")
        
        #sharedNum['uiToNumNascapMaterialCorresponcanceDic'] = preproDataFieldManager.getUiToNumNascapMaterialCorresponcanceDic()
        #self.logger.info("Material dictionary recovered.")
        
        # mapping of the Data fields on the grid
        self.logger.info("Data Fields creation and mapping pending... ")
        try:
            if self.logger.isDebugEnabled():
                timeProfiler.start("DataFields creation")
            preproDataFieldManager.CreateDataField(shared['MeshGroupList'])
            if self.logger.isDebugEnabled():
                timeProfiler.start("DataFields mapping")
            preproDataFieldManager.FillFields(shared['MeshGroupList'], shared['Mesh'])
    
            # defined data and corresponding fields are stored in the
            # sharedData common dictionary
            if ( mappedDataFields == None or mappedMeshFields == None):
                self.logger.debug("No pre-existing DF and MS: initialisation and direct setting.")
                mappedDataFields = preproDataFieldManager.GetAllDataField()
                mappedMeshFields = preproDataFieldManager.GetAllMeshField()
            else: 
                self.logger.debug("Pre-existing DF and MF. New DF appended.")
            self.logger.info("             DONE.")
        except:
            self.logger.error(  "It seems that your groups or properties definition are corrupted \n"
                              + "and fields cannot be mapped properly. \n" 
                              + "Please:\n"
                              + "    1-check that you have properly loaded the properties library \n"
                              + "    2-check your groups settings \n"
                              + "    3-reload the mesh \n"
                              + "    4-re-perform the groups conversion \n"
                              + "    6-clean sharedDataField and sharedMeshField in DataBus \n"
                              + "    7-re-perform the fields mapping.")
            
            # to print the stack trace in case of error
            loggingUtilities.printStackTrace()
            
        # to print the time cost
        if self.logger.isDebugEnabled():
            timeProfiler.stop().print()
