#!/usr/bin/python 
# -*- coding: utf8 -*-

import adodb, MySQLdb
import string
from string import *
from types import *

import config



USER=config.user
PWD=config.password
DATABASE=config.database
IDUSER=config.IDUSER

class DataBase:
    nomDB=''
    def __init__(self,nomD):
        self.nomDB=nomD
        #self.DataBase=DataBase(nomD)
        self.InitialiseDB()
    def InitialiseDB(self): # a surcharger
        pass
        
    def PrintDB(self):
        print self.nomDB

    def Connection(self):
        try :
            conn = adodb.NewADOConnection('mysql') 
            conn.Connect('localhost',USER,PWD,self.nomDB)  # afaire gere erreur connection
        except :
            print "debug Err Database.RechercheSQL : err connection  ************* VERIFIEZ config.py database password etc ******"
        return conn
    
    def RechercheSQL_liste(self,requete):  
        conn = self.Connection() 
        if not conn : return
        cursor = conn.Execute(requete)
        info = cursor.RecordCount( )
        liste = []
        while not cursor.EOF:  #lit les lignes de la requete et place 
                                        #dans la liste 
                    uneligne = cursor.fields
                    liste.append(uneligne)
                    cursor.MoveNext() 
        conn.Close()
        return (liste)
    
    
    def RechercheSQL_dico(self,requete):  
        conn = self.Connection() 
        if not conn : return
        dico = conn.GetDict(requete)
        return dico
    
    def RechercheSQL_tableau(self,requete):  
        conn = self.Connection() 
        if not conn : return
        dico = conn.GetAll(requete)
        return dico

    
    def ExecuteSQL(self,requete):   # execute requete de modification (pas de recherche)
        result=''
        try :
            conn = adodb.NewADOConnection('mysql')  #renvoie -1 si erreur
            conn.Connect('localhost',USER,PWD,self.nomDB)  
        except :
            result = "debug Err Database.ExecutSQL : err connection"
            return result
        try:
            cursor = conn.Execute(requete)
            result=cursor.Affected_Rows()
            conn.CommitTrans( )
        except :
            result ="debug Err Database.ExecutSQL Execution "+str(requete)+" "+str(result)
            return result
            
        conn.Close()
        return result
                                    
        
        
#    def RechercheSQL(self,requete):
#        conn = adodb.NewADOConnection('mysql')
#        conn.Connect('localhost','root','',self.nomDB)
#        dico={}
#        dico = conn.GetDict(requete)
#        return (dico)

class Table: #class Champs:       #afaire changer nom = Table
    nomDB=''
    def __init__(self,nomBase,nomTable, TableBase, auto=True):
        self.nomDB=nomBase              #AFAIRE important creer attribut de classe au lieu d'attribut d'instance=> nomDB et pas self.nomDB
        self.NomTable=nomTable
        self.TableBase=TableBase   #table principale la seule modifiable
        self.DataBase=DataBase(nomBase)   #afaireimportant  passer plutot une reference car ici chq champs a un objet database=>perte memmoire        
#        self.id=-1
        self.lock=False  #true = modification, en cours d edition
#        self.item={'id':-1} #afaire supprimer id, utiliser uniquement self.cleeprimaire
#        self.champ=self.item  #item = ancien nom, a enlever
        self.champ={}
        self.Initialise(auto)

    def Initialise(self, auto): # a surcharger (sauf si auto = true)
        if not auto : 
            pass
