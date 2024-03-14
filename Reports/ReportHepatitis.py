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

from library.Utils             import forceString, forceInt

from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable

from Reports.ReportProtozoa    import CReportProtozoaSetupDialog


def selectData(params, forYear=False):
    month           = params.get('month', QDate())
    db = QtGui.qApp.db
    tableAction        = db.table('Action')
    tableActionType    = db.table('ActionType')
    tableActionPropertyType        = db.table('ActionPropertyType')
    tableRbTest = db.table('rbTest')
    tableActionProperty = db.table('ActionProperty')
    tableActionPropertyString = db.table('ActionProperty_String')
    tableEvent = db.table('Event')
    tableClient = db.table('Client')

    cond = [ tableAction['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             db.joinOr([tableRbTest['note'].eq(u'HBs Ag'), tableRbTest['note'].eq(u'Anti-HCV')]),
             tableActionPropertyString['value'].isNotNull()
           ]
    if forYear:
        cond.append(u'DATE(Action.`endDate`) BETWEEN DATE("%s-01-01") AND DATE("%s-%s-31")'%(month.year(), month.year(), month.month()))
    else:
        cond.append(u'Action.`endDate` LIKE "%s%s"'%(month.toString('yyyy-MM'), u'%'))

    cols = [ tableRbTest['note'],
             tableActionPropertyString['value'],
             u'age(Client.birthDate, "%s-%s-%s") as age'%(month.year(), month.month(), u'01')
           ]

    queryTable = tableAction
    queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.leftJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.leftJoin(tableRbTest, tableRbTest['id'].eq(tableActionPropertyType['test_id']))
    queryTable = queryTable.leftJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
    queryTable = queryTable.leftJoin(tableActionPropertyString, tableActionPropertyString['id'].eq(tableActionProperty['id']))
    queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
    queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))

    stmt = db.selectStmt(queryTable, cols, cond)
    query = db.query(stmt)
    return query


