#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import os
import sys
import config
import Core
from DBase import *
from Mywidgets import *
from operator import itemgetter

# def Fdata(value,vtype=None,debug=False):
#     if isinstance(value,QString):
#         return value
#     if vtype is None:
#         vtype=value.typeName()
#     if value.isNull():
#         if debug:
#             return 'NULL'
#         else:
#             return QString('')
#     elif vtype=='QDate':
#         return value.toDate().toString('dd/MM/yyyy')
#     elif vtype=='QDateTime':
#         return value.toDateTime().toString('dd/MM/yyyy hh:mm')
#     elif vtype in ['int','qlonglong']:
#         return value.toInt()[0]
#     elif vtype=='QString':
#         return value.toString()
#     elif vtype=='bool':
#         return value.toBool()
#     elif vtype=='double' or vtype=='float':
#         return value.toFloat()[0]
#     else:
#         if debug:
#             print value.typeName()
#         return u'indeterminé'

class MyComboModel(QAbstractListModel):     #Convient aussi pour QListView
    def __init__(self, parentwidget,routine=None,firstField=None):
        QAbstractListModel.__init__(self, parent=None)
        self.ParentWidget=parentwidget
        self.MyRequest=Request()
        self.error=None
        self.isEditable=False
        self.dirty=False
        if routine is None:
            self.Routine=QString('')
        else:
            if isinstance(routine,str):
                self.Routine=routine
                self.listdata = self.MyRequest.GetComboList('CALL %s'%self.Routine,firstField )
                if self.MyRequest.lastError().isValid():
                    self.error=self.MyRequest.lastError().text()
                    MyError(parentwidget,self.error)
            elif isinstance(routine,list):
                self.listdata =routine
              
    def Set(self,routine=None,firstField=None):
        if not routine is None:
            self.Routine=routine
            self.listdata = self.MyRequest.GetComboList('CALL %s'%self.Routine,firstField )
            if self.MyRequest.lastError().isValid():
                self.error=self.MyRequest.lastError().text()
        else:
            self.listdata = []
        
                
    def rowCount(self,parent=QModelIndex()): 
        return len(self.listdata)
     
    def columnCount(self, index=QModelIndex()):
        try:
            return len(self.listdata[0])
        except:
            return 0
    
    def data(self, index, role): 
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()][1])
        if role == Qt.EditRole:
            return QVariant(self.listdata[index.row()][1])
        elif role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif role == Qt.ToolTipRole:
            return QVariant(Core.Multiline(self.listdata[index.row()][2]))
        elif role == Qt.ForegroundRole: #Qt.ForegroundRole BUG in pyqt4 with ubuntu 10.04 TODO: test 12.04
            color=self.listdata[index.row()][3].toInt()[0]
            if color>0:
                if color==6:
                    return(QColor(Qt.lightGray))
                elif color==7:
                    return(QColor(Qt.red))
                elif color==8:
                    return(QColor(Qt.green))
        elif role == 33:    #isDeleted
            return QVariant(self.listdata[index.row()][4])
        elif role > 33:    #UserProperty
            return QVariant(self.listdata[index.row()][4+role-33])
        else: 
            return QVariant()
    
    def setData(self,index,value,role=Qt.EditRole):
        if not index.isValid():
            return False
        value=QVariant(value)
        if role == Qt.EditRole:
            self.listdata[index.row()][1]=value.toString()
        elif role == Qt.UserRole:
            self.listdata[index.row()][0]=value
        elif role == Qt.ToolTipRole:
            self.listdata[index.row()][2]=value.toString()
        elif role == Qt.ForegroundRole:
            self.listdata[index.row()][3]=value
        elif role == 33:    #isDeleted
            self.listdata[index.row()][4]=value
        elif role > 33:    #UserProperty
            self.listdata[index.row()][4+role-33]=value
        else: 
            return False
        if role!=33:
            self.dirty = True
            self.SignId(index)
        else:
            self.SignId(index,False)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index,index)
        return True
        
    def flags(self,index):
        if not index.isValid() or not self.isEditable:
            return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        return Qt.ItemFlags(QAbstractListModel.flags(self,index)|Qt.ItemIsEditable)
          
    def Extend(self,value):  #for more user data
        for i in self.listdata:
            i.append(QVariant(value))
        
    def NewLine(self,data):
        for i,j in enumerate(data):
            if i in [1,2]:
                j=QString(j)
            else:
                data[i]=QVariant(j)
        row=self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self.listdata.append(data)
        self.endInsertRows()
        self.dirty = True

    def DeleteLine(self,index):
        self.dirty = True
        self.setData(index, 1, 33)
           
    def GetIndex(self,currentid):
        res=[i for i in self.listdata if i[0]==currentid]
        if len(res)==0:
            MyError(self.ParentWidget,u'L\'identifiant %i est absent de la liste retournée par: %s'%(currentid.toInt()[0],self.Routine))
        return self.listdata.index(res[0])
           
    def SignId(self,index,neg=True):
        if neg:
            self.listdata[index.row()][0]=QVariant(-abs(self.listdata[index.row()][0].toInt()[0]))
        else:
            self.listdata[index.row()][0]=QVariant(abs(self.listdata[index.row()][0].toInt()[0]))
            
    def EditItem(self,values,table,maplist,idindex,delindex,parent):
        values[idindex]=QVariant(abs(values[idindex].toInt()[0]))
        model=MyModel(table,0,parent)
        model.SetNew([values[j] for j in maplist])
        model.New()
        model.Update()
        #if model.Newvalues[0]==0:return model.lastid else: return model.Newvalues[0]
        return model.lastid
    
    def DeleteAll(self,table,parent):
        self.dirty=True
        for i in self.listdata:
            i[4]=1
        self.Update(table,None,parent)  
            
    def DeleteItem(self,table,id,parent):
        model=MyModel(table,abs(id),parent)
        model.Delete()
        
    def Update(self,table,maplist,parent,idindex=0,delindex=4):
        if not self.dirty:
                return
        for i in self.listdata:
            id=i[idindex].toInt()[0]
            if id<=0 and not i[delindex].toBool():
                self.EditItem(i,table,maplist,idindex,delindex,parent)
            elif i[delindex].toBool() and id!=0:
                self.DeleteItem(table,abs(id),parent)
            
    def UpdateRelational(self,table,maplist,tableref,maplistref,idref,delref,parent):
        if not self.dirty:
            return
        for i in self.listdata:
            idtable=i[0].toInt()[0]
            idtableref=i[idref].toInt()[0]
            isdeltable=i[4].toBool()
            isdeltableref=i[delref].toBool()
            if idtable <=0 and not isdeltable:
                lastid=self.EditItem(i,table,maplist,0,4,parent)
                if idtable==0:
                    i[0]=lastid
                if idtableref==0 and not isdeltableref:
                    self.EditItem(i,tableref,maplistref,idref,delref,parent)
            elif isdeltableref and idtableref!=0:
                self.DeleteItem(tableref,abs(idtableref),parent)
                if isdeltable and idtable!=0:
                    self.DeleteItem(table,abs(idtable),parent)
        
    def Print(self):
        fields=['id',u'Libélé','Remarque','Color','isDeleted']
        for n,i in enumerate(self.listdata):
            print 'item %i'%n
            line=[]
            for m,j in enumerate(i):
                if m<5:
                    field=fields[m]
                else:
                    field='user%i'%(m-4)
                line.append('%i.%s=%s'%(m,field,str(Core.Fdata(j,None,True))))
            print ','.join(line) 
            
