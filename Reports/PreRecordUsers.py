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
from PyQt4.QtCore import *

from Reports.Report     import *
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr

from Timeline.Schedule  import CSchedule
from library.DialogBase import CDialogBase
from library.Utils      import *
from Orgs.Utils import getOrgStructureDescendants

from Reports.Ui_PreRecordUsersSetupDialog  import Ui_PreRecordUsersSetupDialog

def selectData(params):
    useRecordPeriod   = params.get('useRecordPeriod', True)
    begRecordDate     = params.get('begRecordDate', None)
    endRecordDate     = params.get('endRecordDate', None)
    useSchedulePeriod = params.get('useSchedulePeriod', False)
    begScheduleDate   = params.get('begScheduleDate', None)
    endScheduleDate   = params.get('endScheduleDate', None)
    orgStructureId    = params.get('orgStructureId', None)
    specialityId      = params.get('specialityId', None)
    specialityFilter  = params.get('specialityFilter', False)
    personId          = params.get('personId', None)
    showDeleted          = params.get('showDeleted', None)

    db = QtGui.qApp.db
    tablePerson = db.table('Person')
    tableSchedule = db.table('Schedule')
    tableScheduleItem = db.table('Schedule_Item')

    cond = [ tableScheduleItem['client_id'].isNotNull(), 
           ]

    if not showDeleted:
        cond.append(tableSchedule['deleted'].eq(0))
        cond.append(tableScheduleItem['deleted'].eq(0))
    if useRecordPeriod:
        if begRecordDate:
            cond.append(tableScheduleItem['recordDatetime'].ge(begRecordDate))
        if endRecordDate:
            cond.append(tableScheduleItem['recordDatetime'].lt(endRecordDate.addDays(1)))
    if useSchedulePeriod:
        if begScheduleDate:
            cond.append(tableSchedule['date'].ge(begScheduleDate))
        if endScheduleDate:
            cond.append(tableSchedule['date'].le(endScheduleDate))
    if personId:
        cond.append(tableSchedule['person_id'].eq(personId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    orderBy = u''
    if specialityFilter:
        orderBy = u' ORDER BY rbSpeciality.code, rbSpeciality.name'
        cond.append('''RP.speciality_id IS NOT NULL''')
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        if not personId:
            cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))

    stmt =  '''SELECT
             COUNT(1) AS cnt,
             Schedule.appointmentType,
             Schedule_Item.recordClass,
             Schedule_Item.recordPerson_id AS person_id,
             IF(Schedule_Item.recordClass = 2, Schedule_Item.note, RP.name) AS name,
             (Schedule.person_id <=> Schedule_Item.recordPerson_id) AS samePerson,
             EXISTS(SELECT 1 FROM vVisitExt
                                   WHERE vVisitExt.client_id = Schedule_Item.client_id
                                   AND Person.speciality_id=vVisitExt.speciality_id
                                   AND DATE(vVisitExt.date) = Schedule.date
                   ) AS visited, Schedule_Item.note
            FROM
            Schedule_Item
            LEFT JOIN Schedule     ON Schedule.id = Schedule_Item.master_id
            LEFT JOIN Person       ON Person.id = Schedule.person_id
            LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
            LEFT JOIN vrbPersonWithSpeciality AS RP ON RP.id = Schedule_Item.recordPerson_id
            WHERE %s
            GROUP BY person_id, name, appointmentType, samePerson,
                      recordClass, visited
            %s'''
    return db.query(stmt % (db.joinAnd(cond), orderBy))


