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
from PyQt4 import QtGui, QtCore, uic
from pprint import pprint
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'plugin_load_times_dialog_base.ui'))


class PluginLoadTimesDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(PluginLoadTimesDialog, self).__init__(parent)
        self.setWindowFlags( self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint )
        self.setupUi(self)
