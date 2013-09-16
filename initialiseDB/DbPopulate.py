#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myrequest as db
from datetime import date,  datetime
import random
import os
import parametres

repertoire=parametres.repertoire
user=parametres.user
password=parametres.password
database=parametres.database
VilleCompletes=parametres.VilleCompletes


def FillCommunesAndRaces():
    
    #os.system("mysql -u %s -p%s -e\"LOAD DATA LOCAL INFILE '/home/francois/Programmes/Kiwi/OpenVet/OpenVet/communes.csv' INTO TABLE %s.Commune FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n';\""%(user,password,table))
    #os.system("mysql -u %s -p%s -e\"LOAD DATA LOCAL INFILE '/home/francois/Programmes/Kiwi/OpenVet/OpenVet/races.csv' INTO TABLE %s.Race FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n';\""%(user,password,table))
    #ne semble pas marcher avec les foreign key, même si la table est vide d'où la methode brute et lente:
    fin=open(repertoire+'communes.csv','r')
    print "Fill commune";
    t1=datetime.now()
    
    if VilleCompletes :  #nouvelle version : toutes les villes de france
        FillCommunes()
    else :#ancienne version
        err2=err1=None
        matable=db.Table('Commune')  #sans validation, plus rapide
        for i in fin:
            w=i.split(';')
            data=[None,w[0],w[1],int(w[2])] 
            #print tuple(data)
            err2=matable.add(tuple(data), True)
            
    fin.close()
    t2=datetime.now()
    (err, res)=db.execute("select count(*) from Commune") 
    print "Nb communes = "+ str(  res[0][0])
    delta = t2-t1
    print str(delta.seconds)+'.'+str(delta.microseconds)+' seconds'
    
    FillRaces()
    
def FillRaces():    
    fin=open(repertoire+'races.csv','r')
    counts=[]
    print "Fill races";
    t1=datetime.now()
    for i in fin:
        w=i.split(';')
        counts.append(int(w[1]))
        data=[None,w[0],int(w[1])]
        #print tuple(data)
        #toujours la M... avec les caractères accentués. Les tables sont pourtant en UTF-8 et lorsque la requête est réalisée dans work bench ça marche : à revoir plus tard
        (err1,err2)=db.add('Race',tuple(data))
    fin.close()
    t2=datetime.now()
    (err, res)=db.execute("select count(*) from Race") 
    print "Nb races = "+ str(  res[0][0])
    delta = t2-t1
    print str(delta.seconds)+'.'+str(delta.microseconds)+' seconds'
    
def CreateListeRobes():
    global robechat, robechien
    robechien=[]
    robechat=[]
    
    fin=open(repertoire+'robes.csv','r')
    counts=[]
    print "liste robes";
    t1=datetime.now()
    for i in fin:
        w=i.split(';')
        if (int(w[1]))==1 :
            robechat.append(w[0])
        elif int(w[1])==2 :
            robechien.append(w[0])
                
    fin.close()
    t2=datetime.now()

    delta = t2-t1
    print str(delta.seconds)+'.'+str(delta.microseconds)+' seconds'

#def FillNomRue():
#    res=db.execute("SELECT idCommune FROM Commune")
#    l=[int(i[0]) for i in res[1]]
#    for i in l:
#        for j in xrange(random.randint(3,60)):
#            data=[None,i,GetVarChar(40)]
#            print db.add('NomRue',tuple(data))

def FillNomRue() :
    global listerues
    cipprecedant=''
    idville=''
    
    EffaceChamp('NomRue')
    if not listerues :
        LitFichierRue()
    for rueville in listerues :
        rue=rueville[0]
        cip=rueville[1]
        
        try :
            if cip<>cipprecedant :
                res=db.execute("SELECT idCommune FROM Commune where CIP="+cip)
                idville=int(res[1][0][0])
                
            if database=='OpenVet10b' or database=='OpenVet10c':
                db.add('NomRue', [None, idville, rue])
            else :
                db.add('NomRue', [None, rue])
                res=db.execute('SELECT idNomRue FROM NomRue where NomRue="'+rue+'";')
                idnomrue=int(res[1][0][0])
                db.add('Commune_has_Rue', [idnomrue, idville], False)
                
            cipprecedant=cip
        except :
            print 'err fillnomrue'
            
        

def GetVarChar(maxlength, variation=0.3):
#    Nom=''
#    for i in xrange(random.randint(int(maxlength*variation),maxlength)):
#        Nom=Nom+chr(random.randint(65,90))
#    return(Nom[0]+Nom[1:].lower())
    return GetCommentaire(maxlength, variation)
