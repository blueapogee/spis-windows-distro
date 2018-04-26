"""
**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

**Project ref:**  Spis/SpisUI

**File name:**    Action.py

**Creation:**     21/06/2003

**Modification:** 01/10/2003

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          Franck Warmont, Gerard Sookahet, Julien Forest

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                 | Creation                   |
|                | Franck.Warmont@artenum.com     |                            |
+----------------+--------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet                | Desing/Validation/         |
|                | Gerard.Sookahet@artenum.com    | Correction/Extension       |
+----------------+--------------------------------+----------------------------+
| 0.3.0          | Julien Forest                  | Creation/Extension         |
|                | J.forest@artenum.com           |                            |
+----------------+--------------------------------+----------------------------+

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


import os, sys

class MeshField:
    '''
    General list of references of mesh elements for DataField. Associated with the DataFields
    a MeshField will refere all mesh elements (e.g Node, Edges, Faces, Cells) on which ones
    the DataFields is deployed. In order to save memory, several DataFields can be associated 
    on the same MeshField.  
    ''' 
    def __init__(self, DId = -1, DName = None, DType = "",
                 DDescription = None, DLocal = None, DMeshElementList = None, DMeshElementIdList = None,
                 DDataFieldList = None):
        '''
        Default cosntructor. 
        '''
        self.Id = DId                                   # required
        self.Name = DName                               # required
        self.Type = DType
        self.Description = DDescription                 # required
        self.Local = DLocal                             # required
        if DMeshElementIdList == None:
            self.MeshElementIdList = []
        else:
            self.MeshElementIdList = DMeshElementIdList # required
        if DMeshElementList == None:
            self.MeshElementList = []
        else:
            self.MeshElementList = DMeshElementList     # required
        self.DataFieldList = DDataFieldList             # required

    def __str__(self):
        res = 'MeshField Id ' + str(self.Id) + os.linesep
        res += 'MeshField Name ' + self.Name + os.linesep
        res += 'MeshField Type ' + self.Type + os.linesep
        res += 'MeshField Description ' + str(self.Description) + os.linesep
        res += 'MeshField Local ' + str(self.Local) + os.linesep
        if (self.Local is 0):
            res += 'MeshField of Nodes' + os.linesep
        if (self.Local is 1):
            res += 'MeshField of Edges' + os.linesep
        if (self.Local is 2):
            res += 'MeshField of Facets' + os.linesep
        if (self.Local is 3):
            res += 'MeshField of Cells' + os.linesep
	if (self.Local is 4):
            res += 'MeshField of Curvi' + os.linesep
        #XXX res += 'MeshField Mesh Element Id List ' + str(self.MeshElementIdList)\
        #XXX       + os.linesep
        res += 'MeshField DataField List ' + str(self.DataFieldList) \
               + os.linesep
        res += 'MeshField Settings ' + str(self.check_settings()) + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Description == None \
           or self.Local == None or self.DataFieldList == None:
            return 0
        return 1
        
    def rebuildMeshElmListFromMeshELmIdList(self, sharedMesh):
        '''
        re-build the MeshElement list for the Mesh Element Id list.
        '''
        for Id in self.MeshElementIdList:
            sys.stdout.write(".")
            self.MeshElementList.append(sharedMesh[self.Local].GetElementById(Id))
            # FIXME : Might not work in hight perf
            # Do this in normal version instead
            # sharedMesh[self.Local].GetElementById(Id)
        print " "
