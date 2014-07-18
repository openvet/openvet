#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('../VetCore')
sys.path.append('..')

from PyQt4 import QtCore, QtGui
#import PyQt4.Qt as qt
from PyQt4.Qt import *

import config

from ui_Form_DialogBase import Ui_DialogBase
from Mywidgets import *

from Core_Consultation import *
from gestion_erreurs import * 


        
class FormulaireBase(QtGui.QDialog, Ui_DialogBase):
    """ 
    Formulaire qui affiche les champs d'une table de la base de donnée
    
    ListeChampAffiches = nom des champs (= identique au nom de la base de donnée), possibilité de regrouper dans des sous listes
    NomChamp = nom affiché (à la place du nom dans la DB)
    TypeChamp (ex comboBox, checkBox...)

    """
    
    
    def __init__(self, parent=None, unetable=None, version=''):
        
        self.version= version 
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
      
        self.une_table = unetable
        
        self.dicoWidget={} # dicoWidget['nomchamp'] = widget associé
        self.dicoWidgetIndependant={}  #idem pour widgets non associés directement à un champ de la data base
        
        #        self.ListeChampIndependant=[]

        self.DesactiveSignaux=False
        self.derniereAction=''
        self.idnouvelletable=None

        
        #regroupement de widget : groupés dans ListeGroupeBox ou masqués ListeChampPersonnel = employés)
        self.ListeGroupeBox1= []    
        self.ListeGroupeBox2=  []
        self.widgetGroupebox=[]
        self.ListeChampPersonnel=[ ]  #champs non affichés par défaut
        #TODO: ajouter NomChamp pour ListeChampPersonnel
        
         #listes des champs de la table client qui seront affichés ( dans l'ordre, avec etiquette NomChamp et le widget de type TypeChamp, 
        self.ListeChampAffiches=[self.ListeGroupeBox1, self.ListeGroupeBox2]
        
        self.NomChamp={}
        
        self.TailleMax={}
    
        
        self.TypeChamp={ } #defaut=LineEdit
           
            
        #création unclient (objet de class TableClient intermédiaire entre affichage et database) :      widget <-> unclient <-> database

        self.modeinfo=False
            
        #self.DataBasedicoChamps=self.une_table.GetDicoChamps() #liste des champs de la Table (= noms des colonnes dans la Data Base)
        self.DataBasedicoChamps={} 
        if self.une_table :
            self.DataBasedicoChamps=self.une_table.GetDicoChamps()
            
        #création des wigets
        
#        self.AfficheChamps()  #A APPELER DANS LES CLASSES DERIVEES
        
        #initialise affichage (masque certains widget) et combo (création listes civilité villes)
        
        
        # signaux  (voir aussi ConnectSignalWidgetIndependant)
#        w=self.dicoWidget['IsVeterinaire']
#        self.connect(w, QtCore.SIGNAL("stateChanged(int)"),self.OnIsVeterinaireClicked)

        self.connect(self.pushButton_editer, QtCore.SIGNAL("clicked(bool)"),  self.OnButtonEditerClicked)
        
