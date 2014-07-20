# -*- coding: utf8 -*-


import sys
sys.path.append('..')

import adodb  #, MySQLdb
import string
from string import *
from types import *

import config
from datetime import *

#from PyQt4 import QtCore, QtGui  #, Qt
from PyQt4.Qt import *


#
#USER=config.user
#PWD=config.password
DATABASE=config.database
IDUSER=config.IDUSER
AFFICHE_CONSOLE=config.DEBUG_AFFICHE_MESSAGE_CONSOLE

class DataBase:
    """gère la connexion et l'exécution de requêtes sql
    input : nom de la base, user, password"""
    
    global Connection_globale, DicoLastId, ListeErreurTransaction
    Connection_globale = None
    DicoLastId={}
    ListeErreurTransaction=[]
    QDataBase=''



    def __init__(self,nomD=config.database, USER=config.user, PWD=config.password, HOST=config.host):
        self.nomDB=nomD
        self.user=USER
        self.pwd=PWD
        self.host=HOST
        self.InitialiseDB()
        
    def InitialiseDB(self): # a surcharger
        pass
    

    def LastIdTable(self, table):
        global DicoLastId
        try :
            lastid= DicoLastId[table.upper()]
        except :
            lastid=0
        return lastid


    def StartTransaction(self):#Attention 1seule transaction à la fois
        global Connection_globale, DicoLastId,  ListeErreurTransaction
        erreur=''
        if Connection_globale :
            erreur='ERREUR/WARNING : 1 transation est dejà en cours'
            if AFFICHE_CONSOLE :
                print erreur
            return (  [Connection_globale, erreur] )
                
        else  :
            result = self.Connection()
            if type(result) == type('string') : # result = erreur
                ListeErreurTransaction.append(result)
                Connection_globale=None
            else :
                Connection_globale=result
                DicoLastId={}
                ListeErreurTransaction=[]
        
        result=self.ExecuteSQL('start transaction')
        return (  [Connection_globale, erreur] )
            
    def Commit(self):
        global Connection_globale, DicoLastId, ListeErreurTransaction
        self.ExecuteSQL('commit')
        Connection_globale.Close()
        Connection_globale=None
        DicoLastId={}
        ListeErreurTransaction=[]
        
        
    def Rollback(self):
        global Connection_globale, DicoLastId, ListeErreurTransaction
        self.ExecuteSQL('rollback')
        Connection_globale.Close()
        Connection_globale=None            
        DicoLastId={}
        ListeErreurTransaction=[]
        
    
    def PrintDB(self):
        print self.nomDB
        
    def ConnectionQDataBase(self):
        db = QSqlDatabase("QMYSQL")
        db.setHostName(self.host)
        db.setDatabaseName(self.nomDB)
        db.setUserName(self.user)
        db.setPassword(self.pwd)
        ok = db.open()
        if ok : 
            self.__class__.QDataBase=db
            return db
        else :
            erreur=db.lastError()
            return erreur.text()
            
            
    def GetQDataBase(self):
        if not self.__class__.QDataBase:
            self.ConnectionQDataBase
        return self.__class__.QDataBase

    def Connection(self):
        """se connecte à la base et renvoie une connexion"""
        try :
            conn = adodb.NewADOConnection('mysql') 
            conn.Connect(self.host,self.user,self.pwd,self.nomDB)  
        except :
            msg="Erreur Table_Base.py classDataBase Connection(self) ************* VERIFIEZ database + password (+/-config.py)  ******"
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg
        return conn #ou msg erreur=> tester type(conn)
        
    def QSqlQueryModel(self, sql, query_model=None):
        db_conn=self.ConnectionQDataBase()
        if not ( 'QSqlDatabase' in str(type(db_conn))) :
            return "Erreur Table_Base.py ConnectionQDataBase()  :"+str(db_conn)
        if not query_model :
            query_model = QSqlQueryModel()
        query_model.setQuery( sql,  db_conn)
        err = query_model.lastError()
        if err.isValid() :
            return err.text()
        else :
            res=query_model.setHeaderData(1, Qt.Horizontal, "Nom")
#            res=query_model.setHeaderData(0, Qt.Horizontal, "id")
            return query_model           
    
    def RechercheSQL_liste(self,requete):  
        """input : requête sql
        return : liste résultats ou msg d'erreur (tester type)"""
        conn = self.Connection() 
        if type(conn)==type('str') : return conn  #= msg d'erreur
        try:
            cursor = conn.Execute(requete)
            info = cursor.RecordCount( )
            liste = []
            while not cursor.EOF:  #lit les lignes de la requete et place dans la liste 
                        uneligne = cursor.fields
                        liste.append(uneligne)
                        cursor.MoveNext() 
            conn.Close()
        except :
            msg="Erreur Table_Base.py classDataBase RechercheSQL_liste() "
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg            
        return (liste)
    
    
    def RechercheSQL_dico(self,requete):  
        conn = self.Connection() 
        if type(conn)==type('str') : return conn  #= msg d'erreur
        try :
            dico = conn.GetDict(requete)
        except :
            msg="Erreur Table_Base.py RechercheSQL_dico() "
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg                        
        return dico
    
    def RechercheSQL_tableau(self,requete):  
        """résultats d'une requête sql sous forme tableau, ou msg erreur"""
        conn = self.Connection() 
        if type(conn)==type('str') : return conn  #= msg d'erreur
        try :
            dico = conn.GetAll(requete)
        except :
            msg="Erreur Table_Base.py RechercheSQL_tableau() "
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg    
        return dico

    
    def ExecuteSQL(self,requete, conn=None):   
        """ requête= uniquement de modification (pas de recherche) \            
        return = nb de lignes modifiees ou msg d'erreur (tester type)"""
        global Connection_globale, DicoLastId 
        result=''
        nouvelle_connection=False
        # création si nécessaire d'une connection
        if not conn : #utilise en 1er la connection passee en parametre sinon Connection_globale sinon en crée une.
            if Connection_globale :
                conn = Connection_globale
            else :
                try :
                    nouvelle_connection=True
                    conn = adodb.NewADOConnection('mysql')  #renvoie -1 si erreur
                    conn.Connect(self.host,self.user,self.pwd,self.nomDB)  
                except :
                    result = "Erreur Database.ExecutSQL : err connection"
                    resut+='\n'+str(sys.exc_info()[1])
                    return result
        #execute la requète
        try:
            if 'NULL' in requete : #TODO: DEBUG ++++++++++++++++  semble ok
                requete=requete.replace('"NULL"','NULL' )  # remplace la chaine de caractere "NULL" par la valeur NULL  
            cursor = conn.Execute(requete)
            result=cursor.Affected_Rows()
            
            if 'INSERT' in requete.upper():
                lastid=cursor.Insert_ID()
                requete=requete.upper()
                table= requete.split('INTO')[1].split('SET')[0].split('VALUE')[0] #nom table = entre INTO et SET ou VALUE
                table=table.replace(' ', '')
                DicoLastId[table]=lastid

            if nouvelle_connection: #ne fait pas de commit si on utilise une connection globale => permet executer plusieurs sql puis commit
                conn.CommitTrans( )
        except :
            result ="Erreur Database.ExecutSQL Execution "+str(requete)+" "+str(result)
            result+='\n'+str(sys.exc_info()[1])
            if not nouvelle_connection :
                        ListeErreurTransaction.append(result)
            return result
            
        if nouvelle_connection: #si la connection n'a pas été créée ne la ferme pas
            conn.Close()
        return result
                                    
    def ListeErreurTransaction(self):
        return ListeErreurTransaction
    
    def AjouteErreurTransaction(self, err): #uniquement lors transaction
        global Connection_globale, ListeErreurTransaction
        if Connection_globale :
            ListeErreurTransaction.append(err)
    
