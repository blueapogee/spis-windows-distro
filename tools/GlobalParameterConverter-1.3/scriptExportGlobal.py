from org.keridwen.modelling.global.parameters import GlobalParameter
from org.keridwen.modelling.global.parameters.io import GlobalParamXMLWriter

import sys
import Modules
import Bin

from Bin.Tasks.shared import *
from Bin.ProjectLoader2 import ProjectLoader2

from java.util import ArrayList
from java.io import File


print "##########################################################"
print "#  SPIS-LEGACY to SPIS-5.xx Global Parameters Converter  #"
print "##########################################################"
print "START"
print ""

if len(sys.argv) < 3 or (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
    print "Usage: runConverter.sh legacyProjectIn.spis outputGlabolParamFile.xml"
    exit()
else:
    spisLegacyProjectDirIn = sys.argv[1]
    outputFilePathName = sys.argv[2]

print "Input SPIS-LEGACY project: " + spisLegacyProjectDirIn
print "Ouput file: " + outputFilePathName

print "Project loading... "
loader = ProjectLoader2()
loader.setLoadingList(["globals"])
loader.load(spisLegacyProjectDirIn)
sharedTasks["context"] = None
print "DONE"

print "Data conversion... "
list = ArrayList()

for keyName in sharedGlobals:
    print sharedGlobals[keyName]
    list.add(GlobalParameter(keyName, sharedGlobals[keyName][0], sharedGlobals[keyName][4], sharedGlobals[keyName][3],  sharedGlobals[keyName][1]))

    
writer = GlobalParamXMLWriter(list)
writer.setFile( File(outputFilePathName))
writer.write()
print "Done"
print ""

print "END"
