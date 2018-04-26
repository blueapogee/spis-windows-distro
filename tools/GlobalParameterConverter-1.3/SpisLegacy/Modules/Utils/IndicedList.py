"""
List of DataField.

**Project ref:**  Spis/SpisUI

**File name:**    DataList.py

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Julien Forest                 | Definition/Creation        |
|                | contact@artenum.com           |                            |
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

class IndicedList:
    '''
    Dynamical Indiced List. in such list, elements are selected trhoug an indice
    that can differ from the index. The indice can be re-ordered, non-continious,
    starts from a value different than zero.
    '''
    def __init__(self):
        self.List = []
        self.IdList = []
        self.NbData = 0
        
    def Add(self, Data):
        self.List.append(Data)
        self.IdList.append(Data.Id)
        self.NbData = len(self.List)

    def Del(self,Data):
        if Data.Id not in self.IdList:
            print ' Data is not in DataList'
        else:
            i = self.IdList.index(Data.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbData = len(self.List)
            
    def GetMaxId(self):
        return(max(self.IdList))
   
    def GetElmsByName(self, name):
        """
        Return the list of elements of the name given in input.
        """
        returnList = []
        index = 0
        while(index < len(self.List)):
            try:
                dataName = self.List[index].Name
            except:
                dataName = None
                print "No name found"
                
            if ( dataName == name and dataName != None):
                returnList.append(self.List[index])
            index = index + 1
        return(returnList)