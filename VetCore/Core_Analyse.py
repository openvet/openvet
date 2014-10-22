#!/usr/bin/env python
# -*- coding: utf8 -*-
#******************************************************************************************************************
# Table: ResultatAnalyse
# fields:
# 0.idResultatAnalyse
#   Analyse_idAnalyse
#   Parametre_id    (NULL for doc)
#   ValeurQuant     (NULL for doc)
#   ValeurQual      (NULL for doc)
# 5.TitreDocument   (NULL for prm)
#   FichierExterne  (NULL for prm)
#   Etiquette       (NULL for prm)
# 8.Remarque        
# 9.isDeleted
# 
# Model ResultatAnalyseImage
# idResultatAnalyse
# Titre
# Etiquette
# FichierInterne
# Remarque
# isDirty
#********************************************************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import os
import sys
import hashlib
import config
import subprocess
from DBase import Request
from Viewer import DocViewer
from MyGenerics import *
import Mywidgets
from PyQt4.QtGui import *



class FormParametre(MyForm):
    def __init__(self,idparametre,data,parent):
        MyForm.__init__(self,u'Paramètre d\'analyse',data,parent)
        self.parent=parent
        self.InactivateEnter()
        self.idparametre=idparametre
        self.fields[2].setTristate(False)
        self.fields[3].setModel(MyComboModel(self.parent,'GetAllUnites()'))
        self.EditButtons[0].clicked.connect(self.OnEditUnite)
        self.connect(self.fields[2],SIGNAL("stateChanged(int)"),self.OnQuantitatif)
        
    def OnEditUnite(self):
        idUnite=self.fields[3].Getid()
        new=[0,'',False,True,False,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Concentration',2]]
        form=MyForm('Unités',data,self)
        form.SetModel(UniteModel,{0:1,1:2})    #GUI_field : DB_Field
        if form.exec_():
            self.fields[3].setModel(MyComboModel(self.parent,'GetUnites()'))
            self.fields[3].Setid(idUnite)
            
    def OnQuantitatif(self,state):
        state=state!=0
        for i in range(3,6):
            self.fields[i].setVisible(state)
            self.labels[i].setVisible(state)
        self.EditButtons[0].setVisible(state)
            

class FormModeleAnalyse(MyForm):
    def __init__(self,data,parent):
        MyForm.__init__(self,u'Modèle d\'analyse',data,parent)
        self.parent=parent
        self.InactivateEnter()
#        self.fields[1].setModel(MyComboModel(self.parent,'GetAllUnites()'))


class ModelViewParameters(MyTableModel):
    def __init__(self, parent,nbHeaders,request,cols=None, *args): 
        MyTableModel.__init__(self, parent,nbHeaders,request,cols=None, *args)

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not index.row() < self.rowCount():
            return False
        value=QVariant(value)
        if role == Qt.EditRole:
            self.listdata[index.row()][index.column()+1]=value
            if self.data(index,34):
                if value.toFloat()<self.listdata[index.row()][4].toFloat() or value.toFloat()>self.listdata[index.row()][5].toFloat():
                    self.listdata[index.row()][self.NbCols+2]=QVariant(7)
                else:
                    self.listdata[index.row()][self.NbCols+2]=QVariant(0)
        elif role == Qt.UserRole:
            self.listdata[index.row()][0]=value
        elif role == Qt.ToolTipRole:
            self.listdata[index.row()][self.NbCols+1]=value
        elif role == Qt.ForegroundRole:
            self.listdata[index.row()][self.NbCols+2]=value
        elif role == 33:    #isDeleted
            self.listdata[index.row()][self.NbCols+3]=value
        elif role > 33:    #UserProperty
            self.listdata[index.row()][self.NbCols+3+role-33]=value
        else: 
            return False
        if role!=33:
            self.dirty = True
            self.SignId(index)
        else:
            self.SignId(index,False)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index,index)
        return True

    def InsertModelAnalyse(self,idModelAnalyse,idAnalyse):
        data=self.Myrequest.GetTableList(5,'CALL GetModelParametres(%i)'%idModelAnalyse)
        for i in data:
            i.extend([QVariant(idAnalyse),QVariant()])
            self.insertRows( self.rowCount(), i, rows=1, index=QModelIndex())
            
    def SetIdAnalyse(self,idAnalyse):
        for i in self.listdata:
            i[11]=QVariant(idAnalyse)
            
    def GetListParameters(self):
        Mylist=[]
        for i in self.listdata:    
            Mylist.append([i[0],i[1],"",QVariant(0),QVariant(0)])
        return Mylist
    
    def Update(self,table,maplist,parent,idindex=0,delindex=4):
        if not self.dirty:
                return
        for i in self.listdata:
            id=i[idindex].toInt()[0]
            if id<=0 and not i[delindex].toBool():
                if i[9].toBool():
                    i[3]=QVariant()       #Valeur Qualitative=NULL
                else:
                    i[2]=QVariant()      #Valeur Quantitative=NULL
                self.EditItem(i,table,maplist,idindex,delindex,parent)
            elif i[delindex].toBool() and id!=0:
                self.DeleteItem(table,abs(id),parent)

