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

import datetime

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDateTime, QTime

from library.Utils             import forceString, forceInt, forceDateTime, forceRef

from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportView        import CPageFormat
from Reports.Utils             import dateRangeAsStr

from Reports.ReportSanatoriumArrived import CReportSanatoriumSetupDialog


def selectActionData(params, flatCode=u''):
    begDate = QDateTime(params.get('begDate', QDate()), QTime(9, 0))
    endDate = QDateTime(params.get('endDate', QDate()), QTime(9, 0))

    db = QtGui.qApp.db
    tableAction        = db.table('Action')
    tableActionType    = db.table('ActionType')
    tableEvent        = db.table('Event')
    tableEventType = db.table('EventType')
    tableRbMedicalAidType = db.table('rbMedicalAidType')

    cond = [tableAction['deleted'].eq(0),
            tableEvent['deleted'].eq(0),
            tableActionType['deleted'].eq(0),
            tableActionType['flatCode'].like('%s'%flatCode),
            tableRbMedicalAidType['code'].eq(8)] #Санаторно-курортная

    if flatCode == u'moving%':
        cond.append(tableAction['begDate'].le(endDate))
        cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(begDate)]))
    elif flatCode == u'leaved':
        cond.append(tableAction['endDate'].ge(begDate))
        cond.append(tableAction['endDate'].lt(endDate.addDays(1)))
    else:
        cond.append(tableAction['begDate'].ge(begDate))
        cond.append(tableAction['begDate'].lt(endDate.addDays(1)))

    if flatCode == u'moving%':
        cols = [u"DISTINCT Action.id AS actionId",
                tableAction['begDate'],
                tableAction['endDate'],
                tableEvent['client_id'],
                tableEvent['relative_id']
                ]
    else:
        cols = [
                u"IF(TIME(Action.`begDate`) >= TIME('00:00:00') AND  TIME(Action.`begDate`) <= TIME('08:59:00'), DATE_FORMAT(DATE_ADD(Action.begDate, INTERVAL -1 DAY), '%d'), DATE_FORMAT(Action.begDate, '%d')) AS day",
                u"IF(TIME(Action.`begDate`) >= TIME('00:00:00') AND  TIME(Action.`begDate`) <= TIME('08:59:00'), DATE_FORMAT(DATE_ADD(Action.begDate, INTERVAL -1 DAY), '%m'), DATE_FORMAT(Action.begDate, '%m')) AS month",
                u"COUNT(Action.id) AS countActions",
                u"COUNT(DISTINCT Event.relative_id) AS countRelatives"
               ]

    queryTable = tableAction
    queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
    queryTable = queryTable.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    queryTable = queryTable.leftJoin(tableRbMedicalAidType, tableRbMedicalAidType['id'].eq(tableEventType['medicalAidType_id']))

    if flatCode == u'moving%':
        orderBy = 'Action.begDate, Action.endDate'
        stmt = db.selectStmt(queryTable, cols, cond, order = orderBy)
    else:
        groupBy = u'''MONTH(Action.begDate), DAY(IF(TIME(Action.`begDate`) >= TIME('00:00:00') AND TIME(Action.`begDate`) <= TIME('08:59:00'), DATE_ADD(Action.begDate, INTERVAL -1 DAY), Action.begDate))'''
        orderBy = u'''MONTH(Action.begDate), DAY(IF(TIME(Action.`begDate`) >= TIME('00:00:00') AND TIME(Action.`begDate`) <= TIME('08:59:00'), DATE_ADD(Action.begDate, INTERVAL -1 DAY), Action.begDate))'''
        stmt = db.selectStmtGroupBy(queryTable, cols, cond, groupBy, orderBy)

    query = db.query(stmt)
    return query


