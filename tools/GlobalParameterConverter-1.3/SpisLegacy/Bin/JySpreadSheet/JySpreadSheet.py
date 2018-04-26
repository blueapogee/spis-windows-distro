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

import java
import javax
#from javax.swing                  import JTabbedPane

import os, shutil, sys

from Bin.Tasks.shared          import sharedFrames
from Bin.Tasks.shared          import sharedTasks
from Bin.Tasks.shared          import sharedFiles
from Bin.Tasks.shared          import sharedFlags

from Bin.Tasks.common          import create_internal_frame
from Bin.exportTemplateControl import exportTemplateControl
from Bin.Tasks.common          import create_internal_frame
from Bin.FrameManager          import FrameManager
from Bin.config                import GL_EXCHANGE, GL_CMD_GMSH, GL_CMD_EDITOR

#from javax.swing               import JOptionPane

import pawt
from pawt                      import swing, colors
from javax.swing               import JProgressBar
from javax.swing               import *
from java.awt                  import *
from java.io                   import File
from java.awt.event            import ItemEvent

from org.spis.imp.ui.util import FileDialog

from threading import Thread

from Bin.Tasks.Task               import Task
from Bin.Tasks.common             import create_internal_frame

from Bin.Tasks.shared             import sharedFrames, sharedGlobals, sharedTasks, sharedCharScales

#from DefaultValues                import picupGlobalParam
#from DefaultValues                import picupGlobalParam

import Bin.JySpreadSheet.ISToDimLessConverter
from Bin.JySpreadSheet.ISToDimLessConverter     import ISToDimLessConverter

COLUMNS_IN = ["Name", "Value", "Unit"]
COLUMNS_OUT = ["Name", "Value", "Expression"]
COMBO_TYPES = ["int", "float", "string"]

