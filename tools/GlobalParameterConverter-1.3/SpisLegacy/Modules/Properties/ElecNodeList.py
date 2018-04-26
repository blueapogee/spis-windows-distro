"""
List of electrical nodes.

**Project ref:**  Spis/SpisUI

**File name:**    ElecNodeList.py

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

class ElecNodeList:
    '''
    List of Data of type ElecNode.
    '''
    def __init__(self):
        self.List = []
        self.IdList = []
        self.NbElecNode = 0
        
    def Add(self, ElecNode):
        self.Add_ElecNode(ElecNode)

    def Add_ElecNode(self, ElecNode):
        self.List.append(ElecNode)
        self.IdList.append(ElecNode.Id)
        self.NbElecNode = self.NbElecNode+1

    def Del_ElecNode(self, ElecNode):
        if ElecNode.Id not in self.IdList:
            print ' ElecNode is not in ElecNodeList'
        else:
            i = self.IdList.index(ElecNode.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbElecNode = self.NbElecNode-1

    def GetElmById(self, IdIn):
        try:
            return self.List[self.IdList.index(IdIn)]
        except:
            return None

