# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate

from Events.Utils import getWorkEventTypeFilter

from Ui_ReportBIRADSSetup import Ui_ReportBIRADSSetupDialog


class CReportBIRADSSetupDialog(QtGui.QDialog, Ui_ReportBIRADSSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbActionType.setAllSelectable(True)
        self.cmbOrganisation.setValue(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.setOrganisationVisible(True)
        self.setOrgStructureVisible(True)
        self.setPersonVisible(True)
        self.setActionTypeVisible(True)
        self.setEventTypeVisible(True)
        self.chkClientDetail.setVisible(True)


    def setOrganisationVisible(self, value):
        self.lblOrganisation.setVisible(value)
        self.cmbOrganisation.setVisible(value)


    def setOrgStructureVisible(self, value):
        self.lblOrgStructure.setVisible(value)
        self.cmbOrgStructure.setVisible(value)


    def setPersonVisible(self, value):
        self.lblPerson.setVisible(value)
        self.cmbPerson.setVisible(value)


    def setActionTypeVisible(self, value):
        self.lblActionType.setVisible(value)
        self.cmbActionType.setVisible(value)


    def setEventTypeVisible(self, value):
        self.lblEventType.setVisible(value)
        self.cmbEventType.setVisible(value)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbActionType.setValue(params.get('actionTypeId', None))
        self.cmbOrganisation.setValue(params.get('organisationId', None))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.chkClientDetail.setChecked(params.get('isClientDetail', False))
        self.cmbEventType.setValue(params.get('eventTypeId', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['actionTypeId'] = self.cmbActionType.value()
        result['personId'] = self.cmbPerson.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['organisationId'] = self.cmbOrganisation.value()
        result['isClientDetail'] = self.chkClientDetail.isChecked()
        result['eventTypeId'] = self.cmbEventType.value()
        return result


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


    @pyqtSignature('int')
    def on_cmbOrganisation_currentIndexChanged(self, index):
        organisationId = self.cmbOrganisation.value()
        self.cmbOrgStructure.setOrgId(organisationId if organisationId else QtGui.qApp.currentOrgId())
        self.cmbPerson.setOrganisationId(organisationId if organisationId else QtGui.qApp.currentOrgId())

