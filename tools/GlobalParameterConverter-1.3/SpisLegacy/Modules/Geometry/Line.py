"""
**Description:**  This module defines the data structure for the Line Object.

**Project ref:**  Spis/SpisUI

**File name:**    Line.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 01/10/2003  GR validation

**Use:**          N/A

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Gerard Sookahet                | Definition/Creation        |
|                | Gerard.Sookahet@artenum.com    |                            |
+----------------+--------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet                | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com    | Validation                 |
+----------------+--------------------------------+----------------------------+

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
from Modules.Geometry.MetaCurve         import MetaCurve
from Modules.Geometry.Point             import Point

class Line(MetaCurve):
    '''
    Defines the data structure for the Line Object.
    '''
    def __init__(self, ElmtNum = None, MetaNum = None, LineNum = None,
                StartPoint = None, EndPoint = None):
        if StartPoint == None:
            StartPoint = Point()
        if EndPoint == None:
            EndPoint = Point()
        MetaCurve.__init__(self, ElmtNum, MetaNum, StartPoint, EndPoint,
                           EndPoint)
        self.LineId = LineNum             # required
        self.Type = 'LINE'
        self.Check_Line()

    def Check_Line(self):
        if self.StartPoint.check_settings() \
               and self.EndPoint.check_settings() \
               and self.StartPoint.Coord == self.EndPoint.Coord:
            print ' Degenerated Line\n'

    def Print_Element(self):
        print self

    def __str__(self):
        res = MetaCurve.__str__(self)
        res += '      Line Id ' + str(self.LineId) + os.linesep
        res += '      Line Settings ' + str(self.check_settings()) + os.linesep
        return res

    def check_settings(self):
        if self.LineId == None:
            return 0
        return MetaCurve.check_settings(self)

