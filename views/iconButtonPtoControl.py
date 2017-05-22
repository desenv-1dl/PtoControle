# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
from qgis.gui import QgsMessageBar
import resources
 
class IconButtonPtoControl(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.initVariables()
        self.iface = iface
        self.setButton(self.createIcon())
        
    def initVariables(self):
        self.iface = None
        self.button = None
        self.controller = None
                 
    def setController(self, c):
        self.controller = c 
        
    def getController(self):
        return self.controller

    def setButton(self, b):
        self.button = b 
    
    def getButton(self):
        return self.button
    
    def createIcon(self):
        button = QtGui.QAction(QtGui.QIcon(":/plugins/export_pto_controle/views/point.png"), 
                                     u"Exporta Pto de Controle", self.iface.mainWindow())
        button.triggered.connect(self.run)
        return button
    
    def showButton(self, bo):
        if bo == 'True':
            self.iface.digitizeToolBar().addAction(self.getButton())
        else:
            self.iface.digitizeToolBar().removeAction(self.getButton()) 
    
    def run(self):
        self.getController().runCommand('open interface')
        
    def msgError(self, text):
        self.iface.messageBar().pushMessage(u"Aviso", text, level=QgsMessageBar.INFO, duration=6) 
    
    def setEnabledToolButton(self, bo):
        if bo == 'True':
            self.getButton().setEnabled(True)
        else:
            self.getButton().setEnabled(False)
            
        
    
