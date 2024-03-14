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
from Reports.Report     import *
from Reports.ReportBase import *
from Reports.ReportView import CPageFormat

from library.Utils      import *

    
class CODLI(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'ОДЛИ')
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=10, topMargin=10, rightMargin=10,  bottomMargin=10)

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setDiagnosisType(True)
        result.chkDiagnosisType.setText(u'Группировать по отделениям')
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(False)
        for i in xrange(result.gridLayout.count()):
            spacer=result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition=result.gridLayout.getItemPosition(i)
                if itemposition!=(29, 0, 1, 1)and itemposition!=(8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result


    def selectData(self, params): 
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        chkDetail = params.get('diagnosisType', False)
        if chkDetail:
            order = 'GROUP BY os.name'
        else:
            order = 'GROUP BY date(Action.endDate), date(Action_Export.dateTime) ORDER BY date(Action.endDate), date(Action_Export.dateTime) desc'
        db = QtGui.qApp.db
        stmt = u'''SELECT os.name as os,at.name as at,date(Action.endDate) AS datvvod, date(Action_Export.dateTime) AS datvigr,
count(Action.`id`) AS vsego,
sum(CASE WHEN Action_Export.success = 1 THEN 1 ELSE 0 end) AS uspeh,
sum(CASE WHEN Action_Export.success = 0 THEN 1 ELSE 0 end) AS oshib
FROM Action
  LEFT JOIN rbExternalSystem es ON es.code = 'N3.ODLI'
  LEFT JOIN Action_Export
    ON (Action_Export.`master_id` = Action.`id`)
    AND (Action_Export.`system_id` = es.id)
  LEFT JOIN Person p ON Action.person_id = p.id
  LEFT JOIN OrgStructure os ON p.orgStructure_id = os.id
  LEFT JOIN ActionType at ON Action.actionType_id = at.id
WHERE Action.`deleted` = 0
AND Action.`status` = 2
AND Action.`actionType_id` IN (SELECT
    id
  FROM ActionType
  WHERE (ActionType.`deleted` = 0)
  AND (ActionType.`class` = 1)
  AND (ActionType.`flatCode` LIKE 's_lab%%')
  AND (ActionType.`serviceType` in (5, 10)))
AND DATE(Action.endDate) BETWEEN %(begDate)s AND %(endDate)s
and exists(select NULL from ActionProperty ap
    left join ActionPropertyType apt on apt.id = ap.type_id
    where ap.action_id = Action.id and ap.deleted = 0 and apt.test_id is not null)
 %(order)s;
        '''% {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate),
               'order': order
               }
        db = QtGui.qApp.db
        return db.query(stmt) 
        
    def selectData2(self, params): 
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        db = QtGui.qApp.db
        stmt = u'''SELECT c.id AS kodp,concat(c.lastName,' ',c.firstName,' ',c.patrName) AS nam, c.birthDate AS datb,e.id AS kodev,at.name AS usl,Action.endDate AS datact
FROM Action
  LEFT JOIN rbExternalSystem es ON es.code = 'N3.ODLI'
  LEFT JOIN Action_Export
    ON (Action_Export.`master_id` = Action.`id`)
    AND (Action_Export.`system_id` = es.id)
  LEFT JOIN Event e ON Action.event_id = e.id
  LEFT JOIN Client c ON e.client_id = c.id
  LEFT JOIN ActionType at ON Action.actionType_id = at.id
WHERE Action.`deleted` = 0
AND Action.`status` = 2
AND Action.`actionType_id` IN (SELECT
    id
  FROM ActionType
  WHERE (ActionType.`deleted` = 0)
  AND (ActionType.`class` = 1)
  AND (ActionType.`flatCode` LIKE 's_lab%%')
  AND (ActionType.`serviceType` in (5, 10)))
  AND Action_Export.success = 0
AND DATE(Action.endDate) BETWEEN %(begDate)s AND %(endDate)s
GROUP BY e.id,Action.id
ORDER BY Action.endDate ;
        '''% {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate)
               }
        db = QtGui.qApp.db
        return db.query(stmt)


    def selectData3(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        db = QtGui.qApp.db
        chkDetail = params.get('diagnosisType', False)
        if chkDetail:
            order = 'ORDER BY os.name, Action.endDate '
        else:
            order = 'ORDER BY Action.endDate '
        stmt = u'''SELECT c.id AS kodp,concat(c.lastName,' ',c.firstName,' ',c.patrName) AS nam, c.birthDate AS datb,e.id AS kodev,at.name AS usl,Action.endDate AS datact,os.name
FROM Action
  LEFT JOIN rbExternalSystem es ON es.code = 'N3.ODLI'
  LEFT JOIN Action_Export
    ON (Action_Export.`master_id` = Action.`id`)
    AND (Action_Export.`system_id` = es.id)
  LEFT JOIN Event e ON Action.event_id = e.id
  LEFT JOIN Client c ON e.client_id = c.id
  LEFT JOIN ActionType at ON Action.actionType_id = at.id
  LEFT JOIN Person p ON Action.person_id = p.id
  LEFT JOIN OrgStructure os ON p.orgStructure_id = os.id
WHERE Action.`deleted` = 0
AND Action.`status` = 2
AND Action.`actionType_id` IN (SELECT
    id
  FROM ActionType
  WHERE (ActionType.`deleted` = 0)
  AND (ActionType.`class` = 1)
  AND (ActionType.`flatCode` LIKE 's_lab%%')
  AND (ActionType.`serviceType` in (5, 10)))
  AND (Action_Export.id is null
  or not exists(select NULL from ActionProperty ap
    left join ActionPropertyType apt on apt.id = ap.type_id
    where ap.action_id = Action.id and ap.deleted = 0 and apt.test_id is not null))
AND DATE(Action.endDate) BETWEEN %(begDate)s AND %(endDate)s
GROUP BY e.id, Action.id, os.name
 %(order)s
;
        ''' % {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate),
               'order': order
               }
        db = QtGui.qApp.db
        return db.query(stmt)

    def build(self, params):
        chkDetail = params.get('diagnosisType', False)
        reportRowSize = 12
        reportData = {}
        secondTitle = u'Экспорт ОДЛИ завершился ошибкой'


        def processQuery(query):
            while query.next():
                record = query.record()
                os= forceString(record.value('os'))
                at= forceString(record.value('at'))
                datvvod= forceDate(record.value('datvvod'))
                datvigr= forceString(record.value('datvigr'))#name
                vsego = forceInt(record.value('vsego'))#+
                uspeh = forceInt(record.value('uspeh'))#+
                oshib = forceInt(record.value('oshib'))#+

                if chkDetail:
                  key = (os,at)
                else:
                  key = (datvvod, datvigr)
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += vsego
                reportLine[1] += uspeh
                reportLine[2] += oshib

        query = self.selectData(params)
        processQuery(query)
        
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        if chkDetail:
            cursor.insertBlock()
            tableColumns = [
                ('40%',  [ u'Подразделение'], CReportBase.AlignLeft),
                ('20%',  [ u'Всего введено результатов'], CReportBase.AlignLeft),
                ('20%',  [ u'Успешно выгружено'], CReportBase.AlignLeft),
                ('20%',  [ u'Выгружено с ошибками'], CReportBase.AlignLeft)
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
                for col in xrange(reportRowSize):
                    if (col<3):
                        table.setText(row, col + colsShift, total[col], fontBold=True)
            for key in keys:
                #key = (osname, fin,   infis,  name)key = (fioP, fio, happy, pol, snil, lgot, serial, number,nazn, mkb, name, vk)

                os= key[0]
                at= key[1]
                #mergeCells(int row, int column, int numRows, int numCols)

                reportLine = reportData[key]

                row = table.addRow()
                table.setText(row, 0, os)

                for col in xrange(reportRowSize):
                    if (col<3):
                        table.setText(row, col + colsShift, reportLine[col])
                    totalByReport[col] = totalByReport[col] + reportLine[col]

            #total
            drawTotal(table,  totalByReport, u'Итого');
        else:
            cursor.insertBlock()
            tableColumns = [
                ('30%', [u'Дата ввода'], CReportBase.AlignLeft),
                ('25%', [u'Дата выгрузки в ОДЛИ'], CReportBase.AlignLeft),
                ('15%', [u'Всего введено результатов'], CReportBase.AlignLeft),
                ('15%', [u'Успешно выгружено'], CReportBase.AlignLeft),
                ('15%', [u'Выгружено с ошибками'], CReportBase.AlignLeft)
            ]

            table = createTable(cursor, tableColumns)
            table.mergeCells(0, 5, 1, 3)
            for col in xrange(reportRowSize):
                table.mergeCells(0, col, 1, 1)

            totalByReport = [0] * reportRowSize
            colsShift = 2

            keys = reportData.keys()
            keys.sort()

            def drawTotal(table, total, text):

                row = table.addRow()

                table.setText(row, 0, text, CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 1)
                for col in xrange(reportRowSize):
                    if (col < 3):
                        table.setText(row, col + colsShift, total[col], fontBold=True)

            for key in keys:
                # key = (osname, fin,   infis,  name)key = (fioP, fio, happy, pol, snil, lgot, serial, number,nazn, mkb, name, vk)

                datvvod = key[0]
                datvigr = key[1]
                # mergeCells(int row, int column, int numRows, int numCols)

                reportLine = reportData[key]

                row = table.addRow()
                table.setText(row, 0, datvvod.toString("dd.MM.yyyy"))
                table.setText(row, 1, datvigr)

                for col in xrange(reportRowSize):
                    if (col < 3):
                        table.setText(row, col + colsShift, reportLine[col])
                    totalByReport[col] = totalByReport[col] + reportLine[col]

            # total
            drawTotal(table, totalByReport, u'Итого');

        query = self.selectData2(params)
        if query.size():
            # рисуем вторую табличку
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            cursor.insertBlock()
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setBlockFormat(CReportBase.AlignCenter)
            cursor.insertText(secondTitle)
            cursor.insertBlock()
            cursor.insertBlock()
            tableColumns = [
                ('8%',  [ u'Код пациента'], CReportBase.AlignLeft),
                ('38%',  [ u'ФИО пациента'], CReportBase.AlignLeft),
                ('8%',  [ u'Дата рождения'], CReportBase.AlignLeft),
                ('8%',  [ u'Код карточки'], CReportBase.AlignLeft),
                ('23%',  [ u'Наименование исследования'], CReportBase.AlignLeft),
                ('15%',  [ u'Дата исследования'], CReportBase.AlignLeft)
                ]

            table = createTable(cursor, tableColumns)

            while query.next():
                record = query.record()
                cl = forceInt(record.value('kodp'))
                las = forceString(record.value('nam'))
                fir = forceDate(record.value('datb'))
                pat = forceInt(record.value('kodev'))
                hap = forceString(record.value('usl'))
                tip = forceString(record.value('datact'))
                row = table.addRow()

                table.setText(row, 0, cl)
                table.setText(row, 1, las)
                table.setText(row, 2, fir.toString("dd.MM.yyyy"))
                table.setText(row, 3, pat)
                table.setText(row, 4, hap)
                table.setText(row, 5, tip)


        query = self.selectData3(params)
        if query.size():
            # рисуем третью табличку
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            cursor.insertBlock()
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setBlockFormat(CReportBase.AlignCenter)
            cursor.insertText(u'Исследования, не попадающие в выгрузку, или еще не выгруженные')
            cursor.insertBlock()
            cursor.insertBlock()
            tableColumns = [
                ('8%', [u'Код пациента'], CReportBase.AlignLeft),
                ('38%', [u'ФИО пациента'], CReportBase.AlignLeft),
                ('8%', [u'Дата рождения'], CReportBase.AlignLeft),
                ('8%', [u'Код карточки'], CReportBase.AlignLeft),
                ('23%', [u'Наименование исследования'], CReportBase.AlignLeft),
                ('15%', [u'Дата исследования'], CReportBase.AlignLeft)
            ]
            table = createTable(cursor, tableColumns)
            chkDetail = params.get('diagnosisType', False)
            os_Old = None

            if chkDetail:
                while query.next():
                    record = query.record()
                    cl = forceInt(record.value('kodp'))
                    las = forceString(record.value('nam'))
                    fir = forceDate(record.value('datb'))
                    pat = forceInt(record.value('kodev'))
                    hap = forceString(record.value('usl'))
                    tip = forceString(record.value('datact'))
                    os = forceString(record.value('name'))
                    if os_Old != os:
                        row = table.addRow()
                        if os == '':
                            table.setText(row, 1, u'не удалось определить подразделение, проверьте исполнителя', None, None, None, True)
                            table.mergeCells(row, 0, 1, 6)
                        else:
                            table.setText(row, 0, os, None, None, None, True)
                            table.mergeCells(row, 0, 1, 6)
                    os_Old = os

                    row = table.addRow()
                    table.setText(row, 0, cl)
                    table.setText(row, 1, las)
                    table.setText(row, 2, fir.toString("dd.MM.yyyy"))
                    table.setText(row, 3, pat)
                    table.setText(row, 4, hap)
                    table.setText(row, 5, tip)
            else:
                while query.next():
                    record = query.record()
                    cl = forceInt(record.value('kodp'))
                    las = forceString(record.value('nam'))
                    fir = forceDate(record.value('datb'))
                    pat = forceInt(record.value('kodev'))
                    hap = forceString(record.value('usl'))
                    tip = forceString(record.value('datact'))
                    row = table.addRow()

                    table.setText(row, 0, cl)
                    table.setText(row, 1, las)
                    table.setText(row, 2, fir.toString("dd.MM.yyyy"))
                    table.setText(row, 3, pat)
                    table.setText(row, 4, hap)
                    table.setText(row, 5, tip)

        return doc