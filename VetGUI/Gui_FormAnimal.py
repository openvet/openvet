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
        
        self.ListeChampAffiches=['Nom', 'Naissance','Robe', 'Sexe', 'Sterilise', 'Identification', 'Commentaires', 'Espece', 'Race1', 'Race2', 'DesactiverRelances']
        
        
        
        self.NomChamp={'Naissance':'Date de naissance', 'Sterilise':u'Stérilisé', 'Espece':u'Espèces', 'Race1': 'Race', 'Race2':'Croisement', 'DesactiverRelances':u'Désactiver les relances'}
        self.TypeChamp={'Naissance':'date','Sexe':'comboBox', 'Sterilise':'checkBox', 'Commentaires':'textEdit','Espece':'comboBox', 'Race1':'comboBox', 'Race2':'comboBox','DesactiverRelances':'checkBox'}
        self.TailleMax={'Sexe':30,'Espece':200, 'Race1':200, 'Race2':200, 'Commentaires':300}
        
        

        self.modeinfo=False        
        
#        self.DataBasedicoChamps=self.une_table.GetDicoChamps() 
        
        
        self.pushButton_perso.setVisible(False)
        
        self.AfficheChamps()

        if self.isNewAnimal:
            self.BasculeModeEdition(True)
        else : 
            self.BasculeModeEdition(False)












