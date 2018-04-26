"""
**Module Name:**  GeoStruct2Gmsh

**Project ref:**  Spis/SpisUI

**File name:**    GeoStruct2Gmsh.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Modules of conversion of geometrical structure to the
GMSH geo format.

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

import os, string

Object = None

ListOfOldElmtNum = []
ListOfNewElmtNum = []
ListOfOldGrpNum = []
ListOfNewGrpNum = []

def Reset_Variables():
    global ListOfOldGrpNum,ListOfNewGrpNum,ListOfOldElmtNum,ListOfNewElmtNum
    ListOfOldElmtNum = []
    ListOfNewElmtNum = []
    ListOfOldGrpNum = []
    ListOfNewGrpNum = []

def ConvertPoint():
    '''
    Convert points. 
    '''
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.PointId
    Line = 'Point('+str(Num)+') = {'+str(Object.Coord[0])+', '+str(Object.Coord[1])+', '+str(Object.Coord[2])+', '+str(Object.UserField[0])+'};\n'
    return Line

def ConvertLine():
    '''
    Convert line.
    '''
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = 'Line ('+str(Num)+') = {'+str(Object.StartPoint.PointId)+', '+str(Object.EndPoint.PointId)+'};\n'
    return Line

def ConvertCircle():
    '''
    Convert circle.
    '''
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = 'Circle ('+str(Num)+') = {'+str(Object.StartPoint.PointId)+', '+str(Object.Center.PointId)+', '+str(Object.EndPoint.PointId)+'};\n'
    return Line

def ConvertEllipse():
    '''
    Convert Ellipse.
    '''
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = 'Ellipse ('+str(Num)+') = {'+str(Object.StartPoint.PointId)+', '+str(Object.Center.PointId)+', '+str(Object.MajorAxePoint.PointId)+', '+str(Object.EndPoint.PointId)+'};\n'
    return Line

def ConvertCurveWire():
    '''
    convert wire (i.e curve)
    '''
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Connection[0].Id)])
    else:
        Line = str(Object.Connection[0].MetaId)
    i = 1
    for curve in Object.Connection[1:]:
        if Object.SwapStartEndPointStatus[i] == 1:
            ep = -1
        else:
            ep = 1
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ep*ListOfOldElmtNum[ListOfNewElmtNum.index(curve.Id)])
        else:
            Line = Line+', '+str(ep*curve.MetaId)
        i = i+1
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = 'Line Loop ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertSurface():
    '''
    convert surface.
    '''
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.WireCurve[0].Id)])
    else:
        Line = str(Object.WireCurve[0].MetaId)
    for Wire in Object.WireCurve[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Wire.Id)])
        else:
            Line = Line+', '+str(Wire.MetaId)
    if Object.Type == 'PLANE SURFACE':
        Type = 'Plane Surface'
    else:
        Type = 'Ruled Surface'

    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = Type+' ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertSurfaceWire():
    '''
    convert Surface wire.
    '''
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Connection[0].Id)])
    else:
        Line = str(Object.Connection[0].MetaId)
    for Surface in Object.Connection[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Surface.Id)])
        else:
            Line = Line+', '+str(Surface.MetaId)
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = 'Surface Loop ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertVolume():
    '''
    convert volume
    '''
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.WireSurface[0].Id)])
    else:
        Line = str(Object.WireSurface[0].MetaId)
    for Wire in Object.WireSurface[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Wire.Id)])
        else:
            Line = Line+', '+str(Wire.MetaId)
    if len(ListOfOldElmtNum) > 0:
        Num = ListOfOldElmtNum[ListOfNewElmtNum.index(Object.Id)]
    else:
        Num = Object.MetaId
    Line = 'Volume ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertPhysicalPoint():
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.ElementList.List[0].Id)])
    else:
        Line = str(Object.ElementList.List[0].PointId)
    for Point in Object.ElementList.List[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Point.Id)])
        else:
            Line = Line+', '+str(Point.PointId)
    if len(ListOfOldGrpNum) > 0:
        Num = ListOfOldGrpNum[ListOfNewGrpNum.index(Object.Id)]
    else:
        Num = Object.Id
    Line = 'Physical Point ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertPhysicalCurve():
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.ElementList.List[0].Id)])
    else:
        Line = str(Object.ElementList.List[0].MetaId)
    for Curve in Object.ElementList.List[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Curve.Id)])
        else:
            Line = Line+', '+str(Curve.MetaId)
    if len(ListOfOldGrpNum) > 0:
        Num = ListOfOldGrpNum[ListOfNewGrpNum.index(Object.Id)]
    else:
        Num = Object.Id
    Line = 'Physical Line ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertPhysicalSurface():
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.ElementList.List[0].Id)])
    else:
        Line = str(Object.ElementList.List[0].MetaId)
    for Surface in Object.ElementList.List[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Surface.Id)])
        else:
            Line = Line+', '+str(Surface.MetaId)
    if len(ListOfOldGrpNum) > 0:
        Num = ListOfOldGrpNum[ListOfNewGrpNum.index(Object.Id)]
    else:
        Num = Object.Id
    Line = 'Physical Surface ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertPhysicalVolume():
    if len(ListOfOldElmtNum) > 0:
        Line = str(ListOfOldElmtNum[ListOfNewElmtNum.index(Object.ElementList.List[0].Id)])
    else:
        Line = str(Object.ElementList.List[0].MetaId)
    for Volume in Object.ElementList.List[1:]:
        if len(ListOfOldElmtNum) > 0:
            Line = Line+', '+str(ListOfOldElmtNum[ListOfNewElmtNum.index(Volume.Id)])
        else:
            Line = Line+', '+str(Volume.MetaId)
    if len(ListOfOldGrpNum) > 0:
        Num = ListOfOldGrpNum[ListOfNewGrpNum.index(Object.Id)]
    else:
        Num = Object.Id
    Line = 'Physical Volume ('+str(Num)+') = {'+Line+'};\n'
    return Line

def ConvertParameter():
    Line = Object.ParameterName+' = '+str(Object.ParameterValue)+';\n'
    return Line

Convert_Tab = {}
Convert_Tab['POINT'] = ConvertPoint
Convert_Tab['LINE'] = ConvertLine
Convert_Tab['CIRCLE'] = ConvertCircle
Convert_Tab['ELLIPSE'] = ConvertEllipse
Convert_Tab['CURVE WIRE'] = ConvertCurveWire
Convert_Tab['SURFACE WIRE'] = ConvertSurfaceWire
Convert_Tab['PLANE SURFACE'] = ConvertSurface
Convert_Tab['RULED SURFACE'] = ConvertSurface
Convert_Tab['VOLUME'] = ConvertVolume
Convert_Tab['POINT GROUP'] = ConvertPhysicalPoint
Convert_Tab['CURVE GROUP'] = ConvertPhysicalCurve
Convert_Tab['SURFACE GROUP'] = ConvertPhysicalSurface
Convert_Tab['VOLUME GROUP'] = ConvertPhysicalVolume
Convert_Tab['PARAMETER'] = ConvertParameter

def Convert(ListOfObject,FileNameOut,ListOfElmtNum = None,ListOfGrpNum
    = None):
    global Object,ListOfOldElmtNum,ListOfNewElmtNum,ListOfOldGrpNum,ListOfNewGrpNum
    Reset_Variables()
    if ListOfElmtNum is not None:
        ListOfOldElmtNum = ListOfElmtNum[0]
        ListOfNewElmtNum = ListOfElmtNum[1]
    if ListOfGrpNum is not None:
        ListOfOldGrpNum = ListOfGrpNum[0]
        ListOfNewGrpNum = ListOfGrpNum[1]

    '''
    ReadRep = 'y'
    if os.path.isfile(FileNameOut):
        print ' File ',FileNameOut,', already exist: Overwrite (y/n) ?'
        while 1:
            print ' ',
            ReadRep = raw_input()
            if ((string.lower(ReadRep) == 'y') or (string.lower(ReadRep) == 'n')):
                break
            else:
                print 'Enter "y" or "n"'
    if string.lower(ReadRep) == 'y':
    '''
    print 'Write the OuputFile:',FileNameOut
    FileOut = open(FileNameOut,"w")
    for Object in ListOfObject.List:
        #if Convert_Tab.has_key(Object.Type):
        NextLine = Convert_Tab[Object.Type]()
        #else:
        #print "ERROR: there is an instance of an abstract class"
        FileOut.write(NextLine)
    FileOut.close()

