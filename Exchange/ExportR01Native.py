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

u"""Экспорт реестра в формате XML. Республика Адыгея"""

import json
import re
import shutil

from operator import itemgetter
import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QRegExp, QTextCodec

from Accounting.Utils import CContractAttributesDescr, CVariantSeries
from Events.Action import CAction
from Exchange.Export import CMultiRecordInfo, updateDictOfListsItem, record2DictOfLists
from Exchange.ExportR08HospitalV59 import mapDiagRslt, mapPptr
from Exchange.Order79Export import (COrder79ExportWizard, COrder79ExportPage1, COrder79PersonalDataWriter,
                                    CExtendedRecord, COrder79ExportPage2,
                                    COrder79v3XmlStreamWriter)
from Exchange.Order200Export import COnkologyInfo, mapLuchTip
from Exchange.Utils import compressFileInZip

from Exchange.Ui_ExportR01NativePage1 import Ui_ExportPage1
from Registry.Utils import getClientInfo
from library.Counter import CCounterController

from library.DbEntityCache import CDbEntityCache
from library.Series import CSeriesHolder
from library.Utils import forceInt, forceString, forceDate, forceDouble, forceRef, forceBool, toVariant, forceStringEx

# ******************************************************************************

VERSION = '3.2'

# выводит в консоль имена невыгруженных полей
DEBUG = False

# ******************************************************************************

def exportR01Native(widget, accountId, accountItemIdList, accountIdList=None, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setAccountIdList(accountIdList)
    QtGui.qApp.setCounterController(CCounterController(wizard))
    wizard.exec_()
    QtGui.qApp.setCounterController(None)


# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта республика Адыгея"""

    def __init__(self, parent=None):
        prefix = 'R01Native'
        title = u'Мастер экспорта реестра услуг для республики Адыгеи'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1, CExportPage2, parent)
        self.__baseFileName = None


    def clearCache(self):
        u"""Очищает кешированные значения переменных"""
        self.__baseFileName = None


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
        u"""Возвращает имя архива"""
        if self.page1.cmbRegistryType.currentIndex() == CExportPage1.registryTypeIdentity:
            return 'H' + self._getBaseFileName() + '.zip'
        return self._getBaseFileName() + '.zip'

    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""
        return self._getBaseFileName(addPostfix) + '.xml'

    def _getBaseFileName(self, addPostfix=True):
        u"""АМ поликлиника
АС поликлиника онко  на основании диагноза С, D45-D47
НМ стационар
НС стационар онко.  на основании диагноза С, D45-D47
S согаз-мед Адыгея (01004)
Т иногородние ( край и далее)  тф.омс
AM010034S01004_23016.zip
AM010034T01_23015.zip
HM010034S01004_23014.zip
AM  010034   S    01004_23016
АМ поликлиника
АС поликлиника онко  на основании диагноза С, D45-D47
НМ стационар
НС стационар онко.  на основании диагноза С, D45-D47
010034  - Реестровый номер медицинской организации (F003)
T – ТФОМС;
S – СМО
01004 – Платильщик F002
YY – две последние цифры порядкового номера года отчетного периода.
MM – порядковый номер месяца отчетного периода:
N – порядковый номер пакета."""
        tableOrganisation = self.db.table('Organisation')
        if self.page1.cmbRegistryType.currentIndex() == CExportPage1.registryTypeIdentity:
            code = forceString(self.db.translate(tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'miacCode'))[:6]
            month = self.info['accDate'].month()
            year = self.info['accDate'].year()
            packetNumber = self.page1.edtPacketNumber.value()
            result = u'I{0}01_{1:02d}{2:02d}{3}'.format(code, int(str(year)[2:]), month, packetNumber)
            return result
        if self.__baseFileName:
            result = self.__baseFileName
        else:
            code = forceString(self.db.translate(tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'miacCode'))[:6]
            month = self.info['accDate'].month()
            year = self.info['accDate'].year()
            typeId = self.info['typeId']
            payerId = self.info['payerId']
            area = forceString(self.db.translate(tableOrganisation, 'id', payerId, 'area'))
            payerCode = forceString(self.db.translate(tableOrganisation, 'id', payerId, 'infisCode')) if area == '0100000000000' else '01'
            typePayer = 'S' if area == '0100000000000' else 'T'
            typeCode = forceString(self.db.translate('rbAccountType', 'id', typeId, 'regionalCode'))
            packetNumber = self.page1.edtPacketNumber.value()
            result = u'{0}{1}{2}{3}_{4:02d}{5:02d}{6}'.format(typeCode, code, typePayer, payerCode, int(str(year)[2:]), month, packetNumber)
            self.__baseFileName = result
        return result

    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        if self.page1.cmbRegistryType.currentIndex() == CExportPage1.registryTypeIdentity:
            return u'H%s' % self._getXmlBaseFileName(addPostfix)
        else:
            return self._getXmlBaseFileName(addPostfix)

# ******************************************************************************


