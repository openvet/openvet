# -*- coding: utf8 -*-
#import Tables
import time
import config
import Core
#import Core_Debug as Debug
#import operator
#from PyQt4 import QtCore

class Consultation:
	def __init__(self,DBase):
		self.DBase=DBase
		self.Date=time.strftime("%d/%m/%Y")
		self.Consultant=None
		self.Type=None
		self.Referant=None
		self.Pathologies=None		#string
		self.DomainePathologie=None
		self.Observations=''
		self.Traitements=''
		self.Commentaire=''
		self.IsBiologie=False
		self.IsImage=False
		self.IsChirurgie=False
		self.IsOrdonnance=False
		self.IsPlanTher=False
		self.idConsultation=0
		self.idConsultant=0
		self.idReferant=0
		self.idTypeConsultation=0
		self.idAnimal=0
		self.idPathologies=[]
		self.Criteres=[]	#list of Critere objects
		
	def Print(self):
		for j in [i for i in self.__dict__.keys() if i[:1] != '_']:
			print'%s : %s'%(j,getattr(self,j))
		
	def GetBiologies(self,idConsultation):
		return self.DBase.RechercheSQL_liste("CALL GetBiologies(%i)"%idConsultation)
			
	def GetImages(self,idConsultation):
		return self.DBase.RechercheSQL_liste("CALL GetImages(%i)"%idConsultation)
	
	def GetChirurgies(self,idConsultation):	
		return self.DBase.RechercheSQL_liste("CALL GetChirurgie(%i)"%idConsultation)
			
	def GetConsultation(self,idConsultation):
		return self.DBase.RechercheSQL_liste("CALL GetConsultation(%i)"%idConsultation)	#TODO: Use Core.GetDbText instead?
		
	def FormatConsultation(self,res):		#TODO: write with Qsting from Core.GetDbText? 
		self.idConsultation=res[0]
		self.Date='%02i/%02i/%i'%(res[1].day,res[1].month,res[1].year)
		self.Type=res[2].decode(config.dbCodec)
		self.Consultant=res[3].decode(config.dbCodec)		
		if res[4]!=None:
			self.Referant=res[4].decode(config.dbCodec)
		else:
			self.Referant=''
		if res[5]!=None:
			self.Pathologies=res[5].decode(config.dbCodec)
			iddomaine=-1
			for i in self.Pathologies.split(','):
				domaine=self.DBase.RechercheSQL_liste("CALL GetDomaine(\"%s\")"%i)
				if iddomaine>0 and domaine[0][0]!=iddomaine:
					self.DomainePathologie=''
					break
				else:
					iddomaine=domaine[0][0]
					self.DomainePathologie=domaine[0][1].decode(config.dbCodec)
		else:
			self.Pathologies='Appuyez sur le Bouton Pathologie'
		if res[6]!=None:
			self.Observations=res[6].decode(config.dbCodec)
		else:
			self.Observations=''
		if res[7]!=None:
			self.Traitements=res[7].decode(config.dbCodec)
		else:
			self.Traitements=''
		self.IsBiologie=res[8] and True or False
		self.IsImage=res[9] and True or False
		self.IsChirurgie=res[10] and True or False
		self.IsOrdonnance=res[11] and True or False
		self.IsPlaTher=res[12] and True or False
		if res[13]!=None:
			self.Commentaire=res[13].decode(config.dbCodec)
		else:
			self.Commentaire=''
		
	def MakeHTML(self):
		text="<a HREF=\"#C%i\"><b>%s</b></a>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp;%s<br>"%(self.idConsultation,self.Date,self.Consultant,self.Type,self.Referant)
		if self.IsBiologie:
			icone=config.WorkingPath+'/images/analyse.png'
			res=self.GetBiologies(self.idConsultation)
			tips=';'.join([i[1].decode(config.dbCodec) for i in res])
			text=text+"<a HREF=\"#B%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Biologie\" src=\"file://%s\"></a>"%(self.idConsultation,tips,icone)
		if self.IsImage:
			icone=config.WorkingPath+'/images/echo.png'
			res=self.GetImages(self.idConsultation)
			tips=';'.join([i[1].decode(config.dbCodec) for i in res])
			text=text+"<a HREF=\"#I%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Imagerie\" src=\"file://%s\"></a>"%(self.idConsultation,tips,icone)
		if self.IsChirurgie:
			icone=config.WorkingPath+'/images/scalpel.png'
			res=self.GetChirurgies(self.idConsultation)
			tips=';'.join([i[0].decode(config.dbCodec) for i in res])
			text=text+"<a HREF=\"#c%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Chirurgie\" src=\"file://%s\"></a>"%(self.idConsultation,tips,icone)
		if self.IsOrdonnance:
			icone=config.WorkingPath+'/images/doc_all.png'
			text=text+"<a HREF=\"#O%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Ordonnance\" src=\"file://%s\"></a>"%(self.idConsultation,icone)
		if self.IsPlanTher:
			icone=config.WorkingPath+'/images/planT.png'
			text=text+"<a HREF=\"#T%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Plan Thérapeutique\" src=\"file://%s\"></a>"%(self.idConsultation,icone)
		text=text+"&emsp;&emsp;&emsp;&emsp;<font color=\"red\">%s</font>"%self.Pathologies
		text=text+"<br>%s<br><span style=\"text-decoration:underline;\">Traitements</span> : %s<br>"%(self.Observations,self.Traitements)
		return text

	def GetConsultants(self):
		return Core.GetDbidText(self.DBase,"""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsConsultant""")
	
	def GetReferants(self):
		return Core.GetDbidText(self.DBase,"""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsReferant""")
	
	def GetTypesConsultation(self):
		return Core.GetDbidText(self.DBase,"SELECT idTypeConsultation,TypeConsultation FROM TypeConsultation")
	
	def GetPathologiesConsultation(self):
		return Core.GetDbidText(self.DBase,"CALL GetPathologiesConsult(%i)"%self.idConsultation)

	def GetCriteresConsultation(self,idPathologie):
		return Core.GetDbLines(self.DBase,"CALL GetCriteresConsult(%i,%i)"%(self.idConsultation,idPathologie))	
		
	def SaveData(self,isNew):
		values=[]
		erreurs=[]
		values.append(self.IdConsultation)
		res=self.DBase.RechercheSQL_liste("SELECT idAnimal FROM Animal WHERE idAnimal=%i"%self.idAnimal)
		if len(res)==1:
			values.append(self.idAnimal)
		else:
			erreurs.append('Animal')
		res=Core.ValideDate(self.Date)
		if res is None:
			erreurs.append('Date')
		else:
			values.append(res)
		self.idConsultant=self.idConsultants[self.idConsultant]
		res=self.DBase.RechercheSQL_liste("""SELECT CONCAT(Nom," ",Prenom) FROM Personne WHERE IsConsultant AND idPersonne=%i"""%self.idConsultant)
		if len(res)==1 and res[0][0].decode(config.dbCodec)==self.Consultant:
			values.append(self.idConsultant)
		else:
			erreurs.append('Consultant')
		if not self.idReferant is None:
			self.idReferant=self.idReferants[self.idReferant]
			res=self.DBase.RechercheSQL_liste("""SELECT CONCAT(Nom," ",Prenom) FROM Personne WHERE IsReferant AND idPersonne=%i"""%self.idReferant)
			if len(res)==1 and res[0][0].decode(config.dbCodec)==self.Referant:
				values.append(self.idReferant)
			else:
				erreurs.append('Referant')
		if self.Observations.size()>65536:
			erreurs.append('Observations')
		else:
			values.append(self.Observations.data())	#en utf-8
		if self.Traitements.size()>65536:
			erreurs.append('Traitements')
		else:
			values.append(self.Traitements.data())
		if self.Commentaire.size()>200:
			erreurs.append('Commentaire')
		else:
			values.append(self.Commentaire.data())
		#Fill TypeConsultation
		self.idTypeConsultation=self.idTypesConsultation[self.idTypeConsultation]
		res=self.DBase.RechercheSQL_liste("""SELECT TypeConsultation FROM TypeConsultation WHERE idTypeConsultation=%i"""%self.idTypeConsultation)
		if len(res)==1 and res[0][0].decode(config.dbCodec)==self.Type:
			ref=[self.IdConsultation,self.idTypeConsultation]
		else:
			erreurs.append('TypeConsultation')
		#TODO fill Pathologie
		if len(erreurs)==0:
			print values
			if isNew:
				pass
				#add
			#TODO write in table typeConsultation
			#TODO write in table consultation is add or update?
			else:
				pass
				#update
			return None
		else:
			return ','.join(erreurs)
			
	
