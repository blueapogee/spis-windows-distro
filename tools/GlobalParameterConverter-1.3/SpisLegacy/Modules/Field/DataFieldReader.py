"""
Module of loading of DataField and Meshfield saved in ASCII/SPIS format. 

**Module Name:**  DataFieldReader

**Project ref:**  Spis/SpisUI

**File type:**    Module

:status:          implemented

**Creation:**     15/11/2004

**Modification:** 15/12/2004  AL preliminary validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          Arsene Lupin

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                   | Creation                   |
|                | Arsene Lupin@artenum.com       |                            |
+----------------+--------------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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


import os
import string 

import Bin.Tasks.shared
#from shared import shared
 
class DataFieldReader:
        '''
        Loading class of DF and MF saved as fields.
        ''' 
        
        
        def __init__(self, dataFieldIn=None, meshFieldIn=None, fileNameIn=None):
            '''
            default constructor
            '''
            self.dataField = dataFieldIn
            self.meshField = meshFieldIn
            self.fileNameIn = fileNameIn
            
            #print "fileNameIn= ", fileNameIn
            
            self.eol = os.linesep
            
            
        def read(self):
            '''
            read the field.
            '''
                
            elmType = {}
            elmType['NODE'] = 0
            elmType['EDGE'] = 1
            elmType['FACE'] = 2
            elmType['CELL'] = 3
            elmType['CURVI'] = 4
            
            '''
            try:
            '''
            if(1):
                #print("tototot XXXX ffff")
                fileIn = open(self.fileNameIn, 'r')
                
                # to jump the header
                tmpLine = (fileIn.readline())[:-1]
                #print "line 1= ", tmpLine
                tmpLine = (fileIn.readline())[:-1]
                #print "line 2= ", tmpLine
                
                tmpLine = (fileIn.readline())[:-1]
                #print "tmpline 3=", tmpLine
                self.dataField.Id =  string.atoi(tmpLine)
                self.dataField.Name = (fileIn.readline())[1:-2]
                #print "DF name= ", self.dataField.Name
                self.dataField.Type = (fileIn.readline())[:-1]
                self.dataField.Description = (fileIn.readline())[1:-2]
                self.dataField.Unit = (fileIn.readline())[1:-2]
                self.dataField.Local = string.atoi( ((fileIn.readline())[:-1]) )
                tmpLine = (fileIn.readline())[:-1]
                if ( tmpLine == 'None'):
                    self.dataField.Value = None
                else:
                    self.dataField.Value = string.atof(tmpLine)
                self.dataField.LockedValue = string.atoi( ((fileIn.readline())[:-1]) )
                #   
                tmpLine = fileIn.readline()
                self.dimValue = string.atoi( (tmpLine)[:-1]) 
                if ( self.dimValue == 1):
                    tmpLine = fileIn.readline()
                    self.tmpList = string.split(tmpLine[:-1],',')
                    self.dataField.ValueList = range(len(self.tmpList))
                    indexTmp = 0
                    for val in self.tmpList:
                        self.dataField.ValueList[indexTmp] = string.atof(val)
                        indexTmp = indexTmp + 1
                else:
                   print "vector"
                   tmpLine = fileIn.readline()
                   outLine = (tmpLine.replace('[', '')).replace(']', ' ')
                   self.tmpList = string.split(outLine[:-1],',')
                   vect = []
                   for val in self.tmpList:
                       if ( len(vect) == self.dimValue):
                           self.dataField.ValueList.append(vect)
                           vect = []
                       else:
                           vect.append(string.atof(val))
    
                self.dataField.MeshFieldId = string.atoi( (fileIn.readline())[:-1])

                # to jump the header
                tmpLine = (fileIn.readline())[:-1]
                self.meshField.Id = string.atoi( (fileIn.readline())[:-1] )
                self.meshField.Name = (fileIn.readline())[1:-2]
                self.meshField.Type = (fileIn.readline())[1:-2]
                self.meshField.Description = (fileIn.readline())[1:-2]
                self.meshField.Local = string.atoi( (fileIn.readline())[:-1] )
                
                             
                tmpLine = fileIn.readline()
                self.tmpList = string.split(tmpLine[:-1],',')
                for val in self.tmpList:
                    self.meshField.MeshElementIdList.append(string.atoi(val))

                tmpLine = fileIn.readline()
                self.tmpTypeList = string.split(tmpLine[:-1],',')
                for Id in self.meshField.MeshElementIdList:
                    keyType = self.tmpTypeList[self.meshField.MeshElementIdList.index(Id)]
                    type = elmType[keyType[1:-1]]
                    indexElm = shared['MeshElmtList'][type].IdList.index(Id)
                    elm = shared['MeshElmtList'][type].List[indexElm]
                    self.meshField.MeshElementList.append(elm)             
                fileIn.close()
            '''    
            except:
                    print "error"
            '''
