#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
sys.path.append('../VetCore')


from PyQt4 import QtCore, QtGui

from Tables import *



class MyComboBox(QtGui.QComboBox):
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
                tableliste =   TableSelectAll(SqlModelTable, sql=sql)
            self.listeTable.append(tableliste)
            self.InitialiseCombo(tableliste )
            
            self.connect(self, QtCore.SIGNAL("OnEnter"),self.OnEnter)
            
            self.connect(self, QtCore.SIGNAL("editTextChanged ( QString  )"),  self.OnEditTextChanged )            
            #DEBUG2 ++++++++++
            
            
            self.desactivesignaux =False
            
            
            
        
    def InitialiseCombo(self, table ):
        
        self.setEditable(True)
#        
        model=table.GetModel()
        self.setModel(model)   
        self.listeModel.append(model)
#    
        view=   QTableView(self) 
        view.verticalHeader().hide() #pas d'étiquettes pour les colonnes ou lignes
        view.horizontalHeader().hide()
        view.setColumnWidth(1, 250)

#        view.setColumnHidden(0, True)#cache colonne 0 (id ) dans popup du comboBox       ATTENTION NE MARCHE PAS SI AVANT SETVIEW !!!! 

#        view.setColumnHidden(1, True)#cache colonne 0 (id ) dans popup du comboBox        

#        view=   QListView(self) #DEBUG+++++++++++
        

        self.setView(view)
        
        view.setColumnHidden(0, True)#cache colonne 0 (id ) dans popup du comboBox        
        
        self.setModelColumn(1) #utilise colonne1 (linedit), colonne 0 = id /
        view.setColumnWidth(1, 500) #marche pas SI FAIT AVANT SETMODEL!!!!
        
        self.setFixedWidth(250)

        
#        model=table.GetModel()
#        self.setModel(model)   
#        self.listeModel.append(model)        
        
    def RecreeView(self):
        view=   QTableView(self) 
        view.verticalHeader().hide() #pas d'étiquettes pour les colonnes ou lignes
        view.horizontalHeader().hide()
        view.setColumnWidth(1, 250)
        self.setView(view)
        view.setColumnHidden(0, True)#cache colonne 0 (id ) dans popup du comboBox        
        self.setModelColumn(1) #utilise colonne1 (linedit), colonne 0 = id /
        view.setColumnWidth(1, 500) #marche pas SI FAIT AVANT SETMODEL!!!!
        
        
    def ChangeModel(self, model):
        #DEBUG +++++++ cree nouvelle view
#        view=   QTableView(self) 
#        view.verticalHeader().hide() #pas d'étiquettes pour les colonnes ou lignes
#        view.horizontalHeader().hide()
#        self.setView(view)
        
        m=self.model()
        self.listeModel.append(m)
        self.setModel(model)   
        
#        v=self.view()
#        v.setModel(model) #DEBUG++++++++++

#        self.update()
        
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
            table =   self.NouvelleSqlModelTable(self.nomTable, sql=sql)
            nouveaumodel=table.GetNouveauModel()
            self.MemoriseTableModel( table, nouveaumodel, motif)
            self.ChangeModel(nouveaumodel)
            
    def NouvelleSqlModelTable(self, nomTable, sql): #à surcharger dans comboBox dérivés de MyComboBox
        print 'WARNING++++++++++++++++   NouvelleSqlModelTable à surcharger dans comboBox dérivés de MyComboBox'
        return  SqlModelTable(nomTable, sql)
            
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
        pass
#        print 'debug'
        
        
    def OnEditTextChanged(self, txt, autorise_minuscules=False) :
        if not autorise_minuscules:
            txt=txt.toUpper()  # pour Personne autoriser les minuscules
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
    



class MyComboBox2(QtGui.QComboBox):
    """ affiche une liste (nb elements max = limitSql) avec motif de recherche sql, et conservation des resultats de  la 
    recherche dans listeModel + motif2model (évite une requete sql si la recherche a déjà été faite) A FAIRE"""
    def __init__(self,parent=None, nomTable='', sql='', tableliste='', nomchampid=''):

        super(MyComboBox2,self).__init__(parent)
        
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
                tableliste =   TableSelectAll(nomTable, sql=sql)
            self.listeTable.append(tableliste)
            self.InitialiseCombo(tableliste )
            
            self.connect(self, QtCore.SIGNAL("OnEnter"),self.OnEnter)
            self.connect(self, QtCore.SIGNAL("editTextChanged ( QString  )"),  self.OnEditTextChanged )            
            self.desactivesignaux =False
        
    def InitialiseCombo(self, table ):
        
        self.setEditable(True)
        
