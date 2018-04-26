"""

**Project ref:**  Spis/SpisUI

**File name:**    TaskBuildAllVTKPipeline.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**Modification:**

**Use:**

**Description:**  This Task add a JyConsole in current desktop

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Sebastien Jourdain        | Definition/Creation        |
|                | jourain@artenum.com       |                            |
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

import os, sys, math, java
from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedFrames

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_JSYNOPTIC, GL_SYNOPTIC_EXCHANGE

class TaskCallJSynoptic(Task):
    """Call the Java 2D Plot Manager for JSynoptic."""
    desc="Build a 2D Plot Manager"

    def run_task(self):
        self.externalRun()
        
    def externalRun(self):
        
        #self.allDataField=sharedData['AllDataField']
        #self.allMeshField=sharedData['AllMeshField']
        
        badCharList = " ()[].:,;!~<>#"
        
        if sharedData['AllDataField'] != None:
                for dataField in sharedData['AllDataField'].List:
                    if dataField.Local == 4:
                        linkedMeshField = sharedData['AllMeshField'].GetMeshFieldById(dataField.MeshFieldId)
                        
                        tmpName = ""
                        for char in dataField.Name:
                            if char in badCharList:
                               char ="_"
                            tmpName = tmpName + char
                       
                        #self.fileNameOut = '"'+GL_SYNOPTIC_EXCHANGE+os.sep+dataField.Name+".txt"+'"'
                        self.fileNameOut = GL_SYNOPTIC_EXCHANGE+os.sep+tmpName+".txt"
                        #print self.fileNameOut
                        sys.stdout.write(".")
                        fileOut =  open(self.fileNameOut, 'w')
                        fileOut.write("# header\n")
                        for i in xrange(len(dataField.ValueList)):
                             tmpLine = `linkedMeshField.MeshElementList[i]`+" "+ `dataField.ValueList[i]`+"\n"
                             fileOut.write(tmpLine)
                        fileOut.close()
        print ""
        print "File convertion done"                
        
        cmd = GL_CMD_JSYNOPTIC+" "+GL_SYNOPTIC_EXCHANGE+os.sep+"*"
        #print cmd
        os.system(cmd)
        print "OK"
        
        
    def internalRun(self):
        from java.lang import System
        System.exit=self.EndTask()
        from jsynoptic.ui import Run
        Run.main([])       
          
          
    def EndTask(self):
         print "End of task"
