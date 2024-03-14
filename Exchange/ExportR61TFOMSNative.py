# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

u"""Экспорт реестра в формате XML. Ростовская область"""

import json
import cProfile
import re
import shutil

from operator import itemgetter
import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QRegExp

from Accounting.Utils import CContractAttributesDescr, CVariantSeries
from Events.Action import CAction
from Exchange.Export import CMultiRecordInfo
from Exchange.ExportR08HospitalV59 import mapDiagRslt, mapPptr
from Exchange.Order79Export import (
    COrder79ExportWizard, COrder79ExportPage1, COrder79PersonalDataWriter,
    COrder79XmlStreamWriter, CExtendedRecord, COrder79ExportPage2)
from Exchange.Order200Export import COnkologyInfo, mapLuchTip
from Exchange.Utils import compressFileInZip, getChecksum

from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1
from Orgs.Utils import getOrganisationInfo
from Registry.Utils import getClientInfo

from library.xlwt import easyxf
from library import xlrd
from library.DbEntityCache import CDbEntityCache
from library.Series import CSeriesHolder
from library.Utils import (forceInt, forceString, forceDate, forceDouble, forceRef, forceBool, formatSNILS, toVariant,
                           forceDateTime, forceStringEx, formatDate)

# ******************************************************************************

VERSION = '3.2'

# выводит в консоль имена невыгруженных полей
DEBUG = False

# ******************************************************************************

def exportR61TFOMSNative(widget, accountId, accountItemIdList, accountIdList=None, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setAccountIdList(accountIdList)
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


    def setAccountIdList(self, accountIdList):
        u"""Запоминает список идентификаторов счетов"""
        self.accountIdList = accountIdList
        self.page1.accountIdList = accountIdList
        if len(self.accountIdList) > 1:
            table = self.db.table('Account_Item')
            self.page1.idList = self.db.getIdList(table, where=[table['master_id'].inlist(accountIdList), table['deleted'].eq(0)])


    def setAccountExposeDate(self):
        u"""Меняет дату выставления счета на текущую"""
        for accountId in self.accountIdList:
            accountRecord = self.db.table('Account').newRecord(['id', 'exposeDate'])
            accountRecord.setValue('id', toVariant(accountId))
            accountRecord.setValue('exposeDate', toVariant(QDate.currentDate()))
            self.db.updateRecord('Account', accountRecord)


    def setAccountNote(self):
        u"""Замещает примечание к счету на переменную NSCHET"""
        for accountId in self.accountIdList:
            accountRecord = self.db.table('Account').newRecord(['id', 'note'])
            accountRecord.setValue('id', toVariant(accountId))
            accountRecord.setValue('note', toVariant(self.note))
            self.db.updateRecord('Account', accountRecord)


    def getZipFileName(self):
        u"""Возвращает имя архива: первые 5 знаков из Organisation.infisCode
        +NN(месяц, например 06 - июнь) заархивировать в формате ZIP"""
        tableOrganisation = self.db.table('Organisation')
        code = forceString(
            self.db.translate(tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'infisCode'))[:5]
        month = self.info['accDate'].month()
        return u'%s%02d.zip' % (code, month)


# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        xmlWriter = (CExportXmlStreamWriter(self, VERSION),
                     CPersonalDataWriter(self, VERSION))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.initFields()
        self.accountIdList = []


    def setAccountIdList(self, accountIdList):
        self.accountIdList = accountIdList


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
            'contract_id': 'Event.contract_id',
            'PR_NOV': '(SELECT regionalCode from Account left join rbAccountType on rbAccountType.id = Account.type_id WHERE Account.id = Account_Item.master_id)',
            # PACIENT_*
            'PACIENT_ID_PAC': 'IF(Event.org_id = 274, Event.client_id + 1000000, Event.client_id)',
            'PACIENT_VPOLIS': 'rbPolicyKind.regionalCode',
            'PACIENT_SPOLIS': """CASE
                WHEN (rbPolicyKind.regionalCode LIKE '1') THEN LEFT(ClientPolicy.serial, 10)
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
            'birthNumber': 'Client.birthNumber',
            'birthWeight': 'Client.birthWeight',
            'socStatus': """(SELECT rbSocStatusType.code
        FROM ClientSocStatus CSS
        LEFT JOIN rbSocStatusType ON rbSocStatusType.id = socStatusType_id
        WHERE CSS.client_id = Client.id AND CSS.deleted = 0
          AND (CSS.endDate IS NULL OR CSS.endDate >= Event.setDate)
          AND CSS.socStatusClass_id in (
            SELECT rbSSC.id FROM rbSocStatusClass rbSSC
            WHERE rbSSC.code = '9' AND rbSSC.group_id IS NULL)
        LIMIT 0, 1)""",
            'clientHasWork': """EXISTS(select NULL FROM ClientWork
                 where client_id = Client.id
                     AND deleted = 0
                     AND (org_id is NOT NULL OR freeInput <> '')
                     AND (post_id is NOT NULL OR post <> ''))""",
            # SLUCH_*
            'SLUCH_IDCASE': 'Account_Item.event_id',
            'SLUCH_USL_OK': "IF(rbEventProfile.code = 'r6020', 3, rbMedicalAidType.regionalCode)",
            'SLUCH_VIDPOM': 'rbMedicalAidKind.regionalCode',
            'vidpom': 'rbMedicalAidType.federalCode',
            'purpose': 'rbEventTypePurpose.purpose',
            'eventProfile': 'rbEventProfile.regionalCode',
            'eventProfileCode': 'rbEventProfile.code',
            'dispanserCode': 'rbDispanser.code',
            'isPrimary': 'Event.isPrimary',
            'ExecPersonOrgStructureId': 'Person.orgStructure_id',
            'UslOrgStructureId': 'Person.orgStructure_id',
            'orgStructureType': 'PersonOrgStructure.type',
            'directionCancerId': """(SELECT
                                    MAX(A1.id)
                                    FROM Action A1
                                    WHERE A1.event_id = Event.id
                                      AND A1.deleted = 0
                                      AND A1.person_id IS NOT NULL
                                      AND A1.endDate IS NOT NULL
                                      AND A1.status = 2
                                      AND A1.actionType_id IN (SELECT
                                          AT1.id
                                        FROM ActionType AT1
                                        WHERE AT1.flatCode = 'directionCancer'
                                        AND AT1.deleted = 0))""",
            'HMP_VID_HMP_raw': None,
            'HMP_METOD_HMP_raw': None,
            'HMP_HMODP': None,
            'HMP_TAL_D': None,
            'HMP_TAL_NUM': None,
            'HMP_TAL_P': None,
            'SLUCH_EXTR': None,
            'SLUCH_PODR': None,
            'SLUCH_LPU': 'PersonOrganisation.miacCode',
            'SLUCH_PROFIL': None,
            'SLUCH_DET': "CASE WHEN rbSpeciality.regionalCode in ('18','19','102','20','21','22','68', '37') THEN 1 ELSE 0 END",
            'SLUCH_NHISTORY': None,
            'USL_P_PER': None,
            'SLUCH_DATE_1': "Event.setDate",
            'SLUCH_DATE_2': 'Event.execDate',
            'SLUCH_DS0': None,
            'SLUCH_DS1': None,
            'DISP_SL_DISP': None,
            'DISP_SL_DS1_PR': None,
            'DISP_SL_PR_D_N': None,
            'DISP_SL_DS2_PR': '',
            'DISP_SL_PR_DS2_N': None,
            'DISP_SL_RSLT_D': None,
            'DS2': """(SELECT GROUP_CONCAT(DS2.MKB)
                              FROM Diagnostic AS DC2
                              LEFT JOIN Diagnosis AS DS2 ON DS2.id = DC2.diagnosis_id
                              WHERE DC2.id in (
                                    SELECT dc.id
                                    FROM Diagnostic dc
                                    LEFT JOIN rbDiagnosisType dt on dt.id = dc.diagnosisType_id
                                    WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0 AND dt.code = '9'))""",
            'DS3': """(SELECT GROUP_CONCAT(DS3.MKB)
                              FROM Diagnostic AS DC3
                              LEFT JOIN Diagnosis AS DS3 ON DS3.id = DC3.diagnosis_id
                              WHERE DC3.id in (
                                    SELECT dc.id
                                    FROM Diagnostic dc
                                    LEFT JOIN rbDiagnosisType dt on dt.id = dc.diagnosisType_id
                                    WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0 AND dt.code = '3'))""",
            'SLUCH_RSLT': 'EventResult.federalCode',
            'SLUCH_ISHOD': 'rbDiagnosticResult.federalCode',
            'SLUCH_PRVS': 'rbSpeciality.regionalCode',
            'SLUCH_IDDOKT_raw': 'Person.SNILS',
            'SLUCH_IDSP': '0',
            'SLUCH_C_ZAB': 'IFNULL(rbDiseaseCharacter_Identification.value, 3)',
            'SLUCH_VB_P': """IF((SELECT COUNT(DISTINCT Action.id)
    FROM Action
    LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
    WHERE Action.event_id = Event.id
      AND Action.deleted = 0
      AND ActionType.flatCode = 'moving') >= 2, 1, '')""",
            'SLUCH_KD_Z': '0',
            'NAPR_FROM_NPR_MO': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(RelegateOrg.miacCode) > 0 THEN RelegateOrg.miacCode ELSE '0' END END",
            'NAPR_FROM_NAPUCH': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(RelegateOrg.infisCode) > 0 THEN RelegateOrg.infisCode ELSE '0' END END",
            'NAPR_FROM_NOM_NAP': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(Event.srcNumber) > 0 THEN LEFT(Event.srcNumber, 16) ELSE '0' END END",
            'NAPR_FROM_NAPDAT': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN IFNULL(Event.srcDate, DATE('1905-01-01')) END",
            'receivedFrom': """CASE WHEN IF(rbEventProfile.code = 'r6020', 3, rbMedicalAidType.regionalCode) in ('1','2') THEN (SELECT APS.value FROM Action AS A
                LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                LEFT JOIN ActionProperty AP ON AP.action_id = A.id
                LEFT JOIN ActionPropertyType APT ON AP.type_id = APT.id
                LEFT JOIN ActionProperty_String APS ON APS.id = AP.id
                WHERE A.event_id = Event.id
                  AND AT.flatCode = 'received' AND A.deleted = 0
                  AND AP.deleted = 0 AND APT.deleted =0
                  AND APT.descr LIKE 'RecFrom'
                LIMIT 0,1) END""",
            'isTransfered': u"""CASE WHEN IF(rbEventProfile.code = 'r6020', 3, rbMedicalAidType.regionalCode) in ('1','2') THEN EXISTS(SELECT NULL FROM Action AS A
                LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                LEFT JOIN ActionProperty AP ON AP.action_id = A.id
                LEFT JOIN ActionPropertyType APT ON AP.type_id = APT.id
                WHERE A.event_id = Event.id
                  AND AT.flatCode = 'moving' AND A.deleted = 0
                  AND AP.deleted = 0 AND APT.deleted =0
                  AND APT.name LIKE 'Переведен в отделение') END
            """,
            # USL_*
            'USL_LPU': 'PersonOrganisation.miacCode',
            'ActionPersonId': 'ActionPerson.id',
            'USL_PODR': None,
            'USL_PROFIL': None,
            'USL_PROFIL_KOIKI': None,
            'USL_DET': "CASE WHEN rbSpeciality.regionalCode in ('18','19','102','20','21','22','68', '37') THEN 1 ELSE 0 END",
            'USL_NPL': None,
            'USL_P_OTK': '0',
            'USL_REAB': None,
            'USL_DATE_IN': None,
            'USL_DATE_OUT': None,
            'USL_DS1': None,
            'USL_CODE_USL': """CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN '0'
                ELSE rbService.code
              END """,
            'USL_KOL_USL': 'Account_Item.amount',
            'USL_TARIF': None,
            'USL_SUMV_USL': u"""CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%') AND rbMedicalAidType.federalCode != '9'
                AND rbEventProfile.regionalCode NOT IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2')) THEN 0
                ELSE Account_Item.sum
              END""",
            'USL_SL_K': 0,
            'USL_IT_SL': None,
            'USL_SK_KOEF': 0,
            'MR_USL_N_MR_N': 1,
            'MR_USL_N_PRVS': None,
            'MR_USL_N_CODE_MD_raw': None,
            'USL_CODE_OPER': u"""IF(rbEventProfile.regionalCode IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2')
                                OR rbMedicalAidType.federalCode = '9'
                                OR rbEventProfile.code in ('r6021', 'r6022', 'r6023', 'r6024'), rbService.infis, NULL)""",
            'USL_KD': None,
            'USL_KSGA': u"""IF(rbMedicalAidType.federalCode = '9'
                                OR rbEventProfile.code in ('r6021', 'r6022', 'r6023', 'r6024'), rbService.infis, NULL)""",
            'USL_PR_DISP': u"""CASE WHEN rbEventProfile.regionalCode IN ('ДВ4', 'ДС1', 'ОПВ', 'ДВ4', 'УД1') THEN '1'
                                   WHEN rbEventProfile.regionalCode IN ('ДВ2', 'УД2') THEN '2' ELSE '0' END""",
            'USL_PR_DISP2': """CASE WHEN EventResult.code IN ('353', '357', '358') THEN '1' ELSE '0' END""",
            # PERS_*
            'PERS_ID_PAC': 'IF(Event.org_id = 274, Event.client_id + 1000000, Event.client_id)',
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
            'PERS_FAM_P': 'UPPER(relatedClient.lastName)',
            'PERS_IM_P': 'UPPER(relatedClient.firstName)',
            'PERS_OT_P': 'UPPER(relatedClient.patrName)',
            'PERS_W_P': 'relatedClient.sex',
            'PERS_DR_P': 'relatedClient.birthDate',
            'relativeId': 'Event.relative_id',
            # KSG_KPG
            'KSG_KPG_N_KSG': """IF(rbService.code LIKE 'st%' or rbService.code LIKE 'ds%',(CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN '0'
                ELSE rbService.code
              END),NULL) """,
            'KSG_KPG_VER_KSG': """IF(rbService.code LIKE 'st%' or rbService.code LIKE 'ds%',YEAR(Event.execDate),NULL)""",
            'KSG_KPG_KSG_PG': """CASE
                    WHEN rbService.code LIKE 'st__.___._' OR rbService.code LIKE 'ds__.___._'THEN 1
                    WHEN rbService.code LIKE 'st__.___' OR rbService.code LIKE 'ds__.___'THEN 0
                    ELSE NULL
                END""",
            'KSG_KPG_KOEF_D': """IF(rbService.code LIKE 'st%' or rbService.code LIKE 'ds%','1.00000',NULL)""",
            'KSG_KPG_KOEF_Z': None,
            'KSG_KPG_KOEF_UP': None,
            'KSG_KPG_BZTSZ': None,
            'KSG_KPG_KOEF_U': None,
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
            'serviceCode': None,
            'persAge': None,
            'isActualPolicy': """IFNULL(ClientPolicy.endDate >= CAST(Event.execDate as date), TRUE)
                AND (ClientPolicy.begDate <= CAST(Event.execDate as date))""",
            'eventCsgMKB': None,
            'serviceType': 'ActionType.serviceType',
            'eventOrder': "IF(rbEventProfile.code = 'r6020', 6, Event.order)",
            'USL_CRIT': "''",
            'isDiagnostic': '(EventType.form = ''001'')',
            'accountItemAmount': 'Account_Item.amount',
            'diagnosticServiceCode': 'rbService.code',
            'diagnosticProfile': 'rbMedicalAidProfile.code',
            'accountItemSum': 'Account_Item.`sum`',
            'actionBegDate': 'Action.begDate',
            'actionEndDate': 'Action.endDate',
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
        self.query_fields['SLUCH_PODR'] = 'SUBSTR(PersonOrgStructure.infisCode, 1, 4)'
        self.query_fields['SLUCH_PROFIL'] = 'rbMedicalAidProfile.code'
        self.query_fields['SLUCH_NHISTORY'] = 'Event.id'
        self.query_fields['SLUCH_DS1'] = 'Diagnosis.MKB'
        self.query_fields['DISP_SL_DISP'] = u"IF(rbEventProfile.regionalCode IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2'), rbEventProfile.regionalCode, NULL)"
        self.query_fields['DISP_SL_DS1_PR'] = u"""IF(rbEventProfile.regionalCode IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2'),
                                                                        IF(rbDiseaseCharacter.code in ('1', '2'), '1', '2'), '')"""
        self.query_fields['DISP_SL_DS2_PR'] = u"""IF(rbEventProfile.regionalCode IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2'),
                              (SELECT MIN(CASE WHEN DDS2.code in ('1', '2') THEN '1' ELSE '2' END)
                              FROM Diagnostic AS DC2
                              LEFT JOIN Diagnosis AS DS2 ON DS2.id = DC2.diagnosis_id
                              LEFT JOIn rbDiseaseCharacter DDS2 ON DDS2.id = DC2.character_id
                              WHERE DC2.id in (
                                    SELECT dc.id
                                    FROM Diagnostic dc
                                    LEFT JOIN rbDiagnosisType dt on dt.id = dc.diagnosisType_id
                                    WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0 AND dt.code = '9')), '')"""
        self.query_fields['DISP_SL_PR_DS2_N'] = u"""IF(rbEventProfile.regionalCode IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2'),
                                                (SELECT MIN(CASE WHEN DDS2.code = '1' THEN '1'
                                                 WHEN DDS2.code in ('2', '6') THEN '2' ELSE '3' END)
                              FROM Diagnostic AS DC2
                              LEFT JOIN Diagnosis AS DS2 ON DS2.id = DC2.diagnosis_id
                              LEFT JOIn rbDispanser DDS2 ON DDS2.id = DC2.dispanser_id
                              WHERE DC2.id in (
                                    SELECT dc.id
                                    FROM Diagnostic dc
                                    LEFT JOIN rbDiagnosisType dt on dt.id = dc.diagnosisType_id
                                    WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0 AND dt.code = '9')), '')"""
        self.query_fields['DISP_SL_RSLT_D'] = u"IF(rbEventProfile.regionalCode IN ('ДВ4', 'ДВ2', 'ДС1', 'ДС3', 'ДС2', 'ДС4', 'ОПВ', 'ПН1', 'ПН2', 'УД1', 'УД2'), EventResult.regionalCode, NULL)"
        self.query_fields['MR_USL_N_PRVS'] = 'IFNULL(ActionSpec.regionalCode, rbSpeciality.regionalCode)'
        self.query_fields['MR_USL_N_CODE_MD_raw'] = 'IFNULL(ActionPerson.SNILS, Person.SNILS)'
        self.query_fields['USL_PODR'] = 'SUBSTR(rbService.code, 1, 4)'
        self.query_fields['USL_PROFIL'] = 'rbMedicalAidProfile.code'
        self.query_fields['USL_DATE_IN'] = 'COALESCE(Visit.DATE, Action.begDate)'
        self.query_fields['USL_DATE_OUT'] = 'COALESCE(Visit.DATE, Action.endDate, Event.execDate)'
        self.query_fields['visitDate'] = 'COALESCE(Visit.DATE, DATE(Action.begDate))'
        self.query_fields['USL_DS1'] = "IF(Action.MKB != '' AND rbMedicalAidType.federalCode = '9', Action.MKB, Diagnosis.MKB)"
        self.query_fields['USL_P_OTK'] = u"""CASE WHEN Action.status = 6 AND rbEventProfile.regionalCode IN ('ДВ4', 'ДС1', 'ДВ4', 'УД1', 'ДВ2', 'УД2') THEN '1' ELSE '0' END"""
        self.query_fields['USL_NZUB'] = u"""CASE WHEN rbMedicalAidType.federalCode = '9' THEN
 (SELECT aps.value
      FROM Action 
      LEFT JOIN ActionPropertyType apt ON apt.actionType_id = Action.actionType_id
      LEFT JOIN ActionProperty ap ON apt.id = ap.type_id AND ap.action_id = Action.id AND ap.deleted = 0
      LEFT JOIN ActionProperty_String aps ON aps.id= ap.id
      WHERE Action.id = Account_Item.action_id AND  apt.deleted = 0 AND apt.typeName = 'ЗУБ' limit 1) END"""
        self.query_fields['USL_KOL_USL'] = "Account_Item.amount"
        self.query_fields['USL_TARIF'] = 'Account_Item.price'
        self.query_fields['UslOrgStructureId'] = 'COALESCE(VisitPerson.orgStructure_id, ActionPerson.orgStructure_id)'
        self.query_fields['USL_NPL'] = """CASE WHEN Action.status = 3 THEN '2'
                                       WHEN Action.status = 6 THEN '1'
                                       WHEN Action.status = 2 AND Action.endDate < Event.setDate THEN '4' END"""


        return u"""/* -- АМБУЛАТОРИЯ -- */
