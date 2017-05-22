# -*- coding: utf-8 -*-
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4 import QtCore, QtGui, uic
from qgis.gui import QgsMessageBar
import sys, os

sys.path.append(os.path.dirname(__file__))
GUI, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'interfacePtoControl.ui'), resource_suffix='')

class InterfacePtoControl(QtGui.QDialog, GUI):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        GUI.__init__(self)
        self.setupUi(self)
        self.initVariables()
        self.iface = iface
        self.canvas = iface.mapCanvas()
                
    def initVariables(self):
        self.iface = None
        self.canvas = None
        self.gif = None
        self.options = [self.csvCheckBox,
                        self.fotosCheckBox,
                        self.monografiaCheckBox,
                        self.croquiCheckBox,
                        self.rAcuraciaCheckBox,
                        self.rImplatacaoCheckBox,
                        self.rinexCheckBox,
                        self.vistaAereaCheckBox,
                        self.kmzCheckBox] 
        
    def setGif(self, g):
        self.gif = g
    
    def getGif(self):
        return self.gif
    
    def confiqGifLabel(self):
        gif = os.path.join(os.path.dirname(__file__), 'loading.gif')
        movie = QtGui.QMovie(gif)
        self.setGif(movie)
        self.giffLabel.setMovie(self.getGif())
        self.getGif().start()
        self.giffLabel.setVisible(False)
        
        
    def showGif(self, bo):
        if bo == 'True':
            self.giffLabel.setVisible(True)
        else:
            self.giffLabel.setVisible(False)
           
    def setController(self, c):
        self.controller = c 
        
    def getController(self):
        return self.controller
    
    def getOptionsChecked(self):
        checkeds = []
        for option in self.options:
            if option.isChecked():
                checkeds.append(unicode(option.text()))   
        return checkeds   
    
    def showDialog(self):
        self.show()
        self.confiqGifLabel()
           
    @pyqtSlot(bool)    
    def on_exportButton_clicked(self):
        path = unicode(QFileDialog.getSaveFileName(self, 'Crie uma pasta para salvar arquivos de camadas :', '')).encode('utf-8')
        if path:
            os.mkdir(path)
            options = self.getOptionsChecked()
            self.getController().runCommand( 'run export', [options, path] )
                    
    @pyqtSlot(bool)    
    def on_cancelButton_clicked(self):
        self.close()
        
    @pyqtSlot(bool)    
    def on_marDesButton_clicked(self):
        if len(self.getOptionsChecked()) == len(self.options):
            action = QtCore.Qt.Unchecked
        else:
            action = QtCore.Qt.Checked
        for option in self.options:
                option.setCheckState(action)
    
    def closeEvent(self, e):
        self.getController().runCommand( 'set enable button', 'True')
        self.getController().runCommand( 'remove selections' )

   