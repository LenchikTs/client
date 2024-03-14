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
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime

from library.Utils             import forceDateTime, forceInt, forceRef, forceString, formatShortName

from Events.ActionStatus       import CActionStatus
from Orgs.Utils                import getOrgStructureDescendants, getOrgStructureFullName, getPersonInfo
from Reports.ReportBase        import CReportBase, createTable
from Reports.Report            import CReport
from Reports.ReportView        import CPageFormat
from Reports.Utils             import dateRangeAsStr
from Reports.JobTypeListDialog import CJobTypeListDialog

from Reports.Ui_ReportInternalDirectionsSetupDialog import Ui_ReportInternalDirectionsSetupDialog


class CReportInternalDirections(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчёт о количестве выписанных направлений на исследования')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.orgId = QtGui.qApp.currentOrgId()
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CInternalDirectionsSetup(parent)
        result.setTitle(self.title())
        return result


    def selectData(self, params):
        db = QtGui.qApp.db
        tableAction       = db.table('Action')
        tableActionType   = db.table('ActionType')
        tableAP           = db.table('ActionProperty')
        tableAPBasic      = db.table('ActionProperty').alias('AP')
        tableAPJob_Ticket = db.table('ActionProperty_Job_Ticket')
        tableJob_Ticket   = db.table('Job_Ticket')
        tableAPT          = db.table('ActionPropertyType')
        tableAPTBasic     = db.table('ActionPropertyType').alias('APT')
        tableAPS          = db.table('ActionProperty_String')
        tableEvent        = db.table('Event')
        tableClient       = db.table('Client')
        tablePerson       = db.table('vrbPersonWithSpeciality')
        tableOrgStructure = db.table('OrgStructure')

        begDate        = params.get('begDate', QDateTime.currentDateTime())
        endDate        = params.get('endDate', QDateTime.currentDateTime())
        actionTypeId   = params.get('actionTypeId', None)
        actionStatus   = params.get('actionStatus', None)
        personId       = params.get('personId', None)
        orgStructureId = params.get('orgStructureId', None)
        jobTypeList    = params.get('jobTypeList', [])
        isJobType      = params.get('isJobType', False)
        isFIO          = params.get('isFIO', False)


        numberTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        numberTable = numberTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
        table = tableAction.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.leftJoin(tableAPTBasic, tableAPTBasic['actionType_id'].eq(tableActionType['id']))
        table = table.leftJoin(tableAPBasic, tableAPBasic['action_id'].eq(tableAction['id']))
        table = table.leftJoin(tableAPJob_Ticket, tableAPJob_Ticket['id'].eq(tableAPBasic['id']))
        table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['setPerson_id']))
        table = table.leftJoin(tableOrgStructure, db.joinAnd([tableOrgStructure['id'].eq(tablePerson['orgStructure_id']), tableOrgStructure['deleted'].eq(0)]))

        cond = [tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableAPTBasic['deleted'].eq(0),
                tableAPBasic['deleted'].eq(0),
                tableAPTBasic['typeName'].like('JobTicket'),
                u'''(DATE(%s) BETWEEN DATE(%s) AND DATE(%s))''' % (tableAction['directionDate'].name(), db.formatDate(begDate), db.formatDate(endDate)),
                tableAPBasic['type_id'].eq(tableAPTBasic['id'])
                ]
        cols = [tableEvent['id'].alias('eventId'),
                tableEvent['client_id'].alias('clientId'),
                tableAPJob_Ticket['value'].alias('jobTicketValue'),
                tableAction['actionType_id'].alias('actionTypeId'),
                tableActionType['code'].alias('actionCode'),
                tableActionType['name'].alias('actionName'),
                tableOrgStructure['id'].alias('orgStructureId'),
                tableOrgStructure['code'].alias('orgStructureCode'),
                tableOrgStructure['name'].alias('orgStructureName'),
                tablePerson ['id'].alias('personId'),
                tablePerson ['name'].alias('personName'),
                tableJob_Ticket['status'].alias('jobTicketStatus')
               ]
        if isFIO:
            cols.append(tableClient['lastName'])
            cols.append(tableClient['firstName'])
            cols.append(tableClient['patrName'])
            cols.append(tableClient['birthDate'])
        if actionStatus is not None:
            cond.append(tableAction['status'].eq(actionStatus))
        if orgStructureId:
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
        if personId:
            cond.append(tableAction['setPerson_id'].eq(personId))
        if actionTypeId:
            cond.append(tableActionType['id'].eq(actionTypeId))
        if jobTypeList:
            tableJob = db.table('Job')
            table = table.innerJoin(tableJob_Ticket, tableJob_Ticket['id'].eq(tableAPJob_Ticket['value']))
            table = table.innerJoin(tableJob, tableJob['id'].eq(tableJob_Ticket['master_id']))
            cond.append(tableJob_Ticket['deleted'].eq(0))
            cond.append(tableJob['deleted'].eq(0))
            cond.append(tableJob['jobType_id'].inlist(jobTypeList))
        else:
            table = table.leftJoin(tableJob_Ticket, db.joinAnd([tableJob_Ticket['id'].eq(tableAPJob_Ticket['value']), tableJob_Ticket['deleted'].eq(0)]))
        if isJobType:
            tableJob = db.table('Job')
            tableRBJobType = db.table('rbJobType')
            if not jobTypeList:
                table = table.leftJoin(tableJob, tableJob['id'].eq(tableJob_Ticket['master_id']))
            table = table.leftJoin(tableRBJobType, tableRBJobType['id'].eq(tableJob['jobType_id']))
            cols.append(tableRBJobType['name'].alias('jobTypeName'))
            cols.append(tableRBJobType['id'].alias('jobTypeId'))
        recordList = db.getRecordList(table, cols, cond)
        dataOS = {}
        jobTicketList = {}
        clientList = {}
        for record in recordList:
            jobTicketValue = forceRef(record.value('jobTicketValue'))
            personId = forceRef(record.value('personId'))
            eventId = forceRef(record.value('eventId'))
            jobTicketLine = jobTicketList.get((personId, eventId), [])
            if jobTicketValue and (not jobTicketLine or jobTicketValue not in jobTicketLine):
                orgStructureId  = forceRef(record.value('orgStructureId'))
                clientId        = forceRef(record.value('clientId'))
                jobTicketStatus = forceInt(record.value('jobTicketStatus'))
                nameOS          = forceString(record.value('orgStructureName'))
                personName      = forceString(record.value('personName'))
                dataPerson = dataOS.setdefault((nameOS, orgStructureId), {})
                if isFIO:
                    clientName = formatShortName(record.value('lastName'), record.value('firstName'), record.value('patrName')) + u', ' + forceString(record.value('birthDate'))
                    if isJobType:
                        dataJobType = dataPerson.setdefault((personName, personId), {})
                        jobTypeName = forceString(record.value('jobTypeName'))
                        jobTypeId   = forceRef(record.value('jobTypeId'))
                        clientListLine = dataJobType.setdefault((jobTypeName, jobTypeId), {})
                        dataAction = clientListLine.setdefault((clientId, clientName), [0]*3)
                    else:
                        clientListLine = dataPerson.setdefault((personName, personId), {})
                        dataAction = clientListLine.setdefault((clientId, clientName), [0]*3)
                    dataAction[0] += 1
                    if clientId and (clientId, clientName) not in clientListLine:
                        dataAction[1] += 1
                    if jobTicketStatus == 2:
                        dataAction[2] += 1
                    jobTicketLine.append(jobTicketValue)
                    jobTicketList[(personId, eventId)] = jobTicketLine
                else:
                    if isJobType:
                        dataJobType = dataPerson.setdefault((personName, personId), {})
                        jobTypeName = forceString(record.value('jobTypeName'))
                        jobTypeId   = forceRef(record.value('jobTypeId'))
                        dataAction  = dataJobType.setdefault((jobTypeName, jobTypeId), [0]*3)
                        clientJobTypeListId = clientList.setdefault(personId, {})
                        clientListId = clientJobTypeListId.setdefault(jobTypeId, [])
                    else:
                        dataAction = dataPerson.setdefault((personName, personId), [0]*3)
                        clientListId = clientList.setdefault(personId, [])
                    dataAction[0] += 1
                    if clientId and clientId not in clientListId:
                        dataAction[1] += 1
                        clientListId.append(clientId)
                    if jobTicketStatus == 2:
                        dataAction[2] += 1
                    jobTicketLine.append(jobTicketValue)
                    jobTicketList[(personId, eventId)] = jobTicketLine
        return dataOS, clientList


    def build(self, params):
        dataOS, clientList = self.selectData(params)
        isJobType = params.get('isJobType', False)
        isFIO     = params.get('isFIO', False)
        tableColumns = [
                        ('5%',  [u'№ п/п'],                              CReportBase.AlignRight),
                        ('25%', [u'Наименование подразделения'],         CReportBase.AlignLeft),
                        ('25%', [u'ФИО врача, специальность врача'],     CReportBase.AlignLeft),
                        ('10%' if isJobType else '15%', [u'Количество оформленных направлений'], CReportBase.AlignLeft),
                        ('10%' if isJobType else '15%', [u'ФИО пациента'] if isFIO else [u'Количество пациентов'], CReportBase.AlignLeft),
                        ('10%' if isJobType else '15%', [u'Статус "Закончено"'], CReportBase.AlignLeft)
                       ]
        if isJobType:
            tableColumns.insert(3, ('15%', [u'Тип работы'],CReportBase.AlignLeft))

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)
        osNames = dataOS.keys()
        osNames.sort()
        iRow = 1
        totalIRow = [0]*3
        totalIRowAll = [0]*3
        prevOS = None#('', None)
        prevOSRow = 1
        if isFIO:
            if isJobType:
                for osName, osId in osNames:
                    dataPerson = dataOS.get((osName, osId), {})
                    totalIRow = [0]*3
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    if prevOS != (osName, osId):
                        prevOS = (osName, osId)
                        prevOSRow = i
                        table.setText(i, 1, osName)
                    personNames = dataPerson.keys()
                    personNames.sort()
                    personRow = 1
                    prevPerson = None#('', None)
                    prevPersonRow = i
                    clientIdList = []
                    for personName, personId in personNames:
                        if prevPerson != (personName, personId):
                            table.setText(i, 2, personName)
                            prevPerson = (personName, personId)
                            prevPersonRow = i
                        dataJobType = dataPerson.setdefault((personName, personId), {})
                        jobTypes = dataJobType.keys()
                        jobTypes.sort()
                        jobTypeRow = 1
                        for jobTypeName, jobTypeId in jobTypes:
                            prevJobTypeRow = i
                            table.setText(i, 3, jobTypeName)
                            clientListLine = dataJobType.setdefault((jobTypeName, jobTypeId), {})
                            clientKeys = clientListLine.keys()
                            clientKeys.sort(key=lambda x: x[1])
                            clientKeyRow = 1
                            for clientId, clientName in clientKeys:
                                dataAction = clientListLine.setdefault((clientId, clientName), [0]*3)
                                if clientId and clientId not in clientIdList:
                                    clientIdList.append(clientId)
                                table.setText(i, 5, clientName)
                                for j, val in enumerate(dataAction):
                                    table.setText(i, j+4, val)
                                    if j != 1:
                                        totalIRow[j] += val
                                        totalIRowAll[j] += val
                                if clientKeyRow < len(clientKeys):
                                    clientKeyRow += 1
                                    i = table.addRow()
                                    table.mergeCells(prevJobTypeRow, 3, i-prevJobTypeRow+1, 1)
                            if jobTypeRow < len(jobTypes):
                                jobTypeRow += 1
                                i = table.addRow()
                        iRow += 1
                        if personRow < len(personNames):
                            personRow += 1
                            i = table.addRow()
                            table.setText(i, 0, iRow)
                            table.mergeCells(prevPersonRow, 0, i-prevPersonRow, 1)
                            table.mergeCells(prevPersonRow, 2, i-prevPersonRow, 1)
                        else:
                            table.mergeCells(prevPersonRow, 0, i-prevPersonRow+1, 1)
                            table.mergeCells(prevPersonRow, 2, i-prevPersonRow+1, 1)
                    totalIRow[1] += len(clientIdList)
                    totalIRowAll[1] += len(clientIdList)
                    table.mergeCells(prevOSRow, 1, i-prevOSRow+1, 1)
                    i = table.addRow()
                    table.setText(i, 0, u'Итого по %s'%(osName), charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRow):
                        table.setText(i, j+4, val, charFormat=CReportBase.ReportSubTitle)
                if dataOS:
                    i = table.addRow()
                    table.setText(i, 0, u'Всего направлений', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRowAll):
                        table.setText(i, j+4, val, charFormat=CReportBase.ReportSubTitle)
            else:
                for osName, osId in osNames:
                    dataPerson = dataOS.get((osName, osId), {})
                    totalIRow = [0]*3
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    if prevOS != (osName, osId):
                        prevOS = (osName, osId)
                        prevOSRow = i
                        table.setText(i, 1, osName)
                    personNames = dataPerson.keys()
                    personNames.sort()
                    personRow = 1
                    prevPerson = ('', None)
                    prevPersonRow = i
                    clientIdList = []
                    for personName, personId in personNames:
                        if prevPerson != (personName, personId):
                            table.setText(i, 2, personName)
                            prevPerson = (personName, personId)
                            prevPersonRow = i
                        clientListLine = dataPerson.setdefault((personName, personId), {})
                        clientKeys = clientListLine.keys()
                        clientKeys.sort(key=lambda x: x[1])
                        clientKeyRow = 1
                        for clientId, clientName in clientKeys:
                            dataAction = clientListLine.setdefault((clientId, clientName), [0]*3)
                            if clientId and clientId not in clientIdList:
                                clientIdList.append(clientId)
                            table.setText(i, 4, clientName)
                            for j, val in enumerate(dataAction):
                                table.setText(i, j+3, val)
                                if j != 1:
                                    totalIRow[j] += val
                                    totalIRowAll[j] += val
                            if clientKeyRow < len(clientKeys):
                                clientKeyRow += 1
                                i = table.addRow()
                        iRow += 1
                        if personRow < len(personNames):
                            personRow += 1
                            i = table.addRow()
                            table.setText(i, 0, iRow)
                            table.mergeCells(prevPersonRow, 0, i-prevPersonRow, 1)
                            table.mergeCells(prevPersonRow, 2, i-prevPersonRow, 1)
                        else:
                            table.mergeCells(prevPersonRow, 0, i-prevPersonRow+1, 1)
                            table.mergeCells(prevPersonRow, 2, i-prevPersonRow+1, 1)
                    totalIRow[1] += len(clientIdList)
                    totalIRowAll[1] += len(clientIdList)
                    table.mergeCells(prevOSRow, 1, i-prevOSRow+1, 1)
                    i = table.addRow()
                    table.setText(i, 0, u'Итого по %s'%(osName), charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRow):
                        table.setText(i, j+3, val, charFormat=CReportBase.ReportSubTitle)
                if dataOS:
                    i = table.addRow()
                    table.setText(i, 0, u'Всего направлений', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRowAll):
                        table.setText(i, j+3, val, charFormat=CReportBase.ReportSubTitle)
        else:
            if isJobType:
                for osName, osId in osNames:
                    dataPerson = dataOS.get((osName, osId), {})
                    totalIRow = [0]*3
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    if prevOS != (osName, osId):
                        prevOS = (osName, osId)
                        prevOSRow = i
                        table.setText(i, 1, osName)
                    personNames = dataPerson.keys()
                    personNames.sort()
                    personRow = 1
                    prevPerson = None#('', None)
                    prevPersonRow = i
                    for personName, personId in personNames:
                        if prevPerson != (personName, personId):
                            table.setText(i, 2, personName)
                            prevPerson = (personName, personId)
                            prevPersonRow = i
                        dataJobType = dataPerson.setdefault((personName, personId), {})
                        jobTypes = dataJobType.keys()
                        jobTypes.sort()
                        jobTypeRow = 1
                        for jobTypeName, jobTypeId in jobTypes:
                            table.setText(i, 3, jobTypeName)
                            dataAction = dataJobType.setdefault((jobTypeName, jobTypeId), [0]*3)
                            for j, val in enumerate(dataAction):
                                table.setText(i, j+4, val)
                                if j != 1:
                                    totalIRow[j] += val
                                    totalIRowAll[j] += val
                            if jobTypeRow < len(jobTypes):
                                jobTypeRow += 1
                                i = table.addRow()
                        iRow += 1
                        if personRow < len(personNames):
                            personRow += 1
                            i = table.addRow()
                            table.setText(i, 0, iRow)
                            table.mergeCells(prevPersonRow, 0, i-prevPersonRow, 1)
                            table.mergeCells(prevPersonRow, 2, i-prevPersonRow, 1)
                        else:
                            table.mergeCells(prevPersonRow, 0, i-prevPersonRow+1, 1)
                            table.mergeCells(prevPersonRow, 2, i-prevPersonRow+1, 1)
                        clientJobTypeListId = clientList.get(personId, {})
                        resClientIdList = set([])
                        for keyCJT, valIdList in clientJobTypeListId.items():
                            resClientIdList |= set(valIdList)
                        clientCount = len(list(resClientIdList))
                        totalIRow[1] += clientCount
                        totalIRowAll[1] += clientCount
                    table.mergeCells(prevOSRow, 1, i-prevOSRow+1, 1)
                    i = table.addRow()
                    table.setText(i, 0, u'Итого по %s'%(osName), charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRow):
                        table.setText(i, j+4, val, charFormat=CReportBase.ReportSubTitle)
                if dataOS:
                    i = table.addRow()
                    table.setText(i, 0, u'Всего направлений', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRowAll):
                        table.setText(i, j+4, val, charFormat=CReportBase.ReportSubTitle)
            else:
                for osName, osId in osNames:
                    dataPerson = dataOS.get((osName, osId), {})
                    totalIRow = [0]*3
                    i = table.addRow()
                    table.setText(i, 0, iRow)
                    if prevOS != (osName, osId):
                        prevOS = (osName, osId)
                        prevOSRow = i
                        table.setText(i, 1, osName)
                    personNames = dataPerson.keys()
                    personNames.sort()
                    personRow = 1
                    prevPerson = ('', None)
                    prevPersonRow = i
                    for personName, personId in personNames:
                        if prevPerson != (personName, personId):
                            table.setText(i, 2, personName)
                            prevPerson = (personName, personId)
                            prevPersonRow = i
                        dataAction = dataPerson.setdefault((personName, personId), [0]*3)
                        for j, val in enumerate(dataAction):
                            table.setText(i, j+3, val)
                            totalIRow[j] += val
                            totalIRowAll[j] += val
                        iRow += 1
                        if personRow < len(personNames):
                            personRow += 1
                            i = table.addRow()
                            table.setText(i, 0, iRow)
                        table.mergeCells(prevPersonRow, 2, i-prevPersonRow, 1)
                    table.mergeCells(prevOSRow, 1, i-prevOSRow+1, 1)
                    i = table.addRow()
                    table.setText(i, 0, u'Итого по %s'%(osName), charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRow):
                        table.setText(i, j+3, val, charFormat=CReportBase.ReportSubTitle)
                if dataOS:
                    i = table.addRow()
                    table.setText(i, 0, u'Всего направлений', charFormat=CReportBase.ReportSubTitle, blockFormat=CReportBase.AlignLeft)
                    table.mergeCells(i, 0, 1, 3)
                    for j, val in enumerate(totalIRowAll):
                        table.setText(i, j+3, val, charFormat=CReportBase.ReportSubTitle)
        return doc


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        personId = params.get('personId', None)
        actionTypeId = params.get('actionTypeId', None)
        actionStatus = params.get('actionStatus', None)
        orgStructureId = params.get('orgStructureId', None)
        rows = []
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if actionTypeId:
            actionTypeName=forceString(db.translate('ActionType', 'id', actionTypeId, 'name'))
            rows.append(u'мероприятие: '+actionTypeName)
        if actionStatus is not None:
            rows.append(u'статус выполнения действия: '+ CActionStatus.text(actionStatus))
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        if personId:
            personInfo = getPersonInfo(personId)
            rows.append(u'направитель: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        jobTypeList = params.get('jobTypeList', [])
        if jobTypeList:
            db = QtGui.qApp.db
            table = db.table('rbJobType')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(jobTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            rows.append(u'Типы работ: %s'%(u', '.join(name for name in nameList if name)))
        else:
            rows.append(u'Типы работ: не задано')
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


class CInternalDirectionsSetup(QtGui.QDialog, Ui_ReportInternalDirectionsSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbActionStatus.insertSpecialValue(u'не задано', None)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        db = QtGui.qApp.db
        table = db.table('ActionType')
        tableAPT = db.table('ActionPropertyType')
        tableQuery = table.leftJoin(tableAPT, tableAPT['actionType_id'].eq(table['id']))
        cond = [table['flatCode'].like('%Direction%'),
                table['deleted'].eq(0),
                table['class'].eq(3),
                tableAPT['typeName'].like('JobTicket')
               ]
        recordList = db.getRecordList(tableQuery, 'ActionType.id, ActionType.code, ActionType.name',  cond, order='code, name')
        self.actionTypes = [None]
        self.cmbActionType.addItem(u'Любой')
        for record in recordList:
            id = forceInt(record.value('id'))
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            self.actionTypes.append(id)
            self.cmbActionType.addItem('%s| %s'%(code, name))
        self.jobTypeList = []


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        begDate = forceDateTime(params.get('begDate', QDateTime.currentDateTime()))
        endDate = forceDateTime(params.get('endDate', QDateTime.currentDateTime()))
        self.edtBegDate.setDate(begDate.date())
        self.edtEndDate.setDate(endDate.date())
        self.edtBegTime.setTime(begDate.time())
        self.edtEndTime.setTime(endDate.time())
        self.cmbActionStatus.setValue(params.get('actionStatus', None))
        self.cmbActionType.setCurrentIndex(params.get('actionTypeIndex', 0))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.chkJobType.setChecked(params.get('isJobType', False))
        self.chkFIO.setChecked(params.get('isFIO', False))
        self.jobTypeList = params.get('jobTypeList', [])
        if self.jobTypeList:
            db = QtGui.qApp.db
            table = db.table('rbJobType')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.jobTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            self.lblJobType.setText(u', '.join(name for name in nameList if name))
        else:
            self.lblJobType.setText(u'не задано')


    def params(self):
        result = {}
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        begTime = self.edtBegTime.time()
        endTime = self.edtEndTime.time()
        result['begDate'] = QDateTime(begDate, begTime)
        result['endDate'] = QDateTime(endDate, endTime)
        result['actionStatus'] = self.cmbActionStatus.value()
        result['personId'] = self.cmbPerson.value()
        actionTypeIndex = self.cmbActionType.currentIndex()
        result['actionTypeIndex'] = actionTypeIndex
        result['actionTypeId'] = self.actionTypes[actionTypeIndex]
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['jobTypeList'] = self.jobTypeList
        result['isJobType'] = self.chkJobType.isChecked()
        result['isFIO'] = self.chkFIO.isChecked()
        return result


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


    @pyqtSignature('')
    def on_btnJobType_clicked(self):
        self.jobTypeList = []
        self.lblJobType.setText(u'не задано')
        dialog = CJobTypeListDialog(self)
        if dialog.exec_():
            self.jobTypeList = dialog.values()
            if self.jobTypeList:
                db = QtGui.qApp.db
                table = db.table('rbJobType')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.jobTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblJobType.setText(u', '.join(name for name in nameList if name))

