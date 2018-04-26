"""
**Module Name:**  Data

**Project ref:**  Spis/SpisUI

**File name:**    Data.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:** .

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

class Data:
    def __init__(self, DId = None, DName = None, DType = None,
                 DDescription = None, DUnit = None, DLocal = None,
                 DValue = None, DLockedValue = None):
        self.Id = DId
        self.Name = DName
        self.Type = DType
        self.Description = DDescription
        self.Unit = DUnit
        self.Local = DLocal
        self.Value = DValue
        self.LockedValue = DLockedValue

    def __str__(self):
        res = 'Data Id ' + str(self.Id) + os.linesep
        res += 'Data Name ' + self.Name + os.linesep
        res += 'Data Type ' + self.Type + os.linesep
        res += 'Data Description ' + self.Description + os.linesep
        res += 'Data Unit ' + str(self.Unit) + os.linesep
        res += 'Data Local ' + str(self.Local) + os.linesep
        if (self.Local is 1):
            res += 'Data on Mesh Nodes' + os.linesep
        if (self.Local is 2):
            res += 'Data on Mesh Edges' + os.linesep
        if (self.Local is 3):
            res += 'Data on Mesh Facets' + os.linesep
        if (self.Local is 4):
            res += 'Data on Mesh Cells' + os.linesep
        res += 'Data Value ' + str(self.Value) + os.linesep
        res += 'Data LockedValue ' + str(self.LockedValue) + os.linesep
        res += 'Data Settings ' + str(self.check_settings()) + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Type == None \
               or self.Description == None or self.Unit == None \
               or self.Local == None or self.Value == None \
               or self.LockedValue == None:
            return 0
        return 1
