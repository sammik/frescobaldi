# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008, 2009, 2010 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

from __future__ import unicode_literals

"""
Keyboard shortcuts settings page.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import app
import icons
import preferences
import sessionmanager

from widgets.urlrequester import UrlRequester


class GeneralPrefs(preferences.GroupsPage):
    def __init__(self, dialog):
        super(GeneralPrefs, self).__init__(dialog)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(StartSession(self))
        layout.addWidget(SavingDocument(self))
        layout.addStretch(1)
            

class StartSession(preferences.Group):
    def __init__(self, page):
        super(StartSession, self).__init__(page)
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        def changed():
            self.changed.emit()
            self.combo.setEnabled(self.custom.isChecked())
        
        self.none = QRadioButton(toggled=changed)
        self.lastused = QRadioButton(toggled=changed)
        self.custom = QRadioButton(toggled=changed)
        self.combo = QComboBox(currentIndexChanged=changed)
        
        grid.addWidget(self.none, 0, 0, 1, 2)
        grid.addWidget(self.lastused, 1, 0, 1, 2)
        grid.addWidget(self.custom, 2, 0, 1, 1)
        grid.addWidget(self.combo, 2, 1, 1, 1)

        app.translateUI(self)
        
    def translateUI(self):
        self.setTitle(_("Session to load if Frescobaldi is started without arguments"))
        self.none.setText(_("Start with no session"))
        self.lastused.setText(_("Start with last used session"))
        self.custom.setText(_("Start with session:"))
        
    def loadSettings(self):
        s = QSettings()
        s.beginGroup("session")
        startup = s.value("startup", "none")
        if startup ==  "lastused":
            self.lastused.setChecked(True)
        elif startup == "custom":
            self.custom.setChecked(True)
        else:
            self.none.setChecked(True)
        sessionNames = sessionmanager.sessionNames()
        self.combo.clear()
        self.combo.addItems(sessionNames)
        custom = s.value("custom", "")
        if custom in sessionNames:
            self.combo.setCurrentIndex(sessionNames.index(custom))

    def saveSettings(self):
        s = QSettings()
        s.beginGroup("session")
        s.setValue("custom", self.combo.currentText())
        if self.custom.isChecked():
            startup = "custom"
        elif self.lastused.isChecked():
            startup = "lastused"
        else:
            startup = "none"
        s.setValue("startup", startup)


class SavingDocument(preferences.Group):
    def __init__(self, page):
        super(SavingDocument, self).__init__(page)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.metainfo = QCheckBox(toggled=self.changed)
        layout.addWidget(self.metainfo)
        
        hbox = QHBoxLayout()
        layout.addLayout(hbox)
        
        self.basedirLabel = l = QLabel()
        self.basedir = UrlRequester()
        hbox.addWidget(self.basedirLabel)
        hbox.addWidget(self.basedir)
        self.basedir.changed.connect(self.changed)
        app.translateUI(self)
        
    def translateUI(self):
        self.setTitle(_("When saving documents"))
        self.metainfo.setText(_("Remember cursor position, bookmarks, etc."))
        self.basedirLabel.setText(_("Default directory:"))
        self.basedirLabel.setToolTip(_("The default folder for your LilyPond documents (optional)."))
        
    def loadSettings(self):
        s = QSettings()
        self.metainfo.setChecked(s.value("metainfo", True) not in (False, "false"))
        self.basedir.setPath(s.value("basedir", ""))
        
    def saveSettings(self):
        s = QSettings()
        s.setValue("metainfo", self.metainfo.isChecked())
        s.setValue("basedir", self.basedir.path())


