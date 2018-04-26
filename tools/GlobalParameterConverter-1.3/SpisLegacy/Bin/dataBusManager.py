"""
Module of managment and cleanning of the common DataBus of SPIS-UI.

**Project ref:**  Spis/SpisUI

**File name:**    dataBusManager.py

:status:          Implemented

**Creation:**     4/05/2006

**Modification:** 27/08/2006  validation

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


from Bin.Tasks.common             import *
import Bin.Tasks.shared
from Bin.Tasks.shared import *

from java.awt.event import ActionEvent
from java.awt.event import ActionListener

from org.spis.imp.ui.shared import DataBusCleaner

import java
import pawt
import javax.swing
from java.awt.event    import ItemEvent
from java.awt          import BorderLayout, GridLayout



class dataBusManager(ActionListener):
    '''
    Module of managment and cleanning of the common DataBus of SPIS-UI.
    '''    
    def __init__(self):
        '''
        Default constructor. 
        '''            
        self.frame = create_internal_frame("Data Bus Cleaner", sharedFrames["gui"].getCurrentDesktop())

        self.dbc = DataBusCleaner()
        self.dbc.setActionListener(self)
        self.frame.contentPane.add( self.dbc, BorderLayout.CENTER)
        
        self.keyFieldTab = []
        listDic = dir(Bin.Tasks.shared)
        for dico in listDic:
            self.tmpKeyList = None
            try:
                cmdTmp = "self.tmpKeyList ="+dico+".keys()"
                exec(cmdTmp)
            except:
                print "Not a dictionnary"
            #print self.listKey
            field = "Field"
            if self.tmpKeyList != None and self.tmpKeyList != []:
                for key in self.tmpKeyList: 
                    self.keyFieldTab.append([dico,key, field])
            
        for index in xrange(len(self.keyFieldTab)):
            self.dbc.registerShared(self.keyFieldTab[index][0], self.keyFieldTab[index][2], self.keyFieldTab[index][1], self.keyFieldTab[index][1])
        
        self.size = self.frame.getParent().getSize()
        self.frame.reshape(0, 0, self.size.width/3, self.size.height)
        self.frame.setVisible(1)
        

        
    def actionPerformed(self, ae):
       actionName = ae.getActionCommand() 

       selectedKeys = self.dbc.getShared().get(self.dbc.getSelectedShared()).getSelectedKeys()
       selectedDic = self.dbc.getShared().get(self.dbc.getSelectedShared()).getName() 
       
       for key in selectedKeys:
           if key == "Name":
               cmdTmp = "Bin.Tasks.shared."+selectedDic+"['"+key+"'] =default"
           elif key == 'TheProjectFileIn':
               cmdTmp = "Bin.Tasks.shared."+selectedDic+"['"+key+"'] =proj.spis"
           elif key == 'TheProjectFileOut':
               cmdTmp = "Bin.Tasks.shared."+selectedDic+"['"+key+"'] =proj.spis"
           elif key == 'projetLoadingFlag': 
               cmdTmp = "Bin.Tasks.shared."+selectedDic+"['"+key+"'] =0"
           else:
               cmdTmp = "Bin.Tasks.shared."+selectedDic+"['"+key+"'] =  None"
           print cmdTmp
           exec(cmdTmp)
       self.frame.dispose()
       self.frame = None
       self = None
       
