"""
**Module Name:**  PlasmaNUMSC 

**Project ref:**  Spis/SpisUI

**File name:**    PlasmaNUMSC.py

**File type:**    Module

:status:          Implemented

**Creation:**     26/12/2003

**Modification:** 06/06/2004  

**Use:**          N/A

**Description:**  Data structure of Plasma fields living on SC  for SPISNUM integration 
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

from Modules.Properties.Data           import Data
from Modules.Properties.DataList       import DataList
from Modules.Properties.PlasmaNUMSC    import PlasmaNUMSC

class PlasmaNUMSCThinsurf(PlasmaNUMSC):
    '''
    Plasma model for the S/C surface.
    '''
    def __init__( self, Id, Name, Description):
        self.Initialise(Id, Name, Description)
        
    def Initialise(self, Id, Name, Description):
        PlasmaNUMSC.__init__(self, Id, Name, Description, None)
              
    def __init__( self, Id, Name, Description, ValueList):
        '''
        Set the plasmaNUM instance with the given ValueList according the 
        default DataList.
        '''
        self.__init__( self, Id, Name, Description)
        self.SetDelfaultDataList( ValueList)
        self.AddThinElmList( ValueList)
        
    
    def AddThinElmList(self, ValueList):
        DataTmp = Data( DataId,
                        'SurfIndexSC',
                        'Int*1',
                        'Index of the side A of the thin surface',
                        '',
                        2,
                        PlaValueList[DataId-1],
                        1) 
        PlaDataList.Add_Data(DataTmp)
        DataId = DataId+1
    
        DataTmp = Data( DataId,
                        'EdgeIndexSC',
                        'Int*1',
                        'Index of the side A of the thin surface',
                        '',
                        2,
                        PlaValueList[DataId-1],
                        1) 
        PlaDataList.Add_Data(DataTmp)
        DataId = DataId+1
    
        DataTmp = Data( DataId,
                        'NodeIndexSC',
                        'Int*1',
                        'Index of the side A of the thin surface',
                        '',
                        2,
                        PlaValueList[DataId-1],
                        1) 
        PlaDataList.Add_Data(DataTmp)
        DataId = DataId+1
