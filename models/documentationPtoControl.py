# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject
from PyQt4 import QtGui, QtCore
from fileExporter import FileExporter

class DocumentationPtoControl(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.initVariables()
        self.iface =iface
        self.canvas = iface.mapCanvas()
        
    def initVariables(self):
        self.iface = None
        self.canvas = None
        
    def setController(self, c):
        self.controller = c 
        
    def getController(self):
        return self.controller

    def validationConfig(self):
        if (self.iface.activeLayer()) and (self.iface.activeLayer().geometryType() == 0):
            layers = self.iface.activeLayer().selectedFeaturesIds()
            if len(layers) > 0:
                self.getController().runCommand( 'set enable button', 'False')
                self.getController().runCommand( 'show dialog')
            else:
                text = u"Para usar essa ferramenta é preciso que os pontos de interesse estejam selecionados!"
                self.getController().runCommand('message erro', text)
        else:
            text = u"Ferramenta para feição tipo ponto!"
            self.getController().runCommand('message erro', text)
            
    def startWorker(self, data ):
        self.getController().runCommand('stop/start gif', 'True')
        thread = QtCore.QThread(self)
        worker = FileExporter(self.iface, data[0], data[1])
        worker.moveToThread(thread)
        worker.finished.connect(self.taskFinished)
        thread.started.connect(worker.exportFilesOfLayers)
        thread.start()
        self.thread = thread
        self.worker = worker
#     
    def taskFinished(self, tipo):
        self.worker.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        self.thread = None
        self.worker = None
        self.getController().runCommand('stop/start gif', 'False')
        self.removeSelections()
    
    def removeSelections(self):
        for i in range(len(self.canvas.layers())):
            try:
                self.canvas.layers()[i].removeSelection()
            except:
                pass
            
        





           
        
