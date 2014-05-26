#!/usr/bin/env python
# -*- coding: utf8 -*-
import re
from PyQt4.QtCore import *
from PyQt4.QtSql import *
import config

class Ctable:
	def __init__(self,DBase,table):
		self.Table=table
		self.DBase=DBase
		res=self.DBase.record(self.Table)
		self.TableFields=[str(res.fieldName(i)) for i in range(res.count())]
		for i in self.TableFields:
			self.__dict__.update({i:None})             

	def Print(self):
		print '#attributes: '+','.join(self.TableFields)
		for i in self.TableFields:
			print '%s : %s\t\t\t(%s)'%(i,str(self.__dict__[i]),type(self.__dict__[i]))

		
	
def ValideDate(date,formatin='dmyy'):
	if not isinstance(date, basestring):
		return None
	if formatin=='dmyy':
		res=re.findall(r'([0-2][0-9]|3[0-1])[-/\. ](0[0-9]|1[0-2])[-/\. ]([1-2][0-9]{3})',date)
	if formatin=='yymd':
		res=re.findall(r'([1-2][0-9]{3})[-/\. ](0[0-9]|1[0-2])[-/\. ]([0-2][0-9]|3[0-1])',date)
	if len(res)==0:
		return None
	#inverse le format de sortie
	res=res[0]
	if formatin=='dmyy':
		date='%s-%s-%s'%(res[2],res[1],res[0])
	if formatin=='yymd':
		date='%s/%s/%s'%(res[2],res[1],res[0])
	return date

def ValideTelephone(tel):
	if not isinstance(tel, basestring):
		return None
	#TODO format tel étrangers
	res=re.findall(r'(0[0-9])[- \.]{,1}([0-9]{2})[- \.]{,1}([0-9]{2})[- \.]{,1}([0-9]{2})[- \.]{,1}([0-9]{2})',tel)
	if len(res)==0:
		return None
	return res

	

if __name__ == '__main__':
	db = QSqlDatabase.addDatabase("QMYSQL")
	db.setHostName ( config.host )
	db.setUserName ( config.user )
	db.setPassword ( config.password )
	db.setDatabaseName(config.database)
	if not db.open():
		print 'connection impossible'
	Mytable=Ctable(db,'Analyse')
	Mytable.Print()
	