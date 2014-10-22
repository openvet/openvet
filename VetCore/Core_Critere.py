# -*- coding: utf8 -*-
import time
import Core
from PyQt4 import QtCore
from MyGenerics import *


class FormConsultationCriteres(MyForm):
    def __init__(self,idConsultation,data,parent):
        MyForm.__init__(self,u'Criteres Pathologiques',data,parent)
        self.InactivateEnter()
        self.idConsultation=idConsultation
        self.idPathologie=0
        self.Resize(QSize(500,0))
        self.CancelOkOnly()
        self.fields[0].setModel(MyComboModel(self.parent,'GetPathologiesConsultCombo(%i)'%idConsultation))
        self.MyModel=None
        #idConsultationCritere,Examen,Critere,3.Valeur,Unite,Norme,Grade,Remarque,Color,9.isDeleted,
        #idCritere,(idPathologieRef,CritereQuant,CritereQual)
        self.connect(self.fields[0],SIGNAL("activated (int)"),self.OnPathologie)
        self.connect(self.fields[2],SIGNAL("activated (int)"),self.OnExamen)
        self.connect(self.fields[3],SIGNAL("activated (int)"),self.OnCritere)
        self.connect(self.fields[4],SIGNAL("clicked (QModelIndex)"),self.OnCritereConsultation)
#        self.connect(self.fields[4],SIGNAL("isDeleted(int)"),self.OnCritereDelete)
        self.connect(self.fields[5],SIGNAL("textEdited(QString)"),self.OnRemarqueEnter)
        self.EditButtons[0].clicked.connect(self.OnEditModel)
        self.EditButtons[1].clicked.connect(self.OnEditExamen)
        self.EditButtons[2].clicked.connect(self.OnEditCritere)
        self.OnPathologie(0)

    def OnPathologie(self,index):
        self.idPathologieRef=self.fields[0].Getid()
        self.idPathologie=self.fields[0].GetProperty(1).toInt()[0]
        self.fields[1].setModel(MyComboModel(self,'GetModelsExamen(%i)'%self.idPathologie))
        self.fields[2].setModel(MyComboModel(self,'GetExamens(%i)'%self.idPathologie))
        self.MyModel=MyTableModel(self,6,'GetConsultationCriteres(%i)'%self.idPathologieRef)
        self.MyModel.SetEditableCol([2,5])
        self.MyModel.SetRightAligned([3,4,5,6])
        self.fields[4].setModel(self.MyModel)  
        self.fields[4].resizeColumnsToContents()
        self.connect(self.MyModel,SIGNAL("dataChanged(QModelIndex,QModelIndex)"),self.OnCritereValueChange) 
        self.OnExamen(0)
        
