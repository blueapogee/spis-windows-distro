"""
System and helper applications configuration module. Please see user manual and
installation guid for more details.  

**File name:**    config.py

**Creation:**     2004/03/31

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais, Arsene Lupin, Yves Le Rumeur

:version:      3.5.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 1.0.0   | Maxime Biais                         | Creation                   |
|         | contact@artenum.com                  |                            |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Arsene Lupin                         | Creation                   |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+
| 3.1.0   | Yves Le Rumeur                       | Modif                      |
|         | lerumeur@artenum.com                 |                            |
+---------+--------------------------------------+----------------------------+
| 3.6.0   | Arsene Lupin                         | Modiications               |
|         | arsene.lupin@artenum.com             |                            |
+---------+--------------------------------------+----------------------------+


PARIS, 2000-2004, Paris, France, `http://www.artenum.com`_

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

.. _`http://www.artenum.com`: http://www.artenum.com
.. _`http://www.spis.org`: http://www.spis.org
"""
__docformat__ = "restructuredtext en"


# DO NOT EDIT THIS FILE
import sys,os, time, java 

print "Loading configuration... "
# to have a clean definition outside the if-case
GL_SPIS_VERSION       = 4.3
GL_SPIS_HOME          = None
GL_DEFAULT_INPUT_PATH = None
GL_DATA_PATH          = None
GL_SPISUIROOT_PATH    = None
GL_GMSH_OUT_PATH      = None
GL_CMD_MEDIT          = None
GL_CMD_GMSH           = None
GL_CMD_TETGEN         = None
GL_CMD_EDITOR         = None
GL_CMD_PARAVIEW       = None
GL_EXCHANGE           = None
GL_VTK_EXCHANGE       = None
GL_IMAGES_EXCHANGE    = None
GL_GEOM_WS_EXCHANGE   = None
GL_KERNEL_EXCHANGE    = None  # exchange directory path for additional SPIS-NUM files (e.g circuti.txt)
GL_DOC_PATH           = None
GL_CASSANDRA_PLUGINS  = None
GL_CMD_JSYNOPTIC      = None
GL_MAX_THREADS_STACK  = 4     #Maximum number of threads in same time, to adjust to nb CPUs
GL_SYSTEM             = None
GL_GUI_LOGGING_CONF   = None
GL_LOG_FILE_PATH      = None
GL_OS_NAME            = None
GL_BLOCK_SIZE         = 512  #Size of the block in the Jython serialisation
GL_MESH_STUDY         = None
GL_DEFAULT_WIZARD_PATH = None
GL_DEFAULT_TRACKS_TEMPLATES_PATH = None
GL_DEFAULT_GEOMETRIES_TEMPLATES_PATH = None
GL_DEFAULT_MATERIAL_TEMPLATES_PATH = None
GL_CURRENT_WIZARD_PATH = None

#print "GL_CURRENT_WIZARD_PATH=", GL_CURRENT_WIZARD_PATH

# now we deal with the systems
if sys.version == "2.1":
    system = os._getOsType()
else:
    system = os.get_os_type()
GL_SYSTEM = system
print 'System= '+GL_SYSTEM

GL_OS_NAME = java.lang.System.getProperty("os.name")
print 'OS name= '+GL_OS_NAME

GL_JAVA_HOME = sys.getBaseProperties()["java.home"]

print "----------------"
if java.lang.System.getenv()["SPIS_HOME"] != None:
    GL_SPIS_HOME = java.lang.System.getenv()["SPIS_HOME"]
elif java.lang.System.getProperty("spis.home") != None:
    GL_SPIS_HOME = java.lang.System.getProperty("spis.home")
else: 
    print "GL_SPIS_HOME not set, use default package structure."
print GL_SPIS_HOME
print "----------------"

