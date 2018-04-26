# Imports
from org.keridwen.core.messaging import EventBuilder
from java.io import File
from java.lang import System

# Loads the project
project = System.getenv("SPIS_PROJECT_FOLDER")
projectFolder = File(project)
EventBuilder.event("org.spis.ui.load.project", projectFolder).triggerCallEvent()




