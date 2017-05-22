# -*- coding: UTF-8 -*-
from PyQt4 import QtCore, QtGui
import psycopg2
import os
from qgis.core import QgsVectorFileWriter, QgsMapLayerRegistry
from PyQt4.QtGui import QFileDialog
from shutil import copyfile
from unicodedata import normalize
import platform
import csv
import psycopg2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FileExporter(QtCore.QObject):
    finished = QtCore.pyqtSignal(int)
    def __init__(self, iface, options, path, parent=None):
        QtCore.QObject.__init__(self)
        self.iface = iface
        self.options = options
        self.path = path
        self.setSep()
        self.setUser()

    def setSep(self):
        self.sep = '/'
                
    def setUser(self):
        s = QtCore.QSettings()
        s.beginGroup("PostgreSQL/connections")
        for x in s.allKeys():
            if x[-9:] == "/username":
                self.u = s.value(x)
            if x[-9:] == '/password':
                self.p = s.value(x)
    
    def getDataCsv(self, fields):
        dataTotal = []
        for layer in range(len(self.iface.activeLayer().selectedFeatures())):
            data=[]
            for field in fields:
                v = self.iface.activeLayer().selectedFeatures()[layer].attribute(field)
                if (isinstance(v, float)) or (isinstance(v, int)):
                    value = str(v).replace('.',',')
                else:
                    value = str(v).encode('utf-8').strip()
                data.append(value)
            dataTotal.append(data)
        return dataTotal
      
    def exportFilesOfLayers(self):
        field = { 
                'monografia': 'path_monografia', 
                'croqui': 'path_croqui', 
                'vista_aerea': 'path_vista_aerea',
                'rinex': 'path_rinex',
                'relatorio_de_implantacao': 'path_rel_implantacao', 
                'relatorio_de_acuracia': 'path_rel_acuracia' 
                 }
        self.foldes =   { 
                        'monografia': '7_Monografia',
                        'croqui': '2_Croqui_de_Campo',
                        'vista_aerea': '3_Vista_Aerea',
                        'rinex': '1_Arquivos_GNSS_RINEX', 
                        'relatorio_de_implantacao': '5_Relatorio_GNSS_de_Implantacao', 
                        'relatorio_de_acuracia': '6_Relatorio_GNSS_de_Cheque-de-Acuracia', 
                        'fotografias' : '4_Fotografias_in_Loco' 
                        }
        for option in self.options:
            foldeFile = normalize('NFKD', option).encode('ascii', 'ignore').replace(' ','_').lower()
            if foldeFile == 'csv':
                self.exportCsv(foldeFile)
            elif foldeFile == 'fotografias':
                self.exportFotos(foldeFile)
            elif foldeFile == 'kmz':
                self.exportKmz(foldeFile)
            else:
                self.exportFiles(foldeFile, field)
        self.finished.emit(1)

           
    def exportCsv(self, foldeFile):
        pathDir = self.path+self.sep
        with open((pathDir+'pto_controle.csv'), 'wb') as csvfile:
            fields = ['cod_ponto', 'tipo_ref', 'coord_n', 'coord_e', 'altitude_geometrica', 'altitude_ortometrica', 
                          'med_altura', 'fuso']
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(fields)
            for data in self.getDataCsv(fields):
                writer.writerow(data)
   
    def exportFiles(self, foldeFile, field):
        pathDir = self.path+self.sep+self.foldes[foldeFile]+self.sep
        os.mkdir(pathDir)
        for layer in range(len(self.iface.activeLayer().selectedFeatures())):
            value = self.iface.activeLayer().selectedFeatures()[layer].attribute(field[foldeFile])
            if platform.system() == 'Linux' :
                u = value[2:].replace('\\', '/').replace('/', ':/', 1)
                url = u[:12]+'/dados/'+u[13:]
                os.system('sshpass -p"'+self.p+'" scp '+self.u+'@'+url+' '+(pathDir))
            else:
                command = 'copy '+value+' '+(pathDir.replace('/','\\'))
                os.popen(command)
    
    def exportKmz(self, foldeFile):
        pathDir = self.path+self.sep
        layerAtivo={}
        for nome in QgsMapLayerRegistry.instance().mapLayers():
            layerAtivo[nome[:-17]] = QgsMapLayerRegistry.instance().mapLayers().get(nome)
        layer = layerAtivo.get(self.iface.activeLayer().name())
        output_layer = pathDir+'pto_controle'
        crs = self.iface.activeLayer().crs()
        QgsVectorFileWriter.writeAsVectorFormat(layer, output_layer, "utf-8", crs, "KML", onlySelected=True)
        
    def exportFotos(self, foldeFile):
        pathDir = self.path+self.sep+self.foldes[foldeFile]+self.sep
        os.mkdir(pathDir)
        conn_string = "host=10.25.163.9 dbname=acervo user=postgres port=5434"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute('select cod_ponto, path_foto  from pto.foto_pto_controle_p;')
        images = []
        for valores in cursor.fetchall():
            images.append([valores[0], valores[1]])
        cursor.close() 
        for layer in range(len(self.iface.activeLayer().selectedFeatures())):
            value = self.iface.activeLayer().selectedFeatures()[layer].attribute('cod_ponto')
            for image in images:
                if image[0] == value:
                    if platform.system() == 'Linux' :
                        u = image[1][2:].replace('\\', '/').replace('/', ':/', 1)
                        url = u[:12]+'/dados/'+u[13:]
                        url = url[:-3]+url[-3:].upper()
                        os.system('sshpass -p"'+self.p+'" scp '+self.u+'@'+url+' '+(pathDir))
                    else:
                        command = 'copy '+image[1]+' '+(pathDir.replace('/','\\'))
                        os.popen(command)
                        
                        