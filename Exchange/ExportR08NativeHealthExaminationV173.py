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

u"""Экспорт реестра  в формате XML. Республика Калмыкия. ДД, (Д3) V173"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QFile

from library.Utils import (
    forceString, forceRef, toVariant, forceBool, forceDouble)
from Exchange.Order79Export import COrder79ExportWizard, COrder79v3XmlStreamWriter
from Exchange.Export import (CAbstractExportPage1Xml, CAbstractExportPage2,
    CExportHelperMixin)
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.ExportR08Hospital import CR08PersonalDataWriter
from Exchange.Utils import compressFileInZip, forceDate

from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1

# ******************************************************************************

def getEventTypeCode(_db, accountId):
    u"""Возвращает префикс имени файла"""
    stmt = u"""SELECT EventType.code
    FROM Account
    LEFT JOIN Contract_Specification ON Contract_Specification.master_id = Account.contract_id
    LEFT JOIN EventType ON Contract_Specification.eventType_id = EventType.id
    WHERE Account.id = %d AND Contract_Specification.deleted = 0
    LIMIT 0,1""" % accountId

    query = _db.query(stmt)
    result = u''

    if query.first():
        record = query.record()
        result = forceString(record.value(0))

    return result

# ******************************************************************************

def formatAccNumber(params):
    u"""две последние цифры Organisation.miacCode организации в умолчаниях)+
        (две последние цифры года из Account.settleDate)
        +(две цифры месяца из Account.settleDate)+(Account.id)"""
    settleDate = params['settleDate']
    return u'{miacCode}{settleYear:02d}{settleMonth:02d}{accId:d}'.format(
        miacCode=params['lpuMiacCode'][-2:],
        settleYear=settleDate.year() % 100,
        settleMonth=settleDate.month(),
        accId=params['accId']
    )

# ******************************************************************************

def exportR08NativeHealthExaminationV173(widget, accountId, accountItemIdList,
                                        _):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Калмыкии"""

    mapPrefixToEventTypeCode = {u'ДВ4': 'DP', u'ДВ2': 'DV', u'ОПВ': 'DO',
                                u'ДС1': 'DS', u'ДС2': 'DU', u'ПН1': 'DF',
                                u'ПН2': 'DF', u'ОН3': 'DR', u'ДВ3': 'DP',
                                u'ДС3': 'DS', u'ДС4': 'DU', u'УД1': 'DA',
                                u'УД2': 'DB'}

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии V200'
        prefix = 'R08D3V200'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

        self.page1.setXmlWriter((CXmlStreamWriter(self.page1),
                                 CPersonalDataWriter(self.page1)))

        self.__xmlBaseFileName = None


    def prefixX(self, accountId):
        u"""Вовзращает префикс имени файла"""
        code = getEventTypeCode(self.db, accountId)
        return self.mapPrefixToEventTypeCode.get(code)


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""

        if self.__xmlBaseFileName:
            result = self.__xmlBaseFileName
        else:
            tblOrganisation = self.db.table('Organisation')
            info = self.info

            payer = self.db.getRecord(tblOrganisation, 'infisCode, isInsurer',
                                      info['payerId'])

            if payer and not forceBool(payer.value(1)):
                payerPrefix = 'T'
                payerCode = '08'
            else:
                payerPrefix = 'S'
                payerCode = forceString(payer.value(0)) if payer else ''

            recipientCode = forceString(self.db.translate(tblOrganisation, 'id',
                                                          QtGui.qApp.
                                                          currentOrgId(),
                                                          'infisCode'))

            settleDate = info['settleDate']
            prefix = self.prefixX(info['accId'])
            params = {
                'year': settleDate.year() % 100,
                'month': settleDate.month(),
                'week': (settleDate.day() / 7 + 1 ) if prefix == 'DA' else '',
                'packetNumber': self.page1.edtPacketNumber.value(),
            }
            postfix = u'{year:02}{month:02}{week}{packetNumber:1}'.format(
                **params) if addPostfix else u''
            result = u'%2sM%s%s%s_%s.xml' % (prefix,
                                             recipientCode, payerPrefix,
                                             payerCode, postfix)
            self.__xmlBaseFileName = result

        return result


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L{0}'.format(self._getXmlBaseFileName(addPostfix)[1:])


    def getZipFileName(self):
        u"""Возвращает имя архива:"""
        return u'{0}.zip'.format(self._getXmlBaseFileName(True)[:-4])

# ******************************************************************************

