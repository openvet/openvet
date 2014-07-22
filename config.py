# -*- coding: utf8 -*-

import os



DEBUG=True
DEBUG_AFFICHE_MESSAGE_CONSOLE=True  #TODO: a enlever lorsuqe les msg d erreurs seront geres par gestion_erreurs.py
#DEBUG = True
DEBUG_AFFICHE_MESSAGE_FENETRE=False


MASQUE_WIDGET_NON_DEV=True
#MASQUE_WIDGET_NON_DEV=False


#user='root'#pour ouvrir la base

repertoire='/home/francois/Programmes/Kiwi/OpenVet/OpenVet/'
WorkingPath='/media/Datas/Kiwi/OpenVet'
#dbCodec='ISO-8859-1'
dbCodec='utf8'
user='root'
password='horizons'
host='localhost'

if os.path.exists('/home/yvon') :
    repertoire='/home/yvon/Documents/programmation/openvet2/openvet2_python/'
    WorkingPath='/home/yvon/Documents/Openvet/'
    user='user_openvet'
    password='0000'


#**************************************defferentes version a tester**************
#database='OpenVet10b'
#database='OpenVet10c'   
#database='OpenVet10d'  #table rue sans idAdresse (=>plusieurs adresses peuvent avoir la mm rue / adresseHistorique = simple lien idclient, idadresse
database='OpenVet13'


#VilleCompletes=True #remplit la base avec toutes les villes de france




nomdatabase=database
#nomdatabasedebug= 'openvetdebug'
#if debug :
#    nomdatabase=nomdatabasedebug
    
passe_confirmation="123"    #password pour confirmer les operations critiques/dangereuses (ex effacer un client)
TAILLEDEBUTVILLE=4          #affiche les villes dans la liste a partir de 4 caracteres
TAILLETELEPHONE=10

IDUSER=1  # ************  chaque utilisateur openvet a un id different


AFFICHEINFOVETO=True  #dans formulaire nouveau client : affiche les case à cocher , si False les masque si véterinaire est décoché
MAXWIDTHQLINEEDIT=300 #largeur des widgets line edit (formulaire nouveau client)
MAXWIDTHQTXTEDIT=500 # "            "               texte edit  "           "               "
MINHEIGHTTXTEDIT=200  # hauteur 

SELECTIONNEVILLEPREFEREE=14679  # -1  =>comboBox ville n'affiche rien, sinon affiche la ville idCommune = SELECTIONNEVILLEPREFEREE
PAYS=33 #33=France

MASQUE_CIP='99 000'  #2 chiffres un espace 3 chiffres  (9=obligatoire, 0= facultatif)
MASQUE_CIP_REG='\d{2}\s{0,1}\d{0,3}'  #autorise 2 chiffres ou + 

TYPE_CONSULTATION_DEFAUT=u'Motivée'   #nouveau formulaire consultation vide
VETO_CONSULTATION_DEFAUT='POINT Yvon'               #nouveau formulaire consultation vide 
