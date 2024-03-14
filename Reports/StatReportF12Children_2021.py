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

from library.Utils                  import forceBool, forceInt, forceRef, forceString
from library.database               import addDateInRange
from library.MapCode                import createMapCodeToRowIdx
from Reports.ReportAcuteInfections  import getFilterAddress
from Reports.ReportPersonSickList   import addAddressCond, addAttachCond
from Orgs.Utils                     import getOrgStructureListDescendants, getOrgStructureAddressIdList
from Reports.Report                 import normalizeMKB
from Reports.ReportBase             import CReportBase, createTable

from StatReportF12Children_2020     import (CStatReportF12Children0_1_2020,
                                            CStatReportF12Children0_14_2020,
                                            CompRowsToOneYear,
                                            selectDataClient,
                                            MainRowsToOneYear,
                                            CompRows,
                                            MainRows,
                                            getClientCountFor1004)



def selectDataToOneYear(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params):
    stmt = u"""
SELECT
   Diagnosis.MKB AS MKB,
   COUNT(*) AS sickCount,
   rbDiseaseCharacter.code AS diseaseCharacter,
   rbDiagnosisType.code AS diagnosisType,
   IF(DATE_ADD(Client.birthDate, INTERVAL 29 DAY) >= Diagnosis.endDate, 1, 0) AS dayAge,
   Diagnosis.client_id,
   age(Client.birthDate, Diagnosis.endDate) AS clientAge,
   EXISTS(SELECT rbResult.id
   FROM
   Diagnostic AS D1
   INNER JOIN Event ON Event.id = D1.event_id
   INNER JOIN rbResult ON rbResult.id = Event.result_id
   WHERE D1.diagnosis_id = Diagnosis.id AND rbResult.continued = 0
   ORDER BY Event.id) AS closedEvent,
   (SELECT IF(rbDispanser.code IN (2,6,1), 1, 0)
    FROM
    Diagnostic AS D1
    LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
    WHERE
      D1.diagnosis_id = Diagnosis.id
      AND (rbDispanser.code IN (2,6,1))
    ORDER BY rbDispanser.code
    LIMIT 1) AS getObserved,
   EXISTS(SELECT rbDispanser.id
    FROM
    Diagnostic AS D1
    LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
    WHERE
      D1.diagnosis_id = Diagnosis.id
      AND (rbDispanser.code = 3 OR rbDispanser.code = 4 OR rbDispanser.code = 5)
    ORDER BY rbDispanser.code) AS getRemovingObserved,
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
          AND (D2.setDate IS NULL OR D2.setDate < %s)
          AND (D2.endDate IS NULL OR D2.endDate >= %s))) = 1, 1, 0) AS observed,
   EXISTS(SELECT ETP.id
    FROM
    Diagnostic AS D1
    INNER JOIN Event AS E ON E.id = D1.event_id
    INNER JOIN EventType AS ET ON ET.id = E.eventType_id
    INNER JOIN rbEventTypePurpose AS ETP ON ETP.id = ET.purpose_id
    WHERE
      D1.diagnosis_id = Diagnosis.id
      AND ET.deleted = 0 AND E.deleted = 0
      AND D1.deleted = 0 AND ETP.code = 2
    ORDER BY ETP.code) AS getProfilactic,
   EXISTS(SELECT E.id
    FROM Diagnostic AS D1 INNER JOIN Event AS E ON E.id = D1.event_id
    WHERE D1.diagnosis_id = Diagnosis.id AND E.deleted = 0
    AND D1.deleted = 0 AND E.isPrimary = 2) AS isNotPrimary,
   EXISTS(SELECT mes.MES.id
    FROM
    Diagnostic AS D1
    JOIN Event AS E ON E.id = D1.event_id
    LEFT JOIN mes.MES ON mes.MES.id = E.MES_id
    LEFT JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id = mes.MES.group_id
    LEFT JOIN EventType_Identification ON E.eventType_id = EventType_Identification.master_id
    LEFT JOIN rbAccountingSystem ON EventType_Identification.system_id = rbAccountingSystem.id
    WHERE
      D1.diagnosis_id = Diagnosis.id AND E.deleted = 0
      AND ((EventType_Identification.deleted = 0 AND EventType_Identification.value = 'dprof'
      AND rbAccountingSystem.urn = 'urn:oid:f12') OR
      (D1.deleted = 0 AND mes.mrbMESGroup.code = 'МедОсм'))) AS getAdultsDispans

FROM Diagnosis
LEFT JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE Diagnosis.diagnosisType_id NOT IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT WHERE RBDT.code = '7' OR RBDT.code = '11')
AND %s
GROUP BY MKB, diseaseCharacter, firstInPeriod, getObserved, getRemovingObserved, getProfilactic, isNotPrimary, getAdultsDispans, observed, rbDiagnosisType.id, closedEvent, dayAge, clientAge, Diagnosis.client_id
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
    isPersonPost = params.get('isPersonPost', 0)
    if isPersonPost:
        tableRBPost = db.table('rbPost')
        if not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticQuery = diagnosticQuery.leftJoin(tableRBPost, tableRBPost['id'].eq(tablePerson['post_id']))
        if isPersonPost == 1:
            diagnosticCond.append("LEFT(rbPost.code, 1) IN ('1','2','3')")
        elif isPersonPost == 2:
            diagnosticCond.append("LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')")
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureIdList:
        if not isPersonPost and not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))
    else:
        if not isPersonPost and not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
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
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Diagnosis.endDate <= SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo))
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
    stmtAddress = u''
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
        stmtAddress = u'''INNER JOIN ClientAddress ON ClientAddress.client_id = Client.id
                          INNER JOIN Address ON Address.id = ClientAddress.address_id
                          INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
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
    isDispanser = params.get('isDispanser', False)
    if isDispanser:
        cond.append(u'''IF((SELECT MAX(rbDispanser.observed)
        FROM
        Diagnostic AS D1
        LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
        WHERE
          D1.diagnosis_id = Diagnosis.id
          AND rbDispanser.observed = 1
          AND D1.endDate = (
            SELECT MAX(D2.endDate)
            FROM Diagnostic AS D2
            WHERE D2.diagnosis_id = Diagnosis.id
              AND D2.dispanser_id IS NOT NULL
              AND (D2.endDate IS NULL OR D2.endDate >= %s)
              AND (D2.setDate IS NULL OR D2.setDate < %s))) = 1, 1, 0)'''%(tableDiagnosis['setDate'].formatValue(begDate), tableDiagnosis['setDate'].formatValue(endDate.addDays(1))))
    return db.query(stmt % (db.joinAnd([tableDiagnosis['setDate'].le(endDate),
                                        tableDiagnosis['setDate'].ge(begDate)]),
                            tableDiagnosis['setDate'].formatValue(endDate.addDays(1)),
                            tableDiagnosis['setDate'].formatValue(endDate.addDays(1)),
                            stmtAddress,
                            db.joinAnd(cond)))


def selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params):
    stmt = u"""
