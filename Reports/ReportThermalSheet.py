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
from PyQt4.QtCore import QDate, QDateTime, QTime

from library.Utils      import calcAge, forceDate, forceDouble, forceRef, forceString, forceTime
from Events.Utils       import getActionTypeIdListByFlatCode
from Orgs.Utils         import getOrgStructureFullName

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Reports.Ui_ReportThermalSheet import Ui_ReportThermalSheetDialog


class CReportThermalSheetDialog(QtGui.QDialog, Ui_ReportThermalSheetDialog):
    def __init__(self, parent=None, currentOrgStructureId=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.currentOrgStructureId = currentOrgStructureId
        if not self.currentOrgStructureId:
            self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
            self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        else:
            self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
            self.cmbOrgStructure.setValue(self.currentOrgStructureId)
        self.medicalDayBegTime = QtGui.qApp.medicalDayBegTime()
        if not self.medicalDayBegTime:
            self.medicalDayBegTime = QTime(9, 0)
        self.edtBegTime.setTime(self.medicalDayBegTime)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        if bool(self.medicalDayBegTime):
            self.edtBegTime.setTime(self.medicalDayBegTime)
        else:
            self.edtBegTime.setTime(params.get('begTime', self.medicalDayBegTime))
        if self.currentOrgStructureId:
            self.cmbOrgStructure.setValue(self.currentOrgStructureId)
        else:
            self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.edtThermalLimit.setValue(params.get('thermalLimit', 0.0))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['begTime'] = self.edtBegTime.time()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['thermalLimit'] = self.edtThermalLimit.value()
        return result


class CReportThermalSheet(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет по данным температурного листа')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.reportThermalSheetSetupDialog = None
        self.clientDeath = 8


    def getSetupDialog(self, parent):
        result = CReportThermalSheetDialog(parent)
        self.reportThermalSheetSetupDialog = result
        return result


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def dumpParams(self, cursor, params):
        description = []
        endDate = params.get('begDate', QDate())
        endTime = params.get('begTime', self.reportThermalSheetSetupDialog.medicalDayBegTime)
        description.append(u'Текущий день: ' + forceString(QDateTime(endDate, endTime)))
        orgStructureId = params.get('orgStructureId', None)
        thermalLimit = params.get('thermalLimit', 0.0)
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')
        description.append(u'Нижний предел температуры: %s'%(str(thermalLimit)))
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        if not begDate:
            begDate = QDate.currentDate()
        if begDate:
            #begTime = params.get('begTime', self.reportThermalSheetSetupDialog.medicalDayBegTime)
            #begDateTime = QDateTime(begDate, begTime) # задача #0011653:0039804
            begDateTime = QDateTime(begDate, QTime())
            #endDateTime = QDateTime(begDate.addDays(1), self.reportThermalSheetSetupDialog.medicalDayBegTime) # задача #0011653:0039804
            endDateTime = QDateTime(begDate, params.get('begTime', self.reportThermalSheetSetupDialog.medicalDayBegTime))
            thermalLimit = params.get('thermalLimit', 0)
            orgStructureId = params.get('orgStructureId', None)
            orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId) if orgStructureId else []
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertBlock()
            cursor.insertText(self.title())
            cursor.insertBlock()
            self.dumpParams(cursor, params)
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            cols = [('5%',  [u'№'],                           CReportBase.AlignLeft),
                    ('25%', [u'ФИО'],                         CReportBase.AlignLeft),
                    ('20%', [u'Подразделение'],               CReportBase.AlignLeft),
                    ('25%', [u'Время измерения температуры'], CReportBase.AlignLeft),
                    ('25%', [u'Данные температуры'],          CReportBase.AlignLeft)
                   ]
            table = createTable(cursor, cols)
            actionTypeIdList = getActionTypeIdListByFlatCode(u'temperatureSheet%')
            if actionTypeIdList:
                tableClient = db.table('Client')
                tableEvent = db.table('Event')
                tableAction = db.table('Action')
                tableAPT = db.table('ActionPropertyType')
                tableAP = db.table('ActionProperty')
                tableAPTemperature = db.table('ActionProperty_Temperature')
                queryTable = tableAction.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
                queryTable = queryTable.innerJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
                queryTable = queryTable.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                queryTable = queryTable.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                queryTable = queryTable.innerJoin(tableAPTemperature, tableAPTemperature['id'].eq(tableAP['id']))
                actionTypeList = getActionTypeIdListByFlatCode(u'moving%')
                cols = [tableClient['lastName'],
                        tableClient['firstName'],
                        tableClient['patrName'],
                        tableClient['birthDate'],
                        tableClient['id'].alias('clientId'),
                        tableAction['endDate'],
                        tableAPTemperature['value'].alias('temperature'),
                        tableAP['action_id']
                        ]
                actionTypeMovingIdList = u''
                if actionTypeList:
                    actionTypeMovingIdList = (','.join(str(actionTypeId) for actionTypeId in actionTypeList if actionTypeId))
                    cols.append(u'''(SELECT OS.name
                        FROM Action AS A
                        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
                        INNER JOIN ActionProperty AS AP ON AP.type_id = APT.id
                        INNER JOIN ActionProperty_OrgStructure AS APOS ON APOS.id = AP.id
                        INNER JOIN OrgStructure AS OS ON OS.id = APOS.value
                        WHERE A.event_id = Event.id AND APT.actionType_id IN (%s)
                        AND A.begDate <= %s AND (A.endDate IS NULL OR A.endDate >= %s)
                        AND AP.action_id = A.id AND A.deleted = 0
                        AND APT.deleted = 0 AND APT.name = '%s'
                        AND OS.deleted = 0
                        ORDER BY A.id DESC
                        LIMIT 1) AS orgStructureName'''%(actionTypeMovingIdList, db.formatDate(begDateTime), db.formatDate(begDateTime), u'Отделение пребывания')
                        )
                cond = [tableAction['deleted'].eq(0),
                        tableEvent['deleted'].eq(0),
                        tableClient['deleted'].eq(0),
                        tableAPT['deleted'].eq(0),
                        tableAP['deleted'].eq(0),
                        tableAction['actionType_id'].inlist(actionTypeIdList),
                        tableAPT['actionType_id'].inlist(actionTypeIdList),
                        tableAPT['typeName'].like(u'Temperature'),
                        tableAPTemperature['value'].ge(thermalLimit)
                        ]
                if orgStructureIdList and actionTypeMovingIdList:
                    orgStructureList = [u'NULL']
                    for orgStructureId in orgStructureIdList:
                        orgStructureList.append(forceString(orgStructureId))
                    cond.append(u'''
                    EXISTS(SELECT OS2.id
                    FROM Action AS A2
                    INNER JOIN ActionPropertyType AS APT2 ON APT2.actionType_id=A2.actionType_id
                    INNER JOIN ActionProperty AS AP2 ON AP2.type_id=APT2.id
                    INNER JOIN ActionProperty_OrgStructure AS APOS2 ON APOS2.id=AP2.id
                    INNER JOIN OrgStructure AS OS2 ON OS2.id=APOS2.value
                    WHERE APT2.actionType_id IN (%s) AND A2.event_id = Event.id
                    AND A2.begDate <= %s AND (A2.endDate IS NULL OR A2.endDate >= %s)
                    AND A2.deleted = 0
                    AND AP2.action_id=A2.id AND APT2.deleted=0
                    AND APT2.name = '%s'
                    AND OS2.deleted=0 AND APOS2.value %s)'''%(actionTypeMovingIdList, db.formatDate(begDateTime), db.formatDate(begDateTime), u'Отделение пребывания', u' IN ('+(','.join(orgStructureList))+')'))
                cond.append(tableAction['endDate'].ge(begDateTime))
                cond.append(tableAction['endDate'].lt(endDateTime))
                records = db.getRecordList(queryTable, cols, cond, u'Client.firstName, Client.lastName, Client.patrName, Action.endDate')
                clientList = {}
                clientNameList = {}
                temperatureList = {}
                for record in records:
                    clientAge = calcAge(forceDate(record.value('birthDate')), QDate.currentDate())
                    FIO = forceString(record.value('lastName')) + u' ' + forceString(record.value('firstName')) + u' ' + forceString(record.value('patrName')) + u'(' + clientAge + u')'
                    clientId = forceRef(record.value('clientId'))
                    temperature = forceDouble(record.value('temperature'))
                    endTime = forceTime(record.value('endDate'))
                    orgStructureName = forceString(record.value('orgStructureName'))
                    if clientId and (clientId, orgStructureName) not in clientNameList.keys():
                        clientNameList[(clientId, orgStructureName)] = (FIO, orgStructureName)
                    temperatureList = clientList.get((clientId, orgStructureName), {})
                    temperatureList[pyTime(endTime)] = '%0.1f' % temperature
                    clientList[(clientId, orgStructureName)] = temperatureList
                if clientList:
                    i = table.addRow()
                    cnt = 1
                    countRow = 0
                    for value in clientList.values():
                        countRow += len(value)
                    for (clientId, orgStructureName), temperatureList in clientList.items():
                        table.setText(i, 0, cnt)
                        FIO, orgStructureName = clientNameList.get((clientId, orgStructureName), u'')
                        table.setText(i, 1, FIO)
                        table.setText(i, 2, orgStructureName)
                        keys = temperatureList.keys()
                        keys.sort()
                        rowNext = i
                        for key in keys:
                            temperature = temperatureList.get(key)
                            table.setText(rowNext, 3, QTime(key).toString('hh:mm'))
                            table.setText(rowNext, 4, temperature)
                            table.mergeCells(i, 0, rowNext-i+1, 1)
                            table.mergeCells(i, 1, rowNext-i+1, 1)
                            table.mergeCells(i, 2, rowNext-i+1, 1)
                            if countRow > rowNext:
                                rowNext = table.addRow()
                        cnt += 1
                        i = rowNext
        return doc


def pyTime(time):
    if time and time.isValid():
        return time.toPyTime()
    else:
        return None


