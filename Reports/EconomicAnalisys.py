# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from EconomicAnalisysSetupDialog import getCond
from library.Utils import forceString

actionJoins = u"""
FROM Action
LEFT JOIN Event on Event.id = Action.event_id
LEFT JOIN Organisation currentOrg on currentOrg.id = Event.org_id
LEFT JOIN EventType ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
LEFT JOIN rbEventProfile ep on ep.id = EventType.eventProfile_id
LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
LEFT JOIN rbService ON rbService.id = ActionType.nomenclativeService_id
LEFT JOIN Contract ON Contract.id = Event.contract_id
LEFT JOIN rbFinance on rbFinance.id = coalesce(Action.finance_id, Contract.finance_id)
LEFT JOIN Contract_Tariff ct ON ct.master_id = Contract.id
    and ct.service_id = rbService.id and ct.deleted = 0
    and (ct.endDate is not null and DATE(Action.endDate) between ct.begDate and ct.endDate
    or DATE(Action.endDate) >= ct.begDate and ct.endDate is null) and ct.tariffType in (2,5)
LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = Event.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code IN ('1', '2', '4')
  ORDER BY rbDiagnosisType.code
  LIMIT 1
  )
LEFT JOIN Person ON Person.id = Action.person_id
LEFT JOIN rbSpeciality PersonSpeciality ON PersonSpeciality.id = Person.speciality_id
LEFT JOIN Client on Client.id = Event.client_id
LEFT JOIN ClientPolicy on ClientPolicy.id = COALESCE((SELECT MAX(cp2.id) 
                                                      FROM ClientPolicy cp2
                                                      WHERE cp2.client_id = Client.id AND cp2.deleted = 0 AND cp2.begDate =
    (select MAX(cp.begDate) from ClientPolicy cp
            WHERE cp.client_id = Client.id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate <= Event.execDate AND (cp.endDate is NULL OR cp.endDate >= Event.execDate))),
   (SELECT MAX(cp2.id)
            FROM ClientPolicy cp2
            WHERE cp2.client_id = Client.id AND cp2.deleted = 0 AND cp2.begDate =
            (select MAX(cp.begDate)
              from ClientPolicy cp
              WHERE cp.client_id = Client.id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate BETWEEN Event.execDate AND ADDDATE(DATE(Event.execDate), 30)
              )),
  (SELECT MAX(cp2.id)
          FROM ClientPolicy cp2
          WHERE cp2.client_id = Event.relative_id AND cp2.deleted = 0 AND cp2.begDate =
          (select MAX(cp.begDate)
          from ClientPolicy cp
          WHERE cp.client_id = Event.relative_id
              AND cp.policyType_id IN (1,2)
              AND cp.deleted = 0
              AND cp.begDate <= Event.execDate AND (cp.endDate is NULL OR cp.endDate >= Event.execDate)
             )))
LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
LEFT JOIN rbMedicalAidType mt ON mt.id = case when rbMedicalAidType.regionalCode in ('271', '272') and Event.execDate >= '2020-05-01' then (select mat.id from rbMedicalAidType mat where mat.regionalCode = IF(rbMedicalAidType.regionalCode = '271', '21', '22') limit 1) else rbMedicalAidType.id end
"""

visitJoins = u"""
FROM Visit
LEFT JOIN Event on Event.id = Visit.event_id
LEFT JOIN EventType  ON EventType.id = Event.eventType_id
LEFT JOIN rbService ON rbService.id = Visit.service_id
LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
LEFT JOIN Contract ON Contract.id = Event.contract_id
LEFT JOIN rbFinance on rbFinance.id = coalesce(Visit.finance_id, Contract.finance_id)
LEFT JOIN Contract_Tariff ct ON ct.master_id = Contract.id
    and ct.tariffType = 0 and ct.service_id = rbService.id and ct.deleted = 0
    and (ct.endDate is not null and DATE(Visit.date) between ct.begDate and ct.endDate
    or DATE(Visit.date) >= ct.begDate and ct.endDate is null)
LEFT JOIN Person ON Person.id = Visit.person_id
LEFT JOIN Client on Client.id = Event.client_id
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
LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
LEFT JOIN rbMedicalAidType mt ON mt.id = case when rbMedicalAidType.regionalCode in ('271', '272') and Event.execDate >= '2020-05-01' then (select mat.id from rbMedicalAidType mat where mat.regionalCode = IF(rbMedicalAidType.regionalCode = '271', '21', '22') limit 1) else rbMedicalAidType.id end
"""

