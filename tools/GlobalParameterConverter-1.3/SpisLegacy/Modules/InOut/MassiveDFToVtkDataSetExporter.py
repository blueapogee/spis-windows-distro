'''
Project : Keridwen / multi-threaded DataFields to VTK exporter <br>
Copyright : 2008-2009 ARTENUM SARL, Paris, France <br>
<a href="http://www.artenum.com">http://www.artenum.com</a><br>
License : GPL V2 <br>
Developed by: Artenum SARL <br>
<a href="http://www.artenum.com">http://www.artenum.com</a><br>
Contract nr : Internal Project <br>
<br>
Creation : 15/08/2010 <br>
@author Julien Forest <br>
@author Jeremie Turbet <br>
@version 1.0 <br>

Description: To be use directly in Keridwen V0.XXX and SPIS-UI 4.XXX and higher 
as simple script, though the JyConsole for instance. 

Require that DF, MF, mesh, GL_MAX_THREADS_STACK, GL_EXCHANGE, GL_VTK_EXCHANGE
be set. 

VTK files are written in the GL_VTK_EXCHANGE directory by default. Please, save 
your spis project after to recover the VTK files. 

Some data structure/localisation are not supported. Please check the cell type /
data localisation compliance. 


Created on Sep 13, 2010

@author: Julien Forest, Artenum SARL, Paris
'''

import sys
from Bin.config  import GL_MAX_THREADS_STACK
from Bin.Tasks.shared import *
try:
    from Bin.FieldDataListViewer2 import DataFieldToVtkDataSetThread
except:
    print "error: impossible to load DataFieldToVtkDataSetThread"
#import dfToVTKExporter




class MassiveDFToVtkDataSetExporter:
    '''
    Export all DF present in the dataFielSet given in constructor (e.g, sharedData["AllDataField"])
    into VTK dataSets. 
    '''


    def __init__(self, mesh, dataFieldSet, meshFieldSet):
        '''
        Constructor
        '''
        self.mesh = mesh
        self.dataFieldSet = dataFieldSet
        self.meshFieldSet = meshFieldSet
        self.aliveThreadList=[]
        self.viewer = None
        
    def viewer(self, cassandraViewer):
        """
        If you want to directly load them to an instanciated Cassandra viewer. 
        Take care can be dangerous due to the memory and CPU cost. 
        """
        self.viewer = cassandraViewer
        
    def exportAll(self):
        ################################################################################
        #  And now the action ....
        ################################################################################
        print "####################################################################"
        print "#                  Start DF to VTK conversion                      #"
        print "####################################################################"
        
        for df in self.dataFieldSet.List:
            print "Exporting "+df.Name+"... "
            mf = self.meshFieldSet.GetMeshFieldById(df.MeshFieldId)
            dimIn = df.Local
            if (df.Local == 0):
                dimOut = 3
            elif (df.Local == 1):
                dimOut = 1
            elif (df.Local == 2):
                dimOut = 2
            elif (df.Local == 3):
                dimOut = 3
            else:
                print "Data localisation not supported"
            
            # to limit the total number of thread   
            self.threadPoolManager(GL_MAX_THREADS_STACK)
        
            try:
                #if(1): 
                self.exportDataFieldToVTK(df, mf, self.mesh, dimIn, dimOut, self.viewer)
            except: 
                print "Error: impossible to export", df.Name
        
        # to be sure that everything is done
        self.threadPoolManager(0)
        
        print "####################################################################"
        print "#                     END OF CONVERSION                            #"
        print "####################################################################"
        print ""
        print "Nb threads still alive: "+ str(len(self.aliveThreadList))
        

    def test(self,i):
        print "test", i
    
    def exportDataFieldToVTK(self, dataFieldIn, meshFieldIn, meshIn, dimIn, dimOut, viewer):
    
        currentOutVtkDataSetList = []
        filePostfix = "NotSet"
    
        if dimOut == 0:
            filePostfix = "onNode"
        elif dimOut == 1:
            filePostfix = "onEdge"
        elif dimOut == 2:
            filePostfix = "onFace"
        elif dimOut == 3:
            filePostfix = "onCell"
        else:
            print "Output cell dimension not supported"
            return(None)
            
        converter = DataFieldToVtkDataSetThread()
        converter.setCassandraViewer(viewer)
        converter.setOutputFileName(dataFieldIn.Name + filePostfix)
        converter.setOutVtkDataSetList(currentOutVtkDataSetList)
        converter.setDataFieldIn(dataFieldIn)
        converter.setMeshFieldIn(meshFieldIn)
        converter.setMesh(meshIn)
        converter.dimInOut( dimIn, dimOut)
        converter.start()
        self.aliveThreadList.append(converter)
        # return(converter.start())
    
        
    def threadPoolManager(self, maxThreadsStack):
        #sys.stdout.write("To many threads, please wait...")
        while (len(self.aliveThreadList) > maxThreadsStack):   
            #sys.stdout.write(".")
            #print "    Nb alive threads= ", len(self.aliveThreadList)
            #print self.aliveThreadList
        
            toBeRemovedList = []
            for currentThread in self.aliveThreadList:
                if (currentThread.isAlive() == False):
                    toBeRemovedList.append(currentThread)
        
            for deadThread in toBeRemovedList:
                self.aliveThreadList.remove(deadThread)
                # to help the garbage collector
                deadThread = None

    

        