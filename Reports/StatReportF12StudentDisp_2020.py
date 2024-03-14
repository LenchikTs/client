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
from PyQt4.QtCore import QDate

from library.database import addDateInRange
from library.MapCode import createMapCodeToRowIdx
from library.Utils import forceBool, forceDate, forceInt, forceRef, forceString, calcAgeInYears
from Reports.Report import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportPersonSickList import addAddressCond, addAttachCond
from Reports.ReportAcuteInfections import CReportAcuteInfectionsSetupDialog, getFilterAddress
from Orgs.Utils import getOrgStructureDescendants, getOrgStructureListDescendants, getOrgStructures, \
    getOrgStructureAddressIdList


def selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList, personId, sex,
               ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure, addrType,
               addressOrgStructureId, locality, params):
    stmt = """
            SELECT
               Event.id,
               Diagnosis.MKB AS MKB,
               count(*) AS sickCount,
               rbDiseaseCharacter.code AS diseaseCharacter,
               rbDiagnosisType.code AS diagnosisType,
               IF(rbDispanser.code = 2 OR rbDispanser.code = 6, 1, 0) AS getObserved,
              Client.sex AS sex,
              Client.birthDate AS birthDate,
              IF(Event.result_id, 1, 0) AS closedEvent,
              IF(rbDispanser.code = 3 OR rbDispanser.code = 4 OR rbDispanser.code = 5, 1, 0) AS getRemovingObserved,
              ((Diagnosis.setDate<= %(endDate)s AND Diagnosis.setDate IS NOT NULL) 
              AND (Diagnosis.setDate>= %(begDate)s )) AS firstInPeriod,
            
              IF(rbDispanser.code = 1, 1, 0) AS observed,
            
              if(rbMedicalAidType.regionalCode in ('262', '261'),1,0) AS getProfilactic,
              IF(Event.isPrimary = 2, 1, 0) AS isNotPrimary,
              if(rbMedicalAidType.regionalCode in ('232','252', '211'),1,0) AS getAdultsDispans
            
            FROM Event
            
            LEFT JOIN Diagnostic ON Event.id = Diagnostic.event_id AND Diagnostic.event_id = (SELECT MAX(dc.event_id) FROM Diagnostic dc
            LEFT JOIN Diagnosis ds  ON dc.diagnosis_id=ds.id
            WHERE Diagnosis.client_id = ds.client_id AND Diagnosis.MKB = ds.MKB)
            LEFT JOIN Diagnosis ON Diagnostic.diagnosis_id=Diagnosis.id
            
            LEFT JOIN Person ON Event.execPerson_id = Person.id
            
            LEFT JOIN Client ON Client.id = Diagnosis.client_id
            LEFT JOIN ClientSocStatus ON ClientSocStatus.client_id = Client.id
            LEFT JOIN rbSocStatusType ON rbSocStatusType.id = ClientSocStatus.socStatusType_id 
            AND rbSocStatusType.code IN ('с04', 'с03')
            
            LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
            LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
            
              INNER JOIN EventType ON EventType.id = Event.eventType_id
              LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
            
            WHERE Diagnostic.diagnosisType_id  IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT 
            WHERE RBDT.code = '1' OR RBDT.code = '2')
            AND Diagnostic.deleted=0 AND Client.deleted=0 AND Diagnosis.deleted=0 AND Event.deleted=0
              AND Event.execDate BETWEEN %(begDate)s AND %(endDate)s
              AND Diagnosis.MKB IS NOT NULL AND Diagnosis.MKB!=''
            AND %(cond)s
            GROUP BY MKB, diseaseCharacter, sex, firstInPeriod, getObserved, getRemovingObserved, getProfilactic, 
            isNotPrimary, observed, getAdultsDispans, rbDiagnosisType.id
    """
    db = QtGui.qApp.db
    tableDiagnosis = db.table('Diagnosis')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableOrgStructureAddress = db.table('OrgStructure_Address')
    tableAddress = db.table('Address')
    specialityId = params.get('specialityId', None)

    cond = []

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                      tableDiagnostic['deleted'].eq(0)
                      ]

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
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureIdList:
        if not isPersonPost and not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))

    if eventTypeIdList:
        tableEventType = db.table('EventType')
        cond.append(tableEventType['id'].inlist(eventTypeIdList))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        diagnosticCond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    if orgStructureIdList:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('age(Client.birthDate, Event.setDate) BETWEEN %(ageFrom)s and %(ageTo)s' % dict(ageFrom=ageFrom,
                                                                                                        ageTo=ageTo))
    if socStatusTypeId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                   + 'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                   + 'ClientSocStatus.socStatusType_id=%d' % socStatusTypeId)
        cond.append('EXISTS(' + subStmt + ')')
    elif socStatusClassId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                   + 'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                   + 'ClientSocStatus.socStatusClass_id=%d' % socStatusClassId)
        cond.append('EXISTS(' + subStmt + ')')

    stmtAddress = ''
    if isFilterAddressOrgStructure:
        addrIdList = None
        cond2 = []
        if (addrType + 1) & 1:
            addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            cond2 = addAddressCond(db, cond2, 0, addrIdList)
        if (addrType + 1) & 2:
            if addrIdList is None:
                addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            cond2 = addAddressCond(db, cond2, 1, addrIdList)
        if ((addrType + 1) & 4):
            if addressOrgStructureId:
                cond2 = addAttachCond(db, cond2, 'orgStructure_id = %d' % addressOrgStructureId, 1, None)
            else:
                cond2 = addAttachCond(db, cond2, 'LPU_id=%d' % QtGui.qApp.currentOrgId(), 1, None)
        if cond2:
            cond.append(db.joinOr(cond2))
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality - 1))
    filterAddress = params.get('isFilterAddress', False)
    if filterAddress:
        if not stmtAddress:
            stmtAddress = u'''INNER JOIN ClientAddress ON ClientAddress.client_id = Client.id
                              INNER JOIN Address ON Address.id = ClientAddress.address_id
                              INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        else:
            stmtAddress += u''' INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        cond.append('ClientAddress.id IN (%s)' % (getFilterAddress(params)))
    if 'attachTo' in params:
        attachOrgId = params['attachTo']
        if attachOrgId:
            cond = addAttachCond(db, cond, 'LPU_id=%d' % attachOrgId,
                                 *params.get('attachType', (0, None, QDate(), QDate())))
    elif 'attachToNonBase' in params:
        cond = addAttachCond(db, cond, 'LPU_id!=%d' % QtGui.qApp.currentOrgId(),
                             *params.get('attachType', (0, None, QDate(), QDate())))
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
                       WHERE CA2.deleted=0 AND %s))''' % (
        QtGui.qApp.db.joinAnd(outerCond), QtGui.qApp.db.joinAnd(innerCond)))
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
        cond.append(u'''EXISTS(SELECT MAX(rbDispanser.observed)
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
              AND  D2.endDate >= %s
              AND  D2.endDate < %s))''' % (
        tableDiagnosis['setDate'].formatValue(begDate), tableDiagnosis['setDate'].formatValue(endDate.addDays(1))))
    st = stmt % {'begDate': db.formatDate(begDate),
                 'endDate': db.formatDate(endDate),
                 'cond': db.joinAnd(cond)
                 }
    return db.query(st)


def selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeIdList, orgStructureIdList,
                     personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, isFilterAddressOrgStructure,
                     addrType, addressOrgStructureId, locality, params, boolThyroidosData=False, fewMKB=None):
    if boolThyroidosData:
        stmt = """
            SELECT
               Diagnosis.client_id,
               Client.deathDate AS begDateDeath
            
            FROM Event
            LEFT JOIN Person ON Event.execPerson_id = Person.id
            LEFT JOIN Diagnostic ON Event.id = Diagnostic.event_id
            LEFT JOIN Diagnosis ON Diagnostic.diagnosis_id=Diagnosis.id
            LEFT JOIN Client ON Client.id = Diagnosis.client_id
            LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
            LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
            
            WHERE Diagnostic.diagnosisType_id  IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT 
            WHERE RBDT.code = '1' OR RBDT.code = '2')
            AND Diagnostic.deleted=0 AND Client.deleted=0 AND Diagnosis.deleted=0 AND Event.deleted=0
              AND Event.execDate BETWEEN %(begDate)s AND %(endDate)s
              AND Diagnosis.MKB IS NOT NULL AND Diagnosis.MKB!=''
    """
    elif fewMKB:
        stmt = """
                SELECT
                   Diagnosis.client_id,
                   Diagnosis.MKB,
                   rbDiseaseCharacter.code AS diseaseCharacter,
                   ((Diagnosis.setDate<= %(endDate)s AND Diagnosis.setDate IS NOT NULL) 
                   AND (Diagnosis.setDate>= %(begDate)s )) AS firstInPeriod,
                   IF(rbDispanser.code = 1, 1, 0) AS observed,
                   age(Client.birthDate, Event.setDate) AS clientAge
        
                FROM Event
                LEFT JOIN Person ON Event.execPerson_id = Person.id
                LEFT JOIN Diagnostic ON Event.id = Diagnostic.event_id
                LEFT JOIN Diagnosis ON Diagnostic.diagnosis_id=Diagnosis.id
                LEFT JOIN Client ON Client.id = Diagnosis.client_id
                LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
        
                WHERE Diagnostic.diagnosisType_id  IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT 
                WHERE RBDT.code = '1' OR RBDT.code = '2')
                AND Diagnostic.deleted=0 AND Client.deleted=0 AND Diagnosis.deleted=0 AND Event.deleted=0
                  AND DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s
                  and %(cond)s
        
                ORDER BY firstInPeriod DESC, observed DESC
            """
    else:
        stmt = """
                SELECT
                   Diagnosis.client_id,
                   rbDiseaseCharacter.code AS diseaseCharacter,
                   ((Diagnosis.setDate<= %(endDate)s AND Diagnosis.setDate IS NOT NULL) 
                   AND (Diagnosis.setDate>= %(begDate)s )) AS firstInPeriod,
                   IF(rbDispanser.code = 1, 1, 0) AS observed
                
                FROM Event
                LEFT JOIN Person ON Event.execPerson_id = Person.id
                LEFT JOIN Diagnostic ON Event.id = Diagnostic.event_id
                LEFT JOIN Diagnosis ON Diagnostic.diagnosis_id=Diagnosis.id
                LEFT JOIN Client ON Client.id = Diagnosis.client_id
                LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
                
                WHERE Diagnostic.diagnosisType_id  IN (SELECT RBDT.id FROM rbDiagnosisType AS RBDT 
                WHERE RBDT.code = '1' OR RBDT.code = '2')
                AND Diagnostic.deleted=0 AND Client.deleted=0 AND Diagnosis.deleted=0 AND Event.deleted=0
                  AND Event.execDate BETWEEN %(begDate)s AND %(endDate)s
                  AND Diagnosis.MKB IS NOT NULL AND Diagnosis.MKB!=''
                GROUP BY Diagnosis.client_id
                ORDER BY firstInPeriod DESC, observed DESC
    """
    db = QtGui.qApp.db
    tableDiagnosis = db.table('Diagnosis')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableOrgStructureAddress = db.table('OrgStructure_Address')
    tableAddress = db.table('Address')
    specialityId = params.get('specialityId', None)

    cond = []

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                      tableDiagnostic['deleted'].eq(0)
                      ]

    if fewMKB:
        cond.append('Diagnosis.MKB IN {0}'.format(fewMKB))
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
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureIdList:
        if not isPersonPost and not specialityId:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
            diagnosticCond.append(tablePerson['deleted'].eq(0))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))

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
    if orgStructureIdList:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureListDescendants(orgStructureIdList)))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('age(Client.birthDate, Event.setDate) BETWEEN "%(ageFrom)s" and "%(ageTo)s"' % dict(ageFrom=ageFrom,
                                                                                                        ageTo=ageTo))
    if socStatusTypeId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                   + 'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                   + 'ClientSocStatus.socStatusType_id=%d' % socStatusTypeId)
        cond.append('EXISTS(' + subStmt + ')')
    elif socStatusClassId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                   + 'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                   + 'ClientSocStatus.socStatusClass_id=%d' % socStatusClassId)
        cond.append('EXISTS(' + subStmt + ')')

    stmtAddress = ''
    if isFilterAddressOrgStructure:
        addrIdList = None
        cond2 = []
        if (addrType + 1) & 1:
            addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            cond2 = addAddressCond(db, cond2, 0, addrIdList)
        if (addrType + 1) & 2:
            if addrIdList is None:
                addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            cond2 = addAddressCond(db, cond2, 1, addrIdList)
        if ((addrType + 1) & 4):
            if addressOrgStructureId:
                cond2 = addAttachCond(db, cond2, 'orgStructure_id = %d' % addressOrgStructureId, 1, None)
            else:
                cond2 = addAttachCond(db, cond2, 'LPU_id=%d' % QtGui.qApp.currentOrgId(), 1, None)
        if cond2:
            cond.append(db.joinOr(cond2))
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality - 1))
    filterAddress = params.get('isFilterAddress', False)
    if filterAddress:
        if not stmtAddress:
            stmtAddress = u'''INNER JOIN ClientAddress ON ClientAddress.client_id = Client.id
                                  INNER JOIN Address ON Address.id = ClientAddress.address_id
                                  INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        else:
            stmtAddress += u''' INNER JOIN AddressHouse ON AddressHouse.id = Address.house_id'''
        cond.append('ClientAddress.id IN (%s)' % (getFilterAddress(params)))
    if 'attachTo' in params:
        attachOrgId = params['attachTo']
        if attachOrgId:
            cond = addAttachCond(db, cond, 'LPU_id=%d' % attachOrgId,
                                 *params.get('attachType', (0, None, QDate(), QDate())))
    elif 'attachToNonBase' in params:
        cond = addAttachCond(db, cond, 'LPU_id!=%d' % QtGui.qApp.currentOrgId(),
                             *params.get('attachType', (0, None, QDate(), QDate())))
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
                           WHERE CA2.deleted=0 AND %s))''' % (
            QtGui.qApp.db.joinAnd(outerCond), QtGui.qApp.db.joinAnd(innerCond)))
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
        cond.append(u'''EXISTS(SELECT MAX(rbDispanser.observed)
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
                  AND  D2.endDate >= %s
                  AND  D2.endDate < %s))''' % (
            tableDiagnosis['setDate'].formatValue(begDate), tableDiagnosis['setDate'].formatValue(endDate.addDays(1))))
    st = stmt % {'begDate': db.formatDate(begDate),
                 'endDate': db.formatDate(endDate),
                 'cond': db.joinAnd(cond)
                 }
    return db.query(st)


class CStatReportF12StudentDisp_2020(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        title = u'Ф.12. 6.Диспансеризация студентов высших учебных учреждений.'
        self.setTitle(title, title)

    def getDefaultParams(self):
        result = CReport.getDefaultParams(self)
        result['ageFrom'] = 15
        result['ageTo'] = 25
        return result

    def dumpParamsMultiSelect(self, cursor, params):
        description = []
        eventTypeList = params.get('eventTypeList', None)
        if eventTypeList:
            db = QtGui.qApp.db
            tableET = db.table('EventType')
            records = db.getRecordList(tableET, [tableET['name']],
                                       [tableET['deleted'].eq(0), tableET['id'].inlist(eventTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            description.append(u'тип события:  %s' % (u','.join(name for name in nameList if name)))
        else:
            description.append(u'тип события:  не задано')
        orgStructureList = params.get('orgStructureList', None)
        if orgStructureList:
            if len(orgStructureList) == 1 and not orgStructureList[0]:
                description.append(u'подразделение: ЛПУ')
            else:
                db = QtGui.qApp.db
                table = db.table('OrgStructure')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(orgStructureList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                description.append(u'подразделение:  %s' % (u','.join(name for name in nameList if name)))
        else:
            description.append(u'подразделение: ЛПУ')
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)

    def dumpParamsIsDispanser(self, cursor, params):
        description = []
        isDispanser = params.get('isDispanser', False)
        if isDispanser:
            description.append(u'Учитывать только состоящих на диспансерном наблюдении')
            columns = [('100%', [], CReportBase.AlignLeft)]
            table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2,
                                cellSpacing=0)
            for i, row in enumerate(description):
                table.setText(i, 0, row)
            cursor.movePosition(QtGui.QTextCursor.End)

    def getSetupDialog(self, parent):
        result = CReportAcuteInfectionsSetupDialog(parent)
        result.setAreaEnabled(False)
        result.setFilterAddressOrgStructureVisible(False)
        result.setAllAddressSelectable(False)
        result.setAllAttachSelectable(False)
        result.setUseInputDate(False)
        result.setPersonPostEnabled(False)
        result.lblEventPurpose.setVisible(False)
        result.lblPerson.setVisible(False)
        result.cmbPerson.setVisible(False)
        result.chkFilterAddress.setVisible(False)
        result.cmbFilterAddressType.setVisible(False)
        result.cmbFilterAddressCity.setVisible(False)
        result.cmbFilterAddressOkato.setVisible(False)
        result.cmbFilterAddressStreet.setVisible(False)
        result.lblFilterAddressHouse.setVisible(False)
        result.edtFilterAddressHouse.setVisible(False)
        result.lblFilterAddressCorpus.setVisible(False)
        result.edtFilterAddressCorpus.setVisible(False)
        result.lblFilterAddressFlat.setVisible(False)
        result.edtFilterAddressFlat.setVisible(False)
        result.cmbEventPurpose.setVisible(False)
        result.lblSocStatusClass.setVisible(False)
        result.cmbSocStatusClass.setVisible(False)
        result.lblSocStatusType.setVisible(False)
        result.cmbSocStatusType.setVisible(False)
        result.cmbFinance.setVisible(False)
        result.cmbOrgStructure.setVisible(False)
        result.chkFilterDead.setVisible(True)
        result.chkFilterDeathBegDate.setVisible(True)
        result.chkFilterDeathEndDate.setVisible(True)
        result.edtFilterDeathBegDate.setVisible(True)
        result.edtFilterDeathEndDate.setVisible(True)
        result.setRegisteredInPeriod(False)
        result.setEventTypeListListVisible(True)
        result.setOrgStructureListVisible(True)
        result.setSpecialityVisible(False)
        result.setCMBEventTypeVisible(False)
        result.setCMBOrgStructureVisible(False)
        result.setChkFilterDispanser(False)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                # if itemposition != (48, 0, 1, 1) and itemposition != (1, 2, 1, 2) and itemposition != (0, 2, 1, 2):
                #     result.gridLayout.removeItem(spacer)
        result.resize(100, 100)
        return result

    def build(self, params):

        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeList = params.get('eventTypeList', None)
        orgStructureList = params.get('orgStructureList', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 15)
        ageTo = params.get('ageTo', 30)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
        addrType = params.get('addressOrgStructureType', 0)
        addressOrgStructureId = params.get('addressOrgStructure', None)
        locality = params.get('locality', 0)
        reportLine = None

        query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList,
                           personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,
                           isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params)

        age17andObserved = 0
        count = 0
        countProfilactic = 0
        countFirstInPeriod = 0
        countGetObserved = 0


        while query.next():
            record = query.record()
            clientId = forceRef(record.value('client_id'))
            MKB = normalizeMKB(forceString(record.value('MKB')))
            sickCount = forceInt(record.value('sickCount'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            diagnosisType = forceString(record.value('diagnosisType'))
            sex = forceInt(record.value('sex'))
            birthDate = forceDate(record.value('birthDate'))
            age = forceInt(calcAgeInYears(birthDate, begDate))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            closedEvent = forceBool(record.value('closedEvent'))
            getObserved = forceInt(record.value('getObserved'))
            observed = forceBool(record.value('observed'))
            getRemovingObserved = forceBool(record.value('getRemovingObserved'))
            getProfilactic = forceBool(record.value('getProfilactic'))
            isNotPrimary = forceBool(record.value('isNotPrimary'))
            getAdultsDispans = forceBool(record.value('getAdultsDispans'))

            if age == 17 and (observed or getObserved):
                age17andObserved += 1
            if observed or getObserved:
                count += 1
                if getProfilactic:
                    countProfilactic += 1
                    if (firstInPeriod and diseaseCharacter == '2') or diseaseCharacter == '1':
                        countFirstInPeriod += 1
                        if getObserved:
                            countGetObserved += 1


        registeredAll = 0
        registeredFirst = 0
        consistsByEnd = 0
        thyroidosUnhangAll = 0
        thyroidosUnhangRecovery = 0
        thyroidosUnhangDeath = 0
        clientIdList = []
        clientIdForThyroidosList = []
        queryClient = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList,
                                       orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId,
                                       socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId,
                                       locality, params)
        while queryClient.next():
            record = queryClient.record()
            clientId = forceRef(record.value('client_id'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            observed = forceBool(record.value('observed'))

            if clientId and clientId not in clientIdList:
                clientIdList.append(clientId)
                registeredAll += 1
                if observed:
                    consistsByEnd += 1
                if firstInPeriod:
                    registeredFirst += 1

        queryFewMKB = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList,
                                       orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId,
                                       socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId,
                                       locality, params,
                                       fewMKB="('B18.0', 'B18.1', 'B18.2', 'B18.2', 'B18.8', 'B18.9', 'C22.0', 'K74.6')")
        MKBDictC22 = {}
        MKBDictK76 = {}
        while queryFewMKB.next():
            record = queryFewMKB.record()
            clientId = forceRef(record.value('client_id'))
            MKB = forceString(record.value('MKB'))
            observed = forceBool(record.value('observed'))
            clientAge = forceInt(record.value('clientAge'))
            if observed and clientAge >= ageFrom and clientAge <= ageTo:
                if MKB in ['B18.0', 'B18.1', 'B18.2', 'B18.2', 'B18.8', 'B18.9']:
                    if MKBDictC22.has_key(clientId):
                        list = MKBDictC22[clientId]
                        list.append('B18.0')
                        MKBDictC22[clientId] = list
                    else:
                        MKBDictC22[clientId] = ['B18.0']
                    if MKBDictK76.has_key(clientId):
                        list = MKBDictK76[clientId]
                        list.append('B18.0')
                        MKBDictK76[clientId] = list
                    else:
                        MKBDictK76[clientId] = ['B18.0']

                if MKB == 'C22.0':
                    if MKBDictC22.has_key(clientId):
                        list = MKBDictC22[clientId]
                        list.append(MKB)
                        MKBDictC22[clientId] = list
                    else:
                        MKBDictC22[clientId] = [MKB]

                if MKB == 'K74.6':
                    if MKBDictK76.has_key(clientId):
                        list = MKBDictK76[clientId]
                        list.append(MKB)
                        MKBDictK76[clientId] = list
                    else:
                        MKBDictK76[clientId] = [MKB]

        for key in MKBDictC22.keys():
            MKBDictC22[key] = set(MKBDictC22[key])
            if len(MKBDictC22[key]) < 2:
                MKBDictC22.pop(key)
        B18C22 = len(MKBDictC22)
        for key in MKBDictK76.keys():
            MKBDictK76[key] = set(MKBDictK76[key])
            if len(MKBDictK76[key]) < 2:
                MKBDictK76.pop(key)
        B18K76 = len(MKBDictK76)

        queryThyroidos = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList,
                                          orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId,
                                          socStatusTypeId, isFilterAddressOrgStructure, addrType, addressOrgStructureId,
                                          locality, params, True)
        while queryThyroidos.next():
            record = queryThyroidos.record()
            clientId = forceRef(record.value('client_id'))
            if clientId and clientId not in clientIdForThyroidosList:
                clientIdForThyroidosList.append(clientId)
                thyroidosUnhangAll += 1
                deathDate = forceDate(record.value('begDateDeath'))
                if deathDate and (begDate <= deathDate and deathDate <= endDate):
                    thyroidosUnhangDeath += 1
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
        self.dumpParamsIsDispanser(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(
            u'''(5000) Число студентов, подлежавших диспансеризации в отчетном году {0}, число студентов, прошедших диспансеризацию в отчетном году {1}, выявлено у них заболеваний с диагнозом, установленным впервые в жизни - всего {2}, из них: взято под диспансерное наблюдение {3}'''.format(count, countProfilactic, countFirstInPeriod, countGetObserved))
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(
            u'''(5100) Профилактические медицинские осмотры обучающихся в общеобразовательных организациях и профессиональных образовательных организациях, а также образовательных организациях высшего образования в целях раннего выявления незаконного потребления наркотических средств и психотропных веществ: подлежало осмотру______, осмотрено_______''')
        cursor.insertBlock()

        return doc