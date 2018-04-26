"""
Default 2D data analysis system. This module will build 2D plots of 
type y=f(x) for DataFields of type Curvi (localisation=4).

**Project ref:**  Spis/SpisUI

**File name:**    BuildPlot2D.py

:status:          Implemented

**Creation:**     10/11/2003

**Modification:** 22/11/2003  validation

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Julien Forest, Sebastien Jourdain

:version:      1.1.0

**Versions and anomalies correction :**

+----------------+--------------------------------------+----------------------------+
| Version number | Author (name, e-mail)                | Corrections/Modifications  |
+----------------+--------------------------------------+----------------------------+
| 0.1.0          | J.Forest                             | Creation                   |
|                | j.fores@atenum.com                   |                            |
+----------------+--------------------------------------+----------------------------+
| 1.1.0          | Sebastian Jourdain                   | Bug correction             |
|                | jourdain@artenum.com                 |                            |
+----------------+--------------------------------------+----------------------------+

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


import sys
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH
from org.slf4j          import Logger
from org.slf4j          import LoggerFactory

#sys.path.append(GL_SPISUIROOT_PATH + "/PostProcessing/Spis2DPlot/")

try:
#if(1): 
    from org.spis.plot import Plot2D
except:
    print "Error: Impossible to load Plot2D in BuildPlot2D.py" 
    print "       Check if the path to jFreeChart is properly set."

from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.common         import create_internal_frame

class BuildPlot2D:
    '''
    Default 2D data analysis system. This module will build 2D plots of
    type y=f(x) for DataFields of type Curvi (localisation=4).
    
    Example of basic plot in command line: 
         a=[]
         b=[]
         for i in range(10):
            x=0.1*i
            a.append(x)
            b.append(math.exp(x))
            
         from Bin.BuildPlot2D import BuildPlot2D
         BuildPlot2D().plot2D(a,b)
    '''
    def __init__(self):
       
        localLogger = LoggerFactory.getLogger("BuildPlot2D")
        localLogger.info("Initialisation of the 2D plot logger")

        self.x = []
        self.y = []
        
        self.title  = ""
        self.legend = ""
        self.internal = create_internal_frame("2D Data Analysis",sharedFrames["gui"].getCurrentDesktop())
        
        
    def setShape(self, x, y, length, eigth):
        self.internal.reshape(x,y, length, eigth)

    def buildDefaultData(self):
        '''
        For test purpose.
        '''
        self.x = [0.0, 1.0, 2.0, 3.0, 4.0]
        self.y = [1.0, 2.0, 3.0, 4.0, 8.0]
        self.title  = "Default plot"
        self.legend = "Example of 2D plot"


    def buildData(self, DataFieldIn, MeshFieldIn):
        self.setDataFromDfAnMF(self, DataFieldIn, MeshFieldIn)
        
    def setDataFromDfAnMF(self, DataFieldIn, MeshFieldIn):
        '''
        Build data structure for y=f(x) plot for the given DataField and Mesh Field. DataField and 
        MeshFiels must be of localisation 4 (curvi).
        '''
        self.title  = "Plot of "+DataFieldIn.Name
        self.legend = DataFieldIn.Name+" versus "+MeshFieldIn.Name

        # we build a dataset such as the DataSet correspond to y
        # and the MeshField to x (or t)
        self.y = DataFieldIn.ValueList
        self.x = MeshFieldIn.MeshElementList
        
    def setXAxisValues(self, XValuesIn):
        self.x = XValuesIn
        
    def setYAxisValues(self, YValuesIn):
        self.Y = YValuesIn
        
    def setValues(self, XValuesIn, YValuesIn):
        
        self.x = XValuesIn
        self.y = YValuesIn
        

    def buildPlot(self):
        '''
        Build a y=f(x) plot.
        '''
        self.titleframe = " 2D plot"
        #print self.x, self.y
        self.plot2D = Plot2D(self.x, self.y, self.titleframe, self.title, self.legend)
        self.plot2Dframe = self.plot2D.getChart()

    def run(self):
        '''
        Run and show the internal manager.
        '''
        print "displaying"
        self.internal.getContentPane().add(self.plot2Dframe)
        self.internal.setVisible(1)
        self.internal.setTitle(self.titleframe)
        self.internal.setIconifiable(1)
        self.internal.setMaximizable(1)
        self.internal.setIconifiable(1)
        self.internal.setResizable(1)
        self.internal.setClosable(1)
        #self.internal.reshape(428, 0, 590, 350)
        #self.internal.toFront()
        self.internal.show()
        #sharedFrames["desktop_pane"].add(self.internal)

    def plot2D(self, XValuesIn, YValuesIn):
        """
        plot directly a 2D plot of y = f(x) type, from XValuesIn as x-axis values and 
        YValuesIn as y-axis values. Both should are listes of numbers (integer or float) of the same length.
        """
        self.setValues(XValuesIn, YValuesIn)
        self.buildPlot()
        self.run()
        self.internal.reshape(428, 0, 590, 350)
        self.internal.toFront()
        self.internal.show()
        

if __name__ == "__main__":
    print 'To see'
    '''
    myplot=BuildPlot2D()
    myframe=JFrame()
    myframe.getContentPane().add(myplot)
    '''

