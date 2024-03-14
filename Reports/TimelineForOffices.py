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
from PyQt4.QtCore import QDate

from library.Utils                  import forceDate, forceRef, forceString, forceTime

from Reports.Report                 import CReport
from Reports.ReportBase             import CReportBase, createTable
from Reports.TimelineForPerson      import CTimelineSetupDialog, selectData


class CTimelineForOffices(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Расписание кабинетов')


    def build(self, description, params):
        db = QtGui.qApp.db
        reportData = {}
        mapPersonIdToName = {}
        query = selectData(params)
        # список (date, personId, office, begTime, endTime, purpose)
        # перестраивается в иерархию reportData[date][office][(begTime, endTime, personId, purpose)...]
        while query.next():
            record = query.record()
            date     = forceDate(record.value('date'))
            personId = forceRef(record.value('person_id'))
            purpose  = forceString(record.value('purposeName'))
            begTime  = forceTime(record.value('begTime'))
            endTime  = forceTime(record.value('endTime'))
            office   = forceString(record.value('office'))
            dateData = reportData.setdefault(date.toPyDate(), {})
            ranges   = dateData.setdefault(office, [])
            ranges.append((begTime, endTime, personId, purpose))
            if personId not in mapPersonIdToName:
                mapPersonIdToName[personId] = forceString(db.translate('vrbPersonWithSpeciality', 'id', personId, 'name'))

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()

        self.outOrgStructureTable(cursor, reportData, mapPersonIdToName)
        return doc


    def outOrgStructureTable(self, cursor, orgStructureData, mapPersonIdToName):
        cursor.movePosition(QtGui.QTextCursor.End)

        tableColumns = [('5.5%', [u'Кабинет'],  CReportBase.AlignLeft)]
        for weekDay in xrange(7):
            name = forceString(QDate.longDayName(weekDay+1)).capitalize()
            tableColumns.append(('4.5%', [name, u'Приём'], CReportBase.AlignLeft))
            tableColumns.append(('4.5%', ['',   u'Назначение'], CReportBase.AlignLeft))
            tableColumns.append(('4.5%', ['',   u'Врач' ], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        for weekDay in xrange(7):
            table.mergeCells(0, weekDay*3+1, 1, 3)

        dateList = orgStructureData.keys()
        dateList.sort()
        prevIsoWeek = None
        week = [None]*7
        officesSet = set()
        for date in dateList:
            isoYear, isoWeek, isoWeekDay = date.isocalendar()
            if prevIsoWeek != isoWeek:
                if prevIsoWeek:
                    self.outWeek(table, week, officesSet, mapPersonIdToName)
                    week = [None]*7
                    officesSet = set()
                prevIsoWeek = isoWeek
            dateData = orgStructureData[date]
            officesSet.update(dateData.keys())
            week[isoWeekDay-1] = date, dateData
        self.outWeek(table, week, officesSet, mapPersonIdToName)


    def outWeek(self, table, week, officesSet, mapPersonIdToName):
        weekFirstRow = table.addRow()
        for weekDay, day in enumerate(week):
            table.mergeCells(weekFirstRow, weekDay*3+1, 1, 3)
            if day:
                table.setText(weekFirstRow, weekDay*3+1, forceString(QDate(day[0])), CReportBase.TableHeader, CReportBase.AlignCenter)
        officesList = list(officesSet)
        officesList.sort()
        weekRowCount = 0
        for office in officesList:
            weekRowCount += self.outOffice(table, week, office, mapPersonIdToName)


    def outOffice(self, table, week, office, mapPersonIdToName):
        rowCount = 0
        for weekDay, day in enumerate(week):
            if day and office in day[1]:
                rowCount = max(rowCount, len(day[1][office])) # ranges

        i = table.addRow()
        for dummy in xrange(rowCount-1):
            table.addRow()

        table.mergeCells(i, 0, rowCount, 1)
        table.setText(i, 0, office, CReportBase.TableHeader, CReportBase.AlignCenter)
        for weekDay, day in enumerate(week):
            if day and office in day[1]:
                ranges = [(begTime, endTime, mapPersonIdToName[personId], purpose)
                           for begTime, endTime, personId, purpose in day[1][office]]
                ranges.sort()
                for j, (begTime, endTime, personName, purpose) in enumerate(ranges):
                    table.setText(i+j, weekDay*3+1, begTime.toString('HH:mm')+'-'+endTime.toString('HH:mm'))
                    table.setText(i+j, weekDay*3+2, purpose)
                    table.setText(i+j, weekDay*3+3, personName)
        return rowCount


class CTimelineForOfficesEx(CTimelineForOffices):
    def exec_(self):
        CTimelineForOffices.exec_(self)


    def getSetupDialog(self, parent):
        result = CTimelineSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        return CTimelineForOffices.build(self, '\n'.join(self.getDescription(params)), params)
