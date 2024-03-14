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

from library.database   import addDateInRange
from library.MapCode    import createMapCodeToRowIdx
from library.Utils      import forceBool, forceInt, forceString

from Reports.Report     import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportAcuteInfections import CReportAcuteInfectionsSetupDialog, getFilterAddress
from Reports.Utils      import getKladrClientRural
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureListDescendants, getOrgStructures


MainRows_2000 = [([u'Сифилис все формы, всего', u'в том числе: мужчины', u'женщины'],            [u'', u'м', u'ж'], [u'01', u'02', u'03'], u'A50-A53'),
                 ([u'в том числе: врожденный сифилис', u''],                                     [u'м', u'ж'],      [u'04', u'05'],        u'A50.0-A50.9'),
                 ([u'в том числе: сифилис ранний врожденный с симптомами', u''],                 [u'м', u'ж'],      [u'06', u'07'],        u'A50.0'),
                 ([u'сифилис ранний врожденный скрытый', u''],                                   [u'м', u'ж'],      [u'08', u'09'],        u'A50.1'),
                 ([u'сифилис поздний врожденный', u''],                                          [u'м', u'ж'],      [u'10', u'11'],        u'A50.3-A50.6'),
                 ([u'сифилис врожденный  неуточненный', u''],                                    [u'м', u'ж'],      [u'12', u'13'],        u'A50.2, A50.7, A50.9'),
                 ([u'ранний сифилис', u''],                                                      [u'м', u'ж'],      [u'14', u'15'],        u'A51.0-A51.9'),
                 ([u'из них: первичный сифилис', u''],                                           [u'м', u'ж'],      [u'16', u'17'],        u'A51.0-A51.2'),
                 ([u'вторичный сифилис', u''],                                                   [u'м', u'ж'],      [u'18', u'19'],        u'A51.3-A51.4'),
                 ([u'из них: сифилис кожи и  слизистых оболочек', u''],                          [u'м', u'ж'],      [u'20', u'21'],        u'A51.3'),
                 ([u'другие формы вторичного сифилиса', u''],                                    [u'м', u'ж'],      [u'22', u'23'],        u'A51.4'),
                 ([u'из них-ранний  нейросифилис', u''],                                         [u'м', u'ж'],      [u'24', u'25'],        u'A51.4'),
                 ([u'сифилис ранний скрытый', u''],                                              [u'м', u'ж'],      [u'26', u'27'],        u'A51.5'),
                 ([u'сифилис ранний неуточненный', u''],                                         [u'м', u'ж'],      [u'28', u'29'],        u'A51.9'),
                 ([u'поздний сифилис', u''],                                                     [u'м', u'ж'],      [u'30', u'31'],        u'A52.0-A52.9'),
                 ([u'из них: сифилис сердечно-сосудистой системы', u''],                         [u'м', u'ж'],      [u'32', u'33'],        u'A52.0'),
                 ([u'поздний нейросифилис', u''],                                                [u'м', u'ж'],      [u'34', u'35'],        u'A52.1-A52.3'),
                 ([u'другие симптомы позднего сифилиса', u''],                                   [u'м', u'ж'],      [u'36', u'37'],        u'A52.7'),
                 ([u'сифилис поздний скрытый', u''],                                             [u'м', u'ж'],      [u'38', u'39'],        u'A52.8'),
                 ([u'сифилис поздний неуточненный', u''],                                        [u'м', u'ж'],      [u'40', u'41'],        u'A52.9'),
                 ([u'другие и неуточненные формы сифилиса', u''],                                [u'м', u'ж'],      [u'42', u'43'],        u'A53.0,A53.9'),
                 ([u'из них: скрытый, неуточненный как ранний или поздний сифилис', u''],        [u'м', u'ж'],      [u'44', u'45'],        u'A53.0'),
                 ([u'сифилис неуточненный', u''],                                                [u'м', u'ж'],      [u'46', u'47'],        u'A53.9'),
                 ([u'Гонококковая инфекция, всего', u'в том числе: мужчины', u'женщины'],        [u'', u'м', u'ж'], [u'48', u'49', u'50'], u'A54.0-A54.9'),
                 ([u'в том числе:  осложненная', u''],                                           [u'м', u'ж'],      [u'51', u'52'],        u'A54.1-A54.2,A54.8-A54.9'),
                 ([u'гонококковая инфекция глаз', u''],                                          [u'м', u'ж'],      [u'53', u'54'],        u'A54.3'),
                 ([u'Трихомоноз, всего', u'в том числе: мужчины', u'женщины'],                   [u'', u'м', u'ж'], [u'55', u'56', u'57'], u'A59.0,A59.8,A59.9'),
                 ([u'Хламидийные  инфекции, всего, всего', u'в том числе: мужчины', u'женщины'], [u'', u'м', u'ж'], [u'58', u'59', u'60'], u'A56.0-A56.4,A56.8'),
                 ([u'Аногенитальная герпетическая вирусная инфекция, всего, всего', u'в том числе: мужчины', u'женщины'], [u'', u'м', u'ж'], [u'61', u'61', u'63'], u'A60.0,A60.1,A60.9'),
                 ([u'Аногенитальные (венерические)   бородавки, всего', u'в том числе: мужчины', u'женщины'],             [u'', u'м', u'ж'], [u'64', u'65', u'66'], u'A63.0'),
           ]


