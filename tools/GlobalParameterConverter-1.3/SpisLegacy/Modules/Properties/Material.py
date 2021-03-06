"""
Modules of definition of material properties.

**Project ref:**  Spis/SpisUI

**File name:**    Material.py

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Julien Forest

:version:      2.0.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                | Definition/Creation        |
|                | Franck Warmont@artenum.com    |                            |
+----------------+-------------------------------+----------------------------+
| 2.0.0          | Julien Forest                 | Re-writting, extension &   |
|                | contact@artenum.com           | Validation                 |
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

class Material:
    '''
    Generic material descriptor. Such type of Material is used to describe the 
    surface and material properties, like conductivity, for instance. 
    Please see the SPIS User Manual for further information.
    '''
    LEGACY_MATERIAL = "legacy"
    NASCAP_LEGACY_MATERIAL = "nascap.legacy.material"
    NASCAP_MATERIAL = NASCAP_LEGACY_MATERIAL
    NASCAP_2K_MATERIAL = "nascap.2k.material"
    EXTENDED_NASCAP_2K_MATERIAL = "extended.nascap.2k.material"

    def __init__(self, MatNum = -1, MatName = None, MatDescription = None, MatDataList = None, NascapDataList = None):
        self.Id = MatNum
        self.Name = MatName
        self.Description = MatDescription
        self.DataList = MatDataList
        self.Color = None
        self.Type = None
        self.NascapDataList = NascapDataList


    def __str__(self):
        res = 'Material Id ' + str(self.Id) + os.linesep
        res += 'Material Name ' + self.Name + os.linesep
        res += 'Material Description ' + str(self.Description) + os.linesep
        res += 'Material Settings ' + str(self.check_settings()) + os.linesep
        if self.DataList is not None:
            for Data in self.DataList.List:
                res += ' Data of Id ' + str(Data.Id) + ', Name ' + Data.Name \
                       + ', Type ' + Data.Type + ' and Value ' \
                       + str(Data.Value) + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Description == None \
               or self.DataList == None:
            return 0
        return 1

    def PrintMaterial(self):
        print self.Id
        print self.Name 
        print self.Description 
	#for Data in self.DataList.List:
	#        print self.DataList[Data] 