#        self.connect(self.pushButton_editer, QtCore.SIGNAL("clicked(bool)"),  self.OnButtonEditerClicked)

        

    def AfficheWidgetsEnfants(self, layout, affiche): #affiche ou masque tous les widgets d'un layout  
        listeenfants=layout.children()
        layout.setEnabled(affiche)
        for enfant in listeenfants : #1ere methode pour retrouver les widgets (ne fonctionne pas avec layout) #AREVOIR utilité ? pour autre type layout?
            try:
                enfant.setVisible(affiche)
            except:
                pass
        i=0
        item=layout.itemAt(i)  #2eme methode pour retrouver les widgets
        while (item) :
            try :
                item.widget().setVisible(affiche)
            except:
                pass
            i+=1
            item=layout.itemAt(i)
            
        
        
    def AfficheChamps(self):
        "fonction principale qui affiche tous les widgets du formulaire puis initialiseChamp  (copie valeurs dans widgets)"
        
        self.formLayout=self.formLayout1                                    #        self.formLayout.setSizeConstraint(QLayout.SetMaximumSize)
        nbchamp=0        
        nbchampaffiches=len( self.ListeChampAffiches )
        for c in self.ListeChampAffiches + self.ListeChampPersonnel:
            
            if 'spacer' in c :  # création d'un widget espace   "spacer:Taille" de l'espace
                size=int(c.split(':')[1])
                spacer=QSpacerItem(size, size)
                self.formLayout.addItem(spacer)
            
            elif 'list' in str(type(c)) : # => widgets regroupés sur la meme ligne, dans une hbox = liste groupe box
                hbox=QHBoxLayout(self)                                                   #hbox.setSizeConstraint(QLayout.SetMaximumSize)
                hbox.setSizeConstraint(QLayout.SetMinimumSize)
                gb=QGroupBox(self)
                gb.setFlat(True)   #masque le cadre                                                     #gb.setAlignment(Qt.AlignLeft) #a revoir ne marche pas
                gb.setMaximumWidth(200)
                self.widgetGroupebox.append(gb)
                
                
                for souschamp in c :  # étiquette+widget
                    nomchamp, widget=self.CreeWidget(souschamp) 
                    label=QLabel( nomchamp)                                                                                 # marchepas:                   label.setMaximumWidth(20)
                    hbox.addWidget(label)                                                                                   #     marchepas:               label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                    hbox.addWidget(widget)                                                                                  # marchepas:                   widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                gb.setLayout(hbox) #TODO: fixer la taille des widgets 
                self.formLayout.addRow( gb)
            else: # la plupart des widgets = une étiquette + widget associé au champ de la database
                nomchamp, widget=self.CreeWidget(c)
                self.formLayout.addRow(nomchamp, widget)


            nbchamp+=1
            
            #gestion des colonnes : 3 colonnes pour les widgets de ListeChampAffiches, la dernière colonne = widgets de ListeChampPersonnel
            if self.formLayout<>self.formLayout_personnel :  
                if nbchamp >= nbchampaffiches :
                    self.formLayout=self.formLayout_personnel #derniere colonne,concerne uniquement les employés de la clinique
                elif nbchamp==22 :
                    self.formLayout=self.formLayout2  #2eme colonne
                elif nbchamp ==44 :
                    self.formLayout=self.formLayout3
        
        
        self.InitialiseChamps()
        
    def InitialiseChamps(self):
        """
        recopie les valeurs des champs dans les widgets
        a faire dans classes dérivées"""
        pass


    def CreeWidget(self, champ):  
        """
        utilisé par AfficheChamps
        crée et retourne une étiquette de champ + widget d'édition (champ=nom du champ dans la DataBase)"""
        
        if 'WIDGET' in champ : #widget indépendant = non lié à la Data Base (ex spacer..., bouton de controle d'affichage)
            return (self.CreeWidgetIndependant(champ))
        try : 
            taille=self.TailleMax[champ]
        except :
            taille=0 #ne change pas taille max du widget
            
        unchamp=self.DataBasedicoChamps[champ] #unchamp =  objet de classe Champ, pointe directement sur le champ de l'objet unclient à éditer
        try :
            nomchamp=self.NomChamp[champ]
        except :
            nomchamp=unchamp.Nom()  #par defaut prend le meme nom  que dans la DataBase 
            self.NomChamp[champ]=nomchamp
        try :
            typechamp=self.TypeChamp[champ]  #pour les checkBox, comboBox...
        except :  #par defaut (le + fréquent) =LineEdit
            typechamp='LineEdit'
            self.TypeChamp[champ]='LineEdit'
        
        widget=self.CreeWidgetEdit(nomchamp, typechamp, taille)                                                                                 #        widget.setMaximumWidth(taille)
        self.dicoWidget[champ]=widget  # mémorise le widget associé au champ
        try :
            self.une_table.AssocieWidgetChamp(widget, champ) # mémorise le widget associé à l'objet champ
        except:
            pass
        
        
        return( [nomchamp, widget])

    def CreeWidgetEdit(self, nomchamp, typechamp, taille): 
       
        if typechamp=='LineEdit' :
#            unwidget=QLineEdit(self)
            unwidget=MyLineEdit(self)
            if not taille :
                taille=config.MAXWIDTHQLINEEDIT
        elif typechamp=='comboBox':
            unwidget=QComboBox(self)
        elif typechamp=='myComboBoxVille':
            unwidget=MyComboBoxVille(self)             
        elif typechamp=='checkBox':
            unwidget=QCheckBox(self)
        elif typechamp=='textEdit':
            unwidget=QTextEdit(self)
            if not taille :
                taille=config.MAXWIDTHQTXTEDIT
        elif typechamp=='spinBox':
            unwidget=QSpinBox(self)
        elif typechamp=='date' :
            unwidget=QDateEdit(self)
            unwidget.setDisplayFormat('dd/MM/yyyy')
            unwidget.setCalendarPopup(True)
            
        if taille  : #si taille=0 ne change pas la taille 
            unwidget.setMaximumWidth(taille)

        return unwidget
        
    def CreeWidgetIndependant(self, champ):
        """ 
        utilisé par CreeWidget
        widget non lié à un champ de la DB  ex checkbox pour permettre edition de la date
        """
        try :
            nomchamp=self.NomChamp[champ]
        except :
            nomchamp=''
            
        if 'checkbox' in champ :
            pass  #TODO:  chekbox ville preferees
            
        elif 'date' in champ: #pour tous les widgets date optionnel => désactivés au début
            nomchamp='Ajouter Date'
            widget=QCheckBox(self)
            
        elif 'Edit' in champ : #ex WIDGETEditCIP
            widget=QLineEdit(self)
            
            if champ=='WIDGETEditCIP':
