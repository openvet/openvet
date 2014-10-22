# -*- coding: utf8 -*-
import re
import os
import codecs
import time
from decimal import Decimal
from MyGenerics import *
from PyQt4 import QtCore, QtGui, QtSql

path = '/media/Datas/Kiwi/OpenVet0.2'
path = '../'
pathimport = path + 'Imports/'
erreur = False

def ExtractNumeric(chaine):
    r = re.findall(r'[0-9]*[ ,]?[0-9]+', chaine)
    if len(r) > 0:
        r[0] = r[0].strip()
    else:
        erreur = True
        r = ['Nombre non trouvé']
    return r

def ExtractUnit(chaine, nombre):
    unites = ['g', 'mg', 'UI', 'CH']
    pattern = re.compile('|'.join(unites))
    start = chaine.find(nombre)
    if start == -1:
        erreur = True
        r = ['Nombre invalide pour unité.']
        return r
    r = re.findall(pattern, chaine[start + len(nombre):])
    if len(r) == 0:
        erreur = True
        r = ['Unité inconnue.']
    return r[0]

def ExtractForme(chaine, isquantitatif):
    formes = ['comprimé', 'goutte', 'poudre', 'ml']
    pattern = ''
    chform = '|'.join(formes)
    if isquantitatif:
        pattern = '[Ss]oit '
        pattern = pattern + '([0-9]*[ ,]?[0-9]+.+)(' + chform + ')([^\.]+)'
    else:
        pattern = '(.+ )(' + chform + ')([^\.]+)'
        # éliminer phrase avant . si il y en a?
    pattern = re.compile(pattern)
    r = re.findall(pattern, chaine)
    if len(r) == 0:
        erreur = True
        r = ['Forme inconnue']
    return ''.join(r[0])

def GetListProp(name):
    fin = open(name, 'r')
    index = 0
    lignes = ''
    liste = []
    valid = False
    for i in fin:
        if not re.match(r'^[1-9]\.', i) is None:
            index += 1
            if valid:
                liste.append(lignes.strip())
            lignes = ''
            valid = False
        else:
            if index in [1, 2, 3, 5, 7, 13, 27]:
                valid = True
                if index in [2, 27]:
                    lignes = lignes + i
                else:
                    if len(i) > 1:
                        lignes = lignes + ' ' + i.strip()        
    fin.close()
    return liste

def GetSubstances(chaine):
# extraction substances actives
    comp = chaine
    start = comp.find('Substance(s) active(s)') + 26
    if start == 25:
        start = 0
    end = comp.find('\n\n', start)
    comp = comp[start:end]
    comp = [i for i in comp.split('\n')]
    substances = []
    for i in comp:
        r = re.findall(r' \.* +[0-9]', i)
        if len(r) == 0:
            continue
        end = i.index(r[0])
        med = i[:end].strip()
        qte = ExtractNumeric(i)[0]
        unit = ExtractUnit(i, qte)
        substances.append([med.lower(), qte, unit])
    return substances

def GetPosologie(chaine, substances):
    # extraction posologie
    comp = chaine
    quantitatif = True
    start = 0
    doses = []
    for i in substances:
        r = re.findall('[0-9]*[ ,]?[0-9]+.+de ' + i[0] + ' par ', comp[start:])
        if len(r) > 0:
            qte = ExtractNumeric(r[0])[0]
            unit = ExtractUnit(r[0], qte)
            doses.append([i[0], qte, unit])
            start = comp[start:].index(r[0]) + len(r[0])
    if len(doses) == 0:
        quantitatif = False
    else:
        quantitatif = True
    forme = ExtractForme(comp, quantitatif)
    return[doses, forme]

def GetPresentation(chaine):
    # extraction présentations
    comp = chaine
    comp = [i for i in comp.split('\n')]
    presentations = []
    amm = False
    for i in comp:
        r = re.findall(r'FR/.+[0-9]+ [0-9]{1,2}/[12][0-9]{3}', i)
        if len(r) == 1:
            amm = True
            continue
        else:
            if amm:
                presentations.append(i.replace('.', ' ').split())
            else:
                r1 = re.findall(r'[^:]+', i)
                presentations.append(r1[0].replace('.', ' ').strip())
    return presentations

def GetDecimal(chaine):
        chaine.replace('\'', '')
