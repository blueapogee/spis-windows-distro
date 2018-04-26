"""
**File name:**    TaskBuiltins.py

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

"""
Builtins for the console mode of the Spis Task manager
"""

import sys
import pickle
from common            import build_task_str
from Bin.Tasks.shared  import sharedTasks

sys.path.append("..")
from Bin.config         import GL_DATA_PATH, GL_SPISUIROOT_PATH, GL_CMD_EDITOR
sys.path.append(GL_SPISUIROOT_PATH)

def save_obj(obj, filename):
    """
    Save any obj in filename.
    """
    stream = open(filename,'w')
    pickle.dump(obj, stream)
    stream.flush()

def load_obj(filename):
    """
    Load a list from a file and return it.
    """
    #return pickle.load(open(filename, 'r'))
    return pickle.loads("\n".join([i.strip() for i in open(filename,"r").readlines()]))

def load_list(list, filename):
    """
    Load a list from a file and keep its reference, so the modified
    object is also modified in the Task Manager and can be used by
    another task.
    """
    for i in list:
        list.remove(i)
    #loaded = pickle.load(open(filename, 'r'))
    loaded = pickle.loads("\n".join([i.strip() for i in open(filename,"r").readlines()]))
    list.extend(loaded)

def load_dict(dict, filename):
    """
    Load a dic from a file and keep its reference, so the modified
    object is also modified in the Task Manager and can be used by
    another task.
    """
    for i in dict.keys():
        del dict[i]
    loaded = pickle.loads("\n".join([i.strip() for i in open(filename,"r").readlines()]))
    #loaded = pickle.load(open(filename, 'rb'))
    dict.update(loaded)

def help(obj):
    """
    Print the docstring of the object obj. (hack for the non existing
    jython help builtin).
    """
    print obj.__doc__

def reload_task(task_name):
    """
    Reload a Task from file. task_name is the full task name.
    """
    
    #FIX ME (not very clean)
    from taskslist import TasksList
    listOfTasks = TasksList()
    listOfTasks.initTasksList()
    
    for i in listOfTasks.tasks:
        exec "import %s" % ("Task" + i[1])
    exec "reload(" + task_name + ")"
    for i in listOfTasks.tasks:
        exec "from %s import %s" % ("Task" + i[1], "Task" + i[1])
    task_id = 0
    for i in range(len(sharedTasks["tasks"]) + 1):
        if "Task" + sharedTasks["tasks"][i][1] == task_name:
            task_id = i
            break
    res = "tmp = " + build_task_str(sharedTasks["tasks"], task_id)
    exec res
    sharedTasks["manager"].replace_task(tmp)
    print "Task <%s> reloaded:" % task_name

def exec_task(task_name):
    """
    Send a request to the taskmanager
    """
    if task_name[:4] == "Task":
        task_name = task_name[4:]
    sharedTasks["event_queue"].append(task_name);
    sharedTasks["event_cond"].signal();
