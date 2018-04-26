"""
Task CAD import module.

**File name:**    TaskCADImporter.py

**Creation:**     2010/02/02

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Yves Le Rumeur

:version:      3.0.0

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

import sys, os
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory

from Bin.Tasks.Task           import Task
#from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.shared         import sharedFlags
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedControls 
from Bin.Tasks.shared         import sharedGroups

from Bin.Tasks.common         import create_internal_frame

from javax.swing              import JOptionPane

from Bin.config               import GL_DATA_PATH, GL_SPISUIROOT_PATH

from Bin.CADImporter          import CADImporter
from Bin.GeomManager          import GeomManager

class TaskCADImporter(Task):
    """Task CAD import module. Call the GEOM manager."""
    desc = "CAD import module"
    
    def run_task(self):
        '''
        Performs the task.
        '''
        self.logger = LoggerFactory.getLogger("Task")
        
        if (sharedFiles['TheCADFileIn'] == None):
            self.logger.error("Error in TaskCADImporter: No main GEOM file defined! GEOM manager automatically called-back (if GUI mode is ON) \n or please choose an input CAD file.")
            if sharedFlags['guiMode'] == 1:
                self.geoManager = GeomManager()
                self.geoManager.setExternalMethod(self.geomManagerControler)
                self.geoManager.buildGUI()
                self.geoManager.show()
        else:
            self.importFile()
            
            
    def geomManagerControler(self):
        '''
        Set the GUI context and initiate the GEOM manager. 
        '''
        if sharedFlags['guiMode'] == 1:
            InternalFrame = create_internal_frame("Error",sharedFrames["gui"].getCurrentDesktop())
            dialogueMessage = "<html>Do you wish to load this file ?</html>"
            response = JOptionPane.showConfirmDialog( InternalFrame, dialogueMessage, "GEOM file loading", JOptionPane.YES_NO_OPTION)
            if response == 0:
                self.importFile()
                self.geoManager.close()
            
            
    def importFile(self):
        '''
        Import the file designed as main file by the GEOM manager. 
        '''
        self.logger.info("Loading GEOM file: "+sharedFiles['TheCADFileIn'])
        try:
            os.remove('tmp.geo')
        except:
            self.logger.debug("No tmp.geo file. Created.")
            sharedFiles['TheCADFileOut'] = 'tmp.geo'
            
        importer = CADImporter()
        if importer.importCAD(sharedFiles['TheCADFileIn'], sharedFiles['TheCADFileOut']):
            # if we have no project pre-defined or not 
            # if not, we reload the groups according the CAD
            if ( sharedControls['groupLoadingFlag'] < 1):
                self.logger.info("Loading groups settings from GEOM file.")
                sharedGroups['GeoGroupList'] = importer.GeoGroupList 
        else:
            self.logger.error("Error in geometric model loading! No Geo Groups defined! Please call the Geom Manager and set the Geo Groups in the geometric model.")


