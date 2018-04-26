"""
**File name:**    TaskManager.py

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

# -*- coding: iso-8859-1 -*-

import time
import sys
import os

from Bin.Tasks.shared     import sharedTasks
from Bin.Tasks.Task       import Task
from threading            import Condition
from Bin.Tasks.common     import build_task_str_single

from Bin.Tasks.common     import create_internal_frame
from javax.swing          import *

from org.spis.imp.ui.util import ProgressBox
from Bin.Tasks.shared     import sharedFrames, sharedFlags

# Autoload tasks modules
#import Bin.Tasks.taskslist
#from Bin.Tasks.taskslist import TasksList
#taskslist = TasksList()

#taskslist.isDeamon = 0
#taskslist.initTasksList()

#####  FIX ME
for i in sharedTasks["tasks"]:
    exec "from %s import %s" % ("Task" + i[1], "Task" + i[1])

#
# WARNING !!! "start" and "end" rules are specials, don't call your
# own task start or end.
#


class TaskManagerException(Exception):
    pass

class TaskManager:
    '''
    Central Task Manager of SPIS-UI. The Task Manager is the kernel of SPIS-UI which 
    performs tasks according to the the dependence tree described into the tasklis.py 
    module. Please the User Manual and/or the corresponding Technical Note for 
    further information. 
    '''
    
    def __init__(self, *tasks):
        """
        Constructor, take tasks that will create the base graph
        """
        if tasks is not None:
           self.tasks = {}
           for task in tasks:
               self.tasks[task.name] = task
           self.build_successors()
           self.simulate = 0
    '''  
    def setTaskList(self, taskListIn):
        for i in taskListIn:
            exec "from %s import %s" % ("Task" + i[1], "Task" + i[1])
    '''    
        
    def initTaskList(self, *tasks):
        '''
        Initialises the dependence tree defined by the task list.
        '''
        self.tasks = {}
        for task in tasks:
            self.tasks[task.name] = task
        self.build_successors()
        self.simulate = 0

    def set_simulate_mode(self, t):
        '''
        Switch the dependence mechanism into simulation mode if 
        the t value equal 1.
        '''
        self.simulate = t

    def toggle_simulate_mode(self):
        if self.simulate == 0:
            self.simulate = 1
        else:
            self.simulate = 0
        return self.simulate

    def is_simulate_mode(self):
        '''
        returns the status of the simulation mode. 
        '''
        return self.simulate

    def set_todo_task(self, task_name):
        '''
        Set task_name as to do . Usefull to shortcut the 
        dependence tree and force a task to be performed again. 
        If the task is considered as done (i.e equal to 1), it 
        will NOT recalled automatically by the dependency graph.
        If the done flag is set to 0, the task will be recalled 
        automatically by the dependency graph. 
        '''
        self.tasks[task_name].done = 0

    def set_done_task(self, task_name):
        '''
        Set task_name as done. Usefull to shortcut the
        dependence tree and set a task as already performed.
        If the task is considered as done (i.e equal to 1), it 
        will NOT recalled automatically by the dependency graph.
        '''
        self.tasks[task_name].done = 1

    def is_done_task(self, task_name):
        '''
        return the status (done or not) of task_name.
        '''
        return self.tasks[task_name].done

    def remove_task(self, task_name):
        """
        Remove a task from the graph and update successors
        """
        try:
            del self.tasks[task_name]
        except KeyError:
            raise TaskManagerException("Task %s does not exist" % task_name)
        # FIXME: don't re-build unconnected nodes (use frames system based)
        # http://www.ai.mit.edu/people/minsky/papers/Frames/frames.html

    def add_task(self, task):
        """
        add a task into the graph and update successors
        """
        self.tasks[task.name] = task
        self.build_successors()


    def respawn_done_tasks(self):
        
        for task_name in self.tasks.keys():
            cur_task = self.tasks[task_name]
            if cur_task.done == 1:
                to_exec =  "tmp = " + build_task_str_single(cur_task)
                exec to_exec
                self.replace_task(tmp)
                tmp.done = 1

    def replace_task(self, task):
        """
        Replace a task in the graph by the new object task. (call
        remove_task an add_task successivly)
        """
        self.remove_task(task.name)
        self.add_task(task)

    def reset_succ_nodes(self):
        """
        Reset the successors list for each node of the graph
        """
        for task in self.tasks.keys():
            task.succ = []

    def build_successors(self):
        """
        Build the successor list for each node
        """
        for task in self.tasks.keys():
            for pred in self.tasks[task].pred:
                self.tasks[pred[0]].succ.append((task, pred[1]))

    def add_nodes(self):
        """
        Add the -start- and -end- nodes into the graph. These nodes
        are used to ensure the good scheduling of tasks: see the
        algorithm explanation for more details.
        """
        self.tasks["start"] = Task("start")
        self.tasks["end"] = Task("end")
        for task in self.tasks.keys():
            if self.tasks[task].useful == 0:
                continue
            if not self.tasks[task].pred and task != "start" and task != "end":
                self.tasks[task].pred = [("start", 0)]
                self.tasks["start"].succ.append((task, 0))
            if not self.tasks[task].succ and task != "start" and task != "end":
                self.tasks[task].succ = [("end", 0)]
                self.tasks["end"].pred.append((task, 0))

    def reset_useful_nodes(self):
        """
        Set the useful attribute to 0 for each nodes of the graph
        """
        for task in self.tasks.keys():
            self.tasks[task].useful = 0

    def reset_done_nodes(self):
        """
        Set the done attribute to 0 for each nodes of the graph
        """
        for task in self.tasks.keys():
            self.tasks[task].done = 0

    def set_useful_nodes(self, task_name):
        """
        Recursivly Set 1 to all the nodes needed to complete the task
        called task_name.
        Follow the successor on the graph beginning from task_name and
        set useful attribute to 1 when a node.
        """
        self.tasks[task_name].useful = 1
        for pred in self.tasks[task_name].pred:
            self.set_useful_nodes(self.tasks[pred[0]].name)

    def schedule(self, task_name):
        """
        Create the schedule list

        with the graph:   A----->C---->D
                                /
                          B-----

        This function will return [[A, B], [C], [D]] because A and B are 2
        tasks which may be executed in the same time
        """
        tmp = []
        res = []
        groups = []
        for task in self.tasks.keys():
            self.get_date(self.tasks[task])
            tmp.append(self.tasks[task])
        tmp.sort()
        cur_date = 0
        j = 0
        while j < len(tmp):
            if tmp[j].date == cur_date:
                if tmp[j].name != "start" and tmp[j].name != "end" \
                       and tmp[j].useful == 1:
                    groups.append(tmp[j])
                j += 1
            else:
                res.append(groups)
                groups = []
                cur_date += 1
        res.append(groups)
        return res

    def check_running_task(self, task_list):
        """
        Check if there is one or more tasks currently running. return
        1 if there is no task running, 1 else.
        """
        for task in task_list:
            if task.done == 0:
                return 0
        return 1

    def print_ord(self, ord):
        if len(ord) == 1:
            return
        #print >> sys.stderr, "------ <flattened_dependency_graph> -------"
        for squadron in ord:
            if squadron != []:
                #print >> sys.stderr, "[",
                for task in squadron:
                    #print >> sys.stderr, task.name,
                    if task.done == 1:
                        print >> sys.stderr, "(already done)",
                #print >> sys.stderr, "]"
        #print >> sys.stderr, "------ </flattened_dependency_graph> ------"

    def stopTask(self, dummy):
        print "TOKILL", self.tokill
        for i in sharedTasks["tasks"]:
            print "Cur", i[1]
            if i[1] == self.tokill:
                i[0].__notify_end()
                i[0]._Thread_stop()
                print "KILLED", i[1]
        
    def run_tasks(self, task_name):
        """
        Run task named task_name and all needed dependencies (warning
        tasks that already been ran must be replaced: a Thread
        subclass, 0, "CADImporter" can be ran only one time: see
        section -7.5.6 Thread Objects, start() method- in the python
        library reference)
        """
        
        textMessage = "Processing task: "+task_name

        if sharedFlags['guiMode']:
            barBox = ProgressBox(sharedFrames["gui"],"Please wait: " + task_name, textMessage)
            self.tokill = task_name
            
            # for future controle
            #stopBox = create_internal_frame("stop box", sharedFrames["gui"].getCurrentDesktop())
            #stopBox.reshape(0, 0, 300, 580)
            #self.stopButton = JButton("Stop task", actionPerformed = self.stopTask)
            #panel = JPanel()
            #panel.add(self.stopButton)
            #stopBox.contentPane.add(panel)
            #stopBox.setVisible(1)
            
        self.reset_useful_nodes()
        self.set_useful_nodes(task_name)
        self.add_nodes()
        ord = self.schedule(task_name)
        self.print_ord(ord)
        if self.simulate == 1:
            return
            
        nbTaskToRun = 0
        for squadron in ord:
            for task in squadron:
                # run the tasks
                if task.done == 0:
                   nbTaskToRun = nbTaskToRun+1

        if nbTaskToRun > 1 :
            if sharedFlags['guiMode']:
                barBox.setNumberOfStep(nbTaskToRun)
            
        print "Number of task to run: ", nbTaskToRun
        
        for squadron in ord:
            condition = Condition()
            # set the condition object to all the task
            for task in squadron:
                task.condition = condition
                # run the tasks
                if task.done == 0:
                    task.start()
                if sharedFlags['guiMode']:
                    barBox.updateMessage(task.name)
                
            while self.check_running_task(squadron) == 0:
                condition.acquire()
                # OSBUG: let the os refresh thread list (1 micro
                # second should be sufficient but 0.001 second is not
                # perceptible and more securre)
                condition.wait(0.1)
                condition.release()
            
            if sharedFlags['guiMode']:
                barBox.nextStep()
        #stopBox.dispose()
        #stopBox = None
        
        if sharedFlags['guiMode']:    
            barBox.dispose()

    def get_date(self, task):
        """
        Recursivly set the date to run for a task.
        """
        if task.date == -1:
            for pred in task.pred:
                if self.tasks[pred[0]].date == -1:
                    self.get_date(self.tasks[pred[0]])
            task.date = 0
            for pred in task.pred:
                if self.tasks[pred[0]].date + pred[1] > task.date:
                    task.date = self.tasks[pred[0]].date + pred[1]

    def generate_dotty_out(self, stream, print_single=0):
        def gen_header(stream):
            stream.write("""digraph finite_state_machine {
 rankdir=LR;
 size="8,5"
 node [shape = circle];
""")
        def gen_footer(stream):
            stream.write("}")
        gen_header(stream)
        for task in self.tasks.values():
            if print_single:
                stream.write(" %s;\n" % task.name)
            for pred in task.pred:
                stream.write(" %s -> %s [ label =\"%i\"];\n" %
                             (task.name, pred[0], pred[1]))
        gen_footer(stream)
        stream.flush()                     

    def __str__(self):
        """
        Pretty print the tasks list.
        """
        res = ""
        for i in self.tasks:
            res += str(self.tasks[i])
        return res
