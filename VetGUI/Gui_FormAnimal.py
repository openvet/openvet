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




class FormAnimal(QtGui.QDialog, Ui_Dialog_animal):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        print parent.dataAnimal
        self.setupUi(self)

#class FormComment(QtGui.QDialog): # cf gui_formclient
#    def __init__(self,parent=None):
#        super(FormComment,self).__init__(parent)
#        self.resize(400, 255)
#        self.setWindowTitle("Edition Consultation")
#        self.buttonBox = QtGui.QDialogButtonBox(self)
#        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 341, 32))
#        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
#        self.label = QtGui.QLabel(self)
#        self.label.setGeometry(QtCore.QRect(20, 20, 191, 17))
#        self.label.setText("Entrez votre commentaire :")
#        self.plainTextEdit = QtGui.QPlainTextEdit(self)
#        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 361, 141))
#        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
#        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

if __name__ == '__main__':
    pass
#    
#    app = QtGui.QApplication(sys.argv)
#    window = WindowsTest()
#    window.show()
#    sys.exit(app.exec_())
