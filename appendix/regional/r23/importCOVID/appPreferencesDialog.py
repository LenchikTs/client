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

# редактор разных умолчаний
from PyQt4 import QtGui
from PyQt4.QtCore import QVariant, pyqtSignature

from KLADR.Utils import getProvinceKLADRCode
from Orgs.Orgs import selectOrganisation
from Ui_appPreferencesDialog import Ui_appPreferencesDialog
from library.Utils import forceRef, forceString, toVariant, forceInt


class CAppPreferencesDialog(QtGui.QDialog, Ui_appPreferencesDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)
        self.cmbProvince.setAreaSelectable(True)
        self.cmbContract.setTable('Contract',
                                  "concat_ws(' | ', (select rbFinance.name from rbFinance where rbFinance.id = Contract.finance_id), Contract.resolution, Contract.number)")
        self.cmbContract.setAddNone(True, u'не задано')
        self.cmbContract.setOrder('finance_id, resolution, number')
        self.cmbEventTypeAdult.setTable('EventType', True, 'deleted = 0 AND isActive = 1', needCache=False)
        self.cmbEventTypeChild.setTable('EventType', True, 'deleted = 0 AND isActive = 1', needCache=False)
        self.cmbResult.setTable('rbResult', True)
        self.cmbDiagnosticResult.setTable('rbDiagnosticResult', True)


    def setProps(self, props):
        self.cmbOrganisation.setValue(forceRef(props.get('orgId', QVariant())))
        self.cmbOrgStructure.setValue(forceRef(props.get('orgStructureId', QVariant())))
        self.cmbPerson.setValue(forceRef(props.get('personId', QVariant())))
        kladrCode = forceString(props.get('defaultKLADR', '2300000000000'))
        self.cmbDefaultCity.setCode(kladrCode)
        provinceKLADR = forceString(props.get('provinceKLADR', ''))
        self.cmbProvince.setCode(provinceKLADR or getProvinceKLADRCode(kladrCode))
        self.cmbContract.setValue(forceRef(props.get('contractId', QVariant())))
        self.cmbEventTypeAdult.setValue(forceRef(props.get('eventTypeId', QVariant())))
        self.cmbEventTypeChild.setValue(forceRef(props.get('eventTypeIdChild', QVariant())))
        self.cmbResult.setValue(forceRef(props.get('resultId', QVariant())))
        self.cmbDiagnosticResult.setValue(forceRef(props.get('diagnosticResultId', QVariant())))
        self.cmbEncoding.setCurrentIndex(forceInt(props.get('encoding', 0)))


    def props(self):
        result = {}
        result['orgId'] = toVariant(self.cmbOrganisation.value())
        result['orgStructureId'] = toVariant(self.cmbOrgStructure.value())
        result['personId'] = toVariant(self.cmbPerson.value())
        result['defaultKLADR'] = toVariant(self.cmbDefaultCity.code())
        result['provinceKLADR'] = toVariant(self.cmbProvince.code())
        result['contractId'] = toVariant(self.cmbContract.value())
        result['eventTypeId'] = toVariant(self.cmbEventTypeAdult.value())
        result['eventTypeIdChild'] = toVariant(self.cmbEventTypeChild.value())
        result['resultId'] = toVariant(self.cmbResult.value())
        result['diagnosticResultId'] = toVariant(self.cmbDiagnosticResult.value())
        result['encoding'] = toVariant(self.cmbEncoding.currentIndex())

        return result

    @pyqtSignature('int')
    def on_cmbOrganisation_currentIndexChanged(self, index):
        orgId = self.cmbOrganisation.value()
        self.cmbOrgStructure.setOrgId(orgId)

    @pyqtSignature('int')
    def on_cmbContract_currentIndexChanged(self, index):
        contractId = self.cmbContract.value()
        if contractId:
            self.cmbEventTypeAdult.setFilter('deleted = 0 AND isActive = 1 and id in (select cs.eventType_id from Contract_Specification cs where cs.deleted = 0 and cs.master_id = {0})'.format(contractId))
            self.cmbEventTypeChild.setFilter('deleted = 0 AND isActive = 1 and id in (select cs.eventType_id from Contract_Specification cs where cs.deleted = 0 and cs.master_id = {0})'.format(contractId))
        else:
            self.cmbEventTypeAdult.setFilter('deleted = 0 AND isActive = 1')
            self.cmbEventTypeChild.setFilter('deleted = 0 AND isActive = 1')

    @pyqtSignature('int')
    def on_cmbEventTypeAdult_currentIndexChanged(self, index):
        eventTypeId = self.cmbEventTypeAdult.value()
        if eventTypeId:
            self.cmbResult.setFilter('eventPurpose_id = (select purpose_id from EventType where id = {0})'.format(eventTypeId))
            self.cmbDiagnosticResult.setFilter('eventPurpose_id = (select purpose_id from EventType where id = {0})'.format(eventTypeId))
        else:
            self.cmbResult.setFilter('')
            self.cmbDiagnosticResult.setFilter('')

    @pyqtSignature('')
    def on_btnSelectOrganisation_clicked(self):
        orgId = selectOrganisation(self, self.cmbOrganisation.value(), False)
        self.cmbOrganisation.updateModel()
        if orgId:
            self.cmbOrganisation.setValue(orgId)

    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)

    @pyqtSignature('int')
    def on_cmbDefaultCity_currentIndexChanged(self):
        cityKLADRCode = self.cmbDefaultCity.code()
        provinceKLADRCode = getProvinceKLADRCode(cityKLADRCode)
        self.cmbProvince.setCode(provinceKLADRCode)