class Champ:
    """représente un champ d'une table, protégé par SetModifiable, Verifie le type des données et la taille, lié à un widget pour l'affichage"""
    def __init__(self, nom, type, ismodifiable=False, isclefprimaire=False):
        self.Nom=nom
        self.Type=type
        self.Null=True
        self.isModifiable=ismodifiable
        self.isClefPrimaire=isclefprimaire
        self.Initialise()
       
    def __init__(self, colonne, ismodifiable=False):#utilise sql : SHOW COLUMNS
        self.isClefPrimaire= (colonne[3]=='PRI' )
        self.NomChamp = colonne[0]
        self.Type=colonne[1]
        self.Null=(colonne[2]=='YES')
        self.isModifiable=ismodifiable
        self.Initialise()
        
    def Initialise(self):
        self.isNum=('int' in self.Type or 'float' in  self.Type or 'decimal' in self.Type)
        self.isTxt=('char' in self.Type or 'text' in self.Type)
        self.isDate=('date'in self.Type)
        self.TailleMax=self.CalculeTailleMax()    # strictement < a taille max
        self.Valeur=None
        self.ListeWidget=[]
    
    def AddWidget(self, w):
        self.ListeWidget.append(w)

    def EffaceListeWidget(self):
        copieliste=self.ListeWidget
        self.ListeWidget=[]
        return copieliste
    
    def SetListeWidget(self, listewidget):
        self.ListeWidget=listewidget
        
    def CopieChamp2Widget(self):
        valeur=self.Value()
        for widget in self.ListeWidget :
            try :
                widget.Set(valeur)
            except :
                print u'debug warning champ.CopieChamp2Widget() (widget.Set non défini pour '+self.Nom()+'?) '
            
            
    def CopieWidget2Champ(self):
        err=''
        if len(self.ListeWidget) > 1 :
            print u'warning: Champ.CopieWidget2Champ() plusieurs widgets associés au champ '+self.Nom()+'(vérifier valeurs identiques)'
        try:
            valeur=self.ListeWidget[0].Get()
            err = self.Set(valeur)
        except:
            print u'warning: Champ.CopieWidget2Champ() widget.Get associés au champ '+self.Nom()+u' non défini?'
        
        return err
        
    def Nom(self):   
        return self.NomChamp
        
    def SetModifiable(self, modifOk=True):
        self.isModifiable=modifOk
        
    def IsModifiable(self):
        return self.isModifiable
    
    
    def IsDate(self):
        return self.isDate
    
    def IsClefPrimaire(self):
        return self.isClefPrimaire
        
    def SetClefPrimaire(self,  isCP=True):
        self.isClefPrimaire=isCP
        self.isModifiable= not isCP

            
        
    def Set(self, valeur):
        err = self.Verifie(valeur)
        if err :
            if 'Warning/Date'in err  :
                err, valeur = self.ConvertirEnDateTime(valeur)
            if  'Warning/Unicode' in err :
                err, valeur = self.ConvertirEnUnicode(valeur)
            
        if not err : 
#            if not valeur : 
#                valeur='NULL'  #remplace None par null sinon ignoré dans requète sql
            self.Valeur=valeur
        return err
        
    def ConvertirEnUnicode(self, valeur):
        err=''
        
        if 'PyQt4.QtCore' in str( type(valeur) )  : # => transforme en string
            try :
                valeur = str( valeur.toUtf8() )#valeur = str( valeur )
            except :
                try :
                    valeur=str( valeur )  #ex QByteArray 
                except :
                    err='Erreur Tables.py:ConvertirEnUnicode '+type(valeur) 
                    print err
                    return( err, valeur)
                
        
        if 'str' in str( type(valeur)  ): #=> conversion string en unicode
            valeur=valeur.decode('utf8')
            
            
        if  type(valeur) != type(u'unicode')  : return 'Erreur/Warning le champ (' + self.NomChamp+') n\'est pas de type texte'
        
        err=self.Verifie(valeur) #verifie la taille 
        
        return(err, valeur)
        
        
    def ConvertirEnDateTime(self, valeur) :
        try :
            err='' 
            (h, min, sec)=(0, 0, 0)
            if 'QDate' in str(type(valeur)) :
                if  type(valeur)=='QDateTime':   #AAAA-MM-JJ HH:MM:SS
                    time=valeur.time()
                    h=time.hour()
                    min=time.minute()
                    sec=time.second()
                    valeur=valeur.date()
                d=valeur.day() 
                y=valeur.year() 
                m=valeur.month()
                valeur=datetime(y, m, d, h, min, sec)
            
            else : #TODO: ajouter h,min,sec
                if '-' in valeur :
                    y,m,d=(int(x) for x in valeur.split('-'))
                    if d>1900 : #format d-m-y
                        (y, d)=(d, y)
                    valeur=datetime(y, m, d)
                elif '/' in valeur :
                    y,m,d=(int(x) for x in valeur.split('/'))
                    if d>1900 : #format d-m-y
                        (y, d)=(d, y)                
                    valeur=datetime(y, m, d)

        except :
            err='Erreur Table_Base.py Champ:ConvertirEnDateTime  date='+str(valeur)
        return (err, valeur)
            
            
            
        
    def SetDirect(self, valeur): #fonction plus rapide à utiliser  lors de lecture de la base de donnée
        if self.isTxt : #and valeur :
            if valeur :
                valeur=valeur.decode('utf8')  #TODO: ++++++++++++++  ESSAYER SANS DECODE ++++++++++
            else : 
                valeur=''   # remplace NULL par '' dans champ texte #TODO: DEBUG ++++++++ VERIFIER SI OK ++++changé 30/5/14 
        self.Valeur=valeur

    def Efface(self):
        if self.isClefPrimaire :
            self.Valeur=-1
        else :
            self.Valeur=None
        
            
        
    def Verifie(self, valeur):
        if not self.isModifiable : return 'Erreur/Warning  Champ '+self.NomChamp + ' non modifiable'
        if not valeur  :
            if not self.Null : return 'Erreur Champ '+self.NomChamp + ' ne peut pas etre NULL'

            else : return None
            
        if self.isDate :
            if not 'datetime' in str( type(valeur) ) : return 'Warning/Date : formater la date '+str(valeur)
            
        if self.isTxt : #verifie si type unicode 
                if 'str' in str( type(valeur) ): return 'Warning/Unicode : convertir string en unicode'
                if 'PyQt4.QtCore' in str( type(valeur) ) : return 'Warning/Unicode : convertir PyQt4.string en unicode'

            
        if self.TailleMax :
            if self.isTxt :
                #if type(valeur) != type('string') : return 'Erreur/Warning le champ (' + self.NomChamp+') n\'est pas de type texte'
                if  type(valeur) != type(u'unicode')  : return 'Erreur/Warning le champ (' + self.NomChamp+') n\'est pas de type texte'
                if len(valeur) >= self.TailleMax : return 'Erreur/Warning  champ texte('+ self.NomChamp+')  trop long >= '+str(self.TailleMax)
            elif self.isNum :
                if 'int' in self.Type :
                    if type(valeur) != type (0) and type(valeur) != type (0L) and type(valeur)!=type(True): return 'Erreur/Warning le champ ('+ self.NomChamp+') n\'est pas de type entier'
                    if valeur>=self.TailleMax : return 'Erreur/Warning champ entier ('+ self.NomChamp+') trop grand >='+str(self.TailleMax)
                    
                elif 'float' in self.Type :
                    if type(valeur) != type (2E5) : return 'Erreur/Warning le champ ('+ self.NomChamp+') n\'est pas de type float'                    
                elif 'decimal' in self.Type :
                    pass #TODO: verifier type decimal, type date etc....
                    
                    
                
                
           
        else :
            return None
            
    
            
        
    def IsNumerique(self):
        return self.isNum
        
    def IsTexte(self):
        return self.isTxt
        
    def Get(self):
        return self.Valeur
    
    def Value(self):
        return self.Valeur

    def GetDate(self, type=''):
        try:
            if not type :
                return self.Valeur
            elif type=='QDate' and self.Valeur:
                (y, m, d)=(self.Valeur.year, self.Valeur.month, self.Valeur.day)
                return QDate(y, m, d)
        except :
            print 'erreur Tables_Base.GetDate()'

    def isTrue(self):
        if self.Valeur :
            return self.Valeur>0
        else :
            return False
        
        
    def Txt(self):
        if self.Valeur  :
            if self.isTxt :
                txt=self.Valeur
            else :
                txt=str(self.Valeur)
            if txt=='NULL' : txt=''
            return txt
        else :
            return ''
        
        
    def CalculeTailleMax(self):     
    
        max=None
        if 'char' in self.Type :
            max=256
    
        elif self.isNum :
            if 'int' in self.Type[0:3] :#4octet   256^4  REMARQUE int(11)   11=action uniquement sur affichage pas sur la taille des int sctockés
                max=4294967296
            elif 'tinyint' in self.Type :# 1octet
                max=256
            elif 'smallint' in self.Type :
                max=65536
            elif 'mediumint' in self.Type :
                max=16777216
            elif 'bigint' in self.Type:
                max=256**5  #256*int :  5 octets

            if  max and not 'unsigned' in self.Type : #max = None si float ou decimal #TODO: a revoir si utilité calculer max
                max=max/2
                
        elif 'date' in self.Type  or 'time' in self.Type  or 'year' in self.Type:
            max=20    #datetime sous forme txt
            
        elif 'longblob' in self.Type or 'longtext' in self.Type : #rem  type text = infini => taille max =None
            max=2**24
            
        return max
    
