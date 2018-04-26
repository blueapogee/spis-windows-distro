"""
Modules of definition of the faces of each cells of the meshing.

**Project ref:**  Spis/SpisUI

**File name:**    Face.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Pascal Seng

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

class Face(MeshElement):
    ''' 
    meshsElement of type FACE (2D). These elements can be TRIANGLE or whathever.
    They are defined by their tops, themselve defined through the MeshElementNodeList.
    The tops connectivity is implicity and by default as direct rotation.
    The other fields are: 
    **FaceId** Id of the element as face (different of the meshElement Id).
    **FaceType** type of face. Currently only TRIANGLE is defined and used.
    **CellOnFace** Id list of cells built on this face.
    **Connection** Edges list on which ones this face is belong in.
    '''
    def __init__(self, ElmtNum = -1, FaceNum = -1, FType = None):
        MeshElement.__init__(self, ElmtNum, 'FACE')
        self.FaceId = FaceNum
        self.FaceType = FType
        self.CellOnFace = []
        self.Connection = []

    def Print_Element(self):
        '''
        Print the current element in stdout.
        '''
        print self

    def __str__(self):
        res = MeshElement.__str__(self)
        res +='    Face Id ' + str(self.FaceId) + os.linesep
        res +='    Face Type ' + str(self.FaceType) + os.linesep
        res +='    Cell On face ' + str(self.CellOnFace) + os.linesep
        res +='    face Settings ' + str(self.check_settings()) + os.linesep
        res +='    Edge Connection' + os.linesep
        for Edge in self.Connection:
            res +='     Mesh Element Id ' + str(Edge.Id) + ' (Edge Id ' \
                   + str(Edge.EdgeId) + ' )' + os.linesep
        return res

    def Modify_Id(self,ElmtNum):
        '''
        Change the Id of the current face and performe the corresponding 
        correction for all related elements (edges, nodes, cells...).
        '''
        for Edge in self.Connection:
            i = Edge.FaceOnEdge.index(self.Id)
            del Edge.FaceOnEdge[i]
            Edge.FaceOnEdge.append(ElmtNum)
            if self.Id in Edge.StartNode.FaceOnNode:
                i = Edge.StartNode.FaceOnNode.index(self.Id)
                del Edge.StartNode.FaceOnNode[i]
            if ElmtNum not in Edge.StartNode.FaceOnNode:
                Edge.StartNode.FaceOnNode.append(ElmtNum)
            if self.Id in Edge.EndNode.FaceOnNode:
                i = Edge.EndNode.FaceOnNode.index(self.Id)
                del Edge.EndNode.FaceOnNode[i]
            if ElmtNum not in Edge.EndNode.FaceOnNode:
                Edge.EndNode.FaceOnNode.append(ElmtNum)
        self.Id = ElmtNum

# XXX removed settings FaceOnNode and EdgeOneNode List in the import
# module
    def Add_Edge(self,Edge):
        '''
        Add a edge to the face definition. This method should imperativelly
        used in place of a simple list.append, because it maintains the 
        self-consistency of related information (connectivity and Ids).
        '''
        if Edge in self.Connection:
            #print ' Edge already in EdgeList'
            spuriousVar = 0
        elif Edge.check_settings() == 0:
            print ' All Edge settings not yet set'
        else:
            if self.Id is not -1:
                Edge.FaceOnEdge.append(self.Id)
                if self.Id not in Edge.StartNode.FaceOnNode:
                    Edge.StartNode.FaceOnNode.append(self.Id)
                if self.Id not in Edge.EndNode.FaceOnNode:
                    Edge.EndNode.FaceOnNode.append(self.Id)
            self.Connection.append(Edge)

    def Del_Edge(self,Edge):
        '''
        Remove a edge from the face definition. This method should imperativelly
        used in place of a simple list.remove, because it maintains the 
        self-consistency of related information (connectivity and Ids).
        '''
        if Edge not in self.Connection:
            print 'Edge is not in EdgeList'
        else:
            if self.Id is not -1:
                i = Edge.FaceOnEdge.index(self.Id)
                del Edge.FaceOnEdge[i]
                i = Edge.StartNode.FaceOnNode.index(self.Id)
                del Edge.StartNode.FaceOnNode[i]
                i = Edge.EndNode.FaceOnNode.index(self.Id)
                del Edge.EndNode.FaceOnNode[i]
            i = self.Connection.index(Edge)
            del self.Connection[i]

    def check_settings(self):
        '''
        Cheks that all settings of the current face are self-consistent.
        '''
        if self.FaceId == -1 or self.FaceType == None:
            return 0
        return MeshElement.check_settings(self)
