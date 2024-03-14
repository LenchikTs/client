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
from PyQt4.QtCore import pyqtSignature, QString

from library.Utils       import forceDate, forceRef, forceString, toVariant, forceStringEx, forceBool, trim, formatName
from library.database    import CTableRecordCache
from Orgs.OrgComboBox    import CPolyclinicComboBox
from Orgs.Orgs           import selectOrganisation
from Events.Utils        import getEventvoucherCounterId, getEventCounterId, getEventName

from Events.Ui_EventVoucherPage   import Ui_EventVoucherPageWidget


class CEventVoucherPage(QtGui.QWidget, Ui_EventVoucherPageWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFocusProxy(self.cmbVoucherOrgs)
        self.eventEditor = None
        self.isSrcRegion = False
        self.cmbVoucherOrgs.setValue(QtGui.qApp.currentOrgId())
        self.cmbVoucherFinance.setTable('rbFinance', True)
        self.cmbDirectionCity.setAreaSelectable(True)
        self.cmbDirectionCity.setCode(QtGui.qApp.defaultKLADR())
        self.cmbDirectionRegion.setEnabled(True)
        self._voucherNumberIsChanged = False


    def protectFromEdit(self, isProtected):
        widgets = [ self.cmbVoucherOrgs,
                    self.btnSelectVoucherOrg,
                    self.cmbVoucherFinance,
                    self.edtVoucherSerial,
                    self.edtVoucherNumber,
                    self.edtVoucherBegDate,
                    self.edtVoucherEndDate,
                    self.cmbDirectionCity,
                    self.cmbDirectionRegion,
                    self.cmbDirectionOrgs,
                    self.btnSelectDirectionOrg,
                    self.cmbDirectionPerson,
                    self.edtDirectionNumber,
                    self.edtDirectionDate,
                    self.edtDirectionMKB
                 ]
        for widget in widgets:
            widget.setEnabled(not isProtected)


    def edtVoucherNumberEnabled(self, eventTypeId):
        result = self.edtVoucherNumber.isEnabled()
        result = result and forceBool(getEventvoucherCounterId(eventTypeId))
        if result:
            result = result and not forceBool(QtGui.qApp.db.translate('rbCounter', 'id', getEventCounterId(eventTypeId), 'sequenceFlag'))
            self.edtVoucherNumber.setEnabled(result)


    def setVoucher(self, record):
        self.cmbVoucherOrgs.setValue(forceRef(record.value('org_id')))
        self.cmbVoucherFinance.setValue(forceRef(record.value('finance_id')))
        self.edtVoucherSerial.setText(forceStringEx(record.value('serial')))
        self.edtVoucherNumber.setText(forceStringEx(record.value('number')))
        self.edtVoucherBegDate.setDate(forceDate(record.value('begDate')))
        self.edtVoucherEndDate.setDate(forceDate(record.value('endDate')))


    def setDirection(self, record):
        self.cmbDirectionCity.setCode(forceString(record.value('directionCity')))
        self.cmbDirectionRegion.setValue(forceString(record.value('directionRegion')))
        directionOrgId = forceRef(record.value('relegateOrg_id'))
        self.cmbDirectionOrgs.setValue(directionOrgId)
        self.cmbDirectionPerson.setOrganisationId(directionOrgId)
        self.edtDirectionNumber.setText(forceString(record.value('srcNumber')))
        self.edtDirectionDate.setDate(forceDate(record.value('srcDate')))
        self.cmbDirectionPerson.setValue(forceRef(record.value('relegatePerson_id')))
        self.edtDirectionMKB.setText(forceStringEx(record.value('directionMKB')))


    def setVoucherEx(self, voucherParams):
        directionOrgId = voucherParams.get('directionOrgId', None)
        directionPersonId = voucherParams.get('directionPersonId', None)
        directionInfo = voucherParams.get('directionInfo', [])
        self.cmbDirectionOrgs.setValue(directionOrgId)
        self.cmbDirectionPerson.setOrganisationId(directionOrgId)
        self.cmbDirectionPerson.setValue(directionPersonId)
        if directionInfo and len(directionInfo) > 2:
            self.edtDirectionNumber.setText(directionInfo[1])
            self.edtDirectionDate.setDate(directionInfo[2])
        self.edtDirectionMKB.setText(voucherParams.get('directionMKB', u''))
        self.cmbDirectionCity.setCode(voucherParams.get('directionCity', u''))
        self.cmbDirectionRegion.setValue(voucherParams.get('directionRegion', u''))
        self.edtVoucherSerial.setText(voucherParams.get('voucherSerial', u''))
        self.edtVoucherNumber.setText(voucherParams.get('voucherNumber', u''))
        self.edtVoucherBegDate.setDate(voucherParams.get('voucherBegDate', None))
        self.edtVoucherEndDate.setDate(voucherParams.get('voucherEndDate', None))


    def getVoucher(self, record, eventId):
        record.setValue('event_id', toVariant(eventId))
        record.setValue('org_id', toVariant(self.cmbVoucherOrgs.value()))
        record.setValue('finance_id', toVariant(self.cmbVoucherFinance.value()))
        record.setValue('serial', toVariant(self.edtVoucherSerial.text()))
        record.setValue('number', toVariant(self.edtVoucherNumber.text()))
        record.setValue('begDate', toVariant(self.edtVoucherBegDate.date()))
        record.setValue('endDate', toVariant(self.edtVoucherEndDate.date()))


    def getDirection(self, record):
        record.setValue('directionCity', toVariant(self.cmbDirectionCity.code()))
        record.setValue('directionRegion', toVariant(self.cmbDirectionRegion.value()))
        record.setValue('relegateOrg_id', toVariant(self.cmbDirectionOrgs.value()))
        record.setValue('relegatePerson_id', toVariant(self.cmbDirectionPerson.value()))
        record.setValue('srcNumber', toVariant(self.edtDirectionNumber.text()))
        record.setValue('srcDate', toVariant(self.edtDirectionDate.date()))
        record.setValue('directionMKB', toVariant(self.edtDirectionMKB.text()))


    def checkVoucherNumber(self, date, eventId, isControlVoucherNumber):
        if self._voucherNumberIsChanged or isControlVoucherNumber:
            voucherNumber = trim(self.edtVoucherNumber.text())
            voucherSerial = trim(self.edtVoucherSerial.text())
            if bool(voucherNumber):
                eventTypeId = self.eventEditor.eventTypeId
                sameVoucherNumberInfo = self.checkUniqueEventVoucherNumber(voucherNumber, eventTypeId, date, eventId, voucherSerial)
                return sameVoucherNumberInfo
        return []


    def checkUniqueEventVoucherNumber(self, voucherNumber, eventTypeId, date, eventId, voucherSerial=None):
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        tableEventVoucher = db.table('Event_Voucher')
        table = tableEvent.innerJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        table = table.innerJoin(tableEventVoucher, tableEventVoucher['event_id'].eq(tableEvent['id']))
        cond   = [tableEventVoucher['number'].eq(voucherNumber),
                  tableEvent['deleted'].eq(0),
                  tableEventVoucher['deleted'].eq(0)
                 ]
        if voucherSerial:
            cond.append(tableEventVoucher['serial'].eq(voucherSerial))
#        if eventTypeId:
#            cond.append(tableEventType['id'].eq(eventTypeId))
        if eventId:
            cond.append(tableEvent['id'].ne(eventId))
        fields = [tableEvent['id'].name(),
                  tableEvent['eventType_id'].name(),
                  tableEvent['setDate'].name(),
                  tableEvent['client_id'].name()
                  ]
        result = []
        recordList = db.getRecordList(table, fields, cond)
        for record in recordList:
            id = forceRef(record.value('id'))
            eventType = getEventName(forceRef(record.value('eventType_id')))
            setDate = forceString(record.value('setDate'))
            clientId = forceRef(record.value('client_id'))
            clientRecord = db.getRecord('Client', 'lastName, firstName, patrName', clientId)
            clientName = formatName(clientRecord.value('lastName'),
                                    clientRecord.value('firstName'),
                                    clientRecord.value('patrName'))
            resultValue = u'Событие(%s): %d от %s, пациент \'%s\'' %(eventType, id, setDate, clientName)
            result.append(resultValue)
        return result


    @pyqtSignature('QString')
    def on_edtVoucherNumber_textEdited(self, value):
        self._voucherNumberIsChanged = True


    @pyqtSignature('')
    def on_btnSelectVoucherOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbVoucherOrgs.value(), False, filter=CPolyclinicComboBox.filter)
        self.cmbVoucherOrgs.updateModel()
        if orgId:
            self.cmbVoucherOrgs.setValue(orgId)
            self.cmbDirectionPerson.setOrganisationId(orgId)


    @pyqtSignature('')
    def on_btnSelectDirectionOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbDirectionOrgs.value(), False, filter=CPolyclinicComboBox.filter)
        self.cmbDirectionOrgs.updateModel()
        if orgId:
            self.cmbDirectionOrgs.setValue(orgId)
            self.cmbDirectionPerson.setOrganisationId(orgId)


    @pyqtSignature('int')
    def on_cmbDirectionOrgs_currentIndexChanged(self, index):
        if not self.isSrcRegion:
            orgId = self.cmbDirectionOrgs.value()
            self.cmbDirectionPerson.setOrganisationId(orgId)
            okato = None
            record = self.organisationCache.get(orgId)
            if record:
                okato = forceStringEx(record.value('OKATO'))
                okato = QString(okato).left(5) if len(okato) > 5 else okato
            if self.cmbDirectionRegion.value() != okato:
                self.cmbDirectionRegion.setValue(okato)
        self.isSrcRegion = False


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor
        if self.eventEditor:
            self.cmbVoucherFinance.setValue(self.eventEditor.eventFinanceId)
        db = QtGui.qApp.db
        self.organisationCache = CTableRecordCache(db, db.forceTable('Organisation'), u'*', capacity=None)


    @pyqtSignature('int')
    def on_cmbDirectionCity_currentIndexChanged(self, index):
        code = self.cmbDirectionCity.code()
        self.cmbDirectionRegion.setKladrCode(code)


    @pyqtSignature('int')
    def on_cmbDirectionRegion_currentIndexChanged(self, index):
        orgId = self.cmbDirectionOrgs.value()
        okato = self.cmbDirectionRegion.value()
        filter = u'''Organisation.isMedical != 0'''
        if okato:
            filter += u''' AND Organisation.OKATO LIKE '%s%%' '''%(okato)
        if self.cmbDirectionOrgs.filter != filter:
            self.isSrcRegion = True
            self.cmbDirectionOrgs.setFilter(filter)
            self.isSrcRegion = True
            self.cmbDirectionOrgs.setValue(orgId)


    @pyqtSignature('QString')
    def on_edtDirectionMKB_textChanged(self, value):
        if value[-1:] == '.':
            value = value[:-1]
        diagName = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', value, 'DiagName'))
        if diagName:
            self.lblDirectionMKBText.setText(diagName)
        else:
            self.lblDirectionMKBText.clear()

