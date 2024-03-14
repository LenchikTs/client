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

from library.Utils      import forceBool, forceInt, forceString
from library.database   import addDateInRange
from Orgs.Utils         import getOrgStructureDescendants
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from ReportAcuteInfections import CReportAcuteInfectionsSetupDialog


def selectData(useInputDate, begInputDate, endInputDate, registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, MKBList, accountAccomp, locality,  params):
    stmt=u"""
SELECT
   COUNT(*) AS cnt,
   MKB,
   clientAge,
   clientSex,
   isWorkingPolicy,
   isPregnancy,
   isWorking,
   isHospital,
   isDeath
   FROM (
SELECT
    Diagnosis.MKB AS MKB,
    age(Client.birthDate, Diagnosis.setDate) AS clientAge,
    Client.sex AS clientSex,
    (rbPolicyType.code = '2') AS isWorkingPolicy,
    ClientWork.id AS isWorking,
EXISTS(SELECT A.id
    FROM Event AS E
    INNER JOIN Action AS A ON A.event_id=E.id
    INNER JOIN ActionType AS AT ON AT.id=A.actionType_id
    INNER JOIN Diagnostic AS Dtic ON Dtic.event_id = E.id
    INNER JOIN Diagnosis AS Dsis ON Dtic.diagnosis_id = Dsis.id
    WHERE Dtic.deleted = 0 AND Dsis.deleted = 0 AND E.deleted = 0
        AND AT.deleted = 0 AND A.deleted = 0
        AND (AT.flatCode LIKE 'moving%%' OR AT.flatCode LIKE 'leaved%%')) AS isHospital,
(Client.sex = 2 AND
    EXISTS(SELECT Diagnostic.id
           FROM  Diagnostic
           JOIN  Event ON Event.id = Diagnostic.event_id
           WHERE Diagnostic.diagnosis_id = Diagnosis.id
             AND Diagnostic.deleted = 0
             AND Event.deleted = 0
             AND Event.pregnancyWeek>0)) AS isPregnancy,
EXISTS(SELECT APS.id
    FROM Event AS E
    INNER JOIN Action AS A ON A.event_id=E.id
    INNER JOIN ActionType AS AT ON AT.id=A.actionType_id
    INNER JOIN ActionProperty AS AP ON AP.action_id=A.id
    INNER JOIN ActionPropertyType AS APT ON AP.type_id=APT.id
    INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
    INNER JOIN Diagnostic AS Dic ON Dic.event_id = E.id
    INNER JOIN Diagnosis AS Dis ON Dic.diagnosis_id = Dis.id
    WHERE Dic.deleted = 0 AND Dis.deleted = 0
    AND E.deleted = 0 AND A.deleted = 0 AND AT.deleted = 0
    AND AP.action_id=A.id AND APT.actionType_id=A.actionType_id
    AND APT.deleted=0 AND AP.deleted=0 AND APT.name = 'Исход госпитализации' AND (APS.value = 'умер%%' OR APS.value = 'смерть%%')) AS isDeath
FROM %s
WHERE %s
) AS T
GROUP BY MKB, clientAge, clientSex, isWorkingPolicy, isWorking, isHospital, isDeath
ORDER BY MKB
    """ # вырезал в главном селекте isWorking и во втором ClientWork.id AS isWorking и isWorking из GROUP BY
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableDiagnosisType = db.table('rbDiagnosisType')
    tableClientPolicy = db.table('ClientPolicy')
    tablePolicyType = db.table('rbPolicyType')
    tableClientAddress = db.table('ClientAddress')
    tableClientWork = db.table('ClientWork')
    tableAddress = db.table('Address')
    tableAddressHouse = db.table('AddressHouse')
    queryTable = tableDiagnosis.leftJoin(tableClient, tableDiagnosis['client_id'].eq(tableClient['id']))
    queryTable = queryTable.leftJoin(tableDiagnosisType, tableDiagnosis['diagnosisType_id'].eq(tableDiagnosisType['id']))
    queryTable = queryTable.leftJoin(tableClientPolicy, '`ClientPolicy`.`id` = getClientPolicyId(`Client`.`id`,1)')
    queryTable = queryTable.leftJoin(tableClientWork, '`ClientWork`.`id` = getClientWorkId(`Client`.`id`)')
    queryTable = queryTable.leftJoin(tablePolicyType, tableClientPolicy['policyType_id'].eq(tablePolicyType['id']))

    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableDiagnosis['mod_id'].isNull())

