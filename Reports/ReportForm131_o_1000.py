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

from library.Utils             import firstYearDay, forceInt, lastYearDay
from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())

    if not endDate:
        return None

    begYearDate = firstYearDay(begDate)
    endYearDate = lastYearDay(endDate)

    db = QtGui.qApp.db
    stmt = u'''
SELECT clientSex,
       clientAge,
       SUM(directed) AS directedCnt,
       SUM(executed) AS executedCnt
FROM (SELECT SUM(DATE(Event.setDate)     BETWEEN %(begYearDate)s AND %(endYearDate)s
                 OR DATE(Event.execDate) BETWEEN %(begYearDate)s AND %(endYearDate)s
                )>0 AS directed,
             SUM(DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s)>0 AS executed,
             Client.sex AS clientSex,
             age(Client.birthDate, %(endYearDate)s) AS clientAge
      FROM Event
      INNER JOIN mes.MES ON mes.MES.id=Event.MES_id
      INNER JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id=mes.MES.group_id
      INNER JOIN Client ON Client.id=Event.client_id
      WHERE (Event.deleted=0)
        AND DATE(Event.setDate) BETWEEN %(begPrevYearDate)s AND %(endYearDate)s
        AND (mes.mrbMESGroup.code='ДиспанС')
      GROUP BY Client.id) AS T
GROUP BY clientSex, clientAge''' % dict(begDate = db.formatDate(begDate),
                                        endDate = db.formatDate(endDate),
                                        begYearDate = db.formatDate(begYearDate),
                                        endYearDate = db.formatDate(endYearDate),
                                        begPrevYearDate = db.formatDate(begYearDate.addYears(-1))
                                       )
    return db.query(stmt)


class CReportForm131_o_1000(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о половозрастном составе населения субъекта Российской Федерации, в том числе подлежащих диспансеризации')


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        return result


    def getReportData(self, query):
        reportData = {}
        for clientAge in xrange(18, 100, 3):
            reportData[clientAge] = [0]*9

        while query.next():
            record = query.record()
            clientSex   = forceInt(record.value('clientSex'))
            clientAge   = forceInt(record.value('clientAge'))
            directedCnt = forceInt(record.value('directedCnt'))
            executedCnt = forceInt(record.value('executedCnt'))
            if directedCnt or executedCnt:
                data = reportData.get(clientAge, None)
                if data is None:
                    reportData[clientAge] = data = [0]*9
                column = 1 if clientSex == 1 else 4
                data[column] += directedCnt
                data[7] += directedCnt
                data[column+1] += executedCnt
                data[8] += executedCnt
        return reportData


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ( '5%', [u'Возраст', u''], CReportBase.AlignLeft),
            ( '3%', [u'№', u''], CReportBase.AlignRight),
            ( '10%', [u'Мужчины', u'Всего проживает в субъекте'], CReportBase.AlignRight),
            ( '10%', [u'', u'Включено в план'], CReportBase.AlignRight),
            ( '10%', [u'', u'Прошли диспансеризацию'], CReportBase.AlignRight),
            ( '10%', [u'Женщины', u'Всего проживает в субъекте'], CReportBase.AlignRight),
            ( '10%', [u'', u'Включено в план'], CReportBase.AlignRight),
            ( '10%', [u'', u'Прошли диспансеризацию'], CReportBase.AlignRight),
            ( '10%', [u'Всего', u'Всего проживает в субъекте'], CReportBase.AlignRight),
            ( '10%', [u'', u'Включено в план'], CReportBase.AlignRight),
            ( '10%', [u'', u'Прошли диспансеризацию'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 1, 3)
        table.mergeCells(0, 8, 1, 3)

        query = selectData(params)

        if query is None:
            return doc

        endDate = params['endDate']
        reportData = self.getReportData(query)
        ages = reportData.keys()
        ages.sort()

        commonAgeStats = self.getCommonAgeStats(ages, endDate)

        result = [0]*9

        for row, age in enumerate(ages):
            data = reportData[age]

            self.addCommonAgeData(data, age, commonAgeStats)

            i = table.addRow()
            table.setText(i, 0, age)
            table.setText(i, 1, row+1)

            for idx, value in enumerate(data):
                column = 2+idx
                table.setText(i, column, value)
                result[idx] += value

        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        for idx, value in enumerate(result):
            column = 2+idx
            table.setText(i, column, value)

        return doc


    def addCommonAgeData(self, data, age, commonAgeStats):
        maleCount = commonAgeStats.get((age, 1), 0)
        femaleCount = commonAgeStats.get((age, 2), 0)
        data[0] = maleCount
        data[3] = femaleCount
        data[6] = maleCount+femaleCount


    def getCommonAgeStats(self, ages, endDate):
        db = QtGui.qApp.db
        result = {}
        if ages:
            date = lastYearDay(endDate)
            strDate = db.formatDate(date)
            tableClient = db.table('Client')
            tableClientAddress = db.table('ClientAddress')
            tableAddress = db.table('Address')
            tableAddressHouse = db.table('AddressHouse')

            clientAddressJoinCond = [tableClientAddress['client_id'].eq(tableClient['id']),
                                     'ClientAddress.`id`=(SELECT MAX(CA.`id`) FROM ClientAddress AS CA WHERE CA.`client_id`=ClientAddress.`client_id`)']

            queryTable = tableClient
            queryTable = queryTable.leftJoin(tableClientAddress, clientAddressJoinCond)
            queryTable = queryTable.leftJoin(tableAddress, tableAddress['id'].eq(tableClientAddress['address_id']))
            queryTable = queryTable.leftJoin(tableAddressHouse, tableAddressHouse['id'].eq(tableAddress['house_id']))

            fields = 'age(birthDate, %s) AS clientAge, sex AS clientSex , COUNT(Client.`id`) AS cnt' % strDate

            cond = ['age(birthDate, %s) IN %s' %(strDate, tableClient['id'].decoratedlist(ages)),
                    'SUBSTR(AddressHouse.`KLADRCode`, 1, 2)=\'%s\''%QtGui.qApp.defaultKLADR()[0:2]]

            stmt = db.selectStmtGroupBy(queryTable, fields, cond, 'clientSex, clientAge')

            query = db.query(stmt)
            while query.next():
                record = query.record()
                clientAge = forceInt(record.value('clientAge'))
                clientSex = forceInt(record.value('clientSex'))
                cnt       = forceInt(record.value('cnt'))
                result[(clientAge, clientSex)] = cnt

        return result


