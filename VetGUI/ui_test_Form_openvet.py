# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './test_Form_openvet.ui'
#
# Created: Mon May 12 12:17:39 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(756, 822)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../.designer/images/icone.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 370, 501, 301))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setMargin(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.tabWidget = QtGui.QTabWidget(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(120, 60, 221, 221))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.pushButton_2 = QtGui.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 90, 99, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(520, 270, 160, 80))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_4 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(410, 10, 231, 251))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_5 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout.addWidget(self.pushButton_5, 0, 0, 1, 1)
        self.pushButton_6 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout.addWidget(self.pushButton_6, 1, 0, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 0, 1, 1, 1)
        self.toolButton = QtGui.QToolButton(self.gridLayoutWidget)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout.addWidget(self.toolButton, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 756, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDossiers_M_dicaux = QtGui.QMenu(self.menubar)
        self.menuDossiers_M_dicaux.setObjectName(_fromUtf8("menuDossiers_M_dicaux"))
        self.menuComptabilit = QtGui.QMenu(self.menubar)
        self.menuComptabilit.setObjectName(_fromUtf8("menuComptabilit"))
        self.menuD_clarations = QtGui.QMenu(self.menuComptabilit)
        self.menuD_clarations.setObjectName(_fromUtf8("menuD_clarations"))
        self.menuConfiguration = QtGui.QMenu(self.menubar)
        self.menuConfiguration.setObjectName(_fromUtf8("menuConfiguration"))
        self.menuBase_de_donn_es = QtGui.QMenu(self.menuConfiguration)
        self.menuBase_de_donn_es.setObjectName(_fromUtf8("menuBase_de_donn_es"))
        self.menuQuitter = QtGui.QMenu(self.menubar)
        self.menuQuitter.setObjectName(_fromUtf8("menuQuitter"))
        self.menuStock = QtGui.QMenu(self.menubar)
        self.menuStock.setObjectName(_fromUtf8("menuStock"))
        self.menuStatistiques = QtGui.QMenu(self.menubar)
        self.menuStatistiques.setObjectName(_fromUtf8("menuStatistiques"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Recettes = QtGui.QAction(MainWindow)
        self.action_Recettes.setObjectName(_fromUtf8("action_Recettes"))
        self.actionD_penses = QtGui.QAction(MainWindow)
        self.actionD_penses.setObjectName(_fromUtf8("actionD_penses"))
        self.action_Banque = QtGui.QAction(MainWindow)
        self.action_Banque.setObjectName(_fromUtf8("action_Banque"))
        self.actionRecoupement_bancaire = QtGui.QAction(MainWindow)
        self.actionRecoupement_bancaire.setObjectName(_fromUtf8("actionRecoupement_bancaire"))
        self.actionTVA = QtGui.QAction(MainWindow)
        self.actionTVA.setObjectName(_fromUtf8("actionTVA"))
        self.action2035 = QtGui.QAction(MainWindow)
        self.action2035.setObjectName(_fromUtf8("action2035"))
        self.actionCommandes = QtGui.QAction(MainWindow)
        self.actionCommandes.setObjectName(_fromUtf8("actionCommandes"))
        self.actionAnalyse = QtGui.QAction(MainWindow)
        self.actionAnalyse.setObjectName(_fromUtf8("actionAnalyse"))
        self.action_Facturation = QtGui.QAction(MainWindow)
        self.action_Facturation.setObjectName(_fromUtf8("action_Facturation"))
        self.actionBureau = QtGui.QAction(MainWindow)
        self.actionBureau.setObjectName(_fromUtf8("actionBureau"))
        self.action_M_dicaments = QtGui.QAction(MainWindow)
        self.action_M_dicaments.setObjectName(_fromUtf8("action_M_dicaments"))
        self.action_Pathologies = QtGui.QAction(MainWindow)
        self.action_Pathologies.setObjectName(_fromUtf8("action_Pathologies"))
        self.actionBackup = QtGui.QAction(MainWindow)
        self.actionBackup.setObjectName(_fromUtf8("actionBackup"))
        self.actionRestore = QtGui.QAction(MainWindow)
        self.actionRestore.setObjectName(_fromUtf8("actionRestore"))
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionR_seau_S_curit = QtGui.QAction(MainWindow)
        self.actionR_seau_S_curit.setObjectName(_fromUtf8("actionR_seau_S_curit"))
        self.actionQuitter = QtGui.QAction(MainWindow)
        self.actionQuitter.setObjectName(_fromUtf8("actionQuitter"))
        self.menuD_clarations.addAction(self.actionTVA)
        self.menuD_clarations.addAction(self.action2035)
        self.menuComptabilit.addAction(self.action_Recettes)
        self.menuComptabilit.addAction(self.actionD_penses)
        self.menuComptabilit.addAction(self.action_Banque)
        self.menuComptabilit.addAction(self.actionRecoupement_bancaire)
        self.menuComptabilit.addAction(self.menuD_clarations.menuAction())
        self.menuBase_de_donn_es.addAction(self.actionBackup)
        self.menuBase_de_donn_es.addAction(self.actionRestore)
        self.menuBase_de_donn_es.addAction(self.actionImport)
        self.menuConfiguration.addAction(self.actionBureau)
        self.menuConfiguration.addAction(self.action_Facturation)
        self.menuConfiguration.addAction(self.action_M_dicaments)
        self.menuConfiguration.addAction(self.action_Pathologies)
        self.menuConfiguration.addSeparator()
        self.menuConfiguration.addAction(self.menuBase_de_donn_es.menuAction())
        self.menuConfiguration.addAction(self.actionR_seau_S_curit)
        self.menuQuitter.addAction(self.actionQuitter)
        self.menuStock.addAction(self.actionCommandes)
        self.menuStock.addAction(self.actionAnalyse)
        self.menubar.addAction(self.menuDossiers_M_dicaux.menuAction())
        self.menubar.addAction(self.menuStock.menuAction())
        self.menubar.addAction(self.menuComptabilit.menuAction())
        self.menubar.addAction(self.menuStatistiques.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menuQuitter.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Open Vet", None))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton", None))
        self.radioButton.setText(_translate("MainWindow", "RadioButton", None))
        self.toolButton.setText(_translate("MainWindow", "...", None))
        self.menuDossiers_M_dicaux.setTitle(_translate("MainWindow", "Dossiers Médicaux", None))
        self.menuComptabilit.setTitle(_translate("MainWindow", "Comptabilité", None))
        self.menuD_clarations.setTitle(_translate("MainWindow", "Déclarations", None))
        self.menuConfiguration.setTitle(_translate("MainWindow", "Paramètres", None))
        self.menuBase_de_donn_es.setTitle(_translate("MainWindow", "Base de données", None))
        self.menuQuitter.setTitle(_translate("MainWindow", "Quitter", None))
        self.menuStock.setTitle(_translate("MainWindow", "Stock", None))
        self.menuStatistiques.setTitle(_translate("MainWindow", "Statistiques", None))
        self.action_Recettes.setText(_translate("MainWindow", "&Recettes", None))
        self.actionD_penses.setText(_translate("MainWindow", "&Dépenses", None))
        self.action_Banque.setText(_translate("MainWindow", "&Banque", None))
        self.actionRecoupement_bancaire.setText(_translate("MainWindow", "Recoupement bancaire", None))
        self.actionTVA.setText(_translate("MainWindow", "TVA", None))
        self.action2035.setText(_translate("MainWindow", "2035", None))
        self.actionCommandes.setText(_translate("MainWindow", "&Commandes", None))
        self.actionAnalyse.setText(_translate("MainWindow", "Visualisation", None))
        self.action_Facturation.setText(_translate("MainWindow", "&Facturation", None))
        self.actionBureau.setText(_translate("MainWindow", "Bureau", None))
        self.actionBureau.setShortcut(_translate("MainWindow", "Ctrl+Alt+B", None))
        self.action_M_dicaments.setText(_translate("MainWindow", "&Médicaments", None))
        self.action_Pathologies.setText(_translate("MainWindow", "&Pathologies", None))
        self.actionBackup.setText(_translate("MainWindow", "Backup", None))
        self.actionRestore.setText(_translate("MainWindow", "Restore", None))
        self.actionImport.setText(_translate("MainWindow", "Import", None))
        self.actionR_seau_S_curit.setText(_translate("MainWindow", "Réseau/Sécurité", None))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter", None))
        self.actionQuitter.setToolTip(_translate("MainWindow", "Quitter l\'application", None))
        self.actionQuitter.setShortcut(_translate("MainWindow", "Ctrl+Q", None))

import resources_rc
