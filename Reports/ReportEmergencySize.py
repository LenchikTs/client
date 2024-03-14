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

from library.database           import addDateInRange
from library.Utils              import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString
from Orgs.Utils                 import getOrganisationInfo
from Reports.Report             import CReport, CReportEx
from Reports.ReportBase         import CReportBase

from Reports.ReportHealthResortAnalysisUsePlacesRegions import CReportHealthResortSetupDialog



def selectData(db, begDate, endDate):
    stmt= u"""
        SELECT
            Account_Item.id as `accountItemId`,
            Event.id as `eventId`,
            Event.payStatus as `payStatus`,
            Event.client_id as `clientId`,
            Account_Item.sum as `sum`,
            Account_Item.refuseType_id as `refuseType`,
            IF(UNIX_TIMESTAMP(EmergencyCall.begDate) + 20 * 60 <= UNIX_TIMESTAMP(EmergencyCall.arrivalDate), 1, 0) as `quick`,
            EmergencyCall.begDate as `begDate`,
            EmergencyCall.arrivalDate as `arrivalDate`,
            Organisation.id as `insurerId`,
            Organisation.area as `policyRegionCode`
        FROM
            Event
            LEFT JOIN Account_Item ON Account_Item.event_id = Event.id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
            LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
            LEFT JOIN Contract ON Contract.id = Event.contract_id
            LEFT JOIN rbFinance ON rbFinance.id = Contract.finance_id
            LEFT JOIN ClientPolicy ON (ClientPolicy.id = getClientPolicyIdForDate(Event.client_id, IF(Contract.id IS NOT NULL AND Contract.deleted=0, IF(rbFinance.code = 2, 1, IF(rbFinance.code = 3, 0, NULL)), NULL), Event.execDate, Event.id))
            LEFT JOIN Organisation ON Organisation.id = ClientPolicy.insurer_id
            LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
        WHERE
            Event.deleted = 0 AND Contract.deleted=0 AND ClientPolicy.deleted = 0
            AND rbMedicalAidType.code in ('4', '5')
            AND %s
    """ # проверять ли ClientPolicy.begDate и ClientPolicy.endDate ?
    tableEvent = db.table('Event')
    cond = []
    addDateInRange(cond, tableEvent['execDate'], begDate, endDate)
    #if orgStructureId:
    #    persons = getOrgStructurePersonIdList(orgStructureId)
    #    cond.append(tableActionStomat['person_id'].inlist(persons))
    return db.query(stmt % (db.joinAnd(cond)))


