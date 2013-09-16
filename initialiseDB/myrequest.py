#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
from datetime import date
import time
import sys


import parametres

host=parametres.host
repertoire=parametres.repertoire
user=parametres.user
password=parametres.password
database=parametres.database


class Table:
    
    def __init__(self,name):
        #self.parent
        try:
            self.con=mdb.connect(host,user,password,database)
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        self.con.set_character_set('utf8')
        self.champs=[]
        self.table=database+'.'+name
        self.getfields()
        
    def getfields(self):
        query="SHOW COLUMNS FROM "+self.table
        cur=self.con.cursor()
        cur.execute(query)
        rows=cur.fetchall()
        cur.close()
        for row in rows:
            champ=[]
            champ.append(row[0])
            a=row[1]
            if a[:7]=='varchar' or a[:4]=='char':
                champ.append(int(a[a.index('(')+1:a.index(')')]))
            if a[:7]=='decimal' or a[:7]=='float':
                champ.append(float)
            if a[:3]=='int' or a[:7]=='tinyint':
                champ.append(int)
            if a[:4]=='date':
                champ.append(date)
            self.champs.append(champ)

    
    def add(self,data,autoindex=False):
        #autoindex=True si le premier champ est autoincrement
        i=1
        lchamps=""
        if autoindex:
            champs=self.champs[1:]
        else:
            champs=self.champs
        for champ in champs:
            lchamps=lchamps+champ[0]+", "
        lchamps=lchamps[:-2]
        values=""
        i=1
        for i in data:
            if i==None:
                continue
            if i=='NULL':
                 values=values+"NULL, "
            elif isinstance(i,str):
                values=values+"\""+i+"\", "
            else:
                values=values+str(i)+", "
        values=values[:-2]
        query="""INSERT INTO %s (%s) VALUES (%s)"""%(self.table,lchamps,values)
        #print query
        error=self.execute(query)
        return error

    def valid(self,data):
        error=None
        i=0
        for champ in self.champs:
            #print(champ,data[i])
            error=self.validcol(data[i],i)
            if error!=None:
                return error
            i+=1
        #verification doublon automatique : idlist=UNIQUE=>error 1062
        error=self.check_doublon(data)
        return error
    
    def check_doublon(self,data):
        error=None
        #TODO doublon nom, adresse
        if self.table=='kiwi.Animal':
            req=[(data[1],1),(data[6],6),(data[9],9)]
            res=self.select(req)
            if len(res)>0:
                error='Doublon Animal'
        if self.table=='kiwi.Banque':
        	req=[(data[1],1),(data[4],4)]
        	res=self.select(req)
        	if len(res)>0:
        		error='Doublon Banque:%i'%res[0][0]
        if self.table=='Kiwi.depenses':
            req=[(data[1],1),(data[2],2),(data[6],6)]
            res=self.select(req)
            if len(res)>0:
                error='Doublon Depense:%i'%res[0][0]
                #TODO raise dialog box to valid
        return error
    
    def validcol(self,data,index):
        error=None
        if data==None:
            return error
        if isinstance(data,str):
            if data=='NULL':
                return error
        if isinstance(self.champs[index][1],int):
            if not isinstance(data,str) or len(data.replace("'",""))>self.champs[index][1]:
                error=self.champs[index][0]+' non valide'
        else:
            if str(self.champs[index][1])=="<type 'datetime.date'>":
            	try:
            		d=time.strptime(data,'%Y-%m-%d')
            	except:
            		error=self.champs[index][0]+' non valide.'
            else:
                if not isinstance(data,self.champs[index][1]):
                    #print data,type(data),self.champs[index][1]
                    error=self.champs[index][0]+' non valide.'
        return error
           
    def update(self,idname,idindex,data):
        if type(data)==list:
            dcolumn=True
        else:
            dcolumn=False
        error=None
        values=""
        if dcolumn==False:
            i=0
            for value in data:
                if value!=None:
                    values=values+self.champs[i][0]+"="
                    if value=='NULL':
                    	values=values+"NULL, "
                    elif isinstance(value,str):
                    	values=values+"\""+value+"\", "
                    else:
				values=values+str(value)+", "
                i+=1
            values=values[:-2]
        else:
            for i in data:
                error=self.validcol(i[0],i[1])
                if error!=None:
                    return error
                values=values+self.champs[i[1]][0]+"="
                if i[0]=='NULL':
                	values=values+"NULL, "
                elif isinstance(i[0],str):
                	values=values+"\""+i[0]+"\", "
                else:
                	values=values+str(i[0])+", "
            values=values[:-2]
        query="""UPDATE %s SET %s WHERE %s=%s"""%(self.table,values,idname,str(idindex))
        #if self.table=='kiwi.Client':
        #	query="""UPDATE %s SET %s WHERE idClient%s=%s"""%(self.table,values,str(idindex))
        #if self.table=='kiwi.Animal':
        #	query="""UPDATE %s SET %s WHERE idAnimal=%s"""%(self.table,values,str(idindex))
        #print query
        error=self.execute(query)
        return error

    def delete(self,idname,idindex):
        query="DELETE FROM "+self.table+" WHERE "+idname+"="+str(idindex)
        #print query
        error=self.execute(query)
        return error

    def select(self,data,order=None,colonne=None):
        if type(data)==list:
            dcolumn=True
        else:
            dcolumn=False
        query="SELECT "
        if colonne==None:
            query=query+"*"
        else:
            query=query+colonne
        query=query+" FROM "+self.table+" WHERE "
        values=""
        if dcolumn==True:
            for i in data:
                if isinstance(i[0],str):
                    values=values+self.champs[i[1]][0]+"='"+i[0]+"' AND "
                else:
                    values=values+self.champs[i[1]][0]+"="+str(i[0])+" AND "
        else:
            i=0
            for value in data:
                if value!=None:
                    values=values+self.champs[i][0]+"="+value+" AND "
                i+=1
        values=values[:-4]
        query=query+values
        if order!=None:
            query=query+" ORDER BY "+order
        cur=self.con.cursor()
        cur.execute(query)
        rows=cur.fetchall()
        cur.close()
        return rows
    
    def select_query(self,query):
    #query=unicode(query,'utf-8')
        cur=self.con.cursor()
        cur.execute(query)
        rows=cur.fetchall()
        cur.close()
        return rows
    
    def execute(self,query):
        error=None
        cur=self.con.cursor()
        try:
            cur.execute(query)
        except mdb.Error, e:
            error="Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        if error==None:
            self.con.commit()
        return error

    def close(self):
        self.con.close()
    
