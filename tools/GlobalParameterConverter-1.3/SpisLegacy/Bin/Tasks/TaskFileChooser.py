"""
**File name:**    TaskFileChooser.py

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
| 4.0.0   | Sebastien Jourdain                   | Creation                   |
|         | jourdain@artenum.com                 |                            |
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
from Bin.Tasks.Task           import Task
import Bin.Tasks.common
from Bin.Tasks.common         import ask_yesno
import FileChooserSwing
from org.spis.imp.ui.util import FileDialog

#sharedTasks

class TaskFileChooser(Task):
    """Task 8: Choose the input CAD file (Swing based GUI)."""
    desc = "File chooser (Swing based GUI)"


    def run_task(self):
        '''Execute the task'''
        crtl = "n"
        if (sharedFiles['TheCADFileIn'] != None):
           if (sharedTasks["context"] != 0):
               strTmp = "<html>Huummm... It seems that you have already a CAD file loaded (probably from a project). <br>Are you sure to keep the same one ? [y]/n </html>"
               crtl = ask_yesno(1, strTmp)
           else:
               crtl = "y"

        if (crtl != "y"):
           
           dialog = FileDialog()
           if (dialog.showOpenDialog(None)):
               sharedFiles['TheCADFileIn'] = dialog.getFileToSave().getAbsolutePath()
               print "Chosen file = "+sharedFiles['TheCADFileIn']
           else:
              sharedFiles['TheCADFileIn'] = None
        else:
            print "Ok, we keep the same CAD"
           
