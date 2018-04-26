"""
**Description:**  This module defines the data structure for the points.

**Project ref:**  Spis/SpisUI

**File name:**    Point.py

:status:          Implemented

**Creation:**     20/07/2003

**Modification:** 01/10/2003  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                 | Definition/Creation        |
|                | Franck.Warmont@artenum.com     |                            |
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
from Modules.Geometry.MetaPoint import MetaPoint

class Point(MetaPoint):
    '''
    Defines the data structure for the GEOM points.
    '''
    def __init__(self, elmt_id = None, meta_id = None, point_id = None,
                 u = None, v = None, w = None):
        MetaPoint.__init__(self, elmt_id, meta_id)
        self.PointId = point_id           # required
        self.Coord   = [u, v, w]          # required
        self.Type = 'POINT'
        self.localResol = None

    def __str__(self):
        res =  MetaPoint.__str__(self)
        res += '     Point Id ' + str(self.PointId) + os.linesep
        res += '     Point Coordinates ' + str(self.Coord[0]) + ", " \
               + str(self.Coord[1]) + ", " + str(self.Coord[2]) + os.linesep
        res += '     Point Settings ' + str(self.check_settings()) + os.linesep
        return res

    def Print_Element(self):
        print self

    def check_settings(self):
        """Check if the object is complete"""
        if self.PointId == None or self.Coord[0] == None \
               or self.Coord[1] == None or self.Coord[2] == None:
            return 0
        return MetaPoint.check_settings(self)
