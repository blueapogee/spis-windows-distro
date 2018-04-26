"""
**Deprecated** Managment of the old SPIS Jython console. 
**File name:**    console_mode.py

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

import traceback
import copy
from code import compile_command
from TaskBuiltins import *
import string, sys
from PythonThread import PythonThread


# Autoload tasks modules
import taskslist
for i in taskslist.tasks:
    exec "from %s import %s" % ("Task" + i[1], "Task" + i[1])


class Console:
    # static attribute
    locals_dic = {}
    def __init__(self, mlocals, mglobals):
        self.command = []
        self.locals = globals()
        self.locals.update(locals())
        self.locals.update(mlocals)
        self.locals.update(mglobals)
        self.globals = copy.copy(globals())

    def update_globals(self):
        for i in globals():
            if not i in self.globals:
                self.locals_dic[i] = globals()[i]
        self.globals = copy.copy(globals())

    def input_loop(self):
        while 1:
            try:
                rline = raw_input(">>> ")
            except EOFError:
                break
            self.handle_line(rline)
            self.update_globals()

    def handle_line(self, text):
        self.command.append(text)
        try:
            code = compile_command(string.join(self.command, '\n'))
        except SyntaxError:
            traceback.print_exc(0)
            self.command = []
            return
        if code is None:
            return
        self.command = []
        pt = PythonThread(code, self)
        self.pythonThread = pt
        pt.start()

    def newInput(self):
        self.startUserInput(str(sys.ps1)+'\t')

    def startUserInput(self, prompt=None):
        #if prompt is not None:
        #   #self.write(prompt, 'prompt')
        #   self.startInput = self.document.createPosition(self.document.length-1)
        #   #self.document.setCharacterAttributes(self.document.length-1, 1, self.styles.get('input'), 1)
        #   self.textpane.caretPosition = self.document.length
        #   ae = ActionEvent(self.textpane, ActionEvent.ACTION_PERFORMED, 'start input')
        #   self.inputAction.actionPerformed(ae)
        toto=""



if __name__ == "__main__":
    c = Console(locals(), globals())
    c.input_loop()

