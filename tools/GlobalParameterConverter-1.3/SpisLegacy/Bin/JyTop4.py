"""
**File name:**    JyTop4.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      4.3.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 4.3.0   | Julien Forest                        | Modif                      |
|         | j.forest@artenum.com                 |                            |
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


import os, time, string

from spis.Top.Simulation import *
from spis.Top.SC import *
from spis.Top.Plasma import *
from spis.Vol.VolMesh import *
from spis.Vol.VolField import *
from spis.Vol.VolDistrib import *
from spis.Vol.Geom import *
from spis.Surf.SurfMesh import *
from spis.Surf.SurfField import *
from spis.Util.Table import *
from spis.Util.Monitor import *
from spis.Top.Top import *


import spis.Top.Default.LocalParameter as LocalParameter
from spis.Top.Default import GlobalParameter

from spis.Top.Default                   import MaterialProperty
from spis.Surf.SurfInteract             import GenericParamSet
        
from Modules.Field.DataField            import DataField
from Modules.Field.DataFieldList        import DataFieldList
from Modules.Field.MeshField            import MeshField
from Modules.Field.MeshFieldList        import MeshFieldList
from Modules.Properties.Material        import Material

from Bin.config                         import GL_EXCHANGE, GL_DEFAULT_INPUT_PATH, GL_DATA_PATH, GL_KERNEL_EXCHANGE

from Bin.Tasks.shared                   import shared
from Bin.Tasks.shared                   import sharedProp
from Bin.Tasks.shared                   import sharedFiles
from Bin.Tasks.shared                   import sharedData
from Bin.Tasks.shared                   import sharedSolver
from Bin.Tasks.shared import sharedNum #FIXME

from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory

from java.util                          import Vector

class JyTop4:
    '''
    Top simulation kernel wrapper. This Jython class wrap the 
    java based SPIS-NUM simulation kernel. Its performs the data 
    structure conversion from UI to NUM, the simulation model 
    building, launches the execution of the simulation loop and 
    recovers the output data.
    '''
    
        
    def __init__(self, spisNumMesh, allDataField, meshDataField):
            '''
            Main constructor of the SPIS-NUM simulation wrapper, pass the global 
            mesh and data structure after the UI2NUM conversion.
            '''    
    
            # building of the related logger
            self.logger = LoggerFactory.getLogger("JyTop4")
            self.logger.info("JyTop initialised")
    
            tmpDate = time.gmtime()
            self.simulationId = `tmpDate[0]`+`tmpDate[1]`+`tmpDate[2]`+`tmpDate[3]`+`tmpDate[4]`+`tmpDate[5]`
            self.logger.info("Initialisation of simulation Nb:"+self.simulationId)
            
            self.logFile = os.path.join(GL_EXCHANGE, "spis_JyTop4.log")   
            self.stream  = open(self.logFile,"w")
            
            # settings of needed inputs parameters
            self.spisNumMesh = spisNumMesh
            
            self.allDataField = allDataField
            self.allMeshField = allDataField
              
    def setSharedProp(self, sharedProp):
        self.sharedProp = sharedProp
        
    def setSharedMaterialModel(self, materialModel, nascapParameterSetList = None):
        """
        Set the material model (i.e legacy or NASCAP based). If the selected model 
        is NASCAP based and extra nascapParameterSetList should be passed as second 
        argument.
        """
        self.materialModel = materialModel
        if nascapParameterSetList != None:
            self.nascapParameterSetList = nascapParameterSetList
        else: 
            self.nascapParameterSetList = None
        
    def setGlobalParameters(self, globalParameters):
        self.globalParameters = globalParameters
                
    #############################################
    #     Create and prepare the simulation     #
    #############################################
    def BuildSim(self):
        '''
        Create and prepare the grids and the simulation model.
        '''
        self.logger.info("SPIS/NUM main is under creation")


        # GEOMETRY INITIALISATION SECTION, MIMICKING (SEMI-)AUTOMATED
        #       DATA TRANSFER  FROM FRAMEWORK TO SPIS NUM


        # Creates meshes and some property fields from framework data.
        # (Of course these definitions and initialisations shall be
        # different in the framework, they are just written here for
        # testing).
        #
        # Data are:
        #
        # - VolMesh (see ThreeDUnstructVolMesh for more on
        #            variable meaning and some classical
        #            constraints on numbering) :

        # cell (tetrahedra) number

        self.geom = ThreeDCartesianGeom()
        self.logger.info("creation of the ThreeDUnstructSurfMesh structure (for SC surface)")

        # -----------------------
        # - Init for spacecraft -
        # -----------------------
        
        #print "******************************************"
        #print self.spisNumMesh.getSpacecraftMesh().getData('EdgeFlagS')
        #print "******************************************"
        #print self.spisNumMesh.getSpacecraftMesh().getData('EdgeRadiusS') 
        #print "******************************************"
        #print sharedSolver["SpisNumCaller"].spisNumMesh.getSpacecraftMesh().getData('EdgeRadiusS') 
        #print "******************************************"


        self.scSurfMesh = \
           ThreeDUnstructSurfMesh(
                      self.geom                                                             , # geom 
                      None                                                                  , # volMesh
                      self.spisNumMesh.getSpacecraftMesh().getFaceNb()                      , # surfNbS
                      self.spisNumMesh.getSpacecraftMesh().getEdgeNb()                      , # edgeNbS
                      self.spisNumMesh.getSpacecraftMesh().getNodeNb()                      , # nodeNbS
                      self.spisNumMesh.getSpacecraftMesh().getSurfEdge()                    , # surfEdgeS
                      self.spisNumMesh.getSpacecraftMesh().getSurfNode()                    , # surfNodeS
                      self.spisNumMesh.getSpacecraftMesh().getEdgeNode()                    , # edgeNodeS
                      self.spisNumMesh.getSpacecraftMesh().getData('SurfFlagS')             , # surfFlagS
                      self.spisNumMesh.getSpacecraftMesh().getSurfIndex()                   , # surfIndexS
                      []                                                                    , # FIXME: Not supported yet in LightMesh (surfIndexS2S)
                      [0.0 for i in range(self.spisNumMesh.getSpacecraftMesh().getFaceNb())]  , # FIXME surfThicknessS
                      self.spisNumMesh.getSpacecraftMesh().getData('EdgeFlagS')             , # edgeFlagS
                      self.spisNumMesh.getSpacecraftMesh().getEdgeIndex()                   , # edgeIndexS
                      []                                                                    , # FIXME: Not supported yet in LightMesh (edgeIndexS2S)
                      self.spisNumMesh.getSpacecraftMesh().getData('EdgeRadiusS')             , # [0 for i in range(self.spisNumMesh.getSpacecraftMesh().getEdgeNb())]  , # edgeRadiusS
                      self.spisNumMesh.getSpacecraftMesh().getData('NodeFlagS')             , # nodeFlagS
                      self.spisNumMesh.getSpacecraftMesh().getNodeIndex()                   , # nodeIndexS
                      []                                                                    , # FIXME: Not supported yet in LightMesh (nodeIndexS2S)
                      self.spisNumMesh.getSpacecraftMesh().getXYZ()                         ) # xyzS


        # ---------------------
        # - Init for boundary -
        # ---------------------

        self.logger.info("creation of the ThreeDUnstructSurfMesh structure (for external boundary surface)")
        self.bdSurfMesh = \
        ThreeDUnstructSurfMesh(
                      self.geom                                                            , # geom 
                      None                                                                 , # volMesh
                      self.spisNumMesh.getBoundaryMesh().getFaceNb()                       , # surfNbs
                      self.spisNumMesh.getBoundaryMesh().getEdgeNb()                       , # edgeNbS
                      self.spisNumMesh.getBoundaryMesh().getNodeNb()                       , # nodeNbS
                      self.spisNumMesh.getBoundaryMesh().getSurfEdge()                     , # surfEdgeS
                      self.spisNumMesh.getBoundaryMesh().getSurfNode()                     , # surfNodeS
                      self.spisNumMesh.getBoundaryMesh().getEdgeNode()                     , # edgeNodeS
                      self.spisNumMesh.getBoundaryMesh().getData('SurfFlagBd')             , # surfFlagS
                      self.spisNumMesh.getBoundaryMesh().getSurfIndex()                    , # surfIndexS
                      [-1 for i in range(self.spisNumMesh.getBoundaryMesh().getFaceNb())]  , # FIXME: Not supported yet in LightMesh (surfIndexS2Bd)
                      [ 0 for i in range(self.spisNumMesh.getBoundaryMesh().getFaceNb())]  , # surfThicknessBd
                      self.spisNumMesh.getBoundaryMesh().getData('EdgeFlagBd')             , 
                      self.spisNumMesh.getBoundaryMesh().getEdgeIndex()                    ,
                      [-1 for i in range(self.spisNumMesh.getBoundaryMesh().getEdgeNb())]  , # FIXME: Not supported yet in LightMesh (edgeIndexS2Bd)
                      self.spisNumMesh.getBoundaryMesh().getData('EdgeRadiusBd')            , # [ 0.1 for i in range(self.spisNumMesh.getBoundaryMesh().getEdgeNb())]  , #edgeRadiusBd (radius of thin wires)
                      self.spisNumMesh.getBoundaryMesh().getData('NodeFlagBd')             ,
                      self.spisNumMesh.getBoundaryMesh().getNodeIndex()                    ,
                      []                                                                   , # FIXME: Not supported yet in LightMesh (nodeIndexS2Bd)
                      self.spisNumMesh.getBoundaryMesh().getXYZ()                          )
 

        # -------------------
        # - Init for volume -
        # -------------------

        self.logger.info("creation of the ThreeDUnstructVolMesh structure (for Plasma Volume)")
        
        #print "XXXX CONTROL XXXXXXX"
        #print "CellSurf", self.spisNumMesh.getVolumeMesh().getCellSurf()
        
        
        self.volMesh = \
        ThreeDUnstructVolMesh(self.geom                                     , 
                       self.bdSurfMesh                                      ,
                       self.scSurfMesh                                      ,
                       self.spisNumMesh.getVolumeMesh().getCellNb()         ,
                       self.spisNumMesh.getVolumeMesh().getFaceNb()         ,
                       self.spisNumMesh.getVolumeMesh().getEdgeNb()         ,
                       self.spisNumMesh.getVolumeMesh().getNodeNb()         ,
                       self.spisNumMesh.getVolumeMesh().getCellSurf()       ,
                       self.spisNumMesh.getVolumeMesh().getCellEdge()       ,
                       self.spisNumMesh.getVolumeMesh().getCellNode()       ,
                       self.spisNumMesh.getVolumeMesh().getSurfEdge()       ,
                       self.spisNumMesh.getVolumeMesh().getSurfNode()       ,
                       self.spisNumMesh.getVolumeMesh().getEdgeNode()       ,
                       self.spisNumMesh.getVolumeMesh().getData('SurfFlag') ,
                       self.spisNumMesh.getVolumeMesh().getSurfIndexSC()    ,
                       []                                                   , # (surfIndexS2V)
                       self.spisNumMesh.getVolumeMesh().getSurfIndexB()     ,
                       self.spisNumMesh.getVolumeMesh().getData('EdgeFlag') ,
                       self.spisNumMesh.getVolumeMesh().getEdgeIndexSC()    , 
                       []                                                   , # (edgeIndexS2V)
                       self.spisNumMesh.getVolumeMesh().getEdgeIndexB()     , 
                       self.spisNumMesh.getVolumeMesh().getData('NodeFlag') ,
                       self.spisNumMesh.getVolumeMesh().getNodeIndexSC()    , 
                       []                                                   , # (nodeIndexS2V)
                       self.spisNumMesh.getVolumeMesh().getNodeIndexB()     , 
                       self.spisNumMesh.getVolumeMesh().getXYZ()            )

        # -----------------------------------------
        # - Linking surface meshes to volume mesh -
        # -----------------------------------------

        self.logger.info("Linking surface meshes to volume mesh")
        self.logger.debug("STEP 0")
        self.bdSurfMesh.setVm(self.volMesh)
        
        self.logger.debug("STEP 1")
        self.scSurfMesh.setVm(self.volMesh)
        
        self.logger.debug("STEP 2")

        # ----------------
        # - Global Param -
        # ----------------

        self.logger.info("creating Global Parameter data")
        
        #from spis.Top.Simulation import *
        from spis.Top.Default import *

        self.globalParameterArray = []
        for key in self.globalParameters.keys():
            p = self.globalParameters[key]
            param = GlobalParameter(key, p[2], p[4], p[3], p[1])
            self.globalParameterArray.append(param)

        
        # ---------------
        # - Local Param -
        # ---------------

        self.localParameterArray = []

        # --------------------------
        # - Local Param for Volume -
        # --------------------------
        self.logger.info("#############   Mapping of Data in Volume  #########")
        paramNameList = [ ['VolInteracFlag', 3] ,\
                          ['BackGroundDens', 3] ]
        spisMesh      = self.spisNumMesh.getVolumeMesh()
        spisNumMesh   = self.volMesh

        self.buildLocalParamFromList(paramNameList, spisMesh, spisNumMesh)

        # ------------------------------
        # - Local Param for Spacecraft -
        # ------------------------------
        self.logger.info("#############   Mapping of Data on S/C surface  #########")
        paramNameList = [ ['MatModelId'      , 2] ,\
                          ['MatTypeId'       , 2] ,\
                          ['MatThickness'    , 2] ,\
                          ['PhotoEmis'       , 2] ,\
                          ['ElecSecEmis'     , 2] ,\
                          ['ProtSecEmis'     , 2] ,\
                          ['VolConduct'      , 2] ,\
                          ['IndConduct'      , 2] ,\
                          ['SurfConduct'     , 2] ,\
                          ['Temperature'     , 2] ,\
                          ['SunFlux'         , 2] ,\
                          ['ElecNodeId'      , 2] ,\
                          ['EdgeElecNodeId'  , 1] ,\
                          ['SCDiriFlag'      , 0] ,\
                          ['SCDiriPot'       , 0] ,\
                          ['SCDiriPotEdge'   , 1] ,\
                          ['SCDiriPotSurf'   , 2] ,\
                          ['SCFourFlag'      , 2] ,\
                          ['SCFourAlpha'     , 2] ,\
                          ['SCFourValue'     , 0] ,\
                          ['SourceId'        , 2] ,\
                          ['SourceCurrent'   , 2] ,\
                          ['SourceTemp'      , 2] ,\
                          ['SourceMach'      , 2] ]
        spisMesh      = self.spisNumMesh.getSpacecraftMesh()
        spisNumMesh   = self.scSurfMesh

        self.buildLocalParamFromList(paramNameList, spisMesh, spisNumMesh)
        
        # ----------------------------
        # - Local Param for Boundary -
        # ----------------------------
        self.logger.info("#############   Mapping of Data on External BD  #########")
        paramNameList = [ ['BdDiriFlag'  , 0] ,\
                          ['BdDiriPot'   , 0] ,\
                          ['BdFourFlag'  , 2] ,\
                          ['BdFourAlpha' , 2] ,\
                          ['BdFourValue' , 0] ,\
                          ['IncomPart'   , 2] ,\
                          ['OutgoPart'   , 2] ]
        spisMesh      = self.spisNumMesh.getBoundaryMesh()
        spisNumMesh   = self.bdSurfMesh

        self.buildLocalParamFromList(paramNameList, spisMesh, spisNumMesh)
        
        self.runId = -1
        self.logger.info("Now, normally everything should be ready for the simulation")
        
                
        ###############################################################
        #                     CALLING SPIS-NUM:                       #
        #    Major place where modifications can be done by users     #
        ###############################################################

        self.logger.debug("GL_DATA_PATH:"+GL_DATA_PATH)
        self.logger.debug("GL_DEFAULT_INPUT_PATH: "+GL_DEFAULT_INPUT_PATH)
        self.logger.debug("Files in GL_DEFAULT_INPUT_PATH:      "+string.join(os.listdir(GL_DEFAULT_INPUT_PATH),"\n      "))
        self.logger.debug(" GL_KERNEL_EXCHANGE: "+ GL_KERNEL_EXCHANGE)
        self.logger.debug("Files in GL_KERNEL_EXCHANGE:       "+string.join(os.listdir(GL_KERNEL_EXCHANGE),"\n      "))

        self.logger.info("Building of the simulation model")
        
        if ( self.materialModel == Material.LEGACY_MATERIAL):
            print "Old constructor for legacy materials."
            # old approach where material properties are not transfered from UI to Num
            self.simu = NumTopFromUI(self.volMesh,
                                     self.bdSurfMesh,
                                     self.scSurfMesh,
                                     self.globalParameterArray,
                                     self.localParameterArray,
                                     GL_DATA_PATH,
                                     GL_KERNEL_EXCHANGE)
        elif ( self.materialModel == Material.NASCAP_MATERIAL ):
            print "New constructor for NASCAP based material"
            # new approach with material prop passed for UI to Num
            self.simu = NumTopFromUI(self.volMesh,
                                     self.bdSurfMesh,
                                     self.scSurfMesh,
                                     self.globalParameterArray,
                                     self.localParameterArray,
                                     GL_DATA_PATH,
                                     GL_KERNEL_EXCHANGE, 
                                     self.nascapParameterSetList)
        else: 
            self.logger.debug("Material model not supported: " + str(self.materialModel))
            

        
    def buildLocalParamFromList(self, list, spisMesh, spisNumMesh):
        for param in list:
            #print "----------->", param[0], param[1], sharedData["AllDataField"].Dic[param[0]].ValueList
            self.buildLocalParam(self.localParameterArray, param[0], param[1], spisMesh, spisNumMesh)

           
    def buildLocalParam(self, paramArray, localName, localisation, spisMesh, spisNumMesh):

        paramArray.append(LocalParameter( localName, 
                                          spisMesh.convertDataToFloatArray(localName), 
                                          localisation, 
                                          spisNumMesh, 
                                          self.allDataField.Dic[localName].Unit,    #sharedData["AllDataField"].Dic[localName].Unit, 
                                          'no comment'))
        
    def Run(self):
        """
        Performs the simulation.
        """
        self.logger.info("SPIS/NUM main is starting")
        self.runId = self.runId + 1
        self.logger.info("Run Nb:" + `self.runId`) 
        self.logger.info("Integration in SPIS/NUM")
        self.simu.integrate()
        self.simu.close()
        self.logger.info("Back from SPIS/NUM")


    def buildNascapParameterSetList(self, materialModel, selectedNascapMaterialList, nascapMaterialCataLog):
        """
        Build the parameters set corresponding to the applied Nascap based material, if any. 
        """
        nascapParameterSetList = []
        for mat in selectedNascapMaterialList:
            currentMatTypeId = mat[0]
            currentNumIndex = mat[1]
            currentMatName = mat[2]
            currentMatDescription = mat[3]
        
            # first we recover the corresponding NASCAP material
            linkedNascapMaterial = nascapMaterialCataLog.GetElmById(currentMatTypeId)
                
            # and then we recover the corresponding values
            vect = Vector() #i.e because SPIS-NUM need Vectors (Java layer)
            for data in linkedNascapMaterial.DataList.List:
                prop = MaterialProperty( data.Name, data.Type, data.Value, data.Unit, data.Description)
                vect.add(prop)
                #print "------->", prop.valuesAsFloat()
                    
            nascapParameterSetList.append(GenericParamSet( currentMatName, currentNumIndex, currentMatDescription, None, vect))
            self.setSharedMaterialModel(materialModel, nascapParameterSetList)
            
            
                    
        
        #####          Examples of possible modifications:        #####

        # GEO simulation: change the above 5 lines into the following #
        # (uncommented them! and comment the above ones):             #

        #print >> self.stream, "creating GEO simulation java objet in SPIS/NUM"
        #self.simu = GeoExample2(self.volMesh, self.bdSurfMesh, self.scSurfMesh,self.globalParameterArray)
        #print >> self.stream, "Integration in SPIS/NUM"
        #self.simu.integrate()
        #print >> self.stream, "Back from SPIS/NUM"

        # LEO simulation: change the above 5 lines into the following #
        # (uncommented them! and comment the above ones):             #

        #print >> self.stream, "creating LEO simulation java objet in SPIS/NUM"
        #self.simu = LeoExample(self.volMesh, self.bdSurfMesh, self.scSurfMesh)
        #print >> self.stream, "Integration in SPIS/NUM"
        #self.simu.integrate(0.001)
        #print >> self.stream, "Back from SPIS/NUM"

        # GEO simulation with photo-emission turned on after a while: #

        #print >> self.stream, "creating GEO simulation java object in SPIS/NUM (with photo-emission)"
        #self.simu = GeoExample2(self.volMesh, self.bdSurfMesh, self.scSurfMesh)
        #print >> self.stream, "Integration in SPIS/NUM"
        #self.simu.integrate(1.0)
        #print >> self.stream, "Back from SPIS/NUM"

        # To dump meshes, and be able to run SPIS-NUM as a standalone #
        # code (within Eclipse), and reload these meshes through the  #
        # import command in the SPIS-NUM menu used when standalone:   #

        #print >> self.stream, "creating LEO simulation java object in SPIS/NUM"
        #self.simu = LeoExample(self.volMesh, self.bdSurfMesh, self.scSurfMesh)
        #print >> self.stream, "mesh dump in SPIS/NUM"
        #self.simu.exportMeshes()
        #print >> self.stream, "Integration in SPIS/NUM"
        #self.simu.integrate(0.001)
        #print >> self.stream, "Back from SPIS/NUM"

        # Many more changes are possible (integration duration...)    #
        # NB: all of these changes will be offered through a better   #
        # user interface later                                        #

