"""
**Module Name:**  PlasmaNUMBd 

**Project ref:**  Spis/SpisUI

**File name:**    PlasmaNUMBd.py

**File type:**    Module

:status:          Implemented

**Creation:**     27/12/2003

**Modification:** 27/12/2003  

**Use:**          N/A

**Description:**  Data structure of Plasma fields living on External Boundary  for SPISNUM integration 
format.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:      Maxime Biais 

:version:      0.&.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Maxime Biais                  | Definition/Creation        |
|                | Maxime.Biais@artenum.com      |                            |
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
from Modules.Properties.Plasma import Plasma 

def PlasmaNUMBd(PlaId,PlaName,PlaDescription,PlaValueList):
    DataId = 1
    PlaDataList=DataList()
    DataTmp=Data(DataId,'SurfFlagBd','Int*1','surface flag of a surface mesh, unused for external boundary','',2,PlaValueList[DataId-1],1) ;PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'EdgeFlagBd','Int*1','edge flag of a surface mesh, unused for external boundary','',1,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'NodeFlagBd','Int*1','node flag of a surface mesh, unused for external boundary','',0,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp) ; DataId = DataId+1
    #DataTmp=Data(DataId,'xyzBd','Int*3','nodes coordinates','',0,PlaValueList[DataId-1],1); PlaDataList.Add_Data(DataTmp)
    DataTmp=Data(DataId,'XyzBd','Int*3','nodes coordinates','',0,PlaValueList[DataId-1],1); PlaDataList.Add_Data(DataTmp); DataId = DataId+1 # correction JFR
 
    DataTmp=Data(DataId,'BdDiriFlag','INT','If 1, Dirichlet condition for Poisson equation on external boundary (fixed potential)','',0,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'BdDiriPot','FLOAT','The potential to be used for Dirichlet condition','[V]',0,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'BdFourFlag','INT','If 1, Fourier condition for Poisson equation on external boundary','',2,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'BdFourAlpha','FLOAT','Alpha parameter in Fourier condition','[m-1]',2,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'BdFourValue','FLOAT','Right hand side parameter in Fourier condition','[V/m]',0,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'IncomPart','INT','If =1, particle are injected','',2,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1
    DataTmp=Data(DataId,'OutgoPart','INT','If =1, outgoing particles bounce specularly, otherwise they are lost (=0)','',2,PlaValueList[DataId-1],1) ; PlaDataList.Add_Data(DataTmp); DataId = DataId+1



    return Plasma(PlaId,PlaName,PlaDescription,PlaDataList)
