"""
**Description:**  This module contains the class GeoElementList. This class
discribes necessary attributes and method to save GeoElement objects in a list.

**Project ref:**  Spis

**File name:**    GeoElementList.py

:status:          Implemented

**Creation:**     01/07/2003

**Modification:** 02/09/2003  FW(Artenum)  Implementation

**References:**   Not Applicable

:author:          Franck Warmont, Gerard Sookahet

:version:         0.2.0

**Versions and anomalies correction :**

+----------------+-----------------------+----------------------------+
| Version number | Author (name, e-mail) | Corrections/Modifications  |
+----------------+-----------------------+----------------------------+
| 0.1.0          | Franck Warmont        | Creation                   |
|                | warmont@artenum.com   |                            |
+----------------+-----------------------+----------------------------+
| 0.2.0          | Gerard Sookahet       | Verification/extension/    |
|                | sookahet@artenum.com  | Validation                 |
+----------------+-----------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000, Paris, France, `http://www.artenum.com`_

.. _`http://www.artenum.com`: http://www.artenum.com
"""
__docformat__ = "restructuredtext en"

# epydoc --html --docformat restructuredtext class.py

class GeoElementList:
    '''
    General list of GeoElement. Such type of list gathers GeoElements
    in an indexed list and offers various accessors. 
    '''
    def __init__(self):
        """
        Defautl constructor. 
        """
        self.List = []
        self.IdList = []
        self.NbElement = 0

    def Add_Element(self, GeoElement):
        '''
        Add a new element to the list.
        '''
        self.List.append(GeoElement)
        self.IdList.append(GeoElement.Id)
        self.NbElement = self.NbElement + 1

    def Del_Element(self, GeoElement):
        '''
        Remove the givene element. 
        '''
        if GeoElement.Id not in self.IdList:
            print ' GeoElement is not in GeoElementList'
        else:
            i = self.IdList.index(GeoElement.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbElement = self.NbElement-1
            
    def GetElmById(self, IdIn):
        '''
        Returns an element according its Id. 
        '''
        try:
            return self.List[self.IdList.index(IdIn)]
        except:
            return None
            
    def rebuildConnectivityFrom(self, geoElmListIn):
        self.List = []
        for Id in self.IdList:
             self.List.append(geoElmListIn.GetElmById(Id))


