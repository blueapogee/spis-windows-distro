# Imports
from java.lang import System
from org.keridwen.core.messaging import EventBuilder
from org.spis.ui.model.node.project import Project
from org.spis.ui.model.node.project.study import Study
from java.io import File
from org.spis.ui.model.key import SpisModelEventKeys



#################################################
# replace simple back slash into double backslah
# 
# to test : tutu = "\u____\t___\a____\b____\c____\e____\f____\p___\v___\r___"
#################################################

def clean(pathIn, requestedOsSep = "\\\\"):
    magicString = "<-->"

    ctrCharDic = {}
    ctrCharDic["\\"] = magicString
    ctrCharDic["\t"] = magicString + "t"
    ctrCharDic["\b"] = magicString + "b"
    ctrCharDic["\p"] = magicString + "p"
    ctrCharDic["\n"] = magicString + "n"
    ctrCharDic["\a"] = magicString + "a"
    ctrCharDic["\f"] = magicString + "f"
    ctrCharDic["\r"] = magicString + "r"
    ctrCharDic["\v"] = magicString + "v"
    ctrCharDic["\'"] = magicString + "'"
    ctrCharDic['\"'] = magicString + '"'
    ctrCharDic["\u"] = magicString + "u"
    ctrCharDic["\U"] = magicString + "U"
    ctrCharDic["\v"] = magicString + "v"
    ctrCharDic["\N"] = magicString + "N"
    ctrCharDic["\o"] = magicString + "o"
    ctrCharDic["\\x"] = magicString + "x"

    for key in ctrCharDic.keys():
        pathIn = pathIn.replace(key, ctrCharDic[key])

    pathOut = pathIn.replace(magicString, requestedOsSep)

    return pathOut


####################################################################
# Script used to create a project and add inside a specific geometry
# Script only compatible with Jython and SPIS 5 and Keridwen 2 and higher
####################################################################


####################################################################
# Edit your variables here
####################################################################

# define the name of the project
projectName=System.getenv("SPIS_PROJECT_NAME")

# define the description of the project
projectDescription=System.getenv("SPIS_PROJECT_DESCRIPTION")

# define the path where the spi5 project will be created
projectPath=System.getenv("SPIS_PROJECT_PATH")
projectPath=clean(projectPath)

# The name of the study
studyName=System.getenv("SPIS_STUDY_NAME")

# The description of the study
studyDescription=System.getenv("SPIS_STUDY_DESCRIPTION")

# The path of the cad file
cadFilePath=System.getenv("SPIS_CAD_FILE")
cadFilePath=clean(cadFilePath)

####################################################################
# END OF THE SETTINGS
####################################################################

 
####################################################################
# DO NOT EDIT BELOW
####################################################################

# set the transition to home panel
EventBuilder.event(SpisModelEventKeys.TRIGGER_TRANSITION, "org.spis.ui.transition.home.next").triggerCallEvent()

# Creates the Project Data Transfer Object
projectDTO = Project()
projectDTO.setProjectName(projectName)
projectDTO.setProjectDescription(projectDescription)
projectDTO.setProjectParentFolder(File(projectPath))

# Creates the new Project from the DTO
EventBuilder.event("org.spis.ui.create.new.project", projectDTO).triggerCallEvent() 

# Creates the Study Data Transfer Object
studyDTO = Study()
studyDTO.setStudyName(studyName)
studyDTO.setStudyDescription(studyDescription)

# Creates the new Study from the DTO
EventBuilder.event("org.spis.ui.create.new.study", studyDTO).triggerCallEvent()

# Saves the project
projectFolder = File(projectDTO.getProjectParentFolder(), projectDTO.getProjectName())
EventBuilder.event("org.spis.ui.save.as", projectFolder).triggerCallEvent()

# set the transition to geometry editor
EventBuilder.event(SpisModelEventKeys.TRIGGER_TRANSITION, "org.spis.ui.transition.project.configuration.next").triggerCallEvent()

# Load cad file 
cadFile=File(cadFilePath)
EventBuilder.event("org.spis.ui.geometry.editor.add.geometry.from.cad.file.to.model", cadFile).triggerCallEvent()

# Saves the project
projectFolder = File(projectDTO.getProjectParentFolder(), projectDTO.getProjectName())
EventBuilder.event("org.spis.ui.save", None).triggerCallEvent()

