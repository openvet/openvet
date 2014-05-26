#!/usr/bin/python
# -*- coding: utf8 -*-

import config

from PyQt4.QtCore import *
from PyQt4.QtGui import *

AFFICHE_CONSOLE=config.DEBUG_AFFICHE_MESSAGE_CONSOLE
AFFICHE_FENETRE=config.DEBUG_AFFICHE_MESSAGE_FENETRE

def AfficheErreur(msg, log=False, fenetre=None):
    try :
        msg=unicode(msg, "utf-8")
    except :
        pass
        
    if AFFICHE_CONSOLE:
        print msg
    if fenetre:
        AfficheFenetre(msg, fenetre)
    if log :
        EcritLog(msg)
        
def EcritLog(msg):
        pass #TODO
        
def AfficheFenetre(msg, fenetre):
    try :
        msg=unicode(msg, "utf-8")
    except :
        pass
    QMessageBox.critical (fenetre, 'Erreur', msg, QMessageBox.Ok)
     
        
