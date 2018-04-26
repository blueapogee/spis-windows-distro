"""
**File name:**    TaskParaview.py

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

from Bin.Tasks.Task               import Task

import os
import sys
from Bin.config         import GL_SPISUIROOT_PATH, GL_CMD_PARAVIEW, GL_VTK_EXCHANGE

from Bin.Tasks.common            import create_internal_frame
from Bin.Tasks.shared            import shared, sharedFrames, sharedProp

from java.awt          import BorderLayout, GridLayout

from java.awt.event import ItemEvent

from Modules.PostProcessing.Include.paraviewControler import paraviewControler

class TaskParaview(Task):
    '''
    Call the Kitware Paraview for post-processing.
    '''
    desc = "Run Paraview"
    def run_task(self):

        vtkFileList = os.listdir(GL_VTK_EXCHANGE)
        print vtkFileList

        controler = paraviewControler()
        tmpCrtFileName = os.path.join(GL_VTK_EXCHANGE, "prCrt.pvs")
        print tmpCrtFileName
        controler.setOutputfile(tmpCrtFileName)

        manager = managerGUI(create_internal_frame("Paraview Manager",
                             sharedFrames["desktop_pane"]), vtkFileList)
        manager.setPVControler(controler)
        #manager.frame.toFront
        manager.show()



class   managerGUI:
  
    def __init__(self, frame, vtkFileListIn ):

        self.frame  = frame
        self.vtkFileList = vtkFileListIn
        self.selectedDataSet = None
        self.pvControler = None

        self.frame.setSize(300, 300)

        # Build the frame
        self.dataPanel = pawt.swing.JPanel()
        self.dataPanel.setLayout(GridLayout(5,1))
        self.frame.getContentPane().add(self.dataPanel, BorderLayout.CENTER)
  
        # add the various components (list and buttons) 
        self.vtkDataFieldComboBox()
        self.dataPanel.add(self.jComboBox)
        self.jComboBox.itemStateChanged = self.eventListener

        self.setPropBut   =  pawt.swing.JButton('Set Data Properties')
        self.setPropBut.actionPerformed = self.setDataProp
        self.dataPanel.add(self.setPropBut) 

        self.addBut    = pawt.swing.JButton('Add') 
        self.addBut.actionPerformed = self.addData
        self.dataPanel.add(self.addBut)

        self.setViewPropBut = pawt.swing.JButton('Set View Properties')
        self.setViewPropBut.actionPerformed = self.setViewProp
        self.dataPanel.add(self.setViewPropBut)

        self.runBut    = pawt.swing.JButton('Run Paraview')
        self.runBut.actionPerformed = self.runParaview
        self.dataPanel.add(self.runBut) 
        self.frame.pack()
        self.frame.toFront()


    # the events managers
    def eventListener(self,e):
        if e.getStateChange() == e.SELECTED:
            self.selectedDataSet = self.jComboBox.getSelectedItem()
            print self.selectedDataSet


    def vtkDataFieldComboBox(self):
        self.jComboBox = JComboBox()
        self.jComboBox.addItem("No Data")
        if (self.vtkFileList != None):
            for elmTmp in self.vtkFileList:
                self.jComboBox.addItem(elmTmp)

    def setDataProp(self, a):
        self.selectedDS = self.selectedDataSet
        print "We set the prop of" 
        print self.selectedDS


    def setViewProp(self, a):
        print "view settings"
        self.annotationList = []
        self.gbViewSettingDia = viewSettingsDialog(create_internal_frame("Global View Settings",
                                              sharedFrames["desktop_pane"]),
                                              self.annotationList, self)

    def showAnnotationList(self): 
        for annot in self.annotationList:
            self.pvControler.setAnnotations(annot, self.annotationList.index(annot))
            print "annotation: ", annot
        self.pvControler.setAnnotationsVisibility(1)
       

    def addData(self, a):
        if ( self.selectedDataSet != None):
            #self.tmpFileName = os.path.join(GL_VTK_EXCHANGE, self.selectedDataSet)
            self.tmpFileName = GL_VTK_EXCHANGE + self.selectedDataSet
            self.pvControler.addVtkDataSet(self.selectedDataSet, self.tmpFileName, 1, 1)


    def runParaview(self, a):

        self.pvControler.writeSeccionScript()
        print "Control script written"

        print "Launch of Paraview"
        self.cmd = GL_CMD_PARAVIEW+" "+self.pvControler.getOutputfile()+" &"
        #print self.cmd
        #os.system(self.cmd)
        #self.theCaller = ToolCaller(GL_CMD_PARAVIEW)
        #self.theCaller.call('','')
        
        ACTION = GL_CMD_PARAVIEW+" "+self.pvControler.getOutputfile()+" &"
                
        #to execute the CAD tool as fork (not locking) mode
        os.java.lang.Runtime.getRuntime().exec(ACTION)

        
    def setPVControler(self, pvControlerIn):
        self.pvControler = pvControlerIn
        

    def show(self):
        self.frame.show()


class viewSettingsDialog:
    
    def __init__(self, frame, annotationList, theCaller):

        self.Caller = theCaller
        self.annotationList = annotationList
        self.frame = frame
        self.dataPanel = pawt.swing.JPanel()
        self.dataPanel.setLayout(GridLayout(4,2))
        self.frame.getContentPane().add(self.dataPanel, BorderLayout.CENTER)
  

        # to have something at the middle of the desktop
        size = sharedFrames["desktop_pane"].getSize()
        dialogueWidth = 400
        dialogueHeight = 150
        self.frame.setSize(dialogueWidth, dialogueHeight)
        self.frame.reshape((int)(size.getWidth()/2 - dialogueWidth/2), 
                           (int)(size.getHeight()/3 - dialogueHeight/2), 
                           dialogueWidth, dialogueHeight)
        #self.frame.toFront()
        self.frame.setClosable(1)

        self.label = pawt.swing.JLabel("View annotations")
        self.dataPanel.add(self.label)

        self.label2 = pawt.swing.JLabel("")
        self.dataPanel.add(self.label2)

        self.annot0 = pawt.swing.JTextField()
        self.annot1 = pawt.swing.JTextField()
        self.annot2 = pawt.swing.JTextField()
        self.annot3 = pawt.swing.JTextField()

        self.dataPanel.add(self.annot0)
        self.dataPanel.add(self.annot1)
        self.dataPanel.add(self.annot2)
        self.dataPanel.add(self.annot3)

        self.exitBut    = pawt.swing.JButton('Save and Exit')
        self.exitBut.actionPerformed = self.saveAndExit
        self.dataPanel.add(self.exitBut)

        self.frame.toFront()
        self.frame.show()

    def setAnnotationList(self, annotationListIn):
        annotationList = annotationListIn

    def saveAndExit(self, a):

        self.annotationList.append(self.annot0.getText())
        self.annotationList.append(self.annot1.getText())
        self.annotationList.append(self.annot2.getText())
        self.annotationList.append(self.annot3.getText())
        self.Caller.showAnnotationList()
        self.close()
        

    def close(self):
        self.frame.dispose()
