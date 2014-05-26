#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_consultation import Ui_tabWidget_medical
from Gui_Pathologie import FormPathologie
#import Gui_Core
import time
import Tables
import config
import Core_Consultation
import Core_Pathologie
import Core_Critere



class TabConsultation(QtGui.QTabWidget,Ui_tabWidget_medical):
    dataClient=''
    dataAnimal=''
    idClient=0
    idAnimal=1
    idEspece=1
    idConsultation=0
    NewConsultation=True
    
    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self,parent)
        self.setupUi(self)
        self.DBase=Tables.DataBase(config.database)
        self.editClient = None
        self.editAnimal = None
        self.editPathologie=None
        self.TypeConsultationDefaut=3
        self.MyConsult= Core_Consultation.Consultation(self.DBase,0)     #TODO: transmit DataBase Connection object
        self.MyPathologie=Core_Pathologie.Pathologie(self.DBase)
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
        #connect actions
        self.comboBox_consultType.currentIndexChanged.connect(self.OnTypeConsultation)
        #self.connect(self.comboBox_veterinaire,QtCore.SIGNAL("keyPressEvent(QKeyEvent)"),self.OnNewConsultant)
        self.comboBox_PathologieDomaine.currentIndexChanged.connect(self.OnDomaine)
        self.connect(self.comboBox_Pathologie, QtCore.SIGNAL("highlighted(int)"),self.OnPathologie)
        self.connect(self.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationSelect)
        self.toolButton_comment.clicked.connect(self.EditCommentaire)
        self.connect(self.comboBox_veterinaire,QtCore.SIGNAL("OnEnter"),self.OnConsultantEnter)
        self.toolButton_Pathologie.clicked.connect(self.EditPathologie)
        self.pushButton_valider.clicked.connect(self.SaveConsultation)
        self.pushButton_Nouveau.clicked.connect(self.OnNewConsultation)
              
    def FillConsultation_Combo(self):
        self.comboBox_veterinaire.Fill(self.MyConsult.GetConsultants())
        self.comboBox_Referant.Fill(self.MyConsult.GetReferants())
        self.comboBox_consultType.Fill(self.MyConsult.GetTypesConsultation())
        self.comboBox_PathologieDomaine.Fill(self.MyPathologie.GetDomaines())
        self.comboBox_Pathologie.Fill(self.MyPathologie.GetPathologies(0,u'Néant'))
                    
    def OnSelectAnimal(self):
        #TODO get idEspece from animal
        self.idEspece=1
        #MAKE consultation enabled
        self.MyConsult.Animal_idAnimal=self.idEspece
        self.MyPathologie.SetEspece(self.idEspece)
        self.FillConsultation_Combo()
        self.GetConsultations()
            
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
