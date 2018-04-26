"""
**File name:**    TaskLoadGroups.py

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

from Modules.Groups.GeoGroupList        import GeoGroupList

from org.spis.imp.ui.util import DirectoryDialog

class TaskLoadGroups(Task):
    '''
    Load groups from a SPIS-UI project. 
    '''
    desc = "Load groups from a SPIS-UI project."
    def run_task(self):
        
        #filename = str(choose(sharedFiles["project_directory"])).strip()
        #load_dict(sharedGroups, filename)
        
        dialog = DirectoryDialog(sharedFiles["project_directory"])
        if (dialog.showDialog(None)):
            self.dirName = dialog.getFileToSave().getAbsolutePath()
            sys.path.append(self.dirName)
            
        print "Path: ", self.dirName
        ############################   
        # load groups 
        ############################
        selectedList = []
        sharedGroups['GeoGroupList'] = GeoGroupList()
        fileList = os.listdir(self.dirName)
        print "File list ", fileList
        for elm in fileList:
            if(elm[-3:]==".py"):
                selectedList.append(elm)
            
        for pls in selectedList:
            tmpName = pls[:-3]
            try:
                print "loading ", pls
                tmpCmd = "import "+tmpName
                exec(tmpCmd)
                tmpCmd = "sharedGroups['GeoGroupList'].Add_Group("+tmpName+".group)"
                exec(tmpCmd)
                
                
                tmpCmd = "self.tmpGrpId = "+tmpName+".group.Id"
                exec(tmpCmd)
                tmp = sharedGroups['GeoGroupList'].GetElmById(self.tmpGrpId)
                if tmp == None:
                    print >> sys.stderr, "Error to recover current Geo group"
                else:
                    self.tmpGrp = tmp
                
                tmp = sharedProp["defaultPlasmaList"].GetElmById(self.tmpGrp.Plasma.Id)
                print tmp.Name
                print tmp.Id

                if tmp == None:
                    print >> sys.stderr, "Warning in Plasma property re-connection."
                else:
                    self.tmpGrp.Plasma = tmp
                tmp = sharedProp["defaultMaterialList"].GetElmById(self.tmpGrp.Material.Id)
                if tmp == None:
                    print >> sys.stderr, "Warning in Material property re-connection."
                else:
                    self.tmpGrp.Material = tmp
                tmp = sharedProp["defaultElecNodeList"].GetElmById(self.tmpGrp.ElecNode.Id)
                if tmp == None:
                    print >> sys.stderr, "Warning in ElectNode property re-connection."
                else:
                    self.tmpGrp.ElecNode = tmp
            except:
                print >> sys.stderr, "Impossible to load ", tmpName
    
