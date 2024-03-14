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

from library.Utils      import *
from EconomicAnalisysSetupDialog import *


class CReportSummaryStomPos(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Основные показатели по стоматологической помощи')

    def selectData(self, params):
        stmt=u"""
    select 	
      SUM(isPos) AS pos,
      SUM(isObr) AS obr,
      SUM(isProf) AS prof,
			round(sum(q.uet),2) as uet, 
			round(sum(q.sum),2) as sum
    from (select Event.id as event_id,
      isPos(rbService.infis, mt.regionalCode, ifnull(Account_Item.price, ct.price)) as isPos,
      IF(rbService.name like 'Обращение%%', 1, 0) AS isObr,
      IF(rbService.infis LIKE 'B04%%', 1, 0) as isProf,
      IFNULL(Account_Item.uet, vAction.amount * ct.uet) as uet,
		  IFNULL(Account_Item.sum, vAction.amount * ct.price) as sum
    from vAction
    left join Event on Event.id = vAction.event_id
    left join Account_Item on Account_Item.action_id = vAction.id and Account_Item.deleted = 0
    left join Account on Account.id = Account_Item.master_id and Account.deleted = 0
    LEFT JOIN ActionType   ON ActionType.id = vAction.actionType_id
    LEFT JOIN rbService    ON rbService.id = IFNULL(Account_Item.service_id, ActionType.nomenclativeService_id)
    LEFT JOIN EventType       ON EventType.id = Event.eventType_id
    LEFT JOIN Contract ON Contract.id = coalesce(Account.contract_id, vAction.contract_id, Event.contract_id)
    LEFT JOIN Contract_Tariff ct ON ct.master_id = IFNULL(Contract.priceList_id, Contract.id) and ct.service_id = rbService.id and ct.deleted = 0
            and (ct.endDate is not null and DATE(vAction.endDate) between ct.begDate and ct.endDate 
            or DATE(vAction.endDate) >= ct.begDate and ct.endDate is null)
            and ct.tariffType in (2,5)
    LEFT JOIN Person          ON Person.id = vAction.person_id
    LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
    left join OrgStructure on OrgStructure.id = Person.orgStructure_id
    left join Client on Client.id = Event.client_id
    LEFT JOIN rbMedicalAidType mt ON mt.id = ifnull(rbService.medicalAidType_id, EventType.medicalAidType_id)
    left join rbFinance on  rbFinance.id = coalesce(vAction.finance_id, Contract.finance_id)
    LEFT JOIN ClientPolicy on ClientPolicy.id = COALESCE((SELECT MAX(cp2.id) 
                                                      FROM ClientPolicy cp2
                                                      WHERE cp2.client_id = Client.id AND cp2.deleted = 0 AND cp2.begDate =
    (select MAX(cp.begDate) from ClientPolicy cp
            WHERE cp.client_id = Client.id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate <= Event.setDate AND (cp.endDate is NULL OR cp.endDate >= Event.setDate))),
   (SELECT MAX(cp2.id)
            FROM ClientPolicy cp2
            WHERE cp2.client_id = Client.id AND cp2.deleted = 0 AND cp2.begDate =
            (select MAX(cp.begDate)
              from ClientPolicy cp
              WHERE cp.client_id = Client.id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate BETWEEN Event.setDate AND ADDDATE(DATE(Event.execDate), 30)
              )),
  (SELECT MAX(cp2.id)
          FROM ClientPolicy cp2
          WHERE cp2.client_id = Event.relative_id AND cp2.deleted = 0 AND cp2.begDate =
          (select MAX(cp.begDate)
          from ClientPolicy cp
          WHERE cp.client_id = Event.relative_id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate <= Event.setDate AND (cp.endDate is NULL OR cp.endDate >= Event.setDate)
             )))	
    left join Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    LEFT JOIN Organisation AS headInsurer ON headInsurer.id = Insurer.head_id
    LEFT JOIN Organisation AS ContractPayer ON ContractPayer.id = Contract.payer_id
    left join Organisation as Payer on Payer.id =
        IFNULL((select max(id) from Organisation o where o.OGRN = Insurer.OGRN and o.deleted = 0 and o.isInsurer = 1
        and o.OKATO = Insurer.OKATO and Insurer.OKATO = '03000' and o.head_id is null), Contract.payer_id)
    where vAction.deleted = 0 
    and Event.deleted = 0
    and rbService.id is not null
    and ifnull(Account_Item.price, ct.price) is not null
    and DATE(vAction.endDate) >= DATE(Event.setDate)
    and vAction.expose = 1
   and %(cond)s 

      union all
    select Event.id as event_id,
       isPos(rbService.infis, mt.regionalCode, ifnull(Account_Item.price, ct.price)) as isPos,
       IF(rbService.name like 'Обращение%%', 1, 0) as isObr,
       IF(rbService.infis LIKE 'B04%%', 1, 0) as isProf,
       IFNULL(Account_Item.uet, ct.uet) as uet,
		   IFNULL(Account_Item.sum, ct.price) as sum
    from Visit
    left join Event on Event.id = Visit.event_id
     
    left join Account_Item on Account_Item.event_id = Visit.event_id and Account_Item.visit_id = Visit.id 
        and Account_Item.action_id is null and Account_Item.deleted = 0
    left join Account on Account.id = Account_Item.master_id and Account.deleted = 0
    LEFT JOIN rbService  ON rbService.id = IF(Account_Item.service_id IS NULL, Visit.service_id, Account_Item.service_id)
    LEFT JOIN EventType       ON EventType.id = Event.eventType_id
    LEFT JOIN Contract ON Contract.id = coalesce(Account.contract_id, Event.contract_id)
    LEFT JOIN Contract_Tariff ct ON ct.master_id = IFNULL(Contract.priceList_id, Contract.id) 
    and ct.tariffType = 0
        and ct.service_id = rbService.id and ct.deleted = 0
            and (ct.endDate is not null and DATE(Visit.date) between ct.begDate and ct.endDate 
            or DATE(Visit.date) >= ct.begDate and ct.endDate is null) 
    LEFT JOIN Person          ON Person.id = Visit.person_id
    LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
    left join OrgStructure on OrgStructure.id = Person.orgStructure_id
    LEFT JOIN rbMedicalAidType mt ON mt.id = ifnull(rbService.medicalAidType_id, EventType.medicalAidType_id)
    left join rbFinance on rbFinance.id = coalesce(Visit.finance_id, Contract.finance_id)
    left join Client on Client.id = Event.client_id
    LEFT JOIN ClientPolicy on ClientPolicy.id = COALESCE((SELECT MAX(cp2.id) 
                                                      FROM ClientPolicy cp2
                                                      WHERE cp2.client_id = Client.id AND cp2.deleted = 0 AND cp2.begDate =
    (select MAX(cp.begDate) from ClientPolicy cp
            WHERE cp.client_id = Client.id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate <= Event.setDate AND (cp.endDate is NULL OR cp.endDate >= Event.setDate))),
   (SELECT MAX(cp2.id)
            FROM ClientPolicy cp2
            WHERE cp2.client_id = Client.id AND cp2.deleted = 0 AND cp2.begDate =
            (select MAX(cp.begDate)
              from ClientPolicy cp
              WHERE cp.client_id = Client.id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate BETWEEN Event.setDate AND ADDDATE(DATE(Event.execDate), 30)
              )),
  (SELECT MAX(cp2.id)
          FROM ClientPolicy cp2
          WHERE cp2.client_id = Event.relative_id AND cp2.deleted = 0 AND cp2.begDate =
          (select MAX(cp.begDate)
          from ClientPolicy cp
          WHERE cp.client_id = Event.relative_id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate <= Event.setDate AND (cp.endDate is NULL OR cp.endDate >= Event.setDate)
             )))    left join Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
             LEFT JOIN Organisation AS headInsurer ON headInsurer.id = Insurer.head_id
             LEFT JOIN Organisation AS ContractPayer ON ContractPayer.id = Contract.payer_id
    left join Organisation as Payer on Payer.id =
        IFNULL((select max(id) from Organisation o where o.OGRN = Insurer.OGRN and o.deleted = 0 and o.isInsurer = 1
        and o.OKATO = Insurer.OKATO and Insurer.OKATO = '03000' and o.head_id is null), Contract.payer_id)
    where Event.deleted = 0 and Visit.deleted = 0 
    and DATE(Visit.date) >= DATE(Event.setDate)
    and rbService.id is not null
    and ifnull(Account_Item.price, ct.price) is not null
    and %(cond)s 
      ) q
    group by q.event_id
    order by q.event_id
        """
        db = QtGui.qApp.db
        return db.query(stmt %{"cond": getCond(params)})

    def build(self, description, params):

        reportData = {'keys' : []}
        rowDict = {'singlePos': u'Разовое посещение', 'obr': u'Обращение по заболеванию (2 и более)',  'prof': u'Профилактический прием', 'total': u'Итого'}

        def processQuery(query):
            defaultVals = {
                        'cnt' : 0, 
                        'uet' : 0, 
                        'sum' : 0, 
                        'cntAll' : 0, 
                    }
            reportData['keys'].append('singlePos')
            reportData['keys'].append('obr')
            reportData['keys'].append('prof')
            reportData['keys'].append('total')
            
            for k in reportData['keys']:
                reportData.setdefault(k, defaultVals.copy())
                
            total = reportData['total']
            
            while query.next():
                record = query.record()
                pos = forceInt(record.value('pos'))
                obr = forceInt(record.value('obr'))
                prof = forceInt(record.value('prof'))
                uet = forceDouble(record.value('uet'))
                sum = forceDouble(record.value('sum'))
                if obr:               
                    key = 'obr'
                    cnt = obr
                elif prof:
                    key = 'prof'
                    cnt = prof
                else:
                    key = 'singlePos'
                    cnt = pos
                    
                reportline = reportData[key]
                reportline['cnt'] += cnt
                reportline['uet'] += uet
                reportline['sum'] += sum
                reportline['cntAll'] += pos
                total['cnt'] += cnt
                total['uet'] += uet
                total['sum'] += sum
                total['cntAll'] += pos

        query = self.selectData(params)
        processQuery(query)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()

        tableColumns = [
            ('30%', u'', CReportBase.AlignCenter),
            ('15%', u'Количество', CReportBase.AlignCenter),
            ('15%', u'УЕТ', CReportBase.AlignCenter),
            ('15%', u'Сумма (руб.)', CReportBase.AlignCenter),
            ('25%', u'Общее количество посещений (первичных и вторичных)', CReportBase.AlignCenter),
            ]

        table = createTable(cursor, tableColumns)
        for repRow in reportData['keys']:
            row = table.addRow()
            table.setText(row, 0, rowDict[repRow], blockFormat=CReportBase.AlignLeft)
            if repRow == 'total':                
                for i, key in enumerate(['uet', 'sum', 'cntAll']):
                    table.setText(row, i+2, reportData[repRow][key], blockFormat=CReportBase.AlignRight)
                table.mergeCells(row, 0, 1, 2)
            else:
                for i, key in enumerate(['cnt', 'uet', 'sum', 'cntAll']):
                    table.setText(row, i+1, reportData[repRow][key], blockFormat=CReportBase.AlignRight)
                
        return doc

class CReportSummaryStomPosEx(CReportSummaryStomPos):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CReportSummaryStomPos.exec_(self)


    def getSetupDialog(self, parent):
        result = CEconomicAnalisysSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CReportSummaryStomPos.build(self, '\n'.join(self.getDescription(params)), params)
