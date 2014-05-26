#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from Core_Critere import Critere
from ui_Form_critere import Ui_DialogCritere

class FormCritere(QtGui.QDialog, Ui_DialogCritere):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.MyCritere=parent.MyCritere #ConsultationCriteres dans MyConsult
        self.idCritereSeuil=QtCore.QString(u'0')
        self.SeuilChanged=False
        self.Grade=None
#        ids=[parent.MyCritere.idCritere,parent.MyCritere.idExamen,parent.MyCritere.idPathologie]
        self.label_Pathologie.setText(QtCore.QString(u'Pathologie: %s'%parent.comboBox_PathologieSelection.currentText()))
        self.label_Examen.setText(QtCore.QString(u'Examen    : %s'%parent.comboBox_Examen.currentText()))
        self.comboBox_Critere.Fill(parent.MyPathologie.GetCriteres(self.MyCritere.Examen_idExamen))
        self.comboBox_Unite.Fill(self.MyCritere.GetUnite())
        self.tableWidget_Seuil.clear()
        self.tableWidget_Seuil.setHorizontalHeaderLabels(QtCore.QStringList()<<u'Seuil Inférieur'<<u'Seuil Supérieur'<<u'Score')
        for i,width in zip(range(3),[120,120,60]):
            self.tableWidget_Seuil.setColumnWidth(i,width)
        self.tableWidget_Seuil.setRowHeight(0,24)   
        #Connect actions
        self.comboBox_Critere.activated.connect(self.OnCritere)
        self.comboBox_Unite.activated.connect(self.OnUnite)
        self.lineEdit_NbGrades.textChanged.connect(self.OnNbGrades)
        self.comboBox_Grade.currentIndexChanged.connect(self.OnGrade)
        self.connect(self.tableWidget_Seuil,QtCore.SIGNAL("OnEnter"),self.OnSeuilEnter)
        #init widgets
        self.comboBox_Critere.setCurrentIndex(self.comboBox_Critere.findData(self.MyCritere.idCritere))
        self.pushButton_Save.clicked.connect(self.OnValid)
        self.pushButton_Cancel.clicked.connect(self.OnClose)
        self.IsInit=True
        self.OnCritere()

    def FillGrade(self,Nb):
        if not Nb.toInt()[1]:
            return
        z=QtCore.QStringList()
        for i in range(Nb.toInt()[0]+1):
            z<<(QtCore.QString(str(i)))
        self.comboBox_Grade.clear()
        self.comboBox_Grade.addItems(z)
        
    def OnCritere(self):
        if not self.IsInit:
            self.OnsaveCritere()
        self.IsInit=False
        self.MyCritere.Critere=self.comboBox_Critere.currentText()
        self.MyCritere.GetCritere(self.comboBox_Critere.GetData())
        self.comboBox_Unite.setCurrentIndex(self.comboBox_Unite.findText(self.MyCritere.Unite_idUnite))
        self.lineEdit_NbGrades.setText(self.MyCritere.NbGrades)
        self.comboBox_Grade.setCurrentIndex=0
        self.plainTextEdit_Remarque.setPlainText(self.MyCritere.Remarque)
        
    def OnUnite(self):
        self.MyCritere.Unite_idUnite=self.comboBox_Unite.currentText()
            
    def OnNbGrades(self):
        if self.lineEdit_NbGrades.text().toInt()[1]:
            self.FillGrade(self.lineEdit_NbGrades.text())
            self.MyCritere.NbGrades=self.lineEdit_NbGrades.text()
         
    def OnGrade(self):
        self.OnSaveGrade()
        self.OnSaveGrade()
        self.Grade=self.comboBox_Grade.currentText()
        self.SeuilChanged=False
        res=self.MyCritere.GetCritereSeuil(self.comboBox_Grade.currentText().toInt()[0])
        if len(res)==0:
            self.idCritereSeuil=QtCore.QString(u'0')
            for i in range(3):
                self.tableWidget_Seuil.setItem(0,i,QtGui.QTableWidgetItem(u''))
        else:
            self.idCritereSeuil=res[0]
            for i,valeur in zip(range(3),res[1:]):
                self.tableWidget_Seuil.setItem(0,i,QtGui.QTableWidgetItem(valeur))
            
    def OnSeuilEnter(self):
        self.SeuilChanged=True
        
    def OnsaveCritere(self): 
        self.MyCritere.Remarque=self.plainTextEdit_Remarque.toPlainText()
        if not self.lineEdit_NbGrades.text().toInt()[1]:
            self.lineEdit_NbGrades.setText(QtCore.QString(u''))
        self.MyCritere.SaveCritere()
        
    def OnSaveGrade(self):
        if self.SeuilChanged==False:
            return
        data=[self.idCritereSeuil,self.Grade]
        for i in range(3):
            if self.tableWidget_Seuil.item(0,i) is None:
                return
            else:
                data.append(self.tableWidget_Seuil.item(0,i).text())
        self.MyCritere.SaveGrade(data)
    
    def OnValid(self):
        self.MyCritere.Print()
        #self.OnsaveCritere()
        #TODO: OnSaveGrade
        self.close()
        
    def OnClose(self):
        self.close()