#                widget.setInputMask(config.MASQUE_CIP)
                reg=QRegExp(config.MASQUE_CIP_REG)  # ex  MASQUE_CIP_REG='\d{2}\s{0,1}\d{5}'
                validator=QRegExpValidator(reg, self)
#                validator=QIntValidator(0, 99999, self) #pb accept espaces++
                widget.setValidator( validator)
                

        try : 
            taille=self.TailleMax[champ]
            widget.setMaximumWidth(taille)
        except :
            pass
            
        self.dicoWidgetIndependant[champ]=widget
        return([nomchamp, widget])
        
    def ConnectSignalWidgetIndependant(self ):
        pass 
                
        
    def AfficheTousLesChamps(self, unetable): 
        """non utilisé : affiche tous les champs d'une table de la base de donnée
        aucun formatage, utile lors développement
        """
        self.formLayout=self.formLayout1
        nbchamp=0
        for champ in unetable.GetListeChamps():
            nbchamp+=1
            nomchamp=champ.Nom()
            
            uneligne=QLineEdit(self)
            uneligne.setObjectName(nomchamp)
            self.formLayout.addRow(nomchamp, uneligne)

            self.ListeChampAffiches.append(nomchamp)
            self.TypeChamp[c]='LineEdit'
            self.dicoWidget[c]=uneligne

            if nbchamp==20 :
                self.formLayout=self.formLayout2
            if nbchamp ==40 :
                self.formLayout=self.formLayout3
                
        

        
        

            
    def BasculeModeEdition(self, bool_edit):
        if bool_edit :
            self.EnableWidget(True)
            self.edition=True
            self.pushButton_editer.setText('Annuler')  #si clique => repasse mode lecture (=> empèche enregistrement client des modifications)
            
        else :
            self.EnableWidget(False)
            self.edition=False
            self.pushButton_editer.setText('Editer')
            
        if self.modeinfo==True :
            self.pushButton_editer.setVisible(False)
        else :
            self.pushButton_editer.setVisible(True)

    def EnableWidget(self,  active):#selon mode edition ou nouveau 
        for widget in self.dicoWidget.values() + self.dicoWidgetIndependant.values() :
            widget.setEnabled(active)

    def OnButtonEditerClicked(self, checked):
        
        if self.pushButton_editer.text()=='Annuler':
            self.derniereAction='Annuler'
            
#            self.accept() #bouton ok => propose de sauvegarder ou réécrit (table2widget) #marche pas boucle sur 
            self.CopieTable2Widget() #réinitialise les champs
        else :
            self.derniereAction='Editer'
        
        self.BasculeModeEdition( not self.edition) #inverse mode edition

    def une_table(self): #a surcharger
        return self.une_table
        
    def id_une_table(self): #a surcharger
        if self.une_table  :
            return self.une_table.Id()

    def SetTable(self, unetable, modeinfo=False):
        if unetable :
            old_table= self.une_table
            self.une_table =unetable
            self.modeinfo=modeinfo
            self.DataBasedicoChamps=self.une_table .GetDicoChamps()  #actualise DataBasedicoChamps avec les champs du nouveau client
            old_table.TransfertWidget(self.une_table )
            self.CopieTable2Widget()
            self.isNouvelleTable=False
            self.BasculeModeEdition(False)

    def VerifieChamps(self, listedeschamps=None):
        "copie le formulaire (la valeur des widgets) dans unetable et retourne les erreurs"
        erreur=''
        for nomchamp in self.DataBasedicoChamps :
            champ=self.DataBasedicoChamps[nomchamp]
            err= champ.CopieWidget2Champ()
            if err :
                if 'ne peut pas etre NULL' in err : err=u' à renseigner !' #change le msg d'erreur
                erreur+=nomchamp+err +'\n'
        return erreur

