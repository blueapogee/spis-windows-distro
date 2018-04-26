
"""
Controler for the general ASCII based file format exporterd. Developped under CNRS / CETP contract. 

**Creation:**     2008/01/01

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      1.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Julien Forest                        | Creation                   |
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


from java.awt.event import ActionListener

try:
    from com.artenum.keridwen.exportGUI import DataExporterPanel
except:
    print "ExporterControler: impossible to load DataExporterPanel"

import os, time, string
from Modules.InOut.MeshWriter         import MeshWriter
from Modules.InOut.DataFieldRawWriter import DataFieldRawWriter
from Modules.InOut.ProjectManager     import ProjectManager

from Bin.Tasks.shared                 import *
from Bin.Tasks.shared                 import sharedFlags
from Bin.FrameManager                 import FrameManager

class Controler:
    """
    Export controler
    """
    def __init__(self):
        """
        Main constructor
        """
        self.boss = None
        self.projectPath = os.path.join(sharedFiles['project_directory'], "Export")
        self.meshFileName = "defaultMesh.msh"
        self.meshComment = "No comment"
        self.dataComment = "No comment"
        self.hostName = "localhost"

        self.controlPanel = DataExporterPanel()
        self.controlPanel.setJyActionListener(ExportActionListener(self))

        self.controlPanel.setDirectoryPath(self.projectPath)
        self.controlPanel.setDataComment(self.dataComment)

        frameManager  = FrameManager()
        frameManager.setGuicontext(sharedFlags['guiMode'])
        self.internalFrame = frameManager.getNewFrame("DataField Exporter")
        self.internalFrame.getContentPane().add(self.controlPanel)

    def showControlPanel(self):
        size = self.internalFrame.getParent().getSize()
        self.internalFrame.reshape(size.width/3-2,0,(size.width*2)/3+2,size.height-70)
        #self.internalFrame.show()
        self.internalFrame.setVisible(1)

    def setHostName(self, hostName):
        self.hostName = hostName

    def setDataFieldName(self, DFName):
        self.dataFieldName = DFName

    def export(self):
        '''
        export the current dataField
        '''
        print "Export dataField: ", self.dataFieldName
        self.exportDF(self.dataFieldName)

    def exportListOfDataFields(self, dataFieldInNameList):
        for name in dataFieldInNameList:
            self.exportDF(name)

    def exportDF(self, dataFieldInName):
        '''
        export the DataField of name dataFieldInName.
        '''
        if self.boss == None:
            self.boss = ProjectManager()
            self.boss.setProjectFullName(self.projectPath)
            self.expDataId = 0

        self.expDataId = self.expDataId + 1
        currentTime = self.getCurrentTime()
        self.boss.addElement("mesh1", MeshWriter(), shared['Mesh'], self.meshFileName, "Mesh", currentTime, "rws", self.meshComment)

        if ((sharedData["AllDataField"].Dic != None) and sharedData["AllDataField"].Dic.has_key(dataFieldInName)):
            dataField   = sharedData["AllDataField"].Dic[dataFieldInName]
            meshFieldId = sharedData["AllDataField"].Dic[dataFieldInName].MeshFieldId
            meshField   = sharedData['AllMeshField'].GetMeshFieldById(meshFieldId)

        
            dataKey = "data"+`self.expDataId`
            print string.replace(dataField.Name, " ","_")
            self.boss.addElement( dataKey, DataFieldRawWriter(), [dataField, meshField, self.meshFileName], 
            self.checkExtension(self.cleanPathName(dataField.Name),"dat"), "DataField", currentTime, "rws", self.dataComment)
            if self.boss.dataDepDic.has_key("mesh1"):
                self.boss.addDepencyForElement("mesh1",dataKey)
            else:
                self.boss.setDependencyGraphForElement("mesh1",[dataKey])
            self.boss.setDependencyGraphForElement(dataKey,["mesh1"])

            self.boss.writeProject(self.controlPanel.isReWriteAll())
            #self.internalFrame.dispose()
            self.internalFrame.setVisible(0)
            print " DONE"
        else:
            print "Error: DataField not defined!"
            #return(None)
  
    def cleanPathName(self, nameIn):
        '''
        remove unsupported characters for file name of nameIn. This will
        replace the following characters by an underscore: space, ",", 
        ":", "=", "-", "[", "]", "(", ")", "?" and "~".
        '''
        forbittenCharList = [" ", ",", ":", "=", "-", "[", "]", "(", ")", "?", "~"]
        for elm in forbittenCharList:
            nameIn = string.replace(nameIn,elm, "_")
        return(nameIn)

    def checkExtension(self, fileName, extension):
        splitFileName = string.split(fileName, ".")
        if len(splitFileName) > 1 and splitFileName[-1] != extension:
            fileNameOut = splitFileName[0]+"."+extension
        elif len(splitFileName) < 2:
            fileNameOut = splitFileName[0]+"."+extension
        return(fileNameOut)

    def getCurrentTime(self):
        localTime = time.localtime()
        currentDate=""
        for elm in localTime:
            currentDate = currentDate+`elm`+"_"
        currentDate = currentDate[:-1]
        return(currentDate)

    def GetPanelData(self):
        self.projectPath = self.controlPanel.getDirectoryPath()
        self.meshFileName = self.controlPanel.getMeshFilePath()  #FIX ME
        self.meshComment = self.controlPanel.getMeshComment()
        self.dataComment = self.controlPanel.getDataComment()

class ExportActionListener(ActionListener):
    def __init__(self, ctr):
        self.ctr = ctr

    def actionPerformed(self, ae):
        self.ctr.GetPanelData()
        self.ctr.export()
