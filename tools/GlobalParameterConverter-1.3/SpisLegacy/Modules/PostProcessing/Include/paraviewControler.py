"""
Call the external tool Paraview for 3D postprocessing. 

**Project ref:**  Spis/SpisUI

**File name:**    paraviewControler.py

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  validation

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

import sys

class paraviewControler:
   '''
   Call the external tool Paraview for 3D postprocessing.
   '''
   def __init__(self):
       print "Initialisation of the paraview controler"
       self.outputFileName =""
       self.vtkDataSetInputList=[]
       self.annotationList=["", "", "", ""]
       self.annotationVisibility = 0

       #just for test
       #self.vtkDataObjectTmp = ("DataField1", "/tmp/julien1086614075/xyz.vtk", 1, 1)
       #self.vtkDataSetInputList.append(self.vtkDataObjectTmp)


   def setOutputfile(self, outputFileNameIn):
       self.outputFileName = outputFileNameIn

   def getOutputfile(self):
       return self.outputFileName
      

   def addVtkDataSet(self, vtkDataSetNameIn, inputVtkFileIn, visibilityIn, scalarBarVisibility):
       self.vtkDataObjectTmp = (vtkDataSetNameIn, inputVtkFileIn, visibilityIn, scalarBarVisibility)
       self.vtkDataSetInputList.append(self.vtkDataObjectTmp)

   def showVtkDataSetList(self):
       for tmpVtkDataSet in self.vtkDataSetInputList:
           print tmpVtkDataSet
       
   def setAnnotations(self, annotationIn, positionIn):
       
       self.annotationList[positionIn] = annotationIn
      
   def setAnnotationsVisibility(self, annotationVisibilityIn):
       self.annotationVisibility = annotationVisibilityIn 

   def writeSeccionScript(self):
       self.fileOut = open(self.outputFileName, "w")

       # generation of the header
       self.fileOut.write("# ParaView State Version 1.4\n")

       # set the main parameters
       self.fileOut.write("set kw(vtkTemp5) [$Application GetMainWindow]\n")
       self.fileOut.write("set kw(vtkTemp19) [$kw(vtkTemp5) GetMainView]\n")
       self.fileOut.write("set kw(vtkTemp166) [$kw(vtkTemp5) GetAnimationInterface]\n")
       self.fileOut.write("[$kw(vtkTemp5) GetRotateCameraButton] SetState 1\n")
       self.fileOut.write("$kw(vtkTemp5) ChangeInteractorStyle 1\n")

       for tmpVtkDataSet in self.vtkDataSetInputList:
           tmpLine1 ='set kw(vtkTemp913) [$kw(vtkTemp5) InitializeReadCustom "legacyreader" "'
           tmpLine1 = tmpLine1 + tmpVtkDataSet[1]+'"]\n'
           self.fileOut.write(tmpLine1)

           tmpLine1 = '$kw(vtkTemp5) ReadFileInformation $kw(vtkTemp913) "'
           tmpLine1 = tmpLine1 + tmpVtkDataSet[1]+'"\n'
           self.fileOut.write(tmpLine1)

           tmpLine1 = '$kw(vtkTemp5) FinalizeRead $kw(vtkTemp913) "'
           tmpLine1 = tmpLine1 + tmpVtkDataSet[1]+'"\n'
           self.fileOut.write(tmpLine1)

           self.fileOut.write('set kw(vtkTemp918) [$kw(vtkTemp913) GetPVWidget {Filename}]\n')

           tmpLine1 = '$kw(vtkTemp918) SetValue "'
           tmpLine1 = tmpLine1 + tmpVtkDataSet[1]+'"\n'
           self.fileOut.write(tmpLine1)

           # set the visibility of the loaded dataField
           self.fileOut.write('$kw(vtkTemp913) AcceptCallback\n')
           self.fileOut.write('set kw(vtkTemp925) [$kw(vtkTemp913) GetPVOutput]\n')
           self.fileOut.write('$kw(vtkTemp925) ColorByPointField {scalars} 3\n')
           self.fileOut.write('$kw(vtkTemp925) DrawSurface\n')
           self.fileOut.write('$kw(vtkTemp925) SetVisibility ')
           self.tmpVar = tmpVtkDataSet[2]
           self.fileOut.write(`self.tmpVar`)
           self.fileOut.write('\n')


           self.fileOut.write('set kw(vtkTemp1032) [$kw(vtkTemp5) GetPVColorMap {scalars} 3]\n')

           # have to be cheked
           #self.fileOut.write('$kw(vtkTemp1032) SetScalarRange 0 17.3205\n')
           #self.fileOut.write('$kw(vtkTemp1032) SetStartHSV 0.6667 1 1\n')
           #self.fileOut.write('$kw(vtkTemp1032) SetEndHSV 0 1 1\n')

           self.fileOut.write('$kw(vtkTemp1032) VectorModeMagnitudeCallback\n')
           self.fileOut.write('$kw(vtkTemp1032) SetScalarBarVisibility ')
           self.tmpVar = tmpVtkDataSet[3]
           self.fileOut.write(`self.tmpVar`)
           self.fileOut.write('\n')

       self.fileOut.write('$kw(vtkTemp19) SetBackgroundColor 0.33 0.35 0.43\n')
       self.fileOut.write('$kw(vtkTemp19) ParallelProjectionOff\n')
       self.fileOut.write('$kw(vtkTemp19) SetCameraState 5 5 39.8564 5 5 5 0 1 0\n')
       self.fileOut.write('$kw(vtkTemp19) SetUseTriangleStrips 0\n')
       self.fileOut.write('$kw(vtkTemp19) SetUseImmediateMode 1\n')
           
       self.fileOut.write('set kw(vtkTemp92) [$kw(vtkTemp19) GetRenderModuleUI]\n')
       self.fileOut.write('catch {$kw(vtkTemp92) SetLODThreshold 5}\n')
       self.fileOut.write('catch {$kw(vtkTemp92) SetLODResolution 50}\n')
       self.fileOut.write('catch {$kw(vtkTemp92) SetOutlineThreshold 5e+06}\n')
       self.fileOut.write('catch {$kw(vtkTemp92) SetRenderInterruptsEnabled 1}\n')

       # loading of the annotations and titles
       self.fileOut.write('set kw(vtkTemp45) [$kw(vtkTemp19) GetCornerAnnotation]\n')
       self.fileOut.write('$kw(vtkTemp45) SetVisibility ' + `self.annotationVisibility`+'\n')
       self.fileOut.write('$kw(vtkTemp45) SetCornerText {' + self.annotationList[0] + '} 0\n')
       self.fileOut.write('$kw(vtkTemp45) SetCornerText {' + self.annotationList[1] + '} 1\n')
       self.fileOut.write('$kw(vtkTemp45) SetCornerText {' + self.annotationList[2] + '} 2\n')
       self.fileOut.write('$kw(vtkTemp45) SetCornerText {' + self.annotationList[3] + '} 3\n')
       self.fileOut.write('$kw(vtkTemp45) SetMaximumLineHeight 0.07\n')

       self.fileOut.write('set kw(vtkTemp61) [$kw(vtkTemp45) GetTextPropertyWidget]\n')
       self.fileOut.write('$kw(vtkTemp61) SetColor 1 1 1\n')
       self.fileOut.write('$kw(vtkTemp61) SetFontFamily 0\n')
       self.fileOut.write('$kw(vtkTemp61) SetBold 0\n')
       self.fileOut.write('$kw(vtkTemp61) SetItalic 0\n')
       self.fileOut.write('$kw(vtkTemp61) SetShadow 0\n')
       self.fileOut.write('$kw(vtkTemp61) SetOpacity 1\n')
       self.fileOut.write('$kw(vtkTemp19) SetOrientationAxesVisibility 0\n')
       self.fileOut.write('$kw(vtkTemp19) SetOrientationAxesInteractivity 1\n')
       self.fileOut.write('$kw(vtkTemp19) SetOrientationAxesOutlineColor 1 1 1\n')

       self.fileOut.write('set kw(vtkTemp229) [$kw(vtkTemp19) GetManipulatorControl2D]\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 0 1 {Roll}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 0 0 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 1 0 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 1 1 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 2 1 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 0 2 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 1 2 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 2 2 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp229) SetCurrentManipulator 2 0 {Zoom}\n')

       self.fileOut.write('set kw(vtkTemp220) [$kw(vtkTemp19) GetManipulatorControl3D]\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 0 2 {FlyIn}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 2 2 {FlyOut}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 0 0 {Rotate}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 1 1 {Rotate}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 1 2 {Rotate}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 0 1 {Roll}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 1 0 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 2 1 {Pan}\n')
       self.fileOut.write('$kw(vtkTemp220) SetCurrentManipulator 2 0 {Zoom}\n')

       self.fileOut.write('set kw(vtkTemp220) [$kw(vtkTemp19) GetManipulatorControl3D]\n')

       self.fileOut.write('set kw(vtkTemp226) [$kw(vtkTemp220) GetWidget {FlySpeed}]\n')
       self.fileOut.write('$kw(vtkTemp226) SetValue 0\n')
       self.fileOut.write('$kw(vtkTemp166) SetNumberOfFrames 100\n')
       self.fileOut.write('$kw(vtkTemp166) SetCurrentTime 0\n')
       self.fileOut.write('$kw(vtkTemp166) SetCacheGeometry 1\n')
       self.fileOut.write('$kw(vtkTemp5) SetCenterOfRotation 5 5 5\n')

       self.fileOut.close()
