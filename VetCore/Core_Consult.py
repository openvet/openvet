#!/usr/bin/python
# -*- coding: utf8 -*-
import Tables
import time
import config
from PyQt4 import QtCore, QtGui

class Consultation:
	def __init__(self):
		self.Date=time.strftime("%d/%m/%Y")
		self.Consultant=None
		self.Type=None
		self.Referant=None
		self.Pathologies=None
		self.Observations=''
		self.Traitements=''
		self.IsBiologie=False
		self.IsImage=False
		self.IsChirurgie=False
		self.IsOrdonnance=False
		self.IsPlanTher=False
		self.IdConsultation=0
		self.DBase=Tables.DataBase(config.database)
		self.idConsultants=[]
		self.idReferants=[]
		self.idTypesConsultation=[]
		
	def Print(self):
		for j in [i for i in self.__dict__.keys() if i[:1] != '_']:
			print'%s : %s'%(j,getattr(self,j))
		
	def GetBiologies(self,idConsultation):
		return self.DBase.RechercheSQL_liste("CALL GetBiologies(%i)"%idConsultation)
			
	def GetImages(self,idConsultation):
		return self.DBase.RechercheSQL_liste("CALL GetImages(%i)"%idConsultation)
	
	def GetChirurgies(self,idConsultation):	
		return self.DBase.RechercheSQL_liste("CALL GetChirurgie(%i)"%idConsultation)
			
	def GetConsultation(self,idConsultation):#!/usr/bin/python		
		return self.DBase.RechercheSQL_liste("CALL GetConsultation(%i)"%idConsultation)
	
	def FormatConsultation(self,res):
		self.IdConsultation=res[0]
		self.Date='%02i/%02i/%i'%(res[1].day,res[1].month,res[1].year)
		self.Type=res[2].decode(config.dbCodec)
		self.Consultant=res[3].decode(config.dbCodec)		
		if res[4]!=None:
			self.Referant=res[4].decode(config.dbCodec)
		else:
			self.Referant=''
		if res[5]!=None:
			self.Pathologies=res[5].decode(config.dbCodec)
		else:
			self.Pathologies=''
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
	
	def MakeHTML(self):
		text="<a HREF=\"#C%i\"><b>%s</b></a>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp;%s<br>"%(self.IdConsultation,self.Date,self.Consultant,self.Type,self.Referant)
		if self.IsBiologie:
			icone=config.WorkingPath+'/images/analyse.png'
			res=self.GetBiologies(self.IdConsultation)
			tips=';'.join([i[1].decode(config.dbCodec) for i in res])
			text=text+"<a HREF=\"#B%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Biologie\" src=\"file://%s\"></a>"%(self.IdConsultation,tips,icone)
		if self.IsImage:
			icone=config.WorkingPath+'/images/echo.png'
			res=self.GetImages(self.IdConsultation)
			tips=';'.join([i[1].decode(config.dbCodec) for i in res])
			text=text+"<a HREF=\"#I%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Imagerie\" src=\"file://%s\"></a>"%(self.IdConsultation,tips,icone)
		if self.IsChirurgie:
			icone=config.WorkingPath+'/images/scalpel.png'
			res=self.GetChirurgies(self.IdConsultation)
			tips=';'.join([i[0].decode(config.dbCodec) for i in res])
			text=text+"<a HREF=\"#c%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Chirurgie\" src=\"file://%s\"></a>"%(self.IdConsultation,tips,icone)
		if self.IsOrdonnance:
			icone=config.WorkingPath+'/images/doc_all.png'
			text=text+"<a HREF=\"#O%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Ordonnance\" src=\"file://%s\"></a>"%(self.IdConsultation,icone)
		if self.IsPlanTher:
			icone=config.WorkingPath+'/images/planT.png'
			text=text+"<a HREF=\"#T%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Plan Thérapeutique\" src=\"file://%s\"></a>"%(self.IdConsultation,icone)
		text=text+"&emsp;&emsp;&emsp;&emsp;<font color=\"red\">%s</font>"%self.Pathologies
		text=text+"<br>%s<br><span style=\"text-decoration:underline;\">Traitements</span> : %s<br>"%(self.Observations,self.Traitements)
		return text

	def GetConsultants(self):
		res=self.DBase.RechercheSQL_liste("""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsConsultant""")
		clst=QtCore.QStringList()
		self.idConsultants=[]
		for i in res:
#			print i[1].decode(config.dbCodec).decode('utf8')
			clst.append(i[1].decode(config.dbCodec))
			self.idConsultants.append(i[0])
		return clst
	
	def GetidConsultants(self,index):
		return self.idConsultants[index]
	
	def GetReferants(self):
		res=self.DBase.RechercheSQL_liste("""SELECT idPersonne,CONCAT(Nom," ",Prenom) FROM Personne WHERE IsReferant""")
		clst=QtCore.QStringList()
		self.idReferants=[]
		for i in res:
			clst.append(i[1].decode(config.dbCodec))
			self.idReferants.append(i[0])
		return clst
	
	def GetTypesConsultation(self):
		res=self.DBase.RechercheSQL_liste("SELECT idTypeConsultation,TypeConsultation FROM TypeConsultation")
		clst=QtCore.QStringList()
		self.idTypesConsultation=[]
		for i in res:
			clst.append(i[1].decode(config.dbCodec))
			self.idTypesConsultation.append(i[0])
		return clst
	
class Consultations:
	def __init__(self):
		self.consultations=[]
		self.textHTML=''
		self.DBase=Tables.DataBase(config.database)
		
	def GetConsultations(self,idAnimal):
		MyConsult=Consultation()
		self.textHTML=''
		self.consultations=self.DBase.RechercheSQL_liste("CALL GetConsultationS(%i)"%idAnimal)
		for i in self.consultations:
			MyConsult.FormatConsultation(i)
			self.textHTML=self.textHTML+'<br>'+MyConsult.MakeHTML()
		return self.textHTML
		
if __name__ == '__main__':
	
	MyConsult=Consultation()
	MyConsult.GetConsultants()
	
	#res=MyConsult.GetConsultation(2)
	#MyConsult.FormatConsultation(res[0])
	
	#MyDossier=Consultations()
	#print MyDossier.GetConsultations(1)


