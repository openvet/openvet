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
# 8.Remarque        (NULL for prm)
# 
# Model ResultatAnalyseParametre:                         Model ResultatAnalyseImage
# idResultatAnalyse                                       idResultatAnalyse
# parametre                                               Titre
# 2 valeur                                                  Etiquette
# unite                                                   FichierInterne
# NorMin                                                  Remarque
# NorMax                                                  isDirty
# 6 Remarque
# isQuant
# 8 idParametre
# isDirty
#********************************************************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import os
import sys
import hashlib
import config
from DBase import Request
from Viewer import DocViewer

class Analyse(QSqlRelationalTableModel):
    def __init__(self, parent=None, *args):  # parentGui_Consultation
        QSqlTableModel.__init__(self, parent, *args)
        # attributes: idAnalyse,Consultation_idConsultation,TypeAnalyse_idTypeAnalyse,DateHeure,DescriptionAnalyse,Prelevement,SyntheseAnalyse,Conclusions 
        self.idAnalyse = None
        self.idEspece = None
        self.isImage = None
        self.setTable('Analyse')
        self.setRelation(2, QSqlRelation('TypeAnalyse', 'idTypeAnalyse', 'Libele'))
        self.select()
        self.mapper = QDataWidgetMapper(parent)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(parent))
        self.mapper.addMapping(parent.dateTimeEdit_analyse, 3)
        self.mapper.addMapping(parent.lineEdit_description, 4)
        self.mapper.addMapping(parent.lineEdit_prelevement, 5)
        self.mapper.addMapping(parent.plainTextEdit_syntheseanalyse, 6)
        self.mapper.addMapping(parent.plainTextEdit_conclusions, 7)
        parent.comboBox_typeanalyse.setModel(self.relationModel(2))
        parent.comboBox_typeanalyse.setModelColumn(self.relationModel(2).fieldIndex('Libele'))
        self.mapper.addMapping(parent.comboBox_typeanalyse, 2)
        self.Resultats = None
        self.Documents =None
    
    def IsImage(self):
        return Request().GetInt("CALL IsAnalyseImage(%i)" % self.idAnalyse, 0)
    
    def IsQuantitatif(self, TypeAnalyse):
        self.isImage=not Request().GetInt("CALL IsAnalyseParam(\"%s\")" % TypeAnalyse, 0)
        return self.isImage
    
    def GetIdTypeAnalyse(self, TypeAnalyse):
        return Request().GetInt("SELECT idTypeAnalyse FROM TypeAnalyse WHERE Libele=\"%s\"" % TypeAnalyse, 0)
    
    def Get(self, idAnalyse, idConsultation, idEspece):
        self.idAnalyse = idAnalyse
        self.idConsultation = idConsultation
        self.idEspece = idEspece
        if idAnalyse == 0:
            self.setFilter('idAnalyse>0')
            row = self.rowCount()
            self.insertRow(row)
            self.mapper.setCurrentIndex(row)    #Not a valid record for QSQLTable
            self.setData(self.index(row, 0), QVariant(0), Qt.EditRole)
            self.setData(self.index(row, 1), QVariant(self.idConsultation), Qt.EditRole)
            self.setData(self.index(row, 3), QVariant(QDateTime.currentDateTime()), Qt.EditRole)
            self.Resultats = ResultatAnalyseParametre(0)
            self.Documents = ResultatAnalyseImage(0)
        else:
            self.setFilter('idAnalyse=%i' % idAnalyse)
            self.mapper.toFirst()
            self.isImage =self.IsImage()
            self.Resultats = ResultatAnalyseParametre(idAnalyse)
            self.Documents = ResultatAnalyseImage(idAnalyse)  
                
#     def SetResultats(self):
#         self.Resultats = ResultatAnalyseImage(0)  # self.idAnalyse
#         self.Documents = ResultatAnalyseParametre(0)
                        
    def Save(self):
        # TODO:transaction from QSqlDatabase
        valid = QString(u'Analyses sauvegardées')
        self.mapper.submit()
        self.submitAll()
        errAnalyse = self.lastError()
        if not errAnalyse.isValid() or (errAnalyse.isValid() and errAnalyse.text().compare(' No Fields to update') == 0):
            if self.idAnalyse == 0:
                self.idAnalyse = Request().GetInt("SELECT LAST_INSERT_ID()", 0)
            if not self.Resultats is None and self.Resultats.isChanged:
                errResultats = self.Resultats.Save(self.idAnalyse)
                if errResultats.isValid():
                    valid = errResultats.text()
            if not self.Documents is None and self.Documents.isChanged:
                errResultats = self.Documents.Save(self.idAnalyse)
                if errResultats.isValid():
                    valid = errResultats.text()
        else:
            valid = errAnalyse.text()
        return valid
        
