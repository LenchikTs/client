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

import datetime

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDateTime, QVariant

from library.Utils            import firstMonthDay, forceDate, forceDouble, forceString, forceRef, lastMonthDay, formatShortNameInt
from library.AmountToWords    import amountToWords
from Orgs.Utils               import getOrganisationInfo
from Reports.Report           import CReport
from Reports.ReportBase       import CReportBase, createTable
from Reports.Utils            import dateRangeAsStr

from Ui_ActReconcilMutualSettlementsSetupDialog import Ui_ActReconcilMutualSettlementsSetupDialog


def selectDataSaldo(contractId, begDate, endDate):
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    cond = [tableAccount['deleted'].eq(0),
            tableAccount['contract_id'].eq(contractId)
           ]
    if begDate:
        cond.append(tableAccount['date'].ge(begDate))
    if endDate:
        cond.append(tableAccount['date'].lt(endDate))
    stmt="""
SELECT
    SUM(Account.sum) AS debet,
    SUM(Account.payedSum) AS kredit
FROM Account
WHERE
     %s
GROUP BY Account.contract_id
    """
    return db.query(stmt % (db.joinAnd(cond)))


def selectData(params):
    date = QDate.currentDate().addDays(-3)
    begDate = params.get('begDate', firstMonthDay(date))
    endDate = params.get('endDate', lastMonthDay(date))
    contractId = params.get('contractId', None)
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableAccountItem = db.table('Account_Item')
    cond = [tableAccount['contract_id'].eq(contractId),
            tableAccount['deleted'].eq(0),
            tableAccount['date'].isNotNull()
           ]
    condAI = [tableAccountItem['master_id'].eq(tableAccount['id']),
              tableAccountItem['date'].isNotNull(),
              tableAccountItem['refuseType_id'].isNull(),
              tableAccountItem['deleted'].eq(0)
              ]
    if begDate:
        cond.append(tableAccount['date'].ge(begDate))
        condAI.append(tableAccountItem['date'].ge(begDate))
    if endDate:
        cond.append(tableAccount['date'].le(endDate))
        condAI.append(tableAccountItem['date'].le(endDate))
    stmt="""
SELECT
    Account.id AS accountId,
    Account.date AS dateA,
    Account.sum AS sumAccount,
    Account.number AS numberAccount,
    Account_Item.id AS accountItemId,
    Account_Item.date AS dateAI,
    Account_Item.number AS numberAccountItem,
    Account_Item.payedSum AS payedSumAccountItem
FROM Account
LEFT JOIN Account_Item ON (%s)
WHERE
     %s
ORDER BY Account.date, Account_Item.date
    """
    return db.query(stmt % (db.joinAnd(condAI), db.joinAnd(cond)))


