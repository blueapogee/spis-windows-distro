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

from Modules.Properties.Data         import Data
from Modules.Properties.DataList     import DataList
from Modules.Properties.PlasmaNUM    import PlasmaNUM

class PlasmaNUMSC(PlasmaNUM):
    '''
    Plasma model for the S/C surface.
    '''
    def __init__( self, Id=-1, Name=None, Description=None):
        self.InitialiseLocal(Id, Name, Description)
        
    def InitialiseLocal(self, Id, Name, Description):
        PlasmaNUM.__init__(self, Id, Name, Description, None)
              
    def __init__( self, Id=-1, Name=None, Description=None, ValueList=None):
        '''
        Set the plasmaNUM instance with the given ValueList according the 
        default DataList.
        '''        
        self.InitialiseLocal(Id, Name, Description)
        
        if ValueList != None:
            self.SetDelfaultDataList(ValueList)
            self.SetAdditionnalDataList(ValueList)             
        
    
    def SetAdditionnalDataList(self, ValueList):
        '''
        Set the default DataList compliant with SPIS-NUM.
        '''
        self.AddData( Data( self.DataId,
                            'SurfFlagS',
                            'Int*1',
                            'surface flag of a surface mesh, bit1=0 => a thin surface',
                            '',
                            2,
                            ValueList[self.DataId-1],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'SurfThicknessS',
                            'Int*1',
                            'surface real physical thickness in case it is considered as thin from the mesh viewpoint (thickness not meshed)',
                            '',
                            2,
                            ValueList[self.DataId],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'EdgeFlagS',
                            'Int*1',
                            'edge flag of a surface mesh, bit0=1 => is on a wire, bit1=1 => is on a thin surface',
                            '',
                            1, 
                            ValueList[self.DataId-1], 
                            1) )

        self.AddData( Data( self.DataId,
                            'EdgeRadiusS',
                            'FLOAT',
                            'real physical wire radius in case this edge is indeed a wire (wire cylinder not meshed)',
                            '[m]',
                            1,
                            ValueList[self.DataId-1],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'NodeFlagS',
                            'INT*1',
                            'node flag of a surface mesh, bit0=1 => node of a wire, bit1=1 => node of thin surface',
                            '',
                            0,
                            ValueList[self.DataId-1],
                            1) )

        self.AddData( Data( self.DataId,
                            'XyzS',
                            'Int*3',
                            'nodes coordinates',
                            '[m]',
                            0,
                            ValueList[self.DataId-1],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'SCDiriFlag',
                            'INT',
                            'If 1, Dirichlet condition for Poisson equation on SC (fixed potential)',
                            '',
                            0, 
                            ValueList[self.DataId-1],
                            1) )

        self.AddData( Data( self.DataId,
                            'SCDiriPot',
                            'FLOAT',
                            'The potential to be used for Dirichlet condition',
                            '[V]', 
                            0,
                            ValueList[self.DataId-1],
                            1) )

        self.AddData( Data( self.DataId,
                            'SCDiriPotEdge',
                            'FLOAT',
                            'The potential to be used for Dirichlet condition, localised on surfaces',
                            '[V]', 
                            1,
                            ValueList[self.DataId-1],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'SCDiriPotSurf',
                            'FLOAT',
                            'The potential to be used for Dirichlet condition, localised on surfaces',
                            '[V]', 
                            2,
                            ValueList[self.DataId-1],
                            1) )
    
        self.AddData( Data( self.DataId,
                            'SCFourFlag',
                            'INT',
                            'If 1, Fourier condition for Poisson equation on SC: alpha pot + d(pot)/dn = value',
                            '',
                            2,
                            ValueList[self.DataId-1],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'SCFourAlpha',
                            'FLOAT',
                            'Alpha parameter in Fourier condition:alpha pot + d(pot)/dn = value',
                            '[m-1]',
                            2,
                            ValueList[self.DataId-1],
                            1) )
                            
        self.AddData( Data( self.DataId,
                            'SCFourValue',
                            'FLOAT',
                            'Right hand side parameter in Fourier condition : alpha pot + d(pot)/dn = value NB: note the centring different from other Fourier parameters',
                            '[V/m]',
                            0,
                            ValueList[self.DataId-1], 
                            1) )

        self.AddData( Data( self.DataId,
                            'SourceId',
                            'INT',
                            'Id/type of an artificial plasma source defined on the spacecraft (e.g. thruster or ion gun)',
                            '',
                            2,
                            ValueList[self.DataId-1],
                            1) )
                        
                        
        self.AddData( Data( self.DataId, 
                            'SourceCurrent', 
                            'FLOAT',
                            'Current of an artificial source defined on the spacecraft (NB: for some sources the unit can be different, e.g. the particle number, or the total current)',
                            '[A/m2]',
                            2,
                            ValueList[self.DataId-1],
                            1) )

        self.AddData( Data( self.DataId,
                            'SourceTemp', 
                            'FLOAT',
                            'Temperature of the emitted Maxwellian distribution',
                            '[eV]',
                            2,
                            ValueList[self.DataId-1],
                            1) )
                           
        self.AddData( Data( self.DataId,
                            'SourceMach',
                            'FLOAT',
                            'Source Mach number (0 => Lambertian)',
                            '[-]',
                            2,
                            ValueList[self.DataId-1],
                            1) )
                            
