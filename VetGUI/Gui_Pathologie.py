#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
#import Core_Consultation
#import Core_Pathologie
from MyGenerics import *
from ui_Form_pathologie import Ui_DialogPathologie
from Gui_Critere import FormCritere
import time

class FormPathologie(QtGui.QDialog, Ui_DialogPathologie):   #On click button_P
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.MyPathologie=parent.MyPathologie
        self.MyConsult=parent.MyConsult
        self.NbCriteres=0
        self.curidExamen=0
        self.curidPathologie=0
        self.curidCritere=0
        self.indexPathologie=0
        self.ChangedRows=[]
        self.editCritere=None
        #format table
        self.tableWidget_Criteres.clear()
        self.tableWidget_Criteres.setHorizontalHeaderLabels(QtCore.QStringList()<<u'Examen'<<u'Critère'<<u'Valeur'<<u'Unitée'<<u'Norme'<<u'Grade')
        widths=[180,240,76,50,110,60]
        #TODO: limit size string for cells 
        for i in range(len(widths)):
            self.tableWidget_Criteres.setColumnWidth(i,widths[i])
        for i in range(12):
            self.tableWidget_Criteres.setRowHeight(i,24)   
        #fill comboboxes
        self.comboBox_PathologieDomaine.setModel(MyComboModel('GetDomaines()'))

        #if len(self.MyConsult.ConsultationPathologies):
#         id=self.comboBox_PathologiePathologie.findData(QtCore.QVariant(self.MyConsult.ConsultationPathologies[0].Pathologie_idPathologie),5)
#         self.comboBox_PathologiePathologie.setCurrentIndex(id)
#         self.OnPathologie()
        self.comboBox_PathologieSelection.Fill(self.MyConsult.GetConsultationPathologies())      
        #connect action
        self.comboBox_PathologieDomaine.currentIndexChanged.connect(self.OnPathologieDomaine)
        self.toolButton_DomaineSelection.clicked.connect(self.OnAddDomainePathologie)
        self.comboBox_Examen.currentIndexChanged.connect(self.OnExamen)
        self.comboBox_Critere.activated.connect(self.OnCritere)
        self.listWidget_Domaines.itemDoubleClicked.connect(self.RemoveDomainePathologie)
        self.connect(self.tableWidget_Criteres,QtCore.SIGNAL("OnEnter"),self.OnCritereEnter)
        self.comboBox_PathologiePathologie.activated.connect(self.OnPathologie)
        self.comboBox_PathologieSelection.activated.connect(self.OnSelection)
        self.toolButton_AddDomaine.clicked.connect(self.OnAddDomaine)
        self.toolButton_AddPathologie.clicked.connect(self.OnAddPathologie)
        self.toolButton_DeletePathologie.clicked.connect(self.OnDeletePathologie)
        self.lineEdit_NomReference.returnPressed.connect(self.CheckDoublonPathologie)
        self.toolButton_AddSelection.clicked.connect(self.OnAddSelection)
        self.toolButton_deleteSelection.clicked.connect(self.OnRemoveSelection)
        self.toolButton_AddCritere.clicked.connect(self.OnEditCritere)
        self.pushButton_SavePathologie.clicked.connect(self.SavePathologie)
        self.pushButton_Save.clicked.connect(self.SaveConsultation)
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        #fill pathologies pour Tous 
        self.OnPathologieDomaine()
        
    def OnPathologieDomaine(self):
        idPathologieDomaine=self.comboBox_PathologieDomaine.GetData()
        if not idPathologieDomaine is None:
            self.comboBox_PathologiePathologie.setModel(MyComboModel('SelectPathologies(%i,%i)'%(self.MyPathologie.idEspece,idPathologieDomaine)))
