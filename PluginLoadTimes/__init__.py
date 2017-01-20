# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginLoadTimes
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
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PluginLoadTimes class from file PluginLoadTimes.
    """
    #
    from .plugin_load_times import PluginLoadTimes
    return PluginLoadTimes(iface)
