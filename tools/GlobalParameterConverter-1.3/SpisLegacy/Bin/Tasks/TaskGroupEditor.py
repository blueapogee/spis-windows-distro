"""
**File name:**    TaskGroupEditor.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
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

import os
from Bin.Tasks.shared                   import shared, sharedFrames, sharedProp, sharedGroups, sharedTasks
from Bin.Tasks.common                   import ask_value
from Bin.Tasks.common                   import create_internal_frame
from Bin.Tasks.Task                     import Task
from Bin.Tasks.shared                   import sharedFrames
from Bin.Tasks.shared                   import sharedFlags

from javax.swing                        import JOptionPane
from java.awt                           import BorderLayout, GridLayout, Color
from javax.swing                        import JCheckBox, JPanel, BoxLayout, Box, JLabel, BorderFactory, JTextField, JScrollPane
from pawt.swing.event                   import ListSelectionListener
from pawt.swing                         import JComboBox, JButton

from Modules.Groups.GeoGroup            import GeoGroup
from Modules.Properties.Material        import Material
from Modules.Properties.ElecNode        import ElecNode
from Modules.Properties.Plasma          import Plasma
from Modules.Properties.DataList        import DataList

from copy import copy

import java.awt
import pawt
import sys
import string

from Bin.SwingUtilities.MutableList     import MutableList

class InitException(Exception):
    pass

class SelectHandler(ListSelectionListener):
    def __init__(self, editor):
        self.editor = editor

    def valueChanged(self, e):
        lsm = e.getSource()
        iSelected = lsm.getMinSelectionIndex()
        self.editor.selected = iSelected
        self.editor.refresh(iSelected)

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
            elif self.name == "border":
                self.editor.setBorderSurface(self.widget)
            elif self.name == "inflate":
                self.editor.setInflate(self.widget)
        except TypeError:
            pass

class ComboHandler(java.awt.event.ActionListener):
    def __init__(self, editor, widget, name):
        self.editor = editor
        self.name   = name
        # text widget implicated
        self.widget = widget

    def actionPerformed(self, e):
        if self.name == "mat":
            self.editor.setCurrentMat(self.widget)
        elif self.name == "elec":
            self.editor.setCurrentElec(self.widget)
        elif self.name == "plasma":
            self.editor.setCurrentPlasma(self.widget)

class GroupEditor:
    '''
    Editor of GEOM groups. This class allows to attribute properties to 
    GEOM groups and to set their priority during the DataField mapping phase.
    '''
    def __init__(self, frame):
        self.frame  = frame
        if not sharedGroups['GeoGroupList']:
            if sharedFlags['guiMode'] == 1:
                InternalFrame = create_internal_frame("Error",sharedFrames["gui"].getCurrentDesktop())
                errorMessage = "<html>No GeoGroup detected, please import a file.</html>"
                toto = JOptionPane.showMessageDialog( InternalFrame, errorMessage, "Error in GroupEditor", JOptionPane.ERROR_MESSAGE)
                raise InitException("")
            else: 
                self.frame.dispose()
                raise InitException("No GeoGroup detected, please import a file")

        # FIXME: Many of the inits MUST NOT BE there... People who
        # FIXME: initialize MaterialList, ElecNodeList and PlasmaList
        # FIXME: MUST integrate a None singleton instance for each of
        # FIXME: these lists. -- Max

        # Inits
        self.GeoGroupList = sharedGroups['GeoGroupList'].List
        
        # material properties
        if sharedProp.has_key('defaultMaterialList') and sharedProp['defaultMaterialList'] != None:
            self.MaterialList = sharedProp['defaultMaterialList'].List
        else:
            self.MaterialList = [Material(MatName="None", MatDataList=DataList())]

        if self.MaterialList == [] or self.MaterialList[0].Name != "None":
            self.MaterialList.insert(0, Material(MatName="None", MatDataList=DataList()))

        # Electrical node properties
        if sharedProp.has_key('defaultElecNodeList') and sharedProp['defaultElecNodeList'] != None:
            self.ElecNodeList = sharedProp['defaultElecNodeList'].List
        else:
            self.ElecNodeList = [ElecNode(ElecName="None", ElecDataList=DataList())]

        if self.ElecNodeList == [] or self.ElecNodeList[0].Name != "None":
            self.ElecNodeList.insert(0, ElecNode(ElecName="None", ElecDataList=DataList()))

        #plasma setting
        if sharedProp.has_key('defaultPlasmaList') and sharedProp['defaultPlasmaList'] != None:
            self.PlasmaList = sharedProp['defaultPlasmaList'].List
        else:
            PlaName = "None"
            PlaDataList = DataList()
            self.PlasmaList = [Plasma(PlaName, PlaDataList)]

        # to add an "empty" plasma model (or None) in the plasma list
        if self.PlasmaList == [] or self.PlasmaList[0].Name != "None":
            self.PlasmaList.insert(0, Plasma(NameIn="None", DataListIn=DataList()))



        self.selected = None
        tmp = []
        for i in self.GeoGroupList:
            tmp.append(i.Id)
            
        # Check box
        self.thinSurf = JCheckBox(actionPerformed = self.setThinSurface);
        self.thinSurf.setText('Thin Surface');
        self.borderSurf = JTextField();
        self.inflate = JTextField();
        self.vtkCheck = JCheckBox(actionPerformed = self.setControlVtkDataset);
        self.vtkCheck.setText('Vtk output');
        
        # Build the frame
        self.dataList = MutableList()
        for i in tmp:
            self.dataList.getContents().addElement(i)
        self.dataList.setSize(50, self.dataList.getHeight())
        self.dataListScroll = JScrollPane(self.dataList)
        self.dataListScroll.setPreferredSize(java.awt.Dimension(100, 0))
        self.dataPanel = JPanel()
        self.dataPanel.setLayout(BoxLayout(
            self.dataPanel, BoxLayout.PAGE_AXIS));
        self.dataPanel.setBorder(BorderFactory.createEmptyBorder(0,5,5,5))
        #self.dataPanel.setBorder(pawt.swing.BorderFactory.createLineBorder(java.awt.Color.black))
        self.addBut    = JButton('Add', actionPerformed = self.addGroup)
        self.removeBut = JButton('Remove',actionPerformed = self.removeGroup)
        self.moveUpBut = JButton('Move Up',actionPerformed = self.moveUpGroup)
        self.moveDownBut = JButton('Move down',actionPerformed = self.moveDownGroup)
        self.splitBut = JButton('Split', actionPerformed = self.splitGroup)
        self.printGeoGrpBut = JButton('Print Geo Grp',actionPerformed = self.printGeoGroup)
        self.printMeshGrpBut = JButton('Print Mesh Grp', actionPerformed = self.printMeshGroup)
        self.okBut     = JButton('OK', actionPerformed = self.close)
        
        self.buttonPane = JPanel()
        #self.buttonPane.setLayout(pawt.swing.BoxLayout(
        #    self.buttonPane, pawt.swing.BoxLayout.X_AXIS));
        self.buttonPane.setLayout(GridLayout(2, 4, 5, 5));
        self.buttonPane.add(self.addBut)
        self.buttonPane.add(self.removeBut)
        self.buttonPane.add(self.moveUpBut)
        self.buttonPane.add(self.moveDownBut)
        self.buttonPane.add(self.splitBut)
        self.buttonPane.add(self.printGeoGrpBut)
        self.buttonPane.add(self.printMeshGrpBut)
        self.buttonPane.add(self.okBut)
        self.buttonPane.setBorder(BorderFactory.createEmptyBorder(5,5,5,5))
        self.dataListScroll.setBorder(BorderFactory.createEmptyBorder(5,5,5,5))
        self.frame.contentPane.add(self.buttonPane, BorderLayout.SOUTH)
        self.frame.contentPane.add(self.dataListScroll, BorderLayout.WEST)
        self.frame.contentPane.add(self.dataPanel, BorderLayout.CENTER)

        # Event handler
        self.dataListHandler = self.dataList.getSelectionModel();
        self.dataListHandler.addListSelectionListener(SelectHandler(self))
        #self.dataList.addActionListener(ComboSelectHandler(self));

        # Right part
        self.nameLabel = JLabel("Name:")
        self.nameInput = pawt.swing.JTextField()
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(self.nameLabel)
        linePanel.add(Box.createHorizontalGlue())
        linePanel.setBorder(BorderFactory.createEmptyBorder(5,0,2,0))
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.nameInput)

        self.descLabel = JLabel("Description:")
        self.descInput = pawt.swing.JTextField()
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(self.descLabel)
        linePanel.add(Box.createHorizontalGlue())        
        linePanel.setBorder(BorderFactory.createEmptyBorder(5,0,2,0))
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.descInput)

        self.matLabel = JLabel("Material:")
        self.matInput = JComboBox()
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(self.matLabel)
        linePanel.add(Box.createHorizontalGlue())
        linePanel.setBorder(BorderFactory.createEmptyBorder(5,0,2,0))
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.matInput)
        #self.initMaterialCombo(self.matInput, self.MaterialList)
        self.init_combo(self.matInput, self.MaterialList)
        
        self.elecLabel = JLabel("ElecNode:")
        self.elecInput = JComboBox()
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(self.elecLabel)
        linePanel.add(Box.createHorizontalGlue())
        linePanel.setBorder(BorderFactory.createEmptyBorder(5,0,2,0))
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.elecInput)
        self.init_combo(self.elecInput, self.ElecNodeList)

        self.plasmaLabel = JLabel("Plasma:")
        self.plasmaInput = JComboBox()
        self.endLabel = JLabel("____")
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(self.plasmaLabel)
        linePanel.add(Box.createHorizontalGlue())        
        linePanel.setBorder(BorderFactory.createEmptyBorder(5,0,2,0))
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.plasmaInput)
        self.dataPanel.add(self.endLabel)
        self.init_combo(self.plasmaInput, self.PlasmaList)
        
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(JLabel('Border:'))
        linePanel.add(Box.createHorizontalGlue())        
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.borderSurf)
        
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(JLabel('Inflate:'))
        linePanel.add(Box.createHorizontalGlue())        
        self.dataPanel.add(linePanel)
        self.dataPanel.add(self.inflate)
        
        linePanel = JPanel()
        linePanel.setLayout(BoxLayout(linePanel,BoxLayout.LINE_AXIS))
        linePanel.add(self.thinSurf)
        linePanel.add(Box.createHorizontalGlue())
        linePanel.add(self.vtkCheck)
        self.dataPanel.add(linePanel)

        self.dataList.setSelectedIndex(0)
        # Text listener - reentrance powered
        self.nameInput.addKeyListener(TextHandler(self, self.nameInput, "name"))
        self.descInput.addKeyListener(TextHandler(self, self.descInput, "desc"))
        self.matInput.addActionListener(ComboHandler(self, self.matInput, "mat"))
        self.elecInput.addActionListener(ComboHandler(self, self.elecInput, "elec"))
        self.plasmaInput.addActionListener(ComboHandler(self, self.plasmaInput, "plasma"))
        self.borderSurf.addKeyListener(TextHandler(self, self.borderSurf, "border"))
        self.inflate.addKeyListener(TextHandler(self, self.inflate, "inflate"))


    def get_instance_from_str(self, list, str):
        for i in list:
            if i.Name == str:
                return i

    def setCurrentName(self, instance):
        self.GeoGroupList[self.selected].Name = instance.getText()

    def setCurrentDesc(self, instance):
        self.GeoGroupList[self.selected].Description = instance.getText()

    def setCurrentMat(self, instance):
       
        #print instance.getSelectedItem() 
        #keyName = instance.getSelectedItem().split("-")[0]
        #print keyName
        
        self.GeoGroupList[self.selected].Material = self.get_instance_from_str(self.MaterialList, instance.getSelectedItem())

    def setCurrentElec(self, instance):
        self.GeoGroupList[self.selected].ElecNode = \
          self.get_instance_from_str(self.ElecNodeList,
                                     instance.getSelectedItem())

    def setThinSurface(self,dummy):
        self.GeoGroupList[self.selected].thin = self.thinSurf.isSelected()

    def setBorderSurface(self,instance):
        tmpValue = instance.getText()
        if not tmpValue == "":
            self.GeoGroupList[self.selected].border = int(tmpValue)

    def setInflate(self,instance):
        tmpValue = instance.getText()
        if not tmpValue == "":
            self.GeoGroupList[self.selected].inflate = float(instance.getText())

    def setControlVtkDataset(self,dummy):
        self.GeoGroupList[self.selected].ctrVtkDataset = self.vtkCheck.isSelected()

    def setCurrentPlasma(self, instance):
        try:
            self.GeoGroupList[self.selected].Plasma = \
                 self.get_instance_from_str(self.PlasmaList, instance.getSelectedItem())
        except TypeError:
            pass

    def updateList(self):            
        
        tmp = []
        for i in self.GeoGroupList:
            tmp.append(i.Id)
        for i in range(len(self.GeoGroupList)):
            self.dataList.getContents().removeElementAt(0)
        for i in tmp:
            self.dataList.getContents().addElement(i)
        
            
    def show(self):
        self.frame.pack()
        self.frame.setVisible(1)
        self.frame.validate()

    def close(self, dummy):
        self.frame.dispose()

	print "Re-set groups conversion"
	sharedTasks["manager"].tasks["GroupManager"].done = 0

    def addGroup(self, dummy):
        
        for i in range(1, len(self.GeoGroupList) + 2):
            if i in [j.Id for j in self.GeoGroupList]:
                continue
            else:
                tmpid = i
                break
        self.GeoGroupList.append(GeoGroup(tmpid))
        self.dataList.getContents().addElement(tmpid)

    def removeGroup(self, dummy):
        if self.dataList.isSelectionEmpty():
            return
        self.GeoGroupList.pop(self.selected)
        self.dataList.getContents().removeElementAt(self.selected)
        
    def moveUpGroup(self, dummy):
        '''
        Increases the priority of the current group.
        '''
        index = copy(self.selected)
        print "selected index", index
        sharedGroups['GeoGroupList'].movUpGroupFromIndex(self.selected)
        self.updateList()
        self.dataList.setSelectedIndex(index-1)
        
    def moveDownGroup(self, dummy):
        '''
        Decreases the priority of the current group.
        '''            
        index = copy(self.selected)
        print "selected index", index
        sharedGroups['GeoGroupList'].movDownGroupFromIndex(self.selected)
        self.updateList()
        self.dataList.setSelectedIndex(index+1)

    def splitGroup(self, dummy):
        '''
        Splits the 3D mesh and duplicates all mesh elements of the 
        current group. This function must be used in case of 2D thin 
        geometric element. This task changes the mesh structure and 
        cannot be undo. The CAD and mesh structure must be reloaded from 
        scratch. for further informtion, please the Technical Note 3.0.
        '''
        print "split group", sharedGroups['GeoGroupList'].List[self.selected].Name

        from TaskMeshSplitter import TaskMeshSplitter
        
        for grp in self.GeoGroupList:
            if grp.thin == 1:
                print "group ", grp.Id, " to be splitted"
                sharedTasks["event_queue"].append("MeshSplitter")
                sharedTasks["context"] = [grp.Id, grp.border, grp.inflate, grp.ctrVtkDataset]
                sharedTasks["caller"] = self
                sharedTasks["event_cond"].signal()
        #self.updateList()
        self.frame.dispose()
        
        
        
    def refresh(self, i):
        self.nameInput.setText(str(self.GeoGroupList[i].Name))
        self.descInput.setText(str(self.GeoGroupList[i].Description))
        try:
            self.matInput.setSelectedItem(self.GeoGroupList[i].Material.Name)
        except AttributeError:
            self.GeoGroupList[i].Material = self.MaterialList[0]
        try:
            self.elecInput.setSelectedItem(self.GeoGroupList[i].ElecNode.Name)
        except AttributeError:
            self.GeoGroupList[i].ElecNode = self.ElecNodeList[0]
        try:
            self.plasmaInput.setSelectedItem(self.GeoGroupList[i].Plasma.Name)
        except AttributeError:
            self.GeoGroupList[i].Plasma = self.PlasmaList[0]
        try:
            self.thinSurf.setSelected(self.GeoGroupList[i].thin)
        except AttributeError:
            self.GeoGroupList[i].thin = 0
            self.thinSurf.setSelected(0)
        try:
            self.borderSurf.setText(`self.GeoGroupList[i].border`)
        except AttributeError:
            self.GeoGroupList[i].border = None
            self.borderSurf.setText('')
        try:
            self.inflate.setText(str(self.GeoGroupList[i].inflate))
        except AttributeError:
            self.GeoGroupList[i].inflate = 0.0
            self.inflate.setText(str(self.GeoGroupList[i].inflate))            
        try:
            self.vtkCheck.setSelected(self.GeoGroupList[i].ctrVtkDataset)
        except AttributeError:
            self.GeoGroupList[i].ctrVtkDataset = 0
            self.vtkCheck.setSelected(0)
            

    #def initMaterialCombo(self,widget, l):
    #    """
    #    Initialise the combo box of material properties
    #    """
    #    for i in l:
    #        #label = JLabel(i.Name)
    #        if (i.Type == Material.LEGACY_MATERIAL):
    #            #label.setBackground(Color.BLUE)
    #            text = i.Name + "- (LEGACY)"
    #        elif (i.Type == Material.NASCAP_MATERIAL or i.Type == Material.NASCAP_2K_MATERIAL):
    #            #label.setBackground(Color.green)
    #            text = i.Name + "- (NASCAP)"
    #        else:
    #            #label.setBackground(Color.white)
    #            text = i.Name
    #        widget.addItem(text)
            

    def init_combo(self, widget, l):
        for i in l:
            widget.addItem(i.Name)
            
    def printGeoGroup(self, dummy):
        print sharedGroups['GeoGroupList'].List[self.selected]
        
    def printMeshGroup(self, dummy):
        if ( not (shared['MeshGroupList'] == None)):
            print shared['MeshGroupList'].List[self.selected]
        else:
            print "Groups not converted yet."

class TaskGroupEditor(Task):
    desc = "Groups editor"
    def run_task(self):
        try:
            frame = create_internal_frame("GroupEditor", sharedFrames["gui"].getCurrentDesktop())
            frame.setSize( 20, 30)
            editor = GroupEditor(frame)
            size = editor.frame.getParent().getSize()
            editor.show()
            editor.frame.reshape(0, 0, size.width/3, size.height)
            print "task GroupEditor is daemonic"
        except InitException, e:
            print >> sys.stderr, e

            
