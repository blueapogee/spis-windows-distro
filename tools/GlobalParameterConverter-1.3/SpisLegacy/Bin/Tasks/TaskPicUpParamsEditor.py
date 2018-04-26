"""
**File name:**    TaskMesher.py

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

import java.awt
import pawt
import sys
import shutil

from javax.swing import JTabbedPane

from Bin.Tasks.Task               import Task
from Bin.Tasks.common             import create_internal_frame
from Bin.config                   import GL_DATA_PATH, GL_SPISUIROOT_PATH
from Bin.Tasks.shared             import sharedFrames, sharedGlobals, sharedTasks, sharedGlobalsPicUp

from DefaultValues                import picupGlobalParam

COLUMNS = ["Name", "Description", "Type", "Unit", "Value"]
COMBO_TYPES = ["int", "float", "string"]

class TaskPicUpParamsEditor(Task):
    '''
    Call the gloabl parameter editor for PicUp3D. 
    '''
    desc = "Solver Initialisation"

    def run_task(self):
        '''
        performs the task, i.e opens the global parameter editor.
        '''
        if sharedTasks["context"]!="batch":
            self.frame = create_internal_frame("Global Parameters Editor for PicUp3D",
                                               sharedFrames["desktop_pane"])
            
            self.frame.addInternalFrameListener(InternalCloser(self))
             
            #scan the dic to built the corresponding tables
            self.tableDic={}
            self.pageList={}
            l = []
            
            if sharedGlobalsPicUp == {}:
                importDict = picupGlobalParam.sharedGlobalsPicUp
                
            else:
                importDict = sharedGlobalsPicUp
                
            # Add spacecraft path
            srcPath = GL_SPISUIROOT_PATH + '../ThirdPart/PicUp3D/defaultsat.sc'
            satPath = GL_DATA_PATH + 'defaultsat.sc'
            shutil.copyfile(srcPath , satPath)
            importDict['picup.3d.object.file'] = ['Spacecraft information', 'Spacecraft file definition', 'string', '[-]', satPath]
                    
            keyList = importDict.keys()
            keyList.sort()        
            
            for i in keyList:
                j = importDict[i]
                page = j[0]
                if not self.tableDic.has_key(page):
                    self.tableDic[page]=TableRender()
                    self.tableDic[page].setName(page)
                    self.pageList[page]=[]
                    
            #vieu hake  qui marche pas TBC  
            for page in self.tableDic.keys():
                for i in self.tableDic[page].getData():
                    sharedGlobalsPicUp[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]       
                                       
            self.tabPane = JTabbedPane()
            for page in self.tableDic.keys():
                 self.tabPane.addTab(page, self.tableDic[page])
                 
            self.importBut    = pawt.swing.JButton('Import from SPIS',
                                                actionPerformed = self.importData)
                 
            self.addBut    = pawt.swing.JButton('Add',
                                                actionPerformed = self.add)
            self.removeBut = pawt.swing.JButton('Remove',
                                                actionPerformed = self.remove)
            self.okBut     = pawt.swing.JButton("save and quit",
                                                actionPerformed = self.close)
            self.buttonPane = pawt.swing.JPanel()
            self.buttonPane.setLayout(pawt.swing.BoxLayout(
                self.buttonPane, pawt.swing.BoxLayout.X_AXIS));
                
            self.buttonPane.add(self.importBut)
            self.buttonPane.add(self.addBut)
            self.buttonPane.add(self.removeBut)
            self.buttonPane.add(self.okBut)
            
            self.frame.contentPane.add(self.tabPane, java.awt.BorderLayout.CENTER)
            self.frame.contentPane.add(self.buttonPane, java.awt.BorderLayout.SOUTH)
            self.tabPane.setSelectedIndex(1)
            self.tabPane.setSelectedIndex(0)
    
            keyList = importDict.keys()
            keyList.sort()
            for i in keyList:
                j = importDict[i]
                page = j.pop(0)
                self.pageList[page].append([str(i)]+[str(k) for k in j])
            
            for page in self.tableDic.keys():
                self.tableDic[page].setData(self.pageList[page])
                #self.tableDic[page].refresh()
            
            indexPage = self.tabPane.getSelectedIndex()
            self.frame.pack()
            self.frame.validate()
            self.frame.setVisible(1)        
        
    def importData(self, e):
        '''
        convert and import global parameters from SPIS-NUM settings.
        '''
        print "import"
        
    def add(self, e):
        '''
        add a new field.
        '''
        page = self.tabPane.getComponentAt(self.tabPane.getSelectedIndex()).getName()
        self.tableDic[page].addCell("None", "None", "None", "None", "None")

    def remove(self, e):
        '''
        removes the selected field.
        '''
        page = self.tabPane.getComponentAt(self.tabPane.getSelectedIndex()).getName()
        self.tableDic[page].removeSelectedRow()

    def transtype(self, value, type):
        if type == "string":
            return value
        elif type == "int":
            return int(value)
        elif type == "float":
            return float(value)
        else:
            raise Exception("Invalid type: " + type)

    def close(self, e):
        '''
        Quite the global parameters editor and save the values. 
        '''
        for page in self.tableDic.keys():
            for i in self.tableDic[page].getData():
                sharedGlobalsPicUp[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]

        print " Global parameters saved to shared memory"
        self.frame.dispose()

class InternalCloser(pawt.swing.event.InternalFrameAdapter):
    def __init__(self,parent):
        self.parent = parent
        
    def internalFrameClosing(self,internalFrameEvent):
        self.parent.close(None)


class MyTableModel(pawt.swing.table.AbstractTableModel):
    def __init__(self):
        self.columnNames = COLUMNS
        self.data = []

    def getColumnCount(self):
        return len(self.columnNames)

    def getRowCount(self):
        return len(self.data)

    def getColumnName(self, col):
        return self.columnNames[col]

    def getValueAt(self, row, col):
        return self.data[row][col]

    def getColumnClass(self, c):
        return type(self.getValueAt(0, c))

    def isCellEditable(self, row, col):
        # all cells are editable
        return 1

    def setValueAt(self, value, row, col):
        self.data[row][col] = value
        self.fireTableCellUpdated(row, col)

    def addCell(self, name, desc, type, unit, value):
        self.data.append([name, desc, type, unit, value])
        self.fireTableRowsInserted(self.getRowCount(), self.getRowCount())

    def refresh(self):
        self.fireTableRowsInserted(0, self.getRowCount())

class TableRender(pawt.swing.JPanel):
    def __init__(self):
        pawt.swing.JPanel.__init__(self, java.awt.GridLayout(1,0))
        self.model = MyTableModel()
        self.table = pawt.swing.JTable(self.model)
        self.table.setPreferredScrollableViewportSize(java.awt.Dimension(1004,
                                                                         275))
        self.scrollPane = pawt.swing.JScrollPane(self.table)
        self.setUpTypeColumn(self.table,
                             self.table.getColumnModel().getColumn(2))
        self.add(self.scrollPane)
        self.setOpaque(1)

    def initColumnSizes(self, table):
        self.model = self.table.getModel()

    def setUpTypeColumn(self, table, column):
        self.combo = pawt.swing.JComboBox()
        for i in COMBO_TYPES:
            self.combo.addItem(i)
        column.setCellEditor(pawt.swing.DefaultCellEditor(self.combo))

    def addCell(self, name, desc, type, unit, value):
        self.model.addCell(name, desc, type, unit, value)

    def removeSelectedRow(self):
        s = self.table.getSelectedRow()
        if s == -1:
            print >> sys.stderr, "Select a row to delete"
            return
        del self.model.data[s]
        self.model.fireTableRowsDeleted(s, s)

    def getData(self):
        return self.model.data

    def setData(self, data):
        self.model.data = data

if __name__ == "__main__":
    frame = pawt.swing.JFrame()
    table = TableRender()
    frame.setContentPane(table)
    frame.pack()
    frame.setVisible(1)
    
