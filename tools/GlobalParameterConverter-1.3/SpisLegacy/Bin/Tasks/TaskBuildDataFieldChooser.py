"""
**File name:**    TaskBuildDataFieldChooser.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      4.1.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 4.1.0   | Julien Forest                        | Modif                      |
|         | contact@artenum.com                  |                            |
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

#import sys
#import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

#from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH
from Bin.Tasks.Task           import Task


class TaskBuildDataFieldChooser(Task):
    '''
    Task called to load a SPIS-UI project. 
    '''
    desc="Build DataFieldChooser"
    
    def run_task(self):

        self.logger = LoggerFactory.getLogger("Task")
        
        #self.logger("Launching of the DataField manager")

        # to be able to reload dynamically the module
        import Bin.FieldDataListViewer2
        reload (Bin.FieldDataListViewer2)
        from Bin.FieldDataListViewer2 import FieldDataListViewer2

        self.datafieldviewer = FieldDataListViewer2()










