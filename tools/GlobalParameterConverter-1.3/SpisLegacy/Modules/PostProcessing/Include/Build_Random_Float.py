"""
**Module Name:**  Build_Random_Float

**Project ref:**  Spis/SpisUI

**File name:**    Build_Random_Float.py

**File type:**    Module

:status:          Implemented

**Creation:**     27/11/2003

**Modification:**

**Use:**          Number of float attached to points for VTK visualization.

**Description:**  This module return an array of float for VTK points.

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


from vtk import *

class Build_Random_Float:
	def __init__(self):
		from PostProcessing.Lib.JavaLib import *
		self.float_array=vtkDoubleArray()
		self.math=vtkMath()

	def Build_Array_Iso(self,num_point,dim):
		for j in range(num_point):
			thefloat=self.math.Random(0, 1)
			for i in range(dim):
				self.float_array.InsertNextValue(thefloat)
		return self.float_array

	def Build_Array(self,num_point,dim):
		for j in range(num_point):
			for i in range(dim):
				self.float_array.InsertNextValue(self.math.Random(0, 1))
		return self.float_array






