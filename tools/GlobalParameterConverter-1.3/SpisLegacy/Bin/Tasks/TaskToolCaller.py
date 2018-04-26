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

import sys, os
from Bin.config import GL_CMD_GMSH
sys.path.append(GL_CMD_GMSH)


import sys
sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR, GL_EXCHANGE
sys.path.append(GL_SPISUIROOT_PATH)


class TaskToolCaller(Task):
    """Generic CAD tool caller. Call the default CAD/GEOM tool."""
    desc = "CAD tool caller (gmsh)"
    def run_task(self):
        
        if not sharedFiles['TheCADFileIn']:
            print >> sys.stderr, "No GEOM file pre-defined. Default file defined as follow:"
            sharedFiles['TheCADFileIn'] = GL_EXCHANGE+os.sep+"cad_sav.geo"
            print "File to load:", sharedFiles['TheCADFileIn']
            try:
               tmpFile = open(sharedFiles['TheCADFileIn'], "w")
               tmpFile.write(" ")
               tmpFile.close()
            except:
               print >> sys.stderr, "ERROR in initialisation of tmp file"
        
        #self.tmp =  '"'+sharedFiles['TheCADFileIn']+'"'+ ' '
         
        #EDITOR = GL_CMD_EDITOR+' '     #by default Jext
        #ACTION = EDITOR+self.tmp+' &'
        #ACTION = ACTION+GL_CMD_GMSH+' '+self.tmp+' &'
        #os.system(ACTION)
        
        
        os.java.lang.Runtime.getRuntime().exec(GL_CMD_EDITOR+' '+sharedFiles['TheCADFileIn'])
        os.java.lang.Runtime.getRuntime().exec(GL_CMD_GMSH+' '+sharedFiles['TheCADFileIn'])
        