#    def OnModelExamen(self): 
  
    def OnExamen(self,index):
        self.idExamen=self.fields[2].Getid()
        self.fields[3].setModel(MyComboModel(self.parent,'GetCriteres(%i,%i)'%(self.idPathologie,self.idExamen)))
        
    def OnCritere(self,index):
        index=self.fields[3].model().index(index)
        idCritere=QVariant(self.fields[3].Getid())
        newcritere=[QVariant(0),self.fields[2].currentText(),self.fields[3].model().data(index,Qt.DisplayRole),QVariant(),self.fields[3].model().data(index,34),
        self.fields[3].model().data(index,35),QVariant(),QVariant(),QVariant(0),QVariant(0),idCritere]
        if not self.MyModel.isExist(idCritere,10):
            self.MyModel.insertRows(0,newcritere)
            self.MyModel.sort(1)
            self.fields[4].resizeColumnsToContents()
        else:
            MyError(self,u'Ce critère est déjà présent dans la liste')
            
    def OnCritereConsultation(self,index):
        self.fields[5].setText(self.MyModel.data(index,Qt.ToolTipRole).toString())
    
    def OnRemarqueEnter(self,text):
        self.MyModel.setData(self.fields[4].currentIndex(),text,Qt.ToolTipRole)  
    
    def OnCritereValueChange(self,index1,index2):
        if index1.column()!=2:
            return
        idCritere=self.MyModel.data(index1,34).toInt()[0]
        if self.MyModel.data(index1,Qt.DisplayRole).toFloat()[1]:
            line=self.MyModel.Myrequest.GetLine('CALL GetCritereGrade(%i,%.3f)'%(idCritere,self.MyModel.data(index1,Qt.DisplayRole).toFloat()[0]))
            if len(line)==0:
                grade=''
            else:
                grade='%i/%i'%(line[0].toInt()[0],line[1].toInt()[0])
            self.MyModel.setData(self.MyModel.index(index1.row(),5),grade,Qt.EditRole)
              
    def OnValid(self):
        if not self.MyModel.dirty:
            return
        for i in self.MyModel.listdata:
            if i[3].toFloat()[1]:
                i.extend([QVariant(self.idPathologieRef),i[3],QVariant(),QVariant('')])
            else:
                i.extend([QVariant(self.idPathologieRef),QVariant(),i[3],QVariant('')])
        #idConsultationCritere,Examen,Critere,3.Valeur,Unite,Norme,Grade,Remarque,Color,9.isDeleted,
        #idCritere,(idPathologieRef,CritereQuant,CritereQual,"")
        self.MyModel.Update('ConsultationCritere',[0,10,11,12,13,6,7,9,14],self,0,9)
        self.accept()        

    def OnEditModel(self):
        idModel=self.fields[1].Getid()
        new=[0,self.idPathologie,'',None,True,False,'']
        Model=MyModel('ModelExamen',idModel,self)
        if not Model.SetNew(new):
            return  
        data=[[u'Nom du Modèle',1,60],[u'Remarque',3,200,80],[u'Critères',6,0,160]]
        form=FormModelExamen(data,self)
        form.SetModel(Model,{0:2,1:3})    #GUI_field : DB_Field
        form.exec_()
#         self.fields[2].setModel(MyComboModel(self,'GetModelsExamen(%i)'%self.idPathologie))    TODO:
#         self.fields[2].Setid(idModel)

    def OnEditExamen(self):
        idExamen=self.fields[2].Getid()
        new=[0,'',None,True,False,'']
        ExamenModel=MyModel('Examen',idExamen,self)
        if not ExamenModel.SetNew(new):
            return  
        data=[[u'Examen',1,60],[u'Remarque',3,200,80]]
        form=MyForm('Examens',data,self)
        form.SetModel(ExamenModel,{0:1,1:2})    #GUI_field : DB_Field
        form.exec_()
        self.fields[2].setModel(MyComboModel(self,'GetExamens(%i)'%self.idPathologie))
        self.fields[2].Setid(idExamen)
        
    def OnEditCritere(self):
        idCritere=self.fields[3].Getid()
        new=[0,0,'',0,'',None,True,False,'']
        self.CritereModel=MyModel('Critere',idCritere,self)
        if not self.CritereModel.SetNew(new):
            return      
        data=[[u'Examen',4],[u'Critere',1,60],[u'Unité',4,None,None,u'Edite l\'unité'],
              [u'Nombre de Grades',8,0,20],[u'Remarque',3,200,80],[u'Seuils',6,300,140]]
        form=FormCritere(idCritere,data,self)
        form.SetModel(self.CritereModel,{0:1,1:2,2:3,3:4,4:5})
        form.exec_()
        self.fields[3].setModel(MyComboModel(self.parent,'GetCriteres(%i,%i)'%(self.idPathologie,self.idExamen)))
        self.fields[3].Setid(idCritere)

class FormModelExamen(MyForm):
    def __init__(self,data,parent):
        MyForm.__init__(self,u'Modèle d\'Examen',data,parent)
        self.parent=parent
        self.Criteres=MyTableModel(self,2,parent.MyModel,[0,1,2,7,8,9,10])
        self.fields[2].setModel(self.Criteres)  
        self.fields[2].resizeColumnsToContents()
        self.resize(500,340)
        
    def OnValid(self):  #TODO
        if self.mapper.submit():
            self.MyModel.Update(self.mapper.currentIndex())
            #save self.Criteres
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Cette entrée constitue un doublon', QMessageBox.Ok | QMessageBox.Default)

