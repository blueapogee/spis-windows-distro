"""
List of compuationnal nodes.

**Project ref:**  Spis/SpisUI

**File name:**    NodeList.py

**File type:**    Module

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

from PickledList import PickledList

# FIXME: this class is useless
class NodeList(PickledList):
    def __init__(self):
        self.List = []
        self.IdList = []
        self.NbNode = 0

    def Add_Node(self, Node):
        self.List.append(Node)
        self.IdList.append(Node.Id)
        self.NbNode = self.NbNode+1

    def Del_Node(self, Node):
        if Node.Id not in self.IdList:
            print ' Node is not in NodeList'
        else:
            i = self.IdList.index(Node.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbNode = self.NbNode-1

    def GetElementById(self, IdIn):
         ''' returns the element of id IdIn.'''
         indexElm = self.IdList.index(IdIn)
         return(self.List[indexElm])

    def SetElementById(self, ElmIn, Idin):
         '''Set the element ElmIn of id Idin'''
         indexElm = self.IdList.index(IdIn)
         self.List[indexElm] = ElmIn