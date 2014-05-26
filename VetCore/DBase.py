# -*- coding: utf8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtSql import *

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
    
class Request():
    def __init__(self,table=None):
        self.res=None
        self.Table=table
        self.Fields=None
        self.lastID=None
        if not table is None:
            self.GetFields()
            self.FieldsName=[i.Name for i in self.Fields]
        
    def SetTable(self,table):
        self.Table=table
        
    def GetInt(self,request,index):
        self.res=None
        query=QSqlQuery()
        query.exec_(request)
        query.next()
        if query.value(index).toInt()[1]:
            self.res=query.value(index).toInt()[0]
        del query
        return self.res  
    
    def GetInts(self,request,index):
        self.res=[]
        query=QSqlQuery()
        query.exec_(request)
        while query.next():
            if query.value(index).toInt()[1]:
                self.res.append(query.value(index).toInt()[0])
        if len(self.res)==0:
            self.res=None
        del query
        return self.res

    def GetString(self,request,index):
        self.res=None
        query=QSqlQuery()
        query.exec_(request)
        query.next()
        self.res=QString(query.value(index))
        del query
        return self.res  
    
    def GetStrings(self,request,index):
        self.res=[]
        query=QSqlQuery()
        query.exec_(request)
        while query.next():
            self.res.append(query.value(index).toString())
        if len(self.res)==0:
            self.res=None
        del query
        return self.res
    
    def GetStringList(self,request,index): 
        self.res=QStringList()
        query=QSqlQuery()
        query.exec_(request)
        while query.next():
            self.res<<query.value(index).toString()
        if len(self.res)==0:
            self.res=None
        del query
        return self.res
         
    def GetidStrings(self,request,index):
        self.res=[]
        query=QSqlQuery()
        query.exec_(request)
        while query.next():
            self.res.append([query.value(index[0]).toInt()[0],query.value(index[1]).toString()])
        del query
        return self.res
    
    def GetLines(self,request):
        self.res=[]
        query=QSqlQuery()
        query.exec_(request)
        while query.next():
            tmp=[]
            for i in range(query.record().count()):
                tmp.append(query.value(i))#.toString()
            self.res.append(tmp)
        del query
        return self.res

    def GetLine(self,request):
        self.res=[]
        query=QSqlQuery()
        query.exec_(request)
        query.next()
        if query.isValid():
            for i in range(query.record().count()):
                self.res.append(query.value(i).toString())                          
#            self.res=[query.value(i) for i in range(query.size())]
        if len(self.res)==0:
            self.res=None
        del query
        return self.res
    
    def GetFields(self,table=None):
        if not table is None:
            self.Table=table
        self.Fields=[]
        query=QSqlQuery()
        query.exec_("SHOW COLUMNS FROM %s"%self.Table)
        while query.next():
            self.Fields.append(Field(query))
            
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
            if 'int' in j.Type:
                if i.toInt()[1]:
                    newvalues.append('%i'%i.toInt()[0])
                else:
                    err.append(j.Name)
            if 'decimal' in j.Type or 'float' in j.Type:
                if i.toFloat()[1]:
                    newvalues.append('%.2f'%i.toFloat()[0])
                else:
                    err.append(j.Name)
            if 'date' in j.Type:
                if i.toDate()[1]:
                    newvalues.append('\"%s"'%i.toString('yyyy-MM-dd'))
                else:
                    err.append(j.Name)
            if 'datetime' in j.Type:
                if i.toDateTime()[1]:
                    newvalues.append('\"%s"'%i.toString('yyyy-MM-dd : hh:mm'))
                else:
                    err.append(j.Name)
            if 'varchar' in j.Type or 'text' in j.Type:
                if i.toString().isEmpty():
                    if j.Null:
                        newvalues.append('NULL')
                    else:
                        err.append(j.Name)
                else:
                    if i.toString().size()<=j.Maxlength:
                        newvalues.append(u'\"%s"'%i.toString())
                    else:
                        err.append(j.Name)
        return (err,newvalues)
                
    def Delete(self,ids):
        query=QSqlQuery()
        query.exec_("DELETE FROM %s WHERE %s"%(self.Table,'='.join(ids)))
        return query.lastError()
    
    def Save(self,values,fields=None):
        if values[0]=='0':
            return self.Add(values)
        else:
            if fields is None:
                fields=self.FieldsName
            return self.Update(fields,values)
    
    def Add(self,values):
        query=QSqlQuery()
        values=','.join(values)
        if not self.Table is None:
            query.exec_("INSERT INTO %s VALUES (%s)"%(self.Table,values))
            self.lastID=query.lastInsertId()
            return query.lastError()
        else:
            return QSqlError('','Table non renseignée.')

    def Update(self,fields,values):
        query=QSqlQuery()
        idtable='='.join(zip(fields,values)[0])
        sets=','.join(['='.join(i) for i in zip(fields,values)[1:]])
        if not self.Table is None:
            query.exec_("UPDATE %s SET %s WHERE %s"%(self.Table,sets,idtable))
            return query.lastError()

class Field:
    def __init__(self,query):
        self.Name=str(query.value(0).toString())
        tmp=str(query.value(1).toString())
        self.Maxlength=None
        if tmp.count('(') and 'varchar' not in tmp:
            self.Type=tmp[:tmp.index('(')]
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
        
        
                