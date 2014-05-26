#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui,QtSql
#from PySide import QtCore, QtGui
import config
from ui_Form_openvet import Ui_MainWindow
from ui_Form_consultation import Ui_tabWidget_medical
from ui_Form_client import Ui_Dialog_client
from ui_Form_animal import Ui_Dialog_animal
from Gui_Consultation import TabConsultation

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, db,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.db=db
        self.editConsultation = TabConsultation(self)
        self.editConsultation.setGeometry(QtCore.QRect(0, 180, 1024, 521))
        #En attendant la connection avec la gestion client
        self.editConsultation.OnSelectAnimal()
        #Connect actions
        self.actionQuitter.triggered.connect(self.Mycloseapp)

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
    #Test
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName ( config.host )
    db.setUserName ( config.user )
    db.setPassword ( config.password )
    db.setDatabaseName(config.database)
    if not db.open():
        QtGui.QMessageBox.warning(None, "Opencompta",
            QtCore.QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)
    #end test
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())
