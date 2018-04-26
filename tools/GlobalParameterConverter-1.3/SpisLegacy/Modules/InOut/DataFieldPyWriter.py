
"""
Serialisation module of Data Field under Python
script like scripts.

**Project ref:**  Spis/SpisUI

**File name:**    DataFieldPyWriter.py 

:status:          Implemented

**Creation:**     01/01/2006

**Modification:** 22/06/2006  JF validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Julien Forest                  | Creation                   |
|                | j.forest@atenum.com            |                            |
+----------------+--------------------------------+----------------------------+
| 1.1.0          | Julien Forest                  | Bug correction             |
|                | j.forest@artenum.com           |                            |
+----------------+--------------------------------+----------------------------+

2004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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
from Modules.InOut.ObjectPyWriter import ObjectPyWriter
# does not work properly up to now
#from Modules.InOut.ObjectPyWriter2 import ObjectPyWriter2

from Bin.Tasks.shared import sharedData

class DataFieldPyWriter:
    '''
    Serialisation module of Data Field under Python script like scripts.
    This module will serialize the given data field under the form of
    a Python/Jython module (i.e script). The results can be saved on 
    disk and reloaded as a classic and simple Python/Jython module, with 
    the import command.
    '''
    
    def __init__(self, dataFieldIn):
        '''
        Default constructor. Takes in input the DataField to serialize.
        '''
        self.badCharList = " ()[].:,;!~<>#-=@\\\/"
        self.dataField = dataFieldIn
        self.outputDirName = ""
        self.outputDirPath = ""
        self.DEFAULT_BLOCK_SIZE = 8192
        self.blockSize = self.DEFAULT_BLOCK_SIZE
        
    def setBlockSize(self, size):
        self.blockSize = size
        
    def setOutputDirPath(self, dirPath):
        '''
        Set the output path directory.
        '''
        self.outputDirPath = dirPath
        
    def setOutputDirName(self, dirName):
        self.outputDirName = dirName
         
    
    def write(self):
        '''
        Write the serialised structure on disk. 
        ''' 
        #StartTime = time.time()
        if self.outputDirName == "":
            tmpDirName = ""
            for char in self.dataField.Name:
                if char in self.badCharList:
                    char ="_"
                tmpDirName = tmpDirName + char
            tmpDirName = "df_"+tmpDirName
        
        
        if not os.path.isdir(os.path.join(self.outputDirPath , tmpDirName)):
            os.makedirs(os.path.join(self.outputDirPath , tmpDirName))
        
        # just to enjoy the life
        fileOut = open( os.path.join(self.outputDirPath , tmpDirName, "__init__.py"), 'w')
        fileOut.close()
        
        tmpFileName = "data_field"+".py"
        self.outputFileName = os.path.join(self.outputDirPath , tmpDirName, tmpFileName)
        

        objw = ObjectPyWriter(self.dataField)
            
        objw.setBlockSize(self.blockSize)
        #print "In DataFieldPyWriter", str(self.blockSize)
        objw.setLongListOn()
        #print "tmpFileName",str(self.blockSize), str(objw.longList)
        objw.setRootDirName(tmpDirName)
        objw.setRootModuleName("data_field")
        #print "    Serialization..."
        objw.readPatern()
        serialisedList = objw.saveToList()
        subModuleDic = objw.getLinkedModuleDic()
        
        # writing of the main file
        #print "    File writing..."
        fileOut = open(self.outputFileName, 'w')
        fileOut.write("\n".join(serialisedList))
        tmpString = None
        fileOut.close()
        print "    Done"
        
        # writing of sub-modules (i.e for too long elements such as lists and dic
        for key in subModuleDic.keys():
            subModuleFileName = os.path.join(self.outputDirPath , tmpDirName, key+".py")
            fileOut = open(subModuleFileName, 'w')
            fileOut.write("\n".join(subModuleDic[key]))
            fileOut.close()
        
        
        # link to the related meshField::
        tmpName = "meshfield"+`self.dataField.MeshFieldId` + ".py"
        meshFieldFileName = os.path.join(self.outputDirPath, tmpDirName, tmpName)
        indexTmp = sharedData['AllMeshField'].IdList.index(self.dataField.MeshFieldId)
        
        #serialisation it-self
        objw = ObjectPyWriter(sharedData['AllMeshField'].List[indexTmp])
        objw.setBlockSize(self.blockSize)
        
        ######################
        objw.setLongListOn()
        ######################
        
        objw.setRootDirName(tmpDirName)
        objw.setRootModuleName("meshfield"+`self.dataField.MeshFieldId`)
        objw.addExcludedMenber('MeshElementList')
        objw.readPatern()
        serialisedList = objw.saveToList()
        subModuleDic = objw.getLinkedModuleDic()
      
        
        # writing of the main module
        fileOut = open(meshFieldFileName, 'w')
        fileOut.write("\n".join(serialisedList))
        fileOut.close()
        
        # writing of related sub-modules
        for key in subModuleDic.keys():
            subModuleFileName = os.path.join(self.outputDirPath , tmpDirName, key+".py")
            fileOut = open(subModuleFileName, 'w')
        
            fileOut.write("\n".join(subModuleDic[key]))
            tmpString = None
            fileOut.close()
            
        # to help the garbage collector
        objw = None
        fileOut = None
        
        #EndTime = time.time() 
        #Min = int((EndTime-StartTime)/60) 
        #Sec = (((EndTime-StartTime)/60)-Min)*60 
        #print ' Time =',Min,'Mn',Sec,'S'
       