class MyTableModel(QAbstractTableModel):
    def __init__(self, parent,nbHeaders,request,cols=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args)
        self.parent=parent
        self.Myrequest = Request()
        if isinstance(request,str):
            self.listdata = self.Myrequest.GetTableList(nbHeaders,'CALL %s' % request)
            self.Headers=self.Myrequest.FieldsName
        if isinstance(request,QAbstractTableModel):     #Duplicate model
            self.listdata=[]
            for row in request.listdata:
                self.listdata.append([j for i,j in enumerate(row) if i in cols])
            self.Headers=[j for i,j in enumerate(request.Headers) if i in cols]
        self.NbCols=nbHeaders
        self.VectorHeaders=[i for i in range(self.NbCols)]
        self.RightAligned=[i for i in range(self.NbCols) if i>0]
        self.EditableCol=[]
        self.dirty=False
         
    def Print(self):
        fields=['id']
        fields.extend(self.Headers)
        fields.extend(['Remarque','Color','isDeleted'])
        for n,i in enumerate(self.listdata):
            print 'item %i'%n
            line=[]
            for m,j in enumerate(i):
                if m<self.NbCols+4:
                    field=fields[m]
                else:
                    field='user%i'%(m-4)
                line.append('%i.%s=%s'%(m,field,str(Core.Fdata(j,None,True))))
            print ','.join(line) 
            
    def SetRightAligned(self,vector):
        self.RightAligned=vector
                       
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata)
     
    def columnCount(self, parent=QModelIndex()):
        return self.NbCols
     
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.Headers[col])
        return QVariant()
      
    def data(self, index, role): 
        if not index.isValid():
            return
        if role == Qt.DisplayRole or role==Qt.EditRole:
            if index.column() in self.VectorHeaders:
                return self.listdata[index.row()][index.column()+1]           
        elif role == Qt.TextAlignmentRole:
            if index.column() in self.RightAligned:
                return QVariant(int(Qt.AlignRight | Qt.AlignCenter))         
        elif role == Qt.ToolTipRole:
            return self.listdata[index.row()][self.NbCols+1]
        elif role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif role == Qt.TextColorRole:
            color=self.listdata[index.row()][self.NbCols+2].toInt()[0]
            if color>0:
                if color==1:
                    return(QColor(Qt.blue))
                if color==6:
                    return(QColor(Qt.lightGray))
                elif color==7:
                    return(QColor(Qt.red))
                elif color==8:
                    return(QColor(Qt.green))
        elif role == 33:    #isDeleted
            return QVariant(self.listdata[index.row()][self.NbCols+3])
        elif role > 33:    #UserProperty
            return QVariant(self.listdata[index.row()][self.NbCols+3+role-33])
            return QVariant()
        else: 
            return QVariant()
         
    def flags(self, index):
        if index.isValid() and index.column() in self.EditableCol:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        else:
            return Qt.ItemIsEnabled
    
    def SetEditableCol(self,cols):
        self.EditableCol=cols
         
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not index.row() < self.rowCount():
            return False
        value=QVariant(value)
        if role == Qt.EditRole:
            self.listdata[index.row()][index.column()+1]=value
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
    
    def sort(self,col,order = Qt.AscendingOrder):
        self.listdata=sorted(self.listdata,key=itemgetter(col+1))

    def SignId(self,index,neg=True):
        if neg:
            self.listdata[index.row()][0]=QVariant(-abs(self.listdata[index.row()][0].toInt()[0]))
        else:
            self.listdata[index.row()][0]=QVariant(abs(self.listdata[index.row()][0].toInt()[0]))
    
    def isExist(self,value,col):
        return len([i[col] for i in self.listdata if value==i[col]])>0
    
    def Clear(self):
        while self.rowCount()>0:
            self.removeRows(self.rowCount()-1)
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        if self.rowCount()==0:
            return False
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
#        self.Deleted.append('%i' % self.listdata[position][0].toInt()[0])
        self.listdata = self.listdata[:position] + self.listdata[position + rows:]
        self.endRemoveRows()
        self.dirty = True
        return True
     
    def insertRows(self, position, data, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.listdata.append(data)
        self.endInsertRows()
        self.dirty = True
             
    def SetModel(self,Parametres):
        valid = False
        if self.rowCount()>0:
            self.removeRows(0,self.rowCount())
        for i in range(Parametres.rowCount()):
            valid = True
            newparametre = Parametres.GetParametre(i)
            if not self.isExist(newparametre[1]):
                self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
                self.listdata.append(newparametre)
                self.endInsertRows()
            else:
                valid = False
        self.dirty = True
        return valid

    def EditItem(self,values,table,maplist,idindex,delindex,parent):
        values[idindex]=QVariant(abs(values[idindex].toInt()[0]))
        model=MyModel(table,0,parent)
        model.SetNew([values[j] for j in maplist])
        model.New()
        model.Update()
        if model.Newfields[0].toInt()[0]==0:
            return model.lastid
        else:
            return model.Newfields[0].toInt()[0]
            
    def DeleteItem(self,table,id,parent):
        model=MyModel(table,abs(id),parent)
        model.Delete()
    
    def DeleteAll(self,table,parent,delindex=4):
        self.dirty=True
        for i in self.listdata:
            i[delindex]=1
        self.Update(table,None,parent,0,delindex)   

    def Update(self,table,maplist,parent,idindex=0,delindex=4):
        if not self.dirty:
                return
        #BeginTransaction TODO: is transaction
        for i in self.listdata:
            id=i[idindex].toInt()[0]
            if id<=0 and not i[delindex].toBool():
                self.EditItem(i,table,maplist,idindex,delindex,parent)
                #Appenderror?
            elif i[delindex].toBool() and id!=0:
                self.DeleteItem(table,abs(id),parent)
            
    def UpdateRelational(self,table,maplist,tableref,maplistref,idref,delref,parent):
        if not self.dirty:
            return
        for i in self.listdata:
            idtable=i[0].toInt()[0]
            idtableref=i[idref].toInt()[0]
            isdeltable=i[4].toBool()
            isdeltableref=i[delref].toBool()
            if idtable <=0 and not isdeltable:
                lastid=self.EditItem(i,table,maplist,0,4,parent)
                if idtable==0:
                    i[0]=lastid
                if idtableref==0 and not isdeltableref:
                    self.EditItem(i,tableref,maplistref,idref,delref,parent)
            elif isdeltableref and idtableref!=0:
                self.DeleteItem(tableref,abs(idtableref),parent)
                if isdeltable and idtable!=0:
                    self.DeleteItem(table,abs(idtable),parent) 
 
        
class MyModel(QAbstractListModel):  #TODO: rename in MyRecordModel
    def __init__(self, table,idTable,parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.parent=parent
        if isinstance(idTable,QVariant):
            idTable=idTable.toInt()[0]
        self.Table=table
        self.Fields=[]
        self.NbFields=0
        self.ParentWidget=parent
        self.MyRequest=Request(table,self.ParentWidget)
        self.GetFields()
        self.listdata=self.MyRequest.GetLineTable(idTable)      
        self.lastid=0
        self.lasterror=None
        
    def Print(self):
        for i in range(self.NbFields):
            value=self.listdata[i]
            if value.isNull():
                value=None
            print '%i. %s : %s'%((i+1),self.Fields[i].Name,str(self.Fdata(i,None,True)))
            
    def ExtendData(self,row,extdata):
        #[id,data1,data2,...]
        if extdata[0]==self.listdata[0]:
            self.listdata.extend(extdata[1:])
        else:
            MyError(self.ParentWidget,u'L\'id des données à ajouter ne coorespond pas à l\'id des données déjà présentes')

    def rowCount(self,parent=QModelIndex()):
        return 1
    
    def columnCount(self,parent=QModelIndex()):
        return self.NbFields
    
    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.column()])
        else: 
            return QVariant()
    
    def Fdata(self,col,vtype=None,debug=False):
        value=self.listdata[col]
        if vtype is None:
            vtype=value.typeName()
        if value.isNull():
            if debug:
                return 'NULL'
            else:
                return QString('')
        elif vtype=='QDate':
            return value.toDate().toString('dd/MM/yyyy')
        elif vtype=='QDateTime':
            return value.toDateTime().toString('dd/MM/yyyy hh:mm')
        elif vtype in ['int','qlonglong']:
            return value.toInt()[0]
        elif vtype=='QString':
            return value.toString()
        elif vtype=='bool':
            return value.toBool()
        elif vtype=='double' or vtype=='float':
            return value.toFloat()[0]
        else:
#            print value.typeName()
            return u'indeterminé'
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.row()==0:
            self.listdata[index.column()] = value
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
            return True
        return False   
       
    def GetFields(self):
        self.Fields=self.MyRequest.GetFields()
        self.NbFields=len(self.Fields)
             
    def SetNew(self,new):
        if self.NbFields!=len(new):
            MyError(self.ParentWidget,u'Le vecteur d\'initialisation de %s n\'est pas valide'%self.Table)
            return False
        else:
            self.Newfields=[QVariant(i) for i in new]
            return True
        
    def Setid(self,idTable):
        self.listdata=self.MyRequest.GetLineTable(idTable)
       
    def New(self):
        self.listdata=self.Newfields
    
    def BeginTransaction(self):
        self.MyRequest.driver().beginTransaction()
        
    def CommitTransaction(self):
        self.MyRequest.driver().commitTransaction()
          
    def Delete(self):
        self.MyRequest.Delete_Act(self.listdata[0].toInt()[0])
        
    def Update(self,index=0):
        values=[]
        for i in range(self.NbFields):
            value=self.listdata[i]
            if value.isNull():
                value=None
            values.append(value)
#        self.Print()
        (err, values) =self.MyRequest.ValidData(values, self.Fields)
        if len(err) == 0:
            error = self.MyRequest.Save(values)
            if error.isValid():
                self.lasterror=error
                if self.lasterror.type()==2:
                    MyError(self.ParentWidget,u'La requête \"%s\" constitue un doublon.'%self.MyRequest.lastQuery())
                    return QVariant()
            else:
                self.lastid=self.MyRequest.lastID
                return self.lastid
        else:
            MyError(self.parent,u'Les champs %s sont invalides'%','.join(err))
            self.lasterror=u'Les champs %s sont invalides'%','.join(err)
            return -1
 