mesJoins = u"""
FROM Event
LEFT JOIN mes.MES on MES.id = Event.MES_id
LEFT JOIN EventType ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
LEFT JOIN Client on Client.id = Event.client_id
LEFT JOIN rbService ON rbService.infis = MES.code
LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = Event.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code IN ('1', '2', '4')
  ORDER BY rbDiagnosisType.code
  LIMIT 1
  )
LEFT JOIN Contract ON Contract.id = Event.contract_id
LEFT JOIN rbFinance on rbFinance.id = Contract.finance_id
LEFT JOIN Contract_Tariff ct ON ct.master_id = Contract.id
    and ct.service_id = rbService.id and ct.deleted = 0
    and (ct.endDate is not null and DATE(Event.execDate) between ct.begDate and ct.endDate
    or DATE(Event.execDate) >= ct.begDate and ct.endDate is null) and ct.tariffType = 13
LEFT JOIN Person ON Person.id = Event.execPerson_id
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
LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
LEFT JOIN rbMedicalAidType mt ON mt.id = case when rbMedicalAidType.regionalCode in ('271', '272') and Event.execDate >= '2020-05-01' then (select mat.id from rbMedicalAidType mat where mat.regionalCode = IF(rbMedicalAidType.regionalCode = '271', '21', '22') limit 1) else rbMedicalAidType.id end
"""

accountJoins = u"""
FROM Account
left join rbAccountType on rbAccountType.id = Account.type_id
LEFT JOIN Contract ON Contract.id = Account.contract_id
LEFT JOIN Account_Item ON Account_Item.master_id = Account.id
LEFT JOIN Contract_Tariff ct ON ct.id = Account_Item.tariff_id
LEFT JOIN Event ON Event.id = Account_Item.event_id
LEFT JOIN Organisation currentOrg on currentOrg.id = Event.org_id
LEFT JOIN Client on Client.id = Event.client_id
LEFT JOIN EventType ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
LEFT JOIN Action ON Action.id = Account_Item.action_id
LEFT JOIN Visit ON Visit.id = Account_Item.visit_id
LEFT JOIN Person ON Person.id = COALESCE(Visit.person_id, Action.person_id, Event.execPerson_id)
LEFT JOIN Person ActionPerson ON ActionPerson.id = Action.person_id
LEFT JOIN rbSpeciality PersonSpeciality ON PersonSpeciality.id = ActionPerson.speciality_id
LEFT JOIN rbFinance on rbFinance.id = COALESCE(Action.finance_id, Visit.finance_id, Contract.finance_id)
LEFT JOIN rbService ON rbService.id = Account_Item.service_id
LEFT JOIN Organisation AS Payer ON Payer.id = Account.payer_id
LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = Event.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code IN ('1', '2', '4')
  ORDER BY rbDiagnosisType.code
  LIMIT 1
  )
LEFT JOIN rbMedicalAidType mt ON mt.id = case when rbMedicalAidType.regionalCode in ('271', '272') and Event.execDate >= '2020-05-01' then (select mat.id from rbMedicalAidType mat where mat.regionalCode = IF(rbMedicalAidType.regionalCode = '271', '21', '22') limit 1) else rbMedicalAidType.id end
"""
actionOnlyMESJoins = u"""
LEFT JOIN mes.MES on MES.id = Event.MES_id
LEFT JOIN rbService mes_service ON mes_service.infis = MES.code
LEFT JOIN Contract_Tariff ct_mes ON ct_mes.master_id = Contract.id
    and ct_mes.service_id = mes_service.id and ct_mes.deleted = 0
    and (ct_mes.endDate is not null and DATE(Event.execDate) between ct_mes.begDate and ct_mes.endDate
    or DATE(Event.execDate) >= ct_mes.begDate and ct_mes.endDate is null) and ct_mes.tariffType = 13
"""

actionCondition = u"""
WHERE Action.deleted = 0
and Event.deleted = 0
and ActionType.nomenclativeService_id is not null
and Event.expose = 1"""

visitCondition = u"""
WHERE Event.deleted = 0
and Event.expose = 1
and Visit.deleted = 0
and Visit.service_id is not null"""

