#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_consultation import Ui_tabWidget_medical
from Gui_Pathologie import FormPathologie
from Gui_Analyse import FormAnalyse
from Gui_ModeleAnalyse import FormModeleAnalyse

#import Gui_Core
import time
import Tables
import config
import Core_Consultation
import Core_Pathologie
import Core_Critere
import Core_Analyse



class TabConsultation(QtGui.QTabWidget,Ui_tabWidget_medical):
    dataClient=''
    dataAnimal=''
    idClient=0
    idAnimal=1
    idEspece=1
    idConsultation=0
    NewConsultation=True
    
    def __init__(self,parent=None):
        QtGui.QTabWidget.__init__(self,parent)
        self.setupUi(self)
        self.DBase=Tables.DataBase(config.database)
        self.Qbase=parent.db
        #self.MyQuery
        self.editClient = None
        self.editAnimal = None
        self.editPathologie=None
        self.importAnalyse=None
        self.TypeConsultationDefaut=3
        self.MyConsult= Core_Consultation.Consultation(self.DBase,0)     #TODO: transmit DataBase Connection object
        self.MyPathologie=Core_Pathologie.Pathologie(self.DBase)
        self.MyAnalyse=Core_Analyse.Analyse(self)
        self.ModeleAnalyse=None
        #init dates
        now=QtCore.QDate.currentDate()
        self.dateEdit_consult.setDate(now)
        self.dateEdit_vacciner_start.setDate(now)
        self.dateEdit_vacciner_end.setDate(now)
        self.dateEdit_ordonance.setDate(now)
        self.dateEdit_docDate.setDate(now)
        self.dateTimeEdit_analyse.setDateTime(QtCore.QDateTime.currentDateTime())
        #hide some widget
        self.HideAnalyse()
        #SetMaxLength
        self.plainTextEdit_conclusions.SetMaxLength(200)
        self.plainTextEdit_syntheseanalyse.SetMaxLength(65535)
        #SetContextMenus
        self.listView_AnalyseImage.addActions((self.DoEditDocument,self.DoDeleteDoc))
        self.tableView_Parametres.addAction(self.DoDeleteParametre)
        #connect actions
        #____________________________***   Tab_Consultation   ***__________________________
        self.comboBox_consultType.currentIndexChanged.connect(self.OnTypeConsultation)
        self.comboBox_PathologieDomaine.currentIndexChanged.connect(self.OnDomaine)
        self.connect(self.comboBox_Pathologie, QtCore.SIGNAL("highlighted(int)"),self.OnPathologie)
        self.connect(self.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationSelect)
        self.toolButton_comment.clicked.connect(self.EditCommentaire)
        self.connect(self.comboBox_veterinaire,QtCore.SIGNAL("OnEnter"),self.OnConsultantEnter)
        self.toolButton_Pathologie.clicked.connect(self.EditPathologie)
        self.pushButton_valider.clicked.connect(self.SaveConsultation)
        self.pushButton_Nouveau.clicked.connect(self.OnNewConsultation)
        #____________________________***  Tab_Analyses   ***______
        self.connect(self.DoEditDocument,QtCore.SIGNAL("triggered()"),self.OnEditAnalyseDocument)
        self.connect(self.DoDeleteDoc,QtCore.SIGNAL("triggered()"),self.OnDeleteAnalyseDocument)
        self.connect(self.DoDeleteParametre,QtCore.SIGNAL("triggered()"),self.OnDeleteParametre)
        self.connect(self.listView_AnalyseImage,QtCore.SIGNAL("doubleClicked (QModelIndex)"),self.OnEditAnalyseDocument)
        self.connect(self.listView_Analyses,QtCore.SIGNAL("activated(QModelIndex)"),self.OnListAnalyse)
        self.connect(self.tableView_Parametres,QtCore.SIGNAL("clicked(QModelIndex)"),self.OnClickParametre)
        self.connect(self.listView_AnalyseImage,QtCore.SIGNAL("clicked(QModelIndex)"),self.OnClickDocument)
        self.toolButton_AddAnalyse.clicked.connect(self.OnNewAnalyse)
        self.pushButton_SaveAnalyse.clicked.connect(self.OnSaveAnalyse) 
        self.connect(self.comboBox_typeanalyse,QtCore.SIGNAL("currentIndexChanged(int)"),self.OnTypeAnalyse)
        self.connect(self.comboBox_model,QtCore.SIGNAL("currentIndexChanged(int)"),self.OnModelAnalyse)
        self.toolButton_EditModelAnalyse.clicked.connect(self.OnEditModel)
        self.comboBox_Parametre.activated.connect(self.OnAddParametre)
        self.lineEdit_AnalyseRemarque.textChanged.connect(self.OnAnalyseRemarque)
        self.pushButton_AnalyseImport.clicked.connect(self.OnImportAnalyse)
        self.radioButton_Parametre.clicked.connect(self.OnVueAnalyse)
        self.radioButton_Document.clicked.connect(self.OnVueAnalyse)
        
    def HideAnalyse(self):
        self.tableView_Parametres.setVisible(False)
        self.comboBox_Parametre.setVisible(False)
        self.label_Parametre.setVisible(False)
        self.toolButton_EditParametre.setVisible(False)
        self.comboBox_typeanalyse.setVisible(False)
        self.label_TypeAnalyse.setVisible(False)
        self.toolButton_EditTypeAnalyse.setVisible(False)
        self.comboBox_model.setVisible(False)
        self.label_model.setVisible(False)
        self.toolButton_EditModelAnalyse.setVisible(False)
        self.lineEdit_AnalyseRemarque.setHidden(True)
        self.label_Analyse_Remarque.setHidden(True)
        self.pushButton_AnalyseImport.setHidden(True)
        self.listView_AnalyseImage.setVisible(False)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)  
        self.label_VueAnalyse.setVisible(False)
        self.radioButton_Parametre.setVisible(False)
        self.radioButton_Document.setVisible(False)
               
    def FillConsultation_Combo(self):
        self.comboBox_veterinaire.Fill(self.MyConsult.GetConsultants())
        self.comboBox_Referant.Fill(self.MyConsult.GetReferants())
        self.comboBox_consultType.Fill(self.MyConsult.GetTypesConsultation())
        self.comboBox_PathologieDomaine.Fill(self.MyPathologie.GetDomaines())
        self.comboBox_Pathologie.Fill(self.MyPathologie.GetPathologies(0,u'Néant'))
                    
    def OnSelectAnimal(self):
        #TODO get idEspece from animal
        #MAKE consultation enabled
        self.MyConsult.Animal_idAnimal=self.idAnimal
        self.MyPathologie.SetEspece(self.idEspece)
        self.FillConsultation_Combo()
        self.GetConsultations()
        self.MyAnalyses=Core_Analyse.Analyses(self.idAnimal)
        self.listView_Analyses.setModel(self.MyAnalyses)
        self.HideAnalyse()
             
    def GetConsultations(self):
        MyDossier=Core_Consultation.Consultations(self.DBase,self.idAnimal)
        self.textBrowser_consultations.setText(MyDossier.Get())
        self.splitter.resize(1021,820)
        
    def OnConsultationSelect(self,link):
        self.FillConsultation_Combo()
        self.NewConsultation=False
        self.idConsultation=int(link.toString().toAscii()[2:])
        if link.toString().toAscii()[1]=='C':
            self.FillFormConsultation()
        if link.toString().toAscii()[1]=='N':
            self.OnNewConsultation()   
        if link.toString().toAscii()[1]=='B':
            print 'view biologie'
        if link.toString().toAscii()[1]=='I':
            print 'view Images'
        if link.toString().toAscii()[1]=='c':
            print 'view Chirurgies'
        if link.toString().toAscii()[1]=='O':
            print 'view Ordonnance'
        if link.toString().toAscii()[1]=='T':
            print 'view Plan thérapeutique'     
      
    def FillFormConsultation(self):
        self.MyConsult.Get(self.idConsultation)
        self.dateEdit_consult.setDate(self.MyConsult.DateConsultation)
        self.dateTimeEdit_analyse.setDate(self.MyConsult.DateConsultation)
        self.comboBox_veterinaire.setCurrentIndex(self.comboBox_veterinaire.findText(self.MyConsult.Consultant))
        index=self.comboBox_consultType.findData(self.MyConsult.TypeConsultation_idTypeConsultation)
        if index>-1:
            self.comboBox_consultType.setCurrentIndex(index)
        if len(self.MyConsult.Referant)>0:
            self.comboBox_Referant.setCurrentIndex(self.comboBox_Referant.findText(self.MyConsult.Referant))
        self.textEdit_consultObs.setText(self.MyConsult.Examen)
        self.textEdit_consultTrait.setText(self.MyConsult.Traitement)
        self.toolButton_comment.setToolTip(self.MyConsult.Commentaires)  
        if not self.MyConsult.DomainePathologie is None:
            self.comboBox_PathologieDomaine.setCurrentIndex(self.comboBox_PathologieDomaine.findText(QtCore.QString(self.MyConsult.DomainePathologie)))
        #TODO: debug si pas de pathologie
        index=self.comboBox_Pathologie.findText(self.MyConsult.ConsultationPathologiesString())
        if index==-1 and not self.MyConsult.ConsultationPathologiesString().isEmpty():
            self.comboBox_Pathologie.setVisible(False)
            self.label_Pathologie.setText(QtCore.QString(u'                                       Pathologies multiples  >>>'))
            self.label_Pathologie.setMaximumWidth(341)
        else:
            self.label_Pathologie.setMaximumWidth(81)
            self.label_Pathologie.setText(QtCore.QString(u'Pathologie'))
            self.comboBox_Pathologie.setVisible(True)
            if index==-1:
                self.comboBox_Pathologie.setCurrentIndex(0)
            else:
                self.comboBox_Pathologie.setCurrentIndex(index)
        self.splitter.resize(1021,460)
        
    def OnTypeConsultation(self):
        if self.comboBox_consultType.currentText()==QtCore.QString("Référée".decode('utf8')):
            self.label_Referant.setVisible(True)
            self.comboBox_Referant.setVisible(True)
        else:
            self.label_Referant.setVisible(False)
            self.comboBox_Referant.setVisible(False)

    def OnDomaine(self):
        iddomaine=self.comboBox_PathologieDomaine.itemData(self.comboBox_PathologieDomaine.currentIndex())
        self.comboBox_Pathologie.Fill(self.MyPathologie.GetPathologies(iddomaine.toInt()[0],u'Néant'))
        
    def OnPathologie(self,link):
        if link>0:
            txt=self.MyPathologie.GetDefinitionPathologie(self.comboBox_Pathologie.itemData(link).toInt()[0])
            QtGui.QToolTip.showText(QtGui.QCursor.pos(), QtCore.QString(txt), widget=self.comboBox_Pathologie)
     
    def OnConsultantEnter(self):
        print'Ouvre formulaire veto'
        
    def UpdateConsultation_mdl(self):
        #attributes: idConsultation,Animal_idAnimal,DateConsultation,TypeConsultation_idTypeConsultation,Personne_idConsultant,Personne_idReferant,
        #Personne_idReferent,Examen,Traitement,Actif,Commentaires
        self.MyConsult.idConsultation=self.idConsultation
        self.MyConsult.DateConsultation=self.dateEdit_consult.date()      
        self.MyConsult.Personne_idConsultant=self.comboBox_veterinaire.GetData()
        self.MyConsult.Consultant=self.comboBox_veterinaire.currentText()
        self.MyConsult.TypeConsultation_idTypeConsultation=self.comboBox_consultType.GetData()
        self.MyConsult.TypeConsultation=self.comboBox_consultType.currentText()
        if self.comboBox_Referant.isVisible():
            self.MyConsult.Personne_idReferant=self.comboBox_Referant.GetData()
            self.MyConsult.Referant=self.comboBox_Referant.currentText()
        else:
            self.MyConsult.Personne_idReferant=None
        self.MyConsult.Examen=self.textEdit_consultObs.toPlainText()
        self.MyConsult.Traitement=self.textEdit_consultTrait.toPlainText()
        self.MyConsult.Animal_idAnimal=self.idAnimal
        if self.comboBox_Pathologie.isVisible():
            idpathologie=self.comboBox_Pathologie.GetData()
            if idpathologie>0:
                if not self.MyConsult.CheckDoublonPathologieRef(idpathologie):
                    tmp=Core_Critere.CriteresConsultation(idpathologie,self)
                    self.MyConsult.ConsultationPathologies.append(tmp)
            
    def SaveConsultation(self):
        self.UpdateConsultation_mdl()
        self.idConsultation=self.MyConsult.Save()
        #TODO: tooltip "Sauvegarde réussie"ou bouton disabled. Enabled apres saisie,onConsultation select, On NewConsulatation
        self.NewConsultation=True
             
    def EditCommentaire(self):
        form=FormComment()
        form.plainTextEdit.insertPlainText(self.MyConsult.Commentaires)
        if form.exec_():
            self.MyConsult.Commentaires=form.plainTextEdit.toPlainText()
            self.toolButton_comment.setToolTip(QtCore.QString(self.MyConsult.Commentaires))
      
    def OnNewConsultation(self):
        self.NewConsultation=True
        self.idConsultation=0
        self.dateEdit_consult.setDate(QtCore.QDate.currentDate())
        self.comboBox_veterinaire.setCurrentIndex(0)
        self.comboBox_consultType.setCurrentIndex(self.TypeConsultationDefaut)
        self.comboBox_Referant.setCurrentIndex(0)
        self.label_Pathologie.setMaximumWidth(81)
        self.label_Pathologie.setText(QtCore.QString(u'Pathologie'))
        self.comboBox_Pathologie.setVisible(True)
        self.comboBox_PathologieDomaine.setCurrentIndex(0)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)
        self.textEdit_consultObs.clear()
        self.textEdit_consultTrait.clear()
        self.toolButton_comment.setToolTip(QtCore.QString('Ajouter un Commentaire'))
        self.splitter.resize(1021,470) 
    
    def EditPathologie(self):
        #TODO: save Consultation & update idConsultation
        self.SaveConsultation()
        if self.editPathologie is None:
            self.editPathologie = FormPathologie(self)
        if self.editPathologie.exec_():
            self.editPathologie.tableWidget_Criteres.clearContents()
            self.editPathologie.NbCriteres=0
            print 'Pathologie éditée'
     
