
"""
**File name:**    GmshGeoConverters.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**
+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 3.1.0   | Yves Le Rumeur                       | Modif                      |
|         | lerumeur@artenum.com                 |                            |
+---------+--------------------------------------+----------------------------+

PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

import os
import string

from Modules.Utils.ObjectList           import ObjectList
from Modules.Utils.ParameterList        import ParameterList
from Modules.Geometry.GeoElementList    import GeoElementList
from Modules.Geometry.Point             import Point
from Modules.Geometry.Circle            import Circle
from Modules.Geometry.Ellipse           import Ellipse
from Modules.Geometry.Line              import Line
from Modules.Geometry.CurveWire         import CurveWire
from Modules.Geometry.RuledSurface      import RuledSurface
from Modules.Geometry.PlaneSurface      import PlaneSurface
from Modules.Geometry.SurfaceWire       import SurfaceWire
from Modules.Geometry.Volume            import Volume
from Modules.Groups.GeoGroupList        import GeoGroupList
from Modules.Groups.GeoGroup            import GeoGroup

class GmshGeoConverters:
    def __init__(self):
        self.ObjectNumber = 0
        self.ParameterNumber = 0
        self.GeoElementNumber = 0
        self.GroupNumber = 0
        self.MetaPointNumber = 0
        self.PointNumber = 0
        self.MetaCurveNumber = 0
        self.LineNumber = 0
        self.LineCounter = 0
        self.CircleNumber = 0
        self.EllipseNumber = 0
        self.MetaWireCurveNumber = 0
        self.WireCurveNumber = 0
        self.MetaSurfaceNumber = 0
        self.PlaneSurfaceNumber = 0
        self.RuledSurfaceNumber = 0
        self.MetaWireSurfaceNumber = 0
        self.WireSurfaceNumber = 0
        self.MetaVolumeNumber = 0
        self.VolumeNumber = 0

        self.MetaPointIdList = {}
        self.MetaCurveIdList = {}
        self.MetaWireCurveIdList =  {}
        self.MetaSurfaceIdList = {}
        self.MetaWireSurfaceIdList =  {}
        self.MetaVolumeIdList = {}

        self.PointGroupIdList = {}
        self.CurveGroupIdList = {}
        self.SurfaceGroupIdList = {}
        self.VolumeGroupIdList = {}
        self.ParameterIdList = {}

        self.Field = []
        self.ListOfObject = ObjectList()
        self.ListOfGeoElement = GeoElementList()
        self.ListOfGeoGroup = GeoGroupList()
        self.ListOfParameter = ParameterList()
        self.ListOfOldElmtNum = []
        self.ListOfNewElmtNum = []
        self.ListOfOldGrpNum = []
        self.ListOfNewGrpNum = []

        self.PhysicalPoint = GeoGroup()
        self.PhysicalCurve = GeoGroup()
        self.PhysicalSurface = GeoGroup()
        self.PhysicalVolume = GeoGroup()

    def Init_defaultPhysical(self):
        ListOfElmt1 = GeoElementList()
        ListOfElmt2 = GeoElementList()
        ListOfElmt3 = GeoElementList()
        ListOfElmt4 = GeoElementList()
        self.PhysicalPoint.Name = 'DEFAULT POINT GROUP'
        self.PhysicalPoint.Type = 'POINT GROUP'
        self.PhysicalPoint.Description = 'POINT'
        self.PhysicalPoint.ElementList = ListOfElmt1
        self.PhysicalCurve.Name = 'DEFAULT CURVE GROUP'
        self.PhysicalCurve.Type = 'CURVE GROUP'
        self.PhysicalCurve.Description = 'CURVE'
        self.PhysicalCurve.ElementList = ListOfElmt2
        self.PhysicalSurface.Name = 'DEFAULT SURFACE GROUP'
        self.PhysicalSurface.Type = 'SURFACE GROUP'
        self.PhysicalSurface.Description = 'SURFACE'
        self.PhysicalSurface.ElementList = ListOfElmt3
        self.PhysicalVolume.Name = 'DEFAULT VOLUME GROUP'
        self.PhysicalVolume.Type = 'VOLUME GROUP'
        self.PhysicalVolume.Description = 'VOLUME'
        self.PhysicalVolume.ElementList = ListOfElmt4

    def Save_DefaultPhysical(self):
        if len(self.PhysicalPoint.ElementList.List) > 0:
            self.GroupNumber = self.GroupNumber+1
            self.PhysicalPoint.Id =  self.GroupNumber
            self.ListOfObject.Add_Object(self.PhysicalPoint)
            self.ListOfGeoGroup.Add_Group(self.PhysicalPoint)
            self.ListOfNewGrpNum.append(self.GroupNumber)
            if len(self.ListOfOldGrpNum) > 0:
                self.ListOfOldGrpNum.append(max(self.ListOfOldGrpNum)+1)
            else:
                self.ListOfOldGrpNum.append(self.GroupNumber)
        if len(self.PhysicalCurve.ElementList.List) > 0:
            self.GroupNumber = self.GroupNumber+1
            self.PhysicalCurve.Id = self.GroupNumber
            self.ListOfObject.Add_Object(self.PhysicalCurve)
            self.ListOfGeoGroup.Add_Group(self.PhysicalCurve)
            self.ListOfNewGrpNum.append(self.GroupNumber)
            if len(self.ListOfOldGrpNum) > 0:
                self.ListOfOldGrpNum.append(max(self.ListOfOldGrpNum)+1)
            else:
                self.ListOfOldGrpNum.append(self.GroupNumber)
        if len(self.PhysicalSurface.ElementList.List) > 0:
            self.GroupNumber = self.GroupNumber+1
            self.PhysicalSurface.Id = self.GroupNumber
            self.ListOfObject.Add_Object(self.PhysicalSurface)
            self.ListOfGeoGroup.Add_Group(self.PhysicalSurface)
            self.ListOfNewGrpNum.append(self.GroupNumber)
            if len(self.ListOfOldGrpNum) > 0:
                self.ListOfOldGrpNum.append(max(self.ListOfOldGrpNum)+1)
            else:
                self.ListOfOldGrpNum.append(self.GroupNumber)
        if len(self.PhysicalVolume.ElementList.List) > 0:
            self.GroupNumber = self.GroupNumber+1
            self.PhysicalVolume.Id = self.GroupNumber
            self.ListOfObject.Add_Object(self.PhysicalVolume)
            self.ListOfGeoGroup.Add_Group(self.PhysicalVolume)
            self.ListOfNewGrpNum.append(self.GroupNumber)
            if len(self.ListOfOldGrpNum) > 0:
                self.ListOfOldGrpNum.append(max(self.ListOfOldGrpNum)+1)
            else:
                self.ListOfOldGrpNum.append(self.GroupNumber)

    def ConvertPlane(self):
        print "Planes are not supported"

    def ConvertPoint(self):
        self.MetaPointNumber = self.MetaPointNumber+1
        self.GeoElementNumber = self.GeoElementNumber+1
        self.PointNumber = self.PointNumber+1
        self.MetaPointIdList[self.Field[1]] = self.ObjectNumber-1
        GeoElement = Point(self.GeoElementNumber, self.MetaPointNumber,
                           self.PointNumber, self.Field[2], self.Field[3],
                           self.Field[4])
        GeoElement.UserField.append(self.Field[5])
        self.PhysicalPoint.ElementList.Add_Element(GeoElement)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertLine(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaCurveNumber = self.MetaCurveNumber+1
        self.LineNumber = self.LineNumber+1
        self.MetaCurveIdList[self.Field[1]] = self.ObjectNumber-1
        i = self.MetaPointIdList[self.Field[2]]
        point1 = self.ListOfObject.List[i]
        i = self.MetaPointIdList[self.Field[3]]
        point2 = self.ListOfObject.List[i]
        GeoElement = Line(self.GeoElementNumber,self.MetaCurveNumber,
                          self.LineNumber,point1,point2)
        self.PhysicalCurve.ElementList.Add_Element(GeoElement)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertCircle(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaCurveNumber = self.MetaCurveNumber+1
        self.CircleNumber = self.CircleNumber+1
        self.MetaCurveIdList[self.Field[1]] = self.ObjectNumber-1
        i = self.MetaPointIdList[self.Field[2]]
        point2 = self.ListOfObject.List[i]
        i = self.MetaPointIdList[self.Field[3]]
        point1 = self.ListOfObject.List[i]
        i = self.MetaPointIdList[self.Field[4]]
        point3 = self.ListOfObject.List[i]
        GeoElement = Circle(self.GeoElementNumber, self.MetaCurveNumber,
                            self.CircleNumber, point1, point2, point3)
        self.PhysicalCurve.ElementList.Add_Element(GeoElement)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertEllipse(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaCurveNumber = self.MetaCurveNumber+1
        self.EllipseNumber = self.EllipseNumber+1
        self.MetaCurveIdList[self.Field[1]] = self.ObjectNumber-1
        i = self.MetaPointIdList[self.Field[2]]
        point3 = self.ListOfObject.List[i]
        i = self.MetaPointIdList[self.Field[3]]
        point1 = self.ListOfObject.List[i]
        i = self.MetaPointIdList[self.Field[4]]
        point2 = self.ListOfObject.List[i]
        i = self.MetaPointIdList[self.Field[5]]
        point4 = self.ListOfObject.List[i]
        GeoElement = Ellipse(self.GeoElementNumber,self.MetaCurveNumber,
                             self.CircleNumber,point1,point2,point3,point4)
        self.PhysicalCurve.ElementList.Add_Element(GeoElement)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertCurveLoop(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaWireCurveNumber = self.MetaWireCurveNumber+1
        self.WireCurveNumber = self.WireCurveNumber+1
        self.MetaWireCurveIdList[self.Field[1]] = self.ObjectNumber-1
        GeoElement = CurveWire(self.GeoElementNumber,
                               self.MetaWireCurveNumber,
                               self.WireCurveNumber)
        for CurveId in self.Field[2:]:
            i = self.MetaCurveIdList[abs(CurveId)]
            Curve = self.ListOfObject.List[i]
            GeoElement.Add_Curve(Curve)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertSurfaceLoop(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaWireSurfaceNumber = self.MetaWireSurfaceNumber+1
        self.WireSurfaceNumber = self.WireSurfaceNumber+1
        self.MetaWireSurfaceIdList[self.Field[1]] = self.ObjectNumber-1
        GeoElement = SurfaceWire(self.GeoElementNumber,
                                 self.MetaWireSurfaceNumber,
                                 self.WireSurfaceNumber)
        for SurfaceId in self.Field[2:]:
            i = self.MetaSurfaceIdList[abs(SurfaceId)]
            Surface = self.ListOfObject.List[i]
            GeoElement.Add_Surface(Surface)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertSurface(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaSurfaceNumber = self.MetaSurfaceNumber+1
        self.MetaSurfaceIdList[self.Field[1]] = self.ObjectNumber-1
        if self.Field[0] == 'Plane Surface':
            self.PlaneSurfaceNumber = self.PlaneSurfaceNumber+1
            GeoElement = PlaneSurface(self.GeoElementNumber,
                                      self.MetaSurfaceNumber,
                                      self.PlaneSurfaceNumber)
        else:
            self.RuledSurfaceNumber = self.RuledSurfaceNumber+1
            GeoElement = RuledSurface(self.GeoElementNumber,
                                      self.MetaSurfaceNumber,
                                      self.RuledSurfaceNumber)
        GeoElement.Create_ExternalWire(
            self.ListOfObject.List[self.MetaWireCurveIdList[self.Field[2]]])
        for WireId in self.Field[3:]:
            GeoElement.Add_Hole(
                self.ListOfObject.List[self.MetaWireCurveIdList[WireId]])
        self.PhysicalSurface.ElementList.Add_Element(GeoElement)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertVolume(self):
        self.GeoElementNumber = self.GeoElementNumber+1
        self.MetaVolumeNumber = self.MetaVolumeNumber+1
        self.MetaVolumeIdList[self.Field[1]] = self.ObjectNumber-1
        self.VolumeNumber = self.VolumeNumber+1
        GeoElement = Volume(self.GeoElementNumber,
                            self.MetaVolumeNumber,
                            self.VolumeNumber)
        GeoElement.Create_ExternalWire(self.ListOfObject.List[ \
            self.MetaWireSurfaceIdList[self.Field[2]]])
        for WireId in self.Field[3:]:
            GeoElement.Add_Hole(self.ListOfObject.List[ \
                self.MetaWireSurfaceIdList[WireId]])
        self.PhysicalVolume.ElementList.Add_Element(GeoElement)
        self.ListOfObject.Add_Object(GeoElement)
        self.ListOfGeoElement.Add_Element(GeoElement)
        self.ListOfNewElmtNum.append(self.GeoElementNumber)
        self.ListOfOldElmtNum.append(self.Field[1])

    def ConvertPhysicalPoint(self):
        ListOfElmt = GeoElementList()
        for number in self.Field[2:]:
            if self.MetaPointIdList.has_key(number):
                GeoElement = self.ListOfObject.List[\
                    self.MetaPointIdList[number]]
                ListOfElmt.Add_Element(GeoElement)
                self.PhysicalPoint.ElementList.Del_Element(GeoElement)
            else:
                print 'The GeoElement of the Group GeoElementList \
                is not in the Geometrical Data Structure'
        self.GroupNumber = self.GroupNumber+1
        self.PointGroupIdList[self.Field[1]] = self.ObjectNumber-1
        Group = GeoGroup()
        Group.Id = self.Field[1] #self.GroupNumber
        Group.Name = 'POINT GROUP(' + str(self.Field[1]) + ')'  #'POINT GROUP(' + str(self.GroupNumber) + ')'
        Group.Type = 'POINT GROUP'
        Group.Description = 'POINT'
        Group.ElementList = ListOfElmt
        self.ListOfObject.Add_Object(Group)
        self.ListOfGeoGroup.Add_Group(Group)
        self.ListOfNewGrpNum.append(self.GroupNumber)
        self.ListOfOldGrpNum.append(self.Field[1])

    def ConvertPhysicalCurve(self):
        ListOfElmt = GeoElementList()
        for number in self.Field[2:]:
            if self.MetaCurveIdList.has_key(number):
                GeoElement = self.ListOfObject.List[\
                    self.MetaCurveIdList[number]]
                ListOfElmt.Add_Element(GeoElement)
                self.PhysicalCurve.ElementList.Del_Element(GeoElement)
            else:
                print 'The GeoElement of the Group GeoElementList \
                is not in the Geometrical Data Structure'
        self.GroupNumber = self.GroupNumber+1
        self.CurveGroupIdList[self.Field[1]] = self.ObjectNumber-1
        Group = GeoGroup()
        Group.Id = self.Field[1] #self.GroupNumber
        Group.Name = 'CURVE GROUP(' + str(self.Field[1]) + ')' #'CURVE GROUP(' + str(self.GroupNumber) + ')'
        Group.Type = 'CURVE GROUP'
        Group.Description = 'CURVE'
        Group.ElementList = ListOfElmt
        self.ListOfObject.Add_Object(Group)
        self.ListOfGeoGroup.Add_Group(Group)
        self.ListOfNewGrpNum.append(self.GroupNumber)
        self.ListOfOldGrpNum.append(self.Field[1])

    def ConvertPhysicalSurface(self):
        ListOfElmt = GeoElementList()
        for number in self.Field[2:]:
            if self.MetaSurfaceIdList.has_key(number):
                GeoElement = self.ListOfObject.List[\
                    self.MetaSurfaceIdList[number]]
                ListOfElmt.Add_Element(GeoElement)
                self.PhysicalSurface.ElementList.Del_Element(GeoElement)
            else:
                print 'The GeoElement of the Group GeoElementList \
                is not in the Geometrical Data Structure'
        self.GroupNumber = self.GroupNumber+1
        self.SurfaceGroupIdList[self.Field[1]] = self.ObjectNumber-1
        Group = GeoGroup()
        Group.Id = self.Field[1] #self.GroupNumber
        Group.Name = 'SURFACE GROUP(' + str(self.Field[1]) + ')' #'SURFACE GROUP(' + str(self.GroupNumber) + ')'
        Group.Type = 'SURFACE GROUP'
        Group.Description = 'SURFACE'
        Group.ElementList = ListOfElmt
        self.ListOfObject.Add_Object(Group)
        self.ListOfGeoGroup.Add_Group(Group)
        self.ListOfNewGrpNum.append(self.GroupNumber)
        self.ListOfOldGrpNum.append(self.Field[1])

    def ConvertPhysicalVolume(self):
        ListOfElmt = GeoElementList()
        for number in self.Field[2:]:
            if self.MetaVolumeIdList.has_key(number):
                GeoElement = self.ListOfObject.List[\
                    self.MetaVolumeIdList[number]]
                ListOfElmt.Add_Element(GeoElement)
                self.PhysicalVolume.ElementList.Del_Element(GeoElement)
            else:
                print 'The GeoElement of the Group GeoElementList \
                is not in the Geometrical Data Structure'
        self.GroupNumber = self.GroupNumber+1
        self.VolumeGroupIdList[self.Field[1]] = self.ObjectNumber-1
        Group = GeoGroup()
        Group.Id = self.Field[1] #self.GroupNumber
        print "ConvertPhysicalVolume GrpIp", Group.Id
        Group.Name = 'VOLUME GROUP(' + str(self.Field[1]) + ')' #'VOLUME GROUP(' + str(self.GroupNumber) + ')'
        Group.Type = 'VOLUME GROUP'
        Group.Description = 'VOLUME'
        Group.ElementList = ListOfElmt
        self.ListOfObject.Add_Object(Group)
        self.ListOfGeoGroup.Add_Group(Group)
        self.ListOfNewGrpNum.append(self.GroupNumber)
        self.ListOfOldGrpNum.append(self.Field[1])

    def ConvertParameter(self):
        self.ParameterNumber = self.ParameterNumber+1
        self.ParameterIdList[self.LineCounter] = self.ObjectNumber-1
        Param = Parameter.Parameter(self.ParameterNumber,self.Field[1],
                                    'CHARACTERISTIC LENGTH',self.Field[2])
        self.ListOfObject.Add_Object(Param)
        self.ListOfParameter.Add_Parameter(Param)
