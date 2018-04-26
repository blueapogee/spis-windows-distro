"""
**File name:**    NascapMaterialsCatalogReader.py

**Creation:**     2010/03/20

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

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

import os, sys

from Bin.Tasks.shared           import sharedProp
from Bin.Tasks.shared           import addElementToSharedList

from Modules.Properties.NascapMaterialFactory import NascapMaterialFactory
from Modules.Properties.NascapMaterialFactory import AddExtendedProperty

from Modules.Properties.MaterialList        import MaterialList
from Modules.Properties.MaterialNUM         import MaterialNUM
from Modules.Properties.Material            import Material

import org.spis.imp.io.nascap 
from org.spis.imp.io.nascap    import NascapXMLReader


class NascapMaterialsCatalogReader:
    """
    XML based Nascap properties catalog reader. 
    This reads the XML based NASCAP properties file and the correspondance list, used 
    to make the link between SPIS numerical material (e.g like default SPIS material) 
    and the corresponding NASCAP material.  
    
    By default the respective names of the NASCAP material catalog and the correspondance
    list are :
    
    - NascapMaterialCatalog.xml
    - materialCorrespondanceList.py
    
    If these files names are not changed, it is only needed to set the directory path where
    both files are stored. 
    """
    
    def __init__(self):
        """
        default constructor.
        """
        self.nascapMaterialNamesList = None
        self.nascapMaterialIdsList = None
        self.catalog = None
        self.correspondanceListName = "materialCorrespondanceList.py"
        self.nascapMaterialCatalogName = "NascapMaterialCatalog.xml"
        
    def setMaterialCorrespondanceListName(self, listName):
        """
        Set the name of the material correspondance list, if this one should 
        be set to the another value than the default one (i.e materialCorrespondanceList.py).
        Pay attention that the modification of this value may impact the compliance of your 
        persistence scheme with the standard SPIS project structure and made it unreadable 
        by another SPIS installation. 
        """
        self.correspondanceListName = listName
        
    def setNascapMaterialCatalogName(self, catalogName):
        """
        Set the name of the NASCAP materials catalog, if this one should 
        be set to the another value than the default one (i.e NascapMaterialCatalog.xml).
        Pay attention that the modification of this value may impact the compliance of your 
        persistence scheme with the standard SPIS project structure and made it unreadable 
        by another SPIS installation. 
        """
        self.nascapMaterialCatalogName = catalogName
        
    def read(self, nascapPropertiesDir):
        """
        Read both catalog and correspondance list. 
        """
        
        # to help the import of the correspondance tables
        sys.path.append(nascapPropertiesDir)        
        
        self.readCorrespondanceTable(nascapPropertiesDir+os.sep+self.correspondanceListName)
        self.readNascapPropertiesFile(nascapPropertiesDir+os.sep+self.nascapMaterialCatalogName)
        
        
    def readCorrespondanceTable(self, fileName):
        """
        Read the correspondance list. Generally not called directly and used through the read method
        only. 
        """
        moduleName = fileName.split(os.sep)[-1:]
        tmpCmd = "import "+moduleName[0][:-3]
        #print tmpCmd
        exec(tmpCmd)
        tmpCmd = "self.nascapMaterialNamesList = "+self.correspondanceListName.split(".")[0]+".nascapMaterialNamesList"
        #print tmpCmd
        exec(tmpCmd)
        tmpCmd = "self.nascapMaterialIdsList = "+self.correspondanceListName.split(".")[0]+".nascapMaterialIdsList"
        #print tmpCmd
        exec(tmpCmd)
        
    def initReferingNumericalMaterialId(self, initialId = None):
        
        if (initialId == None):
            # to avoid overlap with built-in materials
            dn = 1000 
            matIdShift = ( sharedProp['defaultMaterialList'].GetHighestId()/dn + 1) * dn
            print  "matIdShift= ", matIdShift
            self.matId = matIdShift
        else:
            self.matId = initialId
        
    def readNascapPropertiesFile(self, fileName, buildReferingMaterialFlag = 0):
        """
        Read the NASCAP material catalog. Generally not called directly and used through the read method
        only.
        """
        # we initialised the shared list if needed
        self.initDefaultNascapMaterialList()
        
        reader = NascapXMLReader()
        self.catalog = reader.readFile(fileName)
        
        for nascapMat in self.catalog:
            if (buildReferingMaterialFlag):
                nascapMatId = self.matId
            else:
                nascapMatId = self.nascapMaterialIdsList[ self.nascapMaterialNamesList.index(nascapMat.getName())]
            # first we build the NASCAP material itself
            list = nascapMat.getDataList()
            newNascapMat = NascapMaterialFactory( nascapMatId, nascapMat.getName(), "Ext. NASCAP material", list)
            newNascapMat.Type = None #to forbid all sub-properties
                
            # now we add the extended properties for SPIS-NUM models
            for extendedProperty in nascapMat.getExtendedProperties():
                # print "name type descrip unit value"
                #print extendedProperty.getName(), extendedProperty.getType(), extendedProperty.getDescription(), extendedProperty.getUnit(), extendedProperty.getValue() 
                AddExtendedProperty(newNascapMat, extendedProperty.getName(), 
                                                      extendedProperty.getType(), 
                                                      extendedProperty.getDescription(), 
                                                      extendedProperty.getUnit(),
                                                      extendedProperty.getValue())
            
            sharedProp["defaultNascapMaterialList"].Add(newNascapMat)
            if (buildReferingMaterialFlag):
                self.buildReferingNumericalMaterial(self.matId, nascapMatId, nascapMat)
            
            
    def buildReferingNumericalMaterial(self, matId, nascapMatId, nascapMat):
        """
        Internal method
        """           
        # then we build the SPIS Numerical material that refer to the Nascap Material defined above 
        Comment='Ext. NASCAP based numerical material, please check the default values regarding the interaction flags'
                
        # NB: This will refer to: 
        #     A NASCAP based material (MatModelId always equal to 0)
        #     DEfined through its Id (MatTypeId)
        #FIXME: Not robust to be improve
        # for now we add the matIdShift value to avoid any overlap with built-in materials
        ValueList=[0, nascapMatId, 0.0001, 1, 1, 1, 1, 1, 1, 300, 1] 
        newMat = MaterialNUM( self.matId, nascapMat.getName()+" (num. mat.)", Comment, ValueList)
        newMat.Type = Material.NASCAP_2K_MATERIAL
        sharedProp['defaultMaterialList'].Add(newMat)
        self.matId = self.matId + 1
            


    def initDefaultNascapMaterialList(self):
        
        if sharedProp.has_key('defaultNascapMaterialList') == 0 :
                sharedProp['defaultNascapMaterialList'] = None
        sharedProp['defaultNascapMaterialList'] = addElementToSharedList(sharedProp['defaultNascapMaterialList'], MaterialList())