class CR08ExportPage1(CAbstractExportPage1Xml, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""
    mapDiagResultToNazV = {'505': 1, '506': 2, '507':3}


    def __init__(self, parent, prefix):
        xmlWriter = (CXmlStreamWriter(self), CPersonalDataWriter(self))
        CAbstractExportPage1Xml.__init__(self, parent, xmlWriter)
        CExportHelperMixin.__init__(self)
        self.cmbRegistryType.setVisible(False)
        self.lblRegistryType.setVisible(False)
        self.prefix = prefix

        self.exportedActionsList = None
        self.ignoreErrors = False

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(forceBool(prefs.get('Export%sVerboseLog' % prefix, False)))
        self.chkIgnoreErrors.setChecked(forceBool(prefs.get('Export%sIgnoreErrors' % prefix, False)))
        self.edtPacketNumber.setVisible(True)
        self.lblPacketNumber.setVisible(True)

        self.chkIsPerCapitaNorm = QtGui.QCheckBox(self)
        self.chkIsPerCapitaNorm.setText(u'Оплата по подушевому нормативу')
        self.verticalLayout.addWidget(self.chkIsPerCapitaNorm)

        self._orgStructInfoCache = {}


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['Export%sIgnoreErrors' % self.prefix] = toVariant(
            self.chkIgnoreErrors.isChecked())
        prefs['Export%sVerboseLog' % self.prefix] = toVariant(
            self.chkVerboseLog.isChecked())
        return CAbstractExportPage1Xml.validatePage(self)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)

        if hasattr(self, 'chkIsPerCapitaNorm'):
            self.chkIsPerCapitaNorm.setEnabled(not flag)

        if hasattr(self, 'lblPacketCounter'):
            self.lblPacketCounter.setEnabled(not flag)

# ******************************************************************************

    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        params = self.processParams()
        params['isPerCapitaNorm'] =self.chkIsPerCapitaNorm.isChecked()

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuMiacCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'miacCode'))
        params['lpuTfomsCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'tfomsExtCode'))
        params['USL_KODLPU'] = params['lpuCode']
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])
        self.exportedActionsList = []

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
            params['eventCount'] = self.getEventCount()
            params['SLUCH_COUNT'] = params['accNumber']
            params['mapEventIdToSum'] = self.getEventSum()

        params['rowNumber'] = 1
        params['SLUCH_IDCASE'] = 1
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getPersonalDataXmlFileName(False))

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        CAbstractExportPage1Xml.exportInt(self)


    def getOrgStructureInfo(self, _id):
        u"""Возвращает parent_id и infisCode для подразделения"""
        result = self._orgStructInfoCache.get(_id, -1)

        if result == -1:
            result = (None, None)
            record = self._db.getRecord('OrgStructure',
                                        ['parent_id', 'infisCode'], _id)

            if record:
                result = (forceRef(record.value(0)),
                          forceString(record.value(1)))

            self._orgStructInfoCache[_id] = result

        return result


