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

from Orgs.Utils import getOrgStructureDescendants
from Reports.Report     import *
from Reports.ReportBase import *

from library.Utils      import *
from Reports.ReportSetupDialog import CReportSetupDialog
  
    
class CRepService(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Результаты экспорта данных внешних систем')
        self.stattmp1 = ''
        
    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.chkActionClass.setText(u'Группировать по подразделениям')
        result.setPersonVisible(True)
        result.setOrgStructureVisible(True)
        result.setActionTypeVisible(True)
        result.lblActionTypeClass.setVisible(False)
        result.lblActionType.setVisible(False)
        result.cmbActionTypeClass.setVisible(False)
        result.cmbActionType.setVisible(False)
        result.setEventTypeListVisible(True)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (43, 0, 1, 10):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectDatatmp(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        db = QtGui.qApp.db
        stmt = u'''SELECT MAX(ee.id) AS ss FROM Event_Export ee
        LEFT JOIN Event e ON ee.master_id = e.id
  WHERE ee.system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%") and DATE(e.execDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) AND ee.id IS NOT NULL
  GROUP BY ee.master_id
''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate)
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectCount_Event(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        personId = params.get('personId', None)
        orgStructureId = params.get('orgStructureId', None)
        eventTypeList = params.get('eventTypeList', None)
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and Person.orgStructure_id in (%s)' % (','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        if personId:
            condpersonId = ' and Person.id = %d' % personId
        else:
            condpersonId = ''
        if eventTypeList:
            condEvent = ' and EventType.id in (%s)' % (','.join(map(str, eventTypeList)))
        else:
            condEvent = ''
        db = QtGui.qApp.db
        stmt = u'''SELECT count(distinct Event.id)                         AS event_id
       
FROM Event
INNER JOIN EventType            ON EventType.id = Event.eventType_id AND EventType.usishCode != ''
INNER JOIN rbMedicalAidType     ON rbMedicalAidType.id = EventType.medicalAidType_id
LEFT  JOIN Contract             ON Contract.id = Event.contract_id
LEFT  JOIN rbFinance            ON rbFinance.id = Contract.finance_id
LEFT  JOIN Diagnostic           ON Diagnostic.id = getEventDiagnostic(Event.id)
LEFT  JOIN rbDiagnosticResult   ON rbDiagnosticResult.id = Diagnostic.result_id
LEFT  JOIN mes.MES              AS MES         ON MES.id = Event.mes_id
LEFT  JOIN mes.mrbMESGroup      AS mrbMESGroup ON mrbMESGroup.id = MES.group_id
LEFT  JOIN Event_Export as eExport ON eExport.id = (select max(Event_Export.id) from Event_Export where master_id = Event.id AND system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%"))
LEFT  JOIN Event AS PrevEvent   ON PrevEvent.id = Event.prevEvent_id AND PrevEvent.deleted = 0
left join Person on Person.id = Event.execPerson_id
left join OrgStructure as PersonOrgStructure on PersonOrgStructure.id = Person.orgStructure_id
left join OrgStructure as Parent1 on Parent1.id = PersonOrgStructure.parent_id
left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
WHERE Event.deleted = 0
  AND Event.org_id = %(vOrgId)s
  AND Event.setDate != 0
  AND EventType.exportIEMK = 1
  AND Event.setDate IS NOT NULL
  AND DATE(Event.execDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
  AND rbDiagnosticResult.id IS NOT NULL 
   %(orgStructureList)s  %(condpersonId)s %(condEvent)s
  AND IF( rbMedicalAidType.code IN ('1', '2', '3', '7') , -- стационар
          (SELECT if(EXISTS(SELECT * FROM Action a 
                  LEFT JOIN ActionType at ON a.actionType_id = at.id
                   WHERE a.deleted=0 AND at.deleted=0 and a.event_id=Event.id AND at.flatCode in ('moving')) AND 
                  EXISTS(SELECT * FROM Action a 
                  LEFT JOIN ActionType at ON a.actionType_id = at.id
                   WHERE a.deleted=0 AND at.deleted=0 and a.event_id=Event.id AND at.flatCode in ('leaved')),1,0)),     -- проверка на наличие в событии или движения или выписки
          TRUE --          ( mrbMESGroup.id IS NULL OR  mrbMESGroup.code != 'ДиспанС' )   -- это не диспансеризация
        )
''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate),
       'condpersonId': condpersonId,
       'orgStructureList': orgStructureList,
       'vOrgId': QtGui.qApp.currentOrgId(),
       'condEvent': condEvent
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        personId = params.get('personId', None)
        orgStructureId = params.get('orgStructureId', None)
        eventTypeList = params.get('eventTypeList', None)
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and p.orgStructure_id in (%s)' % (','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        if personId:
            condpersonId = ' and p.id = %d' % personId
        else:
            condpersonId = ''
        if not endDate or endDate.isNull():
            return None
        querytmp = self.selectDatatmp(params)
        while querytmp.next():
            record = querytmp.record()
            stattmp = forceString(record.value('ss'))
            if stattmp:
                if self.stattmp1 != '':
                    self.stattmp1 = self.stattmp1 + ',' + stattmp
                else:
                    self.stattmp1 = self.stattmp1 + stattmp
        if self.stattmp1:
            err = ' AND ee.id IN(%s) ' % self.stattmp1
        else:
            err = ''
        if eventTypeList:
            condEvent = ' and e.eventType_id in (%s)' % (','.join(map(str, eventTypeList)))
        else:
            condEvent = ''
        db = QtGui.qApp.db
        stmt = u'''SELECT   
    SUM(CASE WHEN q.stat>0 THEN 1 ELSE 0 END) AS stat1,
    SUM(CASE WHEN q.stat=0 THEN 1 ELSE 0 END) AS stat2,
    q.sysev AS sysev
    FROM(
    SELECT ee.master_id,
    sum(CASE WHEN ee.success>0 THEN 1 ELSE 0 END) AS stat,
    sum(CASE WHEN ee.success=0 THEN 1 ELSE 0 END) AS stat0,
    ee.system_id AS sysev
    FROM Event_Export ee
    left join Event e on e.id=ee.master_id
    left join Person p on p.id=e.execPerson_id
    WHERE  ee.system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%") AND ee.id IS NOT NULL and DATE(e.execDate) 
    BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) %(condpersonId)s %(stattmp1)s %(orgStructureList)s %(condEvent)s
    GROUP BY ee.master_id)q
''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate),
       'condpersonId': condpersonId,
       'orgStructureList': orgStructureList,
       'stattmp1': err,
       'condEvent': condEvent
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectOMSData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if not endDate or endDate.isNull():
            return None
        if self.stattmp1:
            err = ' AND ee.id IN(%s) ' % self.stattmp1
        else:
            err = ''
        db = QtGui.qApp.db
        stmt = u'''SELECT sum(CASE WHEN mm.stat1>0 THEN 1 ELSE 0 END) as st1,sum(CASE WHEN mm.stat2>0 THEN 1 ELSE 0 END) as st2,mm.oo as infis, identi from ( SELECT   
    SUM(CASE WHEN q.stat>0 THEN 1 ELSE 0 END) AS stat1,
    SUM(CASE WHEN q.stat=0 THEN 1 ELSE 0 END) AS stat2,
    q.sysev AS sysev,IF(q.orgInfis!='',q.orgInfis,q.infisCode) AS oo,IF(identi!='',identi,orgident) AS identi
    FROM(
    SELECT ee.master_id,
    sum(CASE WHEN ee.success>0 THEN 1 ELSE 0 END) AS stat,
    sum(CASE WHEN ee.success=0 THEN 1 ELSE 0 END) AS stat0,
    ee.system_id AS sysev,IF(PersonOrgStructure_osi.id, CONCAT(PersonOrgStructure.infisCode,' ',PersonOrgStructure.name),
                        IF(Parent1_osi.id, CONCAT(Parent1.infisCode,' ',Parent1.name),
                          IF(Parent2_osi.id, CONCAT(Parent2.infisCode,' ',Parent2.name),
                            IF(Parent3_osi.id, CONCAT(Parent3.infisCode,' ',Parent3.name),
                              IF(Parent4_osi.id, CONCAT(Parent4.infisCode,' ',Parent4.name), CONCAT(Parent5.infisCode,' ',Parent5.name)))))) as orgInfis,o.infisCode,
            IF(PersonOrgStructure_osi.id, PersonOrgStructure_osi.value,
                        IF(Parent1_osi.id, Parent1_osi.value,
                          IF(Parent2_osi.id, Parent2_osi.value,
                            IF(Parent3_osi.id, Parent3_osi.value,
                              IF(Parent4_osi.id, Parent4_osi.value, Parent5_osi.value))))) as identi, oo.value AS orgident
    FROM Event_Export ee
    left join Event e on e.id=ee.master_id
    left join Person p on p.id=e.execPerson_id
    left join OrgStructure as PersonOrgStructure on PersonOrgStructure.id = p.orgStructure_id
      LEFT JOIN OrgStructure_Identification PersonOrgStructure_osi ON PersonOrgStructure.id = PersonOrgStructure_osi.master_id AND PersonOrgStructure_osi.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
left join OrgStructure as Parent1 on Parent1.id = PersonOrgStructure.parent_id
      LEFT JOIN OrgStructure_Identification Parent1_osi ON Parent1.id = Parent1_osi.master_id AND Parent1_osi.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
      LEFT JOIN OrgStructure_Identification Parent2_osi ON Parent2.id = Parent2_osi.master_id AND Parent2_osi.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
      LEFT JOIN OrgStructure_Identification Parent3_osi ON Parent3.id = Parent3_osi.master_id AND Parent3_osi.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
      LEFT JOIN OrgStructure_Identification Parent4_osi ON Parent4.id = Parent4_osi.master_id AND Parent4_osi.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
      LEFT JOIN OrgStructure_Identification Parent5_osi ON Parent5.id = Parent5_osi.master_id AND Parent5_osi.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
LEFT JOIN Organisation o ON e.org_id = o.id
LEFT JOIN Organisation_Identification oo ON o.id = oo.master_id AND oo.deleted=0 AND oo.system_id = (SELECT id FROM rbAccountingSystem WHERE code = 'org.n3')
    WHERE  ee.system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%")  AND ee.id IS NOT NULL and DATE(e.execDate)
    BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) %(stattmp1)s
    GROUP BY ee.master_id,orgInfis)q

GROUP BY q.master_id,oo
  ORDER BY oo)mm
  GROUP BY mm.oo ORDER BY infis
''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate),
       'stattmp1': err
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectData2(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if not endDate or endDate.isNull():
            return None
        db = QtGui.qApp.db
        stmt = u'''   SELECT  
    SUM(CASE WHEN q.stat3>0 THEN 1 ELSE 0 END) AS stat3,
    SUM(CASE WHEN q.stat3=0 THEN 1 ELSE 0 END) AS stat4,
    q.syscl  
    from (SELECT 
    sum(CASE WHEN ce.success>0 THEN 1 ELSE 0 END) AS stat3,
    sum(CASE WHEN ce.success=0 THEN 1 ELSE 0 END) AS stat4,
    ce.system_id AS syscl
    FROM Client_Export ce
    WHERE ce.system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%")  and DATE(ce.dateTime) 
    BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
    GROUP BY ce.master_id)q
''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate),
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectData3(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        chkDetailPerson = params.get('detailPerson', False)
        orgStructureId = params.get('orgStructureId', None)
        eventTypeList = params.get('eventTypeList', None)
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and p.orgStructure_id in (%s)' % (','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        if chkDetailPerson:
            order = 'p.lastName,p.firstName,p.patrName'
        else:
            order = 'c.lastName,c.firstName,c.patrName'
        personId = params.get('personId', None)
        if personId:
            condpersonId = ' and p.id = %d' % personId
        else:
            condpersonId = ''
        if not endDate or endDate.isNull():
            return None
        if self.stattmp1:
            err = ' AND ee.id IN(%s) ' % self.stattmp1
        else:
            err = ''
        if eventTypeList:
            condEvent = ' and et.id in (%s)' % (','.join(map(str, eventTypeList)))
        else:
            condEvent = ''
        db = QtGui.qApp.db
        stmt = u'''   
    SELECT e.id as event_id,c.id AS cl,c.lastName as las,c.firstName AS fir,
  c.patrName AS pat,c.birthDate AS hap,
    et.name AS tip,DATE(e.setDate) as setdat, DATE(e.execDate) as execdat,
  pp.note AS osh,q.system_id AS sys,
  concat(p.code, ' ' , p.lastName,' ',p.firstName,' ',p.patrName, ' - ', s.name) as pers
    FROM (SELECT ee.id as ss,
    (CASE WHEN ee.success>0 THEN 1 ELSE 0 END) AS stat,
    (CASE WHEN ee.success=0 THEN 1 ELSE 0 END) AS stat1,
    ee.note,ee.master_id,ee.system_id
  FROM Event_Export ee
  LEFT JOIN Event e1 ON ee.master_id = e1.id
  WHERE ee.system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%")  AND ee.id IS NOT NULL and DATE(e1.execDate) 
    BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) %(stattmp1)s)q
    inner JOIN Event e ON e.id=q.master_id
    inner JOIN Person p on e.execPerson_id=p.id
    inner JOIN rbSpeciality s ON p.speciality_id = s.id
    inner JOIN Client c ON e.client_id = c.id
    inner JOIN EventType et ON e.eventType_id = et.id
    inner join Event_Export pp on pp.id=q.ss
    WHERE q.stat=0 %(condpersonId)s %(orgStructureList)s %(condEvent)s
    ORDER BY %(order)s
    limit 1000

''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate),
       'condpersonId': condpersonId,
       'order': order,
       'orgStructureList': orgStructureList,
       'stattmp1': err,
       'condEvent': condEvent
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def select_Event_NOT_EXPORT(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        eventTypeList = params.get('eventTypeList', None)
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and Person.orgStructure_id in (%s)' % (','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        personId = params.get('personId', None)
        if personId:
            condpersonId = ' and Person.id = %d' % personId
        else:
            condpersonId = ''
        if not endDate or endDate.isNull():
            return None

        if self.stattmp1:
            err = ' eExport.master_id = Event.id AND eExport.id IN(%s) ' % self.stattmp1
        else:
            err = u' eExport.id = (select max(Event_Export.id) from Event_Export where master_id = Event.id AND system_id in (SELECT id FROM rbExternalSystem WHERE code LIKE "%%N3.РЕГИСЗ.ИЭМК%%"))'
        if eventTypeList:
            condEvent = ' and EventType.id in (%s)' % (','.join(map(str, eventTypeList)))
        else:
            condEvent = ''
        db = QtGui.qApp.db
        stmt = u'''   
  SELECT Event.id as event_id,
      c.id AS cl,c.lastName as las,c.firstName AS fir,
  c.patrName AS pat,c.birthDate AS hap,
    EventType.name AS tip,DATE(Event.setDate) as setdat, DATE(Event.execDate) as execdat
       
FROM Event
INNER JOIN EventType            ON EventType.id = Event.eventType_id AND EventType.usishCode != ''
INNER JOIN rbMedicalAidType     ON rbMedicalAidType.id = EventType.medicalAidType_id
      LEFT JOIN Client c ON Event.client_id = c.id
LEFT  JOIN Contract             ON Contract.id = Event.contract_id
LEFT  JOIN rbFinance            ON rbFinance.id = Contract.finance_id
LEFT  JOIN Diagnostic           ON Diagnostic.id = getEventDiagnostic(Event.id)
LEFT  JOIN rbDiagnosticResult   ON rbDiagnosticResult.id = Diagnostic.result_id
LEFT  JOIN mes.MES              AS MES         ON MES.id = Event.mes_id
LEFT  JOIN mes.mrbMESGroup      AS mrbMESGroup ON mrbMESGroup.id = MES.group_id
LEFT  JOIN Event_Export as eExport ON %(stattmp1)s
LEFT  JOIN Event AS PrevEvent   ON PrevEvent.id = Event.prevEvent_id AND PrevEvent.deleted = 0
left join Person on Person.id = Event.execPerson_id
left join OrgStructure as PersonOrgStructure on PersonOrgStructure.id = Person.orgStructure_id
left join OrgStructure as Parent1 on Parent1.id = PersonOrgStructure.parent_id
left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id

WHERE Event.deleted = 0
  AND Event.org_id = %(vOrgId)s
  AND Event.setDate != 0
  AND EventType.exportIEMK = 1
  AND Event.setDate IS NOT NULL
  AND DATE(Event.execDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
  AND rbDiagnosticResult.id IS NOT NULL 
   %(orgStructureList)s  %(condpersonId)s %(condEvent)s
  AND IF( rbMedicalAidType.code IN ('1', '2', '3', '7') , -- стационар
          (SELECT if(EXISTS(SELECT * FROM Action a 
                  LEFT JOIN ActionType at ON a.actionType_id = at.id
                   WHERE a.deleted=0 AND at.deleted=0 and a.event_id=Event.id AND at.flatCode in ('moving')) AND 
                  EXISTS(SELECT * FROM Action a 
                  LEFT JOIN ActionType at ON a.actionType_id = at.id
                   WHERE a.deleted=0 AND at.deleted=0 and a.event_id=Event.id AND at.flatCode in ('leaved')),1,0)),     -- проверка на наличие в событии или движения или выписки
          TRUE --          ( mrbMESGroup.id IS NULL OR  mrbMESGroup.code != 'ДиспанС' )   -- это не диспансеризация
        )
        
   AND eExport.id IS NULL
limit 1000
''' % {'begDate': db.formatDate(begDate),
       'endDate': db.formatDate(endDate),
       'condpersonId': condpersonId,
       'vOrgId': QtGui.qApp.currentOrgId(),
       'orgStructureList': orgStructureList,
       'stattmp1': err,
       'condEvent': condEvent
       }
        db = QtGui.qApp.db
        return db.query(stmt)

    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        chkDetailPerson = params.get('detailPerson', False)
        personId = params.get('personId', None)
        orgStructureId = params.get('orgStructureId', None)
        eventTypeList = params.get('eventTypeList', None)
        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if personId:
            rows.append(u'по врачу: %s ' % forceString(db.translate('vrbPerson', 'id', personId, 'name')))

        if chkDetailPerson:
            rows.append(u'детализация по врачам: %s ' % forceString(db.translate('vrbPerson', 'id', personId, 'name')))

        if orgStructureId:
            rows.append(u'детализация по отделению: %s ' % forceString(db.translate('OrgStructure', 'id', orgStructureId, 'name')))

        if eventTypeList:
            tableET = db.table('EventType')
            records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(eventTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            rows.append(u'Тип обращения:  %s'%(u','.join(name for name in nameList if name)))
        
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows

    def build(self, params):
        chkDetailPerson = params.get('detailPerson', False)
        chkActionTypeClass = params.get('chkActionTypeClass', False)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        firstTitle = u"""Колличество ошибок на заданный промежуток времени"""
        secondTitle = u'Типы ошибок. ВНИМАНИЕ отображаются первые 1000 ошибок'
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportTitle)
        # cursor.insertText(firstTitle)
        cursor.insertBlock()
        cursor.insertBlock()
        # рисуем первую табличку
        tableColumns = [
            ('10%',
             [u'Сервис', u'Интегрированная электронная медицинская карта (ИЭМК)', u'Кол-во людей', u'экспортировано'],
             CReportBase.AlignRight),
            ('10%', [u'', u'', u'', u'ошибки экспорта'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'Кол-во событий', u'всего закрытых событий'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'', u'экспортировано'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'', u'ошибки экспорта'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 5)
        table.mergeCells(1, 0, 1, 5)
        table.mergeCells(2, 0, 1, 2)
        table.mergeCells(2, 2, 1, 3)

        query = self.selectData(params)
        while query.next():
            record = query.record()
            stat1 = forceInt(record.value('stat1'))
            stat2 = forceInt(record.value('stat2'))
            row = table.addRow()

            table.setText(row, 3, stat1)
            table.setText(row, 4, stat2)

        query = self.selectCount_Event(params)
        while query.next():
            record = query.record()
            count_event_id = forceInt(record.value('event_id'))

            table.setText(row, 2, count_event_id )

        query = self.selectData2(params)
        while query.next():
            record = query.record()
            stat3 = forceInt(record.value('stat3'))
            stat4 = forceInt(record.value('stat4'))

            table.setText(row, 0, stat3)
            table.setText(row, 1, stat4)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()

        if chkActionTypeClass:
            # рисуем вторую табличку
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setBlockFormat(CReportBase.AlignCenter)
            cursor.insertBlock()
            cursor.insertBlock()
            tableColumns = [
                ('10%', [u'Выгружено успешно случаев'], CReportBase.AlignRight),
                ('10%', [u'Ошибок выгрузки'], CReportBase.AlignRight),
                ('25%', [u'Подразделение выгрузки'], CReportBase.AlignRight),
                ('15%', [u'Код'], CReportBase.AlignRight),
            ]

            table = createTable(cursor, tableColumns)
            query = self.selectOMSData(params)
            while query.next():
                record = query.record()
                cl = forceInt(record.value('st1'))
                las = forceString(record.value('st2'))
                fir = forceString(record.value('infis'))
                identi = forceString(record.value('identi'))
                row = table.addRow()

                table.setText(row, 0, cl)
                table.setText(row, 1, las)
                table.setText(row, 2, fir)
                table.setText(row, 3, identi)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            cursor.insertBlock()

        if chkDetailPerson:

            # рисуем вторую табличку
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setBlockFormat(CReportBase.AlignCenter)
            cursor.insertText(secondTitle)
            cursor.insertBlock()
            cursor.insertBlock()
            tableColumns = [
                ('5%', [u'№'], CReportBase.AlignLeft),
                ('5%', [u'Код пациента'], CReportBase.AlignLeft),
                ('10%', [u'Фамилия'], CReportBase.AlignLeft),
                ('10%', [u'Имя'], CReportBase.AlignLeft),
                ('10%', [u'Отчество'], CReportBase.AlignLeft),
                ('10%', [u'Дата рождения'], CReportBase.AlignLeft),
                ('5%', [u'Код карточки'], CReportBase.AlignLeft),
                ('10%', [u'Тип события'], CReportBase.AlignLeft),
                ('15%', [u'Дата начала/окончания'], CReportBase.AlignLeft),
                ('20%', [u'Ошибка'], CReportBase.AlignLeft)
            ]

            table = createTable(cursor, tableColumns)
            query = self.selectData3(params)
            person = None
            num = 0

            while query.next():
                record = query.record()
                iid = forceInt(record.value('id'))
                cl = forceInt(record.value('cl'))
                event_id = forceInt(record.value('event_id'))
                las = forceString(record.value('las'))
                fir = forceString(record.value('fir'))
                pat = forceString(record.value('pat'))
                hap = forceString(record.value('hap'))
                tip = forceString(record.value('tip'))
                setdat = forceDate(record.value('setdat'))
                execdat = forceDate(record.value('execdat'))
                dat = setdat.toString("dd.MM.yyyy") + ' / ' + execdat.toString("dd.MM.yyyy")
                osh = forceString(record.value('osh'))
                pers = forceString(record.value('pers'))

                if person != pers:
                    row = table.addRow()
                    table.setText(row, 1, u'Врач ' + pers, CReportBase.TableHeader, CReportBase.AlignLeft)
                    table.mergeCells(row, 0, 1, 9)
                    num = 1
                else:
                    num += 1

                row = table.addRow()

                table.setText(row, 0, num)
                table.setText(row, 1, cl)
                table.setText(row, 2, las)
                table.setText(row, 3, fir)
                table.setText(row, 4, pat)
                table.setText(row, 5, hap)
                # table.setText(row, 6, event_id)
                table.setHtml(row, 6,
                              u"<a href='event_" + str(event_id) + u"'><span style='color: rgb(FF, FF, FF);'>" + str(
                                  event_id) + "</span></a>")
                table.setText(row, 7, tip)
                table.setText(row, 8, dat)
                table.setText(row, 9, osh)

                person = pers

        else:

            # рисуем вторую табличку
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setBlockFormat(CReportBase.AlignCenter)
            cursor.insertText(secondTitle)
            cursor.insertBlock()
            cursor.insertBlock()
            tableColumns = [
                ('5%', [u'№'], CReportBase.AlignLeft),
                ('5%', [u'Код пациента'], CReportBase.AlignLeft),
                ('10%', [u'Фамилия'], CReportBase.AlignLeft),
                ('10%', [u'Имя'], CReportBase.AlignLeft),
                ('10%', [u'Отчество'], CReportBase.AlignLeft),
                ('10%', [u'Дата рождения'], CReportBase.AlignLeft),
                ('5%', [u'Код карточки'], CReportBase.AlignLeft),
                ('10%', [u'Тип события'], CReportBase.AlignLeft),
                ('15%', [u'Дата начала/окончания'], CReportBase.AlignLeft),
                ('20%', [u'Ошибка'], CReportBase.AlignLeft)
            ]

            table = createTable(cursor, tableColumns)
            query = self.selectData3(params)
            i = 0
            while query.next():
                record = query.record()
                i += 1
                cl = forceInt(record.value('cl'))
                las = forceString(record.value('las'))
                fir = forceString(record.value('fir'))
                pat = forceString(record.value('pat'))
                hap = forceString(record.value('hap'))
                event_id = forceInt(record.value('event_id'))
                tip = forceString(record.value('tip'))
                setdat = forceDate(record.value('setdat'))
                execdat = forceDate(record.value('execdat'))
                dat = setdat.toString("dd.MM.yyyy") + ' / ' + execdat.toString("dd.MM.yyyy")
                osh = forceString(record.value('osh'))
                row = table.addRow()

                table.setText(row, 0, i)
                table.setText(row, 1, cl)
                table.setText(row, 2, las)
                table.setText(row, 3, fir)
                table.setText(row, 4, pat)
                table.setText(row, 5, hap)
                # table.setText(row, 6, event_id)
                table.setHtml(row, 6, u"<a href='event_" + str(event_id) + u"'><span style='color: rgb(FF, FF, FF);'>" + str(event_id) + "</span></a>")
                table.setText(row, 7, tip)
                table.setText(row, 8, dat)
                table.setText(row, 9, osh)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'Список событий, которые не были экспортированы. Выводятся первые 1000 событий')
        cursor.insertBlock()
        cursor.insertBlock()
        tableColumns = [
            ('5%', [u'№'], CReportBase.AlignLeft),
            ('5%', [u'Код пациента'], CReportBase.AlignLeft),
            ('10%', [u'Фамилия'], CReportBase.AlignLeft),
            ('10%', [u'Имя'], CReportBase.AlignLeft),
            ('10%', [u'Отчество'], CReportBase.AlignLeft),
            ('10%', [u'Дата рождения'], CReportBase.AlignLeft),
            ('5%', [u'Код карточки'], CReportBase.AlignLeft),
            ('10%', [u'Тип события'], CReportBase.AlignLeft),
            ('15%', [u'Дата начала/окончания'], CReportBase.AlignLeft)
        ]

        table = createTable(cursor, tableColumns)
        query = self.select_Event_NOT_EXPORT(params)
        i = 0
        while query.next():
            record = query.record()
            i += 1
            cl = forceInt(record.value('cl'))
            las = forceString(record.value('las'))
            fir = forceString(record.value('fir'))
            pat = forceString(record.value('pat'))
            hap = forceString(record.value('hap'))
            event_id = forceInt(record.value('event_id'))
            tip = forceString(record.value('tip'))
            setdat = forceDate(record.value('setdat'))
            execdat = forceDate(record.value('execdat'))
            dat = setdat.toString("dd.MM.yyyy") + ' / ' + execdat.toString("dd.MM.yyyy")
            row = table.addRow()

            table.setText(row, 0, i)
            table.setText(row, 1, cl)
            table.setText(row, 2, las)
            table.setText(row, 3, fir)
            table.setText(row, 4, pat)
            table.setText(row, 5, hap)
            # table.setHtml(row, 6, u"<a href='event_"+str(event_id)+u"'><span style='text-decoration: none;  color: rgb(FF, FF, FF);'>"+str(event_id)+"</span></a>")
            table.setHtml(row, 6, u"<a href='event_"+str(event_id)+u"'><span style='color: rgb(FF, FF, FF);'>"+str(event_id)+"</span></a>")
            table.setText(row, 7, tip)
            table.setText(row, 8, dat)

        return doc
