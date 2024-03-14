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

from library.Utils import forceBool, forceInt

from library.DialogBase import CDialogBase

from Resources.OrgStructureJobs import COrgStructureJobsModel

from Resources.Ui_JobTemplateDialog import Ui_TemplateDialog


class CJobTemplateDialog(CDialogBase, Ui_TemplateDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('Jobs', COrgStructureJobsModel(self))
        self.setupUi(self)
        self.setModels(self.tblJobs, self.modelJobs, self.selectionModelJobs)
        self.tblJobs.horizontalHeader().moveSection(7, 1)


    def setDateRange(self, begDate, endDate):
        self.edtBegDate.setDate(begDate)
        self.edtEndDate.setDate(endDate)


    def setOrgStructureId(self, orgStructureId):
        db = QtGui.qApp.db
        record = db.getRecord('OrgStructure',
                              ('timelinePeriod', 'timelineCustomLength', 'fillRedDays'),
                              orgStructureId
                              )
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
        self.modelJobs.loadItems(orgStructureId, period, customLength)


    def getDateRange(self):
        return self.edtBegDate.date(), self.edtEndDate.date()


    def getPeriod(self):
        return self.cmbTimelinePeriod.currentIndex()


    def getCustomLength(self):
        return self.edtTimelineCustomLength.value()


    def getFillRedDays(self):
        return self.chkFillRedDays.isChecked()


    def getTemplates(self):
        return self.modelJobs.items()


    def removeExistingJobs(self):
        return self.chkRemoveExistingJobs.isChecked()


    def updatePeriod(self):
        period       = self.cmbTimelinePeriod.currentIndex()
        customLength = self.edtTimelineCustomLength.value()
        self.modelJobs.setPeriod(period, customLength)


    @pyqtSignature('int')
    def on_cmbTimelinePeriod_currentIndexChanged(self, index):
        enableCustomLength = index == 2
        self.lblTimelineCustomLength.setEnabled(enableCustomLength)
        self.edtTimelineCustomLength.setEnabled(enableCustomLength)
        self.updatePeriod()


    @pyqtSignature('int')
    def on_edtTimelineCustomLength_valueChanged(self, i):
        self.updatePeriod()
