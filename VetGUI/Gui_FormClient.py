#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('../VetCore')
sys.path.append('..')

from PyQt4 import QtCore, QtGui
#import PyQt4.Qt as qt
from PyQt4.Qt import *

import config

from ui_Form_animal import Ui_Dialog_animal
from ui_Form_DialogBase import Ui_DialogBase
from Mywidgets import *

from Core_Consultation import *
from gestion_erreurs import * 


        
class FormClient(QtGui.QDialog, Ui_DialogBase):
    """ 
    formulaire pour lire un client (self.edition=False) ou l'éditer / client self.unclient= TableClient
    à la création : formulaire vide, mode nouveau client+édition
    CopieClient2Widget => recopie le client dans les champs du widget (faire SetClient avant pour associer le client au formulaire)
    VerifieChamps => recopie les champs dans client, affiche un msg si erreur
    accept : lié boutton ok, verifie (VerifieChamps) et enregistre le client
    """
    
    Civilite=NouvelleTableCivilite()   #Civilite  et Ville = variable de classe
    Ville=NouvelleTableVille(idPays=config.PAYS)
    
    def __init__(self, parent=None, client=None, version='mycomboville'):
        """ 
        version='liste'   utilise une liste pour remplir combo ville = le + lent  
        version='model'  utilise model/view pour combo ville, avec la liste complète des ville, un peu+rapide
        version='mycomboville' utilise combo personnalisé, nb de ville limité => très rapide
        """
        self.version= version 
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.ListeVilleActif=self.__class__.Ville   #le comboBox ville affiche toutes les villes d'un pays ou une liste plus restreinte (TODO:)
        self.dicoWidget={} # dicoWidget['nomchamp'] = widget associé
        self.dicoWidgetIndependant={}  #idem pour widgets non associés directement à un champ de la data base
        
        #        self.ListeChampIndependant=[]
        self.idnouveauclient=None
        self.cip=''
        self.DesactiveSignaux=False
        self.derniereAction=''
        
        #regroupement de widget : groupés dans ListeGroupeBox ou masqués ListeChampPersonnel = employés)
        self.ListeGroupeBox1= ['IsClient', 'IsVeterinaire', 'IsSalarie','IsFournisseur']    
        self.ListeGroupeBox2=  [ 'IsAssocie','IsCollaborateurLiberal']
        self.ListeGroupeBox2b=['IsConsultant','IsServiceGarde',  'IsReferant'] 
        self.ListeGroupeBox3=['ClientDePassage','AncienClient']
        self.ListeGroupeBox3b=['SousTutelle','MauvaisPayeur' , 'Contentieux'  ]
        self.widgetGroupebox=[]
        self.ListeChampPersonnel=[ 'WIDGETspacer:60',['WIDGETdateentree','DateEntree'], ['WIDGETdatefincontrat','FinContrat'], 'Emploi' , 'Specialite', ['Cadre', 'Temporaire'], 'ConventionCollective', ['Echellon','Coefficient'], 'SalaireHoraire', ['NoOrdre', 'NoCARPV'], 'NoURSSAF', 'NoSecuriteSociale', 'DateNaissance', 'LieuNaissance']
        #TODO: ajouter NomChamp pour ListeChampPersonnel
        
         #listes des champs de la table client qui seront affichés ( dans l'ordre, avec etiquette NomChamp et le widget de type TypeChamp, 
        self.ListeChampAffiches=[self.ListeGroupeBox1, self.ListeGroupeBox2, self.ListeGroupeBox2b,'Civilite_idCivilite','Nom','Prenom',  'Adresse_No' ,  'Adresse_Rue',\
        'WIDGETEditCIP','Commune_idCommune','TelephoneDomicile','TelephoneBureau','TelephonePortable1','TelephonePortable2','Mail','Commentaires', self.ListeGroupeBox3, self.ListeGroupeBox3b, \
        'NbRetardRV', 'NbOublieRV', 'NbOublieOpe']
        
        self.NomChamp={'Civilite_idCivilite':u'Civilité','IsClient':'client', 'IsVeterinaire':u'vétérinaire', 'IsFournisseur':'Fournisseur', \
        'IsSalarie':u'salarié', 'IsAssocie':u'associé' ,'IsCollaborateurLiberal':u'collaborateur libéral','IsConsultant':'consultant',\
        'IsServiceGarde':'service de garde',  'IsReferant':u'référant', 'Prenom':u'Prénom', 'Adresse_No' :u'Numéro batiment/rue', 'Adresse_Rue':'Adresse', \
        'ClientDePassage':'client de passage','AncienClient':'ancien client','SousTutelle':'sous tutelle','MauvaisPayeur':'mauvais payeur' , 'Contentieux' :'contentieux', \
        'WIDGETEditCIP':'Code Postal','Commune_idCommune':'Ville','TelephoneDomicile':u'téléphone domicile','TelephoneBureau':u'téléphone bureau','TelephonePortable1':u'portable 1',\
        'TelephonePortable2':'portable 2','Mail':'e-mail', 'NbRetardRV':'Retards RV', 'NbOublieRV':u'RV oubliés', u'NbOublieOpe':u'Opé oubliées'}
        
        self.TailleMax={'Echellon':60, 'Coefficient':60, 'SalaireHoraire':60, 'NoOrdre':60, 'NoCARPV':60, 'Commentaires':300, 'WIDGETEditCIP':60}
    
        
        self.TypeChamp={'Civilite_idCivilite':'comboBox', 'Commune_idCommune':'comboBox','Commentaires':'textEdit', 'NbRetardRV':'spinBox', \
        'NbOublieRV':'spinBox', 'NbOublieOpe':'spinBox', 'Cadre':'checkBox', 'Temporaire':'checkBox', 'DateEntree':'date' ,'FinContrat':'date' , 'DateNaissance':'date' } #defaut=LineEdit
        if self.version=='mycomboville':
            self.TypeChamp['Commune_idCommune']='myComboBoxVille'#nouvelle methode
            del( self.ListeChampAffiches[self.ListeChampAffiches.index('WIDGETEditCIP')] )
            
        for champ in self.ListeGroupeBox1+self.ListeGroupeBox2+self.ListeGroupeBox3 +self.ListeGroupeBox2b+self.ListeGroupeBox3b:
            self.TypeChamp[champ]='checkBox'

            
            
        #création unclient (objet de class TableClient intermédiaire entre affichage et database) :      widget <-> unclient <-> database
        if not client :
            self.unclient=NouveauClient()
            self.edition=False #mode création client
            self.isNouveauclient=True
        else :
            self.unclient=client #édition d'un client existant
            self.edition=True
            self.isNouveauclient=False
        self.modeinfo=False
            
        self.DataBasedicoChamps=self.unclient.GetDicoChamps() #liste des champs de la Table (= noms des colonnes dans la Data Base)
        self.isSalarie=False
        self.isVeterinaire=False
        #création des wigets
        self.AfficheChamps()
        
        #initialise affichage (masque certains widget) et combo (création listes civilité villes)
        self.ActualiseAffichagePersonnel()
        self.afficheframepersonnel=True#  frame_personnel
        self.OnButtonPersoClicked(False) # masque frame_personnel
        
        self.dicoWidget['IsClient'].setCheckState(Qt.Checked)
        self.InitialiseCivilite()
        self.InitialiseVille()
        
        
        
        # signaux  (voir aussi ConnectSignalWidgetIndependant)
        w=self.dicoWidget['IsVeterinaire']
        self.connect(w, QtCore.SIGNAL("stateChanged(int)"),self.OnIsVeterinaireClicked)
        w=self.dicoWidget['IsSalarie']
        self.connect(w, QtCore.SIGNAL("stateChanged(int)"),self.OnIsSalarieClicked)
        w=self.dicoWidget['Commune_idCommune']
        self.connect(w, QtCore.SIGNAL("editTextChanged(QString)"), self.OncomboVilleChange)
        
        self.connect(self.pushButton_editer, QtCore.SIGNAL("clicked(bool)"),  self.OnButtonEditerClicked)
        self.connect(self.pushButton_perso, QtCore.SIGNAL("clicked(bool)"),  self.OnButtonPersoClicked)
        self.ConnectSignalWidgetIndependant()
        
        if self.isNouveauclient:
            self.BasculeModeEdition(True)
        else : 
            self.BasculeModeEdition(False)
        
    def InitialiseCivilite(self):
        listecivilite=self.__class__.Civilite.GetListe()
        self.dicoWidget['Civilite_idCivilite'].addItems(listecivilite)
        
    def InitialiseVille(self): #TODO: prevoir une autre liste contenant les villes preferees ou les departement preferes et une case a cocher pour afficher le combobox voullu
                                                        #utiliser self.ListeVilleActif


        comboVille=self.dicoWidget['Commune_idCommune'] #comboBox affichant la liste des villes
        
        
        if self.version=='model':  #methode model/view
