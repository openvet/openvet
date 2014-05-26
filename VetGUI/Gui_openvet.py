#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
#sys.path.append('../VetCore')
#sys.path.append('../VetGUI')
#sys.path.append('../images')


sys.path.append('./VetCore')
sys.path.append('./VetGUI')
sys.path.append('./images')


from PyQt4 import QtCore, QtGui
import PyQt4.Qt as qt
#
#from ui_Form_client import Ui_Dialog_client
#from ui_Form_animal import Ui_Dialog_animal

from ui_Form_openvet import  Ui_MainWindow
from ui_Form_consultation_base import Ui_MainWindowConsultation
#from ui_Form_consultation import Ui_MainWindowConsultation

from ui_Form_DialogOuvreClient import  Ui_Dialog_OuvreClient

from Gui_Consultation_base import WindowConsultation
import Core_Consultation

from gestion_erreurs import * 

                                   
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.editClient = None
        self.editAnimal = None
        self.DialOuvrir  = None

        self.connect(self.tabWidgetClient, QtCore.SIGNAL("tabCloseRequested(int)"), self.CloseClient)
        self.connect(self.tabWidgetClient, QtCore.SIGNAL("currentChanged(int)"), self.TabChanged)
        
        self.actionQuitter.triggered.connect(self.Mycloseapp)
        
        self.UneConsult=Core_Consultation.Consultation()
        self.InitialiseListeClient()
        
        
        
        
    def InitialiseListeClient(self): 
        if not self.DialOuvrir : #prepare Dialogue Ouvrir Client
            self.DialOuvrir= FormOuvreClient(self)
            listeclient=self.UneConsult.GetClients() #TODO: barre de progression 
            self.DialOuvrir.comboBox_ListeClient.addItems(listeclient)
            
        index_ongletAjouter=0
        tb=self.tabWidgetClient.tabBar()
        tb.setTabButton(index_ongletAjouter, QtGui.QTabBar.RightSide, None) #enleve boutton close de l'onglet ajouter

        idclient=self.DialogueIdClient()
        
        while (not idclient) :
            AfficheErreur('SELECTIONNER UN CLIENT',  fenetre=self)
            idclient=self.DialogueIdClient()
        self.InsertClient(id=idclient)
        
            
    def DialogueIdClient(self):
        idclient=None
        if self.DialOuvrir.exec_():
            index=self.DialOuvrir.comboBox_ListeClient.currentIndex()
            idclient=self.UneConsult.idListeClients[index]
        return idclient
        

    def TabChanged(self, index):
        #print str(index)
        nbPage=self.tabWidgetClient.count()
        if index == nbPage -1 : #  onglet 'ajouter :
            self.InsertClient(index)
            
#                page=WindowConsultation()
#                self.tabWidgetClient.insertTab(index, page, 'Nouveau client')
#                self.tabWidgetClient.setCurrentIndex(index)




                    

    def InsertClient(self, index=0, id=None):
                
#                i, ok = QtGui.QInputDialog.getInteger(self,'id client', 'id client')
                
                idclient = id or self.DialogueIdClient()
                
#                if ok :
                if idclient:
                    page=WindowConsultation()
                    err = page.ActiveClientId(idclient)
                    nomclient=page.GetNomClientActif()
                    self.tabWidgetClient.insertTab(index, page, nomclient)
                    self.tabWidgetClient.setCurrentIndex(index)
                    pagecourante=self.tabWidgetClient.currentWidget()
                    
#                if index == 0 :  #au debut du programme enleve boutton close de l'onglet ajouter
#                    index_ongletAjouter=self.tabWidgetClient.count()-1  
#                    tb=self.tabWidgetClient.tabBar()
#                    tb.setTabButton(index_ongletAjouter, QtGui.QTabBar.RightSide, None) #enleve boutton close de l'onglet ajouter
#                    


    def CloseClient( self, index):
        
        nbPage=self.tabWidgetClient.count()
        #print ' debug fermeture'+str(index)+'/'+str(nbPage)
        if index == nbPage -1 : #  onglet 'ajouter 
            pass #empeche la fermeture de l'onglet ajouter
        else :
            self.tabWidgetClient.setCurrentIndex(0) #pour empecher emission signal TabChanged et recreation de la tabWidgetClient qui vient d etre detruite (=si juste avant onglet ajoute)
            self.tabWidgetClient.removeTab(index)
            #TODO: a faire detruire page
        
        
    def Mycloseapp(self):
        self.close()
##
#

class FormOuvreClient(QtGui.QDialog, Ui_Dialog_OuvreClient):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)




if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
