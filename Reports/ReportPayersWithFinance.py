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

from library.Utils      import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Reports.Ui_ReportPayersWithFinanceSetup import Ui_ReportPayersWithFinanceSetupDialog


def formatDouble(dValue):
    return '%.2f' % dValue


def selectData(params):
    begDate                = params.get('begDate', None)
    endDate                = params.get('endDate', None)
    contractId             = params.get('contractId', None)
    financeId               = params.get('financeId', 4)
    eventTypeId         = params.get('eventTypeId', None)

    db = QtGui.qApp.db

    cond = 'Account.date >= \'%s-%s-%s\'' % (begDate.year(), begDate.month(),  begDate.day() )
    if endDate:
        cond = '%s AND Account.date <= \'%s-%s-%s\'' % (cond,  endDate.year(), endDate.month(),  endDate.day() )
    if contractId:
        cond = '%s AND Contract.id = %i' % (cond,  contractId)
    if eventTypeId:
        cond = '%s AND Event.eventType_id = %i' % (cond,  eventTypeId)
    if financeId:
        cond = '%s AND Contract.finance_id = %i' % (cond,  financeId)
    stmt = '''
    select
        AccI.id AS AccId,
        AccI.date as exposeDate,
        Account.id AS AccountId,
        Account.amount AS AccCount,
        Account.sum as sum,
        sum(AccI.sum) as sum1,
        ELC.patrName as SurName,
        ELC.firstName as FirstName,
        ELC.lastName as LastName,
        Account.number as docNum,
        Client.lastName as cLastName,
        Client.firstName as cFirstName,
        Client.patrName as cSurName,
        Client.id             as clientId,
        ActionType.code as ATcode,
        ActionType.group_id as ATgroup,
        ActionType.flatCode as flatCode,
        Contract.finance_id as financeId,
        rbFinance.name as financeName,
        if(refuseType_id <> 0, 1, 0) as refused
    from
        Account_Item AS AccI
            LEFT JOIN
        Account ON AccI.master_id = Account.id
            LEFT JOIN
        Event_LocalContract AS ELC ON AccI.event_id = ELC.master_id
            LEFT JOIN
        Event ON AccI.event_id = Event.id
            LEFT JOIN
        Client ON Event.client_id = Client.id
            LEFT JOIN
        Contract ON Contract.id = Account.contract_id
            LEFT JOIN
        rbFinance ON rbFinance.id = Contract.finance_id
            LEFT JOIN
        ActionType_Service ON ActionType_Service.id = (select
                id
            from
                ActionType_Service
            where
                ActionType_Service.service_id = AccI.service_id
            LIMIT 1)
            LEFT JOIN
        ActionType ON ActionType.id = ActionType_Service.master_id
            and ActionType.group_id not in ((SELECT
                id
            FROM
                ActionType
            where
                code = '-'))
    WHERE
        %s
    GROUP BY Event.id , refused, flatCode
    ORDER BY Account.number
    ''' % (cond)
    return db.query(stmt)


