
"""
**File name:**    MetaLexer.py

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

class LexerException(Exception):
    pass

class MetaLexer:
    """
    Meta Lexer for CAD structure.
    """

    def __init__(self, file):
        self.file = file
        self.line_counter = 1
        self.res = []
        self.__pre_scan()
        if not self.tokens:
            raise LexerException("You must add tokens")
        if not self.replacements and not self.replacements == {}:
            raise LexerException("You must add replacements")

    # Lexer handlers
    def _dummy(self, re_name, re_code, parsed):
        """Do nothing"""
        pass

    def _inc_line(self, re_name, re_code, parsed):
        """Increment the line counter"""
        self.line_counter += 1

    def _scan_error(self, re_name, re_code, parsed):
        """Print the error, with location"""
        print >>sys.stderr, "Scan error: line " + str(self.line_counter) \
              + " \"" + parsed + "\"" + ". The parser will ignore this line."

    def scan_next(self):
        """Return the next token in stream self.stream following
        tokens rules defined in self.tokens"""
        if len(self.stream) == 0:
            return ("TOK_EOF", "")
        res = ()
        while not res:
            for myre in self.tokens:
                tmpre = re.compile(myre[1]).match(self.stream)
                if tmpre:
                    size = len(tmpre.group(0))
                    self.stream = self.stream[size:]
                    # Call the associated function
                    myre[2](myre[0], myre[1], tmpre.group(1))
                    if myre[0] != "SEPARATORS" and myre[0] != "ERROR":
                        res = (myre[0], tmpre.group(1))
                    break
        return res

    def scan(self):
        """Scan self.file following tokens rules defined in self.tokens"""
        self.__pre_scan()
        i = 0
        while len(self.stream) != 0:
            for myre in self.tokens:
                tmpre = re.compile(myre[1]).match(self.stream)
                if tmpre:
                    size = len(tmpre.group(0))
                    self.stream = self.stream[size:]
                    i += size
                    # Call the associated function
                    myre[2](myre[0], myre[1], tmpre.group(1))
                    if myre[0] != "SEPARATORS" and myre[0] != "ERROR":
                        self.res.append((myre[0], tmpre.group(1)))
                    break
        return self.res

    def __pre_scan(self):
        self.__readfile()
        for i in self.replacements.keys():
            self.stream = re.sub(i, self.replacements[i], self.stream)

    def __readfile(self):
        """Open self.file and read it into the string self.stream"""
        try:
            file = open(self.file)
            self.stream = file.read()
        except IOError, e:
            print e
            sys.exit(exit_status.GL_SCAN)

if __name__ == "__main__":
    """Testing purpose"""
    lex = GmshLexer(sys.argv[1])
    tokens = lex.scan()
    for i in tokens:
        print "%-10s: %s" % (i[0], i[1])
