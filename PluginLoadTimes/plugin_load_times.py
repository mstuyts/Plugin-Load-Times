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
"""
try:
    from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
except ImportError:
    from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
try:
    from qgis.PyQt.QtGui import QIcon, QColor
    from qgis.PyQt.QtWidgets import QAction, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,QGraphicsRectItem,QGraphicsTextItem
except ImportError:
    from PyQt4.QtGui import QAction, QIcon, QColor, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,QGraphicsRectItem,QGraphicsTextItem
import qgis.utils
# Initialize Qt resources from file resources.py
try:
    from .resources import *
except ImportError:
    from .resources3 import *
# Import the code for the dialog
from .plugin_load_times_dialog import PluginLoadTimesDialog
import os.path
import sys, random


class PluginLoadTimes:
    def __init__(self, iface):
        """Constructor.
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PluginLoadTimes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Plugin Load Times')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PluginLoadTimes')
        self.toolbar.setObjectName(u'PluginLoadTimes')
        # Create the dialog (after translation) and keep reference
        self.dlg = PluginLoadTimesDialog()
        self.dlg.sortspeed.clicked.connect(self.sortingspeed)
        self.dlg.sortspeedrev.clicked.connect(self.sortingspeedrev)
        self.dlg.sortalphabetical.clicked.connect(self.sortingalphabetical)
        self.dlg.sortalphabeticalrev.clicked.connect(self.sortingalphabeticalrev)

    def colorcode(self,time) :
        if float(time[:-1])<0.1:
            color="green"
        elif float(time[:-1])<1:
            color="#eedf00"
        elif float(time[:-1])<5:
            color="orange"
        else:
            color="red"
        return color

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PluginLoadTimes', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action
    def addgraph(self):
        data=qgis.utils.plugin_times
        scene = QGraphicsScene()
        set_angle = 0
        small_times = 0
        small_name="all other plugins"
        colours = []
        plugins = []
        times = []
        percentage = []
        for key,value in sorted(data.items(), key=lambda x: float(x[1][:-1]), reverse=True):
            number = []
            for count in range(3):
                number.append(random.randrange(0, 255))
            colours.append(QColor(number[0],number[1],number[2]))
            plugins.append(key)
            times.append(float(value[:-1]))
        totaltime=sum(times)
        numberoftimes=len(times)
        try:
            listrange=xrange(0, numberoftimes-1)
        except NameError:
            listrange=range(0, numberoftimes-1)
        for id in listrange:
            percentage.append(times[id]/totaltime)
            if percentage[id]>0.03:
                angle = round(float(times[id]*5760)/totaltime)
                ellipse = QGraphicsEllipseItem(0,0,300,300)
                ellipse.setPos(0,0)
                ellipse.setStartAngle(set_angle)
                ellipse.setSpanAngle(5760-set_angle)
                ellipse.setBrush(colours[id])
                set_angle += angle
                scene.addItem(ellipse)
                rectangle=QGraphicsRectItem(-200,(id*30)+25,10,10)
                rectangle.setBrush(colours[id])
                scene.addItem(rectangle)
                legend=QGraphicsTextItem(plugins[id]+" ("+str(int(round(percentage[id]*100)))+"%)")
                legend.setPos(-185,(id*30)+20)
                scene.addItem(legend)
                maxid=id
                
            else:
                small_times+=times[id]
                small_colour=colours[id]
        if small_times>0:
            angle = round(float(small_times*5760)/totaltime)
            ellipse = QGraphicsEllipseItem(0,0,300,300)
            ellipse.setPos(0,0)
            ellipse.setStartAngle(set_angle)
            ellipse.setSpanAngle(angle)
            ellipse.setBrush(small_colour)
            scene.addItem(ellipse)   
            rectangle=QGraphicsRectItem(-200,((maxid+1)*30)+25,10,10)
            rectangle.setBrush(small_colour)
            scene.addItem(rectangle)    
            legend=QGraphicsTextItem(small_name)
            legend.setDefaultTextColor(QColor(160,160,160))
            legend.setPos(-185,((maxid+1)*30)+20)
            scene.addItem(legend)            
        self.dlg.graphicsView.setScene(scene)
        self.dlg.show()
    def sortingspeed(self):
        data=qgis.utils.plugin_times
        outputtext="<table style='border: none;'>"
        for key,value in sorted(data.items(), key=lambda x: float(x[1][:-1]), reverse=False):
            color=self.colorcode(value)
            outputtext += "<tr style='font-weight: bold; font-family: tahoma, arial; font-size: 11pt; color: " + color  + ";'><td style='padding-bottom: 0.5em;'>" + key + ":</td><td style='padding-bottom: 0.5em;'>" + value + "</td></tr>"
        outputtext += "</table>"
        self.dlg.showloadtimes.setText(outputtext)
        self.dlg.show()

    def sortingspeedrev(self):
        data=qgis.utils.plugin_times
        outputtext="<table style='border: none;'>"
        for key,value in sorted(data.items(), key=lambda x: float(x[1][:-1]), reverse=True):
            color=self.colorcode(value)
            outputtext += "<tr style='font-weight: bold; font-family: tahoma, arial; font-size: 11pt; color: " + color  + ";'><td style='padding-bottom: 0.5em;'>" + key + ":</td><td style='padding-bottom: 0.5em;'>" + value + "</td></tr>"
        outputtext += "</table>"
        self.dlg.showloadtimes.setText(outputtext)
        self.dlg.show()

    def sortingalphabetical(self):
        data=qgis.utils.plugin_times
        outputtext="<table style='border: none;'>"
        for key,value in sorted(data.items(), key=lambda x: x[0].lower(), reverse=False):
            color=self.colorcode(value)
            outputtext += "<tr style='font-weight: bold; font-family: tahoma, arial; font-size: 11pt; color: " + color  + ";'><td style='padding-bottom: 0.5em;'>" + key + ":</td><td style='padding-bottom: 0.5em;'>" + value + "</td></tr>"
        outputtext += "</table>"
        self.dlg.showloadtimes.setText(outputtext)
        self.dlg.show()

    def sortingalphabeticalrev(self):
        data=qgis.utils.plugin_times
        outputtext="<table style='border: none;'>"
        for key,value in sorted(data.items(), key=lambda x: x[0].lower(), reverse=True):
            color=self.colorcode(value)
            outputtext += "<tr style='font-weight: bold; font-family: tahoma, arial; font-size: 11pt; color: " + color  + ";'><td style='padding-bottom: 0.5em;'>" + key + ":</td><td style='padding-bottom: 0.5em;'>" + value + "</td></tr>"
        outputtext += "</table>"
        self.dlg.showloadtimes.setText(outputtext)
        self.dlg.show()

    def initGui(self):
        icon_path = ':/plugins/PluginLoadTimes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Plugin Load Times'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Plugin Load Times'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        # show the results
        self.sortingspeedrev()
        self.addgraph()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass

