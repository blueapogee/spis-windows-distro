"""
**File name:**    TaskMaterial.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 3.1.0   | Yves Le Rumeur                       | Modif                      |
|         | lerumeur@artenum.com                 |                            |
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

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import sharedProp, sharedFrames
from Bin.Tasks.shared         import addElementToSharedList
from Bin.Tasks.shared import sharedFlags
from Bin.MaterialMaker        import *

from Bin.Tasks.common                     import create_internal_frame
from Bin.Tasks.TaskImportNascapMaterial import NascapCatalogLoader

from javax.swing                          import BorderFactory
from pawt.swing import JScrollPane
from pawt.swing import JPanel
from pawt.swing import BoxLayout
from java.awt import GridLayout 
from pawt.swing import JButton
from pawt.swing import JLabel
from pawt.swing import JTextField
from javax.swing import JComboBox
from javax.swing import DefaultComboBoxModel
from javax.swing import JTextArea
from javax.swing import JCheckBox
from java.awt import Dimension
from javax.swing              import JOptionPane



class TaskMaterial(Task):
    """Call the Material properties editor."""
    desc = "Task of definition of materials properties"
    
    def run_task(self):
        self.buildUserInterface()
        
    def buildUserInterface(self):
        
        self.frame = create_internal_frame("Properties Catalogs Loader",sharedFrames["gui"].getCurrentDesktop())
        self.size = self.frame.getParent().getSize()
        
        self.frame.reshape( 0, 0, (self.size.width)/3, self.size.height)
        frameSize = self.frame.getSize()
        
        mainPanel = JPanel()
        mainPanel.setLayout(BoxLayout(mainPanel, BoxLayout.Y_AXIS))
        
        # materials sub-panel
        materialPanel = JPanel()
        materialPanel.setPreferredSize( Dimension(frameSize.width, frameSize.height/4))
        materialPanel.setLayout(GridLayout(2,1))
        materialPanel.setBorder(BorderFactory.createTitledBorder("Materials"))
        
        self.defaultPropChckBox = JCheckBox("Default built-in materials")
        self.defaultPropChckBox.setSelected(1)
        materialPanel.add(self.defaultPropChckBox)
        self.nascapPropChckBox = JCheckBox("Ext. NASCAP based materials")
        materialPanel.add(self.nascapPropChckBox)
        
        mainPanel.add(materialPanel)

        # electrical node sub-panel
        elecNodePanel = JPanel()
        elecNodePanel.setPreferredSize( Dimension(frameSize.width, frameSize.height/4))
        elecNodePanel.setBorder(BorderFactory.createTitledBorder("Electrical Nodes Models"))
        elecNodePanel.setLayout(GridLayout(2,1))
        
        self.elecNodeChckBox = JCheckBox("Electrical nodes models")
        self.elecNodeChckBox.setSelected(1)
        elecNodePanel.add(self.elecNodeChckBox)
        
        mainPanel.add(elecNodePanel)
        
        # plasma sub-panel
        plasmaPanel = JPanel()
        plasmaPanel.setPreferredSize( Dimension(frameSize.width, frameSize.height/4))
        plasmaPanel.setLayout(GridLayout(2,1))
        plasmaPanel.setBorder(BorderFactory.createTitledBorder("Plasma Models"))
        
        self.plasmaModelsChckBox = JCheckBox("Plasma Models")
        self.plasmaModelsChckBox.setSelected(1)
        plasmaPanel.add(self.plasmaModelsChckBox)
        
        mainPanel.add(plasmaPanel)
        
        buttonsPanel = JPanel()
        buttonsPanel.setLayout(BoxLayout(buttonsPanel, BoxLayout.X_AXIS))
        
        resetButton = JButton("Reset", actionPerformed = self.resetAction)
        resetButton.setToolTipText("Reset all shared properties catalogs")
        buttonsPanel.add(resetButton)
        
        escButton = JButton("Esc", actionPerformed = self.escAction)
        buttonsPanel.add(escButton)
        
        loadButton = JButton("Load", actionPerformed = self.loadAction)
        buttonsPanel.add(loadButton)
        
        mainPanel.add(buttonsPanel)
        
        self.frame.getContentPane().add(mainPanel);
        
        self.frame.show()
    
    def resetAction(self, dummy):
        print "reset"
        
        if sharedFlags['guiMode'] == 1:
                InternalFrame = create_internal_frame("Warning",sharedFrames["gui"].getCurrentDesktop())
                dialogueMessage = "<html>Do you really want to reset all shared properties catalogs?</html>"
                response = JOptionPane.showConfirmDialog( InternalFrame, dialogueMessage, "Reset Properties", JOptionPane.YES_NO_OPTION)
        if(response == 0):
            sharedProp['defaultMaterialList'] = None
            sharedProp['defaultPlasmaList'] = None
            sharedProp['defaultElecNodeList'] = None
            sharedProp['materialProp'] = None
            print "All properties reset"
            self.frame.dispose()
            self = None
        
    def escAction(self, dummy):
        #print "esc"
        self.frame.dispose()
        self = None
        
    def loadAction(self, dummy):
        #print "load"
        self.buildCatalogs()
        
    def buildCatalogs(self):
        # call the default SPIS material maker
        materials = MaterialMaker()
        
        # build-up the default materiail and properties listes. If these ones are not pre-existing, their are created from scratch. 
        # If they are pre-existing, they are concatenated. 
        
        if self.defaultPropChckBox.isSelected():
            print "Default properties selected and loaded"
            if sharedProp.has_key('defaultMaterialList') == 0:
                sharedProp['defaultMaterialList'] = None
            sharedProp['defaultMaterialList'] = addElementToSharedList(sharedProp['defaultMaterialList'], materials.BuildDefaultMaterialList()) 
       
        if self.plasmaModelsChckBox.isSelected():
            print "Plasma models selected and loaded"
            if sharedProp.has_key('defaultPlasmaList') == 0:
                sharedProp['defaultPlasmaList'] = None
            sharedProp['defaultPlasmaList']   = addElementToSharedList(sharedProp['defaultPlasmaList'], materials.BuildDefaultPlasmaList()) 
        
        if self.elecNodeChckBox.isSelected():
            print "Electrical node models selected and loaded"
            if sharedProp.has_key('defaultElecNodeList') == 0:
                sharedProp['defaultElecNodeList'] = None
            sharedProp['defaultElecNodeList'] = addElementToSharedList(sharedProp['defaultElecNodeList'], materials.BuildDefaultElecNodeList())
        
        if self.nascapPropChckBox.isSelected():
            print "Nascap based material models selected"
            loader = NascapCatalogLoader()
            loader.loadCatalog()
            
        print "Catalogs loaded"
        self.frame.dispose()
        self = None
