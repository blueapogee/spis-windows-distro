

"""
**Module Name:**  ProjectDescriptor

**Project ref:**  Spis/SpisUI

**File type:**    Module

:status:          implemented

**Creation:**     10/01/2005

**Modification:** 20/03/2005  AL preliminary validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          Arsene Lupin

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                   | Creation                   |
|                | Arsene Lupin@artenum.com       |                            |
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

class ProjectDescriptor:

    def __init__(self):
            print "toto"
            self.sharedFiles =  None
            
    def setSharedFiles(self, dicIn):
            self.sharedFiles = dicIn
            