SELECT
   Diagnosis.MKB AS MKB,
   COUNT(*) AS sickCount,
   rbDiseaseCharacter.code AS diseaseCharacter,
   rbDiagnosisType.code AS diagnosisType,
   age(Client.birthDate, Diagnosis.endDate) AS clientAge,
   EXISTS(SELECT rbResult.id
   FROM
   Diagnostic AS D1
   INNER JOIN Event ON Event.id = D1.event_id
   INNER JOIN rbResult ON rbResult.id = Event.result_id
   WHERE D1.diagnosis_id = Diagnosis.id AND rbResult.continued = 0
   ORDER BY Event.id) AS closedEvent,
   (SELECT IF(rbDispanser.code IN (2,6,1), 1, 0)
    FROM
    Diagnostic AS D1
    LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
    WHERE
      D1.diagnosis_id = Diagnosis.id
      AND (rbDispanser.code IN (2,6,1))
    ORDER BY rbDispanser.code
    LIMIT 1) AS getObserved,
   EXISTS(SELECT rbDispanser.id
    FROM
    Diagnostic AS D1
    LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
    WHERE
      D1.diagnosis_id = Diagnosis.id
      AND (rbDispanser.code = 3 OR rbDispanser.code = 4 OR rbDispanser.code = 5)
    ORDER BY rbDispanser.code) AS getRemovingObserved,
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
          AND (D2.setDate IS NULL OR D2.setDate < %s)
          AND (D2.endDate IS NULL OR D2.endDate >= %s))) = 1, 1, 0) AS observed,
   EXISTS(SELECT ETP.id
    FROM
    Diagnostic AS D1
    INNER JOIN Event AS E ON E.id = D1.event_id
    INNER JOIN EventType AS ET ON ET.id = E.eventType_id
    INNER JOIN rbEventTypePurpose AS ETP ON ETP.id = ET.purpose_id
    WHERE
      D1.diagnosis_id = Diagnosis.id
      AND ET.deleted = 0 AND E.deleted = 0
      AND D1.deleted = 0 AND ETP.code = 2
    ORDER BY ETP.code) AS getProfilactic,
   EXISTS(SELECT E.id
    FROM Diagnostic AS D1 INNER JOIN Event AS E ON E.id = D1.event_id
    WHERE D1.diagnosis_id = Diagnosis.id AND E.deleted = 0
    AND D1.deleted = 0 AND E.isPrimary = 2) AS isNotPrimary,
   EXISTS(SELECT mes.MES.id
    FROM
    Diagnostic AS D1
    JOIN Event AS E ON E.id = D1.event_id
    LEFT JOIN mes.MES ON mes.MES.id = E.MES_id
    LEFT JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id = mes.MES.group_id
    LEFT JOIN EventType_Identification ON E.eventType_id = EventType_Identification.master_id
    LEFT JOIN rbAccountingSystem ON EventType_Identification.system_id = rbAccountingSystem.id
    WHERE
      D1.diagnosis_id = Diagnosis.id AND E.deleted = 0
      AND ((EventType_Identification.deleted = 0 AND EventType_Identification.value = 'dprof'
      AND rbAccountingSystem.urn = 'urn:oid:f12') OR
      (D1.deleted = 0 AND mes.mrbMESGroup.code = 'МедОсм'))) AS getAdultsDispans

