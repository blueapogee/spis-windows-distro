"""
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

import pawt
import sys
import os
import traceback
from threading          import Thread, Condition
from Bin.Tasks.common   import ask_value

from org.slf4j             import Logger
from org.slf4j             import LoggerFactory

class TaskException(Exception):
    pass

# Hack for jython-2.1 threading
_counter = 0
def _newid():
    global _counter
    _counter = _counter + 1
    return _counter

class Task(Thread):
    '''
    Generic container for SPIS-UI module. All processing modules 
    should be embeded in a Task inherited from this class. 
    '''
    def __init__(self, name, daemonic = 0, *tasks):
        """
        Constructor
        @arg name: The name of the task
        @arg daemonic: true if the task is daemonic
        @arg tasks: Names of the task dependencies
        """
        Thread.__init__(self, name=name)
        self.daemonic = daemonic
        self.setDaemon(self.daemonic)
        
        self.coreLogger = LoggerFactory.getLogger("Task")

        # Task name
        self.name = name
        # Predecessors list
        self.pred = []
        # Successors list
        self.succ = []
        # done = 1 when task is completed
        self.done = 0
        # useful = 1 when task is a dependency of another or if the
        # task is called to run
        self.useful = None
        # condition is use internally to tell the MainThread if the
        # task is running or not
        self.condition = None
        if name == "start" or name == "end":
            self.date = 0
        else:
            self.date = -1
        for task in tasks:
            self.pred.append((task, 1))
        # jython threading hack
        self.id = _newid()
        self.mycond = Condition()
        # 1 if the task is running, 0 else
        self.running = 0
        
        # building of the related logger
        self.logger = LoggerFactory.getLogger("Task")
        #self.logger.debug("Task initialised")
        
    def __hash__(self):
        """
        Two Task objects are identical if these tasks are the same
        instance (ie. they have the same id). Used to force correct
        run of jython Threaded objects.
        """
        return self.id

    def __notify_end(self):
        self.condition.acquire()
        self.condition.notifyAll()
        self.condition.release()
        self.done = 1

    def run(self):
        """
        Wrapper for the run_task method, handle raised exception in
        the task and notify the main thread when the task is finished.
        """
        if not self.id:
            raise TaskException("Constructor must be called before run")
        if self.condition == None:
            raise TaskException("Condition must be set before run")
        print "task %s begins" % self.name
        self.running = 1
        if self.daemonic:
            self.__notify_end()
        try:
            self.run_task()
        except:
            self.coreLogger.error("Exception raised in task" +self.name + "\n" +"Task aborted!")
            print ">>>>>> Exception raised in task <%s>" % self.name
            print ">>>>>> BEGIN TASK EXCEPTION HANDLING"
            #self.coreLogger.debug(traceback.format_tb(exceptionTraceback))
            traceback.print_exc(file = sys.stdout)
            print ">>>>>> END TASK EXCEPTION HANDLING"
            #pawt.swing.JOptionPane.showMessageDialog(None, "Exception raised in task ")
            #print "Exception raised in task "+self.name
        if not self.daemonic:
            self.__notify_end()
        self.running = 0
        print "task %s just terminate" % self.name

    def run_task(self):
        """
        The real code to execute in the task, you must override it in
        the subclasses descending from there.
        """
        raise TaskException("Subclasses must override .run_task(self)")

    def __cmp__(self, other):
        """
        Comparison used to classify tasks is a simple cmp on
        execution date.
        """
        return cmp(self.date, other.date)

    #def __str__(self):
    #    """
    #    Pretty print the task.
    #    """
    #    res  = "Task: " + self.name
    #    res += " - "
    #    for i in self.pred:
    #        res += str(i) + " "
    #    res += " - date: "
    #    res += str(self.date)
    #    res += os.linesep
    #    return res

    def setGUI(self, cond):
        self.mycond = cond
