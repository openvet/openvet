# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
from ui_Form_openvet import Ui_MainWindow
from ui_Form_consultation import Ui_tabWidget_medical
from ui_Form_client import Ui_Dialog_client
from ui_Form_animal import Ui_Dialog_animal
from Gui_Consultation import TabConsultation

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionQuitter.triggered.connect(self.Mycloseapp)
        self.editConsultation = TabConsultation(self)
        self.editConsultation.setGeometry(QtCore.QRect(0, 180, 1024, 521))
        #En attendant la connection avec la gestion client
        self.editConsultation.OnSelectAnimal()

    def Mycloseapp(self):
        self.close()

# TODO: 
class FormClient(QtGui.QDialog, Ui_Dialog_client):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        print parent.dataClient
        self.setupUi(self)
        self.data=parent.dataClient+' rien'

class FormAnimal(QtGui.QDialog, Ui_Dialog_animal):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        print parent.dataAnimal
        self.setupUi(self)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
