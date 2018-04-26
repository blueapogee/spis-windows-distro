There are three files for gmsh options ("gmsh-options", "spis-gmsh-options.properties", "spis-gmsh-options.back")

The "spis-gmsh-options.properties" file includes options :
	-general
	-geometry
	-mesh
It is use to view and customize geometry or mesh in gmsh or in the mesh viewer.

The "gmsh-options" file is use to put Geometry.AutoCoherence to 0
It's use to correct a bug with gmsh when it went to merge wrong points.

The "spis-gmsh-options.back" file is use to restore the default gmsh configuration file.
These file is never edited.