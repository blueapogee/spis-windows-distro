"""
**File name:**    SimulationDataExtractor.py

**Creation:**     2010/06/10

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest

:version:      1.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Julien Forest                        | Creation                   |
|         | j.forest@artenum.com                 |                            |
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

import time
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory

from Modules.Field.DataField            import DataField
from Modules.Field.DataFieldList        import DataFieldList
from Modules.Field.MeshField            import MeshField
from Modules.Field.MeshFieldList        import MeshFieldList

class SimulationDataExtractor:
    """
    Generic interface of data extraction from simulation models. An inherited class should
    be implemented for each type of simulation model (e.g see SpisNumSimulationDataExtractor for 
    SpisNum kernel as example). 
    """
    
    def __init__(self):
        """
        constructor.
        """
        self.logger = LoggerFactory.getLogger("SimulationDataExtractor")
        self.simulationModel = None
        self.meshFieldDataList = None
        self.dataFieldDataList = None
        self.runId = 0
        self.simulationId = 0
        self.dateIndex = -1
        
    def setDefaultSimulationId(self):
        """
        set the Simulation Id automatically by default, based on the local absolute time. 
        """
        tmpDate = time.gmtime()
        self.simulationId = `tmpDate[0]`+`tmpDate[1]`+`tmpDate[2]`+`tmpDate[3]`+`tmpDate[4]`+`tmpDate[5]`
        self.logger.info("Initialisation of simulation Nb:"+self.simulationId)
                
    def setSimulationId(self, simulationId):
        """
        Set the simulation Id. 
        """
        self.simulationId = simulationId
        
    def setRunId(self, runId):
        """
        set the run Id. 
        """
        self.runId = runId
        
    def setInput(self, simulationModel):
        """
        Set the input simulation model. This model may differ from a simulation kernel to 
        another one. See SpisNumSimulationDataExtractor for illustration. 
        """
        self.simulationModel = simulationModel
        
    def setOutputDataBus(self, sharedMeshFieldDataList, sharedDataFieldDataList):
        """
        Set the output shared data bus (e.g shared["allMeshFieldDataList"] ) where the resulting DataFields and
        MeshFields should be saved. 
        """
        self.meshFieldDataList = sharedMeshFieldDataList
        self.dataFieldDataList = sharedDataFieldDataList
        self.dataIndex = self.dataFieldDataList.GetMaxId() #max(AllDataField.IdList)

        
    def resetDataBus(self):
        """
        rest the output data bus (i.e set to new DataFieldList and MeshFieldList). All previoussly read data will be 
        erased. 
        """
        self.dataFieldDataList = DataFieldList()
        self.meshFieldDataList = MeshFieldList()
        
    def readSimulation(self, mode="a"):
        """
        Should be implemented in the inherited classes.
        """
        
    def exportDataToControledFormat(self, controler, dataList):
        controler.exportListOfDataFields(dataList)