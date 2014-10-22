#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')

import time
#import config

from MyGenerics import *
from Core_Consultation import *


class GuiConsultation():
    idConsultation=0
    NewConsultation=True
    
    def __init__(self,parent=None):
        self.Qbase=parent.Qbase
#        self.DBase=Tables.DataBase(config.database) # TODO: remove line
        self.parent=parent
#        self.editPathologie=None
#        self.MyPathologie=Core_Pathologie.Pathologie(self.DBase)     #TODO: use QBase or Request

        #init dates
        self.parent.pushButton_valider.setEnabled(False)
        now=QtCore.QDate.currentDate()
        self.parent.dateEdit_consult.setDate(now)
        
        #connect actions
        #____________________________***   Tab_Consultation   ***__________________________
        self.parent.comboBox_consultType.currentIndexChanged.connect(self.OnTypeConsultation)
        self.parent.toolButton_TypeConsultation.clicked.connect(self.OnEditTypeConsultation)
        self.parent.comboBox_PathologieDomaine.currentIndexChanged.connect(self.OnDomaine)
#        self.parent.connect(self.parent.comboBox_Pathologie,QtCore.SIGNAL("currentIndexChanged(int)"),self.OnPathologie)
        self.parent.connect(self.parent.comboBox_Pathologie,QtCore.SIGNAL("OnEnter"),self.OnPathologieEnter)
        self.parent.connect(self.parent.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationSelect)
        self.parent.toolButton_comment.clicked.connect(self.EditCommentaire)
        self.parent.connect(self.parent.comboBox_veterinaire,QtCore.SIGNAL("OnEnter"),self.OnConsultantEnter)
        self.parent.toolButton_EditPathologie.clicked.connect(self.EditPathologie)
        self.parent.toolButton_Pathologie.clicked.connect(self.EditCriteresConsultation)
        self.parent.toolButton_EditDomaine.clicked.connect(self.EditDomaine)
        self.parent.pushButton_valider.clicked.connect(self.SaveConsultation)
        self.parent.pushButton_Nouveau.clicked.connect(self.OnNewConsultation)

    def SetAnimal(self,idEspece,idAnimal):
        self.idEspece=idEspece
        self.idAnimal=idAnimal
        self.MyConsultation= Consultation(self.idAnimal,0,self.parent)
        
        self.mapper = QDataWidgetMapper(self.parent)
        self.mapper.setOrientation(Qt.Horizontal)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyConsultation)
        self.MyDelegate=GenericDelegate(self.parent)
        for i in range(2,8):
            self.MyDelegate.insertFieldDelegate(i,self.MyConsultation.Fields[i]) 
        self.mapper.setItemDelegate(self.MyDelegate)
        self.mapper.addMapping(self.parent.dateEdit_consult,2)
        self.mapper.addMapping(self.parent.comboBox_consultType,3)
        self.mapper.addMapping(self.parent.comboBox_veterinaire,4)#Change to Consultant
        self.mapper.addMapping(self.parent.comboBox_Referant,5)
        self.mapper.addMapping(self.parent.textEdit_consultObs,6)#Change to PlainText
        self.mapper.addMapping(self.parent.textEdit_consultTrait,7)#Change to PlainText
        self.FillConsultation_Combo()
        self.mapper.toFirst()
        self.GetConsultations()                
#        self.MyPathologie.SetEspece(self.idEspece)

                   
    def FillConsultation_Combo(self):
        self.parent.comboBox_veterinaire.setModel(MyComboModel(self.parent,'GetConsultants'))
        self.parent.comboBox_Referant.setModel(MyComboModel(self.parent,'GetReferants'))
        self.parent.comboBox_consultType.setModel(MyComboModel(self.parent,'GetTypesConsultation'))
        self.parent.comboBox_PathologieDomaine.setModel(MyComboModel(self.parent,'GetDomaines',u'Tous'))
                                
    def GetConsultations(self):
        MyDossier=Consultations(self.parent,self.idAnimal)
        self.parent.textBrowser_consultations.setText(MyDossier.Get())
        self.parent.splitter.resize(1021,820)
        
    def OnConsultationSelect(self,link):
        self.idConsultation=int(link.toString().toAscii()[2:])
        self.parent.GuiAnalyse.SetConsultation(self.idConsultation)
        self.MyConsultation.SetConsultation(self.idConsultation)
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
        self.parent.pushButton_valider.setEnabled(True)
        self.mapper.toFirst()
        self.parent.toolButton_comment.setToolTip(self.MyConsultation.Fdata(COMMENTAIRE))
        self.parent.label_Pathologies.setText("<font color=\"blue\">* %s *</font>"%self.MyConsultation.Pathologies.LinePathologies)