class JySpreadSheet:
    desc = "Jython based spread-sheet"

    def __init__(self):
        '''
        performs the task, i.e opens the global parameter editor.
        '''

        # initialisation of the engine.
        self.convert = ISToDimLessConverter()
        self.convert.setBuiltIn()
        self.convert.paramTableIn['Temperature'][0]=1.0
        self.convert.paramTableIn["density"][0]= 1e6
        self.convert.paramTableIn["gridLengthX"][0] = 10.0
        self.convert.paramTableIn["gridLengthY"][0] = 10.0
        self.convert.paramTableIn["gridLengthZ"][0] = 10.0
        self.convert.paramTableIn["gridSizeX"][0] = 10
        self.convert.paramTableIn["gridSizeY"][0] = 10
        self.convert.paramTableIn["gridSizeZ"][0] = 10
        self.convert.paramTableIn["Bfield"][0] = 0.0
       
        self.frameManager = FrameManager()
        self.frameManager.setGuicontext(sharedFlags['guiMode'])
        self.frame = self.frameManager.getNewFrame("Units Converter - Characteristic Scales Editor")
 
        #self.frame = create_internal_frame("Units Converter - Characteristic Scales Editor",
        #                                       sharedFrames["desktop_pane"])
        #self.frame.addInternalFrameListener(InternalCloser(self))
       
        self.menuBar = javax.swing.JMenuBar()
        self.frame.setJMenuBar(self.menuBar)

        fileMenu = javax.swing.JMenu()
        fileMenu.setText("File")
        self.menuBar.add(fileMenu)
        
        saveToDataBusMenuItem = javax.swing.JMenuItem("Save to DataBus", actionPerformed = self.saveToDataBus )
        fileMenu.add(saveToDataBusMenuItem)

        #saveToASCAIIMenuItem = javax.swing.JMenuItem("Save to DataBus", actionPerformed = self.close )
        #fileMenu.add(saveToASCAIIMenuItem)

        exitMenuItem = javax.swing.JMenuItem("Exit", actionPerformed = self.close )
        fileMenu.add(exitMenuItem)

        editMenu = javax.swing.JMenu()
        editMenu.setText("Edit")
        self.menuBar.add(editMenu)

        addInputMenuItem = javax.swing.JMenuItem("Add input", actionPerformed = self.newInputParam)
        editMenu.add(addInputMenuItem)
        
        addOutputMenuItem = javax.swing.JMenuItem("Add output", actionPerformed = self.newOutputParam)
        editMenu.add(addOutputMenuItem)

        removeParameterMenuItem = javax.swing.JMenuItem("Remove Parameter", actionPerformed = self.removeSelectedParam)
        editMenu.add(removeParameterMenuItem)
 
 
 
        # initialisation of the INPUT table
        self.inputTabPane = TableRender(COLUMNS_IN)
        pageList = []
        for key in self.convert.paramTableIn.keys():
            tmpDep = ""
            for dep in self.convert.paramTableIn[key][1]:
                tmpDep = tmpDep+" "+dep+","
            pageList.append([key, `self.convert.paramTableIn[key][0]`, `tmpDep[:-1]`])
        self.inputTabPane.setData(pageList)
        
        #initialisation of the OUTPUT table
        self.outputTabPane = TableRender(COLUMNS_OUT)
        pageList = []
        for key in self.convert.paramTableOut.keys():
            pageList.append([key, self.convert.paramTableOut[key][0], self.convert.paramTableOut[key][1]])
        self.outputTabPane.setData(pageList)
        
        self.tabPane = pawt.swing.JSplitPane(pawt.swing.JSplitPane.HORIZONTAL_SPLIT, self.inputTabPane, self.outputTabPane)
        self.tabPane.setOneTouchExpandable(1)
        self.tabPane.setDividerLocation(0.5)
        
        self.computationThread = ComputationThread()
        self.computationThread.setConvert(self.convert)
        self.computationThread.setOutputTabPane(self.outputTabPane)
        self.computationThread.setInputTabPane(self.inputTabPane)
        
 
        self.computeAllBut = pawt.swing.JButton('Compute',
                             actionPerformed = self.computeAll)        
                                        
        self.saveToDataBusBut = pawt.swing.JButton('Save to DataBus',
                                actionPerformed = self.saveToDataBus)
               
        self.buttonPane = pawt.swing.JPanel()
        self.buttonPane.setLayout(pawt.swing.BoxLayout(self.buttonPane, pawt.swing.BoxLayout.X_AXIS))

        self.buttonPane.add(self.computeAllBut)
        self.buttonPane.add(self.saveToDataBusBut)
        
        self.prgBar = JProgressBar()
        self.convert.setPrgBarLoger(self.prgBar)
        self.buttonPane.add(self.prgBar)
         
        self.frame.contentPane.add(self.tabPane, java.awt.BorderLayout.CENTER)
        self.frame.contentPane.add(self.buttonPane, java.awt.BorderLayout.SOUTH)

        self.frame.pack()
        self.frame.validate()
        self.frame.setVisible(1)
    
    
    def close(self, e):
        '''
        Quite the global parameters editor and save the values. 
        '''
        #for page in self.tableDic.keys():
        #    for i in self.tableDic[page].getData():
        #        sharedGlobalsPicUp[i[0]] = [page, i[1], i[2], i[3], self.transtype(i[4], i[2])]

        #print " Global parameters saved to shared memory"
        self.frame.dispose()    

        
    def refreshView(self):
        
        pageList = []
        for key in self.convert.paramTableIn.keys():
            tmpDep = ""
            for dep in self.convert.paramTableIn[key][1]:
                tmpDep = tmpDep+" "+dep+","
            pageList.append([key, `self.convert.paramTableIn[key][0]`, `tmpDep[:-1]`])
        self.inputTabPane.setData(pageList)
        
        
    def newInputParam(self, e):
        ''' add a new input parameter'''
        print "new input"
        self.inputTabPane.addCell("var name", "value", "unit", None, None)
        self.inputTabPane.model.refresh()
        
        
    def newOutputParam(self, e):
        print "new ouput"
        self.outputTabPane.addCell("var name", "value", "formula", None, None)
        self.outputTabPane.model.refresh()


    def removeSelectedParam(self, e):
        print "remove"
        data = self.outputTabPane.removeSelectedRow()
        if data != None:
            self.convert.removeParamOut(data[0])
            
        data = self.inputTabPane.removeSelectedRow()
        if data != None:
            self.convert.removeParamIn(data[0])
            
        self.outputTabPane.model.refresh()
        self.inputTabPane.model.refresh()
        
        
        
    def computeAll(self, e):
        print "compute"
        
        self.prgBar.setIndeterminate(1)

        keyList = self.convert.paramTableIn.keys()
        for line in self.inputTabPane.getData():
            if line[0] not in keyList:
                self.convert.addParamIn(line[0])
            self.convert.paramTableIn[line[0]][0] = float(line[1])
        
        keyList = self.convert.paramTableOut.keys()
        outputData = self.outputTabPane.getData()
        for line in outputData:
            if line[0] not in keyList:
                self.convert.addParamOut(line[0])
            self.convert.paramTableOut[line[0]][1] = line[2]
        
        self.prgBar.setMaximum(len(keyList))
        
        self.computationThread.run()
        
        
        
    def saveToDataBus(self, e):
        print "Export to DataBus"
        for key in self.convert.paramTableOut.keys():
            sharedCharScales[key] = self.convert.paramTableOut[key][0]
        
        
    def setFromGlobalParams(self):
            
        print "set from Global param"
        
    def saveToASCIIFile(self, e):
        print "Save to ASCII file"
        
    