#    
def GetCommentaire(maxlength, variation=0.3):
    global fichier_comm, texte_restant
    
    try :
        if not fichier_comm : #ouvre le fichier la 1ere fois
            fichier_comm = open(repertoire+'commentaires.txt','r')
            texte_restant=''

        taille=random.randint(int(maxlength*variation),maxlength)
        texte=fichier_comm.read(taille-len(texte_restant))
        texte=texte_restant+texte  #ajoute le texte non utilise lors du precedant appel de GetCommentaire
        index=texte.rfind('.')  #coupure si possible a la fin d'une ligne
        if index>0 and index<len(texte) :
            texte_restant=texte[index+1:] #sauve apres la coupure pour le prochain commentaire
            return(texte[:index] )
        if index == len(texte):
            texte_restant=''
            return(texte)
        if index<=0 : #pas de ligne entiere, couper a la fin du dernier mot entier
            index=texte.rfind(' ')
            if index>0 and index<len(texte) :
                texte_restant=texte[index+1:]
                return(texte[:index] )
            if index == len(texte):
                texte_restant=''
                return(texte)
            if index<=0 : #texte vide, fin de fichier?
                fichier_comm.close()
                fichier_comm=''
            
  
    except :
        print "err fichier commentaire (proba EOF) "
        fichier_comm.close()
        fichier_comm=''
        return('')

def GetDate(maxyears):
    end= date.today()
    newdate=date.fromordinal(end.toordinal()-random.randrange(365*maxyears))
    return '%i-%02i-%02i'%(newdate.year,newdate.month,newdate.day)

def Getid(table):
    dicotable={'Civilite':5,'Commune':38950,'Especes':3}
    return random.randrange(dicotable[table])+1

def GetIdNomRueDeCommune(idCommune):
    try :
        res=db.execute("SELECT idNomRue FROM NomRue WHERE Commune_idCommune=%i"%idCommune)
        l=[int(i[0]) for i in res[1]]
        return random.choice(l)
    except :
        print 'err GetIdNomRueDeCommune'
        
def GetRueDeCommune(idCommune):
    try :
        if database=='OpenVet10c':
            res=db.execute("SELECT idNomRue,NomRue FROM NomRue WHERE Commune_idCommune=%i"%idCommune)
            #l=[int(i[0]) for i in res[1]]
            l=res[1]
        else : #openvet10d et suivants
            res=db.execute("SELECT idNomRue,NomRue FROM Commune INNER JOIN Commune_has_Rue ON idCommune=Commune_idCommune INNER JOIN NomRue ON NomRue_idNomRue=idNomRue")
            l=res[1]
        return random.choice(l)
    except :
        print 'err GetNomRueDeCommune'

def GetIdRue(nomrue):
    requete="SELECT idNomRue FROM NomRue WHERE NomRue='"+nomrue+"';"
    res=db.execute(requete)
    return( res[1][0][0] )
def GetRace(espece):
    global listechiens,listechats,listelapins
    dico={1:listechats,2:listechiens,3:listelapins}    #races disponibles par espece
    return random.choice(dico[espece])
    
def GetRobe(espece) :
    if espece==1 :
        robe=random.choice(robechat)
    else :
        robe=random.choice(robechien)
    return(robe)
        
def GetTelephones():
    tels=[]
    Nb=random.randrange(5)
    for i in range(Nb):
        tel='0'
        for j in range(9):
            tel=tel+chr(random.randint(48,57))
        tels.append(tel)
    return tels
 
def NewClient():
    data=[None]
    data.append(Getid('Civilite'))
    ( prenom ,  nom)=GetNom()
    data.append(nom)  
    data.append(prenom)
    if random.random()>0.9:
        #data.append(GetVarChar(180,0.1))#remarque
        data.append(GetCommentaire(180,0.1))#remarque
    else:
        data.append('')
        
    (rue, cip)=GetRue()
    #data.append(GetVarChar(110))#adresse
    data.append(rue)#adresse
    data.append(Getid('Commune'))
    #print data
    db.add('Client',tuple(data))
    tels=GetTelephones()
    res=db.execute("SELECT MAX(idClient) FROM Client")
    idClient=int(res[1][0][0])
    for i in tels:
        data=[None,'Client',idClient]
        data.append(i)#telephone
        data.append('')#email
        if random.random()>0.9:
            data.append(GetVarChar(180,0.1))#remarque
        else:
            data.append('')
        if i==tels[0]:
            data.append(1)
        else:
            data.append(0)
        data.append('NULL')
        #print data
        (err1,err2)=db.add('Repertoire',tuple(data))
        return idClient

def GetNom():
    global listenoms, max_nom, curseur_nom
    if curseur_nom>=max_nom :
        curseur_nom=0
    nomprenom=listenoms[curseur_nom]
    curseur_nom+=1
    return(nomprenom)
    
def GetRue():
    global listerues, max_rue, curseur_rue
    if curseur_rue>=max_rue :
        curseur_rue=0
    rueville=listerues[curseur_rue]
    curseur_rue+=1
    return(rueville)
