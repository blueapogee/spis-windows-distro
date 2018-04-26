
import os
from os import *

pathIn = "/home/juju/Projects/Spis/OldVersionForIntegration/VersionPicUp/SpisUI/Bin/Tasks/"

pathOut = "./"

listOfFiles = listdir(pathOut)

for file in listOfFiles :
    
     print "Checking for ", file
     cmdTmp = "diff "+pathIn+file+" "+pathOut+file 
     os.system(cmdTmp)
