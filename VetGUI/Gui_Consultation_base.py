#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('../VetCore')

from PyQt4 import QtCore, QtGui
import PyQt4.Qt as qt
#from PySide import QtCore, QtGui
from ui_Form_consultation import Ui_MainWindow
from ui_Form_client import Ui_Dialog_client
from ui_Form_animal import Ui_Dialog_animal

import Core_Consultation
from ui_Form_consultation_base import Ui_MainWindowConsultation

from gestion_erreurs import * 

#AFFICHE_CONSOLE=config.DEBUG_AFFICHE_MESSAGE_CONSOLE

class WindowsTest(QtGui.QMainWindow):

    def __init__(self):
        super(WindowsTest, self).__init__()

        self.initUI()

    def initUI(self):
        w= WindowConsultation()
        self.setCentralWidget(w)
        self.setGeometry(100, 100, 1200  , 1200)
        self.show()


class WindowConsultation(QtGui.QMainWindow, Ui_MainWindowConsultation):
    """WindowConsultation represente l'onglet consultation avec 1 client actif, 
    la liste de ses animaux et la liste de ses consultations (=instance de Core_Consultation.Consultation)"""

    NewConsultation=True #TODO: a revoir (utilité?)
    

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.MyConsult=Core_Consultation.Consultation()

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
        #hide some widgetException _mysql_exceptions.OperationalError: (2013, 'Lost connection to MySQL server during query') in <bound method Cursor.__del__ of <MySQLdb.cursors.Cursor object at 0x938a2ec>> ignored

        self.tableWidget_analyses.setVisible(False)
        self.listWidget_analyse.setVisible(False)
        self.lineEdit_titreImage.setVisible(False)
        self.lineEdit_fichier.setVisible(False)
        self.pushButton_addImage.setVisible(False)
        self.toolButton_fichier.setVisible(False)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)
        #fill comboboxes
        self.comboBox_veterinaire.addItems(self.MyConsult.GetConsultants())
        self.comboBox_consultType.addItems(self.MyConsult.GetTypesConsultation())
        self.comboBox_Referant.addItems(self.MyConsult.GetReferants())
        #connect actions
        self.toolButton_addClient.clicked.connect(self.DoClientEdit)
        self.toolButton_addAnimal.clicked.connect(self.DoAnimWindowConsultationalEdit)
        self.comboBox_Animal.activated.connect(self.DoGetConsultations)
        self.comboBox_consultType.currentIndexChanged.connect(self.OnTypeConsultation)
        self.connect(self.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationClicked)
        self.toolButton_comment.clicked.connect(self.DoEditCommentaire)
        self.pushButton_valider.clicked.connect(self.DoEditConsultation)
        self.pushButton_Nouveau.clicked.connect(self.OnNewConsultation)
        self.actionQuitter.triggered.connect(self.Mycloseapp)
        self.comboBox_client.currentIndexChanged.connect(self.OnClientChanged)
        self.comboBox_Animal.currentIndexChanged.connect(self.OnAnimalChanged)

        self.desactiveSignalClientChanged=False
        
        

    def ActiveClientId(self, id,  actualiseListeClient=True):
        "active le client 'id', recrée le comboBox_client (sauf si signalclientchanged) et actualise comboBox_Animal et consultations"

        err=self.MyConsult.ActiveClientId(id)
        #TODO:   titre onglet = nom client
        if err : 
            AfficheErreur('Le client '+str(id)+' n\'existe pas',  fenetre=self)
            return err

        if actualiseListeClient :#recrée la liste client et positionne au bon id
            self.desactiveSignalClientChanged=True
            self.comboBox_client.clear()
            self.comboBox_client.addItems(self.MyConsult.GetListeClients())
            self.comboBox_client.setCurrentIndex(self.MyConsult.GetIndexClientId(id))
            self.desactiveSignalClientChanged=False

        self.ActualiseListeAnimaux()

#        print 'debug : apres actualisation liste animaux de id='+str(id)
#        print self.PrintClientsConsultationActifs()
#        
#        
        try : # active 1er animal
            id1eranimal=self.MyConsult.idAnimaux[0]
            self.MyConsult.ActiveAnimalId(id1eranimal)
            self.DoGetConsultations()
        except : 
            pass