LINEEDIT,CHECKBOX,PLAINTEXTEDIT,COMBOBOX,LIST,TABLE,LABELS,SPINBOX = range(1,9)

class MyForm(QDialog):
    def __init__(self,title,data,parent=None):
        QDialog.__init__(self,parent)
        #data: label,typewidget,(maxlen,Qsize,tooltip_editbutton,rowFormat(0,1:multiple items on a row,2:a single spanning widget))
        self.setWindowTitle(title)
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.spanlayout=QHBoxLayout()
        Skipping=False
        self.labels=[]
        self.fields=[]
        self.popMenus=[]
        self.EditButtons=[]
        for index,i in enumerate(data):
            while len(i)<6:
                if len(i)==5:
                    i.append(False)
                else:
                    i.append(None)        
            if len(i[0])>0:
                label = QLabel('%s :'%i[0],self)
            else:
                label = QLabel()
            self.labels.append(label)
            if i[1]==1: #LineEdit
                field = QLineEdit(self)
                field.setMaxLength(i[2])
            if i[1]==2: #CheckBox
                field=QCheckBox ('')   
            if i[1]==3: #PlainTextEdit
                field=MyPlainTextEdit(self)
                field.SetMaxLength(i[2])
                field.setMaximumSize(1000,i[3])
            if i[1]==4: #Combobox
                field=MyComboBox(self)
                field.setMaximumSize(1000,27)
            if i[1]==5: #ListView
                field=QListView(self)
                field.setMaximumSize(1000,i[3])
                field.setContextMenuPolicy(Qt.CustomContextMenu)
                self.connect(field,SIGNAL('customContextMenuRequested(const QPoint&)'), self.OnListViewMenu)
                menuList = QMenu(field)
                action1=menuList.addAction('Supprimer')
                action1.setData(field)
                self.connect(action1,SIGNAL("triggered()"),self.OnList_delete)
                self.popMenus.append(menuList)
            if i[1]==6: #TableView:
                field=MyTableView(self)
                if not i[3] is None:
                    field.setMaximumSize(1000,i[3])
                field.setContextMenuPolicy(Qt.CustomContextMenu)
                self.connect(field,SIGNAL('customContextMenuRequested(const QPoint&)'), self.OnListViewMenu)
                menuTable = QMenu(field)
                action1=menuTable.addAction('Supprimer')
                action1.setData(field)
                self.connect(action1,SIGNAL("triggered()"),self.OnList_delete)
                self.popMenus.append(menuTable) 
            if i[1]==8: #SpinBox
                field = QSpinBox(self)
                if not i[2] is None:
                    field.setMinimum(i[2])
                if not i[2] is None:
                    field.setMaximum(i[3])   
            field.setObjectName(QString(i[0]))
            self.fields.append(field)
            if i[5]!=2:
                label.setBuddy(field)
            if not i[4] is None:    #isEditable
                tmp=QHBoxLayout()
                tmp.addWidget(field)
                editbutton=QToolButton(self)
                editbutton.setIcon(QIcon('../images/edit1.png'))
                editbutton.setIconSize(QSize(20,20))
                editbutton.setToolTip(QString(i[4]))
                editbutton.setObjectName(QString(i[0]))
                tmp.addWidget(editbutton)
                field=tmp
                self.EditButtons.append(editbutton)
            if i[5]==1:
                Skipping=True
                self.spanlayout.addWidget(label)
                if isinstance(field,QHBoxLayout):
                    self.spanlayout.addLayout(field)
                else:
                    self.spanlayout.addWidget(field)
            elif i[5]==2:
                self.formLayout.setWidget(index, QFormLayout.SpanningRole, field)
            else:
                if Skipping:
                    Skipping=False
                    self.spanlayout.addWidget(label)
                    if isinstance(field,QHBoxLayout):
                        self.spanlayout.addLayout(field)
                    else:
                        self.spanlayout.addWidget(field)
                    self.formLayout.addRow(self.spanlayout)
                    self.spanlayout=QHBoxLayout()  
                else:
                    if isinstance(field,QHBoxLayout):
                        self.formLayout.addRow(label,field)
                    else:
                        self.formLayout.setWidget(index, QFormLayout.LabelRole, label)
                        self.formLayout.setWidget(index, QFormLayout.FieldRole, field)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QHBoxLayout()
        self.pushButton_Cancel = QPushButton(self)
        self.pushButton_Cancel.setMinimumSize(QSize(0, 27))
        self.pushButton_Cancel.setText(u'Annuler')
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        self.pushButton_Add = QPushButton(self)
        self.pushButton_Add.setMinimumSize(QSize(0, 27))
        self.pushButton_Add.setText(u'Nouveau')
        self.horizontalLayout.addWidget(self.pushButton_Add)
        self.pushButton_Delete = QPushButton(self)
        self.pushButton_Delete.setMinimumSize(QSize(0, 27))
        self.pushButton_Delete.setText(u'Supprimer')
        self.horizontalLayout.addWidget(self.pushButton_Delete)
        self.pushButton_Valid = QPushButton(self)
        self.pushButton_Valid.setMinimumSize(QSize(0, 27))
        self.pushButton_Valid.setText(u'Valider')
        self.horizontalLayout.addWidget(self.pushButton_Valid)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        self.pushButton_Delete.clicked.connect(self.OnDelete)
        self.pushButton_Valid.clicked.connect(self.OnValid)
        self.pushButton_Add.clicked.connect(self.OnNew)

        self.setSizeGripEnabled(True)
    
    def Resize(self,size):
        self.setMinimumSize(size)   
         
    def InactivateEnter(self):
        self.pushButton_Valid.setAutoDefault(False)
        self.pushButton_Delete.setAutoDefault(False)
        self.pushButton_Add.setAutoDefault(False)
        self.pushButton_Cancel.setAutoDefault(False)
        
    def CancelOkOnly(self):
        self.pushButton_Add.hide()
        self.pushButton_Delete.hide()   
             
    def AddMenuAction(self,widget,label,function):
        for i in self.popMenus:
            if i.parent()==widget:
                i.addAction(label,function)
        
    def OnListViewMenu(self,point):
        for i in self.popMenus:
            if i.parent()==self.sender():
                i.exec_(i.parent().mapToGlobal(point))
                break
            
    def OnList_delete(self): 
        if self.sender().data().toPyObject().model().data(self.sender().data().toPyObject().currentIndex(), 33).toBool():
            isdeleted=False
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(), False, 33)
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(),0,Qt.ForegroundRole)
            QToolTip.showText(QCursor.pos(),u'Elément restauré.')
        else:
            isdeleted=True
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(), True, 33)
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(),6,Qt.ForegroundRole)
            QToolTip.showText(QCursor.pos(),u'Elément marqué pour la suppression.')
        self.sender().data().toPyObject().emit(SIGNAL("isDeleted(int)"),isdeleted)

    def SetModel(self,model,maplist):