#        sols=re.findall(r'[0-9]+[ ,]?[0-9]*',chaine)
        sols = re.findall(r'[0-9 ,]+', chaine)
        try:
            return Decimal([i for i in sols if len(i.strip()) > 0][0].replace(',', '.').replace(' ', ''))
        except:
            return(Decimal('0'))

def Getunite(chaine):
        sols = re.findall(r'([0-9 ,]+)(DL50|kBq|mEq|millions UI|million.*internationales|[a-z]+)', chaine)
        sol = [i for i in sols if i[0] != ' ']
        if len(sol) == 0:
            return 'aucune'
#         elif sol[0][1]=='milliard':
#             print
        else:
            if sol[0][1] in ['bar', 'x', 'bact', 'ampoule', 'dose', 'milliards']:
                return 'aucune'
            else:
                return sol[0][1]

def GetShortPresentation(chaine):
    first = re.findall(r'(^[0-9 ]*\S+)', chaine)  # TOTEST r'(^[0-9 ]*\S[^\(\)]+)(?:\(s\))?[ -]'
    last = re.findall(r'de ([0-9, ]+\S+$)', chaine)
    if len(first) == 0:
        print 'erreur avec %s' % chaine    
    if len(last) == 0:
        last = re.findall(r'de ([0-9, ]+\S[^\( ]+)', chaine)
        if len(last) == 0:
            last = ['']       
    return ' '.join([first[0].replace('(s)', ''), last[0].replace('(s)', '')])  

def GetVoieAdministration(chaine):
    nchaine = unicode(chaine.decode('latin-1'))
    sel = re.findall(r'ophtalmique|auriculaire|gingivale|buccale|dentaire|[^-]?cutanée|intradermique|transdermique|nasale|inhalée|rectale|vaginale|orale|sublinguale|sous-cutanée|intraveineuse|intramusculaire|intrapéritonéale|intra-articulaire|périarticulaire|péridurale|périneurale|intralésionnelle|infiltration', nchaine)  
    if len(sel) == 0:
        sel = ['autre']
#         print chaine
    return ','.join(sel) 
            
def FormatSelection(liste):
    return[liste[0], liste[5],liste[1], liste[2], liste[3], max('1' * liste[4], '0')]


def ImportComposition(filin='LCompSpeHum.txt', filout='CompHum.txt'):
    print 'Compositions'
    finlog = codecs.open(pathimport + filin, 'r', encoding='iso-8859-1')
    molecules = []
    refs = []
    for line in finlog:
        words = line.split('\t')
        if len(words) > 5:
            if words[0] not in refs:
                refs.append(words[0])
#             if words[0]=='60092590':
#                 print words
            longname=re.sub(r' POUR PR.PARATIONS HOM.OPATHIQUES| BASE| ANHYDRE| SODIQUE','',words[3])
            shortname = re.sub(r'(^\S+ATE D[E\'] ?)|( \(.+\))|(,.+$)|( \S*HYDRAT\S+$)', '', longname) 
            if words[3].count('HOMÉOPATHIQUES'):
                medoc = [0, words[0], words[1], longname, '0,0', words[5], True,shortname]
            else:
                medoc = [0, words[0], words[1], longname, words[4], words[5], False,shortname]
            molecules.append(medoc)
    finlog.close()
    selref = []
    exclude = ['DE', 'SULFATE']     #pourquoi c'est faire déjà dans doublon?
    for ref in refs:
        selection = [[i[1], i[3], i[4], i[5], i[6],i[7]] for i in molecules if i[1] == ref and i[4] != '']
        while len(selection) > 1:
            doublon = [index for index, i in enumerate(selection[1:]) if len([j for j in i[1] if j in selection[0][1] and j not in exclude]) > 0]
            if len(doublon):
                index = doublon[0] + 1
                if GetDecimal(selection[0][2]) > GetDecimal(selection[index][2]):
                    selref.append(FormatSelection(selection[index]))
                else:
                    selref.append(FormatSelection(selection[0]))
                selection.pop(0)
                selection.pop(0)
            else:
                selref.append(FormatSelection(selection[0]))
                selection.pop(0)
        if len(selection) == 1:
            selref.append(FormatSelection(selection[0]))       
    foutlog = codecs.open(pathimport + filout, 'w', encoding='utf-8')
    uq = []
    for i in selref:
        if i not in uq:  # remove doublons
            uq.append(i)
            foutlog.write(';'.join(i) + '\n')
    foutlog.close() 
    
