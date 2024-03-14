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
from PyQt4.QtCore import QDate, Qt, QObject, SIGNAL

from library.Utils       import forceString
from library.DialogBase  import CDialogBase

from Reports.Report      import CReport
from Reports.ReportBase  import CReportBase, createTable


def selectData(params):
    month           = params.get('month', QDate())
    db = QtGui.qApp.db
    tableAction        = db.table('Action')
    tableActionType    = db.table('ActionType')
    tableActionPropertyType        = db.table('ActionPropertyType')
    tableRbTest = db.table('rbTest')
    tableActionProperty = db.table('ActionProperty')
    tableActionPropertyString = db.table('ActionProperty_String')

    cond = [ tableAction['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             db.joinOr([tableRbTest['note'].eq(u'Простейшие'), tableRbTest['note'].eq(u'Малярия'), tableRbTest['note'].eq(u'Яйца глистов')]),
             tableActionPropertyString['value'].isNotNull(),
             u'Action.`endDate` LIKE "%s%s"'%(month.toString('yyyy-MM'), u'%')
           ]
    cols = [ tableRbTest['note'],
             tableActionPropertyString['value']
           ]

    queryTable = tableAction
    queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.leftJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.leftJoin(tableRbTest, tableRbTest['id'].eq(tableActionPropertyType['test_id']))
    queryTable = queryTable.leftJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
    queryTable = queryTable.leftJoin(tableActionPropertyString, tableActionPropertyString['id'].eq(tableActionProperty['id']))

    stmt = db.selectStmt(queryTable, cols, cond)
    query = db.query(stmt)
    return query


class CReportProtozoa(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Ежемесячный отчёт (я/г, простейшие, малярия)')


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
        address = forceString(record.value('address'))
        currentPerson = forceString(QtGui.qApp.db.translate('vrbPerson', 'id', QtGui.qApp.userId, 'name'))
        description = []
        description.append(u'СПб Роспотребнадзор')
        description.append(u'Паразитологический отдел')
        description.append(u'от заведующего КДЛ')
        description.append(orgName)
        description.append(currentPerson)
        description.append(address)
        columns = [ ('70%', [], CReportBase.AlignRight) ,  ('30%', [], CReportBase.AlignRight) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, u'')
            table.setText(i, 1, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.insertText(u'Отчет за %s %s года'%(months[month.month()-1], month.year()))
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertBlock(CReportBase.AlignLeft)


    def getSetupDialog(self, parent):
        dialog = CReportProtozoaSetupDialog(parent)
        dialog.setTitle(self.title())
        return dialog


    def getReportData(self, query):
        reportData = {'protozoaCount':0,
                                'eggsCount':0,
                                'malariaCount':0,
                                'protozoaValue':u'находок нет',
                                'eggsValue':u'находок нет',
                                'malariaValue':u'находок нет'
        }
        while query.next():
            record = query.record()
            note   = forceString(record.value('note'))
            value = forceString(record.value('value'))
            if note == u'Простейшие':
                reportData['protozoaCount'] += 1
                if reportData['protozoaValue']  == u'находок нет' and value == u'обнаружены':
                    reportData['protozoaValue'] = 1
                elif value == u'обнаружены':
                    reportData['protozoaValue'] += 1
            elif note == u'Яйца глистов':
                reportData['eggsCount'] += 1
                if reportData['eggsValue']  == u'находок нет' and value == u'обнаружены':
                    reportData['eggsValue'] = 1
                elif value == u'обнаружены':
                    reportData['eggsValue'] += 1
            elif note == u'Малярия':
                reportData['malariaCount'] += 1
                if reportData['malariaValue']  == u'находок нет' and value == u'обнаружены':
                    reportData['malariaValue'] = 1
                elif value == u'обнаружены':
                    reportData['malariaValue'] += 1
        return reportData


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.insertText(self.title())
        cursor.insertBlock(CReportBase.AlignLeft)
        cursor.insertBlock(CReportBase.AlignLeft)
        self.dumpParams(cursor, params)
        cursor.insertBlock(CReportBase.AlignCenter)
        query = selectData(params)
        if query is None:
            return doc
        reportData = self.getReportData(query)
        columns = [('20%', [], CReportBase.AlignLeft),
                            ('20%', [], CReportBase.AlignCenter),
                            ('20%', [], CReportBase.AlignCenter),
                            ('20%', [], CReportBase.AlignCenter),
                            ('20%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=4, border=0, cellPadding=2, cellSpacing=0)
        table.setText(0, 0, u'')
        table.setText(0, 1, u'Простейшие')
        table.setText(0, 2, reportData['protozoaCount'])
        table.setText(0, 3, reportData['protozoaValue'])
        table.setText(0, 4, u'')
        table.setText(1, 0, u'')
        table.setText(1, 1, u'Яйца глистов')
        table.setText(1, 2, reportData['eggsCount'])
        table.setText(1, 3, reportData['eggsValue'])
        table.setText(1, 4, u'')
        table.setText(2, 0, u'')
        table.setText(2, 1, u'Малярия')
        table.setText(2, 2, reportData['malariaCount'])
        table.setText(2, 3, reportData['malariaValue'])
        table.setText(1, 4, u'')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

        currentPerson = forceString(QtGui.qApp.db.translate('vrbPerson', 'id', QtGui.qApp.userId, 'name'))

        columns = [('70%', [], CReportBase.AlignLeft), ('30%', [], CReportBase.AlignLeft)]
        tableBot = createTable(cursor, columns, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        tableBot.setText(0, 0, u'Зав. лабораторией')
        tableBot.setText(0, 1, u'')
        tableBot.setText(1, 0,  u'/%s/  __________________ '%(currentPerson if currentPerson!='' else ' __________________ '))
        tableBot.setText(1, 1, u'')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


        return doc



class CReportProtozoaSetupDialog(CDialogBase):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        layout = QtGui.QGridLayout()
        self.edtMonth = QtGui.QDateEdit()
        self.edtMonth.setCalendarPopup(True)
        self.edtMonth.setDisplayFormat('yyyy.MM')
        layout.addWidget(QtGui.QLabel(u'Месяц'), 0, 0, 1, 1)
        layout.addWidget(self.edtMonth, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox, 2, 1, 1, 1)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.setLayout(layout)

    def setTitle(self, title):
        self.setObjectName(title)
        self.setWindowTitle(title)

    def params(self):
        result = {}
        result['month'] = self.edtMonth.date()
        return result

    def setParams(self, params):
        self.edtMonth.setDate(params.get('month', QDate.currentDate()))

