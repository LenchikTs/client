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

from PyQt4              import QtGui
from PyQt4.QtCore       import QDate, QTime, QDateTime
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from library.Utils      import forceInt, forceString

from Ui_DiagnosticYearReportSetupDialog import Ui_DiagnosticYearReportSetupDialog


def selectData(reportYear, orgStructureList, params):
    begYear = QDateTime(QDate(reportYear, 1, 1), QTime(0,0,0))
    endYear = QDateTime(QDate(reportYear, 12, 31), QTime(23,59,59))
    reportData = dict()   # {'name' : count}
    db = QtGui.qApp.db

    tableAction      = db.table('Action')
    tableActionType  = db.table('ActionType')
    tableClient      = db.table('Client')
    tableEvent       = db.table('Event')
    tablePerson      = db.table('Person')
    tableOrgStrucure = db.table('OrgStructure')

    queryTable = tableEvent
    queryTable = queryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    queryTable = queryTable.innerJoin(tablePerson, tableAction['setPerson_id'].eq(tablePerson['id']))
    queryTable = queryTable.innerJoin(tableOrgStrucure, tablePerson['orgStructure_id'].eq(tableOrgStrucure['id']))

    cols = [ tableOrgStrucure['name'].alias('orgStructure'),
             'COUNT(*) AS resCount'
           ]
    cond = [ tableAction['deleted'].eq(0),
             tableActionType['serviceType'].inlist([5,10]),
             tableAction['status'].eq(2),
             tableAction['endDate'].ge(begYear),
             tableAction['endDate'].le(endYear),
             '(YEAR(Action.createDatetime) - YEAR(Client.birthDate)) BETWEEN %d AND %d' % (params['ageFrom'], params['ageTo']),
             tableOrgStrucure['id'].inlist(orgStructureList),
           ]

    if params['isUrgent']:
        cond.append(tableAction['isUrgent'].eq(1))
    if params['person']:
        cond.append(tablePerson['id'].eq(params['person']))

    stmt = db.selectStmtGroupBy(queryTable, cols, where=cond, group=tablePerson['orgStructure_id'].name())
    query = db.query(stmt)
    while query.next():
        record = query.record()
        name = forceString(record.value('orgStructure'))
        reportData[name] = forceInt(record.value('resCount'))

    return reportData



class CDiagnosticYearReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=1, topMargin=1, rightMargin=1,  bottomMargin=1)
        self.diagnosticYearReportSetupDialog = None
        self.setTitle(u'Годовой отчет по диагностическим отделениям')

    def getSetupDialog(self, parent):
        result = CDiagnosticYearReportSetupDialog(parent)
        self.diagnosticYearReportSetupDialog = result
        return result

    def getCurrentOrgStructureIdList(self):
        cmbOrgStruct = self.diagnosticYearReportSetupDialog.cmbOrgStructure
        treeIndex = cmbOrgStruct._model.index(cmbOrgStruct.currentIndex(), 0, cmbOrgStruct.rootModelIndex())
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)

        cursor.insertText(u'Годовой отчет за ЛПУ по диагностическим отделениям с учетом плановых и фактических показателей в сравнении с прошедшими периодами')
        cursor.insertBlock()
        alignRight = CReportBase.AlignRight
        alignLeft = CReportBase.AlignLeft

        orgStructureList = self.getCurrentOrgStructureIdList()
        reportYear = params['reportYear']
        years = [ selectData(reportYear, orgStructureList, params),
                  selectData(reportYear-1, orgStructureList, params),
                  selectData(reportYear-2, orgStructureList, params)
                ]
        dic = years[0]

        for i in years[0].keys():
            dic[i] = [years[0][i], years[1].get(i, 0), years[2].get(i, 0)]
        for i in years[1].keys():
            if not dic.has_key(i):
                dic[i] = [0, years[1][i], years[2].get(i, 0)]
        for i in years[2].keys():
            if not dic.has_key(i):
                dic[i] = [0, 0, years[2][i]]

        ## dic = {'name': [countInYear1, countInYear2, countInYear3]}

        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('25%', [u'Отделения', u'', u''], alignLeft),
                ('9%', [u'%d год' % (reportYear), u'Кол-во исследований', u'План'], alignLeft),
                ('8%', [u'', u'', u'Факт'], alignLeft),
                ('8%', [u'', u'% выполн.', u''], alignLeft),

                ('9%', [u'%d год' % (reportYear-1), u'Кол-во исследований', u'План'], alignLeft),
                ('8%', [u'', u'', u'Факт'], alignLeft),
                ('8%', [u'', u'% выполн.', u''], alignLeft),

                ('9%', [u'%d год' % (reportYear-2), u'Кол-во исследований', u'План'], alignLeft),
                ('8%', [u'', u'', u'Факт'], alignLeft),
                ('8%', [u'', u'% выполн.', u''], alignLeft)]
        table = createTable(cursor, cols)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 1, 3)
        table.mergeCells(0, 4, 1, 3)
        table.mergeCells(0, 7, 1, 3)

        table.mergeCells(1, 1, 1, 2)
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(1, 7, 1, 2)

        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(1, 9, 2, 1)

        for orgName, count in dic.items():
            row = table.addRow()
            table.setText(row, 0, orgName)
            table.setText(row, 2, count[0], blockFormat=alignRight)
            table.setText(row, 5, count[1], blockFormat=alignRight)
            table.setText(row, 8, count[2], blockFormat=alignRight)

        return doc



class CDiagnosticYearReportSetupDialog(QtGui.QDialog, Ui_DiagnosticYearReportSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def setParams(self, params):
        self.edtReportYear.setValue(params.get('reportYear', 2000))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.cmbOrgStructure.setValue(params.get('orgStructure', None))
        self.cmbPerson.setValue(params.get('person', None))
        self.chkUrgent.setChecked(params.get('isUrgent', False))

    def params(self):
        return {
            'reportYear':   self.edtReportYear.value(),
            'ageFrom':      self.edtAgeFrom.value(),
            'ageTo':        self.edtAgeTo.value(),
            'orgStructure': self.cmbOrgStructure.value(),
            'person':       self.cmbPerson.value(),
            'isUrgent':     self.chkUrgent.isChecked()
        }

