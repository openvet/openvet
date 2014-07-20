#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
sys.path.append('../VetCore')


from PyQt4 import QtCore, QtGui

from Tables import *





class MyCheckBox(QtGui.QCheckBox):
    def __init__(self,parent=None, tri_state=False):
        super(MyCheckBox,self).__init__(parent)    
        if tri_state :
            self.setTristate()
        
    def Set(self, valeur):
        state=Qt.PartiallyChecked	
        if valeur==0 :
            state=Qt.Unchecked	
        elif valeur>0 :
            state=Qt.Checked
        self.setCheckState(state)
        
        
    def Get(self):
        state=self.checkState()
        if state==Qt.Checked :
            return 1
        if state==Qt.Unchecked	:
            return 0
        return 

class MyLineEdit(QtGui.QLineEdit):
    def __init__(self,parent=None):
        super(MyLineEdit,self).__init__(parent)
        
    def Set(self, valeur):
        self.setText(valeur)
        
    def Get(self):
        return self.text()

class MyDateEdit(QtGui.QDateEdit):
    def __init__(self,parent=None):
        super(MyDateEdit,self).__init__(parent)

    def Set(self, valeur):
        self.setDate(valeur)
        
    def Get(self):
        return self.date()

class MyTextEdit(QtGui.QTextEdit):
    def __init__(self,parent=None):
        super(MyTextEdit,self).__init__(parent)

    def Set(self, valeur):
        self.setText(valeur)
        
    def Get(self):
        return self.toPlainText()        
        
        
class MyComboEspece(QtGui.QComboBox):
    def __init__(self,parent=None):
        super(MyComboEspece,self).__init__(parent)    
        self.listeEnfants=[] #Race est lié à espece
        self.InitialiseListes()
        self.connect(self, QtCore.SIGNAL("currentIndexChanged ( int )"),self.OnCurrentIndexChanged)
        
    def InitialiseListes(self):
        self.tableEspeces=TableSelectAll('Especes', sql='SELECT idEspeces , Espece FROM Especes ORDER BY Espece') #TODO: +/- ajouter champ Actif?
        self.listeEspece = self.tableEspeces.GetListe()
        for espece in self.listeEspece :
            self.addItem(espece)

    def Set(self, id):
        index=self.tableEspeces.GetIndex(id)
        self.setCurrentIndex(index)
            
    def Get(self):
        index=self.currentIndex()
        id=self.tableEspeces.GetId(index)
        return id
        
    def AddEnfant(self, enfant):
        self.listeEnfants.append(enfant)
        
    def OnCurrentIndexChanged(self, index):
        if index > -1 :
            for liste_race in self.listeEnfants :
                id=self.tableEspeces.GetId(index)
                liste_race.OnEspeceChanged(id)

class MyComboRace(QtGui.QComboBox):
    def __init__(self,parent=None):
        super(MyComboRace,self).__init__(parent)    
        self.sql='SELECT idRace , Race FROM Race WHERE Actif'
        self.EspecesActive=-1
        self.SwaptableRaces={}
        self.SwaplisteRaces={}
    def InitialiseListes(self):
        self.clear()
        for race in self.listeRaces :
            self.addItem(race)
    
    def ActualiseListe(self):
        if self.EspecesActive >-1 :
            try :  #vérifie si la liste a déjà été créée
                self.tableRaces=self.SwaptableRaces[self.EspecesActive ]
                self.listeRaces = self.SwaplisteRaces[self.EspecesActive ]
            except :
                recherche_sql=self.sql + ' AND Especes_idEspeces = '+str( self.EspecesActive  )+ ' ORDER BY Race'
                self.tableRaces=TableSelectAll('Race', sql=recherche_sql)
                self.listeRaces = self.tableRaces.GetListe()
                self.SwaptableRaces[self.EspecesActive ] = self.tableRaces  #garde en mémoire les listes
                self.SwaplisteRaces[self.EspecesActive ] = self.listeRaces 
                
            self.InitialiseListes()
                
                
    
    def OnEspeceChanged(self, idespece):
        if self.EspecesActive <> idespece :
            self.EspecesActive=idespece
            self.ActualiseListe()

    def Set(self, id):
        index=self.tableRaces.GetIndex(id)
        self.setCurrentIndex(index)
            
    def Get(self):
        index=self.currentIndex()
        id=self.tableRaces.GetId(index)
        return id

