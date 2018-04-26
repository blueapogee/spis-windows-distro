"""
**File name:**    TaskJyTop.py

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
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedNum
from Bin.Tasks.common         import ask_value
from Bin.Tasks.shared         import sharedSolver
from Bin.Tasks.shared         import sharedFrames

import javax.swing 
from javax.swing              import JFrame
from javax.swing              import JDialog
from javax.swing              import JLabel
from javax.swing              import JButton
from javax.swing              import JPanel
import java.awt
from java.awt import BorderLayout
from javax.swing import BorderFactory

import sys
sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)


class TaskAbout(Task):
    """Task JyTop: Jython wrapping of SPIS-NUM. See technical information 
    for more details.
    """
    desc = "Solver wrapping module (JyTop for SpisNum)"
    
    def run_task(self):
        '''
        Performs the task.
        '''
        self.showDialog()
        
        
    def showDialog(self):
        frame = sharedFrames["gui"].getFrames()[0]
        self.dia = JDialog( frame, "About", 0)
        self.dia.setLayout(BorderLayout())
        text = "<html><br>SPIS, Spacecraft Plasma Interaction System.<br>"
        text = text+'  See <a href="http://www.spis.org">http://www.spis.org</a> for further informations.<br>'
        text = text+"<br>    SPIS-NUM 4.0.00 RC 01, Numerical core, 2009/07/20, FRANCE<br>"
        text = text+"        Copyright (c) ONERA, 2 av E.Belin, TOULOUSE, FRANCE<br>"
        text = text+'     2002, 2003, 2004, Toulouse, France, <a href="http://www.onera.fr">http://www.onera.fr</a><br><br>'
        text = text+"    SPIS-UI 4.2.00 RC 01, Modelling framework, 2009/07/20, FRANCE<BR>"
        text = text+"        Copyright (c) Artenum SARL, 24, rue Louis Blanc, 75010, PARIS <br>"
        text = text+'        2000-2006, Paris, France, <a href="http://www.artenum.com">http://www.artenum.com</a><br> </html>'
        
        textLabel = JLabel(text)
        textLabel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10))
        closeButton = JButton("OK", actionPerformed = self.closeAction)
        tmpBottomPanel = JPanel()
        tmpBottomPanel.add(closeButton)
        self.dia.getContentPane().add(textLabel,BorderLayout.CENTER)
        self.dia.getContentPane().add(tmpBottomPanel,BorderLayout.SOUTH)
        self.dia.setSize(500, 280)
        self.dia.setLocationRelativeTo(None)
        self.dia.show()
        
    def closeAction(self, dummy):
        self.dia.dispose()
        self.dia = None