#2)Тег <ST_OKATO> в блоке <PACIENT>: нужно выгружать только в случае если
# Client.id-> ClientPolicy.PolicyKind_id -> rbPolicyKind.regionalCode=1
#
#4)Тег <LPU_1> в блоке <SLUCH> и в блоке <USL> заполняется по прежнему правилу,
# только используется код OrgStructure.infisCode:
#   Определяем по ответственному за событие врачу
#Account_Item. event_id -> Event.execPerson_id ->Person. orgStructure_id ->
# OrgStructure.infisCode
#Если значение не задано смотрим на вышестоящее подразделение
# OrgStructure. parent_id-> OrgStructure.id-> OrgStructure.infisCode
#Если и у него не заполнено – смотрим еще выше и т.д.
#Если у всех элементов в ветке дерева не будет задано значение – не заполняем
#
#5)Тег <PRVS> в блоке <USL> заполняется по старому правилу, только используется
# код rbSpeciality.regionalCode (вместо rbSpeciality. usishCode)

    def prepareStmt(self, params):
        select = u"""Account_Item.event_id AS eventId,
            Account_Item.service_id AS serviceId,
            Event.client_id AS clientId,
            Action.id AS actionId,
            Visit.id AS visitId,
            Event.execDate,
            LastEvent.id AS lastEventId,

            Account_Item.event_id AS Z_SL_IDCASE,
            rbMedicalAidKind.regionalCode AS Z_SL_VIDPOM,
            PersonOrganisation.infisCode AS Z_SL_LPU,
            IF(rbScene.code = '4', 1, 0) AS Z_SL_VBR,
            Event.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            IF(rbDiagnosticResult.code = '502', 1, 0) AS Z_SL_P_OTK,
            EventResult.regionalCode AS Z_SL_RSLT_D,
            rbMedicalAidUnit.federalCode AS Z_SL_IDSP,

            Event.id AS SL_SL_ID,
            PersonOrgStructure.infisCode AS SL_LPU_1,
            Event.id AS SL_NHISTORY,
            Event.setDate AS SL_DATE_1,
            Event.execDate AS SL_DATE_2,
            Diagnosis.MKB AS SL_DS1,
            IF(Diagnosis.setDate BETWEEN Event.setDate
                AND Event.execDate, 1, '') AS SL_DS1_PR,
            CASE
                WHEN rbDispanser.code = '1' THEN '1'
                WHEN rbDispanser.code IN ('2', '6') THEN '2'
                ELSE '3'
            END AS SL_PR_D_N,
            TotalAmount.amount AS SL_ED_COL,

            PersonOrganisation.infisCode AS USL_LPU,
            ActionOrgSruct.infisCode AS USL_LPU_1,
            IFNULL(Visit.date,
                IFNULL(Action.begDate, Action.endDate)) AS USL_DATE_IN,
            IFNULL(Visit.date, Action.endDate) AS USL_DATE_OUT,
            0 AS USL_P_OTK,
            rbService.infis AS USL_CODE_USL,
            Account_Item.price AS USL_TARIF,
            Account_Item.`sum` AS USL_SUMV_USL,
            ActionPersonSpeciality.regionalCode AS USL_PRVS,
            ActionPerson.regionalCode AS USL_CODE_MD,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            ClientPolicy.serial AS PACIENT_SPOLIS,
            ClientPolicy.number AS PACIENT_NPOLIS,
            IF(rbPolicyKind.regionalCode= '1', Insurer.OKATO,
                '') AS PACIENT_ST_OKATO,
            Insurer.smoCode AS PACIENT_SMO,
            IF(Insurer.smoCode IS NULL OR Insurer.smoCode = '',
                Insurer.OGRN,'') AS PACIENT_SMO_OGRN,
            IF(Insurer.smoCode IS NULL OR Insurer.smoCode = '',
                Insurer.OKATO, '') AS PACIENT_SMO_OK,
            IF((Insurer.smoCode IS NULL OR Insurer.smoCode = '')
                AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                Insurer.shortName,'') AS PACIENT_SMO_NAM,

            Event.client_id AS PERS_ID_PAC,
            UPPER(Client.firstName) AS PERS_IM,
            UPPER(Client.patrName) AS PERS_OT,
            UPPER(Client.lastName) AS PERS_FAM,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            UPPER(Client.birthPlace) AS PERS_MR,
            rbDocumentType.federalCode AS PERS_DOCTYPE,
            IF(rbDocumentType.regionalCode = '3',
                REPLACE(TRIM(ClientDocument.serial),' ', '-'),
                REPLACE(TRIM(ClientDocument.serial),'-', ' ')) AS PERS_DOCSER,
            ClientDocument.number AS PERS_DOCNUM,
            Client.SNILS AS clientSnils,
            EXISTS(
                SELECT NULL FROM ClientDocument AS CD
                LEFT JOIN rbDocumentType ON CD.documentType_id = rbDocumentType.id
                WHERE
                    CD.client_id= Client.id
                    AND rbDocumentType.code = '3'
                    AND CD.deleted = 0
                LIMIT 1
            ) as 'isAnyBirthDoc',
            PersonOrgStructure.parent_id AS personParentOrgStructureId,
            ActionOrgSruct.parent_id AS actionParentOrgStructureId"""
        tables = """Account_Item
            LEFT JOIN Event ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN Diagnostic ON Diagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '1')
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id = Diagnostic.result_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbService ON Account_Item.service_id = rbService.id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Contract_Tariff.unit_id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN Visit ON Account_Item.visit_id = Visit.id
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = IFNULL(Action.person_id, Visit.person_id)
            LEFT JOIN Organisation AS ActionOrg ON ActionOrg.id = ActionPerson.org_id
            LEFT JOIN OrgStructure AS ActionOrgSruct ON ActionPerson.orgStructure_id = ActionOrgSruct.id
            LEFT JOIN rbSpeciality AS ActionPersonSpeciality ON ActionPersonSpeciality.id = ActionPerson.speciality_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile
                ON rbService.medicalAidProfile_id = ServiceMedicalAidProfile.id
            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
            LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
            LEFT JOIN (
                SELECT A.event_id, SUM(A.amount) AS amount
                FROM Account_Item A
                WHERE A.deleted = 0
                GROUP BY A.event_id
            ) AS TotalAmount ON TotalAmount.event_id = Account_Item.event_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidKind ON
                rbMedicalAidKind.id = EventType.medicalAidKind_id
            LEFT JOIN Event AS LastEvent ON
                LastEvent.id = getLastEventId(Event.id)"""
        where = """Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND {0}""".format(self.tableAccountItem['id'].inlist(self.idList))
        orderBy = 'Client.id, Event.id'
        return (select, tables, where, orderBy)


    def getAccMkbList(self, eventId, mkb):
        stmt = u"""SELECT ds.MKB,
                ds.setDate BETWEEN Event.setDate AND Event.execDate,
                CASE
                    WHEN rbDispanser.code = '1' THEN '1'
                    WHEN rbDispanser.code IN ('2', '6') THEN '2'
                    ELSE '3'
                END
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id
                    AND ds.deleted = 0
                    AND dc.deleted = 0)
                LEFT JOIN rbDispanser ON rbDispanser.id = dc.dispanser_id
                LEFT JOIN Event ON dc.event_id = Event.id
                WHERE dc.diagnosisType_id IN (
                    SELECT id
                    FROM rbDiagnosisType
                    WHERE code IN ('2', '9'))
                AND ds.MKB != 'Z00.0'
                AND ds.MKB != '%s'
                AND dc.event_id = %d""" % (mkb, eventId)

        query = self.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            result.append((forceString(record.value(0)),
                           forceString(record.value(1)),
                           forceString(record.value(2))))

        return result


    def getDiagResultList(self, eventId, serviceId):
        u'Возвращает словарь с множествами кодов NAZ*'
        stmt = u"""SELECT CASE
            WHEN rbDiagnosticResult.code = '505' THEN '1'
            WHEN rbDiagnosticResult.code = '506' THEN '2'
            WHEN rbDiagnosticResult.code = '507' THEN '3'
            WHEN rbDiagnosticResult.code = '511' THEN '4'
            ELSE ''
        END AS NAZ_NAZ_V,
        IF(rbHealthGroup.code IN ('1','2'), NULL,
            rbDiagnosticResult.regionalCode) AS NAZ_NAZ_R,
        IF(rbHealthGroup.code NOT IN ('1','2') AND
            rbDiagnosticResult.regionalCode IN ('1','2'),
                rbSpeciality.usishCode,'') AS NAZ_NAZ_SP,
        IF(rbHealthGroup.code NOT IN ('1','2') AND
            rbDiagnosticResult.regionalCode IN ('4','5'),
            rbMedicalAidProfile.regionalCode, NULL) AS NAZ_NAZ_PMP,
        IF(rbHealthGroup.code NOT IN ('1','2') AND
            rbDiagnosticResult.regionalCode = '6',
            rbMedicalAidProfile.regionalCode, NULL) AS NAZ_NAZ_PK,
        rbHealthGroup.code AS healthGroupCode,
        rbDiagnosticResult.regionalCode
        FROM Diagnostic dc
        LEFT JOIN rbDiagnosticResult ON dc.result_id = rbDiagnosticResult.id
        LEFT JOIN rbHealthGroup ON rbHealthGroup.id = dc.healthGroup_id
        LEFT JOIN rbSpeciality ON rbSpeciality.id = dc.speciality_id
        LEFT JOIN Person ON Person.id = dc.person_id
        LEFT JOIN rbService_Profile ON rbService_Profile.master_id = {serviceId}
            AND rbService_Profile.speciality_id = Person.speciality_id
        LEFT JOIN rbMedicalAidProfile ON
            rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
        WHERE dc.event_id = {eventId}""".format(
            eventId=eventId, serviceId=serviceId)
        query = self.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            code = forceString(record.value('healthGroupCode'))
            regionalCode = forceString(record.value('regionalCode'))

            if code not in ('1', '2') and regionalCode:
                result.append(record)

        return result

