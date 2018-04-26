"""
**Module Name:**  ToolCaller

**Project ref:**  Spis/SpisUI

**File name:**    ToolCaller.py

**File type:**    Class/Executable

:status:          Implemented

**Creation:**     05/12/2003

**Modification:** 12/12/2003  GR validation

**Use:**

**Description:**  Module of calling of external tools (e.g. CAD tool).

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Gerard Sookahet, Pascal Seng

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet                      | Extension/correction       |
|                | Gerard.Sookahet@artenum.com          |                            |
+----------------+--------------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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


import sys, os
from config import GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)

from Bin.config import GL_DATA_PATH, GL_CMD_GMSH, GL_CMD_TETGEN, GL_CMD_MEDIT

class ToolCaller:

    def __init__(self, Tool):
        self.BUILD_DATA_PATH = 'OFF'
        self.TheTool = Tool
        print '###############################'
        print '#  External Tool Caller       #'
        print '###############################'
        print 'Tool called:', self.TheTool
        print 'BUILD_DATA_PATH is', self.BUILD_DATA_PATH

    def call(self, FileNameIn, FileNameOut):
        self.FileNameTmp = FileNameIn
        if self.FileNameTmp == None:
            self.FileNameTmp = ''
        
        if self.BUILD_DATA_PATH == 'ON':
            self.FileName1_geo = os.path.join(GL_DATA_PATH, self.FileNameTmp)
        else:
            self.FileName1_geo = self.FileNameTmp
  
        print "thefile", self.FileName1_geo 
        self.cmd = self.TheTool +' '+ self.FileName1_geo
        try:
            print "I am trying the command... "+ self.cmd
            os.system(self.cmd)
        except:
            print "Impossible to execute commend "+ self.cmd + "Are you sure to have defined correctly all paths ?"
        else:
            print"External task done."


