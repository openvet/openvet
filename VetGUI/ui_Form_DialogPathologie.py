# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogPathologie.ui'
#
# Created: Wed Mar 12 22:07:08 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(394, 286)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_icone = QtGui.QLabel(Dialog)
        self.label_icone.setGeometry(QtCore.QRect(20, 30, 51, 51))
        self.label_icone.setText("")
        self.label_icone.setPixmap(QtGui.QPixmap(":/newPrefix/images/warning.png"))
        self.label_icone.setScaledContents(True)
        self.label_icone.setObjectName("label_icone")
        self.label_text = QtGui.QLabel(Dialog)
        self.label_text.setGeometry(QtCore.QRect(100, 30, 281, 91))
        self.label_text.setObjectName("label_text")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 140, 351, 91))
        self.groupBox.setObjectName("groupBox")
        self.radioButton_update = QtGui.QRadioButton(self.groupBox)
        self.radioButton_update.setGeometry(QtCore.QRect(40, 30, 301, 22))
        self.radioButton_update.setObjectName("radioButton_update")
        self.radioButton_add = QtGui.QRadioButton(self.groupBox)
        self.radioButton_add.setGeometry(QtCore.QRect(40, 60, 301, 22))
        self.radioButton_add.setObjectName("radioButton_add")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edition de Pathologies", None, QtGui.QApplication.UnicodeUTF8))
        self.label_text.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Voulez vous :", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_update.setText(QtGui.QApplication.translate("Dialog", "Modifier le nom de la pathologie courante", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_add.setText(QtGui.QApplication.translate("Dialog", "Créer une nouvelle pathologie", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
