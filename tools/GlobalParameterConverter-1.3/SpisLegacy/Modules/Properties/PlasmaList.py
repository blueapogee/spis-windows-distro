"""
List of plasma properties.

**Project ref:**  Spis/SpisUI

**File name:**    PlasmaList.py

:status:          Implemented

**Creation:**     02/07/2003

**Modification:** 02/10/2003  GR validation

**References:**   Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Franck Warmont, Gerard Sookahet

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+-------------------------------+----------------------------+
| Version number | Author (name, e-mail)         | Corrections/Modifications  |
+----------------+-------------------------------+----------------------------+
| 0.1.0          | Franck Warmont                | Definition/Creation        |
|                | Franck Warmont@artenum.com    |                            |
+----------------+-------------------------------+----------------------------+
| 0.2.0          | Gerard Sookahet               | Verification/extension/    |
|                | Gerard.Sookahet@artenum.com   | Validation                 |
+----------------+-------------------------------+----------------------------+

**License:**   Copyright (c) Artenum SARL, 25 rue des Tournelles,
75004, PARIS, 2000-2003, Paris, France, `http://www.artenum.com`_

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

class PlasmaList:
    '''
    List of Data of type Plasma. 
    '''
    def __init__(self):
        self.List = []
        self.IdList = []
        self.NbPlasma = 0
        
    def Add(self, Plasma):
        self.Add_Plasma(Plasma)

    def Add_Plasma(self, Plasma):
        self.List.append(Plasma)
        self.IdList.append(Plasma.Id)
        self.NbPlasma = self.NbPlasma+1

    def Del(self, Plasma):
        self.DelPlasma(Plasma)

    def DelPlasma(self, Plasma):
        if Plasma.Id not in self.IdList:
            print ' Plasma is not in PlasmaList'
        else:
            i = self.IdList.index(Plasma.Id)
            del self.List[i]
            del self.IdList[i]
            self.NbPlasma = self.NbPlasma-1

    def GetElmById(self, IdIn):
        try:
            return self.List[self.IdList.index(IdIn)]
        except:
            return None
