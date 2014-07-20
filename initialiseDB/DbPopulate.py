#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myrequest2 as db
from datetime import date,  datetime
import random
import os
import config

#repertoire=parametres.repertoire
repertoire='./initialiseDB/'
user=config.user
password=config.password
database=config.database 
#VilleCompletes=parametres.VilleCompletes


def FillCommunesAndRaces():
    
    fin=open(repertoire+'communes.csv','r')
    print "Fill commune";
    t1=datetime.now()
    FillCommunes()
    fin.close()
    t2=datetime.now()
    (err, res)=db.execute("select count(*) from Commune") 
    print "Nb communes = "+ str(  res[0][0])
    delta = t2-t1
    print str(delta.seconds)+'.'+str(delta.microseconds)+' seconds'
    
    fin=open(repertoire+'races.csv','r')
    counts=[]

#    FillRace()

def FillRace():
    counts=[]
    fin=open(repertoire+'races.csv','r')
    print "Fill races";
    t1=datetime.now()
    for i in fin:
        w=i.split(';')
        counts.append(int(w[1]))
        data=[None,w[0],int(w[1])]
        (err1,err2)=db.add('Race',tuple(data))
    fin.close()
    t2=datetime.now()
    (err, res)=db.execute("select count(*) from Race") 
    print "Nb races = "+ str(  res[0][0])
    delta = t2-t1
    print str(delta.seconds)+'.'+str(delta.microseconds)+' seconds'

    
    
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
    
#    os.system('ls')       #debug
    
    (err, res)=db.execute("select count(*) from Commune") 
    res=res[0][0]
    if res>10000 :
        print 'nb villes = '+str(res) +' => passe'
        return 
    

    print 'importation villes dans tmp listeville'
    instruction='mysql -u '+user+' -p'+password +' '+database+' < '+repertoire+'villes_de_france.sql'
    os.system(instruction)          
    
    
    
    
    print "copie listeville dans openvet"
    instruction='mysql -u '+user+' -p'+password +' '+database+' < '+repertoire+'copie_tabletmp_villedefrance_OpenVet.sql'
    os.system(instruction)
        

def main():
    global listechiens,listechats,listelapins, listenoms, curseur_nom, max_nom, listerues, curseur_rue, max_rue, fichier_comm

    listenoms=[]
    listerues=[]
    curseur_rue=0
    curseur_nom=0
    fichier_comm=''
    
    
    FillCommunesAndRaces()


    
    
if __name__ == "__main__":
    repertoire='./'
    #main()
    FillRace()
    