def NouvelleTable(DATABASE, nomTable, TableBase=''):
    return Table(nomTable, TableBase)


class Table: 
    """représente une table 
    input : nom base de donnée et nom de la table
    crée automatiquement les objets champs
    EnregistreTable : enregistre (update ou crée) les champs de la table (= représente une ligne)
    LectureId et RechercheSQL* : remplit les champs
    New : efface les valeurs des champs (garde les étiquettes et le format des champs)
    SetChamp  SetChamps : remplit un ou plusieurs champs
    """

    def __init__(self,nomBase,nomTable, TableBase='', auto=True, USER=config.user, PWD=config.password, dataBase=None):
        """TableBase : utile dans le cas de tables liées (JOIN) ou view"""
        self.nomDB=nomBase                                                                                       #(bof) à revoir  creer attribut de classe au lieu d'attribut d'instance=> nomDB et pas self.nomDB
        self.NomTable=nomTable
        
        self.NomTableBase=TableBase   #table principale = la seule modifiable   
        self.SetTableBase(TableBase ) #TODO: voir si supprime fonction
        
        if dataBase :
            self.DataBase=dataBase
        else :
            self.DataBase=DataBase(nomBase, USER, PWD)                                                   # (bof)a revoir   passer plutot une reference car ici chq table a un objet database=>perte memmoire        
        self.indicateur_lock=False  #True = modification = en cours d'édition = pas encore sauvée
        self.champ={}
        self.clefprimaire=None
        self.erreur= None
        self.Widget=None #TODO:  revoir si utilie /un widget associé à une table ! (attention référencé ailleurs)
#        self.Widget={} #T
#        self.ListeTableEnfant=None
        self.enCoursDEdition=False #si True => la table n'est pas encore enregistrée dans la data base 
        self.Initialise(auto)
        
    def ListeEnfants(self): #pour TableLiee (dans Table pour eviter tester si TableLiee)
        return None
        
    def AssocieWidgetChamp(self, w, nomchamp):
        try :
            self.dicoChamps[nomchamp].AddWidget(w)
        except :
            print 'warning exception Table.AssocieWidgetChamp()'
            
            
    def TransfertWidget(self, nouvelletable):
        for nomchamp in self.dicoChamps :
            champ=self.dicoChamps[nomchamp]
            listewidget = champ.EffaceListeWidget()
            nouvelletable.dicoChamps[nomchamp].SetListeWidget(listewidget)
            
        
#    def GetListeWidget(self):
#        return self.Widget

    def SetTableBase(self, nomtable):
            self.NomTableBase = nomtable or self.NomTable    
            self.TableBase=None  #TODO: eventuellement creer la Table

    def Nom(self):
        return self.NomTable
        
    def NomClefPrimaire(self):
        return self.clefprimaire.Nom()
        
    def Initialise(self, auto): # a surcharger (sauf si auto = true)
        if not auto : 
            pass
        else :
            self.listeChamps=[] #liste objet champ
            self.dicoChamps={}
            
            self.erreur=self.ListeChampsAuto()

    def ListeChampsAuto(self):
        msg=None
        requete="SHOW COLUMNS FROM "+self.NomTable+";"
        result=self.RechercheSQL_tableau(requete)
        if type(result)== type('string') : return result #= msg d 'erreur
        for colonne in result :
            newChamp=Champ(colonne)
            self.listeChamps.append(newChamp)
            self.dicoChamps[newChamp.Nom()]=newChamp
        msg=self.ListeChampModifiable()
        return msg
        
        
    def GetListeChamps(self):#generateur
        for champ in self.listeChamps :
            yield champ
        
        
    def GetDicoChamps(self):
        return self.dicoChamps
        
    def ListeChampModifiable(self):   #autorise modification de tous les champs SAUF clef primaire ET unqi
        msg=None
        try :
            requete="SHOW COLUMNS FROM "+self.NomTableBase+";"
            result=self.RechercheSQL_tableau(requete)
            for champ in result :
                nom=champ[0]
                try :
                    if self.dicoChamps[nom].IsClefPrimaire() :
                        self.clefprimaire = self.dicoChamps[nom]
                    else :
                        self.dicoChamps[nom].SetModifiable(True)
                except:
                    if config.DEBUG :
                        print 'warning : info la table '+self.NomTable+' ne reprend pas le champ '+nom+' de la table de base '+self.NomTableBase
                
        except :
            msg= 'Erreur /except Table_Base.py ('+self.NomTable+') ListeChampModifiable() '
            if AFFICHE_CONSOLE :
                print msg
        if not self.clefprimaire :
            msg=self.RechercheClefPrimaire()
            #msg='Erreur/Warning : pas de clé primaire Table : '+self.NomTable
            
        if msg and AFFICHE_CONSOLE :
                print msg
        return msg
        
    def RechercheClefPrimaire(self):
        msg='Erreur/Warning : pas de clé primaire Table : '+self.NomTable
        err=''
        if self.NomTableBase and  self.NomTable != self.NomTableBase :
            unetable= Table(self.nomDB,  self.NomTableBase)
            err=unetable.erreur
            if not err :
                self.TableBase=unetable
                nomCP=unetable.clefprimaire.Nom() #recupere le nom de la cle primaire / existe forcement sinon err=pas de clefprimaire /attention self.clefprimaire=unetable.clefprimaire incorrect car pas le mm objet   
                self.clefprimaire=self.dicoChamps[ nomCP ] 
                self.clefprimaire.SetClefPrimaire()
                return
        return msg+err
        
    def Id(self):
        if self.clefprimaire :
            return self.clefprimaire.Value()
            
    
        
    def EnleveGuillemets(self,c) : #TODO: ne pas enlever les ' mais voir si on peut remplacer par \'  +/- deplacer dans class Champ?
        try:
            return(string.replace(c,'"','""'))
            
        except:
            return -1
    
    def EnleveDoubleGuillemets(self,c) :
        try:
            return(string.replace(c,'""','"'))
        except:
            return -1

    #def LectureId(self, id ,  table='principale') : #lit la ligne  no id 
    def LectureId(self, id ) : #lit la ligne  no id 
        try :
            listeerreurs=''
            requete = "SELECT * FROM "+self.NomTable+" WHERE "+self.clefprimaire.Nom()+" = "+str(id)
            result=self.RechercheRequeteSQL(requete)[0]
            i=0
            for element in result :
                
                err=self.listeChamps[i].SetDirect(element) #sans verif = + rapide
                #err=self.listeChamps[i].Set(element) #avec verification, lors debug seulement
                if err : 
                    listeerreurs+=err
                #self.champ[self.LaListeDesChamps[i] ] = element
                i+=1
                
        except :
            msg="Erreur /except Table_Base.py    Table.lectureId id:"+str(id)+" introuvable??? "+listeerreurs
            if AFFICHE_CONSOLE :    print msg
            return msg
        if not listeerreurs :
            self.SignalIdChange()
        return listeerreurs
        
        
    def ActiveSQL(self, caracteregeneriques, *arg): #TODO: encours
        """active le 1er resultat correspondant aux champs trouvés
        input : True/False (si caracteregeneriques) listechamps recherchés 
        return : nb resultats trouvés si 0 (erreur ou aucun resultat) rien n'est changé si >1 active uniquement le 1er
        """
        result=self.RechercheIdSQLMulti(caracteregeneriques, *arg)
        try :
            nb=len(result)
            id=result[0][0]
            self.LectureId(id)
            return nb
        except :
            return 0
        
        
        
            

    def SignalIdChange(self): #envoie signal 'changé' aux enfants 
        pass
        #fonction à écrire dans les tables dérivées
    
    def SignalTableParentChange(self, parent):
        pass
        
        
    def Efface(self):
        """efface tous les champs et met id=-1 => nouvelle table"""
        for champ in self.listeChamps :
            champ.Efface()
        self.SignalIdChange()
        
        
    def New(self): 
        "crée et retourne une nouvelle table"
        unetable=Table(self.nomDB,self.NomTable, self.NomTableBase,  dataBase=self.DataBase)
