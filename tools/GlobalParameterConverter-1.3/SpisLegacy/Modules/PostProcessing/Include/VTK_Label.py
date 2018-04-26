"""
**File name:**    VTK_Label.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spine.org`_ for
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
.. _`http://www.spine.org`: http://www.spine.org
"""
__docformat__ = "restructuredtext en"

from vtk import *

class VTK_Label:
	def __init__(self,grid,ren):
		from PostProcessing.Lib.JavaLib import *
		self.label=vtkIdFilter()

		self.label.SetInput(grid)
		self.label.PointIdsOn()
		self.label.FieldDataOn()

		self.label_points_visible=vtkSelectVisiblePoints()
		self.label_points_visible.SetInput(self.label.GetOutput())
		self.label_points_visible.SetRenderer(self.ren)
		self.label_points_visible.SelectionWindowOn()

		self.map_label=vtkLabeledDataMapper()
		self.map_label.SetInput(self.label_points_visible.GetOutput())
		self.map_label.SetLabelFormat("%g")
		self.map_label.SetLabelModeToLabelFieldData()

		self.labelActor=vtkActor2D()
		self.labelActor.SetMapper(self.map_label)
		self.labelActor.GetProperty().SetColor(0.75,0.54,0.6)
		#ren.AddActor2D(self.labelActor)
