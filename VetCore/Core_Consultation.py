# -*- coding: utf8 -*-
#import Tables
import time
import config
#import Core
#import operator
from PyQt4 import QtCore
from PyQt4.QtGui import *
from Core_Critere import CriteresConsultation
from Core_Critere import CritereConsultation


class Consultation:
	def __init__(self,DBase,idAnimal):
		self.Table='Consultation'
		self.DBase=DBase
		self.Animal_idAnimal=idAnimal
		self.TableFields=self.DBase.GetFields(self.Table)
		#attributes: idConsultation,Animal_idAnimal,DateConsultation,TypeConsultation_idTypeConsultation,Personne_idConsultant,Personne_idReferant,
		#Personne_idReferent,Examen,Traitement,Actif,Commentaires
		for i in self.TableFields:
			self.__dict__.update({i:None})          
		self.DateConsultation=QtCore.QDate()
		self.TypeConsultation=None
		self.Consultant=None
		self.Referant=None
		self.ConsultationPathologies=[]
		self.IsBiologie=False
		self.IsImage=False
		self.IsChirurgie=False
		self.IsOrdonnance=False
		self.IsPlanTher=False
		self.DomainePathologie=None
		self.idCritere=None
		#TODO add self.Biologies=[], images, chirurgies,.....?
		
	def Print(self):
		print '#attributes: '+','.join(self.TableFields)
		for i in self.TableFields:
			print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))
		print 'Consultant : %s'%self.Consultant
		print 'Référant : %s'%self.Referant
		for i in self.ConsultationPathologies:
			print i.Print()
		print self.IsImage

	def GetBiologies(self,idConsultation):
		res=self.DBase.GetDbidText("CALL GetBiologies(%i)"%idConsultation)
		#TODO: fill self.Biologies
		tmp=[i[1].toLatin1().data() for i in res]
		return QtCore.QString(','.join(tmp))
		#return self.DBase.RechercheSQL_liste("CALL GetBiologies(%i)"%idConsultation)
			
	def GetImages(self,idConsultation):
		res=self.DBase.GetDbidText("CALL GetImages(%i)"%idConsultation)
		#TODO: fill self.images
		tmp=[i[1].toLatin1().data() for i in res]
		return QtCore.QString(','.join(tmp))
		
	def GetChirurgies(self,idConsultation):	
		res=self.DBase.GetDbidText("CALL GetChirurgie(%i)"%idConsultation)
		tmp=[i[1].toLatin1().data() for i in res]
		return QtCore.QString(','.join(tmp))
			
	def Get(self,idConsultation):
		self.idConsultation=idConsultation
		res=self.DBase.GetDbText("CALL GetConsultation(%i)"%idConsultation)
		self.Set(res)
		
	def Set(self,res):
		self.idConsultation=res[0].toInt()[0]
		self.DateConsultation=QtCore.QDate.fromString(res[1], QtCore.Qt.ISODate)
		self.TypeConsultation_idTypeConsultation=res[2]
		self.TypeConsultation=res[3]
		self.Personne_idConsultant=res[4].toInt()[0]
		self.Consultant=res[5]
		self.Personne_idReferant=res[6].toInt()[0]
		self.Referant=res[7]
		self.ConsultationPathologies=[]
		for i in res[8].split(','):
			if i.toInt()[1]:
				tmp=CriteresConsultation(i.toInt()[0],self)
				tmp.Get()
				self.ConsultationPathologies.append(tmp)
				del tmp
		self.Examen=res[10]
		self.Traitement=res[11]
		self.Commentaires=res[17]
		self.Actif=True
		self.IsBiologie=res[12]
		self.IsImage=res[13]
		self.IsChirurgie=res[14]
		self.IsOrdonnance=res[15]
		self.IsPlaTher=res[16]
		self.SingleDomainePathologie()
	
	def ConsultationPathologiesString(self):
		tmp=[i.Pathologie_NomReference.toLatin1().data() for i in self.ConsultationPathologies]
		return QtCore.QString(','.join(tmp))
	
	def SingleDomainePathologie(self):
		domaines=[]
		for i in self.ConsultationPathologies:
			if i.DomainePathologie not in domaines:
				domaines.append(i.DomainePathologie)
		if len(domaines)==1:
			self.DomainePathologie=domaines[0]
		else:
			self.DomainePathologie=None
			
	def MakeHTML(self):
		if self.idConsultation is None:
			return
		#idConsultation,Animal_idAnimal,DateConsultation,Personne_idConsultant,Personne_idReferant,Personne_idReferent,Examen,Traitement,Actif,Commentaires
		text="<a HREF=\"#C%i\"><b>%s</b></a>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp;%s<br>"%(self.idConsultation,self.DateConsultation.toString('dd/MM/yyyy'),self.Consultant,self.TypeConsultation,self.Referant)
		if self.IsBiologie:
			icone=':/newPrefix/images/analyse.png'
			tips=self.GetBiologies(self.idConsultation)
			text=text+"<a HREF=\"#B%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Biologie\" src=\"file:%s\"></a>"%(self.idConsultation,tips,icone)
		if self.IsImage:
			icone='../images/echo.png'
			tips=self.GetImages(self.idConsultation)
			text=text+"<a HREF=\"#I%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Imagerie\" src=\"file:%s\"></a>"%(self.idConsultation,tips,icone)
		if self.IsChirurgie:
			icone='../images/scalpel.png'
			tips=self.GetChirurgies(self.idConsultation)
			text=text+"<a HREF=\"#c%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Chirurgie\" src=\"file:%s\"></a>"%(self.idConsultation,tips,icone)
		if self.IsOrdonnance:
			icone='../images/doc_all.png'
			text=text+"<a HREF=\"#O%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Ordonnance\" src=\"file:%s\"></a>"%(self.idConsultation,icone)
		if self.IsPlanTher:
			icone='../images/planT.png'
			text=text+"<a HREF=\"#T%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Plan Thérapeutique\" src=\"file:%s\"></a>"%(self.idConsultation,icone)
		text=text+"&emsp;&emsp;&emsp;&emsp;<font color=\"red\">%s</font>"%self.ConsultationPathologiesString()
		text=text+"<br>%s<br><span style=\"text-decoration:underline;\">Traitements</span> : %s<br>"%(self.Examen,self.Traitement)
		return text

	def GetConsultants(self):
		return self.DBase.GetDbidText("""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsConsultant""")
	
	def GetReferants(self):
		return self.DBase.GetDbidText("""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsReferant""")
	
	def IsValidVeterinaire(self,id):
		res=[]
		if id==self.Personne_idConsultant:
			res=self.DBase.GetDbidText("SELECT idPersonne,CONCAT(Nom,\" \",Prenom) FROM Personne WHERE idPersonne=%i AND isConsultant=TRUE"%self.Personne_idConsultant)
			if len(res)==0:
				return False
			if res[0][1]!=self.Consultant:
				return False
			else:
				return True
		elif id==self.Personne_idReferant:
			res=self.DBase.GetDbidText("SELECT idPersonne,CONCAT(Nom,\" \",Prenom) FROM Personne WHERE idPersonne=%i AND isReferant=TRUE"%self.Personne_idReferant)
			if len(res)==0:
				return False
			if res[0][1]!=self.Referant:
				return False
			else:
				return True
		
	def IsValidTypeConsultation(self):
		res=self.DBase.GetDbidText("SELECT idTypeConsultation, TypeConsultation FROM TypeConsultation WHERE idTypeConsultation=%i"%self.TypeConsultation_idTypeConsultation)
		if res[0][1]!=self.TypeConsultation:
			return False
		return True
	
	def GetTypesConsultation(self):
		return self.DBase.GetDbidText("SELECT idTypeConsultation,TypeConsultation FROM TypeConsultation")
	
	def GetConsultationPathologies(self):
		tmp=[[i.Pathologie_idPathologie,i.Pathologie_NomReference.toLatin1().data()] for i in self.ConsultationPathologies]
		return tmp
	
	def GetIndexConsultationPathologie(self,idPathologie):
		for i,n in zip(self.ConsultationPathologies,range(len(self.ConsultationPathologies))):
			if i.Pathologie_idPathologie==idPathologie:
				return n
	
	def GetConsultationCriteres(self,idPathologie):
		for i in self.ConsultationPathologies:
			if i.Pathologie_idPathologie==idPathologie:
				return i.Get()
			
	def GetCritereGrade(self,idCritere,Valeur):	
		Grade=QtCore.QString('')
		res=self.DBase.GetDbText("CALL GetCritereGrade(%i,%.2f)"%(idCritere,Valeur))
		if len(res)>0:
			Grade=res[0]+QtCore.QString('/')+res[1]
		return Grade
	
	def CheckDoublonPathologieRef(self,idpathologie):
		for i in self.ConsultationPathologies:
			if i.Pathologie_idPathologie==idpathologie:
				return True
		return False
	
	def UpdateCritere(self,indexPathologie,indexCritere,idCritere,valeur,grade):
		#attributes: idConsultationCritere,Critere_idCritere,PathologieRef_idPathologieRef,CritereQuantitatif,CritereQualitatif,Grade
		if indexCritere>=0:
			self.ConsultationPathologies[indexPathologie].Criteres[indexCritere].SetValues(valeur,grade)
		else:
			#TODO: debug pathologie doublée
			pathologie=self.ConsultationPathologies[indexPathologie]
			tmp=CritereConsultation(pathologie)
			tmp.Set([0,idCritere,pathologie.idPathologieRef,None,None,None])
			tmp.SetValues(valeur, grade)
			pathologie.Criteres.append(tmp)
			del tmp
			
	def Save(self):
		#attributes: idConsultation,Animal_idAnimal,DateConsultation,TypeConsultation_idTypeConsultation,
		#Personne_idConsultant,Personne_idReferant,Personne_idReferent,Examen,Traitement,Actif,Commentaires
		values=[]
		erreurs=[]
		ToDelete=False
		if self.idConsultation>=0:
			values.append('%i'%self.idConsultation)
		else:
			ToDelete=True
			values.append('%i'%abs(self.idConsultation))
		if not self.DBase.RechercheSQL_id("SELECT idAnimal FROM Animal WHERE idAnimal=%i"%self.Animal_idAnimal) is None:
			values.append('%i'%self.Animal_idAnimal)
		else:
			erreurs.append('idAnimal')
		if self.DateConsultation.isValid():
			values.append('\"%s\"'%self.DateConsultation.toString('yyyy-MM-dd'))
		else:
			erreurs.append('DateConsultation')
		self.TypeConsultation_idTypeConsultation=self.TypeConsultation_idTypeConsultation
		if self.IsValidTypeConsultation():
			values.append('%i'%self.TypeConsultation_idTypeConsultation)
		else:
			erreurs.append('idTypeConsultation')
		if self.IsValidVeterinaire(self.Personne_idConsultant):
			values.append('%i'%self.Personne_idConsultant)
		else:
			erreurs.append('idConsultant')
		if self.Personne_idReferant is None:
			values.append('NULL')
		elif self.IsValidVeterinaire(self.Personne_idReferant):
			values.append('%i'%self.Personne_idReferant)
		else:
			erreurs.append('idReferant')	
		if self.Examen.size()>65536:
			erreurs.append('Examen')
		else:
			values.append(u'\"%s\"'%self.Examen)
		if self.Traitement.size()>65536:
			erreurs.append('Traitement')
		else:
			values.append(u'\"%s\"'%self.Traitement)
		values.append('TRUE')
		if self.Commentaires is None:
			values.append('NULL')
		elif self.Commentaires.size()>200:
			erreurs.append('Commentaires')
		else:
			values.append(u'\"%s\"'%self.Commentaires)
		if ToDelete:
			self.DBase.DbDelete(self.Table,[self.TableFields[0],values[0]])
			return
		if len(erreurs)==0:  
			#TODO StartTransaction
			if self.idConsultation==0:
				self.idConsultation=self.DBase.DbAdd( self.Table, values,True)
			else:
				fields=[self.TableFields[0]]
				fields.extend(self.TableFields[2:])
				Nvalues=[values[0]]
				Nvalues.extend(values[2:])
				self.DBase.DbUpdate(self.Table,fields,Nvalues)
			for i in self.ConsultationPathologies:
				i.Save(self.idConsultation)
			#TODO commit
			return self.idConsultation
		else:
			msg='Erreur Save %s: %s'%(self.Table,','.join(erreurs))
			print msg
			return msg				

	
