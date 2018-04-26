"""
**File name:**    TaskSpisNumInterface.py

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

from Bin.Tasks.Task           import Task

# import of shared data and objects i
# (see shared.py file for more informations)
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedProp
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedNum

from Modules.Utils.LoggingUtilities import LoggingUtilities

from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
from org.slf4j.profiler       import Profiler
#loadingLogger = LoggerFactory.getLogger("CoreLogger")


class TaskSpisNumInterface(Task):
    """
    Performs the data structure conversion from SPIS-UI to SPIS-NUM data structure.
    """
    desc = "Initialisation module of SPISNUM"
    def run_task(self):

        # various logging stuff
        self.logger = LoggerFactory.getLogger("Task")
        # to simplify the various (Jython and Java stack printing)
        loggingUtilities = LoggingUtilities(self.logger)
        # to compute the time cost
        if self.logger.isDebugEnabled():
            timeProfiler = Profiler("TaskSpisNumInterface")
            timeProfiler.start("Num Interface builder initialisation")

        # for dynamical reloading
        import Bin.SpisNumInterface
        reload(Bin.SpisNumInterface)
        from Bin.SpisNumInterface import SpisNumInterface
        
        # FIXME: introduce here fields and groups validation

        # instanciation of the UI to Num conversion interface
        Interface = SpisNumInterface(sharedData['AllDataField'], sharedData['AllMeshField'])

        self.logger.info("UI2Num data structure conversion pending...")
           
        ####################################################
        # MESH CONVERSION
        ####################################################        
        try:
            if self.logger.isDebugEnabled():
                timeProfiler.start("Mesh conversion")
            
            ##########
            Interface.BuildList(shared['Mesh'])
            ##########
            
            self.logger.debug("Volume mesh conversion done.")
        except:
            self.logger.error("ERROR in TaskSpisNumInterface: "
                              + "Hummm... Apparently something wrong with your settings. \n"
                              + "Mesh conversion error. Maybe the mesh is not defined\n"
                              + "or corrupted. Please check your mesh setting, clean-up the data bus, re-mesh and try again...")
            loggingUtilities.printStackTrace()
            self.logger.debug("shared['Mesh']= ", str(shared['Mesh']))
            return(None) # to exit the method
            
        ####################################################
        # Volumic fields mapping
        ####################################################    
        try:
            if self.logger.isDebugEnabled():
                timeProfiler.start("DF in volume conversion")
                
            ##########
            Interface.MapDFOnVolMesh()
            ##########
            
            self.logger.debug("DF in volume conversion done.")
        except:
            self.logger.error("ERROR in TaskSpisNumInterface: Hummm... Apparently something wrong with your settings. \n"
                              + "DF in volume conversion error. Maybe datafields or properties or groups are not defined\n"
                              + "or are corrupted. Please check your groups and properties setting, clean-up the data bus, re-mesh and try again...")
            loggingUtilities.printStackTrace()
            return(None) # to exit the method
            
        try:
            if self.logger.isDebugEnabled():
                timeProfiler.start("DF on the inner boundary (i.e S/C) conversion")
            
            ##########
            Interface.MapDFOnSCMesh()
            ##########
            
            self.logger.debug("step 5 done.")
        except:
            self.logger.error("ERROR in TaskSpisNumInterface: Hummm... Apparently something wrong with your settings. \n"
                              + "DF on the inner boundary (i.e S/C) conversion error. Maybe datafields or properties or groups are not defined\n"
                              + "or are corrupted. Please check your groups and properties setting, clean-up the data bus, re-map and try again..."
                              + "Are-you sure that a group is correctly defined for the whole surface of the S/C (i.e no 'holes') ???")
            loggingUtilities.printStackTrace()
            return(None) # to exit the method

        ####################################################
        # Material properties mapping 
        #################################################### 
        try: 
            if self.logger.isDebugEnabled():
                timeProfiler.start("Material properties conversion")
                
            ##########
            Interface.applyMaterialProperties(sharedProp['materialModel'], sharedProp['selectedNascapMaterialList'])
            ##########
            
            self.logger.debug("step 7 done.")
        except:
            self.logger.error("ERROR in TaskSpisNumInterface: Hummm... Apparently something wrong with your settings. \n"
                              + "Material properties conversion error. Maybe material properties or groups are not defined\n"
                              + "or corrupted. Please check your groups and properties settings, clean-up the data bus, re-map and try again..."
                              + "Are-you sure that all your properties models are consistent and/or properly set ???")
            loggingUtilities.printStackTrace()
            self.logger.debug("sharedProp['materialModel']= ", str(sharedProp['materialModel']))
            self.logger.debug("sharedNum['uiToNumNascapMaterialCorresponcanceDic']= ", str(sharedNum['uiToNumNascapMaterialCorresponcanceDic']))
            return(None) # to exit the method
            
            
        try:
            if self.logger.isDebugEnabled():
                timeProfiler.start("DF on external boundary conversion") 
            
            ##########
            Interface.MapDFOnBdMesh()
            ##########
            
            self.logger.debug("step 8 done.")
        except:
            self.logger.error("ERROR in TaskSpisNumInterface: Hummm... Apparently something wrong with your settings. \n"
                              + "DF on external boundary conversion. Maybe your numerical properties (i.e plasma) or groups are not defined\n"
                              + "or corrupted. Please check your groups and properties settings, clean-up the data bus, re-map and try again..."
                              + "Are-you sure that you have set properly the external boundary ???")
            loggingUtilities.printStackTrace()
            return(None) # to exit the method
            
            
        try:
            if self.logger.isDebugEnabled():
                timeProfiler.start("Mesh cross numbering")
            
            ##########
            Interface.buildCrossNumberingBetweenMesh()
            ##########
            
            self.logger.debug("step 9 done.")
            
            
            if self.logger.isDebugEnabled():
                timeProfiler.start("SPIS-NUM compliant mesh structure recovering")
            
            ##########
            sharedNum['SNMesh'] = Interface.GetSpisNumMesh()
            ##########
            
            self.logger.debug("step 10 done.")
            
            self.logger.info("            DONE")
        except:
            self.logger.error("ERROR in TaskSpisNumInterface: Data inconsistency ! Please clean all existing DataFields \n"
                             +"and check your groups settings and properties definitions\n"
                             +"Hummm... Apparently something wrong with your settings. \n"
                             +"Please, check the groups definitions and properties settings, clean-up the data bus and try again.")
            loggingUtilities.printStackTrace()
            
        # to print the time cost
        if self.logger.isDebugEnabled():
            timeProfiler.stop().print()


