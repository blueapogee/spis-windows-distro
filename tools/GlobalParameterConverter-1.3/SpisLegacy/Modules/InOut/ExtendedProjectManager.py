'''
Created on 12 dec. 2010

@author: juju
'''

import shutil, os
from Bin.Tasks.shared import sharedFiles
from org.slf4j                import Logger
from org.slf4j                import LoggerFactory
#loadingLogger = LoggerFactory.getLogger("CoreLogger")
 
class ExtendedProjectManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = LoggerFactory.getLogger("ExtendedProjectManager")
        
    def makeProjectFromTemplate(self, templatePath, projectPath):
        """
        perform the action corresponding to the project template
        """        
        if (os.path.exists(templatePath) != 1):
            self.logger.error( "Template not found! \n"
                              +"Impossible to create the project. Please select another path.")
            return 0
        print "step 2"

        if (os.path.exists(projectPath) == 1):
            print "step 3"
            if (os.path.isdir(projectPath) != 1):
                print "is NOT a directory"
                self.logger.error( "The selected project path is a file (and not a directory). \n"
                                  +"Impossible to create the project. Please select another path.")
                return 0
            else:
                print "step 4"
                if ("project" in os.listdir(projectPath) ):
                    print "step 4 bis"
                    self.logger.error( "Control file found in the directory, This seems to be already \n" 
                                      +"a spis-project. Impossible to create a new project from the template.\n"
                                      +"Please select another directory or un-select generation from template.")
                    return 0
                print "step 4 ter"
            print "step 5"
        else:
            self.logger.info("Directory not existing. Creating it.")
            os.mkdir(projectPath)
            print "step 6"
        
        self.logger.info("Project creation")
        try:
            shutil.copytree( os.path.join(templatePath, "Geom"), os.path.join(projectPath, "Geom"))
            shutil.copytree( os.path.join(templatePath, "Groups"),os.path.join(projectPath, "Groups"))
            shutil.copy( os.path.join(templatePath, "__init__.py"), projectPath)
            shutil.copytree( os.path.join(templatePath, "NumKernel"), os.path.join(projectPath, "NumKernel"))
            shutil.copy( os.path.join(templatePath, "project"), projectPath)
            shutil.copytree( os.path.join(templatePath, "Properties"), os.path.join(projectPath, "Properties"))
            shutil.copy( os.path.join(templatePath, "spis-globals"), projectPath)
            shutil.copy( os.path.join(templatePath, "spis-names"), projectPath)
            shutil.copy( os.path.join(templatePath, "Tmp3D.msh"), projectPath)
            #cp -r $templatePath/simulationDeamon*
            
            # update of the project informations
            sharedFiles["project_directory"] = projectPath
            sharedFiles["projectSavingFlag"] = 1
        except:
            self.logger.error("Impossible to generate the project from the template")
            self.loggingUtilities.printStackTrace()
            return 0
        return 1