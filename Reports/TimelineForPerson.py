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
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils      import firstMonthDay, forceDate, forceInt, forceRef, forceString, forceTime, lastMonthDay
from Orgs.Utils         import getOrgStructureDescendants
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Reports.Ui_TimelineSetupDialog import Ui_TimelineSetupDialog


def selectData(params):
    begDate              = params.get('begDate', None)
    endDate              = params.get('endDate', None)
    personId             = params.get('personId', None)
    personIdList         = params.get('personIdList', None)
    orgStructureId       = params.get('orgStructureId', None)
    specialityId         = params.get('specialityId', None)
    activityId           = params.get('activityId', None)
    isScheduleItemDetail = params.get('isScheduleItemDetail', False)
    isOrgStructureDetail = params.get('isOrgStructureDetail', False)

    db = QtGui.qApp.db
    tableSchedule = db.table('Schedule')
    tablePerson = db.table('Person')

    cond = [ 'Schedule.deleted = 0',
             'Schedule.appointmentType = 1',
           ]
    if begDate:
        cond.append(tableSchedule['date'].ge(begDate))
    if endDate:
        cond.append(tableSchedule['date'].le(endDate))
    if personId:
        cond.append(tableSchedule['person_id'].eq(personId))
    if personIdList:
        cond.append(tableSchedule['person_id'].inlist(personIdList))
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        if not personId and not personIdList:
            cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if activityId:
        tablePersonActivity = db.table('Person_Activity')
        cond.append(db.existsStmt(tablePersonActivity,
                                  [tablePersonActivity['master_id'].eq(tablePerson['id']),
                                   tablePersonActivity['activity_id'].eq(activityId),
                                   tablePersonActivity['deleted'].eq(0),
                                  ]))
    colsOrgStructureDetail = u''
    joinOrgStructureDetail = u''
    if isOrgStructureDetail:
        colsOrgStructureDetail = u', Person.orgStructure_id, OrgStructure.name AS nameOS'
        joinOrgStructureDetail = u'LEFT JOIN OrgStructure ON (OrgStructure.id = Person.orgStructure_id AND OrgStructure.deleted = 0)'
    colsScheduleItemDetail = u''
    if isScheduleItemDetail:
        colsScheduleItemDetail = u''', (SELECT COUNT(DISTINCT Schedule_Item.id)
FROM Schedule_Item
WHERE Schedule_Item.master_id = Schedule.id AND Schedule_Item.deleted = 0) AS scheduleItemAll,
(SELECT COUNT(DISTINCT Schedule_Item.id)
FROM Schedule_Item
WHERE Schedule_Item.master_id = Schedule.id AND Schedule_Item.deleted = 0 AND Schedule_Item.client_id IS NULL) AS scheduleItemFree'''
    stmt="""
SELECT Schedule.date, Schedule.begTime, Schedule.endTime, Schedule.office, Schedule.person_id, rbAppointmentPurpose.code AS purpose,
rbAppointmentPurpose.name AS purposeName
%s
%s
FROM Schedule
LEFT JOIN Person  ON Person.id = Schedule.person_id
LEFT JOIN rbAppointmentPurpose ON rbAppointmentPurpose.id = Schedule.appointmentPurpose_id
%s
WHERE %s"""
    return db.query(stmt % (colsOrgStructureDetail, colsScheduleItemDetail, joinOrgStructureDetail, db.joinAnd(cond)))


