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
from Reports.Report     import *
from Reports.ReportBase import *
from Orgs.Utils import getOrgStructurePersonIdList
from library.Utils      import *
    
class CRepPlatUsl(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Ведомость услуг учета врачебных посещений')
        
    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(True)
        result.setOnlyPermanentAttachVisible(False)
        result.setFinanceVisible(True)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setPersonVisible(True)
        result.chkDetailPerson.setVisible(False)
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
        orgStructureId = params.get('orgStructureId', None)
        financeId = params.get('financeId', None)
        personId = params.get('personId', None)
        eventTypeId = params.get('eventTypeId', None)
        db = QtGui.qApp.db
        if personId:
            condpersonId = ' and e.execPerson_id = %d' % personId
        else:
            condpersonId = ''
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND e.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        condOrgStructure = u''
       #условие по типу финансирования
        if financeId:
            condFinanceId = ' and et.finance_id = %d' % financeId
        else:
            condFinanceId = ''
        #условие по типу события
        if eventTypeId:
            condEventTypeId = ' and et.id = %d' % eventTypeId
        else:
            condEventTypeId = ''
        db = QtGui.qApp.db
        stmt2 = u''' DROP TEMPORARY TABLE IF EXISTS tmp_days;
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_days(DateDay date);
CALL DaysPeriod (DATE(%(begDate)s),DATE(%(endDate)s));''' % dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate))
        db.query(stmt2)            
        
        stmt = u'''
SELECT DAY(IFNULL(e.execDate,td.DateDay)) AS dat,DATE(IFNULL(e.execDate,td.DateDay)) AS dat2
  , SUM(case when isClientVillager(c.id)=0 then 1 else 0 end) AS gor
  , SUM(case when isClientVillager(c.id)=1 then 1 else 0 end) AS sel
  , count(per.cnt) AS ist
  , count(cn.cnt) AS per
  , CONCAT(count(per.cnt), ' / ',count(cn.cnt)) AS perv
  , count(vtor.cnt) AS vt
FROM tmp_days td
  LEFT JOIN Event e ON e.execDate = td.DateDay AND e.deleted=0 %(condpersonId)s
  AND DATE(e.execDate) 
BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
   %(condOrgStructure)s 
  LEFT JOIN EventType et ON et.id = e.eventType_id %(condEventTypeId)s %(condFinanceId)s
  LEFT JOIN Client c ON e.client_id = c.id AND c.deleted=0 and et.id is not null
  left join Diagnosis d on d.id = getEventDiagnosis(e.id)
  left JOIN (SELECT count(e2.id) cnt, client_id FROM Event e2 WHERE e2.client_id IS NOT NULL GROUP BY client_id HAVING cnt=1) per ON per.client_id=c.id
  left JOIN (SELECT count(e2.id) cnt, client_id FROM Event e2 WHERE DATE(e2.execDate) 
BETWEEN DATE(CONCAT(YEAR(DATE(%(begDate)s)),'-01-01')) AND DATE(CONCAT(YEAR(DATE(%(endDate)s)),'-12-31')) GROUP BY client_id HAVING cnt=1) cn ON cn.client_id=c.id 
  LEFT JOIN (SELECT count(e2.id) cnt, client_id FROM Event e2 WHERE DATE(e2.execDate) 
BETWEEN DATE(CONCAT(YEAR(DATE(%(begDate)s)),'-01-01')) AND DATE(CONCAT(YEAR(DATE(%(endDate)s)),'-12-31')) AND e2.client_id IS NOT NULL GROUP BY client_id HAVING cnt>1) vtor ON vtor.client_id=c.id 
GROUP BY dat,dat2
ORDER BY dat2;
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate),
                    condOrgStructure=condOrgStructure, 
                    condEventTypeId=condEventTypeId, 
                    condFinanceId=condFinanceId, 
                    condpersonId=condpersonId
                    )
        
        return db.query(stmt) 
        
        
    def selectData1(self, params): 
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        financeId = params.get('financeId', None)
        personId = params.get('personId', None)
        eventTypeId = params.get('eventTypeId', None)
        
        db = QtGui.qApp.db
        if personId:
            condpersonId = ' and e.execPerson_id = %d' % personId
        else:
            condpersonId = ''
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND e.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND e.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        #условие по типу финансирования
        if financeId:
            condFinanceId = ' and et.finance_id = %d' % financeId
        else:
            condFinanceId = ''
        #условие по типу события
        if eventTypeId:
            condEventTypeId = ' and et.id = %d' % eventTypeId
        else:
            condEventTypeId = ''
        stmt = u'''SELECT SUM(case when isClientVillager(c.id)=0 then 1 else 0 end) AS gor,
  SUM(case when isClientVillager(c.id)=1 then 1 else 0 end) AS sel,count(per.cnt) AS ist,count(cn.cnt) AS per,
  CONCAT(count(per.cnt),' / ',count(cn.cnt)) AS perv,
 count(vtor.cnt) AS vt
  FROM Event e
  LEFT JOIN EventType et ON et.id = e.eventType_id
  LEFT JOIN Client c ON e.client_id = c.id
  left join Diagnosis d on d.id = getEventDiagnosis(e.id)
  left JOIN (SELECT count(e2.id) cnt, client_id FROM Event e2 WHERE e2.client_id IS NOT NULL GROUP BY client_id HAVING cnt=1) per ON per.client_id=c.id
  left JOIN (SELECT count(e2.id) cnt, client_id FROM Event e2 WHERE DATE(e2.execDate) 
BETWEEN DATE(CONCAT(YEAR(DATE(%(begDate)s)),'-01-01')) AND DATE(CONCAT(YEAR(DATE(%(endDate)s)),'-12-31')) GROUP BY client_id HAVING cnt=1) cn ON cn.client_id=c.id 
  LEFT JOIN (SELECT count(e2.id) cnt, client_id FROM Event e2 WHERE DATE(e2.execDate) 
BETWEEN DATE(CONCAT(YEAR(DATE(%(begDate)s)),'-01-01')) AND DATE(CONCAT(YEAR(DATE(%(endDate)s)),'-12-31')) AND e2.client_id IS NOT NULL GROUP BY client_id HAVING cnt>1) vtor ON vtor.client_id=c.id 
  WHERE e.deleted=0 AND c.deleted=0 %(condEventTypeId)s %(condFinanceId)s %(condpersonId)s
  and DATE(e.execDate) 
BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
%(condOrgStructure)s
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate),
                    condOrgStructure=condOrgStructure, 
                    condEventTypeId=condEventTypeId, 
                    condFinanceId=condFinanceId, 
                    condpersonId=condpersonId
                    )
        db = QtGui.qApp.db
        return db.query(stmt) 
       
    def build(self, params):
        query = self.selectData(params)
        query.first()
        
        
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        
        #рисуем третью табличку
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertBlock()
        tableColumns = [
            ('20%',  [ u'Итого',u'Всего'], CReportBase.AlignLeft),
            ('20%',  [ '',u'Краевые(город Краснодар и города края)'], CReportBase.AlignRight),
            ('20%',  [ '',u'Сельские'], CReportBase.AlignRight),
            ('20%',  [ '',u'Истин/первичные'], CReportBase.AlignRight),
            ('20%',  [ '',u'Вторичных'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 5)
        query = self.selectData1(params)
        while query.next():
            record = query.record()
            gor = forceInt(record.value('gor'))
            sel = forceInt(record.value('sel'))
            ist = forceInt(record.value('ist'))
            per = forceInt(record.value('per'))
            perv = forceString(record.value('perv'))
            vt = forceInt(record.value('vt'))
            row = table.addRow()
            table.setText(row, 0, ist+per+vt)
            table.setText(row, 1, gor)
            table.setText(row, 2, sel)
            table.setText(row, 3, perv)
            table.setText(row, 4, vt)
        
        
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        
        
        #рисуем первую табличку
        tableColumns = [
            ('15%',  [ u'№'], CReportBase.AlignLeft),
            ('15%',  [ u'Число посещений в поликлиннике',u'Всего'], CReportBase.AlignRight),
            ('15%',  [ '',u'Краевые (город Краснодар и города края)'], CReportBase.AlignRight),
            ('15%',  [ '',u'Сельские'], CReportBase.AlignRight),
            ('25%',  [ '',u'Истин/первичные'], CReportBase.AlignRight),
            ('15%',  [ '',u'Вторичных'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 1, 1, 6)
        table.mergeCells(0, 0, 2, 1)
        query = self.selectData(params)
        while query.next():
            record = query.record()
            dat = forceInt(record.value('dat'))
            gor = forceInt(record.value('gor'))
            sel = forceInt(record.value('sel'))
            ist = forceInt(record.value('ist'))
            per = forceInt(record.value('per'))
            perv = forceString(record.value('perv'))
            vt = forceInt(record.value('vt'))
            row = table.addRow()
            table.setText(row, 0, dat)
            table.setText(row, 1, ist+per+vt)
            table.setText(row, 2, gor)
            table.setText(row, 3, sel)
            table.setText(row, 4, perv)
            table.setText(row, 5, vt)
        
        
        return doc
