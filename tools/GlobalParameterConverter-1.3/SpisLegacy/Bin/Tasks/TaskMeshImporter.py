"""
**File name:**    TaskMeshImporter.py

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

import sys, shutil, os
sys.path.append("..")

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedControls
from Bin.Tasks.shared         import sharedTasks

from FileChooserSwing         import choose
from org.spis.imp.ui.util     import FileDialog

from Modules.InOut.Gmsh2MeshStruct import Convert as Cv_Gmsh2MeshStruct

from com.artenum.free.mesh.io     import GmshLoader
from com.artenum.free.mesh        import Mesh
from Modules.Groups.MeshGroupList  import MeshGroupList

from Bin.config                    import GL_EXCHANGE, GL_DATA_PATH, GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)


class TaskMeshImporter(Task):
    """Call the mesh importer. This module will import a msh Gmsh file into the SPIS-UI mesh structure."""
    desc = "Meshing module"

    def run_task(self):
        
        if sharedFiles["project_directory"] == None:
            dialog = FileDialog(".")
        else :
            dialog = FileDialog(sharedFiles["project_directory"])
            
        if (dialog.showOpenDialog(None)):
           fileNameIn = dialog.getFileToSave().getAbsolutePath()
        print fileNameIn
        
        ###############################  
        # Mesh loading
        ###############################

        mesh = Mesh()
        try:
            print "Mesh Importing. Please wait..."
            #fileNameIn = os.path.join(dir, "Tmp3D.msh")
            fileNameOut = os.path.join(GL_EXCHANGE, "Tmp3D.msh")
            shutil.copyfile(fileNameIn, fileNameOut)
                
            mesh.load(GmshLoader(fileNameOut))
            shared['Mesh'] = mesh
            shared['MeshGroupList'] = MeshGroupList()
        except:
            print "Impossible to import mesh file", fileNameOut   

        # to avoid to re_mesh the mesh 
        sharedTasks["manager"].set_done_task("Mesher3D")
        
        
        
        
        
        
        
        
        '''
        FileName4 = str(choose(sharedFiles["project_directory"])).strip()
        
        try:
            fileNameOut = os.path.join(GL_EXCHANGE, "Tmp3D.msh")
            shutil.copyfile(FileName4, fileNameOut)
        except: 
            print >> sys.stdwarn, "No mesh file to refere."
            
        try:
            shared['MeshElmtList'], shared['OldNodeNumList'], shared['SkeletonElmtList'], \
            shared['OldSkeletonElmtNumList'], \
            shared['MeshGroupList'] = Cv_Gmsh2MeshStruct( [fileNameOut], \
            shared['cadimport'].GeoElementList, shared['cadimport'].GeoGroupList)
        
            # to brake the dependcy of the task manager
            sharedTasks["manager"].set_done_task("Mesher3D")
        except:
            print >> sys.stderr, "Humm... Apparently, there no mesh file to import."
            print >> sys.stderr, "Are you sure to have define a CAD input file before ?"


        print "memory clean up"
        import java.lang.System
        java.lang.System.gc()
        java.lang.System.runFinalization()
        '''