#________________________________________________***  A N A L Y S E S ***_______________________________________________________
    def GuiAnalyse(self):
        self.comboBox_typeanalyse.setVisible(True)
        self.label_TypeAnalyse.setVisible(True)
        self.toolButton_EditTypeAnalyse.setVisible(True)
        self.pushButton_AnalyseImport.setVisible(True)
        self.lineEdit_AnalyseRemarque.setHidden(False)
        self.label_Analyse_Remarque.setHidden(False)
        if not self.MyAnalyse.isImage:
            self.listView_AnalyseImage.setHidden(True)
            self.comboBox_model.setVisible(True)
            self.label_model.setVisible(True)
            self.toolButton_EditModelAnalyse.setVisible(True)
            self.tableView_Parametres.setHidden(False)
            self.comboBox_Parametre.setHidden(False)
            self.label_Parametre.setHidden(False)
            self.toolButton_EditParametre.setHidden(False)
            self.label_VueAnalyse.setVisible(True)
            self.radioButton_Parametre.setVisible(True)
            self.radioButton_Document.setVisible(True)
            self.radioButton_Parametre.setChecked(True)
            self.tableView_Parametres.setModel(self.MyAnalyse.Resultats)
            self.tableView_Parametres.setColumnHidden(0,True)
            self.tableView_Parametres.resizeColumnsToContents()
    #        if not self.MyAnalyse.Resultats is None:
    #            self.connect(self.MyAnalyse.Resultats,QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"),self.OnParametreChanged)
            if not self.MyAnalyse.Documents is None:
                self.listView_AnalyseImage.setModel(self.MyAnalyse.Documents) 
        else:
            self.tableView_Parametres.setHidden(True)
            self.comboBox_Parametre.setHidden(True)
            self.label_Parametre.setHidden(True)
            self.toolButton_EditParametre.setHidden(True)
            self.listView_AnalyseImage.setHidden(False)
            self.label_VueAnalyse.setVisible(False)
            self.radioButton_Parametre.setVisible(False)
            self.radioButton_Document.setVisible(False)
            if not self.MyAnalyse.Documents is None:
                self.listView_AnalyseImage.setModel(self.MyAnalyse.Documents)
    
    def OnVueAnalyse(self):
        if self.radioButton_Parametre.isChecked():
            self.listView_AnalyseImage.setHidden(True)
            self.tableView_Parametres.setHidden(False)
            self.comboBox_Parametre.setHidden(False)
            self.label_Parametre.setHidden(False)
            self.toolButton_EditParametre.setHidden(False)
        else:
            self.tableView_Parametres.setHidden(True)
            self.comboBox_Parametre.setHidden(True)
            self.label_Parametre.setHidden(True)
            self.toolButton_EditParametre.setHidden(True)
            self.listView_AnalyseImage.setHidden(False)
                
    def OnListAnalyse(self,index):
        if index.isValid():
            idAnalyse=index.data(QtCore.Qt.UserRole).toInt()[0]
            self.MyAnalyse.Get(idAnalyse,self.idConsultation,self.idEspece)
            self.OnTypeAnalyse(None)
                    
    def OnNewAnalyse(self):
        if self.idConsultation==0:
            QtGui.QMessageBox.warning(self,u"Alerte OpenVet",'Vous devez selectionner une consultation pour entrer une nouvelle analyse', QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default)
        else:
            self.HideAnalyse()
            self.comboBox_typeanalyse.setVisible(True)
            self.label_TypeAnalyse.setVisible(True)
            self.toolButton_EditTypeAnalyse.setVisible(True)
            self.lineEdit_AnalyseRemarque.setText("")
            self.MyAnalyse.Get(0,self.idConsultation,self.idEspece)
            self.dateTimeEdit_analyse.setDateTime(QtCore.QDateTime.currentDateTime())
            self.lineEdit_description.setFocus()
        
    def OnDeleteParametre(self):
        index=self.tableView_Parametres.currentIndex()
        if not self.MyAnalyse.Resultats.data(index,QtCore.Qt.DisplayRole).toString().isEmpty():
            if QtGui.QMessageBox.question(self,'OpenVet',u'Etes-vous sûre de vouloir effacer ce résultat?',QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.No:
                return
        self.MyAnalyse.Resultats.removeRows(index.row())
        
    def OnClickParametre(self,index):   
        self.lineEdit_AnalyseRemarque.setText(self.MyAnalyse.Resultats.GetRemarque(index))    
          
    def OnClickDocument(self,index):
        self.lineEdit_AnalyseRemarque.setText(self.MyAnalyse.Documents.GetRemarque(index))
        
    def OnAnalyseRemarque(self):
        if self.MyAnalyse.isImage:
            self.MyAnalyse.Documents.SetRemarque(self.lineEdit_AnalyseRemarque.text())
        elif not self.MyAnalyse.isImage and self.radioButton_Document.isChecked():
            self.MyAnalyse.Documents.SetRemarque(self.lineEdit_AnalyseRemarque.text())
        else:
            self.MyAnalyse.Resultats.SetRemarque(self.lineEdit_AnalyseRemarque.text())
                    
    def OnTypeAnalyse(self,index=None):
        parametre=self.MyAnalyse.GetIdTypeAnalyse(self.comboBox_typeanalyse.currentText())
        self.MyAnalyse.IsQuantitatif(self.comboBox_typeanalyse.currentText())
        if parametre is None:
            return
        self.GuiAnalyse()
        if self.MyAnalyse.idAnalyse==0:
            if not self.MyAnalyse.isImage:
                self.MyAnalyse.Resultats.SetParametres(parametre,self.idEspece) #init Modeles in the same time
                self.comboBox_Parametre.setModel(self.MyAnalyse.Resultats.Parametres)
                self.comboBox_Parametre.setModelColumn(5)
                self.comboBox_model.setModel(self.MyAnalyse.Resultats.Modeles)
        else:
            if self.MyAnalyse.Resultats is None:
                return  #Myanalyse have been modified by Table.SetFilter and so have been combobox.TypeAnalyse, but Resultats have not been initiated yet. 
            self.comboBox_model.setVisible(False)
            self.label_model.setVisible(False)
            self.toolButton_EditModelAnalyse.setVisible(False)
            self.MyAnalyse.Resultats.SetParametres(parametre,self.idEspece)
            self.comboBox_Parametre.setModel(self.MyAnalyse.Resultats.Parametres)
            self.comboBox_Parametre.setModelColumn(5)    
                             
    def OnModelAnalyse(self,index=None):
        if not self.MyAnalyse.Resultats.isEmpty():
            if QtGui.QMessageBox.question(self,'OpenVet',u'Voulez-vous effacer les données présentes?',QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.No:
                return
        idModele=self.comboBox_model.itemData(index,QtCore.Qt.UserRole)
        if idModele.toInt()[0]>0:
            #TODO: if self.lineEdit_description.Text.isEmpty()
            self.lineEdit_description.setText(self.comboBox_model.itemData(index,QtCore.Qt.DisplayRole).toString())
            self.ModeleAnalyse=Core_Analyse.ModeleAnalyse(self.MyAnalyse.Resultats,idModele)
            self.tableView_Parametres.edit(self.MyAnalyse.Resultats.index(0,2))
        
    def OnEditModel(self):
        idModele=self.comboBox_model.itemData(self.comboBox_model.currentIndex(),QtCore.Qt.UserRole)
        self.ModeleAnalyse=Core_Analyse.ModeleAnalyse(self.MyAnalyse.Resultats,idModele)
        (flag,msg)=self.ModeleAnalyse.CheckModele(idModele,self.lineEdit_description.text())
        #TODO: if flag==3: 3 boutons (supprimer,modifier,annuler)
        if QtGui.QMessageBox.question(self,'OpenVet',msg,QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.Cancel)==QtGui.QMessageBox.Yes:
            if flag==3:
                self.ModeleAnalyse.ToDelete=True
            else:
                MyModele=FormModeleAnalyse(self.ModeleAnalyse)
                if MyModele.exec_():
                    self.ModeleAnalyse.Save()
        
    def OnAddParametre(self):
        index=self.comboBox_Parametre.currentIndex()
        if self.MyAnalyse.Resultats.insertRows(0,index):
            self.tableView_Parametres.edit(self.MyAnalyse.Resultats.index(self.MyAnalyse.Resultats.rowCount()-1, 2, QtCore.QModelIndex()))
        else:
            QtGui.QMessageBox.warning(self,u"Alerte OpenVet",u'Ce paramètre est déjà présent dans la liste.', QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default)
                
    def OnImportAnalyse(self):
        self.importAnalyse = FormAnalyse(self)
        if self.importAnalyse.exec_():
            if self.MyAnalyse.Documents.insertRows(0,[self.importAnalyse.Titre,self.importAnalyse.Etiquette,self.importAnalyse.FichierInterne]):
                QtGui.QMessageBox.warning(self,u"Alerte OpenVet",u'Cette image est déjà présente dans la liste.', QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default)
                
    def OnEditAnalyseDocument(self,index=None):
        if index is None:
            index=self.listView_Analyses.currentIndex()
        self.importAnalyse = FormAnalyse(self)
        self.importAnalyse.Set(self.MyAnalyse.Documents.GetDocument(index))
        if self.importAnalyse.exec_():
            self.MyAnalyse.Documents.setData(index,QtCore.QVariant(self.importAnalyse.Titre))
        
    def OnDeleteAnalyseDocument(self):
        index=self.listView_Analyses.currentIndex()
        self.MyAnalyse.Documents.RemoveRow(index.row())
                         
    def OnSaveAnalyse(self):
        valid=self.MyAnalyse.Save()
        QtGui.QToolTip.showText(QtGui.QCursor.pos(),valid, widget=None)
        self.MyAnalyses=Core_Analyse.Analyses(self.idAnimal)
        self.listView_Analyses.setModel(self.MyAnalyses)      
            
class FormComment(QtGui.QDialog):
    def __init__(self,parent=None):
        super(FormComment,self).__init__(parent)
        self.resize(400, 255)
        self.setWindowTitle("Edition Consultation")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 17))
        self.label.setText("Entrez votre commentaire :")
        self.plainTextEdit = QtGui.QPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 361, 141))
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TabConsultation()
    window.show()
    window.OnSelectAnimal()
    sys.exit(app.exec_())
