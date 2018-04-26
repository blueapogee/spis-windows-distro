"""
Modules of definition of the structure of the computing node.

**Project ref:**  Spis/SpisUI

**File name:**    Node.py

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

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
from Modules.Meshing.MeshElement        import MeshElement

class Node(MeshElement):
    """Class of definiton of node object. It contains:
            **Coord**  coordinates of the node (list[u, v, w])
            **NodeId** Id of thenode. This one is different of the meshElement Id.
            **EdgeOnNode** Ids list of edges built on this node. 
            **FaceOnNode** Ids list of faces built on this node.
            **CellOnNode** Ids list of cells built on this node.
    """

    def __init__(self, ElmtNum = -1, NodeNum = -1, u = None,
                 v = None, w = None):
        MeshElement.__init__(self, ElmtNum, 'NODE')
        #to optimise
        self.Coord = [u, v, w]
        #self.Coord = (u, v, w)
        self.NodeId = NodeNum
        self.EdgeOnNode = []
        self.FaceOnNode = []
        self.CellOnNode = []

    def Print_Element(self):
        print self

    def __str__(self):
        res = MeshElement.__str__(self)
        res += '    Node Id ' + str(self.NodeId) + os.linesep
        res += '    Coordinate ' + str(self.Coord) + os.linesep
        res += '    Edge On Node ' + str(self.EdgeOnNode) + os.linesep
        res += '    Face On Node ' + str(self.FaceOnNode) + os.linesep
        res += '    Cell On Node ' + str(self.CellOnNode) + os.linesep
        res += '    Node Settings ' + str(self.check_settings()) + os.linesep
        return res

    def check_settings(self):
        if self.Coord[0] == None or self.Coord[1] == None \
               or self.Coord[2] == None or self.NodeId == -1:
            return 0
        return MeshElement.check_settings(self)
