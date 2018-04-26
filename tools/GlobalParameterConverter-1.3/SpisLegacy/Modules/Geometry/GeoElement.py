"""
**Description:**  This module contains the Parent class GeoElement of all
geometrical elements.

**Project ref:**  Spis

**File name:**    GeoElement.py

:status:          Implemented

**Creation:**     01/07/2003

**Modification:** 02/09/2003  FW(Artenum)  Implementation

**References:**

:author:       Franck Warmont, Gerard Sookahet

:version:      0.3.0

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
"""
__docformat__ = "restructuredtext en"

import os

class GeoElement:
    def __init__(self, elmt_id):
        self.Id = elmt_id    # required
        self.UserField = []
        self.Type = "error"

    def Print_Element(self):
        print self

    def __str__(self):
        res = 'Elmt Id ' + str(self.Id) + os.linesep
        res += 'User Field ' + str(self.UserField) + os.linesep
        res += 'Type ' + self.Type + os.linesep
        res += 'Settings ' + str(self.check_settings()) + os.linesep
        return res

    def check_settings(self):
        """Check if the object is complete"""
        if self.Id == None:
            return 0
        return 1