class CTimelineForPerson(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Расписание амбулаторного приёма врача')


    def build(self, description, params):
        db = QtGui.qApp.db
        reportData = {}
        personNames = []
        isScheduleItemDetail = params.get('isScheduleItemDetail', False)
        isOrgStructureDetail = params.get('isOrgStructureDetail', False)
        personScheduleItemTotal = {}
        query = selectData(params)
        while query.next():
            record = query.record()
            date     = forceDate(record.value('date'))
            personId = forceRef(record.value('person_id'))
            begTime  = forceTime(record.value('begTime'))
            endTime  = forceTime(record.value('endTime'))
            office   = forceString(record.value('office'))
            purpose  = forceString(record.value('purpose'))
            if isOrgStructureDetail:
                orgStructureId = forceRef(record.value('orgStructure_id'))
                nameOS  = forceString(record.value('nameOS'))
                orgStructureData = reportData.setdefault((orgStructureId, nameOS), {})
                personData = orgStructureData.setdefault(personId, {})
                scheduleItemTotalKey = ((orgStructureId, nameOS), personId)
            else:
                personData = reportData.setdefault(personId, {})
                scheduleItemTotalKey = personId
            if not personData:
                personNames.append((forceString(db.translate('vrbPersonWithSpeciality', 'id', personId, 'name')), personId))
            ranges = personData.setdefault(date.toPyDate(), [])
            if isScheduleItemDetail:
                scheduleItemAll = forceInt(record.value('scheduleItemAll'))
                scheduleItemFree = forceInt(record.value('scheduleItemFree'))
                personScheduleItemLine = personScheduleItemTotal.get(scheduleItemTotalKey, [0, 0])
                personScheduleItemLine[0] += scheduleItemAll
                personScheduleItemLine[1] += scheduleItemFree
                personScheduleItemTotal[scheduleItemTotalKey] = personScheduleItemLine
                ranges.append((begTime, endTime, office, purpose, scheduleItemAll, scheduleItemFree))
            else:
                ranges.append((begTime, endTime, office, purpose))
        personNames.sort()

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()

        if isOrgStructureDetail:
            cursor.setCharFormat(CReportBase.ReportTitle)
            if isScheduleItemDetail:
                scheduleItemTotal = 0
                scheduleItemFree  = 0
                scheduleItemOSTotal = {}
                for ((orgStructureId, nameOS), personId), personScheduleItem in personScheduleItemTotal.items():
                    scheduleItemTotal += personScheduleItem[0]
                    scheduleItemFree  += personScheduleItem[1]
                    scheduleItemOS = scheduleItemOSTotal.setdefault(orgStructureId, [0, 0])
                    scheduleItemOS[0] += personScheduleItem[0]
                    scheduleItemOS[1] += personScheduleItem[1]
                cursor.insertBlock()
                cursor.insertText(u'Номерки: всего по ЛПУ - %s, из них свободных - %s'%(scheduleItemTotal, scheduleItemFree))
                cursor.insertBlock()
            for (orgStructureId, nameOS), orgStructureData in reportData.items():
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.setCharFormat(CReportBase.ReportTitle)
                cursor.insertBlock()
                cursor.insertBlock()
                cursor.insertText(nameOS)
                if isScheduleItemDetail:
                    scheduleItemLine = scheduleItemOSTotal.get(orgStructureId, [0, 0])
                    cursor.insertBlock()
                    cursor.insertText(u'Номерки: всего - %s, из них свободных - %s'%(scheduleItemLine[0], scheduleItemLine[1]))
                cursor.insertBlock()
                cursor.insertBlock()
                cursor.setCharFormat(CReportBase.ReportBody)
                for personName, personId in personNames:
                    self.outPersonTable(cursor, personName, orgStructureData.get(personId, {}), isScheduleItemDetail, personScheduleItemTotal.get(((orgStructureId, nameOS), personId), [0, 0]))
        else:
            for personName, personId in personNames:
                self.outPersonTable(cursor, personName, reportData.get(personId, {}), isScheduleItemDetail, personScheduleItemTotal.get(personId, [0, 0]))
        return doc


    def outPersonTable(self, cursor, personName, personData, isScheduleItemDetail, personScheduleItemLine):
        if not personData:
            return
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(personName)
        if isScheduleItemDetail:
            cursor.insertBlock()
            cursor.insertText(u'Номерки: всего - %s, из них свободных - %s'%(personScheduleItemLine[0], personScheduleItemLine[1]))
        cursor.insertBlock()
        tableColumns = []
        if isScheduleItemDetail:
            for weekDay in xrange(7):
                name = forceString(QDate.longDayName(weekDay+1)).capitalize()
                tableColumns.append(('3.43%', [name, u'Дата',    u''               ], CReportBase.AlignLeft))
                tableColumns.append(('4%',    [u'',  u'Приём',   u''               ], CReportBase.AlignLeft))
                tableColumns.append(('2.28%', [u'',  u'Каб',     u''               ], CReportBase.AlignLeft))
                tableColumns.append(('2.28%', [u'',  u'Номерки', u'Всего'          ], CReportBase.AlignLeft))
                tableColumns.append(('2.28%', [u'',  u'',        u'из них свободны'], CReportBase.AlignLeft))
            table = createTable(cursor, tableColumns)
            for weekDay in xrange(7):
                table.mergeCells(0, weekDay*5, 1, 5)
                table.mergeCells(1, weekDay*5, 2, 1)
                table.mergeCells(1, weekDay*5+1, 2, 1)
                table.mergeCells(1, weekDay*5+2, 2, 1)
                table.mergeCells(1, weekDay*5+3, 1, 2)
        else:
            for weekDay in xrange(7):
                name = forceString(QDate.longDayName(weekDay+1)).capitalize()
                tableColumns.append(('5.71%', [name, u'Дата' ], CReportBase.AlignLeft))
                tableColumns.append(('6.28%', ['',   u'Приём'], CReportBase.AlignLeft))
                tableColumns.append(('2.28%', ['',   u'Каб'  ], CReportBase.AlignLeft))
            table = createTable(cursor, tableColumns)
            for weekDay in xrange(7):
                table.mergeCells(0, weekDay*3, 1, 3)
        dateList = personData.keys()
        dateList.sort()
        prevIsoWeek = None
        week = [None]*7
        for date in dateList:
            isoYear, isoWeek, isoWeekDay = date.isocalendar()
            if prevIsoWeek != isoWeek:
                if prevIsoWeek:
                    self.outWeek(table, week, isScheduleItemDetail)
                    week = [None]*7
                prevIsoWeek = isoWeek
            ranges = personData[date]
            ranges.sort()
            week[isoWeekDay-1] = date, ranges
        self.outWeek(table, week, isScheduleItemDetail)


    def outWeek(self, table, week, isScheduleItemDetail):
        rowCount = 0
        for weekDay, day in enumerate(week):
            if day:
                rowCount = max(rowCount, len(day[1]) + (1 if isScheduleItemDetail else 0)) # ranges
        i = table.addRow()
        for dummy in xrange(rowCount-1):
            table.addRow()
        if isScheduleItemDetail:
            for weekDay, day in enumerate(week):
                table.mergeCells(i, weekDay*5, (len(day[1])) if (day and (len(day[1]) +1) < rowCount) else (rowCount-1), 1)
                if day:
                    scheduleItemAllTotal = 0
                    scheduleItemFreeTotal = 0
                    table.setText(i, weekDay*5, forceString(QDate(day[0])))
                    for j, r in enumerate(day[1]):
                        begTime, endTime, office, purpose, scheduleItemAll, scheduleItemFree = r
                        if purpose:
                            table.setText(i+j, weekDay*5+1, begTime.toString('HH:mm')+'-'+endTime.toString('HH:mm') +', '+purpose)
                        else:
                            table.setText(i+j, weekDay*5+1, begTime.toString('HH:mm')+'-'+endTime.toString('HH:mm'))
                        table.setText(i+j, weekDay*5+2, office)
                        table.setText(i+j, weekDay*5+3, scheduleItemAll)
                        table.setText(i+j, weekDay*5+4, scheduleItemFree)
                        scheduleItemAllTotal += scheduleItemAll
                        scheduleItemFreeTotal += scheduleItemFree
                    table.setText(i+j+1, weekDay*5, u'ИТОГО')
                    table.setText(i+j+1, weekDay*5+3, scheduleItemAllTotal)
                    table.setText(i+j+1, weekDay*5+4, scheduleItemFreeTotal)
                    table.mergeCells(i+j+1, weekDay*5, 1, 3)
                else:
                    table.mergeCells(i, weekDay*5+1, rowCount, 1)
                    table.mergeCells(i, weekDay*5+2, rowCount, 1)
        else:
            for weekDay, day in enumerate(week):
                table.mergeCells(i, weekDay*3, rowCount, 1)
                if day:
                    table.setText(i, weekDay*3, forceString(QDate(day[0])))
                    for j, r in enumerate(day[1]):
                        begTime, endTime, office, purpose = r
                        if purpose:
                            table.setText(i+j, weekDay*3+1, begTime.toString('HH:mm')+'-'+endTime.toString('HH:mm') +', '+purpose)
                        else:
                            table.setText(i+j, weekDay*3+1, begTime.toString('HH:mm')+'-'+endTime.toString('HH:mm'))
                        table.setText(i+j, weekDay*3+2, office)
                else:
                    table.mergeCells(i, weekDay*3+1, rowCount, 1)
                    table.mergeCells(i, weekDay*3+2, rowCount, 1)


class CTimelineForPersonEx(CTimelineForPerson):
    def exec_(self):
        CTimelineForPerson.exec_(self)


    def getSetupDialog(self, parent):
        result = CTimelineSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
#        params['accountIdList'] = self.accountIdList
        return CTimelineForPerson.build(self, '\n'.join(self.getDescription(params)), params)


class CTimelineSetupDialog(QtGui.QDialog, Ui_TimelineSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.edtBegDate.setDate(params.get('begDate', firstMonthDay(date)))
        self.edtEndDate.setDate(params.get('endDate', lastMonthDay(date)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.chkScheduleItemDetail.setChecked(params.get('isScheduleItemDetail', False))
        self.chkOrgStructureDetail.setChecked(params.get('isOrgStructureDetail', False))


    def params(self):
        return dict(begDate = self.edtBegDate.date(),
                    endDate = self.edtEndDate.date(),
                    orgStructureId = self.cmbOrgStructure.value(),
                    specialityId = self.cmbSpeciality.value(),
                    personId = self.cmbPerson.value(),
                    isScheduleItemDetail = self.chkScheduleItemDetail.isChecked(),
                    isOrgStructureDetail = self.chkOrgStructureDetail.isChecked()
                   )


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)