#            model=self.__class__.Ville.GetModel(proxymodel=True)

#            model=self.__class__.Ville.GetModel()  #QSqlQueryModel =>liste des villes idville  +  nom ville(CIP)
            model=self.__class__.Ville.GetModel(proxymodel=True)  #nouveau proxymodel, créee à partir de  QSqlQueryModel =>liste des villes idville  +  nom ville(CIP)

            comboVille.setModel(model)   
            
            view=   QTableView() 
            view.verticalHeader().hide() #pas d'étiquettes pour les colonnes ou lignes
            view.horizontalHeader().hide()

            comboVille.setView(view)
            comboVille.setModelColumn(1) #utilise colonne1 (linedit), colonne 0 = idVille /
            comboVille.setFixedWidth(250)
           
#            view.resizeColumnsToContents()            
            view.setColumnWidth(1, 250)
            view.setColumnHidden(0, True)#cache colonne 0 (idVille) dans popup du comboBox

            
        elif self.version=='liste':  #ancienne methode 
            listeville=self.__class__.Ville.GetListe()   #creation liste ville (lent)
            comboVille=self.dicoWidget['Commune_idCommune'] #comboBox affichant la liste des villes.addItems(listeville)
        
        
        
        comboVille.setEditable(True)
        comboVille.setInsertPolicy(QComboBox.NoInsert)