class CReportPayersWithFinance(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по плательщикам')
        self._mapPayerIdToInfo = {}
        self._mapPayerIdToAttachedClientsCount = {}
        self._mapPayerAccountsClientsCount = {}
        self._mapFinanceNameToPayerId = {}
        self.resetHelpers()

    def resetHelpers(self):
        self._mapPayerIdToInfo.clear()
        self._mapPayerIdToAttachedClientsCount.clear()
        self._mapPayerAccountsClientsCount.clear()
        self._mapFinanceNameToPayerId.clear()

    def getSetupDialog(self, parent):
        result = CReportPayersSetup(parent, self)
        result.setTitle(self.title())
        return result

    def getDescription(self, params):
        begDate                = params.get('begDate', None)
        endDate                = params.get('endDate', None)
        contractText           = params.get('contractText', None)
        contractId             = params.get('contractId', None)
        financeText            = params.get('financeText', None)
        financeId              = params.get('financeId', None)

        rows = []
        if begDate:
            rows.append(u'Начальная дата периода: %s'%forceString(begDate))
        if endDate:
            rows.append(u'Конечная дата периода: %s'%forceString(endDate))
        if financeId:
            rows.append(u'Тип финансирования: %s' % financeText)
        if contractId:
            rows.append(u'Контракт: %s' % contractText)

        return rows


    def build(self, params):
        query = selectData(params)
        self.structInfo(query, params)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        detailClients = params.get('detailClients', False)

        tableColumns = [
                        ('5%',
                        [u'№ п/п'], CReportBase.AlignLeft),
                        ('5%',
                        [u'№ дог'], CReportBase.AlignLeft),
                        ('40%',
                        [u'Плательщик'], CReportBase.AlignRight),
                        ('25%',
                        [u'Пациент'], CReportBase.AlignRight),
                        ('14%',
                        [u'Сумма'], CReportBase.AlignRight),
                        ('11%',
                        [u'Код услуги'], CReportBase.AlignRight)
                       ]

        table = createTable(cursor, tableColumns)

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)

        detailFinance =  not bool(params.get('financeId', None))

        numShift = 0
        if detailFinance:
            totalResult = [0, 0, '']
            for financeName, payerIdList in self._mapFinanceNameToPayerId.items():
                self.printHeader(table, financeName, boldChars, depth=1)
                numShift += 1
                result = self.printContractList(payerIdList, table, numShift, boldChars, detailClients)
                #payerCount = len(payerIdList)
                #numShift += 2*payerCount if payerCount > 1 else 0
                self.printResult(table, result, boldChars)

                for idx in range(2):
                    totalResult[idx] += result[idx]

            self.printResult(table, totalResult, boldChars)
            numShift += 1

        else:
            result = self.printContractList(self._mapPayerIdToInfo.keys(), table, numShift, boldChars, detailClients)
            self.printResult(table, result, boldChars)
            numShift += 1

        return doc

    def printContractList(self, payerIdList, table, numShift, boldChars, detailClients):
        def div(value, divider):
            return value/divider if divider else value
        resultAccountSum = 0
        resultAccountServicesAmount = 0
        tmpResultAccountAmount = {}
        counters = {}
        row = 0
        for payerId in payerIdList:
            tmpResultAccountSum = 0

            payerInfo = self._mapPayerIdToInfo[payerId]
            if detailClients:
                self.printHeader(table, payerInfo['payerName'], boldChars, depth=1)
                numShift += 1

            contractInfoList = payerInfo['contractInfoList']
            for contractInfo in contractInfoList:
                i = table.addRow()

                tmpResultAccountAmount[contractInfo['id']] = 1
                #if not contractInfo['exposeDate'].isNull() and not contractInfo['refused']:
                if not contractInfo['refused']:
                    tmpResultAccountSum += contractInfo['accountSum']

                row += 1
                table.setText(i, 0, row)
                table.setText(i, 1, contractInfo['docNum'])
                table.setText(i, 2, contractInfo['payerName'])
                table.setText(i, 3, contractInfo['clientName'])
                table.setText(i, 4, contractInfo['accountSum'])
                table.setText(i, 5, contractInfo['flatCode'])
                if contractInfo['flatCode'] not in counters:
                    counters[contractInfo['flatCode']] = 0
                counters[contractInfo['flatCode']] += 1
            resultAccountSum += tmpResultAccountSum
        docCount = len(tmpResultAccountAmount.keys())
        resultAccountServicesAmount += docCount
        q = []
        map(lambda (x,y): q.append('%s: %i'%(x,y)), counters.items())
        counterText = ', '.join( q )

        return [resultAccountServicesAmount,
                resultAccountSum, counterText]


    def printHeader(self, table, value, boldChars, depth=0):
        i = table.addRow()
        table.setText(i, 0, (u' '*4*depth)+value, charFormat=boldChars)
        table.mergeCells(i, 0, 1, 7)

    def printResult(self, table, result, boldChars):
        i = table.addRow()
        #table.setText(i,  0,  u'Количество договоров: %i. Усл - %i, 16 - %i, Стац - %i'%(result[0],  self.usl,  self.six,  self.stat), charFormat=boldChars)
        table.setText(i, 0, u'Количество счетов: %i. %s'%(result[0], result[2]))
        table.setText(i,  4,  result[1], charFormat=boldChars)
        table.mergeCells(i, 0, 2,  3)

    def structInfo(self, query, params):
