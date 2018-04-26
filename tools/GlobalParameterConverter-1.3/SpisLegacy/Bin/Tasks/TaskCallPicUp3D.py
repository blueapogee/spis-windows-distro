"""
Call the Java based 3D simulation kernel, PicUp3D.

**Project ref:**  Spis/SpisUI

**File name:**    TaskCallPicUp3D.py

**File type:**    Task

:status:          Implemented

**Creation:**     28/12/2003

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Arsene Lupin, Sebastien Jourdain

:version:      0.2.0

**Versions and anomalies correction :**

+----------------+---------------------------+----------------------------+
| Version number | Author (name, e-mail)     | Corrections/Modifications  |
+----------------+---------------------------+----------------------------+
| 0.1.0          | Arsene Lupin              | Definition/Creation        |
|                | lupin@artenum.com         |                            |
+----------------+---------------------------+----------------------------+

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

import java.awt
import pawt

from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedFiles
from Bin.Tasks.shared         import sharedFrames
from Bin.Tasks.shared         import sharedData
from Bin.Tasks.shared         import sharedGlobalsPicUp
from Bin.Tasks.common         import create_internal_frame


from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_VTK_EXCHANGE


class TaskCallPicUp3D(Task):
    """Call the Java based 3D simulation kernel, PicUp3D"""
    desc="Load PicUp3D simulation kernel"
    def run_task(self):
        from org.spis.picup3d                  import PicUp3DGUI
        #from org.spis.picup3d.listener.plot2d  import *
        #from org.spis.picup3d.listener.vtk     import *
        #from org.spis.picup3d.object3d         import *
        #from org.spis.picup3d.source           import *
        #from org.spis.picup3d.current          import *
        #from org.spis.picup3d.ui               import *
        #from org.spis.picup3d.util             import *
        #from javax.swing                       import *

        self.globalParam = java.util.Properties()
        
        scaleFactor = 1;
        
        ## Error when String Should be fixed...
        
        for key in sharedGlobalsPicUp.keys():
            value = sharedGlobalsPicUp[key][4]
            print key, "=", value
            self.globalParam.setProperty(key,value)
            
        self.picUp3d = PicUp3d(self.globalParam)
        
        # Set PIC Loop (String[])
        self.picUp3d.setPicLoop(PicUp3d.DEFAULT_PIC_LOOP_WITH_INTERSEPT)
        
        self.gui = PicUp3DGUI(self.picUp3d,sharedFrames["gui"].getCurrentDesktop())
        self.glassPane = InfiniteProgressPanel()
        self.glassPane.setVisible(0)
        self.gui.setWaitWindows(self.glassPane)

        # Add sources
        self.tank = Tanks(self.picUp3d.getPlasma(), self.picUp3d.getParameterManager())
        self.tank.initAllTanks()
        
        #TBC
        self.tank.preLoading(0.5*(self.picUp3d.getParameterManager().getFloat(GlobalParameterManager.TOTAL_NUMBER_OF_MACRO_PARTICLES) * self.picUp3d.getParameterManager().getFloat(GlobalParameterManager.PARTICLE_LOADING_RATE)) / self.picUp3d.getPlasma().getGridVolume(),self.picUp3d.getPlasma().getDeltaT())


        self.picUp3d.addSource(self.tank)

        # Add 3d objects
        self.object3D = File3dWithMask(self.picUp3d.getParameterManager(), self.picUp3d.getPlasma(), 0, 0, 0)
        #self.object3D = TestMask(self.picUp3d.getParameterManager(), self.picUp3d.getPlasma(), 0, 0, 0)
        
        #object3D.translateToCenter()
        #object3D.scale(scaleFactor)
        #object3D.buildMask()
        #object3D.setPhi(picUp3d.getParameterManager().getFloat(GlobalParameterManager.OBJECT_3D_INITIAL_POTENTIAL))
        
        self.picUp3d.setObject3D(self.object3D)
        

        # Add current balance
        self.picUp3d.addListener(CurrentBalance3D(self.object3D, 1,1))
        
        # Add Listener
        self.picUp3d.addListener(VtkPicUpListener(GL_VTK_EXCHANGE, 10))
        self.picUp3d.addListener(ParticlePicUpListener())
        self.picUp3d.addListener(ParticleEnergyPicUpListener(2))
        self.picUp3d.addListener(MemoryListener())

        #=> self.picUp3d.addListener(org.spis.picup3d.listener.ParticlePicUpListener("/tmp/outputs"));
        #=> 
        #=> Particle[] particles = new Particle[100];
        #=> System.out.println("Nb active part: "+picUp3d.getPlasma().getParticleManager().getNbActiveParticles());
        #=> for (int i = 0; i < particles.length; i++) {
        #=>    particles[i] = picUp3d.getPlasma().getParticleManager().getActiveParticle(
        #=>    i  * picUp3d.getPlasma().getParticleManager().getNbActiveParticles() / particles.length);
        #=> }
        #=> picUp3d.addListener(new TrajectoryVtkPicUpListener("/tmp/outputs", particles));

        self.InternalFrame = create_internal_frame("PicUp3D",sharedFrames["gui"].getCurrentDesktop())
        self.InternalFrame.addInternalFrameListener(InternalCloser(self.picUp3d))
        self.InternalFrame.setVisible(0);
        self.InternalFrame.reshape( 0, 0, 400, 300)
        self.InternalFrame.getContentPane().setLayout(java.awt.BorderLayout())
        self.InternalFrame.getContentPane().add(self.gui,java.awt.BorderLayout.CENTER)
        self.InternalFrame.setGlassPane(self.glassPane);
        self.InternalFrame.setVisible(1);

class InternalCloser(pawt.swing.event.InternalFrameAdapter):
    def __init__(self,picUp):
        self.picUp = picUp
        
    def internalFrameClosing(self,internalFrameEvent):
        self.picUp.stopSimulation()
