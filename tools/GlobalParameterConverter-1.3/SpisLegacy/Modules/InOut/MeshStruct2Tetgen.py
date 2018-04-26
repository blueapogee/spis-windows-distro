"""
**Module Name:**  MeshStruct2Tetgen

**Project ref:**  Spis/SpisUI

**File name:**    MeshStruct2Tetgen.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Modules of conversion of mesh structure to the
Tetgen input format.

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


def Convert(FileName,SatData,CoordList = None):
   SatNodeList = SatData[0]
   SatFaceList = SatData[1]
   print ' Create the output file: '+FileName+'\n'
   FileOut = open(FileName,"w")
   FileOut.write('# Nods\n')

###########################################################################
#                                                                         #
# To have a good visualisation of the mesh in medit, Attribute and        #
# Marker are not used                                                     #
#                                                                         #
###########################################################################
                                                                          #
#   FileOut.write(str(SatNodeList.NbNode)+' 3 1 1\n')                     #
                                                                          #
   FileOut.write(str(SatNodeList.NbNode)+' 3 0 0\n')                      #
                                                                          #
###########################################################################

   for TempNode in SatNodeList.List:
      Attribute = ''
      Marker = ''
      for Num in TempNode.SkeletonId:
         Attribute = Attribute+' '+str(Num)
         Marker = Marker+' '+str(Num)

###########################################################################
#                                                                         #
# To have a good visualisation of the mesh in medit, Attribute and        #
# Marker are not used                                                     #
#                                                                         #
###########################################################################
                                                                          #
#      FileOut.write(str(TempNode.Id)+' '+str(TempNode.Coord[0])+' '+str(TempNode.Coord[1])+' '+str(TempNode.Coord[2])+Attribute+Marker+'\n')
                                                                          #
      FileOut.write(str(TempNode.Id)+' '+str(TempNode.Coord[0])+' '+str(TempNode.Coord[1])+' '+str(TempNode.Coord[2])+'\n')                           #
                                                                          #
###########################################################################

   FileOut.write('# Elements\n')

###########################################################################
#                                                                         #
# To have a good visualisation of the mesh in medit, Attribute and        #
# Marker are not used                                                     #
#                                                                         #
###########################################################################
                                                                          #
#   FileOut.write(str(SatFaceList.NbFace)+' 1\n')                         #
   FileOut.write(str(SatFaceList.NbFace)+' 0\n')                          #
                                                                          #
###########################################################################

   for TempFace in SatFaceList.List:
      Marker = ''
      for Num in TempFace.SkeletonId:
         Marker = Marker+' '+str(Num)
      NodeListString = ''
      for TempNode in TempFace.MeshElementNodeList:
         NodeListString = NodeListString+' '+str(TempNode.Id)


###########################################################################
#                                                                         #
# To have a good visualisation of the mesh in medit, Attribute and        #
# Marker are not used                                                     #
#                                                                         #
###########################################################################
                                                                          #
#      FileOut.write(str(len(TempFace.Connection))+' '+NodeListString+Marker+'\n')                                                                    #
      FileOut.write(str(len(TempFace.Connection))+' '+NodeListString+'\n')#
                                                                          #
###########################################################################

   i = 1
   if CoordList is None:
      CoordList = [[0,0,0]]
   HolePointList = ''
   for Coordinate in CoordList:
      HolePointList = HolePointList+str(i)+' '+str(Coordinate[0])+' '+str(Coordinate[1])+' '+str(Coordinate[2])+'\n'
   FileOut.write('# Holes\n'+str(len(CoordList))+'\n'+HolePointList)
   FileOut.write('# Domains\n0\n')
   FileOut.close()
