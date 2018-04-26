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
import traceback
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory

from javax.swing import JTabbedPane

from Bin.Tasks.Task               import Task
from Bin.Tasks.common             import create_internal_frame
from Bin.Tasks.shared             import sharedFrames, sharedGlobals, sharedTasks, sharedFlags
from DefaultValues                import defaultGlobalParam
from copy import *

from org.spis.imp.ui.util         import FileDialog

COLUMNS = ["Name", "Description", "Type", "Unit", "Value"]
COMBO_TYPES = ["int", "float", "string"]

class TaskParamsEditor(Task):
    '''
    Call the global parameter editor. 
    '''
    desc = "Call the editor of global parameters"

    def run_task(self):
        '''
        performs the task, i.e opens the global parameter editor.
        '''
        
        self.logger = LoggerFactory.getLogger("Task")
        
        if (sharedTasks["context"]!="batch" and sharedFlags['guiMode'] == 1):
            self.frame = create_internal_frame("Global Parameters Editor", sharedFrames["gui"].getCurrentDesktop())
            
            # call to the right internal frame closing method to avoid 
            # make a mess in the table index.
            self.frame.addInternalFrameListener(InternalCloser(self))

            #scan the dic to built the corresponding tables
            self.tableDic={}
            self.pageList={}
            importDict = None
            if sharedGlobals == {}:
                # we perform a deepcopy to avoid a corruption of default values
                importDict = deepcopy(defaultGlobalParam.sharedGlobals)
            else:
                importDict = deepcopy(sharedGlobals)
                
            keyList = importDict.keys()
            keyList.sort()

            for i in keyList:
                indexName = importDict[i][0]
                if not self.tableDic.has_key(indexName):
                    self.tableDic[indexName]=TableRender()
                    self.tableDic[indexName].setName(indexName)
                    self.pageList[indexName]=[]
                                             
            self.tabPane = JTabbedPane()
            for indexName in self.tableDic.keys():
                self.tabPane.addTab(indexName, self.tableDic[indexName])
                 
            self.addBut       = pawt.swing.JButton('Add',actionPerformed = self.add)
            self.removeBut    = pawt.swing.JButton('Remove',actionPerformed = self.remove)
            self.exportCSVBut = pawt.swing.JButton('Export all to CSV', actionPerformed = self.exportToCSVFile)
            self.okBut        = pawt.swing.JButton("save and quit", actionPerformed = self.close)
            self.buttonPane = pawt.swing.JPanel()
            self.buttonPane.setLayout(pawt.swing.BoxLayout(self.buttonPane, pawt.swing.BoxLayout.X_AXIS));
            self.buttonPane.add(self.addBut)
            self.buttonPane.add(self.removeBut)
            self.buttonPane.add(self.exportCSVBut)
            self.buttonPane.add(self.okBut)
            
            if sharedFlags['guiMode'] == 1:
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
            if sharedFlags['guiMode'] == 1:
                self.frame.pack()
                self.frame.validate()
                size = self.frame.getParent().getSize()
                #self.frame.show()
                self.frame.reshape(0, 0, size.width, size.height)
                self.frame.setVisible(1)        
        
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

    def exportToCSVFile(self, e):
        
        fsd = FileDialog( )
        #fsd.addFileType(".csv")
        if ( fsd.showOpenDialog(None) ):   #None should set to the parent component
            selectedFile = fsd.getSelectedFileAsString() 
            #self.importer.loadFile(selectedFile)
            self.logger.debug(selectedFile)
            
            try: 
                self.saveToDataBus()
                self.logger.info("Global parameters saved to shared memory")
            except:
                self.logger.error("Error ! Impossible to save the global parameters. This is probably due to:\n"
                              +" - a misspelling (e.g comma in place of a decimal point)\n"
                              +" - a inconsistency between the value of a parameter and its types \n"
                              +" (e.g char as float) leading to a transtyping error.\n"
                              +"Please check and save again.")
                return() # to exit of the method in case of problem.
            
            colSep = "; "
            try:
                exportedFile = open(selectedFile, "w")
                for key in sharedGlobals.keys():
                    elm = sharedGlobals[key]
                    exportedFile.write (key + colSep + str(elm[0]) + colSep + str(elm[1]) + colSep + str(elm[2]) +colSep + str(elm[3]) + colSep + str(elm[4])+ " \n ")
                exportedFile.close()
                self.logger.info("Done")
            except:
                self.logger.error("Error in export to CSV file format.")
                

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
        Quit the global parameters editor and save the values. 
        '''
        #tmpDic = {}
        try:
            #for page in self.tableDic.keys():
            #    for i in self.tableDic[page].getData():
            #        #print i[1], i[2], i[3], i[4], i[2]
            #        sharedGlobals[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]
            #        tmpDic[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]
            
            self.saveToDataBus()
            
            self.frame.dispose()
            self.tableDic = None
            self.pageList = None
            self.logger.info("Global parameters saved to shared memory")
        except:
            self.logger.error("Error ! Impossible to save the global parameters. This is probably due to:\n"
                              +" - a misspelling (e.g comma in place of a decimal point)\n"
                              +" - a inconsistency between the value of a parameter and its types \n"
                              +" (e.g char as float) leading to a transtyping error.\n"
                              +"Please check and save again.")

    def saveToDataBus(self):
        """
        should be catch by an exception handled
        """
        tmpDic = {}
        for page in self.tableDic.keys():
            for i in self.tableDic[page].getData():
                #print i[1], i[2], i[3], i[4], i[2]
                sharedGlobals[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]
                tmpDic[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]

class InternalCloser(pawt.swing.event.InternalFrameAdapter):
    '''
    Internal closing method to keep a right ordering in the table indexes.
    '''
    def __init__(self,parent):
        self.parent = parent
        
    def internalFrameClosing(self,internalFrameEvent):
        #print "Call to the closing method"
        self.parent.close(None)



class MyTableModel(pawt.swing.table.AbstractTableModel):
    '''
    model for the global parameters table.
    '''
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
        self.logger = LoggerFactory.getLogger("Task")
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
            self.logger.error("Select a row to delete")
            return
        del self.model.data[s]
        self.model.fireTableRowsDeleted(s, s)

    def getData(self):
        return self.model.data

    def setData(self, data):
        self.model.data = data

if __name__ == "__main__":
    '''
    To run the global parameter editor as stand alone application.
    '''
    frame = pawt.swing.JFrame()
    table = TableRender()
    frame.setContentPane(table)
    frame.pack()
    frame.setVisible(1)
    
