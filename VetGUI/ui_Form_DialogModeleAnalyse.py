# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogModeleAnalyse.ui'
#
# Created: Sun May 18 22:36:19 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogModelAnalyse(object):
    def setupUi(self, DialogModelAnalyse):
        DialogModelAnalyse.setObjectName("DialogModelAnalyse")
        DialogModelAnalyse.resize(367, 510)
        self.buttonBox = QtGui.QDialogButtonBox(DialogModelAnalyse)
        self.buttonBox.setGeometry(QtCore.QRect(20, 470, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtGui.QWidget(DialogModelAnalyse)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 344, 451))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_ModeleAnalyse = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_ModeleAnalyse.setObjectName("verticalLayout_ModeleAnalyse")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_ModelLibele = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        self.label_ModelLibele.setFont(font)
        self.label_ModelLibele.setObjectName("label_ModelLibele")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_ModelLibele)
        self.lineEdit_ModeleLibele = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_ModeleLibele.setReadOnly(True)
        self.lineEdit_ModeleLibele.setObjectName("lineEdit_ModeleLibele")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_ModeleLibele)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_RemarqueModel = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_RemarqueModel.setMaxLength(200)
        self.lineEdit_RemarqueModel.setObjectName("lineEdit_RemarqueModel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_RemarqueModel)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalSlider_Modele = QtGui.QSlider(self.layoutWidget)
        self.horizontalSlider_Modele.setMinimum(1)
        self.horizontalSlider_Modele.setMaximum(20)
        self.horizontalSlider_Modele.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Modele.setObjectName("horizontalSlider_Modele")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.horizontalSlider_Modele)
        self.listWidget_Parametres = QtGui.QListWidget(self.layoutWidget)
        self.listWidget_Parametres.setObjectName("listWidget_Parametres")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.listWidget_Parametres)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.verticalLayout_ModeleAnalyse.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.listView_Modeles = QtGui.QListView(self.layoutWidget)
        self.listView_Modeles.setObjectName("listView_Modeles")
        self.horizontalLayout.addWidget(self.listView_Modeles)
        self.verticalLayout_ModeleAnalyse.addLayout(self.horizontalLayout)
        self.label_ModelLibele.setBuddy(self.lineEdit_ModeleLibele)
        self.label_2.setBuddy(self.lineEdit_RemarqueModel)
        self.label_3.setBuddy(self.horizontalSlider_Modele)

        self.retranslateUi(DialogModelAnalyse)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogModelAnalyse.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogModelAnalyse.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModelAnalyse)

    def retranslateUi(self, DialogModelAnalyse):
        DialogModelAnalyse.setWindowTitle(QtGui.QApplication.translate("DialogModelAnalyse", "OpenVet", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ModelLibele.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Modèle :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Remarque :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Priorité :", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Paramètres:", None, QtGui.QApplication.UnicodeUTF8))

