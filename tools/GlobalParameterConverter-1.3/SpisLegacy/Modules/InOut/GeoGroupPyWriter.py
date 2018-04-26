"""
Exports the given GeoGroup as an equivalent Python script. The output scritp can 
be reload aftert just by a Python import. The class scan is not recursive yet. 

**Module Name:**  GroupPyWriter

**Project ref:**  Spis/SpisUI

**File type:**    Module

:status:          implemented

**Creation:**     10/01/2005

**Modification:** 20/03/2005  AL preliminary validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:          Arsene Lupin

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------+----------------------------+
| Version number | Author (name, e-mail)          | Corrections/Modifications  |
+----------------+--------------------------------+----------------------------+
| 0.1.0          | Arsene Lupin                   | Creation                   |
|                | Arsene Lupin@artenum.com       |                            |
+----------------+--------------------------------+----------------------------+

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

import sys
from Modules.InOut import ObjectPyWriter
from Modules.InOut.ObjectPyWriter import ObjectPyWriter

class GeoGroupPyWriter:
        '''
        save the given group object as python script. This script can 
        be imported as simple Python module after.
        '''
        def __init__(self, groupIn):
            
            self.group = groupIn                
            self.eol = "\n" #in order to have projects movable form UNIX to DOS
                
                
        def setOutputFileName(self, fileNameIn):
            '''
            set the output file path and name.
            '''
            self.fileName = fileNameIn;
                

        def readStructure(self):
            '''
            Read the structure (i.e serialised) the given structure.
            '''
            
            self.globalList= []
            
            # PyWriting of the ElecNode member
            self.wrElecNode = ObjectPyWriter(self.group.ElecNode)
            self.wrElecNode.setInstanceName("elecNode")
            #self.wrElecNode.addOverwriteMember("List", tmpValue)
            self.wrElecNode.addExcludedMenber("DataList")
            self.wrElecNode.readPatern()
            list = self.wrElecNode.saveToList()
            self.globalList.append(list)
            
            # PyWriting of the Plasma member
            self.wrPlasma = ObjectPyWriter(self.group.Plasma)
            self.wrPlasma.setInstanceName("plasma")
            #self.wrPlasma.addOverwriteMember("List", tmpValue)
            self.wrPlasma.addExcludedMenber("DataList")
            self.wrPlasma.readPatern()
            list = self.wrPlasma.saveToList()
            self.globalList.append(list)
            
            # PyWriting of the Material Member
            self.wrMaterial = ObjectPyWriter(self.group.Material)
            self.wrMaterial.setInstanceName("material")
            #self.wrMaterial.addOverwriteMember("List", tmpValue)
            self.wrMaterial.addExcludedMenber("DataList")
            self.wrMaterial.readPatern()
            list = self.wrMaterial.saveToList()
            self.globalList.append(list)
            
            # PyWriting of the element list
            self.wrDL = ObjectPyWriter(self.group.ElementList)
            self.wrDL.setInstanceName("elementList")
            #self.wrDL.addOverwriteMember("List", tmpValue)
            self.wrDL.addExcludedMenber("List")
            self.wrDL.readPatern()
            list = self.wrDL.saveToList()
            self.globalList.append(list)
            
            # PyWriting of the group itself
            self.wrGroup = ObjectPyWriter(self.group)
            self.wrGroup.setInstanceName("group")
            self.wrGroup.addOverwriteMember("ElecNode", "elecNode")
            self.wrGroup.addOverwriteMember("Plasma", "plasma")
            self.wrGroup.addOverwriteMember("Material", "material")
            self.wrGroup.addOverwriteMember("ElementList", "elementList")
            self.wrGroup.readPatern()
            list = self.wrGroup.saveToList()
            self.globalList.append(list)

                
        def write(self):
            '''
            write the serialised structure.
            '''
            try:
                fileOut = open(self.fileName, 'w')
                fileOut.write("# DATA")

                for data in self.globalList:
                     for elm in data:
                         fileOut.write(elm+self.eol)
                    
                fileOut.close()
            except:
                print >> sys.stderr, "Error in GeoGroupPyWriter: impossible to export the module"
                    
                   
