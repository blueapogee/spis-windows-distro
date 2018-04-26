"""
Data of type Plasma. Such Data describe thei numerical piroperties of
the plasma model, which means the Initial and Boundries Conditions (IBC).
Their description depends on the Numerical Model (NM). Please see the
SPIS-NUM or the PicUp3D documentation for further informations.

**Project ref:**  Spis/SpisUI

**File name:**    Plasma.py

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

import os
from Modules.Properties.DataList import DataList

class Plasma:
    '''
    Data of type Plasma. Such Data describe the numerical properties of 
    the plasma model, which means the Initial and Boundries Conditions (IBC). 
    Their description depends on the Numerical Model (NM). Please see the 
    SPIS-NUM or the PicUp3D documentation for further informations. 
    '''
    def __init__(self, IdIn = -1, NameIn = None, DescriptionIn = None,
                     DataListIn = None):
        self.Id = IdIn
        self.Name = NameIn
        self.Description = DescriptionIn
        if DataListIn != None:
            self.DataList = DataListIn
        else:
            self.DataList = DataList()
        self.DataId = 1
        self.Type = None

        
    def AddData(self, DataIn):
        '''
        Add a data into the DataList of the plasma object.
        '''
        self.DataList.Add(DataIn)
        self.DataId = self.DataId+1
        
    def PrintDataList(self):
        for elm in self.DataList:
            print elm

    def __str__(self):
        '''
        print all informations relative to the plasma.
        '''
        res = 'Plasma Id ' + str(self.Id) + os.linesep
        res += 'Plasma Name ' + str(self.Name) + os.linesep
        res += 'Plasma Description  ' + str(self.Description) + os.linesep
        res += 'Plasma Settings ' + str(self.check_settings()) + os.linesep
        #if self.DataList is not None:
        #    for Data in self.DataList.List:
        #        res += ' Data of Id ' + Data.Id + ', Name ' + Data.Name \
        #               + ', and Type ' + Data.Type + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Description == None \
               or self.DataList == None:
            return 0
        return 1
