#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('./VetCore')
sys.path.append('./VetGUI')
sys.path.append('./initialiseDB')

import config
from gestion_erreurs import *

import os
from subprocess import Popen, PIPE
import subprocess

import DbPopulate


#from PyQt4 import QtCore, QtGui
from Tables import *
#import Gui_openvet

DATABASE=config.database
IDUSER=config.IDUSER

def Login():
    global USER,  PWD
     
    USER =config.user
    PWD=config.password
#    PWD='test mauvais pwd'
    
    msgErreur=None
    conn = TestConnexionBase()
    if type(conn)== type("string"):
        msgErreur='openvet.py Login() '+conn
        AfficheErreur(msgErreur)
    return msgErreur
    
    
def TestConnexionBase():
    #TODO:   verifie en mm tps la base et le login
    Err=None
    db=DataBase(DATABASE, USER, PWD)
    conn = db.Connection()
    return conn



        
def TestFillConsult():
    unclient=Table(DATABASE, 'viewPersonne','Personne')#,  auto=True)
    unanimal=Table(DATABASE, 'Animal')#,  auto=True)
    tablelien=Table(DATABASE, 'ClientAnimalRef')# ,  auto=True)
    tableconsult=Table(DATABASE, 'Consultation')

    nomclient='LEVETO'
    prenomclient='Bob'
    
    nb = unclient.ActiveSQL(False,'Nom', 'LEVETO') #verifie si déjà crée
    if nb>0 :
        print "clients déjà crées"
        return
    idcommune=10342
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=idcommune, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=True, IsClient=False, IsConsultant=True)
    idveto=unclient.Id()

    nomclient='EASTWOOD'
    prenomclient='Clint'
    idcommune=899
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=idcommune, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
    espece=1
    nomanimal='Grosminet'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)

    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    
    date='16/05/2014'
    typeconsult=2
    
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam1', Traitement='ttt1', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam2', Traitement='ttt2', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)

    espece=2
    nomanimal='Oscar'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam4', Traitement='ttt4', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam3', Traitement='ttt3', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)

    espece=1
    nomanimal='Lechat'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam lechat', Traitement='ttt12', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam2 lechat', Traitement='ttt22', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam3 lechat', Traitement='ttt23', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)

    nomclient='DUPONT-LAJOIE'
    prenomclient='Berthe'
    idcommune=5641
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=idcommune, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
    espece=1
    nomanimal='Mimi'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)

    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())

    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam1', Traitement='ttt1', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam2', Traitement='ttt2', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)

    espece=2
    nomanimal='Surcouf'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam4', Traitement='ttt1', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam3', Traitement='ttt2', DateConsultation=date, TypeConsultation_idTypeConsultation=typeconsult)



def TestChercheEtAfficheTableLiee(AffichageSimple=True):
    
    unclient=Table(DATABASE, 'viewPersonne','Personne')#,  auto=True)
    unanimal=Table(DATABASE, 'Animal')#,  auto=True)
    tablelien=Table(DATABASE, 'ClientAnimalRef ')#,  auto=True)
    uneconsult=Table(DATABASE, 'Consultation')

    #table_animal_consultation=TableLiee(unanimal, uneconsult, 'idAnimal', 'Animal_idAnimal') #ATTENTION ERR => relation 1:1
    
    table_animal_consultation=TableLiee(unanimal, uneconsult, None, 'Animal_idAnimal')#relation 1:n
    table_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
    

#    nbresult=table_client_animal.ActiveSQL(True,'Nom', 'EASTWOOD2')
#    print nbresult
#    print table_client_animal.PrintParentEnfant()
#    nbresult=table_animal_consultation.ActiveSQL(True,'Nom', 'Grosminet2')
#    print table_animal_consultation.PrintParentEnfant()
    
    
    table_client_animal_consultation=TableLiee(unclient,  table_animal_consultation, 'Animal_idAnimal', 'Client_idClient' , tablelien  )
    table_client_animal_consultation.ActiveSQL(True,'Nom', 'EASTWOOD')
        
    if AffichageSimple :
        print 'affiche client/animaux/consultations (format simple)'
        print table_client_animal_consultation.PrintParentEnfant()
    else :
        print 'affiche client/animaux/consultations (format détaillé)'
        print table_client_animal_consultation.PrintParentEnfant(etiquettes=True)
        
    print ' Changement de client :'
    print " table_client_animal_consultation.ActiveSQL(True,'Nom', 'DUPONT-LAJOIE') "
    table_client_animal_consultation.ActiveSQL(True,'Nom', 'DUPONT-LAJOIE')

    if AffichageSimple :
        print 'affiche client/animaux/consultations (format simple)'
        print table_client_animal_consultation.PrintParentEnfant()
    else :
        print 'affiche client/animaux/consultations (format détaillé)'
        print table_client_animal_consultation.PrintParentEnfant(etiquettes=True)