#        print 'debug : apres activation 1er animal de id='+str(id)
#        print self.PrintConsultation()
#        print 'actifs='
#        print self.PrintClientsConsultationActifs()




    def ActualiseListeAnimaux(self):
        self.comboBox_Animal.clear()
        self.comboBox_Animal.addItems(self.MyConsult.GetListeAnimaux())
        
    def ActualiseListeConsultations(self, idconsultation=None, actualiseListeId=False):
        "relecture dans la DB des consultations de l'animal actif (ou d'une consultation si idconsultation)"
        self.MyConsult.RafraichissementListeConsultations(idconsultation, actualiseListeId)
        self.DoGetConsultations() #rafraichissement de l'affichage

    def PrintClientsConsultationActifs(self, etiquettes=False, imprimechampvide=False, nbTab=0):
        return self.MyConsult.PrintClientsConsultationActifs(etiquettes, imprimechampvide, nbTab)

    def PrintConsultation(self, etiquettes=False, imprimechampvide=False, nbTab=0):
        return self.MyConsult.PrintConsultation(etiquettes, imprimechampvide, nbTab)

    def  DoAnimWindowConsultationalEdit(self):
        pass

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


    def GetNomClientActif(self):
        txt= self.MyConsult.GetNomClientActif()  or '--- nouveau client ---'
        return txt
        


    def DoGetConsultations(self):

        self.textBrowser_consultations.setText(self.MyConsult.GetConsultationsHTML())
        self.splitter.resize(1021,820)

    def OnConsultationClicked(self,link):
        self.NewConsultation=False
        idConsultation=int(link.toString().toAscii()[2:]) 
        self.MyConsult.ActiveConsultationId(idConsultation)
        if link.toString().toAscii()[1]=='C':
            self.FillFormConsultation()
        if link.toString().toAscii()[1]=='N':
            self.DoNewConsultation()   
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
        consultationActive=self.MyConsult.GetConsultationActive()
        if not consultationActive : return

        date=self.MyConsult.GetDateConsultation()
        self.dateEdit_consult.setDate(QtCore.QDate(QtCore.QDate(int(date[6:]),int(date[3:5]),int(date[:2]))))
        self.comboBox_veterinaire.setCurrentIndex(self.comboBox_veterinaire.findText(QtCore.QString(consultationActive.Get('Consultant'))))
        self.comboBox_consultType.setCurrentIndex(self.comboBox_consultType.findText(QtCore.QString(consultationActive.Get('TypeConsultation') )))
        referant=consultationActive.Get('Referant')
        if referant :
            self.comboBox_Referant.setCurrentIndex(self.comboBox_Referant.findText(QtCore.QString(referant)))
        self.textEdit_consultObs.setText(QtCore.QString(consultationActive.Get('Examen')))
        self.textEdit_consultTrait.setText(QtCore.QString(consultationActive.Get('Traitement')))
        commentaires=consultationActive.Get('Commentaires')
        if commentaires :
            self.toolButton_comment.setToolTip(QtCore.QString(commentaires))
        self.splitter.resize(1021,470)

    def OnTypeConsultation(self):
        if self.comboBox_consultType.currentText()==QtCore.QString("Référée".decode('utf8')):
            self.label_Referant.setVisible(True)
            self.comboBox_Referant.setVisible(True)
        else:
            self.label_Referant.setVisible(False)
            self.comboBox_Referant.setVisible(False)

    def OnClientChanged(self):#comboBox_client changé => on active le client correspondant au client selectionné
        if self.desactiveSignalClientChanged : return   # bloque signal lorsque comboBox_client récréé (rafraichissement)
        index=self.comboBox_client.currentIndex()
        if index>=0 :
            idclient=self.MyConsult.idClients[index]
            #if idclient <> self.MyConsult.GetIdClientActif():#ne change pas si le client est déjà activé #TODO: a faire
            self.ActiveClientId(idclient, actualiseListeClient=False)


    def OnAnimalChanged(self):
        index=self.comboBox_Animal.currentIndex()
        if index>=0 :
            idanimal=self.MyConsult.idAnimaux[index]
            self.MyConsult.ActiveAnimalId(idanimal)


    def DoEditConsultation(self):

        erreur=''
        
        # 1) lecture des infos
        consultationActive=self.MyConsult.GetConsultationActive()
        q=self.dateEdit_consult.date()
        date='%04i-%02i-%02i'%(q.year(), q.month(), q.day())
        
        indexConsultant=self.comboBox_veterinaire.currentIndex()
        
        if indexConsultant>=0:
            idConsultant=self.MyConsult.GetIdConsultant(indexConsultant)
        else :
            idConsultant=None
            erreur+='Warning : pas de consultant '

        indexTypeConsultation=self.comboBox_consultType.currentIndex()
        if indexTypeConsultation >=0:
            idTypeConsultation=self.MyConsult.GetIdTypeConsultation(indexTypeConsultation)  
        else :
            idTypeConsultation=None
            erreur+='Warning : pas de type consultation '

        idReferant=None
        if self.comboBox_Referant.isVisible():
            indexReferant=self.comboBox_Referant.currentIndex()
            if indexReferant >=0:
                idReferant= self.MyConsult.GetIdReferant(indexReferant) 
            

        Observations=self.textEdit_consultObs.toPlainText().toUtf8()