#            self.comboBox_PathologiePathologie.Fill(self.MyPathologie.GetPathologies(idPathologieDomaine))
                
        
    def OnPathologie(self):
        txt=self.comboBox_PathologiePathologie.currentText()
        self.curidPathologie=self.comboBox_PathologiePathologie.GetData()
        if not self.curidPathologie is None:
            self.MyPathologie.Get(self.curidPathologie)
            self.lineEdit_NomReference.setText(self.MyPathologie.NomReference)
            self.plainTextEdit_Descriptif.setPlainText(self.MyPathologie.DescriptifPublic)
            self.checkBox_Chronic.setChecked(self.MyPathologie.Chronique)
            self.listWidget_Synonymes.clear()
            for i in self.MyPathologie.Synonymes:
                txt=QtGui.QListWidgetItem(i[1])
                txt.setData(5,i[0])
                txt.setFlags(txt.flags()|QtCore.Qt.ItemIsEditable)
                self.listWidget_Synonymes.addItem(txt)
            for i in range(7-len(self.MyPathologie.Synonymes)):
                txt=QtGui.QListWidgetItem('')
                txt.setData(5,0)
                txt.setFlags(txt.flags()|QtCore.Qt.ItemIsEditable)
                self.listWidget_Synonymes.addItem(txt)
            self.listWidget_Domaines.clear()
            for i in self.MyPathologie.Domaines:
                txt=QtGui.QListWidgetItem(i.NomDomaine)
                txt.setData(5,QtCore.QVariant([i.idDomaineRef,i.PathologieDomaine_idPathologieDomaine]))
                self.listWidget_Domaines.addItem(txt)
                
    def OnAddDomainePathologie(self):
        if not self.listWidget_Domaines.findItems(self.comboBox_PathologieDomaine.currentText(),QtCore.Qt.MatchExactly):
            idPathologieDomaine=self.comboBox_PathologieDomaine.GetData()
            txt=QtGui.QListWidgetItem(self.comboBox_PathologieDomaine.currentText())
            txt.setData(5,QtCore.QVariant([0,idPathologieDomaine]))
            self.listWidget_Domaines.addItem(txt)
            
    def RemoveDomainePathologie(self,item):
        i=self.listWidget_Domaines.currentRow()
        idDomaineRef=item.data(5).toList()[0].toInt()[0]
        if idDomaineRef==0:
            self.listWidget_Domaines.takeItem(i)
        else:
            if len(self.MyPathologie.Domaines)>1:
                msgBox=QtGui.QMessageBox.warning(self,u"Alerte OpenVet",'Voulez-vous Vraiment effacer ce domaine de pathologie', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No | QtGui.QMessageBox.Default)
                if msgBox==QtGui.QMessageBox.Yes:
                    item.setHidden(True)
                    
    def OnAddDomaine(self):
        #TODO combobox editable pour modification d'orthographe
        (text,valid)=QtGui.QInputDialog.getText(self,"OpenVet","Entrez le nouveau nom de domaine",QtGui.QLineEdit.Normal,"")
        if valid and not text.isEmpty():
            self.MyPathologie.SaveDomaine(text)
                           
    def OnAddPathologie(self):
        self.MyPathologie.idPathologie=0
        self.lineEdit_NomReference.setText('')
        self.plainTextEdit_Descriptif.setPlainText('')
        self.checkBox_Chronic.setChecked(False)
        self.listWidget_Synonymes.clear()
        for i in range(7):
            txt=QtGui.QListWidgetItem('')
            txt.setData(5,0)
            txt.setFlags(txt.flags()|QtCore.Qt.ItemIsEditable)
            self.listWidget_Synonymes.addItem(txt)
        self.listWidget_Domaines.clear()
        self.lineEdit_NomReference.setFocus()
        
            
    def CheckDoublonPathologie(self):
        res=self.MyPathologie.CheckDoublon(self.lineEdit_NomReference.text())
        if len(res):
            msg=u"Attention la base contient déjà le(s) doublon(s) suivant(s) :\n"
            for i in res:
                msg=msg+'  -%s\n'%i[1]
            msg=msg+u"\nConfirmez-vous cette entrée? (Non recommandé)"
            msgBox = QtGui.QMessageBox.warning(self, 'Alerte OpenVet',msg,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No | QtGui.QMessageBox.Default)
            if msgBox==QtGui.QMessageBox.No:
                self.lineEdit_NomReference.setText(self.MyPathologie.NomReference)
            del msgBox

    
    def OnDeletePathologie(self):
        isused=self.MyPathologie.CheckUsed()
        msg=''
        if isused[0]:
            msg=u'Cette pathologie est référencée dans %i consultation(s).\n'%isused[0]
        if isused[1]:
            msg=msg+u'Cette pathologie est documentée avec %i données.\n'%isused[1]
        msgBox=QtGui.QMessageBox.warning(self,u"Alerte OpenVet",msg+'Voulez-vous Vraiment effacer cette pathologie', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No | QtGui.QMessageBox.Default)
        if msgBox==QtGui.QMessageBox.Yes:
            self.MyPathologie.idPathologie=-self.MyPathologie.idPathologie
            if not self.MyPathologie.Save():
                self.OnPathologieDomaine()
                
        
    def SavePathologie(self):                        
        #idPathologie,NomReference,Chronique,DescriptifPublic+Synonymes
        self.MyPathologie.NomReference=self.lineEdit_NomReference.text()
        self.MyPathologie.Chronique=self.checkBox_Chronic.isChecked()
        self.MyPathologie.DescriptifPublic=self.plainTextEdit_Descriptif.toPlainText()
        self.MyPathologie.Synonymes=[]
        for j in range(self.listWidget_Synonymes.count()):
            i=self.listWidget_Synonymes.item(j)
            if i.text().isEmpty():
                if i.data(5).toInt()[0]>0:
                    self.MyPathologie.Synonymes.append([-i.data(5).toInt()[0],i.text()])
            else:
                self.MyPathologie.Synonymes.append([i.data(5).toInt()[0],i.text()])
        self.MyPathologie.Domaines=[]
        for j in range(self.listWidget_Domaines.count()):
            i=self.listWidget_Domaines.item(j)
            #data: idDomaineRef,PathologieDomaine_idPathologieDomaine,NomDomaine
            if i.isHidden():
                self.MyPathologie.AddDomaine([-i.data(5).toList()[0].toInt()[0],i.data(5).toList()[1],i.text()])
            else:
                self.MyPathologie.AddDomaine([i.data(5).toList()[0],i.data(5).toList()[1],i.text()])
