"""

**Creation:**     2010/09/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      1.1.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.1.0   | Julien Forest                        | Creation                   |
|         | contact@artenum.com                  |                            |
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

import os, string

from Bin.config import GL_SPIS_VERSION

#from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory
from Modules.Utils.LoggingUtilities     import LoggingUtilities

class TrackManager:
    """
    Track manager to handle the SPIS-TRACK scripts. See the User and Developer
    Manuals for further information. 
    """
    def __init__(self):
        self.logger = LoggerFactory.getLogger("TrackManager")
        self.logger.info("TrackManager initialized")
        self.loggingUtilities = LoggingUtilities(self.logger)
        
        self.loadedTrack = None
        self.deamonPath  = None
        self.deamonFile  = None
        
        self.IN_LINED_TRACK = 0
        
    
    def checkLoadedTrackVersion(self):
        """
        Check the version of the preloaded track. 
        """
        return(self.checkTrackVersion(self.loadedTrack))
        
        
    def checkTrackVersion(self, track):
        """
        Check the track version given in argument versus the SPIS's one. 
        
        Track, project and SPIS should have the same version. Older tracks and/or
        projects can sometime be supported by a newer version of SPIS but 
        without guaranty. Please see the SPINE community's forum for further 
        informations. 
        """
        self.logger.info("THE TRACK")

        if (track != None):
            for line in track: 
                #print "...", line
                if ('GL_TRACK_VERSION' in line):
                    self.logger.debug(line)
                    
                    trackVersion = string.atof(line.split("=")[1])
                    print trackVersion, GL_SPIS_VERSION
                    if ( trackVersion == GL_SPIS_VERSION ):
                        self.logger.debug("The version is OK")
                        return(True)
                    elif (trackVersion < GL_SPIS_VERSION ):
                        self.logger.warning( "SPIS TRACK version lower than the current SPIS's one. Compliance not guaranteed.\n"
                                            +"Try to update them manually in the track file to: "+ str(GL_SPIS_VERSION))
                        return(False)
                    elif (trackVersion > GL_SPIS_VERSION ):
                        self.logger.error("SPIS TRACK version too high or not supported")
                    else:
                        self.logger.error("TRACK version no supported or not readable")
            self.logger.error("No SPIS-TRACK version found...!!!"
                              + "Try to add GL_TRACK_VERSION="+str(GL_SPIS_VERSION)+"at the beginning of your script.")
            return(False)
        else:
            self.logger.error("Spis Track is None. This is not normal...")
            return(False)
        
    def setInLinedFlagFromLoadedTrack(self):
        self.setInLinedFlagFromTrack(self.loadedTrack)
        
    def setInLinedFlagFromTrack(self, track):
        """
        Read the IN_LINED_TRACK flag from the flag.
        """
        if (track != None):
            for line in track: 
                #print "...", line
                if ('IN_LINED_TRACK' in line):
                    self.logger.debug(line)
                    self.IN_LINED_TRACK = string.atof(line.split("=")[1])
                    self.logger.info("In-lined in track is: "+str(self.IN_LINED_TRACK))
                else:
                    self.IN_LINED_TRACK = 0
    
    def setInLinedTrackTrue(self):
        """
        Set the IN_LINED_TRACK flag to true, in order to process the track in one unique 
        exec command. This is useful if your track has indented functions (like loops or
        if-case). 
        
        The performances maybe better too, but the memory cost increased.  
        """
        self.IN_LINED_TRACK = 1
        
    def setInLinedTrackFalse(self):
        """
        Set the IN_LINED_TRACK flag to false, in order to process the track line by line. 
        This is useful to debug or process your track in one run but line by line. In case of 
        error the number misunderstood line is returned. 
        
        Currently, this method does not support indented functions (like loops or
        if-case).
        """
        self.IN_LINED_TRACK = 0
        
    def setInLinedTrackToDebug(self):
        """
        Under testing. 
        """
        self.IN_LINED_TRACK = 2
    
    def loadTrack(self, deamonFile):
        """
        Load the track (and do not process it yet), i.e 
        set the self.loadedTrack variable. 
        """
        self.deamonFile = deamonFile
        self.deamonPath = os.path.dirname(deamonFile)
        self.loadedTrack = open(deamonFile).readlines()
        
    def processLoadedTrack(self):
        """
        process the track pre-loaded in self.loadedTrack.
        """
        self.processTrack(self.loadedTrack)
        
    def processTrack(self, track):
        """
        Process the track given in argument. See setting of INLINED flag.
        """
        # to help the track to find itself
        deamonPath = self.deamonPath
        deamonFile = self.deamonFile
        
        if ( self.IN_LINED_TRACK == 0):
            # old fashion by this lazy Maxime
            try: 
                exec ("\n".join(track))
            except:
                self.logger.error( "Error in track, try in not in-lined mode")
                self.loggingUtilities.printStackTrace()
            
        elif ( self.IN_LINED_TRACK == 1):
              
            # ++mieux bien fashion by super Ju for debugging and control
            try: 
                for line in track:
                    #if () FIX ME in cas of indent
                    exec(line)
            except:
                self.logger.error( "Error in track: unable to process line Nb:"+str(track.index(line))+"\n"
                              +'-----> '+line)
                self.loggingUtilities.printStackTrace()
        else:
            self.logger.error( "Not implemented yet")
             
            
        
        