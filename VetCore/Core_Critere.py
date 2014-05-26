# -*- coding: utf8 -*-
import time
#import Core
from PyQt4 import QtCore

class Critere:                  #TODO: dériver d'une classe DataBase ou class abstraite? 
    def __init__(self,DBase):      
        self.Table='Critere'
        self.DBase=DBase
        self.TableFields=self.DBase.GetFields(self.Table)
        #attributes: idCritere,Examen_idExamen,Critere,Unite_idUnite,NbGrades,Remarque
        for i in self.TableFields:
            self.__dict__.update({i:None})
        self.Pathologie_idPathologie=None
        self.CritereGrades=[]             
        
    def Print(self):
        print '#attributes: '+','.join(self.TableFields)
        for i in self.TableFields:
            print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
        for i in self.CritereGrades:
                i.Print()
    
    def Get(self,idCritere):
        self.idCritere=idCritere
        res=self.DBase.GetDbText("CALL GetCritere(%i)"%idCritere)
        self.Examen_idExamen=res[1].toInt()[0]
        self.Critere=res[2]
        self.Unite_idUnite=res[3]
        self.NbGrades=res[4]
        self.Remarque=res[5]
        self.Pathologie_idPathologie=res[6].toInt()[0]
        #Get Grades
        res=self.DBase.GetDbLines("CALL GetCritereGrades(%i)"%idCritere)
        self.CritereGrades=[]
        for i in res:
#            print i
            i[0]=i[0].toInt()[0]
            tmp=CritereGrade(self)
            tmp.Set(i)
            self.CritereGrades.append(tmp)
        return res     
      
    def Set(self,data,idPathologie):
        for i,value in zip(self.TableFields,data):
            self.__dict__.update({i:value})
        self.Pathologie_idPathologie=idPathologie
            
    def GetUnite(self):
        return self.DBase.GetDbidText('SELECT * FROM Unite ORDER By Unite')
    
    def GetIndexGrade(self,idCritereSeuil):
        for i,j in zip(self.CritereGrades,range(len(self.CritereGrades))):
            if i.idCritereSeuil==idCritereSeuil:
                return j
    
    def IsUsed(self):
        return len(self.DBase.GetDbLines('SELECT PathologieRef_idPathologieRef FROM ConsultationCritere WHERE Critere_idCritere=%i'%self.idCritere))
              
    def UpdateGrade(self,data):
        if data[0]>0:
            index=self.CritereGrades[self.GetIndexGrade(data[0])]
            index.Critere_idCritere=self.idCritere
            index.LimiteInf=data[1]
            index.LimiteSup=data[2]
            index.Grade=data[3]
            index.Score=data[4]
        else:
            Ndata=[data[0],self.idCritere]
            Ndata.extend(data[1:])
            tmp=CritereGrade(self)
            tmp.Set(Ndata)
            self.CritereGrades.append(tmp)
              
    def Save(self):
        err=[]
        values=[]
        ToDelete=False
        if self.idCritere<0:
            ToDelete=True
        values.append('%i'%abs(self.idCritere))
        values.append('%i'%self.Examen_idExamen)
        if self.Critere.size()<=60:
            values.append(u'\"%s\"'%self.Critere)
        else:
            err.append(u'Nom du Critère trop long')
        if self.Unite_idUnite.isEmpty():
            values.append('NULL')
        else:
            res=self.DBase.GetDbidText('SELECT * From Unite WHERE idUnite=%i'%self.Unite_idUnite.toInt()[0])
            if len(res):
                values.append('%i'%res[0][0])
            else:
                err.append(u'Unité absente de la table Unite')
        if self.NbGrades.toInt()[1]:
            values.append('%i'%self.NbGrades.toInt()[0])
        else:
            values.append('NULL')
        if not self.Remarque.isEmpty():
            if self.Remarque.size()<=65536:
                values.append('\"%s\"'%self.Remarque.toUtf8().data())
            else:
                err.append(' Remarque trop longue')   
        else:
            values.append('NULL')
        if len(err)==0:
            if ToDelete:
                self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
                return
            if self.idCritere==0:
                #fields=['idCritere','Examen_idExamen','Critere','Unite_idUnite','NbGrades','Remarque']
                self.idCritere=self.DBase.DbAddLinked([self.Table,'CritereRef'], [values,['0','%i'%self.Pathologie_idPathologie,'(SELECT LAST_INSERT_ID())']])
            else:
                Nvalues=[values[0]]
                Nvalues.extend(values[2:])
                fields=[self.TableFields[0]]
                fields.extend(self.TableFields[2:])
                #'idCritere','Critere','Unite_idUnite','NbGrades','Remarque'
                self.DBase.DbUpdate(self.Table,fields,Nvalues)
            for i in self.CritereGrades:
                i.Critere_idCritere=self.idCritere
                i.Save()
            return self.idCritere   
        else:
            msg='Erreur Save Critere :%s'%','.join(err)
            print msg
            return msg
                
