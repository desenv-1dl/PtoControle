# -*- coding: utf-8 -*-
from views.iconButtonPtoControl import IconButtonPtoControl
from views.interfacePtoControl import InterfacePtoControl
from models.documentationPtoControl import DocumentationPtoControl
from controllers.controller import Controller

class Main:
    def __init__(self, iface):
        view1 = IconButtonPtoControl(iface)
        view2 = InterfacePtoControl(iface)
        model = DocumentationPtoControl(iface)
        self.controller = Controller(model, view1, view2)
  
    def initGui(self):
        self.controller.runCommand('add button', 'True')
    
    def unload(self):
        self.controller.runCommand('add button', 'False')
  