#        model=table.GetModel()
#        self.setModel(model)   
#        self.listeModel.append(model)
    
        view=   QTableView(self) 
        view.verticalHeader().hide() #pas d'étiquettes pour les colonnes ou lignes
        view.horizontalHeader().hide()

        self.setView(view)
        self.setModelColumn(1) #utilise colonne1 (linedit), colonne 0 = id /
        self.setFixedWidth(250)
        view.setColumnWidth(1, 250)
        view.setColumnHidden(0, True)#cache colonne 0 (id ) dans popup du comboBox        
        
        model=table.GetModel()
        self.setModel(model)   
        self.listeModel.append(model)
        
        
        
        
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
        print 'WARNING+++++NouvelleTableSelectAll à surcharger '
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
        pass
#        print 'debug'
        
        
    def OnEditTextChanged(self, txt, autorise_minuscules=False) :
        if not autorise_minuscules:
            txt=txt.toUpper()  # pour Personne autoriser les minuscules
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

##DEBUG+++++++++
#        self.sql="""SELECT  
#                    CONCAT ( Commune, ' (',CIP , ')' )
#                    FROM Commune
#                """
#                
                
                
        self.limitSql=' LIMIT 100 '
        self.sql=self.sql+self.limitSql
                
        liste = ModelTableVille(sql=self.sql)
        super(MyComboBoxVille,self).__init__(parent, nomTable, self.sql, tableliste=liste)

    def NouvelleSqlModelTable(self, nomTable, sql): # surcharge de MyComboBox.Nouvelle...
        return  ModelTableVille(sql=sql)  #ATTENTION pas self.sql mais new sql
    
    def PrepareMotifRecherche(self, txt):
        if txt :
            
            if txt.endsWith(')') : return  #pas de filtre car txt=une ville complete
            
            (cip, isInt)=txt.toInt()
            if isInt :
                
                txt= ' CIP LIKE "'+txt+'%"' 
            else :
                txt= ' Commune LIKE "'+txt+'%"'
        return txt



class MyComboBoxVille2(MyComboBox2):

    def __init__(self, parent=None):
        nomTable='Commune'
        self.sql="""SELECT idCommune, 
                    CONCAT ( Commune, ' (',CIP , 'testsql)' )
                    FROM Commune
                """

##DEBUG+++++++++
#        self.sql="""SELECT  
#                    CONCAT ( Commune, ' (',CIP , ')' )
#                    FROM Commune
#                """
#                
                
                
        self.limitSql=' LIMIT 100 '
        self.sql=self.sql+self.limitSql
                
        liste = ModelTableVille2(sql=self.sql)
        super(MyComboBoxVille2,self).__init__(parent, nomTable, self.sql, tableliste=liste)

    def NouvelleSqlModelTable(self, nomTable, sql): # surcharge de MyComboBox.Nouvelle...
        return  ModelTableVille2(sql=sql)  #ATTENTION pas self.sql mais new sql
    
    def PrepareMotifRecherche(self, txt):
        if txt :
            
            if txt.endsWith(')') : return  #pas de filtre car txt=une ville complete
            
            (cip, isInt)=txt.toInt()
            if isInt :
                
                txt= ' CIP LIKE "'+txt+'%"' 
            else :
                txt= ' Commune LIKE "'+txt+'%"'
        return txt