# ******************************************************************************

class R08XmlStreamWriter(COrder79v3XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR')

    completeEventDateFields = ('DATE_Z_1', 'DATE_Z_2')
    completeEventFields1 = (('IDCASE', 'VIDPOM', 'LPU', 'VBR')
                            + completeEventDateFields +
                            ('P_OTK', 'RSLT_D', 'OS_SLUCH'))
    completeEventFields2 = ('IDSP', 'SUMV')

    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields1 = (('SL_ID', 'LPU_1', 'NHISTORY')
                    + eventDateFields +
                    ('DS1', 'DS1_PR', 'PR_D_N'))
    eventFields2 = ('ED_COL', 'TARIF', 'SUM_M')

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'LPU', 'LPU_1')
                     + serviceDateFields +
                     ('P_OTK', 'CODE_USL',  'TARIF', 'SUMV_USL', 'PRVS',
                      'CODE_MD'))
    serviceSubGroup = {}
    nazFields = ('NAZ_N', 'NAZ_R', 'NAZ_SP', 'NAZ_V', 'NAZ_PMP', 'NAZ_PK')
    ds2nFields = ('DS2','DS2_PR', 'PR_DS2_N')

    requiredFields = ('N_ZAP', 'PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'NOVOR',
                      'IDCASE', 'VIDPOM', 'LPU', 'VBR', 'DATE_Z_1', 'DATE_Z_2',
                      'P_OTK', 'RSLT_D', 'IDSP', 'SUMV', 'SL_ID', 'NHISTORY',
                      'DATE_1', 'DATE_2', 'DS1', 'PR_D_N', 'SUM_M', 'DS2',
                      'PR_DS2_N', 'NAZ_N', 'NAZR', 'IDSERV', 'LPU', 'DATE_IN',
                      'DATE_OUT', 'P_OTK', 'CODE_USL',  'SUMV_USL', 'PRVS',
                      'CODE_MD', )

    def __init__(self, parent):
        COrder79v3XmlStreamWriter.__init__(self, parent)


    def dispanserType(self, params):
        u"""Возвращает код типа ДД"""
        return getEventTypeCode(self._parent.db, params['accId'])


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.0')
        self.writeTextElement('DATA', date.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', self._parent.getCompleteEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', formatAccNumber(params))
        self.writeTextElement('DSCHET',
                              params['accDate'].toString(Qt.ISODate))

        if params['payerCode']:
            self.writeTextElement('PLAT', params['payerCode'])

        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeTextElement('DISP', self.dispanserType(params))
        self.writeEndElement() # SCHET

        params['completeEventSum'] = self._parent.getCompleteEventSum()


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        lpu1Code = forceString(record.value('SL_LPU_1'))
        serviceLpu1Code = forceString(record.value('USL_LPU_1'))

        if not lpu1Code:
            parentId = forceRef(record.value('personParentOrgStructureId'))
            lpu1Code = self.getLpuCode(parentId)

            if lpu1Code:
                record.setValue('SL_LPU_1', toVariant(lpu1Code))


        if not serviceLpu1Code:
            parentId = forceRef(record.value('actionParentOrgStructureId'))
            serviceLpu1Code = self.getLpuCode(parentId)

            if serviceLpu1Code:
                record.setValue('USL_LPU_1', toVariant(serviceLpu1Code))

        eventSum = params['mapEventIdToSum'].get(eventId, '0')

        local_params = {
            'SL_SUMV': eventSum,
            'SL_TARIF': eventSum,
            'SL_SUM_M': params['mapEventIdToSum'].get(eventId, '')
        }

        local_params.update(params)

        if eventId != self._lastEventId:
            params['USL_IDSERV'] = 0

            if self._lastEventId:
                self.exportActions(eventId, params)
                self.writeEndElement() # SL

            mkb = forceString(record.value('SL_DS1'))
            accMkbList = self._parent.getAccMkbList(eventId, mkb)
            record.setValue('SL_DS1', toVariant(mkb[:5]))
            _record = CExtendedRecord(record, local_params)
            self.writeGroup('SL', self.eventFields1, _record,
                            closeGroup=False, dateFields=self.eventDateFields)

            for mkb, isPrimary, disp in accMkbList:
                local_params['DS2_N_DS2'] = mkb[:5]
                local_params['DS2_N_DS2_PR'] = isPrimary
                local_params['DS2_N_PR_DS2_N'] = disp
                _record = CExtendedRecord(record, local_params)
                self.writeGroup('DS2_N', self.ds2nFields, _record)

            diagRecordList = self._parent.getDiagResultList(
                eventId, forceRef(record.value('serviceId')))

            if diagRecordList:
                local_params['NAZ_NAZ_N'] = 0

                for diagRecord in diagRecordList:
                    local_params['NAZ_NAZ_N'] += 1
                    _record = CExtendedRecord(diagRecord, local_params)
                    self.writeGroup('NAZ', self.nazFields, _record)

            _record = CExtendedRecord(record, local_params)
            self.writeGroup('SL', self.eventFields2, _record,
                            closeGroup=False, openGroup=False)
            self._lastEventId = eventId


    def exportActions(self, eventId, params):
        u"""Выгружает  все действия по указанному событию"""

        if eventId not in params.setdefault('exportedEvents', set()):
            params['exportedEvents'].add(eventId)
            stmt = (u"""SELECT PersonOrganisation.infisCode AS USL_LPU,
                ActionOrgSruct.infisCode AS USL_LPU_1,
                IFNULL(Action.begDate, Action.endDate) AS USL_DATE_IN,
                Action.endDate AS USL_DATE_OUT,
                0 AS USL_P_OTK,
                rbService.infis AS USL_CODE_USL,
                0 AS USL_TARIF,
                0 AS USL_SUMV_USL,
                rbSpeciality.regionalCode AS USL_PRVS,
                Person.regionalCode AS USL_CODE_MD,
                Action.id AS actionId,
                '1' AS MR_USL_N_MR_N,
                rbSpeciality.regionalCode AS MR_USL_N_PRVS,
                Person.regionalCode AS MR_USL_N_CODE_MD
            FROM Action
            LEFT JOIN Event ON Action.event_id = Event.id
            LEFT JOIN Person ON Person.id = Action.person_id
            LEFT JOIN Organisation ON Organisation.id = IFNULL(Action.org_id, Person.org_id)
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
            LEFT JOIN OrgStructure AS ActionOrgSruct ON Person.orgStructure_id = ActionOrgSruct.id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN rbService ON ActionType.nomenclativeService_id = rbService.id
            WHERE Action.event_id = {evendId}
              AND ActionType.nomenclativeService_id IS NOT NULL
              AND Action.id NOT IN ({exportedActions})
              AND Action.deleted = 0""".format(
                  evendId=eventId, exportedActions=','.join(
                      params.setdefault('exportedActions', set()))))

            query = self._parent.db.query(stmt)

            while query.next():
                params['USL_IDSERV'] += 1
                record = query.record()
                record = CExtendedRecord(record, params)
                self.writeGroup('USL', self.serviceFields, record,
                                subGroup=self.serviceSubGroup,
                                dateFields=self.serviceDateFields)


    def writeService(self, record, params):
        params.setdefault('exportedActions', set()).add(
            forceString(record.value('actionId')))
        params['USL_IDSERV'] += 1
        record = CExtendedRecord(record, params)
        self.writeGroup('USL', self.serviceFields, record,
                        dateFields=self.serviceDateFields)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if self._lastEventId:
            self.exportActions(self._lastEventId, params)

        COrder79v3XmlStreamWriter.writeFooter(self, params)


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))
        eventId = forceRef(record.value('eventId'))

        if eventId != self._lastEventId:
            if self._lastClientId:
                self.exportActions(self._lastEventId, params)
                # выгрузка незавершенных действий
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                self._lastRecord,
                                closeGroup=True, openGroup=False)
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', str(params['rowNumber']))
            params['rowNumber'] += 1

            self.writeTextElement('PR_NOV', params.get('isReexposed','0'))

            params['birthDate'] = forceDate(record.value('PERS_DR'))
            execDate = forceDate(record.value('execDate'))
            params['isJustBorn'] = params['birthDate'].daysTo(execDate) < 28
            params['isAnyBirthDoc'] = forceBool(record.value('isAnyBirthDoc'))
            self.writeClientInfo(record, params)
            self._lastClientId = clientId
            self._lastEventId = None

        COrder79v3XmlStreamWriter.writeRecord(self, record, params)


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))
        patrName = forceString(record.value('PERS_OT'))
        noPatrName = not patrName or patrName.upper() == u'НЕТ'

        local_params = {
            'Z_SL_SUMV': params['completeEventSum'].get(lastEventId),
            'Z_SL_OS_SLUCH': '2' if (noPatrName or (
                params['isJustBorn'] and not params['isAnyBirthDoc'])) else ''
        }

        local_params.update(params)
        record_ = CExtendedRecord(record, local_params)
        COrder79v3XmlStreamWriter.writeCompleteEvent(self, record_, params)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        sex = forceString(record.value('clientSex'))

        local_params = {
            'PACIENT_NOVOR':  ('1%s%s1' % (sex[:1],
                                params['birthDate'].toString('ddMMyy')
                             )) if (params['isJustBorn'] and
                                not params['isAnyBirthDoc']) else '0',
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def getLpuCode(self, parentId):
        u"""Возвращает tfomsCode родительского подразделения"""
        result = None
        i = 0 # защита от перекрестных ссылок

        while not result and parentId and i < 1000:
            parentId, result = self._parent.getOrgStructureInfo(parentId)
            i += 1

        return result

# ******************************************************************************

class CExportPage1(CR08ExportPage1):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CR08ExportPage1.__init__(self, parent, prefix)
        self.chkReexposed.setEnabled(True)


    def prepareStmt(self, params):
        (select, tables, where, orderBy) = CR08ExportPage1.prepareStmt(
            self, params)
        select += """, (SELECT MAX(ds.id) IS NOT NULL
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code = '9')
                  AND dc.event_id = Account_Item.event_id
                  AND rbDiseasePhases.code = 10
                  AND SUBSTR(ds.MKB,1,1) = 'C'
            ) AS SL_DS_ONK,
            ClientDocument.date AS PERS_DOCDATE,
            ClientDocument.origin AS PERS_DOCORG,
            IF(rbPolicyKind.code = '3', ClientPolicy.number, '') AS PERS_ENP,
            1 AS MR_USL_N_MR_N,
            ActionPersonSpeciality.regionalCode AS MR_USL_N_PRVS,
            ActionPerson.regionalCode AS MR_USL_N_CODE_MD,

            rbPolicyKind.code AS policyKindCode"""
        tables += """LEFT JOIN rbDiseasePhases ON
            rbDiseasePhases.id = Diagnostic.phase_id"""

        return (select, tables, where, orderBy)


    def getDiagResultList(self, eventId, serviceId):
        u'Возвращает словарь с множествами кодов NAZ*'
        stmt = u"""SELECT CASE
            WHEN rbDiagnosticResult.code = '505' THEN '1'
            WHEN rbDiagnosticResult.code = '506' THEN '2'
            WHEN rbDiagnosticResult.code = '507' THEN '3'
            WHEN rbDiagnosticResult.code = '511' THEN '4'
            ELSE ''
        END AS NAZ_NAZ_V,
        IF(rbHealthGroup.code IN ('1','2'), NULL,
            rbDiagnosticResult.regionalCode) AS NAZ_NAZ_R,
        IF(rbHealthGroup.code NOT IN ('1','2') AND
            rbDiagnosticResult.regionalCode IN ('1','2'),
                rbSpeciality.federalCode,'') AS NAZ_NAZ_SP,
        IF(rbHealthGroup.code NOT IN ('1','2') AND
            rbDiagnosticResult.regionalCode IN ('4','5'),
            rbMedicalAidProfile.regionalCode, NULL) AS NAZ_NAZ_PMP,
        IF(rbHealthGroup.code NOT IN ('1','2') AND
            rbDiagnosticResult.regionalCode = '6',
            rbMedicalAidProfile.regionalCode, NULL) AS NAZ_NAZ_PK,
        rbHealthGroup.code AS healthGroupCode,
        rbDiagnosticResult.regionalCode,
        (SELECT APS.value
            FROM ActionProperty AP
            LEFT JOIN ActionProperty_String AS APS ON APS.id = AP.id
            WHERE AP.deleted = 0
                AND AP.action_id = Action.id
                AND AP.type_id = (
                    SELECT id FROM ActionPropertyType APT
                    WHERE APT.name = 'Код услуги'
                        AND APT.deleted = 0
                        AND APT.actionType_id = Action.actionType_id)
            LIMIT 1) AS NAZ_NAZ_USL,
        Action.endDate AS NAZ_NAPR_DATE,
        DirectOrg.miacCode AS NAZ_NAPR_MO,
        rbSpeciality.federalCode AS NAZ_NAZ_IDDOKT,
        Action.id AS directionActionId
        FROM Diagnostic dc
        LEFT JOIN rbDiagnosticResult ON dc.result_id = rbDiagnosticResult.id
        LEFT JOIN rbHealthGroup ON rbHealthGroup.id = dc.healthGroup_id
        LEFT JOIN rbSpeciality ON rbSpeciality.id = dc.speciality_id
        LEFT JOIN Person ON Person.id = dc.person_id
        LEFT JOIN rbService_Profile ON rbService_Profile.master_id = {serviceId}
            AND rbService_Profile.speciality_id = Person.speciality_id
        LEFT JOIN rbMedicalAidProfile ON
            rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
        LEFT JOIN Action ON Action.id = (SELECT MAX(A.id)
             FROM Action A
             WHERE A.event_id = {eventId}
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT AT.id
                 FROM ActionType AT
                 WHERE AT.flatCode = 'directionCancer'
        ))
        LEFT JOIN Action AS PrevAction ON PrevAction.id = Action.prevAction_id
        LEFT JOIN ActionType ON ActionType.id = PrevAction.actionType_id
        LEFT JOIN Organisation AS DirectOrg ON DirectOrg.id = (
            SELECT APO.value
            FROM ActionProperty AP
            LEFT JOIN ActionProperty_Organisation AS APO ON APO.id = AP.id
            WHERE AP.deleted = 0
                AND AP.action_id = Action.id
                AND AP.type_id = (
                    SELECT id FROM ActionPropertyType APT
                    WHERE APT.name = 'Куда направляется'
                        AND APT.deleted = 0
                        AND APT.actionType_id = Action.actionType_id))
        LEFT JOIN rbService ON rbService.id = ActionType.nomenclativeService_id
        WHERE dc.event_id = {eventId}""".format(
            eventId=eventId, serviceId=serviceId)
        query = self.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            code = forceString(record.value('healthGroupCode'))
            regionalCode = forceString(record.value('regionalCode'))

            if code not in ('1', '2') and regionalCode:
                result.append(record)

        return result


    def exportInt(self):
        params = self.processParams()
        params['isReexposed'] = '1' if self.chkReexposed.isChecked() else '0'
        self.setProcessParams(params)
        CR08ExportPage1.exportInt(self)

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CAbstractExportPage2.__init__(self, parent, 'Export%s' % prefix)


    def saveExportResults(self):
        fileList = (self._parent.getFullXmlFileName(),
                    self._parent.getPersonalDataFullXmlFileName())
        zipFileName = self._parent.getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                        self.moveFiles([zipFileName]))


    def validatePage(self):
        success = self.saveExportResults()

        if success:
            QtGui.qApp.preferences.appPrefs[
                '%sExportDir' % self.prefix] = toVariant(self.edtDir.text())
            self.wizard().setAccountExposeDate()
        return success