#    workCond = [tableClientWork['deleted'].eq(0), tableClientWork['deleted'].isNull()]
#    cond.append(db.joinOr(workCond))
    addDateInRange(cond, tableDiagnosis['setDate'], begDate, endDate)
#    cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), tableDiagnosis['setDate'].le(endDate)]))
#    cond.append(tableDiagnosis['endDate'].ge(begDate))

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [ tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                       tableDiagnostic['deleted'].eq(0)
                     ]
    if registeredInPeriod:
        addDateInRange(diagnosticCond, tableDiagnostic['setDate'], begDate, endDate)
    if useInputDate:
        tableEvent  = db.table('Event')
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['client_id'].eq(tableClient['id']))
        cond.append(tableEvent['deleted'].eq(0))
        addDateInRange(cond, tableEvent['createDatetime'], begInputDate, endInputDate)
    isPersonPost = params.get('isPersonPost', 0)
    if isPersonPost:
        tableRBPost = db.table('rbPost')
        diagnosticQuery = diagnosticQuery.innerJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticQuery = diagnosticQuery.innerJoin(tableRBPost, tableRBPost['id'].eq(tablePerson['post_id']))
        diagnosticCond.append(tablePerson['deleted'].eq(0))
        if isPersonPost == 1:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureId:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if eventTypeId:
        tableEvent = db.table('Event')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticCond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        diagnosticCond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    cond.append(db.existsStmt(diagnosticQuery, diagnosticCond))

    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Diagnosis.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if socStatusTypeId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                  +'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                  +'ClientSocStatus.socStatusType_id=%d' % socStatusTypeId)
        cond.append('EXISTS('+subStmt+')')
    elif socStatusClassId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                  +'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                  +'ClientSocStatus.socStatusClass_id=%d' % socStatusClassId)
        cond.append('EXISTS('+subStmt+')')
    MKBCond = []
    for MKB in MKBList:
        MKBCond.append( tableDiagnosis['MKB'].like(MKB+'%') )
    cond.append(db.joinOr(MKBCond))
    if not accountAccomp:
        cond.append(tableDiagnosisType['code'].inlist(['1', '2', '4']))
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality-1))
    filterAddress = params.get('isFilterAddress', False)
    if filterAddress:
        filterAddressType = params.get('filterAddressType', 0)
        filterAddressCity = params.get('filterAddressCity', None)
        filterAddressStreet = params.get('filterAddressStreet', None)
        filterAddressHouse = params.get('filterAddressHouse', u'')
        filterAddressCorpus = params.get('filterAddressCorpus', u'')
        filterAddressFlat = params.get('filterAddressFlat', u'')
        queryTable = queryTable.leftJoin(tableClientAddress, tableClient['id'].eq(tableClientAddress['client_id']))
        cond.append(tableClientAddress['type'].eq(filterAddressType))
        cond.append(db.joinOr([tableClientAddress['id'].isNull(), tableClientAddress['deleted'].eq(0)]))
        if filterAddressCity or filterAddressStreet or filterAddressHouse or filterAddressCorpus or filterAddressFlat:
            queryTable = queryTable.leftJoin(tableAddress, tableClientAddress['address_id'].eq(tableAddress['id']))
            queryTable = queryTable.leftJoin(tableAddressHouse, tableAddress['house_id'].eq(tableAddressHouse['id']))
            cond.append(db.joinOr([tableAddress['id'].isNull(), tableAddress['deleted'].eq(0)]))
            cond.append(db.joinOr([tableAddressHouse['id'].isNull(), tableAddressHouse['deleted'].eq(0)]))
        if filterAddressCity:
            cond.append(tableAddressHouse['KLADRCode'].like(filterAddressCity))
        if filterAddressStreet:
            cond.append(tableAddressHouse['KLADRStreetCode'].like(filterAddressStreet))
        if filterAddressHouse:
            cond.append(tableAddressHouse['number'].eq(filterAddressHouse))
        if filterAddressCorpus:
            cond.append(tableAddressHouse['corpus'].eq(filterAddressCorpus))
        if filterAddressFlat:
            cond.append(tableAddress['flat'].eq(filterAddressFlat))
    stmt = stmt % (db.getTableName(queryTable), db.joinAnd(cond))
    return db.query(stmt)


