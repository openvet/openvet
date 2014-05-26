# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './OLDForm_DialogClient.ui'
#
# Created: Wed May 14 16:22:23 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogClient(object):
    def setupUi(self, DialogClient):
        DialogClient.setObjectName(_fromUtf8("DialogClient"))
        DialogClient.resize(847, 672)
        self.buttonBox = QtGui.QDialogButtonBox(DialogClient)
        self.buttonBox.setGeometry(QtCore.QRect(40, 630, 799, 25))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(DialogClient)
        self.formLayoutWidget.setGeometry(QtCore.QRect(80, 10, 581, 611))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboBox_Ville = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox_Ville.setObjectName(_fromUtf8("comboBox_Ville"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBox_Ville)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.textEdit_Commentaires = QtGui.QTextEdit(self.formLayoutWidget)
        self.textEdit_Commentaires.setObjectName(_fromUtf8("textEdit_Commentaires"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.textEdit_Commentaires)
        self.comboBox_civilite = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox_civilite.setObjectName(_fromUtf8("comboBox_civilite"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_civilite)
        self.lineEdit_Noml = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_Noml.setObjectName(_fromUtf8("lineEdit_Noml"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_Noml)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)

        self.retranslateUi(DialogClient)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogClient.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogClient.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogClient)

    def retranslateUi(self, DialogClient):
        DialogClient.setWindowTitle(_translate("DialogClient", "Dialog", None))
        self.label_2.setText(_translate("DialogClient", "Ville", None))
        self.label_3.setText(_translate("DialogClient", "Commentaires", None))
        self.label.setText(_translate("DialogClient", "Nom", None))