#         if self.MyConsultation.Pathologies.Count()<=1:
#             self.parent.label_Pathologie.setMaximumWidth(81)
#             self.parent.label_Pathologie.setText(QtCore.QString(u'Pathologie'))
#             self.parent.comboBox_Pathologie.setVisible(True)
#             index=self.parent.comboBox_Pathologie.model().GetIndex(self.MyConsultation.Pathologies.GetUniquePathologie())
#             if index==-1:
#                 MyError(self.parent,u'Pathologie non trouvée dans la liste')
#                 self.parent.comboBox_Pathologie.setCurrentIndex(0)
#             else:
#                 self.parent.comboBox_Pathologie.setCurrentIndex(index)
#         else:
#             self.parent.comboBox_Pathologie.setVisible(False)
#             self.parent.label_Pathologie.setText(QtCore.QString(u'                                       Pathologies multiples  >>>'))
#             self.parent.label_Pathologie.setMaximumWidth(341)
        MyDomaine=self.MyConsultation.GetDomaine()
        if not MyDomaine.isEmpty():
            self.parent.comboBox_PathologieDomaine.setCurrentIndex(self.parent.comboBox_PathologieDomaine.findText(MyDomaine))
        else:
            self.parent.comboBox_PathologieDomaine.setCurrentIndex(0)
        self.parent.splitter.resize(1021,470)

    def OnNewConsultation(self):
        self.parent.pushButton_valider.setEnabled(True)
        idConsultation=self.MyConsultation.SetConsultation(0)
        if idConsultation>0:
            if QtGui.QMessageBox.question(self.parent,'OpenVet',u'Une consultation existe déjà pour aujourd\'hui. Voulez-vous vraiment en créer une nouvelle?',QtGui.QMessageBox.Yes| QtGui.QMessageBox.Default,QtGui.QMessageBox.No)==QtGui.QMessageBox.No:
                self.MyConsultation.SetConsultation(idConsultation)
                self.FillFormConsultation()
                return
        self.mapper.toFirst()
        self.parent.toolButton_comment.setToolTip(QtCore.QString('Ajouter un Commentaire'))
        self.parent.label_Pathologies.setText("")
#         self.parent.label_Pathologie.setMaximumWidth(81)
#         self.parent.label_Pathologie.setText(QtCore.QString(u'Pathologie'))
#         self.parent.comboBox_Pathologie.setVisible(True)
        self.parent.comboBox_PathologieDomaine.setCurrentIndex(0)
        self.parent.splitter.resize(1021,470) 
        
    def OnTypeConsultation(self):
        if not self.parent.comboBox_consultType.GetProperty(1).isNull():
            self.parent.label_Referant.setVisible(True)
            self.parent.comboBox_Referant.setVisible(True)
        else:
            self.parent.label_Referant.setVisible(False)
            self.parent.comboBox_Referant.setVisible(False)
            
    def OnEditTypeConsultation(self):
        idTable=self.parent.comboBox_consultType.Getid()
        data=[[u'Libélé',1,45,1],[u'Remarque',1,120,2],[u'Choix par défaut',2],[u'Référé',2]]
        form=FormTypeConsultation(idTable,data,self.parent)
        if form.exec_():
            self.parent.comboBox_consultType.setModel(MyComboModel(self.parent,'GetTypesConsultation'))
        
    def OnDomaine(self):
        self.parent.comboBox_Pathologie.setModel(MyComboModel(self.parent,'SelectPathologies(%i,%i)'%(self.idEspece, self.parent.comboBox_PathologieDomaine.Getid())))
        
    def OnPathologieEnter(self):
        self.parent.label_Pathologies.setText("<font color=\"blue\">%s</font>"%self.MyConsultation.Pathologies.Add(self.parent.comboBox_Pathologie.Getid()))

    def EditDomaine(self):
        idDomaine=self.parent.comboBox_PathologieDomaine.Getid()
        new=[0,'',None,True,False,'']
        DomaineModel=MyModel('PathologieDomaine',idDomaine,self.parent)
        if not DomaineModel.SetNew(new):
            return  
        data=[[u'Discipline médicale',1,60],[u'Remarque',3,200,80]]
        form=MyForm('Disciplines médicales',data,self.parent)
        form.SetModel(DomaineModel,{0:1,1:2})    #GUI_field : DB_Field
        form.exec_()
        self.parent.comboBox_PathologieDomaine.setModel(MyComboModel(self.parent,'GetDomaines',u'Tous'))
        self.parent.comboBox_PathologieDomaine.Setid(idDomaine)

    def EditPathologie(self):
        new=[0,'',False,'',True,False,'']
        idPathologie=self.parent.comboBox_Pathologie.Getid()
        model=MyModel('Pathologie',idPathologie,self.parent)
        if not model.SetNew(new):
            return
        data=[[u'Nom de Référence',1,60],[u'Chronique',2],[u'Descriptif',3,65535,81],[u'Domaines',4],['',5,0,64],[u'Synonymes',5,0,64],[u'Documents',5,0,64],[u'Remarque',1,200]]
        form=FormPathologie(idPathologie,data,self.parent)
        form.SetModel(model,{0:1,1:2,2:3}) #{widget:field_model} 5:6
        if form.exec_():
            self.OnDomaine()
    
    def EditCriteresConsultation(self):
        self.SaveConsultation()
        data=[[u'Pathologie',4],[u'Modèles d\'examen',4,None,None,u'Edite les modèles d\'examen'],[u'Examen',4,None,None,u'Edite les examens complémentaires'],
              [u'Critère',4,None,None,u'Edite les critères pathologiques'],[u'',6,None,None,None,2],[u'Remarque',1,200]]
        form=FormConsultationCriteres(self.idConsultation,data,self.parent)
        form.exec_()

    def OnConsultantEnter(self):#TODO: OnEditConsultant
        print'Ouvre formulaire veto'
        