#TODO:   BUG++++++++   si création 2eme comboBox le 1er ne s'affiche pas bien (meme si combo differents ex comboville comboclient)
class MyComboBox(QtGui.QComboBox): #ancienne version, utilisée pour formClient
    """ affiche une liste (nb elements max = limitSql) avec motif de recherche sql, et conservation des resultats de  la 
    recherche dans listeModel + motif2model (évite une requete sql si la recherche a déjà été faite) A FAIRE"""
    def __init__(self,parent=None, nomTable='', sql='', tableliste='', nomchampid=''):

        super(MyComboBox,self).__init__(parent)
        
        if not nomchampid and sql:
            self.nomChampId=sql.split('SELECT')[1].split(',')[0]  #par defaut SELECT id ,...
            
        self.nomChampId=nomchampid
        
            
        
        if nomTable : # nouveau MyComboBox (pour garder compatibilité avec ancien MyComboBox)
            self.listeModel=[]
            self.listeTable=[]
            self.indiceTableEtModel=0
            self.motif2model={}
            self.maxModel=50
            
#            self.maxModel=3 #DEBUG********************************
            
            self.limitSql=' LIMIT 100 '
            self.sqlBase=sql.split('LIMIT')[0]   #enleve LIMIT...
            self.nomTable=nomTable
            if not tableliste :
                sql =  self.sqlBase + self.limitSql
                tableliste = NouvelleTableSelectAll(nomTable, sql=sql) #DEBUG ++++
#                tableliste =   TableSelectAll(nomTable, sql=sql)
            self.listeTable.append(tableliste)
            self.InitialiseCombo(tableliste )
            
            self.connect(self, QtCore.SIGNAL("OnEnter"),self.OnEnter)
            self.connect(self, QtCore.SIGNAL("editTextChanged ( QString  )"),  self.OnEditTextChanged )            
            self.desactivesignaux =False
        
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
        
        
    def SetId(self, id):  #filtre selon l'id (permet de positionner la valeur du  combobox sur l'id correspondant dans la data base
        if not self.nomChampId :
            self.nomChampId=self.sqlBase.split('SELECT')[1].split(',')[0]  #par defaut SELECT id ,...
        motif = self.nomChampId +' = '+str(id)
        self.Filtre(motif)
        
    def Filtre(self, motif):
        if motif in self.motif2model and 'debug'=='annule ce test':    #TODO:  IMPORTANT 
            print 'debug : recupere ancien motif' #BUG NE MARCHE PAS TJRS (popup vide)=>A REVOIR
            nouveaumodel= self.motif2model[motif]
        else :
            sql= self.sqlBase + ' WHERE '+motif + self.limitSql
            table =   self.NouvelleTableSelectAll(self.nomTable, sql=sql)
            nouveaumodel=table.GetNouveauModel()
            self.MemoriseTableModel( table, nouveaumodel, motif)
            self.ChangeModel(nouveaumodel)
            
    def NouvelleTableSelectAll(self, nomTable, sql): #à surcharger dans comboBox dérivés de MyComboBox
        print 'WARNING +++++++  NouvelleTableSelectAll(self, nomTable, sql): #à surcharger dans comboBox dérivés de MyComboBox'
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
            
    def GetId(self, index, colonne_id=0):  #renvoie l'id (cf sql= SELECT id, autres champs FROM...) à partir de l'index  (cf widget curent index)
        #colonne_id=0 si sql = SELECT id, autres champs 
        model=self.model()
        r=model.record(index)  #enregistrement (sql) de la ligne   no index   (lecture de la ligne index: renvoie un Qrecord)
        (valeur, isvalid)=r.value(colonne_id).toInt()   
        if isvalid :
            return valeur            
            
            
    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Return or event.key()==QtCore.Qt.Key_Enter:
            self.emit(QtCore.SIGNAL("OnEnter"))
        else:
            QtGui.QComboBox.keyPressEvent(self,event)

    def OnEnter(self):
        print 'debug'
        
        
    def OnEditTextChanged(self, txt) :
        txt=txt.toUpper()  #TODO: a revoir , pour Personne autoriser les minuscules
#        print txt #debug 
        if not self.desactivesignaux :
            self.desactivesignaux =True     #évite répétition signal lors de changement de motif
            motif=self.PrepareMotifRecherche(txt)
            if motif :
                self.Filtre(motif)
            self.lineEdit().setText(txt)
            self.desactivesignaux =False
                
        
    def PrepareMotifRecherche(self, txt):#a surcharger dans combo dérivés
        return ''
    

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

    def NouvelleTableSelectAll(self, nomTable, sql): # surcharge de MyComboBox.Nouvelle...
        return  TableVille(sql=sql)  #ATTENTION pas self.sql mais new sql
    
    def PrepareMotifRecherche(self, txt):
        if txt :
            
            if txt.endsWith(')') : return  #pas de filtre car txt=une ville complete
            
            (cip, isInt)=txt.toInt()
            if isInt :
                
                txt= ' CIP LIKE "'+txt+'%"' 
            else :
                txt= ' Commune LIKE "'+txt+'%"'
        return txt

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
    cbVille=MyComboBoxVille()
    
#    cbId=QLineEdit()
#    cbVille=QLineEdit()
    
    
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









