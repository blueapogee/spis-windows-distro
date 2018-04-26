"""
Import a CAD structure from a GEO file into a the Spis CAD structure.

**Project ref:**  Spis/SpisUI

**File name:**    CAD_Importer.py

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  GR validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsen Lupin, Maxime Biais

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                         | Creation                   |
|                | Arsen.Lupin@atenum.com               |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | Maxime Biais                         | Bug correction             |
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

import sys, os
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from config import GL_SPISUIROOT_PATH
from Bin.config import GL_DATA_PATH, GL_CMD_GMSH, GL_CMD_TETGEN, GL_CMD_MEDIT

import Bin.Tasks.common

from Bin.Tasks.common   import ask_yesno
from Bin.Tasks.common   import create_internal_frame
from Bin.Tasks.shared   import shared
from Bin.Tasks.shared   import sharedFrames
from Bin.Tasks.shared   import sharedFlags

from threading import Condition

from Modules.InOut.GmshGeo2GeoStruct import Convert as Cv_GmshGeo2GeoStruct
from Modules.InOut.GeoStruct2Gmsh import Convert as Cv_GeoStruct2Gmsh


class CADImporter:
    '''
    Import a CAD structure from a GEO file into a the Spis CAD structure.
    '''
    def __init__(self):
        """
        main constructor
        """
        self.logger = LoggerFactory.getLogger("GeomLogger")
        self.logger.info(' CAD IMPORTER loaded')


        self.BUILD_DATA_PATH = 'ON'
        self.UNROLL_OPTION = 1
        self.MESH_OUTPUT_FORMAT_FLAG = '-format msh1'
        

    def importCAD(self, FileIn, FileOut):
        '''
        Import the CAD file define in FileIn and return the resulting mesh in FileOut
        '''
        print "In import CAD, FileIn= " , FileIn
        print "In import CAD, FileOut= " , FileOut
        

        sharedFlags['importFlag'] = 1
        self.logger.debug( "importFlag= " + `sharedFlags['importFlag']`+"\n"
                          +"BUILD_DATA_PATH= "+ self.BUILD_DATA_PATH+"\n"
                          +"GL_DATA_PATH= "+ GL_DATA_PATH+"\n"
                          +"MESH_OUTPUT_FORMAT_FLAg= "+self.MESH_OUTPUT_FORMAT_FLAG)
        
        if os.path.isfile(GL_CMD_GMSH) != 1:
            self.logger.debug("Gmsh command (call to Gmsh mesher): "+GL_CMD_GMSH)
            self.logger.error("Error in CADImporter: No CAD tool defined! Impossible to process geom file. \n "
                              +"See the framework configuration settings or the ThirdPart components.")
            return(None)
            
        if (sharedFlags['importFlag'] == 1):  
            # first import and export to set proper default geometrical group
            self.logger.debug("Setting of the working directory")
            
            baseNameFileIn = os.path.basename(FileIn)
            self.logger.debug("Base Name= " + baseNameFileIn)
            tmp = baseNameFileIn[:-4]
            self.FileName1 = tmp+"Unrolled.geo"
            
            if self.BUILD_DATA_PATH == 'ON':
                self.FileName0 = os.path.join(GL_DATA_PATH,os.getcwd(),FileIn) #os.path.join(GL_DATA_PATH, FileIn)
                self.FileName1 = os.path.join(GL_DATA_PATH, self.FileName1)
            else:
                self.FileName0 = FileIn
   
            self.logger.debug( "Ref file= " + FileIn + "\n"
                              +"FileIn= " + self.FileName0 + "\n"
                              +"FileOut= " + self.FileName1)
           
            # unrolling option
            if self.UNROLL_OPTION == 1:
                self.logger.info("Unrolling the input file...")
                try:
                    self.cmd = GL_CMD_GMSH+' '+self.MESH_OUTPUT_FORMAT_FLAG+' '+' -0 "'+self.FileName0+'" -o "'+self.FileName1 +'"'
                    self.logger.debug(self.cmd)
                    os.system(self.cmd)
                except:
                    self.logger.error("Error in CAD importer: impossible to unroll the input file. \n"
                                      +"Maybe Gmsh is missing or not working. \n"
                                      +"Let us try to load it directly.")
                    self.FileName1 = self.FileName0
            else:
                self.FileName1 = self.FileName0
           
           
            # import of the CAD structure
            self.logger.info("Loading the CAD model... " + self.FileName1)
            #try:
            self.ObjectList, self.GeoElementList, \
            self.OldGeoElmtNumList, self.GeoGroupList, \
            self.OldGeoGrpNumList, self.ParamList = Cv_GmshGeo2GeoStruct([self.FileName1])
            #except:
            #    print >> sys.stderr,"ERROR 51 (importCAD): error in the CAD loading phase"
            #else:
            #    print "CAD imported"

               
            #re-ordering of groups according the Id of initial Gmsh physicals...
            self.logger.info("Re-ordering geo groups.")
            tmpIdList = []
            for Id in self.GeoGroupList.IdList: 
                tmpIdList.append(Id)

            self.GeoGroupList.IdList.sort()

            tmpGrpList = []
            for grdId in self.GeoGroupList.IdList: 
                oldIndex = tmpIdList.index(grdId)
                tmpGrpList.append(self.GeoGroupList.List[oldIndex])
            self.GeoGroupList.List = tmpGrpList
            
               
            # re-exporting into the geo format of the re-numbered file
            if (FileOut == '' or FileOut == None):
                self.FileOutTmp=FileIn+'.tmp.geo'
                self.logger.debug("No predefined output CAD file. CAD will saved into "+self.FileOutTmp)
            else:
                self.logger.debug("CAD will saved into ")  # + FileOut)
                self.FileOutTmp=FileOut
                print "FileOutTmp= " + self.FileOutTmp
               
            if self.BUILD_DATA_PATH == 'ON':
                self.FileName1_geo = os.path.join(GL_DATA_PATH, self.FileOutTmp)
            else:
                self.FileName1_geo = self.FileOutTmp
       
            try:
                self.logger.info("CAD saved in file "+self.FileName1_geo)
                Cv_GeoStruct2Gmsh(self.ObjectList, self.FileName1_geo)
            except:
                self.logger.error("Error on CADImporter): Error in the export of the CAD cleaned data \n"
                                 +"Please check your physical groups in your GEO file and \n"
                                 +"if all of them corresponds to an existing CAD element.\n")
            else:
                self.logger.info("CAD imported and geo groups properly defined")
                return self.ObjectList, self.GeoElementList, self.OldGeoElmtNumList, self.GeoGroupList, self.OldGeoGrpNumList, self.ParamList
        else:
            self.logger.info("Ok, we continue with the same CAD.")
        return(1)

    def GetGeoGroupList (self):
        '''
        Returns the list of GeoGroups.
        '''
        return self.GeoGroupList

    def GetObjectList (self):
        '''
        Returns the list of all loaded objects.
        '''
        return self.ObjectList
        
    def GetGeoElementList (self):
        '''
        Returns the list of Geom (CAD) elements. 
        '''
        return self.GeoElementList
        
    def GetOldGeoElmtNumList (self):
        return self.OldGeoElmtNumList
        
    def GetOldGeoGrpNumList (self):
        return self.OldGeoGrpNumList
    
    def GetParamList (self):
        return self.ParamList

    def PrintGeoGroups (self):
        print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx '
        print ' INFORMATION ABOUT LIST OF GEO GROUP '
        print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx '
        print
        for self.Group in self.GeoGroupList.List:
            self.Group.Print_Group()
