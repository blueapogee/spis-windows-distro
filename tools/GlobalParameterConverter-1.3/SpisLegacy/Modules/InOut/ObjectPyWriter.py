"""
Exports a given class as an equivalent Python script. The output scritp can 
be reload aftert just by a Python import. The class scan is not recursive yet. 

**Module Name:**  ObjectPyWriter

**Project ref:**  Spis/SpisUI

**File type:**    Module

:status:          implemented

**Creation:**     10/01/2005

**Modification:** 20/03/2005  AL preliminary validation

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
import types

class ObjectPyWriter:
        '''
        Exports a given class as an equivalent Python script. The output 
        script can be reload after just by a Python import. The class scan 
        is not recursive yet.
        '''

        
        def __init__(self, ObjectIn):
            '''
            default constructor.
            '''
            #print "XXXXXXXXXXXX  Entry  XXXXXXXXXXXXX"
            self.instanceOf = ObjectIn
            #self.basicObjectFlag = isinstance(self.instanceOf,(int, float))
            #if self.basicObjectFlag == true:
            #        print "The input object is a basic type"
            self.instanceDescrip = (repr(self.instanceOf)).split(" ")
            #print self.instanceDescrip
            self.patternPath = (self.instanceDescrip[0])[1:]   #patternPath
            self.splittedPath = self.patternPath.split(".")
            self.pattern = self.splittedPath.pop()  #patternObject
            
            try:
                self.patternPath = self.splittedPath[0]
                for elm in self.splittedPath[1:]:
                    self.patternPath = self.patternPath+"."+elm
            except:
                self.patternPath=""
                self.pattern=""
                 
            self.listMembers = None
            self.instanceName = "savedData"
            self.overwritedMembersList = []
            self.overWritedValueList = []
            self.headerFlag = 1
            self.classOutputName = ""
            self.Tabulation = ""
            self.excludedMemberList = []
            self.linkedModuleDic = {}
            self.DEFAULT_BLOCK_SIZE = 4096
            self.blockSize = self.DEFAULT_BLOCK_SIZE
            self.rootModuleName ="rootModule"
            self.rootDirName = ""
            self.longList = 0
                
        def setBlockSize(self, size):
            self.blockSize = size;
                
        def setRootModuleName(self, rootModuleName):
            '''
            set the name of the main module (root module) in case of 
            split serialisation of large lists.
            '''            
            self.rootModuleName = rootModuleName
            
        def setLongListOn(self):
            '''
            set the serialisation mode of list in long mode; i.e
            lists are serialised into several and smaller sub modules.
            '''
            self.longList = 1
            
            
        def setLongListOff(self):
            '''
            set the serialisation mode of list in short mode.
            '''
            self.longList = 0
            
        def setRootDirName(self, rootDirName):
            '''
            set the name of the root directory in case of long 
            serialisation mode.
            '''
            self.rootDirName = rootDirName
                
        def readPatern(self):
            '''
            Read the pattern, i.e list and identify the members, of the given
            object. Not recursive yet.
            '''
             
            #FIX ME: problem if constructor of serialised object need another 
            #parameter than itself
             
            #if self.basicObjectFlag == False:
            # we import the object/module
            self.skelImport = "from "+self.patternPath+" import "+self.pattern
            exec(self.skelImport)
             
            # we create an instance of the pattern
            tmp = "skelInstance="+self.pattern+"()"
            exec(tmp)
             
            # we recover the members of the instance
            self.listMembers = dir(skelInstance)
             
            #print self.pattern
            #print "--------------------"
            #print self.listMembers
            tmpList = []
            for elm in self.listMembers:
                cmd = "self.currentMemberType = type(skelInstance"+"."+elm+")"
                exec(cmd)
                #print "MEMBER --> ", elm, self.currentMemberType
                if self.currentMemberType != types.MethodType:
                    tmpList.append(elm)
                    #print "     adding", elm
            self.listMembers = tmpList
            #print "--------------------"
            #print self.listMembers
            #print "--------------------"
         
            '''
            for mbr in self.listMembers:
                tmp="out = self.instanceOf."+mbr
                #print "tmp= ", tmp
                exec(tmp)
                #print "savedData."+mbr+" =",out
                #self.__init__(out)
                #self.readpattern()
            #else:
            #print "basic type, no pattern to read"
            ''' 
             
        def addExcludedMenber(self, memberName):
            '''
            excludes a member of the serialisation process.
            '''
            self.excludedMemberList.append(memberName)
                 
                 
        def addOverwriteMember(self, memberName, fieldValue):
            '''
            Allows to overwrite a given member of the current object.
            '''
            self.overwritedMembersList.append(memberName)
            self.overWritedValueList.append(fieldValue)
          
          
        def setHeaderOff(self):
            '''
            switch off the header.
            '''
            self.headerFlag = 0
          
          
        def setHeaderOn(self):
            '''
            switch on the header.
            '''
            self.headerFlag = 1
          
          
        def setAsClass(self):
            '''
            save as class (not operational yet)
            '''
            self.classOutputName = "class "+self.pattern+"Class: \n     def __init__(self):"
            self.Tabulation = "          "
          
          
        def setAsScript(self):
            '''
            save as simple script (by default).
            '''
            self.classOutputName = ""
            self.Tabulation = ""
        
        
        def write(self):
            '''
            deprecated.
            '''
            print self.outputList
        
        
        def setInstanceName(self, instanceName):
            '''
            set the instance name.
            '''
            self.instanceName = instanceName
                
                
        def getLinkedModuleDic(self):
            '''
            returns the dictionary of associated sub-modules in case
            of long serialisation mode.
            '''
            return(self.linkedModuleDic)
                
        
        def saveToList(self):
            '''
            save in a list of simple strings the structure of 
            the current instance and return this list. 
            '''
            
            self.outputList = []
            if self.headerFlag > 0 :
                self.outputList.append("")
                self.outputList.append("# Be careful :SAVED DATA STRUCTURE, program generated script!")
                self.outputList.append("# DO NOT EDIT, if you are not sure of what you are doing.")
                self.outputList.append("")
            
            
            self.outputList.append("# object instantiation")
            if len(self.patternPath) > 0:
                self.outputList.append(self.skelImport) 
                tmp = self.instanceName+"= "+self.pattern+"()"
                self.outputList.append(tmp)
            self.outputList.append("")
            
            #print "In ObjectPyWriter", str(self.blockSize)
            
            self.outputList.append("# instance settings")
            for mbr in self.listMembers:
                    if mbr not in self.overwritedMembersList:
                        if mbr not in self.excludedMemberList:  
                            #####
                            tmp="out = self.instanceOf."+mbr
                            exec(tmp)
                            
                            if self.longList == 1 and type(out) == type([]):
                                    self.outputList.append(self.instanceName+"."+mbr+" = range("+`len(out)`+")")
                                    nbSubList = len(out) / self.blockSize
                                    index = 0
                                    if nbSubList > 0:
                                        index = 0
                                        for block in xrange(nbSubList+1):
                                            self.outputList.append("")
                                            self.outputList.append("# external sub-module")
                                            self.outputList.append("from "+self.rootDirName+" import "+mbr+`block`)
                                            self.outputList.append("reload("+mbr+`block`+")")
                                            
                                            tmpLinkedModuleList = []
                                            tmpLinkedModuleList.append("")
                                            tmpLinkedModuleList.append("from "+self.rootDirName+"."+self.rootModuleName+" import "+self.instanceName)
                                            tmpLinkedModuleList.append("")
                                           
                                            '''                                           
                                            for tmpIndex in xrange(self.blockSize):
                                                if index+tmpIndex < len(out):
                                                    tmpLinkedModuleList.append(self.instanceName+"."+mbr+"["+`index+tmpIndex`+"] ="+`out[index+tmpIndex]`)
                                            '''
                                            
                                            if (index+self.blockSize) < len(out):
                                                tmpLinkedModuleList.append(self.instanceName+"."+mbr+"["+`index`+":"+`index+self.blockSize`+"] ="+`out[index:(index+self.blockSize)]`)
                                            else:
                                                tmpLinkedModuleList.append(self.instanceName+"."+mbr+"["+`index`+":"+`len(out)`+"] ="+`out[index:len(out)]`)
                                            
                                                    
                                            self.linkedModuleDic[mbr+`block`] = tmpLinkedModuleList
                                            index = index + self.blockSize
                                        
                                    else:
                                        self.outputList.append(self.instanceName+"."+mbr+" ="+`out`)
                            else:   
                                self.outputList.append(self.instanceName+"."+mbr+" ="+`out`)
                            ####
                    else:
                        #print "overwrited member"
                        val = self.overWritedValueList[self.overwritedMembersList.index(mbr)]
                        self.outputList.append(self.instanceName+"."+mbr+" ="+val)
            
            return self.outputList

                    
                        
