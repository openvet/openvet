# -*- coding: utf8 -*-



from Tables_Base import  *

import time
import config
import Core
from PyQt4 import QtCore, QtGui

from gestion_erreurs import * 

DATABASE=config.database 
IDUSER=config.IDUSER

class MyQSqlQueryModel(QSqlQueryModel):  #debug  TEST
    def __init__(self):
        QSqlQueryModel.__init__(self)
    def data(self, index, role):
        data=QSqlQueryModel.data(self, index, role)
        return(data)


class QSqlQueryModelVille(QSqlQueryModel):  #debug  TEST
    def __init__(self):
        QSqlQueryModel.__init__(self)
        
    def data(self, index, role):
        data=QSqlQueryModel.data(self, index, role)
        row=index.row()
        col=index.column()
        
        if role == Qt.DecorationRole:
#            data=QIcon('icone.png') #rien
#            data=QColor(255, 0, 0)#carre rouge
            return(data)
            
#        elif  role==Qt.ForegroundRole:
#             boldFont=QFont()
#             boldFont.setBold(True)
#             return boldFont
        
        elif role==Qt.CheckStateRole:
             return Qt.Checked
        
        elif role ==Qt.EditRole :   #dans editline
            if data.typeName() == 'QString' and not data.isNull() :
                txt=data.toString()
                txt2= txt #+'testDebug' #ok
                
                data=QVariant(txt2)   #data.setValue(txt2)   QVariant.setValue n'existe pas sous python !!! => nouveau QVariant
                
                Qt.DisplayRole
                return(data)
                
        elif role==Qt.DisplayRole :  #dans popup
            txt=data.toString() #+' DEBUG TEST'
            data=QVariant(txt)
            return(data)
        
            
        
        return(data)

class MyQSortFilterProxyModel(QSortFilterProxyModel) :
#    def __init__(self,  parent=None):
#        QSortFilterProxyModel.__init__( self, parent)
#        
    def __init__(self, parent=None):
        super(MyQSortFilterProxyModel, self).__init__(parent)
        
#    def filterAcceptsColumn( self, source_column, source_parent ):
#        if source_column==1:
#            return  True
#        else : return False
        

class TableAnimal(Table):
    def __init__(self,nomBase,nomTable, TableBase='', auto=True, USER=config.user, PWD=config.password, dataBase=None):
        Table. __init__(self, nomBase,nomTable, TableBase, auto, USER, PWD, dataBase)
        
    def New(self): #important pour creer nouveaux enfants dans table liées (sinon crée instance de Table au lieu de TableAnimal)
        unetable=TableAnimal(self.nomDB,self.NomTable, self.NomTableBase,  dataBase=self.DataBase)
        return unetable
        
    def DescriptionHTML(self):#TODO: a completer ex barré pour dcd, etc...
        txt=''
        txt+=self.Get('Nom')
        txt+=u' (espèce='+str(self.Get('Especes_idEspeces'))+')'
        return txt


class TableClient(Table):
    def __init__(self,nomBase,nomTable, TableBase='', auto=True, USER=config.user, PWD=config.password, dataBase=None):
        Table. __init__(self, nomBase,nomTable, TableBase, auto, USER, PWD, dataBase)
        
    def New(self): #important pour creer nouveaux enfants dans table liées (sinon crée instance de Table au lieu de TableAnimal)
        unetable=TableAnimal(self.nomDB,self.NomTable, self.NomTableBase,  dataBase=self.DataBase)
        return unetable
        
    def DescriptionHTML(self):#TODO: a completer ex barré pour dcd, etc...
        txt=''
        txt+=self.Get('Nom')+' '+self.Get('Prenom')
        txt+=' (id='+str(self.Id())+')'
        return txt
        
def NouveauClient():
    return TableClient(DATABASE, 'viewPersonne','Personne')
    
    
