"""
Modules of conversion of geometrical structure to the PicUp3D sc format.

**Project ref:**  Spis/SpisUI

**File name:**    LightMeshStruct2PicUp.py

:status:          Implemented

**Creation:**     02/07/2005

**Modification:** 02/10/2005   validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       J.Forest, S.Jourdain

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Julien Forest                 | Definition/Creation        |
|                | contact@artenum.com           |                            |
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

def Convert(FileName, NbNodeIn, lightMeshNodeIteratorIn, NbFaceIn, lightMeshFaceIteratorIn):
   '''
   Performs the convertion toward the PicUp3D SC format.
   '''    
   lightMeshNodeIterator = lightMeshNodeIteratorIn
   
   FileOut = open(FileName,"w")
   FileOut.write(str(NbNodeIn)+'\n')
   while lightMeshNodeIterator.hasNext():
       node = lightMeshNodeIterator.next()
       FileOut.write(str(node.getCoord()[0])+' '+str(node.getCoord()[1])+' '+str(node.getCoord()[2])+'\n')

   # writing of the triangles
   FileOut.write(str(NbFaceIn)+'\n')
   while lightMeshFaceIteratorIn.hasNext():
      face = lightMeshFaceIteratorIn.next()
      NodeList = face.getNodes()
      nodeIdList=[]
      for node in NodeList:
          nodeIdList.append(node.getId()-1)
      NodeListString = ""
      for Id in nodeIdList:
         NodeListString = NodeListString+str(Id)+' '
      FileOut.write(NodeListString+'\n')
   
   FileOut.close()
