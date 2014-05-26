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
    
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=True, IsClient=False, IsConsultant=True)
    idveto=unclient.Id()

    nomclient='EASTWOOD'
    prenomclient='Clint'
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
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
    unclient.SetChamps(enregistre_nouveau=True,  Civilite_idCivilite=2,  Commune_idCommune=1, Nom=nomclient,Prenom=prenomclient, IsVeterinaire=False, IsClient=True)
    
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


if __name__ == '__main__':
    global USER,  PWD

    err=Login()
    if not err :

        print '************ CREATION DE CLIENT / ANIMAUX /  CONSULTS***************'
        TestFillConsult()
    
        TestChercheEtAfficheTableLiee(AffichageSimple=True)
            