mesCondition = u"""
WHERE Event.deleted = 0
and Event.expose = 1
AND Event.MES_id is not null"""

hospitalBedProfileJoin = u"""
LEFT JOIN Action AS HospitalAction ON
            HospitalAction.id = (
                SELECT MAX(A.id)
                FROM Action A
                WHERE A.event_id = Event.id AND
                          A.deleted = 0 AND
                          A.actionType_id IN ({0})
            )
left join ActionPropertyType on ActionPropertyType.name = 'койка'
    and ActionPropertyType.actionType_id = HospitalAction.actionType_id and ActionPropertyType.deleted = 0
left join ActionProperty on ActionProperty.type_id = ActionPropertyType.id
    and ActionProperty.action_id = HospitalAction.id and ActionProperty.deleted = 0
left join ActionProperty_HospitalBed on ActionProperty_HospitalBed.id = ActionProperty.id
left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.id = ActionProperty_HospitalBed.value
left join rbHospitalBedProfile on rbHospitalBedProfile.id = OrgStructure_HospitalBed.profile_id"""

accountCondition = u"WHERE Account.deleted = 0 AND Account_Item.deleted = 0"

colActionVisitPos = u"""IF(rbService.id in (select vVisitServices.id from vVisitServices), 1, 0) AS colPos"""
colActionVisitObr = u"IF(rbService.name like 'Обращен%%', 1, 0) as colObr"
colMesObr = u"0 as colObr"
colMesPos = u"0 as colPos"
colMesSMP = u" 0 as colSMP"
colActionVisitSMP = u"IF(substr(rbService.infis, 1, 7) = 'B01.044', 1, 0) as colSMP"
colActionKD = u"IF(substr(rbService.infis, 1, 1) = 'V', WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colKD"
colVisitKD = u"0 as colKD"
colMesKD = u"""if(mt.regionalCode in ('11', '12', '301', '302', '401', '402'),
    WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colKD"""
colAccountKD = u"IF(substr(rbService.infis, 1, 1) in ('V', 'G') AND mt.regionalCode in ('11', '12', '301', '302', '401', '402'), WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colKD"
colAccountKDPD = u"IF(substr(rbService.infis, 1, 1) in ('V', 'G') AND mt.regionalCode in ('11', '12', '301', '302', '401', '402','41', '42', '43', '51', '52', '71', '72', '90', '411', '422', '511', '522'), WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colKD"
colActionVisitPD = u"0 as colPD"
colMesPD = u"""if(mt.regionalCode in ('41', '42', '43', '51', '52', '71', '72', '90', '411', '422', '511', '522'),
    WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colPD"""
colAccountPD = u"""IF(substr(rbService.infis, 1, 1) = 'G' AND mt.regionalCode in ('41', '42', '43', '51', '52', '71', '72', '90', '411', '422', '511', '522'),
WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colPD"""
colMesKDPD = u"""if(mt.regionalCode in ('11', '12', '301', '302', '401', '402','41', '42', '43', '51', '52', '71', '72', '90', '411', '422', '511', '522'),
    WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), 0) as colKD"""
