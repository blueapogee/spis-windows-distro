
"""
**File name:**    GmshGeoParser.py

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
import sys, time
import exit_status
from MetaParser                 import MetaParser
from GmshGeoConverters          import GmshGeoConverters

# FIXED: unrecursived -> less readable but more efficient

# gmsh mini-geo grammar:
#
# gmsh: gmsh EOL
#     | gmsh line_loop
#     | gmsh ruled_surface
#     | gmsh plane_surface
#     | gmsh surface_loop
#     | gmsh volume
#     | gmsh physical_point
#     | gmsh physical_line
#     | gmsh physical_surface
#     | gmsh physical_volume
#     | gmsh line
#     | gmsh point
#     | gmsh plane
#     | gmsh circle
#     | gmsh ellipse
#     | gmsh parameter
#
# line: LINE LPAR NUM RPAR EQ exp
#
# point: POINT LPAR NUM RPAR EQ exp
#
# circle: POINT LPAR NUM RPAR EQ exp
#       | POINT LPAR NUM RPAR EQ exp PLANE exp
#
# ... etc ...
#
# exp: LBRACE NUM RBRACE
#    | LBRACE NUM s_exp RBRACE
#
# s_exp: COMMA NUM
#      | COMMA NUM s_exp
#
#
# The parser is factorized and only 2 general methods
# (__r_general_rule and __r_exp) have been written to handle most of
# the grammar rules)

class GmshGeoParser(MetaParser):
    def __init__(self, lexer, debug = 0):
        MetaParser.__init__(self, lexer, debug)
        self.converters = GmshGeoConverters()
        self.converters.Init_defaultPhysical()
        self.tokens_cor = {
            "TOK_LINE_L":       (self.__r_general_rule,
                                 self.converters.ConvertCurveLoop),
            "TOK_RSURF":        (self.__r_general_rule,
                                 self.converters.ConvertSurface),
            "TOK_PSURF":        (self.__r_general_rule,
                                 self.converters.ConvertSurface),
            "TOK_SURF_L":       (self.__r_general_rule,
                                 self.converters.ConvertSurfaceLoop),
            "TOK_VOLUME":       (self.__r_general_rule,
                                 self.converters.ConvertVolume),
            "TOK_PHY_POINT":    (self.__r_general_rule,
                                 self.converters.ConvertPhysicalPoint),
            "TOK_PHY_LINE":     (self.__r_general_rule,
                                 self.converters.ConvertPhysicalCurve),
            "TOK_PHY_SURF":     (self.__r_general_rule,
                                 self.converters.ConvertPhysicalSurface),
            "TOK_PHY_VOL":      (self.__r_general_rule,
                                 self.converters.ConvertPhysicalVolume),
            "TOK_LINE":         (self.__r_general_rule,
                                 self.converters.ConvertLine),
            "TOK_POINT":        (self.__r_general_rule,
                                 self.converters.ConvertPoint),
            "TOK_PLANE":        (self.__r_general_rule,
                                 self.converters.ConvertPlane),
            "TOK_CIRCLE":       (self.__r_circle,
                                 self.converters.ConvertCircle),
            "TOK_ELLIPSE":      (self.__r_ellipse,
                                 self.converters.ConvertEllipse),
            "TOK_PARAMETER":    (self.__r_general_rule,
                                 self.converters.ConvertParameter)
            }

    def __r_gmsh(self):
        """gmsh rule (see the grammar in the beginning of the file)"""
        while 1:
            start_t = time.time()
            if self.cur_token[0] == "TOK_EOL":
                self._eat("TOK_EOL")
            start_time = time.time()
            tmpToken = self.cur_token[0]
            if self.tokens_cor.has_key(self.cur_token[0]):
                self.tokens_cor[tmpToken][0](self.cur_token)
                self.tokens_cor[tmpToken][1]()
            # print "Token "+ tmpToken +" parsing duration: "+`(time.time() - start_time)`
       
            if self.cur_token[0] == "TOK_EOF":
                return

    def __r_general_rule(self, ftok):
        
        self.converters.ObjectNumber += 1
        self.converters.Field = [ftok[1]]
        self._eat(ftok[0])
        self._eat("TOK_LPAR")
        
        self.converters.Field.append(eval(self._eat("TOK_NUM")))
        #self._eat("TOK_NUM") (for purpose of test only)
        
        self._eat("TOK_RPAR")
        self._eat("TOK_EQ")
        
        self.converters.Field.extend(self.__r_exp())
        #self.__r_exp() (for purpose of test only)
        
        self._eat("TOK_SEMI")

    def __r_circle(self, ftok):
        
        self.converters.ObjectNumber += 1
        self.converters.Field = [ftok[1]]
        self._eat(ftok[0])
        self._eat("TOK_LPAR")
        self.converters.Field.append(eval(self._eat("TOK_NUM")))
        self._eat("TOK_RPAR")
        self._eat("TOK_EQ")
        self.converters.Field.extend(self.__r_exp())
        if self.cur_token[0] == "TOK_PLANE":
            self._eat("TOK_PLANE")
            self.__r_exp()
        self._eat("TOK_SEMI")

    def __r_ellipse(self, ftok):
        
        self.converters.ObjectNumber += 1
        self.converters.Field = [ftok[1]]
        self._eat(ftok[0])
        self._eat("TOK_LPAR")
        self.converters.Field.append(eval(self._eat("TOK_NUM")))
        self._eat("TOK_RPAR")
        self._eat("TOK_EQ")
        self.converters.Field.extend(self.__r_exp())
        if self.cur_token[0] == "TOK_PLANE":
            self._eat("TOK_PLANE")
            self.__r_exp()
        self._eat("TOK_SEMI")


    def __r_exp(self):
        self._eat("TOK_LBRACE")
        res = [eval(self._eat("TOK_NUM"))]
        while self.cur_token[0] != "TOK_RBRACE":
            self._eat("TOK_COMMA")
            res.append(eval(self._eat("TOK_NUM")))
        self._eat("TOK_RBRACE")
        return res

    def parse(self):
        """Run the starting rule"""
        self.__r_gmsh()
        self.converters.Save_DefaultPhysical()
        self.converters.ListOfElmtNum = [self.converters.ListOfOldElmtNum,
                                       self.converters.ListOfNewElmtNum]
        self.converters.ListOfGrpNum = [self.converters.ListOfOldGrpNum,
                                      self.converters.ListOfNewGrpNum]
        # FIXME: compatibility purposes, please use attributes of the
        # FIXME: object instead of this returned values.
        return self.converters.ListOfObject, self.converters.ListOfGeoElement,\
               self.converters.ListOfElmtNum, self.converters.ListOfGeoGroup, \
               self.converters.ListOfGrpNum, self.converters.ListOfParameter

if __name__ == "__main__":
    """Testing purposes"""
    from GmshGeoLexer import GmshGeoLexer
    scanner = GmshGeoLexer(sys.argv[1])
    parser = GmshGeoParser(scanner, 0)
    parser.parse()
