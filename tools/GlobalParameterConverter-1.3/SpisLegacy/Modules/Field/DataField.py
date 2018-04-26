"""
**Description:**  This module defines the data structure for the Data fields

**Project ref:**  Spis/SpisUI

**File name:**    Action.py

**Creation:**     21/06/2003

**Modification:** 01/10/2003  GS preliminary validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          Franck Warmont, Gerard Sookahet, Julien Forest

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                | Creation                   |
|                | Franck.Warmont@artenum.com    |                            |
+----------------+-------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet               | Design/Validation          |
|                | Gerard.Sookahet@artenum.com   | Correction/Extension       |
+----------------+-------------------------------+----------------------------+
| 0.3.0          | Julien Forest                 | Creation/Extension         |
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


import os

class DataField:
    '''
    field object. DataField are used to represent fields of all types (scalar, 
    vectorial or object) on the grid. Each data field is linked to a Meshfield
    object, that itself makethe link with the grid. 
    '''
    def __init__(self, DId = -1, DName = None, DType = None,
                 DDescription = None, DUnit = None, DLocal = None,
                 DValue = None, DLockedValue = None, DValueList = None,
                 DMeshFieldId = None):
        '''
        Main contructor.
        
        :Parameters:
            - `DId`: Id the DataField. This set the self.Id member of the DataField.
            - `DName`: Name of the DataField. This set the self.Name of the DataField.
            - `DType`: Type (e.g float) of the DataField. This set the self.Type of the DataField.
            - `DDescription`: defines the description of the DataField.
            - `DUnit`: defines (if needed) the unit of the DataField.
            - `DLocal`: (REQUIRED) defines the localisation of the data. This set the self.local of the DataField.
                
                local = 0, data on node
                local = 1, data on edge
                local = 2, data on Face
                local = 3, data on Cell

        '''
        self.Id = DId                                   # required
        self.Name = DName                               # required
        self.Type = DType                               # required
        self.Description = DDescription                 # required
        self.Unit = DUnit                               # required
        self.Local = DLocal                             # required
        self.Value = DValue                             # required
        self.LockedValue = DLockedValue                 # required
        if DValueList == None:
            self.ValueList = []
        else:
            self.ValueList = DValueList                 # required
        self.MeshFieldId = DMeshFieldId                 # required
        self.Category =  None

    
    def __str__(self):
        res = 'DataField Id ' + str(self.Id) + os.linesep
        res += 'DataField Name ' + self.Name + os.linesep
        res += 'DataField Type ' + self.Type + os.linesep
        res += 'DataField Description ' + self.Description + os.linesep
        res += 'DataField Unit ' + str(self.Unit) + os.linesep
        res += 'DataField Local ' + str(self.Local) + os.linesep
        if (self.Local is 0):
            res += 'DataField on Mesh Nodes' + os.linesep
        if (self.Local is 1):
            res += 'DataField on Mesh Edges' + os.linesep
        if (self.Local is 2):
            res += 'DataField on Mesh Facets' + os.linesep
        if (self.Local is 3):
            res += 'DataField on Mesh Cells' + os.linesep
	if (self.Local is 4):
            res += 'DataField on Mesh Curvi' + os.linesep
        #XXX res += 'DataField ValueList ' + str(self.ValueList) + os.linesep
        res += 'DataField MeshField Id ' + str(self.MeshFieldId) + os.linesep
        res += 'DataField LockedValue ' + str(self.LockedValue) + os.linesep
        res += 'DataField Settings ' + str(self.check_settings()) + os.linesep
        return res

    def check_settings(self):
        if self.Id == -1 or self.Name == None or self.Type == None\
           or self.Description == None or self.Unit == None \
           or self.Local == None or self.Value == None \
           or self.LockedValue == None or self.ValueList == []\
           or self.MeshFieldId == None:
            return 0
        return 1