#            self.listechamps="id"  #ajouter le nom exact des champs (=comme dans requete sql) SEPARE PAR virgule de la base mysql
#            self.cleeprimaire="id"
#            self.typechamps=['int']
#            self.InitListeChamps()
        else :
            self.listechamps=''
            self.typechamps=[]
            self.typeDuChamp={}
            self.champIsModifiable={}
            self.ListeChampsAuto()
        
    def InitListeChamps(self): #  appeler a la fin de la fonction initialise surchargee
        self.LaListeDesChamps = self.listechamps.split(',')
        self.ChampClassement=self.LaListeDesChamps[0]  #resultat requete classe par defaut sur le 1er champ
        
    def ListeChampsAuto(self):
        requete="SHOW COLUMNS FROM "+self.NomTable+";"
        result=self.RechercheSQL_tableau(requete)
        for unchamp in result :
            self.listechamps += unchamp[0]+','
            self.champIsModifiable[ unchamp[0] ] = False  #par defaut
            self.typechamps .append(unchamp[1])
            self.typeDuChamp[unchamp[0]]= unchamp[1]
            if 'int' in unchamp[1]  or 'float' in  unchamp[1] or 'decimal' in  unchamp[1]  : #initialise a 0 ou '' les champs
                self.champ[unchamp[0]]=0
            else :
                self.champ[unchamp[0]]=''
        self.listechamps=self.listechamps[:-1]
        self.LaListeDesChamps = self.listechamps.split(',')
        if self.LaListeDesChamps[0][:2] == 'id' : # *******************  par defaut le 1er champ = clee primaire commence par 'id....'
            self.cleeprimaire=self.LaListeDesChamps[0]   
        else :
            print 'erreur  ATTENTION pas de clee primaire detectee ***********'
        #print "debug "+str(self.LaListeDesChamps)+"\n"+str(self.typechamps)+'\n'+str(self.typeDuChamp)
        self.ListeChampModifiable()
        
    def ListeChampModifiable(self):
        if not (self.TableBase ) :
            self.TableBase = self.NomTable  #afaire autre solution pour eviter requete c
        requete="SHOW COLUMNS FROM "+self.TableBase+";"
        result=self.RechercheSQL_tableau(requete)
        for champ in result :
            self.champIsModifiable[champ[0]] = True
        self.champIsModifiable[ self.cleeprimaire ] = False
#
#    def FormatUtf8(self, chaine): #debug AFAIRE A COMPLETER pour tous les caracteres accentues
#        #debug ne sert pas
#        if not chaine : return ''
#        return chaine
#        
#        #reste ne sert pas
#        car=chr(232)
#        rempla=chr(195)+chr(168)
#        chaine = replace(chaine,car, rempla) #remplace   e accent aigu    par e accen aigu (RTF8)
#        return chaine
#
#    def ValideChamps(self): #DEBUG AFAIRE A REFAIRE
#        typechaine=type("une chaine")
#        for key in self.item :
#            if type(self.item[key])==typechaine :
#                valide=self.EnleveGuillemets(self.item[key])
#                if valide != -1 :
#                    self.item[key]=valide
#            if self.item[key] == None: 
#                self.item[key]=''  #remplace None par ''
#            
#    def UnValideChamps(self):#DEBUG AFAIRE A REFAIRE
#        for key in self.item :
#            valide=self.EnleveDoubleGuillemets(self.item[key])
#            if valide != -1 :
#                self.item[key]=valide
#            
#    
    def EnleveGuillemets(self,c) :
        try:
            return(string.replace(c,'"','""'))
            
        except:
            return -1
    
    def EnleveDoubleGuillemets(self,c) :
        try:
            return(string.replace(c,'""','"'))
        except:
            return -1

#            
#    def SetId(self,id):                #ATTENTION a utiliser uniquement pour un nouveau client
#            self.id=id                    #verifier que l'id n'est pas deja pris
#            self.item['id']=id
#    def GetId(self):
#        return self.item['id']
#        
    def LectureId(self, id) : #lit la ligne de  nomtable no id  (id = par defaut le 1er champ = clee primaire)
        try :
            requete = "SELECT * FROM "+self.NomTable+" WHERE "+self.cleeprimaire+" = "+str(id)
            result=self.RechercheRequeteSQL(requete)[0]
            i=0
            for element in result :
                self.champ[self.LaListeDesChamps[i] ] = element
                i+=1
