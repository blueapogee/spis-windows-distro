
"""
**File name:**    DeamonWriter.py

**Creation:**     2006/09/30

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      2.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 2.1.0   | Arsene Lupin                         | Modif                      |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+

PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

print "LOADING MODULE DEAMON MANAGER"

import os
#import java
from Bin.config import GL_OS_NAME, GL_SYSTEM, GL_SPIS_VERSION
from Bin.ProjectWriter2 import ProjectWriter2

#from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory

class DeamonWriter:
    
    
    
    def __init__(self, simulationName, runId, scriptTemplate, deamonBaseCmd, pathProjectIn, pathProjectOut):
        '''
        Builds up a python/jython script to run a standalone simulation  
        runnable by SPIS-UI in batch mode. The simulation is then performed as 
        an independent job and can be run in command line mode as follow:
            
            spis_tasks_guiOSX.sh -b SimulationDeamon_MySimulation_Run_0.py
            
        simulationName must be a string.
        
        runId must be an integer.
        
        pathProjectIn is the path of the input project. This project must have its
        pre-processing phase completed (i.e mesh, dataFields, meshFields, globals 
        parameters must be computed and deployed). 
        
        pathProjectOut is the path of the output project. This one can be new (not 
        pre-existing) or be the same as the input one.
        '''
        
        
        
        self.__init__()
        self.logger = LoggerFactory.getLogger("DeamonWriter")
        self.logger.debug("DeamonWriter")
        
                
        self.simulationName = simulationName
        self.runId = runId
        self.pathProjectIn = pathProjectIn
        self.pathProjectOut = pathProjectOut
        
        #self.setDefaultDeamonBaseCmd()
        
        #self.setScriptTemplate()
        
        
    def __init__(self):
                
        self.DEFAULT_DEAMON_BASE_CMD = "runSpis.sh -b"
        
        self.simulationName = ""
        self.runId = 0
        self.pathProjectIn = ""
        self.pathProjectOut = ""
        self.scriptTemplate = ""
        self.deamonBaseCmd = self.DEFAULT_DEAMON_BASE_CMD
        self.templateFileName = ""
        self.headerFlag = True
        
        
        
    def setParameters(self, simulationName, runId, pathProjectIn, pathProjectOut):
        '''
        set the run parameters
        '''
        self.simulationName = simulationName
        self.runId = runId
        self.pathProjectIn = pathProjectIn
        self.pathProjectOut = pathProjectOut
        
    def setTemplateFileName(self, templateFileName):
        self.templateFileName = templateFileName
       
    def getTemplateFileName(self):
        return( self.templateFileName ) 
      
    def loadTemplate(self):
        self.loadTemplateFromFile(self.templateFileName)
        
    def loadTemplateFromFile(self, templateFileName):
        """
        load the track template from a file
        """
        self.templateFileName = templateFileName
        splittedTemplate = open(self.templateFileName).readlines()
        if (splittedTemplate[0][-1:] == "\n"):
            joinChar = ""
        else:
            joinChar= "\n"
        self.scriptTemplate =  joinChar.join(splittedTemplate)
        
    def setScriptTemplate(self, scriptTemplate):
        
        self.scriptTemplate = scriptTemplate
        
                    
    def setPathProjectIn(self, pathProjectIn):
        '''
        set the path of the input project.
        '''
        self.pathProjectIn = pathProjectIn
        
    def getPathProjectIn(self):
        '''
        returns the path of the input project.
        '''
        return(self.pathProjectIn)
        
    def setPathProjectOut(self, pathProjectOut):
        '''
        set the path of the output project.
        '''
        self.pathProjectOut = pathProjectOut
        
    def getPathProjectOut(self):
        '''
        returns the path of the output project.
        '''
        return(self.pathProjectOut)
        
    def addHeader(self):
        
        self.header = " ################################################# \n" \
                     +" #                  SPIS-TRACK                   # \n" \
                     +" ################################################# \n" \
                     + "GL_TRACK_VERSION = "+ str(GL_SPIS_VERSION)+"\n" \
                     + 'print "Daemon file: ", deamonFile \n' \
                     + 'print "Daemon path: ", deamonPath \n' \
                     + 'pathProjectIn = deamonPath \n' \
                     + 'pathProjectOut = deamonPath+os.path.basename(deamonFile)[23:-3] \n'\
                     + " ############## END OF HEADER ################### \n"
                     
        self.scriptTemplate = self.header + self.scriptTemplate
        
    def writeDeamon(self, deamonPath):
        '''
        write the script corresponding to the daemon in the directory set by deamonPath.
        '''
        if (self.headerFlag):
            self.addHeader()
            
        
        self.deamonPath = deamonPath
        self.deamonName = "simulationDeamon_"+self.simulationName+"_Run_"+`self.runId`+".py"
        try:
            print self.deamonPath+os.sep+self.deamonName
            deamonFile = open(self.deamonPath+os.sep+self.deamonName, "w")

            #print >> deamonFile, 'print "Daemon file: ", deamonFile'
            #print >> deamonFile, 'print "Daemon path: ", deamonPath'
            #print >> deamonFile, 'pathProjectIn = deamonPath'
            #print >> deamonFile, 'pathProjectOut = deamonPath+os.path.basename(deamonFile)[23:-3]'+'\n'
            #print >> deamonFile, 'pathProjectIn = "'+self.pathProjectIn+'"\n'
            #print >> deamonFile, 'pathProjectOut = "'+self.pathProjectOut+'"\n'

            print >> deamonFile, self.scriptTemplate
            deamonFile.close()
        except:
            self.logger.error("Error in DeamonWriter: Impossible to write the daemon")
        
    def writeDeamonInProjectIn(self):
        '''
        write the script corresponding to the daemon in the directory of the input project directory. 
        '''
        writer = ProjectWriter2()
        writer.setOuputDirectory(sharedFiles["project_directory"])
        writer.write()
        self.writeDeamon(self.pathProjectIn)
        
    def getDeamonName(self):
        '''
        returns the daemon name.
        '''
        return(self.deamonName)
        
    def setDefaultDeamonBaseCmd(self):
        '''
        set the default command (i.e the spis launching script) for the
        daemon according to operating system.
        '''
        if GL_SYSTEM == 'posix':
            if GL_OS_NAME == "Mac OS X":
                self.deamonBaseCmd = "spis_tasks_guiOSX.sh -b "
            else:
                self.deamonBaseCmd = "spis_tasks_gui.sh -b "
        else:
            self.deamonBaseCmd = "spis_tasks_gui.bat -b "

    def setDeamonBaseCmd(self, cmdIn):
        self.deamonBaseCmd = cmdIn
        
    def getDeamonBaseCmd(self):
        '''
        return the daemon base command.
        '''
        return(self.deamonBaseCmd)
        
    def runDeamon(self, deamonPath, deamonName):
        '''
        launch (run) the daemon as an independent job and returns the corresponding job
        Id. This method is system dependent. Please read the User Manual for further information.
        '''
        cmd = os.getcwd()+os.sep+self.deamonBaseCmd+deamonPath+os.sep+deamonName
        self.logger.debug(cmd)
        try: 
            jobId = os.java.lang.Runtime.getRuntime().exec(cmd)
        except:
            self.logger.error("Impossible to launch the job.")
        return(jobId)
        
    def runSelfDeamon(self):
        '''
        Launch (run) the current (self) daemon.
        '''
        return(self.runDeamon(self.deamonPath, self.deamonName))
        
