#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import PythonMagick
#from xhtml2pdf import pisa

class DocViewer:
    def __init__(self,filename=None):
        if not filename is None:
            self.filename=QString(filename)
        else:
            self.filename=None
        self.image=None
    
    def SetFilename(self,filename):
        self.filename=QString(filename)
           
    def ViewImage(self,size,maxfactor=2.5):     #return a pixmap #TODO:Make single fuction with make sticker(save=True)
        if self.filename is None:
            return
        ext=self.filename.right(self.filename.length()-self.filename.lastIndexOf('.')-1).toLower()
        if ext=='pdf':
            os.system('convert -density 196 %s[0] -resample 72 -trim +repage ../tmp.png'%self.filename)
            #convert -density 196 Task.txt -blur 0x0.7 -resample 72 -unsharp 0x0.7 -trim +repage Task.gif
            self.filename='../tmp.png'
        self.image=QImage(self.filename)
        if self.image.size().width()>self.image.size().height():
            factor=float(size.width())/ self.image.size().width()
        else:
            factor=float(size.height())/ self.image.size().height()
        factor=min(factor,maxfactor)
        scaledimage=self.image.scaled(factor*self.image.size().width(),factor*self.image.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QPixmap.fromImage(scaledimage)
    
    def ViewText(self,widget):
        try:
            text=QString(u'%s'%open(self.filename,'r').read())
        except:
            text=QString.fromLatin1(open(self.filename,'r').read()) #Bug de caractères accentué selon formats
        if self.GetSuffix() in ['html','htm']:
#             if text.count('>')<5:       #if format is invalid (other test more reliable?)
#                 os.system('xhtml2pdf %s ../tmp.pdf'%self.filename)
#                 self.filename=QString('../tmp.pdf')
#                 return False
#             else:        #TODO: if html format is not known us external viewer for conversion in pdf
                widget.setHtml(text)
        else:
            widget.setPlainText(text)
        return True
            
    def MakeSticker(self,size,filename=None):   #filename is  python string
        isPdf=False
        if not filename is None:
            self.filename=filename
        if self.GetSuffix() in ['pdf','html','htm','txt']:
            isPdf=True
            os.system('convert -density 196 %s[0] -resample 72 -trim +repage ../tmp.png'%self.filename)
            filename=self.filename
            self.filename='../tmp.png'
        self.image=QImage(self.filename)
        if self.image.size().width()>self.image.size().height():
            factor=float(size.width())/ self.image.size().width()
        else:
            factor=float(size.height())/ self.image.size().height()
        scaledimage=self.image.scaled(factor*self.image.size().width(),factor*self.image.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if isPdf:
            filename_r=filename[:filename.rindex('.')]+'_r.png'
        else:
            filename_r=self.filename[:self.filename.rindex('.')]+'_r'+self.filename[self.filename.rindex('.'):]
        scaledimage.save(filename_r)
        return QString(filename_r[filename_r.rindex('/')+1:])
    
    def Sharpen(self,sigma=0.0,radius=3):   #TODO: use pythonmagick instead of Os command?
        filename_p=self.Filename_('_p')
        os.system('convert %s -sharpen %.1fx%i %s'%(self.filename,sigma,radius,filename_p))
        self.filename=filename_p
        return filename_p
    
    def Brightness(self,brightness):
        cmd='convert %s '%self.filename
        if brightness>0:
            cmd+='-sigmoidal-contrast %ix0 '%brightness
        else:
            cmd+='+sigmoidal-contrast %ix0 '%brightness
        filename_p=self.Filename_('_p')
        os.system(cmd+'%s'%filename_p)
        self.filename=filename_p
        return filename_p
        
    def Filename_(self,ext,name=None):
        if name is None:
            name=self.filename
        name=str(name)
        if name.count('%s.'%ext)==0:
            name=name[:name.rindex('.')]+str(ext)+name[name.rindex('.'):]
        return QString(name)
    
    def GetSuffix(self,name=None):
        if name is None:
            name=self.filename
        name=str(name)
        return name[name.rindex('.')+1:].lower()