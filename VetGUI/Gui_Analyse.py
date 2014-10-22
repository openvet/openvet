#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
# sys.path.append('../VetCore')
from Gui_ImageBrowser import FormAnalyse

import time
import Tables
import config
import Core_Analyse
from MyGenerics import *


class GuiAnalyse():
    
    def __init__(self,parent):
        self.parent=parent
        self.importAnalyse=None
        self.ModeleAnalyse=None
        self.idTypeAnalyse=None
        self.MyAnalyse=Core_Analyse.Analyse(self.parent)
        self.parent.comboBox_typeanalyse.setModel(MyComboModel(self.parent,'GetTypesanalyse'))
        
        #init dates
        now=QtCore.QDate.currentDate()
        self.parent.dateTimeEdit_analyse.setDateTime(QtCore.QDateTime.currentDateTime())
        #hide some widget
        self.HideAnalyse()
        #SetMaxLength
        self.parent.plainTextEdit_conclusions.SetMaxLength(200)
        self.parent.plainTextEdit_syntheseanalyse.SetMaxLength(65535)
        #SetContextMenus
        self.parent.listView_AnalyseImage.addActions((self.parent.DoEditDocument,self.parent.DoDeleteDoc))
        self.parent.tableView_Parametres.addAction(self.parent.DoDeleteParametre)
        #connect actions
        self.parent.connect(self.parent.DoEditDocument,QtCore.SIGNAL("triggered()"),self.OnEditAnalyseDocument)
        self.parent.connect(self.parent.DoDeleteDoc,QtCore.SIGNAL("triggered()"),self.OnDeleteAnalyseDocument)
        self.parent.connect(self.parent.DoDeleteParametre,QtCore.SIGNAL("triggered()"),self.OnDeleteParametre)
        self.parent.connect(self.parent.listView_AnalyseImage,QtCore.SIGNAL("doubleClicked (QModelIndex)"),self.OnEditAnalyseDocument)
        self.parent.connect(self.parent.listView_Analyses,QtCore.SIGNAL("activated(QModelIndex)"),self.OnListAnalyse)
        self.parent.connect(self.parent.tableView_Parametres,QtCore.SIGNAL("clicked(QModelIndex)"),self.OnClickParametre)
        self.parent.connect(self.parent.listView_AnalyseImage,QtCore.SIGNAL("clicked(QModelIndex)"),self.OnClickDocument)
        self.parent.toolButton_AddAnalyse.clicked.connect(self.OnNewAnalyse)
        self.parent.toolButton_DeleteAnalyse.clicked.connect(self.OnDeleteAnalyse)
        self.parent.pushButton_SaveAnalyse.clicked.connect(self.OnSaveAnalyse)
        self.parent.comboBox_typeanalyse.activated.connect(self.OnTypeAnalyse)
        self.parent.toolButton_EditTypeAnalyse.clicked.connect(self.OnEditTypeAnalyse)
        self.parent.connect(self.parent.comboBox_model,QtCore.SIGNAL("OnEnter"),self.OnModelAnalyse)
        self.parent.toolButton_EditModelAnalyse.clicked.connect(self.OnEditModel)
        self.parent.toolButton_EditParametre.clicked.connect(self.OnEditParametre)
        self.parent.comboBox_Parametre.activated.connect(self.OnAddParametre)
        self.parent.lineEdit_AnalyseRemarque.textChanged.connect(self.OnAnalyseRemarque)
        self.parent.pushButton_AnalyseImport.clicked.connect(self.OnImportAnalyse)
        self.parent.radioButton_Parametre.clicked.connect(self.OnVueAnalyse)
        self.parent.radioButton_Document.clicked.connect(self.OnVueAnalyse)
        
    def HideAnalyse(self):
        self.parent.tableView_Parametres.setVisible(False)
        self.parent.comboBox_Parametre.setVisible(False)
        self.parent.label_Parametre.setVisible(False)
        self.parent.toolButton_EditParametre.setVisible(False)
        self.parent.comboBox_typeanalyse.setVisible(False)
        self.parent.label_TypeAnalyse.setVisible(False)
        self.parent.toolButton_EditTypeAnalyse.setVisible(False)
        self.parent.comboBox_model.setVisible(False)
        self.parent.label_model.setVisible(False)
        self.parent.toolButton_EditModelAnalyse.setVisible(False)
        self.parent.lineEdit_AnalyseRemarque.setHidden(True)
        self.parent.label_Analyse_Remarque.setHidden(True)
        self.parent.pushButton_AnalyseImport.setHidden(True)
        self.parent.listView_AnalyseImage.setVisible(False)
        self.parent.label_Referant.setVisible(False)
        self.parent.comboBox_Referant.setVisible(False)  
        self.parent.label_VueAnalyse.setVisible(False)
        self.parent.radioButton_Parametre.setVisible(False)
        self.parent.radioButton_Document.setVisible(False)
                                  
    def SetAnimal(self,idEspece,idAnimal):
        self.idAnimal=idAnimal
        self.idEspece=idEspece
        self.MyAnalyses=MyComboModel(self.parent,'GetAnalysesAnimal(%i)'%self.idAnimal)
        self.parent.listView_Analyses.setModel(self.MyAnalyses)
        self.HideAnalyse()
    
    def SetConsultation(self,idConsultation):
        self.idConsultation=idConsultation
    
    def ResetAnalyses(self):
        self.MyAnalyses=MyComboModel(self.parent,'GetAnalysesAnimal(%i)'%self.idAnimal)
        self.parent.listView_Analyses.setModel(self.MyAnalyses)
        self.MyAnalyse.Get(0,self.idConsultation,self.idEspece)
        self.parent.dateTimeEdit_analyse.setDateTime(QtCore.QDateTime.currentDateTime())
        if self.parent.listView_AnalyseImage.model():
            self.parent.listView_AnalyseImage.model().Set(None)     
        self.HideAnalyse()
    
    def GuiAnalyse(self):
        self.parent.comboBox_typeanalyse.setVisible(True)
        self.parent.label_TypeAnalyse.setVisible(True)
        self.parent.toolButton_EditTypeAnalyse.setVisible(True)
        self.parent.pushButton_AnalyseImport.setVisible(True)
        self.parent.lineEdit_AnalyseRemarque.setHidden(False)
        self.parent.label_Analyse_Remarque.setHidden(False)
        if not self.MyAnalyse.isImage:
            self.parent.listView_AnalyseImage.setHidden(True)
            self.parent.comboBox_model.setVisible(True)
            self.parent.label_model.setVisible(True)
            self.parent.toolButton_EditModelAnalyse.setVisible(True)
            self.parent.tableView_Parametres.setHidden(False)
            self.parent.comboBox_Parametre.setHidden(False)
            self.parent.label_Parametre.setHidden(False)
            self.parent.toolButton_EditParametre.setHidden(False)
            self.parent.label_VueAnalyse.setVisible(True)
            self.parent.radioButton_Parametre.setVisible(True)
            self.parent.radioButton_Document.setVisible(True)
            self.parent.radioButton_Parametre.setChecked(True)
            model=Core_Analyse.ModelViewParameters(self.parent,5,'GetResultatParametres(%i)' % self.MyAnalyse.idAnalyse)
            model.SetEditableCol([1])
            model.SetRightAligned([1,2,3,4,5])
            self.parent.tableView_Parametres.setModel(model)  
            self.parent.tableView_Parametres.autoResize(0)
            self.parent.listView_AnalyseImage.setModel(Core_Analyse.ModelViewImages(self.parent,'GetResultatImage(%i)'%self.MyAnalyse.idAnalyse))             
        else:
            self.parent.tableView_Parametres.setHidden(True)
            self.parent.comboBox_Parametre.setHidden(True)
            self.parent.label_Parametre.setHidden(True)
            self.parent.toolButton_EditParametre.setHidden(True)
            self.parent.listView_AnalyseImage.setHidden(False)
            self.parent.label_VueAnalyse.setVisible(False)
            self.parent.radioButton_Parametre.setVisible(False)
            self.parent.radioButton_Document.setVisible(False)
            self.parent.listView_AnalyseImage.setModel(Core_Analyse.ModelViewImages(self.parent,'GetResultatImage(%i)'%self.MyAnalyse.idAnalyse))
    
    def OnVueAnalyse(self):
        if self.parent.radioButton_Parametre.isChecked():
            self.parent.listView_AnalyseImage.setHidden(True)
            self.parent.tableView_Parametres.setHidden(False)
            self.parent.comboBox_Parametre.setHidden(False)
            self.parent.label_Parametre.setHidden(False)
            self.parent.toolButton_EditParametre.setHidden(False)
        else:
            self.parent.tableView_Parametres.setHidden(True)
            self.parent.comboBox_Parametre.setHidden(True)
            self.parent.label_Parametre.setHidden(True)
            self.parent.toolButton_EditParametre.setHidden(True)
            self.parent.listView_AnalyseImage.setHidden(False)
                
    def OnListAnalyse(self,index):
        if index.isValid():
            idAnalyse=index.data(QtCore.Qt.UserRole).toInt()[0]
            self.MyAnalyse.Get(idAnalyse,self.idConsultation,self.idEspece)
            self.OnTypeAnalyse()
                    
    def OnNewAnalyse(self):
        if self.idConsultation==0:
            QtGui.QMessageBox.warning(self,u"Alerte OpenVet",'Vous devez selectionner une consultation pour entrer une nouvelle analyse', QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default)
        else:
            self.HideAnalyse()
            self.parent.comboBox_typeanalyse.setVisible(True)
            self.parent.label_TypeAnalyse.setVisible(True)
            self.parent.toolButton_EditTypeAnalyse.setVisible(True)
            self.parent.lineEdit_AnalyseRemarque.setText("")
            self.MyAnalyse.Get(0,self.idConsultation,self.idEspece)
            self.parent.dateTimeEdit_analyse.setDateTime(QtCore.QDateTime.currentDateTime())
            self.parent.lineEdit_description.setFocus()
    
    def OnDeleteAnalyse(self):  
        indexAnalyses=self.parent.listView_Analyses.currentIndex()  
        if QtGui.QMessageBox.question(self.parent,'OpenVet',u'Etes-vous sûre de vouloir effacer l\'analyse : %s ?'%self.parent.listView_Analyses.model().data(indexAnalyses,Qt.DisplayRole).toString(),QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.No:
                return
        if self.MyAnalyse.Delete(self.parent,self.parent.listView_Analyses.model().data(indexAnalyses,Qt.UserRole).toInt()[0]):
            self.ResetAnalyses()
             
    def OnDeleteParametre(self):
        index=self.parent.tableView_Parametres.currentIndex()
        if not self.MyAnalyse.Resultats.data(index,QtCore.Qt.DisplayRole).toString().isEmpty():
            if QtGui.QMessageBox.question(self,'OpenVet',u'Etes-vous sûre de vouloir effacer ce résultat?',QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.No:
                return
        self.MyAnalyse.Resultats.removeRows(index.row())
        
    def OnClickParametre(self,index):  
        self.parent.lineEdit_AnalyseRemarque.setText(self.parent.tableView_Parametres.model().data(index,Qt.ToolTipRole).toString() )    
          
    def OnClickDocument(self,index):
        self.parent.lineEdit_AnalyseRemarque.setText(self.parent.listView_AnalyseImage.model().data(index,Qt.ToolTipRole).toString())
        
    def OnAnalyseRemarque(self):
        if self.MyAnalyse.isImage or (not self.MyAnalyse.isImage and self.parent.radioButton_Document.isChecked()):
            self.parent.listView_AnalyseImage.model().setData(self.parent.listView_AnalyseImage.currentIndex(),QVariant(self.parent.lineEdit_AnalyseRemarque.text()),Qt.ToolTipRole)
        else:
            self.parent.tableView_Parametres.model().setData(self.parent.tableView_Parametres.currentIndex(),QVariant(self.parent.lineEdit_AnalyseRemarque.text()),Qt.ToolTipRole)
                    
    def OnTypeAnalyse(self):
        self.idTypeAnalyse=self.parent.comboBox_typeanalyse.Getid() 
        if self.idTypeAnalyse==0:
            return
        self.MyAnalyse.isImage= self.parent.comboBox_typeanalyse.model().data(self.parent.comboBox_typeanalyse.model().index(self.parent.comboBox_typeanalyse.currentIndex()),34).toBool()
        self.GuiAnalyse()
        if self.MyAnalyse.idAnalyse==0:
            if not self.MyAnalyse.isImage:
                self.parent.comboBox_Parametre.setModel(MyComboModel(self.parent,'GetParametres(%i,%i)'%(self.idTypeAnalyse,self.idEspece)))
                self.parent.comboBox_model.setModel(MyComboModel(self.parent,'GetModeles(%i,%i)'%(self.idTypeAnalyse,self.idEspece)))
            #TODO: else affiche image widgets ??
        else:
            self.parent.comboBox_model.setVisible(False)
            self.parent.label_model.setVisible(False)
            self.parent.toolButton_EditModelAnalyse.setVisible(False)
            self.parent.comboBox_Parametre.setModel(MyComboModel(self.parent,'GetParametres(%i,%i)'%(self.idTypeAnalyse,self.idEspece)))
               
    def OnEditTypeAnalyse(self): 
        self.idTypeAnalyse=self.parent.comboBox_typeanalyse.Getid() 
        new=[0,'',False,'',True,False,'']
        model=MyModel('TypeAnalyse',self.idTypeAnalyse,self.parent)
        if not model.SetNew(new):
            return
        data=[[u'Libélé',1,60],[u'Imagerie',2],[u'Remarque',3,200,80]]
        form=MyForm('type d\'analyse',data,self.parent)
        form.SetModel(model, {0:1,1:2,2:3})
        if form.exec_():
            self.parent.comboBox_typeanalyse.setModel(MyComboModel(self.parent,'GetTypesanalyse'))
            self.parent.comboBox_typeanalyse.Setid(self.idTypeAnalyse)
                                 
    def OnModelAnalyse(self):
        index=self.parent.comboBox_model.currentIndex()
        if not self.parent.tableView_Parametres.model().rowCount()==0:
            if QtGui.QMessageBox.question(self.parent,'OpenVet',u'Voulez-vous effacer les données présentes?',QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.Yes:
                self.parent.tableView_Parametres.model().Clear()
        idModele=self.parent.comboBox_model.Getid()
        if idModele>0:
            if not self.parent.lineEdit_description.text().isEmpty():
                if QtGui.QMessageBox.question(self.parent,'OpenVet',u'Voulez-vous assigner le nom de modèle à la description?',QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.Yes:
                    self.parent.lineEdit_description.setText(self.parent.comboBox_model.itemData(index,QtCore.Qt.DisplayRole).toString())
            else:
                self.parent.lineEdit_description.setText(self.parent.comboBox_model.itemData(index,QtCore.Qt.DisplayRole).toString())
            self.MyAnalyse.idModeleAnalyse=idModele
            debut=self.parent.tableView_Parametres.model().rowCount()
            self.parent.tableView_Parametres.model().InsertModelAnalyse(idModele,self.MyAnalyse.idAnalyse)
            self.parent.tableView_Parametres.autoResize(0)
            self.parent.tableView_Parametres.edit(self.parent.tableView_Parametres.model().index(debut, 1, QtCore.QModelIndex()))
        else:
            self.MyAnalyse.Resultats.removeRows(0,self.MyAnalyse.Resultats.rowCount())
        
    def OnEditModel(self):
        idModele=self.parent.comboBox_model.Getid()
        idTypeAnalyse=self.parent.comboBox_typeanalyse.Getid() 
        parametres=self.parent.tableView_Parametres.model().GetListParameters()
        new=[0,idTypeAnalyse,self.idEspece,'','',QDate.currentDate().toString("yyyy-MM-dd"),0,True,False,'']
        model=MyModel('ModeleAnalyse',idModele,self.parent)
        if not model.SetNew(new):
            return
        data=[[u'Libélé',1,60],[u'Paramètres',5,None,100],[u'Remarque',3,200,80]]
        form=Core_Analyse.FormModeleAnalyse(data,self.parent)
        form.SetModel(model, {0:3,2:4})
        form.fields[1].setModel(MyComboModel(self.parent,parametres))
        if form.exec_():
            self.parent.comboBox_model.setModel(MyComboModel(self.parent,'GetModeles(%i,%i)'%(self.idTypeAnalyse,self.idEspece)))
            self.parent.comboBox_model.Setid(idModele)
            
#         self.ModeleAnalyse=Core_Analyse.ModeleAnalyse(self.MyAnalyse.Resultats,max(idModele.toInt()[0],0))
#         (flag,msg)=self.ModeleAnalyse.CheckModele(idModele,self.parent.lineEdit_description.text())
#         msgbox=QtGui.QMessageBox(self.parent)
#         msgbox.setWindowTitle('OpenVet')
#         msgbox.setIcon(QtGui.QMessageBox.Question)
#         msgbox.setText(msg)
#         msgbox.addButton(QtGui.QMessageBox.Cancel)
#         if flag==3:
#             msgbox.addButton(QtCore.QString('Modifier'),QtGui.QMessageBox.AcceptRole)
#             msgbox.addButton(QtCore.QString('Supprimer'),QtGui.QMessageBox.AcceptRole)
#             choix=msgbox.exec_()
#             if choix==1:
#                 self.ModeleAnalyse.ToDelete=True
#                 err=self.ModeleAnalyse.Save()
#                 self.MyAnalyse.Resultats.Modeles.removeRows(self.parent.comboBox_model.currentIndex())
#                 self.parent.lineEdit_description.setText(QtCore.QString(''))
#                 self.parent.comboBox_model.setCurrentIndex(0)               
#             if choix==0:
#                 MyModele=FormModeleAnalyse(self.ModeleAnalyse)
#                 if MyModele.exec_():
#                     err=self.ModeleAnalyse.Save() 
#         else:
#             msgbox.addButton(QtGui.QMessageBox.Yes)
#             if msgbox.exec_()==QtGui.QMessageBox.Yes:
#                 MyModele=FormModeleAnalyse(self.ModeleAnalyse)
#                 if MyModele.exec_():
#                     err=self.ModeleAnalyse.Save()
#                     self.MyAnalyse.Resultats.SetModele(self.idTypeAnalyse,self.idEspece)
#                     self.parent.comboBox_model.setModel(self.MyAnalyse.Resultats.Modeles)
#                     index=self.MyAnalyse.Resultats.Modeles.GetIndex(self.ModeleAnalyse.Modele)
#                     self.parent.comboBox_model.setCurrentIndex(index)  
    
    def OnEditParametre(self):
        idParametre=self.parent.comboBox_Parametre.Getid()
        new=[0,self.idTypeAnalyse,self.idEspece,'',False,15,0,0,'',True,False,'']
        model=MyModel('Parametre',idParametre,self.parent)
        if not model.SetNew(new):
            return
        data=[[u'Paramètre',1,60],[u'Remarque',3,200,80],[u'Quantitatif',2],[u'unité',4,None,None,u'Edite l\'unité'],[u'Nome Min',1,9],[u'Nome Max',1,9]]
        form=Core_Analyse.FormParametre(idParametre,data,self.parent)
        form.SetModel(model, {0:3,1:8,2:4,3:5,4:6,5:7})
        if form.exec_():
            self.parent.comboBox_Parametre.setModel(MyComboModel(self.parent,'GetParametres(%i,%i)'%(self.idTypeAnalyse,self.idEspece)))
            self.parent.comboBox_typeanalyse.Setid(idParametre)
    
    def OnAddParametre(self):        
        i=self.parent.comboBox_Parametre.model().listdata[self.parent.comboBox_Parametre.currentIndex()]
#       idParametre=i[0]
        if self.parent.tableView_Parametres.model().isExist(i[0],10)==0:
            data=[QVariant(0),i[1],QVariant(),i[6],i[7],i[8],QVariant(i[2]),QVariant(0),QVariant(0),i[5],i[0],QVariant(self.MyAnalyse.idAnalyse),QVariant()]
            self.parent.tableView_Parametres.model().insertRows(self.parent.comboBox_Parametre.model().rowCount(),data)
            self.parent.tableView_Parametres.autoResize(0)
            self.parent.tableView_Parametres.edit(self.parent.tableView_Parametres.model().index(self.parent.tableView_Parametres.model().rowCount()-1, 1, QtCore.QModelIndex()))
        else:
            QtGui.QMessageBox.warning(self.parent,u"Alerte OpenVet",u'Ce paramètre est déjà présent dans la liste.', QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default)
                
    def OnImportAnalyse(self):
        self.importAnalyse = FormAnalyse(self.parent)
        if self.importAnalyse.exec_():
            if not self.parent.listView_AnalyseImage.model().isDoublon(self.importAnalyse.Etiquette,self.importAnalyse.FichierInterne):
                self.parent.listView_AnalyseImage.model().NewLine([0,self.importAnalyse.Titre,'',self.importAnalyse.Etiquette,0,self.importAnalyse.FichierInterne,self.MyAnalyse.idAnalyse,QVariant()])
            else:
                QtGui.QMessageBox.warning(self.parent,u"Alerte OpenVet",u'Cette image est déjà présente dans la liste.', QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default)                 
                
    def OnEditAnalyseDocument(self,index=None):
        if index is None:
            index=self.parent.listView_AnalyseImage.currentIndex()
        self.importAnalyse = FormAnalyse(self.parent)
        self.importAnalyse.Set(self.parent.listView_AnalyseImage.model().GetDocument(index))
        if self.importAnalyse.exec_():
            self.parent.listView_AnalyseImage.model().setData(index,self.importAnalyse.Titre)
        
    def OnDeleteAnalyseDocument(self):
        index=self.parent.listView_AnalyseImage.currentIndex()
        self.parent.listView_AnalyseImage.model().DeleteLine(index)
                         
    def OnSaveAnalyse(self):
        valid=self.MyAnalyse.Save()
        QtGui.QToolTip.showText(QtGui.QCursor.pos(),valid, widget=None)
        self.ResetAnalyses()
        
