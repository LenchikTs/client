# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils      import forceDate, forceInt, forceString, formatDate

from Events.Utils       import getWorkEventTypeFilter
from Orgs.Orgs          import selectOrganisation
from Orgs.Utils         import getOrgStructureAddressIdList, getOrgStructureDescendants
from Registry.Utils     import getClientBanner, getClientInfoEx
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from library.database   import addDateInRange
from library.DialogBase import CDialogBase


def addAddressCond(db, cond, addrType, addrIdList):
    tableClientAddress = db.table('ClientAddress')
    subcond = [tableClientAddress['client_id'].eqEx('`Client`.`id`'),
               tableClientAddress['id'].eqEx('(SELECT MAX(`CA`.`id`) FROM `ClientAddress` AS `CA` WHERE `CA`.`client_id` = ClientAddress.client_id AND `CA`.`type`=%d)' % addrType)
              ]
    if addrIdList is None:
        subcond.append(tableClientAddress['address_id'].isNull())
    else:
        subcond.append(tableClientAddress['address_id'].inlist(addrIdList))
    cond.append(db.existsStmt(tableClientAddress, subcond))
    return cond


def addAttachCond(db, cond, orgCond, attachCategory, attachTypeId, attachBegDate=QDate(), attachEndDate=QDate()):
    outerCond = []
    innerCond = ['CA2.client_id = Client.id']
    if attachBegDate and attachEndDate:
        outerCond.append(db.joinOr([db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) IS NULL'
                                                ]),

                                    db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) >= DATE(%s)'%(db.formatDate(attachBegDate))
                                                ]),

                                    db.joinAnd(['DATE(ClientAttach.endDate) IS NULL',
                                                'DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate))
                                                ]),

                                    db.joinAnd(['DATE(ClientAttach.begDate) IS NOT NULL',
                                                'DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate)),
                                    db.joinAnd(['DATE(ClientAttach.endDate) IS NOT NULL',
                                                'DATE(ClientAttach.endDate) >= DATE(%s)'%(db.formatDate(attachBegDate))
                                                ])
                                                ])
                                    ])
                        )
    elif attachBegDate:
        outerCond.append(db.joinOr([db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) IS NULL'
                                                ]),
                                    db.joinAnd(['DATE(ClientAttach.endDate) IS NOT NULL',
                                                'DATE(ClientAttach.endDate) >= DATE(%s)'%(db.formatDate(attachBegDate))
                                                ])
                                    ])
                        )
    elif attachEndDate:
        outerCond.append(db.joinOr([db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) IS NULL'
                                                ]),
                                    db.joinAnd(['DATE(ClientAttach.begDate) IS NOT NULL',
                                                'DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate))
                                                ])
                                    ])
                        )
        outerCond.append('DATE(ClientAttach.begDate) >= DATE(%s)'%(db.formatDate(attachBegDate)))
        outerCond.append('DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate)))
    if orgCond:
        outerCond.append(orgCond)
    if attachTypeId:
        outerCond.append('attachType_id=%d' % attachTypeId)
        innerCond.append('CA2.attachType_id=%d' % attachTypeId)
    else:
        if attachCategory == 1:
            innerCond.append('rbAttachType2.temporary=0')
        elif attachCategory == 2:
            innerCond.append('rbAttachType2.temporary')
        elif attachCategory == 3:
            innerCond.append('rbAttachType2.outcome')
        elif attachCategory == 0:
            outerCond.append('rbAttachType.outcome=0')
            innerCond.append('rbAttachType2.temporary=0')
    stmt = '''EXISTS (SELECT ClientAttach.id
       FROM ClientAttach
       LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
       WHERE ClientAttach.deleted=0
       AND %s
       AND ClientAttach.id = (SELECT MAX(CA2.id)
                   FROM ClientAttach AS CA2
                   LEFT JOIN rbAttachType AS rbAttachType2 ON rbAttachType2.id = CA2.attachType_id
                   WHERE CA2.deleted=0 AND %s))'''
    cond.append(stmt % (db.joinAnd(outerCond), db.joinAnd(innerCond)))
    return cond


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    sortByExecDate = params.get('sortByExecDate', False)
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
    accountPreliminary = params.get('accountPreliminary', False)
    locality = params.get('locality', 0)
    isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
    isAttachTo = params.get('isAttachTo', False)
    addrType = params.get('addressOrgStructureType', 0)
    addressOrgStructureId = params.get('addressOrgStructure', None)
    registeredInPeriod = params.get('registeredInPeriod', False)
    socStatusClassId = params.get('socStatusClassId', None)
    socStatusTypeId = params.get('socStatusTypeId', None)

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
    vrbPersonWithSpeciality.name AS diagnosticPerson %s
FROM Diagnosis
LEFT JOIN Client ON Client.id = Diagnosis.client_id
LEFT JOIN ClientAddress AS CADR ON CADR.client_id = Diagnosis.client_id
                        AND CADR.id = (SELECT MAX(id) FROM ClientAddress AS CADR2 WHERE CADR2.Type=1 and CADR2.client_id = Diagnosis.client_id)
LEFT JOIN Address ON Address.id = CADR.address_id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
LEFT JOIN rbTraumaType ON rbTraumaType.id = Diagnosis.traumaType_id
LEFT JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id
LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Diagnostic.person_id
LEFT JOIN Event      ON Event.id = Diagnostic.event_id
LEFT JOIN EventType  ON EventType.id = Event.eventType_id
%s
WHERE
    %s
ORDER BY %s Client.lastName, Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.id,
    Diagnosis.MKB, Diagnosis.MKBEx, Diagnostic.endDate
"""
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableClient = db.table('Client')
    tablePerson = db.table('vrbPersonWithSpeciality')
    tableDiagnostic = db.table('Diagnostic')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableEvent  = db.table('Event')
    tableDiagnosisType = db.table('rbDiagnosisType')
    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableDiagnostic['deleted'].eq(0))
#    cond.append(u'''(Diagnosis.id IS NOT NULL AND Diagnosis.deleted = 0) OR Diagnosis.id IS NULL''')
#    cond.append(u'''(Diagnostic.id IS NOT NULL AND Diagnostic.deleted = 0) OR Diagnostic.id IS NULL''')
    cond.append(tableDiagnosis['mod_id'].isNull())
#    addDateInRange(cond, tableDiagnostic['endDate'], begDate, endDate)
#    addDateInRange(cond, tableDiagnostic['setDate'], begDate, endDate)
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        cond.append(db.table('EventType')['purpose_id'].eq(eventPurposeId))
    if registeredInPeriod:
        addDateInRange(cond, tableDiagnosis['setDate'], begDate, endDate)
        addDateInRange(cond, tableDiagnostic['setDate'], begDate, endDate)
    else:
        cond.append(tableDiagnostic['setDate'].le(endDate))
        cond.append(db.joinOr([tableDiagnostic['endDate'].ge(begDate), tableDiagnostic['endDate'].isNull()]))
    if onlyFirstTime:
        cond.append(tableDiagnosis['setDate'].le(endDate))
        cond.append(tableDiagnosis['setDate'].ge(begDate))
    #else:
    #    cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), db.joinAnd([tableDiagnosis['setDate'].le(endDate), tableDiagnosis['setDate'].ge(begDate)])]))
    #    cond.append(db.joinOr([tableDiagnosis['endDate'].ge(begDate), tableDiseaseCharacter['code'].eq('3')]))
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
    joinPost = u''
    isPersonPost = params.get('isPersonPost', 0)
    if isPersonPost:
        joinPost = u'''INNER JOIN rbPost ON rbPost.id = vrbPersonWithSpeciality.post_id'''
        cond.append(tablePerson['deleted'].eq(0))
        if isPersonPost == 1:
            cond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            cond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
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
    diagnosisTypeCodeList = ['1', '2', '4', '3', '98']
    if accountAccomp:
        diagnosisTypeCodeList.extend(['9', '10', '11'])
    if accountPreliminary:
        diagnosisTypeCodeList.extend(['7', '8', '10', '11'])
    if diagnosisTypeCodeList:
        cond.append(tableDiagnosisType['code'].inlist(diagnosisTypeCodeList))
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality-1))
    if isAttachTo:
        attachOrgId = params['attachTo']
        if attachOrgId:
            addAttachCond(db, cond, 'LPU_id=%d'%attachOrgId, *params.get('attachType', (0, None, QDate(), QDate())))
    if isFilterAddressOrgStructure:
        addrIdList = None
        cond2 = []
        if (addrType+1) & 1:
            addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            addAddressCond(db, cond2, 0, addrIdList)
        if (addrType+1) & 2:
            if addrIdList is None:
                addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            addAddressCond(db, cond2, 1, addrIdList)
        if ((addrType+1) & 4):
            if addressOrgStructureId:
                addAttachCond(db, cond2, 'ClientAttach.orgStructure_id=%d'%addressOrgStructureId, 1, None)
            else:
                addAttachCond(db, cond2, 'ClientAttach.LPU_id=%d'%QtGui.qApp.currentOrgId(), 1, None)
        if cond2:
            cond.append(db.joinOr(cond2))
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
    orderBy = u'''Diagnosis.endDate,''' if sortByExecDate else ''
    stmtLocality = ', isClientVillager(Client.id) AS `isVillager`' if params.get('splitClientColumn') else ''
    return db.query(stmt % (stmtLocality, joinPost, db.joinAnd(cond), orderBy))


class CReportPersonSickList(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Заболеваемость: список пациентов')


    def getSetupDialog(self, parent):
        result = CReportPersonSickListSetupDialog(parent)
        result.setSortByExecDateVisible(True)
        result.setAccountPreliminaryVisible(True)
        result.setRegisteredInPeriod(True)
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
        splitClientColumn = params.get('splitClientColumn', False)
        splitDiagnosises = params.get('splitDiagnosises', False)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        if chkTraumaType:
            self.dumpParamsTraumaType(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        if splitClientColumn:
            tableColumns = [
                ('5%', [u'№' ],                         CReportBase.AlignRight),
                ('2%', [u'Пациент', u'ФИО'],            CReportBase.AlignLeft),
                ('2%', [u'', u'Дата рождения'],         CReportBase.AlignLeft),
                ('2%', [u'', u'Возраст'],               CReportBase.AlignLeft),
                ('2%', [u'', u'Пол'],                   CReportBase.AlignCenter),
                ('2%', [u'', u'СНИЛС'],                 CReportBase.AlignLeft),
                ('2%', [u'', u'Документ'],              CReportBase.AlignLeft),
                ('2%', [u'', u'Полис'],                 CReportBase.AlignLeft),
                ('5%', [u'', u'Адрес регистрации'],     CReportBase.AlignLeft),
                ('5%', [u'', u'Адрес проживания'],      CReportBase.AlignLeft),
                ('2%', [u'', u'Занятость'],             CReportBase.AlignLeft),
                ('2%', [u'', u'Телефон'],               CReportBase.AlignLeft),
                ('2%', [u'', u'Местность'],             CReportBase.AlignLeft),
                ('5%', [u'Заболевания', u'Код по МКБ'], CReportBase.AlignLeft),
                ('5%', [u'',            u'Доп.код'],    CReportBase.AlignLeft),
                ('5%', [u'',            u'С'],          CReportBase.AlignLeft),
                ('5%', [u'',            u'По'],         CReportBase.AlignLeft),
                ('5%', [u'',            u'Характер'],   CReportBase.AlignLeft),
                ('5%', [u'',            u'Тип травмы'], CReportBase.AlignLeft),
                ('5%', [u'Осмотры',     u'Дата'],       CReportBase.AlignLeft),
                ('5%', [u'',            u'Госп.'],      CReportBase.AlignLeft),
                ('5%', [u'',            u'СКЛ'],        CReportBase.AlignLeft),
                ('5%', [u'',            u'ДН'],         CReportBase.AlignLeft),
                ('15%',[u'',            u'Врач'],       CReportBase.AlignLeft)
                ]
        else:
            tableColumns = [
                ('5%', [u'№' ],                         CReportBase.AlignRight),
                ('25%',[u'Пациент'],                    CReportBase.AlignLeft),
                ('5%', [u'Заболевания', u'Код по МКБ'], CReportBase.AlignLeft),
                ('5%', [u'',            u'Доп.код'],    CReportBase.AlignLeft),
                ('5%', [u'',            u'С'],          CReportBase.AlignLeft),
                ('5%', [u'',            u'По'],         CReportBase.AlignLeft),
                ('5%', [u'',            u'Характер'],   CReportBase.AlignLeft),
                ('5%', [u'',            u'Тип травмы'], CReportBase.AlignLeft),
                ('5%', [u'Осмотры',     u'Дата'],       CReportBase.AlignLeft),
                ('5%', [u'',            u'Госп.'],      CReportBase.AlignLeft),
                ('5%', [u'',            u'СКЛ'],        CReportBase.AlignLeft),
                ('5%', [u'',            u'ДН'],         CReportBase.AlignLeft),
                ('15%',[u'',            u'Врач'],       CReportBase.AlignLeft)
                ]
        table = createTable(cursor, tableColumns)
        if splitClientColumn:
            table.mergeCells(0, 0,  2, 1)
            table.mergeCells(0, 1,  1, 12)
            table.mergeCells(0, 13, 1, 6)
            table.mergeCells(0, 19, 1, 5)
        else:
            table.mergeCells(0, 0, 2, 1)
            table.mergeCells(0, 1, 2, 1)
            table.mergeCells(0, 2, 1, 6)
            table.mergeCells(0, 8, 1, 5)
        prevClientId = None
        prevClientRowIndex = 0
        prevDiagnosisId = None
        prevDiagnosisRowIndex = 0
        cnt = 0
        i = 0
        col = 0
        query = selectData(params)
        while query.next():
            record = query.record()
            clientId = forceInt(record.value('client_id'))
            diagnosisId = forceInt(record.value('diagnosis_id'))
            MKB = forceString(record.value('MKB'))
            MKBEx = forceString(record.value('MKBEx'))
            setDate = forceDate(record.value('setDate'))
            endDate = forceDate(record.value('endDate'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            if diseaseCharacter == '1':
                diseaseCharacter = u'острый'
            elif diseaseCharacter == '3':
                diseaseCharacter = u'хронический'
            traumaType = forceString(record.value('traumaType'))
            diagnosticDate = forceDate(record.value('diagnosticDate'))
            diagnosticHospital = forceString(record.value('diagnosticHospital'))
            diagnosticSanatorium = forceString(record.value('diagnosticSanatorium'))
            diagnosticDispanser = forceString(record.value('diagnosticDispanser'))
            diagnosticPerson = forceString(record.value('diagnosticPerson'))

            i = table.addRow()
            if prevClientId != clientId or splitDiagnosises:
                prevClientId = clientId
                self.mergePatientRows(table, prevClientRowIndex, i, splitClientColumn)
                prevClientRowIndex = i
                col = 11 if splitClientColumn else 0
                cnt += 1
                table.setText(i, 0, cnt)
                if splitClientColumn:
                    client = getClientInfoEx(clientId)
                    document = client.get('document', u'нет')
                    table.setText(i,  1, client.fullName)
                    table.setText(i,  2, formatDate(client.birthDate))
                    table.setText(i,  3, client.age)
                    table.setText(i,  4, client.sex)
                    table.setText(i,  5, client.SNILS)
                    table.setText(i,  6, document if document else u'нет')
                    table.setText(i,  7, client.policy)
                    table.setText(i,  8, client.get('regAddress', u'не указан'))
                    table.setText(i,  9, client.get('locAddress', u'не указан'))
                    table.setText(i, 10, client.get('work', u'не указано'))
                    table.setText(i, 11, client.phones)
                    table.setText(i, 12, u'Сельская' if forceInt(record.value('isVillager')) else u'Городская')
                else:
                    table.setHtml(i, 1, getClientBanner(clientId))
            if prevDiagnosisId != diagnosisId or splitDiagnosises:
                prevDiagnosisId = diagnosisId
                self.mergeDiagnosisRows(table, prevDiagnosisRowIndex, i, splitClientColumn)
                prevDiagnosisRowIndex = i
                table.setText(i, col+2, MKB)
                table.setText(i, col+3, MKBEx)
                table.setText(i, col+4, forceString(setDate))
                table.setText(i, col+5, forceString(endDate))
                table.setText(i, col+6, forceString(diseaseCharacter))
                table.setText(i, col+7, forceString(traumaType))
            table.setText(i, col+ 8, forceString(diagnosticDate))
            table.setText(i, col+ 9, diagnosticHospital)
            table.setText(i, col+10, diagnosticSanatorium)
            table.setText(i, col+11, diagnosticDispanser)
            table.setText(i, col+12, diagnosticPerson)
        self.mergePatientRows(table, prevClientRowIndex, i+1, splitClientColumn)
        self.mergeDiagnosisRows(table, prevDiagnosisRowIndex, i+1, splitClientColumn)
        return doc


    def mergePatientRows(self, table, start, current, splitted):
        if start:
            mergeRows = current - start
            if mergeRows > 1:
                counter = xrange(13) if splitted else xrange(2)
                for j in counter:
                    table.mergeCells(start, j, mergeRows, 1)


    def mergeDiagnosisRows(self, table, start, current, splitted):
        if start:
            mergeRows = current - start
            colShift = 11 if splitted else 0
            if mergeRows > 1:
                for j in xrange(2, 8):
                    table.mergeCells(start, colShift+j, mergeRows, 1)


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


from Ui_ReportPersonSickListSetup import Ui_ReportPersonSickListSetupDialog


class CReportPersonSickListSetupDialog(CDialogBase, Ui_ReportPersonSickListSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbTraumaType.setTable('rbTraumaType', True)
        self.cmbPhase.setTable('rbDiseasePhases', True)
        self.cmbPhaseEx.setTable('rbDiseasePhases', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbFilterAttachOrganisation.setValue(QtGui.qApp.currentOrgId())
        self.cmbSocStatusType.setTable('vrbSocStatusType', True)
        self.setSortByExecDateVisible(False)
        self.setAccountPreliminaryVisible(False)
        self.setEventPurposeVisible(True)
        self.setEventTypeVisible(True)
        self.setWorkOrganisationVisible(True)
        self.setSexVisible(True)
        self.setAgeVisible(True)
        self.setMKBFilterVisible(True)
        self.setLocalityVisible(True)
        self.setFilterAttachOrganisationVisible(True)
        self.setFilterAddressOrgStructureVisible(True)
        self.setRegisteredInPeriod(False)


    def setRegisteredInPeriod(self, value):
        self.chkRegisteredInPeriod.setVisible(value)
        self.registeredInPeriod = value


    def setSortByExecDateVisible(self, value):
        self.sortByExecDateVisible = value
        self.chkSortByExecDate.setVisible(value)


    def setAccountPreliminaryVisible(self, value):
        self.isAccountPreliminaryVisible = value
        self.chkAccountPreliminary.setVisible(value)


    def setEventPurposeVisible(self,  value):
        self.eventPurposeVisible = value
        self.lblEventPurpose.setVisible(value)
        self.cmbEventPurpose.setVisible(value)


    def setEventTypeVisible(self,  value):
        self.eventTypeVisible = value
        self.lblEventType.setVisible(value)
        self.cmbEventType.setVisible(value)


    def setWorkOrganisationVisible(self,  value):
        self.workOrganisationVisible = value
        self.lblWorkOrganisation.setVisible(value)
        self.cmbWorkOrganisation.setVisible(value)
        self.btnSelectWorkOrganisation.setVisible(value)


    def setSexVisible(self, value):
        self.sexVisible = value
        self.lblSex.setVisible(value)
        self.cmbSex.setVisible(value)


    def setAgeVisible(self, value):
        self.ageVisible = value
        self.lblAge.setVisible(value)
        self.edtAgeFrom.setVisible(value)
        self.lblAgeTo.setVisible(value)
        self.edtAgeTo.setVisible(value)
        self.lblAgeYears.setVisible(value)


    def setMKBFilterVisible(self, value):
        self.MKBFilterVisible = value
        self.lblMKB.setVisible(value)
        self.cmbMKBFilter.setVisible(value)
        self.edtMKBFrom.setVisible(value)
        self.edtMKBTo.setVisible(value)
        self.lblMKBEx.setVisible(value)
        self.cmbMKBExFilter.setVisible(value)
        self.edtMKBExFrom.setVisible(value)
        self.edtMKBExTo.setVisible(value)
        self.lblDiseaseCharacter.setVisible(value)
        self.cmbCharacterClass.setVisible(value)
        self.chkOnlyFirstTime.setVisible(value)
        self.chkAccountAccomp.setVisible(value)
        self.chkAccountPreliminary.setVisible(value)
        self.chkTraumaType.setVisible(value)
        self.chkTraumaTypeAny.setVisible(value)
        self.cmbTraumaType.setVisible(value)


    def setLocalityVisible(self, value):
        self.localityVisible = value
        self.lblLocality.setVisible(value)
        self.cmbLocality.setVisible(value)


    def setFilterAttachOrganisationVisible(self, value):
        self.filterAttachOrganisationVisible = value
        self.chkFilterAttach.setVisible(value)
        self.cmbFilterAttachOrganisation.setVisible(value)


    def setFilterAddressOrgStructureVisible(self, value):
        self.filterAddressOrgStructureVisible = value
        self.chkFilterAddressOrgStructure.setVisible(value)
        self.cmbFilterAddressOrgStructureType.setVisible(value)
        self.cmbFilterAddressOrgStructure.setVisible(value)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        if self.eventPurposeVisible:
            self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        if self.eventTypeVisible:
            self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.chkFilterAttach.setChecked(params.get('isAttachTo', False))
        self.cmbFilterAttachOrganisation.setValue(params.get('attachTo', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        if self.workOrganisationVisible:
            self.cmbWorkOrganisation.setValue(params.get('workOrgId', None))
        if self.sexVisible:
            self.cmbSex.setCurrentIndex(params.get('sex', 0))
        if self.ageVisible:
            self.edtAgeFrom.setValue(params.get('ageFrom', 0))
            self.edtAgeTo.setValue(params.get('ageTo', 150))
        if self.MKBFilterVisible:
            self.chkTraumaType.setChecked(params.get('chkTraumaType', False))
            self.chkTraumaTypeAny.setChecked(params.get('chkTraumaTypeAny', False))
            if self.chkTraumaType.isChecked() and not self.chkTraumaTypeAny.isChecked():
                self.cmbTraumaType.setValue(params.get('traumaTypeId', None))
            else:
                self.cmbTraumaType.setValue(None)
            MKBFilter = params.get('MKBFilter', 0)
            self.cmbMKBFilter.setCurrentIndex(MKBFilter if MKBFilter else 0)
            self.edtMKBFrom.setText(params.get('MKBFrom', 'A00'))
            self.edtMKBTo.setText(params.get('MKBTo',   'Z99.9'))
            self.cmbPhase.setValue(params.get('phaseId', None))
            MKBExFilter = params.get('MKBExFilter', 0)
            self.cmbMKBExFilter.setCurrentIndex(MKBExFilter if MKBExFilter else 0)
            self.edtMKBExFrom.setText(params.get('MKBExFrom', 'A00'))
            self.edtMKBExTo.setText(params.get('MKBExTo',   'Z99.9'))
            self.cmbPhaseEx.setValue(params.get('phaseIdEx', None))
            self.cmbCharacterClass.setCurrentIndex(params.get('characterClass', 0))
            self.chkOnlyFirstTime.setChecked(bool(params.get('onlyFirstTime', False)))
            self.chkAccountAccomp.setChecked(bool(params.get('accountAccomp', False)))
        if self.isAccountPreliminaryVisible:
            self.chkAccountPreliminary.setChecked(bool(params.get('accountPreliminary', False)))
        if self.localityVisible:
            self.cmbLocality.setCurrentIndex(params.get('locality', 0))
        self.chkSortByExecDate.setChecked(self.sortByExecDateVisible and bool(params.get('sortByExecDate', False)))
        if self.filterAddressOrgStructureVisible:
            self.chkFilterAddressOrgStructure.setChecked(params.get('isFilterAddressOrgStructure', False))
            self.cmbFilterAddressOrgStructureType.setCurrentIndex(params.get('addressOrgStructureType', 0))
            self.cmbFilterAddressOrgStructure.setValue(params.get('addressOrgStructure', None))
        if self.registeredInPeriod:
            self.chkRegisteredInPeriod.setChecked(bool(params.get('registeredInPeriod', False)))
        self.chkSplitClientColumn.setChecked(params.get('splitClientColumn', False))
        self.chkSplitDiagnosises.setChecked(params.get('splitDiagnosises', False))
        self.cmbSocStatusClass.setValue(params.get('socStatusClassId', None))
        self.cmbSocStatusType.setValue(params.get('socStatusTypeId', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        if self.eventPurposeVisible:
            result['eventPurposeId'] = self.cmbEventPurpose.value()
        if self.eventTypeVisible:
            result['eventTypeId'] = self.cmbEventType.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['personId'] = self.cmbPerson.value()
        if self.chkFilterAttach.isChecked():
            result['isAttachTo'] = self.chkFilterAttach.isChecked()
            result['attachTo'] = self.cmbFilterAttachOrganisation.value()
        result['specialityId'] = self.cmbSpeciality.value()
        if self.workOrganisationVisible:
            result['workOrgId'] = self.cmbWorkOrganisation.value()
        if self.sexVisible:
            result['sex'] = self.cmbSex.currentIndex()
        if self.ageVisible:
            result['ageFrom'] = self.edtAgeFrom.value()
            result['ageTo'] = self.edtAgeTo.value()
        if self.MKBFilterVisible:
            result['chkTraumaTypeAny'] = self.chkTraumaTypeAny.isChecked()
            if self.chkTraumaType.isChecked() and not self.chkTraumaTypeAny.isChecked():
                result['traumaTypeId'] = self.cmbTraumaType.value()
            result['chkTraumaType'] = self.chkTraumaType.isChecked()
            result['MKBFilter'] = self.cmbMKBFilter.currentIndex()
            result['MKBFrom']   = unicode(self.edtMKBFrom.text())
            result['MKBTo']     = unicode(self.edtMKBTo.text())
            result['phaseId']   = self.cmbPhase.value()
            result['MKBExFilter'] = self.cmbMKBExFilter.currentIndex()
            result['MKBExFrom']   = unicode(self.edtMKBExFrom.text())
            result['MKBExTo']     = unicode(self.edtMKBExTo.text())
            result['phaseIdEx']   = self.cmbPhaseEx.value()
            result['characterClass'] = self.cmbCharacterClass.currentIndex()
            result['onlyFirstTime'] = self.chkOnlyFirstTime.isChecked()
            result['accountAccomp'] = self.chkAccountAccomp.isChecked()
        if self.isAccountPreliminaryVisible:
            result['accountPreliminary'] = self.chkAccountPreliminary.isChecked()
        if self.localityVisible:
            result['locality']      = self.cmbLocality.currentIndex()
        result['sortByExecDate'] = self.chkSortByExecDate.isChecked() if self.sortByExecDateVisible else False
        if self.filterAddressOrgStructureVisible:
            result['isFilterAddressOrgStructure'] = self.chkFilterAddressOrgStructure.isChecked()
            result['addressOrgStructureType'] = self.cmbFilterAddressOrgStructureType.currentIndex()
            result['addressOrgStructureTypeText'] = self.cmbFilterAddressOrgStructureType.currentText()
            result['addressOrgStructure'] = self.cmbFilterAddressOrgStructure.value()
        if self.registeredInPeriod:
            result['registeredInPeriod'] = self.chkRegisteredInPeriod.isChecked()
        result['splitClientColumn'] = self.chkSplitClientColumn.isChecked()
        result['splitDiagnosises'] = self.chkSplitDiagnosises.isChecked()
        result['socStatusClassId'] = self.cmbSocStatusClass.value()
        result['socStatusTypeId'] = self.cmbSocStatusType.value()
        return result


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = 'EventType.purpose_id =%d' % eventPurposeId
        else:
            filter = getWorkEventTypeFilter(isApplyActive=True)
        self.cmbEventType.setFilter(filter)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)


    @pyqtSignature('')
    def on_btnSelectWorkOrganisation_clicked(self):
        orgId = selectOrganisation(self, self.cmbWorkOrganisation.value(), False)
        self.cmbWorkOrganisation.updateModel()
        if orgId:
            self.cmbWorkOrganisation.setValue(orgId)


    @pyqtSignature('int')
    def on_cmbMKBFilter_currentIndexChanged(self, index):
        self.edtMKBFrom.setEnabled(index == 1)
        self.edtMKBTo.setEnabled(index == 1)
        self.cmbPhase.setEnabled(index == 1)


    @pyqtSignature('int')
    def on_cmbMKBExFilter_currentIndexChanged(self, index):
        self.edtMKBExFrom.setEnabled(index == 1)
        self.edtMKBExTo.setEnabled(index == 1)
        self.cmbPhaseEx.setEnabled(index == 1)

