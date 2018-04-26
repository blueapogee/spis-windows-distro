"""
Module of interface between SPIS-UI and SPIS-NUM. Performs the data structure (mesh,
fields, etc...) from UI to NIM.

**File name:**    SpisNumInterface.py

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

from Bin.Tasks.shared import sharedFiles

from copy import copy
#from copy import deepcopy

#import os, sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

#from config import GL_EXCHANGE
from com.artenum.free.mesh.spis.num import SpisNumMesh

#from spis.Top.Default                   import MaterialProperty #NB: requires that SPIS-NUM jar is up-to-date. 
#from spis.Surf.SurfInteract             import GenericParamSet #NB: requires that SPIS-NUM jar is up-to-date.
#
from Modules.Properties.Material        import Material

from java.util                          import Vector

class SpisNumInterface:
    
    def __init__(s, AllDataFieldIn, AllMeshFieldIn):
        
        s.logger = LoggerFactory.getLogger("SpisNumInterface")
        
        s.logger.info(' INTERFACE MODULE BETWEEN SPISUI AND SPISNUM DATA STRUCTURES  ')

        s.AllDataField = AllDataFieldIn
        s.AllMeshField = AllMeshFieldIn
  
  
    def BuildList(s, mesh):
        """
        init the mesh conversion
        """
    
        
        s.mesh = mesh
        
        # build up the SPIS-NUM 
        s.spisNumMesh = SpisNumMesh(s.mesh)

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXX
        # XXX Build of Plasma mesh XXX
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXX
        
        s.spisNumMesh.buildVolumeMesh(s.mesh.getCellIterator(),s.mesh.getNbCell(), s.AllMeshField.Dic['SurfFlag_MF'].MeshElementList, s.AllMeshField.Dic['EdgeFlag_MF'].MeshElementList, s.AllMeshField.Dic['NodeFlag_MF'].MeshElementList)
               
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        # XXX Build of SC and Bd mesh XXX
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        
        s.spisNumMesh.buildSpacecraftMesh(s.AllMeshField.Dic['SurfFlagS_MF'].MeshElementList, s.AllMeshField.Dic['EdgeFlagS_MF'].MeshElementList, s.AllMeshField.Dic['NodeFlagS_MF'].MeshElementList)
        s.spisNumMesh.buildBoundaryMesh(s.AllMeshField.Dic['SurfFlagBd_MF'].MeshElementList, s.AllMeshField.Dic['EdgeFlagBd_MF'].MeshElementList, s.AllMeshField.Dic['NodeFlagBd_MF'].MeshElementList)


    def buildCrossNumberingBetweenMesh(s):
            
        s.logger.info('buildCrossNumberingBetweenMesh ')
        s.spisNumMesh.buildCrossNumberingBetweenMesh()
        s.spisNumMesh.reorderInternalListForSimulationConsistency()
        
        
    def MapDFOnVolMesh(s):
        '''
        Maps the DF on the volume mesh, with the right order of the
        mesh elements on the local (surface) mesh.
        '''

        s.logger.info("DF mapping on Volume mesh")
        
        # Datafield list is composed of 
        #  0 => DatafieldName
        #  1 => MeshFieldName
        #  2 => Dimension of the mapping (node=0, edge=1, face=2, cell=3)
        
        datafieldList  = [['VolInteracFlag', 'VolInteracFlag_MF' , 3 ], \
                          ['BackGroundDens', 'BackGroundDens_MF' , 3 ], \
                          ['SurfFlag'      , 'SurfFlag_MF'       , 2 ], \
                          ['EdgeFlag'      , 'EdgeFlag_MF'       , 1 ], \
                          ['NodeFlag'      , 'NodeFlag_MF'       , 0 ]  ]

        s.applyAllDF(s.spisNumMesh.getVolumeMesh() , datafieldList)
        
        # -----------------------------       
        # FIXME : Have to be done !!!
        # -----------------------------
        #print '    duplicatedNodesParity => Caution: this field is not managed yet'

        
    
    def MapDFOnSCMesh(s):
        '''
        Maps the DF on the S/C surface mesh, with the right order of the
        mesh elements on the local (surface) mesh.
        CAUTION: This method must be called AFTER the MapDFOnVolMesh method.
        '''
       
        s.logger.info("DF mapping on Spacecraft mesh")
        
        # Datafield list is composed of 
        #  0 => DatafieldName
        #  1 => MeshFieldName
        #  2 => Dimension of the mapping (node=0, edge=1, face=2, cell=3)
        
        datafieldList  = [['SurfFlagS'      , 'SurfFlagS_MF'      , 2 ], \
                          ['SurfThicknessS' , 'SurfThicknessS_MF' , 2 ], \
                          ['MatModelId'     , 'MatModelId_MF'     , 2 ], \
                          # ['MatTypeId'      , 'MatTypeId_MF'      , 2 ], \
                          ['MatThickness'   , 'MatThickness_MF'   , 2 ], \
                          ['PhotoEmis'      , 'PhotoEmis_MF'      , 2 ], \
                          ['ElecSecEmis'    , 'ElecSecEmis_MF'    , 2 ], \
                          ['ProtSecEmis'    , 'ProtSecEmis_MF'    , 2 ], \
                          ['VolConduct'     , 'VolConduct_MF'     , 2 ], \
                          ['IndConduct'     , 'IndConduct_MF'     , 2 ], \
                          ['SurfConduct'    , 'SurfConduct_MF'    , 2 ], \
                          ['Temperature'    , 'Temperature_MF'    , 2 ], \
                          ['SunFlux'        , 'SunFlux_MF'        , 2 ], \
                          ['ElecNodeId'     , 'ElecNodeId_MF'     , 2 ], \
                          ['SCFourFlag'     , 'SCFourFlag_MF'     , 2 ], \
                          ['SCFourAlpha'    , 'SCFourAlpha_MF'    , 2 ], \
                          ['SourceId'       , 'SourceId_MF'       , 2 ], \
                          ['SourceCurrent'  , 'SourceCurrent_MF'  , 2 ], \
                          ['SourceTemp'     , 'SourceTemp_MF'     , 2 ], \
                          ['SourceMach'     , 'SourceMach_MF'     , 2 ], \
                          ['SCDiriPotSurf'  , 'SCDiriPotSurf_MF'  , 2 ], \
                          ['EdgeFlagS'      , 'EdgeFlagS_MF'      , 1 ], \
                          ['EdgeRadiusS'    , 'EdgeRadiusS_MF'    , 1 ], \
                          ['EdgeElecNodeId' , 'EdgeElecNodeId_MF' , 1 ], \
                          ['SCDiriPotEdge'  , 'SCDiriPotEdge_MF'  , 1 ], \
                          ['NodeFlagS'      , 'NodeFlagS_MF'      , 0 ], \
                          ['SCDiriFlag'     , 'SCDiriFlag_MF'     , 0 ], \
                          ['SCDiriPot'      , 'SCDiriPot_MF'      , 0 ], \
                          ['SCFourValue'    , 'SCFourValue_MF'    , 0 ]  ]

        s.applyAllDF(s.spisNumMesh.getSpacecraftMesh() , datafieldList)

        # -----------------------------       
        # FIXME : Have to be done !!!
        # -----------------------------
        #print '    duplicatedFacesParityS/duplicatedEdgesParityS/duplicatedNodesParityS => Caution: this field is not managed yet'

        
    def MapDFOnBdMesh(s):

        s.logger.debug("DF mapping on Boundary mesh")
        
        # Datafield list is composed of 
        #  0 => DatafieldName
        #  1 => MeshFieldName
        #  2 => Dimension of the mapping (node=0, edge=1, face=2, cell=3)
        
        datafieldList  = [['SurfFlagBd'  , 'SurfFlagBd_MF'  , 2 ], \
                          ['BdFourFlag'  , 'BdFourFlag_MF'  , 2 ], \
                          ['BdFourAlpha' , 'BdFourAlpha_MF' , 2 ], \
                          ['IncomPart'   , 'IncomPart_MF'   , 2 ], \
                          ['OutgoPart'   , 'OutgoPart_MF'   , 2 ], \
                          ['EdgeFlagBd'  , 'EdgeFlagBd_MF'  , 1 ], \
                          ['NodeFlagBd'  , 'NodeFlagBd_MF'  , 0 ], \
                          ['BdDiriFlag'  , 'BdDiriFlag_MF'  , 0 ], \
                          ['BdDiriPot'   , 'BdDiriPot_MF'   , 0 ], \
                          ['BdFourValue' , 'BdFourValue_MF' , 0 ] ]

        s.applyAllDF(s.spisNumMesh.getBoundaryMesh() , datafieldList)
        s.logger.info("End of conversion")
    
    def applyAllDF(s, currentMesh, datafieldList):
        """
        Set the data field values to SpisNumMesh param, i.e map the values 
        on the corresponding grid in SPIS-NUM.
        
        The first argument set the initial mesh in SPIS-UI. 
        
        The second argument, DatafieldList, set the DataField-MeshField couple
        and the dimension of mapping, as follow: 
        
        0 => DatafieldName
        1 => MeshFieldName
        2 => Dimension of the mapping (node=0, edge=1, face=2, cell=3)
        
        """
        dataSizeMapping = [ currentMesh.getNodeNb(),\
                            currentMesh.getEdgeNb(),\
                            currentMesh.getFaceNb(),\
                            currentMesh.getCellNb() ]
    
        mappingIdIndex  = [ currentMesh.getNodeIndexFromNodeId(),\
                            currentMesh.getEdgeIndexFromEdgeId(),\
                            currentMesh.getFaceIndexFromFaceId(),\
                            currentMesh.getCellIndexFromCellId() ]

        # Map all datafield of the list
        for DFList in datafieldList:
            currentDatafield  = s.AllDataField.Dic[DFList[0]]
            currentMeshField  = s.AllMeshField.Dic[DFList[1]]
            currentMappingDim = DFList[2]
           
            currentMesh.allocateDataField(currentDatafield.Name,dataSizeMapping[currentMappingDim],currentDatafield.Type)
            #print "---->", currentMesh.getDataFromType(currentDatafield.Name,currentDatafield.Type)
            s.applyDF(currentMesh.getDataFromType(currentDatafield.Name,currentDatafield.Type), mappingIdIndex[currentMappingDim], currentDatafield, currentMeshField)
            #print '    ', currentDatafield.Name

           
    
    def applyDF(s, spisNumParamTable, mapFromIdToIndexTable, dataField, meshField):
        s.logger.debug( dataField.Name + " " +meshField.Name)
        for i in xrange(len(spisNumParamTable)):
            spisNumParamTable[mapFromIdToIndexTable[meshField.MeshElementIdList[i]]] = copy(dataField.ValueList[i])
           
           
           
    def applyMaterialProperties(s, materialModel, selectedNascapMaterialList):
        """
        Specific mapping method for extra S/C material properties (e.g NASCAP based materials). 
        The field is directly applied to the SPIS-NUM mesh. This method should be 
        called AFTER that convertMaterialProperties has been processed. 
        """
        
        # re-building of the local cross numbering dictionary
        if (materialModel == Material.NASCAP_MATERIAL):
            uiToNumNascapMaterialCrossNumberingDic = {}
            for mat in selectedNascapMaterialList:
                # first we recover the corresponding NASCAP material
                tmpMatTypeId =  mat[0] # we recover the MatTypeId
                uiToNumNascapMaterialCrossNumberingDic[tmpMatTypeId] = mat[1]
                #print "uiToNumNascapMaterialCrossNumberingDic= ", uiToNumNascapMaterialCrossNumberingDic              
        
        # set the main mesh
        currentMesh = s.spisNumMesh.getSpacecraftMesh()
        
        dataSizeMapping = [ currentMesh.getNodeNb(),\
                            currentMesh.getEdgeNb(),\
                            currentMesh.getFaceNb(),\
                            currentMesh.getCellNb() ]
    
        mappingIdIndex  = [ currentMesh.getNodeIndexFromNodeId(),\
                            currentMesh.getEdgeIndexFromEdgeId(),\
                            currentMesh.getFaceIndexFromFaceId(),\
                            currentMesh.getCellIndexFromCellId() ]
    
        # ['MatTypeId'      , 'MatTypeId_MF'      , 2 ], \
        datafield  = s.AllDataField.Dic['MatTypeId']
        meshField  = s.AllMeshField.Dic['MatTypeId_MF']
        currentMappingDim = 2
           
        # allocate the targeted field on the mesh. 
        currentMesh.allocateDataField(datafield.Name, dataSizeMapping[currentMappingDim], datafield.Type)
        
        spisNumParamTable = currentMesh.getDataFromType(datafield.Name, datafield.Type)
        mapFromIdToIndexTable = mappingIdIndex[currentMappingDim]
        
        
        if (materialModel == Material.NASCAP_MATERIAL):
            s.logger.info("NASCAP based material found. Id conversion needed.")
            for i in xrange(len(spisNumParamTable)):
                s.logger.debug( str(datafield.ValueList[i]) + " "+ str(uiToNumNascapMaterialCrossNumberingDic[datafield.ValueList[i]]) )
                spisNumParamTable[mapFromIdToIndexTable[meshField.MeshElementIdList[i]]] = uiToNumNascapMaterialCrossNumberingDic[datafield.ValueList[i]]
        else:
            s.logger.info("Legacy material found.")
            for i in xrange(len(spisNumParamTable)):
                spisNumParamTable[mapFromIdToIndexTable[meshField.MeshElementIdList[i]]] = copy(datafield.ValueList[i])
                
         
    def GetSpisNumMesh(s):
        '''
        return all data needed for SPIS-NUM.
        '''
        s.spisNumMesh.freeConstructionVariables()
        return s.spisNumMesh
