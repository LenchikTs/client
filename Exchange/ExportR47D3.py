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

u"""Экспорт реестра  в формате XML. Кировск Д3, Д4"""

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, Qt, QTextCodec

from library.Utils import (forceBool, forceInt, toVariant, forceString,
                           forceRef, forceDate)

from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CExportHelperMixin,
                             CAbstractExportPage1Xml,
                             CAbstractExportPage2)
from Exchange.Order79Export import COrder79ExportWizard
from Exchange.ExportR47D1 import PersonalDataWriter, formatAccNumber
from Exchange.Utils import compressFileInZip
from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1

# выводит в консоль имена невыгруженных полей
DEBUG = False

def exportR47D3(widget, accountId, accountItemIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

def getEventTypeCode(_db, accountId):
    u"""Вовзращает префикс имени файла"""
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

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Кировска, ДД"""

    mapPrefixToEventTypeCode = {u'ДВ1': 'DP', u'ДВ2': 'DV', u'ОПВ': 'DO',
        u'ДС1': 'DS', u'ДС2': 'DU', u'ОН1': 'DF', u'ОН2': 'DD', u'ОН3': 'DR'}

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Кировска, ДД'
        prefix = 'R47DD'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

        self.accountIdList = None
        self.__xmlBaseFileName = None


    def setAccountIdList(self, accountIdList):
        u"""Запоминает список идентификаторов счетов"""
        self.accountIdList = accountIdList


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""

        if self.__xmlBaseFileName:
            result = self.__xmlBaseFileName
        else:
            tableOrganisation = self.db.table('Organisation')
            info = self.info

            payerCode = forceString(self.db.translate(tableOrganisation,
                                'id', info['payerId'], 'infisCode'))
            payerPrefix = u'T' if payerCode == u'47' else u'S'
            recipientCode = forceString(self.db.translate(tableOrganisation,
                                'id', QtGui.qApp.currentOrgId(), 'infisCode'))

            year = info['settleDate'].year() %100
            month = info['settleDate'].month()
            packetNumber = info['accId']

            postfix = u'%02d%02d%d' % (year, month,
                                        packetNumber) if addPostfix else u''
            result = u'%2sM%s%s%s_%s.xml' % (self.prefixX(info['accId']),
                    recipientCode, payerPrefix, payerCode, postfix)
            self.__xmlBaseFileName = result

        return result


    def prefixX(self, accountId):
        u"""Вовзращает префикс имени файла"""
        code = getEventTypeCode(self.db, accountId)
        return self.mapPrefixToEventTypeCode.get(code)


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L%s' % self._getXmlBaseFileName(addPostfix)[2:]


    def getZipFileName(self):
        u"""Возвращает имя архива:"""
        return u'%s.zip' % self._getXmlBaseFileName(True)[:-4]

# ******************************************************************************

class CExportPage1(CAbstractExportPage1Xml, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self), PersonalDataWriter(self))
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
        self.edtPacketNumber.setVisible(False)
        self.lblPacketNumber.setVisible(False)

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


    def prepareStmt(self, params):
        select = u"""Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            Action.id AS actionId,
            Visit.id AS visitId,
            Event.execDate,

            Account_Item.event_id AS SLUCH_IDCASE,
            FirstVisitMedicalAidKind.regionalCode AS SLUCH_VIDPOM,
            PersonOrganisation.infisCode AS SLUCH_LPU,
            PersonOrgStructure.tfomsCode AS SLUCH_LPU_1,
            IF(rbScene.code = '5', 1, 0) AS SLUCH_VBR,
            Event.id AS SLUCH_NHISTORY,
            IF(rbDiagnosticResult.code = '502', 1, 0) AS SLUCH_P_OTK,
            Event.setDate AS SLUCH_DATE_1,
            Event.execDate AS SLUCH_DATE_2,
            Diagnosis.MKB AS SLUCH_DS1,
            EventResult.regionalCode AS SLUCH_RSLT_D,
            IF(rbHealthGroup.code IN ('1','2'), '',
                rbDiagnosticResult.regionalCode) AS SLUCH_NAZR,
            IF(rbHealthGroup.code NOT IN ('1','2') AND
                rbDiagnosticResult.regionalCode IN ('1','2'),
                    DiagnosticSpeciality.usishCode,'') AS SLUCH_NAZ_SP,
            IF(rbHealthGroup.code NOT IN ('1','2') AND
                rbDiagnosticResult.regionalCode = '3',
                    rbDiagnosticResult.code,'') AS SLUCH_NAZ_V,
            IF(rbHealthGroup.code NOT IN ('1','2') AND
                rbDiagnosticResult.regionalCode IN ('4','5'),
                FirstVisitMedicalAidProfile.regionalCode, '') AS SLUSH_NAZ_PMP,
            IF(rbDispanser.code IN ('1', '2', '6'), 1, 0) AS SLUCH_PR_D_N,
            rbMedicalAidUnit.federalCode AS SLUCH_IDSP,
            TotalAmount.amount AS SLUCH_ED_COL,

            PersonOrganisation.infisCode AS USL_LPU,
            ActionOrgSruct.tfomsCode AS USL_LPU_1,
            IFNULL(Visit.date, Action.begDate) AS USL_DATE_IN,
            IFNULL(Visit.date, Action.endDate) AS USL_DATE_OUT,
            0 AS USL_P_OTK,
            rbService.code AS USL_CODE_USL,
            Account_Item.price AS USL_TARIF,
            Account_Item.`sum` AS USL_SUMV_USL,
            ActionPersonSpeciality.usishCode AS USL_PRVS,
            ActionPerson.regionalCode AS USL_CODE_MD,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            ClientPolicy.serial AS PACIENT_SPOLIS,
            ClientPolicy.number AS PACIENT_NPOLIS,
            Insurer.OKATO AS PACIENT_ST_OKATO,
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
            ClientDocument.serial AS PERS_DOCSER,
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
            LEFT JOIN rbHealthGroup ON rbHealthGroup.id = Diagnostic.healthGroup_id
            LEFT JOIN rbSpeciality AS DiagnosticSpeciality ON DiagnosticSpeciality.id = Diagnostic.speciality_id
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
            LEFT JOIN Visit AS FirstVisit ON FirstVisit.id = (
                SELECT id FROM Visit AS V1
                WHERE V1.deleted = 0 AND V1.event_id = Account_Item.event_id
                     AND V1.person_id = Event.execPerson_id
                LIMIT 0,1)
            LEFT JOIN rbService AS FirstVisitService ON FirstVisit.service_id = FirstVisitService.id
            LEFT JOIN rbMedicalAidKind AS FirstVisitMedicalAidKind ON
                FirstVisitMedicalAidKind.id = FirstVisitService.medicalAidKind_id
            LEFT JOIN rbMedicalAidProfile AS FirstVisitMedicalAidProfile ON
                FirstVisitMedicalAidProfile.id = FirstVisitService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile
                ON rbService.medicalAidProfile_id = ServiceMedicalAidProfile.id
            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
            LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
            LEFT JOIN (
                SELECT A.event_id, SUM(A.amount) AS amount
                FROM Account_Item A
                WHERE A.deleted = 0
                GROUP BY A.event_id
            ) AS TotalAmount ON TotalAmount.event_id = Account_Item.event_id"""
        where = """Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND {0}""".format(self.tableAccountItem['id'].inlist(self.idList))
        orderBy = 'Client.id, Event.id'

        return (select, tables, where, orderBy)



    def getOrgStructureInfo(self, _id):
        u"""Возвращает parent_id и tfomsCode для подразделения"""
        result = self._orgStructInfoCache.get(_id, -1)

        if result == -1:
            result = (None, None)
            record = self._db.getRecord('OrgStructure',
                    ['parent_id', 'tfomsCode'], _id)

            if record:
                result = (forceRef(record.value(0)),
                        forceString(record.value(1)))

            self._orgStructInfoCache[_id] = result

        return result


    def getAccMkbList(self, eventId, mkb):
        stmt = u"""SELECT ds.MKB
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id
                    AND ds.deleted = 0
                    AND dc.deleted = 0)
                WHERE dc.diagnosisType_id IN (
                    SELECT id
                    FROM rbDiagnosisType
                    WHERE code = '2')
                AND ds.MKB != 'Z00.0'
                AND ds.MKB != '%s'
                AND dc.event_id = %d""" % (mkb, eventId)

        query = self.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            result.append(forceString(record.value(0)))

        return result


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

class XmlStreamWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM')

    eventDateFields = ('DATE_1', 'DATE_2')

    eventFields1 = ('IDCASE', 'VIDPOM', 'LPU', 'LPU_1', 'VBR', 'NHISTORY',
        'P_OTK') + eventDateFields + ('DS1',)

    eventFields2 = ('RSLT_D', 'NAZR', 'NAZ_SP',
        'NAZ_V', 'NAZ_PMP', 'PR_D_N', 'IDSP', 'ED_COL', 'TARIF', 'SUMV',
        'OPLATA')

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = (('IDSERV', 'LPU', 'LPU_1')  + serviceDateFields + ('P_OTK',
        'CODE_USL', 'TARIF', 'SUMV_USL', 'PRVS', 'CODE_MD'))

    ds2nFields = ('DS2', )
    requiredFields = ('N_ZAP', 'PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'IDCASE',
        'VIDPOM', 'LPU', 'VBR', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1', 'RSLT_D',
        'IDSP', 'SUMV', 'DS2', 'IDSERV', 'LPU', 'DATE_IN', 'DATE_OUT', 'P_OTK',
        'CODE_USL', 'SUMV_USL', 'PRVS', 'CODE_MD', )

    mapEventOrderToForPom = {1: '3', 3: '3', 4: '3', 5: '3', 6: '2', 2: '1'}
    mapEventOrderToExtr = {1: '1', 2 : '2', 3: '1', 4: '1', 5: '1', 6: '1'}


    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        self.setCodec(QTextCodec.codecForName('cp1251'))


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', self._parent.getEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', formatAccNumber(params, True))
        self.writeTextElement('DSCHET',
                params['accDate'].toString(Qt.ISODate))
        self.writeTextElement('PLAT', params['payerCode'])
        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeTextElement('DISP', self.dispanserType(params))
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('lastClientId'):
            if params['lastClientId']:
                params['SLUCH_IDCASE'] += 1
                self.writeEndElement() # SLUCH
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['rowNumber']))
            self.writeTextElement('PR_NOV', '0')

            params['birthDate'] = forceDate(record.value('clientBirthDate'))
            execDate = forceDate(record.value('execDate'))
            params['isJustBorn'] = params['birthDate'].daysTo(execDate) < 28
            params['isAnyBirthDoc'] = forceString(record.value('isAnyBirthDoc'))

            self.writeClientInfo(record, params)

            params['rowNumber'] += 1
            params['lastClientId'] = clientId
            params['lastEventId'] = None

        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        params['USL_IDSERV'] += 1

        local_params = {
            'USL_PKUR': '0',
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('USL', self.serviceFields, _record,
                dateFields=self.serviceDateFields)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        sex = forceString(record.value('clientSex'))

        local_params = {
            'PACIENT_NOVOR':  ('%s%s1' % (sex[:1],
                                params['birthDate'].toString('ddMMyy')
                             )) if (params['isJustBorn'] and
                                not params['isAnyBirthDoc']) else '0',
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        patrName = forceString(record.value('PERS_OT'))
        lpu1Code = forceString(record.value('SLUCH_LPU_1'))
        serviceLpu1Code = forceString(record.value('USL_LPU_1'))
        noPatrName = not patrName or patrName.upper() == u'НЕТ'

        if not lpu1Code:
            parentId = forceRef(record.value('personParentOrgStructureId'))
            lpu1Code = self.getLpuCode(parentId)

            if lpu1Code:
                record.setValue('SLUCH_LPU_1', toVariant(lpu1Code))


        if not serviceLpu1Code:
            parentId = forceRef(record.value('actionParentOrgStructureId'))
            serviceLpu1Code = self.getLpuCode(parentId)

            if serviceLpu1Code:
                record.setValue('USL_LPU_1', toVariant(serviceLpu1Code))

        eventSum = params['mapEventIdToSum'].get(eventId, '0')

        local_params = {
            'SLUCH_OS_SLUCH': '2' if (noPatrName or (params['isJustBorn'] and
                    not params['isAnyBirthDoc'])) else '',
            'SLUCH_VERS_SPEC': 'V015',
            'SLUCH_OPLATA': '0',
            'SLUCH_KODLPU': params['lpuCode'],
            'SLUCH_EXTR': self.mapEventOrderToExtr.get(
                                   forceInt(record.value('eventOrder')), ''),
            'SLUCH_SUMV': eventSum,
            'SLUCH_TARIF': eventSum,
        }

        local_params.update(params)

        if eventId != params.setdefault('lastEventId'):
            params['USL_IDSERV'] = 0

            if params['lastEventId']:
                self.writeEndElement() # SLUCH

            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeGroup('SLUCH', self.eventFields1, _record,
                            closeGroup=False, dateFields=self.eventDateFields)

            accMkbList = self._parent.getAccMkbList(eventId,
                forceString(record.value('SLUCH_DS1')))

            for mkb in accMkbList:
                local_params['DS2_N_DS2'] = mkb
                _record = CExtendedRecord(record, local_params, DEBUG)
                self.writeGroup('DS2_N', self.ds2nFields, _record)

            self.writeGroup('SLUCH', self.eventFields2, _record,
                closeGroup=False, openGroup=False)
            params['lastEventId'] = eventId


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params['lastEventId']:
            self.writeEndElement() # SLUCH
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def writeElement(self, elementName, value=None):
        if value or elementName in self.requiredFields:
            self.writeTextElement(elementName, value)


    def getLpuCode(self, parentId):
        u"""Возвращает tfomsCode родительского подразделения"""
        result = None
        i = 0 # защита от перекрестных ссылок

        while not result and parentId and i < 1000:
            parentId, result = self._parent.getOrgStructureInfo(parentId)
            i += 1

        return result


    def dispanserType(self, params):
        u"""Возвращает код типа ДД"""
        return getEventTypeCode(self._parent.db, params['accId'])