colActionVisitCSG = u"0 colCSG"
colMesCSG = u"IF(substr(rbService.infis, 1, 1) = 'G', 1, 0) as colCSG"
colActionUET = u"Action.amount * ct.uet as colUET"
colVisitMesUET = u"0 as colUET"
colAccountUET = u"Account_Item.uet as colUET"
colActionAmount = u"Action.amount as colAmount"
colVisitMesAmount = u"1 as colAmount"
colAccountAmount = u"Account_Item.amount as colAmount"
colActionSUM = u"""round(CASE
WHEN rbFinance.code <> '2' then ct.price
WHEN DATE(Event.setDate) > Action.endDate THEN 0
WHEN Action.org_id IS NOT NULL THEN 0
WHEN Event.execDate >= '2019-03-01' AND SUBSTR(rbService.infis, 1, 3) IN ('B01', 'B02', 'B04', 'B05') and mt.regionalCode in ('21', '22') and rbService.name NOT LIKE '%%обращение%%' 
    AND EXISTS(select a.id
                        from Event e
                        LEFT JOIN soc_obr u ON 1=1
                        left join rbService rs on rs.infis in (u.kusl, u.kusl2)
                        left join ActionType at on at.nomenclativeService_id = rs.id
                        left join Action a on a.event_id = e.id and a.actionType_id = at.id
                        where e.id = Event.id and u.spec = SUBSTR(rbService.infis, 5, 3) and e.deleted = 0 and a.deleted = 0) THEN 0
WHEN mt.regionalCode IN ('232', '252', '262') AND Event.execDate < '2019-03-01' AND SUBSTR(rbService.infis, 1, 3) NOT IN ('B01', 'B04') AND ct.uet = 0 THEN 0
WHEN mt.regionalCode IN ('232', '252', '262') AND Event.execDate >= '2019-03-01' AND SUBSTR(rbService.infis, 1, 7) NOT IN ('B04.031', 'B04.026') THEN 0
WHEN mt.regionalCode = '261' AND Event.execDate < '2019-03-01' AND SUBSTR(rbService.infis, 1, 3) NOT IN ('B01', 'B04') THEN 0
WHEN mt.regionalCode = '261' AND Event.execDate >= '2019-03-01' AND Event.execDate < '2019-06-01' AND SUBSTR(rbService.infis, 1, 7) NOT IN ('B04.047', 'B04.026') THEN 0
WHEN mt.regionalCode = '261' AND ep.regionalCode = '8011' AND Event.execDate >= '2019-06-01' AND SUBSTR(rbService.infis, 1, 7) NOT IN ('B04.047', 'B04.026') AND
  NOT EXISTS (SELECT
      a.id
    FROM Action a
      LEFT JOIN ActionType at
        ON at.id = a.actionType_id
      LEFT JOIN rbService s
        ON s.id = at.nomenclativeService_id
    WHERE a.event_id = Event.id
    AND a.deleted = 0
    AND s.infis IN ('B04.026.002', 'B04.047.002')) THEN 0
WHEN ct.uet > 0 AND Action.endDate >= '2017-01-01' AND Action.endDate < '2018-01-01' AND Event.setDate < ADDDATE(Client.birthDate, INTERVAL 18 YEAR) THEN
    CASE WHEN Action.endDate >= '2017-03-01' AND rbService.infis IN ('B01.064.003', 'B01.064.004', 'B04.064.001', 'B04.064.002') THEN ct.price
    ELSE ROUND(CAST(ct.price AS DECIMAL(12,2)) * 1.3, 2) END
WHEN mt.regionalCode = '211' AND
  ep.regionalCode IN ('8008', '8014') AND
  SUBSTR(rbService.infis, 1, 7) NOT IN ('B04.026', 'B04.047') AND
  NOT EXISTS (SELECT
      a.id
    FROM Action a
      LEFT JOIN ActionType at
        ON at.id = a.actionType_id
      LEFT JOIN rbService s
        ON s.id = at.nomenclativeService_id
    WHERE a.event_id = Event.id
    AND a.deleted = 0
    AND s.infis IN ('B04.026.001.062', 'B04.047.001.061')) THEN 0 
WHEN Event.execDate >= '2019-05-01' and mt.regionalCode = '211' AND ep.regionalCode IN ('8009', '8015') 
    AND SUBSTR(rbService.infis, 1, 1) = 'A' THEN 0
WHEN mt.regionalCode IN ('271', '272') AND
  Action.endDate >= '2017-01-01' AND
  substr(Insurer.area, 1, 2) = '%(defaulRegion)s' THEN 0
WHEN mt.regionalCode = '233' AND rbService.infis IN ('B04.047.002', 'B04.047.004', 'B04.026.002')  THEN 0
ELSE ct.price END * Action.amount, 2) AS colSUM"""
colVisitSUM = u"round(ct.price, 2) as colSUM"
colMesSUM = u"""CalcCSGTarif(Event.id, Event.execDate, rbService.infis, d.mkb,
    WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode), ct.frag1Start,
    ct.frag2Start, age(Client.birthDate, Event.setDate), mt.regionalCode, ct.master_id, ct.price) as colSUM"""