#     def UpdateConsultation_mdl(self):
#         #attributes: idConsultation,Animal_idAnimal,DateConsultation,TypeConsultation_idTypeConsultation,Personne_idConsultant,Personne_idReferant,
#         #Personne_idReferent,Examen,Traitement,Actif,Commentaires
#         self.MyConsult.idConsultation=self.idConsultation
#         self.MyConsult.DateConsultation=self.parent.dateEdit_consult.date()      
#         self.MyConsult.Personne_idConsultant=self.parent.comboBox_veterinaire.GetData()
#         self.MyConsult.Consultant=self.parent.comboBox_veterinaire.currentText()
#         self.MyConsult.TypeConsultation_idTypeConsultation=self.parent.comboBox_consultType.GetData()
#         self.MyConsult.TypeConsultation=self.parent.comboBox_consultType.currentText()
#         if self.parent.comboBox_Referant.isVisible():
#             self.MyConsult.Personne_idReferant=self.parent.comboBox_Referant.GetData()
#             self.MyConsult.Referant=self.parent.comboBox_Referant.currentText()
#         else:
#             self.MyConsult.Personne_idReferant=None
#         self.MyConsult.Examen=self.parent.textEdit_consultObs.toPlainText()
#         self.MyConsult.Traitement=self.parent.textEdit_consultTrait.toPlainText()
#         self.MyConsult.Animal_idAnimal=self.idAnimal
#         if self.parent.comboBox_Pathologie.isVisible():
#             idpathologie=self.parent.comboBox_Pathologie.GetData()
#             if idpathologie>0:
#                 if not self.MyConsult.CheckDoublonPathologieRef(idpathologie):
#                     tmp=Core_Critere.CriteresConsultation(idpathologie,self)
#                     self.MyConsult.ConsultationPathologies.append(tmp)
            
    def SaveConsultation(self):
        #TODO : if MyConsultation.isValid
        self.mapper.submit()
        if self.MyConsultation.Save(self.parent.comboBox_consultType.GetProperty(1),self.mapper.currentIndex()):
            QToolTip.showText(QCursor.pos(),u'Sauvegarde réussie.')
            self.parent.pushButton_valider.setEnabled(False)
            self.GetConsultations()
            self.idConsultation=self.MyConsultation.idConsultation     
#        self.NewConsultation=True
             
    def EditCommentaire(self):
        dlg =QInputDialog(self.parent)                 
        dlg.setInputMode( QtGui.QInputDialog.TextInput)
        dlg.setWindowTitle(u'Commentaire de consultation') 
        dlg.setLabelText("Commentaire:")
        dlg.setTextValue(self.MyConsultation.GetComment())                  
        dlg.resize(700,100)                             
        if dlg.exec_():
            value=dlg.textValue()
            if value.size()>200:
                value.chop(value.size()-200)
                MyError(self.parent,u'Attention le commentaire a été tronqué à 200 caractères: \"%s\"'%value)
            self.MyConsultation.SetComment(value)
            self.parent.toolButton_comment.setToolTip(Core.Multiline(value)) 
      
            
# class FormComment(QtGui.QDialog):   #TODO: Génériquer (title,label,maxsize) MyDialog
#     def __init__(self,parent=None):
#         super(FormComment,self).__init__(parent)
#         self.resize(400, 255)
#         self.setWindowTitle("Edition Consultation")
#         self.buttonBox = QtGui.QDialogButtonBox(self)
#         self.buttonBox.setGeometry(QtCore.QRect(30, 210, 341, 32))
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
#         self.label = QtGui.QLabel(self)
#         self.label.setGeometry(QtCore.QRect(20, 20, 191, 17))
#         self.label.setText("Entrez votre commentaire :")
#         self.plainTextEdit = QtGui.QPlainTextEdit(self)
#         self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 361, 141))
#         self.plainTextEdit.setMaxLength(200)
#         self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
#         self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GuiConsultation()
    window.show()
    window.OnSelectAnimal()
    sys.exit(app.exec_())
