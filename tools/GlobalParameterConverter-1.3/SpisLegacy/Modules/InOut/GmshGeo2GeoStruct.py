"""
**File name:**    GmshGeo2GeoStruct.py

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

from Modules.InOut.GmshGeoLexer   import GmshGeoLexer
from Modules.InOut.GmshGeoParser  import GmshGeoParser
import time

def Convert(input):
    print "Lexing... "
    start_t = time.time()
    scanner = GmshGeoLexer(input[0])
    scan_t = time.time()
    print "DONE."
    print "Parsing... "
    parser = GmshGeoParser(scanner, 0)
    parse_t = time.time()
    print "DONE."
    ListOfObject, ListOfGeoElement, ListOfElmtNum, ListOfGeoGroup, ListOfGrpNum, ListOfParameter = parser.parse()
    end_t = time.time()
    print "DONE."
    print """
    ----- Scanner initialisation:           %f
    ----- Parser initialisation:            %f
    ----- Eating (parsing phase):           %f
    ----- Total Parsing:                    %f
    Total time:                             %f
    """ %(scan_t - start_t, parse_t - scan_t, parser.eat_time, end_t - parse_t, end_t - start_t)
    return ListOfObject, ListOfGeoElement, ListOfElmtNum, ListOfGeoGroup, \
           ListOfGrpNum, ListOfParameter