def AjouteRue(idrue, idCommune):  
    res=db.execute("SELECT count(*) FROM NomRue where idNomRue="+str(idrue)+" AND Commune_idCommune="+str(idCommune))
    nb=int(res[1][0][0])
    if nb<1 :
        db.add('NomRue', [None, idCommune, idrue])  #ne focntionne pas (contrainte), openvet10c :la table nomrue ne devrait pas avoir idcommune si on veut associer une rue a plusieurs communes
def NewClient2():
    data=[None]
    data.append(Getid('Civilite'))
    (prenom, nom)=GetNom()
    data.append(nom)  
    data.append(prenom)
    if random.random()>0.9:
        #data.append(GetVarChar(180,0.1))#remarque
        data.append(GetCommentaire(180,0.1))#remarque
    else:
        data.append('')
    #print db.add('Client',tuple(data)) #debug
    db.add('Client',tuple(data)) 
    res=db.execute("SELECT MAX(idClient) FROM Client")
    try:
        idClient=int(res[1][0][0])
    except :
        idClient=1
        
    if database== "OpenVet10c" :
        data=[None,'Client',idClient]
    else :
        data=[None] #openvet>10c   pas de ref client dans table adresse
        
    #idCommune=Getid('Commune')
    CIPCommune=random.randint(75001,75020)
    res=db.execute("SELECT idCommune FROM Commune WHERE CIP="+str(CIPCommune) )
    idCommune=int(res[1][0][0])
    res=GetRueDeCommune(idCommune)
    idRue=int(res[0])
    nomrue=res[1]
    
    #data.extend([idCommune,GetIdNomRueDeCommune(idCommune),GetVarChar(20),True,True,GetDate(20),'NULL'])
    if database== "OpenVet10c" :
        data.extend([idCommune,idRue,nomrue,True,True,GetDate(20),'NULL'])
    else :
        data.extend([idCommune,idRue,str(random.randint(1, 99)),True,True,GetDate(20),'NULL'])
    
#    (NomRue, CIP)=GetRue()
#    idrue=int( GetIdRue(NomRue) )
#    AjouteRue(idrue, idCommune)
#    data.extend([idCommune,idrue,GetVarChar(20),True,True,GetDate(20),'NULL'])

    
    if random.random()>0.9:
        #data.append(GetVarChar(180,0.1))#remarque
        data.append(GetCommentaire(180,0.1))#remarque
    else:
        data.append('')
    #print data #debug
    #print db.add('Adresse',tuple(data)) #debug
    db.add('Adresse',tuple(data))
    #res=db.execute("SELECT LAST_INSERT_ID()") # !!!arevoir    dangereux sans LOCK  NE fonctionne pas tjrs 0 proba car connexion fermee
    res=db.execute("SELECT MAX(idAdresse) FROM Adresse")   #pas terrible!!!
    idadresse=int(res[1][0][0])
    db.add('AdresseHistorique', [None, idClient, idadresse, GetDate(15)])
    tels=GetTelephones()
    for i in tels:
        data=[None,'Client',idClient]
        data.append(i)#telephone
        data.append('')#email
        if random.random()>0.9:
            #data.append(GetVarChar(180,0.1))#remarque
            data.append(GetCommentaire(180,0.1))#remarque
        else:
            data.append('')
        if i==tels[0]:
            data.append(1)
        else:
            data.append(0)
        data.append('NULL')
        #print data #debug
        (err1,err2)=db.add('Repertoire',tuple(data))
        return idClient
        
def NewAnimal(idClient):
    #data=[None,'NULL','NULL',GetVarChar(44)]  #arevoir nom
    data=[None,'NULL','NULL',GetNomAnimal()]
    
    esp=Getid('Especes')
    data.append(esp)
    data.append(GetRace(esp))
    if random.random()>0.9:
        data.append(GetRace(esp))
    else:
        data.append('NULL')
    #data.extend([GetVarChar(40,0.2),random.choice(['M','F']),GetDate(15),random.choice([0,1])])
    robe=GetRobe(esp)
    data.extend([robe,random.choice(['M','F']),GetDate(15),random.choice([0,1])])
    if random.random()>0.4:
        data.append(GetVarChar(12))
    else:
        data.append('NULL')
    if random.random()>0.9:
        #data.append(GetVarChar(180,0.1))#remarque
        data.append(GetCommentaire(180,0.1))#remarque
    else:
        data.append('NULL')
    #print data
    db.add('Animal',tuple(data))
    res=db.execute("SELECT MAX(idAnimal) FROM Animal")
    data=[None,idClient,int(res[1][0][0]),GetDate(10),'NULL','NULL']
    db.add('ClientAnimalRef',tuple(data))

