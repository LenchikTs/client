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
from PyQt4.QtCore import QDate, QDateTime, QString

from library.Utils      import agreeNumberAndWord, forceBool, forceDouble, forceInt, forceRef, forceString, formatList, formatSex

from Events.Utils       import CPayStatus
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureFullName, getPersonInfo
from Reports.Report     import CReport, getContractName, getEventTypeName

from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr

from MUOMSOFTable1      import CMUOMSOFSetupDialog

def selectData(params, currentYearDate=QDate()):
    begDate = currentYearDate if currentYearDate else params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    eventPurposeId = params.get('eventPurposeId', None)
    eventTypeId = params.get('eventTypeId', None)
    orgStructureId = params.get('orgStructureId', None)
    specialityId = params.get('specialityId', None)
    personId = params.get('personId', None)
    contractIdList = params.get('contractIdList', None)
    insurerId = params.get('insurerId', None)
    sex = params.get('sex', 0)
    ageFrom = params.get('ageFrom', 0)
    ageTo = params.get('ageTo', 150)
    setMembershipIndex = params.get('setMembershipIndex', 0)
    financeId = params.get('financeId', None)
    stmt="""
SELECT
    Event.id as eventId,
    Event.client_id AS clientId,
    (SELECT SUM(A.amount)
    FROM Action AS A
    INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
    WHERE A.event_id = Event.id
    AND AT.flatCode LIKE 'moving%%' AND A.deleted = 0
    GROUP BY A.event_id) AS hospitalHelp,

    rbMedicalAidType.code AS medicalAidTypeCode,
    rbMedicalAidKind.code AS medicalAidKindCode,
    SUM(Account_Item.`amount`) AS `amount`,
    SUM(Account_Item.`sum`) AS `sum`,
    SUM(Account_Item.`uet`) AS `uet`,
    IF(rbEventProfile.code = 5, 1, 0) AS eventProfileCode,
    (SELECT COUNT(*)
     FROM Visit LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
     WHERE Visit.event_id = Event.id
       AND DATE(Event.setDate) <= DATE(Visit.date)
       AND rbVisitType.regionalCode != 3
    ) AS visitCount,

    (SELECT COUNT(*)
     FROM Visit LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
     WHERE Visit.event_id = Event.id
       AND rbVisitType.regionalCode = 8
       AND DATE(Event.setDate) <= DATE(Visit.date)
    ) AS visitCountCode8,

    (SELECT COUNT(*)
     FROM Visit LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
     WHERE Visit.event_id = Event.id
       AND rbVisitType.regionalCode = 1
       AND DATE(Event.setDate) <= DATE(Visit.date)
    ) AS visitCountCode1,

    (SELECT COUNT(*)
     FROM Visit LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
     WHERE Visit.event_id = Event.id
       AND rbVisitType.regionalCode = 10
       AND DATE(Event.setDate) <= DATE(Visit.date)
    ) AS visitCountCode10,

    (SELECT COUNT(Event_CSG.amount)
     FROM Event_CSG
     WHERE Event_CSG.master_id = Event.id AND EventType.regionalCode = '30190'
     AND Event_CSG.payStatus = (%d & (3 << (2*rbFinance.code)))
     ) AS diseaseCSG,

    (SELECT COUNT(Event_CSG.amount)
     FROM Event_CSG
     WHERE Event_CSG.master_id = Event.id AND EventType.regionalCode = '305'
     AND Event_CSG.payStatus = (%d & (3 << (2*rbFinance.code)))
     ) AS emergencyCSG,

    (SELECT COUNT(Event_CSG.amount)
     FROM Event_CSG
     WHERE Event_CSG.master_id = Event.id AND EventType.regionalCode = '30191'
     AND Event_CSG.payStatus = (%d & (3 << (2*rbFinance.code)))
     ) AS preventiveCSG
FROM
    Event
    INNER JOIN EventType              ON EventType.id = Event.eventType_id
    INNER JOIN Client                 ON Client.id = Event.client_id
    INNER JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.execPerson_id
    INNER JOIN rbMedicalAidType        ON rbMedicalAidType.id = EventType.medicalAidType_id
    INNER JOIN rbMedicalAidKind        ON rbMedicalAidKind.id = EventType.medicalAidKind_id
    LEFT JOIN ClientPolicy             ON ClientPolicy.id = getClientPolicyId(Client.id, 1)
    LEFT JOIN rbEventProfile           ON rbEventProfile.id = EventType.eventProfile_id
    LEFT JOIN Account_Item ON Account_Item.event_id = Event.id
    LEFT JOIN Account      ON Account.id = Account_Item.master_id
    LEFT JOIN Contract     ON Contract.id = Account.contract_id
    LEFT JOIN Organisation ON Organisation.id = Contract.payer_id
    LEFT JOIN rbFinance ON rbFinance.id = Contract.finance_id
WHERE Event.deleted = 0
    AND Account_Item.reexposeItem_id IS NULL AND Account_Item.deleted = 0
    AND IF(Contract.id IS NOT NULL, Contract.deleted = 0, 1)
    AND %s
    GROUP BY Event.id
    ORDER BY Event.id, Event.client_id
"""
    db = QtGui.qApp.db
    tableEvent  = db.table('Event')
    tableClient = db.table('Client')
    tablePerson = db.table('vrbPersonWithSpeciality')
    tableAccount = db.table('Account')
    tableContract = db.table('Contract')
    tableOrganisation = db.table('Organisation')
    tableClientPolicy = db.table('ClientPolicy')
    cond = []
    cond.append(tableEvent['execDate'].ge(begDate))
    cond.append(db.joinOr([tableEvent['execDate'].lt(endDate.addDays(1)), tableEvent['execDate'].isNull()]))
    if setMembershipIndex:
        cond.append(tableOrganisation['deleted'].eq(0))
        cond.append(tableOrganisation['infisCode'].like('29%%'))
    else:
        cond.append(u'''EXISTS(SELECT kladr.KLADR.CODE
        FROM ClientAddress
        INNER JOIN Address ON ClientAddress.address_id = Address.id
        INNER JOIN AddressHouse ON Address.house_id = AddressHouse.id
        INNER JOIN kladr.KLADR ON kladr.KLADR.CODE = AddressHouse.KLADRCode
        WHERE Client.id IS NOT NULL AND ClientAddress.client_id = Client.id AND kladr.KLADR.CODE NOT LIKE '29%%'
        AND Address.deleted = 0 AND AddressHouse.deleted = 0
        LIMIT 1)''')
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        cond.append(db.table('EventType')['purpose_id'].eq(eventPurposeId))
    if personId:
        cond.append(tableEvent['execPerson_id'].eq(personId))
    elif orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if financeId:
        cond.append(tableContract['deleted'].eq(0))
        cond.append(tableContract['finance_id'].eq(financeId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if contractIdList:
        cond.append(tableAccount['contract_id'].inlist(contractIdList))
    if insurerId:
        cond.append(tableClientPolicy['insurer_id'].eq(insurerId))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Event.setDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Event.setDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    return db.query(stmt % (CPayStatus.exposedBits, CPayStatus.exposedBits, CPayStatus.exposedBits, db.joinAnd(cond)))

MainRows = [
    (u'Первичная медико-санитарная помощь', u'10',u'х'),
    (u'в том числе: амбулаторная помощь', u'11',u'посещений, единиц'),
    (u'с профилактической целью',u'11.1',u'посещений, единиц'),
    (u'неотложная помощь', u'11.2',u'посещений, единиц'),
    (u'посещений, единиц', u'11.3',u'посещений, единиц'),
    (u'стоматологическая', u'12',u'обращения в связи с заболеваниями СТГ'),
    (u'', u'', u'неотложная помощь СТГ'),
    (u'', u'', u'с профилактической целью СТГ'),
    (u'помощь, оказанная в условиях дневных стационаров всех типов', u'13', u'(пролеченных больных)'),
    (u'стационарная помощь', u'14',u'койко-дней, единиц'),
    (u'', u'', u'(пролеченных больных)'),
    (u'Специализированная медицинская помощь', u'15',u'х'),
    (u'в том числе: амбулаторная помощь', u'16',u'посещений, единиц'),
    (u'с профилактической целью', u'16.1',u'посещений, единиц'),
    (u'неотложная помощь', u'16.2',u'посещений, единиц'),
    (u'обращения в связи с заболеваниями', u'16.3',u'посещений, единиц'),
    (u'стоматологическая',u'17', u'УЕТ, единиц'),
    (u'', u'', u'(посещений)'),
    (u' помощь, оказанная в условиях дневных стационаров всех типов', u'18',u'пациенто-дней, единиц'),
    (u'стационарная помощь', u'19',u'(пролеченных больных)'),
    (u'Скорая медицинская помощь', u'20',u'число вызовов, единиц')
]


class CMUOMSOFForeign(CReport):
    name = u'Раздел III. Сведения об оказанной медицинской помощи лицам, застрахованным на территории других субъектов Российской Федерации'
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(self.name)
        self.currentKladrCode = 29


    def getSetupDialog(self, parent):
        result = CMUOMSOFSetupDialog(parent)
        result.setTitle(self.title())
        result.setFinanceVisible(True)
        result.setSetMembershipVisible(True)
        return result


    def build(self, params):
        begDateParams = params.get('begDate', QDate())
        rowSize = 6
        lenRows = len(MainRows)
        reportData = [ [0]*rowSize for row in xrange(lenRows) ]
        prevClientId = False
        clientRows = set([])
        prevEventId = False
        eventRows = set([])

        query = selectData(params)
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            clientId = forceRef(record.value('clientId'))
            medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
            medicalAidKindCode = QString(forceString(record.value('medicalAidKindCode'))).left(1)
            twoMedicalAidKindCode = QString(forceString(record.value('medicalAidKindCode'))).left(2)
            visitCount = forceInt(record.value('visitCount'))
            visitCount1 = forceInt(record.value('visitCountCode1'))
            visitCount10 = forceInt(record.value('visitCountCode10'))
            visitCount8 = forceInt(record.value('visitCountCode8'))
            sum = forceDouble(record.value('sum'))
            uet = forceDouble(record.value('uet'))
            eventProfileCode = forceBool(record.value('eventProfileCode'))
            hospitalHelp = forceInt(record.value('hospitalHelp'))
            diseaseCSG = forceInt(record.value('diseaseCSG'))
            emergencyCSG = forceInt(record.value('emergencyCSG'))
            preventiveCSG = forceInt(record.value('preventiveCSG'))

            if prevClientId != clientId:
                prevClientId = clientId
                clientRows = set([])

            if prevEventId != eventId:
                prevEventId = eventId
                eventRows = set([])

            if eventProfileCode:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[5]
                    reportLine[0] += diseaseCSG
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[5] = reportLine

                    reportLine = reportData[6]
                    reportLine[0] += emergencyCSG
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[6] = reportLine

                    reportLine = reportData[7]
                    reportLine[0] += preventiveCSG
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[7] = reportLine

                if medicalAidKindCode == u'3':
                    reportLine = reportData[16]
                    reportLine[0] += uet
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[16] = reportLine

                    reportLine = reportData[17]
                    reportLine[0] += visitCount
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[17] = reportLine

            if visitCount1 and medicalAidTypeCode == 6 and not eventProfileCode:
                if medicalAidKindCode == u'1' and twoMedicalAidKindCode != u'12':
                    reportLine = reportData[4]
                    reportLine[0] += visitCount1
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[4] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[15]
                    reportLine[0] += visitCount1
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[15] = reportLine

            if visitCount8 and medicalAidTypeCode == 6 and not eventProfileCode:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[2]
                    reportLine[0] += visitCount8
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[2] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[13]
                    reportLine[0] += visitCount8
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[13] = reportLine

            if twoMedicalAidKindCode == u'12' and medicalAidTypeCode == 6 and not eventProfileCode:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[3]
                    reportLine[0] += visitCount
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[3] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[14]
                    reportLine[0] += visitCount
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[14] = reportLine

            if visitCount10 and medicalAidTypeCode == 7:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[8]
                    reportLine[0] += visitCount10
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[8] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[18]
                    reportLine[0] += visitCount10
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[18] = reportLine

            if medicalAidKindCode == u'2' or medicalAidTypeCode == 4:
                reportLine = reportData[20]
                if eventId not in eventRows:
                    eventRows.add(eventId)
                    reportLine[0] += 1
                if clientId not in clientRows:
                    clientRows.add(clientId)
                    reportLine[2] += 1
                reportLine[4] += sum
                reportData[20] = reportLine

            if medicalAidTypeCode == 1:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[9]
                    reportLine[0] += hospitalHelp
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[9] = reportLine

                    reportLine = reportData[10]
                    reportLine[0] += 1
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[10] = reportLine

                if medicalAidKindCode == u'3':
                    reportLine = reportData[19]
                    reportLine[0] += hospitalHelp
                    reportLine[2] += 1
                    reportLine[4] += sum
                    reportData[19] = reportLine

        currentYearDate = QDate(begDateParams.year(), 1, 1)
        query = selectData(params, currentYearDate)
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            clientId = forceRef(record.value('clientId'))
            medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
            medicalAidKindCode = QString(forceString(record.value('medicalAidKindCode'))).left(1)
            twoMedicalAidKindCode = QString(forceString(record.value('medicalAidKindCode'))).left(2)
            visitCount = forceInt(record.value('visitCount'))
            visitCount1 = forceInt(record.value('visitCountCode1'))
            visitCount10 = forceInt(record.value('visitCountCode10'))
            visitCount8 = forceInt(record.value('visitCountCode8'))
            sum = forceDouble(record.value('sum'))
            uet = forceDouble(record.value('uet'))
            eventProfileCode = forceBool(record.value('eventProfileCode'))
            hospitalHelp = forceInt(record.value('hospitalHelp'))
            diseaseCSG = forceInt(record.value('diseaseCSG'))
            emergencyCSG = forceInt(record.value('emergencyCSG'))
            preventiveCSG = forceInt(record.value('preventiveCSG'))

            if prevClientId != clientId:
                prevClientId = clientId
                clientRows = set([])

            if prevEventId != eventId:
                prevEventId = eventId
                eventRows = set([])

            if eventProfileCode:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[5]
                    reportLine[1] += diseaseCSG
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[5] = reportLine

                    reportLine = reportData[6]
                    reportLine[1] += emergencyCSG
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[6] = reportLine

                    reportLine = reportData[7]
                    reportLine[1] += preventiveCSG
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[7] = reportLine

                if medicalAidKindCode == u'3':
                    reportLine = reportData[16]
                    reportLine[1] += uet
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[16] = reportLine

                    reportLine = reportData[17]
                    reportLine[1] += visitCount
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[17] = reportLine

            if visitCount1 and medicalAidTypeCode == 6 and not eventProfileCode:
                if medicalAidKindCode == u'1' and twoMedicalAidKindCode != u'12':
                    reportLine = reportData[4]
                    reportLine[1] += visitCount1
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[4] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[15]
                    reportLine[1] += visitCount1
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[15] = reportLine

            if visitCount8 and medicalAidTypeCode == 6 and not eventProfileCode:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[2]
                    reportLine[1] += visitCount8
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[2] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[13]
                    reportLine[1] += visitCount8
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[13] = reportLine

            if twoMedicalAidKindCode == u'12' and medicalAidTypeCode == 6 and not eventProfileCode:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[3]
                    reportLine[1] += visitCount
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[3] = reportLine
                if medicalAidKindCode == u'3':
                    reportLine = reportData[14]
                    reportLine[1] += visitCount
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[14] = reportLine

            if visitCount10 and medicalAidTypeCode == 7:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[8]
                    reportLine[1] += visitCount10
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[8] = reportLine

                if medicalAidKindCode == u'3':
                    reportLine = reportData[18]
                    reportLine[1] += visitCount10
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[18] = reportLine

            if medicalAidKindCode == u'2' or medicalAidTypeCode == 4:
                reportLine = reportData[20]
                if eventId not in eventRows:
                    eventRows.add(eventId)
                    reportLine[1] += 1
                if clientId not in clientRows:
                    clientRows.add(clientId)
                    reportLine[3] += 1
                reportLine[5] += sum
                reportData[20] = reportLine

            elif medicalAidTypeCode == 1:
                if medicalAidKindCode == u'1':
                    reportLine = reportData[9]
                    reportLine[1] += hospitalHelp
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[9] = reportLine

                    reportLine = reportData[10]
                    reportLine[1] += 1
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[10] = reportLine

                if medicalAidKindCode == u'3':
                    reportLine = reportData[19]
                    reportLine[1] += hospitalHelp
                    reportLine[3] += 1
                    reportLine[5] += sum
                    reportData[19] = reportLine

        reportLineTotal11 = [0]*rowSize
        for row in [2, 3, 4]:
            reportLine = reportData[row]
            reportLineTotal11[0] += reportLine[0]
            reportLineTotal11[1] += reportLine[1]
            reportLineTotal11[2] += reportLine[2]
            reportLineTotal11[3] += reportLine[3]
            reportLineTotal11[4] += reportLine[4]
            reportLineTotal11[5] += reportLine[5]
        reportData[1] = reportLineTotal11

        reportLineTotal16 = [0]*rowSize
        for row in [13, 14, 15]:
            reportLine = reportData[row]
            reportLineTotal16[0] += reportLine[0]
            reportLineTotal16[1] += reportLine[1]
            reportLineTotal16[2] += reportLine[2]
            reportLineTotal16[3] += reportLine[3]
            reportLineTotal16[4] += reportLine[4]
            reportLineTotal16[5] += reportLine[5]
        reportData[12] = reportLineTotal16

        reportLineTotal10 = [0]*rowSize
        for row in [1, 7, 8, 10]:
            reportLine = reportData[row]
            reportLineTotal10[0] += reportLine[0]
            reportLineTotal10[1] += reportLine[1]
            reportLineTotal10[2] += reportLine[2]
            reportLineTotal10[3] += reportLine[3]
            reportLineTotal10[4] += reportLine[4]
            reportLineTotal10[5] += reportLine[5]
        reportData[0] = reportLineTotal10

        reportLineTotal15 = [0]*rowSize
        for row in [13, 17, 18]:
            reportLine = reportData[row]
            reportLineTotal15[0] += reportLine[0]
            reportLineTotal15[1] += reportLine[1]
            reportLineTotal15[2] += reportLine[2]
            reportLineTotal15[3] += reportLine[3]
            reportLineTotal15[4] += reportLine[4]
            reportLineTotal15[5] += reportLine[5]
        reportData[11] = reportLineTotal15

        reportLineTotal = [0]*rowSize
        for row in [0, 11, 20]:
            reportLine = reportData[row]
            reportLineTotal[0] += reportLine[0]
            reportLineTotal[1] += reportLine[1]
            reportLineTotal[2] += reportLine[2]
            reportLineTotal[3] += reportLine[3]
            reportLineTotal[4] += reportLine[4]
            reportLineTotal[5] += reportLine[5]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.name)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'Раздел III. Сведения об оказанной лицам, застрахованным на территории других субъектов Российской Федерации,  медицинской помощи')
        cursor.insertBlock()

        tableColumns = [
            ('12%',[u'', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ строки', u'', u'2'], CReportBase.AlignCenter),
            ('7%', [u'единица измерения объема медицинской помощи ', u'', u'3'], CReportBase.AlignCenter),
            ('13%', [u'Объем медицинской помощи', u'за отчетный месяц', u'4'], CReportBase.AlignRight),
            ('13%', [u'', u'с начала года', u'5'], CReportBase.AlignRight),
            ('13%', [u'Численность лиц, получивших медицинскую помощь, человек', u'за отчетный месяц', u'6'], CReportBase.AlignRight),
            ('13%', [u'', u'с начала года', u'7'], CReportBase.AlignRight),
            ('13%', [u'Стоимость оказанной медицинской помощи, руб.', u'за отчетный месяц', u'8'], CReportBase.AlignRight),
            ('13%', [u'', u'с начала года', u'9'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(0, 5, 1, 2)
        table.mergeCells(0, 7, 1, 2)

        for row, Rows in enumerate(MainRows):
            reportLine = reportData[row]
            i = table.addRow()
            if i not in [3, 4, 14, 15]:
                table.setText(i, 0, Rows[0])
                table.setText(i, 1, Rows[1])
                table.setText(i, 2, Rows[2])
                table.setText(i, 3, reportLine[0])
                table.setText(i, 4, reportLine[1])
                table.setText(i, 5, reportLine[2])
                table.setText(i, 6, reportLine[3])
                table.setText(i, 7, '%.2f'%(reportLine[4]))
                table.setText(i, 8, '%.2f'%(reportLine[5]))

        table.setText(3, 0, MainRows[0][0])
        table.setText(3, 1, MainRows[0][1])
        table.setText(3, 2, MainRows[0][2])
        table.setText(3, 3, u'х')
        table.setText(3, 4, u'х')
        table.setText(3, 5, u'х')
        table.setText(3, 6, u'х')
        table.setText(3, 7, '%.2f'%(reportLineTotal10[4]))
        table.setText(3, 8, '%.2f'%(reportLineTotal10[5]))

        table.setText(4, 0, MainRows[1][0])
        table.setText(4, 1, MainRows[1][1])
        table.setText(4, 2, MainRows[1][2])
        table.setText(4, 3, reportLineTotal11[0])
        table.setText(4, 4, reportLineTotal11[1])
        table.setText(4, 5, reportLineTotal11[2])
        table.setText(4, 6, reportLineTotal11[3])
        table.setText(4, 7, '%.2f'%(reportLineTotal11[4]))
        table.setText(4, 8, '%.2f'%(reportLineTotal11[5]))

        table.setText(14, 0, MainRows[11][0])
        table.setText(14, 1, MainRows[11][1])
        table.setText(14, 2, MainRows[11][2])
        table.setText(14, 3, u'х')
        table.setText(14, 4, u'х')
        table.setText(14, 5, reportLineTotal15[2])
        table.setText(14, 6, reportLineTotal15[3])
        table.setText(14, 7, '%.2f'%(reportLineTotal15[4]))
        table.setText(14, 8, '%.2f'%(reportLineTotal15[5]))

        table.setText(15, 0, MainRows[12][0])
        table.setText(15, 1, MainRows[12][1])
        table.setText(15, 2, MainRows[12][2])
        table.setText(15, 3, reportLineTotal16[0])
        table.setText(15, 4, reportLineTotal16[1])
        table.setText(15, 5, reportLineTotal16[2])
        table.setText(15, 6, reportLineTotal16[3])
        table.setText(15, 7, '%.2f'%(reportLineTotal16[4]))
        table.setText(15, 8, '%.2f'%(reportLineTotal16[5]))

        i = table.addRow()
        table.setText(i, 0, u'Итого')
        table.setText(i, 3, reportLineTotal[0])
        table.setText(i, 4, reportLineTotal[1])
        table.setText(i, 5, reportLineTotal[2])
        table.setText(i, 6, reportLineTotal[3])
        table.setText(i, 7, '%.2f'%(reportLineTotal[4]))
        table.setText(i, 8, '%.2f'%(reportLineTotal[5]))

        table.mergeCells(8, 0, 3, 1)
        table.mergeCells(8, 1, 3, 1)
        table.mergeCells(12, 0, 2, 1)
        table.mergeCells(12, 1, 2, 1)
        table.mergeCells(19, 0, 2, 1)
        table.mergeCells(19, 1, 2, 1)
        return doc


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', None)
        ageTo = params.get('ageTo', None)
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        specialityId = params.get('specialityId', None)
        personId = params.get('personId', None)
        typeFinanceId = params.get('financeId', None)
        contractIdList = params.get('contractIdList', None)
        insurerId = params.get('insurerId', None)
        setMembershipIndex = params.get('setMembershipIndex', 0)
        rows = []
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if eventPurposeId:
            rows.append(u'Цель обращения: ' + forceString(db.translate('rbEventTypePurpose', 'id', eventPurposeId, 'name')))
        if eventTypeId:
            rows.append(u'тип обращения: ' + getEventTypeName(eventTypeId))
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        if specialityId:
            rows.append(u'специальность: ' + forceString(db.translate('rbSpeciality', 'id', specialityId, 'name')))
        if personId:
            personInfo = getPersonInfo(personId)
            rows.append(u'врач: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        if sex:
            rows.append(u'пол: ' + formatSex(sex))
        if ageFrom is not None and ageTo is not None and ageFrom <= ageTo:
            rows.append(u'возраст: c %d по %d %s' % (ageFrom, ageTo, agreeNumberAndWord(ageTo, (u'год', u'года', u'лет'))))
        if contractIdList:
            if len(contractIdList) == 1:
               rows.append(u'по договору № ' + getContractName(contractIdList[0]))
            else:
               rows.append(u'по договорам №№ ' + formatList([getContractName(contractId) for contractId in contractIdList]))
        if typeFinanceId is not None:
            rows.append(u'тип финансирования: '+ forceString(db.translate('rbFinance', 'id', typeFinanceId, 'name')))
        if insurerId:
            rows.append(u'СМО: ' + forceString(db.translate('Organisation', 'id', insurerId, 'shortName')))
        rows.append(u'принадлежность к городу: ' + [u'По адресу пациента', u'По плательщику в договоре'][setMembershipIndex])
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


