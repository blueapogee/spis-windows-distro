"""
**File name:**    TaskMesher.py

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
from Bin.Tasks.shared         import sharedControls
from Bin.Tasks.common         import ask_value

from Bin.Mesher import Mesher

import sys
sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)

class TaskMesher(Task):
    """Task Mesher: call the meshing module"""
    desc = "Meshing module"
    
    def run_task(self):
        '''
        runs the task.
        '''
        TheMesher = Mesher()

        # temporary
        sharedControls['dimMesh'] = None

        if sharedControls['dimMesh'] == None:
            print '      Choose the type of meshing:'
            print '         1 - 2D surfacic'
            print '         2 - 3D volumic'
            self.control = raw_input()
        else:
            self.control = sharedControls['dimMesh']

        TheMeshFile='tmp.msh'
        FileName4 = TheMeshFile
        if self.control == '1':
            #2D meshing
            TheMesher.mesh2D(sharedFiles['TheCADFileOut'], TheMeshFile)
            print "meshing file=", FileName4
        elif self.control == '2':
            #3D meshing
            TheMesher.mesh3DwithGmsh(sharedFiles['TheCADFileOut'], TheMeshFile)
            print "meshing file=", FileName4
        else:
            print "Please choose your meshing type."


        ################################################################
        #                     Import of the Mesh                       #
        ################################################################

        print 'XXX  ',FileName4,' IS BEING IMPORTED XXX'
        print

        shared['MeshElmtList'], shared['OldNodeNumList'],\
        shared['SkeletonElmtList'], \
        shared['OldSkeletonElmtNumList'], \
        shared['MeshGroupList'] = Cv_Gmsh2MeshStruct([FileName4], \
        shared['cadimport'].GeoElementList, shared['cadimport'].GeoGroupList)

        ################################################################
        #               control of Skeletons (if asked)                   #
        ################################################################
        print
        print 'Do you want to display information about skeletons elements ? (y/[n])'
        self.control = ask_value(self.mycond)

        if self.control == 'y':
            TheMesher.PrintInfoOnSkeleton(shared['SkeletonElmtList'])

        ################################################################
        #               control of MeshElements (if asked)             #
        ################################################################
        print
        print 'Do you want to display information about mesh elements ? (y/[n])'
        self.control = ask_value(self.mycond)

        if self.control == 'y':
             print '   Please give a dimension between 0 to 3 or type \"a\" for all types.'
        self.control = ask_value(self.mycond)

        if self.dim == 'a':
            TheMesher.PrintInfoOnMeshElements(0, shared['MeshElmtList'])
            TheMesher.PrintInfoOnMeshElements(1, shared['MeshElmtList'])
            TheMesher.PrintInfoOnMeshElements(2, shared['MeshElmtList'])
            TheMesher.PrintInfoOnMeshElements(3, shared['MeshElmtList'])
        else:
            TheMesher.PrintInfoOnMeshElements(string.atoi(self.dim), shared['MeshElmtList'])
