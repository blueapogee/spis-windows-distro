"""
**File name:**    DataEditor.py

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


from Bin.Tasks.shared             import shared, sharedFrames, sharedProp
from Bin.Tasks.common             import create_internal_frame
from Bin.Tasks.Task               import Task

from java.awt           import BorderLayout

from Modules.Properties.Data              import Data
from Modules.Properties.DataList          import DataList

import java.awt
import pawt
import sys

from Bin.SwingUtilities.MutableList     import MutableList

class SelectHandler(pawt.swing.event.ListSelectionListener):
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
            elif self.name == "type":
                self.editor.setCurrentType(self.widget)
            elif self.name == "desc":
                self.editor.setCurrentDesc(self.widget)
            elif self.name == "unit":
                self.editor.setCurrentUnit(self.widget)
            elif self.name == "local":
                self.editor.setCurrentLocal(self.widget)
            elif self.name == "value":
                self.editor.setCurrentValue(self.widget)
            elif self.name == "id":
                self.editor.setCurrentId(self.widget)
        except TypeError, e:
            pass

class DataEditor:
    def __init__(self, frame, data_to_edit):
        self.data_to_edit = data_to_edit

        self.frame  = frame
        # Build the frame
        self.dataPanel = pawt.swing.JPanel()
        self.dataPanel.setLayout(pawt.swing.BoxLayout(
            self.dataPanel, pawt.swing.BoxLayout.Y_AXIS));
        self.dataPanel.setBorder(
            pawt.swing.BorderFactory.createLineBorder(java.awt.Color.black))
        self.okBut     = pawt.swing.JButton('OK', actionPerformed = self.close)
        self.buttonPane = pawt.swing.JPanel()
        self.buttonPane.setLayout(pawt.swing.BoxLayout(
            self.buttonPane, pawt.swing.BoxLayout.X_AXIS));
        self.buttonPane.add(self.okBut)
        self.frame.contentPane.add(self.buttonPane, BorderLayout.SOUTH)
        self.frame.contentPane.add(self.dataPanel, BorderLayout.CENTER)

        # Right part
        self.idLabel = pawt.swing.JLabel("Id")
        self.idInput = pawt.swing.JTextField()
        self.dataPanel.add(self.idLabel)
        self.dataPanel.add(self.idInput)

        self.nameLabel = pawt.swing.JLabel("Name")
        self.nameInput = pawt.swing.JTextField()
        self.dataPanel.add(self.nameLabel)
        self.dataPanel.add(self.nameInput)

        self.typeLabel = pawt.swing.JLabel("Type")
        self.typeInput = pawt.swing.JTextField()
        self.dataPanel.add(self.typeLabel)
        self.dataPanel.add(self.typeInput)

        self.descLabel = pawt.swing.JLabel("Description")
        self.descInput = pawt.swing.JTextField()
        self.dataPanel.add(self.descLabel)
        self.dataPanel.add(self.descInput)

        self.unitLabel = pawt.swing.JLabel("Unit")
        self.unitInput = pawt.swing.JTextField()
        self.dataPanel.add(self.unitLabel)
        self.dataPanel.add(self.unitInput)

        self.localLabel = pawt.swing.JLabel("Local")
        self.localInput = pawt.swing.JTextField()
        self.dataPanel.add(self.localLabel)
        self.dataPanel.add(self.localInput)

        self.valueLabel = pawt.swing.JLabel("Value")
        self.valueInput = pawt.swing.JTextField()
        self.dataPanel.add(self.valueLabel)
        self.dataPanel.add(self.valueInput)

        # Text listener - reentrance powered
        self.idInput.addKeyListener(TextHandler(self, self.idInput,
                                                "id"))
        self.nameInput.addKeyListener(TextHandler(self, self.nameInput,
                                                  "name"))
        self.typeInput.addKeyListener(TextHandler(self, self.typeInput,
                                                  "type"))
        self.descInput.addKeyListener(TextHandler(self, self.descInput,
                                                  "desc"))
        self.unitInput.addKeyListener(TextHandler(self, self.unitInput,
                                                  "unit"))
        self.localInput.addKeyListener(TextHandler(self, self.localInput,
                                                  "local"))
        self.valueInput.addKeyListener(TextHandler(self, self.valueInput,
                                                  "value"))
        self.refresh()

    def setCurrentName(self, instance):
        self.data_to_edit.Name = instance.getText()

    def setCurrentType(self, instance):
        self.data_to_edit.Type = instance.getText()

    def setCurrentDesc(self, instance):
        self.data_to_edit.Description = instance.getText()

    def setCurrentUnit(self, instance):
        self.data_to_edit.Unit = instance.getText()

    def setCurrentLocal(self, instance):
        self.data_to_edit.Local = instance.getText()

    def setCurrentValue(self, instance):
        exec "self.data_to_edit.Value = " + instance.getText()

    def setCurrentId(self, instance):
        self.data_to_edit.Id = int(instance.getText())

    def show(self):
        
        self.frame.show()
        self.frame.validate()

    def close(self, dummy):
        self.frame.dispose()

    def refresh(self):
        self.idInput.setText(str(self.data_to_edit.Id))
        self.nameInput.setText(str(self.data_to_edit.Name))
        self.typeInput.setText(str(self.data_to_edit.Type))
        self.descInput.setText(str(self.data_to_edit.Description))
        self.unitInput.setText(str(self.data_to_edit.Unit))
        self.localInput.setText(str(self.data_to_edit.Local))
        self.valueInput.setText(str(self.data_to_edit.Value))