#            self.champ['id']=self.champ[self.cleeprimaire]  #afaire supprimer 'id'
        except :
            print " ERREUR Table.lectureId "
            
            
    def RequeteSet(self):
        sql=' SET '
        try :
            for champ in self.champ.keys() :
                if self.champIsModifiable[champ]  and self.champ[champ]:
                    typeduchamp=self.typeDuChamp[champ]
                    if 'int' in typeduchamp or 'float' in  typeduchamp or 'decimal' in  typeduchamp  :  #AFAIRE avec try except
                        sql+= champ + ' = ' + str( self.champ[ champ ] )+','
                    else :
                        sql+= champ + ' = "' + str( self.champ[ champ ] ) +'",'
            sql=sql[:-1]
        except :
            print  'erreur sql:'+sql+'///champ:'+champ
        print 'debug '+sql
        return sql
        
    def EnregistreTable(self) : #si id< cree la ligne sinon update
        if  not(self.Lock) :
            return 'rien a enregister'
        err=''
        if self.champ[self.cleeprimaire] >0 :
            requete = 'UPDATE '+self.NomTable + self.RequeteSet()  +  ' WHERE '+self.cleeprimaire+ ' = ' + str( self.champ[  self.cleeprimaire ]  ) +';'
            err = self.ExecuteSQL( requete)
        else :
            pass #AFAIRE  CREE LIGNE
        
        #if not err :  #AFAIRE BUG err=retourne le nb de champ modifie=1 si ok
        self.UnLock()
            
        return err
        
    def Lock(self) :
        pass # AFAIRE  verifie DB.Table.Lock = 0 pour self.cleeprimaire (si >0 return = idUserLock) (si = 0 => DB.TableLock = idUser)
        self.lock = True
        return 0 # si la table (la ligne) est deja en mode edition par un autre utilisateur, renvoie l'idUserLock (>0 et <>idUser actuel)
        
    def UnLock(self): #uniquement si meme utilisateur 
        if self.lock :
            pass #AFAIRE met DB.Table lock=0
            self.lock = False
            return ''  #sinon return 'erreur table editee  par autre utilisateur'
    
    def SetChamp(self, champ, valeur, enregistre_auto=False) :
        try :
            erreur=''

#            if champ=='id' or not self.champIsModifiable[champ] :  #afaire supprimer 'id' (inutile)
            if  not self.champIsModifiable[champ] :
                erreur = 'Table.SetChamp : champ non modifiable (clee primaire ou table liee)'
                print 'debug INTERDIT de modifier ce champ (clee primaire ou table liee) Table.SetChamp'
                return erreur
                
            if ( not  self.VerifieTypeChamp(champ, valeur) ) :
                erreur ='Table.SetChamp : erreur type champ'
                print 'debug erreur type champ Table.SetChamp'
                return erreur
            
            if not self.lock :  # Lock() uniquement des la 1ere modification, inutile ensuite
                idLock = self.Lock()
                if idLock > 0 :
                    erreur = 'erreur : la table est actuellement editee par un autre utilisateur'
                    return erreur
            
            #si tout est bon : 
            self.champ[champ]=valeur
            if enregistre_auto :
                erreur= self.EnregistreTable()
            return erreur
        except :
            erreur = 'exception Table.SetChamp (erreur champ?)'
            print 'erreur Table.SetChamp'
            return erreur
            
    def VerifieTypeChamp(self, champ, valeur): #debug VERIFIER TOUS LES TYPES
        letype= type(valeur) 
        typechamp=self.typeDuChamp[champ]
        if ( letype is IntType or letype is FloatType ) and  ('char' in typechamp or 'date' in typechamp ):
            return False
        if letype is StringType and not ('char' in typechamp or 'date' in typechamp ):
            return False
        return True
            
#    def ItemTxt(self):  #(obsolette) retourne un texte avec la valeur de chaque champ
#        texte=''
#        for cle in self.item.keys():
#            texte = texte + str(cle) + ":" + str(self.item[cle]) +" "
#        return texte

    def PrintChamp(self):  #(synonyme itemtxt) retourne un texte avec la valeur de chaque champ
        texte=''
        for cle in self. champ.keys():
            texte = texte + str(cle) + ":" + str(self.champ[cle]) +" "
        return texte

#    def Existe(self):
#        if (self.id > 0 ): return 1
#        return 0
    
#    def Id(self):           #SOUS FORME TEXTE
#        return(str(self.id))
#
#    def GetId(self):
#        return(self.id)
    
#    def SetItemId(self,id): # a surcharger dans la classe derivee pour remplir tous les champs
#        self.id=id
#        self.item={'id':id} #afaire arevoir (2 fois id !!!)
#        
    def RechercheSQLMulti(self,*arg): 
        
            
        requete="SELECT "+self.listechamps+" FROM "+self.NomTable
        
        if 'int' in self.typeDuChamp[arg[0] ]  or 'decimal' in self.typeDuChamp[arg[0] ] or 'float' in self.typeDuChamp[arg[0] ]:
            requete+=" WHERE %s = %s "%(arg[0],arg[1])
        else :
            requete+=" WHERE %s LIKE \"%s\" "%(arg[0],arg[1])
        
        i=3
        taille=len(arg)
        while i < taille:
            if 'int' in self.typeDuChamp[arg[i-1] ]   or 'decimal' in self.typeDuChamp[arg[i-1] ]  or 'float' in self.typeDuChamp[arg[i-1] ] :
                requete=requete+" AND %s = %s "%(arg[i-1],arg[i])
            else :
                requete=requete+" AND %s LIKE \"%s\" "%(arg[i-1],arg[i])
            i=i+2
        uneListe=self.DataBase.RechercheSQL_liste(requete)   #uneListe=self.DataBase.RechercheSQL(requete) #=DICO/old
        return uneListe