class CEmergencySizeReport(CReportEx):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Объемы медицинской помощи', u'Объемы медицинской помощи')
        self.table_columns = [
            ('4%', [u'Номер', '', ''], CReportBase.AlignRight),
            ('16%', [u'Наименование показателя', '', u'1'], CReportBase.AlignLeft),
            ('7%', [u'Количество вызовов (вызов)', u'Фактически выполнено', u'2'], CReportBase.AlignRight),
            ('8%', [u'', u'Принято к оплате', u'3'], CReportBase.AlignRight),
            ('7%', [u'Количество лиц, которым оказана скорая медицинская помощь (чел)', u'Всего', u'4'], CReportBase.AlignRight),
            ('8%', [u'', u'По принятым к оплате счетам', u'5'], CReportBase.AlignRight),
            ('12%', [u'Сумма по выставленным счетам МО (руб.)', '', u'6'], CReportBase.AlignRight),
            ('13%', [u'Сумма отказов по выставленным счетам (руб.)', '', u'7'], CReportBase.AlignRight),
            ('15%', [u'Стоимость единицы объема медицинской помощи по принятым к оплате счетам (руб.)', '', u'8'], CReportBase.AlignRight),
            ('10%', [u'Сумма по оплаченным счетам (руб.)', '', u'9'], CReportBase.AlignRight),
            ]


    def getSetupDialog(self, parent):
        result = CReportHealthResortSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getReportName(self):
        return u'Объемы медицинской помощи и поступление средств ОМС в медицинские организации, оказывающие скорую медицинскую помощь'


    def getDescription(self, params):
        rows = CReport.getDescription(self, params)
        orgId = QtGui.qApp.currentOrgId()
        orgInfo = getOrganisationInfo(orgId)
        rows.append(u'Наименование МО: %s'%orgInfo.get('fullName', ''))
        return rows


    #def getPeriodName(self, params):
    #    begDate = params.get('begDate', QDate.currentDate())
    #    endDate = params.get('endDate', QDate.currentDate())
    #    return begDate.toString(u"dd.MM.yyyy - ") + endDate.toString(u"dd.MM.yyyy")


    def getSelectFunction(self, params = None):
        return selectData


    def getReportData(self, query):
        #context = CInfoContext()
        result = {}
        while query.next():
            record = query.record()
            client_id = forceRef(record.value('clientId'))
            event_id = forceRef(record.value('eventId'))
            account_item_id = forceRef(record.value('accountItemId'))
            if account_item_id is None:
                account_item_id = 0
            date = forceDate(record.value('date'))
            sum_ = forceDouble(record.value('sum'))
            hasPayStatus = (forceInt(record.value('payStatus')) != 0)
            hasRefuse = (forceInt(record.value('refuseType')) != 0)
            quick = forceBool(record.value('quick'))
            insurer_id = forceRef(record.value('insurerId'))
            policyRegionCode = forceString(record.value('policyRegionCode')) if insurer_id else None
            info = (date, sum_, hasPayStatus, hasRefuse, quick, policyRegionCode)
            result.setdefault(client_id, {}).setdefault(event_id, {}).setdefault(account_item_id, []).append(info)

        reportData = [[0,]*8, [0,]*8, [0,]*8, [0,]*8, [0,]*8]
        for client_id in result.keys():
            hasPayedEvent = False
            hasQuickEvent = False
            regionNumber = 1
            for event_id in result[client_id].keys():
                hasPayedAccount = False
                isQuick = False
                for account_item_id in result[client_id][event_id].keys():
                    for (date, sum_, hasPayStatus, hasRefuse, quick, policyRegionCode) in result[client_id][event_id][account_item_id]:
                        reportData[0][4] += sum_
                        if hasPayStatus:
                            hasPayedAccount = True
                        if hasRefuse:
                            reportData[0][5] += sum_
                        if quick:
                            isQuick = True
                            reportData[3][4] += sum_
                            if hasRefuse:
                                reportData[3][5] += sum_
                        if policyRegionCode is None:
                            regionNumber = 4
                        elif policyRegionCode[:2] == '78' or policyRegionCode == '': #TODO: сделать не только для Питера
                            regionNumber = 1
                        else:
                            regionNumber = 2
                        reportData[regionNumber][4] += sum_
                        if hasRefuse:
                            reportData[regionNumber][5] += sum_
                reportData[0][0] += 1
                reportData[regionNumber][0] += 1
                if hasPayedAccount:
                    reportData[0][1] += 1
                    reportData[regionNumber][1] += 1
                    hasPayedEvent = True
                if isQuick:
                    hasQuickEvent = True
                    reportData[3][0] += 1
                    if hasPayedAccount:
                        reportData[3][1] += 1
            reportData[0][2] += 1
            reportData[regionNumber][2] += 1
            if hasPayedEvent:
                reportData[0][3] += 1
                reportData[regionNumber][3] += 1
            if hasQuickEvent:
                reportData[3][2] += 1
                if hasPayedEvent:
                    reportData[3][3] += 1
        for j in xrange(5):
            reportData[j][7] = reportData[j][4] - reportData[j][5]
            reportData[j][6] = round(reportData[j][7] / reportData[j][1] * 100)/100.0 if reportData[j][1] else ''
        return reportData


    def buildInt(self, params, cursor):
        begDate = params.get('begDate', QDate.currentDate())
        endDate = params.get('endDate', QDate.currentDate())

        selectFunction = self.getSelectFunction()
        query = selectFunction(QtGui.qApp.db, begDate, endDate)
        reportData = self.getReportData(query)

        table = self.createTable(cursor)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 2)
        table.mergeCells(0, 4, 1, 2)
        table.mergeCells(0, 6, 2, 1)
        table.mergeCells(0, 7, 2, 1)
        table.mergeCells(0, 8, 2, 1)
        table.mergeCells(0, 9, 2, 1)

        row = table.addRow()
        table.setText(row, 0, '1')
        table.setText(row, 1, u'Плановые объемы')
        table.setText(row, 2, 'X')
        table.setText(row, 4, 'X')
        table.setText(row, 5, 'X')
        table.setText(row, 6, 'X')
        table.setText(row, 7, 'X')
        table.setText(row, 8, 'X')

        row = table.addRow()
        table.setText(row, 0, '2')
        table.setText(row, 1, u'Выполнено всего')
        for i in xrange(8):
            table.setText(row, 2+i, str(reportData[0][i]))

        row = table.addRow()
        table.mergeCells(row, 1, 1, 9)
        table.setText(row, 1, u'из них:')

        row = table.addRow()
        table.setText(row, 0, '3')
        table.setText(row, 1, u'медицинская помощь лицам, застрахованным на территории СПб')
        for i in xrange(8):
            table.setText(row, 2+i, str(reportData[1][i]))

        row = table.addRow()
        table.setText(row, 0, '4')
        table.setText(row, 1, u'медицинская помощь лицам, застрахованным вне территории СПб')
        for i in xrange(8):
            table.setText(row, 2+i, str(reportData[2][i]))

        row = table.addRow()
        table.setText(row, 0, '5')
        table.setText(row, 1, u'медицинская помощь, оказанная в течение 20 минут после вызова')
        for i in xrange(8):
            table.setText(row, 2+i, str(reportData[3][i]))

        row = table.addRow()
        table.mergeCells(row, 1, 1, 9)
        table.setText(row, 1, u'кроме того:')

        row = table.addRow()
        table.setText(row, 0, '6')
        table.setText(row, 1, u'медицинская помощь, оказанная незастрахованным лицам')
        for i in (0, 2, 3):
            table.setText(row, 2+i, str(reportData[4][i]))
        table.setText(row, 3, 'X')
        table.setText(row, 6, 'X')
        table.setText(row, 7, 'X')
        table.setText(row, 8, 'X')
        table.setText(row, 9, 'X')

        return reportData


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        reportName = self.getReportName()
        self.addParagraph(cursor, reportName)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        old_table_columns = [self.table_columns[i] for i in xrange(len(self.table_columns))]
        self.buildInt(params, cursor)
        self.table_columns = old_table_columns
        cursor.movePosition(QtGui.QTextCursor.End)
        for i in xrange(4):
            self.addParagraph(cursor, '')
        sign = u'Руководитель: _________________________________________________'
        self.addParagraph(cursor, sign)
        for i in xrange(2):
            self.addParagraph(cursor, '')
        sign = u'Исполнитель: _________________________________________________'
        self.addParagraph(cursor, sign)
        return doc
