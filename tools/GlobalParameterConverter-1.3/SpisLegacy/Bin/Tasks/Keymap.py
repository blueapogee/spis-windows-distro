"""
**File name:**    Keymap.py

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

from java.awt.event import KeyEvent, InputEvent
from pawt.swing import KeyStroke, text
import string
from Action import Action

_keynames = {}
def getKeyStroke(key):
	if len(_keynames) == 0:
		for name in dir(KeyEvent):
			if name[:3] == 'VK_':
				_keynames[string.lower(name[3:])] = getattr(KeyEvent, name)

	if key is None:
		return KeyStroke.getKeyStroke(KeyEvent.CHAR_UNDEFINED)

	if len(key) == 1:
		return KeyStroke.getKeyStroke(key)

	fields = string.split(key, '-')
	key = fields[-1]
	mods = fields[:-1]

	modifiers = 0
	for mod in mods:
		if mod == 'C':
			modifiers = modifiers | InputEvent.CTRL_MASK
		elif mod == 'S':
			modifiers = modifiers | InputEvent.SHIFT_MASK
		#Meta and Alt don't currently work right
		elif mod == 'M':
			modifiers = modifiers | InputEvent.META_MASK
		elif mod == 'A':
			modifiers = modifiers | InputEvent.ALT_MASK
		else:
			raise ValueError, 'Invalid modifier in '+key

	return KeyStroke.getKeyStroke(_keynames[key], modifiers)


def makeAction(o):
	if isinstance(o, Action): return o
	if callable(o): return Action(o)

class Keymap:
	__keynames = {}
	__defaultKeymap = text.JTextComponent.getKeymap(text.JTextComponent.DEFAULT_KEYMAP)

	def __init__(self, bindings={}, parent=__defaultKeymap):
		self.keymap = text.JTextComponent.addKeymap(None, parent)
		for key, action in bindings.items():
			self.bind(key, action)

	def bind(self, key, action):
		self.keymap.addActionForKeyStroke(getKeyStroke(key), makeAction(action))

	def __tojava__(self, c):
		if isinstance(self.keymap, c):
			return self.keymap

if __name__ == '__main__':
	km = Keymap()
	class T:
		def __init__(self, message):
			self.message = message
			self.__name__ = message
		def __call__(self):
			print self.message

	km.bind('x', T('x'))
	km.bind('C-x', T('C-x'))
	km.bind('A-x', T('A-x'))
	km.bind('up', T('up'))
	km.bind('enter', T('enter'))
	km.bind('tab', T('tab'))
	km.bind('S-tab', T('S-tab'))
        #km.bind('F1', T('F1'))


	text = "hello\nworld"

	from pawt import swing, test

	doc = swing.text.DefaultStyledDocument()
	doc.insertString(0, text, None)
	edit = swing.JTextPane(doc)
	edit.keymap = km

	test(edit, size=(150,80))
