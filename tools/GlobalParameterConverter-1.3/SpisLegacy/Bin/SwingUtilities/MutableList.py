"""
**File name:**    MutableList.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spine.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**
+---------+----------------------------------+----------------------------+
| Version | Author (name, e-mail)            | Corrections/Modifications  |
+---------+----------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                     | Creation                   |
|         | arsene.lupin@artenum.com         |                            |
+---------+----------------------------------+----------------------------+
| 3.1.0   | Yves Le Rumeur                   | Modif                      |
|         | lerumeur@artenum.com             |                            |
+---------+----------------------------------+----------------------------+

PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spine.org`: http://www.spine.org
"""
__docformat__ = "restructuredtext en"

import pawt

class MutableList(pawt.swing.JList):
    def __init__(self):
        pawt.swing.JList.__init__(self, pawt.swing.DefaultListModel())

    def getContents(self):
	return self.getModel()