#     def SaveGrades(self):
#         for i in self.CritereGrades:
#             i.Critere_idCritere=self.idCritere
#             i.Save()

class CritereGrade:
    def __init__(self, parent=None):
        self.DBase=parent.DBase
        self.Table='CritereSeuil'
        self.TableFields=self.DBase.GetFields(self.Table)
        #attributes: idCritereSeuil,Critere_idCritere,LimiteInf,LimiteSup,Grade,Score
        for i in self.TableFields:
            self.__dict__.update({i:None}) 
            
        self.Critere_idCritere=parent.idCritere
          
    def Print(self):
        print 'attributes: '+','.join(self.TableFields)
        for i in self.TableFields:
            print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))    
             
    def Get(self,grade):
        res=self.DBase.GetDbText("CALL GetSeuil(%i,%i)"%(self.Critere_idCritere,grade))
        self.idCritereSeuil=res[0].toInt()[0]
        self.LimiteInf=res[1]
        self.LimiteSup=res[2]
        self.Grade=QtCore.QString('%i'%grade)
        self.Score=QtCore.QString(res[3])
#        self.Remarque=QtCore.QString(res[4])    TODO add Remarque in fields of GetSeuil
        return res
    
    def Set(self,data):
        for i,value in zip(self.TableFields,data):
            self.__dict__.update({i:value})
               
    def CheckDoublon(self):
        return self.DBase.RechercheSQL_id('CALL CheckDoublonCritere(%i,%i)'%(self.Critere_idCritere,self.Grade.toInt()[0]))>0
                
    def Save(self):
        err=[]
        values=[]
        ToDelete=False
        if self.idCritereSeuil<0:
            ToDelete=True
        values.append('%i'%abs(self.idCritereSeuil))
        values.append('%i'%self.Critere_idCritere)
        if self.LimiteInf.toFloat()[1]:
            values.append('%.2f'%self.LimiteInf.toFloat()[0])
        else:
            values.append('NULL')
        if self.LimiteSup.toFloat()[1]:
            values.append('%.2f'%self.LimiteSup.toFloat()[0])
        else:
            values.append('NULL')
        if ' '.join(values[-2:])=='NULL NULL':
            err.append('Erreur Seuils')
        if self.Grade.toInt()[1]:
            values.append('%i'%self.Grade.toInt()[0])
        else:
            err.append('Erreur de Grade')
        if self.Score.isEmpty():
            values.append('NULL')
        else:
            values.append('\"%s\"'%self.Score)
        if self.Score.size()>45:
            err.append('Erreur de Score trop long')
        # for field Remarque
        values.append('NULL')
        if len(err)==0:
            if ToDelete:
                self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
                return
            if self.idCritereSeuil==0:
                #idCritereSeuil,Critere_idCritere,LimiteInf,LimiteSup,Grade,Score,Remarque
                if not self.CheckDoublon():
                    print self.DBase.DbAdd('CritereSeuil',values)
            else:
    
                Nvalues=[]
                fields=[]
                for i in [0,2,3,5]:
                    Nvalues.append(values[i])
                    fields.append(self.TableFields[i])
                #'idCritereSeuil','LimiteInf','LimiteSup','Score'
                self.DBase.DbUpdate('CritereSeuil',fields,Nvalues)  
        else:
            msg='Erreur Save CritereSeuil :%s'%','.join(err)
            print msg
            return msg