#        unetable=Table(self.nomDB,self.NomTable, self.NomTableBase, True, USER, PWD, dataBase=self.DataBase)
        return unetable
        
    def RequeteSet(self):
        sql=' SET '
        try :
            for champ in self.listeChamps :
                value=champ.Value() 
                if not value :
                    value='NULL'
                if champ.IsModifiable() :#  and champ.Value() :
                    
#                    if str( champ.Value() ) == 'NULL':
#                        continue   #ERR empeche effacer un champ
                    if champ.IsNumerique() :
                        sql+= champ.Nom() + ' = ' + str( value )+','
                        
                    elif champ.IsTexte() :
                        valeur=value.replace('"', "'") #remplace " par '
                        sql+= champ.Nom() + ' = "' + valeur  +'",'
                    else :
                        sql+= champ.Nom() + ' = "' + str( value ) +'",'
            sql=sql[:-1]
        except :
            sql =  'erreur Table_Base.py RequeteSet() :'+sql+'champ:'+champ.Nom()
            #slq=msg
            if AFFICHE_CONSOLE :    print sql
        return sql   #remarque renvoie sql ou msg d'erreur
        
    def LastId(self):
        
        try :
            maxid=self.DataBase.LastIdTable(self.NomTableBase)
        except :
            maxid=0
        
        try :
            result=self.RechercheRequeteSQL('SELECT MAX('+self.clefprimaire.Nom()+') FROM '+self.NomTableBase)
#            if type(result)==type('string') : return ('erreur Table.py LastId() '+result)
            result=int(result[0][0])
        except :
            result=0
#            if not result[0][0] : return 0  #1ere ligne créee => retourne id=0
#            return ('erreur Table.py LastId() except')
            
        if result > maxid : maxid=result
            
        return maxid
        
    def EnregistreTable(self) : 
        "En registre la table dans la base de donnée, éventuellement crée une nouvelle ligne (si id<0)"
        if  not(self.indicateur_lock) :  
            return 'Warning : rien à enregister' 
        err=''
        if self.clefprimaire.Value() >0 :
            requete = 'UPDATE '+self.NomTableBase + self.RequeteSet()  +  ' WHERE '+self.clefprimaire.Nom()+ ' = ' + str( self.clefprimaire.Value()  ) +';'
            NbLignesModifiees = self.ExecuteSQL( requete)
            
            if type(NbLignesModifiees)==type('string') : 
                err = NbLignesModifiees
            elif NbLignesModifiees == 0 :
                    err='Warning : aucune ligne modifiée= '
        else :
            try :
                i=self.LastId()
                if type(i)== type('string'): return i #i=erreur
                self.clefprimaire.SetDirect(i+1)
                requete='INSERT INTO '+self.NomTableBase+' '+self.RequeteSet()+','+self.clefprimaire.Nom()+ ' = ' + str( self.clefprimaire.Value() )
                NbLignesModifiees = self.ExecuteSQL(requete)
                if type(NbLignesModifiees)==type('string') : 
                    self.clefprimaire.SetDirect(-1)
                    return 'Erreur Table_Base.py EnregistreTable() creation nouvelle ligne'+NbLignesModifiees
                elif NbLignesModifiees == 0 :
                    err='Warning : aucune ligne modifiée= '                
            except :
                self.clefprimaire.SetDirect(-1)
                return 'Erreur except Table_Base.py EnregistreTable() retrouve no clefprimaire'
            return err
            
            
        if not err :
            self.enCoursDEdition=False
            if self.NomTable <> self.NomTableBase :
                self.LectureId( self.Id()) # RELECTURE POUR METTRE A JOUR LES CLES/CHAMPS EXTERNES
            
        if not err or 'Warning' in err :#unlock aussi si warning
            self.UnLock() #les modifications sont enregistrées  => autorise modifs par autre utilisateurs et empeche autres enregistrements
        return err
        
    def Lock(self) :  # a appeler à chaque fois que la table est en mode édition
        pass # A#TODO:  verifie DB.Table.Lock = 0 pour self.clefprimaire (si >0 return = idUserLock) (si = 0 => DB.TableLock = idUser)
        self.indicateur_lock = True
        return 0 # si la table (la ligne) est deja en mode edition par un autre utilisateur, renvoie l'idUserLock (>0 et <>idUser actuel)
        
    def UnLock(self): #uniquement si meme utilisateur 
        if self.indicateur_lock :
            pass #TODO: met DB.Table lock=0
            self.indicateur_lock = False
            return ''  #sinon return 'erreur table editee  par autre utilisateur'
            
            
    def Get(self, nomchamp):
        """input : nom champ
            return: valeur du champ ou None """ 
        try :
            return self.dicoChamps[nomchamp].Value()
        except :  
            return None #nomchamp n'existe pas
            
    def SetChamps(self, enregistre_nouveau=False,  enregistre_auto=False,efface= False,   **arg) :
        """input:  enregistre_auto=False,   champ=valeur,...,champ= valeur
            return : None ou  msgErreur
        """
        liste_erreurs=''
#        
#        if enregistre_nouveau :
#            self=self.New()
#        
        if (efface or enregistre_nouveau) and self.clefprimaire.Value()>0: #n'efface qu'une fois
