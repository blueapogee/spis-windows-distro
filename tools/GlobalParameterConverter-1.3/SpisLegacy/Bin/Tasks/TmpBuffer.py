
class TmpBuffer:
        def __init__(self):
                self.line = [] 

        def flush(self):
                pass

        def write(self, text):
                self.line = text
                return text

        def getText(self):
                return self.line

