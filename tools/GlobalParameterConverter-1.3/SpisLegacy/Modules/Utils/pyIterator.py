"""
**Module Name:**  pyIterator

**Project ref:**  Spis/SpisUI

**File name:**    pyIterator.py

:status:          Implemented

**Creation:**     10/11/2005

**Modification:** 22/11/2005  Validation

**Use:**

**Description:**  Iterator on Java list.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsen Lupin, Jourdain

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+---------------------------------+----------------------------+
| Version number | Author (name, e-mail)           | Corrections/Modifications  |
+----------------+---------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                    | Creation                   |
|                | Arsen.Lupin@atenum.com          |                            |
+----------------+---------------------------------+----------------------------+

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


import java.util.Iterator

class pyIterator(java.util.Iterator):
    '''
    Iterator on Java list.
    '''

    def __init__(self,listin):
        self.list = listin
        self.currentIndex = 0
        
    def hasNext(self):
        return(self.currentIndex < len(self.list))
            
    def next(self):
        val = self.list[self.currentIndex]
        self.currentIndex = self.currentIndex + 1
        return(val)
            
    def remove(self):
         pass
