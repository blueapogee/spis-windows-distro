"""
**Description:**  This module defines the data structure for the abstrct metasurfaces.

**Project ref:**  Spis/SpisUI

**File name:**    MetaSurface.py

:status:          Implemented

**Creation:**     20/07/2003

**Modification:** 01/10/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------------+----------------------------+
| Version number | Author (name, e-mail)           | Corrections/Modifications  |
+----------------+---------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                  | Definition/Creation        |
|                | Franck.Warmont@artenum.com      |                            |
+----------------+---------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet                 | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com     | Validation                 |
+----------------+---------------------------------+----------------------------+

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

class MetaSurface(GeoElement):
    '''
    Abstract (Meta) class for GEOM Node object.
    '''
    def __init__(self, ElmtNum, MetaNum):
        GeoElement.__init__(self, ElmtNum)
        self.WireOnSurface = []
        self.WireCurve = []
        self.MetaId = MetaNum

    def Print_Element(self):
        print self

    def __str__(self):
        res = GeoElement.__str__(self)
        res += '    Meta Id ' + str(self.MetaId) + os.linesep
        res += '    Wire On Surface ' + str(self.WireOnSurface) + os.linesep
        res += '    Meta Settings' + str(self.check_settings()) + os.linesep
        res += '    List of Curve Wires defined' + os.linesep
        for Wire in self.WireCurve:
            res += '     Geometrical Element Id ' + str(Wire.Id) \
                   + ' of Type ' + Wire.Type + os.linesep
        return res

    def check_settings(self):
        """Check if the object is complete"""
        if self.MetaId == None:
            return 0
        return GeoElement.check_settings(self)

    def Add_Hole(self,Wire):
        if Wire == self.WireCurve[0]:
            print ' HoleWire must be different from principal Wire\n'
        elif len(self.WireCurve) == 0:
            print ' Add the principal CurveWire before the Hole\n'
        elif Wire in self.WireCurve[1:]:
            print ' Wire already used as hole'
        elif Wire.Check_Settings() == 0:
            print ' All Settings must be set to use Wire as hole'
        else:
            if self.Id is not -1:
                Wire.HoleOnWire.append(self.Id)
            self.WireCurve.append(Wire)

    def Create_ExternalWire(self,Wire):
        if len(self.WireCurve) > 0:
            print ' Wire already created, use Change_ExternalWire(Wire) function'
        else:
            if self.Id is not -1:
                Wire.SurfaceOnWire.append(self.Id)
            self.WireCurve.append(Wire)

    def Change_ExternalWire(self,Wire):
        if len(self.WireCurve) == 0:
            print ' External Wire not yet created\n'
        elif Wire.Check_Settings == 0:
            print ' Wire with the Element Id',Wire.Get_Id(),'not yet totally Set\n'
        else:
            if self.Id is not -1:
                i = self.CurveWire[0].SurfaceOnWire.index(self.Id)
                del self.CurveWire[0].SurfaceOnWire[i]
                Wire.SurfaceOnWire.append(self.Id)
            self.WireCurve[0] = Wire
