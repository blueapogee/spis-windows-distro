"""
Main module of SPIS-UI. This module will start the Tasks Manager and 
all relevant modules. 

**File name:**    SpisTasksGraph.py

**Creation:**     2004/03/24

**References:** Please see the SPIS web site `http://www.spis.org`_ for
more information.

:author:       Maxime Biais

:version:      3.0.0

**Versions and anomalies correction :**

+---------+--------------------------------------+----------------------------+
| Version | Author (name, e-mail)                | Corrections/Modifications  |
+---------+--------------------------------------+----------------------------+
| 3.0.0   | Maxime Biais                         | Creation                   |
|         | maxime.biais@artenum.com             |                            |
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
# </autoheader> rewritten

# Java interface
import java

from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_DATA_PATH, GL_GUI_XLM_RESSOURCES_MENU, GL_GUI_XLM_RESSOURCES_TOOL_BAR,GL_GUI_LOGGING_CONF,GL_LOG_FILE_PATH

from org.slf4j import Logger
from org.slf4j import LoggerFactory

import org.apache.log4j.xml
from org.apache.log4j.xml import DOMConfigurator

# loading of the logging configuration system 
# (should be done here in order to have the logging infrastructure ASAP)
import org.spis.imp.ui.shared.SharedContext
sharedContext = org.spis.imp.ui.shared.SharedContext()
sharedContext.filePaths.put("GL_LOG_FILE_PATH", GL_LOG_FILE_PATH)
DOMConfigurator.configure(GL_GUI_LOGGING_CONF);
#print "-------------->GL_GUI_LOGGING_CONF= "+GL_GUI_LOGGING_CONF



from org.spis.imp.jui import SpisGUI
from org.spis.imp     import JCondition

from copy import copy
from threading import Condition
import pawt
#from Console import Console

# Task modules dependencies
import sys, os, getopt

sys.path.append(GL_SPISUIROOT_PATH)
sys.path.append(GL_SPISUIROOT_PATH+os.sep+"Scripts")

#import RenderWindows
from Bin.Tasks.shared import sharedFrames, sharedTasks, sharedFlags
import Bin.Tasks.common
from Bin.Tasks.common import build_task_str, ask_yesno

#for outputs and project directory
from Bin.Tasks.shared import sharedFiles

# Task manager modules dependencies
from Bin.Tasks.Task           import Task

# Autoload tasks modules
import Bin.Tasks.taskslist
from Bin.Tasks.taskslist import TasksList
taskslist = TasksList()

# Spis-task-builtins
from TaskBuiltins import *

from Modules.Utils.TrackManager import TrackManager

# Used to save all executed tasks
executed_tasks = []

class TaskController(Exception):
    pass

class EventHandler:
    def __init__(self):
        self.exeption = {13 : self.showGUI}

    def ask_redo(self):
        tmpcond = Condition()
        res = ask_yesno(tmpcond, "Called task is already done, want you to redo it ?")
        if res == "n" or res == "N":
            return 0
        return 1

    def special(self, tasks, manager, msg):
        if msg == "reset_done_tasks":
            print "Done tasks reseted"
            manager.reset_done_nodes()
        elif msg == "toggle_simulate_mode":
            print "Simulate mode is",
            print manager.toggle_simulate_mode()

    def default(self, tasks, manager, task_id):
        if task_id in self.exeption.keys():
            self.exeption[task_id]()
            return
        self.tmpcond = Condition()
        tasks[task_id][0].setGUI(self.tmpcond)
        if manager.is_done_task(tasks[task_id][0].name):
            if self.ask_redo() == 0:
                print >> sys.stderr, "OK, I do not redo it... watch your clicks !"
                return
            manager.set_todo_task(tasks[task_id][0].name)
        # set all node to "not done = to do"
        # manager.reset_done_nodes()
        executed_tasks.append(int(task_id))
        manager.run_tasks(tasks[int(task_id)][1])
        #print "In default, task_name= "
        #print task_name
        manager.respawn_done_tasks()
        self.tmpcond = Condition()
        # tmp.setGUI(self.tmpcond)
        
        # update of the title of the main frame
        if ( (sharedFrames["gui"] != None) and (sharedFiles["project_directory"] != None)):
            sharedFrames["gui"].updateTitle(sharedFiles["project_directory"])

    def setEventQueue(self, e):
        self.event_queue = e

    def showGUI(self):
        sharedFrames["console"].show()

class TaskGui(Task):
    """Built-in task called in first to build up the Graphical User Interface"""
    desc = "Text User Interface"


    def __init__(self, name, tasks, handler):
        Task.__init__(self, 1, name)

        print 'Building of the graphical user interface.....  '

        self.spisGuiMenu = GL_GUI_XLM_RESSOURCES_MENU
        print self.spisGuiMenu
        self.spisGuiToolBar = GL_GUI_XLM_RESSOURCES_TOOL_BAR
        print self.spisGuiToolBar
        
        self.special_msg = [ "reset_done_tasks", "toggle_simulate_mode" ]
        print 'Building of the tasks manager.....   '
        self.tasks = tasks
        sharedTasks["tasks"] = self.tasks
        
        # Tell the Task manager, that we have a dependance graph stocked
        # in a list
        from Bin.Tasks.TaskManager  import TaskManager
        self.task_manager = TaskManager(*[i[0] for i in self.tasks])
        sharedTasks["manager"] = self.task_manager
                
        # create objects for interfacing Java Swing GUI
        self.event_queue = []
        self.old = []
        self.cond = JCondition()
            
        print "Initialisation of the main GUI..."
        self.myframe = SpisGUI( self.event_queue, self.cond, [ self.spisGuiMenu, self.spisGuiToolBar], globals())
        self.myframe.setSize(1024,700)
        self.myframe.setLocationRelativeTo(None)

        # building of the related logger
        print "Initialisation of the main GUI logger..."
        logger = LoggerFactory.getLogger("TaskGui")
        
        sharedTasks["event_queue"] = self.event_queue
        sharedTasks["event_cond"] = self.cond
        sharedFrames["gui"] = self.myframe
        

        print 'Initialisation of the Spis console.... '
        if (sharedFiles["project_directory"] != None):
            self.log_filename =  os.path.join(sharedFiles["project_directory"], "spis_gui.log")
        else:
            self.log_filename = os.path.join(GL_DATA_PATH, "spis_gui.log")
        print 'Initialisation of the events handler.... '
        self.event_handler = handler
        

    def show(self):
        try: 
            self.myframe.show()
            sys.stdwarn = stdwarn
        except:
            print "Impossible to show the main GUI."
        
        
    def get_task_id(self, task_name):
        j = 0
        for i in self.tasks:
            if i[1] == task_name:
                return j
            j += 1
        return -1


    def run_task(self):
        '''
        Execute the tasks listed in the tasklist (controled by the event queue)
        '''
        while 1:
            self.cond.wait_for_signal()
            if self.old != self.event_queue:
                for i in self.event_queue[-1:]:
                    if i in self.special_msg:
                        self.event_handler.special(self.tasks, self.task_manager,i)
                    else:
                        task_id = int(self.get_task_id(i))
                        print task_id
                        if task_id != -1:
                            self.event_handler.default(self.tasks, self.task_manager, int(self.get_task_id(i)))
                        else:
                            print >> sys.stderr, "MessageIntegrityChecker: Received message <%s> not understandable" % i
                    self.event_queue.remove(i)
                self.old = copy(self.event_queue)


    def __replay_tasks(self):
        print "You are going to run tasks:", executed_tasks
        print "Press enter to continue..."
        raw_input()
        for i in executed_tasks:
            self.task_manager.run_tasks(self.tasks[i][1])
            exec "tmp = " + build_task_str(tasks, task_id)
            self.task_manager.replace_task(tmp)

    def __print_banner(self):
        print
        for i in self.tasks:
            print "Task %2d: %s" % (self.tasks.index(i), i[0].desc)
        print "Task  a: Replay \"executed_tasks\" list"
        print "Task  q: Exit Task Manager"
        print
        print "Enter the task number:"


    def run_task2(self):
        global executed_tasks
        control = "init"
        print 'error'
        while 1:
            self.__print_banner()
            control = raw_input()
            self.task_manager.reset_done_nodes()
            if control == "q":
                break
            if control == "a":
                self.__replay_tasks()
                continue
            try:
                executed_tasks.append(int(control))
                self.task_manager.run_tasks(self.tasks[int(control)][1])
                exec "tmp = " + build_task_str(tasks, task_id)
                self.task_manager.replace_task(tmp)
            except IndexError:
                print "input value error"
            except ValueError:
                print "input value error"

                
class Main:
    def usage(self):
        print """%s: usage:
    -h, --help            - print this help message and exit
    -g, --graphical       - run the GUI
    -b FILE, --batch=FILE - run spis in batch mode, set the batch file
    -p FILE, --proj=FILE  - pre-set the project gieven in argument
    """ % sys.argv[0]


    def main(self):
        """
        Main method. 
        """                
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                       "hb:gG:p:",
                                       ["help", "batch", "graphical","geom","proj"])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)
        t_batch = 0
        t_graphical = 0
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
                sys.exit()
            if o in ("-b", "--batch"):
                print "Track file used for the batch: %s" % a
                t_batch = 1
                taskslist.isDeamon = 0
                taskslist.initTasksList()
                self.batch(a)
            if o in ("-g", "--graphical"):
                t_graphical = 1
                #self.graphical()
            if o in ("-G", "--geom"):
                print opts
                print args
                sharedFiles['TheCADFileIn'] = args[0]
            if o in ("-p", "--proj"):
                print opts
                print args
                sharedFiles['project_directory'] = args[0]
                print "sharedFiles['project_directory']  ----------->", sharedFiles['project_directory']

        if t_batch == 0 or t_graphical == 1: 
            #taskslist.isDeamon = 0
            taskslist.initTasksList()
            self.graphical()

    def batch(self, deamonFile):
        """
        run in batch mode.
        """
        
        sharedFlags['guiMode'] = 0
        sys.stdwarn = sys.stdout

        print 'Building of the tasks manager.....   '
        self.tasks = taskslist.tasks
        sharedTasks["tasks"] = self.tasks

        # Tell the Task manager, that we have a dependence graph stocked
        # in a list
        from Bin.Tasks.TaskManager    import TaskManager
        self.task_manager = TaskManager(*[i[0] for i in self.tasks])
        self.task_manager.reset_done_nodes()
        sharedTasks["manager"] = self.task_manager
       
        # 
        deamonPath = os.path.dirname(deamonFile)
        print "Daemon path in SPIS: ", deamonPath
       
        
        # Read and execute input file         
        tracker = TrackManager()
        tracker.loadTrack(deamonFile)
        tracker.setInLinedFlagFromLoadedTrack()
        if (tracker.checkLoadedTrackVersion()):
            tracker.processLoadedTrack()
            self.logger.info("Spis Track processed successfully")
        else:
            if (self.BY_PASS_VALIDATION):
                self.logger.warn("Track version validation by-passed")
                tracker.processLoadedTrack()
                self.logger.info("Spis Track processed successfully")
            else:
                self.logger.info("Spis Track no processed")
 
        print "End"
        sys.exit()


    def graphical(self):
        
        gui = TaskGui("Gui", taskslist.tasks, EventHandler())
        gui.show()
        gui.condition = Condition()
        gui.start()

if __name__ == "__main__":
    main = Main()
    main.main()
    