class CReportHepatitis(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Исследования на гепатиты B и C для центра СПИД')


    def dumpParams(self, cursor, params):
        months = [
            u'Январь',
            u'Февраль',
            u'Март',
            u'Апрель',
            u'Май',
            u'Июнь',
            u'Июль',
            u'Август',
            u'Сентябрь',
            u'Октябрь',
            u'Ноябрь',
            u'Декабрь',
        ]
        month = params.get('month', None)
        record = QtGui.qApp.db.getRecordEx('Organisation', 'fullName, address', 'id=%s AND deleted = 0'%(str(QtGui.qApp.currentOrgId())))
        orgName = forceString(record.value('fullName'))
        description = []
        description.append(u'Главному врачу')
        description.append(u'СПб ГУЗ «Центр по профилактике и борьбе со СПИД и')
        description.append(u'инфекционными заболеваниями»')
        description.append(u'Наб. Обводного канала 179,')
        description.append(u'Тел./факс   251-08-53')
        columns = [ ('70%', [], CReportBase.AlignRight) ,  ('30%', [], CReportBase.AlignRight) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, u'')
            table.setText(i, 1, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'ОТЧЁТ')
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.insertText(u'Клинико-диагностической лаборатории %s'%orgName)
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.insertText(u'о количестве лабораторно обследованных лиц на антиген вирусного гепатита В (HBs Ag) и ')
        cursor.insertText(u'антитела к вирусу гепатита с (на анти – HCV) среди населения Санкт-Петербурга ')
        cursor.insertText(u'за %s месяц %s года с нарастающим итогом через дробь.'%(months[month.month()-1], month.year()))
        cursor.insertBlock(CReportBase.AlignLeft)


    def getSetupDialog(self, parent):
        result = CReportProtozoaSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getReportData(self, query, queryYear):
        reportData = {'hbs':0,
                                'yearHbs':0,
                                'hbsValue':0,
                                'yearHbsValue':0,
                                'childHbs':0,
                                'childYearHbs':0,
                                'childHbsValue':0,
                                'childYearHbsValue':0,
                                'hcv':0,
                                'yearHcv':0,
                                'hcvValue':0,
                                'yearHcvValue':0,
                                'childHcv':0,
                                'childYearHcv':0,
                                'childHcvValue':0,
                                'childYearHcvValue':0,
        }
        while query.next():
            record = query.record()
            note   = forceString(record.value('note'))
            value = forceString(record.value('value'))
            age = forceInt(record.value('age'))
            if note == u'HBs Ag':
                reportData['hbs'] += 1
                if value ==  u'положительно':
                    reportData['hbsValue'] += 1
                if age<18:
                    reportData['childHbs'] += 1
                    if value ==  u'положительно':
                        reportData['childHbsValue'] += 1
            elif note == u'Anti-HCV':
                reportData['hcv'] += 1
                if value ==  u'положительно':
                    reportData['hcvValue'] += 1
                if age<18:
                    reportData['childHcv'] += 1
                    if value ==  u'положительно':
                        reportData['childHcvValue'] += 1
        while queryYear.next():
            record = queryYear.record()
            note   = forceString(record.value('note'))
            value = forceString(record.value('value'))
            age = forceInt(record.value('age'))
            if note == u'HBs Ag':
                reportData['yearHbs'] += 1
                if value ==  u'положительно':
                    reportData['yearHbsValue'] += 1
                if age<18:
                    reportData['childYearHbs'] += 1
                    if value ==  u'положительно':
                        reportData['childYearHbsValue'] += 1
            elif note == u'Anti-HCV':
                reportData['yearHcv'] += 1
                if value ==  u'положительно':
                    reportData['yearHcvValue'] += 1
                if age<18:
                    reportData['childYearHcv'] += 1
                    if value ==  u'положительно':
                        reportData['childYearHcvValue'] += 1
        return reportData


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock(CReportBase.AlignCenter)
        query = selectData(params)
        queryYear = selectData(params, forYear=True)
        if query is None:
            return doc
        reportData = self.getReportData(query, queryYear)
        columns = [('5%', [u'№ п/п'], CReportBase.AlignLeft),
                            ('19%', [u'Вид лабора-\n торного об-\nследования'], CReportBase.AlignCenter),
                            ('19%', [u'Всего лабора-\nторно обследо-\nвано (чел.)'], CReportBase.AlignCenter),
                            ('19%', [u'Всего выявле-\nно чел. с + ре-\nзультатом'], CReportBase.AlignCenter),
                            ('19%', [u'Всего обследо-\nвано человек'], CReportBase.AlignCenter),
                            ('19%', [u'Выявлено с \n+ результатом'], CReportBase.AlignCenter)]
        table = createTable(cursor, columns, headerRowCount=3, border=1, cellPadding=2, cellSpacing=0)
        table.setText(1, 0, u'1')
        table.setText(1, 1, u'HBs Ag')
        table.setText(1, 2, u'%s / %s'%(reportData['hbs'], reportData['yearHbs']))
        table.setText(1, 3, u'%s / %s'%(reportData['hbsValue'], reportData['yearHbsValue']))
        table.setText(1, 4, u'%s / %s'%(reportData['childHbs'], reportData['childYearHbs']))
        table.setText(1, 5, u'%s / %s'%(reportData['childHbsValue'], reportData['childYearHbsValue']))
        table.setText(2, 0, u'2')
        table.setText(2, 1, u'анти-HCV\n(геп. С)')
        table.setText(2, 2, u'%s / %s'%(reportData['hcv'], reportData['yearHcv']))
        table.setText(2, 3, u'%s / %s'%(reportData['hcvValue'], reportData['yearHcvValue']))
        table.setText(2, 4, u'%s / %s'%(reportData['childHcv'], reportData['childYearHcv']))
        table.setText(2, 5, u'%s / %s'%(reportData['childHcvValue'], reportData['childYearHcvValue']))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'ПРИМЕЧАНИЕ:')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'Исследования на HBs Ag производятся реактивами фирмы:')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'     - ЗАО «Вектор-Бест» Вектогеп В-HBs антиген-стрип;')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'     - Hexagon immunochromatographic rapid test ф.HUMAN.')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'Исследования на на анти - HCV (геп. С) производятся реактивами фирмы:')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'      - ЗАО «Вектор-Бест» Бест анти-ВГС/авто.')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'      - Hexagon immunochromatographic rapid test ф.HUMAN.')
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertText(u'Подтверждающие исследования проводятся на месте, а также на базе Городского диагностического вирусологического центра.')
        currentPerson = forceString(QtGui.qApp.db.translate('vrbPerson', 'id', QtGui.qApp.userId, 'name'))
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertBlock(CReportBase.AlignLeft)
        columns = [('50%', [], CReportBase.AlignLeft), ('50%', [], CReportBase.AlignLeft)]
        tableBot = createTable(cursor, columns, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        tableBot.setText(0, 0, u'Исполнитель- заведующий лабораторией')
        tableBot.setText(0, 1, u' __________________ %s '%(currentPerson if currentPerson!='' else ' __________________ '))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


        return doc

