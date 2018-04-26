
from org.slf4j                          import Logger
from org.slf4j                          import LoggerFactory

class ModulesLogger():
    
    def __init_(self):
        
        # building of the related logger
        self.logger = LoggerFactory.getLogger("ModulesLogger")
        self.logger.info("ModulesLogger initialised")