def selectData(params):
    begDate            = params.get('begDate', QDate())
    endDate            = params.get('endDate', QDate())
    eventPurposeId     = params.get('eventPurposeId', None)
    eventTypeIdList    = params.get('eventTypeList', None)
    orgStructureIdList = params.get('orgStructureList', None)
    personId           = params.get('personId', None)
    sex                = params.get('sex', 0)
    ageFrom            = params.get('ageFrom', 0)
    ageTo              = params.get('ageTo', 150)
    socStatusClassId   = params.get('socStatusClassId', None)
    socStatusTypeId    = params.get('socStatusTypeId', None)
    areaIdEnabled      = params.get('areaIdEnabled', None)
    areaId             = params.get('areaId', None)
    locality           = params.get('locality', 0)

    stmt="""
SELECT
   Diagnosis.MKB AS MKB,
   COUNT(DISTINCT Client.id) AS sickCount,
   Client.sex,
   age(Client.birthDate, IF(Diagnosis.setDate IS NOT NULL, Diagnosis.setDate, Diagnosis.endDate)) AS clientAge,
   (%s) AS clientRural

FROM Diagnosis
INNER JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE Diagnosis.diagnosisType_id NOT IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT WHERE RBDT.code = '7' OR RBDT.code = '11')
AND %s
GROUP BY MKB, sex, clientAge, clientRural
    """
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableEvent = db.table('Event')
    tableOrgStructureAddress = db.table('OrgStructure_Address')
    tableAddress = db.table('Address')

    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableDiagnosis['mod_id'].isNull())
    cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), tableDiagnosis['setDate'].lt(endDate.addDays(1))]))
    cond.append(db.joinOr([tableDiagnosis['endDate'].ge(begDate), tableDiseaseCharacter['code'].eq('3')]))

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [ tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                       tableDiagnostic['deleted'].eq(0)
                     ]

    addDateInRange(diagnosticCond, tableDiagnostic['setDate'], begDate, endDate)
    isPersonPost = params.get('isPersonPost', 0)
    if isPersonPost:
        tableRBPost = db.table('rbPost')
        diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableRBPost, tableRBPost['id'].eq(tablePerson['post_id']))
        diagnosticCond.append(tablePerson['deleted'].eq(0))
        if isPersonPost == 1:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureIdList:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))
    else:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticCond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if eventTypeIdList:
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticCond.append(tableEvent['eventType_id'].inlist(eventTypeIdList))
    elif eventPurposeId:
        tableEventType = db.table('EventType')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        diagnosticCond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    cond.append(db.existsStmt(diagnosticQuery, diagnosticCond))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%(ageFrom))
        cond.append('Diagnosis.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR), 1)'%(ageTo))
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
    if areaIdEnabled:
        stmtAddress = u'''INNER JOIN ClientAddress ON ClientAddress.client_id = Diagnosis.client_id
                        AND ClientAddress.id = (SELECT MAX(id) FROM ClientAddress AS CA WHERE CA.Type=1 and CA.client_id = Diagnosis.client_id)
INNER JOIN Address ON Address.id = ClientAddress.address_id'''
        if areaId:
            orgStructureIdListArea = getOrgStructureDescendants(areaId)
        else:
            orgStructureIdListArea = getOrgStructures(QtGui.qApp.currentOrgId())
        subCond = [ tableOrgStructureAddress['master_id'].inlist(orgStructureIdListArea),
                    tableOrgStructureAddress['house_id'].eq(tableAddress['house_id']),
                  ]
        cond.append(db.existsStmt(tableOrgStructureAddress, subCond))
    else:
        stmtAddress = u''''''
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality-1))
    filterAddress = params.get('isFilterAddress', False)
    if filterAddress:
        if not stmtAddress:
            stmtAddress = u'''INNER JOIN ClientAddress ON ClientAddress.client_id = Client.id
                              INNER JOIN Address ON Address.id = ClientAddress.address_id
                              INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        else:
            stmtAddress += u'''INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        cond.append('ClientAddress.id IN (%s)'%(getFilterAddress(params)))
    return db.query(stmt % (getKladrClientRural(),
                            stmtAddress,
                            db.joinAnd(cond)))


