"""
**File name:**    TaskReloadSolver.py

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

from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.common         import ask_value
from Bin.Tasks.TaskBuiltins   import *

import sys
sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR
sys.path.append(GL_SPISUIROOT_PATH)

from Bin.Tasks.Task           import Task

import os
EDITOR=GL_CMD_EDITOR+' '     #by default for 'emacs '


class TaskReloadSolver(Task):
    """
    Reload dynamically the solver. This function is usefull to relaod the 
    numerical kernel after edition and modification, without restart the whole
    framework. Please see the SPIS-UI User Manual for further informations. 
    """
    desc = "Solver reloading procedure"
    def run_task(self):
	print ""
	print "!-----------------------------------------------------!"
	print " BE CAREFULL: Method still under development !"
	print " An incorrect reloading may be possible. Please check"
	print " the consistency of the reloaded elements."
	print "!-----------------------------------------------------!"
	print ""
        reload_task('TaskJyTop')



