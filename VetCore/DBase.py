# -*- coding: utf8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtSql import *
import MyGenerics

class DBase:
    def __init__(self):
        self.Base=None
        self.errConnection=None
        self.Connection()
        
        
    def Connection(self):
        self.Base = QSqlDatabase.addDatabase("QMYSQL")
        self.Base.setHostName ( 'localhost' )
        self.Base.setUserName ( 'root' )
        self.Base.setPassword ( 'horizons' )
        self.Base.setDatabaseName("Opencompta")
        if not self.Base.open():
            self.errConnection=True
        else:
            self.errConnection=False
    
class Request(QSqlQuery):
    def __init__(self,table=None,parentwidget=None):
        QSqlQuery.__init__(self)#self.Base use .driver pour transactions
        self.res=None
        self.Table=table
        self.Fields=None
        self.lastID=None
        self.ParentWidget=parentwidget
        if not table is None:
            self.GetFields()
            self.FieldsName=[i.Name for i in self.Fields]
        
    def SetTable(self,table):
        self.Table=table
        
    def SetGui(self,parentwidget):
        self.ParentWidget=parentwidget
        
    def Execute(self,request):
        self.exec_(request)
        if self.lastError().isValid():
            MyGenerics.MyError(self.ParentWidget,self.lastError().text())
            return False
        return True
        
    def GetInt(self,request,index):
        self.res=None
        if self.Execute(request):
            self.next()
            if self.value(index).toInt()[1]:
                self.res=self.value(index).toInt()[0]
        return self.res  
    
    def GetInts(self,request,index):
        self.res=[]
        if self.Execute(request):
            while self.next():
                if self.value(index).toInt()[1]:
                    self.res.append(self.value(index).toInt()[0])
        return self.res

    def GetString(self,request,index=0):
        self.res=""
        if self.Execute(request):
            self.next()
            if self.isValid():
                self.res=self.value(index).toString()
        return self.res  
    
    def GetStrings(self,request,index):
        self.res=[]
        self.exec_(request)
        while self.next():
            self.res.append(self.value(index).toString())
        if len(self.res)==0:
            self.res=None
        return self.res
    
    def GetStringList(self,request,index): 
        self.res=QStringList()
        self.exec_(request)
        while self.next():
            self.res<<self.value(index).toString()
        if len(self.res)==0:
            self.res=None
        return self.res
         
    def GetidStrings(self,request,index):
        self.res=[]
        self.exec_(request)
        while self.next():
            self.res.append([self.value(index[0]).toInt()[0],self.value(index[1]).toString()])
        return self.res
    
    def GetLineTable(self,id):
        self.res=[]
        if self.Execute("SELECT * FROM %s WHERE id%s=%i"%(self.Table,self.Table,id)):
            self.next()
            if self.isValid():
                for i in range(self.record().count()):
                    self.res.append(self.value(i))                          
        return self.res
    
    def GetLineModel(self,request):
        self.res=[]
        if self.Execute(request):
            self.next()
            if self.isValid():
                for i in range(self.record().count()):
                    self.res.append(self.value(i))                          
        return self.res
    
    def GetComboList(self,request,firstField=None):
        #QVariant(Id),QString(Libele),QString(Remarque),QVariant(CodeColor),QVariant(isDeleted),QVariant(UserProperty1),QVariant(UserProperty2,...)
        if firstField is None:
            self.res=[]
        else:
            self.res=[[QVariant(0),QString(firstField),QString(''),QVariant(0)]]
        self.exec_(request)
        while self.next():
            tmp=[]
            for i in range(self.record().count()):
                tmp.append(self.value(i))
            if self.record().count()<5:
                tmp.extend([QVariant(0)]*(5-self.record().count()))
            tmp[1]=tmp[1].toString()
            tmp[2]=tmp[2].toString()
            self.res.append(tmp)
        return self.res

    def GetTableList(self,NbCol,request):
        #QVariant(Id),QVariant(col1),...,QVariant(Nbcol),QString(Remarque),QVariant(isDeleted),QVariant(UserProperty1),QVariant(UserProperty2,...
        self.res=[]
        self.exec_(request)
        while self.next():
            tmp=[]
            for i in range(self.record().count()):
                tmp.append(self.value(i))
            if self.record().count()<NbCol+3:
                tmp.extend([QVariant(0)]*(NbCol+3-self.record().count()))
            tmp[NbCol]=tmp[NbCol].toString()
            self.res.append(tmp)
        self.FieldsName=[self.record().fieldName(i+1) for i in range(NbCol)]
        return self.res
    
    def GetLines(self,request):
        self.res=[]
        if self.Execute(request):
            while self.next():
                tmp=[]
                for i in range(self.record().count()):
                    tmp.append(self.value(i))
                self.res.append(tmp)
        return self.res

    def GetLine(self,request):
        self.res=[]
        if self.Execute(request):
            self.next()
            if self.isValid():
                for i in range(self.record().count()):
                    self.res.append(self.value(i))                         
        return self.res
    
    def GetFields(self,table=None):
        if not table is None:
            self.Table=table
        self.Fields=[]
        self.exec_("SHOW COLUMNS FROM %s"%self.Table)
        while self.next():
            self.Fields.append(Field(self))
        return self.Fields
            
    def GetFieldIndex(self,name):
        for i in range(len(self.Fields)):
            if self.Fields[0].Name==name:
                return i
        return -1
    
    def ValidData(self,values,fields=None): #values are QString or QVariant
        err=[]
        newvalues=[]
        if fields is None:
            fields=self.Fields
        if len(values)!=len(fields):
            return ([u'Nombre de valeurs erroné'],None)
        for i,j in zip(values,fields):
            if i is None:
                if j.Null:
                    newvalues.append('NULL')
                else:
                    err.append(j.Name)
                continue
            elif 'int' in j.Type or j.Type=='id':
                if i.toInt()[1]:
                    newvalues.append('%i'%i.toInt()[0])
                else:
                    err.append(j.Name)
            elif 'decimal' in j.Type or 'float' in j.Type:
                if i.toFloat()[1]:
                    newvalues.append('%.2f'%i.toFloat()[0])
                else:
                    err.append(j.Name)
            elif 'date'==j.Type:
                if i.toDate().isValid():
                    newvalues.append('\"%s"'%i.toDate().toString('yyyy-MM-dd'))
                else:
                    err.append(j.Name)
            elif 'datetime'==j.Type:
                if i.toDateTime().isValid():
                    newvalues.append('\"%s"'%i.toDateTime().toString('yyyy-MM-dd : hh:mm'))
                else:
                    err.append(j.Name)
            elif 'varchar' in j.Type or 'text' in j.Type:
                if i.toString().isEmpty() and j.Name!='Identifiant':
                    if j.Null:
                        newvalues.append('NULL')
                    else:
                        err.append(j.Name)
                else:
                    if i.toString().size()<=j.Maxlength:
                        newvalues.append(u'\"%s"'%i.toString())
                    else:
                        err.append(j.Name)
            else:
                err.append(u'%s : Type non trouvé'%j.Name)
        return (err,newvalues)
                
    def Delete_Act(self,id):
        self.exec_("CALL DeleteItemTable(%i,\"%s\")"%(id,self.Table))
        return self.lastError()
    
    def Delete(self,ids):
        self.exec_("DELETE FROM %s WHERE %s"%(self.Table,'='.join(ids)))
        return self.lastError()
    
    def Save(self,values,fields=None):
        if values[0]=='0':
            return self.Add(values)
        else:
            if fields is None:
                fields=self.FieldsName
            return self.Update(fields,values)
    
    def Add(self,values):
        values=','.join(values)
        if not self.Table is None:
            self.exec_("INSERT INTO %s VALUES (%s)"%(self.Table,values))#TODO:if self.Execute
            self.lastID=self.lastInsertId()
            return self.lastError()
        else:
            return QSqlError('','Table non renseignée.')

    def Update(self,fields,values):
        idtable='='.join(zip(fields,values)[0])
        sets=','.join(['='.join(i) for i in zip(fields,values)[1:]])
        if not self.Table is None:
            self.exec_("UPDATE %s SET %s WHERE %s"%(self.Table,sets,idtable))
            return self.lastError()

class Field:
    def __init__(self,query):
        self.Name=str(query.value(0).toString())
        tmp=str(query.value(1).toString())
        self.Maxlength=None
        if tmp.count('(') and 'varchar' not in tmp:
            self.Type=tmp[:tmp.index('(')]
            if self.Type=='decimal':
                self.NbDecimals=tmp[tmp.index(',')+1:tmp.index(')')]
            if self.Type=='int' and query.value(3).toString()=='MUL':
                self.Type='id'
        elif 'varchar' in tmp:
            self.Type=tmp
            self.Maxlength=int(tmp[tmp.index('(')+1:tmp.index(')')])
        elif 'text' in tmp:
            self.Type='text'
            if tmp=='text':
                self.Maxlength=65535
            elif 'tinytext'==tmp:   #To avoid
                self.Maxlength=255
            elif 'mediumtext'==tmp: #To avoid
                self.Maxlength=16777216    
        else:
            self.Type=tmp
        self.Null=str(query.value(2).toString())=='YES'
        
        
                