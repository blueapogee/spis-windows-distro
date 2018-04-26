"""
**File name:**    TaskSolverInit.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Julien forest                        | Creation                   |
|         | julien.forest@artenum.com            |                            |
+---------+--------------------------------------+----------------------------+
| 3.2.0   | Julien forest                        | Modif                      |
|         | julien.forest@artenum.com            |                            |
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
from Bin.Tasks.shared         import sharedSolver, sharedNum
import java.lang.System

class TaskSolverInit(Task):
    '''
    initialises the numerical kernel.
    '''
    desc = "Solver Initialisation"
    def run_task(self):
        print self.desc
        import Bin.SpisNumCaller
        reload(Bin.SpisNumCaller)
        from Bin.SpisNumCaller import SpisNumCaller

        sharedSolver['SpisNumCaller'] = SpisNumCaller(sharedNum['SNMesh'])
        sharedSolver['SpisNumCaller'].runAsInternalTaks()

        # to optimise the garbage collector action and then 
        # reduce the memory foot print
        java.lang.System.runFinalization()