class ResultatAnalyseParametre(QAbstractTableModel):
    def __init__(self, idAnalyse, parent=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args)
        self.Myrequest = Request()
        self.listdata = self.Myrequest.GetLines('CALL GetResultatParametres(%i)' % idAnalyse)
        for i in self.listdata:
            i.append(False)  # IsModified to False
        self.Headers = ['id', u'  Paramètre  ', u'Valeur', u'Unité', u'NorMin', u'NorMax']
        self.isChanged = False
        self.CurrentIndex = 0
#        self.idEspece=None
        self.Parametres = None
        self.Modeles=None
        self.Deleted = []
        
    def Print(self,index=0):
        for i in self.listdata[index]:
            try:
                print i.toString()
            except:
                print i   
                 
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata)
    
    def columnCount(self, parent=QModelIndex()):
        return 6
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.Headers[col])
        return QVariant()
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            if index.column() in [2, 4, 5]:
                if self.listdata[index.row()][index.column()].toFloat()[1]:
                    return QVariant('%.2f' % self.listdata[index.row()][index.column()].toFloat()[0])
                else:
                    return QVariant()            
            else:
                return QVariant(self.listdata[index.row()][index.column()])
        elif index.isValid() and role == Qt.TextAlignmentRole:
            if index.column() > 1:
                return QVariant(int(Qt.AlignRight | Qt.AlignCenter))
        elif index.isValid() and role == Qt.ToolTipRole:
            return self.listdata[index.row()][6]
        elif index.isValid() and index.column() == 2 and role == Qt.TextColorRole:
            if not self.listdata[index.row()][7].toBool():
                return QVariant()
            lmax = self.listdata[index.row()][2].toFloat() > self.listdata[index.row()][5].toFloat()
            lmin = self.listdata[index.row()][2].toFloat() < self.listdata[index.row()][4].toFloat()
            if lmax or lmin:
                return QVariant(QColor(Qt.red))
            else:
                return QVariant()
        else: 
            return QVariant()
        
    def flags(self, index):
        if index.isValid() and index.column() == 2:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        else:
            return Qt.ItemIsEnabled
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            self.listdata[index.row()][2] = value.toString()    
            self.listdata[index.row()][9] = True   
            self.isChanged = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return False
    
    def GetRemarque(self, index):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            return self.listdata[index.row()][6].toString()
        return QVariant()
    
    def SetRemarque(self, value):
        self.listdata[self.CurrentIndex.row()][6] = QVariant(value)
        self.listdata[self.CurrentIndex.row()][9] = True
        self.isChanged = True
            
    def isExist(self, parametre):
        for i in self.listdata:
            if i[1] == parametre:
                return True
        return False
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        if self.rowCount()==0:
            return False
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.Deleted.append('%i' % self.listdata[position][0].toInt()[0])
        self.listdata = self.listdata[:position] + self.listdata[position + rows:]
        self.endRemoveRows()
        self.isChanged = True
        return True
    
    def insertRows(self, position, choix, rows=1, index=QModelIndex()):
        valid = True
        newparametre = self.Parametres.GetParametre(choix)
        if not self.isExist(newparametre[1]):
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.listdata.append(newparametre)
            self.endInsertRows()
        else:
            valid = False  
        self.isChanged = True
        return valid
    
    def isEmpty(self):
        empty=True
        for i in range(self.rowCount()):
            try:
                if not self.listdata[i][2].isEmpty():
                    empty=False
            except:
                if not self.listdata[i][2].toString().isEmpty():
                    empty=False
        return empty
            
    def SetModel(self,Parametres):  #idModel
        valid = False
        if self.rowCount()>0:
            self.removeRows(0,self.rowCount())
#        self.Parametres.SetModel(idModel)
        for i in range(Parametres.rowCount()):
            valid = True
            newparametre = Parametres.GetParametre(i)
            if not self.isExist(newparametre[1]):
                self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
                self.listdata.append(newparametre)
                self.endInsertRows()
            else:
                valid = False
        self.isChanged = True
#        self.Parametres.RestoreAll()
        return valid
    
