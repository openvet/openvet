#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('./VetCore')
sys.path.append('./VetGUI')

import config
from gestion_erreurs import *


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


def TestCreation():
        raw_input("creation de 2clients et affichage tapez <entrée>")
        unclient=Table(DATABASE, 'viewClient','Personne',  auto=True)
#        unclient.Efface()

        unclient.SetChamps(enregistre_auto=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom='POINT',Prenom='Yvon', IsVeterinaire=True )
        mon_id=unclient.Id()  #memorise l'id

        unclient.Efface()
        unclient.SetChamps(enregistre_auto=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom='DUPONT',Prenom='Lajoie', IsVeterinaire=False)
        print unclient.PrintChamp(False) 
        
        unclient.LectureId(mon_id) #recharge le 1er client crée et l'affiche
        print unclient.PrintChamp(False)
        
        raw_input("creation de 2 animaux et affichage tapez <entrée>")
        unanimal=Table(DATABASE, 'Animal',  auto=True)
        unanimal.SetChamps(enregistre_auto=True,  Especes_idEspeces=1, Nom='Lechat')
        id_animal1= unanimal.Id()
        print unanimal.PrintChamp()
        unanimal.Efface()
        unanimal.SetChamps(enregistre_auto=True,  Especes_idEspeces=2, Nom='Lechien')
        print unanimal.PrintChamp()
        
        raw_input("création lien animal/client et affichage tapez <entrée>")
        tablelien=Table(DATABASE, 'ClientAnimalRef ',  auto=True)
        
        tablelien.SetChamps(enregistre_auto=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =mon_id)
        tablelien.Efface()
        tablelien.SetChamps(enregistre_auto=True,  Animal_idAnimal= id_animal1, Client_idClient =mon_id)
        print tablelien.PrintChamp()
        
def TestLiaison():        
        print '************* LIAISON TABLE ANIMAL CLIENT***************'
        unclient=Table(DATABASE, 'viewClient','Personne',  auto=True)
        unanimal=Table(DATABASE, 'Animal',  auto=True)
        tablelien=Table(DATABASE, 'ClientAnimalRef ',  auto=True)
        #TODO: classe ListeTable
        mon_id=unclient.RechercheRequeteSQL('SELECT idPersonne FROM Personne WHERE Nom="POINT" and Prenom="Yvon"')[0][0]
        raw_input("création objet LienTable et affichage tapez <entrée>")
        lien_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
        lien_client_animal.ActualiseListe(mon_id )
        print lien_client_animal.PrintEnfant()
       
       
def TestCreation2():
    print 'Creation de 2 clients et 4 animaux '
    unclient=Table(DATABASE, 'viewClient','Personne',  auto=True)
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom='DURAND',Prenom='Jean', IsVeterinaire=False)
    unautreclient=unclient.New()
    unautreclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom='MARTIN',Prenom='Jacques', IsVeterinaire=False)
    
    unanimal=Table(DATABASE, 'Animal',  auto=True)
    tablelien=Table(DATABASE, 'ClientAnimalRef ',  auto=True)
    
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=1, Nom='Grosminet')
    unautreanimal=unanimal.New()
    unautreanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=2, Nom='Bob')
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unautreanimal.Id(), Client_idClient =unclient.Id())

    table_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
    table_client_animal.LectureId(unclient.Id())
    print table_client_animal.PrintParent()
    print table_client_animal.PrintEnfant()

def TestCreation3():
    clients=[ ['Durand', 'Jean'], ['Dupond', 'Jacques'], ['Albert', '1er']]
    animaux=[[1, 'Grosminet'], [2, 'Bob'], [1, 'Lechat'], [2, 'Lechien'], [1, 'chat2'], [2, 'chien2']]
    idclients=[]
    
    nbclient=len(clients)
    i=0
#    unclient=Table(DATABASE, 'viewClient','Personne',  auto=True) #ATTENTION ne pas confondre viweClient  viewPersonne
    unclient=Table(DATABASE, 'viewPersonne','Personne',  auto=True)
    unanimal=Table(DATABASE, 'Animal',  auto=True)
    tablelien=Table(DATABASE, 'ClientAnimalRef ',  auto=True)

    print '-----------------creation de 3 clients avec chacun 2 animaux ----------'
    while ( i < nbclient) :
        nomclient=clients[i][0]
        prenomclient=clients[i][1]
        unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False)
        idclients.append(unclient.Id() )
        i+=1
        a=0 
        while (a<2) :
            animal=animaux.pop()
            espece=animal[0]
            nomanimal=animal[1]
            unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
            tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
            a+=1
        
    print '--------------------affichage des 3clients et animaux ----------------\n'
    table_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
    
    for idC in idclients :
        raw_input("tapez <entrée>")
        print ' ++++++++++++++ CLIENT No '+str(idC)+'+++++++++++++++++++++\n'
        table_client_animal.LectureId(idC)
        print table_client_animal.PrintParent()
        print table_client_animal.PrintEnfant()
        print '\n'
        
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
    
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=True, IsClient=False)
    idveto=unclient.Id()

    nomclient='EASTWOOD'
    prenomclient='Clint'
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
    espece=1
    nomanimal='Grosminet'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)

    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())

    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam1', Traitement='ttt1')
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam2', Traitement='ttt2')

    espece=2
    nomanimal='Oscar'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam4', Traitement='ttt4')
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam3', Traitement='ttt3')

    espece=1
    nomanimal='Lechat'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam lechat', Traitement='ttt12')
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam2 lechat', Traitement='ttt22')
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam3 lechat', Traitement='ttt23')

    nomclient='DUPONT-LAJOIE'
    prenomclient='Berthe'
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
    espece=1
    nomanimal='Mimi'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)

    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())

    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam1', Traitement='ttt1')
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam2', Traitement='ttt2')

    espece=2
    nomanimal='Surcouf'
    unanimal.SetChamps(enregistre_nouveau=True,  Especes_idEspeces=espece, Nom=nomanimal)
    tablelien.SetChamps(enregistre_nouveau=True,  Animal_idAnimal= unanimal.Id(), Client_idClient =unclient.Id())
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam4', Traitement='ttt1')
    tableconsult.SetChamps(enregistre_nouveau=True, Animal_idAnimal= unanimal.Id(), Personne_idConsultant=idveto, Examen='exam3', Traitement='ttt2')



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


if __name__ == '__main__':
    global USER,  PWD

    err=Login()
    if not err :
        #print '************ CREATION DE CLIENTS / ANIMAUX ***************'
#        TestCreation()
#        TestLiaison()
#        TestCreation2()
#        TestCreation3()


        print '************ CREATION DE CLIENT / ANIMAUX /  CONSULTS***************'
        TestFillConsult()
    
        TestChercheEtAfficheTableLiee(AffichageSimple=True)
            
