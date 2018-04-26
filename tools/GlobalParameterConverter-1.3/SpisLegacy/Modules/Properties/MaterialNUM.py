"""
**Module Name:**  MaterialNUM

**Project ref:**  Spis/SpisUI

**File name:**    MaterialNUM.py

**File type:**    Module

:status:          Implemented

**Creation:**     06/06/2004

**Modification:** 

**Use:**          N/A

**Description:**  Data structure of material properties for NUM integration 
format.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime BIAIS 

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Maxime BIAIS                  | Definition/Creation        |
|                | Maxime.Biais@artenum.com      |                            |
+----------------+-------------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 101-103 Bld MacDonald,
75019, PARIS, 2004-2004, Paris, France, `http://www.artenum.com`_

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

def MaterialNUM( MatId, MatName, MatDescription, MatValueList):
    '''
    Main constructor. Each material should have a different Id (MatId), 
    an optional description (MatDescription), a name (MatName) 
    and a list of data properties requested by SPIS-NUM. At least this list should
    contain the following items: 
        **MatModelId**: Id of the material model used for this material.
        **MatTypeId**: Id of this material in its material model.
        **MatThickness**: Material thickness.
        **PhotoEmis**: Photo-emission control flag, if =1, photoemission is turned on.
        **ElecSecEmis**: Photo-emission control flag, if =1, secondary electron emission under electron impact is turned on.
        
    ''' 
    MatDataList=DataList()   
    MatDataList.Add_Data( Data(1,'MatModelId','INT','Id of the material model used for this material','',2,MatValueList[0],1) )
    MatDataList.Add_Data( Data(2,'MatTypeId','INT','Id of this material in its material model','',2,MatValueList[1],1) )
    MatDataList.Add_Data( Data(3,'MatThickness','FLOAT','Material thickness','[m]',2,MatValueList[2],1))
    MatDataList.Add_Data( Data(4,'PhotoEmis','INT','Photo-emission control flag, if =1, photoemission is turned on.','',2,MatValueList[3],1) )
    MatDataList.Add_Data( Data(5,'ElecSecEmis','INT','If =1, secondary electron emission under electron impact is turned on','',2,MatValueList[3],1) )
    MatDataList.Add_Data( Data(6,'ProtSecEmis','INT','If =1, secondary electron emission under proton impact is turned on','',2,MatValueList[5],1) )
    MatDataList.Add_Data( Data(7,'VolConduct','INT','If =1, volume conductivity through the bulk material is turned on','',2,MatValueList[6],1) )
    MatDataList.Add_Data( Data(8,'IndConduct','INT','If =1, induced volume conductivity through the bulk material is turned on','',2,MatValueList[7],1) )
    MatDataList.Add_Data( Data(9,'SurfConduct','INT','If =1, surface volume conductivity through the bulk material is turned on','',2,MatValueList[8],1) )
    MatDataList.Add_Data( Data(10,'Temperature','FLOAT','Surface temperature','[K]',2,MatValueList[9],1) )
    MatDataList.Add_Data( Data(11,'SunFlux','FLOAT','Sun flux on spacecraft [sun at 1 AU]','[-]',2,MatValueList[9],1) )

    mat = Material(MatId, MatName, MatDescription, MatDataList)
    mat.Type = Material.LEGACY_MATERIAL
   
    return mat
