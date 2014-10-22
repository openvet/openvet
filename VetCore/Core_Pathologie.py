# -*- coding: utf8 -*-
import time
from PyQt4 import QtCore
#from PyQt4.QtGui import *
import Core
from MyGenerics import *
#from Core_Critere import CriteresConsultation

class Pathologies():    #Liste des pathologies d'une consultation
    def __init__(self,idAnimal,idConsultation,parent):
        self.idAnimal=idAnimal
        self.idConsultation=idConsultation
        self.ParentWidget=parent
        self.MyRequest=Request()
        self.GetPathologies()
        
    def GetPathologies(self):
        self.Pathologies=[]
        self.LinePathologies=QString('')
        self.LinePathologies=self.MyRequest.GetString('CALL GetPathologies_line(%i)'%self.idConsultation, 0)
        idPathologies=self.MyRequest.GetLines('CALL GetPathologiesConsult(%i)'%self.idConsultation)
        for index,i in enumerate(idPathologies):
            PathTmp=CPathologie(i[0].toInt()[0],self.ParentWidget)
            PathTmp.ExtendData(index,[i[0],i[2]])
            self.Pathologies.append(PathTmp)
            del PathTmp
    
    def Count(self):
        return len(self.Pathologies)
    
    def GetLine(self):
        inList=QStringList()
        for i in self.Pathologies:
            inList.append(i.listdata[5].toString())
        return inList.join(',')
    
    def Add(self,idPathologie):
        if len([True for i in self.Pathologies if i.listdata[2]==idPathologie])==0:
            PathTmp=CPathologie(0,self.ParentWidget)
            PathTmp.SetNew([0,self.idConsultation,idPathologie,'',False])
            PathTmp.New()
            NomRef=self.MyRequest.GetString('CALL GetPathologie(%i)'%idPathologie,0)
            PathTmp.ExtendData(0,[0,QVariant(NomRef)])
            self.Pathologies.append(PathTmp)
            del PathTmp
        else:
            MyError(self.ParentWidget,u'Cette pathologie est déjà présente dans la sélection')
        return self.GetLine()
    
    def Save(self,lastid):
        for i in self.Pathologies:
            i.listdata[1]=lastid
            i.Update()


class CPathologie(MyModel):                         #classe Pathologie de Consultation
    #idPathologieRef,idConsultation,idPathologie,IdentifiantUQ,isDeleted,NomRérérence
    def __init__(self,idTable=0,parent=None, *args):
#        self.parentwidget=parent
        MyModel.__init__(self,'PathologieRef',idTable,parent, *args)
        self.CriteresConsultation=[]
        
class Pathologie(MyModel):
    #attributes: idPathologie,NomReference,Chronique,DescriptifPublic,isActif,isDeleted
    def __init__(self,idTable,parent=None):
        MyModel.__init__(self,'Pathologie',idTable,parent)

