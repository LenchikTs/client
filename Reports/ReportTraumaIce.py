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

from PyQt4                     import QtGui
from PyQt4.QtCore              import QDate

from library.Utils             import forceString, forceInt, formatSex
from library.DialogBase        import CDialogBase

from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportView        import CPageFormat
from Reports.Utils             import dateRangeAsStr

from Reports.Ui_ReportTraumaSetupDialog import Ui_ReportTraumaSetupDialog


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    byPeriodIssueDate = params.get('byPeriodIssueDate', 0)
    db = QtGui.qApp.db
    tableAction = db.table('Action')
    tableActionType = db.table('ActionType')
    tableEvent = db.table('Event')
    tableActionPropertyType = db.table('ActionPropertyType')
    tableClient = db.table('Client')
    tableActionProperty = db.table('ActionProperty')
    tablePerson = db.table('vrbPerson')
    tableActionPropertyBoolean = db.table('ActionProperty_Boolean')

    cond = [tableAction['deleted'].eq(0),
            tableActionType['deleted'].eq(0),
            tableActionType['flatCode'].eq('trauma'),
            tableActionPropertyType['descr'].eq(u'Гололед'),
            tableActionPropertyBoolean['value'].eq(1),
            tableActionPropertyType['id'].eq(tableActionProperty['type_id'])
            ]
    havingCond = ''

    if byPeriodIssueDate:
        havingCond = u'HAVING incidentDate BETWEEN DATE("%s") AND DATE("%s")' % (forceString(begDate.toString("yyyy-MM-dd")), forceString(endDate.toString("yyyy-MM-dd")))
    else:
        cond.append(u'DATE(Action.`begDate`) BETWEEN DATE("%s") AND DATE("%s")' % (forceString(begDate.toString("yyyy-MM-dd")), forceString(endDate.toString("yyyy-MM-dd"))))

    cols = [tableClient['id'].alias('clientId'),
            tablePerson['name'].alias('personName'),
            u'CONCAT(Client.lastName, " ", Client.firstName, " ", Client.patrName) as clientName',
            tableClient['birthDate'].alias('clientBirthDate'),
            u'age(Client.birthDate, Action.endDate) AS clientAge',
            tableClient['sex'].alias('clientSex'),
            u'GETCLIENTREGADDRESS(Client.id) as clientRegAddress',
            u'GETCLIENTLOCADDRESS(Client.id) as clientLocAddress',

            u''' (SELECT GROUP_CONCAT(contact) FROM ClientContact
                LEFT JOIN rbContactType ON rbContactType.id = ClientContact.contactType_id
                WHERE ClientContact.client_id = Client.id AND rbContactType.name LIKE '%телефон%') AS phones''',

            u'''(SELECT APSp.value FROM ActionProperty AS APp
                LEFT JOIN ActionPropertyType AS APTp ON APTp.id = APp.type_id
                LEFT JOIN ActionProperty_String AS APSp ON APSp.id = APp.id
                WHERE APTp.descr = 'Происшествие' AND Action.id = APp.action_id LIMIT 1) AS incident''',

            u'''(SELECT APDdp.value FROM ActionProperty AS APdp
                LEFT JOIN ActionPropertyType AS APTdp ON APTdp.id = APdp.type_id
                LEFT JOIN ActionProperty_Date AS APDdp ON APDdp.id = APdp.id
                WHERE APTdp.descr = 'Дата происшествия' AND Action.id = APdp.action_id LIMIT 1) AS incidentDate''',

            u'''(SELECT APDdp.value FROM ActionProperty AS APdp
                LEFT JOIN ActionPropertyType AS APTdp ON APTdp.id = APdp.type_id
                LEFT JOIN ActionProperty_Time AS APDdp ON APDdp.id = APdp.id
                WHERE APTdp.descr = 'Время происшествия' AND Action.id = APdp.action_id LIMIT 1) AS incidentTime''',

            u'''(SELECT APDdp.value FROM ActionProperty AS APdp
                LEFT JOIN ActionPropertyType AS APTdp ON APTdp.id = APdp.type_id
                LEFT JOIN ActionProperty_String AS APDdp ON APDdp.id = APdp.id
                WHERE APTdp.descr = 'Диагноз происшествия' AND Action.id = APdp.action_id LIMIT 1) AS incidentDiagnostics'''
            ]

    queryTable = tableAction
    queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
    queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
    queryTable = queryTable.leftJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.leftJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
    queryTable = queryTable.leftJoin(tableActionPropertyBoolean, tableActionPropertyBoolean['id'].eq(tableActionProperty['id']))

    groupBy = u'Action.id '
    if havingCond != '':
        groupBy += havingCond

    stmt = db.selectStmtGroupBy(queryTable, cols, cond, groupBy)
    query = db.query(stmt)
    return query



