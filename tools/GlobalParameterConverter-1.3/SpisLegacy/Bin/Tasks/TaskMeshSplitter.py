"""
**File name:**    TaskGroupManager.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
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

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles, sharedTasks
from Bin.Tasks.shared         import sharedProp
from Bin.Tasks.common         import ask_value

from Bin.MeshSplitter import MeshSplitter

import sys
sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)


class TaskMeshSplitter(Task):
    """
    Performs the mesh splitting for a given group or set of group. 
    typically used for mesh and solve fields around a thin surface
    with potential or electric discontinuities.
    """
    desc = "Task of mesh spliting for thin surfaces"
    def run_task(self):
       
        context = sharedTasks["context"]
        
        splitter = MeshSplitter()
        
        splitter.CrackMeshGrp(context[0], context[1], context[2])
        splitter.GetFields()
        splitter.GetControls()
        
        if context[3] == 1:
            splitter.GetVtkDataSet()
        