def produceTotalLine(table, title, total):
    i = table.addRow()
    table.setText(i, 0, title, CReportBase.TableTotal)
    for j in xrange(len(total)):
            table.setText(i, j+1, total[j], CReportBase.TableTotal)


class CReportDailyAcuteInfectionsHospital(CReport):
    rowTypes = [ (u'J10', u'Грипп, вызванный идентифицированным вирусом гриппа' ),
                 (u'J11', u'Грипп, вирус не идентифицирован' ),
                 (u'J03', u'Ангины'),
                 (u'J06', u'ОРВИ'  ),
                 (u'J18', u'Пневмония'),
                 (u'J20', u'Бронхит'),
                 (u'U07', u'Коронавирусная инфекция'),
                 (u'O99.5', u'Болезни органов дыхания, осложняющие беременность, деторождение и послеродовой период'),
               ]

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Ежедневный отчёт по выявленным острым инфекционным заболеваниям с госпитализацией')


    def getSetupDialog(self, parent):
        result = CReportAcuteInfectionsSetupDialog(parent)
        result.setAccountAccompEnabled(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        useInputDate = bool(params.get('useInputDate', False))
        begInputDate = params.get('begInputDate', QDate())
        endInputDate = params.get('endInputDate', QDate())
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        accountAccomp = params.get('accountAccomp', False)
        locality = params.get('locality', 0)
        reportRowSize = 23
        mapMKBToTypeIndex = {}
        for index, rowType in enumerate(self.rowTypes):
            mapMKBToTypeIndex[rowType[0]] = index
        reportData = {}
        MKBList = []
        query = selectData(useInputDate, begInputDate, endInputDate, registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, [t[0] for t in self.rowTypes], accountAccomp, locality, params)
        while query.next():
            record    = query.record()
            cnt       = forceInt(record.value('cnt'))
            MKB       = forceString(record.value('MKB')).upper()
            age       = forceInt(record.value('clientAge'))
            sex       = forceInt(record.value('clientSex'))
            isWorking = forceBool(record.value('isWorking'))
            isWorkingPolicy = forceBool(record.value('isWorkingPolicy'))
            isHospital = forceBool(record.value('isHospital'))
            isDeath    = forceBool(record.value('isDeath'))
            reportRow = reportData.get(MKB, None)
            if not reportRow:
                reportRow = [0]*reportRowSize
                reportData[MKB] = reportRow
                MKBList.append(MKB)
            if age<3:
                cols = [0, 1, 2]
                if isWorking or isWorkingPolicy:
                    cols += [3]
                else:
                    cols += [4]
            elif age<7:
                cols = [0, 1, 5]
                if isWorking or isWorkingPolicy:
                    cols += [6]
                else:
                    cols += [7]
            elif age<15:
                cols = [0, 1, 8]
                if isWorking or isWorkingPolicy:
                    cols += [9]
                else:
                    cols += [10]
            elif age<18:
                cols = [0, 1, 11]
                if isWorking or isWorkingPolicy:
                    cols += [12]
                else:
                    cols += [13]
            else:
                cols = [0, 14]
            if age >= 18:
                if isHospital:
                    if age >= 18 and age < 30:
                        cols += [15]
                    elif age >= 30 and age < 50:
                        cols += [16]
                    elif age >= 50:
                        cols += [17]
                    cols += [18]
                if isDeath:
                    if age >= 18 and age < 30:
                        cols += [19]
                    elif age >= 30 and age < 50:
                        cols += [20]
                    elif age >= 50:
                        cols += [21]
                    cols += [22]
            for col in cols:
                reportRow[col] += cnt
#            if sex in (1, 2):
#                reportRow[ageGroup*2+sex-1] += cnt
#                reportRow[5+sex] += cnt
#                reportRow[8] += cnt
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ('8%', [u'диагноз'], CReportBase.AlignLeft),
            ( '4%', [u'всего'  ], CReportBase.AlignRight),
            ( '4%', [u'дети (0-17 лет)',     u'всего'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'в т.ч.', u'0-2 года', u'всего'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'3-6 года', u'всего'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'7-14 лет', u'всего'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'подростки\n(15-17 лет)', u'всего'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4%', [u'взрослые (18 лет и старше)', u'всего', u'',   u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'число госпитализированных', u'18-30 лет', u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'30-50 лет',                 u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'старше 51 года',            u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'всего госпита-\nлизиро-\nванных', u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'число умерших', u'18-30 лет',      u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'30-50 лет',                 u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'старше 51 года',            u''], CReportBase.AlignRight),
            ( '4%', [u'',                    u'',   u'всего умерших',             u''], CReportBase.AlignRight),
            ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1) # ДЗ
        table.mergeCells(0, 1, 4, 1) # всего
        table.mergeCells(0, 2, 1, 13)
        table.mergeCells(1, 2, 3, 1)
        table.mergeCells(2, 3, 1, 3)
        table.mergeCells(1, 3, 1, 12)
        table.mergeCells(2, 6, 1, 3)
        table.mergeCells(2, 9, 1, 3)
        table.mergeCells(2, 12, 1, 3)
        table.mergeCells(0, 15, 1, 9)
        table.mergeCells(1, 15, 3, 1)
        table.mergeCells(1, 16, 1, 4)
        table.mergeCells(2, 16, 2, 1)
        table.mergeCells(2, 17, 2, 1)
        table.mergeCells(2, 18, 2, 1)
        table.mergeCells(2, 19, 2, 1)
        table.mergeCells(1, 20, 1, 4)
        table.mergeCells(2, 20, 2, 1)
        table.mergeCells(2, 21, 2, 1)
        table.mergeCells(2, 22, 2, 1)
        table.mergeCells(2, 23, 2, 1)

        prevTypeIndex = None
        total = [0]*reportRowSize
        for MKB in MKBList:
            typeIndex = mapMKBToTypeIndex[MKB[:3] if MKB != u'O99.5' else MKB]
            if typeIndex != prevTypeIndex:
                if prevTypeIndex is not None:
                    produceTotalLine(table, u'всего', total)
                i = table.addRow()
                table.mergeCells(i, 0, 1, reportRowSize+1)
                table.setText(i, 0, self.rowTypes[typeIndex][1])
                prevTypeIndex = typeIndex
                total = [0]*reportRowSize
            row = reportData[MKB]
            i = table.addRow()
            table.setText(i, 0, MKB)
            for j in xrange(reportRowSize):
                table.setText(i, j+1, row[j])
                total[j] += row[j]
        if prevTypeIndex is not None:
            produceTotalLine(table, u'всего', total)
        return doc



class CReportDailyAcuteInfections(CReport):
    rowTypes = [ (u'J10', u'Грипп, вызванный идентифицированным вирусом гриппа' ),
                 (u'J11', u'Грипп, вирус не идентифицирован' ),
                 (u'J03', u'Ангины'),
                 (u'J06', u'ОРВИ'  ),
                 (u'J18', u'Пневмония'),
                 (u'J20', u'Бронхит'),
                 (u'U07', u'Коронавирусная инфекция'),
                 (u'O99.5', u'Болезни органов дыхания, осложняющие беременность, деторождение и послеродовой период'),
               ]

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Ежедневный отчёт по выявленным острым инфекционным заболеваниям')


    def getSetupDialog(self, parent):
        result = CReportAcuteInfectionsSetupDialog(parent)
        result.setAccountAccompEnabled(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        useInputDate = bool(params.get('useInputDate', False))
        begInputDate = params.get('begInputDate', QDate())
        endInputDate = params.get('endInputDate', QDate())
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        accountAccomp = params.get('accountAccomp', False)
        locality = params.get('locality', 0)
        reportRowSize = 19
        mapMKBToTypeIndex = {}
        for index, rowType in enumerate(self.rowTypes):
            mapMKBToTypeIndex[rowType[0]] = index
        reportData = {}
        MKBList = []
        query = selectData(useInputDate, begInputDate, endInputDate, registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, [t[0] for t in self.rowTypes], accountAccomp, locality, params)
        while query.next():
            record    = query.record()
            cnt       = forceInt(record.value('cnt'))
            MKB       = forceString(record.value('MKB')).upper()
            age       = forceInt(record.value('clientAge'))
            sex       = forceInt(record.value('clientSex'))
            isWorking = forceBool(record.value('isWorking'))
            isWorkingPolicy = forceBool(record.value('isWorkingPolicy'))
            isPregnancy = forceBool(record.value('isPregnancy'))
            reportRow = reportData.get(MKB, None)
            if not reportRow:
                reportRow = [0]*reportRowSize
                reportData[MKB] = reportRow
                MKBList.append(MKB)
            if age<3:
                cols = [0, 1, 2]
                if isWorking or isWorkingPolicy:
                    cols += [3]
                else:
                    cols += [4]
            elif age<7:
                cols = [0, 1, 5]
                if isWorking or isWorkingPolicy:
                    cols += [6]
                else:
                    cols += [7]
            elif age<15:
                cols = [0, 1, 8]
                if isWorking or isWorkingPolicy:
                    cols += [9]
                else:
                    cols += [10]
            elif age<18:
                cols = [0, 1, 11]
                if isWorking or isWorkingPolicy:
                    cols += [12]
                else:
                    cols += [13]
            elif age<65:
                cols = [0, 14]
            else:
                cols = [0, 14, 15]
            if age>=18:
                if isWorking or isWorkingPolicy:
                    cols += [16]
                else:
                    cols += [17]
                if isPregnancy:
                    cols += [18]
            for col in cols:
                reportRow[col] += cnt

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ('10%', [u'диагноз'], CReportBase.AlignLeft),
            ( '4.8%', [u'всего'  ], CReportBase.AlignRight),
            ( '4.8%', [u'дети (0-17 лет)',     u'всего'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'в т.ч.', u'0-2 года', u'всего'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'3-6 года', u'всего'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'7-14 лет', u'всего'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'подростки\n(15-17 лет)', u'всего'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',    u'не орга-\nнизованные'], CReportBase.AlignRight),
            ( '4.8%', [u'взрослые (18 лет и старше)', u'всего', u'',   u''], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'в т.ч.', u'', u'65 лет и старше'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',     u'рабо-\nтающие'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',     u'не рабо-\nтающие'], CReportBase.AlignRight),
            ( '4.8%', [u'',                    u'',   u'',     u'бере-\nмен-\nные'], CReportBase.AlignRight),
            ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0,  4,  1) # ДЗ
        table.mergeCells(0, 1,  4,  1) # всего
        table.mergeCells(0, 2,  1, 13)
        table.mergeCells(1, 2,  3,  1)
        table.mergeCells(2, 3,  1,  3)
        table.mergeCells(1, 3,  1, 12)
        table.mergeCells(2, 6,  1,  3)
        table.mergeCells(2, 9,  1,  3)
        table.mergeCells(2, 12, 1,  3)
        table.mergeCells(0, 15, 1,  5)
        table.mergeCells(1, 15, 3,  1)
        table.mergeCells(1, 16, 1,  4)
        table.mergeCells(2, 16, 2,  1)
        table.mergeCells(2, 17, 2,  1)
        table.mergeCells(2, 18, 2,  1)
        table.mergeCells(2, 19, 2,  1)
        prevTypeIndex = None
        total = [0]*reportRowSize
        for MKB in MKBList:
            typeIndex = mapMKBToTypeIndex[MKB[:3] if MKB != u'O99.5' else MKB]
            if typeIndex != prevTypeIndex:
                if prevTypeIndex is not None:
                    produceTotalLine(table, u'всего', total)
                i = table.addRow()
                table.mergeCells(i, 0, 1, reportRowSize+1)
                table.setText(i, 0, self.rowTypes[typeIndex][1])
                prevTypeIndex = typeIndex
                total = [0]*reportRowSize
            row = reportData[MKB]
            i = table.addRow()
            table.setText(i, 0, MKB)
            for j in xrange(reportRowSize):
                table.setText(i, j+1, row[j])
                total[j] += row[j]
        if prevTypeIndex is not None:
            produceTotalLine(table, u'всего', total)
        return doc
