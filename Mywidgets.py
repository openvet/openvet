import sys
from PyQt4 import QtCore, QtGui

class MycomboBox(QtGui.QComboBox):
    def __init__(self,parent=None):
        super(MycomboBox,self).__init__(parent)
        self.setEditable(True)
#   def focusInEvent(self, event):
#           self.emit(QtCore.SIGNAL("focusIn"))
#           QtGui.QWidget.focusInEvent(self, event)
#   def mousePressEvent(self, event):
#           self.emit(QtCore.SIGNAL("focusIn"))
#           QtGui.QWidget.mousePressEvent(self, event)
#   def keyPressEvent(self,event):
#       if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
#           self.emit(QtCore.SIGNAL("OnEnter"))
#           QtGui.QWidget.keyPressEvent(self,event)
#Fill(Function)
