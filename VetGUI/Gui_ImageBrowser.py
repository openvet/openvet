#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from shutil import copyfile
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# import QtPoppler
#import poppler
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
import config
from ui_Form_DialogAnalyse import Ui_Form_DialogAnalyse
from Viewer import DocViewer

class FormAnalyse(QDialog, Ui_Form_DialogAnalyse):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_4)
        self.FichierInterne=None
        self.Etiquette=None
        self.FichierPerso=None
        self.Path=None
        self.Titre=None
        self.ext=None
        self.Importe=True
        self.SizeSticker=QSize(320,240)
        self.MyViewer=DocViewer()
        self.textEdit_DocAnalyse.setHidden(True)
        self.toolButton_Fichier.clicked.connect(self.OnFile)
        self.radioButton_img.clicked.connect(self.OnRadio)
        self.radioButton_doc.clicked.connect(self.OnRadio)
        self.pushButton_Ok.clicked.connect(self.OnValid)
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        #ToolBar
        contrast=QAction(QIcon('../images/contraste.png'),'Contraste',self) #Path_Icones
        brightness=QAction(QIcon('../images/luminosite.png'),u'Luminosité',self)
        balance=QAction(QIcon('../images/balance.png'),'Balance',self)
        sharpen=QAction(QIcon('../images/scalpel.png'),u'Améliore nettetée',self)
        zoom=QAction(QIcon('../images/loupe2.png'),'Zoom',self)
        restore=QAction(QIcon('../images/default.png'),'Restaure l\'image originale',self)
        Lpage=QAction(QIcon('../images/pagegauche.png'),u'Page précédente',self)
        Rpage=QAction(QIcon('../images/pagedroite.png'),u'Page suivante',self)
        self.connect(contrast,SIGNAL("triggered()"),self.OnContrast)
        self.connect(brightness,SIGNAL("triggered()"),self.OnBrightness)
        self.Slider=QSlider(Qt.Horizontal)
        self.Slider.setRange(-100,100)
        self.Slider.setValue(0)
        page=QLineEdit()
        page.setMaximumWidth(50)
        self.ToolBar=QToolBar('Image')
        self.ToolBar.addActions((brightness,contrast,balance,sharpen,zoom,restore))
        self.ToolBar.addWidget(self.Slider)
        self.ToolBar.addAction(Lpage)
        self.ToolBar.addWidget(page)
        self.ToolBar.addAction(Rpage)
        
        
    def Set(self,data):  
        self.Importe=False 
        self.label.setVisible(False)
        self.radioButton_doc.setVisible(False)
        self.radioButton_img.setVisible(False)
        self.toolButton_Fichier.setVisible(False)
        self.lineEdit_Fichier.setVisible(False)
        self.lineEdit_Titre.setText(data[0])
        self.FichierInterne=data[1]
        self.FichierPerso=self.MyViewer.Filename_('_p',data[1])
        if os.path.isfile(self.FichierPerso):
            data[1]=self.FichierPerso
        self.label_FichierInterne.setText('Fichier :%s%s'%(config.Path_Analyses,data[1]))
        path=data[1]
        self.MyViewer.SetFilename('%s%s'%(config.Path_Analyses,path))
        self.ext=self.MyViewer.GetSuffix()
        if str(self.ext) in ['jpg','jpeg','bmp','png','pdf']:
            self.verticalLayout_4.setMenuBar(self.ToolBar)
            self.textEdit_DocAnalyse.setVisible(False)
            self.label_ImageViewer.setVisible(True)
            self.label_ImageViewer.setPixmap(self.MyViewer.ViewImage(self.label_ImageViewer.size()))
        else:
            self.textEdit_DocAnalyse.setVisible(True)
            self.label_ImageViewer.setVisible(False)
            self.MyViewer.ViewText(self.textEdit_DocAnalyse)
            
            
    def OnFile(self):   #TODO: fusion with seilf.Set()
        self.lineEdit_Fichier.setText(QFileDialog.getOpenFileName(self,u'OpenVet-Choisissez le fichier à importer')) 
        path=self.lineEdit_Fichier.text()
        self.MyViewer.SetFilename(path)
        self.ext=self.MyViewer.GetSuffix()
        if str(self.ext) in ['jpg','jpeg','bmp','png']:
            self.radioButton_img.setChecked(True)
            self.FichierInterne='AI' 
        else:
            self.radioButton_doc.setChecked(True)
            self.FichierInterne='AD' 
        if str(self.ext) in ['jpg','jpeg','bmp','png','pdf']:
            self.textEdit_DocAnalyse.setVisible(False)
            self.label_ImageViewer.setVisible(True)
            self.label_ImageViewer.setPixmap(self.MyViewer.ViewImage(self.label_ImageViewer.size()))
        else:       # str(self.ext) in ['txt','rtf','html','htm','cvs']:
            self.textEdit_DocAnalyse.setVisible(True)
            self.label_ImageViewer.setVisible(False)
            self.MyViewer.ViewText(self.textEdit_DocAnalyse)
#                 self.textEdit_DocAnalyse.setVisible(False)
#                 self.label_ImageViewer.setVisible(True)
#                 self.label_ImageViewer.setPixmap(self.MyViewer.ViewImage(self.label_ImageViewer.size()))
        self.FichierInterne=self.FichierInterne+'%010x.%s'%(QDateTime().currentDateTime().toTime_t(),self.ext)
        self.Path=path
        self.label_FichierInterne.setText('Nom de fichier interne : %s'%self.FichierInterne)
            
    def OnRadio(self):
        if self.radioButton_img.isChecked():
            self.FichierInterne='AI'+self.FichierInterne[2:]
        else:
            self.FichierInterne='AD'+self.FichierInterne[2:]
        self.label_FichierInterne.setText('Nom de fichier interne : %s'%self.FichierInterne)    

    def OnSharpen(self):
        self.MyViewer.Shapen()
        
    def OnBrightness(self):
        self.MyViewer.Brightness(self.Slider.value())
        self.Slider.setValue(0)
        self.label_ImageViewer.setPixmap(self.MyViewer.ViewImage(self.label_ImageViewer.size()))
        
    def OnContrast(self):
        pass
        
    def OnValid(self):
        if self.Importe:
            copyfile(self.Path,'%s%s'%(config.Path_Analyses,self.FichierInterne))
            self.Etiquette=self.MyViewer.MakeSticker(self.SizeSticker,'%s%s'%(config.Path_Analyses,self.FichierInterne))
        self.Titre=self.lineEdit_Titre.text()
        self.accept()
        
    def OnCancel(self):
        self.close()
        
    def resizeEvent(self,event):
        if str(self.ext) in ['jpg','jpeg','bmp','png','pdf']:
            self.label_ImageViewer.setPixmap(self.MyViewer.ViewImage(self.label_ImageViewer.size()))
        self.update()
        