SELECT {fields}
FROM Account_Item
    {commonTables}
    LEFT JOIN Visit ON Visit.id = Account_Item.visit_id
    LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
    LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
WHERE (rbMedicalAidType.federalCode not in ('1', '2', '3', '7') -- Амбулатория
       OR rbEventProfile.code = 'r6020') -- приемный покой
AND Account_Item.reexposeItem_id IS NULL
AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
AND {idList}\n""".format(fields=self.prepare_query_field(), idList=idList,
                   commonTables=commonTables)


    def createStacQuery(self, idList, commonTables, actionTables):
        self.query_fields['SLUCH_EXTR'] = 'IF(Event.`order` IN (2, 6), 2, 1)'
        self.query_fields['SLUCH_PODR'] = '''IF(ActionLeaved.id is NOT NULL, LeavedOrgStructure.infisCode, PersonOrgStructure.infisCode)'''
        self.query_fields['SLUCH_PROFIL'] = '''LeavedHBPProfile.code'''
        self.query_fields['SLUCH_NHISTORY'] = 'CASE WHEN LENGTH(Event.externalId) > 0 THEN Event.externalId ELSE Event.id END'
        self.query_fields['SLUCH_DS1'] = 'Diagnosis.MKB'
        self.query_fields['DISP_SL_DISP'] = None
        self.query_fields['DISP_SL_DS1_PR'] = None
        self.query_fields['DISP_SL_DS2_PR'] = None
        self.query_fields['DISP_SL_PR_DS2_N'] = None
        self.query_fields['DISP_SL_RSLT_D'] = None
        self.query_fields['MR_USL_N_PRVS'] = '''IF(ActionType.serviceType IN
            (9, 4), ActionSpec.regionalCode,
            IFNULL(UslSpec.regionalCode, rbSpeciality.regionalCode))'''
        self.query_fields['MR_USL_N_CODE_MD_raw'] = '''IF(ActionType.serviceType IN
            (9, 4), ActionPerson.SNILS, IFNULL(UslPerson.SNILS, Person.SNILS))'''
        self.query_fields['USL_PODR'] = '''IF(ActionType.serviceType = 9, ReanimationOrgStructure.infisCode, IF(ActionLeaved.id is NOT NULL, MovingOrgStructure.infisCode, PersonOrgStructure.infisCode))'''
        self.query_fields['USL_PROFIL'] = u'''IF(ActionType.serviceType = 9,  5, MovingHBPMedicalAidProfile.code)'''
        self.query_fields['USL_PROFIL_KOIKI'] = 'IF(ActionType.serviceType = 9, 10, MovingHBP.tfomsCode)'
        self.query_fields['USL_CRIT'] = "IFNULL(Crit.code,'')"
        self.query_fields['USL_DATE_IN'] = """CASE WHEN Action.begDate IS NOT NULL THEN Action.begDate ELSE Event_CSG.begDate END"""
        self.query_fields['USL_DATE_OUT'] = """CASE WHEN Action.endDate IS NOT NULL THEN Action.endDate ELSE Event_CSG.endDate END"""
        self.query_fields['USL_DS1'] = """CASE WHEN Action.MKB != '' THEN Action.MKB
             WHEN Event_CSG.id is not null then Event_CSG.MKB 
             ELSE Diagnosis.MKB
             END"""
        self.query_fields['UslOrgStructureId'] = 'COALESCE(ActionPerson.orgStructure_id, Person.orgStructure_id)'
        self.query_fields['visitDate'] = 'NULL'
        self.query_fields['USL_TARIF'] = "IF(Event_CSG.id is not null, Account_Item.`price`, 0)"
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
        self.query_fields['eventCsgMKB'] = 'Event_CSG.MKB'
        self.query_fields['USL_KD'] = """CASE WHEN rbMedicalAidType.federalCode IN ('1', '2', '3', '7') AND IFNULL(rbEventProfile.code, '') != 'r6020'
        THEN WorkDays(Event_CSG.begDate, Event_CSG.endDate, EventType.weekProfileCode, rbMedicalAidType.federalCode='7')
        ELSE 0 END"""
        self.query_fields['SLUCH_KD_Z'] = """CASE WHEN rbMedicalAidType.federalCode IN ('1', '2', '3', '7') AND IFNULL(rbEventProfile.code, '') != 'r6020'
                THEN WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, rbMedicalAidType.federalCode='7')
                ELSE 0 END"""
        self.query_fields['movingPersonId'] = 'ActionMoving.person_id'
        self.query_fields['USL_NZUB'] = "NULL"
        self.query_fields['USL_PR_DISP2'] = "'0'"
        self.query_fields['USL_PR_DISP'] = "'0'"
        self.query_fields['USL_NPL'] = """CASE WHEN (rbMedicalAidType.regionalCode = 1 AND (CSGSpecification.level IS NULL AND EventResult.federalCode IN ('102', '105', '106', '107', '108', '110') 
                                                OR CSGSpecification.level IS NOT NULL AND CSGSpecification.level != 2))
                                           OR (rbMedicalAidType.regionalCode = 2 AND (CSGSpecification.level IS NULL AND EventResult.federalCode IN ('202', '205', '206', '207', '208')
                                                OR CSGSpecification.level IS NOT NULL AND CSGSpecification.level != 2))
                                       THEN '3' END"""


        stmt = u"""/* -- СТАЦИОНАР (без ВМП) -- */
    SELECT {fields}
    FROM Account_Item
    {commonTables}
    LEFT JOIN Event_CSG ON Event_CSG.id = Account_Item.eventCSG_id
    LEFT JOIN rbMesSpecification AS CSGSpecification ON CSGSpecification.id = Event_CSG.csgSpecification_id
    LEFT JOIN ActionType AS Crit ON Crit.id = (
        SELECT MAX(AT.id) FROM Action A
          INNER JOIN ActionType AT ON AT.id = A.actionType_id
        WHERE A.deleted = 0
          AND A.event_id = Event.id
          AND Event_CSG.endDate >= CAST(A.endDate AS DATE) 
          AND Event_CSG.begDate <= CAST(A.endDate AS DATE)
          AND (rbService.code in ('st36.013', 'st36.014', 'st36.015') and AT.Code like 'amt%'
                OR rbService.code NOT in ('st36.013', 'st36.014', 'st36.015') AND AT.Code  not like 'amt%')
          AND AT.flatCode = 'CRIT')
    LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
    LEFT JOIN `Action` AS ActionMoving ON ActionMoving.id = (
        SELECT MIN(A.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        LEFT JOIN Person p on p.id = A.person_id
        LEFT JOIN rbSpeciality sp ON sp.id = p.speciality_id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AT.deleted = 0
            AND AT.`flatCode` = 'moving' 
            AND CASE WHEN Event_CSG.id is not null THEN
                    CASE WHEN DATE(A.begDate) != DATE(A.endDate) 
                         THEN Event_CSG.endDate > CAST(A.begDate AS DATE) AND Event_CSG.endDate <= CAST(A.endDate AS DATE) AND sp.regionalCode not in ('4', '223')
                         ELSE Event_CSG.endDate >= CAST(A.begDate AS DATE) AND Event_CSG.endDate <= CAST(A.endDate AS DATE) AND sp.regionalCode not in ('4', '223') END
                    ELSE CAST(Action.endDate AS DATE) between CAST(A.begDate AS date) AND CAST(A.endDate AS date) END)
    {actionTables}
    WHERE Account_Item.reexposeItem_id IS NULL
        AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
        AND {idList}
        AND rbMedicalAidType.federalCode IN ('1', '3', '7') AND IFNULL(rbEventProfile.code, '') != 'r6020'\n""".format(fields=self.prepare_query_field(), idList=idList, commonTables=commonTables, actionTables=actionTables)
        return stmt


    def createStacVmpQuery(self, idList, commonTables, actionTables):

        self.query_fields['MR_USL_N_PRVS'] = 'IFNULL(UslSpec.regionalCode, rbSpeciality.regionalCode)'
        self.query_fields['MR_USL_N_CODE_MD_raw'] = 'IFNULL(UslPerson.SNILS, Person.SNILS)'
        self.query_fields['USL_DATE_IN'] = 'CAST(IFNULL(Action.begDate, Event.setDate) AS DATETIME)'
        self.query_fields['USL_DATE_OUT'] = 'CAST(IFNULL(Action.endDate, Event.execDate) AS DATETIME)'
        self.query_fields['USL_DS1'] = 'Diagnosis.MKB'
        self.query_fields['USL_TARIF'] = 'Contract_Tariff.price'
        self.query_fields['eventCsgMKB'] = None
        self.query_fields['USL_KD'] = "WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, 0)"
        self.query_fields['USL_CRIT'] = "''"
        self.query_fields['KSG_KPG_KOEF_D'] = "NULL"
        self.query_fields['KSG_KPG_N_KSG'] = "NULL"
        self.query_fields['COVID_LEK_WEI'] = "NULL"
        self.query_fields['KSG_KPG_VER_KSG'] = "NULL"
        self.query_fields['KSG_KPG_KSG_PG'] = "NULL"
        self.query_fields['USL_NZUB'] = "NULL"
        self.query_fields['USL_PR_DISP2'] = "'0'"
        self.query_fields['USL_PR_DISP'] = "'0'"
        self.query_fields['SLUCH_EXTR'] = "1"
        self.query_fields['USL_P_OTK'] = "'0'"
        self.query_fields['directionCancerId'] = "NULL"
        self.query_fields['USL_KSGA'] = "NULL"
        self.query_fields['USL_NPL'] = """CASE WHEN EventResult.federalCode IN ('102', '105', '106', '107', '108', '110') THEN '3' END"""
        self.query_fields['USL_PODR'] = '''IF(ActionLeaved.id is NOT NULL, LeavedOrgStructure.infisCode, PersonOrgStructure.infisCode)'''
        self.query_fields['USL_PROFIL'] = u'''MovingHBPMedicalAidProfile.code'''
        self.query_fields['USL_PROFIL_KOIKI'] = 'MovingHBP.tfomsCode'
        self.addHmpFields()

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
            AND AT.`flatCode` = 'moving')
    {actionTables}
    LEFT JOIN rbCureType ON rbCureType.id = Event.cureType_id
    LEFT JOIN rbCureMethod ON rbCureMethod.id = Event.cureMethod_id
    LEFT JOIN rbPatientModel ON rbPatientModel.id = Event.patientModel_id
    LEFT JOIN ActionProperty_Date AS TicketDate ON TicketDate.id = (
        SELECT MAX(AP.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_Date AS APD ON APD.id = AP.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND AT.`flatCode` LIKE 'talonVMP'
            AND APT.`name` LIKE 'Дата выдачи талона на ВМП')
    LEFT JOIN ActionProperty_Date AS TicketPlannedDate ON TicketPlannedDate.id = (
        SELECT  MAX(AP.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_Date AS APD ON APD.id = AP.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND AT.`flatCode` LIKE 'talonVMP'
            AND APT.`name` LIKE 'Дата планируемой госпитализации')
    LEFT JOIN ActionProperty_String AS TicketNumber ON TicketNumber.id = (
        SELECT MAX(AP.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND AT.`flatCode` LIKE 'talonVMP'
            AND APT.`name` LIKE 'Номер талона на ВМП')
    WHERE Account_Item.reexposeItem_id IS NULL
        AND rbMedicalAidType.federalCode = '2'
        AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
        AND {idList}\n""".format(actionTables=actionTables,
                                 fields=self.prepare_query_field(),
                                 commonTables=commonTables,
                                 idList=idList)
        return stmt


    def createQuery(self):
        sysIdf003 = self._getAccSysId('f003')
        commonTables = u"""-- Common tables begin
    INNER JOIN Event ON Event.id = Account_Item.event_id
    -- PACIENT_*
    INNER JOIN Client ON Client.id = Event.client_id
    LEFT JOIN Client relatedClient ON relatedClient.id = Event.relative_id
    LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate, Event.id)
    LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
    LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    -- SLUCH_*
    LEFT JOIN EventType ON EventType.id = Event.eventType_id
    LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
    LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
    LEFT JOIN Organisation AS RelegateOrg ON RelegateOrg.id = Event.relegateOrg_id
    LEFT JOIN Person ON Person.id = Event.execPerson_id
    LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
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
    LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = COALESCE(rbService_Profile.medicalAidKind_id, rbService.medicalAidKind_id, EventType.medicalAidKind_id)
    LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = IFNULL(rbService_Profile.medicalAidProfile_id, rbService.medicalAidProfile_id)
    LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
    -- Диагнозы
    LEFT JOIN Diagnostic ON Diagnostic.id = (
        SELECT dc.id
        FROM Diagnostic dc
        LEFT JOIN rbDiagnosisType dt on dt.id = dc.diagnosisType_id
        WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0
              AND dt.code IN ('1', '2')
              ORDER BY dt.code LIMIT 1) -- заключительный, основной
    LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
    LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
    LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
    LEFT JOIN rbResult AS EventResult ON EventResult.id = Event.result_id
    LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id = Diagnostic.result_id
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
    -- Common tables end (35 JOINS)""".format(sysIdf003=sysIdf003)

        actionTables = u'''-- Подразделение/Профиль для SLUCH
    LEFT JOIN `Action` AS ActionLeaved ON ActionLeaved.id = (
        SELECT MAX(A.id) FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AT.`flatCode` = 'leaved'
        LIMIT 0, 1)
    LEFT JOIN OrgStructure AS LeavedOrgStructure ON LeavedOrgStructure.id = (
        SELECT APOS.value
        FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_OrgStructure AS APOS ON APOS.id = AP.id
        WHERE A.id = ActionLeaved.id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND APT.`name` = 'Отделение'
        LIMIT 0, 1)
    LEFT JOIN OrgStructure AS MovingOrgStructure ON MovingOrgStructure.id = (
        SELECT APOS.value
        FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_OrgStructure AS APOS ON APOS.id = AP.id
        WHERE A.id = ActionMoving.id
            AND AP.deleted = 0 AND APT.deleted = 0
            AND APT.`name` LIKE 'Отделение пребывания'
        LIMIT 0, 1)
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
    LEFT JOIN rbMedicalAidProfile AS MovingHBPMedicalAidProfile ON MovingHBPMedicalAidProfile.id = MovingHBP.medicalAidProfile_id
    LEFT JOIN OrgStructure AS ReanimationOrgStructure ON ReanimationOrgStructure.id = (
        SELECT APOS.value FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_OrgStructure AS APOS ON APOS.id = AP.id
        WHERE A.deleted = 0 AND A.id = Account_Item.action_id
            AND AP.deleted = 0
            AND AT.serviceType = 9
            AND APT.`name` = 'Отделение пребывания'
        LIMIT 0, 1)
    LEFT JOIN Person AS UslPerson ON UslPerson.id = ActionMoving.person_id
    LEFT JOIN rbSpeciality AS UslSpec ON UslSpec.id = UslPerson.speciality_id'''

        self.initFields()
        idList = self.tableAccountItem['id'].inlist(self.idList)
        sqlAmb = self.createAmbQuery(idList, commonTables)
        sqlStac = self.createStacQuery(idList, commonTables, actionTables)
        sqlStacVmp = self.createStacVmpQuery(idList, commonTables, actionTables)

        stmt = u"""{0} UNION ALL {1} UNION ALL {2} ORDER BY PACIENT_ID_PAC, eventId, SLUCH_USL_OK, USL_SUMV_USL DESC, USL_TARIF DESC, USL_CODE_OPER, serviceCode""".format(sqlAmb, sqlStac, sqlStacVmp)
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
        stmt = u'''SELECT IF(Event.org_id = 274, Event.client_id + 1000000, Event.client_id) AS clientId,
            CASE SUBSTRING(IFNULL(RegKLADR.OCATD, '60401000000'), 1, 2)
                WHEN '60' THEN IFNULL(RegKLADR.OCATD, '60401000000')
                WHEN '' THEN ''
                ELSE CONCAT(SUBSTRING(RegKLADR.OCATD, 1, 2), '000000000')
            END AS PERS_OKATOG,
            CASE SUBSTRING(IFNULL(LocKLADR.OCATD, '60401000000'), 1, 2)
                WHEN '60' THEN IFNULL(LocKLADR.OCATD, '60401000000')
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
            Visit.date AS visitDate,
            rbSpeciality.regionalCode AS MR_USL_N_PRVS,
            CAST(Visit.date AS DATETIME) AS USL_DATE_IN,
            CAST(Visit.date AS DATETIME) AS USL_DATE_OUT,
            SUBSTR(rbService.code, 1, 4) AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL, ServiceProfileMedicalAidProfile.code, ServiceMedicalAidProfile.code) AS USL_PROFIL,
            CASE WHEN rbSpeciality.regionalCode in ('18','19','102','20','21','22','68', '37') THEN 1 ELSE 0 END AS USL_DET,
            CAST(IF(EventType.form = '110', Event.execDate, Event.setDate) AS DATE) AS USL_DATE_1,
            rbService.infis AS USL_CODE_USL,
            1 AS USL_KOL_USL,
            0 AS USL_SK_KOEF,
            0 AS USL_SUMV_USL,
            0 AS USL_TARIF,
            VisitPerson.SNILS AS MR_USL_N_CODE_MD_raw,
            VisitPerson.id as visitPersonId,
            Event.contract_id
        FROM Visit
        LEFT JOIN Event ON Event.id = Visit.event_id
        LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
        LEFT JOIN Person ON Person.id = Event.execPerson_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON Visit.service_id = rbService.id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = VisitPerson.speciality_id)
        LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        WHERE Visit.event_id IN (
            SELECT event_id FROM Account_Item
            LEFT JOIN rbPayRefuseType ON
                rbPayRefuseType.id = Account_Item.refuseType_id
            WHERE Account_Item.reexposeItem_id IS NULL
              AND (Account_Item.date IS NULL OR
                (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
              AND {idList})
          AND Visit.deleted = '0'
          ORDER BY Event.id, Visit.date""".format(idList=idList)

        query = self.db.query(stmt)
        resultByDate = {}
        resultByEvent = {}
        resultByPersonId = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            visitDate = forceDate(record.value('visitDate'))
            visitPersonId = forceRef(record.value('visitPersonId'))
            resultByDate[(eventId, visitDate.toPyDate())] = record
            resultByPersonId[(eventId, visitPersonId)] = record
            resultByEvent.setdefault(eventId, []).append(record)
        return resultByDate, resultByEvent, resultByPersonId


    def exportInt(self):
        params = {'MR_USL_N_MR_N': 1}
        if len(self.accountIdList) > 1:
            items = self.tableAccountItem['master_id'].inlist(self.accountIdList)
        else:
            items = self.tableAccountItem['id'].inlist(self.idList)
        self.setStatus(u'Запрос данных посещений...')
        params['visitInfo'], params['visitInfoByEvent'], params['visitInfoByPersonId'] = self.visitInfo(items)
        self.setStatus(u'Запрос адресов клиентов...')
        params['clientAddr'] = dict(self.getAddr(items))
        for msg, name, _class in (
                (u'Запрос данных онкологии...',
                 'onkologyInfo',  CR61OnkologyInfo),
                (u'Запрос данных мед.препаратов...',
                 'medicalSuppliesInfo',  CMedicalSuppliesInfo),
                (u'Запрос данных об имплантации...',
                 'implantsInfo',  CImplantsInfo),
                (u'Запрос данных об услугах обращения...',
                 'obrInfo', CObrInfo),
                (u'Запрос данных об назначениях при дисп....',
                 'appointmentsInfo', CAppointmentsInfo),
              ):
            self.setStatus(msg)
            val = _class()
            params[name] = val.get(self.db, items, self)
        params['CSGCoefficients'] = CCSGCoefficients()
        self.setProcessParams(params)
        COrder79ExportPage1.exportInt(self)


    def setStatus(self, msg):
        self.log(msg)
        self.progressBar.setText(msg)
        QtGui.qApp.processEvents()


    def nschet(self, registryType, params):
        u"""Формирует переменную NSCHET"""

        result = None
        note = params['note']

        if note:
            regexp = QRegExp('^\\s*\\[NSCHET:(\\S+)\\]\\s*$')
            assert regexp.isValid()

            if regexp.indexIn(note) != -1:
                result = forceString(regexp.cap(1))

        if not result:
            payerCodePart = forceInt(params['payerCode'][-2:]) if (registryType == self.registryTypePayment) else 10
            result = u'%2d%02d%s' % (payerCodePart, params['accDate'].month(), params['accNumber'][-1:])
            result = u'%s1' % result[:-1].lstrip()

        return result


class CExportPage2(COrder79ExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        COrder79ExportPage2.__init__(self, parent, 'Export%s' % prefix)


    def saveExportResults(self):
        fileList = (self._parent.getFullXmlFileName(), self._parent.getPersonalDataFullXmlFileName())
        zipFileName = self._parent.getFullZipFileName()

        success = compressFileInZip(fileList, zipFileName)
         
        if success:
            archiveName = self._parent.getZipFileName()
            try:
                checksum = getChecksum(zipFileName)
                xlstempfile = os.path.join(self.getTmpDir(), 'akt_'+archiveName[:-6] + '_' + archiveName[-6:-4] +'.xls')
                try:
                    shutil.copy('Exchange/R61_act.xls', xlstempfile)
                except IOError:
                    shutil.copy('R61_act.xls', xlstempfile)
                existing_workbook = xlrd.open_workbook(xlstempfile, formatting_info=True)

                workbook = xlrd.copy(existing_workbook)
                worksheet = workbook.get_sheet(0)
                style_string = "borders: top double, bottom thin, left thin, right thin;"
                style = easyxf(style_string)
                style_string = "borders: bottom thin;"
                style2 = easyxf(style_string)

                orgInfo = getOrganisationInfo(QtGui.qApp.currentOrgId())
                fullName = orgInfo['fullName']
                if fullName.startswith(u'Государственное бюджетное учреждение Ростовской области'):
                    worksheet.write(3, 1, u'Государственное бюджетное учреждение Ростовской области', style2)
                    worksheet.write(4, 1, fullName.replace(u'Государственное бюджетное учреждение Ростовской области', '').lstrip(), style2)
                else:
                    worksheet.write(3, 1, orgInfo['title'], style2)
                worksheet.write(5, 1, orgInfo['infisCode'], style2)
                worksheet.write(5, 5, orgInfo['miacCode'], style2)
                worksheet.write(12, 2, self._parent.info['accDate'].month(), style2)
                worksheet.write(12, 6, self._parent.info['accDate'].year(), style2)
                worksheet.write(17, 0, archiveName)

                worksheet.write(17, 5, checksum, style)
                worksheet.write(17, 6, '', style)
                worksheet.write(17, 7, '', style)
                worksheet.write(33, 1, formatDate(QDate.currentDate()), style2)

                workbook.save(xlstempfile)

                fileList = (xlstempfile, zipFileName)
            except Exception as e:
                fileList = (zipFileName,)
            zipFileName = os.path.join(self.getTmpDir(), '_' + archiveName)
            success = compressFileInZip(fileList, zipFileName)
            
        return success and self.moveFiles([zipFileName])

    def validatePage(self):
        success = self.saveExportResults()

        if success:
            QtGui.qApp.preferences.appPrefs[
                '%sExportDir' % self.prefix] = toVariant(self.edtDir.text())
            self.wizard().setAccountExposeDate()
            self.wizard().setAccountNote()
        return success

    def moveFiles(self, fileList):
        u"""Переносит файлы из списка в каталог, выбранный пользователем"""

        for src in fileList:
            srcFullName = os.path.join(forceStringEx(self.getTmpDir()), os.path.basename(src))
            dst = os.path.join(forceStringEx(self.edtDir.text()), os.path.basename(src).replace('_', ''))
            success, _ = QtGui.qApp.call(self, shutil.move, (srcFullName, dst))

            if not success:
                break

        return success
# ******************************************************************************

class CExportXmlStreamWriter(COrder79XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR', 'VNOV_D', 'STAT_Z')

    eventDateFields1 = ('DATE_1', 'DATE_2')
    eventDateFields2 = ('NAPDAT',)
    eventFields1 = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'P_CEL', 'HMP',
                    'NAPR_FROM', 'PODR', 'LPU', 'PROFIL', 'DET', 'NHISTORY', 'DN') + eventDateFields1 + ('DS0',
                    'DS1', 'DS2', 'DS3', 'C_ZAB', 'VNOV_M', 'RSLT', 'ISHOD', 'PRVS', 'VERS_SPEC',
                    'IDDOKT', 'OS_SLUCH', 'IDSP', 'SUMV', 'OPLATA', 'SUMP', 'NSVOD', 'KODLPU', 'PRNES', 'KD_Z',
                    'PCHAST', 'VBR', 'DISP_SL', 'CODE_FKSG', 'PR_MO', 'VB_P', 'USL')
    eventFields2 = ('DS_ONK', 'NAPR', 'CONS', 'ONK_SL')
    eventFields = eventFields1 + eventFields2

    onkSlFields = ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M', 'MTSTZ', 'SOD',
                   'K_FR', 'WEI', 'HEI', 'BSA', 'B_DIAG', 'B_PROT', 'ONK_USL')

    consFields = ('PR_CONS', 'DT_CONS')
    consDateFields = ('DT_CONS', )
    ksgKpgFields = ('N_KSG', 'VER_KSG', 'KSG_PG', 'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D', 'KOEF_U')

    naprFields = ('NAPR_DATE', 'NAPR_MO', 'NAPR_LPU', 'NAPR_V', 'MET_ISSL', 'NAPR_USL')

    medicalSuppliesDoseGroup = {
        'LEK_DOSE': {
            'fields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'requiredFields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'prefix': 'COVID_LEK_LEK_PR',
        },
    }

    medicalSuppliesGroup = {
        'LEK_PR': { 'fields': ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK', 'LEK_DOSE'),
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

    naprFromFields = ('NPR_MO', 'NAPUCH', 'NOM_NAP', 'NAPDAT', 'BIO_DAT', 'DSN')

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
    nazSubGroup = {'NAZ': {'fields': ('NAZ_N', 'NAZR', 'NAZ_IDDOKT', 'NAZ_SP', 'NAZ_V', 'NAZ_USL', 'NAPR_DATE', 'NAPR_MO', 'NAPR_LPU', 'NAZ_PMP', 'NAZ_PK'),
                           'dateFields': ('NAPR_DATE',)},
                   }
    eventSubGroup1 = {
        'HMP': {'fields': ('VID_HMP', 'METOD_HMP', 'HMODP', 'TAL_D', 'TAL_NUM', 'TAL_P')},
        'NAPR_FROM': {'fields': naprFromFields, 'dateFields': ('NAPDAT', 'BIO_DAT')},
        'DISP_SL': {'fields': ('DISP', 'M_OKAZ', 'P_OTK', 'DS1_PR', 'NAZ', 'PR_D_N', 'DS2_PR', 'PR_DS2_N', 'GR_D_N', 'RSLT_D'),
                    'subGroup': nazSubGroup},
    }

    eventSubGroup2 = {
        'CONS': {'fields': consFields},
        'NAPR': {'fields': naprFields},
        'ONK_SL': {'fields': onkSlFields,
                            'subGroup': onkSlSubGroup},
    }

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'IDMASTER', 'LPU', 'PODR', 'PROFIL',
                      'PROFIL_KOIKI', 'P_PER', 'REAB', 'CRIT', 'DET', 'NPL', 'P_OTK')  +
                     serviceDateFields +
                     ('KD', 'DS1', 'DS2', 'DS3', 'CODE_USL', 'KOL_USL', 'KSG_KPG', 'TARIF',
                      'SUMV_USL', 'SL_K', 'IT_SL', 'SL_KOEF', 'SK_KOEF',
                      'COVID_LEK', 'MED_DEV', 'MR_USL_N', 'KODLPU', 'KSGA', 'NZUB', 'CODE_OPER', 'PR_DISP', 'PR_DISP2'))



    mapRecFrom = {
        u'Поликлиника': '1',
        u'Самотек': '1',
        u'Другие': '1',
        u'Скорая помощь': '2',
        u'Перевод из ЛПУ': '3',
        u'Санавиация': '3',
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
        self.mapOrgStructureIdToKODLPU = {}
        self.exportedAppointments = set()
        self.exportedDirectionCancers = set()
        self.contactAttributesMap = {}


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        accDate = params['accDate']
        self.startDate = QDate(settleDate.year(), settleDate.month(), 1)
        table = self._parent.db.table('Account')
        accSum = forceDouble(self._parent.db.getSum(table, sumCol='sum', where=table['id'].inlist(self._parent.accountIdList)))
        params['USL_LPU'] = params['lpuMiacCode']
        params['SLUCH_LPU'] = u'510%s' % params['lpuCode']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', self.version)
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', forceString(self._parent.getEventCount()))
        self.writeEndElement()  # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuMiacCode'])
        self.writeTextElement('YEAR', forceString(accDate.year()))
        self.writeTextElement('MONTH', forceString(accDate.month()))
        self.writeTextElement('NSCHET', params['NSCHET'])
        self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))
        self.writeTextElement('SUMMAV', '{0:.2f}'.format(accSum))
        self.writeEndElement()  # SCHET


    def checkerClientInfo(self, record):
        if forceString(record.value('PERS_OT')) == '':
            record.setValue('PERS_OT', u'НЕТ')
        if forceInt(record.value('isActualPolicy')) == 0 and forceInt(record.value('PACIENT_VPOLIS')) != 2:
            record.setValue('PACIENT_SPOLIS', '0000000000')
            record.setValue('PACIENT_NPOLIS', '00000000000000000000')


    def checkerEventInfo(self, record):
        if not forceString(record.value('SLUCH_PODR')):
            record.setValue('SLUCH_PODR', '0')
        if not forceString(record.value('SLUCH_LPU')):
            record.setValue('SLUCH_LPU', '0')
        if not forceString(record.value('SLUCH_PROFIL')):
            record.setValue('SLUCH_PROFIL', '0')
        if not forceString(record.value('SLUCH_RSLT')):
            record.setValue('SLUCH_RSLT', '0')
        if not forceString(record.value('SLUCH_ISHOD')):
            record.setValue('SLUCH_ISHOD', '0')


    def checkerService(self, record):
        if not forceString(record.value('USL_PODR')) or not forceString(record.value('USL_PODR')).isdigit():
            record.setValue('USL_PODR', '0')
        if not forceString(record.value('USL_PROFIL')):
            record.setValue('USL_PROFIL', '0')
        if not forceString(record.value('USL_KOL_USL')):
            record.setValue('USL_KOL_USL', '1')


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        prNov = forceString(record.value('PR_NOV')) or '0'
        changedPrNov = (prNov != params.setdefault('lastPrNov'))

        if (clientId != params.setdefault('lastClientId')) or changedPrNov:
            if params['lastClientId'] or params['lastPrNov']:
                self.eventGroup.clear(self, params)
                self.writeEndElement()  # SLUCH
                self.writeEndElement()  # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['N_ZAP']))
            self.writeTextElement('PR_NOV', prNov)

            clientAddrInfo = params['clientAddr'].get(clientId, {})
            params.update(clientAddrInfo)
            # isAddressError = params['isAddressError']

            # if isAddressError:
            #     self._parent.logError(
            #         u'У пациента %s %s %s (%d) не заполнен адрес' %
            #         (forceString(record.value('PERS_FAM')),
            #          forceString(record.value('PERS_IM')),
            #          forceString(record.value('PERS_OT')),
            #          clientId))
            #     self.abort()

            self.writeClientInfo(record, params)

            params['N_ZAP'] += 1
            params['lastClientId'] = clientId
            params['lastPrNov'] = prNov
            params['lastEventId'] = None

        self.writeEventInfo(record, params)
        # directionCancerId = forceRef(record.value('directionCancerId'))
        # if directionCancerId and directionCancerId not in self.exportedDirectionCancers:
        #     self.writeDirectionCancer(directionCancerId)
        self.writeService(record, params)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        execDate = forceDate(record.value('SLUCH_DATE_2'))
        # eventPurposeCode = forceString(record.value(
        #         'eventPurposeCode'))
        patrName = forceString(record.value('PERS_OT'))
        # haveMoving = self.__haveMoving(eventId)
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        purpose = forceInt(record.value('purpose'))
        isPrimary = forceInt(record.value('isPrimary'))
        eventProfile = forceString(record.value('eventProfile'))
        cureTypeCode = forceString(record.value('HMP_VID_HMP_raw'))
        vidpom = forceString(record.value('SLUCH_VIDPOM'))
        isDiagnostic = forceBool(record.value('isDiagnostic'))
        dispanserCode = forceString(record.value('dispanserCode'))
        birthDate = forceDate(record.value('PERS_DR'))
        setDate = forceDate(record.value('SLUCH_DATE_1'))
        isJustBorn = birthDate.daysTo(setDate) < 29
        isAnyBirthDoc = forceString(record.value('PERS_DOCNUM')) or forceString(record.value('PACIENT_NPOLIS')) and forceString(record.value('PACIENT_NPOLIS')) != '00000000000000000000'
        birthWeight = forceInt(record.value('birthWeight'))
        orgStructureId = forceRef(record.value('ExecPersonOrgStructureId'))
        eventOrder = forceString(record.value('eventOrder'))
        hasObr = bool(params['obrInfo'].get(eventId, None))

        os_sluch = '1' if (isJustBorn and not isAnyBirthDoc) else ''
        if not os_sluch:
            os_sluch = '2' if (not patrName or patrName.upper() == u'НЕТ') else ''

        local_params = {
            'SLUCH_VNOV_M': birthWeight if os_sluch == '1' and birthWeight <= 2500 else None,
            'SLUCH_OS_SLUCH': os_sluch,
            'SLUCH_VERS_SPEC': 'V021',
            'SLUCH_OPLATA': '0',
            'SLUCH_SUMP': '0',
            'SLUCH_NSVOD': '%d%02d' % (uslOk, execDate.month()),
            'SLUCH_KODLPU': self.getKODLPU(orgStructureId),
            'SLUCH_PRNES': '0' if uslOk in [1, 2] else None,
            'SLUCH_PCHAST': '0',
            'SLUCH_IDDOKT': formatSNILS(forceString(record.value('SLUCH_IDDOKT_raw'))),
            'SLUCH_PR_MO': '0',
            'SLUCH_FOR_POM': self.mapEventOrderToForPom.get(eventOrder, '1'),
            'SLUCH_DS_ONK': '1' if forceRef(record.value('')) else '0'
        }

        if forceString(record.value('vidpom')) != '9':
            local_params['SLUCH_DS2'] = forceString(record.value('DS2')).split(',')
            local_params['SLUCH_DS3'] = forceString(record.value('DS3')).split(',')

        if uslOk == 3:
            local_params['SLUCH_VBR'] = '1' if forceInt(record.value('orgStructureType')) == 3 else '0'
            if forceString(record.value('vidpom')) == '9':  # стоматология
                visit = params['visitInfo'].get((eventId, setDate.toPyDate()), None)
                local_params['SLUCH_P_CEL'] = '2.6'  # обращение по другим случаям
                if visit:
                    visitCode = forceString(visit.value('USL_CODE_USL'))
                    if visitCode[6:7] == '2':
                        local_params['SLUCH_P_CEL'] = '1.1'  # посещение в неотложной форме
                    elif visitCode[6:7] == '3':
                        local_params['SLUCH_P_CEL'] = '3.0'  # обращение по заболеванию
            elif eventOrder == '6':
                local_params['SLUCH_P_CEL'] = '1.1'  # посещение в неотложной форме
            elif purpose == 6:
                local_params['SLUCH_P_CEL'] = '1.3'  # диспансерное наблюдение
            elif purpose == 2 and eventProfile == u'ОПВ':
                local_params['SLUCH_P_CEL'] = '2.1'  # профосмотры детские и взрослые
            elif purpose == 2 and eventProfile in [u'ДВ4', u'ДВ2', u'ДС1', u'ДВ4', u'ДВ2', u'УД1', u'УД2', u'ПН1', u'ПН2']:
                local_params['SLUCH_P_CEL'] = '2.2'  # диспансеризации детские и взрослые
            elif purpose == 2 and not eventProfile and len(params['visitInfoByEvent'].get(eventId, [])) > 1:
                local_params['SLUCH_P_CEL'] = '3.1'  # обращение с профилактической целью
            elif purpose == 1 and isPrimary != 3 and hasObr:
                local_params['SLUCH_P_CEL'] = '3.0'  # обращение по заболеванию
            elif purpose == 1 and isPrimary != 3 and not hasObr:
                local_params['SLUCH_P_CEL'] = '1.0'  # посещение по заболеванию
            else:
                local_params['SLUCH_P_CEL'] = '2.6'  # обращение по другим случаям
        else:
            local_params['SLUCH_P_CEL'] = None

        if local_params['SLUCH_P_CEL'] == '1.3' or local_params['SLUCH_P_CEL'] in ['1.0', '3.0'] and dispanserCode in ['2', '6']:
            if dispanserCode == '1':
                local_params['SLUCH_DN'] = '1'
            elif dispanserCode in ['2', '6']:
                local_params['SLUCH_DN'] = '2'
            elif dispanserCode == '4':
                local_params['SLUCH_DN'] = '4'
            elif dispanserCode in ['3', '5']:
                local_params['SLUCH_DN'] = '6'

        # если тег PRZAB пустой, выводить 0
        if not forceString(record.value('SLUCH_PRZAB')):
            record.setValue('SLUCH_PRZAB', '0')

        if uslOk == 1 and vidpom == '32': # если это стационар
            local_params['HMP_METOD_HMP'] = forceString(
                                              record.value('HMP_METOD_HMP_raw'))
            local_params['HMP_VID_HMP'] = cureTypeCode

            if forceString(record.value('USL_CODE_OPER')):
                record.setValue('USL_KOL_USL', '1')

        if uslOk == 1:  # если это стационар
            if vidpom != '32':
                fskgList = params['mapEventIdToFksgCode'].get(eventId, '').split(';')
                local_params['SLUCH_CODE_FKSG'] = ';'.join(x for x in fskgList if x[:2] == 'st')
            else:
                record.setValue('serviceCode', '')
            local_params['SLUCH_DOPL'] = ''

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
        coefList = []
        coefficients = forceString(record.value('coefficients'))
        coefItSl = 0
        if coefficients:
            coefficients = json.loads(coefficients)
            for _code, val in coefficients.items():
                if _code == 'all':
                    coefItSl = val[u'значение']
                    continue
                if _code[:4] != u'ПРЕР':
                    coefList.append((
                        val[u'номер'],
                        format(val[u'значение'], '.5f')))
                else:
                    record.setValue('USL_SK_KOEF', format(val[u'значение'], '.2f'))

        for coefCode, coef in coefList:
            params.setdefault('SL_KOEF_IDSL', []).append(coefCode)
            params.setdefault('SL_KOEF_Z_SL', []).append(coef)
            if coefCode:
                record.setValue('USL_SL_K', toVariant(1))

        if coefItSl:
            record.setValue('USL_IT_SL', toVariant(format(coefItSl, '.5f')))


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        eventId = forceRef(record.value('eventId'))
        tariffType = forceInt(record.value('tariffType'))
        uslOk = forceInt(record.value('SLUCH_USL_OK'))
        vidpom = forceString(record.value('SLUCH_VIDPOM'))
        isDiagnostic = forceBool(record.value('isDiagnostic'))
        execPersonOrgStructureId = forceRef(record.value('ExecPersonOrgStructureId'))
        orgStructureId = forceRef(record.value('UslOrgStructureId'))
        vidpomCode = forceString(record.value('vidpom'))
        visitDate = forceDate(record.value('visitDate'))
        eventProfile = forceString(record.value('eventProfile'))
        eventProfileCode = forceString(record.value('eventProfileCode'))

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

        eventHasObr = params['obrInfo'].get(eventId, None)
        if eventHasObr and forceInt(record.value('USL_TARIF')) == 0:
            codeUsl = forceString(record.value('USL_CODE_USL'))[:4].ljust(11, '0')
            record.setValue('USL_CODE_USL', codeUsl)
        if vidpomCode == '9':  # стоматология
            visit = params['visitInfo'].get((eventId, visitDate.toPyDate()), None)
            if visit:
                record.setValue('USL_CODE_USL', forceString(visit.value('USL_CODE_USL')))
                record.setValue('USL_PODR', forceString(visit.value('USL_CODE_USL'))[:4])
                attributes = self.__getContractAttributes(forceRef(visit.value('contract_id')))
                tarif = forceDouble(attributes['UET_C' if forceInt(record.value('USL_DET')) == 1 else 'UET_A'][visitDate])
                record.setValue('USL_TARIF', tarif)
            record.setValue('USL_KOL_USL', 1)
        elif eventProfile == u'ДВ2' and forceString(record.value('USL_CODE_OPER'))[:7] in ['B04.047', 'B04.023', 'B04.018', 'B04.028', 'B04.029', 'B04.001', 'B04.008']:
            personId = forceRef(record.value('ActionPersonId'))
            visit = params['visitInfoByPersonId'].get((eventId, personId), None)
            if visit:
                record.setValue('USL_CODE_USL', forceString(visit.value('USL_CODE_USL')))
                record.setValue('USL_PODR', forceString(visit.value('USL_CODE_USL'))[:4])
                record.setValue('USL_PROFIL', forceString(visit.value('USL_PROFIL')))
            else:
                record.setValue('USL_CODE_USL', '0')
                record.setValue('USL_PODR', '0')
        elif eventProfile in [u'ДВ4', u'ДС1', u'ДС3', u'ДС2', u'ДС4', u'ОПВ', u'ПН1', u'ПН2', u'УД1', u'УД2']:
            visit = params['visitInfoByEvent'].get(eventId, [])
            if visit:
                if forceString(record.value('USL_CODE_OPER'))[:7] in ['B04.026', 'B04.031', 'B04.047']:
                    record.setValue('USL_CODE_USL', forceString(visit[-1].value('USL_CODE_USL')))
                else:
                    record.setValue('USL_CODE_USL', 0)
                record.setValue('USL_PODR', forceString(visit[-1].value('USL_CODE_USL'))[:4])
            record.setValue('USL_KOL_USL', 1)
        elif eventProfileCode in ['r6021', 'r6022', 'r6023', 'r6024']:
            self._fillDiagnosticService(record, params)
            visit = params['visitInfo'].get((eventId, visitDate.toPyDate()), None)
            if visit:
                record.setValue('USL_CODE_USL', forceString(visit.value('USL_CODE_USL')))
                record.setValue('USL_PODR', forceString(visit.value('USL_CODE_USL'))[:4])
        elif eventProfileCode in ['r6020']:
            visit = params['visitInfoByEvent'].get(eventId, [])
            if visit:
                record.setValue('USL_PODR', forceString(visit[0].value('USL_CODE_USL'))[:4])

        tarif = forceInt(record.value('USL_TARIF'))
        isMainService = forceString(record.value('USL_CODE_USL')) != '' and tarif != 0
        local_params = {
            'MR_USL_N_CODE_MD': formatSNILS(forceString(record.value('MR_USL_N_CODE_MD_raw'))),
            'USL_LPU_1': self.getKODLPU(execPersonOrgStructureId),
        }
        if vidpomCode != '9':
            local_params['USL_DS2'] = forceString(record.value('DS2')).split(',')
            local_params['USL_DS3'] = forceString(record.value('DS3')).split(',')

        record.setValue('USL_KODLPU', self.getKODLPU(execPersonOrgStructureId))
        params['USL_KODLPU'] = self.getKODLPU(execPersonOrgStructureId)

        if not isMainService:
            record.setNull('USL_CRIT')

        if uslOk in [1, 2] and tarif != 0:
            begDate = forceDate(record.value('USL_DATE_IN'))
            eventBegDate = forceDate(record.value('SLUCH_DATE_1'))

            if begDate == eventBegDate:
                receivedFrom = forceString(record.value('receivedFrom'))
                record.setValue('USL_P_PER', toVariant(self.mapRecFrom.get(receivedFrom)))
            else:
                record.setValue('USL_P_PER', toVariant('4'))
            record.setValue('USL_DOPL', '')
            if forceString(record.value('KSG_KPG_N_KSG')):
                attributes = self.__getContractAttributes(forceRef(record.value('contract_id')))
                record.setValue('KSG_KPG_BZTSZ', format(forceDouble(attributes['BS'][forceDate(record.value('USL_DATE_OUT'))]), '.2f'))
                record.setValue('KSG_KPG_KOEF_U', format(forceDouble(attributes['U%s' % params['USL_KODLPU']][forceDate(record.value('USL_DATE_OUT'))]), '.5f'))
                coeffs = params['CSGCoefficients'][forceString(record.value('USL_CODE_USL'))][forceDate(record.value('USL_DATE_OUT'))]
                if isinstance(coeffs, tuple):
                    coefZ, coefUP = coeffs
                    record.setValue('KSG_KPG_KOEF_Z', format(forceDouble(coefZ), '.5f'))
                    record.setValue('KSG_KPG_KOEF_UP', format(forceDouble(coefUP), '.5f'))

            # костыль, потому что не знаю как проверить на NULL =(
            if tarif == -1:
                record.setValue('USL_TARIF', 0)
                record.setValue('USL_SUMV_USL', 0)
            elif vidpom != '32' and forceInt(record.value('USL_SUMV_USL')) > 0:
                self.processCoefficients(record, local_params)
            else:
                record.setValue('USL_SUMV_USL', format(forceDouble(record.value('USL_SUMV_USL')), '.2f'))
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
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.eventGroup.addRecord(_record)

        if params['toggleFlag'] == 2 and eventId not in params['doneVis']:
            params['doneVis'].add(eventId)
            params['toggleFlag'] = 0



    def writeDirectionCancer(self, directionCancerId):
        u"""Сведения об оформлении направления при подозрении или установленном диагнозе ЗНО"""
        stmt = u"""SELECT
aps1.value AS NAPR_NAPR_DATE,
  s2.miacCode AS NAPR_NAPR_MO,
  s2.infisCode AS NAPR_NAPR_LPU,
CASE aps3.value WHEN 'Направление к онкологу' THEN '1'
                WHEN 'Направление на биопсию' THEN '2'
                WHEN 'Направление на дообследование' THEN '3'
                WHEN 'Направление для первичного определения тактики обследования или тактики лечения' THEN '4' END AS NAPR_NAPR_V,
CASE aps4.value WHEN 'лабораторная диагностика' THEN '1'
                WHEN 'инструментальная диагностика' THEN '2'
                WHEN 'методы лучевой диагностики, за исключением дорогостоящих' THEN '3'
                WHEN 'дорогостоящие методы лучевой диагностики (КТ, МРТ, ангиография)' THEN '4' END AS NAPR_MET_ISSL,
s5.infis AS NAPR_NAPR_USL
FROM Action a
LEFT JOIN Person p ON p.id = a.person_id
LEFT JOIN ActionType at ON a.actionType_id = at.id and at.deleted = 0

LEFT JOIN ActionPropertyType apt1 ON apt1.actionType_id = at.id AND apt1.deleted = 0 AND apt1.shortName = 'directDate'
LEFT JOIN ActionProperty ap1 ON ap1.type_id = apt1.id AND ap1.action_id = a.id and ap1.deleted = 0
LEFT JOIN ActionProperty_Date aps1 on aps1.id = ap1.id

LEFT JOIN ActionPropertyType apt2 ON apt2.actionType_id = at.id AND apt2.deleted = 0 AND apt2.shortName = 'directOrg'
LEFT JOIN ActionProperty ap2 ON ap2.type_id = apt2.id AND ap2.action_id = a.id and ap2.deleted = 0
LEFT JOIN ActionProperty_Organisation aps2 on aps2.id = ap2.id
LEFT JOIN Organisation s2 ON s2.id = aps2.value

LEFT JOIN ActionPropertyType apt3 ON apt3.actionType_id = at.id AND apt3.deleted = 0 AND apt3.shortName = 'directOn'
LEFT JOIN ActionProperty ap3 ON ap3.type_id = apt3.id AND ap3.action_id = a.id and ap3.deleted = 0
LEFT JOIN ActionProperty_String aps3 on aps3.id = ap3.id

LEFT JOIN ActionPropertyType apt4 ON apt4.actionType_id = at.id AND apt4.deleted = 0 AND apt4.shortName = 'directRes'
LEFT JOIN ActionProperty ap4 ON ap4.type_id = apt4.id AND ap4.action_id = a.id and ap4.deleted = 0
LEFT JOIN ActionProperty_String aps4 on aps4.id = ap4.id

LEFT JOIN ActionPropertyType apt5 ON apt5.actionType_id = at.id AND apt5.deleted = 0 AND apt5.shortName = 'directServ'
LEFT JOIN ActionProperty ap5 ON ap5.type_id = apt5.id AND ap5.action_id = a.id and ap5.deleted = 0
LEFT JOIN ActionProperty_rbService aps5 on aps5.id = ap5.id
LEFT JOIN rbService s5 ON s5.id = aps5.value
where a.id = {0}""".format(directionCancerId)
        query = self._parent.db.query(stmt)
        if query.first():
            record = query.record()
            self.writeGroup('NAPR', self.naprFields, record)
            self.exportedDirectionCancers.add(directionCancerId)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        #TODO: дублирование кода? Сопоставить с COrder79XmlStreamWriter.writeClientInfo()

        sex = forceString(record.value('PERS_W'))
        birthDate = forceDate(record.value('PERS_DR'))
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        birthNumber = forceInt(record.value('birthNumber'))
        birthWeight = forceInt(record.value('birthWeight'))
        setDate = forceDate(record.value('SLUCH_DATE_1'))
        isJustBorn = birthDate.daysTo(setDate) < 29
        isAnyBirthDoc = forceString(record.value('PACIENT_NPOLIS'))
        socStatus = forceString(record.value('socStatus'))
        clientHasWork = forceInt(record.value('clientHasWork'))
        relativeId = forceRef(record.value('relativeId'))

        if isJustBorn and not isAnyBirthDoc and relativeId:
            record.setValue('PERS_FAM', u'НЕТ')
            record.setValue('PERS_IM', u'НЕТ')
            record.setValue('PERS_OT', u'НЕТ')
            relativeInfo = getClientInfo(relativeId, date=setDate)
            if relativeInfo:
                if relativeInfo.documentRecord:
                    record.setValue('PERS_DOCNUM', forceString(relativeInfo.documentRecord.value('number')))
                    record.setValue('PERS_DOCSER', forceString(relativeInfo.documentRecord.value('serial')))
                    record.setValue('PERS_DOCDATE', forceDate(relativeInfo.documentRecord.value('date')))
                    record.setValue('PERS_DOCORG', forceString(relativeInfo.documentRecord.value('origin')))
                    dtId = forceRef(relativeInfo.documentRecord.value('documentType_id'))
                    if dtId:
                        record.setValue('PERS_DOCTYPE', forceString(QtGui.qApp.db.translate('rbDocumentType', 'id', dtId, 'regionalCode')))
                    else:
                        record.setValue('PERS_DOCTYPE', ' ')
                if relativeInfo.compulsoryPolicyRecord:
                    pk = forceRef(relativeInfo.compulsoryPolicyRecord.value('policyKind_id'))
                    if pk:
                        record.setValue('PACIENT_VPOLIS', forceString(QtGui.qApp.db.translate('rbPolicyKind', 'id', pk, 'regionalCode')))
                    else:
                        record.setValue('PACIENT_VPOLIS', '3')
                    record.setValue('isActualPolicy', 1)
                    record.setValue('PACIENT_SPOLIS', forceString(relativeInfo.compulsoryPolicyRecord.value('serial')))
                    record.setValue('PACIENT_NPOLIS', forceString(relativeInfo.compulsoryPolicyRecord.value('number')))
                    if forceString(record.value('PACIENT_VPOLIS')) == '3':
                        record.setValue('PACIENT_ENP', forceString(relativeInfo.compulsoryPolicyRecord.value('number')))
                    insurrer = forceRef(relativeInfo.compulsoryPolicyRecord.value('insurer_id'))
                    if insurrer:
                        record.setValue('PACIENT_SMO', forceString(QtGui.qApp.db.translate('Organisation', 'id', insurrer, 'miacCode')))
                        record.setValue('PACIENT_SMO_OK', forceString(QtGui.qApp.db.translate('Organisation', 'id', insurrer, 'OKATO')))
        if isJustBorn:
            statZ = '1'
        elif birthDate.addYears(7) > setDate:
            statZ = '2'
        elif birthDate.addYears(14) > setDate:
            statZ = '3'
        else:
            if socStatus in ['c03', 'c04']:
                statZ = '4'
            else:
                if clientHasWork:
                    statZ = '5'
                elif socStatus == 'c07':
                    statZ = '6'
                elif birthDate.addYears(14) < setDate and not socStatus:
                    statZ = '7'
                elif socStatus:
                    statZ = '8'
                else:
                    statZ = None


        local_params = {
            'PACIENT_VNOV_D': birthWeight if isJustBorn and not isAnyBirthDoc and birthWeight <= 2500 else None,
            'PACIENT_NOVOR':  ('%s%s%s' % (sex[:1], birthDate.toString('ddMMyy'), birthNumber)) if isJustBorn and not isAnyBirthDoc else '0',
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
        for field, val in ( #('SLUCH_P_CEL', '3.0'),
                           ('SLUCH_USL_OK', '3'),
                           ('SLUCH_PROFIL', record.value('diagnosticProfile')),
                           ('SLUCH_NHISTORY', record.value('eventId'))):
            record.setValue(field, toVariant(val))


    def _fillDiagnosticService(self, record, params):
        for field, val in (('USL_KOL_USL', record.value('accountItemAmount')),
                           ('USL_SUMV_USL', record.value('accountItemSum')),
                           ('USL_CODE_USL', record.value('diagnosticServiceCode')),
                           ('USL_DATE_IN', record.value('actionBegDate')),
                           ('USL_DATE_OUT', record.value('actionEndDate'))):
            record.setValue(field, toVariant(val))


    def __getContractAttributes(self, contactId):
        result = self.contactAttributesMap.get(contactId, None)
        if result is None:
            result = CContractAttributesDescr(contactId)
            self.contactAttributesMap[contactId] = result
        return result


    def getKODLPU(self, orgStructureId):
        result = self.mapOrgStructureIdToKODLPU.get(orgStructureId, None)
        if result is None:
            db = self._parent.db
            table = db.table('OrgStructure')
            tmpId = orgStructureId
            bookkeeperCode = ''
            while tmpId:
                record = db.getRecordEx(table, [table['parent_id'], table['bookkeeperCode'], table['tfomsCode']], table['id'].eq(tmpId))
                bookkeeperCode = forceString(record.value('bookkeeperCode'))
                if not (bookkeeperCode and bookkeeperCode == forceString(record.value('tfomsCode'))):
                    tmpId = forceRef(record.value('parent_id'))
                    continue
                break
            self.mapOrgStructureIdToKODLPU[orgStructureId] = bookkeeperCode
            result = bookkeeperCode

        return result

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
        eventProfile = forceString(record.value('eventProfile'))
        eventProfileCode = forceString(record.value('eventProfileCode'))
        vidpom = forceString(record.value('vidpom'))
        purpose = forceInt(record.value('purpose'))
        if uslOk == 3 or uslOk == 0:  # амбулатория
            if eventProfile not in [u'ДВ4', u'ДВ2', u'ДС1', u'ДС2', u'ОПВ', u'ПН1'] \
                    and bool(re.match('^29', forceString(record.value('USL_CODE_USL'))))\
                    and forceDouble(record.value('USL_TARIF')) > 0 \
                    and purpose == 2 and vidpom != '9':
                record.setValue('USL_IDMASTER', forceInt(record.value('USL_IDSERV')))
            elif forceDouble(record.value('USL_SUMV_USL')) == 0.0 and eventProfile not in [u'ДВ4', u'ДВ2', u'ДС1', u'ДС2', u'ОПВ', u'ПН1'] and eventProfileCode not in ['r6021', 'r6022']:
                record.setValue('USL_IDMASTER', len(self.idmasterList) + 1)
            elif eventProfile == u'ДВ2' and forceString(record.value('USL_CODE_OPER'))[:7] in ['B04.023', 'B04.018', 'B04.028', 'B04.029', 'B04.001', 'B04.008'] or forceString(record.value('USL_CODE_OPER')) == 'B04.047.003':
                record.setValue('USL_IDMASTER', forceInt(record.value('USL_IDSERV')))
                if forceString(record.value('USL_CODE_OPER')) == 'B04.047.003':
                    self.masterId = forceInt(record.value('USL_IDSERV'))
            elif eventProfile == u'ДВ2':
                record.setValue('USL_IDMASTER', self.masterId)
            elif eventProfile in [u'ДВ4', u'ДВ2', u'ДС1', u'ДС2', u'ОПВ', u'ПН1'] and forceDouble(record.value('USL_TARIF')) == 0.0:
                record.setValue('USL_IDMASTER', len(self.idmasterList)+1)
            elif bool(re.match('^29[0-9]{2}[49]', forceString(record.value('USL_CODE_USL')))):
                record.setValue('USL_IDMASTER', forceInt(record.value('USL_IDSERV')))
            elif eventProfileCode in ['r6021', 'r6022']:
                record.setValue('USL_IDMASTER', forceInt(record.value('USL_IDSERV')))
            else:
                idServ = forceInt(record.value('USL_IDSERV'))
                for i in range(1, len(self.idmasterList) + 1):
                    self.records[i].setValue('USL_IDMASTER', idServ)
                record.setValue('USL_IDMASTER', len(self.idmasterList) + 1)
            pass
        else:  # стационар
            dateIn = forceDate(record.value('USL_DATE_IN')).toPyDate()
            dateOut = forceDate(record.value('USL_DATE_OUT')).toPyDate()
            isMainService = (forceString(record.value('USL_CODE_USL')) != '' and
                forceInt(record.value('USL_TARIF')) != 0)
            orgStruct = forceString(record.value('USL_PODR'))
            eventId = forceRef(record.value('eventId'))
            isTransferred = forceInt(record.value('isTransfered')) # self._parent.isTransferred(eventId)# forceBool(record.value('isTransferred'))

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
        isStom = forceString(record.value('vidpom')) == '9'
        if forceInt(record.value('USL_IDSERV')) > 0:
            if not isDiagnostic and not isStom:
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
        ds2 = forceString(self.records[0].value('SLUCH_DS2'))
        setDate = forceDate(self.records[0].value('SLUCH_DATE_1'))
        mkb = onkologyInfo.get('actionMKB')
        reab = forceInt(self.records[0].value('USL_REAB'))
        birthDate = forceDate(self.records[0].value('PERS_DR'))
        eventProfileCode = forceString(self.records[0].value('eventProfileCode'))

        for record in self.records[1:]:
            bedDays = 0 if record.isNull('USL_KD') else forceInt(record.value('USL_KD'))
            if (mkb == forceString(record.value('USL_DS1'))
                    and bedDays and onkologyInfo.get('ONK_USL_USL_TIP')):
                onkologyInfo['ONK_USL_IDS_USL'] = record.value('USL_IDSERV')
                break
        else:
            if onkologyInfo.get('ONK_USL_USL_TIP'):
                onkologyInfo['ONK_USL_IDS_USL'] = self.records[1].value('USL_IDSERV')

        if eventProfileCode in ['r6020', 'r6021', 'r6022', 'r6023', 'r6024']:
            self.records[0].setValue('SLUCH_PODR',
                self.records[-1].value('USL_PODR'))

        writer.checkerEventInfo(self.records[0])
        if forceString(self.records[0].value('DISP_SL_DISP')):
            appointmentsInfo = params['appointmentsInfo'].get(eventId, {})
            dispanserCode = forceString(self.records[0].value('dispanserCode'))
            self.records[0].setValue('DISP_SL_M_OKAZ', '1')
            self.records[0].setValue('DISP_SL_P_OTK', '0')
            if dispanserCode == '1':
                pr_d_n = '1'
            elif dispanserCode in ['2', '6']:
                pr_d_n = '2'
            else:
                pr_d_n = '3'
            self.records[0].setValue('DISP_SL_PR_D_N', pr_d_n)
            if pr_d_n in ['1', '2'] or forceString(self.records[0].value('DISP_SL_PR_DS2_N')) in ['1', '2']:
                self.records[0].setValue('DISP_SL_GR_D_N', '1')
            onkologyInfo.update(appointmentsInfo)

        record = CExtendedRecord(self.records[0], onkologyInfo)
        _sum = sum(forceDouble(format(forceDouble(rec.value('USL_SUMV_USL')), '.2f')) for rec in self.records[1:])
        record.setValue('SLUCH_SUMV', _sum)

        writer.writeGroup('SLUCH', writer.eventFields1, record,
                          subGroup=writer.eventSubGroup1,
                          closeGroup=False, dateFields=writer.eventDateFields)

        for rec in self.records[1:]:
            if (forceBool(rec.value('isDiagnostic')) and
                    forceString(rec.value('serviceCode'))[:3] == 'A16'):
                continue
            crit = forceString(rec.value('USL_CRIT'))
            isCovidSupples = (uslOk in [1, 3]
                              and ds1 in ('U07.1', 'U07.2')
                              and crit != 'stt5'
                              and reab != 1
                              and not ('O00' <= ds2 <= 'O99' or 'Z34' <= ds2 <= 'Z35')
                              and birthDate.addYears(18) <= setDate)
            isMaster = rec.value('USL_IDSERV') == rec.value('USL_IDMASTER')

            local_params = {}
            local_params.update(onkologyInfo)
            if isCovidSupples and isMaster:
                local_params.update(medicalSuppliesInfo)
            else:
                rec.setValue('COVID_LEK_WEI', None)
            if uslOk == 1 and not isMaster and implantsInfo:
                endDate = forceDate(rec.value('USL_DATE_OUT'))

                codeList = implantsInfo['MED_DEV_CODE_MEDDEV']
                dateList = implantsInfo['MED_DEV_DATE_MED']
                numberList = implantsInfo['MED_DEV_NUMBER_SER']
                _codeList = []
                _dateList = []
                _numberList = []
                for date in dateList:
                    dt = forceDate(date)
                    if dt == endDate:
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
        u'onkoCure': ('ONK_USL_USL_TIP', CRbN013TypeOnkoCureCache),
        u'onkoLekType': ('ONK_USL_HIR_TIP', CRbN014HirLekTypeCache),
        u'onkoLekLines': ('ONK_USL_LEK_TIP_L', CRbN015LekLinesCache),
        u'onkoCycleLek': ('ONK_USL_LEK_TIP_V', CRbN016CycleLekCache),
        u'onkoRadTerap': ('ONK_USL_LUCH_TIP', mapLuchTip)
    }

    __mapPropShortName__ = {'onkoXRDose': 'ONK_SL_SOD',
                            'onkoFR': 'ONK_SL_K_FR',
                            'weight': 'ONK_SL_WEI',
                            'height': 'ONK_SL_HEI',
                            'onkoSurf': 'ONK_SL_BSA'}

    mapProtName = {
        'onkoGistRej': '0',
        'onkoHirDeny': '1',
        'onkoChimDeny': '2',
        'onkoXRDeny': '3',
        'onkoHirRej': '4',
        'onkoChimRej': '5',
        'onkoXRRej': '6',
        'onkoGistDeny': '8'
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
            ControlListOnkoAction.id AS controlListOnkoActionId,
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
                  AND AT.flatCode  = 'CRIT'
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
            (mkb[:3] >= 'D00' and mkb[:3] <= 'D09') or
            (mkb[:3] >= 'D45' and mkb[:3] <= 'D47'))) else 0)
        isOnkology = (mkb[:1] == 'C' or (
                (mkb[:3] >= 'D00' and mkb[:3] <= 'D09') or
                (mkb[:3] >= 'D45' and mkb[:3] <= 'D47'))
            ) and dsOnk == 0
        return dsOnk, isOnkology


    def _processOnkRecord(self, record, parent):
        eventId = forceRef(record.value('eventId'))

        if eventId != self.__currentEventId:
            self.__currentEventId = eventId
            self.serviceNum = 1

        data = COnkologyInfo._processOnkRecord(self, record, parent)
        if data['isOnkology'] and not data.get('ONK_SL_MTSTZ', 0):
            data['ONK_SL_MTSTZ'] = '0'

        if data['isOnkology'] and not data.get('ONK_SL_K_FR', 0):
            data['ONK_SL_K_FR'] = '0'

        if data.has_key('ONK_USL_USL_TIP'):
            if data.get('ONK_SL_DS1_T') is None:
                data['ONK_SL_DS1_T'] = '0'
            if data.get('ONK_USL_USL_TIP') is None:
                data['ONK_USL_USL_TIP'] = '0'
            if data.get('ONK_USL_USL_TIP'):
                data['ONK_USL_NOM_USL'] = self.serviceNum

            self.serviceNum += 1

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

        if data.has_key('ONK_USL_USL_TIP'):
            if data.get('ONK_USL_USL_TIP') not in ['3', '4']:
                data['ONK_USL_LUCH_TIP'] = '0'

            if data.get('ONK_USL_USL_TIP') != '1':
                data['ONK_USL_HIR_TIP'] = '0'

            if data.get('ONK_USL_USL_TIP') not in ('3', '4'):
                data['ONK_SL_SOD'] = '0'

            if data.get('ONK_USL_USL_TIP') != '2':
                data['ONK_USL_LEK_TIP_L'] = '0'
                data['ONK_USL_LEK_TIP_V'] = '0'


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
        _id = forceRef(record.value('controlListOnkoActionId'))
        action = CAction.getActionById(_id) if _id else None

        if action:
            data['actionMKB'] = forceString(action.getRecord().value('MKB'))
            onkoReason = action.getPropertyByShortName('onkoReason')
            data['ONK_SL_DS1_T'] = self.__mapDS1T__.get(onkoReason.getValue())
            for prop in action.getProperties():
                shortName = prop.type().shortName
                name = prop.type().name
                descr = prop.type().descr

                if shortName in self.mapProtName and data['ONK_SL_DS1_T'] in [0, 1, 2]:
                    date = prop.getValueScalar()
                    if (date is not None and isinstance(date,  QDate)
                            and date.isValid() and name):
                        data.setdefault('B_PROT_PROT', []).append(descr)
                        data.setdefault('B_PROT_D_PROT', []).append(date.toString(Qt.ISODate))
                elif shortName in self.mapOnkUsl:
                    fieldName, mapName = self.mapOnkUsl.get(shortName)
                    data[fieldName] = mapName.get(prop.getValue())
                elif shortName in self.__mapPropShortName__:
                    data[self.__mapPropShortName__[shortName]] = prop.getValue()
                elif prop.type().descr == 'PPTR':
                    val = prop.getValue()
                    if val:
                        data['ONK_USL_PPTR'] = mapPptr.get(val.lower(), '0')

            if not data.get('ONK_USL_PPTR'):
                data['ONK_USL_PPTR'] = '0'
        else:
            data['ONK_SL_DS1_T'] = '0'
            data['ONK_SL_MTSTZ'] = '0'
            data['ONK_SL_SOD'] = '0'
            data['ONK_SL_K_FR'] = '0'


    def _processConsilium(self, record, data):
        COnkologyInfo._processConsilium(self, record, data)

        if not data.get('CONS_PR_CONS') and data['isOnkology']:
            data['CONS_PR_CONS'] = '0'


    def _processMedicalSupplies(self, record, data):
        result = COnkologyInfo._processMedicalSupplies(self, record, data)
        return result

# ******************************************************************************

class CPersonalDataWriter(COrder79PersonalDataWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = (('ID_PAC', 'FAM', 'IM', 'OT', 'W',)
                    + COrder79PersonalDataWriter.clientDateFields +
                    ('DOST', 'FAM_P', 'IM_P', 'OT_P', 'W_P', 'DR_P', 'MR', 'DOCTYPE',
                     'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG', 'SNILS', 'OKATOG',
                     'OKATOP', 'ADRES', 'KLADR', 'DOM', 'KVART', 'KORP'))
    clientDateFields = COrder79PersonalDataWriter.clientDateFields + ('DOCDATE', 'DR_P',)

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


class CAppointmentsInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId, '1' AS NAZ_NAZ_N,
CASE aps1.value WHEN 'консультацию в мед организацию по месту прикрепления' THEN '1' 
WHEN 'консультацию в иную мед организацию' THEN '2' 
WHEN 'обследование' THEN '3' 
WHEN 'в дневной стационар' THEN '4' 
WHEN 'госпитализацию' THEN '5' 
WHEN 'в реабилитационное отделение' THEN '6' END AS NAZ_NAZR,
formatSNILS(p.SNILS) AS NAZ_NAZ_IDDOKT,
s2.regionalCode AS NAZ_NAZ_SP,
CASE aps3.value WHEN 'лабораторная диагностика' THEN '1'
              WHEN 'инструментальная диагностика' THEN '2'
              WHEN 'методы лучевой диагностики, за исключением дорогостоящих' THEN '3'
              WHEN 'дорогостоящие методы лучевой диагностики (КТ, МРТ, ангиография)' THEN '4' END AS NAZ_NAZ_V,
s4.infis AS NAZ_NAZ_USL,
aps5.value AS NAZ_NAPR_DATE,
CASE WHEN aps1.value in ('консультацию в иную мед организацию', 'обследование') THEN s6.miacCode END AS NAZ_NAPR_MO,
CASE WHEN aps1.value in ('консультацию в иную мед организацию', 'обследование') THEN CASE WHEN s6.OKATO = '60000' THEN s6.infisCode ELSE '0' END END AS NAZ_NAPR_LPU,
s7.regionalCode AS NAZ_NAZ_PMP,
s8.tfomsCode AS NAZ_NAZ_PK
FROM Account_Item 
LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
LEFT JOIN Action a on a.event_id = Account_Item.event_id
LEFT JOIN Person p ON p.id = a.person_id
LEFT JOIN ActionType at ON a.actionType_id = at.id and at.deleted = 0

LEFT JOIN ActionPropertyType apt1 ON apt1.actionType_id = at.id AND apt1.deleted = 0 AND apt1.shortName = 'directOn'
LEFT JOIN ActionProperty ap1 ON ap1.type_id = apt1.id AND ap1.action_id = a.id and ap1.deleted = 0
LEFT JOIN ActionProperty_String aps1 on aps1.id = ap1.id

LEFT JOIN ActionPropertyType apt2 ON apt2.actionType_id = at.id AND apt2.deleted = 0 AND apt2.shortName = 'directSpec'
LEFT JOIN ActionProperty ap2 ON ap2.type_id = apt2.id AND ap2.action_id = a.id and ap2.deleted = 0
LEFT JOIN ActionProperty_rbSpeciality aps2 on aps2.id = ap2.id
LEFT JOIN rbSpeciality s2 ON s2.id = aps2.value

LEFT JOIN ActionPropertyType apt3 ON apt3.actionType_id = at.id AND apt3.deleted = 0 AND apt3.shortName = 'directRes'
LEFT JOIN ActionProperty ap3 ON ap3.type_id = apt3.id AND ap3.action_id = a.id and ap3.deleted = 0
LEFT JOIN ActionProperty_String aps3 on aps3.id = ap3.id

LEFT JOIN ActionPropertyType apt4 ON apt4.actionType_id = at.id AND apt4.deleted = 0 AND apt4.shortName = 'directServ'
LEFT JOIN ActionProperty ap4 ON ap4.type_id = apt4.id AND ap4.action_id = a.id and ap4.deleted = 0
LEFT JOIN ActionProperty_rbService aps4 on aps4.id = ap4.id
LEFT JOIN rbService s4 ON s4.id = aps4.value

LEFT JOIN ActionPropertyType apt5 ON apt5.actionType_id = at.id AND apt5.deleted = 0 AND apt5.shortName = 'directDate'
LEFT JOIN ActionProperty ap5 ON ap5.type_id = apt5.id AND ap5.action_id = a.id and ap5.deleted = 0
LEFT JOIN ActionProperty_Date aps5 on aps5.id = ap5.id

LEFT JOIN ActionPropertyType apt6 ON apt6.actionType_id = at.id AND apt6.deleted = 0 AND apt6.shortName = 'directOrg'
LEFT JOIN ActionProperty ap6 ON ap6.type_id = apt6.id AND ap6.action_id = a.id and ap6.deleted = 0
LEFT JOIN ActionProperty_Organisation aps6 on aps6.id = ap6.id
LEFT JOIN Organisation s6 ON s6.id = aps6.value

LEFT JOIN ActionPropertyType apt7 ON apt7.actionType_id = at.id AND apt7.deleted = 0 AND apt7.shortName = 'directProfile'
LEFT JOIN ActionProperty ap7 ON ap7.type_id = apt7.id AND ap7.action_id = a.id and ap7.deleted = 0
LEFT JOIN ActionProperty_rbMedicalAidProfile aps7 on aps7.id = ap7.id
LEFT JOIN rbMedicalAidProfile s7 ON s7.id = aps7.value

LEFT JOIN ActionPropertyType apt8 ON apt8.actionType_id = at.id AND apt8.deleted = 0 AND apt8.shortName = 'directHB'
LEFT JOIN ActionProperty ap8 ON ap8.type_id = apt8.id AND ap8.action_id = a.id and ap8.deleted = 0
LEFT JOIN ActionProperty_rbHospitalBedProfile aps8 on aps8.id = ap8.id
LEFT JOIN rbHospitalBedProfile s8 ON s8.id = aps8.value
where at.flatCode = 'appointments' and Account_Item.reexposeItem_id IS NULL AND a.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY a.id""".format(idList=self._idList)
        return stmt


class CObrInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            rbService.infis as serviceInfis
        FROM Account_Item
        LEFT JOIN rbService ON rbService.id = Account_Item.service_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND Account_Item.action_id IS NOT NULL
          AND rbService.infis regexp '^29[0-9]{{2}}2[0-9]{{6}}'
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""".format(idList=self._idList)
        return stmt


class CCSGCoefficients(CSeriesHolder):
    def __init__(self):
        CSeriesHolder.__init__(self, CVariantSeries)
        self.__loadData()


    def __loadData(self):
        db = QtGui.qApp.db
        table = db.table('ro_CSGCoefficients')
        recordList = db.getRecordList(table,
                                      [table['CSGCode'],
                                       table['KOEF_Z'],
                                       table['KOEF_UP'],
                                       table['begDate']
                                       ],
                                      )
        for record in recordList:
            code      = forceString(record.value('CSGCode'))
            begDate   = forceDate(record.value('begDate'))
            valueZ     = forceDouble(record.value('KOEF_Z'))
            valueUP = forceDouble(record.value('KOEF_UP'))
            self.append(code, begDate, (valueZ, valueUP))
# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport

    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR61TFOMSNative,
                      #accNum='06ALL-14',
                      eventIdList=[4],
                      #limit=1000,
                      configFileName='S11AppRostov.ini')
