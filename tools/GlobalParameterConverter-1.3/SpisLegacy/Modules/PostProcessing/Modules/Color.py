"""
**Module Name:**  Color

**Project ref:**  Spis/SpisUI

**File name:**    Color.py

**File type:**    Module

:status:          Implemented

**Creation:**     20/11/2003

**Modification:**

**Use:**          Color to use for VTK actor.

**Description:**  This module return a list of color.

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

import random
from vtk import *
from colorStdTable import colorStdTable

try:
    from Modules.PostProcessing.Lib.JavaLib import *
except:
    print "Error in Color: impossible to load VTK lib."

class Color:

    def __init__(self,num_color=None):
        
        self.Color=[]
        self.num_color = num_color

    def ColorsBySteps(self):	
        stdcol = colorStdTable()
        for i in range(self.num_color):
            #lcolor = colorStdTable.GetColorListLength()
            #colorId = rnd()*lcolor
            #color = colorStdTable.GetColor(colorId)
            listTmp = stdcol.colorsList
            colorName = random.choice(listTmp)
            listTmp.remove(colorName)
            color = stdcol.colorsDic[colorName]
            print 'Color', i, 'is ', colorName, 'as follow', color
            self.Color.append(color)
			
    def ContiniousColors(self):
        for i in range(self.num_color):
            color=[1.0-i*1.0/self.num_color,0.0, 1.0+i*1.0/self.num_color]
            self.Color.append(color)