#    def CopieTable2WidgetNEW(self, efface=False):         
    def CopieTable2Widget(self, efface=False): 
        for unchamp in self.DataBasedicoChamps.values():  
            unchamp.CopieChamp2Widget()
            
            
    

    def CopieTable2WidgetOld(self, efface=False): 
#    def CopieTable2Widget(self, efface=False): 
        self.DesactiveSignaux=True #empeche certains signaux (pas tous) par ex OnIsVeterinaireClicked (qui décoche isClient => indésirable ici)
        id=self.id_une_table
        if efface or not id : #efface tout
            self.EffaceChamps()
      
        else : #copie une_table dans widgets
            for nomchamp in self.dicoWidget.keys():  #dicoWidget[nomchamp]=widget associé
                typechamp= self.TypeChamp[nomchamp]
                if 'ComboBox' in typechamp or 'comboBox' in typechamp :
                    # +/- ajouter à une liste à traiter séparément
                    continue   #a faire dans chq classe dérivée 
                
                widget=self.dicoWidget[nomchamp]
                unchamp=self.DataBasedicoChamps[nomchamp]  #unchamp = objet champ du client
                if 'Edit' in typechamp :
                    txt=unchamp.Txt()
                    widget.setText(txt)
                elif typechamp == 'checkBox' :
                    if unchamp.isTrue():
                        widget.setCheckState(Qt.Checked)
                    else :
                        widget.setCheckState(Qt.Unchecked)

                elif typechamp ==  'spinBox' :
                    nb=unchamp.Value()
                    try :
                        widget.setValue(nb)
                    except:
                        widget.setValue(0)
                elif typechamp ==  'date' :
                    date=unchamp.GetDate('QDate')
                    if date :
                        widget.setDate(date)
                        self.DesativeChamp(nomchamp, active=True)
                    else : 
                        now=QDate.currentDate()
                        widget.setDate(now)
                        self.DesativeChamp(nomchamp)

            
        self.DesactiveSignaux=False
             

    def EffaceChamps(self):
        for nomchamp in self.dicoWidget.keys():
            widget=self.dicoWidget[nomchamp]
            try :
                widget.setText('')  #QLineEdit, ...
            except :
                try :
                    widget.setCheckState(Qt.Unchecked)  #checkBox
                except :
                    try :
                        widget.setValue(0)  #spinBox
                    except:
                        try :
                            now=QDate.currentDate()
                            widget.setDate(now)
                            nomchamp=''
                            for champ in self.dicoWidget.keys() : #retrouve le nom du champ date et DesativeChamp
                                if self.dicoWidget[champ] == widget :
                                    nomchamp=champ
                                    break
                            self.DesativeChamp(nomchamp) #widget de contrôle associé à la date
                            
                        except:
                            pass
                    
    def DesativeChamp(self, champ):
        pass
        
        
    def accept(self):
        save = self.edition #en mode edition enregistre le client
        
#        if self.derniereAction == 'Annuler' :#propose de sauvegarder si on a appuyé avant sur annuler
#            msgBox=QMessageBox()
#            msgBox.setText(u"Vous avez cliqué sur éditer puis annuler")
#            msgBox.setInformativeText(u"Voulez vous sauver vos changement?")
#            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
#            msgBox.setDefaultButton(QMessageBox.Save)
#            reponse = msgBox.exec_()
#            if reponse == QMessageBox.Save :
#                self.OnButtonEditerClicked(True)  #repasse en mode edition puis sauve
#                save=True
#            elif reponse == QMessageBox.Cancel :
#                save=False
#                self.CopieTable2Widget() #réinitialise les champs
#                return


        if save : # enregistrer et repasser en mode lecture si pas d'erreur
            erreur=self.VerifieChamps() #si VerifieChamps ne retourne pas d'erreur...
            if erreur :
                AfficheErreur(erreur, fenetre=self)
            else :
                
                idLock = self.une_table.Lock()  #TODO : verifier si modifications sinon n'enregistre rien
                if idLock > 0 :
                    erreur = 'Erreur : la table"'+self.NomTable +'"est actuellement éditée par un autre utilisateur No:'+str(idLock)
                    if AFFICHE_CONSOLE : print erreur
                    return erreur                
                else : 
                    erreur = self.une_table.EnregistreTable()     
                    if erreur :
                        if AFFICHE_CONSOLE : print erreur
                        return erreur                
                
                self.BasculeModeEdition(False)
        else : #en mode lecture ferme le formulaire
            self.idnouvelletable=self.une_table.Id()
            QtGui.QDialog.accept(self)

class FormComment(QtGui.QDialog): #TODO: revoir utilité
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



