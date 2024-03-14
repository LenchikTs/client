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

from library.Utils      import forceDate, forceInt, forceString

from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from Reports.ReportPersonSickList import CReportPersonSickListSetupDialog


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    eventPurposeId = params.get('eventPurposeId', None)
    eventTypeId = params.get('eventTypeId', None)
    orgStructureId = params.get('orgStructureId', None)
    specialityId = params.get('specialityId', None)
    chkTraumaType = params.get('chkTraumaType', False)
    chkTraumaTypeAny = params.get('chkTraumaTypeAny', False)
    traumaTypeId = params.get('traumaTypeId', None)
    personId = params.get('personId', None)
    workOrgId = params.get('workOrgId', None)
    sex = params.get('sex', 0)
    ageFrom = params.get('ageFrom', 0)
    ageTo = params.get('ageTo', 150)
    MKBFilter = params.get('MKBFilter', 0)
    MKBFrom = params.get('MKBFrom', 'A00')
    MKBTo = params.get('MKBTo', 'Z99.9')
    phaseId = params.get('phaseId', None)
    MKBExFilter = params.get('MKBExFilter', 0)
    MKBExFrom = params.get('MKBExFrom', 'A00')
    MKBExTo = params.get('MKBExTo', 'Z99.9')
    phaseIdEx = params.get('phaseIdEx', None)
    diseaseCharacterCodes = classToCodes(params.get('characterClass', 0))
    onlyFirstTime = params.get('onlyFirstTime', False)
    accountAccomp = params.get('accountAccomp', False)
    locality = params.get('locality', 0)
    stmt="""
SELECT
    Diagnosis.client_id,
    Diagnosis.id AS diagnosis_id,
    Diagnosis.MKB,
    Diagnosis.MKBEx,
    Diagnosis.setDate,
    Diagnosis.endDate,
    rbDiseaseCharacter.code AS diseaseCharacter,
    rbTraumaType.name AS traumaType,
    DATE(Diagnostic.endDate) AS diagnosticDate,
    Diagnostic.hospital AS diagnosticHospital,
    Diagnostic.sanatorium AS diagnosticSanatorium,
    rbDispanser.name AS diagnosticDispanser,
    vrbPersonWithSpeciality.name AS diagnosticPerson,
    Event.setDate AS setDateEvent,
    Event.execDate AS execDateEvent,
    Organisation.shortName AS ORGRelegate,
    ORG.shortName AS ORGClient,
    Client.birthDate,
    Client.lastName,
    Client.firstName,
    Client.patrName
FROM Diagnosis
LEFT JOIN Client ON Client.id = Diagnosis.client_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
LEFT JOIN rbTraumaType ON rbTraumaType.id = Diagnosis.traumaType_id
LEFT JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id
LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnostic.diagnosisType_id
LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Diagnostic.person_id
LEFT JOIN Event      ON Event.id = Diagnostic.event_id
LEFT JOIN EventType  ON EventType.id = Event.eventType_id
LEFT JOIN Organisation  ON (Organisation.id = Event.relegateOrg_id AND Organisation.deleted = 0)
LEFT JOIN ClientAttach ON ClientAttach.client_id = Client.id
LEFT JOIN Organisation AS ORG ON (ORG.id = ClientAttach.LPU_id AND ORG.deleted = 0)
LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
WHERE
    %s
ORDER BY
    Client.lastName, Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.id,
    Diagnosis.MKB, Diagnosis.MKBEx, Event.setDate
"""
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableClient = db.table('Client')
    tablePerson = db.table('vrbPersonWithSpeciality')
    tableDiagnostic = db.table('Diagnostic')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableEvent  = db.table('Event')
    cond = ['''(ClientAttach.deleted=0 AND LPU_id!=%d AND rbAttachType.outcome=0
    AND ClientAttach.id = (SELECT MAX(CA2.id)
    FROM ClientAttach AS CA2
    LEFT JOIN rbAttachType AS rbAttachType2 ON rbAttachType2.id = CA2.attachType_id
    WHERE CA2.deleted=0 AND CA2.client_id = Client.id AND rbAttachType2.temporary=0))'''%(QtGui.qApp.currentOrgId())]
    cond.append(u'''(Diagnosis.id IS NOT NULL AND Diagnosis.deleted = 0) OR Diagnosis.id IS NULL''')
    cond.append(u'''(Diagnostic.id IS NOT NULL AND Diagnostic.deleted = 0) OR Diagnostic.id IS NULL''')
    cond.append(tableDiagnosis['mod_id'].isNull())
    cond.append(tableDiagnostic['setDate'].le(endDate))
    cond.append(db.joinOr([tableDiagnostic['endDate'].ge(begDate), tableDiagnostic['endDate'].isNull()]))
    cond.append(tableEvent['deleted'].eq(0))
    cond.append(tableClient['deleted'].eq(0))
    cond.append(tableDiagnosis['deleted'].eq(0))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        cond.append(db.table('EventType')['purpose_id'].eq(eventPurposeId))
    if onlyFirstTime:
        cond.append(tableDiagnosis['setDate'].le(endDate))
        cond.append(tableDiagnosis['setDate'].ge(begDate))
    else:
        cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), tableDiagnosis['setDate'].le(endDate)]))
        cond.append(db.joinOr([tableDiagnosis['endDate'].ge(begDate), tableDiseaseCharacter['code'].eq('3')]))
    if MKBFilter == 1:
        cond.append(tableDiagnosis['MKB'].ge(MKBFrom))
        cond.append(tableDiagnosis['MKB'].le(MKBTo))
        if phaseId:
            phaseCond = [tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                         tableDiagnostic['deleted'].eq(0),
                         tableDiagnostic['phase_id'].eq(phaseId)]
            cond.append(db.existsStmt(tableDiagnostic, phaseCond))
    if MKBExFilter == 1:
        cond.append(tableDiagnosis['MKBEx'].ge(MKBExFrom))
        cond.append(tableDiagnosis['MKBEx'].le(MKBExTo))
        if phaseIdEx:
            phaseCondEx = [tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                           tableDiagnostic['deleted'].eq(0),
                           tableDiagnostic['phase_id'].eq(phaseIdEx)]
            cond.append(db.existsStmt(tableDiagnostic, phaseCondEx))
    if personId:
        cond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if chkTraumaType:
        if chkTraumaTypeAny:
            cond.append(tableDiagnosis['traumaType_id'].isNotNull())
        elif traumaTypeId:
            cond.append(tableDiagnosis['traumaType_id'].eq(traumaTypeId))
        else:
            cond.append(tableDiagnosis['traumaType_id'].isNull())
    if workOrgId:
        cond.append('EXISTS (SELECT * FROM ClientWork WHERE ClientWork.id = (SELECT MAX(id) FROM ClientWork AS CW WHERE CW.client_id = Client.id) and ClientWork.org_id=%d)' % (workOrgId))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Diagnosis.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if diseaseCharacterCodes:
        if diseaseCharacterCodes != [None]:
            cond.append(tableDiseaseCharacter['code'].inlist(diseaseCharacterCodes))
        else:
            cond.append(tableDiseaseCharacter['code'].isNull())
    if not accountAccomp:
        tableDiagnosisType = db.table('rbDiagnosisType')
        cond.append(tableDiagnosisType['code'].inlist(['1', '2', '4']))
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality-1))
    return db.query(stmt % (db.joinAnd(cond)))