#        begDate                = params.get('begDate', None)
#        endDate                = params.get('endDate', None)
#        contractId             = params.get('contractId', None)
        financeIdParam              = params.get('financeId', None)
#        detailContracts        = params.get('detailContracts', False)

        detailFinance = not bool(financeIdParam)
        self.counters = {}

        self.resetHelpers()

        while query.next():
            record = query.record()

            payerId = forceRef(record.value('clientId'))
            AccountId = forceInt(record.value('AccountId'))
            AccCount = forceInt(record.value('AccCount'))
            exposeDate = forceDate(record.value('exposeDate'))
            sum = forceDouble(record.value('sum1'))
            SurName = forceString(record.value('SurName'))
            FirstName = forceString(record.value('FirstName'))
            LastName = forceString(record.value('LastName'))
            cSurName = forceString(record.value('cSurName'))
            cFirstName = forceString(record.value('cFirstName'))
            cLastName = forceString(record.value('cLastName'))
            docNum = forceString(record.value('docNum'))
            flatCode = forceString(record.value('flatCode'))
            isRef = forceBool(record.value('refused'))
            #financeId = forceInt(record.value('financeId'))
            financeName = forceString(record.value('financeName'))
            payerName = '%s %s %s' %(LastName,  FirstName,  SurName)
            clientName = '%s %s %s' %(cLastName,  cFirstName, cSurName)

            if isRef:
                flatCode = u'Возв.'
            else:
                if not flatCode:
                    flatCode = u'Услуга'

            if detailFinance:
                payerIdList = self._mapFinanceNameToPayerId.setdefault(financeName, [payerId])
                if payerId not in payerIdList:
                    payerIdList.append(payerId)

            payerInfo = self._mapPayerIdToInfo.setdefault(payerId, {'payerName':clientName, 'contractInfoList':[]})
            contractInfoList = payerInfo.setdefault('contractInfoList', [])
            contractInfo = {}
            contractInfo['id'] = AccountId
            contractInfo['payerName'] = payerName
            contractInfo['clientName'] = clientName
            contractInfo['accountServicesAmount'] = AccCount
            contractInfo['accountSum'] = sum
            contractInfo['docNum'] = docNum
            contractInfo['flatCode'] = flatCode
            contractInfo['refused'] = isRef
            contractInfo['exposeDate'] = exposeDate
            contractInfoList.append(contractInfo)



    def getAttachedClientsCount(self, payerId):
        result = self._mapPayerIdToAttachedClientsCount.get(payerId, None)
        if result is None:
            db = QtGui.qApp.db
            tableClientPolicy = db.table('ClientPolicy')
            tableContract = db.table('Contract')
            tableAccount = db.table('Account')
            tableFinance = db.table('rbFinance')
            tablePolicuType = db.table('rbPolicyType')

            queryTable = tableClientPolicy
            queryTable = queryTable.leftJoin(tableAccount,    tableAccount['payer_id'].eq(tableClientPolicy['insurer_id']))
            queryTable = queryTable.leftJoin(tableContract,   tableContract['id'].eq(tableAccount['contract_id']))
            queryTable = queryTable.leftJoin(tableFinance,    tableFinance['id'].eq(tableContract['finance_id']))
            queryTable = queryTable.leftJoin(tablePolicuType, tablePolicuType['id'].eq(tableClientPolicy['policyType_id']))

            cond = [tableClientPolicy['insurer_id'].eq(payerId),
                    tableAccount['exposeDate'].dateBetween(tableClientPolicy['begDate'], tableClientPolicy['endDate']),
                    'IF(rbFinance.`code` = \'2\', rbPolicyType.`code` IN (\'1\',\'2\'), IF(rbFinance.`code` = \'3\', rbPolicyType.`code` IN (\'3\'), 0))']

            result = db.getDistinctCount(queryTable, tableClientPolicy['client_id'].name(), cond)
            self._mapPayerIdToAttachedClientsCount[payerId] = result
        return result

    def getAccountsClientsCount(self, payerId, accountId, clientOrganisationId, freeInputWork, freeInputWorkValue):
        key = (payerId, accountId)
        result = self._mapPayerAccountsClientsCount.get(key, None)
        if result is None:
            db = QtGui.qApp.db
            tableAccountItem = db.table('Account_Item')
            tableEvent       = db.table('Event')
            tableAccount     = db.table('Account')
            tableClientWork  = db.table('ClientWork')

            queryTable = tableAccountItem.innerJoin(tableEvent, tableEvent['id'].eq(tableAccountItem['event_id']))
            queryTable = queryTable.innerJoin(tableAccount, tableAccount['id'].eq(tableAccountItem['master_id']))

            cond = [tableAccount['payer_id'].eq(payerId),
                    tableAccount['id'].eq(accountId)]

            if clientOrganisationId or (freeInputWork and freeInputWorkValue):
                subCond = []
                if clientOrganisationId:
                    subCond.append(tableClientWork['org_id'].eq(clientOrganisationId))
                if (freeInputWork and freeInputWorkValue):
                    subCond.append(tableClientWork['freeInput'].like(freeInputWorkValue))

                cond.append('''
                EXISTS(
                SELECT ClientWork.`id`
                FROM ClientWork
                WHERE ClientWork.client_id=Event.client_id
                AND ClientWork.`id`=(
                                     SELECT MAX(CW.`id`)
                                     FROM ClientWork AS CW
                                     WHERE ClientWork.client_id=CW.client_id)
                AND %s)''' % db.joinOr(subCond))

            result = db.getDistinctCount(queryTable,
                                         tableEvent['client_id'].name(),
                                         cond)
            self._mapPayerAccountsClientsCount[key] = result
        return result


