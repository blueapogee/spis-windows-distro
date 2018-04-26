"""
Modules of conversion of geometrical structure to the
PicUp3D sc format.

**Project ref:**  Spis/SpisUI

**File name:**    MeshStruct2PicUp.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Julien Forest                 | Definition/Creation        |
|                | j.forest@artenum.com          |                            |
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

def Convert(FileName, SatData):
   SatNodeList = SatData[0]
   SatFaceList = SatData[2]
   print ' Create the output file: '+FileName+'\n'
   FileOut = open(FileName,"w")
   FileOut.write(str(SatNodeList.NbNode)+'\n')
   for TempNode in SatNodeList.List:
      FileOut.write(str(TempNode.Coord[0])+' '+str(TempNode.Coord[1])+' '+str(TempNode.Coord[2])+'\n')

   # writing of the triangles
   FileOut.write(str(SatFaceList.NbFace)+'\n')
   for TempFace in SatFaceList.List:
      Marker = TempFace.SkeletonId[0]
      NodeListString = str(TempFace.MeshElementNodeList[0].Id-1)
      for TempNode in TempFace.MeshElementNodeList[1:]:
         NodeListString = NodeListString+' '+str(TempNode.Id-1)
      FileOut.write(NodeListString+' '+str(Marker)+'\n')
   FileOut.close()
