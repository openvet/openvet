# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogBase.ui'
#
# Created: Fri May 23 10:32:52 2014
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

class Ui_DialogBase(object):
    def setupUi(self, DialogBase):
        DialogBase.setObjectName(_fromUtf8("DialogBase"))
        DialogBase.resize(951, 675)
        self.horizontalLayoutWidget = QtGui.QWidget(DialogBase)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 931, 601))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.formLayout1 = QtGui.QFormLayout()
        self.formLayout1.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout1.setObjectName(_fromUtf8("formLayout1"))
        self.horizontalLayout.addLayout(self.formLayout1)
        self.formLayout2 = QtGui.QFormLayout()
        self.formLayout2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout2.setObjectName(_fromUtf8("formLayout2"))
        self.horizontalLayout.addLayout(self.formLayout2)
        self.formLayout3 = QtGui.QFormLayout()
        self.formLayout3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout3.setObjectName(_fromUtf8("formLayout3"))
        self.horizontalLayout.addLayout(self.formLayout3)
        self.formLayout_personnel = QtGui.QFormLayout()
        self.formLayout_personnel.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_personnel.setObjectName(_fromUtf8("formLayout_personnel"))
        self.horizontalLayout.addLayout(self.formLayout_personnel)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(DialogBase)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(220, 610, 711, 61))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_perso = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_perso.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_perso.setObjectName(_fromUtf8("pushButton_perso"))
        self.horizontalLayout_2.addWidget(self.pushButton_perso)
        self.pushButton_editer = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_editer.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_editer.setObjectName(_fromUtf8("pushButton_editer"))
        self.horizontalLayout_2.addWidget(self.pushButton_editer)
        self.buttonBox = QtGui.QDialogButtonBox(self.horizontalLayoutWidget_2)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(DialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogBase)

    def retranslateUi(self, DialogBase):
        DialogBase.setWindowTitle(_translate("DialogBase", "Dialog", None))
        self.pushButton_perso.setText(_translate("DialogBase", "Afficher les informations personnelles", None))
        self.pushButton_editer.setText(_translate("DialogBase", "Editer", None))