class CReportSanatoriumArrivalDiary(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Дневник пребывания больных')


    def getSetupDialog(self, parent):
        result = CReportSanatoriumSetupDialog(parent)
        result.setTitle(self.title())
        result.setShowAddressVisible(False)
        result.setPatronageVisible(True)
        result.setShowBirthDateVisible(False)
        return result


    def dumpParams(self, cursor, params):
        self.params = params
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        description = []
        if begDate and endDate:
            description.append(dateRangeAsStr(u'', begDate, endDate))
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.movePosition(QtGui.QTextCursor.End)
        columns = [ ('100%', [], CReportBase.AlignCenter)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)


    def build(self, params):
        patronage = params.get('patronage', False)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.insertBlock(CReportBase.AlignCenter)
        orgName = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'title'))
        cursor.insertText(orgName)
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(self.title())
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
                        ('20%', [u'Число, месяц'],  CReportBase.AlignLeft),
                        ('20%', [u'Состояло'],             CReportBase.AlignLeft),
                        ('20%' , [u'Прибыло'],         CReportBase.AlignLeft),
                        ('20%', [u'Убыло'],        CReportBase.AlignLeft),
                        ('20%', [u'Состоит'],        CReportBase.AlignLeft),
                        ]
        table = createTable(cursor, tableColumns)
        arrived = 0
        leaved = 0
        dataDict = {}
        query = selectActionData(params, flatCode=u'received%')
        if query:
            while query.next():
                record = query.record()
                day            = forceString(record.value('day'))
                month          = forceString(record.value('month'))
                countActions   = forceInt(record.value('countActions'))
                countRelatives = forceInt(record.value('countRelatives'))
                received = countActions + (countRelatives if patronage else 0)
                arrived += received
                if (month, day) not in dataDict.keys():
                    dataDict[(month, day)] = [0, 0, 0, 0]
                dataDict[(month, day)][1] += received
                dataDict[(month, day)][3] += received

        query = selectActionData(params, flatCode=u'leaved%')
        if query:
            while query.next():
                record = query.record()
                day            = forceString(record.value('day'))
                month          = forceString(record.value('month'))
                countActions   = forceInt(record.value('countActions'))
                countRelatives = forceInt(record.value('countRelatives'))
                leavedA = countActions + (countRelatives if patronage else 0)
                leaved += leavedA
                if (month, day) not in dataDict.keys():
                    dataDict[(month, day)] = [0, 0, 0, 0]
                dataDict[(month, day)][2] += leavedA
                dataDict[(month, day)][3] -= leavedA

        begDate = QDateTime(params.get('begDate', QDate()), QTime(9, 0))
        endDate = QDateTime(params.get('endDate', QDate()), QTime(9, 0))
        clientIdDict = {}
        relativeIdDict = {}
        query = selectActionData(params, flatCode=u'moving%')
        if query:
            while query.next():
                record = query.record()
                begDateAction  = forceDateTime(record.value('begDate'))
                endDateAction  = forceDateTime(record.value('endDate'))
                relativeId = forceRef(record.value('relative_id'))
                date = begDate
                while date <= endDate:
                    if begDateAction <= date and (not endDateAction.date() or endDateAction >= date):
                        clientId = forceRef(record.value('client_id'))
                        dateKey = datetime.date(date.date().year(), date.date().month(), date.date().day())
                        clientIdLine = clientIdDict.get(dateKey, [])
                        if clientId and clientId not in clientIdLine:
                            clientIdLine.append(clientId)
                            clientIdDict[dateKey] = clientIdLine
                            month = unicode(date.date().toString('MM'))
                            day = unicode(date.date().toString('dd'))
                            dataLine = dataDict.get((month, day), [0, 0, 0, 0])
                            moving = 1
                            relativeIdLine = relativeIdDict.get(dateKey, [])
                            if patronage and relativeId and relativeId not in relativeIdLine:
                                relativeIdLine.append(relativeId)
                                relativeIdDict[dateKey] = relativeIdLine
                                moving += 1
                            dataLine[0] += moving
                            dataLine[3] += moving
                            dataDict[(month, day)] = dataLine
                    date = date.addDays(1)

        for key, data in sorted(dataDict.iteritems()):
            i = table.addRow()
            table.setText(i, 0, u'%s.%s'%(key[1], key[0]))
            table.setText(i, 1, data[0])
            table.setText(i, 2, data[1])
            table.setText(i, 3, data[2])
            table.setText(i, 4, data[3])

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'Прибыло за период: %s чел.'%arrived)
        cursor.insertBlock()
        cursor.insertText(u'Убыло за период: %s чел.'%leaved)

        return doc
