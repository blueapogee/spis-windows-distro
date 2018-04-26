'''
Created on Oct 23, 2010

@author: juju
'''
import os, string

    
def load(filePath, paternSubModule):
    
    fileIn = open(filePath)
    dataIn = fileIn.read()
    splitdata = dataIn.split("\n")
    
    for line in splitdata:
        print line
        if ("import" in line and paternSubModule in line):
            print "---->", line
            subModule = line.split("import ")[1]+".py"
            tmpPath = filePath.split(os.sep)[:-1]
            tmpPath.append(subModule)
            print tmpPath
            subModulePath = string.join(tmpPath,os.sep)
            print "sub-module---->", subModulePath
            load(subModulePath, "")
        elif "reload" in line:
            line = ""
        else: 
            exec(line)
        
        