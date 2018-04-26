"""
Module of setting of electrical nodes properties and attributes for the spacecraft.

**File name:**    TaskElecNodeEditor.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+

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
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

from Bin.Tasks.shared                     import shared, sharedFrames, sharedProp
from Bin.Tasks.TemplateEditor             import TemplateEditor
from Bin.Tasks.Task                       import Task
from Bin.Tasks.common                     import create_internal_frame

class ElecNodeEditor(TemplateEditor):
    def __init__(self, frame):
        self.templateID = "defaultElecNodeList"
        self.templateIDListType = "ElecNodeList"
        self.templateIDType = "ElecNode"
        self.templateIDListName = "ElecDataList"
        self.propertiesTypeList = None
        self.relatedPropList = None
        TemplateEditor.__init__(self, frame)

class TaskElecNodeEditor(Task):
    desc = "ElecNode Editor"
    def run_task(self):
        frame = create_internal_frame("Electrical Nodes Editor",sharedFrames["gui"].getCurrentDesktop())
        self.size = frame.getParent().getSize()
        frame.reshape( 0, 0, (self.size.width)/3, self.size.height)                
        editor = ElecNodeEditor(frame)
        editor.show()
        print "task ElecNodeEditor is daemonic"
