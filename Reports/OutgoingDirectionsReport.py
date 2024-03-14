# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2024 SAMSON Group. All rights reserved.
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

from library.Utils       import forceInt, forceRef, forceString, formatShortName, agreeNumberAndWord
from Events.ActionStatus import CActionStatus
from Orgs.Utils          import getOrgStructureDescendants, getOrgStructureFullName, getPersonInfo
from Reports.ReportBase  import CReportBase, createTable
from Reports.Report      import CReport
from Reports.ReportView  import CPageFormat
from Reports.Utils       import dateRangeAsStr
from Reports.ReportExternalDirections import CExternalDirectionsSetup


class COutgoingDirectionsReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка об исходящих направлениях')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.orgId = QtGui.qApp.currentOrgId()
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CExternalDirectionsSetup(parent)
        result.setAgeVisible(True)
        result.setMKBFilterVisible(True)
        result.setCalculationNotesVisible(True)
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
                elif note[1] != u'':
                    otherText.append('%s: %s' % (note[0], note[1]))
        return number, '\n'.join(otherText)


    def selectData(self, params):
        data = {}
        mapOrgIdToName = {}
        actionIdList = []
        reportPropertyData = {}
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
        tablePerson = db.table('Person')

        begDate        = params.get('begDate', QDateTime.currentDateTime())
        endDate        = params.get('endDate', QDateTime.currentDateTime())
        actionTypeId   = params.get('actionTypeId', None)
        actionStatus   = params.get('actionStatus', None)
        personId       = params.get('personId', None)
        organisationId = params.get('organisationId', None)
        isDetalLPU     = params.get('isDetalLPU', True)
        orgStructureId = params.get('orgStructureId', None)
        isSortFIO      = params.get('isSortFIO', False)
        isCalculationNotes = params.get('isCalculationNotes', False)
        MKBFilter          = params.get('MKBFilter', 0)
        MKBFrom            = params.get('MKBFrom', 'A00')
        MKBTo              = params.get('MKBTo', 'Z99.9')
        ageFrom            = params.get('ageFrom', None)
        ageTo              = params.get('ageTo', None)

        orgTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        orgTable = orgTable.leftJoin(tableAPO, tableAPO['id'].eq(tableAP['id']))
        orgCond = [tableAP['action_id'].eq(tableAction['id']),
                   tableAP['deleted'].eq(0),
                   tableAPT['deleted'].eq(0),
                   tableAPT['name'].eq(u'Куда направляется'),
                   tableAPT['typeName'].eq('Organisation')
                   ]
        orgStrStmt = '(%s) AS organisation'%(db.selectStmt(orgTable, [tableAPO['value'].name()], orgCond))

        numberTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        numberTable = numberTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
        numberCond = [tableAP['action_id'].eq(tableAction['id']),
                      tableAP['deleted'].eq(0),
                      tableAPT['deleted'].eq(0),
                      tableAPT['name'].like(u'Номер%'),
                      tableAPT['typeName'].eq(u'Счетчик')
                     ]
        numberStrStmt = '(%s) AS number'%(db.selectStmt(numberTable, [tableAPS['value'].name()], numberCond))

        notesTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        notesTable = notesTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
        notesCond = [tableAP['action_id'].eq(tableAction['id']),
                     tableAP['deleted'].eq(0),
                     tableAPT['deleted'].eq(0),
                     u'''(TRIM(ActionProperty_String.value) IS NOT NULL AND (TRIM(ActionProperty_String.value) != '' OR TRIM(ActionProperty_String.value) != ' '))''',
                     db.joinOr([tableAPT['typeName'].eq('String'), tableAPT['typeName'].eq('Text')])
                     ]
        notesCols = u'''GROUP_CONCAT(CONCAT_WS('&#674', %s, %s) SEPARATOR '$&31#') as q'''%(tableAPT['name'].name(), tableAPS['value'].name())
        notesStrStmt = '(%s) AS notes'%db.selectStmt(notesTable, [notesCols], notesCond)

        table = tableAction.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        table = table.leftJoin(tablePerson, db.joinAnd([tablePerson['id'].eq(tableAction['person_id']), tablePerson['deleted'].eq(0)]))
