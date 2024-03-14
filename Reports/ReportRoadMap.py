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

from library.Utils      import forceInt, forceString
from Reports.Utils      import dateRangeAsStr
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportBIRADSSetupDialog import CReportBIRADSSetupDialog


def selectEventData(params):
    begDate = params.get('begDate', QDate.currentDate())
    endDate = params.get('endDate', QDate.currentDate())

    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    tableEventExport = db.table('Event_Export')

    cols = ['COUNT(DISTINCT Event.id) AS countEvent',
                'COUNT(DISTINCT Event_Export.master_id) AS countExportEvent']

    cond = [tableEvent['setDate'].ge(begDate),
                tableEvent['setDate'].le(endDate)]

    queryTable = tableEvent
    queryTable = queryTable.leftJoin(tableEventExport, tableEventExport['master_id'].eq(tableEvent['id']))

    stmt = db.selectStmt(queryTable, cols, cond)

    return db.query(stmt)

def selectProbeData(params):
    begDate = params.get('begDate', QDate.currentDate())
    endDate = params.get('endDate', QDate.currentDate())

    db = QtGui.qApp.db
    tableProbe = db.table('Probe')

    cols = ['COUNT(Probe.id) AS countProbes',
                'SUM(CASE WHEN status = 3 THEN 1 ELSE 0 END) AS counStatusProbes']

    cond = [tableProbe['createDatetime'].ge(begDate),
                tableProbe['createDatetime'].le(endDate)]


    stmt = db.selectStmt(tableProbe, cols, cond)

    return db.query(stmt)


class CReportRoadMap(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Дорожная карта')


    def getSetupDialog(self, parent):
        result = CReportBIRADSSetupDialog(parent)
        result.setOrganisationVisible(False)
        result.setOrgStructureVisible(False)
        result.setPersonVisible(False)
        result.setActionTypeVisible(False)
        result.setEventTypeVisible(False)
        result.chkClientDetail.setVisible(False)
        result.setTitle(self.title())
        return result


    def dumpParams(self, cursor, params):
        description = []
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if begDate or endDate:
            description.append(dateRangeAsStr(u'за период', begDate, endDate))
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
                        ('5%', [u''],    CReportBase.AlignLeft),
                        ('50%', [ u''], CReportBase.AlignRight),
                        ('15%', [u'Всего создано'],   CReportBase.AlignRight),
                        ('15%', [u'Всего передано'], CReportBase.AlignRight),
                        ('15%', [u'%'], CReportBase.AlignRight)
                       ]
        table = createTable(cursor, tableColumns)

        query = selectEventData(params)
        if query.next():
            countEvent = forceInt(query.record().value('countEvent'))
            countExportEvent = forceInt(query.record().value('countExportEvent'))
            eventPercent = (countExportEvent*100)/countEvent if countEvent else 0

        query = selectProbeData(params)
        if query.next():
            countProbes = forceInt(query.record().value('countProbes'))
            countStatusProbes = forceInt(query.record().value('counStatusProbes'))
            probesPercent = (countStatusProbes*100)/countProbes if countProbes else 0
        row = table.addRow()

        table.setText(row, 0, u'1')
        table.setText(row, 1, u'Количество от общего количества случаев оказания медицинской помощи, информация о которых передана в подсистему ИЭМК регионального сегмента ЕГИСЗ')
        table.setText(row, 2, countEvent)
        table.setText(row, 3, countExportEvent)
        table.setText(row, 4, eventPercent)

        row = table.addRow()
        table.setText(row, 0, u'2')
        table.setText(row, 1, u'Количество результатов исследований методом лабораторной диагностики (от общего числа направлений на исследования),  предоставляемых врачу  в электронном виде из региональных информационных систем Санкт-Петербурга')
        table.setText(row, 2, countProbes)
        table.setText(row, 3, countStatusProbes)
        table.setText(row, 4, probesPercent)

        return doc
