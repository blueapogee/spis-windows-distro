"""
Module of mapping of fields from the groups description.

**File name:**    FieldManager.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
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

import sys
import os
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
loadingLogger = LoggerFactory.getLogger("CoreLogger")

from copy import copy
#from copy import deepcopy

from Modules.Properties.DataList        import DataList
from Modules.Properties.PlasmaList      import PlasmaList
from Modules.Field.DataField            import DataField
from Modules.Field.DataFieldList        import DataFieldList
from Modules.Field.MeshField            import MeshField
from Modules.Field.MeshFieldList        import MeshFieldList
from Modules.Groups.MeshGroup           import MeshGroup


#from java.util                          import ArrayList
#from java.util                          import Vector


from Bin.Tasks.shared import sharedFiles
#from config import GL_EXCHANGE

try: 
    from spis.Top.Default                   import MaterialProperty #NB: requires that SPIS-NUM jar is up-to-date. 
    from spis.Surf.SurfInteract             import GenericParamSet #NB: requires that SPIS-NUM jar is up-to-date.
except: 
    loadingLogger.error("Error: impossible to load MaterialProperty and/or GenericParamSet from SPIS-NUM model."
                        +"Please, check if your SPIS-NUM components are up-to-date.")

from Modules.Properties.Material        import Material


class FieldManager:
    '''
    Performs the fields mapping on the mesh according the meshGroup 
    description and the linked properties. Also perform the needed 
    properties conversion, if needed. 
    '''
    def __init__(self, dataFieldListIn = None, meshFieldListIn = None):
 
        # building of the related logger
        self.logger = LoggerFactory.getLogger("FieldManager")
        self.logger.debug("FieldManager initialised")
        
        # Verbosity control flag
        # if self.VERBOSE = 0 --> no file writing
        # if self.VERBOSE = 1 --> file writing
        # self.VERBOSE = 0
        # print "VERBOSE is ", self.VERBOSE

        self.logger.info( ' CREATE NEEDED DataField AND CORRESPONDING MeshField ')

        if ( dataFieldListIn == None or meshFieldListIn == None):
            self.AllDataField=DataFieldList()
            self.AllMeshField=MeshFieldList()
        else:
            self.logger.info("DataFieldList and MeshFieldList pre-existing")
            self.AllDataField = dataFieldListIn
            self.AllMeshField = meshFieldListIn

            self.logger.info("Clean up of previous pre-processing dataFields and meshFields")
            tmpList = []
            for df in self.AllDataField.List:
                if df.Category == 'pre-processing':
                    self.logger.debug("Removing DF "+ df.Name+ " of category "+ df.Category)
                    tmpList.append(df)
                    
            for df in tmpList:        
                mfId = df.MeshFieldId
                self.AllDataField.Del_DataField(df)
                self.AllMeshField.Del_MeshField(self.AllMeshField.GetMeshFieldById(mfId))
                    
        self.TmpNameList=[]
        '''
        if (sharedFiles["project_directory"] != None):
           self.log_filename =  os.path.join(sharedFiles["project_directory"], "spis_fieldmanager.log")
        else:
        '''    
        #s.log_filename = os.path.join(GL_EXCHANGE, "spis_fieldmanager.log")
        #self.log_stream = open(self.log_filename, "w")
        #if self.VERBOSE == 1:
        #    print >> sys.stderr, "logfile are written in <" + \
        #    self.log_filename + ">"
        #self.logger.debug("logfile are written in <" + self.log_filename + ">")        
                  
    def GetAllDataField(self):
        '''
        Returns all dataFields.
        '''
        return self.AllDataField

        
    def GetAllMeshField(self):
        '''
        Returns all MeshFields.
        '''
        return self.AllMeshField

        
    def CreateDataField(self, MeshGroupList):
        '''
        Create a new DataField. 
        '''
        for GrpMesh in MeshGroupList.List:
            self.logger.info("DFcreation for group "+`GrpMesh.Id`)
            if (GrpMesh.Material != None and GrpMesh.Material.Id != -1):
               for Data in GrpMesh.Material.DataList.List:
                   self.logger.info("    of data "+Data.Name)
                   if (Data.Name not in self.TmpNameList) and (Data.Id is not -1):
                      # DataField
                      exec(Data.Name+' = DataField()')
                      exec(Data.Name+'.Name='+"'"+Data.Name+"'")
                      exec(Data.Name+'.Type='+"'"+Data.Type+"'")
                      exec(Data.Name+'.Description='+"'"+Data.Description+"'")
                      exec(Data.Name+'.Unit='+"'"+Data.Unit+"'")
                      exec(Data.Name+'.Local='+repr(Data.Local))
                      exec(Data.Name+'.LockedValue='+repr(Data.LockedValue))
                      exec(Data.Name+'.Category = '+'"'+'pre-processing'+'"')
                      exec('self.AllDataField.Add_DataField('+Data.Name+')')
                      
                      # Corresponding Mesh Field
                      exec(Data.Name+'_MF'+' = MeshField()')
                      exec(Data.Name+'_MF'+'.Name='+"'"+Data.Name+"_MF'")
                      exec(Data.Name+'_MF'+'.Local='+repr(Data.Local))
                      exec('self.AllMeshField.Add_MeshField('+Data.Name+'_MF'+')')

                      exec('self.TmpNameList.append('+"'"+Data.Name+"'"+')')
            if (GrpMesh.Plasma != None and GrpMesh.Plasma.Id != -1):
                self.logger.info(GrpMesh.Plasma.Name)
                for Data in GrpMesh.Plasma.DataList.List:
                    self.logger.info("    of data "+Data.Name)
                    if (Data.Name not in self.TmpNameList) and (Data.Id is not -1):
                       # DataField
                       exec(Data.Name+' = DataField()')
                       exec(Data.Name+'.Name='+"'"+Data.Name+"'")
                       exec(Data.Name+'.Type='+"'"+Data.Type+"'")
                       exec(Data.Name+'.Description='+"'"+Data.Description+"'")
                       exec(Data.Name+'.Unit='+"'"+Data.Unit+"'")
                       exec(Data.Name+'.Local='+repr(Data.Local))
                       exec(Data.Name+'.LockedValue='+repr(Data.LockedValue))
                       exec(Data.Name+'.Category = '+'"'+'pre-processing'+'"')
                       exec('self.AllDataField.Add_DataField('+Data.Name+')')

                       # Corresponding Mesh Field
                       exec(Data.Name+'_MF'+' = MeshField()')
                       exec(Data.Name+'_MF'+'.Name='+"'"+Data.Name+"_MF'")
                       exec(Data.Name+'_MF'+'.Local='+repr(Data.Local))
                       exec('self.AllMeshField.Add_MeshField('+Data.Name+'_MF'+')')

                       exec('self.TmpNameList.append('+"'"+Data.Name+"'"+')')
            if (GrpMesh.ElecNode != None and GrpMesh.ElecNode.Id != -1):
               self.logger.info(GrpMesh.ElecNode.Name)
               for Data in GrpMesh.ElecNode.DataList.List:
                   self.logger.info("    of data "+Data.Name)
                   if (Data.Name not in self.TmpNameList) and (Data.Id is not -1):
                       # DataField
                       exec(Data.Name+' = DataField()')
                       exec(Data.Name+'.Name='+"'"+Data.Name+"'")
                       exec(Data.Name+'.Type='+"'"+Data.Type+"'")
                       exec(Data.Name+'.Description='+"'"+Data.Description+"'")
                       exec(Data.Name+'.Unit='+"'"+Data.Unit+"'")
                       exec(Data.Name+'.Local='+repr(Data.Local))
                       exec(Data.Name+'.Category = '+'"'+'pre-processing'+'"')
                       exec(Data.Name+'.LockedValue='+repr(Data.LockedValue))
                       exec('self.AllDataField.Add_DataField('+Data.Name+')')

                       # Corresponding Mesh Field
                       exec(Data.Name+'_MF'+' = MeshField()')
                       exec(Data.Name+'_MF'+'.Name='+"'"+Data.Name+"_MF'")
                       exec(Data.Name+'_MF'+'.Local='+repr(Data.Local))
                       exec('self.AllMeshField.Add_MeshField('+Data.Name+'_MF'+')')

                       exec('self.TmpNameList.append('+"'"+Data.Name+"'"+')')

        counter=0
        for DataFld in self.AllDataField.List:
            counter=counter+1
            DataFld.Id=counter
            # Initialisation of the corresponding MeshField
            self.AllMeshField.List[counter-1].Id=counter
            self.AllMeshField.IdList[counter-1]=counter
            self.AllDataField.List[counter-1].Id=counter
            self.AllDataField.IdList[counter-1]=counter
            DataFld.MeshFieldId = counter
            #if self.VERBOSE == 1:
            #    print >> self.log_stream, DataFld
            #    print >> self.log_stream, self.AllMeshField.List[counter-1]
            #    print >> self.log_stream, self.AllDataField.List[counter-1]
            #self.logger.debug(`DataFld`)

    def FillFields(self, MeshGroupList, mesh):
        '''
        Fill (map) the previously created fields according a list of MeshGroups.
        '''
        #one can have loop over Field list to fill them
        #with appropriate list of Mesh Element and Value
        #In this example there is not conflict between group definition
        #(There is no field living on the element of an interface)
        # Loop over Field defined

        
        self.logger.info("DataField mapping")
        
        
        for DataFld in self.AllDataField.List:
            currentIdFlag = [0 for i in range(mesh.getBiggerId()+1)]
            self.logger.debug("    Mapping DataField "+ str(DataFld.Id) +" on groups:") 

            tmpString = "          "
            for GrpMesh in MeshGroupList.List:
                tmpString = tmpString + str(GrpMesh.Id)+" "
                # List of properties to manage               
                propertyList = [GrpMesh.Material, GrpMesh.Plasma, GrpMesh.ElecNode]

                # Loop on each property
                for localProperty in propertyList:
                    # If local prop is defined (Id is not equal to default value)
                    if (localProperty != None and localProperty.Id != -1):
                        dataList = localProperty.DataList.List
                       
                        # Loop over Data list of
                        for data in dataList:
                            # If DataField is the corresponding DataList
                            if data.Name == DataFld.Name:
                                # Init the right iterator
                                if DataFld.Local is 0:
                                    meshElementIterator = GrpMesh.jMeshGroup.getNodeIterator()
                                if DataFld.Local is 1:
                                    meshElementIterator = GrpMesh.jMeshGroup.getEdgeIterator()
                                if DataFld.Local is 2:
                                    meshElementIterator = GrpMesh.jMeshGroup.getFaceIterator()
                                if DataFld.Local is 3:
                                    meshElementIterator = GrpMesh.jMeshGroup.getCellIterator()
                           
                                # Loop over Mesh Element List in this group and  filling of DataField
                                while(meshElementIterator.hasNext()):
                                    meshElmt = meshElementIterator.next()
                                    if currentIdFlag[meshElmt.getId()] is 0:
                                        currentIdFlag[meshElmt.getId()] = 1
                                        DataFld.ValueList.append(copy(data.Value))
                                        self.AllMeshField.List[DataFld.MeshFieldId-1].MeshElementIdList.append(meshElmt.getId())
                                        self.AllMeshField.List[DataFld.MeshFieldId-1].MeshElementList.append(meshElmt)
            self.logger.debug(tmpString)

    def PrintFields(self):
        '''
        Print fields (deprecated).
        '''
        for DataFld in self.AllDataField.List:
            print >> self.log_stream, DataFld
            print >> self.log_stream, self.AllMeshField.List[DataFld.MeshFieldId-1]
            
            
    def extractSelectedNascapMaterialsList(self, meshGroupListIn, nascapMaterialCataLog):    
        ###############################################################
        #    Conversion of the material properties                    #
        ###############################################################
        selectedNascapMaterialList = [] ## List of Ids (MatIds) of corresponding Nascap materials
        selectedLegacyMatTypeIdList = []
        # old fashion, if we want to export ALL material defined
        #for material in sharedProp['defaultMaterialList'].List:

        self.logger.info("NASCAP materials selection")
        
        # more acceptable approach, we convert only materials set on the system
        # according to the group settings    
        numIndex = 0     
        for group in meshGroupListIn.List:
            material = group.Material
            print material.Name, material.Type
            if ( material.Name != "None" ):
                if ( material.Type == Material.NASCAP_2K_MATERIAL or material.Type == Material.NASCAP_LEGACY_MATERIAL ):
                
                    # first we recover the corresponding NASCAP material
                    tmpMatTypeId =  material.DataList.List[1].Value  # we recover the MatTypeId
                    relatedNascapMaterial = nascapMaterialCataLog.GetElmById(tmpMatTypeId)
                    self.logger.debug("Related NASCAP material: " + relatedNascapMaterial.Name)
                    print material.Name, "---> ", relatedNascapMaterial.Name
                    selectedNascapMaterialList.append([tmpMatTypeId, numIndex, material.Name, material.Description]) #FIX ME: passage Name et Descriptio
                    numIndex = numIndex +1
                    
                elif ( material.Type == Material.LEGACY_MATERIAL or material.Type == None): 
                    selectedLegacyMatTypeIdList.append(1)
                    self.logger.debug("Legacy material found.")
                else: 
                    self.logger.error("Material type not supported")
            else:
                self.logger.warn("Material is None: No material defined")
                
        print "length nascap mat list", len(selectedNascapMaterialList)
        print "length legacy mat list", len(selectedLegacyMatTypeIdList)
        
        if ( len(selectedNascapMaterialList) > 0 and len(selectedLegacyMatTypeIdList) == 0):
            self.logger.info("Nascap based material model")
            self.materialModel = Material.NASCAP_MATERIAL   
            return(selectedNascapMaterialList) 
        
        elif ( len(selectedNascapMaterialList) == 0 and len(selectedLegacyMatTypeIdList) > 0 ):
            self.logger.info("Legacy (built-in) material model (deprecated)")
            self.materialModel = Material.LEGACY_MATERIAL
            return(None)
        else:
            self.logger.error("Hybrid material type: no supported")
            self.materialModel = None
            return(None)
            
            
    def convertMaterialProperties(self, meshGroupListIn, nascapMaterialListIn ):
        """
        This methods scans the mesh groups and map the material properties from the list
        given in entry. The returned value (list) depends on the type of selected properties
        (legacy or NASCAP like). If materials set through the groups are legacy the 
        returned list is None. If the materials set through the groups are NASCAP like
        a list of SPIS-NUM GenericParamSet. 
        
        All data related to the properties are stored in the 'MatTypeId' and 'MatTypeId_MF'
        DataField/MeshField couple. 
        
        The data type is stored in sharedProp['materialModel'].
        
        If data are NASCAP based an additional informations are needed and
        stored in sharedNum:
        - 'uiToNumNascapMaterialCrossNumberingDic'that gives the correspondance 
        
        - nascapParameterSetList returned as output of this method. 
        """
        ###############################################################
        #    Conversion of the material properties                    #
        ###############################################################
        nascapParameterSetList = [] 
        legacyParameterSetList = []
        # old fashion, if we want to export ALL material defined
        #for material in sharedProp['defaultMaterialList'].List:

        self.logger.info("Material properties setting")
        
        # more acceptable approach, we convert only materials set on the system
        # according to the group settings 
        numIndex = 0
        self.uiToNumNascapMaterialCrossNumberingDic = {}
        for group in meshGroupListIn.List:
            material = group.Material
            print material.Name, material.Type
            if ( material.Name != "None" ):
                if ( material.Type == Material.NASCAP_2K_MATERIAL or material.Type == Material.NASCAP_LEGACY_MATERIAL ):
                    parameterModelType = 1
                
                    # first we recover the corresponding NASCAP material
                    tmpMatTypeId =  material.DataList.List[1].Value  # we recover the MatTypeId
                    #print "tmpMatTypeId =", tmpMatTypeId
                    relatedNascapMaterial = nascapMaterialListIn.GetElmById(tmpMatTypeId)
                    self.logger.debug("Related NASCAP material: " + relatedNascapMaterial.Name)
                
                    # and then we recover the corresponding values
                    vect = Vector() #i.e because SPIS-NUM need Vectors (Java layer)
                    
                    for data in relatedNascapMaterial.DataList.List:
                        prop = MaterialProperty( data.Name, data.Type, data.Value, data.Unit, data.Description)
                        vect.add(prop)
                        #print "------->", prop.valuesAsFloat()
                    
                    #nascapParameterSetList.append(GenericParamSet( material.Name, material.Id, material.Description, None, vect)) #Fix me
                    nascapParameterSetList.append(GenericParamSet( material.Name, numIndex, material.Description, None, vect))
                    self.uiToNumNascapMaterialCrossNumberingDic[tmpMatTypeId] = numIndex
                    numIndex = numIndex + 1
                    #self.logger.debug("new Nascap mat")
                    
                elif ( material.Type == Material.LEGACY_MATERIAL or material.Type == None): 
                    parameterModelType = -1
                    legacyParameterSetList.append(1)
                    self.logger.debug("Legacy material found.")
                else: 
                    self.logger.error("Material type not supported")
            else:
                self.logger.warn("Material is None")
                
        print "length nascap mat list", len(nascapParameterSetList)
        print "length legacy mat list", len(legacyParameterSetList)
        
        if ( len(nascapParameterSetList) > 0 and len(legacyParameterSetList) == 0):
            self.logger.info("Nascap based material model")
            self.materialModel = Material.NASCAP_MATERIAL   
            return(nascapParameterSetList) 
        elif ( len(nascapParameterSetList) == 0 and len(legacyParameterSetList) > 0 ):
            self.logger.info("Legacy (built-in) material model (deprecated)")
            self.materialModel = Material.LEGACY_MATERIAL
            return(None)
        else:
            self.logger.error("Hybrid material type: no supported")
            self.materialModel = None
            return(None)
            ## E  
    
    def getMaterialModel(self):
        """
        return the material type (i.e legacy or NASCAP based). See Modules.Properties.Material module.
        """
        return(self.materialModel)   
    
    def getUiToNumNascapMaterialCorresponcanceDic(self):
        """
        return the NASCAP materials UI to Num indexes correspondance list.
        """
        return(self.uiToNumNascapMaterialCrossNumberingDic)
            