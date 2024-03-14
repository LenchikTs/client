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
from library.Utils      import forceInt, forceString

from Reports.Report     import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportAcuteInfections import CReportAcuteInfectionsSetupDialog, getFilterAddress
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureListDescendants, getOrgStructures


MainRows_2006 = [(u'Сифилис – все формы',                            u'01', u'A50-A53'),
                 (u'Гонококковая инфекция',                          u'02', u'A54'),
                 (u'Трихомониаз',                                    u'03', u'A59'),
                 (u'Хламидийные  инфекции',                          u'04', u'A55-A56'),
                 (u'Аногенитальная герпетическая вирусная инфекция', u'05', u'A60'),
                 (u'Аногенитальные (вен.) бородавки',                u'06', u'A63'),
                 (u'Чесотка',                                        u'07', u'B86'),
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

    stmt = u"""
SELECT
    Diagnosis.MKB AS MKB,
    COUNT(DISTINCT Client.id) AS sickCount,
    (SELECT rbSST.code
    FROM ClientSocStatus AS CSS
       INNER JOIN rbSocStatusType AS rbSST ON rbSST.id =  CSS.socStatusType_id
    WHERE CSS.deleted=0 AND CSS.client_id=Client.id
       AND (CSS.begDate IS NULL OR CSS.begDate <= IF(Diagnosis.setDate IS NOT NULL, Diagnosis.setDate, Diagnosis.endDate))
       AND (CSS.endDate IS NULL OR CSS.endDate >= IF(Diagnosis.setDate IS NOT NULL, Diagnosis.setDate, Diagnosis.endDate))
       AND CSS.socStatusClass_id IN (SELECT rbSSC_9.id FROM rbSocStatusClass AS rbSSC_9 WHERE rbSSC_9.code = '9')
    ORDER BY CSS.id DESC
    LIMIT 1) AS socStatusTypeCode
FROM Diagnosis
INNER JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE Diagnosis.diagnosisType_id NOT IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT WHERE RBDT.code = '7' OR RBDT.code = '11')
AND %s
GROUP BY MKB, socStatusTypeCode
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
    return db.query(stmt % (stmtAddress,
                            db.joinAnd(cond)))


class CStatReportF9_2006(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Распределение больных по социальным группам. (Ф9)')


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
        mapMainRows = createMapCodeToRowIdx( [row[2] for row in MainRows_2006] )
        rowSize = 8
        reportMainData = [ [0]*rowSize for row in xrange(len(MainRows_2006)) ]
        query = selectData(params)
        while query.next():
            record   = query.record()
            sickCount = forceInt(record.value('sickCount'))
            MKB   = normalizeMKB(forceString(record.value('MKB')))
            socStatusTypeCode = forceString(record.value('socStatusTypeCode'))
            rows = mapMainRows.get(MKB, [])
            for row in rows:
                reportLine = reportMainData[row]
                if socStatusTypeCode == u'с05':
                    reportLine[0] += sickCount
                elif socStatusTypeCode == u'с06':
                    reportLine[1] += sickCount
                elif socStatusTypeCode in (u'с01', u'с02'):
                    reportLine[2] += sickCount
                elif socStatusTypeCode == u'с03':
                    reportLine[3] += sickCount
                elif socStatusTypeCode == u'с04':
                    reportLine[4] += sickCount
                elif socStatusTypeCode in (u'с07', u'с08'):
                    reportLine[5] += sickCount
                elif socStatusTypeCode == u'с09':
                    reportLine[6] += sickCount
                reportLine[7] += sickCount
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(2006)')
        cursor.insertBlock()
        tableColumns = [
            ('15%',[u'Нозология',       u'1'], CReportBase.AlignLeft),
            ('5%', [u'№ строки',        u'2'], CReportBase.AlignRight),
            ('10%',[u'работающий',      u'3'], CReportBase.AlignRight),
            ('10%',[u'неработающий',    u'4'], CReportBase.AlignRight),
            ('10%',[u'дошкольник',      u'5'], CReportBase.AlignRight),
            ('10%',[u'учащийся',        u'6'], CReportBase.AlignRight),
            ('10%',[u'студент',         u'7'], CReportBase.AlignRight),
            ('10%',[u'пенсионер',       u'8'], CReportBase.AlignRight),
            ('10%',[u'военно-служащий', u'9'], CReportBase.AlignRight),
            ('10%',[u'ВСЕГО',           u'10'], CReportBase.AlignRight),
            ]
        table = createTable(cursor, tableColumns)
        for row, rowDescr in enumerate(MainRows_2006):
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            reportLine = reportMainData[row]
            for col in xrange(rowSize):
                table.setText(i, 2+col, reportLine[col])
        return doc