#        self.MyPathologie.Print()
        if not self.MyPathologie.CheckDoublon(self.MyPathologie.NomReference):
            self.MyPathologie.Save()
            QtGui.QToolTip.showText(QtCore.QPoint(660,100),QtCore.QString(u'Pathologie sauvegardée'), widget=None)
            self.OnPathologieDomaine()
        else:
            QtGui.QToolTip.showText(QtCore.QPoint(660,100),QtCore.QString(u'Doublon : Pathologie non sauvegardé'), widget=None)
        
    def OnAddSelection(self):
        if self.comboBox_PathologieSelection.findData(self.MyPathologie.idPathologie)==-1:
            self.comboBox_PathologieSelection.addItem(self.MyPathologie.NomReference, self.MyPathologie.idPathologie)
            self.comboBox_PathologieSelection.setCurrentIndex(self.comboBox_PathologieSelection.count()-1)
        
    def OnRemoveSelection(self):
        self.comboBox_PathologieSelection.removeItem(self.comboBox_PathologieSelection.currentIndex())  
                 
    def OnSelection(self):
        if self.NbCriteres>0:
            self.SaveCriteresConsultation()
        self.curidPathologie=self.comboBox_PathologieSelection.GetData()
        self.indexPathologie=self.MyConsult.GetIndexConsultationPathologie(self.curidPathologie)
        if not self.curidPathologie is None:
            self.MyPathologie.Get(self.curidPathologie)
        self.comboBox_Examen.Fill(self.MyPathologie.GetExamens())
        self.MyConsult.idCritere=self.comboBox_Critere.GetData()
        self.NbCriteres=0
        self.tableWidget_Criteres.clearContents()
        res=self.MyConsult.GetConsultationCriteres(self.curidPathologie)
        for i,index in zip(res,range(len(res))):
            self.FillTable(i,index)
        self.ChangedRows=[]
            
    def FillTable(self,ligne,index):
        if len(ligne)==0:
            return
        self.NbCriteres+=1
        if self.NbCriteres>self.tableWidget_Criteres.rowCount():
            self.tableWidget_Criteres.insertRow(self.tableWidget_Criteres.rowCount())
        for i,align in zip(range(6),[QtCore.Qt.AlignLeft,QtCore.Qt.AlignLeft,QtCore.Qt.AlignRight,QtCore.Qt.AlignRight,QtCore.Qt.AlignCenter,QtCore.Qt.AlignRight]):
            self.tableWidget_Criteres.setItem(self.NbCriteres-1,i,QtGui.QTableWidgetItem(ligne[i+2]))
            self.tableWidget_Criteres.item(self.NbCriteres-1,i).setTextAlignment(align)
            self.tableWidget_Criteres.item(self.NbCriteres-1,i).setData(QtCore.Qt.UserRole,QtCore.QVariant([ligne[0],ligne[1],index]))
            
    def OnExamen(self):
        if not self.comboBox_Examen.GetData() is None:
            self.curidExamen=self.comboBox_Examen.GetData()
            self.comboBox_Critere.Fill(self.MyPathologie.GetCriteres(self.curidExamen))  
            self.curidCritere=self.comboBox_Critere.GetData() 
                         
    def IsNewCritere(self,newid):
        for i in range(self.NbCriteres):
            if newid==self.tableWidget_Criteres.item(i,2).data(QtCore.Qt.UserRole).toList()[1].toInt()[0]:
                return False
        return True
        
    def OnCritere(self):
        self.tableWidget_Criteres.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.MyConsult.idCritere=self.comboBox_Critere.GetData()
        if self.MyConsult.idCritere is None:
            return
        if not self.IsNewCritere(self.MyConsult.idCritere):
            return
        res=self.MyConsult.ConsultationPathologies[self.indexPathologie].New(self.MyConsult.idCritere)
        if len(res)>0:
            self.FillTable([0,res[0],res[1],res[2],'',res[3],res[4],''],-1)
            self.tableWidget_Criteres.scrollToItem(self.tableWidget_Criteres.item(self.NbCriteres-1,2))
            self.tableWidget_Criteres.setCurrentCell(self.NbCriteres-1,2)
            self.tableWidget_Criteres.editItem(self.tableWidget_Criteres.item(self.NbCriteres-1,2))

    def OnCritereEnter(self):
        item=self.tableWidget_Criteres.currentItem()
        try:
            idConsultationCritere=item.data(QtCore.Qt.UserRole).toList()[0].toInt()[0]
            idCritere=item.data(QtCore.Qt.UserRole).toList()[1].toInt()[0]
            index=item.data(QtCore.Qt.UserRole).toList()[2].toInt()[0]
        except:
            return
        if item.column()==2:
            #remove critere if valeur=''
            if item.text()=='':
                if QtGui.QMessageBox.question(self,"OpenVet",QtCore.QString(u'Confirmation avant éffacement du critère?'),QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel)==QtGui.QMessageBox.Yes:
                    if index>=0:
                        self.MyConsult.ConsultationPathologies[self.indexPathologie].Criteres[index].idConsultationCritere*=-1
                    self.tableWidget_Criteres.removeRow(item.row())
                    self.NbCriteres-=1
                    return
            #Get Critere Grade
            res=self.MyConsult.GetCritereGrade(idCritere,item.text().toFloat()[0])
            if not res is None :
                self.tableWidget_Criteres.setItem(item.row(),5,QtGui.QTableWidgetItem(res))
                self.tableWidget_Criteres.item(item.row(),5).setTextAlignment(QtCore.Qt.AlignRight)  
        if idConsultationCritere>0:
            if not idConsultationCritere in self.ChangedRows:
                self.ChangedRows.append(idConsultationCritere) 
                
    def SaveCriteresConsultation(self):
        #attributes: idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
        for i in range(self.NbCriteres):
            ids=self.tableWidget_Criteres.item(i,2).data(QtCore.Qt.UserRole).toList()
            idCritere=ids[1].toInt()[0]
            idConsultationCritere=ids[0].toInt()[0]
            index=ids[2].toInt()[0]
            valeur=self.tableWidget_Criteres.item(i,2).text()
            grade=self.tableWidget_Criteres.item(i,5).text()
            if idConsultationCritere in self.ChangedRows or idConsultationCritere==0:
                self.MyConsult.UpdateCritere(self.indexPathologie,index,idCritere,valeur,grade)   
