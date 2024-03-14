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

from Orgs.Utils         import getOrgStructureDescendants, getOrgStructures
from Reports.Report     import CReport, normalizeMKB
from Reports.ReportAcuteInfections import CReportAcuteInfectionsSetupDialog
from Reports.ReportBase import CReportBase, createTable


MainRows = [
    (u'цереброваскулярные болезни', u'1.0',u'I60-I69'),
    (u'в том числе: субарахноидальное кровоизлияние', u'1.1',u'I60'),
    (u'\tвнутримозговое кровоизлияние', u'1.2',u'I61'),
    (u'\tинфаркт мозга', u'1.3',u'I63'),
    (u'\tинсульт, не уточненный как кровоизлияние или инфаркт', u'1.4',u'I64'),
    (u'\tдругие цереброваскулярные болезни', u'1.5',u'I67'),
    (u'\tпоследствия цереброваскулярных болезней', u'1.6',u'I69'),
    (u'болезни артерий, артериел и капиляров', u'1.7',u'I70-I79'),
    (u'в том числе: склероз', u'1.8',u'I70'),
]


def selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, areaIdEnabled, areaId, locality, params):
    stmt="""
SELECT
   age(Client.birthDate, Diagnosis.endDate) AS clientAge,
   Diagnosis.MKB AS MKB,
   COUNT(*) AS sickCount,
   (%s) AS firstInPeriod,
   IF((SELECT MAX(rbDispanser.observed)
FROM
Diagnostic AS D1
LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
WHERE
  D1.diagnosis_id = Diagnosis.id
  AND D1.endDate = (
    SELECT MAX(D2.endDate)
    FROM Diagnostic AS D2
    WHERE D2.diagnosis_id = Diagnosis.id
      AND D2.dispanser_id IS NOT NULL
      AND  D2.endDate<%s))
      = 1, 1, 0) AS observed

FROM Diagnosis
LEFT JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE %s
GROUP BY clientAge, MKB, firstInPeriod, observed
    """
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableOrgStructureAddress = db.table('OrgStructure_Address')
    tableClientAddress = db.table('ClientAddress')
    tableAddress = db.table('Address')
    tableAddressHouse = db.table('AddressHouse')

    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableDiagnosis['mod_id'].isNull())
    cond.append(tableDiagnosis['MKB'].between('I60', 'I8'))
    cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), tableDiagnosis['setDate'].lt(endDate.addDays(1))]))
    cond.append(db.joinOr([tableDiagnosis['endDate'].ge(begDate), tableDiseaseCharacter['code'].eq('3')]))

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [ tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                       tableDiagnostic['deleted'].eq(0)
                     ]
    if registeredInPeriod:
        addDateInRange(diagnosticCond, tableDiagnostic['setDate'], begDate, endDate)
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureId:
        diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
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
    if areaIdEnabled:
        stmtAddress = u'''LEFT JOIN ClientAddress ON ClientAddress.client_id = Diagnosis.client_id
                        AND ClientAddress.id = (SELECT MAX(id) FROM ClientAddress AS CA WHERE CA.Type=1 and CA.client_id = Diagnosis.client_id)
LEFT JOIN Address ON Address.id = ClientAddress.address_id'''
        if areaId:
            orgStructureIdList = getOrgStructureDescendants(areaId)
        else:
            orgStructureIdList = getOrgStructures(QtGui.qApp.currentOrgId())
        subCond = [ tableOrgStructureAddress['master_id'].inlist(orgStructureIdList),
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
        filterAddressType = params.get('filterAddressType', 0)
        filterAddressCity = params.get('filterAddressCity', None)
        filterAddressStreet = params.get('filterAddressStreet', None)
        filterAddressHouse = params.get('filterAddressHouse', u'')
        filterAddressCorpus = params.get('filterAddressCorpus', u'')
        filterAddressFlat = params.get('filterAddressFlat', u'')
        filterAddressOkato = params.get('filterAddressOkato')
        filterAddressStreetList = params.get('filterAddressStreetList')
        if not stmtAddress:
            stmtAddress = u'''LEFT JOIN ClientAddress ON ClientAddress.client_id = Client.id
                               LEFT JOIN Address ON Address.id = ClientAddress.address_id
                               LEFT JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        else:
            stmtAddress += u''' LEFT JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        cond.append(tableClientAddress['type'].eq(filterAddressType))
        cond.append(db.joinOr([tableClientAddress['id'].isNull(), tableClientAddress['deleted'].eq(0)]))
        if filterAddressCity or filterAddressStreet or filterAddressHouse or filterAddressCorpus or filterAddressFlat:
            cond.append(db.joinOr([tableAddress['id'].isNull(), tableAddress['deleted'].eq(0)]))
            cond.append(db.joinOr([tableAddressHouse['id'].isNull(), tableAddressHouse['deleted'].eq(0)]))
        if filterAddressCity:
            cond.append(tableAddressHouse['KLADRCode'].like('%s%%00'%filterAddressCity.rstrip('0')))
        if filterAddressStreet:
            cond.append(tableAddressHouse['KLADRStreetCode'].like(filterAddressStreet))
        if filterAddressHouse:
            cond.append(tableAddressHouse['number'].eq(filterAddressHouse))
        if filterAddressCorpus:
            cond.append(tableAddressHouse['corpus'].eq(filterAddressCorpus))
        if filterAddressFlat:
            cond.append(tableAddress['flat'].eq(filterAddressFlat))
        if filterAddressOkato:
            cond.append(tableAddressHouse['KLADRStreetCode'].inlist(filterAddressStreetList))
    return db.query(stmt % (db.joinAnd([tableDiagnosis['setDate'].le(endDate),
                                        tableDiagnosis['setDate'].ge(begDate)]),
                            tableDiagnosis['setDate'].formatValue(endDate.addDays(1)),
                            stmtAddress,
                            db.joinAnd(cond)))


class CStatReportF12Inset2008(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        title = u'Ф.12 Вкладыш 2008'
        self.setTitle(title, u'Ф.12')


    def getDefaultParams(self):
        result = CReport.getDefaultParams(self)
        result['ageFrom']     = 0
        result['ageTo']       = 150
        return result


    def getSetupDialog(self, parent):
        result = CReportAcuteInfectionsSetupDialog(parent)
        result.setAreaEnabled(True)
#        result.setMKBFilterEnabled(False)
#        result.setAccountAccompEnabled(False)
        result.setTitle(self.title())
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx( [row[2] for row in MainRows] )

        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        areaIdEnabled = params.get('areaIdEnabled', None)
        areaId = params.get('areaId', None)
        locality = params.get('locality', 0)
        reportLine = None

        rowSize = 9
        reportMainData = [ [0]*rowSize for row in xrange(len(MainRows)) ]
        query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, areaIdEnabled, areaId, locality, params)

        while query.next():
            record    = query.record()
            age       = forceInt(record.value('clientAge'))
            MKB       = normalizeMKB(forceString(record.value('MKB')))
            sickCount = forceInt(record.value('sickCount'))
#            clientCount = forceInt(record.value('clientCount'))
#            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            observed = forceBool(record.value('observed'))

            ageIndex = 0 if age<=14 else 1 if age <= 17 else 2
            cols = [ageIndex]
            if firstInPeriod:
                cols.append(3+ageIndex)
            if observed:
                cols.append(6+ageIndex)


            for row in mapMainRows.get(MKB, []):
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += sickCount

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
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'СВЕДЕНИЯ О ЧИСЛЕ ЦЕРЕБРОВАСКУЛЯРНЫХ ЗАБОЛЕВАНИЙ')
        cursor.insertBlock()
        cursor.insertText(u'1000')
        cursor.insertBlock()
        children  = u'дети\n0-14 лет\nвключительно'
        teenagers = u'подростки\n15-17 лет\nвключительно'
        adult     = u'взрослые\n18 лет\nи старше'
        tableColumns = [
            ('30%',[u'Наименование болезней',                          '',      '', '1'], CReportBase.AlignLeft),
            ('8%', [u'№ строки',                                       '',      '', '2'], CReportBase.AlignLeft),
            ('8%', [u'код МКБ',                                        '',      '', '3'], CReportBase.AlignLeft),
            ('8%', [u'Зарегистрировано больных с данным заболеванием', u'всего', children, '4'], CReportBase.AlignRight),
            ('8%', [u'',                                               '',      teenagers, '5'], CReportBase.AlignRight),
            ('8%', [u'',                                               '',      adult,     '6'], CReportBase.AlignRight),
            ('8%', [u'',                                               u'в т.ч. впервые', children,     '7'], CReportBase.AlignRight),
            ('8%', [u'',                                               '',      teenagers, '8'], CReportBase.AlignRight),
            ('8%', [u'',                                               '',      adult,     '9'], CReportBase.AlignRight),
            ('8%', [u'Состоит на д.н. на конец периода',               '',      children, '10'], CReportBase.AlignRight),
            ('8%', [u'',                                               '',      teenagers,'11'], CReportBase.AlignRight),
            ('8%', [u'',                                               '',      adult,    '12'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1) # Наименование
        table.mergeCells(0, 1, 3, 1) # № стр.
        table.mergeCells(0, 2, 3, 1) # Код МКБ
        table.mergeCells(0, 3, 1, 6) # Зарегистрировано
        table.mergeCells(1, 3, 1, 3) # Всего
        table.mergeCells(1, 6, 1, 3) # Впервые
        table.mergeCells(0, 9, 2, 3) # Д.Н.

        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3+col, reportLine[col])

        return doc
