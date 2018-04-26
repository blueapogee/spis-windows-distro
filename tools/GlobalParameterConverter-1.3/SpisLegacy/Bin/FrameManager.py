"""
Help to provide JInternal frames into the current Desktop. 

**Creation:**     2009/01/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      1.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Julien Forest                        | Creation                   |
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


import os, shutil, sys

from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.shared         import sharedTasks
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedFlags

from Bin.Tasks.common         import create_internal_frame
from Bin.config               import GL_EXCHANGE, GL_CMD_GMSH, GL_CMD_EDITOR


import javax.swing 
from javax.swing              import JOptionPane
from pawt                     import swing, colors
#from java.lang                import Thread, System
from javax.swing              import *
from java.awt                 import *
from java.io                  import File
from java.awt.event           import ItemEvent

from org.spis.imp.ui.util import FileDialog

class FrameManager:
    
    def __init__(self):
        pass
        
    def setGuicontext(self, guiContextIn):
        
        self.guiContext = guiContextIn
        
    def getNewFrame(self):
        """
        generate a new frame. If the shared GUI context equal 1, a JInternalGrame from the current desktop is returned.
        If the shared GUI context equal -1, a JFrame is returned. Otherwise, None is return.
        """
        self.getNewFrame("")
        
    def getNewFrame(self, frameNameIn):
        """
        generate a new frame named frameIn. If the shared GUI context equal 1, a JInternalFrame from the current desktop is returned.
        If the shared GUI context equal -1, an independant JFrame is returned. Overwise, None is return.
        """
        frameOut = None
        if self.guiContext == -1:
            frameOut = JFrame(frameNameIn)
        elif self.guiContext == 1:
            frameOut = create_internal_frame(frameNameIn,sharedFrames["gui"].getCurrentDesktop())
        else:
            print "Impossible to generate a frame."
        return(frameOut)
