"""
**Module Name:** eadWriteManager

**Project ref:**  Spis/SpisUI

**File name:**    ReadWriteManager.py

**File type:**    Executable

:status:          Implemented

**Creation:**     10/11/2005

**Modification:** 

**Use:**

**Description:**  For file format 3 (under-development).

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Sebastein Jourdain

:version:      0.1.0

**Versions and anomalies correction :**

+----------------+---------------------------------+----------------------------+
| Version number | Author (name, e-mail)           | Corrections/Modifications  |
+----------------+---------------------------------+----------------------------+
| 0.1.0          | Sebastien Jourdain              | Creation                   |
|                | jourdain@atenum.com             |                            |
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


from Modules.InOut import MaterialPyWriter
from MaterialPyWriter import MaterialPyWriter

import os

class ReadWriteManager:
    def __init__(self):
        pass
###
# Simple object Serialisation
###
    
    def getMaterialFromFile(self, fileToLoad):
    	print 'Load Material'
    	moduleName = fileToLoad[:-3]
    	tmpCmd = "import "+ moduleName
        exec(tmpCmd)
        tmpCmd = "currentMaterial = "+moduleName+".material)"
        exec(tmpCmd)
        return currentMaterial
    	
    def saveMaterialToFile(self, material, fileToSave):
    	print 'Save Material'
        wr = MaterialPyWriter(material)
        wr.setOutputFileName(fileToSave)
        wr.readStructure()
        wr.write()
        wr = None
        
    def getElectricalNodeFromFile(self, fileToLoad):
    	print 'Load Electrical node'
    	moduleName = fileToLoad[:-3]
    	tmpCmd = "import "+ moduleName
        exec(tmpCmd)
        tmpCmd = "currentElectricalNode = "+moduleName+".elecNode)"
        exec(tmpCmd)
        return currentElectricalNode
    	
    def saveElectricalNodeToFile(self, elecNode, fileToSave):
    	print 'Save Electrical node'
        wr = ElecNodePyWriter(elecNode)
        wr.setOutputFileName(fileToSave)
        wr.readStructure()
        wr.write()
        wr = None
        
    def getPlasmaFromFile(self, fileToLoad):
    	print 'Load Plasma'
    	moduleName = fileToLoad[:-3]
    	tmpCmd = "import "+ moduleName
        exec(tmpCmd)
        tmpCmd = "currentPlasma = "+moduleName+".plasma)"
        exec(tmpCmd)
        return currentPlasma
    	
    def savePlasmaToFile(self, plasma, fileToSave):
    	print 'Save Plasma'
        wr = PlasmaPyWriter(plasma)
        wr.setOutputFileName(fileToSave)
        wr.readStructure()
        wr.write()
        wr = None

###
# Complexe object Serialisation
###

    def saveMaterialListToDir(self, materialList, dirToSave):
        print 'Save all Materials'
        for material in materialList:
            
            #try:
            fileName = os.path.join(dirToSave, "material_" + `material.Id` + ".py")
            print fileName
            self.saveMaterialToFile(material, fileName)
            #except:
            #    print "Impossible to save material"

    def saveElectricalNodeListToDir(self, elecNodeList, dirToSave):
        print 'Save all Electrical Nodes'
        for elecNode in elecNodeList:
            try:
                fileName = os.path.join(dirToSave, "elecNode_"+`elecNode.Id`+".py")
                self.saveElectricalNodeToFile(elecNode, fileName)
            except:
                print "Impossible to save electrical node"

    def savePlasmaListToDir(self, plasmaList, dirToSave):
        print 'Save all Plasma'
        for plasma in plasmaList:
            try:
                fileName = os.path.join(dirToSave, "plasma_"+`plasma.Id`+".py")
                self.saveElectricalNodeToFile(material, fileName)
            except:
                print "Impossible to save plasma"
               
###
# Basic object serialisation
###

    def saveObject(self, object, filename):
        stream = open(filename, "w")
        stream.write("obj = " + str(object))
        stream.flush()

    def loadObject(self, module_name):
        exec "import " + module_name
        exec "obj = module_name.obj"
        return obj

    def createDirectory(self, directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

if __name__ == "__main__":
    class Mip:
        a = 3
    class Mop:
        a = 1
        b = 3
        c = [1, 2, 3]
        d = Mip()
        pouet = "salut"
    mop = Mop()
    test = {"a": 1,  "2": 4, "3": [1,2,3]}
    print test
    r = ReadWriteManager()
    print r.recSaveObject(mop)