def FillClient():
    Entry=1000
    print 'fill client'
    t1=datetime.now()         
    
    boucle1=10
    boucle2=Entry/boucle1
    compteur=0
    for x in xrange(boucle1) :
        print 'nb client = '+str(compteur)
        for i in xrange(boucle2):
            if database == 'OpenVet10b' :
                idClient=NewClient()    #OpenVet10b only
            else :            #elif database == 'OpenVet10c'or database=='OpenVet10d':
                idClient=NewClient2()   #OpenVet10c/d et suivants only
                
            NewAnimal(idClient)
            for j in range(random.randrange(5)):
                NewAnimal(idClient)
        compteur+=boucle2
                
                
                
    t2=datetime.now()  
    (err, res)=db.execute("select count(*) from Client")
    print "Nb client = "+ str(  res[0][0])
    delta = t2-t1
    print str(delta.seconds)+'.'+str(delta.microseconds)+' seconds'
    
def LitFichierNom():
    global listenoms, max_nom
    
    fin=open(repertoire+'nom.csv','r')
    print "lit fichier nom";

    for i in fin:
        w=i.split(';')    
        listenoms.append( (w[0],w[1]) )
    max_nom=len(listenoms)
    
def LitFichierRue():
    global listerues, curseur_rue, max_rue
    
    if len(listerues)<1 :
        fin=open(repertoire+'rues.csv','r')
        print "lit fichier rue";

        for i in fin:
            w=i.split(';')    
            listerues.append( (w[0],w[1]) )
        max_rue=len(listerues)
        print "nb rues = "+str(max_rue)

def LitFichierAnimal():
    global listeanimal, max_animal
    if max_animal <1 :
        fin=open(repertoire+'liste_nomanimal.txt', 'r')
        for i in fin :
            listeanimal.append(i)
        max_animal=len(listeanimal)-1
        
def GetNomAnimal():
    global listeanimal, max_animal
    
    if max_animal==0 :
        LitFichierAnimal()
    return( listeanimal[ random.randint(0, max_animal) ] )
    
    
def EffaceChamp(champ, id=''):
    try :
        print 'efface champ : '+champ
        #res=db.execute("DELETE FROM "+champ + " WHERE "+id+" >-1" +";")
        res=db.execute("DELETE FROM "+champ +";")
    except :
        print "err efface champ :"+champ

def FillCommunes():
    EffaceChamp('Client')
    EffaceChamp('Commune')
    if database=='OpenVet10b' or database=='OpenVet10c' or database=='OpenVet10d':
        #os.system('./creation_TABLE_LISTEVILLE_user_openvet10c.bat')
        
        typedatabase=database
        if database=='OpenVet10d' :
            typedatabase='OpenVet10c'
            
        print 'importation villes dans tmp listeville'
        instruction='mysql -u '+user+' -p'+password +' '+database+' < villes_de_france.sql'
        os.system(instruction)          #mysql -u user_openvet -p0000 OpenVet10b < villes_de_france.sql ')
        print "copie listeville dans openvet"
        instruction='mysql -u '+user+' -p'+password +' '+database+' < copie_tabletmp_villedefrance_'+typedatabase+'.sql'
        os.system(instruction)#'mysql -u user_openvet -p0000 OpenVet10b < copie_tabletmp_villedefrance_openvet10b.sql')
        
def CreateListeRaces():
    global listechiens,listechats,listelapins
    res=db.execute("SELECT idRace FROM Race WHERE Especes_idEspeces=1")
    listechats=[int(i[0]) for i in res[1]]
    res=db.execute("SELECT idRace FROM Race WHERE Especes_idEspeces=2")
    listechiens=[int(i[0]) for i in res[1]]
    res=db.execute("SELECT idRace FROM Race WHERE Especes_idEspeces=3")
    listelapins=[int(i[0]) for i in res[1]]

def main():
    global listechiens,listechats,listelapins, listenoms, curseur_nom, max_nom, listerues, curseur_rue, max_rue, fichier_comm, listeanimal, max_animal, robechat, robechien, maxrobechat, maxrobechien

    listenoms=[]
    listerues=[]
    listeanimal=[]
    curseur_rue=0
    curseur_nom=0
    fichier_comm=''
    max_animal=0
    maxrobechat=0
    maxrobechien=0
    
    
#    FillCommunesAndRaces()
#
    CreateListeRaces()
    CreateListeRobes()
#
#    if database <>'OpenVet10b' :  #== 'OpenVet10c' or database=='OpenVet10d':
#        print 'fill nom rue 10c 10d'
#        FillNomRue()    #OpenVet10c et suivants    
#

    EffaceChamp('Animal')
    EffaceChamp('Client') #vide la table
    LitFichierNom()
    LitFichierRue()
    FillClient()

    
    
if __name__ == "__main__":
    main()
    

