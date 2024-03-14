# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

u"""Экспорт реестра  в формате XML. Ростовская область"""

import json
import cProfile

from decimal import Decimal
from operator import itemgetter

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate

from Accounting.Tariff import CTariff
from Events.Action import CAction
from Exchange.Export import CMultiRecordInfo
from Exchange.ExportR08HospitalV59 import mapDiagRslt, mapPptr
from Exchange.Order79Export import (
    COrder79ExportWizard, COrder79ExportPage1,
    COrder79ExportPage2 as CExportPage2, COrder79PersonalDataWriter,
    COrder79XmlStreamWriter, CExtendedRecord)
from Exchange.Order200Export import COnkologyInfo, CTfomsNomenclatureCache

from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1

from library.DbEntityCache import CDbEntityCache
from library.Utils import (forceInt, forceString, forceDate, forceDouble,
                           forceRef, forceBool, formatSNILS, toVariant,
                           forceDateTime)

# ******************************************************************************

VERSION = '3.2'

# выводит в консоль имена невыгруженных полей
DEBUG = False

# ******************************************************************************

def exportR61Native(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    pr = cProfile.Profile()
    pr.enable()
    wizard.exec_()
    pr.disable()
    pr.dump_stats("r61_profile_stats.txt")


# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта Ростовская область"""

    def __init__(self, parent=None):
        prefix = 'R61Native'
        title = u'Мастер экспорта реестра услуг для Ростовской области'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        xmlWriter = (CExportXmlStreamWriter(self, VERSION),
                     CPersonalDataWriter(self, VERSION))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.initFields()


    def setExportMode(self, flag):
        self.cmbRegistryType.setEnabled(not flag)
        COrder79ExportPage1.setExportMode(self, flag)


    def initFields(self):
        self.query_fields = {
            # для отладки
            'aiId': 'Account_Item.id',
            'eventId': 'Account_Item.event_id',
            'actionTypeFlatCode': 'ActionType.flatCode',
            'coefficients': 'Account_Item.usedCoefficients',
            # PACIENT_*
            'PACIENT_ID_PAC': 'Event.client_id',
            'PACIENT_VPOLIS': 'rbPolicyKind.regionalCode',
            'PACIENT_SPOLIS': """CASE
                WHEN (rbPolicyKind.regionalCode LIKE '1') THEN ClientPolicy.serial
                ELSE ''
              END""",
            'PACIENT_NPOLIS': "IF(rbPolicyKind.code IN(1,2), ClientPolicy.number, '')",
            'PACIENT_ENP': "IF(rbPolicyKind.code IN(1,2), '', ClientPolicy.number)",
            'PACIENT_SMO': 'Insurer.miacCode',
            'PACIENT_SMO_OGRN': """CASE
                WHEN (Insurer.miacCode IS NULL OR Insurer.miacCode LIKE '') THEN Insurer.OGRN
                ELSE ''
              END""",
            'PACIENT_SMO_OK': 'Insurer.OKATO',
            'PACIENT_SMO_NAM': """CASE
                WHEN ((Insurer.miacCode IS NULL OR Insurer.miacCode LIKE '') AND (Insurer.OGRN IS NULL OR Insurer.OGRN LIKE '')) THEN Insurer.shortName
                ELSE ''
              END""",
#            'PACIENT_STAT_Z_raw': 'rbSocStatusType.code',
            # SLUCH_*
            'SLUCH_IDCASE': 'Account_Item.event_id',
            'SLUCH_USL_OK': 'rbEventTypePurpose.regionalCode',
            'SLUCH_VIDPOM': 'rbMedicalAidKind.regionalCode',
            'HMP_VID_HMP_raw': None,
            'HMP_METOD_HMP_raw': None,
            'HMP_HMODP': None,
            'HMP_TAL_D': None,
            'HMP_TAL_NUM': None,
            'HMP_TAL_P': None,
            'NAPR_FROM_NPR_MO': 'RelegateOrgId.value',
            'SLUCH_EXTR': None,
            'SLUCH_PODR': None,
            'SLUCH_LPU': 'PersonOrganisation.miacCode',
            'SLUCH_PROFIL': None,
            'SLUCH_DET': """CASE
                WHEN (age(Client.birthDate,Event.setDate) < 18 AND rbSpeciality.usishCode IN ('22', '81')) THEN 1
                ELSE 0
              END""",
            'SLUCH_NHISTORY': None,
            'USL_P_PER': None,
            'SLUCH_DATE_1': """CAST(CASE
                 WHEN (EventType.form LIKE '110') THEN Event.execDate
                 ELSE Event.setDate
               END AS DATE)""",
            'SLUCH_DATE_2': 'CAST(Event.execDate AS DATE)',
            'SLUCH_DS1': None,
            'SLUCH_RSLT': u"""CASE
                WHEN (mes.mrbMESGroup.code LIKE 'ДиспаснС') THEN ''
                ELSE EventResult.federalCode
              END""",
            'SLUCH_ISHOD': u"""CASE
                WHEN (mes.mrbMESGroup.code LIKE 'ДиспаснС') THEN ''
                ELSE Diagnostic.result_id
              END""",
            'SLUCH_PRVS': 'rbSpeciality.regionalCode',
            'SLUCH_IDDOKT_raw': 'IFNULL(ActionPerson.SNILS, Person.SNILS)',
            'SLUCH_IDSP': '0',
            'SLUCH_C_ZAB': 'IFNULL(rbDiseaseCharacter_Identification.value, 0)',
            'SLUCH_VB_P': """IF((SELECT COUNT(DISTINCT Action.id)
    FROM Action
    LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
    WHERE Action.event_id = Event.id
      AND Action.deleted = 0
      AND ActionType.flatCode = 'moving') >= 2, 1, '')""",
            'NAPR_FROM_NAPUCH': 'RelegateOrg.infisCode',
            'NAPR_FROM_NOM_NAP': 'Event.srcNumber',
            'NAPR_FROM_NAPDAT': 'Event.srcDate',
            'SLUCH_P_CEL': None,
            # USL_*
            'USL_PODR': None,
            'USL_PROFIL': None,
            'USL_PROFIL_KOIKI': None,
            #'USL_CRIT': None,
            'USL_DET': """CASE
                WHEN (age(Client.birthDate,Event.setDate) < 18 AND rbSpeciality.usishCode IN ('22', '81')) THEN 1
                ELSE 0
              END""",
            'USL_NPL': """IF((EventResult.federalCode IN (102,105,106,107,108,110)
                AND rbEventTypePurpose.regionalCode = 1) OR (
                EventResult.federalCode IN (102,105,106,107,108,110) AND
                rbEventTypePurpose.regionalCode = 2), '3','')""",
            'USL_DATE_IN': None,
            'USL_DATE_OUT': None,
            'USL_DS1': None,
            'USL_CODE_USL': """CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN '0'
                ELSE rbService.code
              END """,
            'USL_KOL_USL': u"""CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN '0'
                WHEN (mes.mrbMESGroup.code LIKE 'ДиспаснС') THEN ''
                ELSE Account_Item.amount
              END """,
            'USL_TARIF': None,
            'USL_SUMV_USL': """CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN 0
                ELSE Account_Item.sum
              END""",
            'USL_SL_K': 0,
            'USL_IT_SL': None,
            'USL_SK_KOEF': 0,
            'MR_USL_N_MR_N': 1,
            'MR_USL_N_PRVS': None,
            'MR_USL_N_CODE_MD_raw': None,
            'USL_CODE_OPER': None,
            'USL_KD': None,
            'USL_KSGA': 'IF(EventType.form = ''001'', rbService.infis, NULL)',
            # PERS_*
            'PERS_ID_PAC': 'Event.client_id',
            'PERS_FAM': 'UPPER(Client.lastName)',
            'PERS_IM': 'UPPER(Client.firstName)',
            'PERS_OT': 'UPPER(Client.patrName)',
            'PERS_W': 'Client.sex',
            'PERS_DR': 'Client.birthDate',
            'PERS_MR': 'UPPER(Client.birthPlace)',
            'PERS_DOCTYPE': 'rbDocumentType.regionalCode',
            'PERS_DOCSER': 'ClientDocument.serial',
            'PERS_DOCNUM': 'ClientDocument.number',
            'PERS_SNILS_raw': 'Client.SNILS',
            'PERS_DOCDATE': 'ClientDocument.date',
            'PERS_DOCORG': 'ClientDocument.origin',
            # KSG_KPG
            'KSG_KPG_N_KSG': """IF(rbService.code LIKE 'st%',(CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN '0'
                ELSE rbService.code
              END),NULL) """,
            'KSG_KPG_VER_KSG': """IF(rbService.code LIKE 'st%',YEAR(Event.execDate),NULL)""",
            'KSG_KPG_KSG_PG': """CASE
                    WHEN rbService.code LIKE 'st__.___._' THEN 1
                    WHEN rbService.code LIKE 'st__.___' THEN 0
                    ELSE NULL
                END""",
            'KSG_KPG_KOEF_D': """IF(rbService.code LIKE 'st%',1,NULL)""",
            'KSG_KPG_KOEF_Z': """IF(rbService.code LIKE 'st%',(SELECT `sum` FROM Contract_CompositionExpense
            WHERE master_id = Account_Item.tariff_id
              AND rbTable_id = (
                SELECT MAX(id) FROM rbExpenseServiceItem
                WHERE code = '7')
            LIMIT 1),NULL)""",
            'KSG_KPG_KOEF_UP': """IF(rbService.code LIKE 'st%',(SELECT `sum` FROM Contract_CompositionExpense
            WHERE master_id = Account_Item.tariff_id
              AND rbTable_id = (
                SELECT MAX(id) FROM rbExpenseServiceItem
                WHERE code = '9')
            LIMIT 1),NULL)""",
            'KSG_KPG_KOEF_U': """IF(rbService.code LIKE 'st%',(SELECT `sum` FROM Contract_CompositionExpense
            WHERE master_id = Account_Item.tariff_id
              AND rbTable_id = (
                SELECT MAX(id) FROM rbExpenseServiceItem
                WHERE code = '8')
            LIMIT 1),NULL)""",
            # нововведения 2022
            'COVID_LEK_WEI': """IF(Diagnosis.MKB IN ('U07.1','U07.2'),
            (SELECT APD.value FROM ActionProperty AP
             INNER JOIN Action ON AP.action_id = Action.id
             INNER JOIN ActionType AT ON AT.id = Action.actionType_id
             INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
             INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
             WHERE APT.descr = 'weight' AND AT.flatCode = 'CovidMedicalSupplies'
               AND Action.deleted = 0
               AND AP.deleted = 0 AND Action.event_id = Account_Item.event_id
             LIMIT 1), NULL)""",
            # разное
            'eventPurposeCode': 'rbEventTypePurpose.regionalCode', # для SLUCH_NSVOD
            'tariffType': 'Contract_Tariff.tariffType',
            'mesGroupCode': 'mes.mrbMESGroup.code',
            'serviceCode': None,
            'persAge': None,
            'isActualPolicy': """IFNULL(ClientPolicy.endDate >= CAST(Event.execDate as date), TRUE)
                AND (ClientPolicy.begDate <= CAST(Event.execDate as date))""",
            'actionEventCsgId': None,
            'eventCsgMKB': None,
            'serviceType': 'ActionType.serviceType',
            'eventOrder': u"""IF(mes.mrbMESGroup.code LIKE 'ДиспаснС','',
                Event.order)""",
            'duration': None,
            'maxDuration': None,
            'minDuration': None,
            'mesNote': None,
            'isExposedItem': '''IF(ExposedAccountItem.id IS NULL AND
                rbPayRefuseType.id IS NULL,  0, 1)''',
            'USL_CRIT': "IFNULL(Crit.code,'')",
            'isDiagnostic': '(EventType.form = ''001'')',
            'personOrgStructCode': """(SELECT OSI.value
                FROM OrgStructure_Identification OSI
                WHERE OSI.deleted = 0
                  AND OSI.master_id = Person.OrgStructure_id
                  AND OSI.system_id = (SELECT MAX(id)
                    FROM rbAccountingSystem
                    WHERE code = 'PODR')
                LIMIT 1)""",
            'accountItemAmount': 'Account_Item.amount',
            'diagnosticServiceCode': 'rbService.code',
            'diagnosticProfile': 'rbMedicalAidProfile.code',
            'accountItemSum': 'Account_Item.`sum`',
            'actionBegDate': 'Action.begDate',
            'actionEndDate': 'Action.endDate',
            'contractId': """(SELECT contract_id FROM Account
                              WHERE id = Account_Item.master_id)""",
            'movingPersonId': None,
        }


    def prepare_query_field(self):
        count = len(self.query_fields)
        i = 0
        result_string = ''

        for field, value in self.query_fields.iteritems():
            if value is None:
                result_string += 'NULL'
            elif type(value) is bool:
                result_string += 'TRUE' if value else 'FALSE'
            elif type(value) is int:
                result_string += str(value)
            else:
                result_string += value

            result_string += ' AS `{0}`'.format(field)
            i += 1
            if i < count:
                result_string += ', \n'

        return result_string


    def createAmbQuery(self, idList, commonTables):
        self.query_fields['SLUCH_EXTR'] = "''" # а точно надо ставить "пустышку"?
        self.query_fields['SLUCH_PODR'] = 'SUBSTR(rbService.code, 1, 4)'
        self.query_fields['SLUCH_PROFIL'] = 'rbMedicalAidProfile.code'
        self.query_fields['SLUCH_NHISTORY'] = 'Event.id'
        self.query_fields['SLUCH_DS1'] = 'Diagnosis.MKB'
        self.query_fields['SLUCH_P_CEL'] = None # по-умолчанию используем код для "коротких" обращений из классификатора V025
        self.query_fields['MR_USL_N_PRVS'] = 'IFNULL(ActionSpec.regionalCode, rbSpeciality.regionalCode)'
        self.query_fields['MR_USL_N_CODE_MD_raw'] = 'IFNULL(ActionPerson.SNILS, Person.SNILS)'
        self.query_fields['USL_PODR'] = 'SUBSTR(rbService.code, 1, 4)'
        self.query_fields['USL_PROFIL'] = 'rbMedicalAidProfile.code'
        self.query_fields['USL_DATE_IN'] = 'Event.setDate'
        self.query_fields['USL_DATE_OUT'] = 'Event.execDate'
        self.query_fields['USL_DS1'] = 'Diagnosis.MKB'
        self.query_fields['USL_TARIF'] = 'IFNULL(Account_Item.sum, -1)'

        return u"""/* -- АМБУЛАТОРИЯ -- */
SELECT {fields}
FROM Account_Item
    {commonTables}
    LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
WHERE rbEventTypePurpose.regionalCode = '3' -- Амбулатория
AND Account_Item.reexposeItem_id IS NULL
AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
AND {idList}\n""".format(fields=self.prepare_query_field(), idList=idList,
                   commonTables=commonTables)


    def createStacQuery(self, idList, commonTables, actionTables):
        self.query_fields['SLUCH_EXTR'] = 'IF(Event.`order` IN (2,6), 2, 1)'
        self.query_fields['SLUCH_PODR'] = '''IF(ActionType.serviceType = 9,
            CONCAT(ReanimationOrgStructPODR.value, ReanimationOrgStructN_OTD.value),
            CONCAT(LeavedOrgStructPODR.value, LeavedOrgStructN_OTD.value))'''
        self.query_fields['SLUCH_PROFIL'] = '''IFNULL(LeavedOrgStructPROFIL.value,
            LeavedHBPProfile.code)'''
        self.query_fields['SLUCH_NHISTORY'] = 'Event.externalId'
        self.query_fields['SLUCH_P_CEL'] = None
        self.query_fields['SLUCH_DS1'] = '''(SELECT ds.MKB
          FROM Diagnosis ds
            INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
            INNER JOIN rbDiagnosisType dt on (dc.diagnosisType_id=dt.id)
          WHERE (dt.code = '1' OR dt.code = '2')
            AND dc.event_id = Account_Item.event_id order by -dt.code desc, ds.createDatetime desc limit 1)'''
        self.query_fields['MR_USL_N_PRVS'] = '''IF(ActionType.serviceType IN
            (9, 4), ActionSpec.regionalCode,
            IFNULL(UslSpec.regionalCode, rbSpeciality.regionalCode))'''
        self.query_fields['MR_USL_N_CODE_MD_raw'] = '''IF(ActionType.serviceType IN
            (9, 4), ActionPerson.SNILS, IFNULL(UslPerson.SNILS, Person.SNILS))'''
        self.query_fields['USL_PODR'] = '''IF(ActionType.serviceType = 9,
            CONCAT(ReanimationOrgStructPODR.value, ReanimationOrgStructN_OTD.value),
            CONCAT(MovingOrgStructPODR.value, MovingOrgStructN_OTD.value))'''
        self.query_fields['USL_PROFIL'] = u'''IF(ActionType.serviceType = 9,  5, /*что за константа?*/
            MovingHBPMedicalAidProfile.code)'''
        self.query_fields['USL_PROFIL_KOIKI'] = ('IF(ActionType.serviceType = 9, '
            '10, MovingHBP.tfomsCode)')
        self.query_fields['USL_DATE_IN'] = 'CAST(IFNULL(Action.begDate, CsgAction.begDate) AS DATETIME)'
        self.query_fields['USL_DATE_OUT'] = 'CAST(IFNULL(Action.endDate, CsgAction.endDate) AS DATETIME)'
        self.query_fields['USL_DS1'] = """CASE
            WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN
              CASE
                WHEN (ActionMoving.MKB LIKE '') THEN Diagnosis.MKB
                ELSE ActionMoving.MKB
              END
            ELSE IFNULL(
              (CASE
                WHEN (ActionMoving.MKB LIKE '') THEN Diagnosis.MKB
                ELSE ActionMoving.MKB
              END), CsgAction.MKB)
          END"""
        self.query_fields['USL_TARIF'] = """CASE
            WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN 0
            ELSE Contract_Tariff.price
          END"""
        self.query_fields['USL_CODE_OPER'] = """CASE
            WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN rbService.code
            ELSE NULL
          END"""
        self.query_fields['serviceCode'] = 'rbService.code'
        self.query_fields['persAge'] = """TIMESTAMPDIFF(year,
            Client.birthDate,
            CASE
              WHEN (EventType.form = '110') THEN Event.execDate
              ELSE Event.setDate
            END)"""
        self.query_fields['actionEventCsgId'] = 'Action.eventCSG_id'
        self.query_fields['eventCsgMKB'] = 'ActionCSG.MKB'
        self.query_fields['duration'] = (
            'DATEDIFF(Event_CSG.endDate, Event_CSG.begDate)')
        self.query_fields['minDuration'] = 'mes.CSG.minDuration'
        self.query_fields['maxDuration'] = 'mes.CSG.maxDuration'
        self.query_fields['mesNote'] = 'mes.CSG.note'
        self.query_fields['USL_KD'] = 'ActionMoving.amount'
        self.query_fields['movingPersonId'] = 'ActionMoving.person_id'

        stmt = u"""/* -- СТАЦИОНАР (без ВМП) -- */
    SELECT {fields}
    FROM Account_Item
    {commonTables}
    LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
    LEFT JOIN `Action` AS ActionMoving ON ActionMoving.id = (
        SELECT MAX(A.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AT.deleted = 0
            AND AT.`flatCode` = 'moving' AND
            DATE_FORMAT(IFNULL(Action.begDate, CsgAction.begDate), '%Y-%m-%d %H:%i')
                >= DATE_FORMAT(A.begDate, '%Y-%m-%d %H:%i') AND
            DATE_FORMAT(IFNULL(IFNULL(Action.endDate, CsgAction.endDate),Event.execDate), '%Y-%m-%d %H:%i')
            <= DATE_FORMAT(A.endDate, '%Y-%m-%d %H:%i'))
    {actionTables}
    -- разное
    LEFT JOIN ActionType AS CsgActionType ON (CsgActionType.id = CsgAction.actionType_id)
    LEFT JOIN Event_CSG ON Event_CSG.id = (SELECT MAX(id)
                                         FROM Event_CSG AS E1
                                         WHERE E1.master_id = Event.id)
    LEFT JOIN Event_CSG AS ActionCSG ON (ActionCSG.id = Action.eventCSG_id)
    LEFT JOIN mes.CSG ON mes.CSG.id = (SELECT MAX(id)
                                     FROM mes.CSG AS CSG1
                                     WHERE CSG1.code = Event_CSG.CSGCode)
    WHERE Account_Item.reexposeItem_id IS NULL
        AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
        AND ((Account_Item.eventCSG_id IS NOT NULL AND CsgActionType.flatCode LIKE 'moving')
             OR (Account_Item.eventCSG_id IS NULL AND ActionType.flatCode NOT LIKE 'moving'))
        AND {idList}
    HAVING SLUCH_VIDPOM NOT LIKE '32' -- не ВМП
        AND rbEventTypePurpose.regionalCode = '1'
        AND (CASE
         WHEN (actionEventCsgId IS NOT NULL AND serviceType != 9) THEN (eventCsgMKB = USL_DS1)
         ELSE TRUE
       END)\n""".format(fields=self.prepare_query_field(), idList=idList,
                   commonTables=commonTables, actionTables=actionTables)
        return stmt


    def createStacVmpQuery(self, idList, commonTables, actionTables):
        self.addHmpFields()
        self.query_fields['MR_USL_N_PRVS'] = 'IFNULL(UslSpec.regionalCode, rbSpeciality.regionalCode)'
        self.query_fields['MR_USL_N_CODE_MD_raw'] = 'IFNULL(UslPerson.SNILS, Person.SNILS)'
        self.query_fields['SLUCH_P_CEL'] = None
        self.query_fields['USL_DATE_IN'] = 'CAST(IFNULL(Action.begDate,Event.setDate) AS DATETIME)'
        self.query_fields['USL_DATE_OUT'] = 'CAST(IFNULL(Action.endDate,Event.execDate) AS DATETIME)'
        self.query_fields['USL_DS1'] = 'Diagnosis.MKB'
        self.query_fields['USL_TARIF'] = 'Contract_Tariff.price'
        self.query_fields['actionEventCsgId'] = None
        self.query_fields['eventCsgMKB'] = None
        self.query_fields['duration'] = None
        self.query_fields['minDuration'] = None
        self.query_fields['maxDuration'] = None
        self.query_fields['mesNote'] = None
        self.query_fields['USL_KD'] = 'ActionMoving.amount'

        stmt = u"""/* -- СТАЦИОНАР (ВМП) -- */
    SELECT DISTINCT {fields}
    FROM Account_Item
    {commonTables}
    LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
    LEFT JOIN `Action` AS ActionMoving ON ActionMoving.id = (
        SELECT MAX(A.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AT.deleted = 0
            AND AT.`flatCode` = 'moving' AND
            (CAST(Event.setDate AS DATE ) >= CAST(A.begDate AS DATE) AND
             CAST(Event.execDate AS DATE) <= CAST(A.endDate AS DATE)))
    {actionTables}
    LEFT JOIN rbCureType ON rbCureType.id = Event.cureType_id
    LEFT JOIN rbCureMethod ON rbCureMethod.id = Event.cureMethod_id
    LEFT JOIN rbPatientModel ON rbPatientModel.id = Event.patientModel_id
    LEFT JOIN ActionProperty_Date AS TicketDate ON TicketDate.id = (
        SELECT AP.id FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_Date AS APD ON APD.id = AP.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND AT.`flatCode` LIKE 'talonVMP'
            AND APT.`name` LIKE 'Дата выдачи талона на ВМП'
        ORDER BY APD.value DESC
        LIMIT 0, 1)
    LEFT JOIN ActionProperty_Date AS TicketPlannedDate ON TicketPlannedDate.id = (
        SELECT AP.id FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_Date AS APD ON APD.id = AP.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND AT.`flatCode` LIKE 'talonVMP'
            AND APT.`name` LIKE 'Дата планируемой госпитализации'
        ORDER BY APD.value DESC
        LIMIT 0, 1)
    LEFT JOIN ActionProperty_String AS TicketNumber ON TicketNumber.id = (
        SELECT AP.id FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND AT.`flatCode` LIKE 'talonVMP'
            AND APT.`name` LIKE 'Номер талона на ВМП'
        LIMIT 0, 1)
    WHERE Account_Item.reexposeItem_id IS NULL
        AND rbEventTypePurpose.regionalCode = '1'
        AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
        AND {idList}
    HAVING SLUCH_VIDPOM LIKE '32' -- ВМП\n""".format(actionTables=actionTables,
            fields=self.prepare_query_field(), commonTables=commonTables,
            idList=idList)
        return stmt


    def createQuery(self):
        sysIdf003 = self._getAccSysId('f003')
        commonTables = u"""-- Common tables begin
    INNER JOIN Event ON Event.id = Account_Item.event_id
    -- PACIENT_*
    INNER JOIN Client ON Client.id = Event.client_id
    LEFT JOIN ClientPolicy ON
        ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate)
    LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
    LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    /*LEFT JOIN rbSocStatusType ON rbSocStatusType.id = (
        SELECT socStatusType_id FROM ClientSocStatus CSS
        WHERE CSS.client_id = Client.id AND CSS.deleted = 0
          AND CSS.socStatusClass_id = (
            SELECT rbSSC.id FROM rbSocStatusClass rbSSC
            WHERE rbSSC.code = '2' AND rbSSC.group_id IS NULL LIMIT 0,1)
        LIMIT 0, 1)*/
    -- SLUCH_*
    LEFT JOIN EventType ON EventType.id = Event.eventType_id
    LEFT JOIN Organisation AS RelegateOrg ON RelegateOrg.id = Event.relegateOrg_id
    LEFT JOIN Organisation_Identification AS RelegateOrgId ON (
        RelegateOrg.id = RelegateOrgId.master_id AND
        RelegateOrgId.deleted = 0 AND
        RelegateOrgId.system_id = '{sysIdf003}')
    LEFT JOIN Person ON Person.id = Event.execPerson_id
    LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
    LEFT JOIN ClientDocument ON ClientDocument.id = getClientDocumentId(Client.id)
    LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
    LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
    -- SLUCH_VIDPOM
    LEFT JOIN rbService ON rbService.id = Account_Item.service_id
    LEFT JOIN rbService_Profile ON rbService_Profile.id = (
        SELECT MAX(id) FROM rbService_Profile rs
        WHERE rs.master_id = rbService.id
          AND rs.speciality_id = Person.speciality_id)
    LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = IFNULL(
        rbService_Profile.medicalAidKind_id, IFNULL(
        rbService.medicalAidKind_id, EventType.medicalAidKind_id))
    --
    LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = IFNULL(
        rbService_Profile.medicalAidProfile_id, rbService.medicalAidProfile_id)
    LEFT JOIN rbSpeciality ON (rbSpeciality.id = Person.speciality_id)
    -- Диагнозы
    LEFT JOIN Diagnostic ON (Diagnostic.id = (
        SELECT MAX(dc.id) FROM Diagnostic dc
        WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0
          AND dc.diagnosisType_id IN (
            SELECT id FROM rbDiagnosisType
            WHERE code IN ('1', '2')))) -- заключительный, основной
    LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
        AND Diagnosis.deleted = 0
    LEFT JOIN mes.MES ON mes.MES.id = Event.MES_id
    LEFT JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id = mes.MES.group_id
    LEFT JOIN rbResult AS EventResult ON EventResult.id = Event.result_id
    LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = IFNULL(Account_Item.unit_id, (
        SELECT AI.unit_id FROM Account_Item AI
        WHERE AI.event_id = Event.id AND AI.unit_id IS NOT NULL LIMIT 0,1))
    LEFT JOIN rbDiseaseCharacter_Identification ON rbDiseaseCharacter_Identification.id = (
        SELECT MAX(DCI.id) FROM rbDiseaseCharacter_Identification AS DCI
        WHERE DCI.master_id = Diagnostic.character_id
          AND DCI.system_id = (
            SELECT id FROM rbAccountingSystem WHERE urn = 'urn:tfoms61:V027'))
    LEFT JOIN Action ON Action.id = Account_Item.action_id
    LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
    LEFT JOIN Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
    LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
    LEFT JOIN rbSpeciality AS ActionSpec ON ActionSpec.id = ActionPerson.speciality_id
    LEFT JOIN Action AS CsgAction ON CsgAction.eventCSG_id = Account_Item.eventCSG_id AND CsgAction.deleted = 0
    LEFT JOIN Account_Item AS ExposedAccountItem ON
        ExposedAccountItem.reexposeItem_id = Account_Item.id
    LEFT JOIN ActionType AS Crit ON Crit.id = (
        SELECT MAX(AT.id) FROM Action A
          INNER JOIN ActionType AT ON AT.id = A.actionType_id
        WHERE A.deleted = 0
          AND A.eventCSG_id = Account_Item.eventCSG_id
          AND AT.flatCode = 'CRIT')
    -- Common tables end (35 JOINS)""".format(sysIdf003=sysIdf003)

        actionTables = u'''-- Подразделение/Профиль для SLUCH
    LEFT JOIN `Action` AS ActionLeaved ON ActionLeaved.id = (
        SELECT MAX(A.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AT.`flatCode` = 'leaved'
        LIMIT 0, 1)
    LEFT JOIN ActionProperty_OrgStructure AS LeavedOrgStruct ON LeavedOrgStruct.id = (
        SELECT APOS.id
        FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_OrgStructure AS APOS ON APOS.id = AP.id
        WHERE A.id = ActionLeaved.id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND APT.`name` = 'Отделение'
        LIMIT 0, 1)
    LEFT JOIN ActionProperty_OrgStructure AS MovingOrgStruct ON MovingOrgStruct.id = (
        SELECT APOS.id
        FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_OrgStructure AS APOS ON APOS.id = AP.id
        WHERE A.id = ActionMoving.id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND APT.`name` LIKE 'Отделение пребывания'
        LIMIT 0, 1)
    LEFT JOIN OrgStructure_Identification AS LeavedOrgStructPODR ON
        LeavedOrgStructPODR.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = LeavedOrgStruct.value
              AND OI.deleted = 0
              AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'PODR'))
    LEFT JOIN OrgStructure_Identification AS LeavedOrgStructN_OTD ON
        LeavedOrgStructN_OTD.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = LeavedOrgStruct.value
              AND OI.deleted = 0
              AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'N_OTD'))
    LEFT JOIN OrgStructure_Identification AS LeavedOrgStructPROFIL ON
        LeavedOrgStructPROFIL.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = LeavedOrgStruct.value
              AND OI.deleted = 0
              AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'PROFIL'))
    LEFT JOIN rbMedicalAidProfile AS LeavedHBPProfile ON LeavedHBPProfile .id = (
        SELECT HBP.medicalAidProfile_id FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_rbHospitalBedProfile AS AHBP ON AHBP.id = AP.id
        INNER JOIN rbHospitalBedProfile HBP ON AHBP.value = HBP.id
        INNER JOIN rbMedicalAidProfile AS MAP ON MAP.id = HBP.medicalAidProfile_id
        WHERE A.id = ActionLeaved.id
            AND AP.deleted = 0
            AND APT.`name` = 'Профиль' AND APT.deleted = 0
        LIMIT 0, 1)
    LEFT JOIN rbHospitalBedProfile AS MovingHBP ON MovingHBP.id = (
        SELECT AHBP.value FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_rbHospitalBedProfile AS AHBP ON AHBP.id = AP.id
        WHERE A.id = ActionMoving.id
            AND AP.deleted = 0
            AND APT.`name` = 'Профиль' AND APT.deleted = 0
        LIMIT 0, 1)
    LEFT JOIN rbMedicalAidProfile AS MovingHBPMedicalAidProfile ON
        MovingHBPMedicalAidProfile.id = MovingHBP.medicalAidProfile_id
    LEFT JOIN OrgStructure_Identification AS MovingOrgStructPODR ON
         MovingOrgStructPODR.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = MovingOrgStruct.value
              AND OI.deleted = 0 AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'PODR'))
    LEFT JOIN OrgStructure_Identification AS MovingOrgStructN_OTD ON
         MovingOrgStructN_OTD.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = MovingOrgStruct.value
              AND OI.deleted = 0 AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'N_OTD'))
    LEFT JOIN ActionProperty_OrgStructure AS ReanimationOrgStruct ON ReanimationOrgStruct.id = (
        SELECT AP.id FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        WHERE A.deleted = 0 AND A.id = Account_Item.action_id
            AND AP.deleted = 0
            AND AT.serviceType = 9
            AND APT.`name` = 'Отделение пребывания'
        LIMIT 0, 1)
    LEFT JOIN OrgStructure_Identification AS ReanimationOrgStructPODR ON
        ReanimationOrgStructPODR.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = ReanimationOrgStruct.value
              AND OI.deleted = 0 AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'PODR'))
    LEFT JOIN OrgStructure_Identification AS ReanimationOrgStructN_OTD ON
        ReanimationOrgStructN_OTD.id = (SELECT id FROM OrgStructure_Identification OI
            WHERE OI.master_id = ReanimationOrgStruct.value
              AND OI.deleted = 0 AND OI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'N_OTD'))
    LEFT JOIN Person AS UslPerson ON UslPerson.id = ActionMoving.person_id
    LEFT JOIN rbSpeciality AS UslSpec ON UslSpec.id = UslPerson.speciality_id'''

        self.initFields()
        idList = self.tableAccountItem['id'].inlist(self.idList)
        sqlAmb = self.createAmbQuery(idList, commonTables)
        sqlStac = self.createStacQuery(idList, commonTables, actionTables)
        sqlStacVmp = self.createStacVmpQuery(idList, commonTables, actionTables)

        stmt = u"""{0} UNION ALL {1} UNION ALL {2}
            ORDER BY PACIENT_ID_PAC, eventId, SLUCH_USL_OK, USL_CODE_OPER,
                     serviceCode""".format(
                sqlAmb, sqlStac, sqlStacVmp)
        return self.db.query(stmt)


    def addHmpFields(self):
        self.query_fields['HMP_VID_HMP_raw'] = 'IF(rbCureType.code,rbCureType.code,0)'
        self.query_fields['HMP_METOD_HMP_raw'] = 'IF(rbCureMethod.code,rbCureMethod.code,0)'
        self.query_fields['HMP_HMODP'] = 'IF(rbPatientModel.code,rbPatientModel.code,0)'
        self.query_fields['HMP_TAL_D'] = 'DATE_FORMAT(TicketDate.value, "%Y-%m-%d")'
        self.query_fields['HMP_TAL_NUM'] = 'IFNULL(TicketNumber.value, ''00000000000000000000'')'
        self.query_fields['HMP_TAL_P'] = 'DATE_FORMAT(TicketPlannedDate.value, "%Y-%m-%d")'


    def preprocessQuery(self, query, params):
        # Некоторые услуги (блоки USL) необходимо объединять между собой по следующим признакам:
        #1. один и тот же МКБ или класс МКБ (первая буква);
        #2. один и тот же КСГ (указан в теге CODE_USL).
        result = {}

        while query.next():
            record = query.record()
            csgActionId = forceRef(record.value('csgActionId'))

            if not csgActionId:
                continue

            mkb = forceString(record.value('USL_DS1'))[:1]
            ksg = forceString(record.value('USL_CODE_USL'))
            eventId = forceRef(record.value('SLUCH_IDCASE'))
            dateIn = forceDate(record.value('USL_DATE_IN'))
            key = (eventId, mkb, ksg)
            val = (csgActionId, dateIn)
            if result.has_key(key):
                result[key].append(val)
            else:
                result[key] = [val]

        skipSet = set()
        replaceBegDate = {}
        for val in result.values():
            if len(val) > 1:
                val.sort(key=itemgetter(1))
                (id, begDate) = val[0]
                skipSet.add(id)
                (id, _) = val[-1]
                replaceBegDate[id] = begDate

        query.exec_()
        params['skipSet'] = skipSet
        params['replaceBegDate'] = replaceBegDate


    def getAddr(self, idList):
        stmt = u'''SELECT Event.client_id AS clientId,
            CASE SUBSTRING(RegKLADR.OCATD, 1, 2)
                WHEN '60' THEN RegKLADR.OCATD
                WHEN '' THEN ''
                ELSE CONCAT(SUBSTRING(RegKLADR.OCATD, 1, 2), '000000000')
            END AS PERS_OKATOG,
            CASE SUBSTRING(LocKLADR.OCATD, 1, 2)
                WHEN '60' THEN LocKLADR.OCATD
                WHEN '' THEN ''
                ELSE CONCAT(SUBSTRING(LocKLADR.OCATD, 1, 2), '000000000')
            END AS PERS_OKATOP,
            CASE
                WHEN ((RegAddressHouse.KLADRCode IS NULL OR RegAddressHouse.KLADRCode = '') AND
                            (ClientRegAddress.freeInput IS NULL OR ClientRegAddress.freeInput = '')) THEN 1
                ELSE 0
            END AS isAddressError, -- для детектирования отсутствия адреса
            CASE
                WHEN (RegAddressHouse.KLADRStreetCode IS NULL OR RegAddressHouse.KLADRStreetCode LIKE '') THEN ClientRegAddress.freeInput
                ELSE formatClientAddress(ClientRegAddress.id)
            END  AS PERS_ADRES,
            RPAD(
            (CASE
              WHEN (RegAddressHouse.KLADRStreetCode IS NULL OR RegAddressHouse.KLADRStreetCode LIKE '') THEN RegAddressHouse.KLADRCode
              ELSE RegAddressHouse.KLADRStreetCode
            END), 17, '0') AS PERS_KLADR,
            CASE
                WHEN (RegAddressHouse.id) THEN RegAddressHouse.number
                ELSE LocAddressHouse.number
            END AS PERS_DOM,
            CASE
                WHEN (RegAddressHouse.id) THEN RegAddress.flat
                ELSE LocAddress.flat
            END AS PERS_KVART,
            CASE
                WHEN (RegAddressHouse.id) THEN RegAddressHouse.corpus
                ELSE LocAddressHouse.corpus
            END AS PERS_KORP
    FROM Account_Item
    INNER JOIN Event ON Event.id = Account_Item.event_id
    INNER JOIN Client ON Client.id = Event.client_id
    LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id

    LEFT JOIN ClientAddress AS ClientRegAddress ON (ClientRegAddress.id  = getClientRegAddressId(Client.id))
    LEFT JOIN Address AS RegAddress ON (RegAddress.id = ClientRegAddress.address_id)
    LEFT JOIN AddressHouse RegAddressHouse ON (RegAddressHouse.id = RegAddress.house_id)
    LEFT JOIN kladr.KLADR AS RegKLADR ON (RegKLADR.CODE = RegAddressHouse.KLADRCode)

    LEFT JOIN ClientAddress AS ClientLocAddress ON (ClientLocAddress.id  = getClientLocAddressId(Client.id))
    LEFT JOIN Address AS LocAddress ON (LocAddress.id = ClientLocAddress.address_id)
    LEFT JOIN AddressHouse LocAddressHouse ON (LocAddressHouse.id = LocAddress.house_id)
    LEFT JOIN kladr.KLADR AS LocKLADR ON (LocKLADR.CODE = LocAddressHouse.KLADRCode)
    WHERE Account_Item.reexposeItem_id IS NULL
        AND (Account_Item.date IS NULL OR
             (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
        AND {idList}'''.format(idList=idList)
        query = QtGui.qApp.db.query(stmt)

        while query.next():
            record = query.record()
            clientId = forceRef(record.value('clientId'))
            result = {
                'PERS_OKATOG': forceString(record.value('PERS_OKATOG')),
                'PERS_OKATOP': forceString(record.value('PERS_OKATOP')),
                'isAddressError': forceInt(record.value('isAddressError')),
                'PERS_ADRES': forceString(record.value('PERS_ADRES')),
                'PERS_KLADR': forceString(record.value('PERS_KLADR')),
                'PERS_DOM': forceString(record.value('PERS_DOM')),
                'PERS_KVART': forceString(record.value('PERS_KVART')),
                'PERS_KORP': forceString(record.value('PERS_KORP')),
            }
            yield clientId, result


    def visitInfo(self, idList):
        u"""Экспортирует данные для визитов с 0 стоимостью,
            при тарификации по посещениям"""
        stmt = u"""SELECT
            Visit.event_id AS eventId,
            Diagnosis.MKB AS USL_DS1,
            rbSpeciality.regionalCode AS MR_USL_N_PRVS,
            CAST(Visit.date AS DATETIME) AS USL_DATE_IN,
            CAST(Visit.date AS DATETIME) AS USL_DATE_OUT,
            SUBSTR(rbService.code, 1, 4) AS USL_PODR,
             IF(mes.mrbMESGroup.code = 'ДиспаснС', '',
                IF(rbService_Profile.medicalAidProfile_id IS NOT NULL, ServiceProfileMedicalAidProfile.code,
                 ServiceMedicalAidProfile.code)) AS USL_PROFIL,
            IF(age(Client.birthDate,Event.setDate) < 18 AND rbSpeciality.code IN ('22', '81'), 1, 0) AS USL_DET,
            CAST(IF(EventType.form = '110', Event.execDate, Event.setDate) AS DATE) AS USL_DATE_1,
            RPAD(SUBSTR(rbService.code,1, 4), 11, '0') AS USL_CODE_USL,
            IF(mes.mrbMESGroup.code = 'ДиспаснС', '', 1) AS USL_KOL_USL,
            IF(rbService.code LIKE 'A16%%', rbService.code, '') AS USL_CODE_OPER,
            0 AS USL_SK_KOEF,
            0 AS USL_SUMV_USL,
            0 AS USL_TARIF,
            VisitPerson.SNILS AS MR_USL_N_CODE_MD_raw
        FROM Visit
        LEFT JOIN Event ON Event.id = Visit.event_id
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Event.id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                  AND Diagnostic.deleted = 0 )
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
        LEFT JOIN Person ON Person.id = Event.execPerson_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON Visit.service_id = rbService.id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
        LEFT JOIN mes.mrbMESGroup ON mes.MES.group_id = mes.mrbMESGroup.id
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        WHERE Visit.event_id IN (
            SELECT event_id FROM Account_Item
            LEFT JOIN rbPayRefuseType ON
                rbPayRefuseType.id = Account_Item.refuseType_id
            WHERE Account_Item.reexposeItem_id IS NULL
              AND (Account_Item.date IS NULL OR
                (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
              AND {idList})
          AND Visit.deleted = '0'""".format(idList=idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result.setdefault(eventId, []).append(record)

        return result


    def exportInt(self):
        params  = { 'MR_USL_N_MR_N': 1 }
        items = self.tableAccountItem['id'].inlist(self.idList)
        self.setStatus(u'Запрос данных посещений...')
        params['visitInfo'] = self.visitInfo(items)
        self.setStatus(u'Запрос адресов клиентов...')
        params['clientAddr'] = dict(self.getAddr(items))
        for msg, name, _class in (
                (u'Запрос данных онкологии...',
                 'onkologyInfo',  CR61OnkologyInfo),
                (u'Запрос данных мед.препаратов...',
                 'medicalSuppliesInfo',  CMedicalSuppliesInfo),
                (u'Запрос данных об имплантации...',
                 'implantsInfo',  CImplantsInfo)):
            self.setStatus(msg)
            val = _class()
            params[name] = val.get(self.db, items, self)
        self.setProcessParams(params)
        COrder79ExportPage1.exportInt(self)


    def setStatus(self, msg):
        self.log(msg)
        self.progressBar.setText(msg)
        QtGui.qApp.processEvents()

# ******************************************************************************

class CExportXmlStreamWriter(COrder79XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR', 'STAT_Z')

    eventDateFields1 = ('DATE_1', 'DATE_2')
    eventDateFields2 = ('NAPDAT',)
    eventFields1 = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'P_CEL', 'HMP',
                   'NAPR_FROM',  'PODR', 'LPU',
                   'PROFIL', 'DET', 'NHISTORY') +  eventDateFields1 + ('DS1',
                   'DS2', 'DS3', 'C_ZAB', 'RSLT', 'ISHOD', 'PRVS', 'VERS_SPEC',
                   'IDDOKT', 'OS_SLUCH', 'IDSP', 'SUMV', 'OPLATA', 'SUMP', 'SANK_IT',
                   'NSVOD', 'KODLPU', 'PRNES', 'KD_Z', 'PCHAST', 'VBR',
                   'CODE_FKSG', 'PR_MO', 'VB_P', 'USL')
    eventFields2 = ('DS_ONK', 'NAPR', 'CONS', 'ONK_SL')
    eventFields = eventFields1 + eventFields2

    naprFields = ('NAPR_DATE', 'NAPR_MO', 'NAPR_LPU', 'NAPR_V',
                            'MET_ISSL', 'NAPR_USL')

    onkSlFields = ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M', 'MTSTZ', 'SOD',
                   'K_FR', 'WEI', 'HEI', 'BSA', 'B_DIAG', 'B_PROT', 'ONK_USL')

    consFields = ('PR_CONS', 'DT_CONS')
    consDateFields = ('DT_CONS', )
    ksgKpgFields = ('N_KSG', 'VER_KSG', 'KSG_PG', 'KOEF_Z', 'KOEF_UP', 'BZTSZ',
                    'KOEF_D', 'KOEF_U')

    medicalSuppliesDoseGroup = {
        'LEK_DOSE': {
            'fields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'requiredFields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'prefix': 'COVID_LEK_LEK_PR',
        },
    }

    medicalSuppliesGroup = {
        'LEK_PR': { 'fields': ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK',
                               'LEK_DOSE'),
                    'dateFields': ('DATA_INJ', ),
                    'requiredFields': ('DATA_INJ', 'CODE_SH'),
                    'prefix': 'COVID_LEK',
                    'subGroup': medicalSuppliesDoseGroup,  }
    }

    serviceSubGroup = {
        'SL_KOEF': {'fields': ('IDSL', 'Z_SL')},
        'KSG_KPG': {'fields': ksgKpgFields},
        'COVID_LEK': {'fields': ('WEI', 'LEK_PR'),
                      'subGroup': medicalSuppliesGroup },
        'MED_DEV': {
            'fields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'),
            'dateFields': ('DATE_MED', ),
            'requiredFields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'), },
        'MR_USL_N':{
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    naprFromFields = ('NPR_MO', 'NAPUCH', 'NOM_NAP', 'NAPDAT')

    onkUslSubGroup = {
        'LEK_PR': {'fields': ('REGNUM', 'CODE_SH', 'DATE_INJ'),
                   'dateFields': ('DATE_INJ', )},
    }

    onkSlSubGroup = {
        'ONK_USL': {'fields': ('NOM_USL', 'IDS_USL', 'USL_TIP', 'HIR_TIP',
                               'LEK_TIP_L', 'LEK_TIP_V', 'LEK_PR', 'PPTR',
                               'LUCH_TIP'),
                    'subGroup': onkUslSubGroup },
        'B_DIAG': {'fields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE1',
                              'DIAG_CODE2', 'DIAG_RSLT1', 'DIAG_RSLT2',
                              'REC_RSLT')},
        'B_PROT': {'fields': ('PROT', 'D_PROT')}
    }

    eventSubGroup1 = {
        'HMP': {'fields': ('VID_HMP', 'METOD_HMP', 'HMODP', 'TAL_D', 'TAL_NUM',
                           'TAL_P', 'NPR_MO', 'EXTR')},
        'NAPR_FROM': {'fields': naprFromFields, 'dateFields': ('NAPDAT', )},
    }

    eventSubGroup2 = {
        'CONS': {'fields': consFields},
        'NAPR': {'fields': naprFields},
        'ONK_SL': {'fields': onkSlFields,
                            'subGroup': onkSlSubGroup},
    }

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'IDMASTER', 'LPU', 'PODR', 'PROFIL',
                      'PROFIL_KOIKI', 'P_PER', 'CRIT', 'DET', 'NPL')  +
                     serviceDateFields +
                     ('KD', 'DS1', 'DS2', 'DS3', 'CODE_USL', 'KOL_USL',
                      'KSG_KPG', 'TARIF',
                      'SUMV_USL', 'SL_K', 'IT_SL', 'SL_KOEF', 'SK_KOEF',
                      'COVID_LEK', 'MED_DEV', 'MR_USL_N', 'NAPR', 'ONK_USL',
                      'KODLPU', 'KSGA', 'CODE_OPER'))

    mapRecFrom = {
        u'Поликлиника': '1',
        u'Самотек': '1',
        u'Другие': '1',
        u'Скорая помощь': '2',
        u'Перевод из ЛПУ': '3',
        u'Санавиация': '3',
    }

    MAP_IDSL_CODE = {
        u'КСЛП006': '6', u'КСЛП6.1': '6', u'КСЛП007': '7', u'КСЛП7.1': '7',
        u'КСЛП008': '8', u'КСЛП8.1': '8', u'КСЛП009': '9', u'КСЛП9.1': '9',
        u'КСЛП010': '10', u'КСЛП10.1': '10', u'КСЛП005': '5',
        u'КСЛП011': '1', u'КСЛП012': '2', u'КСЛП013': '12',
    }

    MAP_IDSL_VAL = {
        u'КСЛП006': '0.05', u'КСЛП6.1': '0.05', u'КСЛП007': '0.47',
        u'КСЛП7.1': '0.47', u'КСЛП008': '1.16', u'КСЛП8.1': '1.16',
        u'КСЛП009': '2.07', u'КСЛП9.1': '2.07', u'КСЛП010': '3.49',
        u'КСЛП10.1': '3.49', u'КСЛП005': '0.6', u'КСЛП011': '0.2',
        u'КСЛ0П12': '0.6', u'КСЛП013': '0.63',
    }

    def __init__(self, parent, version='2.1'):
        COrder79XmlStreamWriter.__init__(self, parent, version=VERSION)
        self.sluchDate1 = None
        self.sluchDate1_uslCheck = False
        self.sluchDate2 = None
        self.sluchDate2_uslCheck = False
        self.lastEventId = None
        self.lastUslOk = None
        self.eventGroup = CExportR61EventGroup(self)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        self.startDate = QDate(settleDate.year(), settleDate.month(), 1)
        params['USL_LPU'] = params['lpuMiacCode']
        params['SLUCH_LPU'] = u'510%s' % params['lpuCode']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', self.version)
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', forceString(self._parent.getEventCount()))
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuMiacCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', params['NSCHET'])
        self.writeTextElement('DSCHET', settleDate.toString(Qt.ISODate))
        self.writeTextElement('SUMMAV', '{0:.2f}'.format(params['accSum']))
        self.writeTextElement('SUMMAP', '0.00')
        self.writeEndElement() # SCHET


    def checkerClientInfo(self, record):
        clientId = forceInt(record.value('PACIENT_ID_PAC'))

        if forceString(record.value('PERS_OT')) == '':
            self._parent.logWarning(u'Пациент %d: не указано отчество! Тег заполнится значением "НЕТ".' % (clientId))
            record.setValue('PERS_OT', u'НЕТ')

        self.checkElement(clientId, 'VPOLIS', forceString(record.value('PACIENT_VPOLIS')), 1, optional=True, isClientInfo=True)
        # если задействован не действующий полис (кроме временного)...
        if (forceInt(record.value('isActualPolicy')) == 0 and forceInt(record.value('PACIENT_VPOLIS')) != 2):
            self._parent.logWarning(u'Пациент %d: использован недействительный полис на момент обращения' % (clientId))
            # данные заполняются нулями
            record.setValue('PACIENT_SPOLIS', '0000000000')
            record.setValue('PACIENT_NPOLIS', '00000000000000000000')
        else:
            self.checkElement(clientId, 'SPOLIS', forceString(record.value('PACIENT_SPOLIS')), 10, optional=True, isClientInfo=True)
            self.checkElement(clientId, 'NPOLIS', forceString(record.value('PACIENT_NPOLIS')), 20, optional=True, isClientInfo=True)
        self.checkElement(clientId, 'SMO', forceString(record.value('PACIENT_SMO')), 5, optional=True, isClientInfo=True)
        self.checkElement(clientId, 'SMO_OGRN', forceString(record.value('PACIENT_SMO_OGRN')), 15, optional=True, isClientInfo=True)
        # Вопреки спецификации, ТФОМС РО позволяет вносить в этот тег до 11 символов. Поясняли устно ссылаясь на спеку.
        # В спеке ничего подобного не найдено.
        self.checkElement(clientId, 'SMO_OK', forceString(record.value('PACIENT_SMO_OK')), 11, optional=True, isClientInfo=True)
        self.checkElement(clientId, 'SMO_NAM', forceString(record.value('PACIENT_SMO_NAM')), 100, optional=True, isClientInfo=True)
        self.checkElement(clientId, 'NOVOR', forceString(record.value('PACIENT_NOVOR')), 9, isClientInfo=True)
        self.checkElement(clientId, 'STAT_Z', forceString(record.value('PACIENT_STAT_Z')), 1, isClientInfo=True)

        if forceInt(record.value('PACIENT_VPOLIS')) != 3:
            self.checkFill(clientId, 'DOCDATE', forceString(record.value('PERS_DOCDATE')), isClientInfo=True)
            self.checkFill(clientId, 'DOCORG', forceString(record.value('PERS_DOCORG')), isClientInfo=True)


    def checkerEventInfo(self, record):
        if self.lastEventId:
            if not self.sluchDate1_uslCheck:
                self._parent.logError(u'Обращение %d%s: дата начала случая не соответствует минимальной дате услуг'
                                      % (self.lastEventId, (u'(С)' if self.lastUslOk == 1 else u'(П)')))
            if not self.sluchDate2_uslCheck:
                self._parent.logError(u'Обращение %d%s: дата окончания случая не соответствует максимальной дате услуг'
                                      % (self.lastEventId, (u'(С)' if self.lastUslOk == 1 else u'(П)')))

        eventId = forceInt(record.value('eventId'))
        self.lastEventId = eventId
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        self.lastUslOk = uslOk
        suffix = (u'(С)' if uslOk == 1 else u'(П)')
        vidPom = forceString(record.value('SLUCH_VIDPOM'))
        self.checkElement(eventId, 'VIDPOM', vidPom, 4, suffix=suffix)
        self.checkElement(eventId, 'FOR_POM', forceString(record.value('SLUCH_FOR_POM')), 1, suffix=suffix)

        if uslOk == 1 and vidPom == '32': # только для ВМП
            self.checkElement(eventId, 'VID_HMP', forceString(record.value('HMP_VID_HMP')), 12, suffix=suffix)
            self.checkElement(eventId, 'METOD_HMP', forceString(record.value('HMP_METOD_HMP')), 4, suffix=suffix)
            self.checkFill (eventId, 'TAL_D', forceString(record.value('HMP_TAL_D')), suffix=suffix)
            self.checkElement(eventId, 'TAL_NUM', forceString(record.value('HMP_TAL_NUM')), 20, suffix=suffix)
            if forceString(record.value('HMP_TAL_NUM')) == '00000000000000000000':
                self._parent.logWarning(u'Обращение %d%s: TAL_NUM было не заполнено!' % (eventId, suffix))
            self.checkFill (eventId, 'TAL_P', forceString(record.value('HMP_TAL_P')), suffix=suffix)
        # Тег "NPR_MO" для МО "Министерство здравоохранения Ростовской области" (5610099) не заполняется - это исключение.
        napuch = forceString(record.value('NAPR_FROM_NAPUCH'))
        if (self.checkElement(eventId, 'NAPUCH', napuch, 7, suffix=suffix)):
            if napuch != '5610099':
                self.checkElement(eventId, 'NPR_MO', forceString(record.value('NAPR_FROM_NPR_MO')), 6, suffix=suffix)
        if uslOk == 1:
            self.checkElement(eventId, 'EXTR', forceString(record.value('SLUCH_EXTR')), 2, suffix=suffix)
        if not self.checkElement(eventId, 'PODR', forceString(record.value('SLUCH_PODR')), 8, suffix=suffix):
            record.setValue('SLUCH_PODR', '0')
        if not self.checkElement(eventId, 'LPU', forceString(record.value('SLUCH_LPU')), 6, suffix=suffix):
            record.setValue('SLUCH_LPU', '0')
        self.checkElement(eventId, 'PROFIL', forceString(record.value('SLUCH_PROFIL')), 3, suffix=suffix)
        self.checkElement(eventId, 'DET', forceString(record.value('SLUCH_DET')), 1, suffix=suffix)
        self.checkElement(eventId, 'NHISTORY', forceString(record.value('SLUCH_NHISTORY')), 50, suffix=suffix)
        self.checkElement(eventId, 'P_PER', forceString(record.value('USL_P_PER')), 1, optional=True, suffix=suffix)
        self.checkFill(eventId, 'DATE_1', forceString(record.value('SLUCH_DATE_1')), suffix=suffix)
        self.sluchDate1 = forceDate(record.value('SLUCH_DATE_1')).toPyDate()
        self.sluchDate1_uslCheck = False
        self.checkFill(eventId, 'DATE_2', forceString(record.value('SLUCH_DATE_2')), suffix=suffix)
        self.sluchDate2 = forceDate(record.value('SLUCH_DATE_2')).toPyDate()
        self.sluchDate2_uslCheck = False
        self.checkElement(eventId, 'DS1', forceString(record.value('SLUCH_DS1')), 10, suffix=suffix)

        for mkb in forceString(record.value('SLUCH_DS2')).split(','):
            self.checkElement(eventId, 'DS2', mkb, 10, optional=True,
                              suffix=suffix)

        self.checkElement(eventId, 'RSLT', forceString(record.value('SLUCH_RSLT')), 3, suffix=suffix)
        self.checkElement(eventId, 'ISHOD', forceString(record.value('SLUCH_ISHOD')), 3, suffix=suffix)
        self.checkElement(eventId, 'PRVS', forceString(record.value('SLUCH_PRVS')), 4, suffix=suffix)
        if (forceString(record.value('SLUCH_PRVS')) == '0'):
            self._parent.logError(u'Обращение %d%s: PRVS не может быть \'0\'!' % (eventId, suffix))
        self.checkElement(eventId, 'IDDOKT', forceString(record.value('SLUCH_IDDOKT')), 25, suffix=suffix)
        self.checkElement(eventId, 'OS_SLUCH', forceString(record.value('SLUCH_OS_SLUCH')), 1, optional=True, suffix=suffix)
        #self.checkElement(eventId, 'IDSP', forceString(record.value('SLUCH_IDSP')), 2, suffix=suffix)
        self.checkFill(eventId, 'SUMV', forceString(record.value('SLUCH_SUMV')), suffix=suffix)
        self.checkElement(eventId, 'NSVOD', forceString(record.value('SLUCH_NSVOD')), 3, suffix=suffix)
        self.checkElement(eventId, 'KODLPU', forceString(record.value('SLUCH_KODLPU')), 7, suffix=suffix)
        self.checkElement(eventId, 'PRNES', forceString(record.value('SLUCH_PRNES')), 1, optional=True, suffix=suffix)
        if uslOk == 1:
            self.checkElement(eventId, 'KD_Z', forceString(record.value('SLUCH_KD_Z')), 3, suffix=suffix)
        self.checkElement(eventId, 'PCHAST', forceString(record.value('SLUCH_PCHAST')), 1, suffix=suffix)
        if uslOk == 3:
            self.checkElement(eventId, 'VBR', forceString(record.value('SLUCH_VBR')), 1, suffix=suffix)
        self.checkElement(eventId, 'C_ZAB', forceString(record.value('SLUCH_C_ZAB')), 1, suffix=suffix)

        for mkb in forceString(record.value('SLUCH_DS3')).split(','):
            self.checkElement(eventId, 'DS3', mkb, 10, optional=True,
                              suffix=suffix)

        self.checkElement(eventId, 'NOM_NAP', forceString(record.value('NAPR_FROM_NOM_NAP')), 16, suffix=suffix)
        strNomNap = forceString(record.value('NAPR_FROM_NOM_NAP'))
        strForPom = forceString(record.value('SLUCH_FOR_POM'))
        if uslOk == 1 and len(strNomNap) < 16 and not strNomNap.startswith('0') and strForPom != '1':
            self._parent.logError(u'Обращение %d%s: некорректный NOM_NAP: \'%s\'' % (eventId, suffix, strNomNap))
        self.checkFill(eventId, 'NAPDAT', forceString(record.value('NAPR_FROM_NAPDAT')), suffix=suffix)
        self.checkElement(eventId, 'CODE_FKSG', forceString(record.value('SLUCH_CODE_FKSG')), 40, optional=True, suffix=suffix)

        self.checkFill(eventId, 'SUMV', forceString(record.value('SLUCH_SUMV')), suffix=suffix)


    def checkerService(self, record):
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        suffix = (u'(С)' if uslOk == 1 else u'(П)')
        eventId = forceInt(record.value('eventId'))
        idServ = forceInt(record.value('USL_IDSERV'))
        isDiagnostic = forceBool(record.value('isDiagnostic'))
        # self.checkElement(eventId, 'IDMASTER', forceString(record.value('USL_IDMASTER')), 36, idServ)
        self.checkElement(eventId, 'LPU', forceString(record.value('USL_LPU')), 6, idServ, suffix=suffix)
        if not self.checkElement(eventId, 'PODR', forceString(record.value('USL_PODR')), 8, idServ, suffix=suffix):
            record.setValue('USL_PODR', '0') # по просьбе РОКБ: если тег пустой(что является ошибкой), то заполнять его нулем
        if not self.checkElement(eventId, 'PROFIL', forceString(record.value('USL_PROFIL')), 3, idServ, suffix=suffix):
            record.setValue('USL_PROFIL', '0')  # (тоже самое, что и выше)
        self.checkElement(eventId, 'DET', forceString(record.value('USL_DET')), 1, idServ, suffix=suffix)
        if self.checkFill(eventId, 'DATE_IN', forceString(record.value('USL_DATE_IN')), idServ, suffix=suffix):
            uslDate = forceDate(record.value('USL_DATE_IN')).toPyDate()
            if isDiagnostic:
                self.sluchDate1_uslCheck = True
            elif uslDate < self.sluchDate1 :
                self._parent.logError(
                    u'Обращение %d%s, услуга %d: дата начала услуги меньше даты начала случая (%s &lt; %s)' % (
                    eventId, suffix, idServ, uslDate, self.sluchDate1))
            elif uslDate > self.sluchDate2:
                self._parent.logError(
                    u'Обращение %d%s, услуга %d: дата начала услуги больше даты окончания случая (%s &gt; %s)' % (
                    eventId, suffix, idServ, uslDate, self.sluchDate2))
            elif not self.sluchDate1_uslCheck and uslDate == self.sluchDate1:
                self.sluchDate1_uslCheck = True
        if self.checkFill(eventId, 'DATE_OUT', forceString(record.value('USL_DATE_OUT')), idServ, suffix=suffix):
            uslDate = forceDate(record.value('USL_DATE_OUT')).toPyDate()
            if isDiagnostic:
                self.sluchDate2_uslCheck = True
            elif uslDate < self.sluchDate1:
                self._parent.logError(
                    u'Обращение %d%s, услуга %d: дата окончания услуги меньше даты начала случая (%s &lt; %s)' % (
                    eventId, suffix, idServ, uslDate, self.sluchDate1))
            elif uslDate > self.sluchDate2:
                self._parent.logError(
                    u'Обращение %d%s, услуга %d: дата окончания услуги больше даты окончания случая (%s &gt; %s)' % (
                    eventId, suffix, idServ, uslDate, self.sluchDate2))
            elif not self.sluchDate2_uslCheck and uslDate == self.sluchDate2:
                self.sluchDate2_uslCheck = True
        if uslOk == 1 and forceString(record.value('USL_CODE_OPER')) == '':
            self.checkFill(eventId, 'KD', forceString(record.value('USL_KD')), idServ, suffix=suffix)
        isMainService = forceString(record.value('USL_CODE_USL')) != '' and forceInt(record.value('USL_TARIF')) != 0
        if uslOk != 3 and isMainService:
            self.checkFill(eventId, 'KD', forceInt(record.value('USL_KD')), idServ, suffix=suffix)
        self.checkElement(eventId, 'DS1', forceString(record.value('USL_DS1')),
                          10, idServ, suffix=suffix)
        self.checkElement(eventId, 'CODE_USL', forceString(record.value('USL_CODE_USL')), 20, idServ, suffix=suffix)
        self.checkElement(eventId, 'KOL_USL', forceString(record.value('USL_KOL_USL')), 6, idServ, suffix=suffix)
        self.checkFill(eventId, 'TARIF', forceString(record.value('USL_TARIF')), idServ, suffix=suffix)
        self.checkFill(eventId, 'SUMV_USL', forceString(record.value('USL_SUMV_USL')), idServ, suffix=suffix)
        self.checkElement(eventId, 'PRVS', forceString(record.value('MR_USL_N_PRVS')), 4, idServ, suffix=suffix)
        self.checkElement(eventId, 'CODE_MD', forceString(record.value('MR_USL_N_CODE_MD')), 25, idServ, suffix=suffix)
        self.checkElement(eventId, 'KODLPU', forceString(record.value('USL_KODLPU')), 7, idServ, suffix=suffix)
        self.checkElement(eventId, 'CODE_OPER', forceString(record.value('USL_CODE_OPER')), 16, idServ, optional=True, suffix=suffix)
        self.checkElement(eventId, 'CRIT', forceString(record.value('USL_CRIT')),  10,  idServ, optional=True, suffix=suffix)


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))

        # если дата окончания случая за пределами отчетного периода (начала текущего месяца)
        # то данный случай является "дополнительным"
        date2 = forceDate(record.value('SLUCH_DATE_2'))
        if hasattr(self, 'startDate') and date2 < self.startDate:
            prNov = '1'
        else:
            prNov = forceString(record.value('isExposedItem'))

        changedPrNov = (prNov != params.setdefault('lastPrNov'))

        if (clientId != params.setdefault('lastClientId')) or changedPrNov:
            if params['lastClientId'] or params['lastPrNov']:
                self.eventGroup.clear(self, params)
                self.writeEndElement() # SLUCH
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['N_ZAP']))
            self.writeTextElement('PR_NOV', prNov)

            clientAddrInfo = params['clientAddr'].get(clientId, {})
            params.update(clientAddrInfo)
            isAddressError = params['isAddressError']

            if isAddressError:
                self._parent.logError(
                    u'У пациента %s %s %s (%d) не заполнен адрес' %
                    (forceString(record.value('PERS_FAM')),
                     forceString(record.value('PERS_IM')),
                     forceString(record.value('PERS_OT')),
                     clientId))
                self.abort()

            self.writeClientInfo(record, params)

            params['N_ZAP'] += 1
            params['lastClientId'] = clientId
            params['lastPrNov'] = prNov
            params['lastEventId'] = None

        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def generateCorrectNomNap(self, nom_nap, napuch, year):
        if nom_nap.startswith('0'):
            for i in range(len(nom_nap)):
                if nom_nap[i] != '0':
                    nom_nap = nom_nap[i:]
                    c = 16 - len(napuch) - len(year) - len(nom_nap)
                    if c < 0:
                        return '%s%s%s' % (napuch, year, nom_nap)
                    else:
                        return ('%s%s%0'+str(c)+'d%s') % (napuch, year, 0, nom_nap)
        else:
            return nom_nap

    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        execDate = forceDate(record.value('SLUCH_DATE_2'))
        eventPurposeCode = forceString(record.value(
                'eventPurposeCode'))
        patrName = forceString(record.value('PERS_OT'))
        haveMoving = self.__haveMoving(eventId)
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        cureTypeCode = forceString(record.value('HMP_VID_HMP_raw'))
        vidpom = forceString(record.value('SLUCH_VIDPOM'))
        isDiagnostic = forceBool(record.value('isDiagnostic'))

        local_params = {
            'SLUCH_OS_SLUCH': '2' if (not patrName or
                                      patrName.upper() == u'НЕТ') else '',
            'SLUCH_VERS_SPEC': 'V021',
            'SLUCH_OPLATA': '0',
            'SLUCH_SUMP': '0',
            'SLUCH_SANK_IT': '0',
            'SLUCH_NSVOD': '%s%02d' % (eventPurposeCode[:1],
                    execDate.month()),
            'SLUCH_KODLPU': params['lpuCode'],
            'SLUCH_PRNES': '0' if haveMoving else None,
            'SLUCH_PCHAST': '0',
            'SLUCH_IDDOKT': formatSNILS(forceString(record.value(
                'SLUCH_IDDOKT_raw'))),
            'SLUCH_PR_MO': '0',
            'SLUCH_FOR_POM': self.mapEventOrderToForPom.get(
                forceString(record.value('eventOrder')), ''),
            'SLUCH_DS_ONK': '0',
            'SLUCH_DS2':  self.__getServiceDS2(eventId),
            'SLUCH_DS3': self.__getServiceDS3(eventId),
        }

        resultId = forceRef(record.value('SLUCH_ISHOD'))
        if resultId:
            record.setValue('SLUCH_ISHOD', self.__resultCode(resultId))

        if uslOk == 3:
            local_params['SLUCH_VBR'] = '0'

        # если тег PRZAB пустой, выводить 0
        if not forceString(record.value('SLUCH_PRZAB')):
            record.setValue('SLUCH_PRZAB', '0')

        if uslOk == 1 and vidpom == '32': # если это стационар
            local_params['HMP_METOD_HMP'] = forceString(
                                              record.value('HMP_METOD_HMP_raw'))
            local_params['HMP_VID_HMP'] = cureTypeCode

            if forceString(record.value('USL_CODE_OPER')):
                record.setValue('USL_KOL_USL', '1')

        if uslOk == 1: # если это стационар
            record.setValue('NAPR_FROM_NOM_NAP', self.generateCorrectNomNap(
                forceString(record.value('NAPR_FROM_NOM_NAP')),
                forceString(record.value('NAPR_FROM_NAPUCH')),
                forceDate(record.value('NAPR_FROM_NAPDAT')).toString('yy')
            ))

            if vidpom != '32':
                fskgList = params['mapEventIdToFksgCode'].get(eventId, '').split(';')
                local_params['SLUCH_CODE_FKSG'] = ';'.join(x for x in fskgList if x[:2] == 'st')
            else:
                record.setValue('serviceCode', '')
            local_params['SLUCH_DOPL'] = ''
            # дабы уменьшить размеры SQL запроса, SLUCH_KD_Z расчитывается здесь
            delta = forceDate(record.value('SLUCH_DATE_2')).toPyDate() - forceDate(record.value('SLUCH_DATE_1')).toPyDate()
            params['SLUCH_KD_Z'] = (delta.days if delta.days > 0 else 1)
        elif uslOk == 3: # амбулатория
            params['SLUCH_KD_Z'] = ''

        if isDiagnostic:
            self._fillDiagnosticEvent(record, params)

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)

        if eventId != params.setdefault('lastEventId'):
            params['USL_IDSERV'] = 0
            _record.setValue('USL_IDSERV', 0)
            params['countMove'] = 0

            if params['lastEventId']:
                self.eventGroup.clear(self, params)
                self.writeEndElement() # SLUCH

            self.eventGroup.addRecord(_record)
            params['lastEventId'] = eventId


    def getCountActionMove(self, eventId, params):
        if params.setdefault('countMove', 0) == 0:
            stmt = u"SELECT COUNT(id) as _count FROM vActionMoving WHERE event_id = %d;" % (eventId)
            query = self._parent.db.query(stmt)
            query.next()
            params['countMove'] = forceInt(query.record().value('_count'))
        return params['countMove']


    def processCoefficients(self, record, params):
        u"""Обработка КСЛП"""
        duration = forceInt(record.value('USL_KD'))
        if duration == 0:
            duration = 1
        coefList = []
        coefficients = forceString(record.value('coefficients'))

        if coefficients:
            coefficients = json.loads(coefficients)
            for _, val in coefficients.items():
                for _code in val:
                    if _code == '__all__':
                        continue
                    if _code[:4] != u'Прер':
                        coefList.append((
                            self.MAP_IDSL_CODE.get(_code, _code),
                            self.MAP_IDSL_VAL.get(_code, _code)))
                    else:
                        record.setValue('USL_SK_KOEF',
                                        format(val[_code], '.2f'))

        coefItSl = 0

        for coefCode, coef in coefList:
            params.setdefault('SL_KOEF_IDSL', []).append(coefCode)
            params.setdefault('SL_KOEF_Z_SL', []).append(coef)

            if coefCode:
                record.setValue('USL_SL_K', toVariant(1))
                coefItSl += Decimal(coef)

        if coefItSl:
            record.setValue('USL_IT_SL', toVariant(str(coefItSl)))



    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        eventId = forceRef(record.value('eventId'))
        tariffType = forceInt(record.value('tariffType'))
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        vidpom = forceString(record.value('SLUCH_VIDPOM'))
        isDiagnostic = forceBool(record.value('isDiagnostic'))

        if isDiagnostic:
            codeOper = forceString(record.value('USL_CODE_OPER'))[:3]
            if codeOper and codeOper != 'A16':
                return

        #Если по какой-то причине диагноз выгрузиться некорректно - 'C73. '
        #то "чистим" такую запись от "шелухи"
        uslDs = forceString(record.value('USL_DS1'))
        if (uslDs.strip().endswith('.')):
            record.setValue('USL_DS1', uslDs[:uslDs.strip().rfind('.')])
        del uslDs

        if (tariffType == CTariff.ttCoupleVisits
                and eventId not in params['visitExportedEventList']):
            params['visitExportedEventList'].add(eventId)
            params['toggleFlag'] = 1
            self.exportVisits(eventId, params)
            record.setValue('SLUCH_P_CEL', '3.0')
            params['toggleFlag'] = 2

        if params['toggleFlag'] == 0 and not isDiagnostic:
            record.setValue('SLUCH_P_CEL', '2.6')


        tarif = forceInt(record.value('USL_TARIF'))
        isMainService = forceString(record.value('USL_CODE_USL')) != '' and tarif != 0
        local_params = {
            'MR_USL_N_CODE_MD': formatSNILS(forceString(record.value('MR_USL_N_CODE_MD_raw'))),
        }

        if isMainService:
            personId = forceRef(record.value('movingPersonId'))
            local_params['USL_DS2'] = self.__getServiceDS2(eventId, personId)
            local_params['USL_DS3'] = self.__getServiceDS3(eventId, personId)
        else:
            record.setNull('USL_CRIT')

        if not isMainService or (forceDate(record.value('USL_DATE_OUT')) !=
                forceDate(record.value('SLUCH_DATE_2'))):
            record.setNull('USL_NPL')

        if uslOk in (1, 3) and tarif != 0:
            begDate = forceDate(record.value('USL_DATE_IN'))
            eventBegDate = forceDate(record.value('SLUCH_DATE_1'))

            if begDate == eventBegDate:
                receivedFrom = self.__receivedFrom(eventId)
                record.setValue('USL_P_PER', toVariant(
                                self.mapRecFrom.get(receivedFrom)))
            else:
                record.setValue('USL_P_PER', toVariant('4'))

        if uslOk == 1:
            record.setValue('USL_DOPL', '')
            record.setValue('SLUCH_P_CEL', '')

            # костыль, потому что не знаю как проверить на NULL =(
            if tarif == -1:
                record.setValue('USL_TARIF', 0)
                record.setValue('USL_SUMV_USL', 0)
            elif vidpom != '32' and forceInt(record.value('USL_SUMV_USL')) > 0:
                self.processCoefficients(record, local_params)
            else:
                record.setValue('USL_SUMV_USL', format(forceDouble(record.value('USL_SUMV_USL')), '.2f'))
                record.setValue('USL_KD', toVariant(params['SLUCH_KD_Z']))
        else:
            record.setValue('USL_KD', toVariant(''))

        csgActionId = forceRef(record.value('csgActionId'))

        if csgActionId in params['replaceBegDate'].keys():
            record.setValue('USL_DATE_IN',
                toVariant(params['replaceBegDate'][csgActionId]))

        # не выводить тег, если коэф. не применены
        if (forceDouble(record.value('USL_SK_KOEF')) == 0.0):
                record.setValue('USL_SK_KOEF', '')

        serviceType = forceInt(record.value('serviceType'))
        if serviceType == 9: #реанимация
            record.setValue('USL_KD', toVariant(0))
            record.setValue('USL_CODE_USL', toVariant(0))

        if csgActionId not in params['skipSet'] and eventId not in params['doneVis']:
            params['USL_IDSERV'] += 1

            if isDiagnostic:
                self._fillDiagnosticService(record, params)

            local_params.update(params)
            serviceCode = forceString(record.value('serviceCode'))
            if serviceCode[:2] == 'st':
                local_params['KSG_KPG_BZTSZ'] = (
                    self._parent.contractAttributeByType(
                        u'BS', forceRef(record.value('contractId'))))

            _record = CExtendedRecord(record, local_params, DEBUG)
            self.eventGroup.addRecord(_record)

        if params['toggleFlag'] == 2 and eventId not in params['doneVis']:
            params['doneVis'].add(eventId)
            params['toggleFlag'] = 0


    def exportVisits(self, eventId, params):
        u"""Экспортирует данные для визитов с 0 стоимостью,
            при тарификации по посещениям"""

        recordList = params['visitInfo'].get(eventId, [])

        for record in recordList:
            self.writeService(record, params)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        #TODO: дублирование кода? Сопоставить с COrder79XmlStreamWriter.writeClientInfo()

        sex = forceString(record.value('PERS_W'))
        birthDate = forceDate(record.value('PERS_DR'))
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        socStatus = self.__clientSocStatus(clientId)
        execDate = forceDate(record.value('execDate'))
        isJustBorn = birthDate.daysTo(execDate) < 28
        isAnyBirthDoc = forceString(record.value('PERS_DOCSER')) or forceString(
                                    record.value('PERS_DOCNUM'))
        statZ = self.mapSocStatusCode.get(socStatus, '')

        local_params = {
            'PACIENT_NOVOR':  ('%s%s1' % (sex[:1], birthDate.toString('ddMMyy')
                             )) if isJustBorn and not isAnyBirthDoc else '0',
            'PACIENT_STAT_Z': statZ,
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.checkerClientInfo(_record)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            self.eventGroup.clear(self, params)
            self.writeEndElement() # SLUCH
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST

    def writeElement(self, elementName, value=None):
        if value or elementName == 'USL_TIP':
            self.writeTextElement(elementName, forceString(value))

    def checkElement(self, eventId, key, string, maxLen, idServ=None,
                     optional=False, isClientInfo=False, suffix='',
                     isWarning=False):
        if not self.checkFill(eventId, key, string, idServ, optional,
                              isClientInfo, suffix, isWarning):
            return False
        if not self.checkLength(eventId, key, string, maxLen, idServ,
                                isClientInfo, suffix, isWarning):
            return False
        return True


    def checkLength(self, eventId, key, string, maxLen, idServ=None,
                    isClientInfo=False, suffix='', isWarning=False):
        if len(string) > maxLen:
            if idServ:
                message = u'Обращение %d%s, услуга %d: тег %s превышает допустимую длинну (%d > %d)!' % (
                            eventId, suffix, idServ, key, len(string), maxLen)
            elif isClientInfo:
                message = u'Пациент %d: тег %s превышает допустимую длинну (%d > %d)!' % (
                            eventId, key, len(string), maxLen)
            else:
                message = u'Обращение %d%s: тег %s превышает допустимую длинну (%d > %d)!' % (
                            eventId, suffix, key, len(string), maxLen)

            if isWarning:
                self._parent.logWarning(message)
            else:
                self._parent.logError(message)
            return False
        return True


    def checkFill(self, eventId, key, string, idServ = None, optional = False, isClientInfo = False, suffix='', isWarning=False):
        if not string and not optional:
            if idServ:
                message = u'Обращение %d%s, услуга %d: тег %s - пустой!' % (eventId, suffix, idServ, key)
            elif isClientInfo:
                message = u'Пациент %d: тег %s - пустой!' % (eventId, key)
            else:
                message = u'Обращение %d%s: тег %s - пустой!' % (eventId, suffix, key)
            if isWarning:
                self._parent.logWarning(message)
            else:
                self._parent.logError(message)
            return False
        return True


    def _fillDiagnosticEvent(self, record, params):
        for field, val in (('SLUCH_P_CEL', '3.0'),
                           ('SLUCH_USL_OK', '3'),
                           ('SLUCH_PROFIL', record.value('diagnosticProfile')),
                           ('SLUCH_NHISTORY', record.value('eventId')),
                           ('SLUCH_PODR', record.value('personOrgStructCode'))):
            record.setValue(field, toVariant(val))


    def _fillDiagnosticService(self, record, params):
        for field, val in (('USL_KOL_USL', record.value('accountItemAmount')),
                           ('USL_SUMV_USL', record.value('accountItemSum')),
                           ('USL_CODE_USL', record.value(
                                'diagnosticServiceCode')),
                           ('USL_DATE_IN', record.value('actionBegDate')),
                           ('USL_DATE_OUT', record.value('actionEndDate'))):
            record.setValue(field, toVariant(val))


    def __getServiceDS2(self, eventId, personId=None):
        return self.__getServiceDiagnosisByCode(eventId, personId, '9')


    def __getServiceDS3(self, eventId, personId=None):
        return self.__getServiceDiagnosisByCode(eventId, personId, '3')


    def __getServiceDiagnosisByCode(self, eventId, personId, diagCode):
        stmt = u"""SELECT GROUP_CONCAT(DISTINCT ds.MKB)
    FROM Diagnosis ds
      INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code LIKE '{code}') -- сопутствующий
      AND dc.event_id = {eventId}""".format(code=diagCode, eventId=eventId)
        if personId:
            stmt += u'  AND dc.person_id = {0}'.format(personId)
        query = self._parent.db.query(stmt)
        record = query.record() if query.first() else None
        result = forceString(record.value(0)).split(',') if record else []
        return result


    def __haveMoving(self, eventId):
        stmt = u"""SELECT NULL FROM Action AS A
        LEFT JOIN ActionType as AT on AT.id = A.actionType_id
        WHERE A.event_id = {0} AND AT.flatCode = 'moving'
        AND A.deleted = 0 LIMIT 1""".format(eventId)
        query = self._parent.db.query(stmt)
        return query.first()


    def __clientSocStatus(self, _id):
        stmt = u"""SELECT rbSocStatusType.code
        FROM ClientSocStatus CSS
        LEFT JOIN rbSocStatusType ON rbSocStatusType.id = socStatusType_id
        WHERE CSS.client_id = '{0}' AND CSS.deleted = 0
          AND CSS.socStatusClass_id = (
            SELECT rbSSC.id FROM rbSocStatusClass rbSSC
            WHERE rbSSC.code = '2' AND rbSSC.group_id IS NULL LIMIT 0,1)
        LIMIT 0, 1""".format(_id)
        query = self._parent.db.query(stmt)
        result = ''
        if query.first():
            record = query.record()
            result = forceString(record.value(0))
        return result


    def isTransferred(self, eventId):
        stmt = u"""SELECT NULL FROM Action AS A
                LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                LEFT JOIN ActionProperty AP ON AP.action_id = A.id
                LEFT JOIN ActionPropertyType APT ON AP.type_id = APT.id
                WHERE A.event_id = '{id}'
                  AND AT.flatCode = 'moving' AND A.deleted = 0
                  AND AP.deleted = 0 AND APT.deleted =0
                  AND APT.name LIKE 'Переведен в отделение'""".format(id=eventId)
        query = self._parent.db.query(stmt)
        return query.first()


    def __receivedFrom(self, eventId):
        stmt = u"""SELECT APS.value FROM Action AS A
                LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                LEFT JOIN ActionProperty AP ON AP.action_id = A.id
                LEFT JOIN ActionPropertyType APT ON AP.type_id = APT.id
                LEFT JOIN ActionProperty_String APS ON APS.id = AP.id
                WHERE A.event_id = '{id}'
                  AND AT.flatCode = 'received' AND A.deleted = 0
                  AND AP.deleted = 0 AND APT.deleted =0
                  AND APT.descr LIKE 'RecFrom'
                LIMIT 0,1""".format(id=eventId)
        query = self._parent.db.query(stmt)
        result = ''
        if query.first():
            record = query.record()
            result = forceString(record.value(0))
        return result

    def __resultCode(self, resultId):
        return self._parent._getIdentification('rbDiagnosticResult', resultId,
                                               self._parent._getAccSysIdByUrn('urn:tfoms61:ISHOD'))


# ******************************************************************************

class CExportR61EventGroup:
    COEF_FIELDS = ('SL_KOEF_IDSL', 'SL_KOEF_Z_SL', 'USL_SL_K', 'USL_IT_SL',
                   'USL_SK_KOEF')
    MKB_LIST = ('E10.0', 'E10.1', 'E10.2', 'E10.3', 'E10.4', 'E10.5', 'E10.6',
    'E10.7', 'E10.8', 'E10.9', 'E11.0', 'E11.1', 'E11.2', 'E11.3', 'E11.4',
    'E11.5', 'E11.6', 'E11.7', 'E11.8', 'E11.9', 'G35', 'C91.1', 'Z94.0',
    'Z94.1', 'Z94.4', 'D69.3', 'B20.9', 'B23.2', 'B23.8', 'B22.7')


    def __init__(self, parent):
        self.records = []
        self.idmasterList = []
        self._parent = parent

    def getIdMaster(self, record):
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        if uslOk == 3 or uslOk == 0: # амбулатория
            if forceDouble(record.value('USL_SUMV_USL')) == 0.0:
                self.idmasterList.append(forceInt(record.value('aiId')))
            else:
                idServ = forceInt(record.value('USL_IDSERV'))
                for i in range(1,len(self.idmasterList)+1):
                    self.records[i].setValue('USL_IDMASTER', idServ)
                record.setValue('USL_IDMASTER', len(self.idmasterList)+1)
            pass
        else: # стационар
            dateIn = forceDate(record.value('USL_DATE_IN')).toPyDate()
            dateOut = forceDate(record.value('USL_DATE_OUT')).toPyDate()
            isMainService = (forceString(record.value('USL_CODE_USL')) != '' and
                forceInt(record.value('USL_TARIF')) != 0)
            orgStruct = forceString(record.value('USL_PODR'))
            eventId = forceRef(record.value('eventId'))
            isTransferred = self._parent.isTransferred(eventId)

            if not isMainService:
                probableIdMaster = None
                codeOperNotEmpty = forceString(record.value('USL_CODE_OPER')) != ''

                for item in self.idmasterList:
                    iDateIn = item['DATE_IN']
                    iDateOut = item['DATE_OUT']
                    diffDateOut = (iDateOut > dateOut)

                    if forceInt(record.value('serviceType')) == 9:
                        diffDateOut = (iDateOut >= dateOut)

                    if iDateIn <= dateIn and diffDateOut:
                        record.setValue('USL_IDMASTER', item['IDSERV'])
                        return
                    elif forceString(record.value('USL_CODE_USL')).startswith(u'рАир'):
                        record.setValue('USL_IDMASTER', item['IDSERV'])
                        return
                    elif (probableIdMaster is None and codeOperNotEmpty and
                            iDateIn <= dateIn and iDateOut >= dateOut):
                        if isTransferred:
                            for it in self.idmasterList:
                                if it['PODR'] == orgStruct:
                                    probableIdMaster = it['IDSERV']
                                    break
                        else:
                            probableIdMaster = item['IDSERV']
                        break

                if codeOperNotEmpty and probableIdMaster is not None:
                    record.setValue('USL_IDMASTER', probableIdMaster)
                    return

            idServ = forceInt(record.value('USL_IDSERV'))
            self.idmasterList.append({
                'IDSERV': idServ,
                'DATE_IN': dateIn,
                'DATE_OUT': dateOut,
                'PODR': orgStruct
            })
            record.setValue('USL_IDMASTER', idServ)


    def addRecord(self, record):
        isDiagnostic = forceBool(record.value('isDiagnostic'))
        if forceInt(record.value('USL_IDSERV')) > 0:
            if not isDiagnostic:
                self.getIdMaster(record)
            else:
                record.setValue('USL_IDMASTER', record.value('USL_IDSERV'))

        # костыль, потому что через `serviceType == 9` определять не захотел
        if forceString(record.value('USL_CODE_USL')).startswith(u'рАир'):
            record.setValue('USL_KD', 0)
            record.setValue('USL_CODE_USL', 0)

        if forceString(record.value('USL_CODE_OPER')) != '':
            record.setValue('USL_KD', None)

        self.records.append(record)


    def clear(self, writer, params):
        self.calc()
        self.write(writer, params)
        del self.records[:]
        del self.idmasterList[:]
        self.lastOperMasterId = 3


    def calc(self):
        sumv = 0.0
        for rec in self.records[1:]:
            sumv = forceDouble(format(sumv + forceDouble(rec.value('USL_SUMV_USL')), ".2f"))
        self.records[0].setValue('SLUCH_SUMV', sumv)


    def write(self, writer, params):
        eventId = forceRef(self.records[0].value('eventId'))
        onkologyInfo = params['onkologyInfo'].get(eventId, {})
        medicalSuppliesInfo = params['medicalSuppliesInfo'].get(eventId, {})
        implantsInfo = params['implantsInfo'].get(eventId, {})
        uslOk = forceInt(self.records[0].value('SLUCH_USL_OK'))
        ds1 = forceString(self.records[0].value('SLUCH_DS1'))

        if onkologyInfo.get('ONK_USL_USL_TIP'):
            orgStructList = onkologyInfo.get('orgStructureId', [])
            onkologyInfo['ONK_USL_IDS_USL'] = [self.records[1].value(
                'USL_IDSERV')]*len(onkologyInfo['ONK_USL_USL_TIP'])
            onkologyInfo['ONK_USL_LEK_PR'] = [dict()]*len(onkologyInfo['ONK_USL_USL_TIP'])
            helper = self._parent._parent
            orgStructSysId = helper._getAccSysId('PODR')
            assignedItems = set()
            for record in self.records[1:]:
                begDate = forceDate(record.value('USL_DATE_IN'))
                endDate = forceDate(record.value('USL_DATE_OUT'))
                orgStructureCode = forceString(record.value('USL_PODR'))[:4]
                for i in range(len(orgStructList)):
                    _code = helper._getIdentification('OrgStructure',
                        orgStructList[i], orgStructSysId)
                    _date = onkologyInfo.get('endDate')[i]
                    if (i not in assignedItems
                            and _code == orgStructureCode
                            and begDate <= _date <= endDate):
                        onkologyInfo['ONK_USL_IDS_USL'][i] = forceString(
                            record.value('USL_IDSERV'))
                    for supplyId, supplyInfo in onkologyInfo.get('medicalSupplies', dict()).iteritems():
                        _, actionOrgId, actionEndDate = supplyId
                        if actionOrgId == orgStructList[i] and begDate <= actionEndDate <= endDate:
                            for key in supplyInfo:
                                if key not in onkologyInfo:
                                    onkologyInfo[key] = [list()] * len(onkologyInfo['ONK_USL_USL_TIP'])
                                onkologyInfo[key][i].append(supplyInfo[key])

        if forceBool(self.records[0].value('isDiagnostic')):
            self.records[0].setValue('SLUCH_PODR',
                self.records[-1].value('USL_PODR'))

        writer.checkerEventInfo(self.records[0])
        record = CExtendedRecord(self.records[0], onkologyInfo)

        ksgCount = self.__getKsgCount()
        isTransferred = self._parent.isTransferred(eventId)
        isDead = forceInt(record.value('SLUCH_RSLT')) == 105
        if ksgCount == 1 and isTransferred:
            ksgRecords = self.__selectKsgRecords()
            if not isDead:
                if len(ksgRecords) == 2:
                    firstSum = forceDouble(ksgRecords[0].value('USL_SUMV_USL'))
                    secondSum = forceDouble(ksgRecords[1].value('USL_SUMV_USL'))
                    recordNum = 1 if firstSum > secondSum else 0
                    if firstSum == secondSum:
                        firstBedDays = forceInt(ksgRecords[0].value('USL_KD'))
                        secondBedDays = forceInt(ksgRecords[1].value('USL_KD'))
                        if firstBedDays == secondBedDays:
                            firstTransferCode = forceString(
                                ksgRecords[0].value('USL_P_PER'))
                            recordNum = 1 if firstTransferCode in (
                                '4', '5') else 0
                        else:
                            recordNum = 1 if firstBedDays > secondBedDays else 0

                    ksgRecords[recordNum].setValue('USL_SUMV_USL', 0)
            else:
                deadRecord = self.__findDeadRecord()
                if deadRecord:
                    coefRecord = self.__findCoefRecord()
                    if coefRecord and coefRecord != deadRecord:
                        for field in self.COEF_FIELDS:
                            deadRecord.setValue(field, coefRecord.value(field))
                    for rec in self.records[1:]:
                        if rec != deadRecord:
                            for field in self.COEF_FIELDS:
                                rec.setValue(field, '')
                tariff = forceDouble(deadRecord.value('USL_TARIF'))
                maxTariffRecord = deadRecord
                for rec in ksgRecords:
                    if tariff < forceDouble(rec.value('USL_TARIF')):
                        maxTariffRecord = rec
                        break
                for rec in ksgRecords:
                    if rec != maxTariffRecord:
                        rec.setValue('USL_SUMV_USL', toVariant(0))

        if isTransferred:
            shortRecords = self.__findShortPeriodAliveRecords()
            maxSum = 0
            maxSumRecord = None
            for rec in shortRecords:
                transferCode = forceString(rec.value('USL_P_PER'))
                if (transferCode and transferCode not in ('4', '5')
                        and forceInt(rec.value('USL_KD')) < 3):
                    coef = self.__selectCoef(rec)
                    _sum = coef*forceDouble(rec.value('USL_TARIF'))
                    rec.setValue('USL_SK_KOEF', coef)
                    if _sum > maxSum:
                        maxSum = _sum
                        maxSumRecord = rec
                    if ksgCount == 1 and forceDouble(rec.value('USL_SUMV_USL')):
                        rec.setValue('USL_SUMV_USL', toVariant(format(_sum, '.2f')))
            if ksgCount == 1 and maxSumRecord:
                for rec in shortRecords:
                    if rec != maxSumRecord:
                        rec.setValue('USL_SUMV_USL', toVariant(0))

        if (isTransferred and u'КСЛП005' in forceString(
                record.value('usedCoefficients'))):
            mkb = forceString(record.value('USL_DS2'))
            if not mkb or mkb not in self.MKB_LIST:
                record.value('SL_KOEF_IDSL').remove(u'КСЛП005')
                record.value('SL_KOEF_Z_SL').remove('0.6')
        _sum = sum(forceDouble(format(forceDouble(rec.value(
                   'USL_SUMV_USL')), '.2f')) for rec in self.records[1:])
        record.setValue('SLUCH_SUMV', _sum)

        writer.writeGroup('SLUCH', writer.eventFields1, record,
                          subGroup=writer.eventSubGroup1,
                          closeGroup=False, dateFields=writer.eventDateFields)

        for rec in self.records[1:]:
            if (forceBool(rec.value('isDiagnostic')) and
                    forceString(rec.value('serviceCode'))[:3] == 'A16'):
                continue
            crit = forceString(rec.value('USL_CRIT'))
            isCovidSupples = (uslOk == 1 and ds1 in ('U07.1', 'U07.2') and
                              crit != 'stt5')
            isMaster = rec.value('USL_IDSERV') == rec.value('USL_IDMASTER')

            local_params = {}
            local_params.update(onkologyInfo)
            if isCovidSupples and isMaster:
                local_params.update(medicalSuppliesInfo)
            else:
                rec.setValue('COVID_LEK_WEI', None)
            if uslOk == 1 and not isMaster and implantsInfo:
                endDate = forceDateTime(rec.value('USL_DATE_OUT'))

                codeList = implantsInfo['MED_DEV_CODE_MEDDEV']
                dateList = implantsInfo['MED_DEV_DATE_MED']
                numberList = implantsInfo['MED_DEV_NUMBER_SER']
                _codeList = []
                _dateList = []
                _numberList = []
                for date in dateList:
                    dt = forceDateTime(date)
                    if abs(dt.secsTo(endDate)) < 60:
                        _codeList.append(codeList[dateList.index(date)])
                        _dateList.append(date)
                        _numberList.append(numberList[dateList.index(date)])
                local_params['MED_DEV_CODE_MEDDEV'] = (
                    _codeList if _codeList else None)
                local_params['MED_DEV_DATE_MED'] = (
                    _dateList if _dateList else None)
                local_params['MED_DEV_NUMBER_SER'] = (
                    _numberList if _numberList else None)

            writer.checkerService(rec)
            extRec = CExtendedRecord(rec, local_params)
            writer.writeGroup('USL', writer.serviceFields, extRec,
                    dateFields=writer.serviceDateFields,
                    subGroup=writer.serviceSubGroup)

        writer.writeGroup('SLUCH', writer.eventFields2, record,
                          subGroup=writer.eventSubGroup2, openGroup=False,
                          closeGroup=False, dateFields=writer.eventDateFields)


    def __getKsgCount(self):
        return len(forceString(
            self.records[0].value('SLUCH_CODE_FKSG')).split(';'))


    def __selectKsgRecords(self):
        result = []
        for rec in self.records[1:]:
            if not rec.isNull('KSG_KPG_KOEF_D'):
                result.append(rec)
        return result


    def __findDeadRecord(self):
        for rec in self.records[1:]:
            if forceString(rec.value('USL_P_PER')) in ('4', '5'):
                return rec


    def __findCoefRecord(self):
        for rec in self.records[1:]:
            if (forceString(rec.value('SL_KOEF_IDSL')) or forceString(
                    rec.value('USL_SK_KOEF'))):
                return rec


    def __findShortPeriodAliveRecords(self):
        u'Возвращает список записей, у которых P_PER <> 4 or 5 и KD <= 3'
        result = []
        for rec in self.records[1:]:
            if (forceString(rec.value('P_PER')) not in ('4', '5')
                    and forceInt(rec.value('USL_KD')) < 3):
                result.append(rec)
        return result

    FIRST_KSG_LIST = ('st02.001', 'st02.002', 'st02.003', 'st02.004', 'st02.010',
        'st02.011', 'st03.002', 'st05.008', 'st08.001', 'st08.002', 'st08.003',
        'st12.010', 'st12.011', 'st14.002', 'st15.008', 'st15.009', 'st16.005',
        'st19.007', 'st19.038', 'st19.082', 'st19.090', 'st19.094', 'st19.097',
        'st19.100', 'st19.105', 'st19.106', 'st19.107', 'st19.108', 'st19.109',
        'st19.110', 'st19.111', 'st19.112', 'st19.113', 'st19.114', 'st19.115',
        'st19.116', 'st19.117', 'st19.118', 'st19.119', 'st19.120', 'st19.121',
        'st20.005', 'st20.006', 'st20.010', 'st21.001', 'st21.002', 'st21.003',
        'st21.004', 'st21.005', 'st21.006', 'st25.004', 'st26.001.2', 'st27.012',
        'st30.006', 'st30.010', 'st30.011', 'st30.012', 'st30.014', 'st31.017',
        'st32.002', 'st32.012', 'st32.016', 'st34.001.2', 'st34.002', 'st36.001',
        'st36.007', 'st36.009', 'st36.010', 'st36.011', 'st36.016', 'st36.017',
        'st36.018', 'st36.019')
    SECOND_KSG_LIST = ('st02.012', 'st02.013', 'st09.001', 'st09.002', 'st09.003',
        'st09.004', 'st09.005', 'st09.006', 'st09.007', 'st09.008', 'st09.009',
        'st09.010', 'st10.001', 'st10.002', 'st10.003', 'st10.004', 'st10.005',
        'st10.006', 'st10.007', 'st13.002', 'st13.005', 'st13.007', 'st13.008',
        'st13.009', 'st13.010', 'st14.001', 'st14.003', 'st15.015', 'st15.016',
        'st16.007', 'st16.008', 'st16.009', 'st16.010', 'st16.011', 'st18.002',
        'st19.001', 'st19.002', 'st19.003', 'st19.004', 'st19.005', 'st19.006',
        'st19.008', 'st19.009', 'st19.010', 'st19.011', 'st19.012', 'st19.013',
        'st19.014', 'st19.015', 'st19.016', 'st19.017', 'st19.018', 'st19.019',
        'st19.020', 'st19.021', 'st19.022', 'st19.023', 'st19.024', 'st19.025',
        'st19.026', 'st19.104', 'st20.007', 'st20.008', 'st20.009', 'st24.004',
        'st25.005', 'st25.006', 'st25.007', 'st25.008', 'st25.009', 'st25.010',
        'st25.011', 'st25.012', 'st27.007', 'st27.009', 'st28.002', 'st28.003',
        'st28.004', 'st28.005', 'st29.007', 'st29.008', 'st29.009', 'st29.010',
        'st29.011', 'st29.012', 'st29.013', 'st30.007', 'st30.008', 'st30.009',
        'st30.013', 'st30.015', 'st31.002', 'st31.003', 'st31.004', 'st31.005',
        'st31.006', 'st31.007', 'st31.008', 'st31.009', 'st31.010', 'st31.015',
        'st31.019', 'st32.001', 'st32.003', 'st32.004', 'st32.005', 'st32.006',
        'st32.007', 'st32.008', 'st32.009', 'st32.010', 'st32.011', 'st32.013',
        'st32.014', 'st32.015', 'st32.017', 'st32.018', 'st32.019', 'st34.003',
        'st34.004', 'st34.005')

    def __selectCoef(self, record):
        result = 0.3
        ksg = forceString(record.value('KSG_KPG_N_KSG'))
        if ksg in self.FIRST_KSG_LIST:
            result = 1
        elif ksg in self.SECOND_KSG_LIST:
            result = 0.8
        return result


# ******************************************************************************

class CRbN013TypeOnkoCureCache(CDbEntityCache):
    mapIdToCode = {}

    def __init__(self):
        pass


    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def get(cls, _id):
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            _db = QtGui.qApp.db
            table = _db.table('rbN013TypeOnkoCure')
            record = QtGui.qApp.db.getRecordEx(table, 'code', [
                table['ID_TLech'].eq(_id) ])
            result = forceString(record.value(0)) if record else None
            cls.mapIdToCode[_id] = result
        return result

# ******************************************************************************

class CRbN014HirLekTypeCache(CDbEntityCache):
    mapIdToCode = {}

    def __init__(self):
        pass


    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def get(cls, _id):
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            _db = QtGui.qApp.db
            table = _db.table('rbN014HirLekType')
            record = QtGui.qApp.db.getRecordEx(table, 'code', [
                table['ID_THir'].eq(_id) ])
            result = forceString(record.value(0)) if record else None
            cls.mapIdToCode[_id] = result
        return result

# ******************************************************************************

class CRbN015LekLinesCache(CDbEntityCache):
    mapIdToCode = {}

    def __init__(self):
        pass


    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def get(cls, _id):
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            _db = QtGui.qApp.db
            table = _db.table('rbN015LekLines')
            record = QtGui.qApp.db.getRecordEx(table, 'code', [
                table['ID_TLek_L'].eq(_id) ])
            result = forceString(record.value(0)) if record else None
            cls.mapIdToCode[_id] = result
        return result

# ******************************************************************************

class CRbN016CycleLekCache(CDbEntityCache):
    mapIdToCode = {}

    def __init__(self):
        pass


    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def get(cls, _id):
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            _db = QtGui.qApp.db
            table = _db.table('rbN016CycleLek')
            record = QtGui.qApp.db.getRecordEx(table, 'code', [
                table['ID_TLek_V'].eq(_id) ])
            result = forceString(record.value(0)) if record else None
            cls.mapIdToCode[_id] = result
        return result

# ******************************************************************************

class CR61OnkologyInfo(COnkologyInfo):
    mapOnkUsl = {
        u'Тип услуги': ('ONK_USL_USL_TIP', CRbN013TypeOnkoCureCache),
        u'Тип хирургического лечения':('ONK_USL_HIR_TIP', CRbN014HirLekTypeCache),
        u'Линия лекарственной терапии': ('ONK_USL_LEK_TIP_L', CRbN015LekLinesCache),
        u'Цикл лекарственной терапии': ('ONK_USL_LEK_TIP_V', CRbN016CycleLekCache),
    }

    mapProtName = {
        u'Противопоказания к проведению хирургического лечения': '1',
        u'Противопоказания к проведению химиотерапевтического лечения': '2',
        u'Отказ от проведения хирургического лечения': '4',
        u'Отказ от проведения химиотерапевтического лечения': '5',
    }

    mapGistologyCode = {
        u'Гистологический тип опухоли группа 1': 1,
        u'Гистологический тип опухоли группа 2': 5,
        u'Гистологический тип опухоли группа 3': 6,
        u'Гистологический тип опухоли группа 4': 9,
        u'Гистологический тип клеток группа 1': 2,
        u'Гистологический тип клеток группа 2': 4,
        u'Гистологический тип клеток группа 3': 6,
        u'Гистологический тип клеток группа 4': 8,
        u'Гистологический тип опухоли группа 5': 10,
        u'Степень дифференцировки ткани опухоли': 3,
    }

    mapImmunolgyCode = {
        u'Уровень экспрессии белка HER2': 1,
        u'Наличие мутаций в гене BRAF': 2,
        u'Наличие мутаций в гене c-Kit': 3,
        u'Наличие мутаций в гене RAS': 4,
        u'Наличие мутаций в гене EGFR': 5,
        u'Наличие транслокации в генах ALK или ROS1': 6,
        u'Уровень экспрессии белка PD-L1': 7,
        u'Наличие рецепторов к эстрогенам ': 8,
        u'Наличие рецепторов к прогестерону': 9,
        u'Определение индекса пролиферативной активности экспрессии Ki-67': 10,
        u'Наличие мутаций в генах BRCA': 2,
    }

    def __init__(self):
        COnkologyInfo.__init__(self)
        self.__serviceNum = 1
        self.__currentEventId = None


    def get(self, _db, idList, parent):
        u"""Возвращает словарь с записями по онкологии и направлениям,
            ключ - идентификатор события"""

        onkologyCond = u"""(DS.MKB LIKE 'C%'
              OR (SUBSTR(DS.MKB, 1, 3) BETWEEN 'D00' AND 'D09')
              OR (SUBSTR(DS.MKB, 1, 3) BETWEEN 'D45' AND 'D47'))"""

        stmt = u"""SELECT Event.id AS eventId,
            rbDiseasePhases.code AS diseasePhaseCode,
            rbEventTypePurpose.regionalCode AS uslOk,
            Diagnosis.MKB,
            AccDiagnosis.MKB AS accMKB,
            IF(GistologiaAction.id IS NOT NULL, 1,
                IF(ImmunohistochemistryAction.id IS NOT NULL, 2,
                    0)) AS DIAG_TIP,
            rbTNMphase_Identification.value AS STAD,
            rbTumor_Identification.value AS ONK_T,
            rbNodus_Identification.value AS ONK_N,
            rbMetastasis_Identification.value AS ONK_M,
            GistologiaAction.id AS gistologiaActionId,
            ImmunohistochemistryAction.id AS immunohistochemistryActionId,
            (SELECT GROUP_CONCAT(A.id) FROM Action A
             WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='ControlListOnko'
            )) AS controlListOnkoActionId,
            (SELECT GROUP_CONCAT(A.id)
                FROM Action A
                WHERE A.event_id = Event.id
                  AND A.deleted = 0
                  AND A.actionType_id IN (
                    SELECT AT.id
                    FROM ActionType AT
                    WHERE AT.flatCode ='Consilium'
            )) AS consiliumActionId,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE AT.flatCode = 'directionCancer'
            )) AS directionActionId,
            IF(rbMedicalAidType.code = '6',
                IF(rbDispanser.observed = 1, '1.3',
                    EventType_Identification.value), '') AS pCel,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE AT.flatCode = 'MedicalSupplies')
             ORDER BY A.begDate
            ) AS medicalSuppliesActionId,
            (SELECT AT.code
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                WHERE A.event_id = Event.id AND A.deleted = 0
                  AND AT.flatCode IN ('codeSH', 'MedicalSupplies')
                ORDER BY AT.flatCode
                LIMIT 0,1
            ) AS LEK_PR_CODE_SH,
            KFrAction.id AS kFrActionId
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN Diagnostic ON Diagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0 AND {onkologyCond}
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnostic AS MainDiagnostic ON MainDiagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            LEFT JOIN rbDiagnosisType DT ON DT.id = D.diagnosisType_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0
              AND DT.code IN ('1','2') AND {onkologyCond}
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnosis ON Diagnosis.id = MainDiagnostic.diagnosis_id
        LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            LEFT JOIN rbDiagnosisType DT ON DT.id = D.diagnosisType_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0
              AND DT.code = '9' AND {onkologyCond}
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = AccDiagnostic.diagnosis_id
            AND AccDiagnosis.deleted = 0 AND (AccDiagnosis.MKB LIKE 'C%')
        LEFT JOIN Diagnostic AnyDiagnostic ON AnyDiagnostic.id = IFNULL(Diagnostic.id, AccDiagnostic.id)
        LEFT JOIN rbDiseasePhases ON AnyDiagnostic.phase_id = rbDiseasePhases.id
        LEFT JOIN rbTNMphase ON rbTNMphase.id = IFNULL(AnyDiagnostic.pTNMphase_id, AnyDiagnostic.cTNMphase_id)
        LEFT JOIN rbTumor ON rbTumor.id = IFNULL(AnyDiagnostic.pTumor_id, AnyDiagnostic.cTumor_id)
        LEFT JOIN rbNodus ON rbNodus.id = IFNULL(AnyDiagnostic.pNodus_id, AnyDiagnostic.cNodus_id)
        LEFT JOIN rbMetastasis ON rbMetastasis.id = IFNULL(AnyDiagnostic.pMetastasis_id, AnyDiagnostic.cMetastasis_id)
        LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
        LEFT JOIN Action AS GistologiaAction ON GistologiaAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id = (
                SELECT MAX(AT.id)
                FROM ActionType AT
                WHERE AT.flatCode ='Gistologia'
              )
        )
        LEFT JOIN Action AS ImmunohistochemistryAction ON ImmunohistochemistryAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='Immunohistochemistry'
              )
        )
        LEFT JOIN Action AS ControlListOnkoAction ON ControlListOnkoAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='ControlListOnko'
              )
        )
        LEFT JOIN rbDispanser ON AnyDiagnostic.dispanser_id = rbDispanser.id
        LEFT JOIN EventType_Identification ON
            EventType_Identification.master_id = EventType.id
            AND EventType_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfomsPCEL'
        )
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN rbTNMphase_Identification ON
            rbTNMphase_Identification.master_id = IFNULL(
                MainDiagnostic.cTNMphase_id, MainDiagnostic.pTNMphase_id)
            AND rbTNMphase_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'TNMphase'
            )
        LEFT JOIN rbTumor_Identification ON
            rbTumor_Identification.master_id = IFNULL(
                AnyDiagnostic.cTumor_id, AnyDiagnostic.pTumor_id)
            AND rbTumor_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Tumor'
            )
        LEFT JOIN rbNodus_Identification ON
            rbNodus_Identification.master_id = IFNULL(
                AnyDiagnostic.cNodus_id, AnyDiagnostic.pNodus_id)
            AND rbNodus_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Nodus'
            )
        LEFT JOIN rbMetastasis_Identification ON
            rbMetastasis_Identification.master_id = IFNULL(
                AnyDiagnostic.cMetastasis_id, AnyDiagnostic.pMetastasis_id)
            AND rbMetastasis_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Metastasis'
            )
        LEFT JOIN Action AS KFrAction ON KFrAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.group_id IN (
                    SELECT AT1.id FROM ActionType AT1
                    WHERE AT1.flatCode ='DiapFR')
              )
        )
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Diagnosis.MKB IS NOT NULL OR AccDiagnosis.MKB IS NOT NULL)
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Account_Item.event_id""" .format(idList=idList,
                                                  onkologyCond=onkologyCond)

        query = _db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result[eventId] = self._processOnkRecord(record, parent)

        return result


    def _isOnkology(self, record):
        mkb = forceString(record.value('MKB'))[:3]
        phase = forceInt(record.value('diseasePhaseCode'))

        dsOnk = (1 if (phase == 10 and (
            mkb[:1] == 'C' or
            (mkb[:3] >= 'D00' and mkb [:3] <= 'D09') or
            (mkb[:3] >= 'D45' and mkb [:3] <= 'D47'))) else 0)
        isOnkology = (mkb[:1] == 'C' or (
                (mkb[:3] >= 'D00' and mkb [:3] <= 'D09') or
                (mkb[:3] >= 'D45' and mkb [:3] <= 'D47'))
            ) and dsOnk == 0
        return dsOnk, isOnkology


    def _processOnkRecord(self, record, parent):
        eventId = forceRef(record.value('eventId'))

        if eventId != self.__currentEventId:
            self.__currentEventId = eventId
            self.serviceNum = 1

        data = COnkologyInfo._processOnkRecord(self, record, parent)

        if data['isOnkology']:
            data['ONK_SL_K_FR'] = '0'

        if data.has_key('ONK_USL_USL_TIP'):
            if data.get('ONK_SL_DS1_T') is None:
                data['ONK_SL_DS1_T'] = '0'
            if data.get('ONK_USL_USL_TIP') is None:
                data['ONK_USL_USL_TIP'] = ['0'] * len(data.get('ONK_USL_PPTR', []))
            if data.has_key('ONK_SL_MTSTZ') and not data['ONK_SL_MTSTZ']:
                data['ONK_SL_MTSTZ'] = '0' # обязательно выгружаем 0
            if data.get('ONK_USL_USL_TIP'):
                data['ONK_USL_NOM_USL'] = range(
                    self.serviceNum,
                    self.serviceNum + len(data['ONK_USL_USL_TIP']))
            if data.get('medicalSupplies', dict()) == {}:
                data['ONK_SL_WEI'] = None
                data['ONK_SL_BSA'] = None
                data['ONK_SL_HEI'] = None
            self.serviceNum += len(data['ONK_USL_USL_TIP'])

        ds1t = data.get('ONK_SL_DS1_T')
        if ds1t in (5, 6):
            result = {}

            for key, val in data.iteritems():
                if key[:7] != 'ONK_USL':
                    result[key] = val

            if ds1t == 6:
                result['ONK_SL_MTSTZ'] = '0'

            data = result

        return data


    def _removeUnnessesaryFields(self, data):
        u'Убирает ненужные поля для разных типов услуг'
        def setZeroVal(_dict, key, pos):
            if key in _dict:
                if len(_dict[key]) < i + 1:
                    _dict[key].append('0')
                else:
                    _dict[key][i] = '0'
            else:
                _dict[key] = ['0']

        for i in range(len(data.get('ONK_USL_USL_TIP', []))):
            if 'ONK_USL_USL_TIP' in data and data['ONK_USL_USL_TIP'][i]:
                setZeroVal(data, 'ONK_USL_LUCH_TIP', i)

                if data.get('ONK_USL_USL_TIP')[i] != '1':
                    setZeroVal(data, 'ONK_USL_HIR_TIP', i)

                if data.get('ONK_USL_USL_TIP')[i] not in ('3', '4'):
                    data['ONK_SL_SOD'] = '0'

                if data.get('ONK_USL_USL_TIP')[i] != '2':
                    setZeroVal(data, 'ONK_USL_LEK_TIP_L', i)
                    setZeroVal(data, 'ONK_USL_LEK_TIP_V', i)


    def _processDiagnostics(self, record, data):
        u'Заполняет поля для диагностик'
        for field, diagType in (('gistologiaActionId', 1),
                                ('immunohistochemistryActionId', 2)):
            _id = forceRef(record.value(field))
            action = CAction.getActionById(_id) if _id else None

            if not (action and action.getProperties()):
                continue

            diagDate = forceDate(action.getRecord().value('endDate')).toString(
                Qt.ISODate)

            for prop in action.getProperties():
                if forceString(prop.type().shortName) == 'DIAG_DATE':
                    val = prop.getValue()

                    if val and val.isValid():
                        diagDate = val.toString(Qt.ISODate)

                    continue

                text = prop.getTextScalar().strip()
                descr = forceString(prop.type().descr).strip()

                if not text or not descr:
                    continue

                rslt = mapDiagRslt.get(text, 0)

                if ((diagType == 1 and descr in self.mapGistologyCode.keys()) or
                        (diagType == 2 and
                         descr in self.mapImmunolgyCode.keys())):
                    data.setdefault('B_DIAG_DIAG_DATE', []).append(diagDate)
                    data.setdefault('B_DIAG_DIAG_TIP', []).append(diagType)
                    data.setdefault('B_DIAG_DIAG_RSLT1', []).append(
                        rslt if diagType == 1 else None)
                    data.setdefault('B_DIAG_DIAG_CODE1', []).append(
                        self.mapGistologyCode[descr] if diagType == 1 else None)
                    data.setdefault('B_DIAG_DIAG_RSLT2', []).append(
                        rslt if diagType == 2 else None)
                    data.setdefault('B_DIAG_DIAG_CODE2', []).append(
                        self.mapImmunolgyCode[descr] if diagType == 2 else None)
                    data.setdefault('B_DIAG_REC_RSLT', []).append(
                        1 if rslt else None)


    def _processControlList(self, record, data):
        u'Заполняет поля из контрольного листка'
        idList = forceString(record.value('controlListOnkoActionId')).split(',')
        for _id in idList:
            action = CAction.getActionById(_id) if _id else None

            if action:
                data.setdefault('orgStructureId', []).append(
                    action.getOrgStructureId())
                data.setdefault('endDate', []).append(
                    forceDate(action.getRecord().value('endDate')))

                for prop in action.getProperties():
                    shortName = prop.type().shortName
                    name = prop.type().name
                    descr = prop.type().descr

                    if shortName == 'PROT':
                        date = prop.getValueScalar()

                        if (date is not None and isinstance(date,  QDate)
                                and date.isValid() and name):
                            data.setdefault('B_PROT_PROT', []).append(descr)
                            data.setdefault('B_PROT_D_PROT', []).append(
                                date.toString(Qt.ISODate))
                    if descr == 'SOD':
                        data['ONK_SL_SOD'] = prop.getValueScalar()
                    elif ((self.mapOnkUsl.has_key(shortName) or
                           self.mapOnkUsl.has_key(name))):
                        fieldName, mapName = self.mapOnkUsl.get(
                            shortName, self.mapOnkUsl.get(name))
                        data.setdefault(fieldName, []).append(
                            mapName.get(prop.getValue()))
                    elif self.__mapPropDescr__.has_key(prop.type().descr):
                        data[self.__mapPropDescr__[prop.type().descr]] = prop.getValue()
                    elif prop.type().descr == 'PPTR':
                        val = prop.getValue()
                        if val:
                            data.setdefault('ONK_USL_PPTR', []).append(
                                mapPptr.get(val.lower(), '0'))
                    elif prop.type().descr == 'DS1_T':
                        data['ONK_SL_DS1_T'] = self.__mapDS1T__.get(prop.getValue())

                if 'ONK_USL_PPTR' not in data:
                     data['ONK_USL_PPTR'] = ['0']
                elif not data['ONK_USL_PPTR'][-1]:
                    data['ONK_USL_PPTR'][-1] = '0'


    def _processConsilium(self, record, data):
        COnkologyInfo._processConsilium(self, record, data)

        if not data.get('CONS_PR_CONS') and data['isOnkology']:
            data['CONS_PR_CONS'] = '0'


    def _processMedicalSupplies(self, record, data):
        u'Заполняет поля для медикаментов'
        idList = forceString(record.value(
            'medicalSuppliesActionId')).split(',')
        result = dict()

        for i in idList:
            _id = forceRef(i)
            action = CAction.getActionById(_id) if _id else None

            if action:
                nomenclatureCode = None
                nomenclatureDict = dict()
                endDate = forceDate(action.getRecord().value('endDate'))
                orgStructId = action.getOrgStructureId()
                for prop in action.getProperties():
                    if prop.type().typeName == u'Номенклатура ЛСиИМН':
                        nomenclatureCode = (
                            CTfomsNomenclatureCache.getCode(
                                prop.getValue()))

                for prop in action.getProperties():
                    if prop.type().descr == 'DATE_INJ':
                        val = prop.getValue()
                        nomenclatureDict.setdefault(
                            nomenclatureCode, []).append(
                            val.toString(Qt.ISODate) if val else None)
                else:
                    if nomenclatureCode:
                        nomenclatureDict.setdefault(
                            nomenclatureCode, []).append(None)

                key = _id, orgStructId, endDate
                result[key] = nomenclatureDict

        codeSH = forceString(record.value('LEK_PR_CODE_SH'))
        out = dict()

        for actionId, nomenclatureDict in result.iteritems():
            for key, val in nomenclatureDict.iteritems():
                out[actionId] = dict()
                out[actionId].setdefault('LEK_PR_REGNUM', []).append(key if key else '-')
                out[actionId].setdefault('LEK_PR_DATE_INJ', []).append(val)
                out[actionId].setdefault('LEK_PR_CODE_SH', []).append(codeSH)

        data['medicalSupplies'] = out
        return data

# ******************************************************************************

class CPersonalDataWriter(COrder79PersonalDataWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = (('ID_PAC', 'FAM', 'IM', 'OT', 'W',)
                    + COrder79PersonalDataWriter.clientDateFields +
                    ('DOST', 'FAM_P', 'IM_P', 'OT_P', 'W_P', 'DR_P', 'MR',
                     'DOCTYPE', 'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG',
                     'SNILS', 'OKATOG', 'OKATOP', 'ADRES', 'KLADR', 'DOM',
                     'KVART', 'KORP'))
    clientDateFields = COrder79PersonalDataWriter.clientDateFields + (
        'DOCDATE', 'DR_P')

    def __init__(self, parent, version='2.1'):
        COrder79PersonalDataWriter.__init__(self, parent, version)

# ******************************************************************************

class CMedicalSuppliesInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        regnum = u"""(SELECT N.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature N ON APN.value = N.id
         WHERE APT.descr = 'N20' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1)"""
        stmt = u"""SELECT Account_Item.event_id AS eventId,
        Action.endDate AS COVID_LEK_LEK_PR_DATA_INJ,
        (SELECT NC.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureClass APNC ON APNC.id = AP.id
         INNER JOIN rbNomenclatureClass NC ON APNC.value = NC.id
         WHERE APT.descr = 'V032' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_CODE_SH,
        (SELECT IF(N.code != '', LPAD(N.code, 6, '0'), '') FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature N ON APN.value = N.id
         WHERE APT.descr = 'N20' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_REGNUM,
        (SELECT APS.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_String APS ON APS.id = AP.id
         WHERE APT.descr = 'COD_MARK' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_COD_MARK,
        IF({regnum} IS NOT NULL AND {regnum} != '',
        (SELECT UI.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbUnit APU ON APU.id = AP.id
         INNER JOIN rbUnit_Identification UI ON UI.master_id = APU.value
         WHERE APT.descr = 'V034' AND AP.action_id = Action.id
           AND AP.deleted = 0
           AND UI.system_id = '{unitSysId}'
         LIMIT 1), NULL) AS COVID_LEK_LEK_PR_LEK_DOSE_ED_IZM,
        IF({regnum} IS NOT NULL AND {regnum} != '',
        (SELECT GROUP_CONCAT(APD.value) FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
         WHERE APT.descr = 'Доза' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1), NULL) COVID_LEK_LEK_PR_LEK_DOSE_DOSE_INJ,
        IF({regnum} IS NOT NULL AND {regnum} != '',
        (SELECT GROUP_CONCAT(N.code) FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureUsingType APNU ON APNU.id = AP.id
         INNER JOIN rbNomenclatureUsingType N ON APNU.value = N.id
         WHERE APT.descr = 'OID:1.2.643.5.1.13.13.11.1468'
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1), NULL)  AS COVID_LEK_LEK_PR_LEK_DOSE_METHOD_INJ,
        IF({regnum} IS NOT NULL AND {regnum} != '',
         Action.amount, '') AS COVID_LEK_LEK_PR_LEK_DOSE_COL_INJ
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.flatCode = 'CovidMedicalSupplies'
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id""" .format(
            idList=self._idList,
            regnum=regnum,
            unitSysId=self._parent._getAccSysIdByUrn(
                'urn:tfoms61:1.2.643.5.1.13.13.11.1358'))
        return stmt


class CImplantsInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Action.endDate AS MED_DEV_DATE_MED,
            ActionType.code AS MED_DEV_CODE_MEDDEV,
            (SELECT APS.value FROM ActionProperty AP
             INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
             INNER JOIN ActionProperty_String APS ON APS.id = AP.id
             WHERE APT.descr = 'NUMBER_SER'
               AND AP.deleted = 0 AND AP.action_id = Action.id
             LIMIT 1) AS MED_DEV_NUMBER_SER
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.flatCode = 'MED_DEV'
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id""" .format(idList=self._idList)
        return stmt

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR61Native,
                      #accNum='06ALL-14',
                      eventIdList = [5615168],
                      #limit=1000,
                      configFileName='75_49_s11.ini')
