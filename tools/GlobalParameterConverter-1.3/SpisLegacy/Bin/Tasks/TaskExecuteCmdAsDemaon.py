"""
**File name:**    TaskExecuteCmdAsDemaon.py

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

import sys, os

import Bin.Tasks.shared
from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedProp
from Bin.Tasks.common         import ask_value
from Bin.Tasks.shared         import sharedGroups
from Bin.Tasks.shared         import sharedTasks


sys.path.append("..")
from Bin.config         import *
sys.path.append(GL_SPISUIROOT_PATH)


class TaskExecuteCmdAsDemaon(Task):
    '''Deprecated.'''
    desc = "Conversion of groups"
    
    #def setCmd(self, cmdIn):
    #    self.cmd = cmdIn
       
    #def resetCmd(self):
    #    self.cmd = None
        

    def run_task(self):
        
        self.cmd = sharedTasks['context']
        
        if self.cmd != None:
            os.system(self.cmd)
        else:
            print >> sys.stderr, "Please, define a command."
             
