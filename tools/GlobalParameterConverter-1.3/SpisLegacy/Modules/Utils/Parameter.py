"""
Generic global parameter. Glabal parameters are paremeters NOT specific to
a localisation on the mesh, like the time step or a global temperature of the
system. They can be of all type (float, int, string...) that you whish.

**Project ref:**  Spis/SpisUI

**File name:**    Parameter.py

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

class Parameter:
    '''
    Generic global parameter. Glabal parameters are paremeters NOT specific to 
    a localisation on the mesh, like the time step or a global temperature of the 
    system. They can be of all type (float, int, string...) that you whish. 
    '''
    def __init__(self, ParNum = -1, ParName = None, Descript = None,
                 Val = None):
        self.Id = ParNum
        self.Name = ParName
        self.Description = Descript
        self.Value = Val
        self.Type = 'PARAMETER'

    def Print_Parameter(self):
        print self

    def __str__(self):
        res = 'Parameter Id ',self.Id
        res += 'Parameter Name ',self.Name,
        res += 'Parameter Type ',self.Type
        res += 'Parameter Description ',self.Description
        res += 'Parameter Value ',self.Value
        res += 'Parameter Settings ',self.Settings

    def check_settings():
        if self.Id == -1 or self.Name == None or self.Value == None \
               or self.Description == None:
            return 0
        return 1