#        maplist format GUI_field : DB_Field
        self.MyModel=model
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setOrientation(Qt.Horizontal)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyModel)
        self.MyDelegate=GenericDelegate(self)
        for i,j in enumerate(self.fields):
                if maplist.has_key(i):
                    if isinstance(j,QLineEdit):
                        self.MyDelegate.insertFieldDelegate(maplist[i],self.MyModel.Fields[maplist[i]]) #Debug i+1=>maplist[i]
                    elif isinstance(j,QCheckBox):
                        self.MyDelegate.insertColumnDelegate(maplist[i],CheckboxColumnDelegate())
                    elif isinstance(j,QComboBox):
                        self.MyDelegate.insertColumnDelegate(maplist[i],ComboboxColumnDelegate())
                    elif isinstance(j,(QPlainTextEdit,MyPlainTextEdit)):  #regrouper avec QLineEdit?
                        self.MyDelegate.insertColumnDelegate(maplist[i],PlainTextColumnDelegate())
                    elif isinstance(j,QSpinBox):
                        self.MyDelegate.insertColumnDelegate(maplist[i],IntegerColumnDelegate())              
        self.mapper.setItemDelegate(self.MyDelegate)
        for i,j in enumerate(self.fields):
            if maplist.has_key(i):
                self.mapper.addMapping(j, maplist[i])
        self.mapper.toFirst()
        return True
            
    def OnDelete(self):
        if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de vouloir effacer cet élément?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.Yes:
            self.MyModel.Delete(self.mapper.currentIndex())
            self.mapper.submit()
            self.accept()
    
    def OnValid(self):  #surcharger ou valider avec DBase
        if self.mapper.submit():
            self.MyModel.Update(self.mapper.currentIndex())
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Cette entrée constitue un doublon', QMessageBox.Ok | QMessageBox.Default)
            
    def OnNew(self):
        self.MyModel.New()
        self.fields[0].setFocus()
        self.mapper.toFirst()
    
    def OnCancel(self):
        self.close()
        
        
class GenericDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}

    def insertColumnDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate

    def insertFieldDelegate(self,column,field):
        if field.Type=='int':
            self.insertColumnDelegate(column, IntegerColumnDelegate())
        elif field.Type=='id':
            self.insertColumnDelegate(column, ComboboxColumnDelegate())
        elif field.Type=='text' or 'varchar' in field.Type:
            self.insertColumnDelegate(column, PlainTextColumnDelegate())
        elif field.Type=='datetime':
            self.insertColumnDelegate(column, DateColumnDelegate())
        elif 'decimal' in field.Type:
            self.insertColumnDelegate(column, FloatColumnDelegate(field.NbDecimals))

    def removeColumnDelegate(self, column):
        if column in self.delegates:
            del self.delegates[column]


    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QItemDelegate.paint(self, painter, option, index)


    def createEditor(self, parent, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QItemDelegate.createEditor(self, parent, option,index)

    def setEditorData(self, editor, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QItemDelegate.setModelData(self, editor, model, index)


class IntegerColumnDelegate(QItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum


    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return spinbox


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toInt()[0]
        if isinstance(editor,QLineEdit):
            editor.setText(QString('%i'%value))
        else:
            editor.setValue(value)


    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))


class CheckboxColumnDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(CheckboxColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return self

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toBool()
        if value:
            editor.setCheckState(Qt.Checked)
        else:
            editor.setCheckState(Qt.Unchecked)

    def setModelData(self, editor, model, index):
        if editor.checkState():
            model.setData(index, QVariant(True))
        else:
            model.setData(index, QVariant(False))
    
    
class ComboboxColumnDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(ComboboxColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return self

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        if not value.isNull():
            comboindex=editor.model().GetIndex(value)
        else:
            comboindex=0
        editor.setCurrentIndex(comboindex)

    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.Getid()))
        
        
class FloatColumnDelegate(QItemDelegate):

    def __init__(self, NbDecimals,minimum=0, maximum=10000, parent=None):
        super(FloatColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.NbDecimals=NbDecimals


    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        lineedit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return lineedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toFloat()[0]
        if self.NbDecimals==1:
            editor.setText('%.1f'%value)
        elif self.NbDecimals==2:
            editor.setText('%.2f'%value)
        elif self.NbDecimals==3:
            editor.setText('%.3f'%value)
        else:
            editor.setText('%.4f'%value)

    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))

class DateColumnDelegate(QItemDelegate):

    def __init__(self, minimum=QDate(), maximum=QDate.currentDate(),
                 format="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = QString(format)


    def createEditor(self, parent, option, index):
        dateedit = QDateEdit(parent)
        dateedit.setDateRange(self.minimum, self.maximum)
        dateedit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        dateedit.setDisplayFormat(self.format)
        dateedit.setCalendarPopup(True)
        return dateedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toDate()
        editor.setDate(value)


    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.date()))


class PlainTextColumnDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(PlainTextColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        return lineedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)

    def setModelData(self, editor, model, index):
        if isinstance(editor,(MyPlainTextEdit,QPlainTextEdit,QTextEdit)):
            model.setData(index, QVariant(editor.toPlainText()))
        else:
            model.setData(index, QVariant(editor.text()))
            

class MyError():
    def __init__(self,parent,error):
        print error
        display=QErrorMessage(parent)
        display.showMessage(error)
        