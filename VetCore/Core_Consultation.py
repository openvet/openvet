# -*- coding: utf8 -*-


#*************************************************** VERSION CORE CONSULTATION NEW********************************

from Tables import *
import time
import config
#import Core
from PyQt4 import QtCore #, QtGui

from gestion_erreurs import * 

DATABASE=config.database 
IDUSER=config.IDUSER



class Consultation:
    """correspond au widget consultation => 1 client + liste animaux+ liste consultations"""

    idClients=[]
    listeClients=[]

    def __init__(self):
        
        unclient=TableClient(DATABASE, 'viewPersonne','Personne')#,  auto=True)
        #unanimal=TableAnimal(DATABASE, 'Animal')#,  auto=True) #TODO: utiliser viewAnimal (ajoute espece en clair, etc...)
        unanimal=TableAnimal(DATABASE, 'viewAnimal','Animal')
        tablelien=Table(DATABASE, 'ClientAnimalRef ')#,  auto=True)
        uneconsult=Table(DATABASE, 'viewConsultation', 'Consultation')
        table_animal_consultation=TableLiee(unanimal, uneconsult, None, 'Animal_idAnimal')#relation 1:n
        #table_client_animal=TableLiee(unclient, unanimal, 'Animal_idAnimal', 'Client_idClient' , tablelien     )
        self.table_client_animal_consultation=TableLiee(unclient,  table_animal_consultation, 'Animal_idAnimal', 'Client_idClient' , tablelien  )


        
        self.Date=time.strftime("%d/%m/%Y")
        self.DBase=self.table_client_animal_consultation.DataBase
        self.idAnimaux= []

        
    def PrintConsultation(self, etiquettes=False, imprimechampvide=False, nbTab=0):
        return self.table_client_animal_consultation.PrintParentEnfant(etiquettes, imprimechampvide, nbTab)
    
    def PrintClientsConsultationActifs(self, etiquettes=False, imprimechampvide=False, nbTab=0):  
        return self.table_client_animal_consultation.PrintParentEnfantActifs( etiquettes, imprimechampvide, nbTab)
            
    def ActiveClientId(self, id):
        return self.table_client_animal_consultation.ActiveId(id)
        
    def ActiveClient(self, client): #attention : ne lit pas le client
        self.table_client_animal_consultation.TableParent=client
        
    def GetClientActif(self):
        return self.table_client_animal_consultation.TableParent 
        
    def GetIdClientActif(self):
        return self.table_client_animal_consultation.TableParent.Id()
        #self.table_client_animal_consultation.Id()
        
    def GetNomClientActif(self):
        try :
            txt=self.table_client_animal_consultation.TableParent.DescriptionHTML()
            return txt
        except :
            pass
        
    def ActiveAnimalId(self, id):
        self.table_client_animal_consultation.ActiveEnfantId(id)
        
    def ActiveConsultationId(self, id):
        animalactif=self.table_client_animal_consultation.EnfantActif
        if animalactif :
            animalactif.ActiveEnfantId(id)
            
    def DesactiveConsultation(self):
        animalactif=self.table_client_animal_consultation.EnfantActif
        if animalactif :
            animalactif.DesactiveEnfant()
            
    def NouvelleConsultation(self):
        consult=self.table_client_animal_consultation.TableEnfant.TableEnfant   # client->animal->consultation
        return consult.New()
        
    def NouveauClient(self, activeNewClient=False):
        client=self.table_client_animal_consultation.TableParent
        newclient=client.New()
        if activeNewClient :
            self.ActiveClient(newclient)
        return newclient
    
    def RafraichissementListeAnimaux(self, idanimal=None, actualise_ListeId=False): #ajoute idanimal à la liste ou si None recrée complètement
        self.table_client_animal_consultation.RafraichissementListeEnfants( idenfant=idanimal, actualiseListeId=actualise_ListeId)
    
    def RafraichissementListeConsultations(self, idconsultation=None, actualiseListeId=False):
        """relecture dans la data base de la consultation no idconsultation (ou toutes les consult si None) de l'animal actif"""
        animalactif=self.table_client_animal_consultation.EnfantActif
        if animalactif :
            animalactif.RafraichissementListeEnfants( idconsultation, actualiseListeId)
        else :
            AfficheErreur('Warning : Core_Consultation.py:RafraichissementListeConsultations  ATTENTION pas d\'animal actif')
        
    def GetAnimalActif(self):
        return self.table_client_animal_consultation.EnfantActif
        
    def GetListeAnimauxActif(self): #generateur 
        """générateur : liste des instances d'Animal (animaux du client actif)"""
        for animal in self.table_client_animal_consultation.GetListeEnfant() :
            yield animal
        
    def GetConsultationActive(self):
        animalactif=self.table_client_animal_consultation.EnfantActif
        if animalactif :
            return animalactif.EnfantActif
            
    def GetDateConsultation(self):#consultation active
        try:
            cs=self.GetConsultationActive()
            date=cs.Get('DateConsultation')
            date='%02i/%02i/%i'%(date.day,date.month,date.year)
            return date
        except :
            return None
            
        


    def Print(self):#TODO: a revoir
        for j in [i for i in self.__dict__.keys() if i[:1] != '_']:
            print'%s : %s'%(j,getattr(self,j))
        
    def GetBiologies(self,idConsultation):
        return self.DBase.RechercheSQL_liste("CALL GetBiologies(%i)"%idConsultation)

    def GetImages(self,idConsultation):
        return self.DBase.RechercheSQL_liste("CALL GetImages(%i)"%idConsultation)
    
    def GetChirurgies(self,idConsultation): 
        return self.DBase.RechercheSQL_liste("CALL GetChirurgie(%i)"%idConsultation)
            
    def GetConsultation(self,idConsultation):       
        return self.DBase.RechercheSQL_liste("CALL GetConsultation(%i)"%idConsultation)
    
            
    def GetConsultationsHTML(self):
        text=''
        animalactif=self.GetAnimalActif()
        if animalactif :
            listeconsult = animalactif.ListeTableEnfant
            for consult in listeconsult :
                text+=self.HTML(consult)
        return text
        
    def HTML(self, consult):
        
        idconsult=consult.Id()
        date=consult.Get('DateConsultation')
        try:
            date='%02i/%02i/%i'%(date.day,date.month,date.year)
        except:
            date=''
        veto=consult.Get('Consultant')
        type=consult.Get('TypeConsultation')
        ref=consult.Get('Referant')
        
        if ref == None : ref=''
        
        text="<a HREF=\"#C%i\"><b>%s</b></a>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp;%s<br>"%(idconsult,date,veto,type, ref)
        
        if consult.Get('Biologie')>0:
            icone=config.WorkingPath+'/images/analyse.png'
            res=self.GetBiologies(idconsult)