#        if efface and self.clefprimaire.Value()>0: #n'efface qu'une fois
            self.Efface()
        
        for nomchamp,  valeur in arg.iteritems():
            msg=self.SetChamp(nomchamp, valeur)
            if msg and 'Erreur' in msg : liste_erreurs+=msg
        if enregistre_auto or enregistre_nouveau :
            erreur= self.EnregistreTable()
            liste_erreurs+=erreur
            if liste_erreurs and AFFICHE_CONSOLE : print 'Err Tables.py:SetChamps et enregistre '+liste_erreurs
        return liste_erreurs            
    
    def SetChamp(self, champ, valeur, enregistre_auto=False, enregistre_nouveau=False, efface= False) : 
        """input: champ, valeur, enregistre_auto=False
            return : None ou  msgErreur
        """
        try :
            erreur=''
        
            if (efface or enregistre_nouveau) and self.clefprimaire.Value()>0: #n'efface qu'une fois
                self.Efface()            
            
            unchamp=self.dicoChamps[champ]
            if  not unchamp.IsModifiable() :
                erreur = 'Table.SetChamp : champ :"'+str(champ) +'" non modifiable (clé primaire ou table liée(JOIN/VIEW))'
                if AFFICHE_CONSOLE : print erreur
                return erreur
                
            

            if not self.indicateur_lock :  # Lock() uniquement des la 1ere modification, inutile ensuite
                idLock = self.Lock()
                if idLock > 0 :
                    erreur = 'Erreur : la table"'+self.NomTable +'"est actuellement éditée par un autre utilisateur No:'+str(idLock)
                    if AFFICHE_CONSOLE : print erreur
                    return erreur
                    
                    
            erreur=unchamp.Set(valeur)
            if erreur : 
                if AFFICHE_CONSOLE : print erreur
                return erreur

            #si tout est bon : 
            self.enCoursDEdition=True
            if enregistre_auto or enregistre_nouveau :
                erreur= self.EnregistreTable()
            return erreur
        except :
            erreur = 'Erreur exception Table.SetChamp (erreur champ '+str(champ)+'?)'
            if AFFICHE_CONSOLE : print erreur
            return erreur
            
    def VerifieTypeChamp(self, champ, valeur): #TODO: VERIFIER TOUS LES TYPES
        letype= type(valeur) 
        typechamp=self.typeDuChamp[champ]
        if ( letype is IntType or letype is FloatType ) and  ('char' in typechamp or 'date' in typechamp ):
            return False
        if letype is StringType and not ('char' in typechamp or 'date' in typechamp ):
            return False
        return True
            

    def PrintChamp(self, etiquettes=True, imprimechampvide=False, NbTab=0):  
        """retourne un texte avec la valeur de chaque champ"""
        texte=''
        if etiquettes : texte ='\n'+NbTab*'\t'
        for champ in self.listeChamps :
            if not imprimechampvide and not champ.Txt() :
                continue
            if etiquettes :
                texte+=NbTab*'\t'+'<'+champ.Nom()+'>:'
            texte += ' '+champ.Txt()+' '
            if etiquettes :
                texte += '\n'+NbTab*'\t'
        return texte
        
    def PrintParentEnfantActifs(self, etiquettes=True, imprimechampvide=False, NbTab=0):  
        txt='<'+self.Nom()+'(*)('+str(self.Id())+')>' + self.PrintChamp( etiquettes, imprimechampvide, NbTab)
        return txt
        
        
    def PrintParentEnfant(self, etiquettes=False, imprimechampvide=False, NbTab=0):  
        #texte=NbTab*'\t'+'<'+self.Nom()+'('+str(self.Id())+')>'
        texte=''
        if etiquettes : texte=NbTab*'\t'
        texte+='<'+self.Nom()+'('+str(self.Id())+')>'
        NbTab+=2
        texte+=self.PrintChamp(etiquettes, imprimechampvide, NbTab)+'\n'
        return texte
        
        
    def RechercheIdSQLMulti(self,caracteregeneriques, *arg): 
        """comme RechercheSQLMulti mais ne retourne que la liste d'id"""
        try :
            requete="SELECT "+self.clefprimaire.Nom() +self.PrepareSQLfrom(caracteregeneriques, *arg)
            uneListe=self.DataBase.RechercheSQL_liste(requete)   
        except :
            erreur='Erreur : Table:RechercheIdSQLMulti  verifier si clefprimaire existe (?)'
            if AFFICHE_CONSOLE : print erreur
            return erreur
            
        return uneListe
        
        
        
        
    def RechercheSQLMulti(self,caracteregeneriques, *arg): 
        """Recherche requete sql avec caracteregeneriques (* % ?) ou pas : * % plusieurs caractères ? un seul caractere
        input caracteregeneriques (True/False) champ1,valeur1,champ2,val2...
        return : liste résultats ou msg d'erreur (tester type)"""

        requete="SELECT * " +self.PrepareSQLfrom(caracteregeneriques, *arg)
        uneListe=self.DataBase.RechercheSQL_liste(requete)   #uneListe=self.DataBase.RechercheSQL(requete) #=DICO/old
        return uneListe
        
    def PrepareSQLfrom(self, caracteregeneriques, *arg):

        requete=" FROM "+self.NomTable
        AND=' WHERE '
        i=1
        taille=len(arg)
       
        while i < taille:
            nomchamp=arg[i-1] 
            valeur=arg[i]
            egal=' = '
            
#            if caracteregeneriques and type(valeur)==type('string') and ('*' in valeur  or  '%' in valeur or '?' in valeur):
#                valeur=valeur.replace('*', '%')
#                valeur=valeur.replace('?', '_')
#                egal=' LIKE '
                
            if self.dicoChamps[nomchamp].IsNumerique() :                                   
                requete+=AND+nomchamp+'='+str(valeur)
            else :
                if caracteregeneriques and type(valeur)==type('string') and ('*' in valeur  or  '%' in valeur or '?' in valeur):
                    valeur=valeur.replace('*', '%')
                    valeur=valeur.replace('?', '_')
                    egal=' LIKE '
                
                requete+=AND+nomchamp+egal+'"'+valeur+'"'           
            AND=' AND '
            i=i+2
            
        return requete
        
        
            
            
#TODO:  ???  fonction Delete      def Delete(self): #suppression de l'item de la base de donee         sql="DELETE FROM "+split(self.NomTable)[0]+" WHERE "+split(self.listechamps,",")[0]+"="+str(self.id) #split(nomtable) car nomtable peut etre complexe (ex: Client LEFT OUTER JOIN)

    def RechercheRequeteSQL(self,requete):
        """retourne la liste des résultats de sql ou string msg erreur"""
        uneListe=self.DataBase.RechercheSQL_liste(requete)   #uneListe=self.DataBase.RechercheSQL(requete) #=DICO/old
        return uneListe
    

    def RechercheSQL_tableau(self,requete):  
        return self.DataBase.RechercheSQL_tableau(requete)
    
    def ExecuteSQL(self,requete): 
        """requête insert ou update 
        Return  nb de lignes modifiées ou message d'erreur"""
        return self.DataBase.ExecuteSQL(requete) 
        
        
