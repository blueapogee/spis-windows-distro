"""
Modules of definition of generic mash element structure.

**Project ref:**  Spis/SpisUI

**File name:**    MeshElement.py

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.2.0

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

class MeshElement:
    """Abstract element class. This class is he base forall ohers elements. It contains
    as membres:
    **Id** the Id of the element.
    **Type** the type of the element.
    **SkeletonId** the Id of the skeleton to wich one the element is linked, if 
    the element is a skeleton.
    **MeshElementNodeList** the list of nodes consituting the element.
    **MeshGroupIdList** the list of groups to which ones the element is linked. 
    **SkeletonElementIdList** the list of Id of skeletons to which ones the element is linked.
    **ListId** Temporay Id, sometime used to remember index of meshelement within List.
    **isSelected** flag used to mark the object, for a selection during a processing for example.
    """
    def __init__(self, ElmtNum = -1, ElmtType = None):
        """ main constructor"""
        self.Id = ElmtNum
        self.Type = ElmtType
        self.SkeletonId = []
        self.MeshElementNodeList = []
        self.MeshGroupIdList = []
        self.SkeletonElementIdList = []
        self.ListId = 0 	# Temporay Id, sometime used to remember index of meshelement within List 
        self.isSelected = 0

    def Print_Element(self):
        """ prints the characteritics of the element."""
        print self

    def __str__(self):
        res = 'Mesh Element Id ' + str(self.Id) + os.linesep
        res += 'Mesh Element Type ' + self.Type + os.linesep
        res += 'Belong to Mesh Group of ID ' + str(self.MeshGroupIdList) \
               + os.linesep
        TmpList = []
        for TmpNode in self.MeshElementNodeList:
            TmpList.append(TmpNode.Id)
        #res += 'Living on Node list ' + str(self.MeshElementNodeList) + os.linesep
        res += 'Living on Node list ' + str(TmpList) + os.linesep
        res += 'Belong to Skeleton of ID' + str(self.SkeletonElementIdList) \
               + os.linesep
        res += 'Mesh Element Settings ' + str(self.check_settings()) \
               + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1:
            return 0
        return 1
        
    def GetBaryCenter(self, masses):
        nbNodes = len(self.MeshElementNodeList)
        gravityCenter = [0.0, 0.0, 0.0]
        for coordIndex in xrange(3):
            totalMass = 0.0
            for elm in self.MeshElementNodeList:
                mass = masses[self.MeshElementNodeList.index(elm)]
                totalMass = totalMass + mass
                gravityCenter[coordIndex] =   gravityCenter[coordIndex] + mass*elm.Coord[coordIndex]
                                            
            gravityCenter[coordIndex] = gravityCenter[coordIndex]/totalMass                             
        return(gravityCenter)
                                         
    def GetIsoBaryCenter(self):
        masses =  [1.0 for i in xrange(len(self.MeshElementNodeList))]
        return(self.GetBaryCenter(masses))
        
        