colAccountSum = u"round(Account_Item.sum, 2) as colSUM"
clientId = u"Event.client_id as colClient"
eventId = u"Event.id as colEvent"
orgStructureName = u"OrgStructure.name as colOrgStructure"
orgStructureInfis = u"OrgStructure.infisCode as colOrgStructureInfis"
orgStructureInfisName = u"CONCAT(OrgStructure.infisCode, ' - ', OrgStructure.name) as colOrgStructureInfisName"
parentOrgStructureInfisName = u"CONCAT(parentOrgStructure.infisCode, ' - ', parentOrgStructure.name) as colParentOrgStructureInfisName"
serviceInfis = u"rbService.infis as colServiceInfis"
serviceName = u"rbService.name as colServiceName"
serviceInfisName = u"concat_ws(' ', rbService.code, rbService.name) as colServiceInfisName"
payerTitle = u"""CASE WHEN substr(Insurer.area, 1, 2) = '%(defaulRegion)s' AND Insurer.head_id is not null THEN concat_ws(' ', headInsurer.infisCode, headInsurer.shortName)
WHEN substr(Insurer.area, 1, 2) = '%(defaulRegion)s' AND Insurer.head_id is null THEN concat_ws(' ', Insurer.infisCode, Insurer.shortName)
WHEN Insurer.id is not null and substr(Insurer.area, 1, 2) <> '%(defaulRegion)s' THEN concat_ws(' ', ContractPayer.infisCode, ContractPayer.shortName)
ELSE '0000 Плательщик не определен (нет полиса)' END as colPayerTitle"""
payerTitleAccount = u"concat_ws(' ', Payer.infisCode, Payer.shortName) as colPayerTitle"
financeTitle = u"rbFinance.name as colFinance"
parentOrgStructure = u"parentOrgStructure.name as colParentOrgStructure"
person = u"concat(Person.lastName, ' ', Person.firstName, ' ', Person.patrName, ' (', Person.code, ')') as colPerson"
MKBCode = u"m.diagID as colMKBCode"
MKBName = u"m.DiagName as colMKBName"
eventSetDate = u"Event.setDate as colEventSetDate"
eventExecDate = u"Event.execDate as colEventExecDate"
clientName = u"concat_ws(' ', Client.lastName, Client.firstName, Client.patrName) as colClientName"
age = u"age(Client.birthDate, Event.setDate) as colAge"
clientSex = u"Client.sex as colClientSex"
clientBirthDate = u"Client.birthDate as colClientBirthDate"
regAddress = u"getClientRegAddress(Client.id) as colRegAddress"
locAddress = u"getClientLocAddress(Client.id) as colLocRegAddress"
workAddress = u"getClientWork(Client.id) as colWorkAddress"
medicalType = u"mt.name as colMedicalType"
medicalTypeCode = u"mt.regionalCode as colMedicalTypeCode"
eventType = u"EventType.name as colEventType"
specialityOKSOName = u"rbSpeciality.OKSOName as colSpecialityOKSOName"
personWithSpeciality = u"concat(Person.lastName, ' ', Person.firstName, ' ', Person.patrName, ' (', Person.code, '), ', rbSpeciality.OKSOName) as colPersonWithSpeciality"
contractName = u"concat_ws(' ', Contract.resolution, Contract.number) as colContract"
kpk = u"CONCAT(rbHospitalBedProfile.regionalCode, ' - ', rbHospitalBedProfile.name) as colKPK"
insurerCodeName = u"concat_ws(' ', Insurer.infisCode, Insurer.shortName) as colInsurerCodeName"
isWorking = u"(getClientWorkId(Client.id) is not null) as colIsWorking"
serviceActionBegDate = u"date(Action.begDate) as colServiceBegDate"
serviceVisitBegDate = u"date(Visit.date) as colServiceBegDate"
serviceCSGBegDate = u"date(Event.setDate) as colServiceBegDate"
serviceAccountBegDate = u"IF(Visit.id is not null, date(Visit.date), IF(Action.id is not null, date(Action.begDate), date(Event.setDate))) as colServiceBegDate"
serviceActionEndDate = u"date(Action.endDate) as colServiceEndDate"
serviceVisitEndDate = u"date(Visit.date) as colServiceEndDate"
serviceCSGEndDate = u"date(Event.execDate) as colServiceEndDate"
serviceAccountEndDate = u"IF(Visit.id is not null, date(Visit.date), IF(Action.id is not null, date(Action.endDate), date(Event.execDate))) as colServiceEndDate"
posType = u"""case 
        when substr(rbService.infis, 1, 3) in ('B01', 'B02') and rbService.name like '%%прием%%' and rbService.name not like '%%патронаж%%' and rbService.name not like '%%на дому%%' then 1
        when (substr(rbService.infis, 1,3) = 'B04' and rbService.name like '%%прием%%' and rbService.name like '%%диспансерн%%') then 2
        when substr(rbService.infis, 1,3) = 'B04' and rbService.name like '%%прием%%' and rbService.name not like '%%диспансерн%%' then 3
        when (rbService.name like '%%на дому%%' or rbService.name like '%%патронаж%%') and substr(rbService.infis, 1, 3) in ('B01', 'B02') then 4
        end as colPosType"""
