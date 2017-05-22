#! -*- coding: UTF-8 -*-
from qgis.utils import iface
from PyQt4.QtCore import QObject


class Controller(QObject):
    def __init__(self, model, view1, view2):
        QObject.__init__(self)
        view1.setController(self)
        self.view1 = view1
        view2.setController(self)
        self.view2 = view2
        model.setController(self)
        self.model = model
        self.initCommands()
        
    def initCommands(self):
        self.commands = {'add button' : self.view1.showButton,
                         'set enable button' : self.view1.setEnabledToolButton,
                         'message erro' : self.view1.msgError,
                         'show dialog' : self.view2.showDialog,
                         'open interface' : self.model.validationConfig, 
                         'stop/start gif': self.view2.showGif,
                         'remove selections' : self.model.removeSelections,
                         'run export' : self.model.startWorker,
                        }
    
    def runCommand(self, cmd, param1 = None):
        if param1:
            self.commands[cmd](param1)
        else:
            self.commands[cmd]()    
            
    
           
    
        
        