class CStatReportF9_2000(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'СВЕДЕНИЯ О ЗАБОЛЕВАНИЯХ ИНФЕКЦИЯМИ, ПЕРЕДАВАЕМЫМИ ПОЛОВЫМ ПУТЕМ. (Ф9)')


    def getSetupDialog(self, parent):
        result = CReportAcuteInfectionsSetupDialog(parent)
        result.setMKBFilterEnabled(False)
        result.setRegisteredInPeriod(False)
        result.setAccountAccompEnabled(True)
        result.setOnlyFirstTimeEnabled(False)
        result.setNotNullTraumaTypeEnabled(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx( [row[3] for row in MainRows_2000] )
        rowSize = 11
        reportMainData = []
        for rowDescr in MainRows_2000:
            reportLines = []
            for n in rowDescr[2]:
                reportLines.append([0]*rowSize)
            reportMainData.append(reportLines)
        query = selectData(params)
        while query.next():
            record   = query.record()
            sickCount = forceInt(record.value('sickCount'))
            MKB   = normalizeMKB(forceString(record.value('MKB')))
            sex   = forceInt(record.value('sex'))
            clientRural = forceBool(record.value('clientRural'))
            clientAge  = forceInt(record.value('clientAge'))
            rows = mapMainRows.get(MKB, [])
            for row in rows:
                reportLines = reportMainData[row]
                if len(reportLines) == 3:
                    rowList = [0]
                    if sex:
                        rowList.append(sex)
                else:
                    rowList = []
                    if sex:
                        rowList.append(sex-1)
                for i in rowList:
                    reportLine = reportLines[i]
                    reportLine[0] += sickCount
                    if clientAge <= 1:
                        reportLine[1] += sickCount
                    elif clientAge > 1 and clientAge <= 14:
                        reportLine[2] += sickCount
                    elif clientAge > 14 and clientAge <= 17:
                        reportLine[3] += sickCount
                    elif clientAge > 17 and clientAge <= 29:
                        reportLine[4] += sickCount
                    elif clientAge > 29 and clientAge <= 39:
                        reportLine[5] += sickCount
                    elif clientAge > 39:
                        reportLine[6] += sickCount
                    if clientRural:
                        reportLine[7] += sickCount
                        if clientAge <= 1:
                            reportLine[8] += sickCount
                        elif clientAge > 1 and clientAge <= 14:
                            reportLine[9] += sickCount
                        elif clientAge > 14 and clientAge <= 17:
                            reportLine[10] += sickCount

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(2000)')
        cursor.insertBlock()
        tableColumns = [
            ('25%',[u'Нозология',                                                     u'',                        u'',                        u'',          u'1' ], CReportBase.AlignLeft),
            ('5%', [u'Пол',                                                           u'',                        u'',                        u'',          u'2' ], CReportBase.AlignLeft),
            ('5%', [u'№ строки',                                                      u'',                        u'',                        u'',          u'3' ], CReportBase.AlignRight),
            ('10%',[u'Код по МКБ Х пересмотра',                                       u'',                        u'',                        u'',          u'4' ], CReportBase.AlignLeft),
            ('5%', [u'Число больных с вновь установленным диагнозом в отчетном году', u'ВСЕГО',                   u'',                        u'',          u'5' ], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'в том числе в возрасте:', u'0 – 1 год',               u'',          u'6' ], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'2 – 14 лет',              u'',          u'7' ], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'15 – 17 лет',             u'',          u'8' ], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'18 – 29 лет',             u'',          u'9' ], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'30 – 39 лет',             u'',          u'10'], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'40 лет и старше',         u'',          u'11'], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'из них: сельские жители', u'Всего.',                  u'',          u'12'], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'в том числе в возрасте:', u'0-1 год',   u'13'], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'',                        u'2-14 лет',  u'14'], CReportBase.AlignRight),
            ('5%', [u'',                                                              u'',                        u'',                        u'15-17 лет', u'15'], CReportBase.AlignRight),
            ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 4, 1)
        table.mergeCells(0, 3, 4, 1)
        table.mergeCells(0, 4, 1, 11)
        table.mergeCells(1, 4, 3, 1)
        table.mergeCells(1, 5, 1, 6)
        table.mergeCells(2, 5, 2, 1)
        table.mergeCells(2, 6, 2, 1)
        table.mergeCells(2, 7, 2, 1)
        table.mergeCells(2, 8, 2, 1)
        table.mergeCells(2, 9, 2, 1)
        table.mergeCells(2, 10, 2, 1)
        table.mergeCells(1, 11, 1, 4)
        table.mergeCells(2, 11, 2, 1)
        table.mergeCells(2, 12, 1, 3)

        iOld = 5
        for row, rowDescr in enumerate(MainRows_2000):
            names = rowDescr[0]
            sexs = rowDescr[1]
            rows = rowDescr[2]
            mkb = rowDescr[3]
            for j, cnt in enumerate(rows):
                i = table.addRow()
                table.setText(i, 0, names[j])
                table.setText(i, 1, sexs[j])
                table.setText(i, 2, cnt)
                if j == 0:
                    table.setText(i, 3, mkb)
                reportLines = reportMainData[row]
                for reportLine in reportLines:
                    for column in xrange(rowSize):
                        table.setText(i, 4+column, reportLine[column])
            if len(rows) != 3:
                table.mergeCells(iOld, 0, len(rows), 1)
            table.mergeCells(iOld, 3, len(rows), 1)
            iOld = i+1
        return doc

