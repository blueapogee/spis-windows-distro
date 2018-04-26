"""
Various dialogue boxes. 

**File name:**    common.py

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
from javax.swing import JOptionPane

from Bin.Tasks.shared import sharedFrames, sharedFlags
import javax.swing.BorderFactory
import javax.swing.JDialog
import javax.swing.JProgressBar
import java.awt.BorderLayout



def ask_value(cond):
    if cond != -1:
	#from InputDialog import InputDialog
        #str = []
        #m = InputDialog(cond, str)

        message = "Enter a value."
        if sharedFlags['guiMode']:
            control = JOptionPane.showInputDialog(sharedFrames["gui"], message);

        #cond.acquire()
        #cond.wait()
        #control = str[0]
        #sharedFrames["input_dialog"] = None
    else:
        print ">>>",
        control = raw_input()
    return control

def ask_yesno(cond, message):
    if cond != -1:
        if sharedFlags['guiMode']:
            result = JOptionPane.showConfirmDialog(sharedFrames["gui"], message, "SPIS control", JOptionPane.YES_NO_OPTION);
            if result == JOptionPane.OK_OPTION:
               control = "y"
            elif result == JOptionPane.NO_OPTION:
               control = "n"
            elif result == JOptionPane.CANCEL_OPTION:
               control = "n"
        else: 
            #FIXME
            control = "y"
        
        #sharedFrames["input_dialog"] = None
    else:
        print message
        print ">>>",
        control = raw_input()
    return control

def create_internal_frame(name, desktop_pane):
    """
    asks to the main desktop panel to create and return an internal frame.
    """
    sharedFrames[name] = sharedFrames["gui"].buildInternalFrame(name)
    # FIXME with an "if (desktop_pane != null)"
    #desktop_pane.add(sharedFrames[name])
    sharedFrames["gui"].getCurrentDesktop().add(sharedFrames[name])
    sharedFrames[name].setSize(20, 30)
    return sharedFrames[name]

def build_task_str(tasks, task_id):
    res = "Task" + tasks[int(task_id)][1] + "(\"" +tasks[int(task_id)][1]+ "\""
    res += ", " + str(tasks[int(task_id)][0].daemonic)
    for i in tasks[int(task_id)][0].pred:
        if i[0] != "start" and i[0] != "end":
            res += ", \"" + i[0] + "\""
    res += ")"
    return res

def build_task_str_single(task):
    res = "Task" + task.name + "(\"" + task.name + "\""
    res += ", " + str(task.daemonic)
    for i in task.pred:
        if i[0] != "start" and i[0] != "end":
            res += ", \"" + i[0] + "\""
    res += ")"
    return res
    
def create_progress_bar_box(message):
    """
    creates the progress bar corresponding to the running tasks.
    """
    
    dial = javax.swing.JDialog(sharedFrames["gui"])
    xpos = (sharedFrames["gui"].getWidth()*2)/3
    ypos = (sharedFrames["gui"].getHeight()*1)/4
    dial.setLocation(xpos,ypos)
    
    text = javax.swing.JLabel(message)
    text.setBorder(javax.swing.BorderFactory.createEmptyBorder(0,5,5,5))

    bar = javax.swing.JProgressBar(0)
    bar.setIndeterminate(1)
    bar.setStringPainted(1)
    bar.setBorder(javax.swing.BorderFactory.createEmptyBorder(0,5,5,5))
	    
    dial.getContentPane().add(text, java.awt.BorderLayout.CENTER)
    dial.getContentPane().add(bar, java.awt.BorderLayout.SOUTH)
    dial.setSize(256, 90)
    dial.show()
    return(dial)
    
