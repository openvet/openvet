#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui

from ui_Form_medical import Ui_tabWidget_medical
from Gui_Consultation import GuiConsultation
from Gui_Analyse import GuiAnalyse


class TabMedical(QtGui.QTabWidget,Ui_tabWidget_medical):
    
    def __init__(self,db,parent=None):
        QtGui.QTabWidget.__init__(self,parent)
        self.setupUi(self)
        self.Qbase=db
        self.editClient = None
        self.editAnimal = None
        self.GuiConsultation=GuiConsultation(self)
        self.GuiAnalyse=GuiAnalyse(self)
        
    def OnSelectAnimal(self,idEspece,idAnimal):
        self.setVisible(True)
        self.GuiConsultation.SetAnimal(idEspece,idAnimal)
        self.GuiAnalyse.SetAnimal(idEspece,idAnimal)
#          self.MyAnalyses=Core_Analyse.Analyses(self.idAnimal)
#          self.listView_Analyses.setModel(self.MyAnalyses)
#          self.HideAnalyse()               
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TabMedical(None)
    window.show()
    window.OnSelectAnimal(1,1)
    sys.exit(app.exec_())
