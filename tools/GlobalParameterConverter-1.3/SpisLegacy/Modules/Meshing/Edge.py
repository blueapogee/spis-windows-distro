"""
Edge definition module. 

**Project ref:**  Spis/SpisUI

**File name:**    Edge.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Modules of definition of the edges of cells of the meshing.

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
| 0.3.0          | Pascal Seng                   | Extension                  |
|                | Pascal.Seng@artenum.com       |                            |
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
from Modules.Meshing.Node               import Node
from Modules.Meshing.MeshElement        import MeshElement

class Edge(MeshElement):
    def __init__(self, ElmtNum = -1, EdgeNum = -1, SNode = None,
                 ENode = None):
        if SNode == None:
            SNode = Node()
        if ENode == None:
            ENode = Node()
        MeshElement.__init__(self, ElmtNum, 'EDGE')
        self.EdgeId = EdgeNum
        self.StartNode = SNode
        self.EndNode = ENode
        SNode.EdgeOnNode.append(ElmtNum)
        ENode.EdgeOnNode.append(ElmtNum)
        self.FaceOnEdge = []
        self.CellOnEdge = [] # XXX to be implemented ?!
        self.Check_Edge()
    # XXX to be fixed (split printelement and __str__ which was not done
    def Print_Element(self):
        print self

    def __str__(self):
        res = MeshElement.__str__(self)
        res += '    Edge Id ' + str(self.EdgeId) + os.linesep
        res += '    Start Node Id ' + str(self.StartNode.Id) + os.linesep
        res += '    End Node Id ' + str(self.EndNode.Id) + os.linesep
        res += '    Face On Edge ' + str(self.FaceOnEdge) + os.linesep
        #res += '    Cell On Edge ' + str(self.CellOnEdge) + os.linesep
        res += '    Edge Settings ' + str(self.check_settings()) + os.linesep
        return res

    def Check_Edge(self):
        if self.StartNode.check_settings and self.EndNode.check_settings() \
               and self.StartNode.Coord == self.EndNode.Coord:
            print 'Degenerated Edge'

    def check_settings(self):
        if self.EdgeId == -1 or self.StartNode == None or self.EndNode == None:
            return 0
        return MeshElement.check_settings(self)


