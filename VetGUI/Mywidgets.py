import sys
from PyQt4 import QtCore, QtGui

class MyComboBox(QtGui.QComboBox):
	def __init__(self,parent=None):
		super(MyComboBox,self).__init__(parent)
#	def focusInEvent(self, event):
#	        self.emit(QtCore.SIGNAL("focusIn"))
#	        QtGui.QWidget.focusInEvent(self, event)
#	def mousePressEvent(self, event):
#	        self.emit(QtCore.SIGNAL("focusIn"))
#	        QtGui.QWidget.mousePressEvent(self, event)
	def keyPressEvent(self,event):
		if event.key()==QtCore.Qt.Key_Return or event.key()==QtCore.Qt.Key_Enter:
			#print "enter"
			self.emit(QtCore.SIGNAL("OnEnter"))
		else:
			QtGui.QComboBox.keyPressEvent(self,event)

	def Fill(self,function):
		self.clear()
		lst=function
		for i in lst:
			self.addItem(i[1],i[0])
			
	
	def GetData(self):
		value=self.itemData(self.currentIndex()).toInt()
		if value[1]:
			idata=value[0]
		else:
			idata=None
			print 'Erreur d\'index: %s,\" %s\"'%(self.objectName(),self.currentText())
		return idata

class MyTableWidget(QtGui.QTableWidget):
	def __init__(self,parent=None):
		super(MyTableWidget,self).__init__(parent)
		
	def keyReleaseEvent(self,event):
		if event.key()==QtCore.Qt.Key_Return or event.key()==QtCore.Qt.Key_Enter:
			self.emit(QtCore.SIGNAL("OnEnter"))
		else:
			QtGui.QTableWidget.keyPressEvent(self,event)
	#TODO menu right-click
