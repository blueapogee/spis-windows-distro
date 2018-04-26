
import sys
import traceback

class LoggingUtilities:
    
    def __init__(self, logger):
        self.logger = logger
    
    def printStackTrace(self):
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        self.logger.debug(repr(traceback.format_tb(exceptionTraceback)))
        self.logger.debug("       "+ repr( exceptionValue))