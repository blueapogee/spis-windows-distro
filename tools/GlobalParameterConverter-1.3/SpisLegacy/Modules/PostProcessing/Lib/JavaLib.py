"""
Library for Java wrapping of VTK. 

**Module Name:**  JavaLib

**Project ref:**  Spis/SpisUI

**File name:**    JavaLib.py

**File type:**    Module

:status:          Implemented

**Creation:**     20/11/2003

**Modification:**

**Use:**          A java lib for VTK

**Description:**  This module allows us to use VTK througth Jython.

**References:** Please see the SPIS web site `http://www.spine.org`_ for
more information.

:author:       Pascal Seng

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Pascal Seng               | Definition/Creation        |
|                | seng@artenum.com          |                            |
+----------------+---------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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
.. _`http://www.spine.org`: http://www.spine.org
"""
__docformat__ = "restructuredtext en"

from  java.lang.System import loadLibrary

try:
    loadLibrary("vtkCommonJava")
except:
    print "Error in JavaLib: Impossible to load vtkCommonJava"

try:
    loadLibrary("vtkRenderingJava")
except:
    print "Error in JavaLib: Impossible to load vtkRenderingJava"

try:
    loadLibrary("vtkImagingJava")
except:
    print "Error in JavaLib: Impossible to load vtkImagingJava"

try:
    loadLibrary("vtkIOJava")
except:
    print "Error in JavaLib: Impossible to load vtkIOJava"

try:
    loadLibrary("vtkFilteringJava")
except:
    print "Error in JavaLib: Impossible to load vtkFilteringJava"

try:
    loadLibrary("vtkGraphicsJava")
except:
    print "Error in JavaLib: Impossible to load vtkGraphicsJava"

try:
    loadLibrary("vtkHybridJava")
except:
    print "Error in JavaLib: Impossible to load vtkHybridJava"

try:
    loadLibrary("vtkParallelJava")
except:
    print "Error in JavaLib: Impossible to load vtkParallelJava"

try:
    loadLibrary("vtkWidgetsJava")
except:
    print "Error in JavaLib: Impossible to load vtkWidgetsJava"