isAdult = u"age(Client.birthDate, Event.setDate) >= 18 as colIsAdult"
stepECO = u"""(select aps.value
        from Action ECO_Step
        left join ActionPropertyType apt on apt.actionType_id = ECO_Step.actionType_id and apt.deleted = 0
        left join ActionProperty ap on ap.type_id = apt.id and ap.action_id = ECO_Step.id and ap.deleted = 0
        left join ActionProperty_String aps on aps.id = ap.id
        where ECO_Step.id = (
                        SELECT MAX(A.id)
                        FROM Action A
                        WHERE A.event_id = Event.id AND
                                  A.deleted = 0 AND
                                  A.actionType_id IN (
                                        SELECT AT.id
                                        FROM ActionType AT
                                        WHERE AT.flatCode ='ECO_Step'
                                            AND AT.deleted = 0
                                  )
                    )
            and apt.name = 'Этап ЭКО') AS colStepECO"""
citizenship = 'rbSocStatusType.name as colCitizenship'
colCitizenship = [citizenship, citizenship, citizenship, citizenship]
colEventOrder = ['Event.order as colEventOrder', 'Event.order as colEventOrder', 'Event.order as colEventOrder', 'Event.order as colEventOrder']
colUslSpec = ['substr(rbService.infis, 5, 3) as colUslSpec', 'substr(rbService.infis, 5, 3)  as colUslSpec', 'NULL  as colUslSpec', 'substr(rbService.infis, 5, 3)  as colUslSpec']
colPos = [colActionVisitPos, colActionVisitPos, colMesPos, colActionVisitPos]
colObr = [colActionVisitObr, colActionVisitObr, colMesObr, colActionVisitObr]
colSMP = [colActionVisitSMP, colActionVisitSMP, colMesSMP, colActionVisitSMP]
colKD = [colActionKD, colVisitKD, colMesKD, colAccountKD]
colPD = [colActionVisitPD, colActionVisitPD, colMesPD, colAccountPD]
colKDPD = [colActionKD, colVisitKD, colMesKDPD, colAccountKDPD]
colCSG = [colActionVisitCSG, colActionVisitCSG, colMesCSG, colMesCSG]
colUET = [colActionUET, colVisitMesUET, colVisitMesUET, colAccountUET]
colAmount = [colActionAmount, colVisitMesAmount, colVisitMesAmount, colAccountAmount]
colSUM = [colActionSUM, colVisitSUM, colMesSUM, colAccountSum]
colClient = [clientId, clientId, clientId, clientId]
colClientSex = [clientSex, clientSex, clientSex, clientSex]
colAge = [age, age, age, age]
colPosType = [posType, posType, posType, posType]
colIsAdult = [isAdult, isAdult, isAdult, isAdult]
colClientBirthDate = [clientBirthDate, clientBirthDate, clientBirthDate, clientBirthDate]
colRegAddress = [regAddress, regAddress, regAddress, regAddress]
colLocRegAddress = [locAddress, locAddress, locAddress, locAddress]
colWorkAddress = [workAddress, workAddress, workAddress, workAddress]
colEvent = [eventId, eventId, eventId, eventId]
colOrgStructure = [orgStructureName, orgStructureName, orgStructureName, orgStructureName]
colOrgStructureInfis = [orgStructureInfis, orgStructureInfis, orgStructureInfis, orgStructureInfis]
colOrgStructureInfisName = [orgStructureInfisName, orgStructureInfisName, orgStructureInfisName, orgStructureInfisName]
colParentOrgStructureInfisName = [parentOrgStructureInfisName, parentOrgStructureInfisName, parentOrgStructureInfisName, parentOrgStructureInfisName]
colKPK = [kpk, kpk, kpk, kpk]
colServiceInfis = [serviceInfis, serviceInfis, serviceInfis, serviceInfis]
colServiceName = [serviceName, serviceName, serviceName, serviceName]
colServiceInfisName = [serviceInfisName, serviceInfisName, serviceInfisName, serviceInfisName]
colServiceBegDate = [serviceActionBegDate, serviceVisitBegDate, serviceCSGBegDate, serviceAccountBegDate]
colServiceEndDate = [serviceActionEndDate, serviceVisitEndDate, serviceCSGEndDate, serviceAccountEndDate]
colPayerTitle = [payerTitle, payerTitle, payerTitle, payerTitleAccount]
colFinance = [financeTitle, financeTitle, financeTitle, financeTitle]
colParentOrgStructure = [parentOrgStructure, parentOrgStructure, parentOrgStructure, parentOrgStructure]
colPerson = [person, person, person, person]
colPersonWithSpeciality = [personWithSpeciality, personWithSpeciality, personWithSpeciality, personWithSpeciality]
colMKBCode = [MKBCode, MKBCode, MKBCode, MKBCode]
colMKBName = [MKBName, MKBName, MKBName, MKBName]
colEventSetDate = [eventSetDate, eventSetDate, eventSetDate, eventSetDate]
colEventExecDate = [eventExecDate, eventExecDate, eventExecDate, eventExecDate]
colClientName = [clientName, clientName, clientName, clientName]
colMedicalType = [medicalType, medicalType, medicalType, medicalType]
colMedicalTypeCode = [medicalTypeCode, medicalTypeCode, medicalTypeCode, medicalTypeCode]
colEventType = [eventType, eventType, eventType, eventType]
colSpecialityOKSOName = [specialityOKSOName, specialityOKSOName, specialityOKSOName, specialityOKSOName]
colContract = [contractName, contractName, contractName, contractName]
colInsurerCodeName = [insurerCodeName, insurerCodeName, insurerCodeName, insurerCodeName]
colIsWorking = [isWorking, isWorking, isWorking, isWorking]
colStepECO = [stepECO, stepECO, stepECO, stepECO]