class TableLiee(Table):
    """Table liée à une 2ème table (par Id) ex : client-> animaux   ou animal->consultations
    possède la liste de ces enfants ex unclient -> tous ses animaux
    Lien entre 2 tables : type n:n  1:1  ou 1:n    
    la table parent envoit des signaux aux enfants en cas de changement (=ex en cas de changement de client)
    input : 2 tables (class Table) et nom des champs liés ou TableLien 
    ATTENTION : relation 1:n  un des noms des champs liés doit etre None
    """
    def __init__(self,   tableparent, tableenfant, nomidparent2enfant, nomidenfant2parent,  tablelien=None):
        
        Table. __init__(self,tableparent.nomDB,tableparent.NomTable, tableparent.NomTableBase, dataBase=tableparent.DataBase)
        self.TableLien=tablelien
        self.TableParent=tableparent
        self.dicoChamps =  tableparent.dicoChamps  #pour que Get(Champ) et SetChamp de TableLiee utilisent la tableparent (sinon dicoChamps pointe sur des champs dont la valeur reste tjrs null)
        self.listeChamps = tableparent.listeChamps
        
        self.TableEnfant=tableenfant
        self.NomIdParent2Enfant=nomidparent2enfant  #nom de idenfant dans la table parent 
        self.NomIdEnfant2Parent=nomidenfant2parent  #nom de idparent dans la table enfant 
        self.ListeIdEnfant=[]
        self.ListeTableEnfant =[]
        self.EnfantActif=None
        
        self.clefprimaire=tableparent.clefprimaire   #important pour la sauvegarde

    def New(self): 
        "crée et retourne une nouvelle table liée"
        
        #unetable=TableLiee(self.TableParent,self.TableEnfant, self.NomIdParent2Enfant, self.NomIdEnfant2Parent, self.TableLien) #Err CAR si fait LectureId => changement dans toutes les TableLiee 
        
        newparent=self.TableParent.New()
        newenfant=self.TableEnfant.New()
        unetable=TableLiee(newparent,newenfant, self.NomIdParent2Enfant, self.NomIdEnfant2Parent, self.TableLien)

        return unetable


    def SignalIdChange(self):
        self.ActualiseListe() #recrée la liste des enfants
        if self.ListeTableEnfant : #TODO:  DEBUG******************verifier si enfant->enfant propage signal
            for enfant in self.ListeTableEnfant : #propage signal aux enfants
                enfant.SignalTableParentChange(parent=self)
        if self.Widget :  #envoie un signal à son widget s'il existe pour actualiser affichage
            self.Widget.SignalChange(self)
            
            
    def ActualiseListe(self, idparent=None, creation_enfant=True):
        if not idparent :
            idparent=self.TableParent.Id()
        self.ActualiseListeId(idparent)
        if creation_enfant :
            self.CreationListeEnfants()
            
            
    def RafraichissementListeEnfants(self, idenfant=None, actualiseListeId=False):
        if actualiseListeId :
            self.ActualiseListe()
        if not idenfant : #relit toute la liste
            self.CreationListeEnfants()
        else :
            for enfant in self.ListeTableEnfant : #supprime d'abord l'ancien enfant
                if enfant.Id() == idenfant :
                    self.ListeTableEnfant.remove(enfant)
                    break
            new_enfant=self.TableEnfant.New()
            new_enfant.LectureId( idenfant )
            self.ListeTableEnfant.append( new_enfant)
            
            
            
    def CreationListeEnfants(self):   
        """crée les instances d'enfant à partir de ListeIdEnfant"""

        self.ListeTableEnfant=[]
        self.EnfantActif=None
        for id in self.ListeIdEnfant :
            new_enfant=self.TableEnfant.New()
            new_enfant.LectureId( id )
            self.ListeTableEnfant.append( new_enfant)


#        if not self.ListeIdEnfant : ==> VERSION +COMPLIQUEE  /VERIFIER SI ERREUR CAR LES ENFANTS POURRAIENT ETRE ENCORE UTILISES
#            del(self.ListeTableEnfant[:]) #efface tous les elements de la liste 
#            return
#        compteur=0
#        nbenfant=len(self.ListeIdEnfant)
#        tailleliste=len(self.ListeTableEnfant) # n'efface pas l'ancienne liste mais réutilise les enfants  en mettant à jour leur id (et gère les cas où la nouvelle liste n'est pas de la meme taille que l'ancienne)
#        while (compteur<nbenfant  or  compteur<tailleliste ) :
#            if compteur<nbenfant  and  compteur<tailleliste :
#                self.ListeTableEnfant[compteur].LectureId( self.ListeIdEnfant[compteur])        #met à jour l'id (inutile de créer une nouvelle table )
#            elif compteur>=nbenfant  :                                                                                  # and  compteur<tailleliste (évident cf boucle while)
#                del( self.ListeTableEnfant[compteur:] )                                                             #--->efface la fin de la liste
#                break
#            else :                                                                                                                      #compteur<nbenfant   and compteur>=tailleliste ---> creation table enfant
#                new_enfant=self.TableEnfant.New()
#                new_enfant.LectureId( self.ListeIdEnfant[compteur] )
#                self.ListeTableEnfant.append( new_enfant )
#            compteur+=1
    
    def ActiveId(self, id):
        err= self.LectureId(id)
        return err
        
    def Id(self):
        if self.TableParent :
            return self.TableParent.Id()
            
    def IdParent(self): #synonyme
        if self.TableParent :
            return self.TableParent.Id()
    
    def Get(self, nomchamp):
        if self.TableParent :
            return self.TableParent.Get(nomchamp)
        
        
        
    def ActiveEnfantId(self, idenfant):
        trouve=None
        for enfant in self.ListeTableEnfant :
            if idenfant == enfant.Id() :
                trouve = enfant
                break
        self.EnfantActif=trouve
        return trouve
        
    def DesactiveEnfant(self):
        self.EnfantActif=None
        
    def GetListeEnfant(self): #generateur retourne les enfants du parent ACTIF (utile si enfant est une table liee=>retourne unqiuement type Table)
        for tableLieeEnfant in self.ListeTableEnfant :
            try :
                enfant=tableLieeEnfant.TableParent
            except :
                enfant=tableLieeEnfant #TODO: à tester
                
            yield enfant        
    
    def LectureId(self, id,  table='parent'): 
        """Lecture (activation) de l'id (par defaut table='parent' <=> n'a pas de parent) et signal de changement pour actualiser les enfants"""
        msg_erreur =''
        old_id = self.Id() 
        
        if id == old_id  and  table=='parent':
            return #rien à changer
            
        
        if table == 'parent' :
            msg_erreur=self.TableParent.LectureId(id)
        elif table=='enfant' : #TODO:  A TESTER
            try :
                old_id = self.TableEnfant[0].Id()
                if id <> old_id :
                    msg_erreur=self.TableEnfant[0].LectureId(id) #chande l'id du 1er enfant
                    self.ActiveParent(self.TableEnfant[0])#TODO:   #normalement inutile, on change plutot le parent
            except :
                msg_erreur +=' Erreur : TableLiee:LectureId pas de table enfant(?)'
                if AFFICHE_CONSOLE :
                    print msg_erreur 
                return msg_erreur
        else :
            msg_erreur=table.LectureId(id)  #TODO:  DEBUG   *****AREVOIR*******utilité?????(+verifier id<>old_id)
            
        if not msg_erreur :    #and self.Id() <> old_id :
            self.SignalIdChange()
        return msg_erreur 

    
    def ActiveParent(self, enfant):
        """active le parent qui correspond à enfant (retrouve idParent dans enfant puis lectureId"""
        print '*********debug*********** A FAIRE **************'
    
    def ActualiseListeId(self, idparent):
        "liste des id enfants correspondant à idparent"
        self.ListeIdEnfant=[]
        if self.TableLien : # relation n:n
            nomidparent=self.TableParent.NomClefPrimaire()
            nomidenfant=self.TableEnfant.NomClefPrimaire()
            sql= 'SELECT '+self.NomIdParent2Enfant+' FROM '+self.TableLien.Nom()+ ' WHERE '+self.NomIdEnfant2Parent+' = '+str(idparent) 
#            result=self.TableParent(sql)
#            for ligne in result :
#                self.ListeIdEnfant.append( ligne[0])
                
        elif self.NomIdParent2Enfant : # relation 1:1, la table parent  contient l'id de l'enfant
            nomidparent=self.TableParent.NomClefPrimaire()
            sql = 'SELECT '+self.NomIdParent2Enfant+' FROM '+self.TableParent.Nom()+' WHERE '+nomidparent+' = '+str(idparent) # on recherche dans la table parent l'id enfant
#            result=self.TableParent(sql)
#            self.ListeIdEnfant.append( result[0] ) #un seul resultat
            
        elif self.NomIdEnfant2Parent : #relation n:1, la table enfant contient l'id parent
            nomidenfant=self.TableEnfant.NomClefPrimaire()
            sql = 'SELECT '+nomidenfant+' FROM '+self.TableEnfant.Nom()+' WHERE '+self.NomIdEnfant2Parent +' = '+str(idparent) #on recherche dans la table enfant LES id enfant pour les lignes  = idparent 
