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
        self.DBase=parent.MyConsult.DBase
        self.MyCritere=Critere(self.DBase)
        if not parent.MyConsult.idCritere is None:
            self.MyCritere.Get(parent.MyConsult.idCritere)
        self.SeuilChanged=False
        self.Nbseuils=0
        self.PreviousIndexCritere=0
        self.label_Pathologie.setText(QtCore.QString(u'Pathologie: %s'%parent.comboBox_PathologieSelection.currentText()))
        self.label_Examen.setText(QtCore.QString(u'Examen    : %s'%parent.comboBox_Examen.currentText()))
        self.comboBox_Critere.Fill(parent.MyPathologie.GetCriteres(self.MyCritere.Examen_idExamen))
        self.comboBox_Unite.Fill(self.MyCritere.GetUnite())     
        self.tableWidget_Seuil.clear()
        #TODO: colonne Remarque
        self.tableWidget_Seuil.setHorizontalHeaderLabels(QtCore.QStringList()<<u'Grade'<<u'Seuil Inférieur'<<u'Seuil Supérieur'<<u'Score')
        for i,width in zip(range(4),[60,120,120,120]):
            self.tableWidget_Seuil.setColumnWidth(i,width)
        self.tableWidget_Seuil.setRowHeight(0,24)   
        #Connect actions
        self.comboBox_Critere.activated.connect(self.OnCritere)
        self.comboBox_Unite.activated.connect(self.OnUnite)
        self.spinBox_NbGrade.editingFinished.connect(self.OnNbGrades)
        self.connect(self.tableWidget_Seuil,QtCore.SIGNAL("OnEnter"),self.OnSeuilEnter)
        self.comboBox_Critere.setCurrentIndex(self.comboBox_Critere.findData(self.MyCritere.idCritere))
        self.toolButton_NewCritere.clicked.connect(self.OnNewCritere)
        self.toolButton_DeleteCritere.clicked.connect(self.OnDeleteCritere)
        self.pushButton_Save.clicked.connect(self.OnValid)
        self.pushButton_Cancel.clicked.connect(self.OnClose)
        #init widgets
        self.IsInit=True
        self.OnCritere()
        
    def OnCritere(self):
        if not self.IsInit:
            self.SaveCritere()
        self.PreviousIndexCritere=self.comboBox_Critere.currentIndex()
        self.IsInit=False
        self.MyCritere.Critere=self.comboBox_Critere.currentText()
        self.MyCritere.Get(self.comboBox_Critere.GetData())
        if self.MyCritere.Unite_idUnite.toInt()[1]:
            self.comboBox_Unite.setCurrentIndex(self.comboBox_Unite.findData(self.MyCritere.Unite_idUnite.toInt()[0]))
        self.spinBox_NbGrade.setValue(self.MyCritere.NbGrades.toInt()[0])
        self.plainTextEdit_Remarque.setPlainText(self.MyCritere.Remarque)
        self.Nbseuils=len(self.MyCritere.CritereGrades)
        self.tableWidget_Seuil.clearContents()
        self.tableWidget_Seuil.setRowCount=self.Nbseuils
        for i,n in zip(self.MyCritere.CritereGrades,range(self.Nbseuils)):
            for j,valeur in zip(range(4),[i.Grade,i.LimiteInf,i.LimiteSup,i.Score]):
                self.tableWidget_Seuil.setItem(n,j,QtGui.QTableWidgetItem(valeur))
            self.tableWidget_Seuil.item(n,0).setData(QtCore.Qt.UserRole,i.idCritereSeuil)
        
    def OnUnite(self):
        self.MyCritere.Unite_idUnite=self.comboBox_Unite.currentText()
            
    def OnNbGrades(self):
        self.Nbseuils=self.spinBox_NbGrade.text().toInt()[0]
        delta=self.Nbseuils-self.tableWidget_Seuil.rowCount()
        for i in range(abs(delta)):
            if delta>0:
                self.tableWidget_Seuil.insertRow(self.tableWidget_Seuil.rowCount()-1)
            else:
                if self.tableWidget_Seuil.rowCount()>self.Nbseuils:
                    self.tableWidget_Seuil.removeRow(self.tableWidget_Seuil.rowCount()-1)
                else:
                    QtGui.QMessageBox.warning(self,u"Alerte OpenVet",u'Vous devez supprimer les grades dans le tableau en mettant le grade à \"\", puis en pressant Entrée.', QtGui.QMessageBox.Ok)
    
    def OnNewCritere(self):
        self.SaveCritere()
        self.spinBox_NbGrade.setValue(0)
        self.Nbseuils=0
        self.plainTextEdit_Remarque.setPlainText('')
        self.comboBox_Unite.setCurrentIndex(0)
        self.tableWidget_Seuil.clearContents()
        self.comboBox_Critere.addItem('', 0)
        self.comboBox_Critere.setCurrentIndex(self.comboBox_Critere.count()-1)
        self.MyCritere.idCritere=0
        self.MyCritere.CritereGrades=[] 
        self.IsInit=True
    
    def OnDeleteCritere(self):
        n=self.MyCritere.IsUsed()
        msg=''
        if n:
            msg=u'Ce critère est référencé dans %i consultation(s).\n'%n
        msgBox=QtGui.QMessageBox.warning(self,u"Alerte OpenVet",msg+'Voulez-vous Vraiment effacer cette pathologie', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No | QtGui.QMessageBox.Default)
        if msgBox==QtGui.QMessageBox.Yes:
            if self.MyCritere.idCritere>0:
                self.MyCritere.idCritere*=-1
                self.SaveCritere()
            self.comboBox_Critere.removeItem(self.comboBox_Critere.currentIndex())
            self.tableWidget_Seuil.clearContents()
            self.IsInit=True
                         
    def OnSeuilEnter(self):
        self.SeuilChanged=True
        item=self.tableWidget_Seuil.currentItem()
        index=self.MyCritere.GetIndexGrade(item.data(QtCore.Qt.UserRole))
        if item.column()==0:
            if item.text()=='':
                if QtGui.QMessageBox.question(self,"OpenVet",QtCore.QString(u'Confirmation avant l\'effacement de ce grade?'),QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel)==QtGui.QMessageBox.Yes:
                    self.MyCritere.CritereGrades[index].idCritereSeuil*=-1
                    self.tableWidget_Seuil.removeRow(item.row())
                    self.Nbseuils-=1
                    self.spinBox_NbGrade.setValue(self.Nbseuils)
        
    def SaveCritere(self): 
        #attributes: idCritere,Examen_idExamen,Critere,Unite_idUnite,NbGrades,Remarque
        if self.MyCritere.idCritere==0:
            self.MyCritere.Critere=self.comboBox_Critere.currentText()
        self.MyCritere.Remarque=self.plainTextEdit_Remarque.toPlainText()
        self.MyCritere.NbGrades=QtCore.QString('%i'%self.Nbseuils)
        self.MyCritere.Unite_idUnite=QtCore.QString('%i'%self.comboBox_Unite.GetData())
#       self.MyCritere.NbGrades=self.spinBox_NbGrade_NbGrades.text().toInt()[1]
        #attributes: idCritereSeuil,Critere_idCritere,LimiteInf,LimiteSup,Grade,Score
        for i in range(self.Nbseuils):
            data=[self.tableWidget_Seuil.item(i,0).data(QtCore.Qt.UserRole).toInt()[0]]
            for j in [1,2,0,3]:
                if self.tableWidget_Seuil.item(i,j) is None:
                    data.append(QtCore.QString(''))
                else:
                    data.append(self.tableWidget_Seuil.item(i,j).text())
            self.MyCritere.UpdateGrade(data)
        self.MyCritere.Print()
        idins=self.MyCritere.Save()
        self.comboBox_Critere.setItemData(self.PreviousIndexCritere,QtCore.QVariant(idins),QtCore.Qt.UserRole)
        self.MyCritere.idCritere=idins
    
    def OnValid(self):
        self.SaveCritere()
        self.close()
        
    def OnClose(self):
        self.close()
