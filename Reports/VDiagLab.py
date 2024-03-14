# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
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
from Reports.Report import *
from Reports.ReportBase import *
from Orgs.Utils import getOrgStructurePersonIdList
from library.Utils import *
from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportForm131_1000_SetupDialog import CReportForm131_1000_SetupDialog


class CVdiagLab(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Доступные виды диагностических исследований')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        condOrgStructure = u''
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            if orgStructureIdList:
                condOrgStructure = u''' AND os.id IN (%s)''' % (
                    u','.join(str(personId) for personId in orgStructureIdList if personId))
        db = QtGui.qApp.db
        stmt = u'''
select COUNT(*) as cn,jt.date as dat,os.name as os,jt1.name FROM vJobTicket jt
LEFT JOIN rbJobType jt1 ON jt.jobType_id = jt1.id
  LEFT JOIN OrgStructure os ON jt.orgStructure_id=os.id

  WHERE jt.isUsed=0
  AND jt.datetime  BETWEEN %(begDate)s AND %(endDate)s
  AND jt.deleted=0
  AND os.deleted=0
%(condOrgStructure)s
  GROUP BY jt.orgStructure_id ,jt1.name,jt.date
  ORDER BY os.name,jt.date,jt1.name;
        ''' % dict(begDate=db.formatDate(begDate),
                   endDate=db.formatDate(endDate),
                   condOrgStructure=condOrgStructure)
        db = QtGui.qApp.db
        return db.query(stmt)

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        tableColumns = [
            ('15%', [u'Доступные виды диагностических исследований'], CReportBase.AlignLeft),
            ('15%', [u''], CReportBase.AlignLeft),
            ('15%', [u''], CReportBase.AlignLeft),
            ('15%', [u''], CReportBase.AlignLeft),
            ('40%', [u''], CReportBase.AlignLeft),
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 5)

        query = self.selectData(params)
        d = None
        count = 0
        row = table.addRow()
        table.mergeCells(row, 0, 1, 5)
        while query.next():
            record = query.record()
            cn = forceInt(record.value('cn'))
            dat = forceDate(record.value('dat'))
            name = forceString(record.value('name'))


            if d == dat:
                row = table.addRow()
                table.setText(row, 0, name, None, CReportBase.AlignCenter)
                table.mergeCells(row, 0, 1, 4)
                table.setText(row, 4, cn, None, CReportBase.AlignRight)
                count += cn
            else:
                if d != None:
                    row = table.addRow()
                    table.setText(row, 0, u'Итого за ' + d.toString('dd.MM.yyyy'), CReportBase.TableHeader)
                    table.mergeCells(row, 0, 1, 4)
                    table.setText(row, 4, count, CReportBase.TableHeader, CReportBase.AlignCenter)
                    count = 0
                d = dat
                count += cn
                row = table.addRow()
                table.setText(row, 0, u'Кабинет', CReportBase.TableHeader)
                table.setText(row, 1, '')
                table.setText(row, 2, u'Дата', CReportBase.TableHeader)
                table.setText(row, 3, d.toString('dd.MM.yyyy'), CReportBase.TableHeader, CReportBase.AlignRight)
                table.setText(row, 4, u'Доступно номерков на момент выборки', CReportBase.TableHeader, CReportBase.AlignCenter)
                row = table.addRow()
                table.setText(row, 0, name, None, CReportBase.AlignCenter)
                table.mergeCells(row, 0, 1, 4)
                table.setText(row, 4, cn, None, CReportBase.AlignRight)

        if d:
            row = table.addRow()
            table.setText(row, 0, u'Итого за ' + d.toString('dd.MM.yyyy'), CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 4)
            table.setText(row, 4, count, CReportBase.TableHeader, CReportBase.AlignCenter)


        return doc

