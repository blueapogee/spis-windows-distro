"""
**File name:**    TaskSaveProperties.py

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
# </autoheader>

import os

from Bin.Tasks.shared             import *
from Bin.Tasks.TaskBuiltins       import *
from Bin.Tasks.FileChooserSwing   import choose_save
from Bin.Tasks.Task               import Task

from Modules.InOut import PlasmaPyWriter
from Modules.InOut.PlasmaPyWriter import PlasmaPyWriter

from Modules.InOut import ElecNodePyWriter
from Modules.InOut.ElecNodePyWriter import ElecNodePyWriter

import Modules.InOut.MaterialPyWriter
from Modules.InOut.MaterialPyWriter import MaterialPyWriter

from org.spis.imp.ui.util import DirectoryDialog

class TaskSaveProperties(Task):
    '''
    Saves the properties on file.
    '''
    desc = "Save the propoerties applied to the groups"
    def run_task(self):
            
        fileFomat = None
         
        dialog = DirectoryDialog( sharedFiles["project_directory"]+os.sep+"spis-props" )
        dialog.addFileType(".v2", "Version 2.0")
        if (dialog.showDialog(None)):
            if (dialog.getSelectedFileTypeDescription() == 'Version 2.0'):
                print "V2"
                fileFomat = "V2"
            dirName = dialog.getFileToSave().getAbsolutePath()
            
        print "Saving of the materials and properties"
        if sharedProp != None and fileFomat == "V2":
            if not os.path.isdir(dirName+os.sep+"Materials"):
                os.makedirs(dirName+os.sep+"Materials")
            if not os.path.isdir(dirName+os.sep+"ElecNodes"):
                os.makedirs(dirName+os.sep+"ElecNodes")
            if not os.path.isdir(dirName+os.sep+"Plasmas"):
                os.makedirs(dirName+os.sep+"Plasmas")        
            
            print "Export of materials as Jython modules"
            try:
                for mat in sharedProp['defaultMaterialList'].List:
                     tmpName = "material"+`mat.Id`+".py"
                     print "saving of "+ tmpName
                     fileNameOut = os.path.join(dirName, "Materials", tmpName)
                     wr = MaterialPyWriter(mat)
                     wr.setOutputFileName(fileNameOut)
                     wr.readStructure()
                     wr.write()
                     wr = None
            except:
                print "No material to save"
                 
            print "Export of electical nodes as Jython modules"
            try:
                for elec in sharedProp['defaultElecNodeList'].List:
                     tmpName = "elecNode"+`elec.Id`+".py"
                     print "saving of "+ tmpName
                     fileNameOut = os.path.join(dirName, "ElecNodes", tmpName)
                     wr = ElecNodePyWriter(elec)
                     wr.setOutputFileName(fileNameOut)
                     wr.readStructure()
                     wr.write()
                     wr = None
            except:
                 print "No elecNode to save"
        
            print "Export of plasmas as Jython modules"
            try:
                for plasma in sharedProp['defaultPlasmaList'].List:
                     tmpName = "plasma"+`plasma.Id`+".py"
                     print "saving of "+ tmpName
                     fileNameOut = os.path.join(dirName, "Plasmas", tmpName)
                     wr = PlasmaPyWriter(plasma)
                     print fileNameOut
                     wr.setOutputFileName(fileNameOut)
                     wr.readStructure()
                     wr.write()
                     wr = None
            except:
                print "No plasma to save"
        else:
            print >> sys.stdwarn,"WARNNING 203 (TaskSaveProj): No properties to save."      
