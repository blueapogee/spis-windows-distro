"""
Generic International Unit to Dimless Unti converter for PicUp3D. 
This module is still under validation. 

**Project ref:**  Spis/SpisUI

**File name:**    ISToDimLessConverter.py

:status:          Under Valisation

**Creation:**     10/11/2005

**Modification:** 22/11/2005  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest, Sebastien Jourdain

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | J.Forest                             | Creation                   |
|                | j.fores@atenum.com                   |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | Sebastian Jourdain                   | Bug correction             |
|                | jourdain@artenum.com                 |                            |
+----------------+--------------------------------------+----------------------------+

2005, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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


import math, string


class ISToDimLessConverter:
    '''
    Generic International Unit to Dimless Unti converter for PicUp3D.
    This module is still under validation.
    '''

    def __init__(self):
        
        
        # initialisation of physical constants
        self.CONST_ARRAY = {}
        # charge of electron (Coulomb)
        self.Q_E = 1.6e-19
        self.CONST_ARRAY["Q_E"]= self.Q_E
        
        # permissivity of vacuum
        self.EPSILON_0 = 8.854e-12
        self.CONST_ARRAY["EPSILON_0"]= self.EPSILON_0
        
        #Boltzman's constance
        self.K_B = 1.381e-23
        self.CONST_ARRAY["K_B"]= self.K_B
        
        # mass of electron
        self.M_E = 9.109e-31
        self.CONST_ARRAY["M_E"]= self.M_E

        # Atomic Mass Unit
        self.AMU = 1.6604e-27
        self.CONST_ARRAY["AMU"]= self.AMU
        
        # pre-setting of charateristic scales
        self.Ttilde  = -1.0
        self.NbCells = -1.0
        self.lambdaD = -1.0
        self.omega   = -1.0
        
        self.resetParamTable()
        
    def printConstants(self):
        print "Electron charge", `self.Q_E`
        print "Permissivity of vacuum", `self.EPSILON_0`
        print "Boltzman's constance", `self.K_B`
        print "mass of electron", `self.M_E`
        print "Atomic Mass Unit", `self.AMU`
       
    def resetParamTable(self):
        self.paramTableIn = {}
        self.paramTableOut = {}
        self.loadConstants()
        

    def loadConstants(self):
        
        keyList = self.CONST_ARRAY.keys()
        for cstKey in keyList:
            self.paramTableIn[cstKey] = [self.CONST_ARRAY[cstKey], []]

        
    def addCoupleOfParam(self, keyListIn, keyListOut):
        '''"var name"
        keyIn and keyOut must be lists of string
        '''
        self.paramTableIn[keyIn] = [None, keyListOut]
        self.paramTableOut[keyOut] = [None, expression]
    
    def setPrgBarLoger(self, prgBar):
        self.prgBarLoger = prgBar
    
    def setValueIn(self, keyIn, valueIn):
        self.paramTableIn[keyIn][0] = valueIn
        
    def setExpression(self, keyOut, expression):
        self.paramTableOut[keyOut][1] = expression
        
    def addParamOut(self, keyOut):
        self.paramTableOut[keyOut] = [ None, ""]
    
    def addParamIn(self, keyIn):
        self.paramTableIn[keyIn] = [ None, []]
    
    def removeParamIn(self, keyIn):
        del self.paramTableIn[keyIn]
           
    def removeParamOut(self, keyOut):
        del self.paramTableOut[keyOut]
        
    def printParamTableIn(self):
        '''
        print the whole input table
        '''
        for key in self.paramTableIn.keys():
            print key, self.paramTableIn[key][0], self.paramTableIn[key][1]
    
        
    def printParamTableOut(self):
        '''
        print the whole ouput table
        '''
        for key in self.paramTableOut.keys():
            print key, self.paramTableOut[key][0], self.paramTableOut[key][1], self.paramTableOut[key][2], self.paramTableOut[key][3]
        
        
    def computeDimAllLessValues(self):
        '''
        computes all dimless values.
        '''
        self.prgBarLoger.setIndeterminate(0)
        PrgBarLogerValue = 0
        for key in self.paramTableOut.keys():
            PrgBarLogerValue = PrgBarLogerValue+1
            self.prgBarLoger.setValue(PrgBarLogerValue)
            self.prgBarLoger.repaint()
            self.computeDimlessValue(key)
        
        
    def computeDimlessValue(self, keyOut):
        '''
        compute the value of the parameter keyOut.
        '''
        
        keysIn=[]
        for parameterIn in self.paramTableIn.keys():
            if string.find(self.paramTableOut[keyOut][1], parameterIn) > -1:
                keysIn.append(parameterIn)
                
        for key in keysIn:
            if self.paramTableIn[key][0] == None:
               print "error on ", key
               return None
            else:
               cmdTmp = key+"= self.paramTableIn[\""+key+"\"][0]"
               exec(cmdTmp)
            
        keysOut = []
        for parameterOut in self.paramTableOut.keys():
            if string.find(self.paramTableOut[keyOut][1], parameterOut) > -1:
                if parameterOut != keyOut:
                 keysOut.append(parameterOut)
                
        for depKey in keysOut:
            if self.computeDimlessValue(depKey) == None:
                print "Error in", keyOut
                return None
            cmdTmp = depKey+"= self.paramTableOut[\""+depKey+"\"][0]"
            exec(cmdTmp)
            
        # to compute the value itself
        exec(self.paramTableOut[keyOut][1])
        cmdTmp = "self.paramTableOut[\""+keyOut+"\"][0] = "+keyOut
        exec(cmdTmp)
        return(self.paramTableOut[keyOut][0])
   
   
   
    def setBuiltIn(self):
        
        #temprature
        self.paramTableIn["Temperature"]=[ None, "eV"]
        self.paramTableOut["Ttilde"]=[ None, "Ttilde = Temperature*Q_E"]
                
        # Debye length
        self.paramTableIn["density"] = [ None, "m^-3"]
        self.paramTableOut["lambdaD"] = [ None, "lambdaD = math.sqrt((EPSILON_0*Ttilde)/(density*Q_E*Q_E))"]
        
        # Plasma pulsation
        self.paramTableOut["omega"]=[ None, "omega = math.sqrt((density*Q_E*Q_E)/(EPSILON_0*M_E))"]
        
        #gyropulsation
        self.paramTableIn["Bfield"] = [ None, "T"]
        self.paramTableOut["omegaC"] = [ None, "omegaC = (Q_E*Bfield)/M_E"]
        
        #dim-less B field
        self.paramTableOut["tildeB"] = [ None, "tildeB = omegaC/omega"]
        
        #geometrical scaling ratio
        self.paramTableOut["ScalingRatio"] = [ None, "ScalingRatio = 1.0/lambdaD"]
        
        #dimensionless size of the system
        self.paramTableIn["gridLengthX"] = [ None, "m"]
        self.paramTableIn["gridLengthY"] = [ None, "m"]
        self.paramTableIn["gridLengthZ"] = [ None, "m"]
        self.paramTableOut["tildeLx"] = [ None, "tildeLx = gridLengthX/lambdaD", ["gridLengthX"], ["lambdaD"]]
        self.paramTableOut["tildeLy"] = [ None, "tildeLy = gridLengthY/lambdaD", ["gridLengthY"], ["lambdaD"]]
        self.paramTableOut["tildeLz"] = [ None, "tildeLz = gridLengthZ/lambdaD", ["gridLengthZ"], ["lambdaD"]]
        
        #computationnal grid step
        self.paramTableIn["gridSizeX"] = [ None, ""]
        self.paramTableIn["gridSizeY"] = [ None, ""]
        self.paramTableIn["gridSizeZ"] = [ None, ""]
        self.paramTableOut["tildedX"] = [ None, "tildedX = gridLengthX/(gridSizeX*lambdaD)", ["gridLengthX", "gridSizeX"], ["lambdaD"]]
        self.paramTableOut["tildedY"] = [ None, "tildedY = gridLengthY/(gridSizeY*lambdaD)", ["gridLengthY", "gridSizeY"], ["lambdaD"]]
        self.paramTableOut["tildedZ"] = [ None, "tildedZ = gridLengthZ/(gridSizeZ*lambdaD)", ["gridLengthZ", "gridSizeZ"], ["lambdaD"]]
            
        # total number of cells
        self.paramTableOut["NbCells"]=[ None, "NbCells = gridSizeX*gridSizeY*gridSizeZ", ["gridSizeX", "gridSizeY", "gridSizeZ"], []]    
            
            
        #averaged number of particles by cell
        #TBD
         
        # current scaling factor
        self.paramTableOut["CoeffI"] = [ None, "CoeffI = Q_E*omega", [], ["omega"]]
        
        #thermal current density 
        self.paramTableOut["Jth"] = [ None, "Jth = density*Q_E*math.sqrt(Ttilde/(2.0*3.141592654*M_E))", ["density"], ["Ttilde"]]
            
         