"""
**Description:**  This module defines the control loop for the graphic
interface of the console.

**Project ref:**  Spis/SpisUI

**File name:**    MeshFieldList.py

**Creation:**     20/07/2003

**Modification:** 01/10/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Gerard Sookahet, Julien Forest

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+------------------------------+----------------------------+
| Version number | Author (name, e-mail)        | Corrections/Modifications  |
+----------------+------------------------------+----------------------------+
| 0.1.0          | Gerard Sookahet              | Definition/Creation        |
|                | Gerard.Sookahet@artenum.com  |                            |
+----------------+------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet              | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com  | Validation                 |
+----------------+------------------------------+----------------------------+
| 0.3.0          | Julien Forest                | Extension                  |
|                | j.forest@artenum.com         |                            |
+----------------+------------------------------+----------------------------+

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


class MeshFieldList:
   '''
   This defines a structure to stock all MeshFields in 
   one structure. This is in same time a python dictionnary
   and each meshfield may be called via ist key name. On the
   other and, a second list link this dictionnary and an index.
   Meshfields may also called via the index in the list.
   '''
   def __init__(self):
       '''
       Default constructor.
       '''
       self.List = []
       self.Dic = {}
       self.IdList = []
       self.IdDic = {}
       self.NbElement = 0


   def Add_MeshField(self, MeshField):
       ''' 
       Add and set a new MeshField into the lists.
       '''

       self.List.append(MeshField)
       self.Dic[MeshField.Name] = MeshField

       self.IdList.append(MeshField.Id)
       self.IdDic[MeshField.Name] = MeshField.Id

       self.NbElement = self.NbElement+1


   def Del_MeshField(self, MeshField):
       '''
       Removes the element MeshField
       '''

       if MeshField.Id not in self.IdList:
          print ' MeshField is not in MeshFieldList'
       else:
          i = self.IdList.index(MeshField.Id)
          del self.List[i]
	  del self.Dic[MeshField.Name]
          del self.IdList[i]
	  del self.IdDic[MeshField.Name]
          self.NbElement = self.NbElement-1
         
         
   def GetMeshFieldById(self, idIn):
       ''' 
       returns the element of id IdIn.
       '''

       indexElm = self.IdList.index(idIn)
       return(self.List[indexElm])

