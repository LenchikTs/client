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
from PyQt4.QtCore import QDate, QDateTime

from library.Utils       import forceDateTime, forceInt, forceRef, forceString, formatShortName

from Events.ActionStatus import CActionStatus
from Orgs.Utils          import getPersonInfo
from Reports.ReportBase  import CReportBase, createTable
from Reports.Report      import CReport
from Reports.ReportView  import CPageFormat
from library.DialogBase  import CDialogBase

from Reports.Ui_ReportIncomingDirectionsSetupDialog import Ui_ReportIncomingDirectionsSetupDialog


class CExternalIncomingDirectionsReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка о входящих внешних направлениях')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.orgId = QtGui.qApp.currentOrgId()
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CIncomingDirectionsSetup(parent)
        result.setTitle(self.title())
        return result


    def parseNotes(self, notes):
        number = ''
        otherText = []
        for note in notes:
            note = note.split('&#674')
            if len(note) == 2:
                if note[0] == u'Номер':
                    number = note[1]
                else:
                    otherText.append('%s: %s'%(note[0], note[1]))
        return number, '\n'.join(otherText)


    def selectData(self, params):
        data = {}
        mapOrgIdToName = {}
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableAP = db.table('ActionProperty')
        tableAPT = db.table('ActionPropertyType')
        tableAPO = db.table('ActionProperty_Organisation')
        tableAPS = db.table('ActionProperty_String')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableOrg = db.table('Organisation')

        begDate        = params.get('begDate', QDateTime.currentDateTime())
        endDate        = params.get('endDate', QDateTime.currentDateTime())
        actionTypeId   = params.get('actionTypeId', None)
        actionStatus   = params.get('actionStatus', None)
        personId       = params.get('personId', None)
        organisationId = params.get('organisationId', None)
        isDetalLPU     = params.get('isDetalLPU', True)

        orgTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        orgTable = orgTable.leftJoin(tableAPO, tableAPO['id'].eq(tableAP['id']))
        orgCond = [tableAP['action_id'].eq(tableAction['id']),
                   tableAPT['name'].eq(u'ЛПУ'),
                   tableAPT['typeName'].eq('Organisation'),
                   tableAPO['value'].eq(self.orgId)
                   ]
        orgCondNot = [tableAP['action_id'].eq(tableAction['id']),
                   tableAPT['name'].eq(u'ЛПУ'),
                   tableAPT['typeName'].eq('Organisation')
                   ]

        notesTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        notesTable = notesTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
        notesCond = [tableAP['action_id'].eq(tableAction['id']),
            db.joinOr([tableAPT['typeName'].eq('String'), tableAPT['typeName'].eq('Text')])]
        notesCols = u'''GROUP_CONCAT(CONCAT_WS('&#674', %s, %s) SEPARATOR '$&31#') as q'''%(tableAPT['name'].name(), tableAPS['value'].name())
        notesStrStmt = '(%s) AS notes'%db.selectStmt(notesTable, [notesCols], notesCond)

        table = tableAction.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        cond = [tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableAction['directionDate'].between(begDate, endDate),
                tableEvent['relegateOrg_id'].ne(self.orgId),
                tableEvent['relegateOrg_id'].isNotNull(),
                db.joinOr(['EXISTS(%s)'%(db.selectStmt(orgTable, [tableAPO['value'].name()], orgCond)),
                           'NOT EXISTS(%s)'%(db.selectStmt(orgTable, [tableAPO['id'].name()], orgCondNot))])
                ]
        cols = [tableClient['lastName'],
                tableClient['firstName'],
                tableClient['patrName'],
                tableClient['birthDate'],
                tableAction['begDate'],
                tableAction['status'],
                tableAction['plannedEndDate'],
                tableEvent['relegateOrg_id'].alias('organisation'),
                tableEvent['externalId'].alias('number'),
                tableAction['MKB'],
                notesStrStmt,
               ]

        tableAPSpeciality = db.table('ActionProperty_rbSpeciality')
        tableSpeciality = db.table('rbSpeciality')
        profileTable = tableAP.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        profileTable = profileTable.innerJoin(tableAPSpeciality, tableAPSpeciality['id'].eq(tableAP['id']))
        profileTable = profileTable.innerJoin(tableSpeciality,   tableSpeciality['id'].eq(tableAPSpeciality['value']))
        profileCond = [tableAP['action_id'].eq(tableAction['id']),
                       tableAPT['typeName'].eq(u'rbSpeciality')
                      ]
        profileStrStmt = '(%s) AS profileName'%(db.selectStmt(profileTable, [tableSpeciality['name'].name()], profileCond))
        cols.append(profileStrStmt)
        if actionStatus is not None:
            cond.append(tableAction['status'].eq(actionStatus))
        if personId:
            cond.append(tableAction['person_id'].eq(personId))

        if actionTypeId:
            cond.append(tableActionType['id'].eq(actionTypeId))
        else:
            cond.append(tableActionType['flatCode'].like('%Direction%'))

        if organisationId:
            cond.append(tableEvent['relegateOrg_id'].eq(organisationId))
        if actionTypeId is None and actionStatus is None:
            if personId:
                persAct = ''' and Action.person_id = %s'''%(personId)
                persEve = ''' and Event.execPerson_id = %s'''%(personId)
            else:
                persAct = ''
                persEve = ''
            if organisationId:
                orgEve = ''' and Event.relegateOrg_id = %s'''%(organisationId)
            else:
                orgEve = ''

            db = QtGui.qApp.db
            stmt = u'''SELECT 
  Client.`lastName`, Client.`firstName`, Client.`patrName`, Client.`birthDate`, Action.`begDate`, Action.`status`, 
  Action.`plannedEndDate`, Event.`relegateOrg_id` AS `organisation`, 
  (SELECT GROUP_CONCAT(CONCAT_WS('&#674', ActionPropertyType.`name`, ActionProperty_String.`value`) SEPARATOR '$&31#') as q 
    FROM ActionProperty 
    LEFT JOIN ActionPropertyType ON ActionPropertyType.`id`=ActionProperty.`type_id`  
    LEFT JOIN ActionProperty_String ON ActionProperty_String.`id`=ActionProperty.`id`   
    WHERE (ActionProperty.`action_id`=Action.`id`) AND (((ActionPropertyType.`typeName`='String') 
    OR (ActionPropertyType.`typeName`='Text')))  ) AS notes, 
  (SELECT ActionProperty_String.`value` FROM ActionProperty LEFT JOIN ActionPropertyType ON ActionPropertyType.`id`=ActionProperty.`type_id`  
    LEFT JOIN ActionProperty_String ON ActionProperty_String.`id`=ActionProperty.`id`   
    WHERE (ActionProperty.`action_id`=Action.`id`) AND (ActionPropertyType.`name` LIKE 'Номер%%') 
    AND (ActionPropertyType.`typeName`='Счетчик')  ) AS number 
  
  FROM Action 
  LEFT JOIN ActionType ON ActionType.`id`=Action.`actionType_id`  
  LEFT JOIN Event ON Event.`id`=Action.`event_id`  
  LEFT JOIN Client ON Client.`id`=Event.`client_id`  
  WHERE (Action.`deleted`=0) AND (ActionType.`deleted`=0) 
  AND (ActionType.`flatCode` LIKE '%%Direction%%') 
  AND ((Action.`directionDate` BETWEEN %(begDate)s  AND %(endDate)s)) 
  AND (Event.`relegateOrg_id`!=%(org_)s ) 
  AND (Event.`relegateOrg_id` IS NOT NULL) 
  AND (((EXISTS(SELECT ActionProperty_Organisation.`value` 
    FROM ActionProperty 
    LEFT JOIN ActionPropertyType ON ActionPropertyType.`id`=ActionProperty.`type_id`  
    LEFT JOIN ActionProperty_Organisation ON ActionProperty_Organisation.`id`=ActionProperty.`id`   
    WHERE (ActionProperty.`action_id`=Action.`id`) AND (ActionPropertyType.`name`='ЛПУ') 
    AND (ActionPropertyType.`typeName`='Organisation') AND (ActionProperty_Organisation.`value`=%(org_)s )  )) 
  OR (NOT EXISTS(SELECT ActionProperty_Organisation.`id` 
    FROM ActionProperty 
    LEFT JOIN ActionPropertyType ON ActionPropertyType.`id`=ActionProperty.`type_id`  
    LEFT JOIN ActionProperty_Organisation ON ActionProperty_Organisation.`id`=ActionProperty.`id`   
    WHERE (ActionProperty.`action_id`=Action.`id`) AND (ActionPropertyType.`name`='ЛПУ') 
    AND (ActionPropertyType.`typeName`='Organisation')  )))) %(persAct)s %(orgEve)s 
    
    UNION ALL

  SELECT c.`lastName`, c.`firstName`, c.`patrName`, c.`birthDate`, 
     e.srcDate as begDate, '10' as status, '' as plannedEndDate, e.`relegateOrg_id` AS `organisation`,e.note,e.srcNumber as number
    FROM Event e
    LEFT JOIN Client c ON e.client_id = c.id
WHERE e.deleted=0 
    AND (e.srcDate BETWEEN %(begDate)s AND %(endDate)s) 
    AND e.srcNumber IS NOT NULL 
    AND e.srcNumber!='' 
    AND e.relegateOrg_id!= %(org_)s  
    AND e.relegateOrg_id IS NOT NULL 
    AND e.relegateOrg_id!=''
    AND e.srcDate != '' 
    AND e.srcDate IS NOT NULL %(persEve)s %(orgEve)s 
                '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate),
                    org_=self.orgId,
                    persAct=persAct,
                    persEve=persEve,
                    orgEve=orgEve
                    )
            db = QtGui.qApp.db
            query = db.query(stmt)
            while query.next():
                record = query.record()
                name = formatShortName(record.value('lastName'), record.value('firstName'), record.value('patrName'))
                birthDate = forceString(record.value('birthDate'))
                status = forceInt(record.value('status'))
                if status != 10:
                    actionStatus = CActionStatus.text(status)
                else:
                    actionStatus = ''
                plannedEndDate = forceString(record.value('plannedEndDate'))
                actDate = forceString(record.value('begDate'))
                notes = forceString(record.value('notes')).split('$&31#')
                orgId = forceRef(record.value('organisation'))
                orgName = mapOrgIdToName.get(orgId, u'')
                numberFirst = forceString(record.value('number'))
                if not orgName:
                    orgName = forceString(db.translate(tableOrg, 'id', orgId, 'shortName'))
                    mapOrgIdToName[orgId] = orgName
                numberTwo, otherText = self.parseNotes(notes)
                if isDetalLPU:
                    rows = data.setdefault((orgName, orgId), [])
                    row = [''] * 7
                    row[0] = name
                    row[1] = birthDate
                    row[2] = actDate
                    row[3] = actionStatus
                    row[4] = plannedEndDate
                    row[5] = numberFirst if numberFirst else numberTwo
                    row[6] = otherText
                    rows.append(row)
                else:
                    row = data.setdefault((orgName, orgId), [0] * 5)
                    row[0] += 1
                    if status in (CActionStatus.wait, CActionStatus.withoutResult):
                        row[1] += 1
                    if status == (CActionStatus.canceled, CActionStatus.refused):
                        row[2] += 1
                    if status in (CActionStatus.started, CActionStatus.appointed) and plannedEndDate:
                        row[3] += 1
                    if status == CActionStatus.finished:
                        row[4] += 1
            return data
        else:
            recordList = db.getRecordList(table, cols, cond)
            for record in recordList:
                name = formatShortName(record.value('lastName'), record.value('firstName'), record.value('patrName'))
                birthDate = forceString(record.value('birthDate'))
                status = forceInt(record.value('status'))
                if status != 10:
                    actionStatus = CActionStatus.text(status)
                else:
                    actionStatus = ''
                plannedEndDate = forceString(record.value('plannedEndDate'))
                actDate = forceString(record.value('begDate'))
                notes = forceString(record.value('notes')).split('$&31#')
                orgId = forceRef(record.value('organisation'))
                profileName = forceString(record.value('profileName'))
                MKB = forceString(record.value('MKB'))
                orgName = mapOrgIdToName.get(orgId, u'')
                numberFirst = forceString(record.value('number'))
                if not orgName:
                    orgName = forceString(db.translate(tableOrg, 'id', orgId, 'shortName'))
                    mapOrgIdToName[orgId] = orgName
                numberTwo, otherText = self.parseNotes(notes)
                if isDetalLPU:
                    rows = data.setdefault((orgName, orgId), [])
                    row = ['']*9
                    row[0] = name
                    row[1] = birthDate
                    row[2] = actDate
                    row[3] = actionStatus
                    row[4] = plannedEndDate
                    row[5] = numberFirst if numberFirst else numberTwo
                    row[6] = MKB
                    row[7] = profileName
                    row[8] = otherText
                    rows.append(row)
                else:
                    row = data.setdefault((orgName, orgId), [0]*7)
                    row[0] += 1
                    if status in (CActionStatus.wait, CActionStatus.withoutResult):
                        row[1] += 1
                    if status in (CActionStatus.canceled, CActionStatus.refused):
                        row[2] += 1
                    if status in (CActionStatus.started, CActionStatus.appointed) and plannedEndDate:
                        row[3] += 1
                    if status == CActionStatus.finished:
                        row[4] += 1
                    row[5] = MKB
                    row[6] = profileName
        return data




    def build(self, params):
        isDetalLPU = params.get('isDetalLPU', True)
        data = self.selectData(params)
        if isDetalLPU:
            tableColumns = [
                            ('5%',  [u'№ п/п'],             CReportBase.AlignRight),
                            ('15%', [u'ФИО'],               CReportBase.AlignLeft),
                            ('10%', [u'Д/р'],               CReportBase.AlignLeft),
                            ('10%', [u'Дата направления'],  CReportBase.AlignLeft),
                            ('10%', [u'Состояние'],         CReportBase.AlignLeft),
                            ('10%', [u'Плановая дата'],     CReportBase.AlignLeft),
                            ('10%', [u'Номер направления'], CReportBase.AlignLeft),
                            ('10%', [u'Диагноз'],           CReportBase.AlignLeft),
                            ('10%', [u'Профиль'],           CReportBase.AlignLeft),
                            ('10%', [u'Примечания'],        CReportBase.AlignLeft),
                           ]
        else:
            tableColumns = [
                            ('10%', [u'№ п/п',              u'',       u''                                  ], CReportBase.AlignRight),
                            ('40%', [u'Организация',        u'',       u''                                  ], CReportBase.AlignLeft),
                            ('10%', [u'Кол-во направлений', u'всего',  u''                                  ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'в т.ч.', u'ожидание'], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'отмена'                            ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'назначено'                         ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'закончено'                         ], CReportBase.AlignRight),
                           ]
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)
        if not isDetalLPU:
            table.mergeCells(0, 0, 3, 1)
            table.mergeCells(0, 1, 3, 1)
            table.mergeCells(0, 2, 1, 7)
            table.mergeCells(1, 2, 2, 1)
            table.mergeCells(1, 3, 1, 4)
        orgNames = data.keys()
        orgNames.sort()
        iRow = 1
        totalIRow = 0
        totalIRowAll = 0
        total = [0]*5
        for orgName, orgId in orgNames:
            rows = data.get((orgName, orgId), [])
            if orgName == u'':
                orgName = u'Организация не указана'
            if isDetalLPU:
                iRow = 1
                totalIRow = 0
                i = table.addRow()
                table.setText(i, 0, orgName, charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                table.mergeCells(i, 0, 1, 10)
                for row in rows:
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    for col in xrange(len(row)-1):
                        table.setText(i, col+1, row[col])
                    iRow += 1
                    totalIRow += 1
                    totalIRowAll += 1
                i = table.addRow()
                table.setText(i, 0, u'Итого по %s'%(orgName), charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                table.setText(i, 2, totalIRow, charFormat=CReportBase.ReportSubTitle)
                table.mergeCells(i, 0, 1, 2)
                table.mergeCells(i, 2, 1, 8)
            else:
                if rows:
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    table.setText(i, 1, orgName)
                    iRow += 1
                    for col, val in enumerate(rows):
                        if col < 5:
                            table.setText(i, col+2, val)
                            total[col] += val
        if data:
            i = table.addRow()
            if isDetalLPU:
                table.setText(i, 0, u'Всего направлений', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                table.mergeCells(i, 0, 1, 2)
                table.setText(i, 2, totalIRowAll, charFormat=CReportBase.ReportSubTitle)
                table.mergeCells(i, 2, 1, 8)
            else:
                table.setText(i, 0, u'Итого', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignRight)
                table.mergeCells(i, 0, 1, 2)
                for col, val in enumerate(total):
                    table.setText(i, col+2, val, charFormat=CReportBase.ReportSubTitle)
        return doc


    def getDescription(self, params):
        db = QtGui.qApp.db
        def dateRangeAsStr(begDate, endDate):
            result = ''
            if begDate:
                result += u' с '+forceString(begDate)
            if endDate:
                result += u' по '+forceString(endDate)
            return result
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        personId = params.get('personId', None)
        actionTypeId = params.get('actionTypeId', None)
        actionStatus = params.get('actionStatus', None)
        organisationId = params.get('organisationId', None)
        isDetalLPU     = params.get('isDetalLPU', True)
        rows = []
        if begDate or endDate:
            rows.append(u'за период' + dateRangeAsStr(begDate, endDate))
        if actionTypeId:
            actionTypeName=forceString(db.translate('ActionType', 'id', actionTypeId, 'name'))
            rows.append(u'мероприятие: '+actionTypeName)
        if actionStatus is not None:
            rows.append(u'статус выполнения действия: '+ CActionStatus.text(actionStatus))
        if organisationId is not None:
            rows.append(u'направитель: '+ forceString(db.translate('Organisation', 'id', organisationId, 'shortName')))
        if personId:
            personInfo = getPersonInfo(personId)
            rows.append(u'исполнитель: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        if isDetalLPU:
            rows.append(u'детализировать по Целевым ЛПУ')
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


class CIncomingDirectionsSetup(CDialogBase, Ui_ReportIncomingDirectionsSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbActionStatus.insertSpecialValue(u'не задано', None)
        db = QtGui.qApp.db
        table = db.table('ActionType')
        cond = [table['flatCode'].like('%Direction%'),
                table['deleted'].eq(0),
                table['class'].eq(3)
               ]
        recordList = db.getRecordList(table, 'id, code, name',  cond, order='code, name')
        self.actionTypes = [None]
        self.actionTypeFlatCodes = [None]
        self.cmbActionType.addItem(u'Любой')
        for record in recordList:
            id = forceInt(record.value('id'))
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            self.actionTypes.append(id)
            self.cmbActionType.addItem('%s| %s'%(code, name))


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        begDate = forceDateTime(params.get('begDate', QDateTime.currentDateTime()))
        endDate = forceDateTime(params.get('endDate', QDateTime.currentDateTime()))
        self.edtBegDate.setDate(begDate.date())
        self.edtEndDate.setDate(endDate.date())
        self.edtBegTime.setTime(begDate.time())
        self.edtEndTime.setTime(endDate.time())
        self.cmbActionStatus.setValue(params.get('actionStatus', None))
        self.cmbOrganisation.setValue(params.get('organisationId', None))
        self.cmbActionType.setCurrentIndex(params.get('actionTypeIndex', 0))
        self.cmbPerson.setValue(params.get('personId', None))
        self.chkDetalLPU.setChecked(params.get('isDetalLPU', True))


    def params(self):
        result = {}
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        begTime = self.edtBegTime.time()
        endTime = self.edtEndTime.time()
        result['begDate'] = QDateTime(begDate, begTime)
        result['endDate'] = QDateTime(endDate, endTime)
        result['actionStatus'] = self.cmbActionStatus.value()
        result['personId'] = self.cmbPerson.value()
        actionTypeIndex = self.cmbActionType.currentIndex()
        result['actionTypeIndex'] = actionTypeIndex
        result['actionTypeId'] = self.actionTypes[actionTypeIndex]
        result['organisationId'] = self.cmbOrganisation.value()
        result['isDetalLPU'] = self.chkDetalLPU.isChecked()
        return result
