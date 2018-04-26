
//////////////////////////////////////////////////////////////
//                          Box                             //
//                                                          //
//                                                          //
// This system can be translated                            //
// No physical groups are pre -built                        //
//                                                          //
// Please take to the volume definition in case of insertion//
// into an external system.                                 //
//                                                          //
// author: J.Forest, Artenum SARL                           //
//////////////////////////////////////////////////////////////


// settings parameters
// default values

// Description of the template variables (used by Keridwen Gmsh template parser)
//# Negative half Sphere
//@ halfSphereInitialId # int # Id of the first element in the geo file
//@ halfSphereResolution # float # Negative half sphere resolution
//@ xCenter # float # x center of the sphere
//@ yCenter # float # y center of the sphere
//@ zCenter # float # z center of the sphere
//@ radius # float # radius of the sphere (meter)

halfSphereInitialId = 0;

halfSphereResolution = 1.0;

// Half sphere definition
xCenter = 0.0;
yCenter = 0.0;
zCenter = 0.0;

radius = 1.0;

////////////////////// END OF THE SETTINGS /////////////////////////

///////////////////////////////////////////////////////////
// DO NOT EDIT BELOW
///////////////////////////////////////////////////////////

Point(halfSphereInitialId + 1) = {xCenter, yCenter, zCenter, halfSphereResolution};
Point(halfSphereInitialId + 2) = {xCenter, yCenter + radius, zCenter, halfSphereResolution};
Point(halfSphereInitialId + 3) = {xCenter + radius, yCenter, zCenter, halfSphereResolution};
Point(halfSphereInitialId + 4) = {xCenter, yCenter - radius, zCenter, halfSphereResolution};
Point(halfSphereInitialId + 5) = {xCenter - radius, yCenter, zCenter, halfSphereResolution};
Point(halfSphereInitialId + 6) = {xCenter, yCenter, zCenter - radius, halfSphereResolution};

Circle(halfSphereInitialId + 7) = {halfSphereInitialId + 2, halfSphereInitialId + 1, halfSphereInitialId + 3};
Circle(halfSphereInitialId + 8) = {halfSphereInitialId + 3, halfSphereInitialId + 1, halfSphereInitialId + 4};
Circle(halfSphereInitialId + 9) = {halfSphereInitialId + 4, halfSphereInitialId + 1, halfSphereInitialId + 5};
Circle(halfSphereInitialId + 10) = {halfSphereInitialId + 5, halfSphereInitialId + 1, halfSphereInitialId + 2};
Circle(halfSphereInitialId + 11) = {halfSphereInitialId + 2, halfSphereInitialId + 1, halfSphereInitialId + 6};
Circle(halfSphereInitialId + 12) = {halfSphereInitialId + 3, halfSphereInitialId + 1, halfSphereInitialId + 6};
Circle(halfSphereInitialId + 13) = {halfSphereInitialId + 4, halfSphereInitialId + 1, halfSphereInitialId + 6};
Circle(halfSphereInitialId + 14) = {halfSphereInitialId + 5, halfSphereInitialId + 1, halfSphereInitialId + 6};

Line Loop (halfSphereInitialId + 15) = {halfSphereInitialId + 7, halfSphereInitialId + 12, -(halfSphereInitialId + 11)};
Ruled Surface (halfSphereInitialId + 16) = {halfSphereInitialId + 15};
Line Loop (halfSphereInitialId + 17) = {halfSphereInitialId + 8, halfSphereInitialId + 13, -(halfSphereInitialId + 12)};
Ruled Surface (halfSphereInitialId + 18) = {halfSphereInitialId + 17};
Line Loop (halfSphereInitialId + 19) = {halfSphereInitialId + 9, halfSphereInitialId + 14, -(halfSphereInitialId + 13)};
Ruled Surface (halfSphereInitialId + 20) = {halfSphereInitialId + 19};
Line Loop (halfSphereInitialId + 21) = {halfSphereInitialId + 10, halfSphereInitialId + 11, -(halfSphereInitialId + 14)};
Ruled Surface (halfSphereInitialId + 22) = {halfSphereInitialId + 21};
Line Loop (halfSphereInitialId + 23) = {halfSphereInitialId + 7, halfSphereInitialId + 8, halfSphereInitialId + 9, halfSphereInitialId + 10};
Ruled Surface (halfSphereInitialId + 24) = {halfSphereInitialId + 23};

Surface Loop(halfSphereInitialId + 25) = {halfSphereInitialId + 24, halfSphereInitialId + 22, halfSphereInitialId + 20, halfSphereInitialId + 18, halfSphereInitialId + 16};
Volume(halfSphereInitialId + 26) = {halfSphereInitialId + 25};