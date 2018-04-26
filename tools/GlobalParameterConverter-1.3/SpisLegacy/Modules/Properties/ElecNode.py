"""
**Module Name:**  ElecNode

**Project ref:**  Spis/SpisUI

**File name:**    ElecNode.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Modules of definition of the struture of the electrical nodes.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Pascal Seng

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

class ElecNode:
    '''
    Data of type ElecNode. The ElecNode are corresponding to a collecting 
    current element for the internal electrical balance of the numerical 
    kernel (i.e SPIS-NUM or PicUp3D).
    '''
    # XXX ElecNum must be set to -1
    def __init__(self, ElecNum = -1, ElecName = None,
                 ElecDescription = None, ElecDataList = None):
        self.Id = ElecNum
        self.Name = ElecName
        self.Description = ElecDescription
        self.DataList = ElecDataList
        self.Type = None

    def Print_ElecNode(self):
        print self

    def __str__(self):
        res = 'ElecNode Id ' + str(self.Id) + os.linesep
        res += 'ElecNode Name ' + str(self.Name) + os.linesep
        res += 'ElecNode Description  ' + str(self.Description) + os.linesep
        res += 'ElecNode Settings ' + str(self.check_settings()) + os.linesep
        if self.DataList is not None:
            for Data in self.DataList.List:
                res += ' Data of Id ' + str(Data.Id) + ', Name ' \
                         + Data.Name + ', and Type ' + Data.Type + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Description == None \
               or self.DataList == None:
            return 0
        return 1