def ImportSpecialite(filin='LSpeHum.txt', filout='SpeHum.txt'):
    print "Specialite"
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='iso-8859-1')
    for line in finlog:
        line = line.replace(';', ',')
        words = line.split('\t')
        if len(words) > 5:
            words[1] = words[1].replace('\"', '')
            names = words[1].split()
            if len(names[0]) < 4 or 'Enreg homéo' in words[5]:
                name = ' '.join([names[0], names[1]])
            else:
                name = names[0].strip('.,')
#             if name=='STEROGYL':
#                 print words[1]
            if 'Enreg homéo' in words[5]:
                selection.append([words[0], name, words[1].split(',')[0], ' ', ' ', '1'])
            else:
                Vadmin = GetVoieAdministration(words[3]).encode('latin-1')
                selection.append([words[0], name, words[1].split(',')[0], words[2], Vadmin, '0'])
    finlog.close()   
    foutlog = codecs.open(pathimport + filout, 'w', encoding='utf-8')
    for i in selection:
        foutlog.write(';'.join(i) + '\n')
    foutlog.close() 
    
def ImportPresentation(filin='LPresSpeHum.txt', filout='PresHum.txt'):
    print "Présentation"
    selection = []
    finlog = codecs.open(pathimport + 'LPresSpeHum.txt', 'r', encoding='iso-8859-1')
    for line in finlog:
        words = line.split('\t')
        if len(words) > 5:
            short = GetShortPresentation(words[2])
            selection.append([words[0], short])
    finlog.close()   
    foutlog = codecs.open(pathimport + 'PresHum.txt', 'w', encoding='utf-8')
    for i in selection:
        foutlog.write(';'.join(i) + '\n')
    foutlog.close() 