def CreationDB():
    global USER,  PWD
    

    
     
    USER =config.user
    PWD=config.password
    f='openvet13_1.sql'
    
    
    cmd='mysql -u '+USER+' -p'+PWD+' <'+f
#    result=os.popen(cmd)
#    err=result.read()

    
    p='-p'+PWD
    

#    p1 = Popen(["mysql", '-u', USER, p,'<',  f], stdout=PIPE, stderr=PIPE)#Pb redirection '<' ne fonctionne pas => essayer shell
#    result=p1.communicate()

#    p1 = Popen(["mysql", '-u', USER, p,'<',  f],  shell=True) # err bloque a communicate
#    result=p1.communicate()

#    err=result[1]
#    if err :
#        print '-----------------------------------------------------------------'
#        print '-----------------------------------------------------------------'
#        print '*******Err creation DB'+err
#        print '-----------------------------------------------------------------'
#        print '-----------------------------------------------------------------'


#    try :
#        #subprocess.check_call('l564s -l4969+4E', shell=True)
#        result=subprocess.check_output('l564s -l4969+4E', shell=True)
#    except subprocess.CalledProcessError as err:  # pb impossible de recuperer message d'erreur (seulemnt code,etc...)
#        print '-----------------------------------------------------------------'
#        print '-----------------------------------------------------------------'
#        print '*******Err creation DB'+err
#        print '-----------------------------------------------------------------'
#        print '-----------------------------------------------------------------'
#        


    print 'Création database'
    p1 = Popen(cmd,  stdout=PIPE, stderr=PIPE,  shell=True) # err bloque a communicate
    result=p1.communicate()

    err=result[1]
    if err :
        print '-----------------------------------------------------------------'
        print '-----------------------------------------------------------------'
        print '*******Err creation DB'+err
        print '-----------------------------------------------------------------'
        print '-----------------------------------------------------------------'

    else :
        print 'fin Création database OK'



def AppliquePatch():
    global USER,  PWD
     
    USER =config.user
    PWD=config.password
    f='openvet13_1patch.sql'
    
    
    cmd='mysql -u '+USER+' -p'+PWD+' <'+f
    p='-p'+PWD
    print 'patch DB :'+f
    p1 = Popen(cmd,  stdout=PIPE, stderr=PIPE,  shell=True) # err bloque a communicate
    result=p1.communicate()

    err=result[1]
    if err :
        print '-----------------------------------------------------------------'
        print '-----------------------------------------------------------------'
        print '*******Err patch DB'+err
        print '-----------------------------------------------------------------'
        print '-----------------------------------------------------------------'

    else :
        print ' OK'
        
def ExecuteCommande(commande):
    print 'commande  :'+commande
    p1 = Popen(commande,  stdout=PIPE, stderr=PIPE,  shell=True) # err bloque a communicate
    result=p1.communicate()

    err=result[1]
    if err :
        print '-----------------------------------------------------------------'
        print '-----------------------------------------------------------------'
        print '*******Err commande '+err
        print '-----------------------------------------------------------------'
        print '-----------------------------------------------------------------'

    else :
        print ' OK'



def SauveDB():
    global USER,  PWD    
    commande='mysqldump -u '+USER+' -p'+PWD+' OpenVet13 > sauvegardeDB.sql'
    ExecuteCommande(commande)

def RestaureDB():
    global USER,  PWD
    f='sauvegardeDB.sql'
    commande='mysql -u '+USER+' -p'+PWD+  ' -D '+config.database +    ' <'+f
    ExecuteCommande(commande)


if __name__ == '__main__':
    global USER,  PWD

    err=Login()
    
#    SauveDB()
    
    if os.path.exists('sauvegardeDB.sql'):
        print 'Restaure DB'
        RestaureDB()
        print 'fin'
        
    else :
        
        
        if err :
            CreationDB()
        
        err=Login()
        
        if not err :
            DbPopulate.FillCommunesAndRaces()
            print '************ CREATION DE CLIENT / ANIMAUX /  CONSULTS***************'
            TestFillConsult()
            AppliquePatch()
            TestChercheEtAfficheTableLiee(AffichageSimple=True)
                