class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):

    # Наследие МКТ: понятия ФЛК и Счет ОМС перепутаны. Поэтому в интерфейсе сделал как им привычно,
    # а в коде оставил как правильно было бы
    registryTypeFlk = 0  # Счет ОМС
    registryTypeIdentity = 1  # ФЛК (идентификация полисных данных)

    u"""Первая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        xmlWriter = (CExportXmlStreamWriter(self),
                     CPersonalDataWriter(self, version=VERSION))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.initFields()
        self.accountIdList = []
        self.edtPacketNumber.setEnabled(False)
        self.edtPacketNumber.setValue(0)


    def setExportMode(self, flag):
        self.cmbRegistryType.setEnabled(not flag)
        COrder79ExportPage1.setExportMode(self, flag)
        self.edtPacketNumber.setEnabled(False)


    def setAccountIdList(self, accountIdList):
        self.accountIdList = accountIdList


    def initFields(self):
        self.query_fields = {
            # для отладки
            'aiId': 'Account_Item.id',
            'eventId': 'Account_Item.event_id',
            'actionTypeFlatCode': 'ActionType.flatCode',
            'coefficients': 'Account_Item.usedCoefficients',
            'contract_id': 'Event.contract_id',
            'PR_NOV': '0',
            # PACIENT_*
            'PACIENT_ID_PAC': 'Event.client_id',
            'PACIENT_VPOLIS': 'rbPolicyKind.regionalCode',
            'PACIENT_SPOLIS': "IF(rbPolicyKind.regionalCode = '1', LEFT(ClientPolicy.serial, 10), '')",
            'PACIENT_NPOLIS': "ClientPolicy.number",
            'PACIENT_ENP': "IF(rbPolicyKind.regionalCode = '3', ClientPolicy.number, '')",
            'PACIENT_SMO': 'Insurer.infisCode',
            'PACIENT_SMO_NAM': "Insurer.fullName",
            'PACIENT_SMO_OGRN': "Insurer.OGRN",
            'PACIENT_SMO_OK': "Insurer.OKATO",
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
            # Z_SL_*
            'lastEventId': 'Event.id',
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
            # Z_SL
            'Z_SL_IDCASE': 'Account_Item.event_id',
            'Z_SL_USL_OK': "IF(rbEventProfile.code = 'r6020', 3, rbMedicalAidType.regionalCode)",
            'Z_SL_VIDPOM': """CASE WHEN rbSpeciality.isHigh = 0 THEN '11'
                                            WHEN rbSpeciality.isHigh = 1 AND rbSpeciality.federalCode in ('39', '49', '76') THEN '12'
                                            ELSE '13' END""",
            'Z_SL_NPR_MO': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(RelegateOrg.miacCode) > 0 THEN RelegateOrg.miacCode ELSE '0' END END",
            'Z_SL_NPR_DATE': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN IFNULL(Event.srcDate, DATE('1905-01-01')) END",
            'Z_SL_LPU': 'PersonOrganisation.miacCode',
            'Z_SL_DATE_Z_1': "Event.setDate",
            'Z_SL_DATE_Z_2': 'Event.execDate',
            'Z_SL_KD_Z': "''",
            'Z_SL_VNOV_M': None,
            'Z_SL_RSLT': 'EventResult.federalCode',
            'Z_SL_ISHOD': 'rbDiagnosticResult.federalCode',
            'Z_SL_OS_SLUCH': None,
            'Z_SL_VB_P': """IF((SELECT COUNT(DISTINCT Action.id)
                    FROM Action
                    LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
                    WHERE Action.event_id = Event.id
                      AND Action.deleted = 0
                      AND ActionType.flatCode = 'moving') >= 2, 1, '')""",
            'Z_SL_IDSP': '0',
            'Z_SL_SUMV': '0',
            # SL
            'SL_SL_ID': '1',
            'SL_PODR': None,
            'SL_PROFIL': None,
            'SL_PROFIL_K': None,
            'SL_DET': "CASE WHEN rbSpeciality.federalCode in ('18','19','102','20','21','22','68', '37') THEN 1 ELSE 0 END",
            'SL_NHISTORY': None,
            'SL_P_PER': None,
            'SL_DATE_1': "Event.setDate",
            'SL_DATE_2': 'Event.execDate',
            'SL_KD': "''",
            'SL_WEI': None,
            'SL_DS0': """CASE WHEN LEFT(rbService.infis, 2) in ('st', 'ds') THEN (SELECT MAX(DS0.MKB)
                              FROM Diagnostic AS DC0
                              LEFT JOIN Diagnosis AS DS0 ON DS0.id = DC0.diagnosis_id
                              WHERE DC0.id in (
                                    SELECT dc.id
                                    FROM Diagnostic dc
                                    LEFT JOIN rbDiagnosisType dt on dt.id = dc.diagnosisType_id
                                    WHERE dc.event_id = Account_Item.event_id AND dc.deleted = 0 AND dt.code = '7')) END""",
            'SL_DS1': None,
            'SL_C_ZAB': 'IFNULL(rbDiseaseCharacter_Identification.value, 3)',
            'SL_DS_ONK': '0',
            'SL_DN': None,
            'SL_CODE_MES1': 'rbService_Identification.value',
            'SL_REAB': None,
            'SL_PRVS': 'rbSpeciality.federalCode',
            'SL_VERS_SPEC': "'V021'",
            'SL_IDDOKT': 'formatSNILS(Person.SNILS)',
            'SL_ED_COL': '1',
            'SL_TARIF': None,
            'SL_SUM_M': None,

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

            'NAPR_FROM_NPR_MO': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(RelegateOrg.miacCode) > 0 THEN RelegateOrg.miacCode ELSE '0' END END",
            'NAPR_FROM_NAPUCH': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(RelegateOrg.infisCode) > 0 THEN RelegateOrg.infisCode ELSE '0' END END",
            'NAPR_FROM_NOM_NAP': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN CASE WHEN LENGTH(Event.srcNumber) > 0 THEN LEFT(Event.srcNumber, 16) ELSE '0' END END",
            'NAPR_FROM_NAPDAT': "CASE WHEN Event.relegateOrg_id IS NOT NULL THEN IFNULL(Event.srcDate, DATE('1905-01-01')) END",
            'receivedFrom': u"""CASE WHEN IF(rbEventProfile.code = 'r6020', 3, rbMedicalAidType.code) IN ('1', '2', '3', '7') THEN (SELECT APS.value FROM Action AS A
                LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                LEFT JOIN ActionProperty AP ON AP.action_id = A.id
                LEFT JOIN ActionPropertyType APT ON AP.type_id = APT.id
                LEFT JOIN ActionProperty_String APS ON APS.id = AP.id
                WHERE A.event_id = Event.id
                  AND AT.flatCode = 'received' AND A.deleted = 0
                  AND AP.deleted = 0 AND APT.deleted =0
                  AND APT.name LIKE 'Кем направлен'
                LIMIT 0,1) END""",
            'isTransfered': u"""CASE WHEN IF(rbEventProfile.code = 'r6020', 3, rbMedicalAidType.code) in ('1', '2', '3', '7') THEN EXISTS(SELECT NULL FROM Action AS A
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
            'USL_VID_VME': None,
            'ActionPersonId': 'ActionPerson.id',
            'USL_PODR': None,
            'USL_PROFIL': None,
            'USL_DET': "CASE WHEN rbSpeciality.federalCode in ('18','19','102','20','21','22','68', '37') THEN 1 ELSE 0 END",
            'USL_NPL': None,
            'USL_P_OTK': '0',
            'USL_REAB': None,
            'USL_DATE_IN': None,
            'USL_DATE_OUT': None,
            'USL_DS': None,
            'USL_CODE_USL': 'rbService.code',
            'USL_KOL_USL': 'Account_Item.amount',
            'USL_TARIF': 'Account_Item.price',
            'USL_SUMV_USL': 'Account_Item.sum',
            'KSG_KPG_SL_K': "0",
            'KSG_KPG_IT_SL': None,
            'MR_USL_N_MR_N': 1,
            'MR_USL_N_PRVS': None,
            'USL_CODE_OPER': u"""IF(rbEventProfile.regionalCode IN ('ДВ2', 'ДВ4', 'ДС3', 'ДС4', 'ОПВ', 'ПН2', 'УД1', 'УД2')
                                OR rbMedicalAidType.federalCode = '9'
                                OR rbEventProfile.code in ('r6021', 'r6022', 'r6023', 'r6024', 'r6025', 'r6026', 'r6027', 'r6028', 'r6029'), rbService.infis, NULL)""",
            'USL_KSGA': u"""IF(rbMedicalAidType.federalCode = '9'
                                OR rbEventProfile.code in ('r6021', 'r6022', 'r6023', 'r6024', 'r6025', 'r6026', 'r6027', 'r6028', 'r6029'), rbService.infis, NULL)""",
            # PERS_*
            'PERS_ID_PAC': 'Event.client_id',
            'PERS_FAM': 'UPPER(Client.lastName)',
            'PERS_IM': 'UPPER(Client.firstName)',
            'PERS_OT': 'UPPER(Client.patrName)',
            'PERS_W': 'Client.sex',
            'PERS_DR': 'Client.birthDate',
            'PERS_MR': 'Client.birthPlace',
            'PERS_DOCTYPE': 'rbDocumentType.regionalCode',
            'PERS_DOCSER': 'ClientDocument.serial',
            'PERS_DOCNUM': 'ClientDocument.number',
            'PERS_SNILS': 'formatSNILS(Client.SNILS)',
            'PERS_DOCDATE': 'ClientDocument.date',
            'PERS_DOCORG': 'ClientDocument.origin',
            'PERS_FAM_P': 'UPPER(relatedClient.lastName)',
            'PERS_IM_P': 'UPPER(relatedClient.firstName)',
            'PERS_OT_P': 'UPPER(relatedClient.patrName)',
            'PERS_W_P': "IFNULL(relatedClient.sex, '')",
            'PERS_DR_P': 'relatedClient.birthDate',
            'relativeId': 'Event.relative_id',
            # KSG_KPG
            'KSG_KPG_N_KSG': """IF(rbService.code LIKE 'st%' or rbService.code LIKE 'ds%',(CASE
                WHEN (ActionType.serviceType = 4 OR (ActionType.code LIKE 'A%%' OR ActionType.code LIKE 'B%%')) THEN '0'
                ELSE rbService.code
              END), '') """,
            'KSG_KPG_VER_KSG': """IF(rbService.code LIKE 'st%' or rbService.code LIKE 'ds%', YEAR(Event.execDate), '')""",
            'KSG_KPG_KSG_PG': """CASE
                    WHEN rbService.code LIKE 'st__.___._' OR rbService.code LIKE 'ds__.___._'THEN 1
                    WHEN rbService.code LIKE 'st__.___' OR rbService.code LIKE 'ds__.___'THEN 0
                    ELSE ''
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
            'eventPurposeCode': 'rbEventTypePurpose.regionalCode', # для Z_SL_NSVOD
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
        self.query_fields['SL_PODR'] = None
        self.query_fields['SL_PROFIL'] = 'rbMedicalAidProfile.code'
        self.query_fields['SL_NHISTORY'] = 'Event.id'
        self.query_fields['SL_DS1'] = 'Diagnosis.MKB'
        self.query_fields['Z_SL_IDSP'] = '29'
        self.query_fields['MR_USL_N_PRVS'] = 'COALESCE(VisitSpec.federalCode, ActionSpec.federalCode, rbSpeciality.federalCode)'
        self.query_fields['MR_USL_N_CODE_MD'] = 'formatSNILS(COALESCE(VisitPerson.SNILS, ActionPerson.SNILS, Person.SNILS))'
        self.query_fields['USL_PROFIL'] = 'COALESCE(VisitProfile.code, ActionProfile.code)'
        self.query_fields['USL_DATE_IN'] = 'COALESCE(Visit.DATE, Action.begDate)'
        self.query_fields['USL_DATE_OUT'] = 'COALESCE(Visit.DATE, Action.endDate, Event.execDate)'
        self.query_fields['visitDate'] = 'COALESCE(Visit.DATE, DATE(Action.begDate))'
        self.query_fields['USL_DS'] = "IF(Action.MKB != '' AND rbMedicalAidType.federalCode = '9', Action.MKB, Diagnosis.MKB)"
        self.query_fields['USL_P_OTK'] = u"""CASE WHEN Action.status = 6 AND rbEventProfile.regionalCode IN ('ДВ4', 'ДС1', 'ДВ4', 'УД1', 'ДВ2', 'УД2') THEN '1' ELSE '0' END"""
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
    LEFT JOIN rbSpeciality AS VisitSpec ON VisitSpec.id = VisitPerson.speciality_id
    LEFT JOIN rbMedicalAidProfile AS VisitProfile ON VisitProfile.id = VisitSpec.medicalAidProfile_id
    LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
WHERE rbMedicalAidType.code = '6'
AND Account_Item.reexposeItem_id IS NULL
AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
AND {idList}\n""".format(fields=self.prepare_query_field(), idList=idList, commonTables=commonTables)


    def createStacQuery(self, idList, commonTables, actionTables):
        self.query_fields['SL_PODR'] = 'IF(ActionLeaved.id IS NOT NULL, LeavedOrgStructure.infisCode, PersonOrgStructure.infisCode)'
        self.query_fields['SL_PROFIL'] = '''rbMedicalAidProfile.code'''
        self.query_fields['SL_NHISTORY'] = 'CASE WHEN LENGTH(Event.externalId) > 0 THEN Event.externalId ELSE Event.id END'
        self.query_fields['SL_PROFIL_K'] = """IFNULL((SELECT si.value FROM rbSpeciality
LEFT JOIN rbSpeciality_Identification si ON rbSpeciality.id = si.master_id AND si.deleted = 0
LEFT JOIN rbAccountingSystem `as` ON si.system_id = `as`.id
WHERE `as`.code = 'PROFIL_K' AND rbSpeciality.id = IF(ActionType.serviceType IN (9, 4), ActionSpec.id, IFNULL(UslSpec.id, rbSpeciality.id)) LIMIT 1), MovingHBP.tfomsCode)"""
        self.query_fields['SL_DS1'] = 'Diagnosis.MKB'
        self.query_fields['Z_SL_IDSP'] = '33'
        self.query_fields['Z_SL_VIDPOM'] = "'31'"
        self.query_fields['MR_USL_N_PRVS'] = '''IF(ActionType.serviceType IN (9, 4), ActionSpec.federalCode, IFNULL(UslSpec.federalCode, rbSpeciality.federalCode))'''
        self.query_fields['MR_USL_N_CODE_MD'] = '''formatSNILS(IF(ActionType.serviceType IN (9, 4), ActionPerson.SNILS, IFNULL(UslPerson.SNILS, Person.SNILS)))'''
        self.query_fields['USL_PODR'] = 'IF(ActionLeaved.id IS NOT NULL, LeavedOrgStructure.infisCode, PersonOrgStructure.infisCode)'
        self.query_fields['USL_PROFIL'] = u'''IF(Event_CSG.id is not null, MovingHBPMedicalAidProfile.code, IF(ActionType.serviceType = 9,  5, ActionProfile.code))'''
        self.query_fields['USL_CRIT'] = "IFNULL(Crit.code,'')"
        self.query_fields['USL_DATE_IN'] = """CASE WHEN Action.begDate IS NOT NULL THEN Action.begDate ELSE Event_CSG.begDate END"""
        self.query_fields['USL_DATE_OUT'] = """CASE WHEN Action.endDate IS NOT NULL THEN Action.endDate ELSE Event_CSG.endDate END"""
        self.query_fields['USL_DS'] = """CASE WHEN Action.MKB != '' THEN Action.MKB
             WHEN Event_CSG.id is not null then Event_CSG.MKB 
             ELSE Diagnosis.MKB
             END"""
        self.query_fields['UslOrgStructureId'] = 'COALESCE(ActionPerson.orgStructure_id, Person.orgStructure_id)'
        self.query_fields['visitDate'] = 'NULL'
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
        self.query_fields['SL_KD'] = """CASE WHEN rbMedicalAidType.code IN ('1', '2', '3', '7') AND IFNULL(rbEventProfile.code, '') != 'r6020'
        THEN WorkDays(Event_CSG.begDate, Event_CSG.endDate, EventType.weekProfileCode, rbMedicalAidType.federalCode='7')
        ELSE 0 END"""
        self.query_fields['Z_SL_KD_Z'] = """CASE WHEN rbMedicalAidType.code IN ('1', '2', '3', '7') AND IFNULL(rbEventProfile.code, '') != 'r6020'
                THEN WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, rbMedicalAidType.federalCode='7')
                ELSE 0 END"""
        self.query_fields['movingPersonId'] = 'ActionMoving.person_id'
        self.query_fields['USL_NPL'] = """CASE WHEN (rbMedicalAidType.code = 1 AND (CSGSpecification.level IS NULL AND EventResult.federalCode IN ('102', '105', '106', '107', '108', '110') 
                                                OR CSGSpecification.level IS NOT NULL AND CSGSpecification.level != 2))
                                           OR (rbMedicalAidType.code = 7 AND (CSGSpecification.level IS NULL AND EventResult.federalCode IN ('202', '205', '206', '207', '208')
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
                         THEN Event_CSG.endDate > CAST(A.begDate AS DATE) AND Event_CSG.endDate <= CAST(A.endDate AS DATE) AND sp.federalCode not in ('4', '223')
                         ELSE Event_CSG.endDate >= CAST(A.begDate AS DATE) AND Event_CSG.endDate <= CAST(A.endDate AS DATE) AND sp.federalCode not in ('4', '223') END
                    ELSE CAST(Action.endDate AS DATE) between CAST(A.begDate AS date) AND CAST(A.endDate AS date) END)
    {actionTables}
    WHERE Account_Item.reexposeItem_id IS NULL
        AND (Account_Item.date IS NULL OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
        AND {idList}
        AND rbMedicalAidType.code = '1'\n""".format(fields=self.prepare_query_field(), idList=idList, commonTables=commonTables, actionTables=actionTables)
        return stmt


    def createQuery(self):
        sysIdf003 = self._getAccSysId('f003')
        commonTables = u"""-- Common tables begin
    INNER JOIN Event ON Event.id = Account_Item.event_id
    -- PACIENT_*
    INNER JOIN Client ON Client.id = Event.client_id
    LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate, Event.id)
    LEFT JOIN Client relatedClient ON relatedClient.id = Event.relative_id
                                         and Client.birthDate > (Event.setDate - INTERVAL 29 DAY)
                                         and ClientPolicy.id is null
    LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
    LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
    -- Z_SL_*
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
    -- Z_SL_VIDPOM
    LEFT JOIN rbService ON rbService.id = Account_Item.service_id
    LEFT JOIN rbService_Identification ON rbService_Identification.id = (
        SELECT MAX(si.id) FROM rbService_Identification AS si
        WHERE si.master_id = rbService.id
          AND si.system_id = (
            SELECT id FROM rbAccountingSystem WHERE code = 'MES001'))
    LEFT JOIN rbService_Profile ON rbService_Profile.id = (
        SELECT MAX(id) FROM rbService_Profile rs
        WHERE rs.master_id = rbService.id
          AND rs.speciality_id = Person.speciality_id)
    LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = COALESCE(rbService_Profile.medicalAidKind_id, rbService.medicalAidKind_id, EventType.medicalAidKind_id)
    LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
    LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = rbSpeciality.medicalAidProfile_id
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
            SELECT id FROM rbAccountingSystem WHERE urn = 'urn:tfoms01:V027'))
    LEFT JOIN Action ON Action.id = Account_Item.action_id
    LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
    LEFT JOIN Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
    LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
    LEFT JOIN rbSpeciality AS ActionSpec ON ActionSpec.id = ActionPerson.speciality_id
    LEFT JOIN rbMedicalAidProfile AS ActionProfile ON ActionProfile.id = ActionSpec.medicalAidProfile_id
    -- Common tables end (35 JOINS)""".format(sysIdf003=sysIdf003)

        actionTables = u'''-- Подразделение/Профиль для Z_SL
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
    LEFT JOIN rbHospitalBedProfile AS MovingHBP ON MovingHBP.id = (
        SELECT OSHB.profile_id FROM Action A
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id and APT.typeName = 'HospitalBed'
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_HospitalBed AS AHBP ON AHBP.id = AP.id
        INNER JOIN OrgStructure_HospitalBed OSHB ON OSHB.id = AHBP.value
        WHERE A.id = ActionMoving.id
            AND AP.deleted = 0
            AND APT.`name` = 'койка' AND APT.deleted = 0
        LIMIT 0, 1)
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
    LEFT JOIN rbSpeciality AS UslSpec ON UslSpec.id = UslPerson.speciality_id
    LEFT JOIN rbMedicalAidProfile AS MovingHBPMedicalAidProfile ON MovingHBPMedicalAidProfile.id = UslSpec.medicalAidProfile_id'''

        self.initFields()
        idList = self.tableAccountItem['id'].inlist(self.idList)
        sqlAmb = self.createAmbQuery(idList, commonTables)
        sqlStac = self.createStacQuery(idList, commonTables, actionTables)

        stmt = u"""{0} UNION ALL {1} ORDER BY PACIENT_ID_PAC, eventId, Z_SL_USL_OK, USL_SUMV_USL DESC, USL_TARIF DESC, USL_CODE_OPER, serviceCode""".format(sqlAmb, sqlStac)
        return self.db.query(stmt)


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

            mkb = forceString(record.value('USL_DS'))[:1]
            ksg = forceString(record.value('USL_CODE_USL'))
            eventId = forceRef(record.value('Z_SL_IDCASE'))
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
            RegSTREET.OCATD AS PERS_OKATOG,
            LocSTREET.OCATD AS PERS_OKATOP,
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
    LEFT JOIN kladr.STREET AS RegSTREET ON (RegSTREET.CODE = RegAddressHouse.KLADRStreetCode)

    LEFT JOIN ClientAddress AS ClientLocAddress ON (ClientLocAddress.id  = getClientLocAddressId(Client.id))
    LEFT JOIN Address AS LocAddress ON (LocAddress.id = ClientLocAddress.address_id)
    LEFT JOIN AddressHouse LocAddressHouse ON (LocAddressHouse.id = LocAddress.house_id)
    LEFT JOIN kladr.KLADR AS LocKLADR ON (LocKLADR.CODE = LocAddressHouse.KLADRCode)
    LEFT JOIN kladr.STREET AS LocSTREET ON (LocSTREET.CODE = LocAddressHouse.KLADRStreetCode)
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
            PersonSpeciality.federalCode AS MR_USL_N_PRVS,
            CAST(Visit.date AS DATETIME) AS USL_DATE_IN,
            CAST(Visit.date AS DATETIME) AS USL_DATE_OUT,
            SUBSTR(rbService.code, 1, 4) AS USL_PODR,
            VisitProfile.code AS USL_PROFIL,
            CASE WHEN PersonSpeciality.federalCode in ('18','19','102','20','21','22','68', '37') THEN 1 ELSE 0 END AS USL_DET,
            CAST(IF(EventType.form = '110', Event.execDate, Event.setDate) AS DATE) AS USL_DATE_1,
            rbService.infis AS USL_CODE_USL,
            1 AS USL_KOL_USL,
            0 AS USL_SUMV_USL,
            0 AS USL_TARIF,
            VisitPerson.SNILS AS MR_USL_N_CODE_MD_raw,
            VisitPerson.id as visitPersonId,
            Event.contract_id
        FROM Visit
        LEFT JOIN Event ON Event.id = Visit.event_id
        LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
        LEFT JOIN rbSpeciality PersonSpeciality ON VisitPerson.speciality_id = PersonSpeciality.id
        LEFT JOIN rbService ON Visit.service_id = rbService.id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN rbMedicalAidProfile AS VisitProfile ON VisitProfile.id = PersonSpeciality.medicalAidProfile_id
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
                 'onkologyInfo',  CR01OnkologyInfo),
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
        counterId = forceRef(QtGui.qApp.db.translate('rbCounter', 'code', 'packageNumber', 'id'))
        if counterId:
            self.edtPacketNumber.setValue(forceInt(QtGui.qApp.getDocumentNumber(None, counterId, self._parent.info['accDate'])))
        QtGui.qApp.processEvents()
        (xmlWriter, personalDataWriter) = self.xmlWriter()
        xmlWriter._lastClientId = None
        xmlWriter._lastPrNov = None
        xmlWriter._lastEventId = None
        registryType = self.cmbRegistryType.currentIndex()
        personalDataWriter.setVersion(VERSION)
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
            payerCodePart = forceInt(params['payerCode'][-2:] if params['payerCode'] else 10)
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
        return success and self.moveFiles([zipFileName])

    def validatePage(self):
        success = self.saveExportResults()

        if success:
            QtGui.qApp.preferences.appPrefs['%sExportDir' % self.prefix] = toVariant(self.edtDir.text())
            if self._parent.page1.chkSetExposeDate.isChecked():
                self.wizard().setAccountExposeDate()
            self.wizard().setAccountNote()
        return success

    def moveFiles(self, fileList):
        u"""Переносит файлы из списка в каталог, выбранный пользователем"""
        success = False
        for src in fileList:
            srcFullName = os.path.join(forceStringEx(self.getTmpDir()), os.path.basename(src))
            dst = os.path.join(forceStringEx(self.edtDir.text()), os.path.basename(src).replace('-', ''))
            success, _ = QtGui.qApp.call(self, shutil.move, (srcFullName, dst))

            if not success:
                break

        return success
