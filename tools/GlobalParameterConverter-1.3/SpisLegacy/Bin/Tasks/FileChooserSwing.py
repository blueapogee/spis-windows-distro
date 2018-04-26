"""
Various file dialogue boxes.

**File name:**    FileChooserSwing.py

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

from pawt import swing
import java

def choose(dir=None, file=None):
    frame = swing.JFrame('FileChooser', visible=0)
    chooser = swing.JFileChooser()
    if dir != None:
        chooser.setCurrentDirectory(java.io.File(dir))
        if file != None:
            chooser.setSelectedFile(java.io.File(dir + "/" + file))
    chooser.showOpenDialog(frame)
    mop = chooser.getSelectedFile()
    frame.dispose()
    return mop

def choose_save(dir=None, file=None):
    frame = swing.JFrame('FileChooser', visible=0)
    chooser = swing.JFileChooser()
    if dir != None:
        chooser.setCurrentDirectory(java.io.File(dir))
        if file != None:
            chooser.setSelectedFile(java.io.File(dir + "/" + file))
    chooser.showSaveDialog(frame)
    mop = chooser.getSelectedFile()
    frame.dispose()
    return mop

def choose_dir(dir=None):
    chooser = swing.JFileChooser()
    chooser.setFileSelectionMode(swing.JFileChooser.DIRECTORIES_ONLY)
    if dir != None:
        chooser.setCurrentDirectory(java.io.File(dir))
    ret = chooser.showDialog(None, "Select Directory")
    if ret == swing.JFileChooser.APPROVE_OPTION:
        mop = chooser.getSelectedFile()
    else:
        mop = None
    return mop

