#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myrequest as db
from datetime import date
import random
import os

user='root'
password='horizons'
table='OpenVet10b'
#table='OpenVet10c'  #change in myrequest.py

def FillCommunesAndRaces():
    
    #os.system("mysql -u %s -p%s -e\"LOAD DATA LOCAL INFILE '/home/francois/Programmes/Kiwi/OpenVet/OpenVet/communes.csv' INTO TABLE %s.Commune FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n';\""%(user,password,table))
    #os.system("mysql -u %s -p%s -e\"LOAD DATA LOCAL INFILE '/home/francois/Programmes/Kiwi/OpenVet/OpenVet/races.csv' INTO TABLE %s.Race FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n';\""%(user,password,table))
    #ne semble pas marcher avec les foreign key, même si la table est vide d'où la methode brute et lente:
    fin=open('/home/francois/Programmes/Kiwi/OpenVet/OpenVet/communes.csv','r')
    for i in fin:
        w=i.split(';')
        data=[None,w[0],w[1],int(w[2])]
        print tuple(data)
        (err1,err2)=db.add('Commune',tuple(data))
    fin.close()
    fin=open('/home/francois/Programmes/Kiwi/OpenVet/OpenVet/races.csv','r')
    counts=[]
    for i in fin:
        w=i.split(';')
        counts.append(int(w[1]))
        data=[None,w[0],int(w[1])]
        print tuple(data)
        #toujours la M... avec les caractères accentués. Les tables sont pourtant en UTF-8 et lorsque la requête est réalisée dans work bench ça marche : à revoir plus tard
        (err1,err2)=db.add('Race',tuple(data))
    fin.close()

def FillNomRue():
    res=db.execute("SELECT idCommune FROM Commune")
    l=[int(i[0]) for i in res[1]]
    for i in l:
        for j in xrange(random.randint(3,60)):
            data=[None,i,GetVarChar(40)]
            print db.add('NomRue',tuple(data))
       
def GetVarChar(maxlength, variation=0.3):
    Nom=''
    for i in xrange(random.randint(int(maxlength*variation),maxlength)):
        Nom=Nom+chr(random.randint(65,90))
    return(Nom[0]+Nom[1:].lower())

def GetDate(maxyears):
    end= date.today()
    newdate=date.fromordinal(end.toordinal()-random.randrange(365*maxyears))
    return '%i-%02i-%02i'%(newdate.year,newdate.month,newdate.day)

def Getid(table):
    dicotable={'Civilite':5,'Commune':1310,'Especes':3}
    return random.randrange(dicotable[table])+1

def GetNomRue(idCommune):
    res=db.execute("SELECT idNomRue FROM NomRue WHERE Commune_idCommune=%i"%idCommune)
    l=[int(i[0]) for i in res[1]]
    return random.choice(l)

def GetRace(espece):
    global listechiens,listechats,listelapins
    dico={1:listechats,2:listechiens,3:listelapins}    #races disponibles par espece
    return random.choice(dico[espece])

def GetTelephones():
    tels=[]
    Nb=random.randrange(5)
    for i in range(Nb):
        tel='0'
        for j in range(7):
            tel=tel+chr(random.randint(48,57))
        tels.append(tel)
    return tels
 
def NewClient():
    data=[None]
    data.append(Getid('Civilite'))
    data.append(GetVarChar(50))#nom
    data.append(GetVarChar(40))#Prenom
    if random.random()>0.9:
        data.append(GetVarChar(180,0.1))#remarque
    else:
        data.append('')
    data.append(GetVarChar(110))#adresse
    data.append(Getid('Commune'))
    #print data
    print db.add('Client',tuple(data))
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
        print data
        (err1,err2)=db.add('Repertoire',tuple(data))
        return idClient

def NewClient2():
    data=[None]
    data.append(Getid('Civilite'))
    data.append(GetVarChar(50))#nom
    data.append(GetVarChar(40))#Prenom
    if random.random()>0.9:
        data.append(GetVarChar(180,0.1))#remarque
    else:
        data.append('')
    print db.add('Client',tuple(data))
    res=db.execute("SELECT MAX(idClient) FROM Client")
    idClient=int(res[1][0][0])
    
    data=[None,'Client',idClient]
    idCommune=Getid('Commune')
    data.extend([idCommune,GetNomRue(idCommune),GetVarChar(20),True,True,GetDate(20),'NULL'])
    if random.random()>0.9:
        data.append(GetVarChar(180,0.1))#remarque
    else:
        data.append('')
    print data
    print db.add('Adresse',tuple(data))
    tels=GetTelephones()
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
        print data
        (err1,err2)=db.add('Repertoire',tuple(data))
        return idClient
        
def NewAnimal(idClient):
    data=[None,'NULL','NULL',GetVarChar(44)]
    esp=Getid('Especes')
    data.append(esp)
    data.append(GetRace(esp))
    if random.random()>0.9:
        data.append(GetRace(esp))
    else:
        data.append('NULL')
    data.extend([GetVarChar(40,0.2),random.choice(['M','F']),GetDate(15),random.choice([0,1])])
    if random.random()>0.4:
        data.append(GetVarChar(12))
    else:
        data.append('NULL')
    if random.random()>0.9:
        data.append(GetVarChar(180,0.1))#remarque
    else:
        data.append('NULL')
    #print data
    print db.add('Animal',tuple(data))
    res=db.execute("SELECT MAX(idAnimal) FROM Animal")
    data=[None,idClient,int(res[1][0][0]),GetDate(10),'NULL','NULL']
    db.add('ClientAnimalRef',tuple(data))
    

def main():
    global listechiens,listechats,listelapins
    FillCommunesAndRaces()
    res=db.execute("SELECT idRace FROM Race WHERE Especes_idEspeces=1")
    listechats=[int(i[0]) for i in res[1]]
    res=db.execute("SELECT idRace FROM Race WHERE Especes_idEspeces=2")
    listechiens=[int(i[0]) for i in res[1]]
    res=db.execute("SELECT idRace FROM Race WHERE Especes_idEspeces=3")
    listelapins=[int(i[0]) for i in res[1]]
    Entry=1000
    #FillNomRue()    #OpenVet10c only
    for i in xrange(Entry):
        idClient=NewClient()    #OpenVet10b only
        #idClient=NewClient2()   #OpenVet10c only
        NewAnimal(idClient)
        for j in range(random.randrange(5)):
            NewAnimal(idClient)

if __name__ == "__main__":
    main()
    

