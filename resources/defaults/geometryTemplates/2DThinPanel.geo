
//////////////////////////////////////////////////////////////
//         Simple rectangular 2D THIN PLATE model           //
//                                                          //
// This model automatically build a surrounding "pizza box" //
//with an extra space of four times the averaged local mesh //
//size.                                                     //
//                                                          //
// This sytem can be rotated, translated and the plate size //
//can be set in the xy-directions.                          //
// Physical groups are pre-built and the initial ID drift   //
//can be set.                                               //
//                                                          //
// Please take to the volume definition in case of insertion//
//into an external system.                                  //
//                                                          //
// author: J.Forest, Artenum SARL                           //
//////////////////////////////////////////////////////////////

// Description of the template variables (used by Keridwen Gmsh template parser)
//# 2D Thin Plate
//@ initialID # int # Id of the first element in the geo file
//@ extRes # float # External computational domain resolution
//@ innerRes # float # Thin surface resolution
//@ lengthX # float # Thin surface length along X axis
//@ lengthY # float # Thin surface length along Y axis
//@ rotAxisX # float # Rotation vector, X coordinate
//@ rotAxisY # float # Rotation vector, Y coordinate
//@ rotAxisZ # float # Rotation vector, Z coordinate
//@ rotAngle # float # Rotation angle (radian)
//@ transX # float # System translation vector, X coordinate
//@ transY # float # System translation vector, Y coordinate
//@ transZ # float # System translation vector, Z coordinate

//Initial ID drift
initialID = 100;

//local mesh characteristic sizes
//external computationnal domain bound
extRes = 0.5;

//inner computationnal domain bound (i.e. S/C thin surface)
innerRes = 0.2;

// thin plate size (in the xy-plan by default)
lengthX = 2.0;
lengthY = 1.0;

// pizza box size
pBoxLengthX = 4.0*((innerRes+extRes*0.5)*0.5)+lengthX; // add an extra space of 4 times the averaged local mesh size
pBoxLengthY = 4.0*((innerRes+extRes*0.5)*0.5)+lengthY; // add an extra space of 4 times the averaged local mesh size
pBoxThincknessZ = 4.0*((innerRes+extRes*0.5)*0.5); // in absolute value


//global system rotation 
rotAxisX = 1.0;
rotAxisY = 0.0;
rotAxisZ = 0.0;
rotAngle = 0.0;    // example Pi/4.0;

//global system translation vector (for both thin surface + pizza box)
transX = 0.0;
transY = 0.0;
transZ = 0.0;

////////////////////// END OF THE SETTINGS /////////////////////////

// definition of the thin surface it-self (Please DO NOT MODIFY)
Point(1+initialID) = {-lengthX, lengthY, 0, innerRes};
Point(2+initialID) = {lengthX, lengthY, 0, innerRes};
Point(3+initialID) = {lengthX, -lengthY, 0, innerRes};
Point(4+initialID) = {-lengthX, -lengthY, 0, innerRes};

//Definition of the pizzaBox (Please DO NOT MODIFY)
Point(6+initialID) = {pBoxLengthX, pBoxLengthY, pBoxThincknessZ, extRes};
Point(7+initialID) = {pBoxLengthX, pBoxLengthY, -pBoxThincknessZ, extRes};
Point(8+initialID) = {pBoxLengthX, -pBoxLengthY, pBoxThincknessZ, extRes};
Point(9+initialID) = {pBoxLengthX, -pBoxLengthY, -pBoxThincknessZ, extRes};
Point(10+initialID) = {-pBoxLengthX, -pBoxLengthY, -pBoxThincknessZ, extRes};
Point(11+initialID) = {-pBoxLengthX, -pBoxLengthY, pBoxThincknessZ, extRes};
Point(12+initialID) = {-pBoxLengthX, pBoxLengthY, pBoxThincknessZ, extRes};
Point(13+initialID) = {-pBoxLengthX, pBoxLengthY, -pBoxThincknessZ, extRes};

Point(14+initialID) = {pBoxLengthX, pBoxLengthY, 0, extRes*0.5};
Point(15+initialID) = {pBoxLengthX, -pBoxLengthY, 0, extRes*0.5};
Point(16+initialID) = {-pBoxLengthX, -pBoxLengthY, 0, extRes*0.5};
Point(17+initialID) = {-pBoxLengthX, pBoxLengthY, 0, extRes*0.5};