#            result=self.TableParent(sql)
#            for ligne in result :
#                self.ListeIdEnfant.append( ligne[0])
                
        result=self.TableParent.RechercheRequeteSQL(sql)
        for ligne in result :
            self.ListeIdEnfant.append( ligne[0])
    
    def PrintParent(self):
        if TableParent :
            return self.TableParent.PrintChamp()
        
    def PrintParentEnfant(self, etiquettes=False, imprimechampvide=False, nbTab=0):  
#        txt=nbTab*'\t'+'<'+self.TableParent.Nom()+'('+str(self.TableParent.Id())+')>'+self.TableParent.PrintChamp(etiquettes, imprimechampvide)+'\n'
        txt=''
        if etiquettes : txt='\t'*nbTab
        txt+='<'+self.TableParent.Nom()+'('+str(self.TableParent.Id())+')>'+self.TableParent.PrintChamp(etiquettes, imprimechampvide, nbTab)+'\n'
        nbTab+=2
        listeenfant=self.ListeEnfants()
        for enfant in listeenfant:
            txt+=nbTab*'\t'+'---->'+enfant.PrintParentEnfant(etiquettes, imprimechampvide, nbTab)
        return txt
    
    def PrintParentEnfantActifs(self, etiquettes=False, imprimechampvide=False, nbTab=0):  
        txt=''
        if self.TableParent :
            txt+='<'+self.TableParent.Nom()+'(*)('+str(self.TableParent.Id())+')>'+self.TableParent.PrintChamp(etiquettes, imprimechampvide, nbTab)+'\n'
            nbTab+=2
            if self.EnfantActif :
                txt+=nbTab*'\t'+'---->'+self.EnfantActif.PrintParentEnfantActifs(etiquettes, imprimechampvide, nbTab)
        return txt
        
        
    def ListeEnfants(self):
        return self.ListeTableEnfant 
        

    def AddEnfant(self, enfant): #enfant = table ou liste de tables TODO: CREE LE LIEN SI TABLE LIEN
        #self.ListeTableEnfant.append(enfant)

        if type(enfant)<>type(self.TableEnfant) :
            erreur='ERREUR TableLiee:Addenfant() le type enfant est incorrect'
            self.DataBase.AjouteErreurTransaction(erreur)
            if AFFICHE_CONSOLE :
                print erreur
            return erreur
            
        idparent=self.TableParent.Id()
        if not(idparent) or idparent<0 : 
            erreur='ERREUR TableLiee:Addenfant() parent n\'a pas un id valide'
            self.DataBase.AjouteErreurTransaction(erreur)
            if AFFICHE_CONSOLE :
                print erreur
            return erreur          
            
        #idenfant=self.TableEnfant.Id()
        idenfant=enfant.Id()
        if not(idenfant) or idenfant<0 : 
            erreur='ERREUR TableLiee:Addenfant() enfant n\'a pas un id valide'
            self.DataBase.AjouteErreurTransaction(erreur)
            if AFFICHE_CONSOLE :
                print erreur
            return erreur            

        #TODO: VERIFIER PAS DE DOUBLON ENFANT (verifer sur idenfant) ***************************
        
        if enfant in self.ListeTableEnfant :
            erreur='ERREUR TableLiee:Addenfant() doublon enfant (utilisation probable de la meme instance d\'enfant)'
            self.DataBase.AjouteErreurTransaction(erreur)
            if AFFICHE_CONSOLE :
                print erreur
            return erreur            
        
        idenfant=enfant.Id()
        for lesenfants in self.ListeTableEnfant :
            if lesenfants.Id()== idenfant :
                erreur='ERREUR TableLiee:Addenfant() doublon enfant (id enfant déjà existant)'
                self.DataBase.AjouteErreurTransaction(erreur)
                if AFFICHE_CONSOLE :
                    print erreur
                return erreur                    
        
        nomidenfant=self.NomIdParent2Enfant
        nomidparent=self.NomIdEnfant2Parent


        if self.TableLien : # relation n:n => nouvelle ligne dans table lien
#            arg=[`nomidparent`, idparent, nomidenfant, idenfant]
            #erreur=self.TableLien.SetChamps(enregistre_nouveau=True, enregistre_auto=False,efface= False,arg)
#            erreur=self.TableLien.SetChamps(enregistre_nouveau=True, *nomidparent= idparent, *nomidenfant=idenfant)
#            self.TableLien.Efface()
            erreur1=self.TableLien.SetChamp( nomidparent, idparent, efface=True)
            erreur=self.TableLien.SetChamp( nomidenfant, idenfant)
            if erreur1 : erreur+=erreur1
            self.TableLien.EnregistreTable()
            if erreur : self.DataBase.AjouteErreurTransaction(erreur)

        elif self.NomIdEnfant2Parent : #relation n:1 (1:n), la table enfant contient l'id parent => met à jour idparent dans table enfant
            nomidenfant2parent=self.NomIdEnfant2Parent
            erreur=self.TableEnfant.SetChamp( nomidenfant2parent,  idparent, efface=True, enregistre_auto=True)
            if erreur : self.DataBase.AjouteErreurTransaction(erreur)
            
        elif self.NomIdParent2Enfant : # relation 1:1, la table parent  contient l'id de l'enfant (UNIQUE)
            nomidparent2enfant = self.NomIdParent2Enfant
            erreur=self.TableParent.SetChamps(nomidparent2enfant, idenfant, efface=True, enregistre_auto=True) 
            if erreur : self.DataBase.AjouteErreurTransaction(erreur)
            
#        self.ActualiseListe() #TODO: ajouter seulement 1 enfant (si pas doublon)
            #ATTENTION NE MARCHE PAS SI TRANSACTION car actualise liste utilise recherche SQL
        self.ListeTableEnfant.append(enfant)
        self.ListeIdEnfant.append(enfant.Id())
        
    def RemoveEnfant(self, enfant): #TODO: ENLEVE LE LIEN
        try :
            self.ListeTableEnfant.remove(enfant) #a faire a partir idenfant (pas forcement la mm instance d enfant)
        except :
            pass
            
    def ClearListeEnfant(self):
        self.ListeTableEnfant= None #TODO: à revoir , libérer mémoire?        
    
    def PrintEnfant(self):
        txt=''
        compteur=1
#        if self.ListeIdEnfant :
#            for idenfant in self.ListeIdEnfant :
#                self.TableEnfant.LectureId(idenfant)
#                txt+='--------------  No '+str(compteur)+'--------------------\n'
#                txt+=self.TableEnfant.PrintChamp()+'\n---------------------------\n'
#                compteur+=1

        if self.ListeTableEnfant :
            for enfant in self.ListeTableEnfant :
                txt+='--------------  No '+str(compteur)+'--------------------\n'
                txt+=enfant.PrintChamp()+'\n---------------------------\n'
                compteur+=1

        return txt


#class ListeTable: #TODO: afaire ou enlever ???
#    def __init__(self, table1, parent=None):
#        self.ListeTable=table1
#        self.Parent=parent
#        self.Actif=table1
#        self.ListeId=None
#        
#    def ActualiseId(self):
#        try :
#         nomidparent=self.Parent.clefprimaire.Nom()
#         idparent=self.Parent.clefprimaire.Value()  
#        
#        except :
#            pass #TODO: 
#        
    
