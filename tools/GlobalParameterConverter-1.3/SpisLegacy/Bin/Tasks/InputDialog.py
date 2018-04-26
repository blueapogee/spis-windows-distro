"""
**File name:**    InputDialog.py

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

import pawt
from java.awt           import BorderLayout

from Bin.Tasks.shared             import sharedFrames
from Bin.Tasks.common             import create_internal_frame

class ExitListener(pawt.swing.event.InternalFrameListener):
    def __init__(self, callback_obj):
        self.callback_obj = callback_obj

    def internalFrameActivated(self, e):
        pass

    def internalFrameClosed(self, e):
        self.callback_obj.answer(e)

    def internalFrameClosing(self, e):
        pass

    def internalFrameDeactivated(self, e):
        pass

    def internalFrameDeiconified(self, e):
        pass

    def internalFrameIconified(self, e):
        pass

    def internalFrameOpened(self, e):
        pass

class InputDialog:
    def __init__(self, cond, shared, internal_frame = None):
        self.cond = cond
        self.shared = shared
        self.frame = create_internal_frame("input_dialog", sharedFrames["desktop_pane"])
        #self.frame.setSize(200, 100)

        size = sharedFrames["desktop_pane"].getSize()
        dialogueWidth = 400
        dialogueHeight = 100
        self.frame.setSize(dialogueWidth, dialogueHeight)
        self.frame.reshape( (int)(size.getWidth()/2 - dialogueWidth/2), 
                            (int)(size.getHeight()/3 - dialogueHeight/2), 
                            dialogueWidth, 
                            dialogueHeight)

        # FIXME; freeze all
        # self.frame.addInternalFrameListener(ExitListener(self))
        self.frame.setClosable(0)
        self.text = pawt.swing.JTextField()
        self.label = pawt.swing.JLabel("Enter a value:")
        self.button = pawt.swing.JButton('OK', actionPerformed=self.answer)
        self.frame.contentPane.add(self.button, BorderLayout.SOUTH)
        self.frame.contentPane.add(self.text, BorderLayout.CENTER)
        self.frame.contentPane.add(self.label, BorderLayout.NORTH)
        self.frame.toFront()
        self.frame.show()
        self.frame.validate()

    def answer(self, m):
        self.shared.append(self.text.getText())
        self.cond.acquire()
        self.cond.notifyAll()
        self.cond.release()
        self.frame.dispose()

class YesNoDialog:
    def __init__(self, cond, shared, message, internal_frame = None):
        self.cond = cond
        self.shared = shared
        self.frame = create_internal_frame("input_dialog", sharedFrames["desktop_pane"])
        size = sharedFrames["desktop_pane"].getSize()
        #self.frame.setPosition(200,200)
        dialogueWidth = 400
        dialogueHeight = 100
        self.frame.setSize(dialogueWidth, dialogueHeight)
        self.frame.reshape((int)(size.getWidth()/2 - dialogueWidth/2), (int)(size.getHeight()/3 - dialogueHeight/2), dialogueWidth, dialogueHeight) 
        self.frame.toFront()
        self.frame.setClosable(0)
        self.label = pawt.swing.JLabel(message)
        self.buttonY = pawt.swing.JButton('Yes', actionPerformed=self.answerY)
        self.buttonN = pawt.swing.JButton('No', actionPerformed=self.answerN)
        self.frame.contentPane.add(self.label,   BorderLayout.NORTH)
        self.frame.contentPane.add(self.buttonY, BorderLayout.CENTER)
        self.frame.contentPane.add(self.buttonN, BorderLayout.EAST)
        self.frame.show()
        self.frame.validate()

    def wrap_dispose(self):
        self.cond.acquire()
        self.cond.notifyAll()
        self.cond.release()
        self.frame.dispose()

    def answerY(self, m):
        self.shared.append("y")
        self.wrap_dispose()

    def answerN(self, m):
        self.shared.append("n")
        self.wrap_dispose()