class ModelViewImages(MyComboModel):
    def __init__(self, parent,routine,*args): 
        MyComboModel.__init__(self, parent,routine)
        self.MyViewer=DocViewer()
        self.maxiconesize=QSize(128,96)
        
    def data(self, index, role): 
        if not index.isValid():
            return
        if role == Qt.DisplayRole and not self.listdata[index.row()][4].toBool():
            return QVariant(self.listdata[index.row()][1])
        elif role == Qt.UserRole and not self.listdata[index.row()][4].toBool():
            return QVariant(self.listdata[index.row()][0])
        elif role == Qt.ToolTipRole and not self.listdata[index.row()][4].toBool():
            return QVariant(self.listdata[index.row()][2])
        elif role == Qt.DecorationRole and not self.listdata[index.row()][4].toBool():
            self.MyViewer.SetFilename(config.Path_Analyses+'%s'%self.listdata[index.row()][3].toString())
            return self.MyViewer.ViewImage(self.maxiconesize)
        elif role == 33:    #isDeleted
            return QVariant(self.listdata[index.row()][4])
        elif role > 33:    #UserProperty
            return QVariant(self.listdata[index.row()][4+role-33])
        return QVariant()
    
    def GetDocument(self,index):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            return [self.listdata[index.row()][1],self.listdata[index.row()][5].toString()]

    def isDoublon(self,fileLabel,fileExt):
        for i in self.listdata:
            #os.system('compare -metric MAE -fuzz 10%% %s%s %s%s null'%(config.Path_Analyses,i[3].toString(),config.Path_Analyses,fileLabel))==0 Too slow
            result = subprocess.Popen(['identify','-quiet','-format','%#\n',config.Path_Analyses+i[3].toString(),config.Path_Analyses+fileLabel],stdout=subprocess.PIPE).communicate()[0]
            if result[65:-2]==result[:64]:
                os.remove('%s%s'%(config.Path_Analyses,fileLabel))
                os.remove('%s%s'%(config.Path_Analyses,fileExt))
                return True
        return False
    
    def SetIdAnalyse(self,idAnalyse):
        for i in self.listdata:
            i[6]=QVariant(idAnalyse)
    
    def Update(self,table,maplist,parent,idindex=0,delindex=4):
        if not self.dirty:
                return
        for i in self.listdata:
            id=i[idindex].toInt()[0]
            if id<=0 and not i[delindex].toBool():
                self.EditItem(i,table,maplist,idindex,delindex,parent)
            elif i[delindex].toBool() and id!=0:
                self.DeleteItem(table,abs(id),parent)
                os.remove('%s%s'%(config.Path_Analyses,i[3].toString()))
                os.remove('%s%s'%(config.Path_Analyses,i[5].toString()))

