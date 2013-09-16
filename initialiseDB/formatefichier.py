#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myrequest as db
from datetime import date,  datetime
import random
import os
import parametres


            
def FormateFichierNom():

    listenoms=[]
    
    fin=open('liste_nom.txt','r')
     
    
    
    print "lit fichier nom";

    for ligne in fin:
        try :
            ligne=ligne.strip()
            indice=ligne.rfind(' ')   #dernier caractere espace
            n=ligne[:indice]
            p=ligne[indice+1:]
        except:
            pass
        listenoms.append(  (n,p)  ) 
        

    print "ecrit fichier nom"
    
    f=open('nom.csv','w')
    for client in listenoms :
        f.write( client[0]+';'+client[1] +'\n')
    f.close()
         
def FormateFichierRue():

    listerues=[]
    
    fin=open('liste_rueParis.txt','r')
     
    
    
    print "lit fichier rue";
    
    NoArrondissement=0
    for ligne in fin:
        try : 
            
            try :
                NoArrondissement = int(ligne) 
            
            except : #err si ligne = nom de rue
                ligne=ligne.strip()
                indice=ligne.rfind('(aussi')   #supprime info  du type  (aussi dans le 4eme)
                if indice>0 : 
                    ligne=ligne[:indice]
                if ligne :
                    listerues.append(  (ligne,  str(75000+NoArrondissement) )  )

        except:
            pass

        
    print "ecrit fichier rue"
    
    f=open('rues.csv','w')
    for rue in listerues :
        f.write( rue[0]+';'+rue[1] +'\n')
    f.close()
         
    
def main():
    
    #FormateFichierNom()
    FormateFichierRue()
    
if __name__ == "__main__":
    main()
    

