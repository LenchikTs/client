# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
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

from Orgs.Utils import getOrgStructurePersonIdList
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from library.Utils import forceString


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    db = QtGui.qApp.db
    condOrgStructure = u''
    if orgStructureId:
        personIdList = getOrgStructurePersonIdList(orgStructureId)
        if personIdList:
            condOrgStructure = u" AND e.execPerson_id IN (%s)" % (u','.join(str(personId) for personId in personIdList))
    stmt = u'''SELECT c.id,
CONCAT(c.lastName,' ',c.firstName,' ',c.patrName) as nam,
e.execDate AS dat,
d.MKB AS mkb,
SUM(case when DATE(e.setDate)=date(e.execDate) then 1 else 0 end) AS rav,
SUM(case when DATE(e.setDate)< date(e.execDate) then 1 else 0 end) AS kol,
SUM(case when d.MKB='z01.2' then 1 else 0 end) AS kolZ
FROM Event e
LEFT JOIN Client c ON e.client_id = c.id
left join Diagnosis d on d.id = getEventDiagnosis(e.id)
WHERE e.deleted=0 AND c.deleted=0 and e.execDate >= %(begDate)s and e.execDate < %(endDate)s
%(condOrgStructure)s
GROUP BY c.id
ORDER BY lastName
    ''' % dict(begDate=db.formatDate(begDate),
               endDate=db.formatDate(endDate.addDays(1)),
               condOrgStructure=condOrgStructure
               )
    db = QtGui.qApp.db
    return db.query(stmt)


def selectData1(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    db = QtGui.qApp.db
    condOrgStructure = u''
    if orgStructureId:
        personIdList = getOrgStructurePersonIdList(orgStructureId)
        if personIdList:
            condOrgStructure = u" AND e.execPerson_id IN (%s)" % (u','.join(str(personId) for personId in personIdList))
    stmt = u'''SELECT 
COUNT(DISTINCT e.client_id) as nam1,
SUM(DATE(e.setDate)=date(e.execDate)) AS rav1,
SUM(DATE(e.setDate)< date(e.execDate)) AS kol1,
SUM(d.MKB='z01.2') AS kolZ1
FROM Event e
LEFT JOIN Client c ON e.client_id = c.id
left join Diagnosis d on d.id = getEventDiagnosis(e.id)
WHERE e.deleted=0 AND c.deleted=0 and e.execDate >= %(begDate)s and e.execDate < %(endDate)s
%(condOrgStructure)s
    ''' % dict(begDate=db.formatDate(begDate),
               endDate=db.formatDate(endDate.addDays(1)),
               condOrgStructure=condOrgStructure
               )
    db = QtGui.qApp.db
    return db.query(stmt)


class CRepPos(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведение о количестве посещений')
        
    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemPosition = result.gridLayout.getItemPosition(i)
                if itemPosition != (29, 0, 1, 1) and itemPosition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        
        # рисуем третью табличку
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertBlock()
        tableColumns = [
            ('25%', [u'Кол-во людей'], CReportBase.AlignLeft),
            ('25%', [u'Количество посещений (одно посещение)'], CReportBase.AlignRight),
            ('25%', [u'Количество обращений по заболеванию (2 и более посещений)'], CReportBase.AlignRight),
            ('25%', [u'Количество проф.осмотров'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        query = selectData1(params)
        while query.next():
            record = query.record()
            row = table.addRow()
            nam1 = forceString(record.value('nam1'))
            rav1 = forceString(record.value('rav1'))
            kol1 = forceString(record.value('kol1'))
            kolZ1 = forceString(record.value('kolZ1'))
            table.setText(row, 0, nam1)
            table.setText(row, 1, rav1)
            table.setText(row, 2, kol1)
            table.setText(row, 3, kolZ1)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()

        # рисуем первую табличку
        tableColumns = [
            ('10%', [u'№'], CReportBase.AlignLeft),
            ('15%', [u'ФИО'], CReportBase.AlignRight),
            ('15%', [u'Дата'], CReportBase.AlignRight),
            ('15%', [u'Диагноз'], CReportBase.AlignRight),
            ('15%', [u'Количество посещений (одно посещение)'], CReportBase.AlignRight),
            ('15%', [u'Количество обращений по заболеванию (2 и более посещений)'], CReportBase.AlignRight),
            ('15%', [u'Количество проф.осмотров'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        query = selectData(params)
        num = 0
        while query.next():
            record = query.record()
            num += 1  
            nam = forceString(record.value('nam'))
            dat = forceString(record.value('dat'))
            mkb = forceString(record.value('mkb'))
            rav = forceString(record.value('rav'))
            kol = forceString(record.value('kol'))
            kolZ = forceString(record.value('kolZ'))
            row = table.addRow()
            table.setText(row, 0, num)
            table.setText(row, 1, nam)
            table.setText(row, 2, dat)
            table.setText(row, 3, mkb)
            table.setText(row, 4, rav)
            table.setText(row, 5, kol)
            table.setText(row, 6, kolZ)

        return doc
