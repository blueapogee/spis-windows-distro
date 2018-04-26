"""
Call the DataBus Cleaner to manage data in the common DataBus of SPIS-UI.

**Project ref:**  Spis/SpisUI

**File name:**    TaskDataBusCleaner.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

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


from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import *

from Bin.dataBusManager import dataBusManager

import sys
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE, GL_CASSANDRA_PLUGINS

class TaskDataBusCleaner(Task):
    """Call the Data Bus Manager. Tool to manage and clean up the Commmon Data Bus."""
    desc="Tool to manage and clean up the Commmon Data Bus"
    def run_task(self):
        '''
        Performs the Task.
        ''' 
        dbm = dataBusManager()

