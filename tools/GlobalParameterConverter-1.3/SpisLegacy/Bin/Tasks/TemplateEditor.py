"""
**File name:**    TemplateEditor.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais, Julien Forest

:version:      4.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 4.0.0   | Julien Forest                        | Modification               |
|         | julien.forest@artenum.com            |                            |
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

from Bin.Tasks.shared                     import shared, sharedFrames, sharedProp
from Bin.Tasks.common                     import ask_value
from Bin.Tasks.common                     import create_internal_frame
from Bin.Tasks.Task                       import Task

from java.awt                             import BorderLayout

from Modules.Properties.Material          import Material
from Modules.Properties.MaterialList      import MaterialList
from Modules.Properties.Plasma            import Plasma
from Modules.Properties.PlasmaList        import PlasmaList
from Modules.Properties.ElecNode          import ElecNode
from Modules.Properties.ElecNodeList      import ElecNodeList
from Modules.Properties.DataList          import DataList
from Modules.Properties.Data              import Data

import java.awt
import pawt
# import sys
import copy
from copy import deepcopy

from Bin.SwingUtilities.MutableList       import MutableList
from Bin.Tasks.DataEditor                 import DataEditor

from javax.swing                          import BorderFactory
from pawt.swing import JScrollPane
from pawt.swing import JPanel
from pawt.swing import BoxLayout
from pawt.swing import JButton
from pawt.swing import JLabel
from pawt.swing import JTextField
from javax.swing import JComboBox
from javax.swing import DefaultComboBoxModel
from javax.swing import JTextArea

from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory

# FIXME: clean up the 3 following classes

class ParserException(Exception):
    pass

class SelectHandler(pawt.swing.event.ListSelectionListener):
    def __init__(self, editor):
        self.editor = editor

    def valueChanged(self, e):
        lsm = e.getSource()
        iSelected = lsm.getMinSelectionIndex()
        self.editor.selected = iSelected        
        self.editor.refresh(iSelected)

class SelectHandlerData(pawt.swing.event.ListSelectionListener):
    def __init__(self, editor):
        self.editor = editor

    def valueChanged(self, e):
        lsm = e.getSource()
        iSelected = lsm.getMinSelectionIndex()
        self.editor.dataSelected = int(iSelected)

class TextHandler(java.awt.event.KeyAdapter):
    def __init__(self, editor, widget, name):
        self.editor = editor
        self.name   = name
        # text widget implicated
        self.widget = widget

    def keyReleased(self, e):
        try:
            if self.name == "name":
                self.editor.setCurrentName(self.widget)
            elif self.name == "desc":
                self.editor.setCurrentDesc(self.widget)
        except TypeError:
            pass

class TemplateEditor:
    """
    Standard template for properties and data edition.
    """
    def __init__(self, frame):
        """
        Default constructor.
        """
        
        # building of the related logger
        self.logger = LoggerFactory.getLogger("TemplateEditor")
        self.logger.info("TemplateEditor initialised")
        
        # initialise the default property dictionary if this one does not exist 
        if not (sharedProp.has_key('defaultDataList')) or sharedProp['defaultDataList'] == None:
            sharedProp['defaultDataList'] = DataList()

        self.propertyListView = sharedProp['defaultDataList'].List
        self.propertyListViewPrint = [str(i.Id) + "("+ str(i.Name) + ")" for i in sharedProp['defaultDataList'].List]

        if self.templateID == None  \
               or self.templateIDListType == None \
               or self.templateIDType == None \
               or self.templateIDListName == None:
            raise ParserException("You must set self.templateID* before calling TemplateEditor Constructor")

        # initialised an empty property is this one is not in the property list or if it is 
        # equal to None 
        if not (sharedProp.has_key(self.templateID) and sharedProp[self.templateID] != None):
            self.logger.warn("Apparently property list not in shared dictionaries. Created from scratch.")
            exec "sharedProp[self.templateID] = " + self.templateIDListType + "()"
        else:
            self.logger.info("Property list"+str(self.templateID)+" existing and found.")

        # initialisation of the Property list model
        self.PropertyList = sharedProp[self.templateID].List

        self.selected = None
        self.allDataSelected = None
        self.dataSelected = None
        
        #flag to hind the material type in order to force a simple rendering when needed
        self.hideType=0
              
        # Build the frame   
        self.frame  = frame
        
        # Property list view initialisation (left panel)
        tmp = []
        for i in self.PropertyList:
            tmp.append(i.Id)
        
        self.propertyListView = MutableList()
        for i in tmp:
            #print "ADDING PROPERTY: ", i
            self.propertyListView.getContents().addElement(i)
            
        self.propertyListView.setSize(50, self.propertyListView.getHeight())
        self.propertyListViewScroll = JScrollPane(self.propertyListView)
        self.propertyListViewScroll.setPreferredSize(java.awt.Dimension(100, 0))
        
        # buttons for the properties
        self.addBut       = JButton('Add', actionPerformed = self.addGroup)
        self.duplicateBut = JButton('Duplicate', actionPerformed = self.duplicateGroup)
        self.removeBut    = JButton('Remove', actionPerformed = self.removeGroup)
        self.okBut        = JButton('OK', actionPerformed = self.close)
        
        self.buttonPane = JPanel()
        self.buttonPane.setLayout(BoxLayout(self.buttonPane, BoxLayout.X_AXIS))
        self.buttonPane.setBorder(BorderFactory.createTitledBorder("Properties control"))
        
        self.buttonPane.add(self.addBut)
        self.buttonPane.add(self.duplicateBut)
        self.buttonPane.add(self.removeBut)
        self.buttonPane.add(self.okBut)
        
        # data related sub panel
        self.dataPanel = JPanel()
        self.dataPanel.setLayout(BorderLayout());
        self.dataPanel.setBorder(BorderFactory.createLineBorder(java.awt.Color.black))
        
        self.frame.contentPane.add(self.buttonPane, BorderLayout.SOUTH)
        self.frame.contentPane.add(self.propertyListViewScroll, BorderLayout.WEST)
        self.frame.contentPane.add(self.dataPanel, BorderLayout.CENTER)

        # Event handler
        self.propertyListViewHandler = self.propertyListView.getSelectionModel();
        self.propertyListViewHandler.addListSelectionListener(SelectHandler(self))
        
        # top panel (with Name and Description fields)
        self.topPan = JPanel()
        self.topPan.setLayout(BoxLayout(self.topPan, BoxLayout.Y_AXIS))
        
        self.nameLabel = JLabel("Name")
        self.nameInput = JTextField()
        self.topPan.add(self.nameLabel)
        self.topPan.add(self.nameInput)

        self.descLabel = JLabel("Description")
        self.descInput = JTextArea()
        self.descriptionScroll = JScrollPane(self.descInput)
        self.descriptionScroll.setPreferredSize(java.awt.Dimension(200, 100))

        self.topPan.add(self.descLabel)
        self.topPan.add(self.descriptionScroll)
        
        # type panel (with the combo box)
        self.typePanel = JPanel()
        #self.typePanel.setBorder(BorderFactory.createTitledBorder("Linked material"))
        self.typeLabel = JLabel("Type")
        self.typeComboBox = JComboBox()
        self.typeComboBox.setModel(self.initTypeComboBoxModel())
        
        self.typePanel.add(self.typeLabel)
        self.typePanel.add(self.typeComboBox)
        self.topPan.add(self.typePanel)
        
        self.dataPanel.add(self.topPan, BorderLayout.NORTH)


        # Data list management        
        self.listPane  = JPanel()
        self.listPane.setBorder(BorderFactory.createTitledBorder("Data"))
        self.listPane.setLayout(BorderLayout())
        
        self.rightList   = MutableList()
        self.rightListScroll = JScrollPane(self.rightList)
        
        self.toButPane  = JPanel()
        self.toButPane.setLayout(BoxLayout(self.toButPane, BoxLayout.Y_AXIS))
        
        # action relative to the data
        self.toLeftBut  = JButton('Add',actionPerformed = self.addToLeft)
        self.toRightBut = JButton('Remove',actionPerformed = self.removeData)
        self.toModBut   = JButton('Modify', actionPerformed = self.modifyData)
        self.toRefBut   = JButton('Refresh',actionPerformed = self.refreshWrap)
        
        self.toButPane.add(self.toLeftBut)
        self.toButPane.add(self.toModBut)
        self.toButPane.add(self.toRightBut)
        self.toButPane.add(self.toRefBut)
        
        self.listPane.add(self.rightListScroll, BorderLayout.CENTER)
        self.listPane.add(self.toButPane, BorderLayout.EAST)
        
        self.dataPanel.add(self.listPane, BorderLayout.CENTER)
        
        # related property panel
        self.relatedPropertyPanel = JPanel()
        self.relatedPropertyPanel.setBorder(BorderFactory.createTitledBorder("Related Property"))
        
        # initialisation of the combo box used to select the second panel (related propertie) 
        # if the selected property is NASCAP based.
        self.relatedPropComboBox = JComboBox()
        tmpComboBoxModel = self.initRelatedPropComboBox()
        if ( tmpComboBoxModel != None ):
            self.relatedPropComboBox.setModel(tmpComboBoxModel)
            
        self.relatedPropertyPanel.add(self.relatedPropComboBox)
        self.editRelatedPropBut = JButton("Edit", actionPerformed = self.editRelatedProp)
        self.relatedPropertyPanel.add(self.editRelatedPropBut)
        #disable by default: then cannot be used if the selected material is not NSACAP based
        self.relatedPropComboBox.setEnabled(0)
        self.editRelatedPropBut.setEnabled(0)
        
        self.dataPanel.add(self.relatedPropertyPanel, BorderLayout.SOUTH)

        # Event handler
        self.rightListHandler = self.rightList.getSelectionModel();
        self.rightListHandler.addListSelectionListener(SelectHandlerData(self))

        # data list panel
        self.rightListScroll.setPreferredSize(java.awt.Dimension(250, 250))

        # Text listener - reentrance powered
        self.nameInput.addKeyListener(TextHandler(self, self.nameInput,"name"))
        self.descInput.addKeyListener(TextHandler(self, self.descInput,"desc"))
       
        #FIX ME 
        #self.frame.setSize(600, 400)
        #size = self.frame.getParent().getSize()
        #self.frame.setSize(size.width/2,size.height-70);
        
    def initTypeComboBoxModel(self):
        if ( self.propertiesTypeList != None ):
            self.typeComboBoxModel = DefaultComboBoxModel(self.propertiesTypeList)
        else:
            self.typeComboBoxModel = DefaultComboBoxModel(["None"])
        return(self.typeComboBoxModel)


    def initRelatedPropComboBox(self):

        #if ( sharedProp["defaultNascapMaterialList"] != None ):
        #    self.relatedPropList = sharedProp["defaultNascapMaterialList"].List
        if ( self.relatedPropList != None ):
            self.relatedPropNameList = []
            self.relatedPropNameList.append("None")
            for prop in self.relatedPropList:
                self.relatedPropNameList.append(str(prop.Name))
            comboModel = DefaultComboBoxModel(self.relatedPropNameList)
            return(comboModel)
        else:
            return (None)

    def editRelatedProp(self, relatedAction):
        """
        launch a secondary editor for the related properties (i.e NASCAP)
        """
        # the selectedRelatedPropId is defined by the MatTypeId (index 1) in the data list
        selectedRelatedPropId = self.PropertyList[self.selected].DataList.List[1].Value
    
        for item in self.relatedPropList:
            if ( item.Id == selectedRelatedPropId ):
                selectedRelatedPropIndex = self.relatedPropList.index(item)
                break
        
        frame = create_internal_frame("Related Material Properties Editor",sharedFrames["gui"].getCurrentDesktop())
        self.size = frame.getParent().getSize()
        frame.reshape( (self.size.width)/3, 0, (self.size.width)/3, self.size.height)
        
        editor = RelatedMaterialEditor(frame, selectedRelatedPropIndex)
        editor.show()

    def addToLeft(self, e):
        
        if self.propertyListView.isSelectionEmpty():
            return
        tmp = Data()
        self.PropertyList[self.selected].DataList.List.append(tmp)
        self.rightList.getContents().addElement(
            str(tmp.Id) + "("+ str(tmp.Name) + ")")

    def removeData(self, e):
        '''
        Remove the selected data.
        '''
        if self.rightList.isSelectionEmpty():
            self.logger.error("Please select a data to remove.")
            return
        self.PropertyList[self.selected].DataList.List.pop(self.dataSelected)
        self.rightList.getContents().removeElementAt(self.dataSelected)

    def modifyData(self, e):
        '''
        Call the data editor to modify the selected data.
        '''
        if self.dataSelected is not None:
            dataFrame = create_internal_frame("DataEditor",sharedFrames["gui"].getCurrentDesktop())
            dataFrame.setVisible(0);
            dataFrame.reshape( 574, 0, 430, 350) 
         
            editor = DataEditor( dataFrame, self.PropertyList[self.selected].DataList.List[self.dataSelected])
            editor.show()
        else: 
            self.logger.error("Please, select the data to modify.")

    def setCurrentName(self, instance):
        self.PropertyList[self.selected].Name = instance.getText()

    def setCurrentDesc(self, instance):
        self.PropertyList[self.selected].Description = instance.getText()

    def show(self):
        self.frame.show()
        #self.frame.validate()

    def close(self, dummy):
        self.frame.dispose()

    def addGroup(self, dummy):
        
        for i in range(1, len(self.PropertyList) + 2):
            if i in [j.Id for j in self.PropertyList]:
                continue
            else:
                tmpid = i
                break
        exec "self.PropertyList.append(" + self.templateIDType + "(tmpid, " + self.templateIDListName + " = propertyListView()))"
        self.propertyListView.getContents().addElement(tmpid)
        
    def duplicateGroup(self, dummy):
        """
        duplicate the selected group
        """
        #print "duplicate group"
        if self.propertyListView.isSelectionEmpty():
            self.logger.error("Please select a property to duplicate")
            return
        #print self.selected
        #print self.PropertyList[self.selected]
        newGroup = deepcopy(self.PropertyList[self.selected])
        
        maxId = -1
        for item in self.PropertyList:
            if (item.Id > maxId):
                maxId = item.Id
        
        newGroup.Id = maxId + 1
        
        newGroup.Name = newGroup.Name + "-1"
        #print newGroup.Name, newGroup.Id
        
        self.PropertyList.append(newGroup)
        exec "self.PropertyList.append(" + self.templateIDType + "(newGroup.Id, " + self.templateIDListName + " = newGroup.propertyListView ))"
        self.propertyListView.getContents().addElement(newGroup.Id)

    def removeGroup(self, dummy):
        if self.propertyListView.isSelectionEmpty():
            self.logger.error("Please select a property to remove.")
            return
        self.PropertyList.pop(self.selected)
        self.propertyListView.getContents().removeElementAt(self.selected)

    def refreshWrap(self, e):
        self.refresh(self.selected)
        
    def refreshCombobox(self, relatedMatTypeId):
        for relatedItem in self.relatedPropList:
            if ( relatedItem.Id == relatedMatTypeId ):
                tmpSelectedPropName = relatedItem.Name
                break
        self.relatedPropComboBox.setSelectedItem(tmpSelectedPropName)
        

    def refresh(self, i):
        """
        Refresh the data view according to the property selected on the left panel (i.e Property list). 
        This property is identified through the index i. 
        """
        self.nameInput.setText(str(self.PropertyList[i].Name))
        self.descInput.setText(str(self.PropertyList[i].Description))
        
        #print "Selection index i is ;", i
        #print "Material Name is: ", self.PropertyList[i].Name
        #print "Material Id is: ", self.PropertyList[i].Id
        #print "Material type is: ", self.PropertyList[i].Type
        #print "hideType is: ", self.hideType
        
        # management of the combo box
        # the rendering differ depending on the type of data  
        if (self.hideType == 1):
            #print "Type hided"
            self.typeComboBox.setSelectedIndex(0)
            self.relatedPropComboBox.setEnabled(0)
            self.editRelatedPropBut.setEnabled(0)
            
        elif ( self.PropertyList[i].Type == Material.LEGACY_MATERIAL):
            #print "Type is LEGACY"
            self.typeComboBox.setSelectedIndex(1)
            self.relatedPropComboBox.setEnabled(0)
            self.editRelatedPropBut.setEnabled(0)
            
        elif(self.PropertyList[i].Type == Material.NASCAP_MATERIAL):
            #print "Type is NASCAP"
            self.typeComboBox.setSelectedIndex(2)
            self.relatedPropComboBox.setEnabled(0) #FIXME
            # the related material is recovered through the MatTypeId value, stored in 
            # indx 1 in the propertyListView
            self.refreshCombobox(self.PropertyList[i].DataList.List[1].Value)
            self.editRelatedPropBut.setEnabled(1)
            
        elif(self.PropertyList[i].Type == Material.NASCAP_2K_MATERIAL):
            #print "Type is NASCAP 2K"
            self.typeComboBox.setSelectedIndex(3)
            self.relatedPropComboBox.setEnabled(0) #FIXME
            self.refreshCombobox(self.PropertyList[i].DataList.List[1].Value)
            self.editRelatedPropBut.setEnabled(1)
        else:
            # this include the case if self.PropertyList[i].Type == None
            # and/or if hideType == true
            #print "No type"
            self.typeComboBox.setSelectedIndex(0)
            self.relatedPropComboBox.setEnabled(0)
            self.editRelatedPropBut.setEnabled(0)
        
        # update the list of data (right panel)    
        self.rightList.getContents().removeAllElements()
        for j in self.PropertyList[i].DataList.List:
            self.rightList.getContents().addElement(str(j.Id) + "("+ str(j.Name) + ")")
            
class RelatedMaterialEditor(TemplateEditor):
    '''
    Editor of material data. 
    '''
    def __init__(self, frame, selectedProp = None):
        self.templateID = "defaultNascapMaterialList"
        self.templateIDListType = "MaterialList"
        self.templateIDType = "Material"
        self.templateIDListName = "MatDataList"
        self.templateIDPrec = "MatData"
        self.propertiesTypeList =  ["Related Property"]
        self.relatedPropList = None
        
            
        TemplateEditor.__init__(self, frame)
        # in order to avoid a bad refresh of the combo box if the prop reloaded form proejct are
        # considered as nascap.prop
        self.hideType = 1
        
        self.selected = selectedProp
        self.refresh(selectedProp)