# ******************************************************************************


class CExportXmlStreamWriter(COrder79v3XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO', 'SMO', 'SMO_NAM', 'NOVOR', 'VNOV_D')
    clientFields2 = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                     'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR', 'VNOV_D')
    SLUCHFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'DATE_1', 'DATE_2', 'CODE_MES1', 'ED_COL')
    SLUCHDateFields = ('DATE_1', 'DATE_2')

    eventDateFields = ('DATE_Z_1', 'DATE_Z_2', 'NPR_DATE')
    completeEventFields1 = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO', 'NPR_DATE', 'LPU', 'DATE_Z_1', 'DATE_Z_2',
                            'KD_Z', 'VNOV_M', 'RSLT', 'ISHOD', 'OS_SLUCH', 'VB_P')
    completeEventFields2 = ('IDSP', 'SUMV')

    SLDateFields = ('DATE_1', 'DATE_2')
    SLFields1 = ('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET', 'P_CEL', 'NHISTORY', 'P_PER') + SLDateFields + ('KD',
                 'WEI', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK', 'DN', 'CODE_MES1', 'CODE_MES2', 'NAPR', 'CONS', 'ONK_SL', 'KSG_KPG', 'REAB', 'PRVS', 'VERS_SPEC',
                 'IDDOKT', 'ED_COL', 'TARIF', 'SUM_M', 'LEK_PR', 'USL', 'COMENTSL')

    KSG_KPG = ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG', 'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D', 'KOEF_U', 'CRIT', 'SL_K', 'IT_SL', 'SL_KOEF')
    SL_KOEF = ('IDSL', 'Z_SL')
    LEK_PR = ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK', 'LEK_DOSE')
    LEK_DOSE = ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ')

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = ('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME', 'DET') + serviceDateFields + ('DS', 'CODE_USL',
                     'KOL_USL', 'TARIF', 'SUMV_USL', 'MED_DEV', 'MR_USL_N', 'NPL')

    MED_DEV = ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER')
    MR_USL_N = ('MR_N', 'PRVS', 'CODE_MD')
    SANK = ('S_CODE', 'S_SUM', 'S_TIP', 'SL_ID', 'S_OSN', 'DATE_ACT', 'NUM_ACT', 'CODE_EXP', 'S_COM', 'S_IST')
    eventSubGroup1 = None
    eventSubGroup2 = None
    consFields = ('PR_CONS', 'DT_CONS')
    consDateFields = ('DT_CONS',)
    naprFields = ('NAPR_DATE', 'NAPR_MO', 'NAPR_LPU', 'NAPR_V', 'MET_ISSL', 'NAPR_USL')
    onkSlFields = ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M', 'MTSTZ', 'SOD',
                   'K_FR', 'WEI', 'HEI', 'BSA', 'B_DIAG', 'B_PROT', 'ONK_USL')
    onkUslSubGroup = {
        'LEK_PR': {'fields': ('REGNUM', 'CODE_SH', 'DATE_INJ'),
                   'dateFields': ('DATE_INJ',)},
    }

    onkSlSubGroup = {
        'ONK_USL': {'fields': ('USL_TIP', 'HIR_TIP',
                               'LEK_TIP_L', 'LEK_TIP_V', 'LEK_PR', 'PPTR',
                               'LUCH_TIP'),
                    'subGroup': onkUslSubGroup},
        'B_DIAG': {'fields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE1',
                              'DIAG_CODE2', 'DIAG_RSLT1', 'DIAG_RSLT2',
                              'REC_RSLT')},
        'B_PROT': {'fields': ('PROT', 'D_PROT')}
    }

    eventSubGroupKSG = {'KSG_KPG': {'fields': KSG_KPG,
                                 'subGroup': {'SL_KOEF': {'fields': SL_KOEF}}},
                        'CONS': {'fields': consFields}, 'NAPR': {'fields': naprFields},
                        'ONK_SL': {'fields': onkSlFields, 'subGroup': onkSlSubGroup},
                        'LEK_PR':  {
                                 'fields': LEK_PR, 'dateFields': ('DATA_INJ',),
                                 'subGroup': {'LEK_DOSE': {'fields': LEK_DOSE}}}
                        }
    eventSubGroup = {'CONS': {'fields': consFields}, 'NAPR': {'fields': naprFields},
                     'ONK_SL': {'fields': onkSlFields, 'subGroup': onkSlSubGroup},
                     'LEK_PR': {
                                'fields': LEK_PR, 'dateFields': ('DATA_INJ',),
                                'subGroup': {'LEK_DOSE': {'fields': LEK_DOSE}}}
                     }

    requiredFields = ()

    eventDateFields1 = ('DATE_Z_1', 'DATE_Z_2')
    eventDateFields2 = ('NAPDAT',)
    eventFields = ()

    ksgKpgFields = ('N_KSG', 'VER_KSG', 'KSG_PG', 'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D', 'KOEF_U')

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
                    'subGroup': medicalSuppliesDoseGroup}
    }
    serviceSubGroup = {
        'MED_DEV': {
            'fields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'),
            'dateFields': ('DATE_MED', ),
            'requiredFields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'), },
        'MR_USL_N': {
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    naprFromFields = ('NPR_MO', 'NAPUCH', 'NOM_NAP', 'NAPDAT', 'BIO_DAT', 'DSN')


    nazSubGroup = {'NAZ': {'fields': ('NAZ_N', 'NAZR', 'NAZ_IDDOKT', 'NAZ_SP', 'NAZ_V', 'NAZ_USL', 'NAPR_DATE', 'NAPR_MO', 'NAPR_LPU', 'NAZ_PMP', 'NAZ_PK'),
                           'dateFields': ('NAPR_DATE',)},
                   }

    mapRecFrom = {
        u'Поликлиника': '1',
        u'Самотек': '1',
        u'Другие': '1',
        u'Скорая помощь': '2',
        u'Перевод из ЛПУ': '3',
        u'Санавиация': '3',
    }
    mapEventOrderToForPom = {'1': '3', '3': '3', '6': '2', '2': '1'}


    def __init__(self, parent):
        COrder79v3XmlStreamWriter.__init__(self, parent)
        self.Z_SLDate1 = None
        self.Z_SLDate1_uslCheck = False
        self.Z_SLDate2 = None
        self.Z_SLDate2_uslCheck = False
        self._lastEventId = None
        self._lastClientId = None
        self._lastPrNov = None
        self.lastUslOk = None
        self.eventGroup = CExportR01EventGroup(self)
        self.mapOrgStructureIdToKODLPU = {}
        self.exportedAppointments = set()
        self.exportedDirectionCancers = set()
        self.contactAttributesMap = {}
        self.setCodec(QTextCodec.codecForName('cp1251'))


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        accDate = params['accDate']
        self.startDate = QDate(settleDate.year(), settleDate.month(), 1)
        table = self._parent.db.table('Account')
        registryType = self._parent.cmbRegistryType.currentIndex()
        accSum = forceDouble(self._parent.db.getSum(table, sumCol='sum', where=table['id'].inlist(self._parent.accountIdList)))
        params['USL_LPU'] = params['lpuMiacCode']
        params['Z_SL_LPU'] = u'510%s' % params['lpuCode']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', VERSION if registryType == CExportPage1.registryTypeFlk else '3.1')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        if registryType == CExportPage1.registryTypeFlk:
            self.writeTextElement('SD_Z', forceString(self._parent.getEventCount()))
        self.writeEndElement()  # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuMiacCode'])
        self.writeTextElement('YEAR', forceString(accDate.year()))
        self.writeTextElement('MONTH', forceString(accDate.month()))
        payerId = params['payerId']
        payerCode = forceString(self._parent.db.translate('Organisation', 'id', payerId, 'infisCode'))
        if registryType == CExportPage1.registryTypeFlk:
            self.writeTextElement('NSCHET', params['NSCHET'])
            self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))
            self.writeTextElement('PLAT', payerCode)
            self.writeTextElement('SUMMAV', '{0:.2f}'.format(accSum))
        self.writeEndElement()  # SCHET


    def checkerClientInfo(self, record):
        # if forceString(record.value('PERS_OT')) == '':
        #     record.setValue('PERS_OT', u'НЕТ')
        if forceInt(record.value('isActualPolicy')) == 0 and forceInt(record.value('PACIENT_VPOLIS')) != 2:
            record.setValue('PACIENT_SPOLIS', '0000000000')
            record.setValue('PACIENT_NPOLIS', '00000000000000000000')


    def checkerEventInfo(self, record):
        if not forceString(record.value('Z_SL_LPU')):
            record.setValue('Z_SL_LPU', '0')
        if not forceString(record.value('Z_SL_PROFIL')):
            record.setValue('Z_SL_PROFIL', '0')
        if not forceString(record.value('Z_SL_RSLT')):
            record.setValue('Z_SL_RSLT', '0')
        if not forceString(record.value('Z_SL_ISHOD')):
            record.setValue('Z_SL_ISHOD', '0')


    def checkerService(self, record):
        if not forceString(record.value('USL_PROFIL')):
            record.setValue('USL_PROFIL', '0')
        if not forceString(record.value('USL_KOL_USL')):
            record.setValue('USL_KOL_USL', '1')


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        prNov = forceString(record.value('PR_NOV')) or '0'
        changedPrNov = (prNov != self._lastPrNov)
        registryType = self._parent.cmbRegistryType.currentIndex()

        if (clientId != self._lastClientId) or changedPrNov:
            if self._lastClientId or self._lastPrNov:
                self.eventGroup.clear(self, params)
                if registryType == CExportPage1.registryTypeFlk:
                    self.writeEndElement()  # Z_SL
                self.writeEndElement()  # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['N_ZAP']))

            if registryType == CExportPage1.registryTypeFlk:
                self.writeTextElement('PR_NOV', prNov)

            clientAddrInfo = params['clientAddr'].get(clientId, {})
            params.update(clientAddrInfo)
            self.writeClientInfo(record, params)

            params['N_ZAP'] += 1
            self._lastClientId = clientId
            self._lastPrNov = prNov
            self._lastEventId = None

        if registryType == CExportPage1.registryTypeFlk:
            self.writeEventInfo(record, params)
            self.writeService(record, params)
        else:
            self.writeIdentityEventInfo(record, params)
            self.writeService(record, params)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if self._lastEventId:
            self.eventGroup.clear(self, params)
            self.writeEndElement()  # SLUCH
            self.writeEndElement()  # ZAP
        self.writeEndElement()  # ZL_LIST


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        if eventId == self._lastEventId:
            return
        params['USL_IDSERV'] = 0
        eventId = forceRef(record.value('eventId'))
        execDate = forceDate(record.value('Z_SL_DATE_2'))
        # eventPurposeCode = forceString(record.value(
        #         'eventPurposeCode'))
        patrName = forceString(record.value('PERS_OT'))
        # haveMoving = self.__haveMoving(eventId)
        uslOk = forceInt(record.value('Z_SL_USL_OK'))
        purpose = forceInt(record.value('purpose'))
        isPrimary = forceInt(record.value('isPrimary'))
        eventProfile = forceString(record.value('eventProfile'))
        eventProfileCode = forceString(record.value('eventProfileCode'))
        cureTypeCode = forceString(record.value('HMP_VID_HMP_raw'))
        vidpom = forceString(record.value('Z_SL_VIDPOM'))
        isDiagnostic = forceBool(record.value('isDiagnostic'))
        dispanserCode = forceString(record.value('dispanserCode'))
        birthDate = forceDate(record.value('PERS_DR'))
        setDate = forceDate(record.value('Z_SL_DATE_1'))
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
            'Z_SL_VNOV_M': birthWeight if os_sluch == '1' and birthWeight <= 2500 else None,
            'Z_SL_OS_SLUCH': os_sluch,
            'Z_SL_VERS_SPEC': "'V021'",
            'SL_LPU_1': self.getKODLPU(orgStructureId),
            'Z_SL_FOR_POM': self.mapEventOrderToForPom.get(eventOrder, '1'),
        }

        if forceString(record.value('vidpom')) != '9':
            local_params['SL_DS2'] = forceString(record.value('DS2')).split(',')
            local_params['SL_DS3'] = forceString(record.value('DS3')).split(',')

        if uslOk == 3:
            local_params['Z_SL_VBR'] = '1' if forceInt(record.value('orgStructureType')) == 3 else '0'
            local_params['SL_P_CEL'] = '1.0'  # посещение по заболеванию
        else:
            local_params['SL_P_CEL'] = None

        if dispanserCode == '1':
            record.setValue('SL_DN', '1')
        elif dispanserCode in ['2', '6']:
            record.setValue('SL_DN', '2')
        elif dispanserCode == '4':
            record.setValue('SL_DN', '4')
        elif dispanserCode in ['3', '5']:
            record.setValue('SL_DN', '6')

        if uslOk == 1:  # если это стационар
            self.processCoefficients(record, local_params)
            if vidpom != '32':
                fskgList = params['mapEventIdToFksgCode'].get(eventId, '').split(';')
                local_params['SL_CODE_FKSG'] = ';'.join(x for x in fskgList if x[:2] == 'st')
                local_params['SL_PR_MO'] = 1 if len(fskgList) > 1 else 0
            else:
                record.setValue('serviceCode', '')
            begDate = forceDate(record.value('USL_DATE_IN'))
            eventBegDate = forceDate(record.value('SL_DATE_1'))
            if begDate == eventBegDate:
                receivedFrom = forceString(record.value('receivedFrom'))
                record.setValue('SL_P_PER', toVariant(self.mapRecFrom.get(receivedFrom, '1')))
            else:
                record.setValue('SL_P_PER', toVariant('4'))
            # не выводить тег, если коэф. не применены
            if forceDouble(record.value('SL_SK_KOEF')) == 0.0:
                record.setValue('SL_SK_KOEF', '')
            local_params['Z_SL_DOPL'] = ''


        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.eventGroup.addRecord(_record)
        self._lastEventId = eventId


    def writeIdentityEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        params['USL_IDSERV'] = 0
        if eventId == self._lastEventId:
            return
        local_params = {
            'SLUCH_IDCASE': record.value('Z_SL_IDCASE'), 'SLUCH_USL_OK': record.value('Z_SL_USL_OK'),
            'SLUCH_VIDPOM': record.value('Z_SL_VIDPOM'), 'SLUCH_DATE_1': record.value('Z_SL_DATE_Z_1'),
            'SLUCH_DATE_2': record.value('Z_SL_DATE_Z_2'), 'SLUCH_CODE_MES1': record.value('SL_CODE_MES1')}
        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.eventGroup.addRecord(_record)
        self._lastEventId = eventId


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

        for coefCode, coef in coefList:
            params.setdefault('SL_KOEF_IDSL', []).append(coefCode)
            params.setdefault('SL_KOEF_Z_SL', []).append(coef)
            if coefCode:
                record.setValue('KSG_KPG_SL_K', toVariant(1))

        if coefItSl:
            record.setValue('KSG_KPG_IT_SL', toVariant(format(coefItSl, '.5f')))


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        execPersonOrgStructureId = forceRef(record.value('ExecPersonOrgStructureId'))
        record.setValue('USL_VID_VME', forceString(record.value('USL_CODE_USL')))
        local_params = {
            'USL_LPU_1': self.getKODLPU(execPersonOrgStructureId),
        }
        if forceString(record.value('USL_CODE_USL'))[:2] not in ['st', 'ds']:
            params['USL_IDSERV'] += 1
        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.eventGroup.addRecord(_record)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        sex = forceString(record.value('PERS_W'))
        birthDate = forceDate(record.value('PERS_DR'))
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        birthNumber = forceInt(record.value('birthNumber'))
        birthWeight = forceInt(record.value('birthWeight'))
        setDate = forceDate(record.value('Z_SL_DATE_Z_1'))
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
                        record.setValue('PACIENT_SMO', forceString(QtGui.qApp.db.translate('Organisation', 'id', insurrer, 'infisCode')))
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

        registryType = self._parent.cmbRegistryType.currentIndex()

        if registryType == CExportPage1.registryTypeFlk:
            local_params = {
                'PACIENT_VNOV_D': birthWeight if isJustBorn and not isAnyBirthDoc and birthWeight <= 2500 else None,
                'PACIENT_NOVOR':  ('%s%s%s' % (sex[:1], birthDate.toString('ddMMyy'), birthNumber)) if isJustBorn and not isAnyBirthDoc else '0',
                'PACIENT_STAT_Z': statZ,
            }
        else:
            local_params = {}

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.checkerClientInfo(_record)
        if registryType == CExportPage1.registryTypeFlk:
            self.writeGroup('PACIENT', self.clientFields, _record)
        else:
            self.writeGroup('PACIENT', self.clientFields2, _record)


    def _getContractAttributes(self, contactId):
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


