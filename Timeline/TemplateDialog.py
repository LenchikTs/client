# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.DialogBase         import CDialogBase
from library.Utils              import forceBool, forceInt
from Timeline.PersonTimeTable   import CPersonTimeTableModel

from Timeline.Ui_TemplateDialog import Ui_TemplateDialog


class CTemplateDialog(CDialogBase, Ui_TemplateDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('TimeTable', CPersonTimeTableModel(self))
        self.setupUi(self)
        self.setModels(self.tblTimeTable, self.modelTimeTable, self.selectionModelTimeTable)
        self.tblTimeTable.horizontalHeader().moveSection(7, 1)


    def setDateRange(self, begDate, endDate):
        self.edtBegDate.setDateRange(begDate, endDate)
        self.edtEndDate.setDateRange(begDate, endDate)
        self.edtBegDate.setDate(begDate)
        self.edtEndDate.setDate(endDate)


    def setPersonId(self, personId):
        db = QtGui.qApp.db
        record = db.getRecord('Person', ('timelinePeriod', 'timelineCustomLength', 'fillRedDays'), personId)
        if record:
            period       = forceInt(record.value('timelinePeriod'))
            customLength = forceInt(record.value('timelineCustomLength'))
            fillRedDays  = forceBool(record.value('fillRedDays'))
        else:
            period       = 0
            customLength = 0
            fillRedDays  = False
        self.cmbTimelinePeriod.setCurrentIndex(period)
        self.edtTimelineCustomLength.setValue(customLength)
        self.chkFillRedDays.setChecked(fillRedDays)
        self.modelTimeTable.loadItems(personId, period, customLength)


    def getDateRange(self):
        return self.edtBegDate.date(), self.edtEndDate.date()


    def getPeriod(self):
        return self.cmbTimelinePeriod.currentIndex()


    def getCustomLength(self):
        return self.edtTimelineCustomLength.value()


    def getFillRedDays(self):
        return self.chkFillRedDays.isChecked()


    def getTemplates(self):
        return self.modelTimeTable.items()


    def removeExistingSchedules(self):
        return self.chkRemoveExistingSchedules.isChecked()


    def updateSchedulePeriod(self):
        period       = self.cmbTimelinePeriod.currentIndex()
        customLength = self.edtTimelineCustomLength.value()
        self.modelTimeTable.setPeriod(period, customLength)


    @pyqtSignature('int')
    def on_cmbTimelinePeriod_currentIndexChanged(self, index):
        enableCustomLength = index == 2
        self.lblTimelineCustomLength.setEnabled(enableCustomLength)
        self.edtTimelineCustomLength.setEnabled(enableCustomLength)
        self.updateSchedulePeriod()


    @pyqtSignature('int')
    def on_edtTimelineCustomLength_valueChanged(self, i):
        self.updateSchedulePeriod()
