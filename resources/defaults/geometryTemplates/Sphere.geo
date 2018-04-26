
//////////////////////////////////////////////////////////////
//     Simple spherical model (for external bounds)         //
//                                                          //
//                                                          //
// This system can be translated                            //
// No physical groups are pre -built                        //
//                                                          //
// Please take to the volume definition in case of insertion//
//into an external system.                                  //
//                                                          //
// author: J.Forest, Artenum SARL                           //
//////////////////////////////////////////////////////////////


// settings parameters
// default values

// Description of the template variables (used by Keridwen Gmsh template parser)
//# Sphere
//@ extSphereInitialId # int # Id of the first element in the geo file
//@ extRadius # float # Sphere radius
//@ extResol # float # Sphere resolution
//@ translateX # float # Sphere centre, X coordinate
//@ translateY # float # Sphere centre, Y coordinate
//@ translateZ # float # Sphere centre, Z coordinate

extSphereInitialId = 1000;

extRadius = 2.5;
extResol = 0.30;

translateX = 0.0;
translateY = 0.0;
translateZ = 0.0;

///////////////////////////////////////////////////////////
// DO NOT EDIT BELOW
///////////////////////////////////////////////////////////
// extSphere
Point(extSphereInitialId+1) = {extRadius+0.0, 0.0, 0.0, extResol};
Point(extSphereInitialId+2) = {-extRadius+0.0, 0.0, 0.0, extResol};
Point(extSphereInitialId+3) = {0.0, extRadius+0.0, 0.0, extResol};
Point(extSphereInitialId+4) = {0.0, -extRadius+0.0, 0.0, extResol};
Point(extSphereInitialId+5) = {0.0, 0.0, extRadius+0.0, extResol};
Point(extSphereInitialId+6) = {0.0, 0.0, -extRadius+0.0, extResol};
Point(extSphereInitialId+7) = {0.0, 0.0, 0.0, extResol};

Circle (extSphereInitialId+9) = {extSphereInitialId+4, extSphereInitialId+7, extSphereInitialId+1};
Circle (extSphereInitialId+10) = {extSphereInitialId+4, extSphereInitialId+7, extSphereInitialId+5};
Circle (extSphereInitialId+11) = {extSphereInitialId+1, extSphereInitialId+7, extSphereInitialId+5};
Circle (extSphereInitialId+12) = {extSphereInitialId+4, extSphereInitialId+7, extSphereInitialId+2};
Circle (extSphereInitialId+13) = {extSphereInitialId+2, extSphereInitialId+7, extSphereInitialId+5};
Circle (extSphereInitialId+14) = {extSphereInitialId+2, extSphereInitialId+7, extSphereInitialId+3};
Circle (extSphereInitialId+15) = {extSphereInitialId+3, extSphereInitialId+7, extSphereInitialId+1};
Circle (extSphereInitialId+16) = {extSphereInitialId+6, extSphereInitialId+7, extSphereInitialId+3};
Circle (extSphereInitialId+17) = {extSphereInitialId+6, extSphereInitialId+7, extSphereInitialId+2};
Circle (extSphereInitialId+18) = {extSphereInitialId+6, extSphereInitialId+7, extSphereInitialId+4};
Circle (extSphereInitialId+19) = {extSphereInitialId+6, extSphereInitialId+7, extSphereInitialId+1};
Circle (extSphereInitialId+20) = {extSphereInitialId+3, extSphereInitialId+7, extSphereInitialId+5};

Line Loop (extSphereInitialId+22) = {extSphereInitialId+12, -(extSphereInitialId+17), extSphereInitialId+18};
Ruled Surface (extSphereInitialId+22) = {extSphereInitialId+22};

Line Loop (extSphereInitialId+24) = {extSphereInitialId+10, -(extSphereInitialId+13), -(extSphereInitialId+12)};
Ruled Surface (extSphereInitialId+24) = {extSphereInitialId+24};

Line Loop (extSphereInitialId+26) = {extSphereInitialId+13, -(extSphereInitialId+20), -(extSphereInitialId+14)};
Ruled Surface (extSphereInitialId+26) = {extSphereInitialId+26};

Line Loop (extSphereInitialId+28) = {extSphereInitialId+14, -(extSphereInitialId+16), extSphereInitialId+17};
Ruled Surface (extSphereInitialId+28) = {extSphereInitialId+28};

Line Loop (extSphereInitialId+30) = {extSphereInitialId+11, -(extSphereInitialId+10), extSphereInitialId+9};
Ruled Surface (extSphereInitialId+30) = {extSphereInitialId+30};

Line Loop (extSphereInitialId+32) = {extSphereInitialId+11, -(extSphereInitialId+20), extSphereInitialId+15};
Ruled Surface (extSphereInitialId+32) = {extSphereInitialId+32};

Line Loop (extSphereInitialId+34) = {extSphereInitialId+15, -(extSphereInitialId+19), extSphereInitialId+16};
Ruled Surface (extSphereInitialId+34) = {extSphereInitialId+34};

Line Loop (extSphereInitialId+36) = {extSphereInitialId+9, -(extSphereInitialId+19), extSphereInitialId+18};
Ruled Surface (extSphereInitialId+36) = {extSphereInitialId+36};

// translation function
Translate {translateX, translateY, translateZ} {
  Surface{extSphereInitialId + 34, extSphereInitialId + 32, extSphereInitialId + 26, extSphereInitialId + 24, extSphereInitialId + 36, extSphereInitialId + 30, extSphereInitialId + 22, extSphereInitialId + 28};
}
