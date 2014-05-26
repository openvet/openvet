#!/usr/bin/python
# -*- coding: utf8 -*-
import Tables
import time
import config

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
		
	def Print(self):
		for j in [i for i in self.__dict__.keys() if i[:1] != '_']:
			print'%s : %s'%(j,getattr(self,j))
		
	def GetBiologies(self,idConsultation):
		DBase=Tables.DataBase(config.database)
		res=DBase.RechercheSQL_liste("CALL GetBiologies(%i)"%idConsultation)
		return res
			
	def GetImages(self,idConsultation):
		DBase=Tables.DataBase(config.database)
		res=DBase.RechercheSQL_liste("CALL GetImages(%i)"%idConsultation)
		return res
	
	def GetChirurgie(self,idConsultation):
		DBase=Tables.DataBase(config.database)
		
		res=DBase.RechercheSQL_liste("CALL GetChirurgie(%i)"%idConsultation)
		return res
			
	def GetConsultation(self,idConsultation):
		DBase=Tables.DataBase(config.database)
		
		res=DBase.RechercheSQL_liste("CALL GetConsultation(%i)"%idConsultation)
		self.IdConsultation=res[0][0]
		self.Date='%02i/%02i/%i'%(res[0][1].day,res[0][1].month,res[0][1].year)
		self.Type=res[0][2].decode(config.dbCodec)
		self.Consultant=res[0][3].decode(config.dbCodec)		
		if res[0][4]!=None:
			self.Referant=res[0][4].decode(config.dbCodec)
		else:
			self.Referant=''
		if res[0][5]!=None:
			self.Pathologies=res[0][5].decode(config.dbCodec)
		else:
			self.Pathologies=''
		if res[0][6]!=None:
			self.Observations=res[0][6].decode(config.dbCodec)
		else:
			self.Observations=''
		if res[0][7]!=None:
			self.Traitements=res[0][7].decode(config.dbCodec)
		else:
			self.Traitements=''
		if res[0][8]:
			self.IsBiologie=True
		if res[0][9]:
			self.IsImage=True
		if res[0][10]:
			self.IsChirurgie=True
		if res[0][10]:
			self.IsOrdonnance=True
		if res[0][11]:
			self.IsPlanTher=True
	
	def MakeHTML(self):
		text="<b>%s</b>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp;%s<br>"%(self.Date,self.Consultant,self.Type,self.Referant)
		if self.IsBiologie:
			icone=config.WorkingPath+'/images/analyse.png'
			res=self.GetBiologies(self.IdConsultation)
			tips=';'.join([i[1].decode(config.dbCodec) for i in res])
			text=text+"<img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Biologie\" src=\"file://%s\">"%(tips,icone)
		if self.IsImage:
			icone=config.WorkingPath+'/images/echo.png'
			res=self.GetImages(self.IdConsultation)
			tips=';'.join([i[1].decode(config.dbCodec) for i in res])
			text=text+"<img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Imagerie\" src=\"file://%s\">"%(tips,icone)
		if self.IsChirurgie:
			icone=config.WorkingPath+'/images/scalpel.png'
			res=self.GetChirurgie(self.IdConsultation)
			tips=';'.join([i[0].decode(config.dbCodec) for i in res])
			text=text+"<img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Chirurgie\" src=\"file://%s\">"%(tips,icone)
		if self.IsOrdonnance:
			icone=config.WorkingPath+'/images/doc_all.png'
			text=text+"<img style=\"width: 32px; height: 32px;\" alt=\"Ordonnance\" src=\"file://%s\">"%icone
		if self.IsPlanTher:
			#TODO tips
			icone=config.WorkingPath+'/images/planT.png'
			text=text+"<img style=\"width: 32px; height: 32px;\" alt=\"Plan Thérapeutique\" src=\"file://%s\">"%icone
		text=text+"&emsp;&emsp;&emsp;&emsp;<font color=\"red\">%s</font>"%self.Pathologies
		text=text+"<br>%s<br><span style=\"text-decoration:underline;\"Traitements :</span> %s<br>"%(self.Observations,self.Traitements)
		return text
		
if __name__ == '__main__':
	MyConsult=Consultation()
	print MyConsult.GetConsultation(2)
	print MyConsult.MakeHTML()
	#MyConsult.Print()
	
#DBase=Tables.DataBase('OpenVet12')
#res=DBase.RechercheSQL_liste("CALL GetConsultation(1)")
#print res
#test=Tables.Table('OpenVet12','Personne', '', auto=True) 