class CReportTraumaIce(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Журнал \"Гололед\"')
        self.orientation = CPageFormat.Landscape

    def getSetupDialog(self, parent):
        result = CReportTraumaSetupDialog(parent)
        result.setTitle(self.title())
        return result

    def dumpParams(self, cursor, params):
        self.params = params
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        description = []

        if begDate and endDate:
            description.append(dateRangeAsStr(u'', begDate, endDate))

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.movePosition(QtGui.QTextCursor.End)
        columns = [('100%', [], CReportBase.AlignCenter)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)

        for i, row in enumerate(description):
            table.setText(i, 0, row)

        cursor.movePosition(QtGui.QTextCursor.End)


    def build(self, params):
        cnt = params.get('cntUser', 1)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(self.title())
        cursor.insertBlock()

        self.dumpParams(cursor, params)
        tableColumns = [('5%',  [u'№'],  CReportBase.AlignLeft),
                        ('10%', [u'Номер медицинской карты'], CReportBase.AlignLeft),
                        ('10%', [u'Врач'], CReportBase.AlignLeft),
                        ('10%', [u'Ф.И.О. пострадавшего'], CReportBase.AlignLeft),
                        ('10%', [u'Дата рождения (полных лет)'], CReportBase.AlignLeft),
                        ('5%',  [u'Пол'], CReportBase.AlignLeft),
                        ('10%', [u'Адрес'], CReportBase.AlignLeft),
                        ('10%', [u'Телефон'], CReportBase.AlignLeft),
                        ('10%', [u'Происшествие'], CReportBase.AlignLeft),
                        ('10%', [u'Дата и время происшествия'], CReportBase.AlignLeft),
                        ('10%', [u'Диагноз'], CReportBase.AlignLeft)
                        ]
        table = createTable(cursor, tableColumns)
        query = selectData(params)

        if query is None:
            return doc

        while query.next():
            record = query.record()
            clientId = forceInt(record.value('clientId'))
            personName = forceString(record.value('personName'))
            clientName = forceString(record.value('clientName'))
            clientBirthDate = forceString(record.value('clientBirthDate'))
            clientAge = forceString(record.value('clientAge'))
            clientSex = forceInt(record.value('clientSex'))
            clientRegAddress = forceString(record.value('clientRegAddress'))
            clientLocAddress = forceString(record.value('clientLocAddress'))
            phones = forceString(record.value('phones'))
            incident = forceString(record.value('incident'))
            incidentDate = forceString(record.value('incidentDate'))
            incidentTime = forceString(record.value('incidentTime'))
            incidentDiagnostics = forceString(record.value('incidentDiagnostics'))

            i = table.addRow()
            table.setText(i, 0, cnt)
            cnt += 1
            table.setText(i, 1, clientId)
            table.setText(i, 2, personName)
            table.setText(i, 3, clientName)
            table.setText(i, 4, u'%s (%s)' % (clientBirthDate, clientAge))
            table.setText(i, 5, formatSex(clientSex))

            if clientRegAddress == clientLocAddress:
                table.setText(i, 6, clientRegAddress)
            else:
                table.setText(i, 6, u'Рег: %s \nФакт:%s' % (clientRegAddress, clientLocAddress))

            table.setText(i, 7, phones)
            table.setText(i, 8, incident)
            table.setText(i, 9, u'%s %s' % (incidentDate, incidentTime))
            table.setText(i, 10, incidentDiagnostics)

        return doc



class CReportTraumaSetupDialog(CDialogBase, Ui_ReportTraumaSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbPeriodIssueDate.setCurrentIndex(params.get('byPeriodIssueDate', 0))
        self.edtCntUser.setValue(params.get('cntUser', 1))

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['byPeriodIssueDate'] = self.cmbPeriodIssueDate.currentIndex()
        result['cntUser'] = self.edtCntUser.value()
        return result
