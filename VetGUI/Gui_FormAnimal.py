#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('../VetCore')
sys.path.append('..')

from PyQt4 import QtCore, QtGui
#import PyQt4.Qt as qt
from PyQt4.Qt import *

import config

#from ui_Form_animal import Ui_Dialog_animal

from Gui_FormulaireBase import *


from Mywidgets import *

from Core_Consultation import *
from gestion_erreurs import * 




class FormAnimal(FormulaireBase):
    def __init__(self, parent=None, animal=None):

        #création unanimal (objet de class Tablenimal intermédiaire entre affichage et database) :      widget <-> unanimal<-> database
        if not animal :
            self.une_table=NewAnimal()
            self.edition=False #mode création client
            self.isNewAnimal=True
        else :
            self.une_table=animal#édition d'un client existant
            self.edition=True
            self.isNewAnimal=False        

        FormulaireBase.__init__(self, parent, unetable=self.une_table)

        self.ListeGroupeBox1=['Race_idRace','Race2_idRace']
        self.ListeChampAffiches=['Nom', 'Naissance','Robe', 'Sexe', 'Sterilise', 'Identification', 'Commentaires', 'Especes_idEspeces', self.ListeGroupeBox1, 'DesactiverRelances']

        

        self.NomChamp={'Naissance':'Date de naissance', 'Sterilise':u'Stérilisé', 'Especes_idEspeces':u'Espèces', 'Race_idRace': 'Race', 'Race2_idRace':'X ', 'DesactiverRelances':u'Désactiver les relances'}
        self.TypeChamp={'Naissance':'date','Sexe':'comboBox', 'Sterilise':'checkBox', 'Commentaires':'myTextEdit','Especes_idEspeces':'myComboEspece', 'Race_idRace':'myComboRace', 'Race2_idRace':'myComboRace','DesactiverRelances':'checkBox'}
        self.TailleMax={'Sexe':30,'Espece':200, 'Race1':200, 'Race2':200, 'Commentaires':300}

        self.dicoWidgetLienParentEnfant={'Especes_idEspeces':['Race_idRace', 'Race2_idRace']}#Espece->Race ==> lorsque Espece change envoi un signal à Race pour mettre à jour sa liste

        self.modeinfo=False        

#        self.DataBasedicoChamps=self.une_table.GetDicoChamps() 


        self.pushButton_perso.setVisible(False)

        self.AfficheChamps()

        if self.isNewAnimal:
            self.BasculeModeEdition(True)
        else : 
            self.BasculeModeEdition(False)