class Consultations:
	def __init__(self,DBase):
		self.consultations=[]
		self.textHTML=''
		self.DBase=DBase
		
	def GetConsultations(self,idAnimal):
		MyConsult=Consultation(self.DBase)
		self.textHTML=''
		self.consultations=self.DBase.RechercheSQL_liste("CALL GetConsultationS(%i)"%idAnimal)
		for i in self.consultations:
			MyConsult.FormatConsultation(i)
			self.textHTML=self.textHTML+MyConsult.MakeHTML()+'<br>'
		icone=config.WorkingPath+'/images/add.png'
		self.textHTML=self.textHTML+"<a HREF=\"#N-1\"><img title=\"Nouvelle Consultation\" style=\"width: 32px; height: 32px;\" alt=\"Nouvelle Consultation\" src=\"file://%s\"></a>"%(icone)
		return self.textHTML

class Pathologie:
	def __init__(self,DBase):
		self.idPathologie=0
		self.NomReference=''
		self.IsChronic=False
		self.Descriptif=''
		self.Domaines=[]
		self.Synonymes=[]
		self.idEspece=None
		self.Criteres=[]
		self.DBase=DBase
	
	def SetEspece(self,IdEspece):
		self.idEspece=IdEspece
		
	def GetDomaines(self):
		return Core.GetDbidText(self.DBase,"CALL GetDomaines()",True)
	
	def GetPathologies(self,idPathologieDomaine):
		return Core.GetDbidText(self.DBase,"CALL SelectPathologies(%i,%i)"%(self.idEspece,idPathologieDomaine))

	def GetDefinitionPathologie(self,idPathologie):
		return Core.GetDbText(self.DBase,"SELECT DescriptifPublic FROM Pathologie WHERE idPathologie=%i"%idPathologie)[0]
	
	def GetPathologie(self,idPathologie):
		self.idPathologie=idPathologie
		res=self.DBase.RechercheSQL_liste("CALL GetPathologie(%i)"%idPathologie)
		self.NomReference=res[0][0].decode(config.dbCodec)
		self.IsChronic=(res[0][1]==1)
		self.Descriptif=res[0][2].decode(config.dbCodec)
		if not res[0][3] is None:
			self.Synonymes=[i.decode(config.dbCodec) for i in res[0][3].split(',') if len(i)>0]
			for i in range(max(7-len(res[0][3].split(',')),2)):
				self.Synonymes.append('')
				
	def GetExamens(self):	
		return Core.GetDbidText(self.DBase,"CALL GetExamens(%i)"%self.idPathologie)
	
	def GetCriteres(self,idExamen):
		return Core.GetDbidText(self.DBase,"CALL GetCriteres(%i,%i)"%(self.idPathologie,idExamen))
	
	def GetDocuments(self):
		return Core.GetDbText(self.DBase,"CALL GetPathologieDocuments(%i)"%self.idPathologie)
	
		#TODO GetDocuments,GetTraitements
		#TODO SetCriteres Pathologie

class Critere:
	def __init__(self,DBase):
		self.idConsultationCritere=0
		self.idPathologie=0
		self.idExamen=0
		self.idCritere=0
		self.Valeur=''
		self.Unite=''
		self.Grade=''
		self.DBase=DBase
		
	def GetCritereGrade(self,Valeur):
		self.Valeur=Valeur	
		res=Core.GetDbText(self.DBase,"CALL GetCritereGrade(%i,%f)"%(self.idCritere,Valeur))
		if len(res)>0:
			self.Grade=res[0]
			self.NbGrades=res[1]
		return res
	
	def GetCritere(self,idCritere):
		self.idCritere=idCritere
		return Core.GetDbText(self.DBase,"CALL GetCritere(%i)"%idCritere)
	
	def SaveCritere(self):
		pass
	def ToList(self):
		return[self.idCritere,self.Valeur,self.Grade,self.NbGrades]
		
if __name__ == '__main__':
	
	MyConsult=Consultation()
	MyConsult.GetConsultants()




