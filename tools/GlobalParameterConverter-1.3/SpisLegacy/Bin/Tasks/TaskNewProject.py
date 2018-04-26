"""
**File name:**    TaskNewProject.py

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

from Bin.Tasks.shared             import *
from Bin.Tasks.TaskBuiltins       import *
from FileChooserSwing   import *
from Bin.Tasks.common             import *
from Bin.Tasks.Task               import Task

import os
from threading import Condition
import pawt
import java

from java.awt           import BorderLayout

class InputDialogSpe:
    def __init__(self, cond, shared, internal_frame):
        self.cond = cond
        self.shared = shared
        self.frame = internal_frame
        self.frame.setSize(200, 100)
        self.text = pawt.swing.JTextField()
        self.button2 = pawt.swing.JButton('Browse', actionPerformed=self.browse)
        self.button = pawt.swing.JButton('OK', actionPerformed=self.answer)
        self.frame.contentPane.add(self.button, BorderLayout.EAST)
        self.frame.contentPane.add(self.button2, BorderLayout.SOUTH)
        self.frame.contentPane.add(self.text, BorderLayout.CENTER)
        self.frame.show()
        self.frame.validate()

    def browse(self, m):
        filename = str(choose_dir(sharedFiles["project_directory"])).strip()
        self.text.setText(filename)

    def answer(self, m):
        self.shared.append(self.text.getText())
        self.cond.acquire()
        self.cond.notifyAll()
        self.cond.release()
        self.frame.dispose()


class TaskNewProject(Task):
    '''
    Create a new Project.
    '''
    desc = "Create a new Project"
    def run_task(self):
        print "Choose in which directory you want to save the project."
        frame = create_internal_frame("Directory chooser", sharedFrames["desktop_pane"])

        cond = Condition()
        str = []
        m = InputDialogSpe(cond, str, frame)
        cond.acquire()
        cond.wait()
        dir = str[0]
        
        sharedFiles["project_directory"] = dir
        if not os.path.isdir(dir):
            os.makedirs(dir)
        
        self.fileName = dir+os.sep+"__init__.py"
        fileOut = open(self.fileName, 'w')
        fileOut.write("")
        fileOut.close()
        
        if not os.path.isdir(dir+os.sep+"vtk"):
            os.makedirs(dir+os.sep+"vtk")
        if not os.path.isdir(dir+os.sep+"DataFields"):
            os.makedirs(dir+os.sep+"DataFields")
        if not os.path.isdir(dir+os.sep+"Properties"):
            os.makedirs(dir+os.sep+"Properties")
        if not os.path.isdir(dir+os.sep+"Properties"+os.sep+"Materials"):
            os.makedirs(dir+os.sep+"Properties"+os.sep+"Materials")
        if not os.path.isdir(dir+os.sep+"Properties"+os.sep+"ElecNodes"):
            os.makedirs(dir+os.sep+"Properties"+os.sep+"ElecNodes")
        if not os.path.isdir(dir+os.sep+"Properties"+os.sep+"Plasmas"):
            os.makedirs(dir+os.sep+"Properties"+os.sep+"Plasmas")
        if not os.path.isdir(dir+os.sep+"Reporting"):
            os.makedirs(dir+os.sep+"Reporting")
        if not os.path.isdir(dir+os.sep+"Images"):
            os.makedirs(dir+os.sep+"Images")
        frame.dispose()
        