#        
#    def RechercheSQL(self,champ,rech,order=0,*arg): # AFAIRE TYPE INT ************* #recherche tous les items avec requete SQL champ LIKE rech
#        requete="SELECT "+self.listechamps+" FROM "+self.NomTable  +" WHERE %s LIKE \"%s\""%(champ,rech)
#        if (order): #AFAIRE UTILISER FONCTION REQUETE
#            if arg[0]:
#                requete=requete+" ORDER BY "
#                for s in arg[0] :
#                    requete=requete+s+","
#                if (requete[len(requete)-1]==","):requete=requete[0:len(requete)-1]#efface dernier ","
#            else:
#                requete=requete+" ORDER BY "+self.ChampClassement  #classement par defaut
#                
#        uneListe=self.DataBase.RechercheSQL_liste(requete)   #uneListe=self.DataBase.RechercheSQL(requete) #=DICO/old
#        return uneListe

#    def Delete(self): #suppression de l'item de la base de donee
#        sql="DELETE FROM "+split(self.NomTable)[0]+" WHERE "+split(self.listechamps,",")[0]+"="+str(self.id) #split(nomtable) car nomtable peut etre complexe (ex: Client LEFT OUTER JOIN)
#        result=self.ExecuteSQL(sql)
#        if result < 1 :
#            result=0            #erreur -1 ou  aucun effacement
#        return result           #1=> ok  0=>err
        
    def RechercheRequeteSQL(self,requete):
        uneListe=self.DataBase.RechercheSQL_liste(requete)   #uneListe=self.DataBase.RechercheSQL(requete) #=DICO/old
        return uneListe
    
#        
#    def Requete(self,champ,rech,order=0,*arg): #recherche tous les items avec requete SQL champ LIKE rech
#        requete="SELECT "+self.listechamps+" FROM "+self.NomTable  +" WHERE %s LIKE \"%s\""%(champ,rech)
#        if (order):
#            if arg[0]:
#                requete=requete+" ORDER BY "
#                for s in arg[0] :
#                    requete=requete+s+","
#                if (requete[len(requete)-1]==","):requete=requete[0:len(requete)-1]#efface dernier ","
#            else:
#                requete=requete+" ORDER BY "+self.ChampClassement  #classement par defaut
#        return requete

#
#        
#    def RechercheSQL_dico(self,requete):  
#        dico=self.DataBase.RechercheSQL_dico(requete)
#        return dico
#    
    def RechercheSQL_tableau(self,requete):  
        return self.DataBase.RechercheSQL_tableau(requete)
    
    def ExecuteSQL(self,requete): #requete insert ou update
        return self.DataBase.ExecuteSQL(requete) 
        



if __name__ == "__main__":
    test=Table(DATABASE,'Personne', '', auto=True)    
    table_client=Table(DATABASE, 'viewClient','Personne',  auto=True)
    
#    print "recherche sur nom =>"
#    print test.RechercheSQLMulti("Prenom",'Yvon','Nom','%POINT%')
    print "recherche sur nom et client =>"
    print test.RechercheSQLMulti("isClient",'TRUE','Nom','%POINT%')
    
    
#    print "recherche sur nom et pas client =>"
#    print test.RechercheSQLMulti("isClient",'FALSE','Nom','%POINT%')
#    
    print "recherche dans viewclient =>"
    print table_client.RechercheSQLMulti('Nom', '%PO%')
    
    print "lecture un id"
    table_client.LectureId(1)
    print table_client.PrintChamp()
    
    #AFAIRE   SAUVEGARDE : facile pour tables simples, plus compliquee pour view
    print 'set champ id (interdit)'
    table_client.SetChamp('idPersonne',5)
    
    print 'set champ prenom'
    table_client.SetChamp('Prenom','Kanya2') 
    print table_client.PrintChamp()
    
    print 'enregistre client'
    err=table_client.EnregistreTable()
    print 'fin enregistre client '+str(err)

    print 'set champ CIP : interdit'
    table_client.SetChamp('CIP','60000') 
