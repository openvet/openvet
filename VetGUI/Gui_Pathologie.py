#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
import Core_Consultation
from ui_Form_pathologie import Ui_DialogPathologie
#import Gui_Core
import time

class FormPathologie(QtGui.QDialog, Ui_DialogPathologie):   #On click button_P]
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.NbCriteres=0
        self.MyPathologie=parent.MyPathologie
        self.MyConsult=parent.MyConsult
        self.MyCritere=Core_Consultation.Critere(self.MyPathologie.DBase)
        self.ChangedRows=[]
        #format table
        self.tableWidget_Criteres.setHorizontalHeaderLabels(QtCore.QStringList()<<u'Examen'<<u'Critère'<<u'Valeur'<<u'Unitée'<<u'Norme'<<u'Grade')
        widths=[180,240,76,50,110,60]
        #TODO: limit size string for cells 
        for i in range(len(widths)):
            self.tableWidget_Criteres.setColumnWidth(i,widths[i])
        for i in range(12):
            self.tableWidget_Criteres.setRowHeight(i,24)   
        #fill comboboxes
        self.comboBox_PathologieDomaine.Fill(self.MyPathologie.GetDomaines())
        self.comboBox_PathologieSelection.Fill(self.MyConsult.GetPathologiesConsultation())      
        #connect action
        self.comboBox_PathologieDomaine.currentIndexChanged.connect(self.OnPathologieDomaine)
        self.comboBox_Examen.currentIndexChanged.connect(self.OnExamen)
        self.comboBox_Critere.activated.connect(self.OnCritere)
        self.tableWidget_Criteres.itemChanged.connect(self.OnCritereEnter)
        #self.tableWidget_Criteres.itemActivated.connect(self.OnCritereEnter)
        self.comboBox_PathologiePathologie.activated.connect(self.OnPathologie)
        self.comboBox_PathologieSelection.activated.connect(self.OnSelection)
        self.toolButton_AddPathologie.clicked.connect(self.OnAddPathologie) #in selection
        self.toolButton_deletePathologie.clicked.connect(self.OnRemovePathologie)
        self.accepted.connect(self.SaveCriteresConsultation)
        #fill pathologies pour Tous 
        self.OnPathologieDomaine()
        
    def OnPathologieDomaine(self):
        idPathologieDomaine=self.comboBox_PathologieDomaine.GetData()
        if not idPathologieDomaine is None:
            self.comboBox_PathologiePathologie.Fill(self.MyPathologie.GetPathologies(idPathologieDomaine))
        
    def OnPathologie(self):
        txt=self.comboBox_PathologiePathologie.currentText()
        idPathologie=self.comboBox_PathologiePathologie.GetData()
        if not idPathologie is None:
            self.MyPathologie.GetPathologie(idPathologie)
            self.label_NomPathologie.setText(QtCore.QString(self.MyPathologie.NomReference))
            self.plainTextEdit_Descriptif.setPlainText(QtCore.QString(self.MyPathologie.Descriptif))
            self.checkBox_Chronic.setChecked(self.MyPathologie.IsChronic)
            self.listWidget_Synonymes.clear()
            for i in self.MyPathologie.Synonymes:
                txt=QtGui.QListWidgetItem(QtCore.QString(i))
                txt.setFlags(txt.flags()|QtCore.Qt.ItemIsEditable)
                self.listWidget_Synonymes.addItem(txt)
                         
    def OnSelection(self):
        idPathologie=self.comboBox_PathologieSelection.GetData()
        if not idPathologie is None:
            self.MyPathologie.GetPathologie(idPathologie)
        self.comboBox_Examen.Fill(self.MyPathologie.GetExamens())
        if self.NbCriteres>0:
            self.SaveCriteresConsultation()
        self.NbCriteres=0
        self.tableWidget_Criteres.clearContents()
        res=self.MyConsult.GetCriteresConsultation(idPathologie)
        for i in res:
            self.FillTable(i)
        self.ChangedRows=[]
            
    def FillTable(self,ligne):
        if len(ligne)==0:
            return
        self.NbCriteres+=1
        if self.NbCriteres>self.tableWidget_Criteres.rowCount():
            self.tableWidget_Criteres.insertRow(self.tableWidget_Criteres.rowCount())
        for i,align in zip(range(6),[QtCore.Qt.AlignLeft,QtCore.Qt.AlignLeft,QtCore.Qt.AlignRight,QtCore.Qt.AlignRight,QtCore.Qt.AlignCenter,QtCore.Qt.AlignRight]):
            self.tableWidget_Criteres.setItem(self.NbCriteres-1,i,QtGui.QTableWidgetItem(ligne[i+2]))
            self.tableWidget_Criteres.item(self.NbCriteres-1,i).setTextAlignment(align)
            self.tableWidget_Criteres.item(self.NbCriteres-1,i).setData(QtCore.Qt.UserRole,QtCore.QVariant([ligne[0],ligne[1]]))
            
    def OnExamen(self):
        if not self.comboBox_Examen.GetData() is None:
            self.comboBox_Critere.Fill(self.MyPathologie.GetCriteres(self.comboBox_Examen.GetData()))                

    def OnCritere(self):
        if not self.comboBox_Critere.GetData() is None:
            res=self.MyCritere.GetCritere(self.comboBox_Critere.GetData())
            if len(res)>0:
                self.FillTable([0,res[0],res[1],res[2],'',res[3],res[4],''])
                self.tableWidget_Criteres.editItem(self.tableWidget_Criteres.item(self.NbCriteres-1,2))

    def OnCritereEnter(self,item):
        if item is None:
            return
        if item.column()==2:
            if len(item.data(QtCore.Qt.UserRole).toList())==2:
                self.MyCritere.idCritere=item.data(QtCore.Qt.UserRole).toList()[1].toInt()[0]
            res=self.MyCritere.GetCritereGrade(item.text().toFloat()[0])
            if len(res)==0 :
                return
            self.tableWidget_Criteres.setItem(item.row(),5,QtGui.QTableWidgetItem(res[0]+'/'+res[1]))
            self.tableWidget_Criteres.item(item.row(),5).setTextAlignment(QtCore.Qt.AlignRight)
        if item.isSelected():
            if item.data(QtCore.Qt.UserRole).toList()[0].toInt()[0]!=0:
                if not item.row in self.ChangedRows:
                    self.ChangedRows.append(item.row())
            else:
                #TODO: sort by examen if data[0]==0
                pass
           
    def OnAddPathologie(self):
        if self.comboBox_PathologieSelection.findData(self.MyPathologie.idPathologie)==-1:
            self.comboBox_PathologieSelection.addItem(self.MyPathologie.NomReference, self.MyPathologie.idPathologie)
            self.comboBox_PathologieSelection.setCurrentIndex(self.comboBox_PathologieSelection.count()-1)
        
    def OnRemovePathologie(self):
        self.comboBox_PathologieSelection.removeItem(self.comboBox_PathologieSelection.currentIndex())  
        
    def SaveCriteresConsultation(self):
        for i in range(self.NbCriteres):
            ids=self.tableWidget_Criteres.item(i,2).data(QtCore.Qt.UserRole).toList()
            ids.append(QtCore.QVariant(self.comboBox_PathologieSelection.GetData()))
            valeur=self.tableWidget_Criteres.item(i,2).text()
            grade=self.tableWidget_Criteres.item(i,5).text()
            if ids[0].toInt()[0]==0 or i in self.ChangedRows:
                self.MyConsult.SaveCritere(ids,valeur,grade)
     