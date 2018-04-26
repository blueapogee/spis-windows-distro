"""
**File name:**    TaskLoadCAD.py

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

import sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.shared             import *
from TaskBuiltins       import *
from FileChooserSwing   import choose
from Bin.Tasks.Task               import Task
from org.spis.imp.ui.util import FileDialog

class TaskLoadCAD(Task):
    '''
    Load the main CAD file into the framework and build up the 
    complete GEOM model. 
    '''
    desc = "Load the  CAD structure"
    def run_task(self):
        
        self.logger = LoggerFactory.getLogger("Task") 
            
        print "cadimport=", shared['cadimport']        
        if (shared['cadimport'] != None):
           self.logger.error(  "Hummm... It seems that you have already imported a CAD file.\n"
                             + "If you wish to re-load a CAD file from scratch, please re-start the framework. \n")
           sharedFlags['importFlag'] = 0
        else:
           sharedFlags['importFlag']  = 1
        
        if sharedFlags['importFlag'] == 1:
           # sharedFiles["project_directory"]
           dir = sharedFiles["project_directory"]
           if dir == None:
              dir = "."
           dialog = FileDialog(dir)
           if (dialog.showOpenDialog(None)):
               filename = dialog.getFileToSave().getAbsolutePath()
               load_dict(sharedFiles, filename)
        else: 
           self.logger.debug("Ok, we continue with the same CAD file.")