def getColsStmt(cols):
    stmtCols = ['', '', '', '']
    for col in cols:
        for idx, item in enumerate(stmtCols):
            if stmtCols[idx]:
                stmtCols[idx] += u', ' + col[idx]
            else:
                stmtCols[idx] = col[idx]
    return stmtCols
    
def getJoinStmt(cols, params):
    joinStmt = [actionJoins, visitJoins, mesJoins, accountJoins]
    for idx, item in enumerate(joinStmt):
        if colInsurerCodeName in cols and idx == 3:
            joinStmt[idx] += u"""
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
LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
"""
        if colOrgStructure in cols or colOrgStructureInfis in cols or colOrgStructureInfisName in cols or params.get('orgStructureId', None):
           joinStmt[idx] += u"""
LEFT JOIN OrgStructure on OrgStructure.id = Person.orgStructure_id"""
        if colParentOrgStructure in cols or colParentOrgStructureInfisName in cols:
            joinStmt[idx] += u"""
LEFT JOIN OrgStructure as parentOrgStructure on parentOrgStructure.id = OrgStructure.parent_id"""
        if colPayerTitle in cols or params.get('payer', None):
            if idx < 3:
                joinStmt[idx] += u"""
LEFT JOIN Organisation AS headInsurer ON headInsurer.id = Insurer.head_id
LEFT JOIN Organisation AS ContractPayer ON ContractPayer.id = Contract.payer_id"""
        if params.get('specialityId', None) or colSpecialityOKSOName in cols or colPersonWithSpeciality in cols:
            joinStmt[idx] += u"""
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id"""
        if colMKBCode in cols:
            if idx in [0,2,3]:
                joinStmt[idx] += u"""
LEFT JOIN MKB m on m.diagID = d.MKB"""
            else:
                joinStmt[idx] += u"""
LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = Event.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code IN ('1', '2', '4')
  ORDER BY rbDiagnosisType.code
  LIMIT 1
  )
LEFT JOIN MKB m on m.diagID = d.MKB"""
        if colCitizenship in cols:
            joinStmt[idx] += u"""
            LEFT JOIN ClientSocStatus ON ClientSocStatus.client_id = Client.id and ClientSocStatus.deleted = 0
            LEFT JOIN rbSocStatusClass ON rbSocStatusClass.id = ClientSocStatus.socStatusClass_id
            LEFT JOIN rbSocStatusType ON rbSocStatusType.id = ClientSocStatus.socStatusType_id
            """
        if params.get('profileBed', None) or colKPK in cols:
            stmt = u"""SELECT GROUP_CONCAT(AT.id) as idList
                                FROM ActionType AT
                                WHERE AT.flatCode ='moving'
                                    AND AT.deleted = 0"""
            query = QtGui.qApp.db.query(stmt)
            if query.first():
                record = query.record()
                idList = forceString(record.value('idList'))
                if not idList:
                    idList = 'null'
            joinStmt[idx] += hospitalBedProfileJoin.format(idList)
            
    return joinStmt
   
