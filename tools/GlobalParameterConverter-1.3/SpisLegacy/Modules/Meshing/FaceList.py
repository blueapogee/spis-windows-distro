"""
**Module Name:**  FaceList

**Project ref:**  Spis/SpisUI

**File name:**    FaceList.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  List of faces.

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


from PickledList import PickledList

class FaceList(PickledList):
    def __init__(self):
        self.List = []
        self.IdList = []
        self.NbFace = 0

    def Add_Face(self, Face):
        self.List.append(Face)
        self.IdList.append(Face.Id)
        self.NbFace = self.NbFace+1

    def Del_Face(self, Face):
        if Face.Id not in self.IdList:
            print ' Face is not in FaceList'
        else:
            i = self.IdList.index(Face.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbFace = self.NbFace-1

    def GetElementById(self, IdIn):
         ''' returns the element of id IdIn.'''
         indexElm = self.IdList.index(IdIn)
         return(self.List[indexElm])

    def SetElementById(self, ElmIn, Idin):
         '''Set the element ElmIn of id Idin'''
         indexElm = self.IdList.index(IdIn)
         self.List[indexElm] = ElmIn

