"""
**Description:**  This module contains the class Circle. This Class discribes the
                  geometrical element Circle of the geometrical data structure.

**Project ref:**  Spis/SpisUI

**File name:**    Circle.py

:status:          Implemented

**Creation:**     01/07/2003

**Modification:** 02/09/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+------------------------------+----------------------------+
| Version number | Author (name, e-mail)        | Corrections/Modifications  |
+----------------+------------------------------+----------------------------+
| 0.1.0          | Franck Warmont               | Definition/Creation        |
|                | warmont@artenum.com          |                            |
+----------------+------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet              | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com  | Validation                 |
+----------------+------------------------------+----------------------------+

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

class Circle(MetaCurve):
    def __init__(self, ElmtNum = None, MetaNum = None, CircleNum = None,
                 CPoint = None, SPoint = None, EPoint = None):
        '''
        Default constructor. 
        '''
        if CPoint == None:
            CPoint = Point()
        if SPoint == None:
            SPoint = Point()
        if EPoint == None:
            EPoint = Point()
        MetaCurve.__init__(self, ElmtNum, MetaNum, SPoint, EPoint, EPoint)
        self.CircleId = CircleNum
        self.Center = CPoint
        self.Type = 'CIRCLE'
        self.Check_Circle()

    def Check_Circle(self):
        if not self.Center.check_settings() \
               or not self.StartPoint.check_settings() \
               or not self.EndPoint.check_settings() \
               or self.Center.Coord == self.EndPoint.Coord \
               or self.StartPoint.Coord == self.Center.Coord:
            print ' Degenerated Circle'
            print self.Center

    def Print_Element(self):
        print self

    def __str__(self):
        res = MetaCurve.__str__(self)
        res += '      Circle Id ' + str(self.CircleId) + os.linesep
        res += '      Circle Center Point Id ' + str(self.Center.PointId) \
               + os.linesep
        res += '      Circle Settings ' + str(self.check_settings()) \
               + os.linesep
        return res

    def check_settings(self):
        if self.CircleId == None or self.Center == None:
            return 0
        return MetaCurve.check_settings(self)

