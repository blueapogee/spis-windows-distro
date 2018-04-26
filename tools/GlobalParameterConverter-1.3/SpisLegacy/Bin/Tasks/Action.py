"""
Manage the actions (commands) done by the main GUI and forward them to the 
TaskManager. 
**File name:**    Action.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
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

from pawt import swing

class Action(swing.AbstractAction):
        '''
        Manage the actions (commands) done by the main GUI and forward them to the
        TaskManager.
        '''
	def __init__(self, name, action=None, icon=None, description=None, needEvent=0):
		if action is None:
			action = name
			name = action.__name__

		#swing.AbstractAction.__init__(self, name)
		self.name = name
		self.icon = icon
		if icon:
			self.setIcon(swing.Action.SMALL_ICON, icon)
		if description:
			self.setText(swing.Action.SHORT_DESCRIPTION, description)
			self.description = description
		else:
			self.description = name
		self.action = action

		self.enabled = 1
		self.needEvent = needEvent

	def actionPerformed(self, event):
		if self.needEvent:
			self.action(event)
		else:
			self.action()

	def createMenuItem(self):
		mi = swing.JMenuItem(self.name, actionListener=self, enabled=self.enabled)
		return mi

class TargetAction(Action):
	def actionPerformed(self, event):
		if self.needEvent:
			self.action(self.getTarget(), event)
		else:
			self.action(self.getTarget())
