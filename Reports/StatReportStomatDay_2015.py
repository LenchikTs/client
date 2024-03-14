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
from PyQt4.QtCore import QDate

from library.database          import addDateInRange
from library.Utils             import forceDate, forceDouble, forceInt, forceRef, forceString, formatShortNameInt

from Events.Action             import CAction
from Orgs.Utils                import getOrgStructurePersonIdList
from Registry.RegistryTable    import codeIsPrimary
from Registry.Utils            import formatAddressInt, getAddress, getClientAddress
from Reports.ReportBase        import CReportBase
from Reports.Report            import CReport, CReportEx
from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.Utils             import dateRangeAsStr


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    personId = params.get('personId', None)

    stmt= u"""
        SELECT
            Event.id                  AS `eventId`,
            rbResult.name             AS `eventResult`,
            Event.client_id           AS `clientId`,
            Client.lastName,
            Client.firstName,
            Client.patrName,
            Client.birthDate,
            Event.execDate            AS `date`,
            Event.isPrimary           AS `isPrimary`,
            Diagnosis.MKB             AS `MKB`,
            ActionType.flatCode       AS actionFlatCode,
            Action.id                 AS `actionId`,
            Account_Item.service_id   AS `serviceId`,
            rbService.code            AS `serviceCode`,
            Account_Item.amount       AS `amount`,
            Account_Item.uet          AS `uet`,
            Account_Item.sum          AS `sum`
        FROM
            Event
            INNER JOIN EventType  ON EventType.id = Event.eventType_id
            INNER JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            INNER JOIN Client     ON Client.id = Event.client_id
            LEFT  JOIN Contract   ON Contract.id = Event.contract_id
            LEFT  JOIN Diagnosis  ON Diagnosis.id = getEventDiagnosis(Event.id)
            LEFT  JOIN Action     ON Action.event_id = Event.id AND Action.deleted = 0
            LEFT  JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT  JOIN Account    ON Account.contract_id = Event.contract_id AND Account.deleted=0
            LEFT  JOIN Account_Item ON     Account_Item.master_id = Account.id
                                       AND Account_Item.deleted=0
                                       AND Account_Item.event_id=Event.id
                                       AND Account_Item.action_id = Action.id
                                       AND Account_Item.reexposeItem_id IS NULL
                                       AND Account_Item.refuseType_id IS NULL
            LEFT  JOIN rbService  ON rbService.id = Account_Item.service_id
            LEFT  JOIN rbResult   ON rbResult.id = Event.result_id
        WHERE
            Event.deleted = 0
            AND rbMedicalAidType.code = '9'
            AND %s
        ORDER BY Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.id,
                 Event.execDate, Event.id,
                 rbService.code
    """
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    cond = []
    addDateInRange(cond, tableEvent['execDate'], begDate, endDate)
    if orgStructureId:
        persons = getOrgStructurePersonIdList(orgStructureId)
        cond.append(tableEvent['execPerson_id'].inlist(persons))
    if personId:
        cond.append(tableEvent['execPerson_id'].eq(personId))
    return db.query(stmt % (db.joinAnd(cond)))
#            AND ActionType.flatCode IN('dentitionInspection', 'parodentInsp')


class CStomatDayReport_2015(CReportEx): #actStomatReportDay_2015
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по работе врача-стоматолога')
        self.table_columns = [
            ('5%',  [u'№ п/п',                                    u'1'], CReportBase.AlignRight),
            ('16%', [u'ФИО пациента, дата рождения, номер карты', u'2'], CReportBase.AlignLeft),
            ('16%', [u'Адрес',                                    u'3'], CReportBase.AlignLeft),
            ('5%',  [u'Первичный',                                u'4'], CReportBase.AlignRight),
            ('5%',  [u'Дата посещения',                           u'5'], CReportBase.AlignRight),
            ('5%',  [u'№ наряда',                                 u'6'], CReportBase.AlignRight),
            ('5%',  [u'Признак зуба',                             u'7'], CReportBase.AlignLeft),
            ('5%',  [u'код по МКБ',                               u'8'], CReportBase.AlignRight),
            ('16%', [u'Код услуги',                               u'9'], CReportBase.AlignLeft),
            ('5%',  [u'Кол-во',                                   u'10'], CReportBase.AlignRight),
            ('5%',  [u'УЕТ',                                      u'11'], CReportBase.AlignRight),
            ('5%',  [u'Сумма, руб.',                              u'12'], CReportBase.AlignRight),
            ('7%',  [u'Исход',                                    u'13'], CReportBase.AlignLeft),
            ]

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setPersonVisible(True)
        result.setFinanceVisible(False)
        result.setSpecialityVisible(False)
        result.setInsurerVisible(False)
        result.setStageVisible(False)
        result.setPayPeriodVisible(False)

        # заменяем подходящий комбобокс:
        result.setWorkTypeVisible(True)
        result.lblWorkType.setText(u'Адрес: ')
        result.cmbAddressType = result.cmbWorkType
        result.cmbAddressType.setMaxCount(0)
        result.cmbAddressType.setMaxCount(2)
        result.cmbAddressType.addItem(u'регистрации')
        result.cmbAddressType.addItem(u'проживания')
        result.params = lambda : dict(CReportSetupDialog.params(result).items() + [('addressType', result.cmbWorkType.currentIndex())])

        result.setOwnershipVisible(False)
        result.setWorkOrganisationVisible(False)
        result.setSexVisible(False)
        result.setAgeVisible(False)
        result.setActionTypeVisible(False)
        result.setMKBFilterVisible(False)
        result.setEventTypeVisible(False)
        result.lblEventType.hide()
        result.cmbEventType.hide()
        result.chkOnlyPermanentAttach.hide()
        result.chkDetailPerson.hide()
        return result


    def getPeriodName(self, params):
        begDate = params.get('begDate', QDate.currentDate())
        endDate = params.get('endDate', QDate.currentDate())
        return dateRangeAsStr(u'за период', begDate, endDate)


    def _getClientNameEtc(self, record):
        lastName = forceString(record.value('lastName'))
        firstName = forceString(record.value('firstName'))
        patrName = forceString(record.value('patrName'))
        birthDate = forceDate(record.value('birthDate'))
        clientId  = forceRef(record.value('clientId'))
        shortName = formatShortNameInt(lastName, firstName, patrName)
        return u'%s, %s, %s' % (shortName,  forceString(birthDate), clientId)


    def _getClientAddress(self, addressType, record):
        clientId  = forceRef(record.value('clientId'))
        addressRecord = getClientAddress(clientId, addressType)
        if addressRecord:
            addressInfo = getAddress(addressRecord.value('address_id'), addressRecord.value('freeInput'))
            return formatAddressInt(addressInfo)
        else:
            return '-'


    def _getToothSet(self, actionId):
        result = set()
        action = CAction.getActionById(actionId)
        propertiesByName = action.getPropertiesByName()
        for name in propertiesByName:
            if action[name]:
                nameParts = name.split(u'.')
                if len(nameParts) == 3:
                    if nameParts[0] not in (u'Низ', u'Верх') and nameParts[2]:
                        if nameParts[1] == u'Верхний':
                            result.add(action[u'Верх.%s.%s' %(nameParts[1],nameParts[2])])
                        elif nameParts[1] == u'Нижний':
                            result.add(action[u'Низ.%s.%s' %(nameParts[1],nameParts[2])])
        return result


    def getReportData(self, query, addressType):
        reportData = []
