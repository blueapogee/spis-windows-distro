"""
**Module Name:**  SkeletonElement

**Project ref:**  Spis/SpisUI

**File name:**    SkeletonElement.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Modules of definition of the structure to the
skeleton elements. The skeleton elements are mesh elements directly linked,
in terms of groups, to the pre-existing group on the geometry (CAD).

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
from Modules.Meshing.EdgeList           import EdgeList
from Modules.Meshing.FaceList           import FaceList
from Modules.Meshing.CellList           import CellList
from Modules.Meshing.NodeList           import NodeList
from Modules.Meshing.MeshElement        import MeshElement

class SkeletonElement:
    '''
    Modules of definition of the structure to the skeleton elements. 
    The skeleton elements are mesh elements directly linked, in terms of 
    groups, to the pre-existing group on the geometry (CAD). They typically correspond
    to the boundaries. 
    '''
    def __init__(self, ElmtNum = None, ElmtType = None, ElmtNodeList = None):
        self.Id = ElmtNum
        self.Type = ElmtType
        if ( ElmtNodeList != None) :
            self.NodeNumber = len(ElmtNodeList.List)
        else : 
            print "ERROR: ElmtNodeList null"
        self.SkeletonNodeList = ElmtNodeList
        self.SkeletonEdgeList = EdgeList() # List of Edge that derive
					   # from skeleton element
        self.SkeletonFaceList = FaceList() # List of Face that derive
					   # from skeleton element
        self.SkeletonCellList = CellList() # List of Cell that derive
					   # from skeleton element

        self.Comments = ""
        self.Settings = 1

    def Print_Element(self):
        print self

    def __str__(self):
        res = 'Skeleton Element Id ' + str(self.Id) + os.linesep
        res += 'Skeleton Element Type ' + self.Type + os.linesep
        res += 'Comments: ' + self.Comments + os.linesep
        res += 'Skeleton Element Geometry Group Id ' + str(self.GeoGroup.Id)\
               + os.linesep
        res += 'Skeleton Element Geometry Element Id ' \
               + str(self.GeoElement.Id) + os.linesep
        res += 'Skeleton Element Node Number ' + str(self.NodeNumber) + os.linesep
        res += 'Skeleton Element Mesh Element Id ' \
               + str(self.SkeletonMeshElement.Id) + os.linesep
        res += 'Skeleton Element Settings ' + str(self.Settings) + os.linesep
        res += 'List of Mesh Element nodes ' \
               + str(self.SkeletonNodeList.IdList) + os.linesep
        res += 'List of Mesh Element edges ' \
               + str(self.SkeletonEdgeList.IdList) + os.linesep
        res += 'List of Mesh Element faces ' \
               + str(self.SkeletonFaceList.IdList) + os.linesep
        res += 'List of Mesh Element cells ' \
               + str(self.SkeletonCellList.IdList) + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Type == None or self.SkeletonNodeList == None:
            return 0
        return 1
