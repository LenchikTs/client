# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
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

from Orgs.Utils import getOrgStructurePersonIdList
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from library.Utils import forceInt, forceString


class CSOClab(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о загруженных результатах из АИС СОЦ-Лаборатория')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.resize(400, 10)
        return result


    @staticmethod
    def selectData(params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND napr.setPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        db = QtGui.qApp.db
        stmt = u'''SELECT COUNT(at.id) AS sl, at.name AS name
                FROM Event e
                LEFT JOIN Action a ON e.id = a.event_id
                LEFT JOIN Client c ON c.id = e.client_id
                LEFT JOIN ActionType at ON a.actionType_id = at.id
                LEFT JOIN Action napr ON napr.id = a.prescription_id and napr.deleted = 0
                WHERE at.flatCode LIKE 'soc%%'
                    AND at.flatCode != 'soc001'
                    AND e.deleted = 0
                    AND c.deleted = 0
                    AND a.deleted = 0
                    AND at.deleted = 0
                    AND a.status = 2
                    AND a.endDate IS NOT NULL
                    AND a.endDate BETWEEN {begDate} AND {endDate}
                    {condOrgStructure}
                GROUP BY at.id, at.name
                ORDER BY at.name
        '''.format(begDate=db.formatDate(begDate),
                   endDate=db.formatDate(QDateTime(endDate.addDays(1)).addSecs(-1)),
                   condOrgStructure=condOrgStructure)
        db = QtGui.qApp.db
        return db.query(stmt) 


    def build(self, params):
        reportRowSize = 2
        reportData = {}

        def processQuery(query):
            while query.next():
                record = query.record()
                act = forceInt(record.value('sl'))
                name = forceString(record.value('name'))
                key = (name,)
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += act

        query = self.selectData(params)
        processQuery(query)
        
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        tableColumns = [
            ('70%', [u'Наименование исследования'], CReportBase.AlignLeft),
            ('30%', [u'Кол-во загруженных исследований'], CReportBase.AlignRight)
            ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 5, 1, 3)
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 1, 1)
        totalByReport = [0]*reportRowSize
        colsShift = 1
        keys = reportData.keys()
        keys.sort()

        def drawTotal(table,  total,  text): 
            row = table.addRow()
            table.setText(row, 0, text, CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 1)
            for col in xrange(reportRowSize-1):
                table.setText(row, col + colsShift, total[col], fontBold=True)

        for key in keys:
            name = key[0]
            reportLine = reportData[key]
            row = table.addRow()
            table.setText(row, 0, name)
            for col in xrange(reportRowSize-1):
                table.setText(row, col + colsShift, reportLine[col])
                totalByReport[col] = totalByReport[col] + reportLine[col]
        drawTotal(table,  totalByReport, u'Итого')
        return doc
