"""
Build a sphere in the geo Gmsh format according a predefined template and 
setting parameters. 

**Project ref:**  Spis/SpisUI

**File name:**    CAD_Importer.py

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest, Sebastien Jourdain

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | J.forest                             | Creation                   |
|                | j.forest@atenum.com                  |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | J.forest                             | Bug correction             |
|                | j.forest@atenum.com                  |                            |
+----------------+--------------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

import string

class buildGenericSphere:
    '''
    Build a sphere in the geo Gmsh format according a predefined template and
    setting parameters.
    '''

    def __init__(self):
        '''
        Default constructor.
        '''    
        self.subSystemName = "genericSphere"
        
        #generic sphere model
        self.specificModelParameters={}
        
        self.subSystemId = 1000
        
        
        self.centerX = 0.0;
        self.specificModelParameters["centerX"] = self.centerX
        self.centerY = 0.0;
        self.specificModelParameters["centerY"] = self.centerY
        self.centerZ = 0.0;
        self.specificModelParameters["centerZ"] = self.centerZ
        self.radius = 1.0;
        self.specificModelParameters["radius"] = self.radius
        self.localResol = 0.1;
        self.specificModelParameters["localResol"] = self.localResol
        
        
        self.templateNode  = ["Point(nodeId) = {radius+centerX, centerY, centerZ, localResol};",
                         "Point(nodeId) = {-radius+centerX, centerY, centerZ, localResol};",
                         "Point(nodeId) = {centerX, radius+centerY, centerZ, localResol};",
                         "Point(nodeId) = {centerX, -radius+centerY, centerZ, localResol};",
                         "Point(nodeId) = {centerX, centerY, radius+centerZ, localResol};",
                         "Point(nodeId) = {centerX, centerY, -radius+centerZ, localResol};",
                         "Point(nodeId) = {centerX, centerY, centerZ, localResol};"]

        self.templateCurve = ["Circle (curveId) = {pt4, pt7, pt1};",
                             "Circle (curveId) = {pt4, pt7, pt5};",
                             "Circle (curveId) = {pt1, pt7, pt5};",
                             "Circle (curveId) = {pt4, pt7, pt2};",
                             "Circle (curveId) = {pt2, pt7, pt5};",
                             "Circle (curveId) = {pt2, pt7, pt3};",
                             "Circle (curveId) = {pt3, pt7, pt1};",
                             "Circle (curveId) = {pt6, pt7, pt3};",
                             "Circle (curveId) = {pt6, pt7, pt2};",
                             "Circle (curveId) = {pt6, pt7, pt4};",
                             "Circle (curveId) = {pt6, pt7, pt1};",
                             "Circle (curveId) = {pt3, pt7, pt5};"]
                         
        self.templateSurface = ["Line Loop (loopId) = {curve4_, -curve9_, curve10_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve2_, -curve5_, -curve4_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve5_, -curve12_, -curve6_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve6_, -curve8_, curve9_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve3_, -curve2_, curve1_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve3_, -curve12_, curve7_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve7_, -curve11_, curve8_};",
                              "Ruled Surface (surfId) = {surfId};",
                              "Line Loop (loopId) = {curve1_, -curve11_, curve10_};",
                              "Ruled Surface (surfId) = {surfId};"]
             
        self.scriptOut = []
        
        
    def convertNodes(self):
        '''
        Export the construction nodes only.
        '''
        #nodes definition
        self.elmId = self.subSystemId
        self.firstNodeId = self.elmId
        for tmpLine in self.templateNode:
            self.elmId = self.elmId +1
            tmpLine = string.join( string.split(tmpLine, "nodeId"), `self.elmId`)
            tmpLine = string.join( string.split(tmpLine, "radius"), `self.specificModelParameters["radius"]`)
            tmpLine = string.join( string.split(tmpLine, "centerX"), `self.specificModelParameters["centerX"]`)
            tmpLine = string.join( string.split(tmpLine, "centerY"), `self.specificModelParameters["centerY"]`)
            tmpLine = string.join( string.split(tmpLine, "centerZ"), `self.specificModelParameters["centerZ"]`)
            tmpLine = string.join( string.split(tmpLine, "localResol"), `self.specificModelParameters["localResol"]`)
            self.scriptOut.append(tmpLine)
        
        
    def convertCurves(self):
        '''
        Export the construction lines and nodes only. The surfaces are 
        node generated.
        ''' 
        self.convertNodes()
        
        #curves definition
        self.elmId = self.elmId +1;
        self.firstCurveId = self.elmId
        self.scriptOut.append("")
        firstCurveId = self.elmId
        for tmpLine in self.templateCurve:
            self.elmId = self.elmId +1
            tmpLine = string.join( string.split(tmpLine, "curveId"), `self.elmId`)
            tmpLine = string.join( string.split(tmpLine, "pt1"), `self.firstNodeId+1`)
            tmpLine = string.join( string.split(tmpLine, "pt2"), `self.firstNodeId+2`)
            tmpLine = string.join( string.split(tmpLine, "pt3"), `self.firstNodeId+3`)
            tmpLine = string.join( string.split(tmpLine, "pt4"), `self.firstNodeId+4`)
            tmpLine = string.join( string.split(tmpLine, "pt5"), `self.firstNodeId+5`)
            tmpLine = string.join( string.split(tmpLine, "pt6"), `self.firstNodeId+6`)
            tmpLine = string.join( string.split(tmpLine, "pt7"), `self.firstNodeId+7`)
            self.scriptOut.append(tmpLine)
            
    def convertSurfaces(self):
        '''
        Export the surfaces and the sub-dimension construction elemens (curves, nodes).
        The output provide a complete system.
        '''
        self.convertCurves()
        
        #surfaces definition
        self.elmId = self.elmId +1;
                
        self.scriptOut.append("")
        firstCurveId = self.elmId
        for tmpLine in self.templateSurface:
            self.elmId = self.elmId +1
            tmpLine = string.join( string.split(tmpLine, "loopId"), `self.elmId`)
            tmpLine = string.join( string.split(tmpLine, "surfId"), `self.elmId-1`)
            tmpLine = string.join( string.split(tmpLine, "curve1_"), `self.firstCurveId+1`)
            tmpLine = string.join( string.split(tmpLine, "curve2_"), `self.firstCurveId+2`)
            tmpLine = string.join( string.split(tmpLine, "curve3_"), `self.firstCurveId+3`)
            tmpLine = string.join( string.split(tmpLine, "curve4_"), `self.firstCurveId+4`)
            tmpLine = string.join( string.split(tmpLine, "curve5_"), `self.firstCurveId+5`)
            tmpLine = string.join( string.split(tmpLine, "curve6_"), `self.firstCurveId+6`)
            tmpLine = string.join( string.split(tmpLine, "curve7_"), `self.firstCurveId+7`)
            tmpLine = string.join( string.split(tmpLine, "curve8_"), `self.firstCurveId+8`)
            tmpLine = string.join( string.split(tmpLine, "curve9_"), `self.firstCurveId+9`)
            tmpLine = string.join( string.split(tmpLine, "curve10_"), `self.firstCurveId+10`)
            tmpLine = string.join( string.split(tmpLine, "curve11_"), `self.firstCurveId+11`)
            tmpLine = string.join( string.split(tmpLine, "curve12_"), `self.firstCurveId+12`)
            
            self.scriptOut.append(tmpLine)
            
    def convertAll(self):
        '''
        Export all type of element. The output provides a complete system.
        '''
        self.convertSurfaces()
        
 
            
    def exportToGmsh(self, fileName):
        '''
        Export on a file the converted structure. 
        '''       
        print "Export to gmsh geo format"
        #fileName = self.subSystemName+".geo"
        fileOut = open(fileName, 'w')
        fileOut.write("// "+self.subSystemName+"\n")
        
        for line in self.scriptOut:
            fileOut.write(line+"\n")
        fileOut.close()
