
"""
Exports the given ElecNode as an equivalent Python script. The output scritp can 
be reload aftert just by a Python import. The class scan is not recursive yet. 

**Module Name:**  ElecNodePyWriter

**Project ref:**  Spis/SpisUI

**File type:**    Module

:status:          implemented

**Creation:**     10/01/2005

**Modification:** 20/03/2005  AL preliminary validation

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

import sys
from Modules.InOut import ObjectPyWriter
from Modules.InOut.ObjectPyWriter import ObjectPyWriter

#from Scripts import ObjectPyWriter
#from Scripts.ObjectPyWriter import ObjectPyWriter


class ElecNodePyWriter:
        '''
        save the given elecNode object as python script. This script can 
        be imported as simple Python module after.
        '''

        def __init__(self, elecNodeIn):
            '''
            default constructor. Take the ElectroNode to serialise as input.
            '''    
            self.elecNode = elecNodeIn                
            self.eol = "\n" #in order to have projects movable form UNIX to DOS
                
                
        def setOutputFileName(self, fileNameIn):
            '''
            Set the name of the output file. 
            '''
            self.fileName = fileNameIn;
                

        def readStructure(self):
                '''
                Read the structure (i.e perform the serialisation) of the 
                given object.
                '''                
                self.globalList= []
                self.dataNameList = []
                
                # PyWriting of each data
                self.dataIndex = 0
                for data in self.elecNode.DataList.List:
                        #print "    "+data.Name  
                        self.wr = ObjectPyWriter(data)
                        dataName = "data"+`self.dataIndex`
                        self.dataNameList.append(dataName)
                        self.wr.setInstanceName(dataName)
                        self.wr.readPatern()
                        self.wr.setHeaderOff()
                        list = self.wr.saveToList()
                        self.globalList.append(list)
                        self.dataIndex = self.dataIndex + 1
                
                # creation of the temporary list
                tmpValue = "["
                for dataName in self.dataNameList:
                      tmpValue = tmpValue+dataName+","
                tmpValue = tmpValue[:-1]+"]"
                
                # PyWriting of the data list
                self.wrDL = ObjectPyWriter(self.elecNode.DataList)
                self.wrDL.setInstanceName("dataList")
                self.wrDL.addOverwriteMember("List", tmpValue)
                self.wrDL.readPatern()
                list = self.wrDL.saveToList()
                self.globalList.append(list)
                
                # PyWriting of the elecNode itself
                self.wrPlasma = ObjectPyWriter(self.elecNode)
                self.wrPlasma.setInstanceName("elecNode")
                self.wrPlasma.addOverwriteMember("DataList", "dataList")
                self.wrPlasma.readPatern()
                list = self.wrPlasma.saveToList()
                self.globalList.append(list)

                
        def write(self):
                '''
                Write the serialised object on file.
                '''
                try:
                    fileOut = open(self.fileName, 'w')
                
                    fileOut.write("# DATA")

                    for data in self.globalList:
                         for elm in data:
                             fileOut.write(elm+self.eol)
                        
                    fileOut.close()
                except:
                    print >> sys.stderr, "error: impossible to export the module"
                    
                    
