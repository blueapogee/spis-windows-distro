"""
**Module Name:**  NascapMaterial

**Project ref:**  Spis/SpisUI

**File name:**    NascapMaterial.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Data structure of material properties at the NASCAP
format.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Pascal Seng

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                | Definition/Creation        |
|                | Franck Warmont@artenum.com    |                            |
+----------------+-------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet               | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com   | Validation                 |
+----------------+-------------------------------+----------------------------+
| 0.3.0          | Pascal Seng                   | Extension                  |
|                | Pascal.Seng@artenum.com       |                            |
+----------------+-------------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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

from Modules.Properties.Data     import Data
from Modules.Properties.DataList import DataList
from Modules.Properties.Material import Material
#from org.slf4j                   import Logger
#from org.slf4j                   import LoggerFactory


def NascapMaterialFactory(MatId, MatName, MatDescription, MatValueList, ExtendedValueList = None):
    '''
    Build-up a Material object from NASCAP properties. NASCAP properties are defined through the MatValueList. 
    The MatValueList is a list of Data object of location 2 (surface). The MatValueList should fit the 
    following fixed structure/order for its elements: 
    see the source code.  
    The MatId correspond to the material Id, as defined in NASCAP and SPIS-NUM. 
    '''
    #logger = LoggerFactory.getLogger("ModulesLogger")
      
          
    # Nascap Material properties
    MatDataList = DataList()        
    MatDataList.Add_Data( Data(1, 'RDC','FLOAT', 'Relative Dielectric Constant', '',2, MatValueList[0], 1) )
    MatDataList.Add_Data( Data(2, 'DMT','FLOAT', 'Dielectric Material Thickness', 'M', 2, MatValueList[1], 1) )
    MatDataList.Add_Data( Data(3, 'BUC','FLOAT', 'Bulk Conductivity', 'ohm-1.m-1', 2, MatValueList[2], 1) )
    MatDataList.Add_Data( Data(4, 'ATN','FLOAT', 'Atomic Number', '', 2, MatValueList[3] ,1) )
    MatDataList.Add_Data( Data(5, 'MSEY','FLOAT', 'Maximum Secondary Electron Yield for Electron Impact', '',2,MatValueList[4],1) )
    MatDataList.Add_Data( Data(6, 'PEE','FLOAT', 'Primary Electron Energy that produces maximum Secondary yield', 'Kev', 2, MatValueList[5],1) )
    MatDataList.Add_Data( Data(7, 'RPR1','FLOAT', 'Range Parameter P7', 'Angstrom', 2, MatValueList[6], 1) )
    MatDataList.Add_Data( Data(8, 'RPN1','FLOAT', 'Range Parameter P8', '', 2, MatValueList[7], 1) )
    MatDataList.Add_Data( Data(9, 'RPR2','FLOAT', 'Range Parameter P9', 'Angstrom', 2, MatValueList[8], 1) )
    MatDataList.Add_Data( Data(10, 'RPN2','FLOAT', 'Range Parameter P10', '', 2, MatValueList[9], 1) )
    MatDataList.Add_Data( Data(11, 'SEY','FLOAT', 'Secondary Electron Yield due to Impact of 1 Kev protons','',2,MatValueList[10],1) )
    MatDataList.Add_Data( Data(12, 'IPE','FLOAT', 'Incident Proton Energy that Produces maximum Secondary Electron Yield','Kev',2,MatValueList[11],1) )
    MatDataList.Add_Data( Data(13, 'PEY','FLOAT', 'Photo-electron Yield for Normal Incident Sunlight','A/m2',2,MatValueList[12],1) )
    MatDataList.Add_Data( Data(14, 'SRE','FLOAT', 'Surface Resistivity','Ohm',2,MatValueList[13],1) )
    MatDataList.Add_Data( Data(15, 'MAP','FLOAT', 'Maximum (absolute) Potential Attainable before Discharging Will Occur','V',2,MatValueList[14],1) )
    MatDataList.Add_Data( Data(16, 'MPD','FLOAT', 'Maximum Potential Difference between Surface and Underlying Conductor before discharging will occur','V',2,MatValueList[15],1) )
    MatDataList.Add_Data( Data(17, 'RCC','FLOAT', 'Radiation Induced Conductivity Coefficient','ohm-1.m-1',2,MatValueList[16],1) )
    MatDataList.Add_Data( Data(18, 'RCP','FLOAT', 'Radiation Induced Conductivity Power','?',2,MatValueList[17],1) )
    MatDataList.Add_Data( Data(19, 'MAD','FLOAT', 'Material Density','kg/m3',2,MatValueList[18],1))
    #FIXME
    #MatDataList.Add_Data( Data(21,'NAS','FLOAT','Not Applicable','',2,MatValueList[20],1) )
    #MatDataList.Add_Data( Data(22,'nascapMatId','INT','nascapMatId','',2,MatId,1))

    mat = Material(MatId, MatName, MatDescription, MatDataList)
    mat.Type = Material.NASCAP_2K_MATERIAL
    #mat.NascapDataList = NascapDataList
    return mat

def AddExtendedProperty(material, name, type, description, unit, value):
    """
    Add an extract property to the current material, for extra properties supported by SPIS-Num, for instance. 
    The default properties list (i.e 19 Nascap parameters) shoudl be defined before (see constructor). 
    """
    dataId = material.DataList.GetMaxId() + 1
    #print "in factory ---> dataId, name, type, description, unit, 2, value, 1"
    #print "in factory --->", dataId, name, type, description, 2, value, 1
    material.DataList.Add_Data( Data( dataId, name, type, description, unit, 2, value, 1) )
    material.EXTENDED_NASCAP_2K_MATERIAL
    

'''
def checkIdToNameConsistency():
    
   #default NASCAP material identification
   IdToMatNameTable = range(26)
   IdToMatNameTable[0] = ("ITOC")
   IdToMatNameTable[1] = ("CERS")
   IdToMatNameTable[2] = ("CFRP")
   IdToMatNameTable[3] = ("KAPT")
   IdToMatNameTable[4] = ("COSR")
   IdToMatNameTable[5] = ("EPOX")
   IdToMatNameTable[6] = ("BLKP")
   IdToMatNameTable[7] = ("BLKH")
   IdToMatNameTable[8] = ("BLKC")
   IdToMatNameTable[9] = ("PCBZ")
   IdToMatNameTable[10]= ("PSG1")
   IdToMatNameTable[11]= ("TEFL")
   IdToMatNameTable[12]= ("CONT")
   IdToMatNameTable[13]= ("GOLD")
   IdToMatNameTable[14]= ("SILV")
   IdToMatNameTable[15]= ("ALOX")
   IdToMatNameTable[16]= ("STEE")
   IdToMatNameTable[17]= ("AL2K")
   IdToMatNameTable[18]= ("AU2K")
   IdToMatNameTable[19]= ("KA2K")
   IdToMatNameTable[20]= ("TE2K")
   IdToMatNameTable[21]= ("OSR2K")
   IdToMatNameTable[22]= ("BK2K")
   IdToMatNameTable[23]= ("SC2K")
   IdToMatNameTable[24]= ("NP2K")
   IdToMatNameTable[25]= ("GP2K")
   
   if (MatId == None):
       logger.warn("set Material Id by Name: "+MatName)
       if MatName in IdToMatNameTable:
           MatId = IdToMatNameTable.index(IdToMatNameTable)
       else:
           logger.error("Material not existing into the NASCAP material list, Id set to -1")
           MatId = -1
   elif ( (MatName == None) or (MatName == "")):
       logger.warn("set Material Name by Id")
       MatName = IdToMatNameTable[MatId]
   else:
       if (MatName == IdToMatNameTable[MatId]):
           logger.error("Material Id and Name not matching")
'''
