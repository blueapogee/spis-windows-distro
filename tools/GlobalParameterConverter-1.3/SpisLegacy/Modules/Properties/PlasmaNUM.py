"""
**Module Name:**  PlasmaNUM 

**Project ref:**  Spis/SpisUI

**File name:**    PlasmaNUM.py

**File type:**    Module

:status:          Implemented

**Creation:**     11/12/2003

**Modification:** 06/06/2003  

**Use:**          N/A

**Description:**  Data structure of PlasmaSN  for SPISNUM integration 
format.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:      Maxime Biais, Julien Forest

:version:      2.0.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Maxime Biais                  | Definition/Creation        |
|                | Maxime.Biais@artenum.com      |                            |
+----------------+-------------------------------+----------------------------+
| 2.0.0          | Julien Forest                 | Definition/Creation        |
|                | contact@artenum.com            |                            |
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
from Modules.Properties.Plasma   import Plasma 

class PlasmaNUM(Plasma):
    '''
    Plasma model in volume for SPIS-NUM.
    '''
    def __init__( self, Id=-1, Name=None, Description=None):
        self.Initialise(Id, Name, Description)
      
      
    def Initialise(self, Id, Name, Description):
        Plasma.__init__(self, Id, Name, Description, None)
        
              
    def __init__( self, Id=-1, Name=None, Description=None, ValueList=None):
        '''
        Default constructor. Set the plasmaNUM instance with 
        the given ValueList according the 
        default DataList.
        '''
        self.Initialise(Id, Name, Description)        
        if ValueList != None:
            self.SetDelfaultDataList(ValueList)
    
    
    def SetDelfaultDataList(self, ValueList):
        '''
        Set the default DataList compliant with SPIS-NUM.
        '''
        self.AddData( Data( self.DataId,
                            'SurfFlag',
                            'Int*1',
                            'surface flag, bit0=1 => on SC, bit1=1 => is a thin surface (2D), bit3=1 => on boundary ',
                            '',
                            2,
                            ValueList[self.DataId-1],
                            1))
    
        self.AddData( Data( self.DataId,
                            'EdgeFlag',
                            'Int*1','edge flag, bit0=1 => on SC, bit1=1 => is a thin surface (2D), bit2=1 => is a wire (1D), bit3=1 => on boundary',
                            '',
                            1,
                            ValueList[self.DataId-1],
                            1))
    
        self.AddData( Data( self.DataId,
                            'NodeFlag',
                            'Int*1','node flag, bit0=1 => on SC, bit1=1 => is a thin surface (2D), bit2=1 => is a wire (1D), bit3=1 => on boundary',
                            '',
                            0,
                            ValueList[self.DataId-1],
                            1) )
    
        self.AddData( Data( self.DataId,
                            'Xyz',
                            'Int*3',
                            'nodes coordinates',
                            '[m]',
                            0,
                            ValueList[self.DataId-1],
                            1) )
    
        self.AddData( Data( self.DataId,
                            'VolInteracFlag',
                            'INT',
                            'If 1, volume interaction is computed in that region (typically charge exchange)',
                            '',
                            3,
                            ValueList[self.DataId-1],
                            1) )
    
        self.AddData( Data( self.DataId,
                            'BackGroundDens',
                            'FLOAT',
                            'Fixed background density used to compute volume interaction (typically: neutral density)',
                            '[m-3]',
                            3,
                            ValueList[self.DataId-1],
                            1) )
