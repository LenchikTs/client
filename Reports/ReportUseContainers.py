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
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils             import forceInt, forceRef, forceString

from Reports.Utils             import getJobTicketPropertyAction
from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable
from ContainerTypeListEditorDialog import CContainerTypeListEditorDialog

from Reports.Ui_ReportUseContainersSetup import Ui_ReportUseContainersSetupDialog


def selectData(params):
    begDate           = params.get('begDate', QDate())
    endDate           = params.get('endDate', QDate())
    orgStructureId    = params.get('orgStructureId', None)
    containerTypeList = params.get('containerTypeList', None)
    if not endDate:
        return None
    db = QtGui.qApp.db
    tableAction        = db.table('Action')
    tableActionType    = db.table('Action')
    tablePerson        = db.table('Person')
    tableContainerType = db.table('rbContainerType')
    cond = [tableAction['deleted'].eq(0),
            tableActionType['deleted'].eq(0)
            ]
    queryTable = u''
    if orgStructureId:
        orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
        if orgStructureIdList:
            queryTable = u'INNER JOIN Person ON Person.id = Action.person_id'
            cond.append(tablePerson['deleted'].eq(0))
            cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    if containerTypeList:
        cond.append(tableContainerType['id'].inlist(containerTypeList))
    stmt = u'''SELECT
    rbContainerType.id AS containerTypeId,
    rbContainerType.name AS containerTypeName,
    SUM(Action.amount) AS amountA,
    SUM(ActionType_TissueType.amount) AS amountATTT,
    %(jobTicketPA)s AS jobTicketId,
    ActionType_TissueType.tissueType_id,
    ActionType_TissueType.containerType_id,
    ActionType_TissueType.id AS aTTTId
    FROM Action
    INNER JOIN ActionType ON ActionType.id = Action.actionType_id
    INNER JOIN ActionType_TissueType ON ActionType_TissueType.master_id = Action.actionType_id
    INNER JOIN rbTissueType ON rbTissueType.id = ActionType_TissueType.tissueType_id
    INNER JOIN rbContainerType ON rbContainerType.id = ActionType_TissueType.containerType_id
    INNER JOIN TakenTissueJournal ON TakenTissueJournal.id = Action.takenTissueJournal_id
    %(queryTable)s
    WHERE DATE(TakenTissueJournal.datetimeTaken) IS NOT NULL
    AND DATE(TakenTissueJournal.datetimeTaken) >= %(begDate)s AND DATE(TakenTissueJournal.datetimeTaken) <= %(endDate)s
    AND rbTissueType.id = TakenTissueJournal.tissueType_id AND TakenTissueJournal.deleted = 0
    AND %(cond)s
    GROUP BY containerTypeId, containerTypeName, jobTicketId, tissueType_id, containerType_id, aTTTId
    ORDER BY containerTypeName
    ''' % { 'jobTicketPA': getJobTicketPropertyAction(),
            'queryTable' : queryTable,
            'begDate'    : db.formatDate(begDate),
            'endDate'    : db.formatDate(endDate),
            'cond'       : db.joinAnd(cond)
          }
    return db.query(stmt)


class CReportUseContainers(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Использование контейнеров')


    def dumpParams(self, cursor, params):
        description = self.getDescription(params)
        description.insert(len(description)-2, u'события %s'%([u'только закрытые', u'только открытые', u'все'][params.get('eventStatus', 0)]))
        containerTypeList = params.get('containerTypeList', None)
        if containerTypeList:
            db = QtGui.qApp.db
            table = db.table('rbContainerType')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(containerTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            description.insert(len(description)-2, u'тип контейнера:  %s'%(u','.join(name for name in nameList if name)))
        else:
            description.insert(len(description)-2, u'тип контейнера:  не задано')
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getSetupDialog(self, parent):
        result = CReportUseContainersSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getReportData(self, query):
        reportData = {}
        reportDataTotal = 0
        jobTicketDict = {}
        containerTypeList = []
        while query.next():
            record = query.record()
            containerTypeId   = forceRef(record.value('containerTypeId'))
            containerTypeName = forceString(record.value('containerTypeName'))
            jobTicketId       = forceRef(record.value('jobTicketId'))
            tissueTypeId      = forceRef(record.value('tissueType_id'))
            containerTypeATId = forceRef(record.value('containerType_id'))
            containerTypeList = jobTicketDict.get((jobTicketId, tissueTypeId, containerTypeATId), [])
            if containerTypeId not in containerTypeList:
                amountA    = forceInt(record.value('amountA'))
                amountATTT = forceInt(record.value('amountATTT'))
                reportLine = reportData.get((containerTypeId, containerTypeName), 0)
                reportLine += (amountA * amountATTT) if amountATTT else amountA
                reportDataTotal += (amountA * amountATTT) if amountATTT else amountA
                reportData[(containerTypeId, containerTypeName)] = reportLine
                containerTypeList.append(containerTypeId)
                jobTicketDict[(jobTicketId, tissueTypeId, containerTypeATId)] = containerTypeList
        return reportData, reportDataTotal


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ( '10%', [u'№'],              CReportBase.AlignLeft),
            ( '50%', [u'Тип контейнера'], CReportBase.AlignLeft),
            ( '40%', [u'Количество'],     CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        query = selectData(params)
        if query is None:
            return doc
        reportData, total = self.getReportData(query)
        repKeys = reportData.keys()
        repKeys.sort(key=lambda item: item[1])
        cnt = 1
        for repKey in repKeys:
            i = table.addRow()
            table.setText(i, 0, cnt)
            table.setText(i, 1, repKey[1])
            table.setText(i, 2, reportData.get(repKey, 0))
            cnt += 1
        i = table.addRow()
        table.setText(i, 0, u'Всего')
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 2, total)
        return doc


class CReportUseContainersSetupDialog(QtGui.QDialog, Ui_ReportUseContainersSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.containerTypeList = []


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.containerTypeList =  params.get('containerTypeList', [])
        if self.containerTypeList:
            db = QtGui.qApp.db
            table = db.table('rbContainerType')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.containerTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            self.lblContainerType.setText(u','.join(name for name in nameList if name))
        else:
            self.lblContainerType.setText(u'не задано')


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['containerTypeList'] = self.containerTypeList
        return result


    @pyqtSignature('')
    def on_btnContainerType_clicked(self):
        self.containerTypeList = []
        self.lblContainerType.setText(u'не задано')
        dialog = CContainerTypeListEditorDialog(self)
        if dialog.exec_():
            self.containerTypeList = dialog.values()
            if self.containerTypeList:
                db = QtGui.qApp.db
                table = db.table('rbContainerType')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.containerTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblContainerType.setText(u','.join(name for name in nameList if name))

