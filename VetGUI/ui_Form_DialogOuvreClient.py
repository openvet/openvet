# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogOuvreClient.ui'
#
# Created: Mon May  5 17:52:37 2014
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

class Ui_Dialog_OuvreClient(object):
    def setupUi(self, Dialog_OuvreClient):
        Dialog_OuvreClient.setObjectName(_fromUtf8("Dialog_OuvreClient"))
        Dialog_OuvreClient.resize(846, 302)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/images/add1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog_OuvreClient.setWindowIcon(icon)
        Dialog_OuvreClient.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_OuvreClient)
        self.buttonBox.setGeometry(QtCore.QRect(430, 230, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.comboBox_ListeClient = QtGui.QComboBox(Dialog_OuvreClient)
        self.comboBox_ListeClient.setGeometry(QtCore.QRect(10, 100, 771, 31))
        self.comboBox_ListeClient.setObjectName(_fromUtf8("comboBox_ListeClient"))
        self.pushButton_NouveauClient = QtGui.QPushButton(Dialog_OuvreClient)
        self.pushButton_NouveauClient.setGeometry(QtCore.QRect(800, 90, 41, 41))
        self.pushButton_NouveauClient.setText(_fromUtf8(""))
        self.pushButton_NouveauClient.setIcon(icon)
        self.pushButton_NouveauClient.setObjectName(_fromUtf8("pushButton_NouveauClient"))

        self.retranslateUi(Dialog_OuvreClient)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_OuvreClient.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_OuvreClient.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_OuvreClient)

    def retranslateUi(self, Dialog_OuvreClient):
        Dialog_OuvreClient.setWindowTitle(_translate("Dialog_OuvreClient", "Ouvrir une fiche client", None))

import resources_rc