#        self.MyConsult.Print()
        self.MyConsult.Save()  
             
    def OnCancel(self):
        self.close()   
          
    def SaveConsultation(self):
        #SavePathologie
        self.SaveCriteresConsultation()
        self.close()         

    def OnEditCritere(self):
        #TODO: are pathologie et examen renseignés
        self.editCritere = FormCritere(self)
        if self.editCritere.exec_():
            print ('critere edité')
        
    
# class FormNewPathologie(QtGui.QDialog):
#     def __init__(self,parent=None):
#         super(FormNewPathologie,self).__init__(parent)
#         self.setWindowTitle("Edition Pathologie")
#         self.resize(394, 286)
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(icon)
#         self.buttonBox = QtGui.QDialogButtonBox(self)
#         self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
#         self.label_icone = QtGui.QLabel(self)
#         self.label_icone.setGeometry(QtCore.QRect(20, 30, 51, 51))
#         self.label_icone.setPixmap(QtGui.QPixmap(":/newPrefix/images/warning.png"))
#         self.label_icone.setScaledContents(True)
#         self.label_text = QtGui.QLabel(self)
#         self.label_text.setGeometry(QtCore.QRect(100, 30, 281, 91))
#         self.label_text.setWordWrap(True)
#         self.label_text.setText(u"Vous avez modifié un nom de référence de pathologie.\nAvant d'enregistrer cette donnée veuillez confirmer votre intention.")
#         self.groupBox = QtGui.QGroupBox(self)
#         self.groupBox.setTitle(u"Voulez-vous :")
#         self.groupBox.setGeometry(QtCore.QRect(20, 140, 351, 91))
#         self.radioButton_update = QtGui.QRadioButton(self.groupBox)
#         self.radioButton_update.setText(u"Modifier le nom de la pathologie courante")
#         self.radioButton_update.setChecked(True)
#         self.radioButton_update.setGeometry(QtCore.QRect(40, 30, 301, 22))
#         self.radioButton_add = QtGui.QRadioButton(self.groupBox)
#         self.radioButton_add.setGeometry(QtCore.QRect(40, 60, 301, 22))
#         self.radioButton_add.setText(u"Créer une nouvelle pathologie")
#         self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
#         self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
