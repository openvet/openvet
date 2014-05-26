# -*- coding: utf8 -*-


import sys
sys.path.append('..')

import MySQLdb
import config

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

    
    def ExecuteSQL(self,requete):   
        """ requête= uniquement de modification (pas de recherche) \            
        return = nb de lignes modifiees ou msg d'erreur (tester type)"""
        result=''
        conn = self.Connection() 
        if type(conn)==type('str') : return conn
        try:
            cur=conn.cursor()
            cur.execute(requete)
            conn.commit()
            cur.close()
        except :
            result ="Err Database.ExecutSQL Execution "+str(requete)+" "+str(result)
            result+='\n'+str(sys.exc_info()[1])
            return result           
        return result
                                    