class Analyse(QSqlTableModel):  #TODO: dériver de MyGenerics.MyModel?
    def __init__(self, parent=None, *args):  # parentGui_Consultation
        QSqlTableModel.__init__(self, parent, *args)
        # attributes: idAnalyse,Consultation_idConsultation,TypeAnalyse_idTypeAnalyse,DateHeure,DescriptionAnalyse,Prelevement,SyntheseAnalyse,Conclusions
        self.parent=parent 
        self.idAnalyse = None
        self.idEspece = None
        self.idModeleAnalyse=None
        self.isImage = None
        self.setTable('Analyse')   
        self.select()
        self.mapper = QDataWidgetMapper(parent)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self)
        self.mapper.setItemDelegate(TypeAnalyseDeleguate(parent))
        self.mapper.addMapping(parent.dateTimeEdit_analyse, 3)
        self.mapper.addMapping(parent.lineEdit_description, 4)
        self.mapper.addMapping(parent.lineEdit_prelevement, 5)
        self.mapper.addMapping(parent.plainTextEdit_syntheseanalyse, 6)
        self.mapper.addMapping(parent.plainTextEdit_conclusions, 7)
        self.mapper.addMapping(parent.comboBox_typeanalyse, 2)
        self.MyRequest=Request('Analyse')
    
    def IsImage(self):
        self.isImage=Request().GetInt("CALL IsAnalyseImage(%i)" % self.idAnalyse, 0)
        return self.isImage
    
    def Get(self, idAnalyse, idConsultation, idEspece):
        self.idAnalyse = idAnalyse
        self.idConsultation = idConsultation
        self.idEspece = idEspece
        if idAnalyse == 0:
            self.setFilter('idAnalyse>0')
            row = self.rowCount()
            self.insertRow(row)
            self.mapper.setCurrentIndex(row)
            self.setData(self.index(row, 0), QVariant(0), Qt.EditRole)
            self.setData(self.index(row, 1), QVariant(self.idConsultation), Qt.EditRole)
            self.setData(self.index(row, 3), QVariant(QDateTime.currentDateTime()), Qt.EditRole)
        else:
            self.setFilter('idAnalyse=%i' % idAnalyse)
            self.mapper.toFirst()
            self.isImage =self.IsImage()
                        
    def Delete(self,parent,idAnalyse):
        return self.MyRequest.Execute('CALL SoftDeleteItemTable(%i,\"Analyse\")'%idAnalyse)
        
    def Save(self):
        valid = None
        self.mapper.submit()
        self.MyRequest.driver().beginTransaction()
        self.submitAll()
        errAnalyse = self.lastError()
        if not errAnalyse.isValid() or (errAnalyse.isValid() and errAnalyse.text().compare(' No Fields to update') == 0):
            if self.idAnalyse == 0:
                self.idAnalyse = Request().GetInt("SELECT LAST_INSERT_ID()", 0)            
            if not self.parent.tableView_Parametres.model() is None:
                self.parent.tableView_Parametres.model().SetIdAnalyse(self.idAnalyse)
                self.parent.tableView_Parametres.model().Update('ResultatAnalyse',[0,11,10,2,2,12,12,12,6,8],self.parent,0,8)
                if self.parent.tableView_Parametres.model().MyRequest.lastError().isValid():
                    valid=self.parent.tableView_Parametres.model().MyRequest.lastError().text()
            if not self.parent.listView_AnalyseImage.model()is None:
                self.parent.listView_AnalyseImage.model().SetIdAnalyse(self.idAnalyse)    
                self.parent.listView_AnalyseImage.model().Update('ResultatAnalyse',[0,6,7,7,7,1,5,3,2,4],self.parent,0,4)
                if self.parent.listView_AnalyseImage.model().MyRequest.lastError().isValid():
                    valid=self.parent.listView_AnalyseImage.model().MyRequest.lastError().text()
            if not self.idModeleAnalyse is None:
                self.MyRequest.SetTable('ModeleAnalyse')
                self.MyRequest.Update(['idModeleAnalyse','LastSelection'],['%i'%self.idModeleAnalyse,'\"%s"'%QDate.currentDate().toString('yyyy-MM-dd')])
                if self.MyRequest.lastError().isValid():
                    valid=self.MyRequest.lastError().text()
        else:
            valid = errAnalyse.text()
        if valid is None:
            valid=QString(u'Analyses sauvegardées')
            self.MyRequest.driver().commitTransaction ()
        else:
            self.MyRequest.driver().rollbackTransaction ()
        return valid   


class TypeAnalyseDeleguate(QItemDelegate):   
    def setEditorData(self,editor,index):
        if type(editor)==Mywidgets.MyComboBox:
            value = index.model().data(index, Qt.DisplayRole)
            if not value.isNull():
                comboindex=editor.model().GetIndex(value)
            else:
                comboindex=0
            editor.setCurrentIndex(comboindex)
        elif type(editor)==QDateTimeEdit:
            value = index.model().data(index, Qt.DisplayRole).toDateTime()
            editor.setDateTime(value)
        else:
            value=index.model().data(index,Qt.DisplayRole).toString()
            editor.setText(value)
             
    def setModelData(self,editor,model,index):
#        print type(editor)
        if type(editor)==Mywidgets.MyComboBox:
            model.setData(index, QVariant(editor.Getid()))
        elif type(editor)==QDateTimeEdit:    
            model.setData(index,QVariant(editor.dateTime()))
        elif type(editor)==MyPlainTextEdit:
            model.setData(index,editor.toPlainText())
        else:
            model.setData(index,editor.text())
 
        
#debug only        
def Print(self,List,index=0):
    for i in List[index]:
        try:
            print i.toString()
        except:
            print i  
             
if __name__ == '__main__':
    db = QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName (config.host)
    db.setUserName (config.user)
    db.setPassword (config.password)
    db.setDatabaseName(config.database)
    if not db.open():
        print 'connection impossible'
    MyAnalyse = Analyse(db, 'Analyse')
    MyAnalyse.Print()
