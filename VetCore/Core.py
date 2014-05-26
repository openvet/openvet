#!/usr/bin/env python
# -*- coding: utf8 -*-
import re
from PyQt4 import QtCore
import Tables

def GetDbLines(DBase,request):	#TODO: Move in Table
	clst=[]
	res=DBase.RechercheSQL_liste(request)
	if len(res)==0:
		return([])
	for i in res:
		tmp=[]
		for j in i:
			if not j is None:
				tmp.append(QtCore.QString(str(j).decode(DBase.dbCodec)))
			else:
				tmp.append(QtCore.QString(''))
		clst.append(tmp)
	return clst

def GetDbText(DBase,request):
	clst=[]
	res=DBase.RechercheSQL_liste(request)
# 	TODO:
# 	if not type(res)==tuple:
# 		return None
	if len(res)==0:
		return([])
	for i in res[0]:
		if not i is None:
			clst.append(QtCore.QString(str(i).decode(DBase.dbCodec)))
		else:
			clst.append(QtCore.QString(''))
	return clst

def GetDbidText(DBase,request,Tous=False):
	clst=[]
	if Tous:
		clst.append([0,QtCore.QString("Tous")])
	res=DBase.RechercheSQL_liste(request)
	for i in res:
		txt=QtCore.QString(i[1].decode(DBase.dbCodec))
		clst.append([i[0],txt])
	return clst
		
	
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

def Logout(chaine):
	fout=open('debug.log','a')
	fout.write(chaine+'n')
	fout.close()
	

if __name__ == '__main__':
	a=QtCore.QString(u'')
	print a.toUtf8()
	