if config.DEBUG :
    def TestTable():
        print 'EXEMPLES D UTILISATION DES TABLES'
        print 'test d\'erreur : essai mauvais nom de table'
        nb=raw_input('tapez <entrée>')
        test=Table(DATABASE,'PersonneTESTDERREUR', USER=config.user, PWD=config.password, auto=True)   
        if test.erreur :    print "test.erreur = "+test.erreur
        nb=raw_input('tapez <entrée>')
        print 'correction'
        nb=raw_input('tapez <entrée>')
        test=Table(DATABASE,'Personne', USER=config.user, PWD=config.password, auto=True)   
        if test.erreur :    print "test.erreur = "+test.erreur
        
        #table_client=Table(DATABASE, ' Personne LEFT JOIN Commune ON Personne.Commune_idCommune = Commune.idCommune','Personne',  auto=True)
        #ne fonctionne pas
        
        table_client=Table(DATABASE, 'viewClient','Personne',  auto=True)
        nb=raw_input('tapez <entrée>')
        print "recherche id=1"
        nb=raw_input('tapez <entrée>')
        print test.LectureId(1)
        print test.PrintChamp()
            
        nb=raw_input('tapez <entrée>')
        print "recherche sur nom et client  avec caractere generiques=>"
        nb=raw_input('tapez <entrée>')
        print test.RechercheSQLMulti(True,"IsClient",'TRUE','Nom','*Du%on?')#   % ou * sont équivalents

        nb=raw_input('tapez <entrée>')
        print "recherche dans viewclient /sans caractere generiques=>"
        print table_client.RechercheSQLMulti(False,'Nom', 'Dupond')
        nb=raw_input('tapez <entrée>')
        
        print "lecture un id+printChamp"
        nb=raw_input('tapez <entrée>')
        table_client.LectureId(1)
        print table_client.PrintChamp()

        
        nb=raw_input('tapez <entrée>')
        print 'test d\'erreur : set champ id (interdit=clef primaire)'
        nb=raw_input('tapez <entrée>')
        table_client.SetChamp('idPersonne',5)
        
        nb=raw_input('tapez <entrée>')
        print 'set champ prenom + print sans étiquettes'
        nb=raw_input('tapez <entrée>')
        table_client.SetChamp('Prenom','Kanya nouveau prenom') 
        print table_client.PrintChamp(etiquettes=False)
        
        nb=raw_input('tapez <entrée>')
        print 'enregistre client'
        err=table_client.EnregistreTable()
        
        print 'fin enregistre client '+str(err)
        
        nb=raw_input('tapez <entrée>')
        print 'test d\'erreur : set champ CIP : interdit (table liée/view)'
        nb=raw_input('tapez <entrée>')
        table_client.SetChamp('CIP','60000') 

        nb=raw_input('tapez <entrée>')
        print 'nouveau client et set nom=dupond'
        table_client.Efface()
        table_client.SetChamp('Nom', 'Dupond')
        
        nb=raw_input('tapez <entrée>')
        print '1/ test d\'erreur :essaie d\'enregistrer/modifier une table incomplete'
        nb=raw_input('tapez <entrée>')
        erreur=table_client.EnregistreTable()
        print erreur
       
        nb=raw_input('tapez <entrée>')
        print '2/ complete la table et enregistre'
        nb=raw_input('tapez <entrée>')
#        table_client.SetChamps(Civilite_idCivilite=2,  Commune_idCommune=1)
        table_client.SetChamps(enregistre_auto=True,  Civilite_idCivilite=2,  Commune_idCommune=1)
#        erreur=table_client.EnregistreTable()
        print erreur    
        
    def Test2TablesLiees():
        unclient=Table(DATABASE, 'viewClient','Personne',  auto=True)
        unclient.LectureId(1)
        print unclient.PrintChamp(False)
        unanimal=Table(DATABASE, 'Animal',  auto=True)
        unanimal.LectureId(1)
        print unanimal.PrintChamp()
        tablelien=Table(DATABASE, 'ClientAnimalRef ',  auto=True)
        print tablelien.PrintChamp()
    #    lien_client_animal=LienTable(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
        lien_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
        lien_client_animal.ActualiseListe(1 )
        print "Liste des enfants :\n"
        print lien_client_animal.PrintEnfant()
    
    def TestConnectionGlobale():
        #cree2database et verifie meme connection globale
        USER=config.user  
        PWD=config.password

        print 'commence 2 StartTransaction (verifie que la 2eme connection globale n\'est pas créée cf adresse des instances) et affiche warning'

        base1=DataBase(DATABASE, USER, PWD)                                                   
        base2=DataBase(DATABASE, USER, PWD)                                                   
        
        (con1, err1)=base1.StartTransaction()
        (con2, err2)=base2.StartTransaction()  #pour verifier le warning et que la transaction globale est unique (la meme pour base1 et base2)
        
        print con1, err1
        print con2, err2
        
        print "test creation d'un client temporaire puis rollback"
        unclient=Table(DATABASE, 'viewPersonne','Personne')#,  auto=True)
        nomclient='EASTWOOD (temporaire)'
        prenomclient='Clint'
        unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
        print "lecture dans database avant rollback (normalement vide)"
        print base1.RechercheSQL_liste("select * from Personne where Nom='"+nomclient+"'")
    
        print "rollback :"
        base2.Rollback()
        print "lecture dans database après rollback (normalement vide)"
        print base1.RechercheSQL_liste("select * from Personne where Nom='"+nomclient+"'")

        print "test creation de 2 clients definitif puis commit"
        (con1, err1)=base1.StartTransaction()
        
        nomclient='ClientTestCommit1'
        unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)


        nomclient='ClientTestCommit2'
        unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)

        print "lecture dans database avant commit (normalement vide)"
        print base1.RechercheSQL_liste("select * from Personne where Nom LIKE '%TestCommit%'")
        
        print 'commit'
        base2.Commit()
        
        print "lecture dans database apres commit => 2 clients TestCommit"
        print base1.RechercheSQL_liste("select * from Personne where Nom LIKE '%TestCommit%'")

        
        print 'test ecriture directe (sans transaction) : si pas instruction StartTransaction => écriture directe'
        nomclient='ClientTestDirect'
        unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
        print "lecture dans database de %Test%"
        print base1.RechercheSQL_liste("select * from Personne where Nom LIKE '%Test%'")
        
        print 'efface tout Test'
        print base1.ExecuteSQL('DELETE FROM Personne WHERE Nom LIKE "%Test%"')
        print base1.RechercheSQL_liste("select * from Personne where Nom LIKE '%Test%'")

    def TestAddenfant():
        USER=config.user  
        PWD=config.password
        
        base1=DataBase(DATABASE, USER, PWD)                                                   


        (con1, err1)=base1.StartTransaction()        
        
        
        unclient=Table(DATABASE, 'viewPersonne','Personne')
        unanimal=Table(DATABASE, 'Animal')#,  auto=True)
        tablelien=Table(DATABASE, 'ClientAnimalRef')# ,  auto=True)
        table_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
        
        
        nomclient='EASTWOOD (temporaire)'
        prenomclient='Clint'
        unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)

        espece=1
        nomanimal='Grosminet (temporaire)'
        unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
        
        print table_client_animal.PrintParentEnfant()
        
        table_client_animal.AddEnfant(unanimal)




        unanimal=Table(DATABASE, 'Animal')#IMPORTANT CREER NEW ANIMAL
        nomanimal='Mimi (temporaire)'
        unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
        table_client_animal.AddEnfant(unanimal)

        print 'test doublon instance enfant'

        nomanimal='Mimi2 (temporaire)'
        unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
        table_client_animal.AddEnfant(unanimal)
        
        print 'test doublon id enfant'
        unanimal=Table(DATABASE, 'Animal')#NEW ANIMAL
        unanimal.ActiveSQL(True, 'Nom','%Mimi2%')
        table_client_animal.AddEnfant(unanimal)


        
        print table_client_animal.PrintParentEnfant()
        
        base1.Rollback()


if __name__ == "__main__":
  
    
#    TestTable()
    Test2TablesLiees()
    #TestConnectionGlobale()
    TestAddenfant()
