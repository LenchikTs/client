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
from PyQt4.QtCore import QDateTime, QLocale, QDate

from library.Utils      import forceBool, forceDouble, forceRef, forceString, forceInt
from Reports.Report     import CReport
from Reports.ReportView import CPageFormat
from Reports.ReportBase import CReportBase, createTable
from Reports.FinanceSummaryByDoctors import CFinanceSummarySetupDialog
from Reports.FinanceSummaryByServices import selectDataByEvents, selectDataByActions, selectDataByVisits


class CFinanceSummaryByOrgStructures(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по подразделениям')
        self.datailVAT = False
        self.orientation = CPageFormat.Landscape


    def build(self, description, params):
        reportDataAll = {}
        reportRowSize = 9
        def processQuery(query, reportDataGlobal):
            while query.next():
                record = query.record()
                code        = forceString(record.value('code'))
                name        = forceString(record.value('name'))
                amount      = forceDouble(record.value('amount'))
                price       = forceDouble(record.value('price'))
                orgStructureId   = forceRef(record.value('orgStructureId'))
                orgStructureName   = forceString(record.value('orgStructureName'))
                orgStructureCode   = forceString(record.value('orgStructureCode'))
                uet         = forceDouble(record.value('uet'))
                if amount == int(amount):
                   amount = int(amount)
                sum         = forceDouble(record.value('sum'))
                payedSum         = forceDouble(record.value('payedSum'))
                exposed     = forceBool(record.value('exposed'))
                refused     = forceBool(record.value('refused'))
                key = (name if name else u'Без указания услуги',
                               code, price)
                reportData = reportDataGlobal
                reportOrgStructureData = reportData.setdefault((orgStructureId, orgStructureCode, orgStructureName), {})
                reportLine = reportOrgStructureData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += amount
                reportLine[1] += uet
                reportLine[2] += sum
                if exposed:
                    reportLine[3] += amount if sum == payedSum else forceInt(amount-(sum-payedSum)/price)
                    reportLine[4] += uet
                    reportLine[5] += payedSum
                if refused:
                    reportLine[6] += amount if payedSum==0 else forceInt((sum-payedSum)/price)
                    reportLine[7] += uet
                    reportLine[8] += sum-payedSum
                reportOrgStructureData[key] = reportLine
                reportData[(orgStructureId, orgStructureCode, orgStructureName)] = reportOrgStructureData
            return reportDataGlobal

        query = selectDataByEvents(params)
        reportDataAll = processQuery(query, reportDataAll)
        query = selectDataByVisits(params)
        reportDataAll = processQuery(query, reportDataAll)
        query = selectDataByActions(params)
        reportDataAll = processQuery(query, reportDataAll)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()
        tableColumns = [
                          ('50%', [ u'Подразделение'], CReportBase.AlignLeft ),
                          ('50%', [ u'Оказано услуг на сумму'], CReportBase.AlignLeft ),
                       ]
        self.tableColumnsLen = len(tableColumns)
        table = createTable(cursor, tableColumns)

        locale = QLocale()
        self.groupRows = 2

        def printTableData(table, reportData):
            totalByReport = [0]*reportRowSize
            totalReportPrice = 0

            orgStructureKeys = reportData.keys()
            orgStructureKeys.sort()

            for orgStructureId, orgStructureCode, orgStructureName in orgStructureKeys:
                totalByOrgStructure = [0]*reportRowSize
                reportOrgStructureData = reportData.get((orgStructureId, orgStructureCode, orgStructureName), {})
                if not reportOrgStructureData:
                    continue

                keys = reportOrgStructureData.keys()
                keys.sort()

                for key in keys:

                    price = key[2]


                    reportLine = reportOrgStructureData[key]
                    totalReportPrice += price

                    for j in xrange(reportRowSize):
                        totalByReport[j] += reportLine[j]
                        totalByOrgStructure[j] += reportLine[j]
                self.addTotal(table, u'%s'%(orgStructureName if orgStructureName else u'Не указано'), totalByOrgStructure, locale, totalReportPrice)
            self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice)
            totalByReport = [0]*reportRowSize
            totalReportPrice = 0

        printTableData(table, reportDataAll)

        return doc


    def addTotal(self, table, title, reportLine, locale, totalPrice, width=2):
        if reportLine[5]:
            i = table.addRow()
            table.setText(i, 0, title, CReportBase.TableTotal)
            table.setText(i, 1, locale.toString(float(reportLine[5]), 'f', 2))


class CFinanceSummaryByOrgStructuresEx(CFinanceSummaryByOrgStructures):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSummaryByOrgStructures.exec_(self)


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate              = params.get('begDate', None)
        endDate              = params.get('endDate', None)
        confirmation         = params.get('confirmation', False)
        confirmationBegDate  = params.get('confirmationBegDate', None)
        confirmationEndDate  = params.get('confirmationEndDate', None)
        confirmationType     = params.get('confirmationType', 0)
        refuseType           = params.get('refuseType', None)
        isPeriodOnService    = params.get('isPeriodOnService', False)

        finance = params.get('finance', None)

        rows = []
        if isPeriodOnService:
            rows.append(u'учитывать период по услуге')
        if begDate:
            rows.append(u'Дата начала периода: %s'%forceString(begDate))
        if endDate:
            rows.append(u'Дата окончания периода: %s'%forceString(endDate))
        if finance:
            rows.append(u'Тип финансирования: %s'%forceString(db.translate('rbFinance', 'id', finance, 'name')))
        if confirmation:
            rows.append(u'Тип подтверждения: %s'%{0: u'без подтверждения',
                                                  1: u'оплаченные',
                                                  2: u'отказанные'}.get(confirmationType, u''))
            if confirmationBegDate:
                rows.append(u'Начало периода подтверждения: %s'%forceString(confirmationBegDate))
            if confirmationEndDate:
                rows.append(u'Окончание периода подтверждения: %s'%forceString(confirmationEndDate))
            if refuseType:
                rows.append(u'Причина отказа: %s'%forceString(db.translate('rbPayRefuseType', 'id', refuseType, 'CONCAT_WS(\' | \', code,name)')))
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


    def getSetupDialog(self, parent):
        result = CFinanceSummarySetupDialog(parent)
        result.setVisiblePeriodOnService(True)
        result.setOrgStructureVisible(False)
        result.setSpecialityVisible(False)
        result.setPersonVisible(False)
        result.setDetailClientVisible(False)
        result.setFreeInputWorkVisible(False)
        result.setInsurerDoctorsVisible(False)
        result.setVisibleServiceGroup(False)
        result.setVisibleFinance(True)
        result.setVisibleDetailPerson(False)
        result.setVisibleDetailOrgStructure(False)
        result.setVisibleClientOrganisation(False)
        result.setVisibleSocStatusParams(False)
        result.setVisibleDetailFinance(False)
        result.setVisibleDetailPayer(False)
        result.setVisibleDetailVAT(False)
        result.setEventTypeVisible(False)
        result.setEventTypeListVisible(False)
        result.setVisibleDetailMedicalAidKind(False)
        result.setVisibleDetailSpeciality(False)
        result.setVisibleDetailActionType(False)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CFinanceSummaryByOrgStructures.build(self, '\n'.join(self.getDescription(params)), params)



def parseDate(date):
    return forceString(QDate.fromString(date, 'yyyy.MM').toString('MMMM yyyy'))