if system == 'posix':
    ##################################################################
    #             Settings for UNIX based systems                    #
    ##################################################################
   
    #in order to have always a directory to write
    user = os.getenv('USER')
    print 'user= '+user
    t = str(int(time.time()))
    tmpDir = "/tmp/"+user+"spistmp"+t+"/"
    print "Tmp files directory= "+tmpDir
    os.mkdir(tmpDir)
    GL_EXCHANGE = tmpDir
   
    # for the VTK files exchanges
    GL_VTK_EXCHANGE = os.path.join(tmpDir, "Vtk")
    os.mkdir(GL_VTK_EXCHANGE)
   
    # for the geom (CAD) files workspace 
    GL_GEOM_WS_EXCHANGE = os.path.join(tmpDir, "Geom")
    os.mkdir(GL_GEOM_WS_EXCHANGE)
   
    GL_IMAGES_EXCHANGE = os.path.join(tmpDir,"Images")
    os.mkdir(GL_IMAGES_EXCHANGE)
   
    GL_SYNOPTIC_EXCHANGE = filename = os.path.join(tmpDir, "synoptic")
    os.mkdir(GL_SYNOPTIC_EXCHANGE)
   
    GL_MESH_STUDY = os.path.join(tmpDir,"MeshStudy")
    os.mkdir(GL_MESH_STUDY)

    if GL_SPIS_HOME != None:
        GL_SPISUIROOT_PATH = GL_SPIS_HOME+os.sep+"SpisUI"
    else:
        GL_SPISUIROOT_PATH = r"../SpisUI/"
    print GL_SPISUIROOT_PATH
    GL_DEFAULT_INPUT_PATH = r"../SpisUI/DefaultValues/"
   
    GL_DATA_PATH = tmpDir
    GL_GMSH_OUT_PATH = tmpDir

    if GL_OS_NAME == "Mac OS X":
        GL_CMD_GMSH = r"../ThirdPart/Gmsh/MacOSX/gmsh-2.4.2/Gmsh.app/Contents/Resources/bin/gmsh"
    else:
        #GL_CMD_GMSH = r"../ThirdPart/Gmsh/Linux-I386/gmsh-2.4.2/gmsh"
        GL_CMD_GMSH = r"../ThirdPart/Gmsh/Linux/x86_64/gmsh-2.4.2-linux-x86_64-glibc2_5/bin/gmsh.sh"

    GL_CMD_MEDIT = r"../ThirdPartx/medit-2.2-linux"
    GL_CMD_TETGEN = r"../ThirdPart/tetgen"

    CLASSPATH = java.lang.System.getProperty("java.class.path")
    GL_CMD_EDITOR = GL_JAVA_HOME+"/bin/java -Xmx32m -classpath "+CLASSPATH+" org.jext.Jext"
    GL_CMD_JSYNOPTIC = GL_JAVA_HOME+"/bin/java -classpath "+CLASSPATH+" jsynoptic.ui.Run"

    GL_CMD_PARAVIEW = r"../ThirdPart/Paraview/I386-Linux/bin/paraview"
    GL_DOC_PATH = "../Doc"
   
    if GL_OS_NAME == "Mac OS X":
        GL_CMD_DOCVIEWER = r"/Applications/Safari.app/Contents/MacOS/Safari "
    elif GL_OS_NAME == "Linux":
        GL_CMD_DOCVIEWER = r"firefox "
    else:
        GL_CMD_DOCVIEWER = r"../ThirdPart/JVM/Linux-I386/jre/bin/java -jar ../ThirdPart/Multivalent/Multivalent20040415.jar"
