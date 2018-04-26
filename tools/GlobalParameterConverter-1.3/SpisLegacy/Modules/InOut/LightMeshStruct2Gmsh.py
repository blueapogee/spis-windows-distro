"""
Import module from Gmsh mesh format to SPIS-UI LightMesh
data structure.

**Project ref:**  Spis/SpisUI

**File name:**    LightMeshStruct2Gmsh.py

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Sebastien Jourdain

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Sebastien Jourdain             | Bug correction             |
|                | jourdain@artenum.com           |                            |
+----------------+--------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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

Node = None
Element = None

ListOfOldSkeletonElmtNum = []
ListOfNewSkeltonElmtNum = []
ListOfOldNodeNum = []
ListOfNewNodeNum = []

def Reset_Variables():
   global ListOfOldNodeNum,ListOfNewNodeNum,ListOfOldSkeletonElmtNum,ListOfNewSkeltonElmtNum
   ListOfOldSkeletonElmtNum = []
   ListOfNewSkeltonElmtNum = []
   ListOfOldNodeNum = []
   ListOfNewNodeNum = []

Convert_Type = {}
Convert_Type['LINE'] = '1'
Convert_Type['TRIANGLE'] = '2'
Convert_Type['QuUADRANGLE'] = '3'
Convert_Type['TETRAHEDRON'] = '4'
Convert_Type['HEXAHEDRON'] = '5'
Convert_Type['PRISM'] = '6'
Convert_Type['PYRAMID'] = '7'
Convert_Type['POINT'] = '15'


def Convert( FileNameOut, NbNode, nodeList, NbMesh, meshElmListIn):
    
   if 1:
      print 'Write the OuputFile:', FileNameOut
      FileOut = open(FileNameOut, "w")
      FileOut.write('$NOD\n'+str(NbNode)+'\n')
      
      for  node in nodeList:
         NextLine = str(node.getId())+' '+str(node.getCoord()[0])+' '+str(node.getCoord()[1])+' '+str(node.getCoord()[2])+'\n'
         FileOut.write(NextLine)
      FileOut.write('$ENDNOD\n')
      
      
      FileOut.write('$ELM\n')
      FileOut.write(str(NbMesh)+'\n')
         
      for elm in meshElmListIn:
          NextLine = str(elm.getId())+' '+str(elm.getSize())+' '+str(elm.getMeshGroupId()[0]+" ")   #+' '+str(elm.GeoElement.Id)+' '+str(elm..getNbNode())
          
          for node in elm.getNodes():
              NextLine = NextLine + str(node.getId())+" "
          NextLine = NextLine+'\n'
          FileOut.write(NextLine)
          
      FileOut.write('$ENDELM\n')
      
      FileOut.close()
      