class CReportPolyclinicsOthersPersonList(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Список пациентов из других поликлиник')


    def getSetupDialog(self, parent):
        result = CReportPersonSickListSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def dumpParamsTraumaType(self, cursor, params):
        description = []
        traumaTypeId = params.get('traumaTypeId', None)
        chkTraumaTypeAny = params.get('chkTraumaTypeAny', False)
        if chkTraumaTypeAny:
            nameTraumaType = u'любой'
        elif traumaTypeId:
            nameTraumaType = forceString(QtGui.qApp.db.translate('rbTraumaType', 'id', traumaTypeId, 'name'))
        else:
            nameTraumaType = u'не определен'
        description.append(u'Тип травмы: ' + nameTraumaType)
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)


    def build(self, params):
        chkTraumaType = params.get('chkTraumaType', False)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        if chkTraumaType:
            self.dumpParamsTraumaType(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ('20%', [u'Дата посещения' ],        CReportBase.AlignLeft),
            ('40%', [u'Ф. И. О. / поликлиника'], CReportBase.AlignLeft),
            ('20%', [u'Дата рождения'],          CReportBase.AlignLeft),
            ('20%', [u'Ds по МКБ'],              CReportBase.AlignLeft)
            ]
        table = createTable(cursor, tableColumns)
        prevClientId = None
        prevClientRowIndex = 0
        query = selectData(params)
        while query.next():
            record = query.record()
            clientId = forceInt(record.value('client_id'))
            MKB = forceString(record.value('MKB'))
            setDateEvent = forceDate(record.value('setDateEvent')).toString('dd.MM.yyyy')
            execDateEvent = forceDate(record.value('execDateEvent')).toString('dd.MM.yyyy')
            ORGRelegate = forceString(record.value('ORGRelegate'))
            ORGClient = forceString(record.value('ORGClient'))
            birthDate = forceDate(record.value('setDateEvent')).toString('dd.MM.yyyy')
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            i = table.addRow()
            table.setText(i, 0, setDateEvent + u'-' + execDateEvent)
            if prevClientId != clientId:
                prevClientId = clientId
                prevClientRowIndex = i
                table.setText(i, 1, lastName + u' ' + firstName + u' ' + patrName + (u' / %s'%ORGRelegate if ORGRelegate else (u' / %s'%ORGClient if ORGClient else u'')))
                table.setText(i, 2, birthDate)
            table.mergeCells(prevClientRowIndex, 1, i-prevClientRowIndex+1, 1)
            table.mergeCells(prevClientRowIndex, 2, i-prevClientRowIndex+1, 1)
            table.setText(i, 3, MKB)
        return doc


def classToCodes(characterClass):
    if characterClass == 1:
        return ['1']
    elif characterClass == 2:
        return ['3']
    elif characterClass == 3:
        return ['1','3']
    elif characterClass == 4:
        return [None]
    else:
        return []