#            tips=';'.join([i[1].decode(config.dbCodec) for i in res])  #TODO: DEBUG A REVOIR decode ou pas
            tips=';'.join([i[1]  for i in res])
            tips=tips.decode('utf8')
            text=text+"<a HREF=\"#B%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Biologie\" src=\"file://%s\"></a>"%(idconsult,tips,icone)
        if consult.Get('Imagerie')>0:
            icone=config.WorkingPath+'/images/echo.png'
            res=self.GetImages(idconsult)
            tips=';'.join([i[1]  for i in res])
            tips=tips.decode('utf8')
            text=text+"<a HREF=\"#I%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Imagerie\" src=\"file://%s\"></a>"%(idconsult,tips,icone)
        if consult.Get('Chirurgie')>0:
            icone=config.WorkingPath+'/images/scalpel.png'
            res=self.GetChirurgies(idconsult)
            tips=';'.join([i[1]  for i in res])
            tips=tips.decode('utf8')
            text=text+"<a HREF=\"#c%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Chirurgie\" src=\"file://%s\"></a>"%(idconsult,tips,icone)
        if consult.Get('Ordonnance')>0:
            icone=config.WorkingPath+'/images/doc_all.png'
            text=text+"<a HREF=\"#O%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Ordonnance\" src=\"file://%s\"></a>"%(idconsult,icone)
        if consult.Get('PlanTherapeutique')>0:
            icone=config.WorkingPath+'/images/planT.png'
            text=text+"<a HREF=\"#T%i\"><img style=\"width: 32px; height: 32px;\" alt=\"%s\" src=\"file://%s\"></a>"%(idconsult,u'Plan Thérapeutique',icone)
        text=text+"&emsp;&emsp;&emsp;&emsp;<font color=\"red\">%s</font>"%consult.Get('Pathologies')  
        text=text+"<br>%s<br><span style=\"text-decoration:underline;\">Traitements</span> : %s<br>"%(consult.Get('Examen') ,consult.Get('Traitement'))


        return text
        

    def GetConsultants(self):
        res=self.DBase.RechercheSQL_liste("""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsConsultant""")
        clst=QtCore.QStringList()
        self.idConsultants=[]
        for i in res:
#           print i[1].decode(config.dbCodec).decode('utf8')
            clst.append(i[1].decode(config.dbCodec))
            self.idConsultants.append(i[0])
        return clst
        
    def GetClients(self, filtre = 'isClient'):# ex  filtre='isClient AND IsVeterinaire AND  not isValide'

        sql="""SELECT idPersonne, 
        CONCAT (viewPersonne.Nom," ",viewPersonne.Prenom," (",Commune,")") ,
        (SELECT GROUP_CONCAT(Nom) FROM Animal LEFT JOIN ClientAnimalRef ON Animal.idAnimal=ClientAnimalRef.Animal_idAnimal 
        WHERE Client_idClient=idPersonne) FROM viewPersonne 
        """
        if filtre :
            sql=sql+'WHERE '+filtre

        res=self.DBase.RechercheSQL_liste(sql)  #CONCAT nom,prenom,liste animaux


        
        clst=QtCore.QStringList()
        self.idListeClients=[]
        for i in res:
#           print i[1].decode(config.dbCodec).decode('utf8')
            try :
                clst.append(    i[1].decode(config.dbCodec) + ' animal:'+i[2].decode(config.dbCodec)   )
            except :  #pas d'animal
                clst.append(    i[1].decode(config.dbCodec)   )
                
            self.idListeClients.append(i[0])
        return clst
    
    def GetIdConsultant(self,index):
        return self.idConsultants[index]
    
    def GetReferants(self):
        res=self.DBase.RechercheSQL_liste("""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsReferant""")
        clst=QtCore.QStringList()
        self.idReferants=[]
        for i in res:
            clst.append(i[1].decode(config.dbCodec))
            self.idReferants.append(i[0])
        return clst
        
    def GetIdReferant(self,index):
        return self.idReferants[index]    
        
        
    def GetTypesConsultation(self):
        res=self.DBase.RechercheSQL_liste("SELECT idTypeConsultation,TypeConsultation FROM TypeConsultation")
        clst=QtCore.QStringList()
        self.idTypesConsultation=[]
        for i in res:
            clst.append(i[1].decode(config.dbCodec))
            self.idTypesConsultation.append(i[0])
        return clst
        
    def GetIdTypeConsultation(self,index):
        return self.idTypesConsultation[index]
        
    def GetListeAnimaux(self):#animaux du client actif
        """retourne la liste des animaux (du client actif) sous forme de QStringList"""
        clst=QtCore.QStringList()
        self.idAnimaux=[]
        for animal in self.GetListeAnimauxActif():
            nomanimal=animal.DescriptionHTML()
#            clst.append(nomanimal.decode(config.dbCodec))#(i[1].decode(config.dbCodec))
            #clst.append(nomanimal.decode('utf8'))
            clst.append(nomanimal)
            self.idAnimaux.append(animal.Id())
        return clst    
        
    def GetListeClients(self):
        """retourne la liste des clients (tous ceux déjà lus au moins 1 fois) sous forme de QStringList """
        #idclientactif=self.table_client_animal_consultation.TableParent.Id()#clientactif=self.table_client_animal_consultation.TableParent
        idclientactif=self.GetIdClientActif()  
        if not idclientactif in self.idClients : #client activé pour la 1ere fois
            self.idClients.append(idclientactif) 
            #DEBUG++++  #self.ActiveClientId(idclientactif)
            
            self.listeClients.append(self.GetClientActif() )
#            newClient = TableClient(DATABASE, 'viewPersonne','Personne')#,  auto=True)
#            newClient.LectureId(idclientactif)
#            self.listeClients.append(newClient)#garde une copie du client    <=========  erreur, éviter de faire des copies, pb de mise à jour affichage lors modif client si 2 références clients<>
            
        clst=QtCore.QStringList()
        for unclient in self.listeClients :
            nomclient=unclient.DescriptionHTML()
#            clst.append(nomclient.decode('utf8'))
            clst.append(nomclient)
        return clst
            
    def GetIndexClientId(self, id):
        try :
            index = self.idClients.index(id)
        except :
            index= 'erreur id '+str(id)+' n\'est pas dans la liste idClients'
        return index
            
        
if __name__ == '__main__':
    
    MyConsult=Consultation()
    liste= MyConsult.GetConsultants()
    for item in liste :
        print str(item.toUtf8())
        
    #MyConsult.ActiveSQL(True,'Nom', '%POINT%')
    MyConsult.ActiveClientId(1)
    MyConsult.ActiveAnimalId(1)    
    print MyConsult.GetConsultationsHTML()
    
    #res=MyConsult.GetConsultation(2)
    #MyConsult.FormatConsultation(res[0])
    
    #MyDossier=Consultations()
    #print MyDossier.GetConsultations(1)



