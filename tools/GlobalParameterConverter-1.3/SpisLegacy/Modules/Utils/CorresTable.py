"""
**Module Name:**  CorresTable

**Project ref:**  Spis/SpisUI

**File name:**    CorresTable.py

:status:          Implemented

**Creation:**     10/11/2005

**Modification:** 22/11/2005  validation

**Use:**

**Description:**  Import a CAD structure from a GEO file into a the Spis CAD structure

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | julien Forest                  | Creation                   |
|                | j.forest@atenum.com            |                            |
+----------------+--------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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



class CorresTable:
        '''
        Manage correspondance table beetween mesh elements.
        '''
        def __init__(self):
            #print "Creation of a correspondance table"
            self.VERBOSE = 0
            self.resetTables()

        def setElmList(self, elmList):
            self.elmList = elmList
                
        def resetTables(self):
            if self.VERBOSE > 0 :
                print "in resetTables"
            self.duplicatedElmList    = []
            self.correspondingElmList = []
            self.elmList = []
            self.compoundTable = []
                
        def buildCompoundTable(self):
            if self.VERBOSE > 0 :
                print "in buildCompoundTable"
            self.compoundTable = []
            for i in range(len(self.duplicatedElmList)):
                self.couple = [self.duplicatedElmList[i], self.correspondingElmList[i]]
                self.compoundTable.append(self.couple)
            print "compount Table built"
                
        def setElmList(self, elmList):
            '''
            Set the mesh element list on which one the correspondance table is based on. 
            '''
            self.elmList = elmList
              
        def addCoupleByIndex(self, indexIn, indexOut):
            
            # Lists of old to new edges for already duplicated edges
            # /!\  Lists of INDEX
            self.duplicatedElmList.append(indexIn)
            self.correspondingElmList.append(indexOut)
            
        def addCoupleByElm(self, elmIn, elmOut):
            
            # Lists of old to new edges for already duplicated edges
            # /!\  Lists of INDEX
            self.duplicatedElmList.append(self.elmList.index(elmIn))
            self.correspondingElmList.append(self.elmList.index(elmOut))

                
        def getNewElmIndex(self, oldElm):
            ''' returns the index of the new elements corresponding to oldElm.'''
            oldElmIndex = self.elmList.index(oldElm)
            indexTemp = self.duplicatedElmList.index(oldElmIndex)
            return(self.correspondingElmList[indexTemp])
                
        def getNewElmIndexByIndex(self, indexOldElm):
            ''' returns the index of the nwem element corresponding to the oldElm
            index indexOldElm.'''
            indexTemp =self.duplicatedElmList.index(indexOldElm)
            return(self.correspondingElmList[indexTemp])
                
        def getNewElmByIndex(self, indexIn):
            indexTemp = self.duplicatedElmList.index(indexIn)
            return(self.elmList[self.correspondingElmList[indexTemp]])
                
        def getNewElm(self, elm):
            oldElmIndex = self.elmList.index(elm)
            return(self.getNewElmByIndex(oldElmIndex))
            
        def getCouple(self, index):
            return(self.duplicatedElmList[index], self.correspondingElmList[index])
                
        def getOldElm(self, newElmIn):
            newElmIndex = self.elmList.index(newElmIn)
            indexTmp = self.correspondingElmList.index(newElmIndex)
            return(self.elmList[self.duplicatedElmList[indexTmp]])
                
        def getOldElmByIndex(self, newElmIndex):
            indexTmp = self.correspondingElmList.index(newElmIndex)
            return(self.elmList[self.duplicatedElmList[indexTmp]])             
            
                
