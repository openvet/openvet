#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('./VetCore')
sys.path.append('./VetGUI')
sys.path.append('./images')

import config
from gestion_erreurs import *

#from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui
from Tables import *
import Gui_openvet

DATABASE=config.database
IDUSER=config.IDUSER

def Login():
    #TODO: demande user et mot de passe = IDENTIQUE BASE DONNEE
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

    db=DataBase(DATABASE, USER, PWD)
    conn = db.Connection()
    return conn


if __name__ == '__main__':
    global USER,  PWD

    err=Login()
    if not err :

        app = QtGui.QApplication(sys.argv)
        window = Gui_openvet.MainWindow()
        window.show()
        sys.exit(app.exec_())
