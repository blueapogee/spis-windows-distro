
"""
**Module Name:**  DataFieldRawWriter

**Project ref:**  Keridwen / SPIS-UI

:status:          under development, developped under CNRS/CETP support contract.

**Creation:**     08/08/2008

**Modification:** 08/08/2008 

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          Julien Forest

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Julien Forest                  | Creation                   |
|                | j.forest@artenum.com           |                            |
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

import sys, string
import com.artenum.free.mesh.io.exporter.GmshExporter
from Modules.InOut.Writer import Writer

class DataFieldRawWriter(Writer):

	def __init__(self):
            self.dataField = None
            self.meshField = None
            self.fileNameOut = None
            self.elmIdShift =  1
            self.meshFileName = "Not defined"
            self.HEADER_ON = 1
            self.SWAP_COLUMN_ON = 0

        def setHeaderOff(self):
        	self.HEADER_ON = 0
        
        def setHeaderOn(self):
        	self.HEADER_ON = 1

        def swapColumnOff(self):
        	self.SWAP_COLUMN_ON = 0
        	
        def swapColumnOn(self):
        	self.SWAP_COLUMN_ON = 1

        def setData(self, data):
            self.dataField = data[0]
            self.meshField = data[1]
            self.meshFileName = data[2]
	    
        def setOutputFileName(self, fileNameOut):
            self.fileNameOut = fileNameOut

        def setElmIdShift(self, shift):
            self.elmIdShift = shift

        def write(self):

            if self.dataField.Local < 5: 
                sys.stdout.write("DataField exporting...      ")
                try:
                #if(1):
                   ###############################################
                   # managment of the data
                   ###############################################
                   # here the logic is first to recover the Id of the MeshField
                   # supporting the datafield and then use it to print the Id 
                   # of each mesh element suporting each data.

                   outPutFile = open( self.fileNameOut, "w")
	       
                   nbValues = len(self.dataField.ValueList)
                   meshFieldId = self.dataField.MeshFieldId
                   
                   #FIX ME
                   if self.dataField.Local == 4:
                       self.HEADER_ON=0
                       self.SWAP_COLUMN_ON=1

                   if self.HEADER_ON:
                       print >> outPutFile, "# format :"
                       print >> outPutFile, "# file_name_of_related_mesh (see .proj control file for more informations"
                       print >> outPutFile, "# Number_of_values "
                       print >> outPutFile, "# Localisation_on_cell ( 0 = on node, 1 = on edge, 2 = on face, 3 = on cell"
                       print >> outPutFile, "# value Id_of_the_hosting_element (Id starting at 1)"
                       print >> outPutFile, "# "+self.meshFileName
                       print >> outPutFile, `nbValues`
                       print >> outPutFile, `self.dataField.Local`
                   for index in xrange(nbValues):
                       data = self.dataField.ValueList[index]
                       if self.dataField.Local == 4:
                           elmId = self.meshField.MeshElementIdList[index]
                       else:
                           elmId = self.meshField.MeshElementIdList[index] + self.elmIdShift
                       if self.SWAP_COLUMN_ON:
                           outPutFile.write(`elmId`+" "+`data`+"\n")
                       else:
                           outPutFile.write(`data`+" "+`elmId`+"\n")
		   
                   outPutFile.close()
                   #self.compressFromFile(self.fileNameOut)         
                except:
                   print >> sys.stdwarn, "Error in data saving"
            else:
                print "DataFields of localisation higher than XXXX not supported yet."
                outPutFile = open( self.fileNameOut, "w")
                print >> outPutFile, "# DataFields of localisation higher than XXXXX not supported yet."
            outPutFile.close()
            