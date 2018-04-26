"""
Generic GEOM manager. This module will manage in a common workspace all 
your CAD files needed to describe your GEOM and the reference of a main file to 
be loaded into SPIS-UI. This module is independent on the CAD format and can work 
with all type of data. It will call relevant external CAD tools, modelers and 
editor.  

This module can also be used as standalone application. Please see the SPIS-UI User
Manual for further information. 

**Project ref:**  Spis/SpisUI

**File name:**    GeomManager.py

:status:          Implemented

**Creation:**     10/07/200r63

**Modification:** 22/08/2003  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest, Sebastien Jourdain

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | J.Forest                             | Creation                   |
|                | j.fores@atenum.com                   |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | Sebastian Jourdain                   | Bug correction             |
|                | jourdain@artenum.com                 |                            |
+----------------+--------------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"

import os, shutil, string, sys
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")

from Bin.Tasks.shared          import sharedFrames
from Bin.Tasks.shared          import sharedTasks
from Bin.Tasks.shared          import sharedFiles
from Bin.Tasks.shared          import sharedFlags

from Bin.Tasks.common          import create_internal_frame
from Bin.exportTemplateControl import exportTemplateControl
from Bin.Tasks.common          import create_internal_frame
from Bin.FrameManager          import FrameManager
from Bin.config                import GL_EXCHANGE, GL_CMD_GMSH, GL_CMD_EDITOR

from javax.swing               import JOptionPane, JButton, JPanel, BorderFactory, JScrollPane, ImageIcon, JTree, JLabel
from javax.swing.tree          import DefaultMutableTreeNode

from java.awt                  import BorderLayout, GridLayout
#from java.io                   import File
#from java.awt.event            import ItemEvent

from org.spis.imp.ui.util      import FileDialog



class GeomManager:
    '''
    Generic GEOM manager. This module will manage in a common workspace all
    needed CAD files to describe the complete geometric model. It also set the reference of 
    the main CAD file that should be loaded into SPIS-UI as entry point. 
    This module is independent on the CAD format and can work
    with all type of data. It will call relevant external CAD tools, modelers and
    editor.
    '''
        
    def __init__(self):
        
        self.logger = LoggerFactory.getLogger("GeomLogger")
        self.logger.info("Start Geom Manager")
        
        self.frameManager = FrameManager()
        self.frameManager.setGuicontext(sharedFlags['guiMode'])
        self.InternalFrame = self.frameManager.getNewFrame("Geometry/CAD manager")
        self.externalMethod = None
    
    def setFrame(self, frameIn): 
        self.InternalFrame = frameIn
        
    def buildGUI(self):
        
        self.reBuildTree()

        self.InternalFrame.getContentPane().setLayout(BorderLayout())
        if sharedFiles['TheCADFileIn'] != None:
            self.mainFileNameLabel = JLabel("Main file:"+sharedFiles['TheCADFileIn'])
        else:
            self.mainFileNameLabel = JLabel("Main file:")
        self.InternalFrame.getContentPane().add( self.mainFileNameLabel, BorderLayout.NORTH)

        self.InternalFrame.getContentPane().add( JScrollPane(self.tree),BorderLayout.CENTER)
        self.InternalFrame.setVisible(1)
        
        self.addNewFileButton   = JButton('New file', actionPerformed = self.newFile)
        self.addFileButton      = JButton('Add file', actionPerformed = self.addFile)
        self.removeFileButton   = JButton('Remove file', actionPerformed = self.removeFile)
        self.setAsMainButton    = JButton('Set as main',actionPerformed = self.setAsMain)
        
        
        self.editWithEditorButton    = JButton('Editor', actionPerformed = self.editWithEditor)
        self.editWithCADToolButton   = JButton('CAD tool',actionPerformed = self.editWithCADTool)
        self.optionsButton           = JButton('New File',actionPerformed = self.newFile)
        self.updateProjectButton     = JButton('Update project',actionPerformed = self.updateProject)
                                            
        self.buttonPane = JPanel()
        self.buttonPane.setLayout(GridLayout(3, 3, 5, 5))
        
        self.buttonPane.add(self.addNewFileButton)
        self.buttonPane.add(self.addFileButton)
        self.buttonPane.add(self.removeFileButton)
        self.buttonPane.add(self.setAsMainButton)
        
        self.buttonPane.add(self.editWithEditorButton)
        self.buttonPane.add(self.editWithCADToolButton)
        self.buttonPane.add(self.updateProjectButton)
        
        self.buttonPane.setBorder(BorderFactory.createEmptyBorder(5,5,5,5))
        #self.dataListScroll.setBorder(BorderFactory.createEmptyBorder(5,5,5,5))
        self.InternalFrame.contentPane.add(self.buttonPane, BorderLayout.SOUTH)

        templatePanel = JPanel()
        buildSphereButton = JButton(actionPerformed = self.buildSphere)
        
        buildSphereButton.setIcon( ImageIcon(self.InternalFrame.getClass().getResource("/basicSphere.png")));
        templatePanel.add(buildSphereButton)
        self.InternalFrame.contentPane.add(templatePanel, BorderLayout.EAST)
        
        #FIX ME: put a better layout manager
        self.controlPanel = JPanel(GridLayout(10, 1, 5, 5))
        self.InternalFrame.contentPane.add(self.controlPanel, BorderLayout.WEST)
        
        
    def show(self):
        self.InternalFrame.setVisible(0);        
        # in UI context
        if sharedFlags['guiMode'] == 1:
            size = self.InternalFrame.getParent().getSize()
            self.InternalFrame.reshape(0,0,size.width/3+2,size.height)
        if sharedFlags['guiMode'] == -1:
            self.InternalFrame.reshape(0, 0, 400, 600)
        self.InternalFrame.setVisible(1);

        
    def newFile(self, dummy):
        """
        add an new empty file to the workspace.
        """        
        InternalDialogueFrame = self.frameManager.getNewFrame("Warning")
        dialogueMessage = "Please set a name for the new file."
        response = JOptionPane.showInputDialog( InternalDialogueFrame, dialogueMessage, "New EOM file", JOptionPane.OK_OPTION)
        
        # just to have the right extension
        splitPath = response.split(".")
        extension = splitPath[-1]
        if ( extension != "geo" ):
            cleanedFileName=""
            if (len(splitPath) > 1):      
                for elm in splitPath[:-1]:
                    cleanedFileName = cleanedFileName +"_"+ elm
            else:
                cleanedFileName = splitPath[0]
            cleanedFileName = cleanedFileName +".geo"
        else:
            cleanedFileName = response
        
        try: 
            fileOut = open(os.path.join(GL_EXCHANGE, "Geom", cleanedFileName), 'w')
            fileOut.write("")
            fileOut.close()
        except:
            self.logger.error("Impossible to open the selected file")
            
        self.rootNode.add(DefaultMutableTreeNode(cleanedFileName))
        self.tree.updateUI()
        InternalDialogueFrame.dispose()


    def reBuildTree(self):
        """
        rebuild the tree from the directory listing
        """
        self.rootNode = DefaultMutableTreeNode('GEOM workspace')
        
        list = os.listdir(os.path.join(GL_EXCHANGE, "Geom"))
        
        for elm in list:
            node = DefaultMutableTreeNode(elm)
            self.rootNode.add(node)
             
        self.tree = JTree(self.rootNode)
        self.tree.updateUI()
        
        
    def getSelectedNodePath(self):
        """
        return the selected node
        """
        if self.tree.getSelectionPath() != None:
            return(self.tree.getSelectionPath().getLastPathComponent().toString())
        else:
            return(None)
        
        
    def check(self, dummy):
        print "dffddf"
        
    def buildSphere(self, dummy):
        """
        call the module of pre-set sphere in Gmsh geo format.
        """
        tmplateControler = exportTemplateControl("sphere")
        tmplateControler.setGeomManagerToUpdate(self)
        
        
    def editWithCADTool(self, dummy):
        """
        call the CAD tool and edit the selected file.
        """
        if self.getSelectedNodePath() != None:
            selectedFile = os.path.join(GL_EXCHANGE, "Geom", self.getSelectedNodePath())
            ACTION = GL_CMD_GMSH+' '+selectedFile+' &'
            print ACTION
            #os.system(ACTION)
            
            #to execute the CAD tool as fork (not locking) mode
            os.java.lang.Runtime.getRuntime().exec(ACTION)
        else:
            self.logger.error("Please select a file before to edit it!")
            
        
    def editWithEditor(self, dummy):
        """
        Edit the selected file.
        """
        if self.getSelectedNodePath() != None:
            selectedFile = os.path.join(GL_EXCHANGE, "Geom", self.getSelectedNodePath())
            ACTION = GL_CMD_EDITOR+' '+selectedFile
            
            #to execute the CAD tool in demaon (not locking) mode
            os.java.lang.Runtime.getRuntime().exec(ACTION)    
        else:
            self.logger.error("Please select a file before to edit it!")
        
        
    def setAsMain(self, dummy):
        """
        set the main GEOM file, i.e the CAD file calling all relevant other CAD components.
        """
        sharedFiles['TheCADFileIn'] = os.path.join(GL_EXCHANGE, "Geom", self.getSelectedNodePath())
        self.mainFileNameLabel.setText("Main file: "+sharedFiles['TheCADFileIn'])
        self.logger.info("main GEOM file" + sharedFiles['TheCADFileIn'])
        if self.externalMethod != None:
            self.externalMethod()
        
        
    def setAsMainFileFrom(self, AbsPathIn, fileNameIn):
        """
        set the file given in argument as main CAD file.
        """
        sharedFiles['TheCADFileIn'] = self.addFileFrom(AbsPathIn, fileNameIn)
        print "sharedFiles['TheCADFileIn'] in GeomManager= "+sharedFiles['TheCADFileIn'] 
        
        
    def updateProject(self, dummy):
        """
        update the project according to the current status of the workspace.
        """
        try:
            fileList = os.listdir(os.path.join(GL_EXCHANGE, "Geom"))
            if ( fileList != []):
                for file in fileList:
                    fileNameIn = os.path.join(GL_EXCHANGE, "Geom", file)
                    fileNameOut = os.path.join(sharedFiles["project_directory"], "Geom", file)
                    shutil.copyfile(fileNameIn, fileNameOut)
            self.logger.info("Project updated")
        except:
            self.logger.error("Impossible to update the project. \n Maybe it is not defined yet. \n Please save the current project before to update it.")
            
            
    def setExternalMethod(self, methodIn):

        self.externalMethod = methodIn
        
        
    def addFile(self, dummy):
        """
        adds a new GEOM file to the workspace. 
        """
        dialog = FileDialog()
        
        if (dialog.showOpenDialog(None)):
            fileNameIn = dialog.getFileToSave().getName()
            fileNameInAbsPath = dialog.getFileToSave().getAbsolutePath()
            self.logger.debug("Chosen file = "+fileNameInAbsPath)
           
            fileNameOut = os.path.join(GL_EXCHANGE, "Geom", fileNameIn)
            #FIX ME : rajouter control si fichier existe avec meme nom
            shutil.copyfile(fileNameInAbsPath, fileNameOut)
           
            self.addNodeOnTree(fileNameIn)
           
    def addFileFrom(self, AbsPathIn, fileNameIn):
        fileNameInAbsPath = os.path.join(AbsPathIn, fileNameIn)
        fileNameOut = os.path.join(GL_EXCHANGE, "Geom", fileNameIn)
        shutil.copyfile(fileNameInAbsPath, fileNameOut)
        return(fileNameOut)
        
           
    def addNodeOnTree(self, fileNameIn):
        self.rootNode.add(DefaultMutableTreeNode(fileNameIn))
        self.tree.updateUI()
        
        
    def removeFile(self, dummy):
        """
        remove the selected file of the current workspace
        """
        selectedFile = os.path.join(GL_EXCHANGE, "Geom", self.getSelectedNodePath())
        if sharedFlags['guiMode'] == 1 or sharedFlags['guiMode'] == -1:
            InternalFrame = self.frameManager.getNewFrame("Warning")
            dialogueMessage = "<html>Do you really want to remove this file from the workspace ?</html>"
            response = JOptionPane.showConfirmDialog( InternalFrame, dialogueMessage, "GEOM file loading", JOptionPane.YES_NO_OPTION)
            if response == 0:
                os.remove(selectedFile)
                self.tree.getSelectionPath().getLastPathComponent().getParent().remove(self.tree.getSelectionPath().getLastPathComponent())
                self.tree.updateUI()
                print "file removed"
        
    def close(self):
        self.InternalFrame.dispose()
        self = None #in order to force the garbage collector to do its job.
           
           
           
    def readParametrisedGeometricalModel(self, geomDirPath):
        """
        read the geometric models
        """
        geomPrefix = "TP_ESD"
        paramPrefix = "GEOM_PARAM"
        
        geomFileList = {}
        paramFileList = {}
        
        filelist = os.listdir(geomDirPath)
        for fileName in filelist:
            if fileName[:len(geomPrefix)] == geomPrefix: 
                geomFileList[fileName] = fileName
            elif fileName[:len(paramPrefix)] == paramPrefix:
                paramFileList[fileName] = self.readGeomParametersFile(os.path.join( geomDirPath,fileName))
        return( geomFileList, paramFileList )
           
    def readGeomParametersFile(self, fileName):
        """
        Read the parameters file for the geometric model.
        """
        paramDic = {}        
        fileIn = open(fileName, "r")
        lines = fileIn.readlines()
        joinedLines = string.join(lines)
        
        # to remove the comments in the file
        while ("/*" in joinedLines or "*/" in joinedLines):
            joinedLines = string.replace( joinedLines, joinedLines[ joinedLines.index("/*"): joinedLines.index("*/")+2], "")
            
        splitLines = joinedLines.split("\n")
        for elm in splitLines:
            if "=" in elm:
                splitElm = elm.split("=")
                key = splitElm[0].replace(" ", "") # small trick to remove all space from the key name
                paramDic[key] = splitElm[1][:-1].replace(" ", "")
        fileIn.close()
        return(paramDic)
        
        
    def writeGeomParametersFile(self, fileName, paramDic):
        """
        Write the parameters file of a parametrised system. 
        """
        fileOut = open(fileName, "w")
        for key in paramDic.keys():
            fileOut.write(key+" = "+str( paramDic[key] )+";\n")
        fileOut.close()
        
        
           
class MainGeomManager:
    '''
    To call the Geom Manager as standalone application.
    '''
    
    def usage(self):
        print """%s: usage:
    -h, --help            - print this help message and exit
    -g, --graphical       - run the GUI
    -b FILE, --batch=FILE - run spis in batch mode, set the batch file
    """ % sys.argv[0]

    def main(self):
        
        import Bin.config

        self.geomManager = GeomManager()
        self.geomManager.buildGUI()
        
        openProjectButton = JButton(actionPerformed = self.openProject)
        openProjectButton.setIcon( ImageIcon(self.geomManager.InternalFrame.getClass().getResource("/openProject2.png")))
        self.geomManager.controlPanel.add(openProjectButton)
        
        saveProjectButton = JButton(actionPerformed = self.saveProject)
        saveProjectButton.setIcon( ImageIcon(self.geomManager.InternalFrame.getClass().getResource("/saveProject2.png")))
        self.geomManager.controlPanel.add(saveProjectButton)
        
        closeButton = JButton("Exit", actionPerformed = self.close )
        self.geomManager.buttonPane.add(closeButton)
        
        self.geomManager.show()
        
    def close(self, dummy):
        import sys
        sys.exit()
        
    def openProject(self, dummy):
        print "Open project"

        from org.spis.imp.ui.util  import DirectoryDialog
        from Bin.ProjectLoader2    import ProjectLoader2
        
        #default project format
        sharedFiles["projectSavingFormat"] = "V2"


        dialog = DirectoryDialog("")
        dialog.addFileType(".v1", "Version 1.0")
        dialog.addFileType(".v3", "Version 3.0")
        dialog.addFileType(".v2", "Version 2.0")
        
        if (dialog.showDialog(None)):
            if (dialog.getSelectedFileTypeDescription() == 'Version 1.0'):
                print "V1"
                sharedFiles["projectSavingFormat"] = "V1"
            if (dialog.getSelectedFileTypeDescription() == 'Version 2.0'):
                print "V2"
                sharedFiles["projectSavingFormat"] = "V2"
            if (dialog.getSelectedFileTypeDescription() == 'Version 3.0'):
                print "V3"
                sharedFiles["projectSavingFormat"] = "V3"
            sharedFiles["project_directory"] = dialog.getFileToSave().getAbsolutePath()
          
            self.loader = ProjectLoader2()
            self.loader.setLoadingList([ "projectInfo","geomFile"])
            self.loader.load()      

            self.geomManager.reBuildTree()
            
            
    def saveProject(self, dummmy):
        
        from org.spis.imp.ui.util  import DirectoryDialog
        from Bin.ProjectWriter2    import ProjectWriter2
        from Bin.ProjectWriter3    import ProjectWriter3
        
        #if the project path is not defined, we open a file browser
        #otherwise, we save in the default directory
        print "Project path ", sharedFiles["project_directory"]
        print "projectSavingFlag =", sharedFiles["projectSavingFlag"]
             
        dialog = DirectoryDialog("")
        dialog.addFileType(".v1", "Version 1.0")
        dialog.addFileType(".v3", "Version 3.0")
        dialog.addFileType(".v2", "Version 2.0")
        sharedFiles["projectSavingFlag"] = 1
    
        if (dialog.showDialog(None)):
            if (dialog.getSelectedFileTypeDescription() == 'Version 1.0'):
                print "V1"
                sharedFiles["projectSavingFormat"] = "V1"
            if (dialog.getSelectedFileTypeDescription() == 'Version 2.0'):
                print "V2"
                sharedFiles["projectSavingFormat"] = "V2"
            if (dialog.getSelectedFileTypeDescription() == 'Version 3.0'):
                print "V3"
                sharedFiles["projectSavingFormat"] = "V3"
            sharedFiles["project_directory"] = dialog.getFileToSave().getAbsolutePath()
                
        if sharedFiles["projectSavingFormat"] == "V1":
            print "Deprecated format"
        elif sharedFiles["projectSavingFormat"] == "V2":
            writer = ProjectWriter2()
            writer.setOuputDirectory(sharedFiles["project_directory"])
            writer.createNewProject()
            writer.write()
        elif sharedFiles["projectSavingFormat"] == "V3":
            writer = ProjectWriter3()
            writer.setOuputDirectory(sharedFiles["project_directory"])
            writer.write()
        else:
            print "Unsupported format"
        
                      
if __name__ == "__main__":
    
    from Bin.Tasks.shared         import sharedFlags
    sharedFlags['guiMode'] = -1
    
    main = MainGeomManager()
    main.main()
    
    
    
