


import os
from Bin.Tasks.Task                        import Task
from Bin.Tasks.shared                      import sharedProp, sharedFiles
from Modules.InOut.NascapMaterialsCatalogWriter import NascapMaterialsCatalogWriter


from org.spis.imp.ui.util                   import DirectoryDialog
from Bin.config                             import GL_DATA_PATH, GL_SPISUIROOT_PATH


class TaskExportNascapMaterial(Task):
    """Import NASCAP based materials catalog.
    """
    desc = "Export NASCAP based materials catalog."
    
    def run_task(self):
        '''
        Perform the task
        '''
        
        writer = NascapMaterialsCatalogWriter( sharedProp["defaultNascapMaterialList"].List)
        writer.buildCatalog()

        if sharedFiles.has_key("LAST_MATERIAL_PATH"):
            PATH_IN = sharedFiles["LAST_MATERIAL_PATH"]
        else:
            PATH_IN = GL_SPISUIROOT_PATH
            
        fsd = DirectoryDialog(PATH_IN )
        #fsd.addFileType(".xml", "Nascap format");
        if ( fsd.showSaveDialog(None) ):   #None should set to the parent compoenet
            selectedDir = fsd.getSelectedFileAsString() 
            #self.importer.loadFile(selectedFile)
            print selectedDir

        if not os.path.isdir(selectedDir):
            os.makedirs(selectedDir)
        writer.write( selectedDir+os.sep+"NascapMaterialCatalog.xml")
        try:
           writer.writeCorrespondanceListes(selectedDir+os.sep+"correspondanceListes.py")
        except:
            print "Impossible to write the material correspondance list"