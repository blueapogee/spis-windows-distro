
                    SPIS 5.2.4 2017/02/20
     SPIS-UI Integrated Modelling Environnement (SPIS-UI IME)

             Spacecraft Plasma Interaction Software
                  see: http://www.spis.org


    The Spacecraft Plasma Interaction System, SPIS, is a simulation software
 based on an electrostatic 3D unstructured Particle-In-Cell plasma model and
 consisting of a JAVA based highly modular Object Oriented library, called
 SPIS/NUM. SPIS is designed to be used for a broad range of industrial and
 scientific applications.
 	The simulation kernel is integrated into a complete modular
 pre-processing/computation/postprocessing framework, called SPIS/UI, allowing
 a high degree of integration of external tools, such as CAD, meshers and
 visualization libraries, and a very easy and flexible access to each level of
 the numerical modules via the Jython script language. Developed in an Open
 Source approach, SPIS is available for the whole community and is used by
 members of the European SPINE network.
  
 
Please, contact the SPIS TEAM for further information: 
 
         contact [at] spis.org

I) Run the application: 

        	- Spis.sh 
			- SpisGeo.sh
        	- SpisDust.sh

See documentation for more information


II) Known bugs:

A) On some Windows systems, the generation of the unique name for the cache
directory, based on a unique time stamp, may fail. In that case, the name of
the cache directory must be defined manually by editing the launching script
as follows.

1) Open the Spis.bat file with the text editor of your choice

2) The first line of the script file corresponds to the definition of the
unique time stamp:

set NOW=%date:~-4,4%%date:~-7,2%%date:~-10,2%%time:~-11,2%%time:~-8,2%%time:~-5,2%%time:~-2,2%

On some Windows systems, this line generates spaces in the variable name that
prevent the execution script from working properly. In this case, replace this
line by the following:
set NOW=1

!!! Beware that if you run several SPIS instances simultaneously, the value of
the NOW variable should differ for each execution


B) Some OS do not support files whose name contains a long chain of characters.
To avoid that, it is recommended to create the SPIS projects in a short
arborescence tree, as for instance C:/SpisProjects".

C) SPIS uses Gmsh as CAD engine and mesher. Gmsh is a native component that
depends on the targeted platform (OS and hardware architecture). On some OS,
Gmsh may also depend on related external libraries (e.g. glibc, Fltk...). For
these reasons, the CAD import/loading may fail if Gmsh does not run properly.
In this case, please install manually a version of Gmsh appropriate to target
plateform (see http://geuz.org/gmsh/) and set the corresponding path as described
in Software User Manual (section 9.4-Property file and configuration of native
components) to fix such troubleshooting. As a rule of thumb, gmsh version 2.4.2
was adapted to most tested platforms.

D) There have been some problems launching SPIS 5 on some Windows 7 Enterprise
64 bits: the launch time of SPIS can take up to 10 minutes.

This wad to be due to McAfee antivirus that prevents SPIS from starting properly.

It can be verified by launching Windows "Task Manager" and looking in the
"Processes" tab while starting SPIS. Upon SPIS startup, the task associated
with McAfee software (called "McShield") takes 100% of processor usage.
Stopping SPIS stops this "McShield" task.

Disabling McAfee solves the problem and SPIS startup is then instantaneous. To
disable McAfee, right-click on McAfee logo at the bottom right of the task bar
and select "disable scan". This is however a temporary fix and this is not
recommended on the long term as the computer will be vulnerable to viruses. A
more sustainable solution will have to be fixed in the future to allow SPIS
running properly with any antivirus.

E) Some OS do not support file or directory name that include spaces. It is
recommended to remove any of them from your project arborescence tree, project
name, mesh file name, geometrical file name, etc...


Done at Toulouse, France, 20th of February 2017.
