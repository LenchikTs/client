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
from PyQt4.QtCore import pyqtSignature, QDate

from library.database   import addDateInRange
from library.Utils      import forceBool, forceInt, forceRef, forceString, formatShortName

from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportF30  import CReportF30SetupDialog, CReportF30Base


def selectData(begDate, endDate, useInputDate, begInputDate, endInputDate, eventPurposeId, eventTypeId, orgStructureId, socStatusClassId, socStatusTypeId, visitPayStatus, groupingRows, typeFinanceId, tariff, visitHospital, sex, ageFrom, ageTo, isEventClosed, scene):
    stmt="""
SELECT
   person_id,
   %(groupIdDef)s,
   %(groupNameDef)s,
   COUNT(person_id) AS cnt,
   scene_id,
   illness,
   ageGroup,
   Person.lastName,
   Person.firstName,
   Person.patrName
   FROM (
SELECT
    Visit.person_id,
    Visit.scene_id,
    %(internalDefs)s
    EmergencyCall.disease as illness,
    IF( ADDDATE(Client.birthDate, INTERVAL 18 YEAR)<=Visit.date,
        2,
        IF ( ADDDATE(Client.birthDate, INTERVAL 15 YEAR)>Visit.date,
          0,
          1)
      ) AS ageGroup
FROM Visit
LEFT JOIN Event     ON Event.id = Visit.event_id
LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
INNER JOIN EventType ON EventType.id = Event.eventType_id
LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
LEFT JOIN Client   ON Client.id = Event.client_id
LEFT JOIN Person    ON Person.id = Visit.person_id
%(internalJoins)s
WHERE Visit.deleted = 0 AND EventType.deleted = 0
AND Event.deleted = 0 AND EventType.form = 110
AND EmergencyCall.deleted = 0
AND DATE(Event.setDate) <= DATE(Visit.date)
AND %(cond)s
) AS T
LEFT JOIN Person ON Person.id = T.person_id
LEFT JOIN rbPost ON rbPost.id = Person.post_id
%(externalJoins)s
GROUP BY group_id, person_id, scene_id, illness, ageGroup
ORDER BY groupName, Person.lastName, Person.firstName, Person.patrName
    """
    db = QtGui.qApp.db
    tableVisit  = db.table('Visit')
    tableEvent  = db.table('Event')
    tableEventType = db.table('EventType')
    tableClient = db.table('Client')
    tablePerson = db.table('Person')

    cond = []
    addDateInRange(cond, tableVisit['date'], begDate, endDate)
    if useInputDate:
        addDateInRange(cond, tableEvent['createDatetime'], begInputDate, endInputDate)
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        cond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
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
    if visitPayStatus >= 0:
        cond.append(u'getPayCode(Visit.finance_id, Visit.payStatus) = %d'%(visitPayStatus))
    if typeFinanceId:
        cond.append(tableVisit['finance_id'].eq(typeFinanceId))
    if tariff == 2:
        cond.append(tableVisit['service_id'].isNull())
    elif tariff == 1:
        cond.append(tableVisit['service_id'].isNotNull())
    if scene:
        cond.append('Visit.scene_id = %i' % scene)
    if not visitHospital:
        cond.append(u'''EventType.medicalAidType_id IS NULL OR (EventType.medicalAidType_id NOT IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN (\'7\')))''')
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Visit.date >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Visit.date < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if isEventClosed == 1:
        cond.append('Event.execDate is not NULL')
    elif isEventClosed == 2:
        cond.append('Event.execDate is NULL')
    if groupingRows == 1: # по должности
        groupIdDef    = 'Person.post_id AS group_id'
        groupNameDef  = 'rbPost.name AS groupName'
        internalDefs  = ''
        internalJoins = ''
        externalJoins = ''
    elif groupingRows == 2: # по профилю оплаты
        groupIdDef    = 'visitService_id  AS group_id'
        groupNameDef  = 'visitServiceName AS groupName'
        internalDefs  = 'Visit.service_id AS visitService_id, rbService.Code AS visitServiceName,'
        internalJoins = 'LEFT JOIN rbService ON rbService.id = Visit.service_id'
        externalJoins = ''
    elif groupingRows == 3: # по страховым
        tableCP = db.table('ClientPolicy')
        tableOrganisation = db.table('Organisation')
        condCP = u'''ClientPolicy.id = (SELECT CP.id
                                        FROM ClientPolicy AS CP
                                        INNER JOIN rbPolicyType ON rbPolicyType.id = CP.policyType_id
                                        WHERE CP.client_id = Client.id AND CP.deleted = 0 AND CP.begDate <= Visit.date AND (CP.endDate IS NULL OR CP.endDate >= Visit.date)
                                        ORDER BY rbPolicyType.isCompulsory DESC, CP.begDate DESC
                                        LIMIT 1)'''
        condOrg = [ tableOrganisation['id'].eq(tableCP['insurer_id']),
                    tableOrganisation['deleted'].eq(0)]
        groupIdDef    = 'orgId AS group_id'
        groupNameDef  = 'orgName AS groupName'
        internalDefs  = 'Organisation.id AS orgId, Organisation.fullName AS orgName,'
        internalJoins = '''LEFT JOIN ClientPolicy ON (%s)
                           LEFT JOIN Organisation ON (%s)'''%(condCP, db.joinAnd(condOrg))
        externalJoins = ''
    else: # по специальности
        groupIdDef    = 'Person.speciality_id AS group_id'
        groupNameDef  = 'rbSpeciality.name AS groupName'
        internalDefs  = ''
        internalJoins = ''
        externalJoins = 'LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id'
    return db.query(stmt
                    % dict(groupIdDef    = groupIdDef,
                           groupNameDef  = groupNameDef,
                           internalDefs  = internalDefs,
                           internalJoins = internalJoins,
                           cond          = db.joinAnd(cond),
                           externalJoins = externalJoins
                          )
                   )


