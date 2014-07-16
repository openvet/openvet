#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('../VetCore')
sys.path.append('..')

from PyQt4 import QtCore, QtGui
#import PyQt4.Qt as qt
from PyQt4.Qt import *

import config

from ui_Form_consultation_base import Ui_MainWindowConsultation
#from ui_Form_animal import Ui_Dialog_animal
#from ui_Form_DialogBase import Ui_DialogBase


from Gui_FormClient import *
from Gui_FormAnimal import *

from Mywidgets import *

from Core_Consultation import *
from gestion_erreurs import * 

from multiprocessing import Process, Queue
        


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
    Formulaire_Client=None

    def __init__(self, parent=None, formulaireclient=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.mainwindows=parent
        
        self.MyConsult=Consultation()
        
        #self.ThreadPrepareFormulaireClient() #en tache de fond  marche pas pb creation Qwidget dans thread =pb connect signal
        
        self.__class__.Formulaire_Client=  formulaireclient or FormClient()
        
        self.formulaireEditClient = None
        
        self.__class__.Formulaire_Animal=None
        self.formulaireEditAnimal = None
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
        
        
#        self.label_Referant.setVisible(False)
#        self.comboBox_Referant.setVisible(False)
        
        self.frame_edit_consult.setVisible(False)
        
        #fill comboboxes
        self.comboBox_veterinaire.addItems(self.MyConsult.GetConsultants())
        self.comboBox_consultType.addItems(self.MyConsult.GetTypesConsultation())
        self.comboBox_Referant.addItems(self.MyConsult.GetReferants())
        #connect actions
        self.toolButton_editClient.clicked.connect(self.DoClientEdit)
        self.toolButton_addClient.clicked.connect(self.DoNouveauClient)
        self.toolButton_ClientInfo.clicked.connect(self.DoClientInfo)
        self.toolButton_addAnimal.clicked.connect(self.DoAnimWindowConsultationalEdit)
        self.toolButton_editAnimal.clicked.connect(self.DoAnimalEdit)
        
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
        
        if config.MASQUE_WIDGET_NON_DEV :
            self.DesactiveLesWidgetsNonImplementes()
        
    def DesactiveLesWidgetsNonImplementes(self):
        tab=self.tabWidget_medical
        
        tab.setCurrentWidget(self.tab_consulation)
        
        self.frame_vaccin.setVisible(False)
        
        index_analyses= tab.indexOf(self.tab_analyses)
        tab.removeTab(index_analyses)
        
        index_ordonnances = tab.indexOf(self.tab_ordonnances)
        tab.removeTab(index_ordonnances )
        
        index_vaccins  = tab.indexOf( self.tab_vaccins )
        tab.setTabEnabled(index_vaccins  , False)
        
        
        index_planTherapeutique = tab.indexOf(self.tab_planTherapeutique)
        tab.removeTab(index_planTherapeutique )
        
        index_documents = tab.indexOf(self.tab_documents)
        tab.removeTab(index_documents )
        
        
        
    def ThreadPrepareFormulaireClient(self): #TODO: supprimer, ne marche pas
        objet=UnFormulaireClient(self)
        self.objet=objet
        t=QThread()
        self.threadclient=t
        objet.moveToThread(t)
        objet.connect(t, QtCore.SIGNAL("started()"),   objet.creationform)
    
        t.start()
        
        print objet.form
        
    def ThreadPrepareFormulaireClient_old(self): #TODO: supprimer, ne marche pas
        if self.__class__.Formulaire_Client :
            self.formulaireEditClient =self.__class__.Formulaire_Client #recupere le formulaire global (= le meme pour tous les WindowConsultation)
            
        else :
            queue=Queue()  #pour récupérer le formulaire crée dans le sous processus
            self.queueformulaireclient=queue
            
            p = Process(target=self.ThreadCreeFormulaireClient, args=(queue,))
            p.start() #lance en tache de fond le processus de création de formClient
        
    def ThreadCreeFormulaireClient(self, queue): #TODO: supprimer, ne marche pas
        #crée un formulaire client en tache de fond et le place dans queue

        editClient = FormClient(self)  #marche pas
        queue.put(editClient)
#        queue.put(  "test" )
    def ActualiseListeClients(self, id=None):#recrée la liste client et positionne au bon id  
    
            if not id :
                id=self.MyConsult.GetIdClientActif()
    
            self.desactiveSignalClientChanged=True
            self.comboBox_client.clear()
            self.comboBox_client.addItems(self.MyConsult.GetListeClients())
            self.comboBox_client.setCurrentIndex(self.MyConsult.GetIndexClientId(id))
            self.desactiveSignalClientChanged=False
    
    def ActualiseListeClientsDeTousLesOngletsConsultation(self):
        
        if self.mainwindows :
            self.mainwindows.ActualiseListeClientsDeTousLesOngletsConsultation()
            
    
    def ActiveClientId(self, id,  actualiseListeClient=True):
        "active le client 'id', recrée le comboBox_client (sauf si signalclientchanged) et actualise comboBox_Animal et consultations"

        err=self.MyConsult.ActiveClientId(id)
        #TODO:   titre onglet = nom client
        if err : 
            AfficheErreur('Le client '+str(id)+' n\'existe pas',  fenetre=self)
            return err

        if actualiseListeClient :#recrée la liste client et positionne au bon id
            self.ActualiseListeClients(id)
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
            self.DoGetConsultations()  #efface la consultation (pas d'animal actif)
            
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
        
    def CreeFormClient(self):
        if not self.__class__.Formulaire_Client : #utilise le meme FormClient pour toutes les instances de classes
            self.__class__.Formulaire_Client = FormClient()
        self.formulaireEditClient = self.__class__.Formulaire_Client 
        
    def CreeFormAnimal(self):
        if not self.__class__.Formulaire_Animal : #utilise le meme Form Animal pour toutes les instances de classes
            self.__class__.Formulaire_Animal = FormAnimal()
        self.formulaireEditAnimal = self.__class__.Formulaire_Animal 
        

    def DoClientEdit(self):
        if not self.formulaireEditClient :  # self.formulaireEditClient   =  formulaire client  pour edition ou nouveau client/création  s'il n'existe pas 
            self.CreeFormClient()
            
        self.formulaireEditClient.SetClient(self.MyConsult.GetClientActif())
        if self.formulaireEditClient.exec_():
            print 'ok edition client' 
            self.ActualiseNomOnglet()  #si nom client change
            self.ActualiseListeClientsDeTousLesOngletsConsultation()
            
    def DoClientInfo(self):
        if not self.formulaireEditClient :  # self.formulaireEditClient   =  formulaire client  pour edition ou nouveau client/création  s'il n'existe pas 
            self.CreeFormClient()
            
        self.formulaireEditClient.SetClient(self.MyConsult.GetClientActif(), modeinfo=True)
        if self.formulaireEditClient.exec_():
            pass
            
    def DoNouveauClient(self):
        if not self.formulaireEditClient : #création du formulaire client s'il n'existe pas 
            self.CreeFormClient()
            
        nouveauclient=self.MyConsult.NouveauClient()
        self.formulaireEditClient.SetClient(nouveauclient)
        if self.formulaireEditClient.exec_():
            print 'ok nouveau client' #self.formulaireEditClient.data
            idclient=self.formulaireEditClient.idnouveauclient
            if idclient :
                self.ActiveClientId(idclient)  #TODO: important : ajouter idclient  à la liste de tous les clients (gui_openvet)
                self.ActualiseNomOnglet()  #si nom client change
                self.ActualiseListeClientsDeTousLesOngletsConsultation()
                

    def DoAnimalEdit(self):
#        self.dataAnimal='Son nom est minou'
        if not self.formulaireEditAnimal :
            self.CreeFormAnimal()
            
        self.formulaireEditAnimal.SetTable(self.MyConsult.GetAnimalActif())
        if self.formulaireEditAnimal.exec_():
            pass #TODO:
            


    def GetNomClientActif(self):
        txt= self.MyConsult.GetNomClientActif()  or '--- nouveau client ---'
        return txt
        


    def DoGetConsultations(self):

        self.textBrowser_consultations.setText(self.MyConsult.GetConsultationsHTML())
#        self.splitter.resize(1021,820)

    def OnConsultationClicked(self,link):
        self.frame_edit_consult.setVisible(True)
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
#        self.splitter.resize(1021,470)

    def OnTypeConsultation(self):
        if self.comboBox_consultType.currentText()==QtCore.QString("Référée".decode('utf8')):
            self.label_Referant.setEnabled(True)
            self.comboBox_Referant.setEnabled(True)
#            self.label_Referant.setVisible(True)
#            self.comboBox_Referant.setVisible(True)
        else:
            self.label_Referant.setEnabled(False)
            self.comboBox_Referant.setEnabled(False)
            
#            self.label_Referant.setVisible(False)
#            self.comboBox_Referant.setVisible(False)

    def OnClientChanged(self):#comboBox_client changé => on active le client correspondant au client selectionné
        if self.desactiveSignalClientChanged : return   # bloque signal lorsque comboBox_client récréé (rafraichissement)
        index=self.comboBox_client.currentIndex()
        if index>=0 :
            idclient=self.MyConsult.idClients[index]
            #if idclient <> self.MyConsult.GetIdClientActif():#ne change pas si le client est déjà activé #TODO: a faire
            self.ActiveClientId(idclient, actualiseListeClient=False)
            self.ActualiseNomOnglet()

    def ActualiseNomOnglet(self, text=None):
        try :
            stacked_widget=self.parent() # liste des widgets (fenetres consultation) affiché dans onglets
            tab_widget=stacked_widget.parent() #tabwidget qui gere les onglets consultation
            indexpage=stacked_widget.currentIndex() #onglet en cours
            
            if not text :
                text=self.MyConsult.GetNomClientActif()
            
            tab_widget.setTabText (indexpage, text)
        except:
            print 'erreur Gui_Consultation_base.ActualiseNomOnglet()'

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
#        if self.comboBox_Referant.isVisible():
        if self.comboBox_Referant.isEnabled():
            indexReferant=self.comboBox_Referant.currentIndex()
            if indexReferant >=0:
                idReferant= self.MyConsult.GetIdReferant(indexReferant) 
            

        Observations=self.textEdit_consultObs.toPlainText().toUtf8()  #TODO:  +++++++++ ESSAYER SANS toUtf8++++
        Traitements=self.textEdit_consultTrait.toPlainText() #.toUtf8()

        
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
        
#        self.label_Referant.setVisible(False)
#        self.comboBox_Referant.setVisible(False)
        
        
        self.textEdit_consultObs.clear()
        self.textEdit_consultTrait.clear()
        self.toolButton_comment.setToolTip(QtCore.QString('Ajouter un Commentaire'))
#        self.splitter.resize(1021,470) 

    def Mycloseapp(self):
        self.close()


#class FormClient(QtGui.QDialog, Ui_Dialog_client):
#    def __init__(self, parent=None):
#        QtGui.QDialog.__init__(self, parent)
#        print parent.dataClient
#        self.setupUi(self)
#        self.data=parent.dataClient+' rien'
        

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    window = WindowsTest()
    window.show()
    sys.exit(app.exec_())
