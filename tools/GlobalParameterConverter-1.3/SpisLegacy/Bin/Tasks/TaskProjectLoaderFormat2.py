"""
**File name:**    TaskLoadProj.py

**Creation:**     2004/03/31

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
| 3.1.0   | Yves Le Rumeur                       | Modif                      |
|         | lerumeur@artenum.com                 |                            |
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

from Bin.Tasks.shared              import *
from Bin.Tasks.common              import *
from Bin.Tasks.TaskBuiltins        import *
from Bin.Tasks.FileChooserSwing    import *


#import java
#import pawt
#import javax.swing
#from java.awt.event                import ItemEvent
#from java.awt                      import BorderLayout, GridLayout

import sys
#, shutil, os

#sys.path.append("..")
from Bin.config                    import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, GL_EXCHANGE
sys.path.append(GL_SPISUIROOT_PATH)
from Bin.Tasks.Task                import Task


#from org.spis.imp.ui.util import DirectoryDialog

from Bin.ProjectLoader2 import ProjectLoader2

class TaskProjectLoaderFormat2(Task):
    """TaskProjectLoaderFormat2"""
    desc = "Saving of the current project"
    
    
    def run_task(self):

        self.loader = ProjectLoader2()
        self.loader.setLoadingList(sharedTasks["context"])
        self.loader.load()
        sharedTasks["context"] = None
         
