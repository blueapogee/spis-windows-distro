"""
**Module Name:**  ElecNodeNUM 

**Project ref:**  Spis/SpisUI

**File name:**    ElecNodeNUM.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/02/2004

**Modification:** 02/02/2004  

**Use:**          N/A

**Description:**  Data structure of Default ElecNodeSN  for SPISNUM integration 
format.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:      Maxime Biais 

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Maxime Biais                  | Definition/Creation        |
|                | Maxime.Biais@artenum.com      |                            |
+----------------+-------------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; version 2 
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
from Modules.Properties.ElecNode import ElecNode 

def ElecNodeNUM(ENId, ENName, ENDescription, ENValueList):
        
    DataId = 0
    ENDataList=DataList()
    DataId = DataId+1
    DataTmp=Data(DataId, 'ElecNodeId', 'INT', 'The (macro) electric surface node. This element is related to (SC ground, array ground)', '', 2, ENValueList[0], 1)
    ENDataList.Add_Data(DataTmp)
    
    DataId = DataId+1
    DataTmp=Data(DataId, 'EdgeElecNodeId', 'INT', 'The (macro) electric edge node. This element is related to (SC ground, array ground)', '', 1, ENValueList[0], 1)
    ENDataList.Add_Data(DataTmp)
    
    #FOR TEST PURPOSE
    #print "Node Id=", ENId
    #print ENDataList.List
    #if ENDataList.List != None:
    #    print ENDataList.List[0]
    #    print ENDataList.List[1]
    #else:
    #    print ENDataList.List

    return ElecNode(ENId, ENName, ENDescription, ENDataList)
