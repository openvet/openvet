#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_DialogModeleAnalyse import Ui_DialogModelAnalyse
from Core_Analyse import ModelesAnalyse

class FormModeleAnalyse(QDialog, Ui_DialogModelAnalyse):
    def __init__(self, Modele,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_ModeleAnalyse)
        #TODO mapper?
        self.lineEdit_ModeleLibele.setText(Modele.Modele[3])
        self.lineEdit_RemarqueModel.setText(Modele.Modele[5])
        self.horizontalSlider_Modele.setValue(Modele.Modele[6].toInt()[0])
        self.listWidget_Parametres.clear()
        for i in Modele.Parametres:
            self.listWidget_Parametres.addItem(i[5].toString())
        self.MyModels=ModelesAnalyse(Modele.Modele[2],Modele.Modele[4])
        self.MyModels.selection=Modele.Modele[1]
        if Modele.Modele[0]==3:
            pass#TODO:add newModele
        self.horizontalSlider_Modele.setMinimum(1)
        self.horizontalSlider_Modele.setMaximum(self.MyModels.rowCount())
        self.listView_Modeles.setModel(self.MyModels)
        self.connect(self.horizontalSlider_Modele,SIGNAL('valueChanged(int)'),self.OnSlider)
        
    def OnSlider(self,value):
        self.MyModels.setData(self.MyModels.indexSelection, value, Qt.EditRole)
        #sort ne marche pas
        self.MyModels.sort(3,Qt.AscendingOrder)
        self.Print()
    
    def Print(self):    #debug Only
        for i in self.MyModels.listdata:
            tmp=[]
            for j in i:
                try:
                    tmp.append('%s'%j.toString())
                except:
                    tmp.append('%s'%j) 
            print ';'.join(tmp)   