#        orgCond.append(tableAPO['value'].ne(self.orgId))
        cond = [tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableActionType['flatCode'].like('%Direction%'),
                tableAction['directionDate'].between(begDate, endDate),
#                'EXISTS(%s)'%(db.selectStmt(orgTable, [tableAPO['value'].name()], orgCond))
                ]
        cols = [tableClient['id'].alias('clientId'),
                tableClient['lastName'],
                tableClient['firstName'],
                tableClient['patrName'],
                tableClient['birthDate'],
                tableAction['begDate'],
                tableAction['status'],
                tableAction['plannedEndDate'],
                tableAction['MKB'].alias('ActionMKB'),
                tableAction['person_id'].alias('person'),
                tableAction['id'].alias('actionId'),
                orgStrStmt,
                notesStrStmt,
                numberStrStmt
               ]
        cols.append(u'''(SELECT Diagnosis.MKB FROM Diagnosis WHERE Diagnosis.id = (SELECT getEventDiagnosis(Event.id)) AND Diagnosis.deleted = 0) AS MKB''')
        tableAPHBP = db.table('ActionProperty_rbHospitalBedProfile')
        tableHBP = db.table('rbHospitalBedProfile')
        profileTable = tableAP.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        profileTable = profileTable.innerJoin(tableAPHBP, tableAPHBP['id'].eq(tableAP['id']))
        profileTable = profileTable.innerJoin(tableHBP,   tableHBP['id'].eq(tableAPHBP['value']))
        profileCond = [tableAP['action_id'].eq(tableAction['id']),
                       tableAP['deleted'].eq(0),
                       tableAPT['deleted'].eq(0),
                       tableAPT['typeName'].eq(u'rbHospitalBedProfile')
                      ]
        profileStrStmt = '(%s) AS profileName'%(db.selectStmt(profileTable, [tableHBP['name'].name()], profileCond))
        cols.append(profileStrStmt)
        if actionStatus is not None:
            cond.append(tableAction['status'].eq(actionStatus))
        if orgStructureId:
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
        if personId:
            cond.append(tableAction['person_id'].eq(personId))
        if actionTypeId:
            cond.append(tableActionType['id'].eq(actionTypeId))
        if organisationId:
            orgCond.append(tableAPO['value'].eq(organisationId))
            cond.append(db.existsStmt(orgTable, orgCond))
        if MKBFilter == 1:
            cond.append(tableAction['MKB'].ge(MKBFrom))
            cond.append(tableAction['MKB'].le(MKBTo))
        if ageFrom <= ageTo:
                cond.append('Action.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)' % ageFrom)
                cond.append('Action.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)' % (ageTo+1))
        order = u''
        if isSortFIO:
            order = u'Client.lastName, Client.firstName, Client.patrName'
        recordList = db.getRecordList(table, cols, cond, order)
        for record in recordList:
            clientId = forceString(record.value('clientId'))
            name = formatShortName(record.value('lastName'), record.value('firstName'), record.value('patrName')) + u', ' + clientId
            birthDate = forceString(record.value('birthDate'))
            status = forceInt(record.value('status'))
            actionStatus = CActionStatus.text(status)
            plannedEndDate = forceString(record.value('plannedEndDate'))
            actDate = forceString(record.value('begDate'))
            notes = forceString(record.value('notes')).split('$&31#')
            numberFirst = forceString(record.value('number'))
            orgId = forceRef(record.value('organisation'))
            profileName = forceString(record.value('profileName'))
            MKB = forceString(record.value('MKB'))
            ActionMKB = forceString(record.value('ActionMKB'))
            person = forceString(QtGui.qApp.db.translate('vrbPersonWithSpeciality', 'id', forceRef(record.value('person')), 'name'))
            orgName = mapOrgIdToName.get(orgId, u'')
            if not orgName:
                orgName = forceString(db.translate(tableOrg, 'id', orgId, 'shortName'))
                mapOrgIdToName[orgId] = orgName
            numberTwo, otherText = self.parseNotes(notes)
            if isDetalLPU:
                rows = data.setdefault((orgName, orgId), [])
                row = ['']*11
                row[0] = name
                row[1] = birthDate
                row[2] = actDate
                row[3] = actionStatus
                row[4] = plannedEndDate
                row[5] = numberFirst if numberFirst else numberTwo
                row[6] = MKB
                row[7] = ActionMKB
                row[8] = person
                row[9] = profileName
                row[10] = otherText
                rows.append(row)
            else:
                row = data.setdefault((orgName, orgId), [0]*8)
                row[0] += 1
                if status in (CActionStatus.wait, CActionStatus.withoutResult):
                    row[1] += 1
                if status == (CActionStatus.canceled, CActionStatus.refused):
                    row[2] += 1
                if status in (CActionStatus.started, CActionStatus.appointed) and plannedEndDate:
                    row[3] += 1
                if status == CActionStatus.finished:
                    row[4] += 1
                row[5] = MKB
                row[6] = ActionMKB
                row[7] = profileName
            if isCalculationNotes:
                actionId = forceRef(record.value('actionId'))
                if actionId and actionId not in actionIdList:
                    actionIdList.append(actionId)
        if isCalculationNotes and actionIdList:
            notesTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
            notesTable = notesTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
            notesCond = [tableAP['deleted'].eq(0),
                         tableAPT['deleted'].eq(0),
                         tableAP['action_id'].inlist(actionIdList),
                         u'''(TRIM(ActionProperty_String.value) IS NOT NULL AND (TRIM(ActionProperty_String.value) != '' OR TRIM(ActionProperty_String.value) != ' '))''',
                         db.joinOr([tableAPT['typeName'].eq('String'), tableAPT['typeName'].eq('Text')])
                        ]
            notesCols = u'''COUNT(ActionPropertyType.name) AS APTCount, ActionPropertyType.name AS APTName'''
            records = db.getRecordListGroupBy(notesTable, [notesCols], notesCond, tableAPT['name'].name(), tableAPT['name'].name())
            for record in records:
                APTCount = forceInt(record.value('APTCount'))
                APTName = forceString(record.value('APTName'))
                reportProperty = reportPropertyData.get(APTName, 0)
                reportProperty += APTCount
                reportPropertyData[APTName] = reportProperty
        return data, reportPropertyData


    def build(self, params):
        isDetalLPU = params.get('isDetalLPU', True)
        isCalculationNotes = params.get('isCalculationNotes', False)
        data, reportPropertyData = self.selectData(params)
        if isDetalLPU:
            tableColumns = [
                            ('5%',  [u'№ п/п'],             CReportBase.AlignRight),
                            ('10%', [u'ФИО'],               CReportBase.AlignLeft),
                            ('10%', [u'Д/р'],               CReportBase.AlignLeft),
                            ('5%', [u'Дата направления'],  CReportBase.AlignLeft),
                            ('10%', [u'Состояние'],         CReportBase.AlignLeft),
                            ('5%', [u'Плановая дата'],     CReportBase.AlignLeft),
                            ('10%', [u'Номер направления'], CReportBase.AlignLeft),
                            ('5%', [u'Диагноз'],           CReportBase.AlignLeft),
                            ('5%', [u'Диагноз направителя'],           CReportBase.AlignLeft),
                            ('10%', [u'Направитель'],           CReportBase.AlignLeft),
                            ('10%', [u'Профиль'],           CReportBase.AlignLeft),
                            ('10%', [u'Примечания'],        CReportBase.AlignLeft),
                           ]
        else:
            tableColumns = [
                            ('5%',  [u'№ п/п',              u'',       u''                                  ], CReportBase.AlignRight),
                            ('15%', [u'Организация',        u'',       u''                                  ], CReportBase.AlignLeft),
                            ('10%', [u'Кол-во направлений', u'всего',  u''                                  ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'в т.ч.', u'ожидание'], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'отмена'                            ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'назначено'                         ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'закончено'                         ], CReportBase.AlignRight),
                            ('10%', [u'',                   u'',       u'диагноз'                           ], CReportBase.AlignLeft),
                            ('10%', [u'',                   u'',       u'диагноз направителя'                           ], CReportBase.AlignLeft),
                            ('10%', [u'',                   u'',       u'профиль'                           ], CReportBase.AlignLeft),
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
                table.mergeCells(i, 0, 1, 12)
                for row in rows:
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    for col in xrange(11):
                        table.setText(i, col+1, row[col])
                    iRow += 1
                    totalIRow += 1
                    totalIRowAll += 1
                i = table.addRow()
                table.setText(i, 0, u'Итого по %s'%(orgName), charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                table.setText(i, 2, totalIRow, charFormat=CReportBase.ReportSubTitle)
                table.mergeCells(i, 0, 1, 2)
                table.mergeCells(i, 2, 1, 11)
            else:
                if rows:
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    table.setText(i, 1, orgName)
                    iRow += 1
                    for col, val in enumerate(rows):
                        table.setText(i, col+2, val)
                        if col < 5:
                            total[col] += val
        if data:
            i = table.addRow()
            if isDetalLPU:
                table.setText(i, 0, u'Всего направлений', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                table.mergeCells(i, 0, 1, 2)
                table.setText(i, 2, totalIRowAll, charFormat=CReportBase.ReportSubTitle)
                table.mergeCells(i, 2, 1, 11)
            else:
                table.setText(i, 0, u'Итого', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignRight)
                table.mergeCells(i, 0, 1, 2)
                for col, val in enumerate(total):
                    table.setText(i, col+2, val, charFormat=CReportBase.ReportSubTitle)
        if isCalculationNotes:
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            columns = [ ('100%', [], CReportBase.AlignLeft) ]
            table = createTable(cursor, columns, headerRowCount=len(reportPropertyData.keys()), border=0, cellPadding=2, cellSpacing=0)
            reportPropertyKeys = reportPropertyData.keys()
            reportPropertyKeys.sort()
            for row, APTName in enumerate(reportPropertyKeys):
                APTCount = reportPropertyData.get(APTName, 0)
                table.setText(row, 0, APTName + u' - ' + forceString(APTCount), charFormat=CReportBase.ReportSubTitle)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
        return doc


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        personId = params.get('personId', None)
        actionTypeId = params.get('actionTypeId', None)
        actionStatus = params.get('actionStatus', None)
        organisationId = params.get('organisationId', None)
        isDetalLPU     = params.get('isDetalLPU', True)
        orgStructureId = params.get('orgStructureId', None)
        MKBFilter = params.get('MKBFilter', 0)
        MKBFrom = params.get('MKBFrom', 'A00')
        MKBTo = params.get('MKBTo', 'Z99.9')
        ageFrom = params.get('ageFrom', None)
        ageTo = params.get('ageTo', None)
        rows = []
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if actionTypeId:
            actionTypeName=forceString(db.translate('ActionType', 'id', actionTypeId, 'name'))
            rows.append(u'мероприятие: '+actionTypeName)
        if actionStatus is not None:
            rows.append(u'статус выполнения действия: '+ CActionStatus.text(actionStatus))
        if organisationId is not None:
            rows.append(u'целевое ЛПУ: '+ forceString(db.translate('Organisation', 'id', organisationId, 'shortName')))
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        if personId:
            personInfo = getPersonInfo(personId)
            rows.append(u'направитель: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        if isDetalLPU:
            rows.append(u'детализировать по Целевым ЛПУ')
        if MKBFilter:
            MKBFrom = params.get('MKBFrom', 'A00')
            MKBTo = params.get('MKBTo',   'Z99.9')
            rows.append(u'коды диагнозов по МКБ с %s по %s'%(forceString(MKBFrom), forceString(MKBTo)))
        if ageFrom is not None and ageTo is not None and ageFrom <= ageTo:
            rows.append(u'возраст: c %d по %d %s' % (ageFrom, ageTo, agreeNumberAndWord(ageTo, (u'год', u'года', u'лет'))))
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows

