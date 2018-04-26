"""
**File name:**    TaskSaveGroups.py

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

import os
from Bin.Tasks.shared             import *
from Bin.Tasks.TaskBuiltins       import *
from Bin.Tasks.Task               import Task

from org.spis.imp.ui.util import DirectoryDialog

import Modules.InOut.GeoGroupPyWriter
from Modules.InOut.GeoGroupPyWriter import GeoGroupPyWriter

class TaskSaveGroups(Task):
    '''
    Save the geometrical and mesh groups.
    '''
    desc = "Save the geometrical and mesh groups"
    
    def run_task(self):
        '''
        Performs the task to save individualy the set of defined geo groups.
        '''            

        if sharedFiles["project_directory"] != None:
            dialog = DirectoryDialog(sharedFiles["project_directory"])
        else:
            dialog = DirectoryDialog()
            
        if (dialog.showDialog(None)):
            dirName = dialog.getFileToSave().getAbsolutePath()
            print "Groups saving"
            
            if not os.path.isdir(dirName):
                os.makedirs(dirName)
            
            if sharedGroups != None:
                for grp in sharedGroups['GeoGroupList'].List:
                    tmpName = "geoGroup"+`grp.Id`+".py"
                    print "saving of "+ tmpName
                    fileNameOut = os.path.join(dirName, tmpName)
                    print fileNameOut
                    try:
                        wr = GeoGroupPyWriter(grp)
                        wr.setOutputFileName(fileNameOut)
                        wr.readStructure()
                        wr.write()
                        wr = None
                    except:
                        print >> sys.stderr,"ERROR : Impossible to save group", grp.Name     
            else:
                print >> sys.stdwarn,"WARNNING 204 (TaskSaveProj): No groups to save."
    
        
        
        
        