#        colCount = 13

        prevEventId = None
        while query.next():
            record = query.record()
            eventId     = forceRef(record.value('eventId'))
            actionFlatCode = forceString(record.value('actionFlatCode'))
            actionId    = forceRef(record.value('actionId'))
            serviceCode = forceString(record.value('serviceCode'))
            amount      = forceDouble(record.value('amount'))
            uet         = forceDouble(record.value('uet'))
            sum         = forceDouble(record.value('sum'))

            if prevEventId != eventId:
                date        = forceDate(record.value('date'))
                isPrimary   = forceInt(record.value('isPrimary'))
                MKB         = forceString(record.value('MKB'))
                eventResult = forceString(record.value('eventResult'))

                reportLine = [ self._getClientNameEtc(record),              # 0
                               self._getClientAddress(addressType, record), # 1
                               codeIsPrimary[isPrimary] if 0<=isPrimary<len(codeIsPrimary[isPrimary]) else unicode(isPrimary), # 2
                               forceString(date),                           # 3
                               '',
                               set(),                                       # 5
                               MKB,                                         # 6
                               [],                                          # 7
                               '',                                          # 8
                               '',                                          # 9
                               '',                                          # 10
                               eventResult,                                 # 11
                               '',                                          # 12
                             ]
                reportData.append(reportLine)
                prevEventId = eventId

            if actionFlatCode in ('dentitionInspection', 'parodentInsp'):
                reportLine[5] |= set(self._getToothSet(actionId))

            if serviceCode:
                reportLine[7].append((serviceCode, amount, uet, sum))
        return reportData


    def buildInt(self, params, cursor):
        addressType = params.get('addressType', 0)
        query = selectData(params)
        reportData = self.getReportData(query, addressType)
        reportDataTotal = [0]*3
        table = self.createTable(cursor)
        for reportRow, reportLine in enumerate(reportData):
            reportLineTotal = [0]*3
            row = table.addRow()
            lastRow = row
            table.setText(row, 0, reportRow+1)
            reportLine[5] = ','.join(sorted(reportLine[5]))
            for i in (0, 1, 2, 3, 4, 5, 6, 11):
               table.setText(row, i+1, reportLine[i])
            for subRow, subLine in enumerate(reportLine[7]):
                if lastRow<row+subRow:
                    lastRow = table.addRow()
                table.setText(row+subRow, 8, subLine[0])
                table.setText(row+subRow, 9, subLine[1])
                table.setText(row+subRow,10, subLine[2])
                table.setText(row+subRow,11, '%.2f'%subLine[3])
                for i in xrange(3):
                    reportLineTotal[i] += subLine[i+1]
                    reportDataTotal[i] += subLine[i+1]
            lastRow = table.addRow()
            table.setText(lastRow, 1, u'Итого:')
            table.mergeCells(lastRow, 1, 1, 8)
            table.setText(lastRow, 9, reportLineTotal[0])
            table.setText(lastRow,10, reportLineTotal[1])
            table.setText(lastRow,11, '%.2f'%reportLineTotal[2])

            table.mergeCells(row, 0, lastRow-row+1, 1)
            table.mergeCells(row, 1, lastRow-row, 1)
            table.mergeCells(row, 2, lastRow-row, 1)
            table.mergeCells(row, 3, lastRow-row, 1)
            table.mergeCells(row, 4, lastRow-row, 1)
            table.mergeCells(row, 5, lastRow-row, 1)
            table.mergeCells(row, 6, lastRow-row, 1)
            table.mergeCells(row, 7, lastRow-row, 1)
            table.mergeCells(row, 12, lastRow-row, 1)

        if len(reportData) > 0:
            row = table.addRow()
            table.setText(row, 1, u'Итого:')
            table.mergeCells(row, 0, 1, 3)
            table.setText(row, 3, len(reportData))
            table.setText(row, 9, reportDataTotal[0])
            table.setText(row,10, reportDataTotal[1])
            table.setText(row,11, '%.2f'%reportDataTotal[2])