class CReportPayersSetup(QtGui.QDialog, Ui_ReportPayersWithFinanceSetupDialog):
    def __init__(self, parent, report):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self._report = report
        self.cmbFinance.setTable('rbFinance', addNone=True)
        self.cmbEventType.setTable('EventType', addNone=True)
        self.chkDetailContracts.setVisible(False)

    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbContract.setValue(params.get('contractId', None))
        self.cmbFinance.setValue(params.get('financeId', None))
        self.chkDetailContracts.setChecked(params.get('detailContracts', False))
        self.chkDetailClients.setChecked(params.get('detailClients', False))
        self.cmbEventType.setValue(params.get('eventTypeId', None))

    def params(self):
        params = {}

        params['contractId'] = self.cmbContract.value()
        params['contractText'] = forceString(self.cmbContract.currentText())
        params['financeId']  = self.cmbFinance.value()
        params['financeText'] = self.cmbFinance.currentText()
        params['eventTypeId']  = self.cmbEventType.value()

        params['begDate'] = self.edtBegDate.date()
        params['endDate'] = self.edtEndDate.date()

        params['detailContracts']  = self.chkDetailContracts.isChecked()
        params['detailClients'] = self.chkDetailClients.isChecked()

        return params


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbContract.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbContract.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbFinance_currentChanged(self, index):
        financeId = self.cmbFinance.value()
        self.cmbContract.setFinanceId(financeId)


    @pyqtSignature('int')
    def on_cmbContract_currentChanged(self, index):
        contractId = self.cmbContract.value()
        self.chkDetailContracts.setEnabled(bool(contractId))