else:
    ##################################################################
    #             Settings for Windows based system                  #
    ##################################################################
        
    #system =='windows':
    GL_SPISUIROOT_PATH = r"..\\..\\SpisUI\\"
    #print "GL_SPISUIROOT_PATH = " + GL_SPISUIROOT_PATH
 
    #Setting of the exchange disk
    DISK = "C"

    # to recover the tmp directory
    #tmpDirRoot=os.getenv('TMP')
    #tmpDirRoot=DISK+":\\"
    tmpDirRoot = sys.environ["TMP"]
   
    t = str(int(time.time()))
    tmpDirExt="spistmp"+t
    tmpDir=tmpDirRoot+tmpDirExt+"\\"
    os.mkdir(tmpDir)

    GL_DATA_PATH = tmpDir
    GL_EXCHANGE = tmpDir
    GL_DEFAULT_INPUT_PATH = GL_SPISUIROOT_PATH + "DefaultValues\\"

    # for the VTK files exchanges
    GL_VTK_EXCHANGE = tmpDir+"\Vtk\\"
    os.mkdir(GL_VTK_EXCHANGE)

    # geom (CAD) exchange workspace
    GL_GEOM_WS_EXCHANGE = tmpDir+"\Geom\\"
    os.mkdir(GL_GEOM_WS_EXCHANGE)
   
    GL_IMAGES_EXCHANGE = tmpDir+"/Images/"
    os.mkdir(GL_IMAGES_EXCHANGE)

    GL_SYNOPTIC_EXCHANGE = filename = os.path.join(tmpDir, "synoptic")
    os.mkdir(GL_SYNOPTIC_EXCHANGE)
   
    GL_MESH_STUDY = os.path.join(tmpDir,"MeshStudy")
    os.mkdir(GL_MESH_STUDY)

    print "Tmp files directory= "+GL_DATA_PATH
    # because gmsh use cygwin under windows and does not support 
    # the back slash
    #GL_GMSH_OUT_PATH = "/cygdrive/"+DISK+"/"+tmpDirExt
    # This is not true anymore woth gmsj 1.60 and higher
    GL_GMSH_OUT_PATH = GL_EXCHANGE
    GL_CMD_GMSH = os.path.join(GL_SPISUIROOT_PATH, "..", "ThirdPart", "Gmsh", "Windows", "gmsh-2.4.2-Windows", "gmsh.exe ")

    GL_CMD_PARAVIEW = os.path.join(GL_SPISUIROOT_PATH, "..", "ThirdPart", "Paraview", "Windows", "ParaView", "bin", "paraview.exe")
    CLASSPATH = java.lang.System.getProperty("java.class.path") 
    GL_CMD_EDITOR = os.path.join(GL_SPISUIROOT_PATH, "..", "ThirdPart", "JVM", "Windows", "jre", "bin", "java.exe ") + "-Xmx32m -classpath "+CLASSPATH+" org.jext.Jext"
    GL_DOC_PATH = "..\..\..\Doc"
    GL_CMD_DOCVIEWER_WIN1 = r'C:\\Program Files\\Mozilla FireFox\\firefox.exe'
    GL_CMD_DOCVIEWER_WIN2 = r'C:\\Program Files\\Internet Explorer\\iexplorer.exe'
    GL_CMD_DOCVIEWER = None
  
################################################## 
# Non OS dependent settings
##################################################
   
GL_CASSANDRA_PLUGINS = os.path.join(GL_SPISUIROOT_PATH, "..", "ThirdPart", "Cassandra-2.4.02", "plugin")

GL_KERNEL_EXCHANGE = os.path.join(tmpDir,"Kernel", "") # The last item is only to add an extra os sep, because SPIS-NUM does not cat properly the paths
os.mkdir(GL_KERNEL_EXCHANGE)
   
# initialisation of default values

#if sharedFiles['projectNumElmFlag'] == None or sharedFiles['projectNumElmFlag'] == 0:
NUM_PARAM_PATH = os.path.join(GL_SPISUIROOT_PATH, "DefaultValues")

# GUI settongs
GL_GUI_XLM_RESSOURCES_MENU = os.path.join(GL_SPISUIROOT_PATH, "AuxLibs", "resource", "SpisMenu.xml")
GL_GUI_XLM_RESSOURCES_TOOL_BAR = os.path.join(GL_SPISUIROOT_PATH, "AuxLibs", "resource", "SpisToolBar.xml")

# Logging system settings
GL_GUI_LOGGING_CONF = os.path.join(GL_SPISUIROOT_PATH, "AuxLibs", "resource", "log4j.xml")

GL_LOG_FILE_PATH = os.path.join(GL_EXCHANGE)

GL_DEFAULT_GEOMETRIES_TEMPLATES_PATH = os.path.join(GL_SPISUIROOT_PATH, "Templates", "Geometries")
GL_DEFAULT_TRACKS_TEMPLATES_PATH = os.path.join(GL_SPISUIROOT_PATH, "Templates", "Tracks")
GL_DEFAULT_WIZARD_PATH = os.path.join(GL_SPISUIROOT_PATH, "Templates", "Wizards")
GL_DEFAULT_MATERIAL_TEMPLATES_PATH = os.path.join(GL_SPISUIROOT_PATH, "Templates", "Materials")

