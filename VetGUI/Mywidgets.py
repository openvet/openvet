#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyComboBox(QComboBox):
	def __init__(self,parent=None):
		super(MyComboBox,self).__init__(parent)
#	def focusInEvent(self, event):
#			self.emit(QtCore.SIGNAL("focusIn"))
#			QtGui.QWidget.focusInEvent(self, event)
#	def mousePressEvent(self, event):
#			self.emit(QtCore.SIGNAL("focusIn"))
#			QtGui.QWidget.mousePressEvent(self, event)

	def keyPressEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QComboBox.keyPressEvent(self,event)

# 	def Fill(self,function,Remarque=False,Color=False):
# 		self.clear()
# 		lst=function
# 		for i in lst:
# 			self.addItem(i[1],i[0])
# 		colors=[Qt.black,Qt.red,Qt.green]
# 		for i in range(self.count()):
# 			if Remarque:
# 				try:
# 					self.setItemData(i,QVariant(lst[i][2]),Qt.ToolTipRole)
# 				except:
# 					pass
# 			if Color:
# 				try:
# 					self.setItemData(i,colors[lst[i][3]],Qt.BackgroundColorRole)
# 				except:
# 					pass
					
	def GetData(self):
		value=self.itemData(self.currentIndex()).toInt()
		if value[1]:
			idata=value[0]
		else:
			idata=None
			print 'Erreur d\'index: %s,\" %s\"'%(self.objectName(),self.currentText())
		return idata
	
	def Setid(self,idTable):
		index=[i for i,j in enumerate(self.model().listdata) if idTable==j[0].toInt()[0]]
		if len(index)==0:
			self.setCurrentIndex(0)
		else:
			self.setCurrentIndex(index[0])
	
	def Getid(self):
		return self.itemData(self.currentIndex(),Qt.UserRole).toInt()[0]
	
	def GetRemarque(self):
		return self.itemData(self.currentIndex(),Qt.ToolTipRole).toString()

	def GetProperty(self,index):
		return self.itemData(self.currentIndex(),33+index)

	def GetDeleted(self):
		return self.itemData(self.currentIndex(),33)

class MyTableWidget(QTableWidget):
	def __init__(self,parent=None):
		super(MyTableWidget,self).__init__(parent)
		
	def keyReleaseEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QTableWidget.keyPressEvent(self,event)


class MyPlainTextEdit(QPlainTextEdit):
	def __init__(self,parent=None):
		super(MyPlainTextEdit,self).__init__(parent)
		self.MaxLength=0
		self.textChanged.connect(self.OnLimitLength)
		
	def SetMaxLength(self,length):
		self.MaxLength=length
		
	def OnLimitLength(self):
		if self.MaxLength==0:
			return
		text=self.toPlainText()
		if text.length()>self.MaxLength:
			self.setPlainText(text.remove(text.length()-1,1))
			self.moveCursor(QTextCursor.End)
	
	def setText(self,value):
		self.setPlainText(value)
			
class MyTableView(QTableView):
	def __init__(self,parent=None):
		super(MyTableView,self).__init__(parent)
	
	def keyReleaseEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QTableWidget.keyPressEvent(self,event)
		
	def autoResize(self,varcol):
		#redimentionne avec la colonne varcol étant la plus large possible, sous réserve que les autres colonnes affichent les données en entier.
		self.resizeColumnsToContents()
		if self.model() is None:
			return
		tot=6+sum([self.columnWidth(i) for i in range(self.model().columnCount()) if i!=varcol])
		self.setColumnWidth(varcol,self.width()-tot)