#     def EditModele(self,idModele,Libele):
#         #Make Identifiant
#         listid=['%i'%i[8].toInt()[0] for i in self.listdata]
#         listid.sort()
#         listid.append('%i'%self.Parametres.idEspece)
#         hash=hashlib.md5(''.join(listid)).hexdigest()
#         #Check for existing model
#         self.ModeleCandidat=Request().GetLine('CALL IsModeleExist(\"%s\",\"%s\")' %(hash,Libele))
#         self.ModeleCandidat.append(QString(hash))
#         #Prepare Qestion.Dialog
#         res=[None,None]
#         if self.ModeleCandidat[0].toInt()[0]==3:
#             msg=u'Un modèle \"%s\" avec les mêmes paramètres existe déjà.Voulez-vous le supprimer'%self.ModeleCandidat[3]
#         if self.ModeleCandidat[0].toInt()[0]==0:
#             msg=u'Voulez Vous ajouter le Modéle \"%s\"?'%Libele #TODO: dialog for remarque & priorité
#         if self.ModeleCandidat[0].toInt()[0]==2:
#             msg=u'Voulez Vous ajouter renomer le Modéle \"%s\" en \"%s\"?'%(self.ModeleCandidat[3],Libele)
#             res = Request().GetLines('CALL GetModele(%i)'%self.ModeleCandidat[1].toInt()[0])
#         if self.ModeleCandidat[0].toInt()[0]==1:
#             msg=u'Voulez Vous Modifier la liste de paramètres du Modéle \"%s\"?'%self.ModeleCandidat[3]
#             res = Request().GetLines('CALL GetModele(%i)'%self.ModeleCandidat[1].toInt()[0])
#         self.ModeleCandidat.extend(res)
#         #self.ModeleCandidat=[flag,idModele,idTypeAnalyse,Libele,idEspece,Remarque,Priorite
#         return msg
    
    def SaveModele(self,idModele,Libele):
        Myrequest = Request('ModeleAnalyse') 
        if self.ModeleCandidat[0].toInt()[0]==3:
            Myrequest.Delete([Myrequest.Fields[0].Name, idModele])  #TODO: isAcitve=false if intergrité référentiel perturbée
        if self.ModeleCandidat[0].toInt()[0]==0:
            values=[QVariant(0),QVariant(self.Parametres.idTypeAnalyse),QVariant(Libele),QVariant(self.Parametres.idEspece),None,QVariant(1),QVariant(9),QVariant(QString('tmp'))]
            (err, values) = Myrequest.ValidData(values)
            if len(err) == 0:
                error = Myrequest.Save(values)
                if not error.isValid():
                    lastid=Myrequest.lastID()
                    Myrequest = Request('LigneModeleAnalyse') 
                    for i in self.listdata:
                        values=[QVariant(0),lastid,i[8]]
                        (err, values) = Myrequest.ValidData(values)
                        if len(err) == 0:
                            error = Myrequest.Save(values)
                    Myrequest.lastID()
                    return error
                else:
                    print 'Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err))
                    return QSqlError('','Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err)))   
             
    def SetParametres(self, idTypeAnalyse, idEspece):
        self.Parametres = Parametres(idTypeAnalyse, idEspece)
        self.Modeles=ModelesAnalyse(idTypeAnalyse, idEspece)
    
    def Save(self, idAnalyse): 
        Myrequest = Request('ResultatAnalyse')  
        for i in self.Deleted:
            Myrequest.Delete([Myrequest.Fields[0].Name, i])
        for i in self.listdata:
            if not i[9]:
                continue  # Not modified
            values = [i[0], QVariant(idAnalyse),i[8]]
            if i[2].toFloat()[1]:
                values.extend([i[2], None, None,None,None, i[6]])
            else:
                values.extend([None, i[2], None,None,None,i[6]])
            (err, values) = Myrequest.ValidData(values)
            if len(err) == 0:
                # TODO Myrequest.Save(values,[3,4,9]) if update  
                error = Myrequest.Save(values)
                if not error.isValid():
                    return error
            else:
                print 'Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err))
                return QSqlError('','Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err)))   

        
class ResultatAnalyseImage(QAbstractListModel):
    def __init__(self, idAnalyse, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args) 
        self.Myrequest = Request()
        self.MyViewer=DocViewer()
        self.listdata = self.Myrequest.GetLines('CALL GetResultatImage(%i)' % idAnalyse)
        self.maxiconesize=QSize(128,96)
        self.isChanged = False
        self.CurrentIndex = 0
        self.Deleted = []
                
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            if self.listdata[index.row()][1].toString().isEmpty():
                return QVariant(self.listdata[index.row()][2])
            else:
                return QVariant(self.listdata[index.row()][1])
        elif index.isValid() and role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif index.isValid() and role == Qt.ToolTipRole:
            return QVariant(self.listdata[index.row()][3])
        elif index.isValid() and role == Qt.DecorationRole:
            self.MyViewer.SetFilename('../Archives/%s'%self.listdata[index.row()][2].toString())
            return self.MyViewer.ViewImage(self.maxiconesize)
        else: 
            return QVariant()
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            self.listdata[index.row()][1] = value   
            self.listdata[index.row()][5] = QVariant(True)   
            self.isChanged = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return False
    
    def GetDocument(self,index):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            return [self.listdata[index.row()][1].toString(),self.listdata[index.row()][3].toString()]
            
    def GetRemarque(self, index):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            return self.listdata[index.row()][4].toString()
        return QVariant()
    
    def SetRemarque(self, value):
        self.listdata[self.CurrentIndex.row()][4] = QVariant(value)
        self.listdata[self.CurrentIndex.row()][5] = QVariant(True)
        self.isChanged = True  
          
    def RemoveRow(self, position):
        self.Deleted.append('%i' % self.listdata[position][0].toInt()[0])
        self.listdata = self.listdata[:position] + self.listdata[position + 1:]
        self.removeRow(position)
        self.isChanged = True
    
    def insertRows(self, position, data, rows=1, index=QModelIndex()):
#        hashKey=QImage('../Archives/%s'%data[1]).cacheKey() doesn't work use ImageMagick instead
        doublon=False
        for i in self.listdata:
            if os.system('compare -metric AE ../Archives/%s ../Archives/%s null'%(data[1],i[2].toString()))==0:
                doublon=True
                break
        if doublon:
            os.remove('../Archives/%s'%data[1])
            os.remove('../Archives/%s'%data[2])
        else:
            ligne=[QVariant(0),QVariant(data[0]),QVariant(data[1]),QVariant(data[2]),QVariant(),QVariant(True)]
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.listdata.append(ligne)
            self.endInsertRows()
            self.isChanged=True
        return doublon
    
    def EditImage(self,position):
        pass
    
    def Save(self, idAnalyse): 
        Myrequest = Request('ResultatAnalyse')  
        for i in self.Deleted:
            Myrequest.Delete([Myrequest.Fields[0].Name, i])
        for i in self.listdata:
            if not i[5].toBool():
                continue  # Not modified
            values = [i[0], QVariant(idAnalyse), None,None, None, i[1],i[3],i[2],i[4]]
            (err, values) = Myrequest.ValidData(values)
            if len(err) == 0:
                error = Myrequest.Save(values)
                if not error.isValid():
                    return error
            else:
                print 'Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err))
                return QSqlError('','Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err)))   

       
class Parametres(QSqlQueryModel):
    def __init__(self, idTypeAnalyse, idEspece, parent=None, *args):
        QSqlQueryModel.__init__(self, parent, *args)
        self.RequestAll=QSqlQuery('CALL GetParametres(%i,%i)' % (idTypeAnalyse, idEspece))
        self.idEspece=idEspece
        self.idTypeAnalyse=idTypeAnalyse
        self.setQuery(self.RequestAll)
        
    def SetModel(self,idModel):
        self.setQuery(QSqlQuery('CALL GetModelParametres(%i)' % idModel))
        
    def RestoreAll(self):
        self.setQuery(QSqlQuery(self.RequestAll))
        
    def GetParametre(self, index):
        res = [QVariant(0)]
        for i in [5, -1, 2, 3, 4, -1, 1, 0]:
            if index == -1:
                res.append(QVariant())
            else:
                res.append(self.record(index).value(i))
        res.append(True)
        return res
    
class ModeleAnalyse():
    def __init__(self,Resultat,idModele):
        self.idModele=idModele.toInt()[0]
        self.Resultat=Resultat.listdata
        self.Parametres=Parametres(Resultat.Parametres.idTypeAnalyse, Resultat.Parametres.idEspece)
        # flag,idModele,idTypeAnalyse,Libele,idEspece,Remarque,Priorite
        self.Modele=[None,idModele,self.Parametres.idTypeAnalyse,None,self.Parametres.idEspece,None,2]
        self.ModeleCandidat=None
        self.ToDelete=False
        if idModele>0:
            self.Parametres.SetModel(self.idModele)
            #fill tableview_Parametres with Parametres
            Resultat.SetModel(self.Parametres)
            self.Get()
            
    def Get(self):
        res = Request().GetLine('CALL GetModele(%i)'%self.idModele)
        self.Modele[3]=res[0]   #libele
        self.Modele[5]=res[1]   #remarque
        self.Modele[6]=res[2]   #Priorité
        
    def CheckModele(self,idModele,Libele):
        #Make Identifiant
        listid=['%i'%i[8].toInt()[0] for i in self.Resultat]
        listid.sort()
        listid.append('%i'%self.Parametres.idEspece)
        hash=hashlib.md5(''.join(listid)).hexdigest()
        #Check for existing model
        #self.ModeleCandidat=[flag,idident,idLibele,ExistingLibele,identifiant,NewLibele
        self.ModeleCandidat=Request().GetLine('CALL IsModeleExist(\"%s\",\"%s\")' %(hash,Libele))
        self.ModeleCandidat.append(QString(hash))
        self.ModeleCandidat.append(Libele)
        #Prepare Qestion.Dialog
        if self.ModeleCandidat[0].toInt()[0]==3:
            msg=u'Un modèle \"%s\" avec les mêmes paramètres existe déjà.Voulez-vous le supprimer ou le modifier?'%self.ModeleCandidat[3]
        if self.ModeleCandidat[0].toInt()[0]==0:
            msg=u'Voulez Vous ajouter le Modéle \"%s\"?'%Libele
        if self.ModeleCandidat[0].toInt()[0]==2:
            msg=u'Voulez Vous ajouter renomer le Modéle \"%s\" en \"%s\"?'%(self.ModeleCandidat[3],Libele)
        if self.ModeleCandidat[0].toInt()[0]==1:
            msg=u'Voulez Vous Modifier la liste de paramètres du Modéle \"%s\"?'%self.ModeleCandidat[3]
        self.EditModele()
        return (self.ModeleCandidat[0].toInt()[0],msg)
    
    def EditModele(self):
        if self.ModeleCandidat[0].toInt()[0]==2:        #renomme le modèle
            res = Request().GetLine('CALL GetModele(%i)'%self.ModeleCandidat[1].toInt()[0])
            self.Modele[3]=self.ModeleCandidat[5]   #newlibele
            self.Modele[5]=res[1]   #remarque
            self.Modele[6]=res[2]   #Priorité
                       
        if self.ModeleCandidat[0].toInt()[0]==1:        #change liste des parametres
            res = Request().GetLine('CALL GetModele(%i)'%self.ModeleCandidat[2].toInt()[0])
            self.Modele[3]=res[0]   #libele
            self.Modele[5]=res[1]   #remarque
            self.Modele[6]=res[2]   #Priorité
            self.Parametres=[[i[8],None,None,None,None,i[1]]for i in self.Resultat]                
            
        if self.ModeleCandidat[0].toInt()[0]==0:        #nouveau modèle
            self.Modele[3]=self.ModeleCandidat[5]       #newlibele
            self.Modele[5]=QString('')                  #remarque
            self.Modele[6]=QVariant(2)                  #Priorité
            self.Parametres=[[i[8],None,None,None,None,i[1]]for i in self.Resultat]
                  
class ModelesAnalyse(QAbstractListModel): 
    def __init__(self, idTypeAnalyse, idEspece, isAucun=True,parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args) 
        #idModele,Libele,Remarque,Priorite
        res = Request().GetLines('CALL GetModeles(%i,%i)' %(idTypeAnalyse,idEspece))#order by priorite
        if isAucun:
            self.listdata=[[QVariant(0),QString('Aucun'),QVariant(),QVariant(0)]]
            self.listdata.extend(res)
        else:
            self.listdata=res
        self.selection=None
        self.indexSelection=None
                
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()][1])
        elif index.isValid() and role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif index.isValid() and role == Qt.ToolTipRole:
            return QVariant(self.listdata[index.row()][2])
        elif index.isValid() and role == Qt.TextColorRole:
            if self.listdata[index.row()][0]==self.selection:
                self.indexSelection=index
                return QVariant(QColor(Qt.red))
        else: 
            return QVariant()
#TODO: Get index for selection       
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.row() < self.rowCount():
#            self.CurrentIndex = index
            self.listdata[index.row()][3] = QVariant(value)   
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return False
                          
class Analyses(QAbstractListModel): 
    def __init__(self, idAnimal, parent=None, *args): 
        QAbstractListModel.__init__(self, parent, *args) 
        self.Myrequest = Request()
        self.listdata = self.Myrequest.GetLines('CALL GetAnalysesAnimal(%i)' % idAnimal)
 
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()][1])
        elif index.isValid() and role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif index.isValid() and role == Qt.ToolTipRole:
            return QVariant(self.listdata[index.row()][3])
        else: 
            return QVariant()
        
#For debbug purpose only
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
