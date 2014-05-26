#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
from ui_Form_consult2 import Ui_MainWindow
from ui_Form_client import Ui_Dialog_client
from ui_Form_animal import Ui_Dialog_animal
sys.path.append('../VetCore')
import Core_Consult


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    dataClient=''
    dataAnimal=''
    idClient=0
    idAnimal=1
    idConsultation=0
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.editClient = None
        self.editAnimal = None
        #init dates
        now=QtCore.QDate.currentDate()
        self.dateEdit_consult.setDate(now)
        self.dateEdit_vacciner_start.setDate(now)
        self.dateEdit_vacciner_end.setDate(now)
        self.dateEdit_ordonance.setDate(now)
        self.dateEdit_docDate.setDate(now)
        self.dateTimeEdit_analyse.setDate(now)
        #hide some widget
        self.tableWidget_analyses.setVisible(False)
        self.listWidget_analyse.setVisible(False)
        self.lineEdit_titreImage.setVisible(False)
        self.lineEdit_fichier.setVisible(False)
        self.pushButton_addImage.setVisible(False)
        self.toolButton_fichier.setVisible(False)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)
        #fill comboboxes
        MyConsult=Core_Consult.Consultation()
        self.comboBox_veterinaire.addItems(MyConsult.GetConsultants())
        self.comboBox_consultType.addItems(MyConsult.GetTypesConsultation())
        self.comboBox_Referant.addItems(MyConsult.GetReferants())
        #connect actions
        self.toolButton_addClient.clicked.connect(self.DoClientEdit)
        self.toolButton_addAnimal.clicked.connect(self.DoAnimalEdit)
        self.comboBox_Animal.activated.connect(self.DoGetConsultations)
        self.comboBox_consultType.activated.connect(self.OnTypeConsultation)
        self.connect(self.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationClicked)
        
        self.actionQuitter.triggered.connect(self.Mycloseapp)

    def DoClientEdit(self):
        self.dataClient='Mon nom est untel'
        if self.editClient is None:
            self.editClient = FormClient(self)
        if self.editClient.exec_():
            print self.editClient.data
  
    def DoAnimalEdit(self):
        self.dataAnimal='Son nom est minou'
        if self.editAnimal is None:
                self.editAnimal = FormAnimal(self)
        if self.editAnimal.exec_():
            print self.editAnimal.data
            
    def DoGetConsultations(self):
        MyDossier=Core_Consult.Consultations()
        self.textBrowser_consultations.setText(MyDossier.GetConsultations(self.idAnimal))
        self.splitter.resize(1021,850)
        
    def OnConsultationClicked(self,link):
        self.idConsultation=int(link.toString().toAscii()[2:])
        if link.toString().toAscii()[1]=='C':
            self.FillFormConsultation()
        if link.toString().toAscii()[1]=='B':
            print 'view biologie'#TODO
        if link.toString().toAscii()[1]=='I':
            print 'view Images'
        if link.toString().toAscii()[1]=='c':
            print 'view Chirurgies'
        if link.toString().toAscii()[1]=='O':
            print 'view Ordonnance'
        if link.toString().toAscii()[1]=='T':
            print 'view Plan thérapeutique'     
      
    def FillFormConsultation(self):
        MyConsult=Core_Consult.Consultation()
        res=MyConsult.GetConsultation(self.idConsultation)
        MyConsult.FormatConsultation(res[0])
        #TODO fill form
        self.dateEdit_consult.setDate(QtCore.QDate(QtCore.QDate(int(MyConsult.Date[6:]),int(MyConsult.Date[3:5]),int(MyConsult.Date[:2]))))
        self.comboBox_veterinaire.setCurrentIndex(self.comboBox_veterinaire.findText(QtCore.QString(MyConsult.Consultant)))

        self.textEdit_consultObs.setText(QtCore.QString(MyConsult.Observations))
        self.textEdit_consultTrait.setText(QtCore.QString(MyConsult.Traitements))
        self.splitter.resize(1021,450)
        
    def OnTypeConsultation(self):
        if self.comboBox_consultType.currentText()==QtCore.QString("Référée".decode('utf8')):
            self.label_Referant.setVisible(True)
            self.comboBox_Referant.setVisible(True)
        
    def Mycloseapp(self):
        self.close()


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