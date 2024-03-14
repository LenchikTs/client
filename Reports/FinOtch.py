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
  
    
class CFinOtch(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по услугам, в разрезе счетов')

    def selectData(self, params):
        stmt=u"""
    select Account.number AS num, Account.date AS dat, q.fin as fin, q.infis as infis,count(distinct q.event_id) as cnt,sum(q.KD) as kd,round(sum(q.sum),2) as sum , q.orgstructure_name as osname
    from (select Event.client_id, Event.id as event_id, Contract.id as contract_id, rbFinance.id as finance_id, rbFinance.name as fin, Person.id as person_id, Account.id as account_id,
    OrgStructure.id as OrgStructure_id, OrgStructure.name OrgStructure_name, rbSpeciality.name as specialityName,
    Person.speciality_id as speciality_id, Person.org_id as org_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code as tabn, mt.regionalCode, mt.name as VPNAME,
    rbService.infis,  rbService.name, Event.execDate,  
    IF(rbService.name like 'Обращение по поводу заболевания к%%', 1, 0) as isObr,
    0 as KD,
      IFNULL(Account_Item.price, ct.price) as price, 
    IFNULL(Account_Item.sum, vAction.amount * ct.price) as sum,
    (Account_Item.id IS NOT NULL) AS exposed,
    (Account_Item.id is not null and Account_Item.refuseType_id IS NULL) AS payed,
    (Account_Item.id IS NOT NULL AND Account_Item.refuseType_id IS NOT NULL) as refused
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
    LEFT JOIN rbMedicalAidType mt ON mt.id = ifnull(rbService.medicalAidType_id, EventType.medicalAidType_id)
    left join rbFinance on  rbFinance.id = coalesce(vAction.finance_id, Contract.finance_id)
    left join Client on Client.id = Event.client_id
    left join ClientPolicy on ClientPolicy.id = getClientPolicyIdForDate(Client.id, 1, Event.execDate, Event.id)
    left join Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    left join Organisation as Payer on Payer.id =
        IFNULL((select max(id) from Organisation o where o.OGRN = Insurer.OGRN and o.deleted = 0 and o.isInsurer = 1
        and o.OKATO = Insurer.OKATO and Insurer.OKATO = '03000' and o.head_id is null), Contract.payer_id)
    where vAction.deleted = 0 
    and Event.deleted = 0
    and rbService.id is not null
    and ifnull(Account_Item.price, ct.price) is not null
    and DATE(vAction.endDate) >= DATE(Event.setDate)
    /*and vAction.expose = 1*/
      and %(cond)s
    
    
    union all
    
    select Event.client_id, Event.id as event_id, Contract.id as contract_id, rbFinance.id as finance_id, rbFinance.name as fin, Person.id as person_id, Account.id as account_id,
    OrgStructure.id as OrgStructure_id, OrgStructure.name OrgStructure_name, rbSpeciality.name as specialityName,
    Person.speciality_id as speciality_id, Person.org_id as org_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code as tabn, mt.regionalCode, mt.name as VPNAME,
    rbService.infis,  rbService.name, Event.execDate,
    IF(rbService.name like 'Обращение по поводу заболевания к%%', 1, 0) as isObr,
    0 as KD, 
    IFNULL(Account_Item.price, ct.price) as price, 
    IFNULL(Account_Item.sum, ct.price) as sum,
    (Account_Item.id IS NOT NULL) AS exposed,
    (Account_Item.id is not null and Account_Item.refuseType_id IS NULL) AS payed,
    (Account_Item.id IS NOT NULL AND Account_Item.refuseType_id IS NOT NULL) as refused
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
    left join ClientPolicy on ClientPolicy.id = getClientPolicyIdForDate(Client.id, 1, Event.execDate, Event.id)
    left join Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    left join Organisation as Payer on Payer.id =
        IFNULL((select max(id) from Organisation o where o.OGRN = Insurer.OGRN and o.deleted = 0 and o.isInsurer = 1
        and o.OKATO = Insurer.OKATO and Insurer.OKATO = '03000' and o.head_id is null), Contract.payer_id)
    where Event.deleted = 0 and Visit.deleted = 0 
    and DATE(Visit.date) >= DATE(Event.setDate)
    and rbService.id is not null
    and ifnull(Account_Item.price, ct.price) is not null
      and %(cond)s
    
    union all
    
    select Event.client_id, Event.id as event_id, Contract.id as contract_id, rbFinance.id as finance_id, rbFinance.name as fin, Person.id as person_id, Account.id as account_id,
    OrgStructure.id as OrgStructure_id, OrgStructure.name OrgStructure_name, rbSpeciality.name as specialityName,
    Person.speciality_id as speciality_id, Person.org_id as org_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code as tabn, mt.regionalCode, mt.name as VPNAME,
    rbService.infis,  rbService.name, Event.execDate, 
     0 as isObr,  WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode) as KD,  
    IFNULL(Account_Item.price, CalcCSGTarif(Event.id, Event.execDate, r2.infis, d.mkb, WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode)
	, ct.frag1Start, ct.frag2Start, age(Client.birthDate, Event.setDate), mt.regionalCode, ct.master_id, ct.price)) as price,
    IFNULL(Account_Item.sum, CalcCSGTarif(Event.id, Event.execDate, r2.infis, d.mkb, WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode)
	, ct.frag1Start, ct.frag2Start, age(Client.birthDate, Event.setDate), mt.regionalCode, ct.master_id, ct.price)) as sum,
    (Account_Item.id IS NOT NULL) AS exposed,
    (Account_Item.id is not null and Account_Item.refuseType_id IS NULL) AS payed,
    (Account_Item.id IS NOT NULL AND Account_Item.refuseType_id IS NOT NULL) as refused
    from Event
    left join Client on Client.id = Event.client_id
    left join Account_Item on Account_Item.event_id = Event.id and Account_Item.visit_id is null and Account_Item.action_id is null and Account_Item.deleted = 0
    left join Account on Account.id = Account_Item.master_id and Account.deleted = 0
    left join mes.MES on MES.id = Event.MES_id
    LEFT JOIN EventType ON EventType.id = Event.eventType_id
    LEFT JOIN rbService r2 ON r2.infis = MES.code
    LEFT JOIN rbService ON rbService.id = IFNULL(Account_Item.service_id, r2.id)
    left join Diagnosis d on d.id = getEventDiagnosis(Event.id) 
    LEFT JOIN rbMedicalAidType mt ON mt.id = ifnull(rbService.medicalAidType_id, EventType.medicalAidType_id)
    LEFT JOIN Contract ON Contract.id = coalesce(Account.contract_id, Event.contract_id)
    left join rbFinance on rbFinance.id = Contract.finance_id
    LEFT JOIN Contract_Tariff ct ON ct.master_id = IFNULL(Contract.priceList_id, Contract.id) 
        and ct.service_id = rbService.id and ct.deleted = 0
            and (ct.endDate is not null and DATE(Event.execDate) between ct.begDate and ct.endDate 
            or DATE(Event.execDate) >= ct.begDate and ct.endDate is null) 
            and ct.tariffType = 13 AND (ct.eventType_id = Event.eventType_id or ct.eventType_id is null)
    LEFT JOIN Person ON Person.id = Event.execPerson_id
    LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
    left join OrgStructure on OrgStructure.id = Person.orgStructure_id
    left join ClientPolicy on ClientPolicy.id = getClientPolicyIdForDate(Client.id, 1, Event.execDate, Event.id)
    left join Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    left join Organisation as Payer on Payer.id =
        IFNULL((select max(id) from Organisation o where o.OGRN = Insurer.OGRN and o.deleted = 0 and o.isInsurer = 1
        and o.OKATO = Insurer.OKATO and Insurer.OKATO = '03000' and o.head_id is null), Contract.payer_id)
    where Event.execDate is not null and Event.deleted = 0
    and substr(rbService.infis, 1, 1) = 'G' and ifnull(Account_Item.price, ct.price) is not null
    and %(cond)s) q
  LEFT JOIN Account ON Account.id = q.account_id
    group by  Account.number, Account.date, q.infis
    order by Account.number,Account.date,q.infis
    """
        db = QtGui.qApp.db
        return db.query(stmt %{"cond": getCond(params)})

    def build(self, description, params):
        reportRowSize = 6
        reportData = {}
# osname = forceString(record.value('osname'))
  #              fin = forceString(record.value('fin'))
#                infis = forceString(record.value('infis'))
               # name = forceString(record.value('name'))
             #   amount = forceInt(record.value('amount'))
           #     kd = forceInt(record.value('kd'))
         #       pd = forceInt(record.value('pd'))
       #         uet = forceDouble(record.value('uet'))
     #           sum = forceDouble(record.value('sum'))
   #             cnt = forceInt(record.value('cnt'))
 #               pos = forceInt(record.value('pos'))

                #key = (osname, fin,   infis,  name)
              #  reportLine = reportData.setdefault(key, [0]*reportRowSize)
            #    reportLine[0] += amount
          #      reportLine[1] += kd
        #        reportLine[2] += pd
      #          reportLine[3] += uet
    #            reportLine[4] += sum
  #              reportLine[5] += cnt
#                 reportLine[6] += pos


        def processQuery(query):
            while query.next():
                record = query.record()
                num= forceString(record.value('num'))#name
                dat= forceString(record.value('dat'))#name
                fin = forceString(record.value('fin'))#+
                infis = forceString(record.value('infis'))#+
                kd = forceInt(record.value('kd'))#+
                sum = forceDouble(record.value('sum'))#+
                cnt = forceInt(record.value('cnt'))#+
                osname = forceString(record.value('osname'))#+

                key = (num, dat,   infis, fin,  osname )
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                
                reportLine[1] += kd
                reportLine[2] += sum
                reportLine[0] += cnt
             #   reportLine[0] += kd
             #   reportLine[1] += sum
              #  reportLine[2] += cnt
        query = self.selectData(params)
        processQuery(query)
        
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
            ('15%',  [ u'Дата'], CReportBase.AlignLeft),
            ('20%',  [ u'Код услуги'], CReportBase.AlignLeft),
            ('15%',  [ u'Случаев'], CReportBase.AlignLeft),
            ('15%',  [ u'К/Д'], CReportBase.AlignRight),
            ('15%',  [ u'Сумма'], CReportBase.AlignRight),
            ('20%',  [ u'Отделение'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 1)
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 2, 1)

        totalBynum = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        colsShift = 2
        prevnum = None
        prevdat = None
        
        keys = reportData.keys()
        keys.sort()
        def drawTotal(table,  total,  text): 
    
            row = table.addRow()

            table.setText(row, 1, text, CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 2)
            for col in xrange(reportRowSize):
                if (col<3):
                    table.setText(row, col + colsShift, total[col])
        
        for key in keys:
            #key = (osname, fin,   infis,  name)
            osname = key[4]
            infis = key[2]
            dat = key[1]
            num= key[0]
            #mergeCells(int row, int column, int numRows, int numCols)

        
            reportLine = reportData[key]
            if prevnum!=None and prevnum!=num:
                drawTotal(table,  totalBynum, u'%s итого' % prevnum);
                totalBynum = [0]*reportRowSize
                
            
                
            if prevnum!=num:
                row = table.addRow()
                table.setText(row, 0, num, CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 6)
                
            row = table.addRow()     
            table.setText(row, 5, osname)       
            table.setText(row, 0, dat)
            table.setText(row, 1, infis)
            for col in xrange(reportRowSize):
                if (col<3):
                    table.setText(row, col + colsShift, reportLine[col])
                totalByReport[col] = totalByReport[col] + reportLine[col]
                totalBynum[col] = totalBynum[col] + reportLine[col]
            prevnum = num
        #total
        drawTotal(table,  totalBynum, u'%s итого' % prevnum);
        drawTotal(table,  totalByReport, u'Итого');
        return doc

class CFinOtchEx(CFinOtch):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinOtch.exec_(self)


    def getSetupDialog(self, parent):
        result = CEconomicAnalisysSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CFinOtch.build(self, '\n'.join(self.getDescription(params)), params)
