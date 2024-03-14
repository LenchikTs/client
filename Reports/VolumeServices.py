# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui
from PyQt4.QtCore import *
from Reports.Report import *
from Reports.ReportBase import *

from library.Utils import *
from Reports.ReportSetupDialog import CReportSetupDialog


class CVolumeServices(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setPersonVisible(True)
        result.cmbPerson.setVisible(False)
        result.lblPerson.setVisible(False)
        result.chkDetailPerson.setText(u'В разрезе врачей')
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if not endDate or endDate.isNull():
            return None
        db = QtGui.qApp.db
        stmt = u'''SELECT 
  e.id,formatClientName(c1.id) as cli,os.name as osname,CONCAT(p.code,' ',formatPersonName(p.id)) as pers,
        at.code as infis,at.name as name,a.amount as usl,ct.price as price , e.externalId,
  
  case when Event_Payment.typePayment = 0 then 'Наличная оплата' else 'Электронная оплата' end as typePayment,Account_Item.payedSum
   FROM Event e
  LEFT JOIN Action a ON e.id = a.event_id
  LEFT JOIN EventType et ON e.eventType_id = et.id
  LEFT JOIN rbFinance f ON et.finance_id = f.id
  LEFT JOIN ActionType at ON a.actionType_id = at.id
  LEFT JOIN rbService s ON at.nomenclativeService_id = s.id
  LEFT JOIN Contract c ON e.contract_id = c.id
  left JOIN Contract_Tariff ct ON ct.service_id=s.id AND c.id=ct.master_id
  LEFT JOIN Person p ON a.person_id=p.id
  LEFT JOIN OrgStructure os ON p.orgStructure_id=os.id
  LEFT JOIN Client c1 ON e.client_id = c1.id
  left join Account_Item on Account_Item.event_id = e.id and Account_Item.refuseType_id IS NULL
  
left join Event_Payment on e.id = Event_Payment.master_id
left join rbCashOperation co ON Event_Payment.cashOperation_id = co.id and co.code=1 

  WHERE e.execDate BETWEEN %(begDate)s AND %(endDate)s AND f.code=4 
  AND (ct.price IS NOT NULL OR os.name)
  AND a.deleted=0
  AND e.deleted=0
  AND at.deleted=0
  AND ct.deleted=0
  GROUP BY a.id
  ORDER BY c1.lastName,c1.firstName,c1.patrName,e.id
        ''' % {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate),
               }
        db = QtGui.qApp.db
        return db.query(stmt)

    def build(self, params):
        reportRowSize = 6
        reportData = {}
        chkDetailPerson = params.get('detailPerson', False)

        def processQuery(query):
            while query.next():
                record = query.record()
                if chkDetailPerson:
                    osname = forceString(record.value('pers'))
                else:
                    osname = forceString(record.value('osname'))
                cli = forceString(record.value('cli'))
                infis = forceString(record.value('infis'))
                name = forceString(record.value('name'))
                externalId = forceString(record.value('externalId'))
                amount = forceInt(record.value('usl'))
                payedSum = forceDouble(record.value('payedSum'))
                price = forceDouble(record.value('price'))
                pd = amount*price

                key = (osname, cli,   infis,  name, externalId)
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += amount
                reportLine[1] += price
                reportLine[2] += pd
                reportLine[3] += payedSum
        query = self.selectData(params)
        processQuery(query)
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.insertText(self.title())
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'ОБЪЕМ медицинских услуг оказанных пациентам')
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setCharFormat(CReportBase.ReportBody)
     #   cursor.insertText(description)
        cursor.insertBlock()

        tableColumns = [
            ('10%', [u'Услуга', u'Код'], CReportBase.AlignLeft),
            ('20%', ['', u'Наименование'], CReportBase.AlignLeft),
            ('10%', [u'Кол-во услуг'], CReportBase.AlignRight),
            ('10%', [u'Стоимость услуги'], CReportBase.AlignRight),
            ('10%', [u'Общая стоимость услуги'], CReportBase.AlignRight),
            ('10%', [u'Оплачено'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 2)
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 2, 1)

        totalByFin = [0]*reportRowSize
        totalByOs = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        colsShift = 2
        prevFin = None
        prevOs = None

        keys = reportData.keys()
        keys.sort()

        def drawTotal(table,  total,  text):

            row = table.addRow()

            table.setText(row, 1, text + u': кол-во услуг - %s'
                          % (total[0]), CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 2)
            for col in xrange(reportRowSize):
                if col < 4:
                    table.setText(row, col + colsShift, total[col])

        for key in keys:
            osname = key[0]
            cli = key[1]
            infis = key[2]
            name = key[3]
            externalId = key[4]

            reportLine = reportData[key]
            if prevFin is not None and prevFin != cli:
                drawTotal(table,  totalByFin, u'%s итого' % prevFin)
                totalByFin = [0]*reportRowSize

            if prevOs is not None and prevOs != osname:
                drawTotal(table,  totalByOs, u'%s итого' % prevOs)
                totalByOs = [0]*reportRowSize

            if prevOs != osname:
                row = table.addRow()
                table.setText(row, 1, osname, CReportBase.TableHeader, CReportBase.AlignCenter)
                table.mergeCells(row, 0, 1, 6)

            if prevFin != cli:
                row = table.addRow()
                table.setText(row, 0, u'Пациент '+cli + u' Договор ' + externalId, CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 6)

            row = table.addRow()
            table.setText(row, 0, infis)
            table.setText(row, 1, name)
            for col in xrange(reportRowSize):
                if col < 4:
                    table.setText(row, col + colsShift, reportLine[col])
                totalByReport[col] = totalByReport[col] + reportLine[col]
                totalByFin[col] = totalByFin[col] + reportLine[col]
                totalByOs[col] = totalByOs[col] + reportLine[col]
            prevFin = cli
            prevOs = osname
        #total
        drawTotal(table, totalByFin, u'%s итого' % prevFin)
        drawTotal(table, totalByOs, u'%s итого' % prevOs)
        drawTotal(table, totalByReport, u'Итого')
        return doc
