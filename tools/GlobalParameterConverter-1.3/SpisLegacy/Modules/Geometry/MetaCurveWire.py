"""
**Description:**  This module contains the Parent class MetaCurveWire.

**Project ref:**  Spis

**File name:**    MetaCurveWire.py

:status:          Implemented

**Creation:**     01/07/2003

**Modification:** 02/09/2003  FW(Artenum)  Implementation

:author:          Franck Warmont, Gerard Sookahet

:version:         0.3.0

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
from Modules.Geometry.GeoElement        import GeoElement

class MetaCurveWire(GeoElement):
    '''
    Abstract (Meta) class for wire curve. 
    '''
    def __init__(self, ElmtNum, MetaNum):
        GeoElement.__init__(self, ElmtNum)
        self.MetaId = MetaNum
        self.Connection = []
        self.SurfaceOnWire = []
        self.HoleOnWire = []
        # FIXME: trouver un nom plus explicite
        self.SwapStartEndPointStatus = []

    def Print_Element(self):
        print self

    def __str__(self):
        res = GeoElement.__str__(self)
        res += '    Meta Id ' + str(self.MetaId) + os.linesep
        res += '    Surface On Wire ' + str(self.SurfaceOnWire) + os.linesep
        res += '    Hole On Wire ' + str(self.HoleOnWire) + os.linesep
        res += '    Meta Settings ' + str(self.check_settings()) + os.linesep
        res += '    List of Curves defined ' + os.linesep
        for Curve in self.Connection:
            res += '    Geometrical Element Id ' + str(Curve.Id) \
                   + ' of Type ' + Curve.Type + os.linesep
        return res

    def Check_Wire(self):
        self.WireIsClosed = 0
        PointList = []
        for curve in self.Connection:
            PointList.append(curve.StartPoint)
            PointList.append(curve.EndPoint)
        j = 0
        for i in range(2*len(self.Connection)):
            point = PointList[0]
            del PointList[0]
            if point in PointList:
                j = j+1
        if ((j == len(self.Connection)) and (len(self.Connection) > 0)):
            self.WireIsClosed = 1
            CurveList = [self.Connection[0]]
            SwapList = [self.SwapStartEndPointStatus[0]]
            length = len(self.Connection)-1
            del self.Connection[0]
            del self.SwapStartEndPointStatus[0]
            for i in range(length):
                j = 0
                for curve in self.Connection:
                    Swap = self.SwapStartEndPointStatus[0]
                    if SwapList[len(SwapList)-1] == 1:
                        EndPoint = CurveList[len(CurveList)-1].StartPoint
                    else:
                        EndPoint = CurveList[len(CurveList)-1].EndPoint
                    if ((EndPoint == curve.StartPoint) or (EndPoint == curve.EndPoint)):
                        if EndPoint == curve.EndPoint:
                            Swap = 1
                        break
                    j = j+1
                CurveList.append(curve)
                SwapList.append(Swap)
                if j >= len(self.Connection):
                    j = len(self.Connection)-1
                del self.Connection[j]
                del self.SwapStartEndPointStatus[j]
            self.Connection = CurveList
            self.SwapStartEndPointStatus = SwapList

    def Add_Curve(self,Curve):
        if Curve in self.Connection:
            print 'Curve already in CurveWire'
        elif Curve.check_settings() == 0:
            print ' All Curve settings not yet set'
        else:
            if self.Id is not -1:
                Curve.WireOnCurve.append(self.Id)
            self.Connection.append(Curve)
            self.SwapStartEndPointStatus.append(0)
            self.Check_Wire()

    def Del_Curve(self,curve):
        if curve not in self.Connection:
            print 'Curve is not in CurveWire'
        else:
            if self.Id is not -1:
                i = curve.WireOnCurve.index(self.Id)
                del curve.WireOnCurve[i]
            i = self.Connection.index(curve)
            del self.Connection[i]
            del self.SwapStartEndPointStatus[i]
            self.Check_Wire()