def getStmt(colsStmt, cols, groupCols, orderCols, params, queryList=['action', 'visit', 'mes'], additionCond=u" and ct.id is not null", having='', isOnlyMES=False):
    
    actionCols, visitCols, mesCols, accountCols = getColsStmt(cols)
    actionJoins, visitJoins, mesJoins, accountJoins = getJoinStmt(cols, params)
    cond = getCond(params)
    if colCitizenship in cols:
        cond += " AND rbSocStatusClass.code = '8' AND rbSocStatusType.socCode is not null"

    if params['dataType'] == 1:
        queryList = queryList
    else:
        queryList = ['account']
            
    if additionCond:
        cond += additionCond
    
    if groupCols:
        groupCols = "GROUP BY " + groupCols
    if orderCols:
        orderCols = "ORDER BY " + orderCols
    if having:
        having = u'HAVING ' + having
        
    var = dict()
    var["colsStmt"] = colsStmt
        
    stmt = u"""
%(colsStmt)s
from (
"""
        
    if 'action' in queryList:
        stmt += u"""
select %(actionCols)s
%(actionJoins)s
%(actionCondition)s
and %(cond)s
%(having)s"""
        var["actionCols"] = actionCols
        var["actionJoins"] = actionJoins
        if isOnlyMES:
            var["actionJoins"] = actionJoins + actionOnlyMESJoins
            if params['cashPayments']:
                var["actionCondition"] = actionCondition + " and Event.MES_id is not null and ct_mes.id is not null and Action.`payStatus` = 768"
            else:
                var["actionCondition"] = actionCondition + " and Event.MES_id is not null and ct_mes.id is not null"
        else:
            var["actionJoins"] = actionJoins
            if params['cashPayments']:
                var["actionCondition"] = actionCondition + " and Action.`payStatus` = 768"
            else:
                var["actionCondition"] = actionCondition



    if 'visit' in queryList:
        if 'action' in queryList:
            stmt += u" union all"
            
        stmt += u"""
select %(visitCols)s
%(visitJoins)s
%(visitCondition)s
and %(cond)s
%(having)s"""
        var["visitCols"] = visitCols
        var["visitJoins"] = visitJoins
        if params['cashPayments']:
            var["visitCondition"] = visitCondition + " and Visit.`payStatus` = 768"
        else:
            var["visitCondition"] = visitCondition
    if 'mes' in queryList:
        if 'action' in queryList or 'visit' in queryList:
            stmt += u" union all"
        stmt += u"""
select %(mesCols)s
%(mesJoins)s
%(mesCondition)s
and %(cond)s
%(having)s"""
        var["mesCols"] = mesCols
        var["mesJoins"] = mesJoins
        if params['cashPayments']:
            var["mesCondition"] = mesCondition + " and Event.`payStatus` = 768"
        else:
            var["mesCondition"] = mesCondition

    if 'account' in queryList:
        stmt += u"""
select %(accountCols)s
%(accountJoins)s
%(accountCondition)s
and %(cond)s
%(having)s
"""
        var["accountCols"] = accountCols
        var["accountJoins"] = accountJoins
        if params['cashPayments']:
            var["accountCondition"] = accountCondition + " and Account_Item.refuseType_id is not NULL"
        else:
            var["accountCondition"] = accountCondition
            
    stmt += u""") q
%(group)s
%(order)s
"""
    var["cond"] = cond
    var["group"] = groupCols
    var["order"] = orderCols
    var["having"] = having
    
    stmt = stmt % var
    stmt = stmt % {'defaulRegion': QtGui.qApp.provinceKLADR()[:2]}
        
    return stmt
