# -*- coding: utf8 -*-
import re

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
	print ValideTelephone('03.81.94.13.66')
			
	
