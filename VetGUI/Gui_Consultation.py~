# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
from ui_Form_consultation import Ui_MainWindow
from ui_Form_client import Ui_Dialog_client
from ui_Form_animal import Ui_Dialog_animal
sys.path.append('../VetCore')
import Core_Consultation


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    dataClient=''
    dataAnimal=''
    idClient=0
    idAnimal=1
    idConsultation=0
    NewConsultation=True
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.editClient = None
        self.editAnimal = None
        #init dates
        now=QtCore.QDate.currentDate()
        self.dateEdit_consult.setDate(now)
        self.dateEdit_vacciner_start.setDate(now)
        self.dateEdit_vacciner_end.setDate(now)
        self.dateEdit_ordonance.setDate(now)
        self.dateEdit_docDate.setDate(now)
        self.dateTimeEdit_analyse.setDate(now)
        #hide some widget
        self.tableWidget_analyses.setVisible(False)
        self.listWidget_analyse.setVisible(False)
        self.lineEdit_titreImage.setVisible(False)
        self.lineEdit_fichier.setVisible(False)
        self.pushButton_addImage.setVisible(False)
        self.toolButton_fichier.setVisible(False)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)
        #fill comboboxes
        self.MyConsult=Core_Consultation.Consultation()
        self.comboBox_veterinaire.addItems(self.MyConsult.GetConsultants())
        self.comboBox_consultType.addItems(self.MyConsult.GetTypesConsultation())
        self.comboBox_Referant.addItems(self.MyConsult.GetReferants())
        #connect actions
        self.toolButton_addClient.clicked.connect(self.DoClientEdit)
        self.toolButton_addAnimal.clicked.connect(self.DoAnimalEdit)
        self.comboBox_Animal.activated.connect(self.DoGetConsultations)
        self.comboBox_consultType.currentIndexChanged.connect(self.OnTypeConsultation)
        self.connect(self.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationClicked)
        self.toolButton_comment.clicked.connect(self.DoEditCommentaire)
        self.pushButton_valider.clicked.connect(self.DoEditConsultation)
        self.pushButton_Nouveau.clicked.connect(self.OnNewConsultation)
        self.actionQuitter.triggered.connect(self.Mycloseapp)

    def DoClientEdit(self):
        self.dataClient='Mon nom est untel'
        if self.editClient is None:
            self.editClient = FormClient(self)
        if self.editClient.exec_():
            print self.editClient.data
  
    def DoAnimalEdit(self):
        self.dataAnimal='Son nom est minou'
        if self.editAnimal is None:
                self.editAnimal = FormAnimal(self)
        if self.editAnimal.exec_():
            print self.editAnimal.data
            
    def DoGetConsultations(self):
        MyDossier=Core_Consultation.Consultations()
        self.textBrowser_consultations.setText(MyDossier.GetConsultations(self.idAnimal))
        self.splitter.resize(1021,820)
        
    def OnConsultationClicked(self,link):
        self.NewConsultation=False
        self.idConsultation=int(link.toString().toAscii()[2:])
        if link.toString().toAscii()[1]=='C':
            self.FillFormConsultation()
        if link.toString().toAscii()[1]=='N':
            self.DoNewConsultation()   
        if link.toString().toAscii()[1]=='B':
            print 'view biologie'
        if link.toString().toAscii()[1]=='I':
            print 'view Images'
        if link.toString().toAscii()[1]=='c':
            print 'view Chirurgies'
        if link.toString().toAscii()[1]=='O':
            print 'view Ordonnance'
        if link.toString().toAscii()[1]=='T':
            print 'view Plan thérapeutique'     
      
    def FillFormConsultation(self):
        res=self.MyConsult.GetConsultation(self.idConsultation)
        self.MyConsult.FormatConsultation(res[0])
        self.dateEdit_consult.setDate(QtCore.QDate(QtCore.QDate(int(self.MyConsult.Date[6:]),int(self.MyConsult.Date[3:5]),int(self.MyConsult.Date[:2]))))
        self.comboBox_veterinaire.setCurrentIndex(self.comboBox_veterinaire.findText(QtCore.QString(self.MyConsult.Consultant)))
        self.comboBox_consultType.setCurrentIndex(self.comboBox_consultType.findText(QtCore.QString(self.MyConsult.Type)))
        if len(self.MyConsult.Referant)>0:
            self.comboBox_Referant.setCurrentIndex(self.comboBox_Referant.findText(QtCore.QString(self.MyConsult.Referant)))
        self.textEdit_consultObs.setText(QtCore.QString(self.MyConsult.Observations))
        self.textEdit_consultTrait.setText(QtCore.QString(self.MyConsult.Traitements))
        self.toolButton_comment.setToolTip(QtCore.QString(self.MyConsult.Commentaire))
        self.splitter.resize(1021,470)
        
    def OnTypeConsultation(self):
        if self.comboBox_consultType.currentText()==QtCore.QString("Référée".decode('utf8')):
            self.label_Referant.setVisible(True)
            self.comboBox_Referant.setVisible(True)
        else:
            self.label_Referant.setVisible(False)
            self.comboBox_Referant.setVisible(False)
            
    def DoEditConsultation(self):
        self.MyConsult.IdConsultation=self.idConsultation
        q=self.dateEdit_consult.date()
        self.MyConsult.Date='%02i/%02i/%i'%(q.day(),q.month(),q.year())
        self.MyConsult.idConsultant=self.comboBox_veterinaire.currentIndex()
        self.MyConsult.Consultant=self.comboBox_veterinaire.currentText().toUtf8()
        self.MyConsult.idTypeConsultation=self.comboBox_consultType.currentIndex()
        self.MyConsult.Type=self.comboBox_consultType.currentText().toUtf8()
        if self.comboBox_Referant.isVisible():
            self.MyConsult.idReferant=self.comboBox_Referant.currentIndex()
            self.MyConsult.Referant=self.comboBox_Referant.currentText().toUtf8()
        else:
            self.MyConsult.idReferant=None
        self.MyConsult.Observations=self.textEdit_consultObs.toPlainText().toUtf8()
        self.MyConsult.Traitements=self.textEdit_consultTrait.toPlainText().toUtf8()
        self.MyConsult.idAnimal=self.idAnimal
        self.MyConsult.SaveData(self.NewConsultation)
        self.NewConsultation=True
             
    def DoEditCommentaire(self):
        form=FormComment()
        form.plainTextEdit.insertPlainText(self.MyConsult.Commentaire)
        if form.exec_():
            self.MyConsult.Commentaire=form.plainTextEdit.toPlainText().toUtf8()
            self.toolButton_comment.setToolTip(QtCore.QString(self.MyConsult.Commentaire.data().decode('utf8')))
      
    def OnNewConsultation(self):
        self.NewConsultation=True
        self.dateEdit_consult.setDate(QtCore.QDate.currentDate())
        self.comboBox_veterinaire.setCurrentIndex(0)
        self.comboBox_consultType.setCurrentIndex(0)
        self.comboBox_Referant.setCurrentIndex(0)
        self.label_Referant.setVisible(False)
        self.comboBox_Referant.setVisible(False)
        self.textEdit_consultObs.clear()
        self.textEdit_consultTrait.clear()
        self.toolButton_comment.setToolTip(QtCore.QString('Ajouter un Commentaire'))
        self.splitter.resize(1021,470) 
        
    def Mycloseapp(self):
        self.close()


class FormClient(QtGui.QDialog, Ui_Dialog_client):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        print parent.dataClient
        self.setupUi(self)
        self.data=parent.dataClient+' rien'

class FormAnimal(QtGui.QDialog, Ui_Dialog_animal):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        print parent.dataAnimal
        self.setupUi(self)

class FormComment(QtGui.QDialog):
    def __init__(self,parent=None):
        super(FormComment,self).__init__(parent)
        self.resize(400, 255)
        self.setWindowTitle("Edition Consultation")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 17))
        self.label.setText("Entrez votre commentaire :")
        self.plainTextEdit = QtGui.QPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 361, 141))
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
