"""
**File name:**    Styles.py

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

from pawt.swing.text import StyleContext, StyleConstants, TabSet, TabStop
import string

class Styles:
	def __init__(self, context=None):
		if context is None:
			context = StyleContext()
		self.context = context
		self.default = self.context.getStyle(StyleContext.DEFAULT_STYLE)

	def add(self, name, parent=None, tabsize=None, **keywords):
		if parent is None:
			parent = self.default
		style = self.context.addStyle(name, parent)

		for key, value in keywords.items():
			key = string.upper(key[0])+key[1:]
			meth = getattr(StyleConstants, "set"+key)
			meth(style, value)

		if tabsize is not None:
			charWidth=StyleConstants.getFontSize(style)
			tabs = []
			for i in range(20):
				tabs.append(TabStop(i*tabsize*charWidth))
			StyleConstants.setTabSet(style, TabSet(tabs))
		return style

	def get(self, stylename):
		return self.context.getStyle(stylename)

	def __tojava__(self, c):
		if isinstance(self.context, c):
			return self.context