class CriteresConsultation:
    def __init__(self,idPathologie, parent=None):   #parent is Consultation
        self.DBase=parent.DBase
        self.Table='PathologieRef'
        self.TableFields=self.DBase.GetFields(self.Table)
        #attributes: idPathologieRef,Consultation_idConsultation,Pathologie_idPathologie
        for i in self.TableFields:
            self.__dict__.update({i:None}) 
        self.Consultation_idConsultation=parent.idConsultation    
        self.Pathologie_idPathologie=idPathologie
        res=self.DBase.GetDbText("CALL GetPathologieDomaine(%i)"%idPathologie)
        self.idDomainePathologie=res[0].toInt()[0]
        self.DomainePathologie=res[1]
        self.Pathologie_NomReference=res[2]
        self.idPathologieRef=0
        if self.Consultation_idConsultation > 0:
            res=self.DBase.RechercheSQL_id("CALL GetPathologieRef(%i,%i)"%(self.Consultation_idConsultation,self.Pathologie_idPathologie))
            if not res is None:
                self.idPathologieRef=res
        self.Criteres=[]
        
    def Print(self):
        print '#attributes: '+','.join(self.TableFields)
        for i in self.TableFields:
            print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
        for i in self.Criteres:
            i.Print() 
               
    def Get(self):
        res=self.DBase.GetDbLines("CALL GetCriteresConsult(%i,%i)"%(self.Consultation_idConsultation,self.Pathologie_idPathologie))
        self.Criteres=[]
        for i in res:
            tmp=CritereConsultation(self)
            data=[i[0].toInt()[0],i[1].toInt()[0],self.idPathologieRef]
            if i[4].toFloat()[1]:
                data.extend([QtCore.QString(i[4]),QtCore.QString('')])
            else:
                data.extend([QtCore.QString(''),QtCore.QString(i[4])])
            data.append(QtCore.QString(i[7]))
            tmp.Set(data)
            self.Criteres.append(tmp)
        return res
    
    def Set(self,data):
        for i,value in zip(self.TableFields,data):
            self.__dict__.update({i:value})
            
    def Save(self, idConsultation=None):
        #Save return ([fields],[values])->list->DBase.MultiEdit(list)
        #idPathologieRef,Consultation_idConsultation,Pathologie_idPathologie
        err=[]
        values=[]
        ToDelete=False
        if not idConsultation is None:
            self.Consultation_idConsultation=idConsultation
        if self.idPathologieRef<0:
            ToDelete=True
        values.append('%i'%abs(self.idPathologieRef))           
        if self.Consultation_idConsultation>0:
            values.append('%i'%self.Consultation_idConsultation)
        else:
            err.append('idConsultation')
        if self.Pathologie_idPathologie>0:
            values.append('%i'%self.Pathologie_idPathologie)
        else:
            err.append('idPathologie')
        values.append('NULL')
        if ToDelete:
            self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
            return
        if len(err)==0:
            if ToDelete:
                self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
            elif self.idPathologieRef==0:
                self.idPathologieRef=self.DBase.DbAdd( self.Table, values,True)
            else:
                fields=['idPathologieRef','Pathologie_idPathologie']
                Nvalues=[values[0],values[2]]
                self.DBase.DbUpdate(self.Table,fields,Nvalues)
                #Delete old criteres if exist       
            for i in self.Criteres:
                i.Save(self.idPathologieRef)
        else:
            msg='Erreur Save %s: %s'%(self.Table,','.join(err))
            print msg
            return msg
    
    def New(self,idCritere):  #old GetNewCritere
        res=self.DBase.GetDbText("CALL GetNewConsultationCritere(%i)"%idCritere)
#         tmp=CritereConsultation(self)
#         data=[0,idCritere,self.idPathologieRef]
#         data.extend([QtCore.QString('')]*3)
#         tmp.Set(data)
#         self.Criteres.append(tmp)
        return res

