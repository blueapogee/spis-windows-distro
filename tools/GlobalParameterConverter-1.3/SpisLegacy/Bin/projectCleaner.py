
import os

print "SPIS project cleanning tool"

PROJECT_ROOT= "NOWHERE"
print "PROJECT_ROOT= ", PROJECT_ROOT

def cleanDF():
    dfList = os.listdir(PROJECT_ROOT+"/DataFields")
    for elm in dfList:
        fileList = os.listdir(PROJECT_ROOT+"/DataFields/"+elm)
        print PROJECT_ROOT+"/DataFields/"+elm
        for fileName in fileList:
            if fileName.split(".")[1] == "class":
               os.remove(PROJECT_ROOT+"/DataFields/"+elm+"/"+fileName)

print "Loaded and ready to act"

