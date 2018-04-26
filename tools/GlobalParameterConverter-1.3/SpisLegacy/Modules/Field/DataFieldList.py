
"""
**Description:**  This module defines the list of field of data.

**Project ref:**  Spis/SpisUI

**File name:**    DataFieldList.py

**Creation:**     02/07/2003

**Modification:** 10/09/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Julien Forest

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Gerard Sookahet                | Definition/Creation        |
|                | Gerard.Sookahet@artenum.com    |                            |
+----------------+--------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet                | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com    | Validation                 |
+----------------+--------------------------------+----------------------------+
| 0.3.0          | Julien Forest                  | Extension                  |
|                | j.forest@artenum.com           |                            |
+----------------+--------------------------------+----------------------------+

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

class DataFieldList:
    '''
    List of dataField. This list gathers registered dataFields in an 
    indexed list. It provides also high performance accessors.
    '''
    def __init__(self):
        '''
        Default constructor. 
        '''
        self.List = []
        self.Dic = {}
        self.IdList = []
        self.IdDic = {}
        self.NbData = 0

    def Add_DataField(self, DataField):
        '''
        Add the DataField in input to the list.
        '''
        self.List.append(DataField)
        
        # correspondance dictionary 
        # this return the DataField in function of its name
        self.Dic[DataField.Name] = DataField
        
        self.IdList.append(DataField.Id)
        self.IdDic[DataField.Name] = DataField.Id
        self.NbData = self.NbData+1

    def Del_DataField(self,DataField):
        '''
        Remove the given DataField from the list.
        '''
        if DataField.Id not in self.IdList:
            print ' Datafield is not in DataList'
        else:
            i = self.IdList.index(DataField.Id)
            del self.List[i]
            del self.Dic[DataField.Name]
            del self.IdList[i]
            del self.IdDic[DataField.Name]
            self.NbData = self.NbData-1
 
    def GetElementById(self, IdIn):
        ''' 
        returns the element of id IdIn.
        '''
        indexElm = self.IdList.index(IdIn)
        return(self.List[indexElm])

    def SetElementById(self, ElmIn, Idin):
        '''
        Set the element ElmIn of id Idin.
        '''
        indexElm = self.IdList.index(IdIn)
        self.List[indexElm] = ElmIn
       
    def GetMaxId(self):
        return(max(self.IdList))

