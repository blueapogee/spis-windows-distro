'''
Created on Sep 13, 2010

@author: juju
'''
from Bin.Tasks.Task           import Task
from Bin.Tasks.shared         import shared
from Bin.Tasks.shared         import sharedData

from Modules.InOut.MassiveDFToVtkDataSetExporter  import MassiveDFToVtkDataSetExporter

#import sys
#from Bin.DataExporter.ExporterControler import Controler

#from threading import Thread
from Bin.config           import GL_MAX_THREADS_STACK

class TaskExportAllDFToVtk(Task):
    '''
    Export all present DataFields to VTK dataSet.
    '''


    def run_task(self):
        '''
        Performs the task.
        '''
        mesh = shared['Mesh']
        
        dataFieldSet = sharedData['AllDataField']
        meshFieldSet = sharedData['AllMeshField']

        exporter = MassiveDFToVtkDataSetExporter( mesh, dataFieldSet, meshFieldSet)
        exporter.exportAll()
        
        