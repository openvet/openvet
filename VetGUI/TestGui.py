import sys
from PyQt4 import QtCore, QtGui

class Form(QtGui.QDialog):
    def __init__(self):
        self.line=QtGui.QLineEdit("zob ici:")
#         self.my=QtGui.QListWidget(self)
#         self.my.addItem("zob")
        
app=QtGui.QApplication(sys.argv)
form=Form()
form.show()
app.exec_()
        