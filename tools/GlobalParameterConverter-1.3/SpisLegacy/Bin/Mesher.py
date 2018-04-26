"""
**Module Name:**  Mesher

**Project ref:**  Spis/SpisUI

**File name:**    Mesher.py

**File type:**    Class/Executable

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 12/12/2003  GR validation

**Use:**

**Description:**  Import a CAD structure from a GEO file into a the Spis CAD structure

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Maxime Biais

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                         | Creation                   |
|                | Arsene.Lupin@Artenum.com             |                            |
+----------------+--------------------------------------+----------------------------+
| 0.2.0          | Maxime Biais                         | Extension/correction       |
|                | Maxime.Biais@artenum.com             |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | Maxime Biais                         | Bugs correction            |
|                | Maxime.Biais@artenum.com             |                            |
+----------------+--------------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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

import sys, os, string
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from config import GL_SPISUIROOT_PATH

from Modules.InOut.GmshGeo2GeoStruct import Convert as Cv_GmshGeo2GeoStruct
from Modules.InOut.GeoStruct2Gmsh import Convert as Cv_GeoStruct2Gmsh
from Modules.InOut.Gmsh2MeshStruct import Convert as Cv_Gmsh2MeshStruct
from Modules.InOut.MeshStruct2Gmsh import Convert as Cv_MeshStruct2Gmsh
from Modules.InOut.MeshStruct2Tetgen import Convert as Cv_MeshStruct2Tetgen
from Bin.config import GL_DATA_PATH, GL_CMD_GMSH, GL_CMD_TETGEN, GL_CMD_MEDIT, GL_GMSH_OUT_PATH

from com.artenum.free.mesh.io  import GmshLoader
from com.artenum.free.mesh     import Mesh

class Mesher:

    def __init__(self):
        self.logger = LoggerFactory.getLogger("MeshLogger")
        self.BUILD_DATA_PATH = 'ON'
        
        self.MESH_OUTPUT_FORMAT_FLAG = '-format msh1'

        self.GMSH_MESHING_OPT = self.MESH_OUTPUT_FORMAT_FLAG

    def mesh2D(self, FileNameIn, FileNameOut):
        if self.BUILD_DATA_PATH == 'ON':
            self.FileName1_geo = os.path.join(GL_DATA_PATH, FileNameIn)
        else:
            self.FileName1_geo = FileNameIn

        #definition of the file exchange
        if FileNameOut=='':          #### faire aussi un test pour le cas || FileOut==None:
            self.FileOutTmp=FileNameIn+'.tmp.msh'
            self.logger.debug("No pre-defined output mesh file. Meshing will saved into "+self.FileOutTmp)
        else:
            self.FileOutTmp=FileNameOut

        if self.BUILD_DATA_PATH == 'ON':
            self.FileName3_msh = os.path.join(GL_DATA_PATH, 'Tmp2D.msh')
        else:
            self.FileName3_msh = self.FileOutTmp
        self.FileName3_out=self.FileName3_msh+"out"

        if self.BUILD_DATA_PATH == 'ON':
            self.FileName4Out=GL_GMSH_OUT_PATH+'/Tmp2D.msh'
        else:
            self.FileName4Out=self.FileOutTmp

        # definition of the meshing command 
        self.cmd = GL_CMD_GMSH + ' ' + self.GMSH_MESHING_OPT + ' ' + ' -2 '+self.FileName1_geo+' -o '+self.FileName4Out+' > '+self.FileName3_out
        try:
            self.logger.info("I am trying the command... "+ self.cmd)
            os.system(self.cmd)
        except:
            self.logger.errror("Impossible to execute command "+ self.cmd 
                               + "Are you sure to have defined correctly all paths to Gmsh (ThirdPart component) ?")
        else:
            self.logger.info("Mesh 2D done.")
        return self.FileName3_msh



    def mesh3DwithGmsh(self, FileNameIn, FileNameOut):
        if self.BUILD_DATA_PATH == 'ON':
            self.FileName1_geo = os.path.join(GL_DATA_PATH, FileNameIn)
        else:
            self.FileName1_geo = FileNameIn
        self.logger.info("3D meshing with Gmsh from "+self.FileName1_geo)

        # create 3D meshing

        #definition of the file exchange
        if FileNameOut=='':          #### faire aussi un test pour le cas || FileOut==None:
            self.FileOutTmp=FileNameIn+'.tmp.msh'
            self.logger.debug("No predfined output mesh file. Meshing will saved into "+self.FileOutTmp)
        else:
            self.FileOutTmp=FileNameOut

        if self.BUILD_DATA_PATH == 'ON':
            self.FileName3_msh = os.path.join(GL_DATA_PATH, 'Tmp3D.msh')
        else:
            self.FileName3_msh = self.FileOutTmp
        self.FileName3_out=self.FileName3_msh+"out" 

        if self.BUILD_DATA_PATH == 'ON':
           self.FileName4Out = GL_GMSH_OUT_PATH+'/Tmp3D.msh' # os.path.join(GL_GMSH_OUT_PATH,'Tmp3D.msh')
        else:
            self.FileName4Out=self.FileOutTmp



        # definition of the meshing command 
        self.cmd = GL_CMD_GMSH + ' ' + self.MESH_OUTPUT_FORMAT_FLAG + ' ' + ' -3 '+self.FileName1_geo+' -o '+self.FileName4Out+' > '+self.FileName3_out
        try:
            self.logger.info("I am trying  command... "+ self.cmd)
            os.system(self.cmd)
        except:
            self.logger.errror("Impossible to execute command "+ self.cmd 
                               + "Are you sure to have defined correctly all paths to Gmsh (ThirdPart component) ?")
        else:
            self.logger.info("Mesh 3D done.")
        return self.FileName3_msh


    def getMeshFileOut(self):
        return self.FileName3_msh

        
    def mesh3DwithTetgen(self, FileNameIn, FileNameOut):
        #File2 = os.path.join(GL_DATA_PATH, 'Demo-2.tmp.smesh')
        File2 = os.path.join(GL_DATA_PATH, FileNameIn)
        print "  Volum meshing"
        Cv_MeshStruct2Tetgen(File2,[MeshElmtList[0],MeshElmtList[2]])
        File2 = os.path.join(GL_DATA_PATH, 'Demo-2.tmp.smesh')
        cmd = GL_CMD_TETGEN + ' -pga0.3 ' + File2
        try:
            print "I am trying the command... "+ self.cmd
            os.system(self.cmd)
        except:
            print "Impossible to execute command "+ self.cmd + "Are you sure to have correctly defined all paths ?"
        else:
            print"3D mesh done."

    def MeshImport(self, meshFileIn):
        mesh = Mesh()
        try:
            self.logger.info("Mesh Importing. Please wait...")
            mesh.load(GmshLoader(meshFileIn))
        except:
            self.logger.error("Error in Bin/Mesher/MeshImport: Impossible to import" + meshFileIn)
        return(mesh)


    def PrintInfoOnSkeleton (self, SkeletonElmtList):
        for self.Elmt in SkeletonElmtList.List:
            self.Elmt.Print_Element()
            # check skeleton carateristics
            # this should be done in  the settings methods that apply on each skeleton type !
            if self.Elmt.Type == 'NODE':
                if self.Elmt.SkeletonNodeList.NbNode is not 1:
                    print 'ERROR Wrong Node number for this Element'
                if self.Elmt.SkeletonEdgeList.NbEdge is not 0:
                    print 'ERROR Wrong Edge number for this Element'
                if self.Elmt.SkeletonFaceList.NbFace is not 0:
                    print 'ERROR Wrong Face number for this Element'
                if self.Elmt.SkeletonCellList.NbCell is not 0:
                    print 'ERROR Wrong Face number for this Element'
            if self.Elmt.Type == 'LINE':
                if self.Elmt.SkeletonNodeList.NbNode is not 2:
                    print 'ERROR Wrong Node number for this Element'
                if self.Elmt.SkeletonEdgeList.NbEdge is not 1:
                    print 'ERROR Wrong Edge number for this Element'
                if self.Elmt.SkeletonFaceList.NbFace is not 0:
                    print 'ERROR Wrong Face number for this Element'
                if self.Elmt.SkeletonCellList.NbCell is not 0:
                    print 'ERROR Wrong Face number for this Element'
            if self.Elmt.Type == 'TRIANGLE':
                if self.Elmt.SkeletonNodeList.NbNode is not 3:
                    print 'ERROR Wrong Node number for this Element'
                if self.Elmt.SkeletonEdgeList.NbEdge is not 3:
                    print 'ERROR Wrong Edge number for this Element'
                if self.Elmt.SkeletonFaceList.NbFace is not 1:
                    print 'ERROR Wrong Face number for this Element'
                if self.Elmt.SkeletonCellList.NbCell is not 0:
                    print 'ERROR Wrong Face number for this Element'
            if self.Elmt.Type == 'TETRAHEDRON':
                if self.Elmt.SkeletonNodeList.NbNode is not 4:
                    print 'ERROR Wrong Node number for this Element'
                if self.Elmt.SkeletonEdgeList.NbEdge is not 6:
                    print 'ERROR Wrong Edge number for this Element'
                if self.Elmt.SkeletonFaceList.NbFace is not 4:
                    print 'ERROR Wrong Face number for this Element'
                if self.Elmt.SkeletonCellList.NbCell is not 1:
                    print 'ERROR Wrong Face number for this Element'

    def PrintInfoOnMeshElements (self, dim, MeshElmtList):
        '''
        display informations about mesh.
        '''
        print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx '
        print ' INFORMATION ABOUT LIST OF MESH ELEMENT OF DIMENSION', dim
        print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx '
        print
        if dim > 3:
            print 'Element dimension too high (should be between 0 to 3)'
        else:
            for self.Elmt in MeshElmtList[dim].List:
               self.Elmt.Print_Element()
            for self.Index in MeshElmtList[dim].IdList:
               print self.Index