class CActReconciliationMutualSettlements(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Акт сверки взаимных расчетов')


    def getSetupDialog(self, parent):
        result = CActReconcilMutualSettlementsSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getPersonName(self, code, orgId, begDate):
        personName = u''
        if orgId:
            db = QtGui.qApp.db
            tablePerson = db.table('Person')
            tableRBPost = db.table('rbPost')
            cols = [tablePerson['lastName'],
                    tablePerson['firstName'],
                    tablePerson['patrName']
                    ]
            cond = [tablePerson['deleted'].eq(0),
                    tableRBPost['code'].eq(code),
                    tablePerson['org_id'].eq(orgId),
                    db.joinOr([tablePerson['retireDate'].isNull(), tablePerson['retireDate'].ge(begDate)])
                    ]
            record = db.getRecordEx(tableRBPost.innerJoin(tablePerson, tablePerson['post_id'].eq(tableRBPost['id'])), cols, cond)
            if record:
                lastName = forceString(record.value('lastName'))
                firstName = forceString(record.value('firstName'))
                patrName = forceString(record.value('patrName'))
                personName = formatShortNameInt(lastName, firstName, patrName)
        return personName


    def build(self, params):
        date = QDate.currentDate().addDays(-3)
        begDate = params.get('begDate', firstMonthDay(date))
        endDate = params.get('endDate', lastMonthDay(date))
        contractId = params.get('contractId', None)
        doc = QtGui.QTextDocument()
        if contractId:
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setCharFormat(CReportBase.ReportBody)
            descriptionIns1 = u'Акт сверки взаимных расчетов за период ' + begDate.toString('dd.MM.yyyy') + u' г. ' + u'по ' + endDate.toString('dd.MM.yyyy') + u' г.'
            orgId = QtGui.qApp.currentOrgId()
            orgInfo = getOrganisationInfo(orgId)
            if not orgInfo:
                QtGui.qApp.preferences.appPrefs['orgId'] = QVariant()
            shortName = orgInfo.get('shortName', u'ЛПУ в настройках не указано!')
            db = QtGui.qApp.db
            tableContract = db.table('Contract')
            tableOrganisation = db.table('Organisation')
            cond = [tableContract['id'].eq(contractId),
                    tableOrganisation['deleted'].eq(0),
                    tableOrganisation['deleted'].eq(0)]
            record = db.getRecordEx(tableContract.innerJoin(tableOrganisation, tableOrganisation['id'].eq(tableContract['payer_id'])), [tableOrganisation['shortName']], cond)
            payerName = forceString(record.value('shortName')) if record else u''
            descriptionIns2 = u'между СПб ГБУЗ ' + shortName + u' и ' + payerName + u'.'
            tableHeaderColumns = [
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter),
                              ('12.5%', [u''], CReportBase.AlignCenter)
                           ]
            tableHeader = createTable(cursor, tableHeaderColumns, headerRowCount = 2, border = 0)
            tableHeader.setText(0, 0, descriptionIns1, charFormat = CReportBase.ReportTitle)
            tableHeader.setText(1, 0, descriptionIns2, charFormat = CReportBase.ReportTitle)
            tableHeader.mergeCells(0, 0,  1, 8)
            tableHeader.mergeCells(1, 0,  1, 8)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            self.dumpParams(cursor, params)
            tableColumns = [
                              ('12.5%', [u'' , u'Дата'    ], CReportBase.AlignLeft),
                              ('12.5%', [u'' , u'Документ'], CReportBase.AlignLeft),
                              ('12.5%', [u'' , u'Дебет'   ], CReportBase.AlignLeft),
                              ('12.5%', [u'' , u'Кредит ' ], CReportBase.AlignLeft),
                              ('12.5%', [u'' , u'Дата'    ], CReportBase.AlignRight),
                              ('12.5%', [u'' , u'Документ'], CReportBase.AlignRight),
                              ('12.5%', [u'' , u'Дебет'   ], CReportBase.AlignRight),
                              ('12.5%', [u'' , u'Кредит ' ], CReportBase.AlignRight)
                           ]
            self.tableColumnsLen = len(tableColumns)
            table = createTable(cursor, tableColumns)
            table.mergeCells(0, 0,  1, 4)
            table.mergeCells(0, 4,  1, 4)
            table.mergeCells(2, 0,  1, 2)
            table.mergeCells(2, 4,  1, 2)
            table.setText(0, 0, shortName, charFormat = CReportBase.ReportTitle, blockFormat = CReportBase.AlignCenter)
            table.setText(0, 4, payerName, charFormat = CReportBase.ReportTitle, blockFormat = CReportBase.AlignCenter)
            debet = 0.00
            kredit = 0.00
            begSaldoDate = QDate(begDate.year(), 1, 1)
            if begSaldoDate < begDate:
                records = selectDataSaldo(contractId, QDate(begDate.year(), 1, 1), begDate)
                while records.next():
                    record = records.record()
                    debet += forceDouble(record.value('debet'))
                    kredit += forceDouble(record.value('kredit'))

            i = table.addRow()
            table.setText(i, 0, u'Сальдо начальное', charFormat = CReportBase.ReportSubTitle)
            table.mergeCells(i, 0,  1, 2)
            table.setText(i, 2, '%.2f'%(debet))
            table.setText(i, 3, '%.2f'%(kredit))
            table.setText(i, 4, u'Сальдо начальное', charFormat = CReportBase.ReportSubTitle, blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 4,  1, 2)

            reportData = {}
            accountIdList = []
            accountItemIdList = []
            reportTotal = [0.00, 0.00]
            query = selectData(params)
            while query.next():
                record = query.record()
                accountId = forceRef(record.value('accountId'))
                if accountId and accountId not in accountIdList:
                    accountIdList.append(accountId)
                    dateA = forceDate(record.value('dateA'))
                    dateAccount = datetime.date(dateA.year(), dateA.month(), dateA.day())
                    numberAccount = forceString(record.value('numberAccount'))
                    sumAccount = forceDouble(record.value('sumAccount'))
                    debetAccount = reportData.get((dateAccount, numberAccount, 0), 0.00)
                    debetAccount += sumAccount
                    reportData[(dateAccount, numberAccount, 0)] = debetAccount
                accountItemId = forceRef(record.value('accountItemId'))
                if accountItemId and accountItemId not in accountIdList:
                    accountItemIdList.append(accountItemId)
                    dateAI = forceDate(record.value('dateAI'))
                    if dateAI:
                        dateAccountItem = datetime.date(dateAI.year(), dateAI.month(), dateAI.day())
                        numberAccountItem = forceString(record.value('numberAccountItem'))
                        payedSumAccountItem = forceDouble(record.value('payedSumAccountItem'))
                        kreditAccount = reportData.get((dateAccountItem, numberAccountItem, 1), 0.00)
                        kreditAccount += payedSumAccountItem
                        reportData[(dateAccountItem, numberAccountItem, 1)] = kreditAccount
            dataKeys = reportData.keys()
            dataKeys.sort()
            for (date, number, type) in dataKeys:
                res = reportData.get((date, number, type), 0.00)
                i = table.addRow()
                reportTotal[type] += res
                table.setText(i, 0, forceDate(date).toString('dd.MM.yyyy'))
                table.setText(i, 1, number)
                table.setText(i, type + 2, '%.2f'%(res))

            i = table.addRow()
            table.setText(i, 0, u'Обороты за период', charFormat = CReportBase.ReportSubTitle)
            for col, val in enumerate(reportTotal):
                table.setText(i, col+2, '%.2f'%(val))
            table.mergeCells(i, 0,  1, 2)
            table.setText(i, 4, u'Обороты за период', charFormat = CReportBase.ReportSubTitle, blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 4,  1, 2)

            saldoEndDebet = (reportTotal[0] - reportTotal[1]) + debet
            i = table.addRow()
            table.setText(i, 0, u'Сальдо конечное', charFormat = CReportBase.ReportSubTitle)
            table.mergeCells(i, 0,  1, 2)
            table.setText(i, 2, '%.2f'%(saldoEndDebet))
            table.setText(i, 3, '%.2f'%(kredit))
            table.setText(i, 4, u'Сальдо конечное', charFormat = CReportBase.ReportSubTitle, blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 4,  1, 2)

            i = table.addRow()
            table.setText(i, 0, u'По данным ' + shortName)
            table.mergeCells(i, 0,  1, 4)
            table.setText(i, 4, u'По данным ' + payerName, blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 4,  1, 4)

            endPeriod = forceString(endDate.addDays(1))
            boldChars = QtGui.QTextCharFormat()
            boldChars.setFontWeight(QtGui.QFont.Bold)
            i = table.addRow()
            table.setText(i, 0, u'На ' + endPeriod + u' задолженность в пользу ' + shortName + u' (%s)'%(amountToWords(saldoEndDebet)), charFormat = boldChars)
            table.setText(i, 2, '%.2f'%(saldoEndDebet) + u' руб.', charFormat = boldChars, blockFormat = CReportBase.AlignCenter)
            table.mergeCells(i, 0,  1, 2)
            table.mergeCells(i, 2,  1, 2)
            table.mergeCells(i, 4,  1, 2)
            table.mergeCells(i, 6,  1, 2)

            if kredit > 0:
                i = table.addRow()
                table.setText(i, 0, u'На ' + endPeriod + u' задолженность в пользу ' + payerName + u' (%s)'%(amountToWords(kredit)), charFormat = boldChars)
                table.setText(i, 2, '%.2f'%(kredit) + u' руб.', charFormat = boldChars, blockFormat = CReportBase.AlignCenter)
                table.mergeCells(i, 0,  1, 2)
                table.mergeCells(i, 2,  1, 2)
                table.mergeCells(i, 4,  1, 2)
                table.mergeCells(i, 6,  1, 2)

            i = table.addRow()
            table.setText(i, 0, u'От ' + shortName)
            table.mergeCells(i, 0,  1, 4)
            table.setText(i, 4, u'От ' + payerName, blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 4,  1, 4)

            i = table.addRow()
            table.setText(i, 0, u'Руководитель')
            table.mergeCells(i, 1,  1, 2)
            table.setText(i, 3, self.getPersonName(u'1001', orgId, begDate))
            table.setText(i, 4, u'Руководитель', blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 5,  1, 2)

            i = table.addRow()
            table.setText(i, 0, u'Главный бухгалтер')
            table.mergeCells(i, 1,  1, 2)
            table.setText(i, 3, self.getPersonName(u'90010', orgId, begDate))
            table.setText(i, 4, u'Главный бухгалтер', blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 5,  1, 2)

            i = table.addRow()
            table.setText(i, 0, u'М.П.')
            table.mergeCells(i, 0,  1, 4)
            table.setText(i, 4, u'М.П.', blockFormat = CReportBase.AlignLeft)
            table.mergeCells(i, 4,  1, 4)

        return doc


    def getDescription(self, params):
        date = QDate.currentDate().addDays(-3)
        begDate = params.get('begDate', firstMonthDay(date))
        endDate = params.get('endDate', lastMonthDay(date))
        contractText         = params.get('contractText', None)
        rows = []
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if contractText:
            rows.append(u'Контракт: %s' % contractText)
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


class CActReconcilMutualSettlementsSetupDialog(QtGui.QDialog, Ui_ActReconcilMutualSettlementsSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.edtBegDate.setDate(params.get('begDate', firstMonthDay(date)))
        self.edtEndDate.setDate(params.get('endDate', lastMonthDay(date)))
        self.cmbContract.setValue(params.get('contractId', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['contractId'] = self.cmbContract.value()
        result['contractText'] = forceString(self.cmbContract.currentText())
        return result

