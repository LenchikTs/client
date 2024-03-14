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

u"""Экспорт реестра  в формате XML. Республика Калмыкия. ДД, (Д3)"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from library.Utils import (forceString, forceRef, toVariant, forceDate,
                           forceBool)
from Exchange.Order79Export import (COrder79ExportWizard,
                                    COrder79v3XmlStreamWriter)
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.ExportR08Hospital import (CR08PersonalDataWriter as
                                        PersonalDataWriter)
from Exchange.ExportR47D3 import CExportPage1, CExportPage2, getEventTypeCode

def exportR08NativeHealthExamination(widget, accountId, accountItemIdList, _):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CR08ExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

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

class CR08ExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Калмыкии"""

    mapPrefixToEventTypeCode = {u'ДВ1': 'DP', u'ДВ2': 'DV', u'ОПВ': 'DO',
                                u'ДС1': 'DS', u'ДС2': 'DU', u'ОН1': 'DF',
                                u'ОН2': 'DD', u'ОН3': 'DR'}

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии'
        prefix = 'R08D3'
        COrder79ExportWizard.__init__(self, title, prefix, CR08ExportPage1,
                                      CExportPage2, parent)

        self.page1.setXmlWriter((R08XmlStreamWriter(self.page1),
                                 PersonalDataWriter(self.page1)))

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

            year = info['settleDate'].year() %100
            month = info['settleDate'].month()
            packetNumber = self.page1.edtPacketNumber.value()

            postfix = u'%02d%02d%d' % (year, month,
                                       packetNumber) if addPostfix else u''
            result = u'%2sM%s%s%s_%s.xml' % (self.prefixX(info['accId']),
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

class CR08ExportPage1(CExportPage1):
    u"""Первая страница мастера экспорта"""
    mapDiagResultToNazV = {'505': 1, '506': 2, '507':3}

    def __init__(self, parent, prefix):
        CExportPage1.__init__(self, parent, prefix)
        self._orgStructInfoCache = {}
        self.edtPacketNumber.setVisible(True)
        self.lblPacketNumber.setVisible(True)


    def getOrgStructureInfo(self, _id):
        u"""Возвращает parent_id и tfomsCode для подразделения"""
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
        (select, tables, where, orderBy) = CExportPage1.prepareStmt(
            self, params)
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


if __name__ == '__main__':
    #pylint: disable=wrong-import-position
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position
    testAccountExport(exportR08NativeHealthExamination, 730)