def execute(query):
    try:
        con=mdb.connect(host,user,password,database)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    con.set_character_set('utf8')        
    error=None
    cur=con.cursor()
    rows=None
    #print query
    try:
        cur.execute(query)
        rows=cur.fetchall()
    except mdb.Error, e:
        error="Error %d: %s" % (e.args[0], e.args[1])
    cur.close()
    if error==None: #erreur a revoir indentation corrigee
        con.commit()
    con.close()
    return (error,rows)
    
def savedata(query):
    try:
        con=mdb.connect(host,user,password,database)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    #con.set_character_set('utf8')        
    error=None
    cur=con.cursor()
    print query
    try:
        cur.execute(query)
    except mdb.Error, e:
        error="Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
    if error==None:
    	con.commit()
    con.close()
    return (error)    


def get_listclt(data=None):
    if data==None:
        res=execute("SELECT idlist FROM kiwi.Client ORDER BY idlist")
    else:
        res=execute("SELECT idlist FROM kiwi.Client WHERE idlist LIKE '"+data+"%' ORDER BY idlist")
    reslist=[]
    for i in res[1]:
        reslist.append(i[0])
    return reslist

def get_communes(data=None):
    if data==None:
        res=execute("SELECT * FROM kiwi.Communes ORDER BY Commune")
    else:
        res=execute("SELECT * FROM kiwi.Communes WHERE Commune LIKE '"+data+"%' ORDER BY Commune")
    reslist=[]
    for i in res[1]:
        reslist.append((i[0],i[1]))
    return reslist

def get_datacltanl(data):
    clt=execute("""SELECT * FROM kiwi.Client WHERE idlist=\"%s\""""%data)
    clt=clt[1][0]
    idclt=clt[0]
    res=execute("SELECT * FROM kiwi.Animal WHERE Client_idClient='"+str(idclt)+"'")
    reslist=[]
    for i in res[1]:
        reslist.append(i)
    return (clt,reslist)

def get_lstAnimal(idclt):
	res=execute("SELECT * FROM kiwi.Animal WHERE Client_idClient='"+str(idclt)+"'")
    	reslist=[]
    	for i in res[1]:
    		reslist.append(i)
    	return reslist

def get_idAnimal(idClient,nom):
  	res=execute("SELECT idAnimal FROM kiwi.Animal WHERE Client_idClient='"+str(idClient)+"' AND nom='"+nom+"'")
  	return res[1]
  	
def get_client(idclt):
	clt=execute("SELECT * FROM kiwi.Client WHERE idClient='"+str(idclt)+"'")
	clt=clt[1][0]
	return clt
()

def get_especes():
	lst=[]
	esp=execute("SELECT Espece FROM kiwi.Races GROUP BY Espece")
	esp=esp[1]
	for i in esp:
		lst.append(i[0].replace('\r',''))
	return lst

def get_races(espece):
	lst=[]
	res=execute("SELECT Race FROM kiwi.Races WHERE Espece LIKE '%s'"%(espece+'%'))
	res=res[1]
	for i in res:
		if len(i[0])>0:
			lst.append(i[0])
	return lst

def add(table,data, autoincrement=True):
    err2=err1=None
    a=Table(table)
    err1=a.valid(data)
    if err1==None:
            err2=a.add(data,autoincrement)
    a.close()
    return (err1,err2)

def update(table,idindex,data,idname=None):
    err2=err1=None
    if idname==None:
    	if table=='Client':
    		idname='idClient'
    	if table=='Animal':
    		idname='idAnimal'
    a=Table(table)
    err1=a.valid(data)
    if err1==None:
            err2=a.update(idname,idindex,data)
    a.close()
    return (err1,err2)

def delete(table,idname,idindex):
    a=Table(table)
    a.delete(idname,idindex)
    a.close()
    
#print get_lstAnimal(9)
#res=get_especes()
#res=get_races('Chien')
#print res
#data=(None,'Céleris','Amélie',"22, rue de l'hélébore",'Vandoncourt','25450','03.91.60.38.08','NULL','NULL','Céleris Amélie Vandoncourt','NULL',0.0)
#update('Client',9,data)
#data=(None,"L'homme",'Hector',"2, rue d'Enfer",'Vandoncourt','25450','03.91.36.10.08','NULL','NULL',"L'homme Hector Vandoncourt","C'est rien",0.0)
#add('Client',data)
#query="INSERT INTO kiwi.Races (Race,Espece) VALUES ('rien','Canard')"
#res=savedata(query)
#print res

#print add('Client',data)
#print get_datacltanl('Lamine Daniel Icy')

#adresse="18, rue de l'établi"
#query="""UPDATE kiwi.Client SET %s="%s" WHERE idClient=8"""%('adresse',adresse)
#print query
#con=mdb.connect('localhost','root','horizons','kiwi') #test in class 
#con.set_character_set('utf8')        
#cur=con.cursor()
#cur.execute(query)
#cur.close()
#con.commit()
#con.close()
