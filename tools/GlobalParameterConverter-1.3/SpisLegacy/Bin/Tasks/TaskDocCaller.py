"""
**File name:**    TaskToolCaller.py

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


from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.common         import ask_value
from Bin.ToolCaller           import ToolCaller

import sys, os
from Bin.config         import GL_CMD_DOCVIEWER, GL_DOC_PATH
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_EXCHANGE, GL_SYSTEM

class TaskDocCaller(Task):
    """Call the document viewer."""
    desc = "Documentation caller (Multivalent)"

    def run_task(self):
        
        if GL_SYSTEM != 'posix':
            fileOut = open(GL_EXCHANGE+os.sep+"callDoc.bat", 'w')
            print GL_EXCHANGE+os.sep+"callDoc.bat"
            docPath = os.path.join(GL_DOC_PATH,'index.html')
            if GL_CMD_DOCVIEWER == None: 
                fileOut.write(docPath)
            else:
                fileOut.write('"'+GL_CMD_DOCVIEWER+'" '+docPath)
            fileOut.close()
            os.system(GL_EXCHANGE+os.sep+"callDoc.bat")
        else:
            self.theCaller = ToolCaller(GL_CMD_DOCVIEWER)
            docPath = os.path.join(GL_DOC_PATH)
            if (os.path.isdir(docPath)):
               docPath = os.path.join(GL_DOC_PATH,'index.html') 
            else:
               # docPath = "http://195.101.59.123/projects/spine/home/spis/documentation/"
               docPath = "../Doc/index.html"
            self.theCaller.call(docPath,'')
            
            
