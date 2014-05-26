# -*- coding: utf8 -*-


import sys
sys.path.append('..')

import MySQLdb
import config
from PyQt4 import QtCore

#AFFICHE_CONSOLE=config.DEBUG_AFFICHE_MESSAGE_CONSOLE
AFFICHE_CONSOLE=1
DATABASE=config.database
IDUSER=config.IDUSER


class DataBase:
    """gère la connexion et l'exécution de requêtes sql
    input : nom de la base, user, password"""
    
    def __init__(self,nomD, USER=config.user, PWD=config.password):
        self.dbCodec=config.dbCodec     #'ISO-8859-1'
        self.nomDB=nomD
        self.user=USER
        self.pwd=PWD
        self.InitialiseDB()
        
    def InitialiseDB(self): # a surcharger
        pass
        
    def PrintDB(self):
        print self.nomDB

    def Connection(self):
        """se connecte à la base et renvoie une connexion"""
        try :
            conn=MySQLdb.connect('localhost',self.user,self.pwd,self.nomDB)  
        except :
            msg="Erreur Table.py classDataBase Connection(self) ************* VERIFIEZ database + password (+/-config.py)  ******"
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg
        return conn #ou msg erreur=> tester type(conn)

    def RechercheSQL_id(self,requete):
        """input : requête sql
        return : liste résultats ou msg d'erreur (tester type)"""
        conn = self.Connection() 
        if type(conn)==type('str') : return conn  #= msg d'erreur
        try:
            cur=conn.cursor()
            cur.execute(requete)
            liste=cur.fetchall()
            cur.close()
        except :
            msg="Erreur Table.py classDataBase RechercheSQL_liste() "
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg
        if liste is None:
            return None
        else:
            return liste[0][0]

    def RechercheSQL_liste(self,requete):
        """input : requête sql
        return : liste résultats ou msg d'erreur (tester type)"""
        conn = self.Connection() 
        if type(conn)==type('str') : return conn  #= msg d'erreur
        try:
            cur=conn.cursor()
            cur.execute(requete)
            liste=cur.fetchall()
            cur.close()
        except :
            msg="Erreur Table.py classDataBase RechercheSQL_liste() "
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
            msg="Erreur Table.py RechercheSQL_dico() "
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
            msg="Erreur Table.py RechercheSQL_tableau() "
            msg+='\n'+str(sys.exc_info()[1])
            if AFFICHE_CONSOLE :
                print msg
            return msg    
        return dico

    
    def ExecuteSQL(self,requete,Returnid=False):   
        """ requête= uniquement de modification (pas de recherche) \            
        return = nb de lignes modifiees ou msg d'erreur (tester type)"""
        result=''
        id=0
        conn = self.Connection() 
        if type(conn)==type('str') : return conn
        try:
            cur=conn.cursor()
            cur.execute(requete)
            if Returnid:
                cur.execute("SELECT LAST_INSERT_ID()")
                id=cur.fetchall()[0][0]
            conn.commit()
            cur.close()
            return id
        except :
            result ="Err Database.ExecutSQL Execution "+str(requete)+" "+str(result)
            result+='\n'+str(sys.exc_info()[1])
            return result           
#        return result
    
    def ExecuteMultiSQL(self,requetes):   
        """ requête= uniquement de modification (pas de recherche) \            
        return = nb de lignes modifiees ou msg d'erreur (tester type)"""
        result=''
        conn = self.Connection() 
        if type(conn)==type('str') : return conn
        try:
            cur=conn.cursor()
            conn.begin()
            for i in requetes:
                cur.execute(i)
            conn.commit()
            cur.close()
        except :
            conn.rollback()
            result ="Err Database.ExecutSQL Execution "+str(requetes)+" "+str(result)
            result+='\n'+str(sys.exc_info()[1])
            return result           
        return result
 
    
    def GetFields(self,table):
        result=[]
        res=self.RechercheSQL_liste("SHOW COLUMNS FROM %s"%table)
        for i in res:
            result.append(i[0])
        return result
            
                                    
    def DbAdd(self,table,valeurs,Returnid=False):
        valeurs=','.join(valeurs)
        return self.ExecuteSQL("INSERT INTO %s VALUES (%s)"%(table,valeurs),Returnid)
    
    
    def DbAddLinked(self,tables,values):
        requetes=[]
        for table,valeurs in zip(tables,values):
            valeurs=','.join(valeurs)
            requetes.append("INSERT INTO %s VALUES (%s)"%(table,valeurs))
        print self.ExecuteMultiSQL(requetes)
        
    def DbUpdate(self,table,champs,valeurs):
        idtable='='.join(zip(champs,valeurs)[0])
        sets=','.join(['='.join(i) for i in zip(champs,valeurs)[1:]])
#        print "UPDATE %s SET %s WHERE %s"%(table,sets,idtable)
        self.ExecuteSQL("UPDATE %s SET %s WHERE %s"%(table,sets,idtable))
        
    def DbDelete(self,table,ids):
        self.ExecuteSQL("DELETE FROM %s WHERE %s"%(table,'='.join(ids)))
        
    def GetDbLines(self,request):
        clst=[]
        res=self.RechercheSQL_liste(request)
        if len(res)==0:
            return([])
        for i in res:
            tmp=[]
            for j in i:
                if not j is None:
                    tmp.append(QtCore.QString(str(j).decode(self.dbCodec)))
                else:
                    tmp.append(QtCore.QString(''))
            clst.append(tmp)
        return clst

    def GetDbText(self,request):
        clst=[]
        res=self.RechercheSQL_liste(request)
        if len(res)==0:
            return([])
        for i in res[0]:
            if not i is None:
                clst.append(QtCore.QString(str(i).decode(self.dbCodec)))
            else:
                clst.append(QtCore.QString(''))
        return clst

    def GetDbidText(self,request,defaut=None):
        clst=[]
        if not defaut is None:
            clst.append([0,QtCore.QString(defaut)])
        res=self.RechercheSQL_liste(request)
        for i in res:
            txt=QtCore.QString(i[1].decode(self.dbCodec))
            clst.append([i[0],txt])
        return clst
    
if __name__ == '__main__':
    DBase=DataBase(config.database)
    print DBase.DbAdd('PathologieSynonyme',['0','1','\"Rien\"'],True)