class TableSelectAll(Table):#  <=>   Table QModel : fournit un QSqlModel 
    # correspond à un SELECT * FROM Table, les résultats sont dans ListeElement + ListeId
    def __init__(self, nomTable, listeElement={}, listeId={}, qmodel='', listeproxymodel=[], initialiseListe= False, sql='', TableBase='', auto=True, USER=config.user, PWD=config.password, dataBase=None):
        nomBase=DATABASE
        self.ListeElement=listeElement
        self.Listeid=listeId
        self.QModel=qmodel
        self.listeProxyModel = listeproxymodel
        Table. __init__(self, nomBase,nomTable, TableBase, auto, USER, PWD, dataBase)
        self.sql=sql
        if initialiseListe : 
            self.LectureListe()  #liste simple (<>model/view)
        
    def GetListe(self):  #liste simple (<>model/view)
        if not self.ListeElement:
            self.LectureListe()
        return self.ListeElement
        
    def GetListeid(self):
        return self.Listeid
        
    def GetModel(self, proxymodel=False):
        "retourne un QSqlQueryModel  (ou QSortFilterProxyModel = copie du model avec possibilité de filtre/trie)"

        if not self.QModel :
            self.CreationModel()

        if proxymodel :
            return self.CreationProxyModel()
        else :
            return self.QModel

            #self.LectureModel(proxymodel)
        
    def GetNouveauModel(self, independant=False):
        return self.CreationModel(independant)
        
    def GetId(self, index):  #renvoie l'id (cf sql= SELECT id, autres champs FROM...) à partir de l'index  (cf widget curent index)
        if not self.QModel : #simple liste Qstring
            return self.Listeid[index]
        else :# model/view
            r=self.QModel .record(index)  #enregistrement (sql) de la ligne   no index   (lecture de la ligne index: renvoie un Qrecord)
            (valeur, isvalid)=r.value(0).toInt()   #1ere colonne = id
            if isvalid :
                return valeur
            
        
    def GetIndex(self, id):
        if not self.QModel : #simple liste Qstring
            return self.Listeid.index(id)
        else :
            start=self.QModel.index(0, 0)  #colonne 0 row 0  => indique colonne de recherche
            recherche=self.QModel.match(start, Qt.DisplayRole, QVariant(id), flags=Qt.MatchExactly)
            resultat=recherche[0]
            return resultat.row()
            
    def SetSql(self, sql):
        self.sql=sql
        
    def LectureListe(self):   #liste simple (<>model/view)
        res=self.DataBase.RechercheSQL_liste(self.sql)
        clst=QtCore.QStringList()
        self.Listeid=[ ]
        for i in res:
            clst.append(    i[1].decode(config.dbCodec)   )
            self.Listeid.append(i[0])        
        self.ListeElement=clst
        
    def CreationModel(self, independant=False):  #surchargée dans tables dérivées (ex ville => model personnalisé pour gérer affichage)
        model=self.DataBase.QSqlQueryModel(self.sql)
        if not independant :
            self.QModel=model
        return model
        
    def CreationProxyModel(self):
        if not self.QModel :
            self.CreationModel()
        myproxymodel=MyQSortFilterProxyModel()
        myproxymodel.setSourceModel(self.QModel)
        self.listeProxyModel.append(myproxymodel )
        return myproxymodel            
        
    def LectureModel(self,  proxymodel=False):  #OBSOLETTE  #TODO: enlever
        model=self.DataBase.QSqlQueryModel(self.sql)
        self.QModel=model

#        querymodel=MyQSqlQueryModel()  #debug TEST  surcharge QSqlQueryModel.data()  ==> lent
#        model=self.DataBase.QSqlQueryModel(self.sql, querymodel)

        if proxymodel :
            myproxymodel=MyQSortFilterProxyModel()
            myproxymodel.setSourceModel(model)
            self.QModel=myproxymodel
        
        
        

class TableCivilite(TableSelectAll):
    ListeElement=[]   #attribut de class
    ListeId=[]
    QModel=''
    ListeProxyModel=[] 
    def __init__(self, initialiseListe=False) :
        nomTable='Civilite'
        sql="""SELECT idCivilite, 
        CONCAT ( Civilite, ' (', CiviliteAbrev, ')' )
        FROM Civilite
        WHERE Actif ;"""
        TableSelectAll. __init__(self, nomTable, self.__class__.ListeElement, self.__class__.ListeId, self.__class__.QModel,self.__class__.ListeProxyModel,  initialiseListe, sql)
        

def NouvelleTableCivilite(initialiseListe=False):
    return TableCivilite(initialiseListe)


class TableVille(TableSelectAll):
    ListeElement=[]   #attribut de class, non utilisé si independant=True
    ListeId=[]
    QModel=''
    ListeProxyModel=[] 
    def __init__(self, initialiseListe=False, idPays=33, sql='', independant=False) :
        nomTable='Commune'
        if not sql : #sql par défaut
            sql="""SELECT idCommune, 
            CONCAT ( Commune, ' (',CIP , ')' )
            FROM Commune
            WHERE Actif  AND Pays_idPays = """+str(idPays)
            
        if independant :  #n'utilise pas les listes de class (=global =utilisées pour toutes les instances)mais crée une liste (self) par instance
            self.ListeElement=[]
            self.ListeId=[]
            self.QModel=''
            self.ListeProxyModel=[] 
#            TableSelectAll. __init__(self, nomTable, self.ListeElement, self.ListeId, self.QModel,self.ListeProxyModel,  initialiseListe, sql)
        else :
            self.ListeElement=self.__class__.ListeElement
            self.ListeId= self.__class__.ListeId
            self.QModel=self.__class__.QModel
            self.ListeProxyModel=self.__class__.ListeProxyModel
#            TableSelectAll. __init__(self, nomTable, self.__class__.ListeElement, self.__class__.ListeId, self.__class__.QModel,self.__class__.ListeProxyModel,  initialiseListe, sql)

        TableSelectAll. __init__(self, nomTable, self.ListeElement, self.ListeId, self.QModel,self.ListeProxyModel,  initialiseListe, sql)

    def CreationModel(self, independant =False):  #=> model personnalisé pour gérer affichage)
        modelville=QSqlQueryModelVille()
        model=self.DataBase.QSqlQueryModel(self.sql, query_model=modelville)
        
        self.QModel=model
        
        return model
        
#    def GetModel(self):
#        return self.__class__.QModel


def NouvelleTableVille(initialiseListe=False, idPays=33, sql='', independant=False):
    return TableVille(initialiseListe, idPays, sql, independant)