FROM Diagnosis
LEFT JOIN Client ON Client.id = Diagnosis.client_id
%s
LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE Diagnosis.diagnosisType_id NOT IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT WHERE RBDT.code = '7' OR RBDT.code = '11')
AND %s
GROUP BY MKB, diseaseCharacter, firstInPeriod, getObserved, getRemovingObserved, getProfilactic, isNotPrimary, getAdultsDispans, observed, rbDiagnosisType.id, closedEvent, clientAge
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
    else:
        diagnosticCond.append(tableDiagnostic['setDate'].le(endDate))
        diagnosticCond.append(db.joinOr([tableDiagnostic['endDate'].ge(begDate), tableDiagnostic['endDate'].isNull()]))
    if specialityId:
        diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['speciality_id'].eq(specialityId))
        diagnosticCond.append(tablePerson['deleted'].eq(0))
    isPersonPost = params.get('isPersonPost', 0)
    if isPersonPost:
        tableRBPost = db.table('rbPost')
        if not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticQuery = diagnosticQuery.leftJoin(tableRBPost, tableRBPost['id'].eq(tablePerson['post_id']))
        if isPersonPost == 1:
            diagnosticCond.append("LEFT(rbPost.code, 1) IN ('1','2','3')")
        elif isPersonPost == 2:
            diagnosticCond.append("LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')")
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureIdList:
        if not isPersonPost and not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))
    else:
        if not isPersonPost and not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
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
    if ageFrom <= ageTo:
        cond.append("age(Client.birthDate, Diagnosis.endDate) BETWEEN %d AND %d" % (ageFrom, ageTo))
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
    stmtAddress = u''
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
        stmtAddress = u'''INNER JOIN ClientAddress ON ClientAddress.client_id = Client.id
                          INNER JOIN Address ON Address.id = ClientAddress.address_id
                          INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        cond.append('ClientAddress.id IN (%s)'%(getFilterAddress(params)))
    if 'attachTo' in params:
        attachOrgId = params['attachTo']
        if attachOrgId:
            cond = addAttachCond(db, cond, 'LPU_id=%d'%attachOrgId, *params.get('attachType', (0, None, QDate(), QDate())))
    elif 'attachToNonBase' in params:
        cond = addAttachCond(db, cond, 'LPU_id!=%d'%QtGui.qApp.currentOrgId(), *params.get('attachType', (0, None, QDate(), QDate())))
    elif 'attachType' in params:
        addAttachCond(db, cond, '', *params['attachType'])
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
    if params.get('MKBFrom'):
        cond.append(tableDiagnosis['MKB'].ge(params.get('MKBFrom')))
    if params.get('MKBTo'):
        cond.append(tableDiagnosis['MKB'].le(params.get('MKBTo')))
    isDispanser = params.get('isDispanser', False)
    if isDispanser:
        cond.append(u'''IF((SELECT MAX(rbDispanser.observed)
        FROM
        Diagnostic AS D1
        LEFT JOIN rbDispanser ON rbDispanser.id = D1.dispanser_id
        WHERE
          D1.diagnosis_id = Diagnosis.id
          AND rbDispanser.observed = 1
          AND D1.endDate = (
            SELECT MAX(D2.endDate)
            FROM Diagnostic AS D2
            WHERE D2.diagnosis_id = Diagnosis.id
              AND D2.dispanser_id IS NOT NULL
              AND (D2.endDate IS NULL OR D2.endDate >= %s)
              AND (D2.setDate IS NULL OR D2.setDate < %s))) = 1, 1, 0)'''%(tableDiagnosis['setDate'].formatValue(begDate), tableDiagnosis['setDate'].formatValue(endDate.addDays(1))))
    return db.query(stmt % (db.joinAnd([tableDiagnosis['setDate'].le(endDate),
                                        tableDiagnosis['setDate'].ge(begDate)]),
                            tableDiagnosis['setDate'].formatValue(endDate.addDays(1)),
                            tableDiagnosis['setDate'].formatValue(endDate.addDays(1)),
                            stmtAddress,
                            db.joinAnd(cond)))




class CStatReportF12Children0_14_2021(CStatReportF12Children0_14_2020):
    def __init__(self, parent):
        CStatReportF12Children0_14_2020.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CStatReportF12Children0_14_2020.getSetupDialog(self, parent)
        result.chkFilterExcludeLeaved.setVisible(False)
        result.chkFilterExcludeLeaved.setChecked(False)
        result.chkRegisteredInPeriod.setChecked(True)
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
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 14)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
        addrType = params.get('addressOrgStructureType', 0)
        addressOrgStructureId = params.get('addressOrgStructure', None)
        locality = params.get('locality', 0)
        detailMKB = params.get('detailMKB', False)
        reportLine = None

        rowSize = 9
        rowCompSize = 4
        if detailMKB:
            reportMainData = {}  # { MKB: [reportLine] }
            reportCompData = {}  # { MKB: [reportLine] }
        else:
            reportMainData = [ [0]*rowSize for row in xrange(len(reportMainRows)) ]
            reportCompData = [ [0]*rowCompSize for row in xrange(len(reportCompRows)) ]
        query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params)
        while query.next():
            record              = query.record()
            clientId            = forceRef(record.value('client_id'))
            clientAge           = forceInt(record.value('clientAge'))
            MKB                 = normalizeMKB(forceString(record.value('MKB')))
            sickCount           = forceInt(record.value('sickCount'))
            diseaseCharacter    = forceString(record.value('diseaseCharacter'))
            diagnosisType       = forceString(record.value('diagnosisType'))
            firstInPeriod       = forceBool(record.value('firstInPeriod'))
            closedEvent         = forceBool(record.value('closedEvent'))
            getObserved         = forceBool(record.value('getObserved'))
            observed            = forceBool(record.value('observed'))
            getRemovingObserved = forceBool(record.value('getRemovingObserved'))
            getProfilactic      = forceBool(record.value('getProfilactic'))
            getAdultsDispans    = forceBool(record.value('getAdultsDispans'))
            isNotPrimary        = forceBool(record.value('isNotPrimary'))

            cols = [0]
            if clientAge >= 0 and clientAge < 5:
                cols.append(1)
            elif clientAge >= 5 and clientAge < 10:
                cols.append(2)
            if diseaseCharacter == '1': # острое
                cols.append(4)
                if getAdultsDispans:
                    cols.append(6)
                if getObserved:
                    cols.append(5)
            elif firstInPeriod:
                cols.append(4)
                if getAdultsDispans:
                    cols.append(6)
                if getObserved:
                    cols.append(5)
            if getObserved:
                cols.append(3)
            if getRemovingObserved:
                cols.append(7)
            if observed:
                cols.append(8)

            if detailMKB:
                reportLine = reportMainData.setdefault(MKB, [0]*rowSize)
                for col in cols:
                    reportLine[col] += sickCount
            else:
                for row in mapMainRows.get(MKB, []):
                    reportLine = reportMainData[row]
                    for col in cols:
                        reportLine[col] += sickCount

            if diagnosisType == '98' and clientAge >= 0 and clientAge < 1:
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
        registeredAll = 0
        registeredFirst = 0
        consistsByEnd = [0, 0, 0, 0, 0]
        clientIdList = []
        clientIdFor1003List1 = {}
        clientIdFor1003List2 = {}
        queryClient = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params)
        while queryClient.next():
            record    = queryClient.record()
            clientId         = forceRef(record.value('client_id'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            firstInPeriod    = forceBool(record.value('firstInPeriod'))
            observed         = forceBool(record.value('observed'))
            clientAge        = forceInt(record.value('clientAge'))
            MKB              = normalizeMKB(forceString(record.value('MKB')))
            if clientId and MKB in [u'B18', u'K74.6']:
                clientIdFor10031 = clientIdFor1003List1.setdefault(clientId, [])
                if MKB not in clientIdFor10031:
                    clientIdFor10031.append(MKB)
            if clientId and MKB in [u'B18', u'C22.0']:
                clientIdFor10032 = clientIdFor1003List2.setdefault(clientId, [])
                if MKB not in clientIdFor10032:
                    clientIdFor10032.append(MKB)
            if clientId and clientId not in clientIdList:
                clientIdList.append(clientId)
                registeredAll += 1
                if observed:
                    consistsByEnd[0] += 1
                    if clientAge >= 0 and clientAge < 5:
                        consistsByEnd[1] += 1
                    elif clientAge >= 5 and clientAge < 10:
                        consistsByEnd[2] += 1
                if firstInPeriod:
                   registeredFirst += 1
        for clientIdFor10031 in clientIdFor1003List1.values():
            consistsByEnd[3] += (1 if len(clientIdFor10031) == 2 else 0)
        for clientIdFor10032 in clientIdFor1003List2.values():
            consistsByEnd[4] += (1 if len(clientIdFor10032) == 2 else 0)

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
        self.dumpParamsMultiSelect(cursor, params)
        self.dumpParamsIsDispanser(cursor, params)
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(1000)')
        cursor.insertBlock()

        tableColumns = [
            ('25%', [u'Наименование классов и отдельных болезней', u'',                                                                     u'',                                          u'1'], CReportBase.AlignLeft),
            ('5%',  [u'№ строки',                                  u'',                                                                     u'',                                          u'2'], CReportBase.AlignLeft),
            ('16%', [u'Код по МКБ-10 пересмотра',                  u'',                                                                     u'',                                          u'3'], CReportBase.AlignLeft),
            ('6%',  [u'Зарегистрировано заболеваний',              u'всего',                                                                u'',                                          u'4'], CReportBase.AlignRight),
            ('6%',  [u'',                                          u'из них(из гр. 4):',                                                    u'в возрасте 0 - 4 года',                     u'5'], CReportBase.AlignRight),
            ('6%',  [u'',                                          u'',                                                                     u'в возрасте 5 - 9 лет',                      u'6'], CReportBase.AlignRight),
            ('6%',  [u'',                                          u'из них(из гр. 4):',                                                    u'взято под диспансерное наблюдение',         u'7'], CReportBase.AlignRight),
            ('6%',  [u'',                                          u'',                                                                     u'с впервые в жизни установленным диагнозом', u'8'], CReportBase.AlignRight),
            ('6%',  [u'',                                          u'из заболеваний с впервые в жизни установленным диагнозом (из гр. 8):', u'взято под диспансерное наблюдение',         u'9'], CReportBase.AlignRight),
            ('6%',  [u'',                                          u'',                                                                     u'выявлено при профосмотре',                  u'10'], CReportBase.AlignRight),
            ('6%',  [u'Снято с диспансерного наблюдения',          u'',                                                                     u'',                                          u'11'], CReportBase.AlignRight),
            ('6%',  [u'Состоит на д.н. на конец периода',          u'',                                                                     u'',                                          u'12'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1) # Наименование
        table.mergeCells(0, 1, 3, 1) # № стр.
        table.mergeCells(0, 2, 3, 1) # Код МКБ
        table.mergeCells(0, 3, 1, 7) # Всего
        table.mergeCells(1, 3, 2, 1) # Всего
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(1, 6, 1, 2)
        table.mergeCells(1, 7, 1, 2)
        table.mergeCells(1, 8, 1, 2)
        table.mergeCells(0, 9, 3, 1)
        table.mergeCells(0, 10, 3, 1)
        table.mergeCells(0, 11, 3, 1)

        if detailMKB:
            for row, MKB in enumerate(sorted(reportMainData.keys())):
                reportLine = reportMainData[MKB]
                reportLine[8] = reportLine[3] - reportLine[7]
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
                reportLine[8] = reportLine[3] - reportLine[7]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2] + (u' (часть)' if row == 58 else ''))
                for col in xrange(rowSize):
                    table.setText(i, 3+col, reportLine[col])
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(self.format1001(registeredAll, registeredFirst, consistsByEnd[0]))
        cursor.insertBlock()
        cursor.insertText(u'(1002) Состоит под диспансерным  наблюдением  на конец отчетного года (из стр. 1.0 гр. 12) детей в возрасте: 0 - 4 года - %d, 5 - 9 лет - %d'%(consistsByEnd[1], consistsByEnd[2]))
        cursor.insertBlock()
        cursor.insertText(u'(1003) Из числа пациентов, состоящих на конец отчетного года под диспансерным наблюдением (гр. 12): состоит под диспансерным наблюдением лиц с хроническим вирусным гепатитом (B18) и циррозом печени (K74.6) одновременно %d чел.; с хроническим вирусным гепатитом (B18) и гепатоцеллюлярным раком (C22.0) одновременно %d чел.'%(consistsByEnd[3], consistsByEnd[4]))
        cursor.insertBlock()
        cursor.insertText(u'(1004) Число лиц с болезнями системы кровообращения, взятых под диспансерное наблюдение (стр. 10.0 гр. 8) - %d, из них умерло %d.' %
            getClientCountFor1004(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params, selectData))
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(u'Дети (до 14 лет включительно).')
        cursor.insertBlock()
        cursor.insertText(u'ФАКТОРЫ, ВЛИЯЮЩИЕ НА СОСТОЯНИЕ ЗДОРОВЬЯ НАСЕЛЕНИЯ')
        cursor.insertBlock()
        cursor.insertText(u'И ОБРАЩЕНИЯ В МЕДИЦИНСКИЕ ОРГАНИЗАЦИИ (С ПРОФИЛАКТИЧЕСКОЙ ЦЕЛЬЮ)')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cursor.insertText(u'(1100)')
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


    def format1001(self, registeredAll, registeredFirst, consistsByEnd):
        return u'(1001) Число физических лиц зарегистрированных пациентов – всего - %d , из них с диагнозом , установленным впервые в жизни - %d , состоит под диспансерным наблюдением на конец отчетного года (из гр. 12, стр. 1.0) - %d .' % (registeredAll, registeredFirst, consistsByEnd)



class CStatReportF12Children0_1_2021(CStatReportF12Children0_1_2020):
    def __init__(self, parent):
        CStatReportF12Children0_1_2020.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CStatReportF12Children0_1_2020.getSetupDialog(self, parent)
        result.chkFilterExcludeLeaved.setVisible(False)
        result.chkFilterExcludeLeaved.setChecked(False)
        result.chkRegisteredInPeriod.setChecked(True)
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx( [row[2] for row in MainRowsToOneYear] )
        mapCompRows = createMapCodeToRowIdx( [row[2] for row in CompRowsToOneYear] )

        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeList = params.get('eventTypeList', None)
        orgStructureList = params.get('orgStructureList', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 1)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
        addrType = params.get('addressOrgStructureType', 0)
        addressOrgStructureId = params.get('addressOrgStructure', None)
        locality = params.get('locality', 0)
        detailMKB = params.get('detailMKB', False)
        reportLine = None

        self.resAll4 = 0
        self.res5 = 0
        self.res1011 = 0
        self.res10 = 0
        self.res1819 = 0
        self.res18 = 0
        rowSize = 16
        rowCompSize = 4
        clientIdDict = {}
        if detailMKB:
            reportMainData = {}  # { MKB: [reportLine] }
            reportCompData = {}  # { MKB: [reportLine] }
        else:
            reportMainData = [ [0]*rowSize for row in xrange(len(MainRowsToOneYear)) ]
            reportCompData = [ [0]*rowCompSize for row in xrange(len(CompRowsToOneYear)) ]
        query = selectDataToOneYear(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params)
        while query.next():
            record              = query.record()
            dayAge              = forceBool(record.value('dayAge'))
            clientAge           = forceInt(record.value('clientAge'))
            clientId            = forceRef(record.value('client_id'))
            MKB                 = normalizeMKB(forceString(record.value('MKB')))
            sickCount           = forceInt(record.value('sickCount'))
            diseaseCharacter    = forceString(record.value('diseaseCharacter'))
            diagnosisType       = forceString(record.value('diagnosisType'))
            firstInPeriod       = forceBool(record.value('firstInPeriod'))
            closedEvent         = forceBool(record.value('closedEvent'))
            getObserved         = forceBool(record.value('getObserved'))
            observed            = forceBool(record.value('observed'))
            getRemovingObserved = forceBool(record.value('getRemovingObserved'))
            getProfilactic      = forceBool(record.value('getProfilactic'))
            getAdultsDispans    = forceBool(record.value('getAdultsDispans'))
            isNotPrimary        = forceBool(record.value('isNotPrimary'))

            cols = [0]
            if clientAge >= 0 and clientAge < 1:
                cols.append(1)
            elif clientAge >= 1 and clientAge < 3:
                cols.append(2)
            if dayAge:
                cols.append(3)
            if diseaseCharacter == '1': # острое
                if getObserved:
                    if clientAge >= 0 and clientAge < 1:
                        cols.append(8)
                    elif clientAge >= 1 and clientAge < 3:
                        cols.append(9)
                if getAdultsDispans:
                    if clientAge >= 0 and clientAge < 1:
                        cols.append(10)
                    elif clientAge >= 1 and clientAge < 3:
                        cols.append(11)
            elif firstInPeriod:
                if clientAge >= 0 and clientAge < 1:
                    cols.append(6)
                elif clientAge >= 1 and clientAge < 3:
                    cols.append(7)
                if getObserved:
                    if clientAge >= 0 and clientAge < 1:
                        cols.append(8)
                    elif clientAge >= 1 and clientAge < 3:
                        cols.append(9)
                if getAdultsDispans:
                    if clientAge >= 0 and clientAge < 1:
                        cols.append(10)
                    elif clientAge >= 1 and clientAge < 3:
                        cols.append(11)
            if getObserved:
                if clientAge >= 0 and clientAge < 1:
                    cols.append(4)
                elif clientAge >= 1 and clientAge < 3:
                    cols.append(5)
            if getRemovingObserved:
                if clientAge >= 0 and clientAge < 1:
                    cols.append(12)
                elif clientAge >= 1 and clientAge < 3:
                    cols.append(13)
            if observed:
                if clientAge >= 0 and clientAge < 1:
                    cols.append(14)
                elif clientAge >= 1 and clientAge < 3:
                    cols.append(15)


            if detailMKB:
                reportLine = reportMainData.setdefault(MKB, [0]*rowSize)
                self.processReportLine(row, reportLine, clientId, clientIdDict, cols, sickCount)
            else:
                for row in mapMainRows.get(MKB, []):
                    reportLine = reportMainData[row]
                    self.processReportLine(row, reportLine, clientId, clientIdDict, cols, sickCount)

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
        self.dumpParamsMultiSelect(cursor, params)
        self.dumpParamsIsDispanser(cursor, params)
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(1500)')
        cursor.insertBlock()

        tableColumns = [
            ('12%', [u'Наименование классов и отдельных болезней',                    u'',                                                                           u'',                                          u'',              u'1'], CReportBase.AlignLeft),
            ('3%',  [u'№ строки',                                                     u'',                                                                           u'',                                          u'',              u'2'], CReportBase.AlignLeft),
            ('5%',  [u'Код по МКБ-10 пересмотра',                                     u'',                                                                           u'',                                          u'',              u'3'], CReportBase.AlignLeft),
            ('5%',  [u'Зарегистрировано заболеваний',                                 u'Всего в возрасте от 0 до 3 лет',                                             u'',                                          u'',              u'4'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'из них(из гр. 4):',                                                          u'',                                          u'до 1 года',     u'5'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'6'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'до 1 мес.',     u'7'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'из них (из гр. 5 и 6):',                                                     u'взято под диспансерное наблюдение',         u'до 1 года',     u'8'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'9'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'с впервые в жизни установленным диагнозом', u'до 1 года',     u'10'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'11'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'из заболеваний с впервые в жизни установленным диагнозом (из гр. 10 и 11):', u'взято под диспансерное наблюдение',         u'до 1 года',     u'12'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'13'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'выявлено при профосмотре',                  u'до 1 года',     u'14'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'15'], CReportBase.AlignRight),
            ('5%',  [u'Снято с диспансерного наблюдения',                             u'',                                                                           u'',                                          u'до 1 года',     u'16'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'17'], CReportBase.AlignRight),
            ('5%',  [u'Состоит под диспансерным наблюдением на конец отчетного года', u'',                                                                           u'',                                          u'до 1 года',     u'18'], CReportBase.AlignRight),
            ('5%',  [u'',                                                             u'',                                                                           u'',                                          u'от 1 до 3 лет', u'19'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1) # Наименование
        table.mergeCells(0, 1, 4, 1) # № стр.
        table.mergeCells(0, 2, 4, 1) # Код МКБ
        table.mergeCells(0, 3, 1, 12) # Всего
        table.mergeCells(1, 3, 3, 1) # Всего
        table.mergeCells(1, 4, 2, 3)
        table.mergeCells(1, 7, 1, 4)
        table.mergeCells(2, 7, 1, 2)
        table.mergeCells(2, 9, 1, 2)
        table.mergeCells(1, 11, 1, 4)
        table.mergeCells(2, 11, 1, 2)
        table.mergeCells(2, 13, 1, 2)
        table.mergeCells(0, 15, 3, 2)
        table.mergeCells(0, 17, 3, 2)

        self.res1819 = 0
        self.res18 = 0
        if detailMKB:
            for row, MKB in enumerate(sorted(reportMainData.keys())):
                reportLine = reportMainData[MKB]
                reportLine[14] = reportLine[4] - reportLine[12]
                reportLine[15] = reportLine[5] - reportLine[13]
                self.res1819 += reportLine[14] + reportLine[15]
                self.res18 += reportLine[14]
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
            for row, rowDescr in enumerate(MainRowsToOneYear):
                reportLine = reportMainData[row]
                reportLine[14] = reportLine[4] - reportLine[12]
                reportLine[15] = reportLine[5] - reportLine[13]
                self.res1819 += reportLine[14] + reportLine[15]
                self.res18 += reportLine[14]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2] + (u' (часть)' if row == 58 else ''))
                for col in xrange(rowSize):
                    table.setText(i, 3+col, reportLine[col])
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertText(u'(1601) Число физических лиц зарегистрированных пациентов в возрасте до 3 лет – всего %d, из них в возрасте до 1 года %d, из них (из стр. 1) с диагнозом, установленным впервые в жизни %d, из них в возрасте до 1 года %d, состоит под диспансерным наблюдением на конец отчетного года детей в возрасте до 3 лет (из гр. 18 и 19 стр. 1.0) %d, из них в возрасте до 1 года %d.'%(self.resAll4, self.res5, self.res1011, self.res10, self.res1819, self.res18))
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.insertText(u'Факторы, влияющие на состояние здоровья населения и обращения в медицинские организации (с профилактической и иными целями)')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cursor.insertText(u'(1600)')
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
        resH90H91 = 0
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
                if MKB == u'Z82.2':
                    resH90H91 += reportLine[0]
        else:
            for row, rowDescr in enumerate(CompRowsToOneYear):
                reportLine = reportCompData[row]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2])
                table.setText(i, 3, reportLine[0])
                table.setText(i, 4, reportLine[1])
                table.setText(i, 5, reportLine[2])
                if rowDescr[1] == u'1.7.1.1':
                    resH90H91 += reportLine[0]

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertText(u'(1650) Из стр.1.7.1.1. таблицы 1600: обследовано на выявление кондуктивной и нейросенсорной потери слуха - %d.'%(resH90H91))
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End)
        return doc
