"""
Load SPIS-UI properties from a SPIS-UI project. Please see the
User Manual and/or the corresponding Technical Note for further information.

**File name:**    TaskLoadProperties.py

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
from TaskBuiltins       import *
from FileChooserSwing   import choose_dir
from Bin.Tasks.Task               import Task

from Modules.Field.DataFieldList        import DataFieldList
from Modules.Field.MeshField            import MeshField
from Modules.Field.MeshFieldList        import MeshFieldList
from Modules.Groups.MeshGroup           import MeshGroup

from Modules.Properties.PlasmaList      import PlasmaList
from Modules.Properties.MaterialList    import MaterialList
from Modules.Properties.ElecNodeList    import ElecNodeList

class TaskLoadProperties(Task):
    '''
    Load SPIS-UI properties from Python based format (e.g spis-project version 2). Please see the 
    User Manual and/or the corresponding Technical Note for further information. 
    '''
    desc = "Load SPIS-UI properties from Python based format (e.g spis-project version 2)."

    def run_task(self):
        '''
        Performs the task.
        '''            
        dirName = str(choose_dir(sharedFiles["project_directory"])).strip()
                
        if (dirName != None and dirName !="" and dirName !="None"):
            
            # we add the dir path to the path for the python modules loading
            sys.path.append(dirName)
            materialDir = dirName+os.sep+"Materials"
            sys.path.append(materialDir)
            elecNodeDir = dirName+os.sep+"ElecNodes"
            sys.path.append(elecNodeDir)
            plasmaDir = dirName+os.sep+"Plasmas"
            sys.path.append(plasmaDir)
            
            
            # loading of materials   
            print "Loading Python based materials catalog"
            selectedList = []
            sharedProp['defaultMaterialList'] = MaterialList()
            fileList = os.listdir(materialDir)
            for elm in fileList:
                if(elm[-3:]==".py"):
                  selectedList.append(elm)
            for pls in selectedList:
                   tmpName = pls[:-3]
                   try:
                       print "loading of ", pls
                       tmpCmd = "import "+tmpName
                       exec(tmpCmd)
                       tmpCmd = "sharedProp['defaultMaterialList'].Add_Material("+tmpName+".material)"
                       exec(tmpCmd)
                   except:
                       print >> sys.stderr, "Impossible to load ", tmpName
               
                
            # loading of electical Node   
            print "Loading Python based electrical nodes catalog"
            selectedList=[]
            sharedProp['defaultElecNodeList'] = ElecNodeList()
            fileList = os.listdir(elecNodeDir)
            for elm in fileList:
                if(elm[-3:]==".py"):
                  selectedList.append(elm)
            for pls in selectedList:
                   tmpName = pls[:-3]
                   try:
                       print "loading of ", pls
                       tmpCmd = "import "+tmpName
                       exec(tmpCmd)
                       tmpCmd = "sharedProp['defaultElecNodeList'].Add_ElecNode("+tmpName+".elecNode)"
                       exec(tmpCmd)
                   except:
                       print >> sys.stderr, "Impossible to load ", tmpName
                
                
            # loading of plasmas   
            print "Loading Python based plasma catalog"
            selectedList=[]
            sharedProp['defaultPlasmaList']=PlasmaList()
            fileList = os.listdir(plasmaDir)
            for elm in fileList:
                if(elm[-3:]==".py"):
                  selectedList.append(elm)
            for pls in selectedList:
                   tmpName = pls[:-3]
                   try:
                       print "loading of ", pls
                       tmpCmd = "import "+tmpName
                       exec(tmpCmd)
                       tmpCmd = "sharedProp['defaultPlasmaList'].Add_Plasma("+tmpName+".plasma)"
                       exec(tmpCmd)
                   except:
                       print >> sys.stderr, "Impossible to load ", tmpName
        