# ******************************************************************************

class CXmlStreamWriter(R08XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO',
                    'SMO', 'SMO_NAM', 'NOVOR')

    eventFields1 = (('SL_ID', 'LPU_1', 'NHISTORY')
                    + R08XmlStreamWriter.eventDateFields +
                    ('DS1', 'DS1_PR', 'DS_ONK', 'PR_D_N'))

    nazFields = ('NAZ_N', 'NAZ_R', 'NAZ_IDDOKT', 'NAZ_V', 'NAZ_USL', 'NAPR_DATE',
                 'NAPR_MO', 'NAZ_PMP', 'NAZ_PK')
    nazDateFields = ('NAPR_DATE', )

    requiredFields = ('N_ZAP', 'PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'NOVOR',
                      'IDCASE', 'VIDPOM', 'LPU', 'VBR', 'DATE_Z_1', 'DATE_Z_2',
                      'P_OTK', 'RSLT_D', 'IDSP', 'SUMV', 'SL_ID', 'NHISTORY',
                      'DATE_1', 'DATE_2', 'DS1', 'PR_D_N', 'SUM_M', 'DS2',
                      'PR_DS2_N', 'NAZ_N', 'NAZR', 'IDSERV', 'LPU', 'DATE_IN',
                      'DATE_OUT', 'P_OTK', 'CODE_USL',  'SUMV_USL', )

    serviceFields = ('IDSERV', 'LPU', 'LPU_1', 'DATE_IN', 'DATE_OUT',
                     'P_OTK', 'CODE_USL',  'TARIF', 'SUMV_USL', 'MR_USL_N')
    serviceSubGroup = {
        'MR_USL_N': {'fields': ('MR_N', 'PRVS', 'CODE_MD')},
    }

    def __init__(self, parent):
        R08XmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.1')
        self.writeTextElement('DATA', date.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', self._parent.getCompleteEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', formatAccNumber(params))
        self.writeTextElement('DSCHET',
                              params['accDate'].toString(Qt.ISODate))

        if params['payerCode']:
            self.writeTextElement('PLAT', params['payerCode'])

        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeTextElement('DISP', self.dispanserType(params))
        self.writeEndElement() # SCHET

        params['completeEventSum'] = self._parent.getCompleteEventSum()


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        lpu1Code = forceString(record.value('SL_LPU_1'))
        serviceLpu1Code = forceString(record.value('USL_LPU_1'))

        if not lpu1Code:
            parentId = forceRef(record.value('personParentOrgStructureId'))
            lpu1Code = self.getLpuCode(parentId)

            if lpu1Code:
                record.setValue('SL_LPU_1', toVariant(lpu1Code))


        if not serviceLpu1Code:
            parentId = forceRef(record.value('actionParentOrgStructureId'))
            serviceLpu1Code = self.getLpuCode(parentId)

            if serviceLpu1Code:
                record.setValue('USL_LPU_1', toVariant(serviceLpu1Code))

        eventSum = params['mapEventIdToSum'].get(eventId, 0)

        local_params = {
            'SL_SUMV': '{0:.2f}'.format(eventSum),
            'SL_TARIF': '{0:.2f}'.format(eventSum),
            'SL_SUM_M': params['mapEventIdToSum'].get(eventId, '')
        }
        local_params.update(params)

        if eventId != self._lastEventId:
            params['USL_IDSERV'] = 0

            if self._lastEventId:
                self.exportActions(eventId, params)
                self.writeEndElement() # SL

            mkb = forceString(record.value('SL_DS1'))
            accMkbList = self._parent.getAccMkbList(eventId, mkb)
            record.setValue('SL_DS1', toVariant(mkb[:5]))
            _record = CExtendedRecord(record, local_params)
            self.writeGroup('SL', self.eventFields1, _record,
                            closeGroup=False, dateFields=self.eventDateFields)

            for mkb, isPrimary, disp in accMkbList:
                local_params['DS2_N_DS2'] = mkb[:5]
                if isPrimary and isPrimary != '0':
                    local_params['DS2_N_DS2_PR'] =  isPrimary
                local_params['DS2_N_PR_DS2_N'] = disp
                _record = CExtendedRecord(record, local_params)
                self.writeGroup('DS2_N', self.ds2nFields, _record)

            diagRecordList = self._parent.getDiagResultList(
                eventId, forceRef(record.value('serviceId')))

            if diagRecordList:
                local_params['NAZ_NAZ_N'] = 0

                for diagRecord in diagRecordList:
                    local_params['NAZ_NAZ_N'] += 1
                    nazR = forceString(diagRecord.value('3'))
                    dsOnk = forceString(record.value('USL_DS_ONK'))
                    if not (nazR == '3' and dsOnk == '1'):
                        record.setValue('NAZ_NAZ_USL', '')
                    _record = CExtendedRecord(diagRecord, local_params)
                    self.writeGroup('NAZ', self.nazFields, _record,
                                    dateFields=self.nazDateFields)

            _record = CExtendedRecord(record, local_params)
            self.writeGroup('SL', self.eventFields2, _record,
                            closeGroup=False, openGroup=False)
            self._lastEventId = eventId


    def exportActions(self, eventId, params):
        u"""Выгружает  все действия по указанному событию"""

        if eventId not in params.setdefault('exportedEvents', set()):
            params['exportedEvents'].add(eventId)
            stmt = (u"""SELECT PersonOrganisation.infisCode AS USL_LPU,
                ActionOrgSruct.infisCode AS USL_LPU_1,
                IFNULL(Action.begDate, Action.endDate) AS USL_DATE_IN,
                Action.endDate AS USL_DATE_OUT,
                0 AS USL_P_OTK,
                rbService.infis AS USL_CODE_USL,
                0 AS USL_TARIF,
                0 AS USL_SUMV_USL,
                rbSpeciality.regionalCode AS MR_USL_N_PRVS,
                Person.regionalCode AS MR_USL_N_CODE_MD,
                1 AS MR_USL_N_MR_N,
                Action.id AS actionId
            FROM Action
            LEFT JOIN Event ON Action.event_id = Event.id
            LEFT JOIN Person ON Person.id = Action.person_id
            LEFT JOIN Organisation ON Organisation.id = IFNULL(Action.org_id, Person.org_id)
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
            LEFT JOIN OrgStructure AS ActionOrgSruct ON Person.orgStructure_id = ActionOrgSruct.id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN rbService ON ActionType.nomenclativeService_id = rbService.id
            WHERE Action.event_id = {evendId}
              AND (ActionType.nomenclativeService_id IS NOT NULL
                   AND ActionType.class != 1)
              AND Action.id NOT IN ({exportedActions})
              AND Action.deleted = 0""".format(
                  evendId=eventId, exportedActions=','.join(
                      params.setdefault('exportedActions', set()))))

            query = self._parent.db.query(stmt)

            while query.next():
                params['USL_IDSERV'] += 1
                record = query.record()
                for field in 'USL_TARIF', 'USL_SUMV_USL':
                    record.setValue(field, '{0:.2f}'.format(
                        forceDouble(record.value(field))))
                record = CExtendedRecord(record, params)
                self.writeGroup('USL', self.serviceFields, record,
                                subGroup=self.serviceSubGroup,
                                dateFields=self.serviceDateFields)


    def writeService(self, record, params):
        params.setdefault('exportedActions', set()).add(
            forceString(record.value('actionId')))
        params['USL_IDSERV'] += 1
        record = CExtendedRecord(record, params)
        for field in 'USL_TARIF', 'USL_SUMV_USL':
            record.setValue(field, '{0:.2f}'.format(
                forceDouble(record.value(field))))
        self.writeGroup('USL', self.serviceFields, record,
                        subGroup=self.serviceSubGroup,
                        dateFields=self.serviceDateFields)

# ******************************************************************************

class CPersonalDataWriter(CR08PersonalDataWriter):
    u"""Осуществляет запись данных экспорта в XML"""
    clientDateFields = ('DR_P', 'DOCDATE', 'DR')
    clientFields = ('ID_PAC', 'FAM', 'IM', 'OT', 'W', 'DR',
                    'DOST', 'TEL', 'FAM_P', 'IM_P', 'OT_P', 'W_P', 'MR',
                    'DOCTYPE', 'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG', 'SNILS',
                    'OKATOG', 'OKATOP')

    def __init__(self, parent):
        CR08PersonalDataWriter.__init__(self, parent)

    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']

        self.version = '3.2' if settleDate > QDate(2019, 10, 1) else '3.1'
        CR08PersonalDataWriter.writeHeader(self, params)


    def writeRecord(self, record, params):
        policyKindCode = forceString(record.value('policyKindCode'))
        if policyKindCode != '3':
            record.setNull('PERS_SPOLIS')
            record.setNull('PERS_NPOLIS')
        CR08PersonalDataWriter.writeRecord(self, record, params)

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position
    testAccountExport(exportR08NativeHealthExaminationV173,
        configFileName=u'75_3_s11.ini',
        eventIdList=[2413243])
