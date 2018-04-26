"""
Module of generation of standard NASCAP material. 

**File name:**    MaterialMaker.py

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

# Specific Modules
from Modules.Properties.MaterialNUM         import MaterialNUM
from Modules.Properties.PlasmaNUM           import PlasmaNUM
from Modules.Properties.PlasmaNUMSC         import PlasmaNUMSC
#from Modules.Properties.PlasmaNUMSCThinSurf import PlasmaNUMSCThinSurf
from Modules.Properties.PlasmaNUMBd         import PlasmaNUMBd
from Modules.Properties.ElecNodeNUM         import ElecNodeNUM

# Generic Modules
from Modules.Properties.Material            import Material
from Modules.Properties.MaterialList        import MaterialList
from Modules.Properties.PlasmaList          import PlasmaList
from Modules.Properties.ElecNode            import ElecNode
from Modules.Properties.ElecNodeList        import ElecNodeList
from Modules.Properties.Data                import Data
from Modules.Properties.DataList            import DataList



class MaterialMaker:
    '''
    Module of generation of default material and plasmas property models. Please see, 
    the documentation for more information.
    '''

    def __init__(s):
        print '##############################################'
        print '# Module of definition of material, plasma   #'
        print '# and electric node properties               #'
        print '##############################################'


    def BuildDefaultMaterialList(s):
        # Initialisation of a few different materials with different thickness and default values for other data

	
        DefaultMaterialList = MaterialList()

        # ITOC (material type = 0)
        Comment='Material coated with ITO, other parameters set to default: sunlit, interactions on, 125 microns thick, 300K, basic material model (based on NASCAP properties)'
        ValueList=[0, 0, 0.000125, 1, 1, 1, 1, 1, 1, 300, 1] 
        DefaultMaterialList.Add(MaterialNUM(0,'ITO, default',Comment,ValueList))
        DefaultMaterialList.Add(MaterialNUM(1,'ITO, shade','ITO, default + in shade', [0, 0, 0.000125, 1, 1, 1, 1, 1, 1, 300, 0]))
        DefaultMaterialList.Add(MaterialNUM(2,'ITO, interactions off','ITO, default + interactions off', [0, 0, 0.000125, 0, 0, 0, 0, 0, 0, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(3,'ITO, shade, interactions off','ITO, default + interactions off + in shade', [0, 0, 0.000125, 0, 0, 0, 0, 0, 0, 300, 0]))

        # CERS (material type = 1)
        Comment='Solar cell material, Cerium doped silicon with MgF2 coating, other params set to default: 100 microns thick, 350K, sunlit, interactions on, basic material model (based on NASCAP properties)'
        ValueList=[0, 1, 0.000100, 1, 1, 1, 1, 1, 1, 350, 1] 
        DefaultMaterialList.Add(MaterialNUM(100,'CERS, default',Comment,ValueList))
        DefaultMaterialList.Add(MaterialNUM(101,'CERS, shade, T=-50C','CERS, default + no sun + T=223K',[0, 1, 0.000100, 1, 1, 1, 1, 1, 1, 223, 0]))
        DefaultMaterialList.Add(MaterialNUM(102,'CERS, interactions off','CERS, default + interactions off',[0, 1, 0.000100, 0, 0, 0, 0, 0, 0, 350, 1]))
        DefaultMaterialList.Add(MaterialNUM(102,'CERS, shade, T=-50C, interactions off','CERS, default + no sun + T=223K + interactions off',[0, 1, 0.000100, 0, 0, 0, 0, 0, 0, 223, 0]))
        
        # CFRP (material type = 2)
        Comment='Carbon fibre, conducting, no resin layer, other params set to default: 1 mm thick, 300K, shade, interactions on, basic material model (based on NASCAP properties)'
        ValueList=[0, 2, 0.001, 1, 1, 1, 1, 1, 1, 300, 0] 
        DefaultMaterialList.Add(MaterialNUM(200,'CFRP, default',Comment,ValueList))

        # Kapton (material type = 3)
        Comment='Kapton (R), other params set to default: 50 microns thick, sunlit, interactions on, 373K, basic material model (based on NASCAP properties)'
        ValueList=[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1] 
        DefaultMaterialList.Add(MaterialNUM(300,'Kapton, default',Comment,ValueList))
        DefaultMaterialList.Add(MaterialNUM(301,'Kapton, 25 microns','Kapton, default + 25 microns',[0, 3, 0.000025, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(302,'Kapton, shade','Kapton, default + in shade + T=-50K', [0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 223, 0]))
        DefaultMaterialList.Add(MaterialNUM(303,'Kapton, 25 microns, shade','Kapton, default + 25 microns + in shade + T=-50K',[0, 3, 0.000025, 1, 1, 1, 1, 1, 1, 223, 0]))
        DefaultMaterialList.Add(MaterialNUM(304,'Kapton, interactions off','Kapton, default + interactions off',[0, 3, 0.000050, 0, 0, 0, 0, 0, 0, 300, 1]))

        # other Nascap based materials
        DefaultMaterialList.Add(MaterialNUM(400,'cosr, default','Optical solar reflector without MgF2 coating. Cerium doped glass type MARECS/ECS, 150 microns',[0, 4, 0.000150, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(500,'Epoxy','Thin layer of Epoxy resin on (conducting) Carbon fibre, 2 microns',[0, 5, 0.000002, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(600,'blkp','Non conductive black paint. SEE yields are as measured for Electrodag 501. 25 microns',[0, 6, 0.000025, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(700,'blkh','Non conductive black paint HERBERTS 1002-E. Values updated 3.10.88. Conduct. measured by ESTEC, SEE yield by DERTS. 400 microns',[0, 7, 0.000400, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(800,'blkc','Conductive black paint Electrodag 501',[0, 8, 0.001, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(900,'PCB-Z','White paint PCB-Z assumed to be conductive in space',[0, 9, 0.000070, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000,'PSG 120 ','White paint PSG 120 FD assumed to be conductive in space. Becomes conductive and FLUORESCENT under irradiation. SEE measurements by DERTS',[0, 10, 0.000070, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1100,'Teflon','Teflon, DERTS measurements of SEE, 25 microns',[0, 11, 0.000025, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1200,'cont','Generic Dielectric after 5 years in GEO environment (contaminated), 100 microns',[0, 12, 0.000100, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1300,'Gold','Gold, default',[0, 13, 0.001000, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1400,'Silver','Silver as from NASCAP library',[0, 14, 0.001000, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1500,'Al oxyde','Oxydized Aluminium.  SEE yields from DERTS for Aluminium/Kapton. 10 microns',[0, 15, 0.000010, 1, 1, 1, 1, 1, 1, 300, 1]))
        DefaultMaterialList.Add(MaterialNUM(1600,'Steel','Steel, SEE sigma +Emax from DERTS, curve shape from CONT material',[0, 16, 0.001000, 1, 1, 1, 1, 1, 1, 300, 1]))

        # extra materials, to be user-modified
        DefaultMaterialList.Add(MaterialNUM(1000001,'TBD material 1','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000002,'TBD material 2','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000003,'TBD material 3','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000004,'TBD material 4','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000005,'TBD material 5','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000006,'TBD material 6','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000007,'TBD material 7','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000008,'TBD material 8','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000009,'TBD material 9','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))
        DefaultMaterialList.Add(MaterialNUM(1000010,'TBD material 10','extra material value set, to be modified by user (initialised to Kapton default)',[0, 3, 0.000050, 1, 1, 1, 1, 1, 1, 373, 1]))

        print "Default material generated."
        return(DefaultMaterialList)


    def BuildDefaultPlasmaList(s):
        
        # Initialisation of Plasma variables
        DefaultPlasmaList = PlasmaList()

        #######################################
        # Default values for the plasma model #
        #######################################

        #################################################
        # Definition of Initial and Boundary Conditions #
        # for the plasma model in volum                 #
        # This is based on the PlasmaNUM class          #
        #################################################
        PlasmaSN = PlasmaNUM( 100,                                       # Id of the property
                              'Plasma Model in Volume, default',         # Name 
                              'Default volume settings: no volume interaction nor background density',  # Description
                                                                         # list of values and correspoding flag in SpisNum  
                              [0,                                        # surfFlag
                               0,                                        # edgeFlag
                               0,                                        # nodeFlag
                               [0.,0.,0.],                               # xyz 
                               0,                                        # VolInteracFlag
                               0.0])                                     # BackGroundDens
        DefaultPlasmaList.Add_Plasma(PlasmaSN)


       

        #################################################
        # Definition of Initial and Boundary Conditions #
        # for the plasma model on the SC surface        #
        # To the PlasmaNUM data, we add specific values #
        # issued from the PlasmaNUMSC class             #
        #################################################
        PlasmaSC = PlasmaNUMSC( 200,
                              'Spacecraft, default',
                              'Default SC settings: 0 Dirichlet potential, no source',
                                                   # list of values and corresponding flags in SpisNum
                              [1,                  # surfFlag
                               1,                  # edgeFlag
                               1,                  # nodeFlag
                               [0.,0.,0.],         # xyz
                               0,                  # VolInteracFlag
                               0.0,                # BackGroundDens
                               0,                  # surfFlagS 
                               0,                  # surfThicknessS
                               0,                  # edgeFlagS
                               0.,                  # edgeRadiusS
                               0,                  # nodeFlagS
                               [0.,0.,0.],         # xyzS
                               1,                  # SCDiriFlag
                               0.0,                # SCDiriPot
                               0.0,                # SCDiriPotEdge
                               0.0,                # SCDiriPotSurf
                               0,                  # SCFourFlag
                               1.,                 # SCFourAlpha
                               0.,                 # SCFourValue
                               -1,                 # SourceId
                               0.,                 # SourceCurrent
                               1.,                 # SourceTemp
                               0.0])               # SourceMach
        DefaultPlasmaList.Add_Plasma(PlasmaSC)
        

        #################################################
        # Definition of Initial and Boundary Conditions #
        # for the plasma model on the SC surface for    #
        #                  THIN WIRES                   #
        # To the PlasmaNUM data, we add specific values #
        # issued from the PlasmaNUMSC class             #
        #################################################
        PlasmaSC = PlasmaNUMSC( 201,
                              'Spacecraft Boundary Plasma Model,  THIN WIRES',
                              'SC settings: THIN WIRES, 0 Dirichlet potential, no source',
                                                   # list of values and correspoding flag in SpisNum
                              [1,                  # surfFlag
                               5,                  # edgeFlag
                               5,                  # nodeFlag
                               [0.,0.,0.],         # xyz
                               0,                  # VolInteracFlag
                               0.0,               # BackGroundDens
                               0,                 # surfFlagS
                               0,                 # surfThicknessS
                               1,                 # edgeFlagS
                               .001,              # edgeRadiusS
                               1,                 # nodeFlagS
                               [0.,0.,0.],        # xyzS
                               1,                 # SCDiriFlag
                               0.0,               # SCDiriPot
                               0.0,               # SCDiriPotEdge
                               0.0,               # SCDiriPotSurf
                               0,                 # SCFourFlag
                               1.,                # SCFourAlpha
                               0.,                # SCFourValue
                               -1,                 # SourceId
                               0.,                # SourceCurrent
                               1.,                # SourceTemp
                               0.])               # SourceMach
        
        # we add this property to the DefaultPlasmaList
        DefaultPlasmaList.Add_Plasma(PlasmaSC)
      

        #################################################
        # Definition of Initial and Boundary Conditions #
        # for the plasma model on the external surface  #
        #################################################
        PlasmaBd = PlasmaNUM( 300,
                              'Boundary, default',
                              'Default boundary settings: Fourier (alpha=1), particle injection on, outgoing particle to a sink',
                              [8,
                               8,
                               8,
                               [0.,0.,0.],
                               0,
                               0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,1,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        
        #######################################################################
        # Definition of Initial and Boundary Conditions for the plasma model  #
        #        on the SC surface  on THIN SURFACES                          #
        # To the PlasmaNUM data, we add specific values issued from the       #
        # PlasmaNUMSC class                                                   #
        #######################################################################        
        PlasmaSCTHINA = PlasmaNUM( 2005,
                          'Spacecraft THIN SURFACE, face A, no border, default',
                          'Default SC settings: 0 Dirichlet potential, no source, TBC!!!',
                                             # list of values and correspoding flag in SpisNum
                                             # these values are defined everywhere on the mesh
                          [3,                  # surfFlag
                           3,                  # edgeFlag      TBC, corrected JFR
                           3,                  # nodeFlag
                           [0.,0.,0.],         # xyz
                           0,                  # VolInteracFlag
                           0.0,               # BackGroundDens
                           2,             # surfFlagS
                            0,             # surfThicknessS
                            2,             # edgeFlagS
                            .001,          # edgeRadiusS
                            2,             # nodeFlagS
                           [0.,0.,0.],    # xyzS
                           1,             # SCDiriFlag
                           0.0,           # SCDiriPot
                           0.0,           # SCDiriPotEdge
                           0.0,           # SCDiriPotSurf
                           0,             # SCFourFlag
                           1.,            # SCFourAlpha
                           0.,            # SCFourValue
                           -1,            # SourceId
                           0.,            # SourceCurrent
                           1.,            # SourceTemp
                           0.,            # SourceMach
                           1.0,           # surfIndexSC     TBC
                           1.0,           # edgeIndexSC     TBC
                           1.0,           # nodeIndexSC     TBC
                           ])
        DefaultPlasmaList.Add_Plasma(PlasmaSCTHINA)



#        PlasmaSCTHINB = PlasmaNUM( 2006,
#                              'Spacecraft THIN SURFACE, face B, no border, default',
#                              'Default SC settings: 0 Dirichlet potential, no source, TBC !!!',
#                                                 # list of values and correspoding flag in SpisNum
#                              [3,                  # surfFlag
#                               35,                  # edgeFlag      TBC, corrected JFR
#                               35,                  # nodeFlag
#                               [0.,0.,0.],         # xyz
#                               0,                  # VolInteracFlag
#                               0.0])               # BackGroundDens
        
        # now we add fields related to the SC THIN surface, border excluded
        #        PlasmaTmpSC = PlasmaNUMSC( -1,           # the PlasmaNUMSC object is just tmp
        #                                   None,         # it is not needed to give it name and so on...
        #                                   None,
        #                                                  # list of values and correspoding flag in SpisNum
        #                                                  #these value are defined only on the related-submesh
        #                                   [34,            # surfFlagS
        #                                    0,             # surfThicknessS
        #                                    34,            # edgeFlagS
        #                                    .001,          # edgeRadiusS
        #                                    34,            # nodeFlagS
        #                                    [0.,0.,0.],    # xyzS
        #                                    1,             # SCDiriFlag
        #                                    0.0,           # SCDiriPot
        #                                    0.0,           # SCDiriPotEdge
        #                                    0.0,           # SCDiriPotSurf
        #                                    0,             # SCFourFlag
        #                                    1.,            # SCFourAlpha
        #                                    0.,            # SCFourValue
        #                                    -1,            # SourceId
        #                                    0.,            # SourceCurrent
        #                                    1.,            # SourceTemp
        #                                    0.,            # SourceMach
        #                                    1.0,           # surfIndexSC     TBC
        #                                    1.0,           # edgeIndexSC     TBC
        #                                    1.0,           # nodeIndexSC     TBC
        #                                    ])
        #        for DataTmp in PlasmaTmpSC.DataList.List:
        #            PlasmaSCTHINB.DataList.Add_Data(DataTmp)                           
        #DefaultPlasmaList.Add_Plasma(PlasmaSCTHINB)
        
        
                
#        PlasmaSCTHINABorder = PlasmaNUM( 2007,
#                              'Spacecraft THIN SURFACE, face A, border, default',
#                              'Default SC settings: 0 Dirichlet potential, no source, TBC !!!',
#                                                 # list of values and correspoding flag in SpisNum
#                              [3,                  # surfFlag
#                               19,                  # edgeFlag      TBC, corrected JFR
#                               19,                  # nodeFlag
#                               [0.,0.,0.],         # xyz
#                               0,                  # VolInteracFlag
#                               0.0])               # BackGroundDens

        # now we add fields related to the SC THIN surface, border excluded
        #        PlasmaTmpSC = PlasmaNUMSC( -1,           # the PlasmaNUMSC object is just tmp
        #                                   None,         # it is not needed to give it name and so on...
        #                                   None,
        #                                                  # list of values and correspoding flag in SpisNum
        #                                                  #these value are defined only on the related-submesh
        #                                   [2,             # surfFlagS
        #                                    0,             # surfThicknessS
        #                                    18,            # edgeFlagS
        #                                    .001,          # edgeRadiusS
        #                                    18,            # nodeFlagS
        #                                    [0.,0.,0.],    # xyzS
        #                                    1,             # SCDiriFlag
        #                                    0.0,           # SCDiriPot
        #                                    0.0,           # SCDiriPotEdge
        #                                    0.0,           # SCDiriPotSurf
        #                                    0,             # SCFourFlag
        #                                    1.,            # SCFourAlpha
        #                                    0.,            # SCFourValue
        #                                    -1,            # SourceId
        #                                    0.,            # SourceCurrent
        #                                    1.,            # SourceTemp
        #                                    0.,            # SourceMach
        #                                    1.0,           # surfIndexSC     TBC
        #                                    1.0,           # edgeIndexSC     TBC
        #                                    1.0,           # nodeIndexSC     TBC
        #                                    ])
        #        for DataTmp in PlasmaTmpSC.DataList.List:
        #            PlasmaSCTHINABorder.DataList.Add_Data(DataTmp)
#        DefaultPlasmaList.Add_Plasma(PlasmaSCTHINABorder)  
                           
#        PlasmaSCTHINBBorder = PlasmaNUM( 2008,
#                              'Spacecraft THIN SURFACE, face B, border, default',
#                              'Default SC settings: 0 Dirichlet potential, no source, TBC !!!',
#                                                 # list of values and correspoding flag in SpisNum
#                              [3,                  # surfFlag
#                               51,                  # edgeFlag      TBC, corrected JFR
#                               51,                  # nodeFlag
#                               [0.,0.,0.],         # xyz
#                               0,                  # VolInteracFlag
#                               0.0])               # BackGroundDens

        # now we add fields related to the SC THIN surface, border excluded
        #        PlasmaTmpSC = PlasmaNUMSC( -1,           # the PlasmaNUMSC object is just tmp
        #                                   None,         # it is not needed to give it name and so on...
        #                                   None,
        #                                                  # list of values and correspoding flag in SpisNum
        #                                                  #these value are defined only on the related-submesh
        #                                   [34,            # surfFlagS
        #                                    0,             # surfThicknessS
        #                                    50,            # edgeFlagS
        #                                    .001,          # edgeRadiusS
        #                                    50,            # nodeFlagS
        #                                    [0.,0.,0.],    # xyzS
        #                                    1,             # SCDiriFlag
        #                                    0.0,           # SCDiriPot
        #                                    0.0,           # SCDiriPotEdge
        #                                    0.0,           # SCDiriPotSurf
        #                                    0,             # SCFourFlag
        #                                    1.,            # SCFourAlpha
        #                                    0.,            # SCFourValue
        #                                    -1,            # SourceId
        #                                    0.,            # SourceCurrent
        #                                    1.,            # SourceTemp
        #                                    0.,            # SourceMach
        #                                    1.0,           # surfIndexSC     TBC
        #                                    1.0,           # edgeIndexSC     TBC
        #                                    1.0,           # nodeIndexSC     TBC
        #                                    ])
        #        for DataTmp in PlasmaTmpSC.DataList.List:
        #            PlasmaSCTHINBBorder.DataList.Add_Data(DataTmp)
        #DefaultPlasmaList.Add_Plasma(PlasmaSCTHINBBorder)    
                                     

        # Other spacecraft values
        PlasmaSC = PlasmaNUMSC(210,'Spacecraft, pot = -1000','default settings + potential changed to -1000V',
                             [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,-1000.0,-1000.0,-1000.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)
        
        PlasmaSC=PlasmaNUMSC(211,'Spacecraft, pot = -20','default settings + potential changed to -20V',
                                [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,-20.0,-20.0,-20.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)
        
        PlasmaSC=PlasmaNUMSC(220,'Spacecraft, source 1 on','default settings + source 1 on (broad Xenon plume: Xe+, 600 A/m2, 30 eV, Mach 0)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,1,600.,30.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(221,'Spacecraft, source 2 on','default settings + source 2 on (typical SPT thruster: Xe+, 600 A/m2, 30 eV, Mach 10)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,2,600.,30.,10.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC = PlasmaNUMSC(222,'Spacecraft, source 3 on','default settings + source 3 on (plausible high current electron source such as a hollow cathode: 1 eV, 1000 A/m2...)',
                                [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,3,1000.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(223,'Spacecraft, source 1 on (Mach 7), pot = -20V','default settings + source 1 on (Xenon plume: Xe+, 600 A/m2, 5 eV, Mach 7)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,-20.0,-20.0,-20.0,0,1.,0.,1,600.,5.,7.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(231,'Spacecraft, TBD 1','extra SC plasma value set, to be modified by user (initialized to default, pot=0, no source)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(232,'Spacecraft, TBD 2','extra SC plasma value set, to be modified by user (initialized to default, pot=0, no source)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(233,'Spacecraft, TBD 3','extra SC plasma value set, to be modified by user (initialized to default, pot=0, no source)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(234,'Spacecraft, TBD 4','extra SC plasma value set, to be modified by user (initialized to default, pot=0, no source)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

        PlasmaSC=PlasmaNUMSC(235,'Spacecraft, TBD 5','extra SC plasma value set, to be modified by user (initialized to default, pot=0, no source)',
                              [1,1,1,[0.,0.,0.],0,0.0, 0,0,0,0.0,0,[0.,0.,0.],1,0.0,0.0,0.0,0,1.,0.,-1,0.,1.,0.])
        DefaultPlasmaList.Add_Plasma(PlasmaSC)


        #################################################
        #         a few customised Plasmas              #
        #################################################
        PlasmaSC = PlasmaNUM( 250,
                              'Spacecraft, source 2, typical of neutral',
                              'Default SC settings + source 2 on, 1 mA (of neutrals!), 0.05eV, Mach 0',
                                                 # list of values and corresponding flag in SpisNum
                              [1,                  # surfFlag
                               1,                  # edgeFlag
                               1,                  # nodeFlag
                               [0.,0.,0.],         # xyz
                               0,                  # VolInteracFlag
                               0.0,               # BackGroundDens
                               0,             # surfFlagS 
                               0,             # surfThicknessS
                               0,             # edgeFlagS
                               0.0,             # edgeRadiusS
                               0,             # nodeFlagS
                               [0.,0.,0.],    # xyzS
                               1,             # SCDiriFlag
                               0.0,           # SCDiriPot
                               0.0,           # SCDiriPotEdge
                               0.0,           # SCDiriPotSurf
                               0,             # SCFourFlag
                               1.,            # SCFourAlpha
                               0.,            # SCFourValue
                               2,             # SourceId
                               0.001,         # SourceCurrent
                               0.05,          # SourceTemp
                               0.])           # SourceMach
                               
        # we add this property to the DefaultPlasmaList
        DefaultPlasmaList.Add_Plasma(PlasmaSC)

    
        # Other boundary values
        PlasmaBd=PlasmaNUM(310,'Boundary, no injection','default settings + particle injection off',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,0,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(311,'Boundary, no injection, pot = 0','default settings + particle injection off + quasi-Dirichlet potential = 0 (alpha->infinity)',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1000000.,0.,0,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(320,'Boundary, symmetry','symmetry conditions: Neumann (Fourier alpha=0), no injection, outgoing particle reflected',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,0.,0.,0,1])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(331,'Boundary, TBD 1','extra boundary plasma value set, to be modified by user (initialized to default)',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,1,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(332,'Boundary, TBD 2','extra boundary plasma value set, to be modified by user (initialized to default)',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,1,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(333,'Boundary, TBD 3','extra boundary plasma value set, to be modified by user (initialized to default)',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,1,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(334,'Boundary, TBD 4','extra boundary plasma value set, to be modified by user (initialized to default)',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,1,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaBd=PlasmaNUM(335,'Boundary, TBD 5','extra boundary plasma value set, to be modified by user (initialized to default)',[8,8,8,[0.,0.,0.],0,0.0])
        PlasmaTmpBd=PlasmaNUMBd(-1,None,None,[0,0,0,[0.,0.,0.],0,0.,1,1.,0.,1,0])
        for DataTmp in PlasmaTmpBd.DataList.List:
            PlasmaBd.DataList.Add_Data(DataTmp)
        DefaultPlasmaList.Add_Plasma(PlasmaBd)

        PlasmaSN=PlasmaNUM(110,'Volume, interaction on','default settings + volume interaction on + background density = 1 m-3',[0,0,0,[0.,0.,0.],1,1.0])
        DefaultPlasmaList.Add_Plasma(PlasmaSN)
        
        PlasmaId = 335  # the last max Id above.
        
        # Other volume values
        nbOtherPlasma = 10
        for plasmaIndex in xrange(nbOtherPlasma):
            PlasmaId = PlasmaId+1
            PlasmaSN=PlasmaNUM(PlasmaId,'Volume, TBD 1','extra volume plasma value set, to be modified by user (initialized to default)',[0,0,0,[0.,0.,0.],0,0.0])
            DefaultPlasmaList.Add_Plasma(PlasmaSN)

                

        '''
        PlasmaSN=PlasmaNUM(121,'Volume, TBD 1','extra volume plasma value set, to be modified by user (initialized to default)',[0,0,0,[0.,0.,0.],0,0.0])
        DefaultPlasmaList.Add_Plasma(PlasmaSN)

        PlasmaSN=PlasmaNUM(122,'Volume, TBD 2','extra volume plasma value set, to be modified by user (initialized to default)',[0,0,0,[0.,0.,0.],0,0.0])
        DefaultPlasmaList.Add_Plasma(PlasmaSN)

        PlasmaSN=PlasmaNUM(123,'Volume, TBD 3','extra volume plasma value set, to be modified by user (initialized to default)',[0,0,0,[0.,0.,0.],0,0.0])
        DefaultPlasmaList.Add_Plasma(PlasmaSN)

        PlasmaSN=PlasmaNUM(124,'Volume, TBD 4','extra volume plasma value set, to be modified by user (initialized to default)',[0,0,0,[0.,0.,0.],0,0.0])
        DefaultPlasmaList.Add_Plasma(PlasmaSN)

        PlasmaSN=PlasmaNUM(125,'Volume, TBD 5','extra volume plasma value set, to be modified by user (initialized to default)',[0,0,0,[0.,0.,0.],0,0.0])
        DefaultPlasmaList.Add_Plasma(PlasmaSN)
        '''

        print "Default plasma generated."
        
        return(DefaultPlasmaList)



    def BuildDefaultElecNodeList(s):
        
        #total number of electrical nodes        
        nbElecNode = 20
        
        # Initialisation of ElecNode variable
        DefaultElecNodeList=ElecNodeList()
        
        DefaultElecNodeList.Add_ElecNode(ElecNodeNUM(0,'Spacecraft ground (ElecNode-0)','electric node 0 (SC ground)',[0]))
        
        for elecNodeIndex in xrange(nbElecNode):
            elecNodeId = elecNodeIndex + 1
            #print elecNodeId,'ElecNode-'+`elecNodeId`,`elecNodeId`+'th electric node',[elecNodeId]
            DefaultElecNodeList.Add_ElecNode(ElecNodeNUM(elecNodeId,'ElecNode-'+`elecNodeId`,`elecNodeId`+'th electric node',[elecNodeId]))
            
        print "Default electrical nodes generated."
        
        return(DefaultElecNodeList)