class CExportR01EventGroup:
    def __init__(self, parent):
        self.records = []
        self._parent = parent

    def addRecord(self, record):
        self.records.append(record)


    def clear(self, writer, params):
        self.calc()
        self.write(writer, params)
        del self.records[:]


    def calc(self):
        sumv = 0.0
        edcol = 0
        for rec in self.records[1:]:
            sumv = forceDouble(format(sumv + forceDouble(rec.value('USL_SUMV_USL')), ".2f"))
            edcol = forceInt(edcol + forceInt(rec.value('USL_KOL_USL')))
        self.records[0].setValue('Z_SL_SUMV', sumv)
        if forceInt(self.records[0].value('Z_SL_KD_Z')) > 0:
            self.records[0].setValue('SL_ED_COL', forceInt(self.records[0].value('Z_SL_KD_Z')))
        else:
            self.records[0].setValue('SL_ED_COL', edcol)
        if forceString(self.records[0].value('USL_CODE_USL'))[:2] in ['ds', 'st']:
            self.records[0].setValue('SL_TARIF', self.records[0].value('USL_TARIF'))
        else:
            self.records[0].setValue('SL_TARIF', sumv)
        self.records[0].setValue('SL_SUM_M', sumv)

        if self._parent._parent.cmbRegistryType.currentIndex() == CExportPage1.registryTypeIdentity:
            self.records[0].setValue('SLUCH_ED_COL', self.records[0].value('SL_ED_COL'))


    def write(self, writer, params):
        eventId = forceRef(self.records[0].value('eventId'))
        onkologyInfo = params['onkologyInfo'].get(eventId, {})
        medicalSuppliesInfo = params['medicalSuppliesInfo'].get(eventId, {})
        implantsInfo = params['implantsInfo'].get(eventId, {})
        uslOk = forceInt(self.records[0].value('Z_SL_USL_OK'))
        ds1 = forceString(self.records[0].value('SL_DS1'))
        ds2 = forceString(self.records[0].value('SL_DS2'))
        setDate = forceDate(self.records[0].value('Z_SL_DATE_1'))
        mkb = onkologyInfo.get('actionMKB')
        reab = forceInt(self.records[0].value('USL_REAB'))
        birthDate = forceDate(self.records[0].value('PERS_DR'))
        eventProfileCode = forceString(self.records[0].value('eventProfileCode'))

        for record in self.records[1:]:
            bedDays = 0 if record.isNull('SL_KD') else forceInt(record.value('SL_KD'))
            if (mkb == forceString(record.value('USL_DS'))
                    and bedDays and onkologyInfo.get('ONK_USL_USL_TIP')):
                onkologyInfo['ONK_USL_IDS_USL'] = record.value('USL_IDSERV')
                break
        else:
            if onkologyInfo.get('ONK_USL_USL_TIP'):
                onkologyInfo['ONK_USL_IDS_USL'] = self.records[1].value('USL_IDSERV')

        if forceString(self.records[0].value('KSG_KPG_N_KSG')):
            attributes = self._parent._getContractAttributes(forceRef(self.records[0].value('contract_id')))
            self.records[0].setValue('KSG_KPG_BZTSZ', format(forceDouble(attributes['BS' if forceString(self.records[0].value('USL_CODE_USL'))[:2] == 'st' else 'BS_ds'][forceDate(self.records[0].value('USL_DATE_OUT'))]), '.2f'))
            self.records[0].setValue('KSG_KPG_KOEF_U', format(forceDouble(attributes['KOEF_U' if forceString(self.records[0].value('USL_CODE_USL'))[:2] == 'st' else 'KOEF_U_ds'][forceDate(self.records[0].value('USL_DATE_OUT'))]), '.5f'))
            coeffs = params['CSGCoefficients'][forceString(self.records[0].value('USL_CODE_USL'))][forceDate(self.records[0].value('USL_DATE_OUT'))]
            if isinstance(coeffs, tuple):
                coefZ, coefUP = coeffs
                self.records[0].setValue('KSG_KPG_KOEF_Z', format(forceDouble(coefZ), '.5f'))
                self.records[0].setValue('KSG_KPG_KOEF_UP', format(forceDouble(coefUP), '.5f'))

        writer.checkerEventInfo(self.records[0])

        record = CExtendedRecord(self.records[0], onkologyInfo)
        _sum = sum(forceDouble(format(forceDouble(rec.value('USL_SUMV_USL')), '.2f')) for rec in self.records[1:])
        record.setValue('Z_SL_SUMV', _sum)
        registryType = self._parent._parent.cmbRegistryType.currentIndex()
        if registryType == CExportPage1.registryTypeIdentity:
            writer.writeGroup('SLUCH', writer.SLUCHFields, record, closeGroup=True, dateFields=writer.SLUCHDateFields)
            return
        writer.writeGroup('Z_SL', writer.completeEventFields1, record,
                          subGroup=writer.eventSubGroup1,
                          closeGroup=False, dateFields=writer.eventDateFields)
        if forceString(self.records[0].value('USL_CODE_USL'))[:2] in ['st', 'ds']:
            writer.writeGroup('SL', writer.SLFields1, record, writer.eventSubGroupKSG, closeGroup=False, dateFields=writer.SLDateFields)
        else:
            writer.writeGroup('SL', writer.SLFields1, record, writer.eventSubGroup, closeGroup=False, dateFields=writer.SLDateFields)

        for rec in self.records[1:]:
            if forceString(rec.value('serviceCode'))[:2] in ['st', 'ds']:
                continue
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
            if uslOk == 1 and implantsInfo:
                endDate = forceDate(rec.value('USL_DATE_OUT'))

                codeList = implantsInfo['MED_DEV_CODE_MEDDEV']
                dateList = implantsInfo['MED_DEV_DATE_MED']
                numberList = implantsInfo['MED_DEV_NUMBER_SER']
                _codeList = []
                _dateList = []
                _numberList = []
                for i, date in enumerate(dateList):
                    dt = forceDate(date)
                    if dt == endDate:
                        _codeList.append(codeList[i])
                        _dateList.append(date)
                        _numberList.append(numberList[i])
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

        writer.writeEndElement()  # SL
        writer.writeGroup('Z_SL', writer.completeEventFields2, record,
                          subGroup=writer.eventSubGroup2, openGroup=False,
                          closeGroup=False, dateFields=writer.eventDateFields)


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
                table['TLech_NAME'].eq(_id)])
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
                table['THir_NAME'].eq(_id)])
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
                table['TLek_NAME_L'].eq(_id)])
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
                table['TLek_NAME_V'].eq(_id)])
            result = forceString(record.value(0)) if record else None
            cls.mapIdToCode[_id] = result
        return result

