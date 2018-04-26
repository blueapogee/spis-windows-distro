"""
Modules of list of geometrical groups.

**Project ref:**  Spis/SpisUI

**File name:**    GeoGroupList.py

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

class GeoGroupList:
    '''
    List of geo groups.
    '''
    def __init__(self):
        self.List = []
        self.IdList = []
        self.NbGroup = 0

    def Add_Group(self,Group):
        '''
        Adds a new group to the current list of geo groups. 
        this method updates self.List, self.IdList and self.NbGroup 
        members. This method nust be used in state of the append command.
        '''
        self.List.append(Group)
        self.IdList.append(Group.Id)
        self.NbGroup = self.NbGroup+1

    def Del_Group(self,Group):
        '''
        Removes the group given in parameter from the current list.
        This method nust be used in state of the append remove.
        '''
        if Group.Id not in self.IdList:
            print ' Group is not in GeoGroupList'
        else:
            i = self.IdList.index(Group.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbGroup = self.NbGroup-1
            
    def movUpGroup(self, Group):
        indexGrp = self.List.index(Group)
        if indexGrp > 0:
            tmpGrp = self.List[indexGrp-1]
            self.List[indexGrp-1] = self.List[indexGrp]
            self.List[indexGrp] = tmpGrp
            
            tmpGrpId = self.IdList[indexGrp-1]
            self.IdList[indexGrp-1] = self.IdList[indexGrp]
            self.IdList[indexGrp] = tmpGrpId
        
        #print "----"
        #for indexGrp in xrange(len(self.List)):
        #    print self.List[indexGrp].Id, self.IdList[indexGrp]
            
    def movDownGroup(self, Group):
        indexGrp = self.List.index(Group)
        if indexGrp < len(self.List-1):
            tmpGrp = self.List[indexGrp+1]
            self.List[indexGrp+1] = self.List[indexGrp]
            self.List[indexGrp] = tmpGrp     
            
            tmpGrpId = self.IdList[indexGrp-1]
            self.IdList[indexGrp-1] = self.IdList[indexGrp]
            self.IdList[indexGrp] = tmpGrpId
        
        #print "----"
        #for indexGrp in xrange(len(self.List)):
        #    print self.List[indexGrp].Id, self.IdList[indexGrp]
    
    def movUpGroupFromIndex(self, indexGrp):
        if indexGrp > 0:
            tmpGrp = self.List[indexGrp-1]
            self.List[indexGrp-1] = self.List[indexGrp]
            self.List[indexGrp] = tmpGrp
            
            tmpGrpId = self.IdList[indexGrp-1]
            self.IdList[indexGrp-1] = self.IdList[indexGrp]
            self.IdList[indexGrp] = tmpGrpId
        
        #print "----"
        #for indexGrp in xrange(len(self.List)):
        #    print self.List[indexGrp].Id, self.IdList[indexGrp]
            
            
    def movDownGroupFromIndex(self, indexGrp):
        print "index", indexGrp
        if indexGrp+1 < (len(self.List)):
            tmpGrp = self.List[indexGrp+1]
            self.List[indexGrp+1] = self.List[indexGrp]
            self.List[indexGrp] = tmpGrp
            
            tmpGrpId = self.IdList[indexGrp+1]
            self.IdList[indexGrp+1] = self.IdList[indexGrp]
            self.IdList[indexGrp] = tmpGrpId
        
        #print "----"
        #for indexGrp in xrange(len(self.List)):
        #    print self.List[indexGrp].Id, self.IdList[indexGrp]
            
    def GetElmById(self, IdIn):
        try:
            return self.List[self.IdList.index(IdIn)]
        except:
            return None
