

"""
**Module Name:**  ProjectManager

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

import os, sys, md5
from socket import gethostname


class ProjectManager:
    '''
    General purpose project manager.
    '''
    def __init__(self):

        self.clearListes()
        self.projectName = None
        self.projectPath = None
        self.fullProjectName = None
        self.eol = os.linesep
        self.verbose = 0
        self.readingBufferSize = 4096
        self.hostname = gethostname()

    def clearListes(self):
        '''
	clear all listes of stored data. 
	'''
        self.sharedFiles =  None
        self.dataDic = {}
        self.dataList = []
        self.fileDic = {}
        self.correspDic = {}
        self.dataDepDic = {}
        self.fileDepDic = {}


    def setSharedFiles(self, dicIn):
        '''
        deprected. 
        '''
        self.sharedFiles = dicIn
            
    def setProjectName(self, projectName):
        '''
        set the name of the project (without its path).
        '''
        self.projectName = projectName
    
    def setProjectPath(self, projectPath):
        '''
        set the path of the project.
        '''
        self.projectPath = projectPath

    def setProjectFullName(self, projectPath, projectName):
        '''
        set the full name (path+name) of the project.
        '''
        self.setProjectPath(projectPath)
        self.setProjectName(projectName)
        self.fullProjectName = self.projectPath+os.sep+self.projectName

    def setProjectFullName(self, projectPathAndName):
        '''
        set the full name (path+name) of the project.
        '''
        self.fullProjectName = projectPathAndName

    def setHostName(self, hostname):
        self.hostname = hostname

    def addElement(self, dataKeyName, writer, data, fileName, path, upDate, rights, description):
        '''
        add a data in the list of dat to save. Data can be mesh, DataField or all 
        other object. An adapted writer (derived from the Bin.InOut.Writer 
        interface) should be implemented for the data. See Bin.InOut.MeshWriter or
        Bin.InOut.DataFieldRawWriter for examples. fileName should be the name of the with
        with its extension (e.g defaultMesh.msh) but without its path. The path should be
        defined relatively at the project root.
        '''
        self.dataDic[dataKeyName] = [writer, data, fileName, path, self.hostname, upDate, rights, description]

    def setDependencyGraphForElement(self, dataKeyName, depList):
        '''
        set the dependency graph for the data of name dataKeyName. The second parameter
        should be a list with the names of the data on wich dataKeyName depend on. 
        '''
        print "setDependencyGraphForElement"
        self.dataDepDic[dataKeyName] = depList

    def addDepencyForElement(self, dataKeyName, dep):
        self.dataDepDic[dataKeyName].append(dep)

    def delElement(self, dataName):
        print "To be implemented"


    def getWriter(self, dataKeyName):
        '''
        return a pointer toward the writer of the data of name dataKeyName. 
        Maybe used for additional settings on the data writer. 
        '''
        return self.dataDic[dataKeyName] 


    def writeProject(self, writeAll = 1):
        '''
        write the full project (data and control file).
        '''
        # creation of the projet directory
        #self.fullProjectName = self.projectPath+os.sep+self.projectName
        print self.fullProjectName
        if not os.path.isdir(self.fullProjectName):
            os.makedirs(self.fullProjectName)

        self.writeData(writeAll)
        if self.verbose > 2:
            print "keys in dic", self.fileDic.keys()
        self.writeControlFileAsASCIIRaw()


    def writeData(self, writeAll = 1):
        '''
        write all data previously stored in the dataList (see
        addElement method for further information).
        '''
        #for data in self.dataList:
        for dataKeyName in self.dataDic.keys():
            data = self.dataDic[dataKeyName]
            if not os.path.isdir(self.fullProjectName+os.sep+data[3]):
                os.makedirs(self.fullProjectName+os.sep+data[3])

            if dataKeyName not in self.correspDic.keys() or writeAll == 1:
                fullDataPath = self.fullProjectName+os.sep+data[3]+os.sep+data[2]
                print fullDataPath
                writer = data[0]
                writer.setData(data[1])
                writer.setOutputFileName(fullDataPath)
                writer.write()

                fileHashKey = self.readFileKey(fullDataPath)
                print fileHashKey
                self.fileDic[fileHashKey] = [data[2], data[3], data[4], data[5], data[6], data[7]]
                #self.dataDic[dataKeyName] = fileHashKey
                self.correspDic[dataKeyName] = fileHashKey

    def computeFileDependency(self):
        '''
	    compute the dependency graph for the written files. The data dependency graph 
	    and the data should be called before. 
	    '''

        for dataKeyName in self.dataDepDic.keys():
            tmpDepTree = []
            for depName in self.dataDepDic[dataKeyName]:
                #tmpDepTree.append(self.dataDic[depName])
                tmpDepTree.append(self.correspDic[depName])
            #self.fileDepDic[self.dataDic[dataKeyName]] = tmpDepTree
            self.fileDepDic[self.correspDic[dataKeyName]] = tmpDepTree

    def readFileKey(self, fulFileName):
        '''
	    compute the hash, with the MD5 algorithm, of the 
	    file of full name (path+name) fullFileName. The
        hash is returned as an hex string. 
        '''
        fileIn = open(fulFileName)

        m = md5.new()
        tmpBuffer = fileIn.read(self.readingBufferSize)
        while tmpBuffer != "":
            m.update(tmpBuffer)
            tmpBuffer = fileIn.read(self.readingBufferSize)
            sys.stdout.write(".")
        fileIn.close()
        print ""
        return(m.hexdigest())


    def writeControlFile(self, extension):
        '''
        write the control file into the project. This the generic
        method. Please do not use. 
        '''
        crtFileName = self.projectPath+os.sep+"project."+extension 

    def writeControlFileAsASCIIRaw(self):
        '''
        write the control file under ASCII raw and colum format, as follow:
        Files identification list
        MD5 key, file name, relative path, hostname, last update, access rights, comment
        Files dependency list
        MD5 key of the pointing file, MD5_dep1, MD5_dep2, MD5_dep3 ...
        '''
        rawSep = ", "

        extension = "proj"
        crtFileName = self.fullProjectName+os.sep+"project."+extension
        #try:
        if(1):
           fileOut = open(crtFileName, 'w')
           # file list
           fileOut.write("# Files identification list"+self.eol)
           fileOut.write("# MD5 key, file name, relative path, hostname, last update, access rights, comment"+self.eol)
           #for key in self.fileDic.keys():
           for item in self.fileDic.items(): 
           #fileOut.write(`key`+rawSep)
              fileOut.write(`item[0]`+rawSep)
              #for elm in self.fileDic[key]:
              for elm in item[1][:-1]:
                 fileOut.write(`elm`+rawSep)
              fileOut.write(`item[1][-1:][0]`+self.eol)
		   
           # dependencies list
           self.computeFileDependency()
           fileOut.write("# Files dependency list"+self.eol)
           fileOut.write("# MD5 key of the pointing file, MD5_dep1, MD5_dep2, MD5_dep3 ..."+self.eol) 
           for item in self.fileDepDic.items():
               fileOut.write(`item[0]`+rawSep)
               for elm in item[1][:-1]:
                   fileOut.write(`elm`+rawSep)
               fileOut.write(`item[1][-1:][0]`+self.eol)
													       
           fileOut.close()
        #except:
        #    print >> sys.stderr, "error: impossible to export the module"

    def writeControlFileAsJyScript(self):
        print "writeControlFileAsJyScript"


