"""
**File name:**    SpisTasks.py

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

# This script work partially under python. Please use jython to run
# tasks which raise exception under pyhton

# Task modules dependencies
import sys, os
sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH
sys.path.append(GL_SPISUIROOT_PATH)

# Task manager modules dependencies
from Bin.Tasks.Task           import Task
from Bin.Tasks.TaskManager    import TaskManager

# Autoload tasks modules
from Bin.Tasks import taskslist
for i in taskslist.tasks:
    exec "from %s import %s" % ("Task" + i[1], "Task" + i[1])

# Spis-task-builtins
from Bin.Tasks.TaskBuiltins import *

# Used to save all executed tasks
executed_tasks = []

class TaskTextGui(Task):
    """Special task"""
    desc = "Text User Interface"
    def __init__(self, name, tasks):
        Task.__init__(self, 1, name)
        self.tasks = tasks
        # Tell the Task manager, that we have a dependance graph stocked
        # in a list
        self.task_manager = TaskManager(*[i[0] for i in self.tasks])

    def __replay_tasks(self):
        print "You are going to run tasks:", executed_tasks
        print "Press enter to continue..."
        raw_input()
        for i in executed_tasks:
            self.task_manager.run_tasks(self.tasks[i][1])
            exec "tmp = Task" + self.tasks[i][1] + "(\"" \
                 + self.tasks[i][1] + "\")"
            self.task_manager.replace_task(tmp)

    def __print_banner(self):
        print
        for i in self.tasks:
            print "Task %2d: %s" % (self.tasks.index(i), i[0].desc)
        print "Task  a: Replay \"executed_tasks\" list"
        print "Task  q: Exit Task Manager"
        print
        print "Enter the task number:"

    def run_task(self):
        global executed_tasks
        control = "init"
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
                exec "tmp = Task" + self.tasks[int(control)][1] + "(\"" \
                     + self.tasks[int(control)][1] + "\")"
                self.task_manager.replace_task(tmp)
            except IndexError:
                print "input value error"
            except ValueError:
                print "input value error"

if __name__ == "__main__":
    from threading import Condition
    gui = TaskTextGui("TextGui", taskslist.tasks)
    gui.condition = Condition()
    gui.start()