class FormCritere(MyForm):
    def __init__(self,idCritere,data,parent):
        MyForm.__init__(self,u'Grades des critères pathologiques',data,parent)
        self.parent=parent
        self.idCritere=idCritere
        self.fields[0].setModel(MyComboModel(self.parent,'GetExamens(0)'))
        self.fields[2].setModel(MyComboModel(self.parent,'GetUnites()'))
        self.fields[3].setEnabled(False)
        self.GradesModel=MyTableModel(self,3,'GetCritereGrades(%i)'%idCritere)
        self.GradesModel.SetEditableCol([0,1,2])
        self.fields[5].setModel(self.GradesModel)  
        self.fields[5].resizeColumnsToContents() 
        self.AddMenuAction(self.fields[5],'Ajouter',self.OnAddGrade) 
        self.connect(self.fields[5],SIGNAL("isDeleted(int)"),self.OnGradeDelete)
        self.connect(self.GradesModel,SIGNAL("dataChanged(QModelIndex,QModelIndex)"),self.OnGradeChange)
        self.EditButtons[0].clicked.connect(self.OnEditUnite)

    def OnEditUnite(self):
        idUnite=self.fields[2].Getid()
        new=[0,'',False,True,False,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Concentration',2]]
        form=MyForm('Unités',data,self)
        form.SetModel(UniteModel,{0:1,1:2})    #GUI_field : DB_Field
        form.exec_()
        self.fields[2].setModel(MyComboModel(self.parent,'GetUnites()'))
        self.fields[2].Setid(idUnite)
        
    def OnGradeDelete(self):
        newvalue=max(self.parent.CritereModel.data(self.parent.CritereModel.index(0,4,QModelIndex()),Qt.DisplayRole).toInt()[0]-1,0)
        self.parent.CritereModel.setData(self.parent.CritereModel.index(0,4,QModelIndex()),newvalue,Qt.EditRole)
        #TODO: update is Actif
        
    def OnAddGrade(self):
        self.GradesModel.insertRows(self.GradesModel.rowCount()-1,[0,self.GradesModel.rowCount(),'0.00','0.00','',0,0])
        newvalue=self.parent.CritereModel.data(self.parent.CritereModel.index(0,4,QModelIndex()),Qt.DisplayRole).toInt()[0]+1
        self.parent.CritereModel.setData(self.parent.CritereModel.index(0,4,QModelIndex()),newvalue,Qt.EditRole)
        self.GradesModel.sort(0)

    def OnGradeChange(self):
        self.GradesModel.sort(0)
        #TODO: check consistency for grade & min/max
        
    def OnValid(self):
        if self.mapper.submit():
            self.MyModel.Update(self.mapper.currentIndex())
            #idCritereSeuil,grade,limInf,limSup,Remarque,Color,6.isDeleted,identifiant,idCritere,isActif
            self.GradesModel.Update('CritereSeuil',[0,8,2,3,1,4,9,6,7],self,0,6)
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Cette entrée constitue un doublon', QMessageBox.Ok | QMessageBox.Default)


              
# class Critere:                  #TODO: dériver d'une classe DataBase ou class abstraite? 
#     def __init__(self,DBase):      
#         self.Table='Critere'
#         self.DBase=DBase
#         self.TableFields=self.DBase.GetFields(self.Table)
#         #attributes: idCritere,Examen_idExamen,Critere,Unite_idUnite,NbGrades,Remarque
#         for i in self.TableFields:
#             self.__dict__.update({i:None})
#         self.Pathologie_idPathologie=None
#         self.CritereGrades=[]             
#         
#     def Print(self):
#         print '#attributes: '+','.join(self.TableFields)
#         for i in self.TableFields:
#             print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
#         for i in self.CritereGrades:
#                 i.Print()
#     
#     def Get(self,idCritere):
#         self.idCritere=idCritere
#         res=self.DBase.GetDbText("CALL GetCritere(%i)"%idCritere)
#         self.Examen_idExamen=res[1].toInt()[0]
#         self.Critere=res[2]
#         self.Unite_idUnite=res[3]
#         self.NbGrades=res[4]
#         self.Remarque=res[5]
#         self.Pathologie_idPathologie=res[6].toInt()[0]
#         #Get Grades
#         res=self.DBase.GetDbLines("CALL GetCritereGrades(%i)"%idCritere)
#         self.CritereGrades=[]
#         for i in res:
# #            print i
#             i[0]=i[0].toInt()[0]
#             tmp=CritereGrade(self)
#             tmp.Set(i)
#             self.CritereGrades.append(tmp)
#         return res     
#       
#     def Set(self,data,idPathologie):
#         for i,value in zip(self.TableFields,data):
#             self.__dict__.update({i:value})
#         self.Pathologie_idPathologie=idPathologie
#             
#     def GetUnite(self):
#         return self.DBase.GetDbidText('SELECT * FROM Unite ORDER By Unite')
#     
#     def GetIndexGrade(self,idCritereSeuil):
#         for i,j in zip(self.CritereGrades,range(len(self.CritereGrades))):
#             if i.idCritereSeuil==idCritereSeuil:
#                 return j
#     
#     def IsUsed(self):
#         return len(self.DBase.GetDbLines('SELECT PathologieRef_idPathologieRef FROM ConsultationCritere WHERE Critere_idCritere=%i'%self.idCritere))
#               
#     def UpdateGrade(self,data):
#         if data[0]>0:
#             index=self.CritereGrades[self.GetIndexGrade(data[0])]
#             index.Critere_idCritere=self.idCritere
#             index.LimiteInf=data[1]
#             index.LimiteSup=data[2]
#             index.Grade=data[3]
#             index.Score=data[4]
#         else:
#             Ndata=[data[0],self.idCritere]
#             Ndata.extend(data[1:])
#             tmp=CritereGrade(self)
#             tmp.Set(Ndata)
#             self.CritereGrades.append(tmp)
#               
#     def Save(self):
#         err=[]
#         values=[]
#         ToDelete=False
#         if self.idCritere<0:
#             ToDelete=True
#         values.append('%i'%abs(self.idCritere))
#         values.append('%i'%self.Examen_idExamen)
#         if self.Critere.size()<=60:
#             values.append(u'\"%s\"'%self.Critere)
#         else:
#             err.append(u'Nom du Critère trop long')
#         if self.Unite_idUnite.isEmpty():
#             values.append('NULL')
#         else:
#             res=self.DBase.GetDbidText('SELECT * From Unite WHERE idUnite=%i'%self.Unite_idUnite.toInt()[0])
#             if len(res):
#                 values.append('%i'%res[0][0])
#             else:
#                 err.append(u'Unité absente de la table Unite')
#         if self.NbGrades.toInt()[1]:
#             values.append('%i'%self.NbGrades.toInt()[0])
#         else:
#             values.append('NULL')
#         if not self.Remarque.isEmpty():
#             if self.Remarque.size()<=65536:
#                 values.append('\"%s\"'%self.Remarque.toUtf8().data())
#             else:
#                 err.append(' Remarque trop longue')   
#         else:
#             values.append('NULL')
#         if len(err)==0:
#             if ToDelete:
#                 self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
#                 return
#             if self.idCritere==0:
#                 #fields=['idCritere','Examen_idExamen','Critere','Unite_idUnite','NbGrades','Remarque']
#                 self.idCritere=self.DBase.DbAddLinked([self.Table,'CritereRef'], [values,['0','%i'%self.Pathologie_idPathologie,'(SELECT LAST_INSERT_ID())']])
#             else:
#                 Nvalues=[values[0]]
#                 Nvalues.extend(values[2:])
#                 fields=[self.TableFields[0]]
#                 fields.extend(self.TableFields[2:])
#                 #'idCritere','Critere','Unite_idUnite','NbGrades','Remarque'
#                 self.DBase.DbUpdate(self.Table,fields,Nvalues)
#             for i in self.CritereGrades:
#                 i.Critere_idCritere=self.idCritere
#                 i.Save()
#             return self.idCritere   
#         else:
#             msg='Erreur Save Critere :%s'%','.join(err)
#             print msg
#             return msg
#                 
# 
# class CritereGrade:
#     def __init__(self, parent=None):
#         self.DBase=parent.DBase
#         self.Table='CritereSeuil'
#         self.TableFields=self.DBase.GetFields(self.Table)
#         #attributes: idCritereSeuil,Critere_idCritere,LimiteInf,LimiteSup,Grade,Score
#         for i in self.TableFields:
#             self.__dict__.update({i:None}) 
#             
#         self.Critere_idCritere=parent.idCritere
#           
#     def Print(self):
#         print 'attributes: '+','.join(self.TableFields)
#         for i in self.TableFields:
#             print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))    
#              
#     def Get(self,grade):
#         res=self.DBase.GetDbText("CALL GetSeuil(%i,%i)"%(self.Critere_idCritere,grade))
#         self.idCritereSeuil=res[0].toInt()[0]
#         self.LimiteInf=res[1]
#         self.LimiteSup=res[2]
#         self.Grade=QtCore.QString('%i'%grade)
#         self.Score=QtCore.QString(res[3])
# #        self.Remarque=QtCore.QString(res[4])    TODO add Remarque in fields of GetSeuil
#         return res
#     
#     def Set(self,data):
#         for i,value in zip(self.TableFields,data):
#             self.__dict__.update({i:value})
#                
#     def CheckDoublon(self):
#         return self.DBase.RechercheSQL_id('CALL CheckDoublonCritere(%i,%i)'%(self.Critere_idCritere,self.Grade.toInt()[0]))>0
#                 
#     def Save(self):
#         err=[]
#         values=[]
#         ToDelete=False
#         if self.idCritereSeuil<0:
#             ToDelete=True
#         values.append('%i'%abs(self.idCritereSeuil))
#         values.append('%i'%self.Critere_idCritere)
#         if self.LimiteInf.toFloat()[1]:
#             values.append('%.2f'%self.LimiteInf.toFloat()[0])
#         else:
#             values.append('NULL')
#         if self.LimiteSup.toFloat()[1]:
#             values.append('%.2f'%self.LimiteSup.toFloat()[0])
#         else:
#             values.append('NULL')
#         if ' '.join(values[-2:])=='NULL NULL':
#             err.append('Erreur Seuils')
#         if self.Grade.toInt()[1]:
#             values.append('%i'%self.Grade.toInt()[0])
#         else:
#             err.append('Erreur de Grade')
#         if self.Score.isEmpty():
#             values.append('NULL')
#         else:
#             values.append('\"%s\"'%self.Score)
#         if self.Score.size()>45:
#             err.append('Erreur de Score trop long')
#         # for field Remarque
#         values.append('NULL')
#         if len(err)==0:
#             if ToDelete:
#                 self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
#                 return
#             if self.idCritereSeuil==0:
#                 #idCritereSeuil,Critere_idCritere,LimiteInf,LimiteSup,Grade,Score,Remarque
#                 if not self.CheckDoublon():
#                     print self.DBase.DbAdd('CritereSeuil',values)
#             else:
#     
#                 Nvalues=[]
#                 fields=[]
#                 for i in [0,2,3,5]:
#                     Nvalues.append(values[i])
#                     fields.append(self.TableFields[i])
#                 #'idCritereSeuil','LimiteInf','LimiteSup','Score'
#                 self.DBase.DbUpdate('CritereSeuil',fields,Nvalues)  
#         else:
#             msg='Erreur Save CritereSeuil :%s'%','.join(err)
#             print msg
#             return msg
# 
# class CriteresConsultation:
#     def __init__(self,idPathologie, parent=None):   #parent is Consultation
#         self.DBase=parent.DBase
#         self.Table='PathologieRef'
#         self.TableFields=self.DBase.GetFields(self.Table)
#         #attributes: idPathologieRef,Consultation_idConsultation,Pathologie_idPathologie
#         for i in self.TableFields:
#             self.__dict__.update({i:None}) 
#         self.Consultation_idConsultation=parent.idConsultation    
#         self.Pathologie_idPathologie=idPathologie
#         res=self.DBase.GetDbText("CALL GetPathologieDomaine(%i)"%idPathologie)
#         self.idDomainePathologie=res[0].toInt()[0]
#         self.DomainePathologie=res[1]
#         self.Pathologie_NomReference=res[2]
#         self.idPathologieRef=0
#         if self.Consultation_idConsultation > 0:
#             res=self.DBase.RechercheSQL_id("CALL GetPathologieRef(%i,%i)"%(self.Consultation_idConsultation,self.Pathologie_idPathologie))
#             if not res is None:
#                 self.idPathologieRef=res
#         self.Criteres=[]
#         
#     def Print(self):
#         print '#attributes: '+','.join(self.TableFields)
#         for i in self.TableFields:
#             print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
#         for i in self.Criteres:
#             i.Print() 
#                
#     def Get(self):
#         res=self.DBase.GetDbLines("CALL GetCriteresConsult(%i,%i)"%(self.Consultation_idConsultation,self.Pathologie_idPathologie))
#         self.Criteres=[]
#         for i in res:
#             tmp=CritereConsultation(self)
#             data=[i[0].toInt()[0],i[1].toInt()[0],self.idPathologieRef]
#             if i[4].toFloat()[1]:
#                 data.extend([QtCore.QString(i[4]),QtCore.QString('')])
#             else:
#                 data.extend([QtCore.QString(''),QtCore.QString(i[4])])
#             data.append(QtCore.QString(i[7]))
#             tmp.Set(data)
#             self.Criteres.append(tmp)
#         return res
#     
#     def Set(self,data):
#         for i,value in zip(self.TableFields,data):
#             self.__dict__.update({i:value})
#             
#     def Save(self, idConsultation=None):
#         #Save return ([fields],[values])->list->DBase.MultiEdit(list)
#         #idPathologieRef,Consultation_idConsultation,Pathologie_idPathologie
#         err=[]
#         values=[]
#         ToDelete=False
#         if not idConsultation is None:
#             self.Consultation_idConsultation=idConsultation
#         if self.idPathologieRef<0:
#             ToDelete=True
#         values.append('%i'%abs(self.idPathologieRef))           
#         if self.Consultation_idConsultation>0:
#             values.append('%i'%self.Consultation_idConsultation)
#         else:
#             err.append('idConsultation')
#         if self.Pathologie_idPathologie>0:
#             values.append('%i'%self.Pathologie_idPathologie)
#         else:
#             err.append('idPathologie')
#         values.append('NULL')
#         if ToDelete:
#             self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
#             return
#         if len(err)==0:
#             if ToDelete:
#                 self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
#             elif self.idPathologieRef==0:
#                 self.idPathologieRef=self.DBase.DbAdd( self.Table, values,True)
#             else:
#                 fields=['idPathologieRef','Pathologie_idPathologie']
#                 Nvalues=[values[0],values[2]]
#                 self.DBase.DbUpdate(self.Table,fields,Nvalues)
#                 #Delete old criteres if exist       
#             for i in self.Criteres:
#                 i.Save(self.idPathologieRef)
#         else:
#             msg='Erreur Save %s: %s'%(self.Table,','.join(err))
#             print msg
#             return msg
#     
#     def New(self,idCritere):  #old GetNewCritere
#         res=self.DBase.GetDbText("CALL GetNewConsultationCritere(%i)"%idCritere)
# #         tmp=CritereConsultation(self)
# #         data=[0,idCritere,self.idPathologieRef]
# #         data.extend([QtCore.QString('')]*3)
# #         tmp.Set(data)
# #         self.Criteres.append(tmp)
#         return res
# 
# class CritereConsultation:
#     def __init__(self, parent=None):    #Parent is CriteresConsultation
#         self.DBase=parent.DBase
#         self.Table='ConsultationCritere'
#         self.TableFields=self.DBase.GetFields(self.Table)
#         #attributes: idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
#         for i in self.TableFields:
#             self.__dict__.update({i:None}) 
#         self.Valeur=QtCore.QString('')
#         self.PathologieRef_idPathologieRef=parent.idPathologieRef
#           
#     def Print(self):
#         print '#attributes: '+','.join(self.TableFields)
#         for i in self.TableFields:
#             print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
#         print 'Valeur:%s'%self.Valeur
#      
#     def Get(self,idConsultationCritere):
#         #attributes: idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
#         self.idConsultationCritere=idConsultationCritere
#         res=self.DBase.GetDbText("SELECT * FROM ConsultationCritere(%i)"%idConsultationCritere)
#         self.Critere_idCritere=res[1].toInt()[0]
#         self.PathologieRef_idPathologieRef=res[2].toInt()[0]
#         self.CritereQuantitatif=res[3]
#         self.CritereQualitatif=res[4]
#         self.Grade=res[5]
#         return res
#     
#     def Set(self,data):
#         for i,value in zip(self.TableFields,data):
#             self.__dict__.update({i:value})
#         
#     def SetValues(self,valeur,grade):
#         self.Valeur=valeur
#         self.Grade=grade
#         if self.Valeur.toFloat()[1]:
#             self.CritereQuantitatif=self.Valeur
#             self.CritereQualitatif=QtCore.QString('')
#         else:
#             self.CritereQuantitatif=QtCore.QString('')
#             self.CritereQualitatif=self.Valeur
#         
#     def GetCritereGrade(self,Valeur):
#         self.Valeur=Valeur    
#         res=self.DBase.GetDbText("CALL GetCritereGrade(%i,%.2f)"%(self.idCritere,Valeur))
#         if len(res)>0:
#             self.Grade=res[0]+QtCore.QString('/')+res[1]
#         return self.Grade
# 
#     def Save(self,idPathologieRef=None):
#         err=[]
#         values=[]
#         ToDelete=False
#         if not idPathologieRef is None:
#             self.PathologieRef_idPathologieRef=idPathologieRef
#         if self.idConsultationCritere>=0:
#             values.append('%i'%self.idConsultationCritere)
#         else:
#             values.append('%i'%abs(self.idConsultationCritere))
#             ToDelete=True
#         if self.Critere_idCritere>0:
#             values.append('%i'%self.Critere_idCritere)
#         else:
#             err.append('idCritere')
#         if self.PathologieRef_idPathologieRef>0:
#             values.append('%i'%self.PathologieRef_idPathologieRef)
#         else:
#             err.append('idPathologieRef')
#         if self.CritereQuantitatif.isEmpty() and self.CritereQualitatif.isEmpty():
#             err.append('Valeur Nulle')
#         else:
#             if self.CritereQuantitatif.toFloat()[1]:
#                 values.append('%.2f'%self.CritereQuantitatif.toFloat()[0])
#                 values.append('NULL')
#             else:
#                 values.append('NULL')
#                 if self.CritereQualitatif.size()>20:
#                     err.append('Critere Qualitatif trop long')  
#                 else:
#                     values.append('\"%s\"'%self.CritereQualitatif)
#             
#         if self.Grade.size()>20:
#             err.append('Grade trop long')
#         if self.Grade.isEmpty():
#             values.append('NULL')
#         else:
#             values.append('\"%s\"'%self.Grade)
#         if len(err)==0:
#             if self.idConsultationCritere==0:
#                     #idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
#                     dberr=self.DBase.DbAdd( self.Table, values)
#                     if not dberr is None:
#                         print dberr
#             elif ToDelete:
#                 self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
#             else:
#                 Nvalues=[values[0]]
#                 Nvalues.extend(values[3:])
#                 fields=[self.TableFields[0]]
#                 fields.extend(self.TableFields[3:])
#                 #idConsultationCritere,CritereQuantitatif,CritereQualitatif,Grade
#                 dberr=self.DBase.DbUpdate(self.Table,fields,Nvalues)
#                 if not dberr is None:
#                     print dberr
#         else:
#             msg='Erreur Save %s :%s'%(self.Table,','.join(err))
#             print msg
#             return msg
#                 
#     def DeleteConsultationCritere(self,idConsultationCritere):
#         self.DBase.DbDelete('ConsultationCritere',['idConsultationCritere',str(idConsultationCritere)])
#         
    
if __name__ == '__main__':
    pass
