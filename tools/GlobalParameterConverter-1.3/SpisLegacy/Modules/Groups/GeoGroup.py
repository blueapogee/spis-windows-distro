"""
Modules of definition of geometrical groups (groups on
CAD elements) for definition of physical properties.
"a la GMSH".

**Module Name:**  GeoGroup

**Project ref:**  Spis/SpisUI

**File name:**    GeoGroup.py

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.2.0

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

import os
from Modules.Geometry.GeoElementList    import GeoElementList
from Modules.Properties.Material        import Material
from Modules.Properties.ElecNode        import ElecNode
from Modules.Properties.Plasma          import Plasma

class GeoGroup:
    '''
    Modules of definition of geometrical groups (groups on
    CAD elements) for definition of physical properties.
    "a la GMSH".
    '''

    def __init__(self, GrpNum = -1, GrpName = None, GrpType = None,
                 GrpDescription = None, GrpVisible = None,
                 GrpElementList = None, GrpMaterial = None,
                 GrpElecNode = None, GrpPlasma = None):
        self.Id = GrpNum
        self.Name = GrpName
        self.Type = GrpType
        self.Description = GrpDescription
        self.Visible = GrpVisible
        self.thin = 0
        self.border = 0
        self.ctrVtkDataset = 0
        
        if GrpElementList == None:
            self.ElementList = GeoElementList()
        else:
            self.ElementList = GrpElementList

        if GrpMaterial == None:
            self.Material = Material()
        else:
            self.Material = GrpMaterial

        if GrpElecNode == None:
            self.ElecNode = ElecNode()
        else:
            self.ElecNode = GrpElecNode

        if GrpPlasma == None:
            self.Plasma = Plasma()
        else:
            self.Plasma = GrpPlasma

        self.IsDuplicated = 0 # 0-group None-duplicated
                              # 1-group duplicated

    def Print_Group(self):
        print self

    def __str__(self, fieldSep = None):
        if fieldSep == None:
           sep = ""
        else: 
           sep = fieldSep
        res = 'Geometrical Group Id' +sep+ str(self.Id) + os.linesep
        res += 'Geometrical Group Name '+sep+ str(self.Name) + os.linesep
        res += 'Geometrical Group Type '+sep+ str(self.Type) + os.linesep
        res += 'Geometrical Group Description '+sep+ str(self.Description) + os.linesep
        res += 'Geometrical Group Visible '+sep+ str(self.Visible) + os.linesep
        res += 'Geometrical Group Settings '+sep+ str(self.check_settings()) \
               + os.linesep
        res += 'Geometrical Group Material Id '+sep+ str(self.Material.Id) \
               +  ' of Type/Name '+sep+ str(self.Material.Name) + os.linesep
        res += 'Geometrical Group ElecNode Id '+sep+ str(self.ElecNode.Id) \
               + ' of Type/Name '+sep+ str(self.ElecNode.Name) + os.linesep
        res += 'Geometrical Group Plasma Id '+sep+ str(self.Plasma.Id) + \
               ' of Type/Name '+sep+ str(self.Plasma.Name) +  os.linesep
        res += 'Geometrical Group Number of Element '+sep+ str(self.ElementList.NbElement) + os.linesep
        res += 'Geometrical Group Element Id List '+sep \
               + str(self.ElementList.IdList) + os.linesep
        res += 'List of Elements defined'
        for GeoElement in self.ElementList.List:
            res += ' Geometrical Element Id '+sep+ str(GeoElement.Id) \
                   +sep+ ' of Type '+sep+ str(GeoElement.Type) + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Type == None \
           or self.Description == None or self.Visible == None \
           or self.ElementList == None or self.Material == None \
           or self.Material == None or self.ElecNode == None \
           or self.Plasma == None:
            return 0
        return 1
