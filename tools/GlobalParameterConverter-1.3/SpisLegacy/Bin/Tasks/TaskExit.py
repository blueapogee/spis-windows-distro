"""

**Project ref:**  Spis/SpisUI

**File name:**    TaskBuildAllVTKPipeline.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**Modification:**

**Use:**

**Description:**  This Task is used to build all the vtk pipeline of
		  visualization.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Arsene Lupin              | Definition/Creation        |
|                | lupin@artenum.com         |                            |
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

import sys, java
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared, sharedFlags, sharedFrames
from javax.swing              import JOptionPane
from Bin.Tasks.common         import create_internal_frame

from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE, GL_CASSANDRA_PLUGINS


class TaskExit(Task):
	"""Exit task"""
	desc="Exit the Spis system."

	def run_task(self):
            loadingLogger = LoggerFactory.getLogger("CoreLogger")
            if sharedFlags['guiMode'] == 1:
                InternalFrame = create_internal_frame("Warning",sharedFrames["gui"].getCurrentDesktop())
                dialogueMessage = "<html>Do you really want to quit SPIS?</html>"
                response = JOptionPane.showConfirmDialog( InternalFrame, dialogueMessage, "Quit SPIS", JOptionPane.YES_NO_OPTION)
                if response == 0:
                    loadingLogger.info("Exit SPIS. Bye!")
                    # Ok, I know. I am a little bite violent...
                    java.lang.System.exit(1)
            


