"""
**Description:**  This module defines the data structure for the abstract meta wires
on surfaces.

**Project ref:**  Spis/SpisUI

**File name:**    MetaSurfaceWire.py

:status:          Implemented

**Creation:**     20/07/2003

**Modification:** 01/10/2003  GR validation

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
from Modules.Geometry.GeoElement import GeoElement

class MetaSurfaceWire(GeoElement):
    '''
    Abstract (Meta) class for GEOM Wire object.
    '''
    def __init__(self, ElmtNum, MetaNum):
        GeoElement.__init__(self, ElmtNum)
        self.MetaId = MetaNum
        self.Connection = []
        self.VolumeOnWire = []
        self.HoleOnWire = []

    def Print_Element(self):
        print self

    def __str__(self):
        res = GeoElement.__str__(self)
        res += '    Volume On Wire ' + str(self.VolumeOnWire) + os.linesep
        res += '    Hole On Wire ' + str(self.HoleOnWire) + os.linesep
        res += '    Meta Id ' + str(self.MetaId) + os.linesep
        res += '    Meta Settings ' + str(self.check_settings()) + os.linesep
        res += '    List of Surfaces defined:' + os.linesep
        for Surface in self.Connection:
            res += '     Geometrical Element Id ' + str(Surface.Id) \
                   + ' of Type ' + Surface.Type + os.linesep

    def check_settings(self):
        """Check if the object is complete"""
        if self.MetaId == None:
            return 0
        return GeoElement.check_settings(self)

    def Check_Wire(self):
        self.WireIsClosed = 0
        CurveList = []
        for Surface in self.Connection:
            for Curve in Surface.WireCurve[0].Connection:
                CurveList.append(Curve)
        length = len(CurveList)
        j = 0
        for i in range(length):
            Curve = CurveList[0]
            del CurveList[0]
            if Curve in CurveList:
                j = j+1
        if ((j == (length/2)) and (len(self.Connection) > 0)):
            self.WireIsClosed = 1

    def Add_Surface(self,Surface):
        if Surface in self.Connection:
            print ' Surface aulready in Wire\n'
        elif Surface.check_settings() == 0:
            print ' All Surface settings not yet set'
        else:
            if self.Id is not -1:
                Surface.WireOnSurface.append(self.Id)
            self.Connection.append(Surface)
            self.Check_Wire()

    def Del_Surface(self,Surface):
        if Surface not in self.Connection:
            print ' Surface is not in Wire\n'
        else:
            if self.Id is not -1:
                i = Surface.WireOnSurface.index(self.Id)
                del Surface.WireOnSurface[i]
            i = self.Connection.index(Surface)
            del self.Connection[i]
            self.Check_Wire()





















