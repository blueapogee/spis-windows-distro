"""
Generic 3D cell of mesh. Typically thetraedron. 

**Project ref:**  Spis/SpisUI

**File name:**    Cell.py

**File type:**    Module

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**Use:**          N/A

**Description:**  Generic 3D cell of mesh. Typically thetraedron.

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
from Modules.Meshing.MeshElement        import MeshElement

class Cell(MeshElement):
    '''
    mesh element of type cell. This element is a generic cell (dim 3) 
    and its type can be defined by the parameter CellType. Its members are:
    **CellId** Id of the cell (different of the meshElement.Id)
    **CellType** Type of the cell (typically THETRAEDRON)
    **Connection** List of faces living on this cell. 
    '''        
        
    def __init__(self, ElmtNum = None, CellNum = -1, FType = None):
        MeshElement.__init__(self, ElmtNum, 'CELL')
        self.CellId = CellNum
        self.CellType = FType
        self.Connection = []

    def Print_Element(self):
        print self

    def __str__(self):
        res = MeshElement.__str__(self)
        res += '    Cell Id ' + str(self.CellId) + os.linesep
        res += '    Cell Type ' + str(self.CellType) + os.linesep
        # XXX res += '    Face List ' + str(FaceList) + os.linesep
        res += '    Cell Settings ' + str(self.check_settings()) + os.linesep
        res += '    Face Connection ' + os.linesep
        for Face in self.Connection:
#XXX erreur de syntax
           res += '     Mesh Element Id ' + str(Face.Id) + ' ( Face Id ' \
                  + str(Face.FaceId) + ' )' + os.linesep
        return res

        
        
    def check_settings(self):
        """ check if the current element is set (return 1) or not (return 0)"""
        if self.CellId == -1 or self.CellType == None:
            return 0
        return MeshElement.check_settings(self)

        
    def Modify_Id(self, ElmtNum):
        """Change the Id of the ELEMENT to ElmtNum. This method corrects also 
           the corresponding connection."""
        for Face in self.Connection:
            i = Face.CellOnFace.index(self.Id)
            del Face.CellOnFace[i]
            Face.CellOnFace.append(ElmtNum)
        self.Id = ElmtNum

        
        
        
    def Add_Face(self,Face):
        if Face in self.Connection:
            print ' Face already in FaceList'
        elif Face.check_settings() == 0:
            print ' All Face settings not yet set'
        else:
            if self.Id is not -1:
                Face.CellOnFace.append(self.Id)
            self.Connection.append(Face)

    def Del_Face(self,Face):
        if Face not in self.Connection:
            print ' Face is not in FaceList'
        else:
            if self.Id is not -1:
                i = Face.CellOnFace.index(self.Id)
                del Face.CellOnFace[i]
            i = self.Connection.index(Face)
            del self.Connection[i]
