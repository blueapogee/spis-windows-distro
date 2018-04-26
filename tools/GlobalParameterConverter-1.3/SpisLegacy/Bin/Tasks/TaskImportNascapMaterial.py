
"""
**File name:**    TasImportNascapMaterial.py

**Creation:**     2010/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information. contract reference, ESA/ETEC funding,CCN2/ on SPIS-TD

:author:       Julien Forest

:version:      1.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Julien Forest                        | Creation                   |
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

import os
from Bin.Tasks.Task             import Task
from Bin.Tasks.shared           import shared
from Bin.Tasks.shared           import sharedData
from Bin.Tasks.shared           import sharedProp
from Bin.Tasks.shared           import sharedFiles
from Bin.Tasks.shared           import addElementToSharedList

from Modules.Properties.MaterialList            import MaterialList
from Modules.InOut.NascapMaterialsCatalogReader import NascapMaterialsCatalogReader

from Bin.config                                 import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_DEFAULT_MATERIAL_TEMPLATES_PATH
from Bin.MaterialMaker                          import MaterialMaker


import org.spis.imp.ui.util.FileDialog


class TaskImportNascapMaterial(Task):
    """Import NASCAP based materials catalog.
    """
    desc = "Import NASCAP based materials catalog."
    
    def run_task(self):
        '''
        Perform the task
        '''
        loader = NascapCatalogLoader()
        loader.loadCatalog()
        
class NascapCatalogLoader:
    """
    Loader for a set of NASCAP materials stored in an XML NASCAP-2K compliant file. This loader
    supports additional and extended properties supported/required by SPIS-NUM (see the SPIS-NUM
    documentation for further informations). 
    """
    
    def __init__(self):
        toto = 1

    def loadCatalog(self):        
        if sharedFiles.has_key("LAST_MATERIAL_PATH"):
            PATH_IN = sharedFiles["LAST_MATERIAL_PATH"]
        else:
            PATH_IN = GL_DEFAULT_MATERIAL_TEMPLATES_PATH
        
        fsd = org.spis.imp.ui.util.FileDialog( PATH_IN )
        fsd.addFileType(".xml", "Nascap format")
        if ( fsd.showOpenDialog(None) ):   #None should set to the parent component
            selectedFile = fsd.getSelectedFileAsString() 
            #self.importer.loadFile(selectedFile)
            print selectedFile
            
            # just to recover the last opened directory where were the data
            splitPath = selectedFile.split(os.sep)[:-1]
            dirPath = ""
            for elm in splitPath:
                dirPath = dirPath+elm+os.sep
            sharedFiles["LAST_MATERIAL_PATH"] = dirPath     

            # if they is no pre-existing list this one is created
            # If they are pre-existing, they are concatenated. 
            if sharedProp.has_key('defaultMaterialList') == 0:
                sharedProp['defaultMaterialList'] = None
            sharedProp['defaultMaterialList'] = addElementToSharedList(sharedProp['defaultMaterialList'], MaterialList())
                
            if sharedProp.has_key('defaultPlasmaList') == 0:
                sharedProp['defaultPlasmaList'] = None
            sharedProp['defaultPlasmaList'] = addElementToSharedList(sharedProp['defaultPlasmaList'], MaterialMaker().BuildDefaultPlasmaList())
        
            if sharedProp.has_key('defaultElecNodeList') == 0 :
                sharedProp['defaultElecNodeList'] = None
            sharedProp['defaultElecNodeList'] = addElementToSharedList(sharedProp['defaultElecNodeList'], MaterialMaker().BuildDefaultElecNodeList())
        
            if sharedProp.has_key('defaultNascapMaterialList') == 0 :
                sharedProp['defaultNascapMaterialList'] = None
            sharedProp['defaultNascapMaterialList'] = addElementToSharedList(sharedProp['defaultNascapMaterialList'], MaterialList())
            
            reader = NascapMaterialsCatalogReader()
            reader.initReferingNumericalMaterialId()
            reader.readNascapPropertiesFile(selectedFile, 1) # set flag to true to generate the corresponding refering NumMat
            

                
                

        
        
        
        
        
  
