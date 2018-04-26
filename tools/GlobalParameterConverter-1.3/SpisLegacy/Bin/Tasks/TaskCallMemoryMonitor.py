"""

**Project ref:**  Spis/SpisUI

**File name:**    TaskBuildAllVTKPipeline.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**Modification:**

**Use:**

**Description:**  This Task add a JyConsole in current desktop

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Sebastien Jourdain        | Definition/Creation        |
|                | jourain@artenum.com       |                            |
+----------------+---------------------------+----------------------------+

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

from Bin.Tasks.Task           import Task
from Bin.Tasks.common         import create_internal_frame
from Bin.Tasks.shared         import sharedFrames

#from java.lang                import Thread, System
from java.awt                 import BorderLayout

class TaskCallMemoryMonitor(Task):
    """Java memory monitor"""
    desc="Build a MemoryMonitor"

    def run_task(self):
        theInternaFrame = create_internal_frame("Memory monitor - Artenum",sharedFrames["gui"].getCurrentDesktop())
        theInternaFrame.setVisible(0);
        theInternaFrame.reshape( 579, 0, 440, 350)

        from com.artenum.tk.ui import MemoryMonitor
                
        monitor = MemoryMonitor()
        theInternaFrame.getContentPane().setLayout(BorderLayout())
        theInternaFrame.getContentPane().add(monitor,BorderLayout.CENTER)
        theInternaFrame.setVisible(1);
                
