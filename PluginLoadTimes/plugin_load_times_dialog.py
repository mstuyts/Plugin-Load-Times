# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginLoadTimesDialog
                                 A QGIS plugin
 Show how long each QGIS plugin loads
                             -------------------
        begin                : 2017-01-18
        copyright            : (C) 2017 by Michel Stuyts
        email                : info@stuyts.xyz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
try:
    from qgis.PyQt.QtCore import *
except ImportError:
    from PyQt4.QtCore import *
try:
    from qgis.PyQt.QtGui import QIcon
    from qgis.PyQt.QtWidgets import QDialog
except ImportError:
    from PyQt4.QtGui import QIcon, QDialog
try:
    from PyQt4 import uic
except ImportError:
    from PyQt5 import uic
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'plugin_load_times_dialog_base.ui'))


class PluginLoadTimesDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(PluginLoadTimesDialog, self).__init__(parent)
        self.resize(QSize(700, 500).expandedTo(self.minimumSizeHint()))
        self.setWindowIcon(QIcon(":/plugins/PluginLoadTimes/icon.png"))
        self.setWindowFlags( self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowMinMaxButtonsHint)
        self.setupUi(self)
