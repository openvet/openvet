#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
sys.path.append('../VetCore')


from PyQt4 import QtCore, QtGui

from Tables import *


class MyComboBox(QtGui.QComboBox):
    """ affiche une liste (nb elements max = limitSql) avec motif de recherche sql, et conservation des resultats de  la 
    recherche dans listeModel + motif2model (évite une requete sql si la recherche a déjà été faite)"""
    def __init__(self,parent=None, nomTable='', sql='', tableliste=''):

        super(MyComboBox,self).__init__(parent)
        
        if nomTable : # compatibilité avec ancien MyComboBox
            self.listeModel=[]
            self.listeTable=[]
            self.indiceTableEtModel=0
            self.motif2model={}
            self.maxModel=50
            self.limitSql=' LIMIT 100 '
            self.sqlBase=sql.split('LIMIT')[0]   #enleve LIMIT...
            self.nomTable=nomTable
            if not tableliste :
                sql =  self.sqlBase + self.limitSql
                tableliste =   TableSelectAll(nomTable, sql=sql)
            self.listeTable.append(tableliste)
            self.InitialiseCombo(tableliste )
            
            self.connect(self, QtCore.SIGNAL("OnEnter"),self.OnEnter)
            
        
        
    def InitialiseCombo(self, table ):
        
        self.setEditable(True)
        
        model=table.GetModel()
        self.setModel(model)   
        self.listeModel.append(model)
    
        view=   QTableView() 
        view.verticalHeader().hide() #pas d'étiquettes pour les colonnes ou lignes
        view.horizontalHeader().hide()

        self.setView(view)
        self.setModelColumn(1) #utilise colonne1 (linedit), colonne 0 = id /
        self.setFixedWidth(250)
        view.setColumnWidth(1, 250)
        view.setColumnHidden(0, True)#cache colonne 0 (id ) dans popup du comboBox        
        
    def ChangeModel(self, model):
        self.setModel(model)   
        
    def Filtre(self, motif):
        if motif in self.motif2model :
            nouveaumodel= self.motif2model[motif]
        else :
            sql= self.sqlBase + ' WHERE '+motif + self.limitSql
            table =   self.NouvelleTableSelectAll(self.nomTable, sql=sql)
            nouveaumodel=table.GetNouveauModel()
            self.MemoriseTableModel( table, nouveaumodel, motif)
            self.ChangeModel(nouveaumodel)
            
    def NouvelleTableSelectAll(self, nomTable, sql): #à surcharger dans comboBox dérivés de MyComboBox
        return  TableSelectAll(nomTable, sql)
            
    def MemoriseTableModel(self, table, model, motif):
        taille= len (self.listeTable)  
        if taille < self.maxModel :  #on remplit les tableaux de 0 à 49  (maxModel=50)
            self.motif2model[motif] = model
            self.listeTable.append(table)
            self.listeModel.append(model)
            self.indiceTableEtModel+=1     #attention indiceTableEtModel = taille -1

        else : #on repart de indice = 0 -> 49 (remarque taille reste toujours = 50)
            if self.indiceTableEtModel  == self.maxModel -1  :   #quand taille passe de  49 à 50   indiceTableEtModel  =49
                self.indiceTableEtModel  = 0
            else :
                self.indiceTableEtModel  += 1   #boucle de 0 à 49 indéfiniement
            
            ancienmodel=self.listeModel[self.indiceTableEtModel]
            self.listeTable[ self.indiceTableEtModel ] = table
            self.listeModel[ self.indiceTableEtModel ] = model
            for motif in self.motif2model.keys() : #retirer ancienmodel
                if self.motif2model[motif] == ancienmodel :
                    del( self.motif2model[motif])
                    break
            
    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Return or event.key()==QtCore.Qt.Key_Enter:
            self.emit(QtCore.SIGNAL("OnEnter"))
        else:
            QtGui.QComboBox.keyPressEvent(self,event)

    def OnEnter(self):
        print 'debug'

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




class MyComboBoxVille(MyComboBox):

    def __init__(self, parent=None):
        nomTable='Commune'
        self.sql="""SELECT idCommune, 
                    CONCAT ( Commune, ' (',CIP , ')' )
                    FROM Commune
                """
        self.limitSql=' LIMIT 100 '
        self.sql=self.sql+self.limitSql
                
        liste = TableVille(sql=self.sql)
        super(MyComboBoxVille,self).__init__(parent, nomTable, self.sql, tableliste=liste)

    def NouvelleTableSelectAll(self, nomTable, sql): #à surcharger dans comboBox dérivés de MyComboBox
        return  TableVille(sql=sql)  #ATTENTION pas self.sql mais new sql
    
    


class MyTableWidget(QtGui.QTableWidget):
	def __init__(self,parent=None):
		super(MyTableWidget,self).__init__(parent)
		
	def keyReleaseEvent(self,event):
		if event.key()==QtCore.Qt.Key_Return or event.key()==QtCore.Qt.Key_Enter:
			self.emit(QtCore.SIGNAL("OnEnter"))
		else:
			QtGui.QTableWidget.keyPressEvent(self,event)
	#TODO menu right-click




if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    w= QMainWindow()
    w.setGeometry(100, 100, 500  , 500)
    
    
    layout = QVBoxLayout()
    
    cb=MyComboBoxVille()
    layout.addWidget(cb)
    
    cb.Filtre(' Commune LIKE "%LACR%" OR (CIP>59999 AND CIP<61000   )')
    
    
    cbId=QComboBox()
    cbVille=QComboBox()
    
    cbId=QLineEdit()
    cbVille=QLineEdit()
    
    
    layout.addWidget(cbId)
    layout.addWidget(cbVille)
    
    
    
#TEST MAPPER
    sqlville="SELECT CIP, Commune FROM Commune LIMIT 100"
    ville=NouvelleTableVille(sql=sqlville, independant=True)
#    model2 = ville.GetNouveauModel(independant=True)  # attention GetModel = model de class avec 1er sql  BUG CHANGE LE MDEL PRECEDANT
#    TEST model2 pour avoir CIP au lieu de id
    mapper = QDataWidgetMapper()
    mapper.setModel(cb.model() )
#    mapper.setModel(model2 )
#    mapper.addMapping(cbId, 0, "currentIndex")
    mapper.addMapping(cbId, 0)
    mapper.addMapping(cbVille, 1)    
#    mapper.addMapping(cbVille, 1, 'currentIndex')    
    mapper.toFirst()
# FIN TEST MAPPER    
    
    centralW= QWidget()
    centralW.setLayout(layout) 
    w.setCentralWidget(centralW)
    w.show()
    sys.exit(app.exec_())









