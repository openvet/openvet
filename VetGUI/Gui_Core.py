#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
import Core

def FillCombobox(combobox,function):       #Fill from list of items. Do not fit for large list TODO transfert in Core
    combobox.clear()
    lst=function
    for i in lst:
        combobox.addItem(i[1],i[0])


