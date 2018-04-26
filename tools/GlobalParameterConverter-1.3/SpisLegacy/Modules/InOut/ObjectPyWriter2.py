'''


DOES NOT WOK UP TO NOW

Created on Oct 22, 2010

@author: juju
'''
from Modules.InOut.ObjectPyWriter import ObjectPyWriter

class ObjectPyWriter2(ObjectPyWriter):
    
    def __init__(self, ObjectIn):
        ObjectPyWriter.__init__(self, ObjectIn)        
        self.formatVersion = 2.00
        self.lineLength = 256
        
    def saveToList(self):
        '''
        save in a list of simple strings the structure of 
        the current instance and return this list. 
        '''
        
        self.outputList = []
        if self.headerFlag > 0 :
            
            self.outputList.append("")
            self.outputList.append("# ObjectPyWriter serialized data")
            self.outputList.append("FORMART_VERSION= "+str(2.00))
            self.outputList.append("BLOCK_SIZE= "+str(self.blockSize))
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
                        
                        if type(out) == type([]):
                            if self.longList == 1:
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
                                        self.outputList.append(self.instanceName+"."+mbr+"["+`index`+":"+`index+self.blockSize`+"] = "+mbr+`block`+".dataBlock")
                                        
                                        # writting of the related block 
                                        tmpLinkedModuleList = []
                                        tmpLinkedModuleList.append("")
                                        #tmpLinkedModuleList.append("from "+self.rootDirName+"."+self.rootModuleName+" import "+self.instanceName)
                                        tmpLinkedModuleList.append("# block linked to "+self.instanceName)
                                        tmpLinkedModuleList.append("")
                                       
                                        '''                                           
                                        for tmpIndex in xrange(self.blockSize):
                                            if index+tmpIndex < len(out):
                                                tmpLinkedModuleList.append(self.instanceName+"."+mbr+"["+`index+tmpIndex`+"] ="+`out[index+tmpIndex]`)
                                        '''
                                        tmpLinkedModuleList.append("INDEX_IN= "+str(index))
                                        tmpLinkedModuleList.append("INDEX_OUT= "+str(index+self.blockSize))
                                        if (index+self.blockSize) < len(out):
                                            #tmpLinkedModuleList.append("dataBlock ="+`out[index:(index+self.blockSize)]`)
                                            tmpLinkedModuleList.append("dataBlock = range("+str(index)+", "+str(index+self.blockSize)+")")
                                            subIndex = 0
                                            for elm in out[index:(index+self.blockSize)]:
                                                tmpLinkedModuleList.append("dataBlock["+str(subIndex)+"]="+str(elm))
                                                subIndex = subIndex + 1
                                        else:
                                            #tmpLinkedModuleList.append("dataBlock ="+`out[index:len(out)]`)
                                            tmpLinkedModuleList.append("dataBlock = range("+str(index)+", "+str(len(out))+")")
                                            subIndex = 0
                                            for elm in out[index:len(out)]:
                                                tmpLinkedModuleList.append("dataBlock["+str(subIndex)+"]="+str(elm))
                                                subIndex = subIndex + 1
                                        
                                        self.linkedModuleDic[mbr+`block`] = tmpLinkedModuleList
                                        index = index + self.blockSize
                                    
                                else:
                                    self.outputList.append(self.instanceName+"."+mbr+" ="+`out`)
                            else:
                                self.outputList.append(self.instanceName+"."+mbr+" = range("+str(len(out))+")")
                                subIndex = 0
                                for elm in out:
                                    self.outputList.append(self.instanceName+"."+mbr+"["+str(subIndex)+"]="+str(elm))
                                    subIndex = subIndex + 1                                
                        else:   
                            self.outputList.append(self.instanceName+"."+mbr+" ="+`out`)
                        ####
                else:
                    #print "overwrited member"
                    val = self.overWritedValueList[self.overwritedMembersList.index(mbr)]
                    self.outputList.append(self.instanceName+"."+mbr+" ="+val)
        
        return self.outputList
    
        