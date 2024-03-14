#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
## Copyright (C) 2012 Rauhfusa hospital ( №19 ). All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QTime

from library.Utils                    import forceBool, forceDate, forceRef, forceString, forceTime, formatName
from Orgs.Utils                       import getPersonInfo
from Registry.Utils                   import getClientPhonesEx
from Reports.DailyJournalBeforeRecord import CDailyJournalBeforeRecord, CDailyJournalBeforeRecordSetup
from Reports.ReportBase               import CReportBase, createTable
from Reports.ReportView               import CPageFormat
from Timeline.Schedule                import CSchedule


class CPreRecordClientsCard(CDailyJournalBeforeRecord):
    title_columns = [ ('100%', [], CReportBase.AlignCenter)]

    def __init__(self, parent = None):
        CDailyJournalBeforeRecord.__init__(self, parent)
        self.setTitle(u'Карточка предварительной записи пациентов')
        self.orientation = CPageFormat.Landscape
        self.table_columns = [
            ('3%',  [u'№'], CReportBase.AlignRight),
            ('5%',  [u'Время'], CReportBase.AlignLeft),
            ('5%',  [u'Каб.'], CReportBase.AlignLeft),
            ('8%',  [u'Назначение'], CReportBase.AlignLeft),
            ('18%',  [u'Вид деятельности'], CReportBase.AlignLeft),
            ('18%', [u'Пациент'], CReportBase.AlignLeft),
            ('15%', [u'Телефон'], CReportBase.AlignLeft),
            ('28%', [u'Примечания'], CReportBase.AlignLeft)
            ]
        self.isFirstEntryPatient = 0
        self.firstEntryPatientDict = {}


    def getSetupDialog(self, parent):
        result = CDailyJournalBeforeRecordSetup(parent)
        result.setFirstEntryPatientVisible(True)
        return result


    def getSheduleItemData(self, scheduleList, accountingSystemId, isPrimary, showEmptyItems, order):
        db = QtGui.qApp.db

        scheduleIdList = []
        for schedule in scheduleList:
            scheduleIdList.append( schedule.value('id') )
        if accountingSystemId == -2: # адрес проживания
            clientIdentifier = 'getClientLocAddress(Schedule_Item.client_id)'
        elif accountingSystemId == -1: # адрес регистрации
            clientIdentifier = 'getClientRegAddress(Schedule_Item.client_id)'
        elif accountingSystemId is None: #
            clientIdentifier = 'Schedule_Item.client_id'
        else:
            clientIdentifier = 'getClientIdentifier(Schedule_Item.client_id,%d)' % accountingSystemId

        tableScheduleItem = db.table('Schedule_Item')
        cond = [tableScheduleItem['deleted'].eq(0),
                tableScheduleItem['master_id'].inlist(scheduleIdList),
               ]
        if not showEmptyItems or isPrimary:
            cond.append(tableScheduleItem['client_id'].isNotNull())
        if order == 0: # по идентификатору
            orderCols = 'clientIdentifier, Schedule_Item.time'
        elif order == 2: # по фио
            orderCols = 'Client.lastName, Client.firstName, Client.patrName, Schedule_Item.time'
        else: # order == 1: # по времени
            orderCols = 'Schedule_Item.time'

        if isPrimary:
            havingCond = 'isPrimary'
        else:
            havingCond = ''

        stmt = 'SELECT Schedule_Item.time,'                                     \
                      ' Schedule_Item.client_id,'                               \
                      ' Schedule_Item.note,'                                    \
               ' %(clientIdentifier)s AS clientIdentifier,'                     \
               ' Schedule_Item.complaint AS comment,'    \
               ' rbActivity.name AS activityName,'   \
               ' rbAppointmentPurpose.name AS AP,'   \
               ' Schedule.office AS office,'   \
               ' NOT EXISTS(SELECT NULL '                                       \
                        ' FROM Schedule_Item AS SI '                            \
                        ' JOIN Schedule AS S ON S.id = SI.master_id'            \
                        ' WHERE SI.deleted=0'                                   \
                          ' AND S.deleted=0'                                    \
                          ' AND SI.client_id = Schedule_Item.client_id'         \
                          ' AND S.date = Schedule.date'                         \
                          ' AND SI.time<Schedule_Item.time) AS isPrimary,'      \
               ' Client.lastName, Client.firstName, Client.patrName,'           \
               ' Client.birthDate'                                              \
               ' FROM Schedule_Item'                                            \
               ' LEFT JOIN Client   ON Client.id = Schedule_Item.client_id'     \
               ' LEFT JOIN Schedule ON Schedule.id = Schedule_Item.master_id'   \
               ' LEFT JOIN rbActivity ON Schedule.activity_id = rbActivity.id'   \
               ' LEFT JOIN rbAppointmentPurpose ON Schedule_Item.appointmentPurpose_id = rbAppointmentPurpose.id'   \
               ' WHERE %(cond)s'                                                \
               ' %(havingKV)s%(havingCond)s '                                   \
               ' ORDER BY %(order)s'                                            \
               % dict(clientIdentifier = clientIdentifier,
                      cond             = db.joinAnd(cond),
                      havingKV         = 'HAVING ' if havingCond else '',
                      havingCond       = havingCond,
                      order            = orderCols)
        return db.query(stmt)


    def printDailyJournalRow(self, cursor, record, date):
        time = forceTime(record.value('time'))
        clientId = forceRef(record.value('client_id'))
        if clientId:
            name = formatName(record.value('lastName'), record.value('firstName'), record.value('patrName'))
            birthDate = forceDate(record.value('birthDate'))
            nameAndBirthDate = '%s (%s)'%(name, birthDate.toString('dd.MM.yyyy'))
            note = forceString(record.value('comment'))
            phone = getClientPhonesEx(clientId)
            activity = forceString(record.value('activityName'))
            AP = forceString(record.value('AP'))
            office = forceString(record.value('office'))[0:3]
        else:
            nameAndBirthDate = note = phone = activity = AP = office = ''
        row = self.currentTable.addRow()
        charFormat = self.normalChars
        if self.isFirstEntryPatient:
            if self.firstEntryPatientDict.get((clientId, date.toPyDate()), QTime()) == time:
                charFormat = self.boldChars
        self.currentTable.setText(row, 0, self.rowInTable, charFormat)
        self.currentTable.setText(row, 1, time.toString('hh:mm') if time else u'--:--', charFormat)
        self.currentTable.setText(row, 2, office, charFormat)
        self.currentTable.setText(row, 3, AP, charFormat)
        self.currentTable.setText(row, 4, activity, charFormat)
        self.currentTable.setText(row, 5, nameAndBirthDate, charFormat)
        self.currentTable.setText(row, 6,  phone, charFormat)
        self.currentTable.setText(row, 7, note, charFormat)
        self.calcRowAndInsertPageBreakIfRequired(cursor)


    def build(self, params):
        date = params.get('begDateDailyJournal', QDate())
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        outputTablePerPage = forceBool(params.get('outputTablePerPage', 0))
        outputNotScheduled = forceBool(params.get('outputNotScheduled', 0))
        order       = params.get('order', None)
        isPrimary          = params.get('isPrimary', None)
        accountingSystemId = params.get('accountingSystemId', None)
        showEmptyItems     = forceBool(params.get('showEmptyItems', 0))
        self.pageRowCount  = params.get('rowCount', 0)
        self.isFirstEntryPatient = params.get('isFirstEntryPatient', 0)

        self.boldChars = QtGui.QTextCharFormat()
        self.boldChars.setFontWeight(QtGui.QFont.Bold)
        self.normalChars = QtGui.QTextCharFormat()
        self.normalChars.setFontWeight(QtGui.QFont.Normal)

        personIdList = self.getPersonIdList(date, orgStructureId, personId)
        self.firstEntryPatientDict = {}
        doc = QtGui.QTextDocument()
        if date and personIdList:
            self.rowOnPage = 0
            cursor = QtGui.QTextCursor(doc)
            table = createTable(cursor, self.title_columns, headerRowCount=1, border=0, cellPadding=2, cellSpacing=0)
            #row = table.addRow()
            table.setText(0, 0, u'Карточка предварительной записи пациентов', charFormat=CReportBase.ReportTitle)
            table.addRow()
            cursor.movePosition(QtGui.QTextCursor.End)
            if self.isFirstEntryPatient:
                scheduleListForPersonList = self.getScheduleListForPersonList(date, personIdList)
                if scheduleListForPersonList:
                    query = self.getSheduleItemData(scheduleListForPersonList, accountingSystemId, isPrimary, showEmptyItems, order)
                    while query.next():
                        record = query.record()
                        time = forceTime(record.value('time'))
                        clientId = forceRef(record.value('client_id'))
                        firstEntryPatientTime = self.firstEntryPatientDict.get((clientId, date.toPyDate()), QTime())
                        if not firstEntryPatientTime or firstEntryPatientTime > time:
                            self.firstEntryPatientDict[(clientId, date.toPyDate())] = time
            for i, personId in enumerate(personIdList):
                scheduleList = self.getScheduleList(date, personId)
                if scheduleList:
                    cursor = self.createTableForPerson(cursor, personId, date, scheduleList, order, accountingSystemId, isPrimary, showEmptyItems)
                    cursor.insertText(u'\n')
                    cursor.insertText(u'\n')
                elif outputNotScheduled:
                    cursor = self.createTableForPerson(cursor, personId, date, None, order, accountingSystemId, isPrimary, showEmptyItems)
                    cursor.insertText(u'\n')
                    cursor.insertText(u'\n')
                if outputTablePerPage and self.rowOnPage > 0 and i < len(personIdList) - 1:
                    self.insertPageBreak(cursor)
                    cursor.insertBlock()
                    cursor.insertBlock()
                    cursor.insertBlock()
                    cursor.insertBlock()
                    cursor.movePosition(QtGui.QTextCursor.End)
        return doc


    def getScheduleListForPersonList(self, date, personIdList):
        db = QtGui.qApp.db
        tableSchedule = db.table('Schedule')
        cond = [tableSchedule['deleted'].eq(0),
                tableSchedule['person_id'].inlist(personIdList),
                tableSchedule['date'].eq(date),
                tableSchedule['appointmentType'].eq(CSchedule.atAmbulance),
               ]
        recordList = db.getRecordList(tableSchedule, '*', cond, 'begTime')
        return recordList


    def createTableForPerson(self, cursor, personId, date, scheduleList, order, accountingSystemId, isPrimary, showEmptyItems):
        personInfo = getPersonInfo(personId)
        personName     = personInfo['fullName']
        specialityName = personInfo['specialityName']
        cursor.insertText(u'%s, %s\n' %(forceString(date),  date.longDayName(date.dayOfWeek() )))
        cursor.insertText(u'врач: %s, %s'%(personName, specialityName))
        if scheduleList:
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            query = self.getSheduleItemData(scheduleList, accountingSystemId, isPrimary, showEmptyItems, order)
            if query.next():
                self.currentTable = createTable(cursor, self.table_columns,  1, 1, 2, 0)
                self.rowInTable = 1
                record = query.record()
                time = forceTime(record.value('time'))
                clientId = forceRef(record.value('client_id'))
                self.printDailyJournalRow(cursor, record, date)
                while query.next():
                    record = query.record()
                    self.printDailyJournalRow(cursor, record, date)
            else:
                cursor.insertText(u'На этот день никто не записан\n')
        cursor.movePosition(QtGui.QTextCursor.End)
        return cursor

