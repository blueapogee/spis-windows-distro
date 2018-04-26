
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
//# Plane Surface
//@ planeInitialId # int # Id of the first element in the geo file
//@ planeResolution # float # Plane surface resolution
//@ x1 # float # x coordinate of the first point defining the plane surface
//@ y1 # float # y coordinate of the first point defining the plane surface
//@ z1 # float # z coordinate of the first point defining the plane surface
//@ x2 # float # x coordinate of the second point defining the plane surface
//@ y2 # float # y coordinate of the second point defining the plane surface
//@ z2 # float # z coordinate of the second point defining the plane surface
//@ x3 # float # x coordinate of the third point defining the plane surface
//@ y3 # float # y coordinate of the third point defining the plane surface
//@ z3 # float # z coordinate of the third point defining the plane surface

planeInitialId = 0;

planeResolution = 1.0;

// Plane definition
x1 = 0.0;
y1 = 0.0;
z1 = 0.0;

x2 = 1.0;
y2 = 0.0;
z2 = 0.0;

x3 = 0.0;
y3 = 1.0;
z3 = 1.0;

////////////////////// END OF THE SETTINGS /////////////////////////

///////////////////////////////////////////////////////////
// DO NOT EDIT BELOW
///////////////////////////////////////////////////////////

Point(planeInitialId + 1) = {x1, y1, z1, planeResolution};
Point(planeInitialId + 2) = {x2, y2, z2, planeResolution};
Point(planeInitialId + 3) = {x3, y3, z3, planeResolution};
Point(planeInitialId + 4) = {x2+x3-x1, y2+y3-y1, z2+z3-z1, planeResolution};

Line (planeInitialId + 5) = {planeInitialId + 1, planeInitialId + 2};
Line (planeInitialId + 6) = {planeInitialId + 2, planeInitialId + 4};
Line (planeInitialId + 7) = {planeInitialId + 4, planeInitialId + 3};
Line (planeInitialId + 8) = {planeInitialId + 3, planeInitialId + 1};

Line Loop (planeInitialId + 9) = {planeInitialId + 5, planeInitialId + 6, planeInitialId + 7, planeInitialId + 8};
Plane Surface (planeInitialId + 10) = {planeInitialId + 9};