# ******************************************************************************

class CR01OnkologyInfo(COnkologyInfo):
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
                WHERE rbAccountingSystem.code = 'AccTFOMS'
            )
        LEFT JOIN rbTumor_Identification ON
            rbTumor_Identification.master_id = IFNULL(
                AnyDiagnostic.cTumor_id, AnyDiagnostic.pTumor_id)
            AND rbTumor_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'AccTFOMS'
            )
        LEFT JOIN rbNodus_Identification ON
            rbNodus_Identification.master_id = IFNULL(
                AnyDiagnostic.cNodus_id, AnyDiagnostic.pNodus_id)
            AND rbNodus_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'AccTFOMS'
            )
        LEFT JOIN rbMetastasis_Identification ON
            rbMetastasis_Identification.master_id = IFNULL(
                AnyDiagnostic.cMetastasis_id, AnyDiagnostic.pMetastasis_id)
            AND rbMetastasis_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'AccTFOMS'
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

                text = forceString(prop.getTextScalar()).strip()
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
                     'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG', 'SNILS', 'OKATOG'))
    clientDateFields = COrder79PersonalDataWriter.clientDateFields + ('DOCDATE', 'DR_P',)

    def __init__(self, parent, version='3.2'):
        COrder79PersonalDataWriter.__init__(self, parent, version)

    def setVersion(self, version):
        self.version = version

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
        Action.amount,
        Action.begDate,
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
         (SELECT APS.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Integer APS ON APS.id = AP.id
         WHERE APT.descr = 'COL_INJ' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_LEK_DOSE_COL_INJ
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
                'urn:tfoms01:1.2.643.5.1.13.13.11.1358'))
        return stmt

    def get(self, _db, _idList, parent):
        self._parent = parent
        self._idList = _idList
        query = _db.query(self._stmt())
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            covidCount = forceInt(record.value('amount'))
            begDate = forceDate(record.value('begDate'))
            dateCovid = forceDate(record.value('COVID_LEK_LEK_PR_DATA_INJ'))
            for i in xrange(covidCount):
                if begDate != dateCovid and covidCount > 1:
                    record.setValue('COVID_LEK_LEK_PR_DATA_INJ', begDate.addDays(i))
                if eventId in result:
                    updateDictOfListsItem(result[eventId], record)
                else:
                    result[eventId] = record2DictOfLists(record)
        return result


class CImplantsInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Action.endDate AS MED_DEV_DATE_MED,
            (SELECT n.regionalCode FROM ActionProperty AP
             INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
             INNER JOIN ActionProperty_rbNomenclature APS ON APS.id = AP.id
             INNER JOIN rbNomenclature n ON APS.value = n.id
             WHERE APT.shortName = 'medkind'
               AND AP.deleted = 0 AND AP.action_id = Action.id
             LIMIT 1) AS MED_DEV_CODE_MEDDEV,
            (SELECT APS.value FROM ActionProperty AP
             INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
             INNER JOIN ActionProperty_String APS ON APS.id = AP.id
             WHERE APT.shortName = 'marknumber'
               AND AP.deleted = 0 AND AP.action_id = Action.id
             LIMIT 1) AS MED_DEV_NUMBER_SER
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.flatCode = 'Code_MDV'
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
s2.federalCode AS NAZ_NAZ_SP,
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
        table = db.table('soc_CSGCoefficients')
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
    testAccountExport(exportR01Native,
                      #accNum='06ALL-14',
                      eventIdList=[4],
                      #limit=1000,
                      configFileName='S11App01.ini')
