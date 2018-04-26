"""
**File name:**    TaskExportAllDAF.py

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
from Bin.Tasks.shared         import sharedData

import sys
from Bin.DataExporter.ExporterControler import Controler

from threading import Thread
from Bin.config           import GL_MAX_THREADS_STACK

class TaskExportAllDF(Task):
    """
    ....
    """
    desc = "..."
    
    def run_task(self):
        '''
        Performs the task.
        '''
        # ctr = Controler()
	# #by default, data exproted into the project directory.
	# #ctr.projectPath="/Users/julien/AAA_exportAllTest"
	# ctr.exportListOfDataFields(sharedData["AllDataField"].Dic.keys())

        # FIX ME : multi-threading not supported by project cotnrol file and mesh
	# file. Should be move into the project manager. 
        nbMaxThreads = 1 #GL_MAX_THREADS_STACK
	NbRunningThreads = 0

        sizeListOfData = len(sharedData["AllDataField"].Dic.keys())

        for thrId in xrange(nbMaxThreads):
            indexStart = (thrId*sizeListOfData)/nbMaxThreads
	    if thrId*(sizeListOfData+1)/nbMaxThreads < sizeListOfData:
	        indexEnd = (thrId+1)*sizeListOfData/nbMaxThreads
            else:
		indexEnd = sizeListOfData
	    tmpList = sharedData["AllDataField"].Dic.keys()[indexStart:indexEnd]
	    print `indexStart`, `indexEnd`
	    exportData = MultiExporter()
	    exportData.setList(tmpList)
	    NbRunningThreads = NbRunningThreads + 1

            print NbRunningThreads
	    #print tmpList
	    
	    exportData.setThreadCont(NbRunningThreads)
            exportData.start()
	print "DONE"
       
class MultiExporter(Thread):
      def __init__(self):
         Thread.__init__(self)
	 self.ctr = Controler()
	 self.list = None
	 self.threadsCont = 1
	 
      def setList(self, list):
          self.list = list
	  
      def setThreadCont(self, cont):
          self.threadsCont = cont

      def decreasesThreadsCont(self):
          self.threadsCont = self.threadsCont - 1

      def run(self):
	  self.ctr.exportListOfDataFields(self.list)
	  self.decreasesThreadsCont()