class CritereConsultation:
    def __init__(self, parent=None):    #Parent is CriteresConsultation
        self.DBase=parent.DBase
        self.Table='ConsultationCritere'
        self.TableFields=self.DBase.GetFields(self.Table)
        #attributes: idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
        for i in self.TableFields:
            self.__dict__.update({i:None}) 
        self.Valeur=QtCore.QString('')
        self.PathologieRef_idPathologieRef=parent.idPathologieRef
          
    def Print(self):
        print '#attributes: '+','.join(self.TableFields)
        for i in self.TableFields:
            print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
        print 'Valeur:%s'%self.Valeur
     
    def Get(self,idConsultationCritere):
        #attributes: idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
        self.idConsultationCritere=idConsultationCritere
        res=self.DBase.GetDbText("SELECT * FROM ConsultationCritere(%i)"%idConsultationCritere)
        self.Critere_idCritere=res[1].toInt()[0]
        self.PathologieRef_idPathologieRef=res[2].toInt()[0]
        self.CritereQuantitatif=res[3]
        self.CritereQualitatif=res[4]
        self.Grade=res[5]
        return res
    
    def Set(self,data):
        for i,value in zip(self.TableFields,data):
            self.__dict__.update({i:value})
        
    def SetValues(self,valeur,grade):
        self.Valeur=valeur
        self.Grade=grade
        if self.Valeur.toFloat()[1]:
            self.CritereQuantitatif=self.Valeur
            self.CritereQualitatif=QtCore.QString('')
        else:
            self.CritereQuantitatif=QtCore.QString('')
            self.CritereQualitatif=self.Valeur
        
    def GetCritereGrade(self,Valeur):
        self.Valeur=Valeur    
        res=self.DBase.GetDbText("CALL GetCritereGrade(%i,%.2f)"%(self.idCritere,Valeur))
        if len(res)>0:
            self.Grade=res[0]+QtCore.QString('/')+res[1]
        return self.Grade

    def Save(self,idPathologieRef=None):
        err=[]
        values=[]
        ToDelete=False
        if not idPathologieRef is None:
            self.PathologieRef_idPathologieRef=idPathologieRef
        if self.idConsultationCritere>=0:
            values.append('%i'%self.idConsultationCritere)
        else:
            values.append('%i'%abs(self.idConsultationCritere))
            ToDelete=True
        if self.Critere_idCritere>0:
            values.append('%i'%self.Critere_idCritere)
        else:
            err.append('idCritere')
        if self.PathologieRef_idPathologieRef>0:
            values.append('%i'%self.PathologieRef_idPathologieRef)
        else:
            err.append('idPathologieRef')
        if self.CritereQuantitatif.isEmpty() and self.CritereQualitatif.isEmpty():
            err.append('Valeur Nulle')
        else:
            if self.CritereQuantitatif.toFloat()[1]:
                values.append('%.2f'%self.CritereQuantitatif.toFloat()[0])
                values.append('NULL')
            else:
                values.append('NULL')
                if self.CritereQualitatif.size()>20:
                    err.append('Critere Qualitatif trop long')  
                else:
                    values.append('\"%s\"'%self.CritereQualitatif)
            
        if self.Grade.size()>20:
            err.append('Grade trop long')
        if self.Grade.isEmpty():
            values.append('NULL')
        else:
            values.append('\"%s\"'%self.Grade)
        if len(err)==0:
            if self.idConsultationCritere==0:
                    #idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
                    dberr=self.DBase.DbAdd( self.Table, values)
                    if not dberr is None:
                        print dberr
            elif ToDelete:
                self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
            else:
                Nvalues=[values[0]]
                Nvalues.extend(values[3:])
                fields=[self.TableFields[0]]
                fields.extend(self.TableFields[3:])
                #idConsultationCritere,CritereQuantitatif,CritereQualitatif,Grade
                dberr=self.DBase.DbUpdate(self.Table,fields,Nvalues)
                if not dberr is None:
                    print dberr
        else:
            msg='Erreur Save %s :%s'%(self.Table,','.join(err))
            print msg
            return msg
                
    def DeleteConsultationCritere(self,idConsultationCritere):
        self.DBase.DbDelete('ConsultationCritere',['idConsultationCritere',str(idConsultationCritere)])
        
    
if __name__ == '__main__':
    import Tables
    import config 
    from Core_Consultation import Consultation
    DBase=Tables.DataBase(config.database)
    
    MyConsultation=Consultation(DBase,1)
    MyConsultation.Get(1)
    MyCriteres= CriteresConsultation(1,MyConsultation)
    MyCriteres.Get()
#     print MyCriteres.NewCritere(1)
    MyCriteres.Print()
    
#     MyCritere=Critere(DBase)
#     data=[0,3,QtCore.QString('Ileus'),QtCore.QString('aucune'),QtCore.QString('1'),QtCore.QString('facteur aggravant')]
#     MyCritere.Set(data,2)
#     MyCritere.Save()
#     MyCritere.Remarque=QtCore.QString('rien')
#     MyCritere.SaveCritere()
#     MyCritere.GetCritere(1)
#     MyCritere.Print()
#     MyGrade=CritereGrade(MyCritere)
#     MyGrade.GetCritereSeuil(0)
#     MyGrade.Score=QtCore.QString('1')
#     MyGrade.SaveGrade()
#     MyGrade.GetCritereSeuil(0)
#     MyGrade.Print()
