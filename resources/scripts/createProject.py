########################################################
# Project creation
########################################################

# Imports
from org.keridwen.core.messaging import EventBuilder
from org.spis.ui.model.node.project import Project
from org.spis.ui.model.node.project.study import Study
from org.keridwen.modelling.group.editor.app import GroupsTreeEditor
from com.artenum.frida.processing import GroupOperatorTypeFilter
from com.artenum.frida.processing import PropertyTypesFilter
from com.artenum.frida.io import PropertyTypesFilterReader
from com.artenum.frida.io import GroupOperatorTypeFilterReader
from org.keridwen.core.settings import ApplicationSettings
from org.spis.ui.mesh.model import MeshEditorNode
from com.artenum.penelope.mesh.interfaces import Mesh
from spis.Top.Top import NumTopFromUI
from org.spis.ui.simulation.util import SimulationFinalizer
from spis.Util.Instrument import InstrumentsCatalogue
from org.spis.instruments import Instrument
from org.spis.ui.simulation.command.dto import ProgressInstrumentAndNumTopFromUiDTO
from java.io import File



# Creates the Project Data Transfer Object
projectDTO = Project()
projectDTO.setProjectName("DefaultProject")
projectDTO.setProjectDescription("Project generated via Jython script")
projectDTO.setProjectParentFolder(File("/home/benj/Bureau/testpython"))

print"the Project Data Transfer Object is created"

# Creates the new Project from the DTO
EventBuilder.event("org.spis.ui.create.new.project", projectDTO).triggerCallEvent()

print"the new Project from the DTO is created"

# Creates the Study Data Transfer Object
studyDTO = Study()
studyDTO.setStudyName("DefaultStudy")
studyDTO.setStudyDescription("")

print"the Study Data Transfer Object is created"
                
# Creates the new Study from the DTO
EventBuilder.event("org.spis.ui.create.new.study", studyDTO).triggerCallEvent()

print"the new Study from the DTO is created"

# Saves the project
projectFolder = File(projectDTO.getProjectParentFolder(), projectDTO.getProjectName())
EventBuilder.event("org.spis.ui.save.as", projectFolder).triggerCallEvent()

print"project is saved"

# Load mesh file from .msh file
meshFile=File("/home/benj/Bureau/testpython/cad_sav.msh")
meshEditorNode=EventBuilder.event("org.spis.ui.mesh.editor.reset.main.mesh.node", None).triggerCallEvent()
meshEditorNode=EventBuilder.event("org.spis.ui.mesh.editor.add.mesh.from.file", meshFile).triggerCallEvent()
mesh=meshEditorNode.getMesh()

print"the mesh file is loaded"

# ---------------------------------
# Load group file from .xml file
# ---------------------------------
groupFile=File("/home/benj/Bureau/testpython/groups.xml")

# define the group operators
groupOperatorTypeFilterReader = GroupOperatorTypeFilterReader()
groupOperatorTypeFilterFilePath = ApplicationSettings.getProperty("org.spis.ui.group.editor.groupOperators")
groupOperatorTypeFilterFile = File(groupOperatorTypeFilterFilePath)
readGroupOperatorTypeFilter = groupOperatorTypeFilterReader.readGroupOperatorTypeFilter(groupOperatorTypeFilterFile)

# Define group types
propertyTypesFilterReader = PropertyTypesFilterReader()
groupTypesFilePath = ApplicationSettings.getProperty("org.spis.ui.group.editor.groupTypes")
propertyTypesFileterFile = File(groupTypesFilePath)
propertyTypesFilter = propertyTypesFilterReader.readPropertyTypesFilter(propertyTypesFileterFile)

groupTreeEditor=GroupsTreeEditor(propertyTypesFilter, readGroupOperatorTypeFilter, False)
EventBuilder.event("org.spis.ui.group.editor.load.catalogues", groupTreeEditor).triggerCallEvent()
groupTreeEditor.setMesh(mesh)
groupTreeEditor.loadGroupListFile(groupFile)
EventBuilder.event("org.spis.ui.group.editor.deploy.fields",groupTreeEditor).triggerCallEvent()

print"groups are loaded"

# Load electrical circuit
electricalCircuitFile=File("/home/benj/Bureau/testpython/circuit.txt")
EventBuilder.event("org.spis.ui.electrical.circuit.load.file",electricalCircuitFile).triggerCallEvent()

print"electrical circuit is loaded"

# create Run 
EventBuilder.event("org.spis.ui.global.parameters.create.run",None).triggerCallEvent()

# Copy electrical circuit 
EventBuilder.event("org.spis.ui.global.parameters.copy.electrical.circuit",None).triggerCallEvent()

print"new run is created"

# Load global parameters
globalParametersFile=File("/home/benj/Bureau/testpython/globalParameters-5.1.0.xml")
EventBuilder.event("org.spis.ui.global.parameters.load.global.parameters.from.file.without.ui",globalParametersFile).triggerCallEvent()

print"global parameters are created"

# Perform ui2num
numTopFromUI = EventBuilder.event("org.spis.ui.ui2num", None).triggerCallEvent()

print"ui2num is done"

# create catalogue used to create default instruments
instrumentCatalogue=InstrumentsCatalogue(numTopFromUI.getSimu());

print"catalogue used to create default instruments is computed"

# create default instruments
EventBuilder.event("org.spis.ui.create.default.instruments",instrumentCatalogue).triggerCallEvent()

print"default instruments are created"

# Saves the project
projectFolder = File(projectDTO.getProjectParentFolder(), projectDTO.getProjectName())
EventBuilder.event("org.spis.ui.save", None).triggerCallEvent()

print"project is saved"

# Prepares the simulation
EventBuilder.event("org.spis.ui.prepare.simulation", None).triggerCallEvent()

print"simulation is prepared"

print"simulation is launching"

# Launches simulation
progressInstrumentAndNumTopFromUiDTO = EventBuilder.event("org.spis.ui.launch.simulation", None).triggerCallEvent()
simulationFinalizer = SimulationFinalizer(progressInstrumentAndNumTopFromUiDTO.getNumTopFromUI())
progressInstrument = progressInstrumentAndNumTopFromUiDTO.getProgressInstrument()
progressInstrument.addListener(simulationFinalizer)
simulationFinalizer.waitForSimulation()

print"simulation is finished"

print"time series are extracting"

#extract time series
simulationSupervisor = EventBuilder.event("org.spis.ui.extract.time.data", None).triggerSignalEvent()

print"time series are extracted"

print"end"

#end of the script
sys.exit()


