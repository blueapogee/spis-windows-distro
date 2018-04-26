"""
**File name:**    PythonThread.py

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
import sys
from java.lang import Thread, System
import threading

class PythonThread(Thread):
    '''
    Thread corresponding to the Tasks.
    '''
    def __init__(self, code, console):
        self.code = code
        self.console = console
        self.locals = console.locals 
        self.mute = 0
        
    def setMute(self, mute):
        self.mute = mute

    def run(self):
        try:
            for i in self.locals:
                exec "global " + i
            exec self.code in self.locals
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            l = len(traceback.extract_tb(sys.exc_traceback))
            try:
                1/0
            except:
                m = len(traceback.extract_tb(sys.exc_traceback))
                traceback.print_exception(exc_type, exc_value, exc_traceback, l-m)
        if self.mute == 0:
            self.console.newInput()
        self.console.restoreIO()

    def stopPython(self):
        self.stop()
