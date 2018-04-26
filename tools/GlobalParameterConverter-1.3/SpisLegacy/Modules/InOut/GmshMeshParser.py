
"""
**File name:**    GmshMeshParser.py

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
from MetaParser import MetaParser

# gmsh grammar:
#
# gmsh: BNOD EOL NUM points ENDNOD EOL BELM NUM elms ENDELM
#
# points: point
#       | point points
#
# point: NUM NUM NUM NUM EOL
#
# elms: elm
#     | elm elms
#
# elm: NUM 1 NUM NUM NUM - NUM NUM EOL
#    | NUM 2 NUM NUM NUM - NUM NUM NUM EOL
#    | NUM 3 NUM NUM NUM - NUM NUM NUM NUM EOL
#    | NUM 4 NUM NUM NUM - NUM NUM NUM NUM EOL
#    | NUM 5 NUM NUM NUM - NUM NUM NUM NUM NUM NUM NUM NUM EOL
#    | NUM 6 NUM NUM NUM - NUM NUM NUM NUM NUM NUM EOL
#    | NUM 7 NUM NUM NUM - NUM NUM NUM NUM NUM EOL
#    | NUM 15 NUM NUM NUM - NUM EOL
#

class GmshMeshParser(MetaParser):
    def __init__(self, lexer, debug = 0):
        MetaParser.__init__(self, lexer, debug)
        self.switch_cor = {
            "1"   :       2,
            "2"   :       3,
            "3"   :       4,
            "4"   :       4,
            "5"   :       8,
            "6"   :       6,
            "7"   :       5,
            "15"  :       1
            }

    def __r_gmsh(self):
        """gmsh rule (see the grammar in the beginning of the file)"""
        self._parse_trace("%-25s: %s" % ("rule gmsh",
                                          str(self.cur_token)))
        self._eat("TOK_BNOD")
        self._eat("TOK_EOL")
        self._eat("TOK_NUM")
        self._eat("TOK_EOL")
        self.__r_points()
        self._eat("TOK_ENOD")
        self._eat("TOK_EOL")
        self._eat("TOK_BELM")
        self._eat("TOK_EOL")
        self._eat("TOK_NUM")
        self._eat("TOK_EOL")
        self.__r_elms()
        self._eat("TOK_EELM")

    def __r_points(self):
        """
        prerequisites rule (see the print grammar in the beginning of the
        file)
        """
        self._parse_trace("%-25s: %s" % ("rule points",
                                          str(self.cur_token)))
        while self.cur_token[0] == "TOK_NUM":
            self._eat("TOK_NUM")
            self._eat("TOK_NUM")
            self._eat("TOK_NUM")
            self._eat("TOK_NUM")
            self._eat("TOK_EOL")

    def __r_elm(self):
        """elm rule (see the grammar in the beginning of the file)"""
        self._parse_trace("%-25s: %s" % ("rule elm",
                                          str(self.cur_token)))
        self._eat("TOK_NUM")
        switcher = self._eat("TOK_NUM")
        self._eat("TOK_NUM")
        self._eat("TOK_NUM")
        self._eat("TOK_NUM")
        for i in range(self.switch_cor[switcher]):
            self._eat("TOK_NUM")
        self._eat("TOK_EOL")

    def __r_elms(self):
        """elms rule (see the grammar in the beginning of the file)"""
        self._parse_trace("%-25s: %s" % ("rule elms",
                                          str(self.cur_token)))
        while self.cur_token[0] == "TOK_NUM":
            self.__r_elm()

    def parse(self):
        """Run the starting rule"""
        self.__r_gmsh()

if __name__ == "__main__":
    """Testing purposes"""
    from GmshMeshLexer import GmshMeshLexer
    scanner = GmshMeshLexer(sys.argv[1])
    parser = GmshMeshParser(scanner, 0)
    parser.parse()