def GetListeAdministration(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
#         if len(words[4].split(','))>1:
#             print words[4].split(',')
        for word in words[4].split(','):
            if word.strip() not in selection and len(word.strip()) > 0:
                selection.append(word.strip())
    finlog.close()
    return selection

def GetListeMolecule(filin):
    selection = []
    myliste=[]
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        if words[2].strip() not in selection and len(words[2].strip()) > 0:
            selection.append(words[2].strip())
            #TODO: GET famille therapeutique
            myliste.append([words[2].strip(),words[1].strip(),words[0]])
    finlog.close()
    return myliste

def GetUniteAdministration(chaine):
    nchaine = unicode(chaine.decode('latin-1'))
    sols = re.findall(r'comprimé|gélule|capsule|suspension|solution|dispersion|buvable|injectable|perfusion', nchaine)
    if len(sols) == 0:
        return (chaine, False)
    elif len(sols) == 2:
        if sols[1] == 'buvable':
            return ('solution buvable', False)
        else:
            return ('solution injectable', True)
    elif len(sols) == 1 and sols[0] == 'suspension':
        return (chaine, False)
    else:
        return (sols[0].encode('latin-1'), False)
    return
    
def GetListeUniteMedoc(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        word = words[3].strip()
        if words[5].strip() == '0':  # if isHomeo skip
            word = GetUniteAdministration(word)
            if word not in selection:
                selection.append(word)
    finlog.close()
    return selection

def GetListeContenant(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        word = words[3].strip()
        if word not in selection:
            selection.append(word)
    finlog.close()
    return selection

def GetListeUniteMolecule(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        word = words[2]
        valeur = GetDecimal(word)
        unite = Getunite(word)
        try:
            unite = unite.strip()
        except:
            print 'Erreur %s' % word
        if unite not in selection:
            selection.append(unite)
    finlog.close()
    return selection

def SaveVoiesAdministration(filin, parent):
    model = MyModel('VoieAdministration', 0, parent)
    for i in GetListeAdministration(filin):
        model.SetNew([0, unicode(i.decode('latin-1')), QVariant(), True])
        model.New()
        model.Update()

    
def SaveMedicament(filin, parent=None):
    model = MyModel('Medicament', 0, parent)
    modelRef = MyModel('VoieAdministrationRef', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split(';')
        data = []
        for j in i:
            j = unicode(j.strip().decode('latin-1'))
            if len(j) == 0:
                j = QVariant()
            data.append(j)
        ishomeo = True
        isinj = False
        if i[5].strip() == '0':
            ishomeo = False               
            isinj = GetUniteAdministration(i[3])[1]
#         if data[1]=='APTIVUS':
#             print
        model.SetNew([0, data[1], data[2], 'H' + data[0], ishomeo, isinj, data[3], QVariant(), 0, 1, ''])
        model.New()
        idMedicament = model.Update()
        # Save Voies Administrations in VoieAdministrationRef
        if data[4] == QVariant():
            continue
        if idMedicament.toInt()[1]:
            idMedicament = idMedicament.toInt()[0]
            for i in data[4].split(','):
                idVoie = model.MyRequest.GetInt('CALL GetidVoieAdmin(\"%s\")' % i, 0)
                if not idVoie is None:
                    modelRef.SetNew([0, idVoie, idMedicament, 1, ''])
                else:
                    print u'%s non trouvé dans la base' % i
            modelRef.New()
            modelRef.Update()

def SavePresentation(filin, parent):
    model = MyModel('Presentation', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split(';')
        i[1] = unicode(i[1].strip().decode('latin-1'))
        idMedicament = model.MyRequest.GetInt('CALL GetidMedicament_Cip(\"H%s\")' % i[0], 0)
        if not idMedicament is None:
            model.SetNew([0, idMedicament, i[1], QVariant(), QVariant(), True, ''])
            model.New()
            model.Update()
        else:
            print 'H%s non trouvé' % i[0]

def SaveMolecules(filin, parent):
    model = MyModel('Molecule', 0, parent)
    for i in GetListeMolecule(filin):
        if not model.MyRequest.GetInt('CALL isVaccin_Cip(\"H%s\")'%i[2],0):
            model.SetNew([0,unicode(i[0].decode('latin-1')),unicode(i[1].decode('latin-1')), QVariant(), True,False])
            model.New()
            if model.Update()==-1:
                print model.lasterror+' pour :'
                print i
            
def SaveCompositions(filin,parent): #TODO
    model = MyModel('Molecule', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split(';')
        i[1] = unicode(i[1].strip().decode('latin-1'))
        idMedicament = model.MyRequest.GetInt('CALL GetidMedicament_Cip(\"H%s\")' % i[0], 0)
        if not idMedicament is None:
            model.SetNew([0, idMedicament, i[1], QVariant(), QVariant(), True, ''])#TOMODIFY
            model.New()
            model.Update()
        else:
            print 'H%s non trouvé' % i[0]
    
#ImportComposition()
# ImportSpecialite()
# ImportPresentation()
# for i,j in enumerate(GetListeAdministration('SpeHum.txt')):
#     print '%i.%s'%(i+1,j)
# for i,j in enumerate(GetListeUniteMedoc('SpeHum.txt')):
#     print '%i.%s'%(i+1,j)
# for i,j in enumerate(GetListeContenant('CompHum.txt')):
#     print '%i.%s'%(i+1,j)      
# for i,j in enumerate(GetListeUniteMolecule('CompHum.txt')):
#     print '%i.%s'%(i+1,j)

if __name__ == '__main__':
    t0=time.time()
    app = QtGui.QApplication(sys.argv)
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName ( config.host )
    db.setUserName ( config.user )
    db.setPassword ( config.password )
    db.setDatabaseName(config.database)
    if not db.open():
        QtGui.QMessageBox.warning(None, "Opencompta",
            QtCore.QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)
       
    window = QDialog()
    window.show()
    SaveVoiesAdministration('SpeHum.txt',window)
    SaveMedicament('SpeHum.txt',window)
#     SavePresentation('PresHum.txt',window)
    SaveMolecules('CompHum.txt',window)
    print time.time()-t0  
    sys.exit(app.exec_())



 
# final=[]
# for i in selref:
#     if i[0]=='60028495':
#         print 'Dolirhume'
#     spe=[j for j in selection if i[0]==j[0]][0]
#     item=list(spe)
#     item.extend(i[1:])
#     final.append(item)     
# foutlog=codecs.open(pathimport+'MedHum.txt','w',encoding='utf-8')
# for i in final:
#     foutlog.write(';'.join(i)+'\n')
# foutlog.close()           


#     extrait=[None]*len(liste)
#     extrait[0]=liste[0]
#     extrait[1]=GetSubstances(liste[1])
#     extrait[2]=re.sub(r'\.$','',liste[2])
#     extrait[3]=liste[3].replace('.','').replace(' et ',', ').lower().split(',')
#     extrait[4]=re.sub(r'\.$','',liste[4])
#     extrait[5]=GetPosologie(liste[5],extrait[1])
#     extrait[6]=GetPresentation(liste[6])


