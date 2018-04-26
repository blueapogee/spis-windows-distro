"""
Module of settings and groups managment.

**Project ref:**  Spis/SpisUI

**File name:**    Demo_1.py

**File type:**    Executable

:status:          Implemented

**Creation:**     01/09/2003

**Modification:** 02/10/2003  GR validation

**Use:**          jython Demo_1.py

**Description:**  Propoerties groups managment demonstration.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Gerard Sookahet

:version:      0.3.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 0.1.0   | Arsene Lupin                         | Creation                   |
|         | Arsene@Lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 0.2.0   | Gerard Sookahet                      | Extension/correction       |
|         | Gerard.Sookahet@artenum.com          |                            |
+---------+--------------------------------------+----------------------------+

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

print "Please wait... "

# System Modules
import sys, os
import sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from config import GL_SPISUIROOT_PATH

from Bin.Tasks.shared         import sharedFlags, sharedFrames
from Bin.Tasks.common         import create_internal_frame

import javax.swing 
from javax.swing import JOptionPane

# Generic Modules
from Modules.Properties.Material        import Material
from Modules.Properties.MaterialList    import MaterialList
from Modules.Properties.Plasma          import Plasma
from Modules.Properties.PlasmaList      import PlasmaList
from Modules.Properties.ElecNode        import ElecNode
from Modules.Properties.ElecNodeList    import ElecNodeList
from Modules.Properties.Data            import Data
from Modules.Properties.DataList        import DataList
from Modules.Groups.MeshGroup           import MeshGroup

class GroupManager:

    def __init__(s):
        s.logger = LoggerFactory.getLogger("GroupLogger")
        s.logger.info("Group manager initiated")

    def PrintWarning(s):
        print 'BE CAREFULL !!!!'

    def DefineGeoGroups(s, GeoGroupList, sharedProp):
        
        s.logger.info("Define groups and apply corresponding properties")
        
        # This shall be done through GUI, and saved for futher use in xml file
        # GroupList are order (Node, Edge, Face and Cell geometry groups)

        #fro three faces of the inner cube
        GeoGroupList.List[0].Name = 'SpacecraftSurface_1' 
        GeoGroupList.List[0].Material = sharedProp['defaultMaterialList'].List[0] #for ITOC
        GeoGroupList.List[0].Plasma = sharedProp['defaultPlasmaList'].List[1]     #for PlasmaSC
        GeoGroupList.List[0].ElecNode = sharedProp['defaultElecNodeList'].List[0] #for ElecNodeNum-1 
        
        #for the three others faces of the inner cube
        GeoGroupList.List[1].Name = 'SpacecraftSurface_2'
        GeoGroupList.List[1].Material = sharedProp['defaultMaterialList'].List[1] #for CERS
        GeoGroupList.List[1].Plasma = sharedProp['defaultPlasmaList'].List[1]     #for PlasmaSC
        GeoGroupList.List[1].ElecNode = sharedProp['defaultElecNodeList'].List[1] #for ElecNodeNum-2 
    
        #for three faces of the external boundary    
        GeoGroupList.List[2].Name = 'ExternalBoundary_1'
        GeoGroupList.List[2].Plasma = sharedProp['defaultPlasmaList'].List[2]     #for PlasmaB

        #for three others faces of the external boundary        
        GeoGroupList.List[3].Name = 'ExternalBoundary_2'
        GeoGroupList.List[3].Plasma = sharedProp['defaultPlasmaList'].List[2]     #for PlasmaB
    
        #for the plasma in volum    
        GeoGroupList.List[4].Name = 'PlasmaVolume'
        GeoGroupList.List[4].Plasma = sharedProp['defaultPlasmaList'].List[0]     #for PlasmaSN

        s.logger.info('Groups defined')

        
    def ConvertGeoToMeshGroup(s, GeoGroupListIn, MeshGroupListIn, mesh):
        
        s.logger.info("Convert groups to Geo model to mesh data")
        if GeoGroupListIn != None:
            for GeoGroup in GeoGroupListIn.List:
                s.logger.info("Conversion of group " + `GeoGroup.Id`)
                MeshGroupTmp = MeshGroup()
                MeshGroupTmp.Id = GeoGroup.Id
                MeshGroupTmp.Name = GeoGroup.Name
                MeshGroupTmp.Type = GeoGroup.Type
                MeshGroupTmp.Description = GeoGroup.Description
                MeshGroupTmp.Visible = GeoGroup.Visible
                
                MeshGroupTmp.jMeshGroup = mesh.getMeshGroupById(GeoGroup.Id)
                
                #s.logger.debug(MeshGroupTmp.Visible)
                MeshGroupTmp.Material = GeoGroup.Material
                #s.logger.debug( MeshGroupTmp.Material)
                MeshGroupTmp.ElecNode = GeoGroup.ElecNode
                #s.logger.debug(MeshGroupTmp.ElecNode)
                MeshGroupTmp.Plasma = GeoGroup.Plasma
                #s.logger.debug(MeshGroupTmp.Plasma)
                MeshGroupListIn.Add_Group(MeshGroupTmp)
        else:
            s.logger.error("Apparently, there is no groups defined! Please load a GEOM file and define groups before.")
        s.logger.info('geoToMesh conversion done')
        
        
            
    def PrintInfoAboutMeshGroups(s, MeshGroupListIn):
        print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx '
        print ' INFORMATION ABOUT LIST OF MESH GROUP '
        print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx '
        print
        print
        for Group in MeshGroupListIn.List:
            Group.Print_Group()

    def setGUI(s, cond):
        s.mycond = cond
        print 'gui condition set'
