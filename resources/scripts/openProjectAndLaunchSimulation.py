# Imports
from org.keridwen.core.messaging import EventBuilder
from java.io import File
from java.lang import System
from org.spis.ui.simulation.util import SimulationFinalizer
from org.spis.instruments import Instrument
from org.spis.ui.simulation.command.dto import ProgressInstrumentAndNumTopFromUiDTO

# Loads the project
projectFolder = File("/home/benj/Bureau/SphereLowResolution.spis5")
EventBuilder.event("org.spis.ui.load.project", projectFolder).triggerCallEvent()

print"loading project"

# Launches UI 2 NUM
EventBuilder.event("org.spis.ui.ui2num", None).triggerCallEvent()

print"ui2num is done"

# Cleans the output folders
EventBuilder.event("org.spis.ui.clean.output.folders", None).triggerCallEvent()

print"output folder is cleaned"

# Prepares the simulation
EventBuilder.event("org.spis.ui.prepare.simulation", None).triggerCallEvent()

print"The simulation is built"

# Load instruments
EventBuilder.event("org.spis.ui.load.instrument.from.model.to.simulation", None).triggerCallEvent()

print"instruments are loaded"

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



