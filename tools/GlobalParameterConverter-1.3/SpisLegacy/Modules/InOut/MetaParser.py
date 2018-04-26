"""
**File name:**    MetaParser.py

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


import re
import sys
import exit_status
import time

class ParserException(Exception):
    pass

class MetaParser:
    def __init__(self, lexer, debug = 0):
        self.lexer = lexer
        self.cur_token = lexer.scan_next()
        self.debug_trace = debug
        self.eat_time = 0

    def _parse_trace(self, str):
        """Print the parse trace (debug)"""
        if self.debug_trace:
            print >>sys.stderr, str

    def _parse_error(self):
        """Print the error, and put the good exit status"""
        print >>sys.stderr, "Parse error: <%s> not expected" \
              % self.cur_token[1]
        sys.exit(exit_status.GL_PARSE)

    def _eat(self, token_to_eat):
        """
        Eat the current token, modify the tokens list and update the
        current tokens
        """
        res = self.cur_token[1]
        if self.cur_token[0] == token_to_eat:
            #t0 = time.time()
            self.cur_token = self.lexer.scan_next()
            #t1 = time.time()
            #print "time to eat", `(t1-t0)`
        else:
            self._parse_error()
        return res

    def parse(self):
        """Run the starting rule"""
        raise ParserException("You need to overload the parse function")
