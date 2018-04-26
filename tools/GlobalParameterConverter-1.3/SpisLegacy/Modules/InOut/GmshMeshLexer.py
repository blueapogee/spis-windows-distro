
"""
**File name:**    GmshMeshLexer.py

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


from MetaLexer import MetaLexer

class GmshMeshLexer(MetaLexer):
    '''
    Lexer for Gmsh mesh file.
    '''
    def __init__(self, file):
        # Warning! The order of tokens is important (ERROR must be the last
        self.tokens = [
            ("TOK_NUM",  "([-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?)",
             self._dummy),
            ("TOK_BNOD",   "(\$NOD)",         self._dummy),
            ("TOK_ENOD",   "(\$ENDNOD)",      self._dummy),
            ("TOK_BELM",   "(\$ELM)",         self._dummy),
            ("TOK_EELM",   "(\$ENDELM)",      self._dummy),
            ("TOK_EOL",    "(\n\r|\r\n|\n)",  self._inc_line),
            ("SEPARATORS", "(\s+)",           self._dummy),
            ("ERROR",      "(.*)",            self._scan_error)
            ]
        self.replacements = {}
        MetaLexer.__init__(self, file)

if __name__ == "__main__":
    """Testing purpose"""
    import sys
    lex = GmshMeshLexer(sys.argv[1])
    tokens = lex.scan()
    for i in tokens:
        print "%-10s: %s" % (i[0], i[1])