class CPreRecordUsers(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Предварительная запись по пользователям')

    def dumpParams(self, cursor, params):
        description = []
        db = QtGui.qApp.db
        useRecordPeriod = params.get('useRecordPeriod', True)
        begRecordDate = params.get('begRecordDate', None)
        endRecordDate = params.get('endRecordDate', None)
        useSchedulePeriod = params.get('useSchedulePeriod', False)
        begScheduleDate = params.get('begScheduleDate', None)
        endScheduleDate = params.get('endScheduleDate', None)
        orgStructureId = params.get('orgStructureId', None)
        specialityFilter = params.get('specialityFilter', False)
        specialityId = params.get('specialityId', None)
        personId = params.get('personId', None)
        detailCallCenter = params.get('detailCallCenter', False)
        showDeleted = params.get('showDeleted', None)

        if useRecordPeriod:
            if begRecordDate or endRecordDate:
                description.append(dateRangeAsStr(u'период постановки в очередь', begRecordDate, endRecordDate))
        if useSchedulePeriod:
            if begScheduleDate or endScheduleDate:
                description.append(dateRangeAsStr(u'период планируемого приёма', begScheduleDate, endScheduleDate))
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')
        if specialityId:
            description.append(u'специальность: ' + forceString(db.translate('rbSpeciality', 'id', specialityId, 'name')))
        if personId:
            personInfo = getPersonInfo(personId)
            description.append(u'врач: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        if detailCallCenter:
            description.append(u'Детализировать Call-центр')
        if showDeleted:
            description.append(u'учитывать удаленные записи')
        if specialityFilter:
            description.append(u'врачи-специалисты')
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, description, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        detailCallCenter = params.get('detailCallCenter', False)
        self.makeTable(cursor, doc, self.analyzeData(detailCallCenter, selectData(params)))
        return doc

    def analyzeData(self, detailCallCenter, query):
        mapATtoCol = { CSchedule.atAmbulance:1, CSchedule.atHome:4 }
        reportData = []
        reportDict = {}

        while query.next():
            record = query.record()
            appointmentType = forceInt(record.value('appointmentType'))
            personId        = forceRef(record.value('person_id'))
            name            = forceString(record.value('name'))
            samePerson      = forceBool(record.value('samePerson'))
            recordClass     = forceInt(record.value('recordClass'))
            visited         = forceBool(record.value('visited'))
            cnt             = forceInt(record.value('cnt'))
            recordNote      = forceString(record.value('note'))
            column = mapATtoCol.get(appointmentType, -1)
            if column>=0:
                if recordClass == 1: # Инфомат
                    key = (1, u'Инфомат')
                elif recordClass == 2 or u'цто' in recordNote: # call-центр
                    if detailCallCenter:
                        key = (2, u'Call-центр ' + name)
                    else:
                        key = (2, u'Call-центр')
                elif recordClass in (3, 5, 6, 7):  # интернет
                    key = (2, u'Интернет')
                else: #
                    if personId:
                        key = (0, name)
                    else:
                        key = (0, 'demo')
                rowData = reportDict.get(key, None)
                if not rowData:
                    rowData = [0]*7
                    reportDict[key] = rowData

                rowData[column] += cnt # всего
                if visited:
                    rowData[column+1] += cnt # выполнено
                if samePerson:
                    rowData[column+2] += cnt # актив

        keys = reportDict.keys()
        keys.sort()
        for key in keys:
            rowData = reportDict[key]
            rowData[0] = key
            reportData.append(rowData)
        return reportData


    def makeTable(self, cursor, doc, reportData):
        tableColumns = [
                        ( '4%', [u'№',             ''],          CReportBase.AlignLeft),
                        ('17%', [u'Пользователь',  ''],          CReportBase.AlignLeft),
                        ('13%', [u'Амбулаторно',  u'Всего'],     CReportBase.AlignLeft),
                        ('13%', [ '',             u'Выполнено'], CReportBase.AlignLeft),
                        ('13%', [ '',             u'Актив'],     CReportBase.AlignLeft),
                        ('13%', [u'На дому',      u'Всего'],     CReportBase.AlignLeft),
                        ('13%', [ '',             u'Выполнено'], CReportBase.AlignLeft),
                        ('13%', [ '',             u'Актив'],     CReportBase.AlignLeft)
                      ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 1, 3)

        total = [0]*6
        n = 1
        for rowData in reportData:
            i = table.addRow()
            table.setText(i, 0, n)
            table.setText(i, 1, rowData[0][1])
            for column in range(6):
                table.setText(i, column+2, rowData[column+1])
                total[column]+=rowData[column+1]
            n += 1

        i = table.addRow()
        table.setText(i, 1, u'Итого')
        for column in range(6):
            table.setText(i, column+2, total[column])


class CPreRecordUsersEx(CPreRecordUsers):
    def exec_(self):
        CPreRecordUsers.exec_(self)

    def getSetupDialog(self, parent):
        result = CPreRecordUsersSetupDialog(parent)
        result.setTitle(self.title())
        return result

    def build(self, params):
        chkOrgStructure = params.get('chkOrgStructure', None)
        return CPreRecordUsers.build(self, '\n'.join(self.getDescription(params)), params)


class CPreRecordUsersSetupDialog(CDialogBase, Ui_PreRecordUsersSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.chkRecordPeriod.setChecked(params.get('useRecordPeriod', True))
        self.edtBegRecordDate.setDate(params.get('begRecordDate', firstMonthDay(date)))
        self.edtEndRecordDate.setDate(params.get('endRecordDate', lastMonthDay(date)))
        self.chkSchedulePeriod.setChecked(params.get('useSchedulePeriod', False))
        self.edtBegScheduleDate.setDate(params.get('begScheduleDate', firstMonthDay(date)))
        self.edtEndScheduleDate.setDate(params.get('endScheduleDate', lastMonthDay(date)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.chkDetailCallCenter.setChecked(params.get('detailCallCenter', False))
        self.chkSpecialityFilter.setChecked(params.get('specialityFilter', False))
        self.chkShowDeleted.setChecked(params.get('showDeleted', False))


    def params(self):
        return dict(useRecordPeriod   = self.chkRecordPeriod.isChecked(),
                    begRecordDate     = self.edtBegRecordDate.date(),
                    endRecordDate     = self.edtEndRecordDate.date(),
                    useSchedulePeriod = self.chkSchedulePeriod.isChecked(),
                    begScheduleDate   = self.edtBegScheduleDate.date(),
                    endScheduleDate   = self.edtEndScheduleDate.date(),
                    orgStructureId    = self.cmbOrgStructure.value(),
                    specialityId      = self.cmbSpeciality.value(),
                    personId          = self.cmbPerson.value(),
                    detailCallCenter  = self.chkDetailCallCenter.isChecked(),
                    specialityFilter  = self.chkSpecialityFilter.isChecked(), 
                    showDeleted  = self.chkShowDeleted.isChecked()
                   )
