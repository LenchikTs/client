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
from PyQt4.QtCore import QDate, QDateTime
from Reports.Report import CReport
from Reports.Utils import dateRangeAsStr
from Reports.ReportBase import CReportBase, createTable
from ReportSetupDialog import CReportSetupDialog
from Orgs.Utils import getOrgStructurePersonIdList, getOrgStructureFullName
from library.Utils import forceString, forceDate, forceInt
from PyQt4.QtCore import *
    
class CSanAviacExport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Результаты экспорта данных в сервис "Сан-авиация"')

    def getSetupDialog(self, parent):
        result = CFinReestrSetupDialog(parent)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer=result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition=result.gridLayout.getItemPosition(i)
                if itemposition!=(29, 0, 1, 1)and itemposition!=(8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result


    def selectData(self, params): 
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        db = QtGui.qApp.db
        stmt = u'''select 
            cast(a.begDate as date) dateTrans,
            cast(aee.`dateTime` as date) exportdate,
            count(case when aee.success = 1 then aee.id else null end) succescount,
            count(case when aee.success = 0 then aee.id else null end) errorcount
        from Event e 
            inner join `Action` a on a.event_id = e.id and a.deleted = 0 and e.deleted = 0 
            inner join ActionType actp on actp.id = a.actionType_id and actp.serviceType = 9 and actp.deleted = 0
            inner join EventType et on et.id = e.eventType_id and et.deleted=0 and et.code not in('hospDir','egpuDisp','plng') and et.context not in('relatedAction','inspection')
            inner join Action_Export aee on aee.master_id = a.id
        	inner join rbExternalSystem es ON aee.system_id = es.id AND es.code='SanAviaService'
            WHERE a.begDate BETWEEN %(begDate)s AND %(endDate)s   
        group by cast(a.begDate as date), cast(aee.`dateTime` as date)
        LIMIT 500
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate))
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectDataDetail(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        db = QtGui.qApp.db
        stmt = u'''
            select 
            c.id clientid,
            CONCAT_WS(' ', c.lastName, c.firstName, c.patrName) fio, 
            c.birthDate birthDate,
            'не экспортирована' exporterror,
            e.id cardid
from  Action a
  LEFT JOIN Action_Export aee ON aee.master_id = a.id
  LEFT JOIN ActionType at ON a.actionType_id = at.id AND at.serviceType=9
  LEFT JOIN Event e ON a.event_id = e.id
  LEFT JOIN Client c ON e.client_id = c.id
  LEFT JOIN EventType et ON e.eventType_id = et.id
  LEFT JOIN rbExternalSystem es ON aee.system_id = es.id AND es.code='SanAviaService'
  WHERE e.deleted = 0
  AND a.deleted = 0
  AND at.deleted = 0
  AND et.deleted=0 and et.code NOT IN ('hospDir','egpuDisp','plng') and et.context NOT IN ('relatedAction','inspection')
  AND e.execDate IS NULL AND a.endDate IS NULL AND a.status=0
  AND a.begDate BETWEEN %(begDate)s AND %(endDate)s AND aee.id IS NULL
union all
select 
            c.id clientid,
            CONCAT_WS(' ', c.lastName, c.firstName, c.patrName) fio, 
            c.birthDate birthDate,
            aee.note exporterror,
            e.id cardid
from  Action a
  LEFT JOIN Action_Export aee ON aee.master_id = a.id
  LEFT JOIN ActionType at ON a.actionType_id = at.id
  LEFT JOIN Event e ON a.event_id = e.id
  LEFT JOIN Client c ON e.client_id = c.id
  LEFT JOIN EventType et ON e.eventType_id = et.id
  LEFT JOIN rbExternalSystem es ON aee.system_id = es.id 
  WHERE e.deleted = 0
  AND a.deleted = 0
  AND at.deleted = 0
  AND et.deleted=0 and et.code NOT IN ('hospDir','egpuDisp','plng') and et.context NOT IN ('relatedAction','inspection')
  AND at.serviceType=9 AND es.code='SanAviaService' AND aee.success=0
  AND a.begDate BETWEEN %(begDate)s AND %(endDate)s limit 500;
        ''' % dict(begDate=db.formatDate(begDate),
                   endDate=db.formatDate(endDate))
        db = QtGui.qApp.db
        return db.query(stmt)

    def getDescription(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())

        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()

        tableColumns = [
            ('35%',  [ u'Дата перевода в ОРиА'], CReportBase.AlignLeft),
            ('35%',  [ u'Дата экспорта'], CReportBase.AlignLeft),
            ('15%',  [ u'Экспортировано успешно'], CReportBase.AlignRight),
            ('15%',  [ u'Экспортировано с ошибками'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        query = self.selectData(params)
        while query.next():
            record = query.record()
            dateTrans = forceString(record.value('dateTrans'))
            exportdate = forceString(record.value('exportdate'))
            succescount = forceString(record.value('succescount'))
            errorcount = forceString(record.value('errorcount'))

            row = table.addRow()
            
            
            table.setText(row, 0, dateTrans)
            table.setText(row, 1, exportdate)
            table.setText(row, 2, succescount)
            table.setText(row, 3, errorcount)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'Пациенты из ОРиА не экспортированы в Web-сервис или экспортированы с ошибками')
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('5%', [u'№ п/п'], CReportBase.AlignCenter),
            ('10%', [u'Код пациента'], CReportBase.AlignRight),
            ('20%', [u'ФИО пациента'], CReportBase.AlignLeft),
            ('10%', [u'Дата рождения'], CReportBase.AlignCenter),
            ('10%', [u'Код карточки'], CReportBase.AlignRight),
            ('45%', [u'Ошибки экспорта'], CReportBase.AlignLeft)
        ]

        table = createTable(cursor, tableColumns)
        query = self.selectDataDetail(params)
        countRec = 1
        while query.next():
            record = query.record()
            num = forceString(countRec)
            clientid = forceString(record.value('clientid'))
            fio = forceString(record.value('fio'))
            birthDate = forceDate(record.value('birthDate')).toString('dd.MM.yyyy')
            cardid = forceString(record.value('cardid'))
            exporterror = forceString(record.value('exporterror'))

            row = table.addRow()

            table.setText(row, 0, num)
            table.setText(row, 1, clientid)
            table.setText(row, 2, fio)
            table.setText(row, 3, birthDate)
            table.setText(row, 4, cardid)
            table.setText(row, 5, exporterror)

            countRec = countRec + 1

        return doc

class CFinReestrSetupDialog(CReportSetupDialog):
    def __init__(self, parent=None):
        CReportSetupDialog.__init__(self, parent)
        self.setEventTypeVisible(False)
        self.setOnlyPermanentAttachVisible(False)
        self.chkDetailPerson.setVisible(False)
        self.setOrgStructureVisible(False)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        CReportSetupDialog.setParams(self, params)

    def params(self):
        result = CReportSetupDialog.params(self)
        return result

