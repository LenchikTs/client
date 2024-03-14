# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
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
from library.Utils      import forceBool, forceInt, forceRef, forceString

from Orgs.Utils         import getOrgStructureListDescendants, getOrgStructureAddressIdList
from Reports.Report     import normalizeMKB
from Reports.ReportPersonSickList import addAddressCond, addAttachCond
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportAcuteInfections import getFilterAddress
from library.MapCode    import createMapCodeToRowIdx
from StatReportF12Seniors_2020 import CStatReportF12Seniors_2020, MainRows, CompRows
from StatReportF12Adults_2021 import selectData

def getSeniorAgesCond(begDate, today='Diagnosis.endDate'):
    cond = 'IF(Client.sex = 1, 60, 55)'
    if begDate:
        if begDate.year() == 2021:
            cond = 'IF(Client.sex = 1, 61, 56)'
        if begDate.year() == 2022 or begDate.year() == 2023:
            cond = 'IF(Client.sex = 1, 62, 57)'
        if begDate.year() >= 2024:
            cond = 'IF(Client.sex = 1, 63, 58)'
    return 'age(Client.birthDate, %s) >= %s' % (today, cond)


def selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params, boolThyroidosData = False):
    if boolThyroidosData:
        stmt = u"""
SELECT
  Diagnosis.client_id,
  Client.deathDate AS begDateDeath
FROM Diagnosis
LEFT JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE %s  AND (Diagnosis.MKB >= 'E00' AND Diagnosis.MKB <= 'E07') AND EXISTS(SELECT MAX(rbDispanser.observed)
FROM
Diagnostic AS D1
LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
WHERE
  D1.diagnosis_id = Diagnosis.id
  AND Diagnosis.diagnosisType_id NOT IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT WHERE RBDT.code IN ('7','11','51','52','53','54'))
  AND D1.endDate = (
    SELECT MAX(D2.endDate)
    FROM Diagnostic AS D2
    WHERE D2.diagnosis_id = Diagnosis.id
      AND D2.dispanser_id IS NOT NULL
      AND  D2.endDate < %s))
    """
    else:
        stmt = u"""
SELECT
   Diagnosis.client_id,
   rbDiseaseCharacter.code AS diseaseCharacter,
   (%s) AS firstInPeriod,

   Diagnosis.MKB,

   IF((SELECT MAX(rbDispanser.observed)
FROM
Diagnostic AS D1
LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
WHERE
  D1.diagnosis_id = Diagnosis.id
  AND Diagnosis.diagnosisType_id NOT IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT WHERE RBDT.code IN ('7','11','51','52','53','54'))
  AND D1.endDate = (
    SELECT MAX(D2.endDate)
    FROM Diagnostic AS D2
    WHERE D2.diagnosis_id = Diagnosis.id
      AND D2.dispanser_id IS NOT NULL
      AND  D2.endDate<%s))
      = 1, 1, 0) AS observed,

EXISTS(SELECT NULL
FROM Event
JOIN Diagnostic ON Diagnostic.event_id = Event.id
JOIN mes.MES ON Event.MES_id = mes.MES.id
JOIN mes.mrbMESGroup ON mes.MES.group_id = mes.mrbMESGroup.id
WHERE Event.deleted = 0 AND mes.MES.deleted = 0 AND mes.mrbMESGroup.deleted = 0 AND Diagnostic.deleted = 0
AND mes.mrbMESGroup.code = 'МедОсм' AND Diagnostic.diagnosis_id = Diagnosis.id) AS hasMedOsm,

EXISTS(SELECT NULL
FROM Event
JOIN Diagnostic ON Diagnostic.event_id = Event.id
JOIN EventType ON Event.eventType_id = EventType.id
JOIN EventType_Identification AS ETI ON ETI.master_id = EventType.id
WHERE Event.deleted = 0 AND EventType.deleted = 0 AND ETI.deleted = 0 AND Diagnostic.deleted = 0
AND ETI.value = 'prof' AND Diagnostic.diagnosis_id = Diagnosis.id) AS hasProf

FROM Diagnosis
INNER JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE %s
GROUP BY Diagnosis.client_id,Diagnosis.MKB
ORDER BY firstInPeriod DESC, observed DESC
    """
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    specialityId = params.get('specialityId', None)

    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableDiagnosis['mod_id'].isNull())
    diagnosticQuery = tableDiagnostic
    diagnosticCond = [ tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                       tableDiagnostic['deleted'].eq(0)
                     ]
    if registeredInPeriod:
        addDateInRange(diagnosticCond, tableDiagnostic['setDate'], begDate, endDate)
    if specialityId:
        diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['speciality_id'].eq(specialityId))
        diagnosticCond.append(tablePerson['deleted'].eq(0))
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureIdList:
        if not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))
    else:
        if not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if eventTypeIdList:
        tableEvent = db.table('Event')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticCond.append(tableEvent['eventType_id'].inlist(eventTypeIdList))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        diagnosticCond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    cond.append(db.existsStmt(diagnosticQuery, diagnosticCond))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    else:
        cond.append(tableClient['sex'].ne(0))
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL IF(Client.sex = 2 AND %d < 56, 56, IF(Client.sex = 1 AND %d < 61, 61, %d)) YEAR)'%(ageFrom, ageFrom, ageFrom))
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
    stmtAddress = ''
    if isFilterAddressOrgStructure:
        addrIdList = None
        cond2 = []
        if (addrType+1) & 1:
            addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            cond2 = addAddressCond(db, cond2, 0, addrIdList)
        if (addrType+1) & 2:
            if addrIdList is None:
                addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            cond2 = addAddressCond(db, cond2, 1, addrIdList)
        if ((addrType+1) & 4):
            if addressOrgStructureId:
                cond2 = addAttachCond(db, cond2, 'orgStructure_id = %d'%addressOrgStructureId, 1, None)
            else:
                cond2 = addAttachCond(db, cond2, 'LPU_id=%d'%QtGui.qApp.currentOrgId(), 1, None)
        if cond2:
            cond.append(db.joinOr(cond2))
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
            stmtAddress += u''' INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        cond.append('ClientAddress.id IN (%s)'%(getFilterAddress(params)))
    if 'attachTo' in params:
        attachOrgId = params['attachTo']
        if attachOrgId:
            cond = addAttachCond(db, cond, 'LPU_id=%d'%attachOrgId, *params.get('attachType', (0, None, QDate(), QDate())))
    elif 'attachToNonBase' in params:
        cond = addAttachCond(db, cond, 'LPU_id!=%d'%QtGui.qApp.currentOrgId(), *params.get('attachType', (0, None, QDate(), QDate())))
    elif 'attachType' in params:
        cond = addAttachCond(db, cond, '', *params['attachType'])
    excludeLeaved = params.get('excludeLeaved', False)
    if excludeLeaved:
        outerCond = ['ClientAttach.client_id = Client.id']
        innerCond = ['CA2.client_id = Client.id']
        cond.append('''EXISTS (SELECT ClientAttach.id
           FROM ClientAttach
           LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
           WHERE ClientAttach.deleted=0
           AND %s
           AND ClientAttach.id = (SELECT MAX(CA2.id)
                       FROM ClientAttach AS CA2
                       LEFT JOIN rbAttachType AS rbAttachType2 ON rbAttachType2.id = CA2.attachType_id
                       WHERE CA2.deleted=0 AND %s))'''% (QtGui.qApp.db.joinAnd(outerCond), QtGui.qApp.db.joinAnd(innerCond)))
        cond.append(tableClient['deathDate'].isNull())
    if 'dead' in params:
        cond.append(tableClient['deathDate'].isNotNull())
        if 'begDeathDate' in params:
            begDeathDate = params['begDeathDate']
            if begDeathDate:
                cond.append(tableClient['deathDate'].dateGe(begDeathDate))
        if 'endDeathDate' in params:
            endDeathDate = params['endDeathDate']
            if endDeathDate:
                cond.append(tableClient['deathDate'].dateLe(endDeathDate))
    if boolThyroidosData:
        return db.query(stmt % (stmtAddress, db.joinAnd(cond), tableDiagnosis['setDate'].formatValue(endDate.addDays(1))))
    else:
        return db.query(stmt % (db.joinAnd([tableDiagnosis['setDate'].le(endDate),
                                            tableDiagnosis['setDate'].ge(begDate)]),
                                tableDiagnosis['setDate'].formatValue(endDate.addDays(1)),
                                stmtAddress,
                                db.joinAnd(cond)))


def getClientCountFor4004(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params):
    clientsCount = 0
    clientsRemovingObserved = 0
    clientsDeadCount = 0
    clientsDeadCountI00_99 = 0

    query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, None, params)
    while query.next():
        record = query.record()
        sickCount = forceInt(record.value('sickCount'))
        getRemovingObserved = forceBool(record.value('getRemovingObserved'))
        clientsCount += sickCount
        if getRemovingObserved:
            clientsRemovingObserved += sickCount

    isDead = params.get('dead', False)
    params['dead'] = True
    query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, None, params)
    while query.next():
        record = query.record()
        sickCount = forceInt(record.value('sickCount'))
        getRemovingObserved = forceBool(record.value('getRemovingObserved'))
        MKB = forceString(record.value('MKB'))
        diagnosisType = forceString(record.value('diagnosisType'))

        if getRemovingObserved:
            clientsDeadCount += sickCount
            if MKB.startswith('I') and diagnosisType == '4':
                clientsDeadCountI00_99 += sickCount

    params['dead'] = isDead
    return (clientsCount, clientsRemovingObserved, clientsDeadCount, clientsDeadCountI00_99)


class CStatReportF12Seniors_2021(CStatReportF12Seniors_2020):
    def __init__(self, parent):
        CStatReportF12Seniors_2020.__init__(self, parent)
        self.setTitle(u'Ф12. 5.Взрослые старше трудоспособного возраста.')


    def getSetupDialog(self, parent):
        result = CStatReportF12Seniors_2020.getSetupDialog(self, parent)
        result.chkRegisteredInPeriod.setChecked(True)
        result.chkFilterExcludeLeaved.setVisible(False)
        result.chkFilterExcludeLeaved.setChecked(False)
        return result


    def build(self, params, reportMainRows=MainRows, reportCompRows=CompRows):
        mapMainRows = createMapCodeToRowIdx( [row[2] for row in reportMainRows] )
        mapCompRows = createMapCodeToRowIdx( [row[2] for row in reportCompRows] )

        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeList = params.get('eventTypeList', None)
        orgStructureList = params.get('orgStructureList', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 56)
        ageTo = params.get('ageTo', 150)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
        addrType = params.get('addressOrgStructureType', 0)
        addressOrgStructureId = params.get('addressOrgStructure', None)
        locality = params.get('locality', 0)
        detailMKB = params.get('detailMKB', False)
        if begDate and endDate:
            params['extraAgesCond'] = getSeniorAgesCond(begDate, "DATE('%04d-12-31')"%endDate.year())
        reportLine = None

        rowSize = 8
        rowCompSize = 4
        if detailMKB:
            reportMainData = {}  # { MKB: [reportLine] }
            reportCompData = {}  # { MKB: [reportLine] }
        else:
            reportMainData = [ [0]*rowSize for row in xrange(len(reportMainRows)) ]
            reportCompData = [ [0]*rowCompSize for row in xrange(len(reportCompRows)) ]
        query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, None, params)
        while query.next():
            record    = query.record()
            MKB       = normalizeMKB(forceString(record.value('MKB')))
            sickCount = forceInt(record.value('sickCount'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            diagnosisType = forceString(record.value('diagnosisType'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            observed = forceBool(record.value('observed'))
            hasMedOsm = forceBool(record.value('hasMedOsm'))
            hasProf = forceBool(record.value('hasProf'))
            closedEvent = forceBool(record.value('closedEvent'))
            getObserved = forceInt(record.value('getObserved'))
            getRemovingObserved = forceBool(record.value('getRemovingObserved'))
            getProfilactic      = forceBool(record.value('getProfilactic'))
            isNotPrimary        = forceBool(record.value('isNotPrimary'))
            getAdultsDispans    = forceBool(record.value('getAdultsDispans'))

            cols = [0]
            if getObserved:
                cols.append(1)
            if getRemovingObserved:
                cols.append(6)
            if observed or hasMedOsm or hasProf:
                cols.append(7)
            if diseaseCharacter == '1': # острое
                cols.append(2)
                if getObserved:
                    cols.append(3)
                if getProfilactic and not getAdultsDispans:
                    cols.append(4)
                if getAdultsDispans:
                    cols.append(5)
            elif firstInPeriod:
                cols.append(2)
                if getObserved:
                    cols.append(3)
                if getProfilactic and not getAdultsDispans:
                    cols.append(4)
                if getAdultsDispans:
                    cols.append(5)

            if detailMKB:
                reportLine = reportMainData.setdefault(MKB, [0]*rowSize)
                for col in cols:
                    reportLine[col] += sickCount
            else:
                for row in mapMainRows.get(MKB, []):
                    reportLine = reportMainData[row]
                    for col in cols:
                        reportLine[col] += sickCount

            if diagnosisType == '98':
                if detailMKB:
                    reportLine = reportCompData.setdefault(MKB, [0]*rowCompSize)
                    reportLine[0] += sickCount
                    if getProfilactic and isNotPrimary:
                        reportLine[1] += sickCount
                    if closedEvent:
                        reportLine[2] += sickCount
                else:
                    for row in mapCompRows.get(MKB, []):
                        reportLine = reportCompData[row]
                        reportLine[0] += sickCount
                        if getProfilactic and isNotPrimary:
                            reportLine[1] += sickCount
                        if closedEvent:
                            reportLine[2] += sickCount
        queryClient = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params)
        registeredAll = 0
        registeredFirst = 0
        consistsByEnd = [0, 0, 0]
        clientIdList = []
        clientIdFor4003List1 = {}
        clientIdFor4003List2 = {}
        while queryClient.next():
            record    = queryClient.record()
            clientId = forceRef(record.value('client_id'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            observed = forceBool(record.value('observed'))
            MKB = normalizeMKB(forceString(record.value('MKB')))
            if clientId and MKB in [u'B18', u'K74.6']:
                clientIdFor40031 = clientIdFor4003List1.setdefault(clientId, [])
                if MKB not in clientIdFor40031:
                    clientIdFor40031.append(MKB)
            if clientId and MKB in [u'B18', u'C22.0']:
                clientIdFor40032 = clientIdFor4003List2.setdefault(clientId, [])
                if MKB not in clientIdFor40032:
                    clientIdFor40032.append(MKB)

            if clientId and clientId not in clientIdList:
                clientIdList.append(clientId)
                registeredAll += 1
                if observed:
                    consistsByEnd[0] += 1
                if firstInPeriod:
                   registeredFirst += 1
        for clientIdFor40031 in clientIdFor4003List1.values():
            consistsByEnd[1] += (1 if len(clientIdFor40031) == 2 else 0)
        for clientIdFor40032 in clientIdFor4003List2.values():
            consistsByEnd[2] += (1 if len(clientIdFor40032) == 2 else 0)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        chkFilterAttachType = params.get('chkFilterAttachType', False)
        dead = params.get('dead', False)
        chkFilterAttach = params.get('chkFilterAttach', False)
        attachToNonBase = params.get('attachToNonBase', False)
        excludeLeaved = params.get('excludeLeaved', False)
        if chkFilterAttachType or dead or chkFilterAttach or attachToNonBase or excludeLeaved:
           self.dumpParamsAttach(cursor, params)
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParamsMultiSelect(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(4000)')
        cursor.insertBlock()

        tableColumns = [
            ('15%', [u'Наименование классов и отдельных болезней',        u'',                                                                     u'',                                                                    u'1'], CReportBase.AlignLeft),
            ('5%',  [u'№ строки',                                         u'',                                                                     u'',                                                                    u'2'], CReportBase.AlignLeft),
            ('10%', [u'Код по МКБ-10 пересмотра',                         u'',                                                                     u'',                                                                    u'3'], CReportBase.AlignLeft),
            ('10%', [u'Зарегистрировано пациентов с данным заболеванием', u'Всего',                                                                u'',                                                                    u'4'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'из них(из гр. 4):',                                                    u'взято под диспансерное наблюдение',                                   u'5'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'',                                                                     u'с впервые в жизни установленным диагнозом',                           u'6'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'из заболеваний с впервые в жизни установленным диагнозом (из гр. 6):', u'взято под диспансерное наблюдение',                                   u'7'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'',                                                                     u'выявлено при профосмотре',                                            u'8'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'',                                                                     u'выявлено при диспансеризации определенных групп взрослого населения', u'9'], CReportBase.AlignRight),
            ('10%', [u'Снято с диспансерного наблюдения',                 u'',                                                                     u'',                                                                    u'10'], CReportBase.AlignRight),
            ('10%', [u'Состоит на д.н. на конец периода',                 u'',                                                                     u'',                                                                    u'11'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1) # Наименование
        table.mergeCells(0, 1, 3, 1) # № стр.
        table.mergeCells(0, 2, 3, 1) # Код МКБ
        table.mergeCells(0, 3, 1, 6) # Всего
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(1, 6, 1, 3)
        table.mergeCells(0, 9, 3, 1)
        table.mergeCells(0, 10, 3, 1)

        if detailMKB:
            for row, MKB in enumerate(sorted(reportMainData.keys())):
                reportLine = reportMainData[MKB]
                reportLine[7] = reportLine[1] - reportLine[6]
                if not MKB:
                    MKBDescr, MKB = u'', u'Не указано'
                else:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB, 'DiagName'))
                if MKB.endswith('.0') and not MKBDescr:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB[:-2], 'DiagName'))
                i = table.addRow()
                table.setText(i, 0, MKBDescr)
                table.setText(i, 1, row+1)
                table.setText(i, 2, MKB)
                for col in xrange(rowSize):
                    table.setText(i, 3+col, reportLine[col])
        else:
            for row, rowDescr in enumerate(reportMainRows):
                reportLine = reportMainData[row]
                reportLine[7] = reportLine[1] - reportLine[6]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2] + (u' (часть)' if row == 58 else ''))
                for col in xrange(rowSize):
                    table.setText(i, 3+col, reportLine[col])

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'(4001) Число физических лиц зарегистрированных пациентов – всего %d , из них с диагнозом , установленным впервые в жизни %d , состоит под диспансерным наблюдением на конец отчетного года (из гр. 11, стр. 1.0) %d.'%(registeredAll, registeredFirst, consistsByEnd[0]))
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'(4003) Из числа пациентов, состоящих на конец отчетного года под диспансерным наблюдением (гр. 11): состоит под диспансерным наблюдением лиц с хроническим вирусным гепатитом (B18) и циррозом печени (K74.6) одновременно %d чел.; с хроническим вирусным гепатитом (B18) и гепатоцеллюлярным раком (C22.0) одновременно %d чел.'%(consistsByEnd[1], consistsByEnd[2]))
        cursor.insertBlock()
        cursor.insertText(u'Число лиц с болезнями системы кровообращения,состоявших под диспансерном наблюдением (стр.10.0 гр.5) %d из них снято %d из них умерло (из графы 2) %d, из из них умерло от болезней системы кровообращения (из графы 3) %d' %
            getClientCountFor4004(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params))
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(u'Взрослые старше трудоспособного возраста.')
        cursor.insertBlock()
        cursor.insertText(u'ФАКТОРЫ, ВЛИЯЮЩИЕ НА СОСТОЯНИЕ ЗДОРОВЬЯ НАСЕЛЕНИЯ')
        cursor.insertBlock()
        cursor.insertText(u'И ОБРАЩЕНИЯ В МЕДИЦИНСКИЕ ОРГАНИЗАЦИИ (С ПРОФИЛАКТИЧЕСКОЙ ЦЕЛЬЮ)')
        cursor.insertBlock()
        cursor.insertText(u'(4100)')
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('30%', [u'Наименование', u'', u'1'], CReportBase.AlignLeft),
            ('10%', [u'№ строки', u'', u'2'], CReportBase.AlignLeft),
            ('15%', [u'Код МКБ-10', u'', u'3'], CReportBase.AlignLeft),
            ('15%', [u'Обращения', u'всего', u'4'], CReportBase.AlignRight),
            ('15%', [u'', u'из них: повторные', u'5'], CReportBase.AlignRight),
            ('15%', [u'', u'законченные случаи', u'6'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 3)

        if detailMKB:
            for row, MKB in enumerate(sorted(reportCompData.keys())):
                reportLine = reportCompData[MKB]
                if not MKB:
                    MKBDescr, MKB = u'', u'Не указано'
                else:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB, 'DiagName'))
                if MKB.endswith('.0') and not MKBDescr:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB[:-2], 'DiagName'))
                i = table.addRow()
                table.setText(i, 0, MKBDescr)
                table.setText(i, 1, row+1)
                table.setText(i, 2, MKB)
                table.setText(i, 3, reportLine[0])
                table.setText(i, 4, reportLine[1])
                table.setText(i, 5, reportLine[2])
        else:
            for row, rowDescr in enumerate(reportCompRows):
                reportLine = reportCompData[row]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2])
                table.setText(i, 3, reportLine[0])
                table.setText(i, 4, reportLine[1])
                table.setText(i, 5, reportLine[2])

        return doc
