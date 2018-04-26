"""
**File name:**    NascapMaterialsCatalogWriter.py

**Creation:**     2010/03/20

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      1.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Julien Forest                        | Creation                   |
|         | j.forest@artenum.com                 |                            |
+---------+--------------------------------------+----------------------------+

PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
import os
import org.spis.imp.property 
from org.spis.imp.property import NascapMaterial
from org.spis.imp.io.nascap import NascapXMLWriter

from java.io import File
#from gettext import Catalog

from org.spis.imp.ui.util import FileDialog


class NascapMaterialsCatalogWriter:
    """
    Writer for the NASCAP materials catalog and the correspondance list. 
    """
    
    def __init__(self, matList=[]):
        self.matList = matList
        self.catalog = []
        
    def addMaterialToCatalog(self, mat):
        dataList = mat.DataList.List
        nascapMat = NascapMaterial( mat.Id, mat.Name, dataList[0].Value, 
                                                      dataList[1].Value, 
                                                      dataList[2].Value, 
                                                      dataList[3].Value, 
                                                      dataList[4].Value, 
                                                      dataList[5].Value, 
                                                      dataList[6].Value, 
                                                      dataList[7].Value, 
                                                      dataList[8].Value, 
                                                      dataList[9].Value, 
                                                      dataList[10].Value, 
                                                      dataList[11].Value, 
                                                      dataList[12].Value, 
                                                      dataList[13].Value, 
                                                      dataList[14].Value, 
                                                      dataList[15].Value, 
                                                      dataList[16].Value, 
                                                      dataList[17].Value, 
                                                      dataList[18].Value) 
        # managment of the extended properties
        nbExtendedProperties = len(dataList) - 19
        for i in xrange(nbExtendedProperties) :
            dataIndex = i +19
            print "******>> ",dataList[dataIndex].Name, dataList[dataIndex].Type, dataList[dataIndex].Unit, str(dataList[dataIndex].Value), dataList[dataIndex].Description 
            nascapMat.addExtendedProperty(dataList[dataIndex].Name, dataList[dataIndex].Type, dataList[dataIndex].Unit, str(dataList[dataIndex].Value), dataList[dataIndex].Description)
            
        self.catalog.append(nascapMat)
        
    def write(self, fileName):
        """
        Write the NASCAP material catalog.
        """
        writer = NascapXMLWriter()
        try:
            writer.writeToFile( File(fileName), self.catalog)
        except: 
            print "Impossible to write the file"    
        
    def buildCatalog(self):
        for mat in self.matList:
            #dataList = mat.DataList.List
            self.addMaterialToCatalog(mat)
            
    def writePythonInitFile(self, dirName):

        try:
        #if(1):
            fileOut = open(dirName+os.sep+"__init__.py", 'w')
            fileOut.write("# to help the load of the correspondence tables as standard Python modules")
            fileOut.close()
        except:
            print "error"
                        
    def writeCorrespondanceList(self, fileName):
        """
        Write the correspondance list to make the link between the NASCAP materials catalog and the 
        SPIS numerical material list.
        """
        outputTmpString = ""
        tmpNameListString = "nascapMaterialNamesList= [ '"+self.catalog[0].getName()+"'"
        tmpIdListString = "nascapMaterialIdsList= ["+`self.catalog[0].getId()`
        for mat in self.catalog[1:]:
            tmpNameListString =  tmpNameListString + ", '" + mat.getName() +"'"
            tmpIdListString = tmpIdListString + ", " + `mat.getId()`
        tmpNameListString =  tmpNameListString + "] \n"
        tmpIdListString = tmpIdListString + "] \n"
        
        try:
            fileOut = open(fileName, 'w')
            fileOut.write(tmpNameListString)
            fileOut.write(tmpIdListString)
            fileOut.close()
        except:
            print "error"
            
