"""
Module of Python/Jython serialisation of SPIS-UI global
parameters.

**Project ref:**  Spis/SpisUI

**File name:**    GlobalParamWriter.py

**File type:**    Executable

:status:          Under Validation

**Creation:**     10/02/2006

**Modification:** 10/02/2006

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Maxime Biais

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+---------------------------------+----------------------------+
| Version number | Author (name, e-mail)           | Corrections/Modifications  |
+----------------+---------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                    | Creation                   |
|                | Arsen.Lupin@atenum.com          |                            |
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


class GlobalParamWriter:
        '''
        Module of Python/Jython serialisation of SPIS-UI global parameters.
        '''
        def __init__(self, globlParams):
                self.paramList = globlParams
                
        def setOutputFileName(self, fileNameIn):
                self.fileName = fileNameIn;
                
                      
        def readStructure(self):
                
                # PyWriting of the data list
                self.wrDL = ObjectPyWriter(self.paramList)
                self.wrDL.setInstanceName("paramList")
                self.wrDL.addOverwriteMember("Dico", tmpValue)
                self.wrDL.readPatern()
                list = self.wrDL.saveToList()
                self.globalList.append(list)
                
                
        def write(self):
                try:
                    fileOut = open(self.fileName, 'w')
                
                    fileOut.write("# DATA")

                    for data in self.globalList:
                         for elm in data:
                             fileOut.write(elm+self.eol)
                        
                    fileOut.close()
                except:
                    print >> sys.stderr, "error: impossible to export the module"
                
