"""
Properties groups on mesh. 

**File name:**    MeshGroup.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 3.1.0   | Yves Le Rumeur                       | Modif                      |
|         | lerumeur@artenum.com                 |                            |
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

from Modules.Meshing.MeshElementList    import MeshElementList
from Modules.Meshing.SkeletonElementList import SkeletonElementList
from Modules.Properties.Material        import Material
from Modules.Properties.ElecNode        import ElecNode
from Modules.Properties.Plasma          import Plasma

from com.artenum.free.mesh.interfaces  import MeshGroup as JMeshGroup

class MeshGroup:
    '''
    Properties groups on mesh.
    '''
    def __init__(self, GrpNum = -1, GrpName = None, GrpType = None,
                 GrpDescription = None, GrpVisible = None,
                 GrpSkeletonList = None,
                 GrpElementList = None,
                 GrpMaterial = None, GrpElecNode = None,
                 GrpPlasma = None, jMeshGroupIn = None):
        
        self.Id = GrpNum
        self.Name = GrpName
        self.Type = GrpType
        self.Description = GrpDescription
        self.Visible = GrpVisible
        
        self.jMeshGroup = jMeshGroupIn



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

    """
    commment 1
    """
    __docformat__ = "restructuredtext en"
    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Type == None \
               or self.Description == None or self.Visible == None \
               or self.SkeletonElementList == None \
               or self.MeshElementList == None or self.Plasma == None \
               or self.Material == None or self.ElecNode == None:
            return 0
        return 1

    def Print_Group(self):
        print self

    def __str__(self):
        res = 'Mesh Group Id ' + str(self.Id) + os.linesep
        res += 'Mesh Group Name ' + self.Name + os.linesep
        res += 'Mesh Group Type ' + self.Type + os.linesep
        res += 'Mesh Group Description ' + str(self.Description) + os.linesep
        res += 'Mesh Group Visible ' + str(self.Visible) + os.linesep
        res += 'Mesh Group Settings ' + str(self.check_settings()) + os.linesep
        res += 'Mesh Group Material Id ' + str(self.Material.Id) \
               + ' of Type/Name ' + str(self.Material.Name) + os.linesep
        res += 'Mesh Group ElecNode Id ' + str(self.ElecNode.Id) \
               + ' of Type/Name ' + str(self.ElecNode.Name) + os.linesep
        res += 'Mesh Group Plasma Id ' + str(self.Plasma.Id) \
               + ' of Type/Name ' + str(self.Plasma.Name) + os.linesep
        return res
