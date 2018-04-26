"""
**Module Name:**  PropertiesList

**Project ref:**  Spis/SpisUI

**File name:**    PropertiesList.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  List of material characteristics.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Julien Forest                 | Definition/Creation        |
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

class PropertiesList:
    '''
    List of Data of Type Material. 
    '''
    def __init__(self):
        self.IdList = []
        self.List = []
        self.NbProperty = 0

    def Add(self, Property):
        self.Add_Property(Property)
        
    def Add_Property(self, Property):
        self.List.append(Property)
        self.IdList.append(Property.Id)
        self.NbMaterial = self.NbProperty+1
        
    def Del(self, Property):
        self.Del_Property(property)

    def Del_Property(self, Property):
        if Property.Id not in self.IdList:
            print ' Material is not in MaterialList'
        else:
            i = self.IdList.index(Property.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbProperty = self.NbProperty-1

    def GetElmById(self, IdIn):
        try:
            return self.List[self.IdList.index(IdIn)]
        except:
            return None
        
    def GetHighestId(self):
        maxId = -10000;
        for currentId in IdList:
            if currentId > maxId:
                maxId = currentId
        return(maxId)