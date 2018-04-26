"""
Module of control of the generation of geo gmsh objects from tremplate. This module
will provides a generix GUI for this.  
**Project ref:**  Spis/SpisUI

**File name:**    exportTemplateControl.py

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  validation

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

import os, shutil, sys, string

from Bin.buildGenericSphere   import buildGenericSphere
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.shared         import sharedTasks
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedFlags

from Bin.Tasks.common         import create_internal_frame
from Bin.config               import GL_EXCHANGE, GL_CMD_GMSH, GL_CMD_EDITOR
from Bin.FrameManager         import FrameManager


import java
import javax.swing 
from Bin.Tasks.common         import create_internal_frame
from Bin.config               import GL_EXCHANGE, GL_CMD_GMSH, GL_CMD_EDITOR
from pawt import swing
from javax.swing              import JOptionPane
from pawt                     import swing, colors
from java.awt                 import *
from java.io                  import File

from org.spis.imp.ui.util     import FileDialog

class exportTemplateControl:
    '''
    Module of control of the generation of geo gmsh objects from tremplate. This module
    will provides a generix GUI for this.
    '''
    def __init__(self, template):
        '''
        Default cosntructor. 
        ''' 
        if template == "sphere":
            self.model = buildGenericSphere()
        else:
            print "Tmplate not defined"
            
        self.frameManager = FrameManager()
        self.frameManager.setGuicontext(sharedFlags['guiMode'])
        self.InternalFrame = self.frameManager.getNewFrame("Geometry/CAD manager")

        jLabel1 =  javax.swing.JLabel()
        globalPanel =  javax.swing.JPanel()
        jLabel2 =  javax.swing.JLabel()
        self.subSystemName =  javax.swing.JTextField()
        subSystemIdLabel =  javax.swing.JLabel()
        self.subSystemId =  javax.swing.JTextField()
        centralPanel =  javax.swing.JPanel()
        levelExportPanel =  javax.swing.JPanel()
        self.nodeCheckBox =  javax.swing.JCheckBox()
        self.curveCheckBox =  javax.swing.JCheckBox()
        self.surfaceCheckBox =  javax.swing.JCheckBox()
        objectSettingPanel =  javax.swing.JPanel()
        exportPanel =  javax.swing.JPanel()
        exportButton =  javax.swing.JButton(actionPerformed = self.buildSphere)
        exportSelectionPanel =  javax.swing.JPanel()
        self.gmshExportSelection =  javax.swing.JCheckBox()
        jCheckBox5 =  javax.swing.JCheckBox()
        
        jLabel1.setText("jLabel1");
        
        self.InternalFrame.getContentPane().setLayout( java.awt.BorderLayout(5, 5));
        self.InternalFrame.getContentPane().setBorder(javax.swing.BorderFactory.createEmptyBorder(15, 15, 15, 15))
        
        
        globalPanel.setLayout( java.awt.GridLayout(2, 2))
        
        jLabel2.setText("Subsystem Name");
        globalPanel.add(jLabel2);
        self.subSystemName.setText(self.model.subSystemName)
        
        globalPanel.add(self.subSystemName);
        subSystemIdLabel.setText("Subsystem Id");
        globalPanel.add(subSystemIdLabel);
        self.subSystemId.setText(`self.model.subSystemId`)
        globalPanel.add(self.subSystemId);
        
        self.InternalFrame.getContentPane().add(globalPanel, java.awt.BorderLayout.NORTH);
        
        
        centralPanel.setLayout(java.awt.BorderLayout(15, 15))
        
        levelExportPanel.setLayout( java.awt.GridLayout(6, 1, 5, 5));
        
        levelExportPanel.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createLineBorder( java.awt.Color(0, 0, 0)), "Export level"));

        self.nodeCheckBox.setText("Nodes")
        self.nodeCheckBox.setBorder(javax.swing.BorderFactory.createEmptyBorder(5, 5, 5, 5))
        self.nodeCheckBox.setMargin( java.awt.Insets(0, 0, 0, 0))        
        levelExportPanel.add(self.nodeCheckBox)
        
        self.curveCheckBox.setText("Curves")
        self.curveCheckBox.setBorder(javax.swing.BorderFactory.createEmptyBorder(5, 5, 5, 5))
        self.curveCheckBox.setMargin( java.awt.Insets(0, 0, 0, 0));
        levelExportPanel.add(self.curveCheckBox);
        
        self.surfaceCheckBox.setText("Surfaces");
        self.surfaceCheckBox.setBorder(javax.swing.BorderFactory.createEmptyBorder(15, 15, 15, 15));
        self.surfaceCheckBox.setMargin( java.awt.Insets(0, 0, 0, 0));
        levelExportPanel.add(self.surfaceCheckBox);
        
        centralPanel.add(levelExportPanel, java.awt.BorderLayout.EAST);
        
        objectSettingPanel.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createLineBorder( java.awt.Color(0, 0, 0)), "Object settings"));
        centralPanel.add(objectSettingPanel, java.awt.BorderLayout.CENTER);
        objectSettingPanel.setLayout(java.awt.GridLayout((len(self.model.specificModelParameters.keys())+4), 2, 3, 3))
        
        self.paramField = {}
        keyList = self.model.specificModelParameters.keys()
        keyList.sort()
        for key in keyList:
            label =  javax.swing.JLabel()
            label.setText(key)
            field =  javax.swing.JTextField()
            field.setText(`self.model.specificModelParameters[key]`)
            objectSettingPanel.add(label)
            objectSettingPanel.add(field)
            self.paramField[key] = field
        
        
        
        self.InternalFrame.getContentPane().add(centralPanel, java.awt.BorderLayout.CENTER);
        
        exportPanel.setLayout( java.awt.BorderLayout());
        
        exportButton.setText("Export");
        exportPanel.add(exportButton, java.awt.BorderLayout.EAST);
        
        exportSelectionPanel.setLayout( java.awt.BorderLayout())
        exportSelectionPanel.setBorder(javax.swing.BorderFactory.createEmptyBorder(15, 15, 15, 15))
        
        self.gmshExportSelection.setText("Gmsh (geo)")
        self.gmshExportSelection.setBorder(javax.swing.BorderFactory.createEmptyBorder(5, 5, 5, 5))
        self.gmshExportSelection.setMargin( java.awt.Insets(0, 0, 0, 0))
        self.gmshExportSelection.setSelected(1)
        exportSelectionPanel.add(self.gmshExportSelection, java.awt.BorderLayout.NORTH)
        
        #jCheckBox5.setText("VTK ")
        #jCheckBox5.setBorder(javax.swing.BorderFactory.createEmptyBorder(5, 5, 5, 5))
        #jCheckBox5.setMargin( java.awt.Insets(0, 0, 0, 0))
        #exportSelectionPanel.add(jCheckBox5, java.awt.BorderLayout.SOUTH)
        
        exportPanel.add(exportSelectionPanel, java.awt.BorderLayout.CENTER)
        
        self.InternalFrame.getContentPane().add(exportPanel, java.awt.BorderLayout.SOUTH)
        
        self.InternalFrame.pack()
        
        if sharedFlags['guiMode'] == 1:
            size = self.InternalFrame.getParent().getSize()
            self.InternalFrame.reshape(size.width/3,0,2*size.width/3,size.height-70)
        if sharedFlags['guiMode'] == -1:
            self.InternalFrame.reshape(400,0,400,600)
        
        self.InternalFrame.setVisible(1);
        
        
    def setGeomManagerToUpdate(self, manager):
        self.manager = manager
        
        
    def buildSphere(self, dummy):
        
        self.model.subSystemName = self.subSystemName.getText()
        self.model.subSystemId = string.atoi(self.subSystemId.getText())
        
        keyList = self.paramField.keys()
        for key in keyList:
            self.model.specificModelParameters[key] =  string.atof(self.paramField[key].getText())

        if self.gmshExportSelection.isSelected():
            if self.surfaceCheckBox.isSelected():
                self.model.convertSurfaces()
            elif self.curveCheckBox.isSelected():
                self.model.convertCurves()
            elif self.nodeCheckBox.isSelected():
                self.model.convertNodes()
            else:
                print "No export done"
            #self.model.convertAll()
            self.model.exportToGmsh(os.path.join(GL_EXCHANGE, "Geom", (self.model.subSystemName+".geo")))
            
            self.manager.addNodeOnTree(self.model.subSystemName+".geo")
        self.InternalFrame.dispose()
        