class FormPathologie(MyForm):
    def __init__(self,idPathologie,data,parent):
        MyForm.__init__(self,u'Pathologie',data,parent)
        self.InactivateEnter()
        self.idPathologie=idPathologie
        self.fields[3].setModel(MyComboModel(self.parent,'GetDomaines'))
        self.fields[4].setModel(MyComboModel(self.parent,'GetPathologieDomaines(%i)'%idPathologie))      
        self.fields[5].setModel(MyComboModel(self.parent,'GetPathologieSynonymes(%i)'%idPathologie))
        self.fields[5].model().isEditable=True
        self.AddMenuAction(self.fields[5],'Ajouter',self.AddSynonyme)
        self.fields[6].setModel(MyComboModel(self.parent,'GetPathologieDocuments(%i)'%idPathologie))
        self.OnDocumentSelect(self.fields[6].model().index(0,0))
        self.AddMenuAction(self.fields[6],'Ajouter',self.AddDocument)
        self.connect(self.fields[3],SIGNAL("OnEnter"),self.OnDomainetEnter)
        self.connect(self.fields[6],SIGNAL("clicked (QModelIndex)"),self.OnDocumentSelect)
        self.connect(self.fields[6],SIGNAL("isDeleted(int)"),self.OnDocumentDelete)
        self.connect(self.fields[7],SIGNAL("textEdited(QString)"),self.OnRemarqueEnter)
        
    def OnDomainetEnter(self):  
        self.fields[4].model().NewLine([0,self.fields[3].currentText(),self.fields[3].GetRemarque(),0,0,self.fields[3].Getid(),self.idPathologie,''])
    def AddSynonyme(self):
        self.fields[5].model().NewLine([0,'','',0,False,self.idPathologie,''])
        self.fields[5].edit(self.fields[5].model().index(self.fields[5].model().rowCount()-1))
            
    def AddDocument(self):
        outpath='../Archives/Pathologies/'
        inpath=QFileDialog.getOpenFileName(self,u'Selectionner un document',outpath)
        if not inpath.isEmpty():
            fname=Core.ImportFile(inpath,outpath)
            self.fields[6].model().NewLine([0,fname,'',0,False,outpath,0,self.idPathologie,0,''])            
            self.fields[6].setCurrentIndex(self.fields[6].model().index(self.fields[6].model().rowCount()-1))
            self.fields[7].clear()
            self.OnRemarqueEnter('')
    
    def OnDocumentSelect(self,index):
        if index.isValid():
            self.fields[7].setText(index.model().data(index, Qt.ToolTipRole).toString())
            
    def OnDocumentDelete(self,isdeleted):
        if QMessageBox.question(self,u"Suppression de document",u"Voulez-vous supprimer le document définitivement des archives?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            self.fields[6].model().setData(self.fields[6].currentIndex(),QVariant(1),37)
        else:
            self.fields[6].model().setData(self.fields[6].currentIndex(),QVariant(1),37)
            self.fields[6].model().setData(self.fields[6].currentIndex(),QVariant(0),33)
            
    def OnRemarqueEnter(self,text):
        self.fields[6].model().setData(self.fields[6].currentIndex(),text,Qt.ToolTipRole)

    def OnValid(self):
        if self.mapper.submit():
            self.MyModel.BeginTransaction()
            self.MyModel.Update(self.mapper.currentIndex())
            self.fields[4].model().Update('DomaineRef',[0,6,5,4,7],self)
            self.fields[5].model().Update('PathologieSynonyme',[0,5,1,4,6],self)
            #idPathologieDocument,Document,Remarque,color,isDeletedDoc,5.Path,idDocumentRef,idPathologie,idDeletedRef,9.Identifiant
            self.fields[6].model().UpdateRelational('PathologieDocument',[0,1,5,2,4,8],'DocumentsRef',[6,0,7,4,8],6,8,self)
            self.MyModel.CommitTransaction()
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Cette entré constitue un doublon', QMessageBox.Ok | QMessageBox.Default)                
            
    

class PathologieDomaine:
    def __init__(self,parent=None):
        #attributes: idDomaineRef,Pathologie_idPathologie,PathologieDomaine_idPathologieDomaine,IsPrincipal
        self.Table='DomaineRef'
        self.DBase=parent.DBase
        self.TableFields=self.DBase.GetFields(self.Table)
        for i in self.TableFields:
            self.__dict__.update({i:None})          
        self.NomDomaine=None
        self.Pathologie_idPathologie=parent.idPathologie

    def Print(self):
        print '#attributes: '+','.join(self.TableFields)
        for i in self.TableFields:
            print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
        print 'Nom de domaine : '+self.NomDomaine     
        
    def Set(self,data):
        try:
            self.idDomaineRef=data[0].toInt()[0]
        except:
            self.idDomaineRef=data[0]
        try:
            self.PathologieDomaine_idPathologieDomaine=data[1].toInt()[0]
        except:
            self.PathologieDomaine_idPathologieDomaine=data[1]
        self.NomDomaine=data[2]

    def Save(self):
        #attributes: idDomaineRef,Pathologie_idPathologie,PathologieDomaine_idPathologieDomaine,IsPrincipal
        values=[]
        err=[]
        ToDelete=False
        if self.idDomaineRef>=0:
            values.append('%i'%self.idDomaineRef)
        else:
            values.append('%i'%abs(self.idDomaineRef))
            ToDelete=True
        if self.Pathologie_idPathologie>0:
            values.append('%i'%self.Pathologie_idPathologie)
        else:
            err.append('idPathologie')
        if self.PathologieDomaine_idPathologieDomaine>0:
            values.append('%i'%self.PathologieDomaine_idPathologieDomaine)
        else:
            err.append('idPathologieDomaine')  
        if self.IsPrincipal:
            values.append('TRUE')
        else:
            values.append('False')          
        if ToDelete:
            self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
            return
        if len(err)==0:  
            if self.idDomaineRef==0:
                self.idDomaineRef=self.DBase.DbAdd(self.Table, values,True)
            else:
                self.DBase.DbUpdate(self.Table,self.TableFields,values)      
        else:
            msg='Erreur Save %s: %s'%(self.Table,','.join(err))
            print msg
            return msg   
         
if __name__ == '__main__':
    import Tables
    import config 
    DBase=Tables.DataBase(config.database)
    MyPathologie=Pathologie(DBase)
    MyPathologie.Get(1)
    MyPathologie.Print()
    