#        linedit=comboVille.lineEdit()
#        linedit.selectAll()
        
        if self.version =='liste': #debug
            index=self.__class__.Ville.GetIndex( config.SELECTIONNEVILLEPREFEREE )    #retourne index à partir de idCommune
            w.setCurrentIndex(index)  # à l'ouverture positionne comboBox Ville sur  SELECTIONNEVILLEPREFEREE (si -1=> vide)

    def OnIsVeterinaireClicked(self, state):
        if self.DesactiveSignaux: return
        if state == Qt.Checked :
            self.isVeterinaire=True
        else :
            self.isVeterinaire=False
        self.ActualiseAffichagePersonnel()
        
    def OncomboVilleChange(self, text):
#        print text
        re=".*"+text+".*"
        expr=QRegExp(re)
        
    def OnButtonPersoClicked(self, checked):
        self.afficheframepersonnel=not self.afficheframepersonnel  #bascule visible/invisible
        self.AfficheWidgetsEnfants(self.formLayout_personnel, self.afficheframepersonnel)
        if self.afficheframepersonnel:
            self.pushButton_perso.setText('Masquer les informations personnelles')
        else :
            self.pushButton_perso.setText('Afficher les informations personnelles')
            
    def OnButtonEditerClicked(self, checked):
        
        if self.pushButton_editer.text()=='Annuler':
            self.derniereAction='Annuler'
        else :
            self.derniereAction='Editer'
        
        self.BasculeModeEdition( not self.edition) #inverse mode edition
        
    def OnIsSalarieClicked(self, state):
        if self.DesactiveSignaux: return
        if state == Qt.Checked :
            self.isSalarie=True
        else :
            self.isSalarie=False
        self.ActualiseAffichagePersonnel()
        
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
            
            
            
    def ActualiseAffichagePersonnel(self):
        if self.isVeterinaire==True or self.isSalarie== True :
            bool_affichewidgetpersonnel = True
            self.pushButton_perso.setEnabled(True)
        else :
            bool_affichewidgetpersonnel= False
            self.pushButton_perso.setEnabled(False)
            
        if config.AFFICHEINFOVETO : # 2 choix d'affichage : masque les widget ou les désactive
            self.widgetGroupebox[1].setEnabled(bool_affichewidgetpersonnel)
            self.widgetGroupebox[2].setEnabled(bool_affichewidgetpersonnel)
        else :
            self.widgetGroupebox[1].setVisible(bool_affichewidgetpersonnel)
            self.widgetGroupebox[2].setVisible(bool_affichewidgetpersonnel)
            
        
        if bool_affichewidgetpersonnel  :  #décoche par défaut client si véto ou salarié est coché (remarque: autorise l'inverse = cocher client sans décocher véto)
            if not self.DesactiveSignaux :   #  cf CopieClient2Widget (coche automatiquement isVéto => empécher le décochage de isClient)
                self.dicoWidget['IsClient'].setCheckState(Qt.Unchecked)  
        else : #ni véto ni salarié
            self.dicoWidget['IsClient'].setCheckState(Qt.Checked) 
            
    def EnableWidget(self,  active):#selon mode edition ou nouveau client
        
        for widget in self.dicoWidget.values() + self.dicoWidgetIndependant.values() :
            widget.setEnabled(active)
        if self.isVeterinaire==True or self.isSalarie== True :
            self.pushButton_perso.setEnabled(True)#toujours actif
            
        
        
        
    def AfficheChamps(self):
        "fonction principale qui affiche tous les widgets du formulaire +/- recopie unclient dans widgets"
        
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

        if self.edition==True:
            self.CopieClient2Widget()
        else : 
            self.CopieClient2Widget(efface=True) #efface les widgets
                
                
        #self.formLayout=self.formLayout_personnel   #changement de colonne
            
        #for c in self.ListeChampPersonnel : #champ masqués si client =True, concerne uniquement les employés de la clinique

    def CreeWidget(self, champ):  
        "crée et retourne une étiquette de champ + widget d'édition (champ=nom du champ dans la DataBase)"
        
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
        return( [nomchamp, widget])

    def CreeWidgetEdit(self, nomchamp, typechamp, taille): 
       
        if typechamp=='LineEdit' :
            unwidget=QLineEdit(self)
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
        for champ in self.dicoWidgetIndependant.keys() :
            widget=self.dicoWidgetIndependant[champ]
            if champ=='WIDGETdatefincontrat' :
                self.connect(widget, QtCore.SIGNAL("stateChanged(int)"),self.OnCheckBoxActiveDateFin)
                self.OnCheckBoxActiveDateFin(False)
            elif champ == 'WIDGETdateentree' :
                self.connect(widget, QtCore.SIGNAL("stateChanged(int)"),self.OnCheckBoxActiveDateDebut)
                self.OnCheckBoxActiveDateDebut(False)
                
            elif champ=='WIDGETEditCIP':
                self.connect(widget, QtCore.SIGNAL("textChanged (QString)"),self.OnEditCIP)
                self.connect(widget, QtCore.SIGNAL("editingFinished()"),self.OnFinEditCIP)
                
    def OnEditCIP(self, cip):

        if len(cip.replace(' ', ''))==2:  #filtre seulement si code format '99 '
            self.SelectionneCip(cip)

        
        
    def OnFinEditCIP(self): #version<> mycomboville
        cip=self.dicoWidgetIndependant['WIDGETEditCIP'].text()
        self.SelectionneCip(cip)
        

    def SelectionneCip(self, cip):  #version<> mycomboville
            cip=cip.replace(' ', '')
            if self.cip == cip :#ne filtre pas si le cip n'a pas changé
                return
            self.cip = cip 
            recherche='*('+cip+'*'   #  ex recherche (60   
            combo=self.dicoWidget['Commune_idCommune']
            proxymodel=combo.model()
            proxymodel.setFilterKeyColumn(1)  #  nomcommune(CIP)
            proxymodel.setFilterRegExp ( QRegExp(recherche, syntax = QRegExp.Wildcard)  )


    def OnCheckBoxActiveDateFin(self, state):
        w=self.dicoWidget['FinContrat']
        w.setEnabled(state)
        
    def OnCheckBoxActiveDateDebut(self, state):
        w=self.dicoWidget['DateEntree']
        w.setEnabled(state)
        
    def AfficheTousLesChamps(self): 
        "non utilisé : affiche tous les champs d'une table de la base de donnée"
        self.formLayout=self.formLayout1
        nbchamp=0
        for champ in self.unclient.GetListeChamps():
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
                
                
    def SetClient(self, client, modeinfo=False):
        self.unclient=client
        self.modeinfo=modeinfo
        self.DataBasedicoChamps=self.unclient.GetDicoChamps()  #actualise DataBasedicoChamps avec les champs du nouveau client
        self.CopieClient2Widget()
        self.isNouveauclient=False
        self.BasculeModeEdition(False)
        
    def CopieClient2Widget(self, efface=False):
        "recopie tous les champs de unclient dans les widgets (ou efface tous les widgets)"
        
        self.DesactiveFramePersonnel()
        self.DesactiveSignaux=True #empeche certains signaux (pas tous) par ex OnIsVeterinaireClicked (qui décoche isClient => indésirable ici)
        
        id=self.unclient.Id()
        if efface or not id : #efface tout
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
                                self.DesativeChamp(nomchamp)
                                
                            except:
                                pass
                    
            try :
                widget=self.dicoWidget['Commune_idCommune']        
                if self.version == 'mycomboville' :
                    pass #TODO: ++++++++++
                else :
                    index=self.__class__.Ville.GetIndex( config.SELECTIONNEVILLEPREFEREE)
                    widget.setCurrentIndex(index)
                    nomville=widget.currentText()
                    cip=nomville.split('(')[1].split(')')[0]#récupère code postal entre ()
                    self.dicoWidgetIndependant['WIDGETEditCIP'].setText(cip)
            except :
                pass
                
            self.dicoWidget['IsClient'].setCheckState(Qt.Checked)
             #Fin efface
            
        
        else : #copie client dans widgets
            for nomchamp in self.dicoWidget.keys():  #dicoWidget[nomchamp]=widget associé
                typechamp= self.TypeChamp[nomchamp]
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
                        
                elif typechamp == 'myComboBoxVille' :
                    idville=unchamp.Value()
                    widget.SetId(idville)
                        
                elif typechamp ==  'comboBox' :
                    #index=widget.currentIndex()
                    if nomchamp == 'Civilite_idCivilite' :
                        idcivilite=unchamp.Value()
                        index=self.__class__.Civilite.GetIndex(idcivilite)
                        widget.setCurrentIndex(index)
                    elif nomchamp == 'Commune_idCommune' :#self.version <>'mycomboville' 
                        idville=unchamp.Value()
                        index=self.__class__.Ville.GetIndex(idville)  # récupère index dans liste des Villes
                        widget.setCurrentIndex(index)
                        nomville=widget.currentText()
                        try :
                            cip=nomville.split('(')[1].split(')')[0]#récupère code postal entre ()
                            self.dicoWidgetIndependant['WIDGETEditCIP'].setText(cip)
                        except :
                            print 'erreur WIDGETEditCIP Gui_Consultation_base.CopieClient2Widget()'

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
            self.isVeterinaire=self.dicoWidget['IsVeterinaire'] .isChecked()
            self.isSalarie= self.dicoWidget['IsSalarie'] .isChecked()
            self.ActualiseAffichagePersonnel()
            
        self.DesactiveSignaux=False
         
    def DesativeChamp(self, champ, active=False):
        if active :
            state=Qt.Checked
        else :
            state=Qt.Unchecked
        
        if champ=='DateEntree' :
            self.dicoWidgetIndependant['WIDGETdateentree'].setCheckState(state)
            self.OnCheckBoxActiveDateDebut(state)
             
        elif champ=='FinContrat':
            self.dicoWidgetIndependant['WIDGETdatefincontrat'].setCheckState(state)
            self.OnCheckBoxActiveDateFin(state)
        
    def DesactiveFramePersonnel(self, desactive=True):
        self.afficheframepersonnel=desactive
        self.OnButtonPersoClicked(True) # clique logiciel sur boutton perso => bascule afficheframepersonnel
        
        
    def VerifieChamps(self, listedeschamps=None):
        "copie le formulaire (la valeur des widgets) dans unclient et retourne les erreurs"
        erreur=''
        if not listedeschamps : 
            if self.isSalarie or self.isVeterinaire :
                listedeschamps=self.ListeChampAffiches+self.ListeChampPersonnel
            else :
                listedeschamps=self.ListeChampAffiches
        for unchamp in listedeschamps :
            err=''
            
            if 'WIDGET' in unchamp :    # ne fait pas partie de la data base
                continue                        #champ suivant

            if 'list' in str(type(unchamp)) : # => liste groupe box
                err=self.VerifieChamps(  unchamp)  #unchamp est en realité une liste de champs => appel récursif
            
            else :              
                
                #1/ récupère la valeur du widget
            
                widget=self.dicoWidget[unchamp]   #widget associé au champ
                if not widget.isEnabled() :  #ne lit pas les widget désactivés
                    continue
                typechamp=self.TypeChamp[unchamp ] 
                valeur='__aucunevaleur__'
                if 'Edit' in typechamp : #  line ou text edit
                    if typechamp == 'LineEdit' :
                        valeur=widget.text()
                    else : 
                        valeur=widget.toPlainText()
                elif typechamp == 'checkBox' :
                    valeur = widget.isChecked()
                    
                elif typechamp == 'myComboBoxVille':
                    index=widget.currentIndex()
                    valeur=widget.GetId(index)
                    
                elif typechamp ==  'comboBox' :
                    index=widget.currentIndex()
                    if unchamp == 'Civilite_idCivilite' :
                        valeur=self.__class__.Civilite.GetId(index)
                    elif unchamp == 'Commune_idCommune' : #self.version <> 'mycomboville'  car typechamp ==  'comboBox' 
                        valeur=self.ListeVilleActif.GetId(index)
                        if not valeur :
                            valeur='__aucunevaleur__' 
                            err='erreur Commune (index invalide) Gui_Consultation_base::VerifieChamps()'

                elif typechamp ==  'spinBox' :
                    valeur=widget.value()
                elif typechamp ==  'date' :
                    valeur=widget.date()
                    
                #2/ mémorise (dans un client)  et test si valeur est correct
                if valeur <> '__aucunevaleur__' :
                    err=self.unclient.SetChamp(unchamp, valeur)  
                    
            if err :
                if 'ne peut pas etre NULL' in err : err=u' à renseigner !' #change le msg d'erreur
                erreur+=self.NomChamp[unchamp]+err +'\n'
                
        return erreur
            
            
            
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
            
    def reject(self):
        if (self.edition  and self.isNouveauclient) or (not self.edition  and not self.isNouveauclient) :
            QtGui.QDialog.reject(self)   #nouveau client    ou      ancien client en lecture simple => sort du formulaire 
        else :                                      #sinon repasse en visualisation fiche client
            self.BasculeModeEdition(False)
            
    def accept(self):
        save = self.edition #en mode edition enregistre le client
        
        if self.derniereAction == 'Annuler' :#propose de sauvegarder si on a appuyé avant sur annuler
            msgBox=QMessageBox()
            msgBox.setText(u"Vous avez cliqué sur éditer puis annuler")
            msgBox.setInformativeText(u"Voulez vous sauver vos changement?")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save)
            reponse = msgBox.exec_()
            if reponse == QMessageBox.Save :
                self.OnButtonEditerClicked(True)  #repasse en mode edition puis sauve
                save=True
            elif reponse == QMessageBox.Cancel :
                return


        if save : # enregistrer et repasser en mode lecture si pas d'erreur
            erreur=self.VerifieChamps() or self.unclient.EnregistreTable()     #si VerifieChamps ne retourne pas d'erreur, EnregistreTable
            if erreur :
                AfficheErreur(erreur, fenetre=self)
            else :
                self.BasculeModeEdition(False)
        else : #en mode lecture ferme le formulaire
            self.idnouveauclient=self.unclient.Id()
            QtGui.QDialog.accept(self)
            
                



class FormComment(QtGui.QDialog): #TODO: a déplacer dans un autre fichier
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
    pass
#    
#    app = QtGui.QApplication(sys.argv)
#    window = WindowsTest()
#    window.show()
#    sys.exit(app.exec_())
