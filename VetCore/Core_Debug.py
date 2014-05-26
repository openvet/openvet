#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import date
import random
import os

def GetVarChar(maxlength, variation=0.3):
    Nom=''
    for i in xrange(random.randint(int(maxlength*variation),maxlength)):
        Nom=Nom+chr(random.randint(65,90))
    return(Nom[0]+Nom[1:].lower())

def GetDate(maxyears):
    end= date.today()
    newdate=date.fromordinal(end.toordinal()-random.randrange(365*maxyears))
    return '%i-%02i-%02i'%(newdate.year,newdate.month,newdate.day)
