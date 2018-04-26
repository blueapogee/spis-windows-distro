"""
**Module Name:**  GmshGeoLexer

**Project ref:**  Spis/SpisUI

**File name:**    GmshGeoLexer.py

**File type:**    Executable

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  GR validation

**Use:**

**Description:**  Lexer for CAD structure from a GEO file.

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      0.3.0

**Versions and anomalies correction :**

+----------------+---------------------------------+----------------------------+
| Version number | Author (name, e-mail)           | Corrections/Modifications  |
+----------------+---------------------------------+----------------------------+
| 0.1.0          | Maxime Biais                    | Creation                   |
|                | maxime.biais@atenum.com         |                            |
+----------------+---------------------------------+----------------------------+

04, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"


from MetaLexer import MetaLexer

class GmshGeoLexer(MetaLexer):
    '''
    Lexer for CAD structure from a GEO file.
    '''

    def __init__(self, file):
    
        # Warning! The order of tokens is important (ERROR must be the last
        self.tokens = [
            ("TOK_NUM",  "([-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?)",
             self._dummy),
            ("TOK_LINE_L",    "(Line Loop)",     self._dummy),
            ("TOK_RSURF",     "(Ruled Surface)", self._dummy),
            ("TOK_PSURF",     "(Plane Surface)", self._dummy),
            ("TOK_SURF_L",    "(Surface Loop)",  self._dummy),
            ("TOK_VOLUME",    "(Volume)",        self._dummy),
            ("TOK_PHY_POINT", "(Physical Point)",self._dummy),
            ("TOK_PHY_LINE",  "(Physical Line)", self._dummy),
            ("TOK_PHY_SURF",  "(Physical Surface)",self._dummy),
            ("TOK_PHY_VOL",   "(Physical Volume)",self._dummy),
            ("TOK_LINE",      "(Line)",          self._dummy),
            ("TOK_POINT",     "(Point)",         self._dummy),
            ("TOK_PLANE",     "(Plane)",         self._dummy),
            ("TOK_CIRCLE",    "(Circle)",        self._dummy),
            ("TOK_ELLIPSE",   "(Ellipse)",       self._dummy),
            ("TOK_PARAMETER", "(Parameter)",     self._dummy),
            ("TOK_LPAR",      "(\()",            self._dummy),
            ("TOK_RPAR",      "(\))",            self._dummy),
            ("TOK_EQ",        "(=)",             self._dummy),
            ("TOK_LBRACE",    "({)",             self._dummy),
            ("TOK_RBRACE",    "(})",             self._dummy),
            ("TOK_COMMA",     "(,)",             self._dummy),
            ("TOK_SEMI",      "(;)",             self._dummy),
            ("TOK_EOL",       "(\n\r|\r\n|\n)",  self._inc_line),
            ("SEPARATORS",    "(\s+)",           self._dummy),
            ("ERROR",         "(.*)",            self._scan_error)
            ]
        self.replacements = {
            "//.*":            ""
            }
        MetaLexer.__init__(self, file)

if __name__ == "__main__":
    """Testing purpose"""
    import sys
    lex = GmshGeoLexer(sys.argv[1])
    tokens = lex.scan()
    for i in tokens:
        print "%-10s: %s" % (i[0], i[1])
