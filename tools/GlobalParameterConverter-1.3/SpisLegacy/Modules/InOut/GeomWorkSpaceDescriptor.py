"""
Exports the given GroupNum as an equivalent Python script. The output scritp can 
be reload aftert just by a Python import. The class scan is not recursive yet. 

**Module Name:**  GeomWorkSpaceDescriptor:

**Project ref:**  Spis/SpisUI

**File type:**    Module

:status:          implemented

**Creation:**     10/07/2006

**Modification:** 20/08/2006  AL preliminary validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          J.Forest

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Julien Forest                  | Creation                   |
|                | j.forest@artenum.com           |                            |
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

import os

class GeomWorkSpaceDescriptor:
    '''
    Module of GEOM/CAD project management. This modules will manage the 
    references of the workspace containing all CAD files used to describe the 
    whole modelled geometry. He will also set the reference to the main file 
    (i.e entry point) for the framework.
    '''

    def __init__(self):
            '''
            Default cosntructor.
            '''
            self.listFiles = None
            self.nameMainFile = None
            self.canonicalPath = None
            
    def setMainFile(self, nameMainFileIn):
            '''
            set the reference to the main CAD file.
            '''
            self.nameMainFile = nameMainFileIn
            
    def updateListFiles(self):
            '''
            update the list of files present in the workspace.
            '''
            if self.canonicalPath != None:
                self.listFiles = os.listdir(self.canonicalPath)
            
    def setCanonicalPath(self, pathIn):
            '''
            set the path of the workspace directory.
            '''
            self.canonicalPath = pathIn