// connectivity
Line(1+initialID) = {1+initialID, 2+initialID};
Line(2+initialID) = {2+initialID, 3+initialID};
Line(3+initialID) = {3+initialID, 4+initialID};
Line(4+initialID) = {4+initialID, 1+initialID};
Line(5+initialID) = {10+initialID, 13+initialID};
Line(6+initialID) = {13+initialID, 7+initialID};
Line(7+initialID) = {7+initialID, 9+initialID};
Line(8+initialID) = {9+initialID, 10+initialID};
Line(9+initialID) = {13+initialID, 17+initialID};
Line(10+initialID) = {17+initialID, 12+initialID};
Line(11+initialID) = {17+initialID, 1+initialID};
Line(12+initialID) = {10+initialID, 16+initialID};
Line(13+initialID) = {16+initialID, 11+initialID};
Line(14+initialID) = {16+initialID, 4+initialID};
Line(15+initialID) = {7+initialID, 14+initialID};
Line(16+initialID) = {14+initialID, 6+initialID};
Line(17+initialID) = {14+initialID, 2+initialID};
Line(18+initialID) = {9+initialID, 15+initialID};
Line(19+initialID) = {15+initialID, 8+initialID};
Line(20+initialID) = {8+initialID, 6+initialID};
Line(21+initialID) = {6+initialID, 12+initialID};
Line(22+initialID) = {12+initialID, 11+initialID};
Line(23+initialID) = {11+initialID, 8+initialID};
Line(24+initialID) = {3+initialID, 15+initialID};
Line(25+initialID) = {15+initialID, 14+initialID};
Line(26+initialID) = {14+initialID, 17+initialID};
Line(27+initialID) = {17+initialID, 16+initialID};
Line(28+initialID) = {16+initialID, 15+initialID};



// first half-space volume
Line Loop(29+initialID) = {1+initialID, 2+initialID, 3+initialID, 4+initialID};
Plane Surface(30+initialID) = {29+initialID};
Line Loop(31+initialID) = {2+initialID, 24+initialID, 25+initialID, 17+initialID};
Plane Surface(32+initialID) = {31+initialID};
Line Loop(33+initialID) = {24+initialID,-(28+initialID), 14+initialID,-(3+initialID)};
Plane Surface(34+initialID) = {33+initialID};
Line Loop(35+initialID) = {4+initialID,-(11+initialID), 27+initialID, 14+initialID};
Plane Surface(36+initialID) = {35+initialID};
Line Loop(37+initialID) = {11+initialID, 1+initialID, -(17+initialID), 26+initialID};
Plane Surface(38+initialID) = {37+initialID};
Line Loop(39+initialID) = {26+initialID, -(9+initialID), 6+initialID, 15+initialID};
Plane Surface(40+initialID) = {39+initialID};
Line Loop(41+initialID) = {15+initialID,-(25+initialID),-(18+initialID),-(7+initialID)};
Plane Surface(42+initialID) = {41+initialID};
Line Loop(43+initialID) = {9+initialID, 27+initialID, -(12+initialID), 5+initialID};
Plane Surface(44+initialID) = {43+initialID};
Line Loop(45+initialID) = {6+initialID, 7+initialID, 8+initialID, 5+initialID};
Plane Surface(46+initialID) = {45+initialID};
Line Loop(47+initialID) = {8+initialID, 12+initialID, 28+initialID, -(18+initialID)};
Plane Surface(48+initialID) = {47+initialID};

Surface Loop(49+initialID) = {40+initialID, -(38+initialID), -(36+initialID), 30+initialID, -(32+initialID), 34+initialID, 48+initialID, -(46+initialID), -(42+initialID), 44+initialID};
Volume(50+initialID) = {49+initialID};


// second half space volume
Line Loop(51+initialID) = {20+initialID, -(16+initialID), -(25+initialID), 19+initialID};
Plane Surface(52+initialID) = {51+initialID};
Line Loop(53+initialID) = {19+initialID, -(23+initialID), -(13+initialID), 28+initialID};
Plane Surface(54+initialID) = {53+initialID};
Line Loop(55+initialID) = {23+initialID, 20+initialID, 21+initialID, 22+initialID};
Plane Surface(56+initialID) = {55+initialID};
Line Loop(57+initialID) = { 16+initialID, 21+initialID, -(10+initialID), -(26+initialID)};
Plane Surface(58+initialID) = {57+initialID};
Line Loop(59+initialID) = {10+initialID, 22+initialID, -(13+initialID),-(27+initialID)};
Plane Surface(60+initialID) = {59+initialID};
Surface Loop(61+initialID) = {60+initialID, 58+initialID, 52+initialID, -(56+initialID), -(54+initialID), -(34+initialID), 32+initialID, -(30+initialID), 38+initialID, 36+initialID};
Volume(62+initialID) = {61+initialID};

// definition of the physical groups
Physical Surface(63+initialID) = {56+initialID, 54+initialID, 52+initialID, 48+initialID, 42+initialID, 46+initialID, 40+initialID, 44+initialID, 60+initialID, 58+initialID};
Physical Surface(64+initialID) = {30+initialID};
Physical Line(65+initialID) = {1+initialID, 4+initialID, 3+initialID, 2+initialID};

// computational volume by union of both half-spaces
Physical Volume(66+initialID) = {50+initialID, 62+initialID};

//translation and rotation operations
Rotate {{rotAxisX, rotAxisY, rotAxisZ}, {0, 0, 0}, rotAngle} {
  Volume{62+initialID, 50+initialID};
}

Translate {transX, transY, transZ} {
  Volume{62+initialID, 50+initialID};
}


