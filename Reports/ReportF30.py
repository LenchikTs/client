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
from library.MapCode    import createMapCodeToRowIdx
from library.Utils      import forceInt, forceRef, forceString, formatShortName

from Events.Utils       import getWorkEventTypeFilter
from Events.EventTypeListEditorDialog import CEventTypeListEditorDialog, formatEventTypeIdList
from Reports.Report     import CReport, normalizeMKB
from Reports.SpecialityListDialog import CSpecialityListDialog, formatSpecialityIdList
from Reports.ContingentTypeListDialog import CContingentTypeListDialog, formatContingentTypeList
from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable


def selectData(params, scene):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    useInputDate = bool(params.get('useInputDate', False))
    begInputDate = params.get('begInputDate', QDate())
    endInputDate = params.get('endInputDate', QDate())
    eventPurposeId = params.get('eventPurposeId', None)
    eventTypeId = params.get('eventTypeId', None)
    eventTypeList = params.get('eventTypeList', [])
    isEventTypeVisible = params.get('isEventTypeVisible', None)
    orgStructureId = params.get('orgStructureId', None)
    socStatusClassId = params.get('socStatusClassId', None)
    socStatusTypeId = params.get('socStatusTypeId', None)
    typeFinanceId = params.get('typeFinanceId', None)
    tariff = params.get('tariff', 0)
    visitPayStatus = params.get('visitPayStatus', 0)
    visitPayStatus -= 1
    groupingRows = params.get('groupingRows', 0)
    visitHospital = params.get('visitHospital', False)
    isEventClosed = params.get('isEventClosed', 0)
    sex = params.get('sex', 0)
    ageFrom = params.get('ageFrom', 0)
    ageTo = params.get('ageTo', 150)
    isSpecialityListVisible = params.get('isSpecialityListVisible', False)
    specialityList = params.get('specialityList', [])
    stmt="""
SELECT
   person_id,
   %(groupIdDef)s,
   %(groupNameDef)s,
   COUNT(person_id) AS cnt,
   scene_id,
   illness,
   %(MKB)s,
   ageGroup,
   Person.lastName,
   Person.firstName,
   Person.patrName
   FROM (
SELECT
    Event.id AS eventId,
    Event.execPerson_id,
    Visit.person_id,
    Visit.scene_id,
    %(internalDefs)s
    rbEventTypePurpose.code = '1' as illness,
    IF( ADDDATE(Client.birthDate, INTERVAL 18 YEAR)<=Visit.date,
        2,
        IF ( ADDDATE(Client.birthDate, INTERVAL 15 YEAR)>Visit.date,
          0,
          1)
      ) AS ageGroup
FROM Visit
LEFT JOIN Event     ON Event.id = Visit.event_id
LEFT JOIN EventType ON EventType.id = Event.eventType_id
LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
LEFT JOIN Client   ON Client.id = Event.client_id
LEFT JOIN Person    ON Person.id = Visit.person_id
%(internalJoins)s
WHERE Visit.deleted = 0
AND Event.deleted = 0
AND DATE(Event.setDate) <= DATE(Visit.date)
AND %(cond)s
) AS T
LEFT JOIN Person ON Person.id = T.person_id
LEFT JOIN rbPost ON rbPost.id = Person.post_id
%(externalJoins)s
GROUP BY group_id, person_id, scene_id, MKB, illness, ageGroup
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
    if isEventTypeVisible:
        if eventTypeId:
            cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventTypeList:
        cond.append(tableEvent['eventType_id'].inlist(eventTypeList))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        cond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    if isSpecialityListVisible and specialityList:
        cond.append(tablePerson['speciality_id'].inlist(specialityList))
    cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
#    if eventTypeIdList:
#        cond.append(tableEvent['eventType_id'].inlist(eventTypeIdList))
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
    MKB = '''(SELECT Diagnosis.MKB
    FROM Diagnosis INNER JOIN Diagnostic ON Diagnostic.diagnosis_id=Diagnosis.id
    INNER JOIN rbDiagnosisType ON Diagnostic.diagnosisType_id=rbDiagnosisType.id
    WHERE Diagnostic.event_id = T.eventId AND Diagnosis.deleted = 0 AND Diagnostic.deleted = 0
    AND (rbDiagnosisType.code = '1'
    OR (rbDiagnosisType.code = '2' AND Diagnostic.person_id = T.execPerson_id
    AND (NOT EXISTS (SELECT DC.id FROM Diagnostic AS DC
    INNER JOIN rbDiagnosisType AS DT ON DT.id = DC.diagnosisType_id WHERE DT.code = '1'
    AND DC.event_id = T.eventId
    LIMIT 1)))) LIMIT 1) AS MKB'''
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
                           MKB           = MKB,
                           internalDefs  = internalDefs,
                           internalJoins = internalJoins,
                           cond          = db.joinAnd(cond),
                           externalJoins = externalJoins
                          )
                   )


class CReportF30Base(CReport):
    def __init__(self, parent, additionalFields = False):
        CReport.__init__(self, parent)
        self.additionalFields = additionalFields


    def getSetupDialog(self, parent):
        result = CReportF30SetupDialog(parent)
        result.setTitle(self.title())
        result.setAdditionalFieldsVisible(self.additionalFields)
        result.setCMBEventTypeVisible(True)
        result.setEventTypeListListVisible(False)
        return result

    def getSceneId(self, code):
        result = None
        recordsScene = QtGui.qApp.db.getRecordList('rbScene', 'id', 'code = %s'%code)
        for recordScene in recordsScene:
            result = forceRef(recordScene.value('id'))
        return result

    def produceTotalLine(self, table, title, total, add1):
        i = table.addRow()
        table.setText(i, 0, title, CReportBase.TableTotal)
        if add1 == 1:
            table.setText(i, 1, i-1)
        for j in xrange(len(total)):
            table.setText(i, j+1+add1, total[j], CReportBase.TableTotal)


class CReportF30(CReportF30Base):
    def __init__(self, parent, additionalFields = False):
        CReportF30Base.__init__(self, parent, additionalFields)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Форма 30', u'Форма 30')


    def getSetupDialog(self, parent):
        result = CReportF30SetupDialog(parent)
        result.setTitle(self.title())
        result.setAdditionalFieldsVisible(self.additionalFields)
        result.setCMBEventTypeVisible(False)
        result.setEventTypeListListVisible(True)
        result.setSpecialityListVisible(True)
        return result


    def dumpParamsMultiSelect(self, cursor, params):
        description = []
        isEventTypeVisible = params.get('isEventTypeVisible', False)
        if not isEventTypeVisible:
            eventTypeList = params.get('eventTypeList', None)
            if eventTypeList:
                db = QtGui.qApp.db
                tableET = db.table('EventType')
                records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(eventTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                description.append(u'тип события:  %s'%(u','.join(name for name in nameList if name)))

        isSpecialityListVisible = params.get('isSpecialityListVisible', False)
        if isSpecialityListVisible:
            specialityList = params.get('specialityList', [])
            if specialityList:
                db = QtGui.qApp.db
                table = db.table('rbSpeciality')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(specialityList)])
                description.append(u'специальность:  %s'%(u', '.join(forceString(record.value('name')) for record in records if forceString(record.value('name')))))

        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)


    def build(self, params):
        detailChildren = params.get('detailChildren', False)
        scene = params.get('sceneId',  None) if self.additionalFields else None
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
        query = selectData(params, scene)

        columnShift = 0 if detailChildren else 1
        reportData = {}
        personInfoList = []
        MainRows = [u'A00 - T99.9, U00 - U99.9']
        mapMainRows = createMapCodeToRowIdx( [row for row in MainRows] )
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
            MKBRec    = normalizeMKB(forceString(record.value('MKB')))
            ageGroup  = forceInt(record.value('ageGroup'))
            reportRow[0] += cnt
            if MKBRec in mapMainRows.keys():#if illness:
                reportRow[1] += cnt
                if not detailChildren:
                    if ageGroup in (0, 1):
                        ageGroup = 0
                    else:
                        ageGroup = 1
                reportRow[2+ageGroup] += cnt
            sceneIndex = sceneIndexes.get(sceneId, 0)
            reportRow[5+sceneIndex*2-columnShift] += cnt
            if MKBRec in mapMainRows.keys():#if illness:
                reportRow[6+sceneIndex*2-columnShift] += cnt

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParamsMultiSelect(cursor, params)
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


from Ui_ReportF30Setup import Ui_ReportF30SetupDialog


class CReportF30SetupDialog(QtGui.QDialog, Ui_ReportF30SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
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
        self.eventTypeList = []
        self.specialityList = []
        self.setCMBEventTypeVisible(True)
        self.setEventTypeListListVisible(False)
        self.setSpecialityListVisible(False)
        self.setContingentTypeVisible(False)


    def setSpecialityListVisible(self, value):
        self.isSpecialityListVisible = value
        self.btnSpecialityList.setVisible(value)
        self.lblSpecialityList.setVisible(value)


    def setCMBEventTypeVisible(self, value):
        self.isEventTypeVisible = value
        self.cmbEventType.setVisible(value)
        self.lblEventType.setVisible(value)


    def setEventTypeListListVisible(self, value):
        self.btnEventTypeList.setVisible(value)
        self.lblEventTypeList.setVisible(value)


    def setInputDateVisible(self, value):
        if not value:
            self.grpUseInputDate.setChecked(value)
        self.grpUseInputDate.setVisible(value)


    def setContingentTypeVisible(self, value):
        self.btnContingentTypeList.setVisible(value)
        self.lblContingentTypeList.setVisible(value)


    def setAdditionalFieldsVisible(self, flag = True):
        self.cmbScene.setVisible(flag)
        self.lblScene.setVisible(flag)
        self.cmbOrgStructure.setVisible(not flag)
        self.lblOrgStructure.setVisible(not flag)
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId()) if flag else self.cmbScene.setValue(None)
        self.flag = flag


    def setPayPeriodVisible(self, value):
        pass


    def setWorkTypeVisible(self, value):
        pass


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setEventTypeVisible(self, visible=True):
        pass


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.grpUseInputDate.setChecked(bool(params.get('useInputDate', False)))
        self.edtBegInputDate.setDate(params.get('begInputDate', QDate.currentDate()))
        self.edtEndInputDate.setDate(params.get('endInputDate', QDate.currentDate()))
        self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbTypeFinance.setValue(params.get('typeFinanceId', None))
        self.cmbTariff.setCurrentIndex(params.get('tariff', 0))
        self.cmbSocStatusClass.setValue(params.get('socStatusClassId', None))
        self.cmbSocStatusType.setValue(params.get('socStatusTypeId', None))
        self.cmbVisitPayStatus.setCurrentIndex(params.get('visitPayStatus', 0))
        self.cmbGrouping.setCurrentIndex(params.get('groupingRows', 0))
        self.chkDetailChildren.setChecked(params.get('detailChildren', False))
        self.chkVisitHospital.setChecked(params.get('visitHospital', False))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.chkAmbulator.setChecked(params.get('onlyAmbulator', True))
        self.cmbIsEventClosed.setCurrentIndex(params.get('isEventClosed', 0))
        self.cmbScene.setValue(params.get('sceneId', None))
        if self.isEventTypeVisible:
            self.cmbEventType.setValue(params.get('eventTypeId', None))
        else:
            self.eventTypeList =  params.get('eventTypeList', [])
            if self.eventTypeList:
                self.lblEventTypeList.setText(formatEventTypeIdList(self.eventTypeList))
            else:
                self.lblEventTypeList.setText(u'не задано')
        if self.isSpecialityListVisible:
            self.specialityList = params.get('specialityList', [])
            if self.specialityList:
                self.lblSpecialityList.setText(formatSpecialityIdList(self.specialityList))
            else:
                self.lblSpecialityList.setText(u'не задано')
        self.contingentTypeList = params.get('contingentTypeIdList', [])
        self.lblSpecialityList.setText(formatContingentTypeList(self.contingentTypeList))


    def params(self):
        return dict(
            begDate         = self.edtBegDate.date(),
            endDate         = self.edtEndDate.date(),
            useInputDate    = self.grpUseInputDate.isChecked(),
            begInputDate    = self.edtBegInputDate.date(),
            endInputDate    = self.edtEndInputDate.date(),
            eventPurposeId  = self.cmbEventPurpose.value(),
            orgStructureId  = QtGui.qApp.currentOrgStructureId() if self.flag else self.cmbOrgStructure.value(),
            socStatusClassId = self.cmbSocStatusClass.value(),
            socStatusTypeId = self.cmbSocStatusType.value(),
            typeFinanceId   = self.cmbTypeFinance.value(),
            tariff          = self.cmbTariff.currentIndex(),
            visitPayStatus  = self.cmbVisitPayStatus.currentIndex(),
            groupingRows    = self.cmbGrouping.currentIndex(),
            detailChildren  = self.chkDetailChildren.isChecked(),
            visitHospital   = self.chkVisitHospital.isChecked(),
            sex             = self.cmbSex.currentIndex(),
            ageFrom         = self.edtAgeFrom.value(),
            ageTo           = self.edtAgeTo.value(),
            onlyAmbulator   = self.chkAmbulator.isChecked(),
            isEventClosed = self.cmbIsEventClosed.currentIndex(),
            sceneId = self.cmbScene.value()  if self.flag else None,
            eventTypeList   = self.eventTypeList if not self.isEventTypeVisible else [],
            eventTypeId     = self.cmbEventType.value() if self.isEventTypeVisible else None,
            isEventTypeVisible = self.isEventTypeVisible,
            specialityList   = self.specialityList if self.isSpecialityListVisible else [],
            isSpecialityListVisible = self.isSpecialityListVisible,
            contingentTypeIdList = self.contingentTypeList,
            )


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        if self.isEventTypeVisible:
            eventPurposeId = self.cmbEventPurpose.value()
            if eventPurposeId:
                filter = 'EventType.purpose_id=%d' % eventPurposeId
            else:
                filter = getWorkEventTypeFilter(isApplyActive=True)
            self.cmbEventType.setFilter(filter)


    @pyqtSignature('int')
    def on_cmbSocStatusClass_currentIndexChanged(self, index):
        socStatusClassId = self.cmbSocStatusClass.value()
        filter = ('class_id=%d' % socStatusClassId) if socStatusClassId else ''
        self.cmbSocStatusType.setFilter(filter)


    @pyqtSignature('')
    def on_btnEventTypeList_clicked(self):
        self.eventTypeList = []
        self.lblEventTypeList.setText(u'не задано')
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = u'EventType.purpose_id =%d' % eventPurposeId
        else:
            filter = getWorkEventTypeFilter(isApplyActive=True)
        dialog = CEventTypeListEditorDialog(self, filter)
        if dialog.exec_():
            self.eventTypeList = dialog.values()
            if self.eventTypeList:
                self.lblEventTypeList.setText(formatEventTypeIdList(self.eventTypeList))


    @pyqtSignature('')
    def on_btnSpecialityList_clicked(self):
        self.specialityList = []
        self.lblSpecialityList.setText(u'не задано')
        dialog = CSpecialityListDialog(self)
        if dialog.exec_():
            self.specialityList = dialog.values()
            if self.specialityList:
                self.lblSpecialityList.setText(formatSpecialityIdList(self.specialityList))


    @pyqtSignature('')
    def on_btnContingentTypeList_clicked(self):
        self.contingentTypeList = []
        self.lblContingentTypeList.setText(u'не задано')
        dialog = CContingentTypeListDialog(self)
        if dialog.exec_():
            self.contingentTypeList = dialog.values()
            if self.contingentTypeList:
                self.lblContingentTypeList.setText(formatContingentTypeList(self.contingentTypeList))
