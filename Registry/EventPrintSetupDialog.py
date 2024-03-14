# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import *

from library.Utils import *
from Reports.Report import *
from Reports.ReportBase import *
from Ui_EventPrintSetupDialog import Ui_EventPrintSetupDialog

class CEventPrintSetupDialog(QtGui.QDialog, Ui_EventPrintSetupDialog):
    def __init__(self, parent=None,  patient = ''):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        date = QDate.currentDate().addDays(-3)
        self.endDate.setDate(lastMonthDay(date))
        self.begDate.setDate(firstMonthDay(date))
        
    def getParams(self):
        return {
            'begDate' : self.begDate.date(), 
            'endDate' : self.endDate.date(), 
            'orgStructureId' : self.cmbOrgStructure.value(), 
            #'dateType' : 0 if self.rbPoUsl.isChecked() else 1
        }
