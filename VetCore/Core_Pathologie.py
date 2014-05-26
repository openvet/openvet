# -*- coding: utf8 -*-
import time
from PyQt4 import QtCore
#from PyQt4.QtGui import *
#from Core_Critere import CriteresConsultation

class Pathologie:
    def __init__(self,DBase):
        #attributes: idPathologie,NomReference,Chronique,DescriptifPublic
        self.Table='Pathologie'
        self.DBase=DBase
        self.TableFields=self.DBase.GetFields(self.Table)
        for i in self.TableFields:
            self.__dict__.update({i:None})          
        self.Domaines=[]
        self.Synonymes=[]
        self.CriteresConsultation=[]
        self.idEspece=None     

    def Print(self):
        print '#attributes: '+','.join(self.TableFields)
        for i in self.TableFields:
            print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
        print 'Synonymes :'
        for i in self.Synonymes:
            print i
        print 'Domaines :'
        for i in self.Domaines:
            print i.Print()

    def SetEspece(self,IdEspece):
        self.idEspece=IdEspece
        
    def GetDomaines(self):
        return self.DBase.GetDbidText("CALL GetDomaines()",'Tous')
    
    def GetPathologies(self,idPathologieDomaine,defaut=None):
        return self.DBase.GetDbidText("CALL SelectPathologies(%i,%i)"%(self.idEspece,idPathologieDomaine),defaut)

    def GetDefinitionPathologie(self,idPathologie):
        res=self.DBase.GetDbText("SELECT DescriptifPublic FROM Pathologie WHERE idPathologie=%i"%idPathologie)
        if len(res):
            return self.DBase.GetDbText("SELECT DescriptifPublic FROM Pathologie WHERE idPathologie=%i"%idPathologie)[0]
    
    def Get(self,idPathologie):
        self.idPathologie=idPathologie
        res=self.DBase.GetDbText("CALL GetPathologie(%i)"%idPathologie)
        self.NomReference=res[0]
        self.Chronique=(res[1].toInt()[0]==1)
        self.DescriptifPublic=res[2]
        self.Synonymes=self.DBase.GetDbidText("SELECT idPathologieSynonyme,Synonyme FROM PathologieSynonyme WHERE Pathologie_idPathologie=%i"%idPathologie)
        res=self.DBase.GetDbLines("CALL GetDomaine_id(%i)"%self.idPathologie)
        self.Domaines=[]
        for i in res:
            self.AddDomaine(i)     
                                 
    def AddDomaine(self,data):
        #data: idDomaineRef,PathologieDomaine_idPathologieDomaine,NomDomaine
        tmp=PathologieDomaine(self)
        tmp.Set(data)
        self.Domaines.append(tmp)
        del tmp
          
    def DeleteDomaine (self,idDomaineRef):
        for i in self.Domaines:
            if i.idDomaineRef==idDomaineRef:
                i.idDomaineRef=-idDomaineRef
                return
        print 'idDomaineRef non trouvé.'
        return -1
    
    def SaveDomaine(self,domaine):
        pass
    #TODO:
                              
    def GetExamens(self):    
        return self.DBase.GetDbidText("CALL GetExamens(%i)"%self.idPathologie)
    
    def GetCriteres(self,idExamen):
        return self.DBase.GetDbidText("CALL GetCriteres(%i,%i)"%(self.idPathologie,idExamen))
    
    def GetDocuments(self):
        return self.DBase.GetDbText("CALL GetPathologieDocuments(%i)"%self.idPathologie)
    
    #TODO GetTraitements
    
    def CheckDoublon(self,nom):
        if len(self.DBase.GetDbidText("CALL CheckDoublonPathologie(\"%s\")"%nom))==0:
            return False
        else:
            return True
    
    def CheckUsed(self):
        res=self.DBase.GetDbText("CALL CheckUsedPathologie(%i)"%self.idPathologie)
        return(res[0].toInt()[0],res[1].toInt()[0])
                
    def Save(self):
        #idPathologie,NomReference,Chronique,DescriptifPublic
        #synonymes
        values=[]
        err=[]
        ToDelete=False
        if self.idPathologie>=0:
            values.append('%i'%self.idPathologie)
        else:
            values.append('%i'%abs(self.idPathologie))
            ToDelete=True
        if self.NomReference.size()<=60:
            values.append('\"%s\"'%self.NomReference)
        else:
            err.append(u'Nom de référence trop long')
        if self.Chronique:
            values.append('TRUE')
        else:
            values.append('FALSE')
        if self.DescriptifPublic.size()<=65536:
            values.append('\"%s\"'%self.DescriptifPublic)
        else:
            err.append(u'Descriptif trop long')
        if ToDelete:
            self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
            return
        if len(err)==0:  
            #TODO BeginTrans & vérifier que enregistrement édité n'ont pas été supprimés?
            if self.idPathologie==0:
                self.idPathologie=self.DBase.DbAdd(self.Table, values,True)
                self.DBase.DbAdd('PathologieEspece',['0','%i'%self.idPathologie,'%i'% self.idEspece])                  

            else:
                self.DBase.DbUpdate(self.Table,self.TableFields,values)
            for i in self.Synonymes:
                if i[0]<0:
                    self.DBase.DbDelete("PathologieSynonyme",['idPathologieSynonyme','%i'%abs(i[0])])
                if i[0]==0:
                    self.DBase.DbAdd("PathologieSynonyme",['0','%i'%self.idPathologie,'\"%s\"'%i[1]])
                if i[0]>0:
                    self.DBase.DbUpdate("PathologieSynonyme",['idPathologieSynonyme','Synonyme'],['%i'%i[0],'\"%s\"'%i[1]])
            for i in self.Domaines:
                i.Pathologie_idPathologie=self.idPathologie
                i.Save()
            #TODO Commit         
        else:
            msg='Erreur Save %s: %s'%(self.Table,','.join(err))
            print msg
            return msg    

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
#     MyPathologie.DescriptifPublic.append(QtCore.QString(u'Et Voilà'))
#     MyPathologie.Synonymes.append([0,QtCore.QString(u'Eléboïte')])
#     MyPathologie.Print()
#     MyPathologie.Save()
    