#        Observations=str(Observations).decode('utf8') #TODO: revoir erreur encodage (eventuellemnt au niveau table setchamp)
        Traitements=self.textEdit_consultTrait.toPlainText() #.toUtf8()
#        Traitements=str(Traitements).decode('utf8')
        
        idAnimal=self.MyConsult.GetAnimalActif().Id()
        
        if not consultationActive :
            consultationActive = self.MyConsult.NouvelleConsultation()  #rem: impossible à activer car n'a pas encore d'id
            nouvelleconsultation=True
        else :
            nouvelleconsultation=False
        
        # 2) enregistre dans la base de donnée
        erreur+=consultationActive.SetChamps(enregistre_auto=True, DateConsultation=date,Animal_idAnimal=idAnimal, TypeConsultation_idTypeConsultation=idTypeConsultation, \
                Personne_idConsultant=idConsultant, Personne_idReferant=idReferant, Examen=Observations, Traitement=Traitements) #enregistre dans la base la consultation

        # 3) actualise affichage
        if nouvelleconsultation :
            self.ActualiseListeConsultations(idconsultation=consultationActive.Id(), actualiseListeId=True) #rafraichissement 
            self.MyConsult.ActiveConsultationId( consultationActive.Id()  )
        else :
            self.ActualiseListeConsultations(idconsultation=consultationActive.Id()) #rafraichissement simple (relecture de consultation dans database sans recréer la liste des consultations
        
        if erreur :
            AfficheErreur('erreur Gui_Consultation_base.py:DoEditConsultation   '+erreur)
            
        self.NewConsultation=True

    def DoEditCommentaire(self):
        print 'afaire' #TODO:
        return 
        form=FormComment()
        form.plainTextEdit.insertPlainText(self.MyConsult.Commentaire)
        if form.exec_():
            self.MyConsult.Commentaire=form.plainTextEdit.toPlainText().toUtf8()
            self.toolButton_comment.setToolTip(QtCore.QString(self.MyConsult.Commentaire.data().decode('utf8')))

    def OnNewConsultation(self):
        print 'afaire' #TODO:
        
        self.MyConsult.DesactiveConsultation()
       
        self.NewConsultation=True
        self.dateEdit_consult.setDate(QtCore.QDate.currentDate())
        self.comboBox_veterinaire.setCurrentIndex(0)
        self.comboBox_consultType.setCurrentIndex(0)
        self.comboBox_Referant.setCurrentIndex(0)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)
        self.textEdit_consultObs.clear()
        self.textEdit_consultTrait.clear()
        self.toolButton_comment.setToolTip(QtCore.QString('Ajouter un Commentaire'))
        self.splitter.resize(1021,470) 

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
    window = WindowsTest()
    window.show()
    sys.exit(app.exec_())
