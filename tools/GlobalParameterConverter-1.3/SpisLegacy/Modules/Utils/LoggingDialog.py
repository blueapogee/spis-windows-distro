


class LoggingDialog:

    init(self):
        print "init"

    setContexte(context):
       
    setDialogPanel(self, errorMessage, message):
        if context == GRAPHICAL_INTERNAL:
           InternalFrame = create_internal_frame("Error",sharedFrames["gui"].getCurrentDesktop())
           dialogFrame = JOptionPane.showMessageDialog( InternalFrame, errorMessage, "Error in cell transtyping.", JOptionPane.ERROR_MESSAGE)
         else:
           print >> sys.stderr, "No visualisation cell type selected! Please select one before."