class Consultations:
	def __init__(self,DBase,idAnimal):
		self.consultations=[]
		self.textHTML=''
		self.DBase=DBase
		self.idAnimal=idAnimal
		
	def Get(self):
		self.textHTML=''
		self.consultations=self.DBase.GetDbLines("CALL GetConsultations(%i)"%self.idAnimal)
		for i in self.consultations:
			MyConsult=Consultation(self.DBase,self.idAnimal)
			MyConsult.Set(i)
			self.textHTML=self.textHTML+MyConsult.MakeHTML()+'<br>'
			del MyConsult
		icone=config.WorkingPath+'/images/add.png'
		self.textHTML=self.textHTML+"<a HREF=\"#N-1\"><img title=\"Nouvelle Consultation\" style=\"width: 32px; height: 32px;\" alt=\"Nouvelle Consultation\" src=\"file://%s\"></a>"%(icone)
		return self.textHTML

	
# class Pathologie:
# 	def __init__(self,DBase):
# 		self.idPathologie=0
# 		self.NomReference=''
# 		self.IsChronic=False
# 		self.Descriptif=''
# 		self.Domaines=[]
# 		self.Synonymes=[]
# 		self.idEspece=None
# 		#self.Criteres=[]
# 		self.DBase=DBase
# 	
# 	def SetEspece(self,IdEspece):
# 		self.idEspece=IdEspece
# 		
# 	def GetDomaines(self):
# 		return self.DBase.GetDbidText("CALL GetDomaines()",'Tous')
# 	
# 	def GetPathologies(self,idPathologieDomaine):
# 		return self.DBase.GetDbidText("CALL SelectPathologies(%i,%i)"%(self.idEspece,idPathologieDomaine),u'Néant')
# 
# 	def GetDefinitionPathologie(self,idPathologie):
# 		return self.DBase.GetDbText("SELECT DescriptifPublic FROM Pathologie WHERE idPathologie=%i"%idPathologie)[0]
# 	
# 	def GetPathologie(self,idPathologie):
# 		self.idPathologie=idPathologie
# 		res=self.DBase.RechercheSQL_liste("CALL GetPathologie(%i)"%idPathologie)
# 		self.NomReference=res[0][0].decode(config.dbCodec)
# 		self.IsChronic=(res[0][1]==1)
# 		self.Descriptif=res[0][2].decode(config.dbCodec)
# 		if not res[0][3] is None:
# 			self.Synonymes=[i.decode(config.dbCodec) for i in res[0][3].split(',') if len(i)>0]
# 			for i in range(max(7-len(res[0][3].split(',')),2)):
# 				self.Synonymes.append('')
# 				
# 	def GetExamens(self):	
# 		return self.DBase.GetDbidText("CALL GetExamens(%i)"%self.idPathologie)
# 	
#  	def GetCriteres(self,idExamen):
#  		return self.DBase.GetDbidText("CALL GetCriteres(%i,%i)"%(self.idPathologie,idExamen))
# 	
# 	def GetDocuments(self):
# 		return self.DBase.GetDbText("CALL GetPathologieDocuments(%i)"%self.idPathologie)
# 	
# 		#TODO GetDocuments,GetTraitements
# 		#TODO SetCriteres Pathologie
		

if __name__ == '__main__':
	import Tables
	import config 
	DBase=Tables.DataBase(config.database)
 	MyConsult=Consultation(DBase,1)
 	MyConsult.Get(1)
 	MyConsult.Print()
# 	print MyConsult.MakeHTML()
# 	MyConsults=Consultations(DBase,1)
# 	MyConsults.Get()
#	MyConsult.Print()
#	MyConsult.GetPathologiesConsultation()
#	MyConsult.GetConsultants()