class MyComboBoxClient(MyComboBox):  #DEBUG+++++++++++
    def __init__(self, parent=None):
        nomTable='viewPersonne'
        self.sql="""SELECT idPersonne, 
        CONCAT (viewPersonne.Nom," ",viewPersonne.Prenom," (",Commune,")") ,
        (SELECT GROUP_CONCAT(Nom) FROM Animal LEFT JOIN ClientAnimalRef ON Animal.idAnimal=ClientAnimalRef.Animal_idAnimal 
        WHERE Client_idClient=idPersonne) FROM viewPersonne 
        """
        self.limitSql=' LIMIT 100 '
        self.sql=self.sql+self.limitSql
                
        liste = TableListeClient(sql=self.sql)
        super(MyComboBoxClient,self).__init__(parent, nomTable, self.sql, tableliste=liste)
        self.setFixedWidth(450)
        

    def NouvelleTableSelectAll(self, nomTable, sql): # surcharge de MyComboBox.Nouvelle...
        return  TableListeClient(sql=sql)  #ATTENTION pas self.sql mais new sql
    
    def PrepareMotifRecherche(self, txt):
#        if txt :
#            
#            if txt.endsWith(')') : return  #pas de filtre car txt=une ville complete
#            
#            (cip, isInt)=txt.toInt()
#            if isInt :
#                
#                txt= ' CIP LIKE "'+txt+'%"' 
#            else :
#                txt= ' Commune LIKE "'+txt+'%"'
        txt=' Nom LIKE "'+txt+'%"'
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

class WindowsTest(QtGui.QMainWindow):

    def __init__(self):
        super(WindowsTest, self).__init__()

        self.initUI()

    def initUI(self):

        layout = QHBoxLayout()
        centralW= QWidget()
        centralW.setLayout(layout) 
        self.setCentralWidget(centralW)
        
        
        self.qframe1=QFrame()
        layout.addWidget(self.qframe1)

        self.cb=MyComboBoxVille(self.qframe1)
#        layout.addWidget(self.cb)
        self.cb.Filtre(' Commune LIKE "%LACR%" OR (CIP>59999 AND CIP<61000   )')


#        cbId=QComboBox()
#        cbVille=QComboBox()
#        
#        cbId=QLineEdit()
#        cbVille=QLineEdit()
#        
#        
#        layout.addWidget(cbId)
#        layout.addWidget(cbVille)
#        
#        cbclient=MyComboBoxClient()
#        layout.addWidget(cbclient)
##        

        self.qframe2=QFrame()
        layout.addWidget(self.qframe2)

        self.cbville2=MyComboBoxVille2(self.qframe2) #debug
#        layout.addWidget(self.cbville2)
#Mycomboboxville   Mycomboboxville2  => marche pas => pb = model

        b=QPushButton('debug1')
        layout.addWidget(b)
        b.clicked.connect(self.Onbclicked)

        b=QPushButton('debug2')
        layout.addWidget(b)
        b.clicked.connect(self.Onbclicked2)


        self.setGeometry(100, 100, 1500  , 1500)
        self.show()

    def Onbclicked2(self):        
        pass


    def Onbclicked(self):        
        
        v=self.cb.view()
        m=self.cb.model()
        
        v=QTableView()
        v.setModel(m)
        v.show()
        m=self.cb.setView(v)
        
        v.update()
        v.repaint()
        v.show()
        v.setModel(m)
        
        v=self.cbville2.view()
        m=self.cbville2.model()
        v.update()
        v.repaint()
        v.show()
        v.setModel(m)
        
        
        print 'cb'
#        print self.cb
#        print self.cb.model()
        print self.cb.view()
        print 'cbville2'
#        print self.cbville2
#        print self.cbville2.model()
        print self.cbville2.view()
    
##TEST MAPPER
#    sqlville="SELECT CIP, Commune FROM Commune LIMIT 100"
#    ville=NouvelleTableVille(sql=sqlville)
##    model2 = ville.GetNouveauModel(independant=True)  # attention GetModel = model de class avec 1er sql  BUG CHANGE LE MDEL PRECEDANT
##    TEST model2 pour avoir CIP au lieu de id
#    mapper = QDataWidgetMapper()
#    mapper.setModel(cb.model() )
##    mapper.setModel(model2 )
##    mapper.addMapping(cbId, 0, "currentIndex")
#    mapper.addMapping(cbId, 0)
#    mapper.addMapping(cbVille, 1)    
##    mapper.addMapping(cbVille, 1, 'currentIndex')    
#    mapper.toFirst()
## FIN TEST MAPPER    
    
        



if __name__ == '__main__':
    
    
    app = QtGui.QApplication(sys.argv)
    window = WindowsTest()
    window.show()
    sys.exit(app.exec_())    
    
    
    