class InternalCloser(pawt.swing.event.InternalFrameAdapter):
    def __init__(self,parent):
        self.parent = parent
        
    def internalFrameClosing(self,internalFrameEvent):
        self.parent.close(None)
        
        
        
        
class MyTableModel(pawt.swing.table.AbstractTableModel):
    def __init__(self, columnsIn):
        self.columnNames = columnsIn
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
    ''' define the view corresponding to the spreadsheet'''
    
    def __init__(self, columnsIn):
        pawt.swing.JPanel.__init__(self, java.awt.GridLayout(1,0))
        self.model = MyTableModel(columnsIn)
        self.table = pawt.swing.JTable(self.model)
        self.table.setPreferredScrollableViewportSize(java.awt.Dimension(256,
                                                                         256))
        self.scrollPane = pawt.swing.JScrollPane(self.table)
        #self.setUpTypeColumn(self.table,
        #                     self.table.getColumnModel().getColumn(2))
        self.add(self.scrollPane)
        self.setOpaque(1)
        
    def changeSize(self, length, height):
        self.table.setPreferredScrollableViewportSize(java.awt.Dimension(length,
                                                                         height))
        
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
        data = None
        s = self.table.getSelectedRow()
        if s == -1:
            print >> sys.stderr, "Select a row to delete"
            return
        data = self.model.data[s]
        del self.model.data[s]
        self.model.fireTableRowsDeleted(s, s)
        return data
        
    def getSelectedData(self):
        s = self.table.getSelectedRow()
        if s == -1:
            print >> sys.stderr, "Select a row to delete"
            return
        return(self.model.data[s])

    def getData(self):
        return self.model.data

    def setData(self, data):
        self.model.data = data


class ComputationThread(Thread):

    def __init__(self):
        Thread.__init__(self)
         
    def setConvert(self, converter):
        self.convert = converter
        
    def setOutputTabPane(self, outputTabPaneIn):
        self.outputTabPane = outputTabPaneIn
        
    def setInputTabPane(self, inputTabPaneIn):
        self.inputTabPane = inputTabPaneIn
 
    def run(self):
        self.convert.computeDimAllLessValues()
         
        pageList = []
        for key in self.convert.paramTableOut.keys():
            pageList.append([key, self.convert.paramTableOut[key][0], self.convert.paramTableOut[key][1]]) #, self.convert.paramTableOut[key][2]]) 
        self.outputTabPane.setData(pageList)
        
        self.outputTabPane.model.refresh()
        self.inputTabPane.model.refresh()
   
     
class MainSpredSheet:
    '''
    To call the Spread Sheet as standalone application.
    '''

    def usage(self):
        print """%s: usage:
    -h, --help            - print this help message and exit
    -g, --graphical       - run the GUI
    -b FILE, --batch=FILE - run spis in batch mode, set the batch file
    """ % sys.argv[0]

    def main(self):
   
        import Bin.config

        self.spreadSheet = JySpreadSheet()
        #self.geomManager.buildGUI()
   
        closeButton = JButton("Exit", actionPerformed = self.close )
        self.spreadSheet.buttonPane.add(closeButton)
   
        #self.geomManager.show()
   
    def close(self, dummy):
        import sys
        sys.exit()


if __name__ == "__main__":

    from Bin.Tasks.shared         import sharedFlags
    sharedFlags['guiMode'] = -1

    main = MainSpredSheet()
    main.main()