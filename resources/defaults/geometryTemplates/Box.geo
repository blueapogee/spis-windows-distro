
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
//# Box
//@ boxInitialId # int # Id of the first element in the geo file
//@ boxRes # float # Box resolution
//@ lengthX # float # Box length along X axis
//@ lengthY # float # Box length along Y axis
//@ lengthZ # float # Box length along Z axis
//@ rotAxisX # float # Rotation vector, X coordinate
//@ rotAxisY # float # Rotation vector, Y coordinate
//@ rotAxisZ # float # Rotation vector, Z coordinate
//@ rotAngle # float # Rotation angle (radian)
//@ translateX # float # System translation, X coordinate
//@ translateY # float # System translation, Y coordinate
//@ translateZ # float # System translation, Z coordinate

boxInitialId = 2000;

boxRes = 0.30;

// Box size
lengthX = 1.0;
lengthY = 1.0;
lengthZ = 1.0;

//global system rotation 
rotAxisX = 1.0;
rotAxisY = 0.0;
rotAxisZ = 0.0;
rotAngle = 0.0;    // example Pi/4.0;

//global system translation vector
translateX = 0.0;
translateY = 0.0;
translateZ = 0.0;

////////////////////// END OF THE SETTINGS /////////////////////////

///////////////////////////////////////////////////////////
// DO NOT EDIT BELOW
///////////////////////////////////////////////////////////

Point(boxInitialId + 1) = {0, lengthY, lengthZ, boxRes};
Point(boxInitialId + 2) = {lengthX, lengthY, lengthZ, boxRes};
Point(boxInitialId + 3) = {lengthX, 0, lengthZ, boxRes};
Point(boxInitialId + 4) = {lengthX, 0, 0, boxRes};
Point(boxInitialId + 5) = {lengthX, lengthY, 0, boxRes};
Point(boxInitialId + 6) = {0, lengthY, 0, boxRes};
Point(boxInitialId + 7) = {0, 0, 0, boxRes};
Point(boxInitialId + 8) = {0, 0, lengthZ, boxRes};

Line (boxInitialId + 9) = {boxInitialId + 1, boxInitialId + 2};
Line (boxInitialId + 10) = {boxInitialId + 2, boxInitialId + 5};
Line (boxInitialId + 11) = {boxInitialId + 5, boxInitialId + 6};
Line (boxInitialId + 12) = {boxInitialId + 6, boxInitialId + 1};
Line (boxInitialId + 13) = {boxInitialId + 1, boxInitialId + 8};
Line (boxInitialId + 14) = {boxInitialId + 8, boxInitialId + 3};
Line (boxInitialId + 15) = {boxInitialId + 3, boxInitialId + 2};
Line (boxInitialId + 16) = {boxInitialId + 8, boxInitialId + 7};
Line (boxInitialId + 17) = {boxInitialId + 7, boxInitialId + 4};
Line (boxInitialId + 18) = {boxInitialId + 4, boxInitialId + 3};
Line (boxInitialId + 19) = {boxInitialId + 4, boxInitialId + 5};
Line (boxInitialId + 20) = {boxInitialId + 7, boxInitialId + 6};

Line Loop (boxInitialId + 21) = {boxInitialId + 10, -(boxInitialId + 19), boxInitialId + 18, boxInitialId + 15};
Plane Surface (boxInitialId + 21) = {boxInitialId + 21};
Line Loop (boxInitialId + 22) = {boxInitialId + 17, boxInitialId + 18, -(boxInitialId + 14), boxInitialId + 16};
Plane Surface (boxInitialId + 22) = {boxInitialId + 22};
Line Loop (boxInitialId + 23) = {boxInitialId + 11, -(boxInitialId + 20), boxInitialId + 17, boxInitialId + 19};
Plane Surface (boxInitialId + 23) = {boxInitialId + 23};
Line Loop (boxInitialId + 24) = {boxInitialId + 16, boxInitialId + 20, boxInitialId + 12, boxInitialId + 13};
Plane Surface (boxInitialId + 24) = {boxInitialId + 24};
Line Loop (boxInitialId + 25) = {boxInitialId + 9, -(boxInitialId + 15), -(boxInitialId + 14), -(boxInitialId + 13)};
Plane Surface (boxInitialId + 25) = {boxInitialId + 25};
Line Loop (boxInitialId + 26) = {boxInitialId + 9, boxInitialId + 10, boxInitialId + 11, boxInitialId + 12};
Plane Surface (boxInitialId + 26) = {boxInitialId + 26};

//translation and rotation operations
Rotate {{rotAxisX, rotAxisY, rotAxisZ}, {0, 0, 0}, rotAngle} {
  Surface{boxInitialId + 21, boxInitialId + 22, boxInitialId + 23, boxInitialId + 24, boxInitialId + 25, boxInitialId + 26};
}

Translate {translateX, translateY, translateZ} {
  Surface{boxInitialId + 21, boxInitialId + 22, boxInitialId + 23, boxInitialId + 24, boxInitialId + 25, boxInitialId + 26};
}
