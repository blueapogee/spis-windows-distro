"""
**Module Name:**  Gmsh2GeoStruct

**Project ref:**  Spis/SpisUI

**File name:**    Gmsh2GeoStruct.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:** Module of conversion from the geo Gmsh CAD format to the
geometric structure.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet, Pascal Seng

:version:      0.3.0

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
| 0.3.0          | Pascal Seng                   | Extension                  |
|                | Pascal.Seng@artenum.com       |                            |
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

ObjectNumber = 0
ParameterNumber = 0
GeoElementNumber = 0
GroupNumber = 0
MetaPointNumber = 0
PointNumber = 0
MetaCurveNumber = 0
LineNumber = 0
LineCounter = 0
CircleNumber = 0
EllipseNumber = 0
MetaWireCurveNumber = 0
WireCurveNumber = 0
MetaSurfaceNumber = 0
PlaneSurfaceNumber = 0
RuledSurfaceNumber = 0
MetaWireSurfaceNumber = 0
WireSurfaceNumber = 0
MetaVolumeNumber = 0
VolumeNumber = 0

MetaPointIdList = {}
MetaCurveIdList = {}
MetaWireCurveIdList =  {}
MetaSurfaceIdList = {}
MetaWireSurfaceIdList =  {}
MetaVolumeIdList = {}

PointGroupIdList = {}
CurveGroupIdList = {}
SurfaceGroupIdList = {}
VolumeGroupIdList = {}
ParameterIdList = {}

print "start importing"
Field = []
ListOfObject = ObjectList()
print "importing Geo elements"
ListOfGeoElement = GeoElementList()
print "importing group (physical) list"
ListOfGeoGroup = GeoGroupList()
print "importing parameters list"
ListOfParameter = ParameterList()
ListOfOldElmtNum = []
ListOfNewElmtNum = []
ListOfOldGrpNum = []
ListOfNewGrpNum = []

FileIn = None

PhysicalPoint = GeoGroup()
PhysicalCurve = GeoGroup()
PhysicalSurface = GeoGroup()
PhysicalVolume = GeoGroup()

def Reset_Variables():
   global ObjectNumber,ParameterNumber,GeoElementNumber,GroupNumber,MetaPointNumber,PointNumber,MetaCurveNumber,LineNumber,LineCounter,CircleNumber,EllipseNumber,MetaWireCurveNumber,WireCurveNumber,MetaSurfaceNumber,PlaneSurfaceNumber,RuledSurfaceNumber,MetaWireSurfaceNumber,WireSurfaceNumber,MetaVolumeNumber,VolumeNumber,MetaPointIdList,MetaCurveIdList,MetaWireCurveIdList,MetaSurfaceIdList,MetaWireSurfaceIdList,MetaVolumeIdList,PointGroupIdList,CurveGroupIdList,SurfaceGroupIdList,VolumeGroupIdList,ParameterIdList,Field,ListOfObject,ListOfGeoElement,ListOfGeoGroup,ListOfParameter,ListOfOldElmtNum,ListOfNewElmtNum,ListOfOldGrpNum,ListOfNewGrpNum,PhysicalPoint,PhysicalCurve,PhysicalSurface,PhysicalVolume
   ObjectNumber = 0
   ParameterNumber = 0
   GeoElementNumber = 0
   GroupNumber = 0
   MetaPointNumber = 0
   PointNumber = 0
   MetaCurveNumber = 0
   LineNumber = 0
   CircleNumber = 0
   EllipseNumber = 0
   MetaWireCurveNumber = 0
   WireCurveNumber = 0
   MetaSurfaceNumber = 0
   PlaneSurfaceNumber = 0
   RuledSurfaceNumber = 0
   MetaWireSurfaceNumber = 0
   WireSurfaceNumber = 0
   MetaVolumeNumber = 0
   VolumeNumber = 0

   MetaPointIdList = {}
   MetaCurveIdList = {}
   MetaWireCurveIdList =  {}
   MetaSurfaceIdList = {}
   MetaWireSurfaceIdList =  {}
   MetaVolumeIdList = {}

   PointGroupIdList = {}
   CurveGroupIdList = {}
   SurfaceGroupIdList = {}
   VolumeGroupIdList = {}
   ParameterIdList = {}

   Field = []
   ListOfObject = ObjectList()
   ListOfGeoElement = GeoElementList()
   ListOfGeoGroup = GeoGroupList()
   ListOfParameter = ParameterList()
   ListOfOldElmtNum = []
   ListOfNewElmtNum = []
   ListOfOldGrpNum = []
   ListOfNewGrpNum = []

   PhysicalPoint = GeoGroup()
   PhysicalCurve = GeoGroup()
   PhysicalSurface = GeoGroup()
   PhysicalVolume = GeoGroup()

def Init_defaultPhysical():
   global PhysicalPoint,PhysicalCurve,PhysicalSurface,PhysicalVolume
   ListOfElmt1 = GeoElementList()
   ListOfElmt2 = GeoElementList()
   ListOfElmt3 = GeoElementList()
   ListOfElmt4 = GeoElementList()
   PhysicalPoint.Name = 'DEFAULT POINT GROUP'
   PhysicalPoint.Type = 'POINT GROUP'
   PhysicalPoint.Description = 'POINT'
   PhysicalPoint.ElementList = ListOfElmt1
   PhysicalCurve.Name = 'DEFAULT CURVE GROUP'
   PhysicalCurve.Type = 'CURVE GROUP'
   PhysicalCurve.Description = 'CURVE'
   PhysicalCurve.ElementList = ListOfElmt2
   PhysicalSurface.Name = 'DEFAULT SURFACE GROUP'
   PhysicalSurface.Type = 'SURFACE GROUP'
   PhysicalSurface.Description = 'SURFACE'
   PhysicalSurface.ElementList = ListOfElmt3
   PhysicalVolume.Name = 'DEFAULT VOLUME GROUP'
   PhysicalVolume.Type = 'VOLUME GROUP'
   PhysicalVolume.Description = 'VOLUME'
   PhysicalVolume.ElementList = ListOfElmt4

def Save_DefaultPhysical():
   global PhysicalPoint,PhysicalCurve,PhysicalSurface,PhysicalVolume,GroupNumber,ListOfObject,ListOfGeoGroup,ListOfNewGrpNum,ListOfOldGrpNum
   if len(PhysicalPoint.ElementList.List) > 0:
      GroupNumber = GroupNumber+1
      PhysicalPoint.Id =  GroupNumber
      ListOfObject.Add_Object(PhysicalPoint)
      ListOfGeoGroup.Add_Group(PhysicalPoint)
      ListOfNewGrpNum.append(GroupNumber)
      if len(ListOfOldGrpNum) > 0:
         ListOfOldGrpNum.append(max(ListOfOldGrpNum)+1)
      else:
         ListOfOldGrpNum.append(GroupNumber)
   if len(PhysicalCurve.ElementList.List) > 0:
      GroupNumber = GroupNumber+1
      PhysicalCurve.Id = GroupNumber
      ListOfObject.Add_Object(PhysicalCurve)
      ListOfGeoGroup.Add_Group(PhysicalCurve)
      ListOfNewGrpNum.append(GroupNumber)
      if len(ListOfOldGrpNum) > 0:
         ListOfOldGrpNum.append(max(ListOfOldGrpNum)+1)
      else:
         ListOfOldGrpNum.append(GroupNumber)
   if len(PhysicalSurface.ElementList.List) > 0:
      GroupNumber = GroupNumber+1
      PhysicalSurface.Id = GroupNumber
      ListOfObject.Add_Object(PhysicalSurface)
      ListOfGeoGroup.Add_Group(PhysicalSurface)
      ListOfNewGrpNum.append(GroupNumber)
      if len(ListOfOldGrpNum) > 0:
         ListOfOldGrpNum.append(max(ListOfOldGrpNum)+1)
      else:
         ListOfOldGrpNum.append(GroupNumber)
   if len(PhysicalVolume.ElementList.List) > 0:
      GroupNumber = GroupNumber+1
      PhysicalVolume.Id = GroupNumber
      ListOfObject.Add_Object(PhysicalVolume)
      ListOfGeoGroup.Add_Group(PhysicalVolume)
      ListOfNewGrpNum.append(GroupNumber)
      if len(ListOfOldGrpNum) > 0:
         ListOfOldGrpNum.append(max(ListOfOldGrpNum)+1)
      else:
         ListOfOldGrpNum.append(GroupNumber)

def AlphaNum2Str(val):
   try:
      AlphaNumber = string.atof(val)
   except:
      AlphaNumber = val
   else:
      if string.find(val,'.') == -1:
         AlphaNumber = string.atoi(val)
      else:
         AlphaNumber = string.atof(val)
   return AlphaNumber

def ConvertPoint():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,MetaPointNumber,MetaPointIdList,PointNumber,PhysicalPoin,ListOfNewElmtNum,ListOfOldElmtNum
   MetaPointNumber = MetaPointNumber+1
   GeoElementNumber = GeoElementNumber+1
   PointNumber = PointNumber+1
   MetaPointIdList[Field[1]] = ObjectNumber-1
   GeoElement = Point(GeoElementNumber,MetaPointNumber,PointNumber,Field[2],Field[3],Field[4])
   GeoElement.UserField.append(Field[5])
   PhysicalPoint.ElementList.Add_Element(GeoElement)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertLine():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,MetaCurveNumber,MetaCurveIdList,LineNumber,PhysicalCurve,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaCurveNumber = MetaCurveNumber+1
   LineNumber = LineNumber+1
   MetaCurveIdList[Field[1]] = ObjectNumber-1
   i = MetaPointIdList[Field[2]]
   point1 = ListOfObject.List[i]
   i = MetaPointIdList[Field[3]]
   point2 = ListOfObject.List[i]
   GeoElement = Line(GeoElementNumber,MetaCurveNumber,LineNumber,point1,point2)
   PhysicalCurve.ElementList.Add_Element(GeoElement)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertCircle():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,MetaCurveNumber,MetaCurveIdList,CircleNumber,PhysicalCurve,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaCurveNumber = MetaCurveNumber+1
   CircleNumber = CircleNumber+1
   MetaCurveIdList[Field[1]] = ObjectNumber-1
   i = MetaPointIdList[Field[2]]
   point2 = ListOfObject.List[i]
   i = MetaPointIdList[Field[3]]
   point1 = ListOfObject.List[i]
   i = MetaPointIdList[Field[4]]
   point3 = ListOfObject.List[i]
   GeoElement = Circle(GeoElementNumber, MetaCurveNumber, CircleNumber,
                       point1, point2, point3)
   PhysicalCurve.ElementList.Add_Element(GeoElement)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertEllipse():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,MetaCurveNumber,MetaCurveIdList,EllipseNumber,PhysicalCurve,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaCurveNumber = MetaCurveNumber+1
   EllipseNumber = EllipseNumber+1
   MetaCurveIdList[Field[1]] = ObjectNumber-1
   i = MetaPointIdList[Field[2]]
   point3 = ListOfObject.List[i]
   i = MetaPointIdList[Field[3]]
   point1 = ListOfObject.List[i]
   i = MetaPointIdList[Field[4]]
   point2 = ListOfObject.List[i]
   i = MetaPointIdList[Field[5]]
   point4 = ListOfObject.List[i]
   GeoElement = Ellipse(GeoElementNumber,MetaCurveNumber,CircleNumber,point1,point2,point3,point4)
   PhysicalCurve.ElementList.Add_Element(GeoElement)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertCurveLoop():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,FileIn,MetaWireCurveNumber,MetaWireCurveIdList,WireCurveNumber,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaWireCurveNumber = MetaWireCurveNumber+1
   WireCurveNumber = WireCurveNumber+1
   MetaWireCurveIdList[Field[1]] = ObjectNumber-1
   GeoElement = CurveWire(GeoElementNumber,MetaWireCurveNumber,WireCurveNumber)
   for CurveId in Field[2:]:
      i = MetaCurveIdList[abs(CurveId)]
      Curve = ListOfObject.List[i]
      GeoElement.Add_Curve(Curve)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertSurfaceLoop():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,FileIn,MetaWireSurfaceNumber,MetaWireSurfaceIdList,WireSurfaceNumber,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaWireSurfaceNumber = MetaWireSurfaceNumber+1
   WireSurfaceNumber = WireSurfaceNumber+1
   MetaWireSurfaceIdList[Field[1]] = ObjectNumber-1
   GeoElement = SurfaceWire(GeoElementNumber,MetaWireSurfaceNumber,WireSurfaceNumber)
   for SurfaceId in Field[2:]:
      i = MetaSurfaceIdList[abs(SurfaceId)]
      Surface = ListOfObject.List[i]
      GeoElement.Add_Surface(Surface)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertSurface():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,MetaSurfaceNumber,MetaSurfaceIdList,PlaneSurfaceNumber,RuledSurfaceNumber,PhysicalSurface,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaSurfaceNumber = MetaSurfaceNumber+1
   MetaSurfaceIdList[Field[1]] = ObjectNumber-1
   if Field[0] == 'Plane Surface':
      PlaneSurfaceNumber = PlaneSurfaceNumber+1
      GeoElement = PlaneSurface(GeoElementNumber,MetaSurfaceNumber,PlaneSurfaceNumber)
   else:
      RuledSurfaceNumber = RuledSurfaceNumber+1
      GeoElement = RuledSurface(GeoElementNumber,MetaSurfaceNumber,RuledSurfaceNumber)
   GeoElement.Create_ExternalWire(ListOfObject.List[MetaWireCurveIdList[Field[2]]])
   for WireId in Field[3:]:
      GeoElement.Add_Hole(ListOfObject.List[MetaWireCurveIdList[WireId]])
   # FIXME: c'est la fete
   # TempList = [GeoElement]
   # PhysicalSurface.Add_ElementList(TempList)
   PhysicalSurface.ElementList.Add_Element(GeoElement)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertVolume():
   global ListOfObject,ListOfGeoElement,GeoElementNumber,MetaVolumeNumber,MetaVolumeIdList,VolumeNumber,PhysicalVolume,ListOfNewElmtNum,ListOfOldElmtNum
   GeoElementNumber = GeoElementNumber+1
   MetaVolumeNumber = MetaVolumeNumber+1
   MetaVolumeIdList[Field[1]] = ObjectNumber-1
   VolumeNumber = VolumeNumber+1
   GeoElement = Volume(GeoElementNumber,MetaVolumeNumber,VolumeNumber)
   GeoElement.Create_ExternalWire(ListOfObject.List[MetaWireSurfaceIdList[Field[2]]])
   for WireId in Field[3:]:
      GeoElement.Add_Hole(ListOfObject.List[MetaWireSurfaceIdList[WireId]])
   PhysicalVolume.ElementList.Add_Element(GeoElement)
   ListOfObject.Add_Object(GeoElement)
   ListOfGeoElement.Add_Element(GeoElement)
   ListOfNewElmtNum.append(GeoElementNumber)
   ListOfOldElmtNum.append(Field[1])

def ConvertPhysicalPoint():
   global ObjectList,ListOfGeoGroup,GroupNumber,PhysicalPoint,ListOfNewGrpNum,ListOfOldGrpNum
   ListOfElmt = GeoElementList()
   for number in Field[2:]:
      if MetaPointIdList.has_key(number):
         GeoElement = ListOfObject.List[MetaPointIdList[number]]
         ListOfElmt.Add_Element(GeoElement)
         PhysicalPoint.ElementList.Del_Element(GeoElement)
      else:
         print 'The GeoElement of the Group', `GeoElementList`, 'is not in the Geometrical Data Structure'
   GroupNumber = GroupNumber+1
   PointGroupIdList[Field[1]] = ObjectNumber-1
   Group = GeoGroup()
   Group.Id = GroupNumber
   Group.Name = 'POINT GROUP(' + str(GroupNumber) + ')'
   Group.Type = 'POINT GROUP'
   Group.Description = 'POINT'
   Group.ElementList = ListOfElmt
   ListOfObject.Add_Object(Group)
   ListOfGeoGroup.Add_Group(Group)
   ListOfNewGrpNum.append(GroupNumber)
   ListOfOldGrpNum.append(Field[1])

def ConvertPhysicalCurve():
   global ObjectList,ListOfGeoGroup,GroupNumber,PhysicalCurve,ListOfNewGrpNum,ListOfOldGrpNum
   ListOfElmt = GeoElementList()
   for number in Field[2:]:
      if MetaCurveIdList.has_key(number):
         GeoElement = ListOfObject.List[MetaCurveIdList[number]]
         ListOfElmt.Add_Element(GeoElement)
         PhysicalCurve.ElementList.Del_Element(GeoElement)
      else:
         print 'The GeoElement of the Group GeoElementList is not in the Geometrical Data Structure'
   GroupNumber = GroupNumber+1
   CurveGroupIdList[Field[1]] = ObjectNumber-1
   Group = GeoGroup()
   Group.Id = GroupNumber
   Group.Name = 'CURVE GROUP(' + str(GroupNumber) + ')'
   Group.Type = 'CURVE GROUP'
   Group.Description = 'CURVE'
   Group.ElementList = ListOfElmt
   ListOfObject.Add_Object(Group)
   ListOfGeoGroup.Add_Group(Group)
   ListOfNewGrpNum.append(GroupNumber)
   ListOfOldGrpNum.append(Field[1])

def ConvertPhysicalSurface():
   global ObjectList,ListOfGeoGroup,GroupNumber,PhysicalSurface,ListOfNewGrpNum,ListOfOldGrpNum
   ListOfElmt = GeoElementList()
   for number in Field[2:]:
      if MetaSurfaceIdList.has_key(number):
         GeoElement = ListOfObject.List[MetaSurfaceIdList[number]]
         ListOfElmt.Add_Element(GeoElement)
         PhysicalSurface.ElementList.Del_Element(GeoElement)
      else:
         print 'The GeoElement of the Group GeoElementList is not in the Geometrical Data Structure'
   GroupNumber = GroupNumber+1
   SurfaceGroupIdList[Field[1]] = ObjectNumber-1
   Group = GeoGroup()
   Group.Id = GroupNumber
   Group.Name = 'SURFACE GROUP(' + str(GroupNumber) + ')'
   Group.Type = 'SURFACE GROUP'
   Group.Description = 'SURFACE'
   Group.ElementList = ListOfElmt
   ListOfObject.Add_Object(Group)
   ListOfGeoGroup.Add_Group(Group)
   ListOfNewGrpNum.append(GroupNumber)
   ListOfOldGrpNum.append(Field[1])

def ConvertPhysicalVolume():
   global ObjectList,ListOfGeoGroup,GroupNumber,PhysicalVolume,ListOfNewGrpNum,ListOfOldGrpNum
   ListOfElmt = GeoElementList()
   for number in Field[2:]:
      if MetaVolumeIdList.has_key(number):
         GeoElement = ListOfObject.List[MetaVolumeIdList[number]]
         ListOfElmt.Add_Element(GeoElement)
         PhysicalVolume.ElementList.Del_Element(GeoElement)
      else:
         print 'The GeoElement of the Group GeoElementList is not in the Geometrical Data Structure'
   GroupNumber = GroupNumber+1
   VolumeGroupIdList[Field[1]] = ObjectNumber-1
   Group = GeoGroup()
   Group.Id = GroupNumber
   Group.Name = 'VOLUME GROUP(' + str(GroupNumber) + ')'
   Group.Type = 'VOLUME GROUP'
   Group.Description = 'VOLUME'
   Group.ElementList = ListOfElmt
   ListOfObject.Add_Object(Group)
   ListOfGeoGroup.Add_Group(Group)
   ListOfNewGrpNum.append(GroupNumber)
   ListOfOldGrpNum.append(Field[1])

def ConvertNothing():
   return 1

def ConvertParameter():
   global ObjectList,ListOfParameter,ParameterNumber
   ParameterNumber = ParameterNumber+1
   ParameterIdList[LineCounter] = ObjectNumber-1
   Param = Parameter.Parameter(ParameterNumber,Field[1],'CHARACTERISTIC LENGTH',Field[2])
   ListOfObject.Add_Object(Param)
   ListOfParameter.Add_Parameter(Param)

def Line2Field(Line):
   global Field
   back = 0
   Field = []
   i = string.find(Line,'//')
   if i <> -1:
      Line = Line[0:i]
   if string.find(Line,'=') <> -1:
      if string.find(Line,'(') <> -1:
         i = string.index(Line,'(')
         Field.append(string.strip(Line[0:i]))
         Line = Line [i+1:]
         i = string.find(Line,')')
         Field.append(string.atoi(string.strip(Line[0:i])))
         Line = Line [i+1:]
         i = string.find(Line,'{')
      else:
         i = string.index(Line,'=')
         Field.append('Parameter')
         Field.append(string.strip(Line[0:i]))
      Line = Line [i+1:]
   elif ((len(Line) == 0) or ('{' not in Line)):
      Field.append('Nothing')
   else:
      i = string.index(Line,'{')
      Field.append(string.strip(Line[0:i]))
      Line = Line [i+1:]
   try:
      Back = Read_Tab[Field[0]](Line)
   except:
      Back = 0
      print ' '+Field[0],' Command not implemented\n'
   return Back

def Read_Value(Line):
   global Field
   i = string.find(Line,'}')
   Line = Line [0:i]
   while 1:
      i = string.find(Line,',')
      if i == -1:
         Field.append(AlphaNum2Str(string.strip(Line[i+1:])))
         break
      else:
         Field.append(AlphaNum2Str(string.strip(Line[0:i])))
         Line = Line[i+1:]

def Read_Circle(Line):
   Read_Value(Line)

def Read_Ellipse(Line):
   Read_Value(Line)

def Read_Parameter(Line):
   i = string.find(Line,';')
   Line = Line [0:i]
   Field.append(AlphaNum2Str(string.strip(Line)))

def Read_Nothing(Line):
   return 1

Read_Tab = {}
Read_Tab['Point'] = Read_Value
Read_Tab['Line'] = Read_Value
Read_Tab['Circle'] = Read_Circle
Read_Tab['Ellipse'] = Read_Ellipse
Read_Tab['Line Loop'] = Read_Value
Read_Tab['Plane Surface'] = Read_Value
Read_Tab['Ruled Surface'] = Read_Value
Read_Tab['Surface Loop'] = Read_Value
Read_Tab['Volume'] = Read_Value
Read_Tab['Physical Point'] = Read_Value
Read_Tab['Physical Line'] = Read_Value
Read_Tab['Physical Surface'] = Read_Value
Read_Tab['Physical Volume'] = Read_Value
Read_Tab['Parameter'] = Read_Parameter
Read_Tab['Nothing'] = Read_Nothing

Convert_Tab = {}
Convert_Tab['Point'] = ConvertPoint
Convert_Tab['Line'] = ConvertLine
Convert_Tab['Circle'] = ConvertCircle
Convert_Tab['Ellipse'] = ConvertEllipse
Convert_Tab['Line Loop'] = ConvertCurveLoop
Convert_Tab['Plane Surface'] = ConvertSurface
Convert_Tab['Ruled Surface'] = ConvertSurface
Convert_Tab['Surface Loop'] = ConvertSurfaceLoop
Convert_Tab['Volume'] = ConvertVolume
Convert_Tab['Physical Point'] = ConvertPhysicalPoint
Convert_Tab['Physical Line'] = ConvertPhysicalCurve
Convert_Tab['Physical Surface'] = ConvertPhysicalSurface
Convert_Tab['Physical Volume'] = ConvertPhysicalVolume
Convert_Tab['Parameter'] = ConvertParameter
Convert_Tab['Nothing'] = ConvertNothing

def Convert(InputList):
   global LineCounter,ObjectNumber,FileIn
   Reset_Variables()
   for FileNameIn in InputList:
      if not os.path.isfile(FileNameIn):
         print ' No such file ',FileNameIn,',check the path'
         break
      print ' Read the input file:',FileNameIn
      FileIn = open(FileNameIn,"r")
      LineCounter = 0
      Init_defaultPhysical()
      while 1:
         NextLine = FileIn.readline()
         LineCounter = LineCounter+1
         if not NextLine:
            break
         else:
            if Line2Field(NextLine) == 0:
               print ' Read Error in file:',FileNameIn,'at line:',LineCounter,'\n'
            elif Field[0] <> 'Nothing':
               if Convert_Tab.has_key(Field[0]):
                  ObjectNumber = ObjectNumber+1
                  # FIXME: don't except for anything
                  #try:
                  Convert_Tab[Field[0]]()
                  #except:
                     #ObjectNumber = ObjectNumber-1
                     #print ' Convert Error in file:',FileNameIn,'at line:',LineCounter,'\n'
               else:
                  print ' '+Field[0],'Function not yet Implementted\n'
      Save_DefaultPhysical()
      FileIn.close()
   ListOfElmtNum = [ListOfOldElmtNum,ListOfNewElmtNum]
   ListOfGrpNum = [ListOfOldGrpNum,ListOfNewGrpNum]
   return ListOfObject,ListOfGeoElement,ListOfElmtNum,ListOfGeoGroup,ListOfGrpNum,ListOfParameter