class CReportF30_SMPBase(CReportF30Base):
    def getSetupDialog(self, parent):
        result = CReportF30_SMPSetupDialog(parent)
        result.setTitle(self.title())
        result.setAdditionalFieldsVisible(self.additionalFields)
        return result


class CReportF30_SMP(CReportF30_SMPBase):
    def __init__(self, parent, additionalFields = False):
        CReportF30_SMPBase.__init__(self, parent, additionalFields)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Форма Ф30 (СМП)', u'Форма Ф30 (СМП)')


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        useInputDate = bool(params.get('useInputDate', False))
        begInputDate = params.get('begInputDate', QDate())
        endInputDate = params.get('endInputDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        typeFinanceId = params.get('typeFinanceId', None)
        tariff = params.get('tariff', 0)
        visitPayStatus = params.get('visitPayStatus', 0)
        visitPayStatus -= 1
        groupingRows = params.get('groupingRows', 0)
        detailChildren = params.get('detailChildren', False)
        visitHospital = params.get('visitHospital', False)
        isEventClosed = params.get('isEventClosed', 0)
        scene = params.get('sceneId',  None) if self.additionalFields else None
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        db = QtGui.qApp.db
        sceneNames   = []
        sceneIndexes = {}
        for index, record in enumerate(db.getRecordList('rbScene', 'id, name', '', 'code')):
            sceneId = forceRef(record.value(0))
            sceneName = forceString(record.value(1))
            sceneIndexes[sceneId] = index
            sceneNames.append(sceneName)
        if not(sceneNames):
            sceneNames.append(u'не определено')
        reportRowSize = 1+4+2*len(sceneNames)
        reportRowSize = reportRowSize if detailChildren else reportRowSize-1
        query = selectData(begDate, endDate, useInputDate, begInputDate, endInputDate, eventPurposeId, eventTypeId, orgStructureId, socStatusClassId, socStatusTypeId, visitPayStatus, groupingRows, typeFinanceId, tariff, visitHospital, sex, ageFrom, ageTo, isEventClosed, scene)
        columnShift = 0 if detailChildren else 1
        reportData = {}
        personInfoList = []
        while query.next():
            record    = query.record()
            groupId   = forceRef(record.value('group_id'))
            personId  = forceRef(record.value('person_id'))
            reportRow = reportData.get((groupId, personId), None)
            if not reportRow:
                reportRow = [0]*reportRowSize
                reportData[groupId, personId] = reportRow
                groupName = forceString(record.value('groupName'))
                lastName = forceString(record.value('lastName'))
                firstName = forceString(record.value('firstName'))
                patrName = forceString(record.value('patrName'))
                personName = formatShortName(lastName, firstName, patrName)
                personInfoList.append((groupName, personName, groupId, personId))
            cnt       = forceInt(record.value('cnt'))
            sceneId   = forceInt(record.value('scene_id'))
            illness   = forceBool(record.value('illness'))
            ageGroup  = forceInt(record.value('ageGroup'))
            reportRow[0] += cnt
            if illness:
                reportRow[1] += cnt
                if not detailChildren:
                    if ageGroup in (0, 1):
                        ageGroup = 0
                    else:
                        ageGroup = 1
                reportRow[2+ageGroup] += cnt
            sceneIndex = sceneIndexes.get(sceneId, 0)
            reportRow[5+sceneIndex*2-columnShift] += cnt
            if illness:
                reportRow[6+sceneIndex*2-columnShift] += cnt

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ('30%', [u'ФИО врача',             u''], CReportBase.AlignLeft),
            ( '5%', [u'всего посещений',       u''], CReportBase.AlignRight),
            ( '5%', [u'по поводу заболеваний', u'всего'   ], CReportBase.AlignRight),
            ( '5%', [u'',                      u'дети'    ], CReportBase.AlignRight),
            ( '5%', [u'',                      u'взр.'    ], CReportBase.AlignRight),
            ]
        if detailChildren:
            tableColumns.insert(4, ( '5%', [u'', u'подр.'], CReportBase.AlignRight))
        for sceneName in sceneNames:
            tableColumns.append(  ('5%', [sceneName, u'всего'   ], CReportBase.AlignRight) )
            tableColumns.append(  ('5%', [u'',       u'по заб.' ], CReportBase.AlignRight) )
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        ageLength = 4 if detailChildren else 3
        table.mergeCells(0, 2, 1, ageLength)
        for sceneIndex in xrange(len(sceneNames)):
            table.mergeCells(0, 6+sceneIndex*2-columnShift, 1, 2)
        prevGroupName = None
        total = None
        grandTotal = [0]*reportRowSize
        for groupName, personName, groupId, personId in personInfoList:
            if prevGroupName != groupName:
                if total:
                    self.produceTotalLine(table, u'всего', total, 0)
                total = [0]*reportRowSize
                i = table.addRow()
                table.mergeCells(i, 0, 1, reportRowSize+1)
                table.setText(i, 0, groupName, CReportBase.TableHeader)
                prevGroupName = groupName
            row = reportData[groupId, personId]
            i = table.addRow()
            table.setText(i, 0, personName)
            for j in xrange(reportRowSize):
                table.setText(i, j+1, row[j])
                total[j] += row[j]
                grandTotal[j] += row[j]
        if total:
            self.produceTotalLine(table, u'всего', total, 0)
        self.produceTotalLine(table, u'итого', grandTotal, 0)
        return doc


class CReportF30_SMPSetupDialog(CReportF30SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='purpose = 7')
        self.cmbEventType.setTable('EventType', True, filter='(EventType.purpose_id IN (SELECT rbEventTypePurpose.id from rbEventTypePurpose where rbEventTypePurpose.purpose = 7))')
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbSocStatusType.setTable('vrbSocStatusType', True)
        self.cmbTypeFinance.setTable('rbFinance', True)
        self.cmbTariff.setCurrentIndex(0)
        self.cmbVisitPayStatus.setCurrentIndex(0)
        self.cmbGrouping.setCurrentIndex(0)
        self.cmbScene.setTable('rbScene', True, None)
        self.cmbScene.setVisible(False)
        self.lblScene.setVisible(False)
        self.flag = None
        self.setCMBEventTypeVisible(True)
        self.setEventTypeListListVisible(False)
        self.setSpecialityListVisible(False)


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = 'EventType.purpose_id=%d' % eventPurposeId
        else:
            filter = '(EventType.purpose_id IN (SELECT rbEventTypePurpose.id from rbEventTypePurpose where rbEventTypePurpose.purpose = 7))'
        self.cmbEventType.setFilter(filter)

