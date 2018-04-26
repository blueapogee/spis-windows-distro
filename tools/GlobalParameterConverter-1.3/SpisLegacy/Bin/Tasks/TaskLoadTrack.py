
        
        
from Modules.Utils.TrackManager import TrackManager

from Bin.Tasks.Task           import Task
from Bin.Tasks.common         import create_internal_frame
from Bin.Tasks.shared         import sharedFrames, sharedFiles

from Bin.config               import GL_DEFAULT_TRACKS_TEMPLATES_PATH

from javax.swing import JFileChooser
from java.io import File

#from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory
from Modules.Utils.LoggingUtilities     import LoggingUtilities

class TaskLoadTrack(Task):
    """Java memory monitor"""
    desc="Build a MemoryMonitor"
    
    def run_task(self):
        
        self.BY_PASS_VALIDATION = 1
        
        if sharedFiles.has_key("LAST_TRACK_PATH"):
            PATH_IN = sharedFiles["LAST_TRACK_PATH"]
        else:
            PATH_IN = GL_DEFAULT_TRACKS_TEMPLATES_PATH
        
        self.logger = LoggerFactory.getLogger("Task")
        #self.logger.info("TrackManager initialised")
        #self.loggingUtilities = LoggingUtilities(self.logger)
        
        chooser = JFileChooser()
        chooser.setCurrentDirectory(File(PATH_IN))
        chooser.showDialog(None, None)
        if (chooser.getSelectedFile() != None):
            selectedTrackFile = chooser.getSelectedFile().absolutePath
            sharedFiles["LAST_TRACK_PATH"] = selectedTrackFile

            tracker = TrackManager()
            tracker.loadTrack(selectedTrackFile)
            tracker.setInLinedFlagFromLoadedTrack()
            if (tracker.checkLoadedTrackVersion()):
                tracker.processLoadedTrack()
                self.logger.info("Spis Track processed successfully")
            else:
                if (self.BY_PASS_VALIDATION):
                    self.logger.warn("Track version validation by-passed")
                    tracker.processLoadedTrack()
                    self.logger.info("Spis Track processed successfully")
                else:
                    self.logger.info("Spis Track no processed")
        