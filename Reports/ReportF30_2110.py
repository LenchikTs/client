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
from library.Utils      import forceBool, forceInt, forceRef, forceString, formatShortName
from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportF30  import CReportF30Base, CReportF30SetupDialog

def selectData(begDate, endDate, useInputDate, begInputDate, endInputDate, eventPurposeId, eventTypeList, orgStructureId, socStatusClassId, socStatusTypeId, visitPayStatus, groupingRows, typeFinanceId, tariff, visitHospital, sex, ageFrom, ageTo, isEventClosed, scene):
    stmt="""
SELECT
   person_id,
   %(groupIdDef)s,
   %(groupNameDef)s,
   COUNT(person_id) AS cnt,
   SUM(isVillager) AS villagerCnt,
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
    rbEventTypePurpose.code = '1' as illness,
    IF(isCLientVillager(Client.`id`), 1, 0) AS isVillager,
    IF( ADDDATE(Client.birthDate, INTERVAL 18 YEAR)<=Visit.date,
        2,
        IF ( ADDDATE(Client.birthDate, INTERVAL 15 YEAR)>Visit.date,
          0,
          1)
      ) AS ageGroup
FROM Visit
LEFT JOIN Event      ON Event.id = Visit.event_id
LEFT JOIN EventType  ON EventType.id = Event.eventType_id
LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
LEFT JOIN Client     ON Client.id = Event.client_id
LEFT JOIN Person     ON Person.id = Visit.person_id
INNER JOIN rbFinance ON rbFinance.id = Visit.finance_id
%(internalJoins)s
WHERE Visit.deleted = 0
AND Event.deleted = 0
AND rbFinance.code = 2
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
    if eventTypeList:
        cond.append(tableEvent['eventType_id'].inlist(eventTypeList))
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
    if scene:
        cond.append('Visit.scene_id = %i' % scene)
    if tariff == 2:
        cond.append(tableVisit['service_id'].isNull())
    elif tariff == 1:
        cond.append(tableVisit['service_id'].isNotNull())
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


    stmt = stmt % dict(
                       groupIdDef    = groupIdDef,
                       groupNameDef  = groupNameDef,
                       internalDefs  = internalDefs,
                       internalJoins = internalJoins,
                       cond          = db.joinAnd(cond),
                       externalJoins = externalJoins
                      )

    return db.query(stmt )


class CReportF30_2110(CReportF30Base):
    def __init__(self, parent, additionalFields = False):
        CReportF30Base.__init__(self, parent, additionalFields)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Форма 30. Работа врачей амбулаторно-поликлинического учреждения (подразделения) в системе ОМС(2110)', u'Форма 30. Работа врачей амбулаторно-поликлинического учреждения (подразделения) в системе ОМС(2110)')


    def getSetupDialog(self, parent):
        result = CReportF30SetupDialog(parent)
        result.setTitle(self.title())
        result.setCMBEventTypeVisible(False)
        result.setEventTypeListListVisible(True)
        return result


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        useInputDate = bool(params.get('useInputDate', False))
        begInputDate = params.get('begInputDate', QDate())
        endInputDate = params.get('endInputDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeList = params.get('eventTypeList', [])
        orgStructureId = params.get('orgStructureId', None)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        typeFinanceId = params.get('typeFinanceId', None)
        isEventClosed = params.get('isEventClosed', 0)
        scene = params.get('sceneId',  None) if self.additionalFields else None
        tariff = params.get('tariff', 0)
        visitPayStatus = params.get('visitPayStatus', 0)
        visitPayStatus -= 1
        groupingRows = params.get('groupingRows', 0)
        detailChildren = params.get('detailChildren', False)
        visitHospital = params.get('visitHospital', False)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        onlyAmb = params.get('onlyAmbulator', True)
        #print onlyAmb
        basicSceneId = self.getSceneId('2')
        ambSceneId = self.getSceneId('1')
        #print ambSceneId
        reportRowSize = (13 if detailChildren else 10)
        #reportRowSize = reportRowSize if detailChildren else reportRowSize-1
        query = selectData(begDate, endDate, useInputDate, begInputDate, endInputDate, eventPurposeId, eventTypeList, orgStructureId, socStatusClassId, socStatusTypeId, visitPayStatus, groupingRows, typeFinanceId, tariff, visitHospital, sex, ageFrom, ageTo, isEventClosed, scene)

#        columnShift = 0 if detailChildren else 1
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
            cnt         = forceInt(record.value('cnt'))
            sceneId     = forceInt(record.value('scene_id'))
            illness     = forceBool(record.value('illness'))
            ageGroup    = forceInt(record.value('ageGroup'))
            villagerCnt = forceInt(record.value('villagerCnt'))
            if (not onlyAmb) or (sceneId == ambSceneId):
                reportRow[0] += cnt
                reportRow[1] += villagerCnt
                if ageGroup in (0, 1):
                    reportRow[2] += cnt
                if illness:
                    if ageGroup in (0, 1):
                        reportRow[4] += cnt
                        if detailChildren:
                            reportRow[5] += cnt
                    else:
                        reportRow[3] += cnt
            if basicSceneId == sceneId:
                reportRow[6 if detailChildren else 5] += cnt
                reportRow[7 if detailChildren else 6] += villagerCnt
                if illness:
                    reportRow[8 if detailChildren else 7] += cnt
                if ageGroup in (0, 1):
                    reportRow[9 if detailChildren else 8] += cnt
                    if illness:
                        reportRow[10 if detailChildren else 9] += cnt
                    if detailChildren:
                        reportRow[11] += cnt
                        if illness:
                            reportRow[12] += cnt

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        procentCol = '7%' if detailChildren else '10%'

        tableColumns = [
('15%',
 [u'ФИО врача', u'', u'1'], CReportBase.AlignLeft),
('3%',
 [u'№ строки', u'', u'2'], CReportBase.AlignLeft),
(procentCol,
 [u'Число посещений', u'врачей, включая профилак-тические - всего', u'3'], CReportBase.AlignRight),
(procentCol,
 [u'', u'в том числе сельскими жителями', u'4'], CReportBase.AlignRight),
(procentCol,
 [u'', u'детьми 0 - 17 лет (из гр. 3)', u'5'], CReportBase.AlignRight),
(procentCol,
 [u'Из общего числа посещений сделано по поводу заболеваний', u'взрослыми 18 лет и старше', u'6'], CReportBase.AlignRight),
(procentCol,
 [u'', u'детьми 0 - 17 лет', u'7'], CReportBase.AlignRight),
(procentCol,
 [u'Число посещений врачами на дому', u'всего', u'9' if detailChildren else u'8'], CReportBase.AlignRight),
 (procentCol,
 [u'', u'в том числе сельских жителей', u'10' if detailChildren else u'9'], CReportBase.AlignRight),
(procentCol,
 [u'', u'из них(гр. 8) по поводу заболеваний', u'11' if detailChildren else u'10'], CReportBase.AlignRight),
(procentCol,
 [u'', u'в том числе детей 0 - 17 лет включительно', u'12' if detailChildren else u'11'], CReportBase.AlignRight),
(procentCol,
 [u'', u'из них(гр. 11) по поводу заболеваний', u'13' if detailChildren else u'12'], CReportBase.AlignRight)
                       ]

        if detailChildren:
            tableColumns.insert( 5, ( procentCol, [u'', u'подр.', u'8'], CReportBase.AlignRight))
            tableColumns.insert(10, ( procentCol, [u'', u'подр.', u'13'], CReportBase.AlignRight))
            tableColumns.insert(11, ( procentCol, [u'', u'из них(гр. 12) по поводу заболеваний', u'14'], CReportBase.AlignRight))

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 1, 3 if detailChildren else 2)
        table.mergeCells(0, 8 if detailChildren else 7, 1, 8 if detailChildren else 6)

        prevGroupName = None
        total = None
        grandTotal = [0]*reportRowSize
        for groupName, personName, groupId, personId in personInfoList:
            if prevGroupName != groupName:
                if total:
                    self.produceTotalLine(table, u'всего', total, 1)
                total = [0]*reportRowSize
                i = table.addRow()
                table.mergeCells(i, 2, 1, reportRowSize)
                table.setText(i, 0, groupName, CReportBase.TableHeader)
                table.setText(i, 1, i-1, CReportBase.TableHeader)
                prevGroupName = groupName
            row = reportData[groupId, personId]
            i = table.addRow()
            table.setText(i, 0, personName)
            table.setText(i, 1, i-1)
            for j in xrange(reportRowSize):
                table.setText(i, j+2, row[j])
                total[j] += row[j]
                grandTotal[j] += row[j]
        if total:
            self.produceTotalLine(table, u'всего', total, 1)
        self.produceTotalLine(table, u'итого', grandTotal, 1)
        return doc
