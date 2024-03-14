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

u"""Экспорт реестра скорой медицинской помощи в формате XML. Мурманск"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, Qt

from library.Utils import (forceBool, forceInt, toVariant, forceString,
    forceRef, forceDate)
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
    CAbstractExportPage1Xml, CAbstractExportPage2)
from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.ExtendedRecord import CExtendedRecord

from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1


def exportR51EmergencyXml(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта СМП Мурманской области"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг СМП для Мурманской области'
        CAbstractExportWizard.__init__(self, parent, title)
        self.prefix = 'R51SMPXml'
        self.page1 = CExportPage1(self, self.prefix)
        self.page2 = CExportPage2(self, self.prefix)

        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, self.prefix)


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""
        tableOrganisation = self.db.table('Organisation')
        tableOrgStructure = self.db.table('OrgStructure')
        info = self.info

        lpuCode = forceString(self.db.translate(
            tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
        orgStructCode = forceString(self.db.translate(tableOrgStructure,
            'id', self.info['accOrgStructureId'], 'infisCode'))
        payerCode = forceString(self.db.translate(
            tableOrganisation, 'id', info['payerId'], 'infisCode'))
        year = info['settleDate'].year() %100
        month = info['settleDate'].month()
        packetNumber = self.page1.edtPacketNumber.value()

        postfix = u'S510%s_%02d%02d%03d' % (payerCode, year, month,
            packetNumber) if addPostfix else u''
        result = u'M510%s%s047%s.xml' % (lpuCode, orgStructCode, postfix)
        return result


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return u'H%s' % self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L%s' % self._getXmlBaseFileName(addPostfix)


    def getRegionalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи региональных данных."""
        return u'T%s' % self._getXmlBaseFileName(addPostfix)


    def getPersonalDataFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getPersonalDataXmlFileName())


    def getRegionalDataFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getRegionalDataXmlFileName())


    def getFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getXmlFileName())

# ******************************************************************************

class CExportPage1(CAbstractExportPage1Xml, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self), PersonalDataWriter(self),
            RegionalDataWriter(self))
        CAbstractExportPage1Xml.__init__(self, parent, xmlWriter)
        CExportHelperMixin.__init__(self)
        self.prefix = prefix

        for widget in self.cmbRegistryType, self.lblRegistryType:
            widget.setVisible(False)

        self.actionTypeMultipleBirth = None
        self.exportedActionsList = None
        self.ignoreErrors = False

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(forceBool(prefs.get('Export%sVerboseLog' % prefix, False)))
        self.chkIgnoreErrors.setChecked(forceBool(prefs.get('Export%sIgnoreErrors' % prefix, False)))
        self.edtPacketNumber.setValue(forceInt(prefs.get('Export%sPacketNumber' % prefix, 1)))


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['Export%sIgnoreErrors' % self.prefix] = toVariant(
            self.chkIgnoreErrors.isChecked())
        prefs['Export%sVerboseLog' % self.prefix] = toVariant(
            self.chkVerboseLog.isChecked())
        prefs['Export%sPacketNumber' % self.prefix] = toVariant(
            self.edtPacketNumber.value() + 1)
        return CAbstractExportPage1Xml.validatePage(self)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)

        if hasattr(self, 'lblPacketCounter'):
            self.lblPacketCounter.setEnabled(not flag)

        if hasattr(self, 'edtPacketNumber'):
            self.edtPacketNumber.setEnabled(not flag)

# ******************************************************************************

    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        params = {
            'SLUCH_USL_OK': '4',
            'SLUCH_EXTR': '2',
            'SLUCH_DET': '0',
            'SLUCH_ED_COL': '1',
            'SLUCH_IDSP': '15',
            'SLUCH_PROFIL': '84',
            'SLUCH_PODR': '',
            'USL_PROFIL': '84',
            'USL_DET': '0',
            'SUM_VID_FIN': '1',
            'SUM_USL_VID_FIN': '1',
            'SLUCH_TOWN_HOSP': '047',
            'SLUCH_P_OTK': '0',
            'PACIENT_SMO_OK': '47000',
        }

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])
        self.exportedActionsList = []

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        self.actionTypeMultipleBirth = forceRef(self.db.translate(
            'ActionType', 'flatCode', 'MultipleBirth', 'id'))

        if not self.actionTypeMultipleBirth:
            self.logError(u'Не найден тип действия "Многоплодные роды" '
                u'(плоский код: "MultipleBirth")')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
            params['clientCount'] = self.clientCount()
            params['mapEventIdToSum'] = self.getEventSum()
            params['SLUCH_LPU_1'] = forceString(self.db.translate(
                'OrgStructure', 'id', params['accOrgStructureId'],
                'infisCode'))
            params['SLUCH_COUNT'] = params['accNumber']

        params['rowNumber'] = 0
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getPersonalDataXmlFileName(False))
        params['regionalDataFileName'] = (
            self._parent.getRegionalDataXmlFileName(False))

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        regionalDataFile = QFile(self._parent.getRegionalDataFullXmlFileName())
        regionalDataFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter, regionalDataWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        regionalDataWriter.setDevice(regionalDataFile)
        CAbstractExportPage1Xml.exportInt(self)


    def clientCount(self):
        u"""Подсчет количества уникальных пациентов в реестре счета"""
        stmt = """SELECT COUNT(DISTINCT Event.client_id)
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Event.client_id IS NOT NULL AND
            Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        """ % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = 0

        if query and query.first():
            record = query.record()

            if record:
                result = forceInt(record.value(0))

        return result


    def createQuery(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            Event.execDate AS SLUCH_DATE_1,
            Event.execDate AS SLUCH_DATE_2,
            EventResult.regionalCode AS SLUCH_RSLT,
            IF(rbDiagnosticResult.regionalCode IS NULL,
                EventResult.regionalCode,
                rbDiagnosticResult.regionalCode) AS SLUCH_ISHOD,
            Diagnosis.MKB AS SLUCH_DS1,
            EmergencyCall.numberCardCall AS SLUCH_NHISTORY,
            rbMedicalAidKind.regionalCode AS SLUCH_VIDPOM,
            CONCAT('510', IF(RelegateOrg.id IS NOT NULL,
                RelegateOrg.smoCode, AttachOrg.smoCode)) AS SLUCH_NPR_MO,
            rbSpeciality.federalCode AS SLUCH_PRVS,
            Person.regionalCode AS SLUCH_IDDOKT,
            Account_Item.`sum` AS SLUCH_TARIF,
            Account_Item.`sum` AS SLUCH_SUMV,
            Diagnosis.MKB AS USL_DS,
            Account_Item.`sum` AS USL_TARIF,
            Account_Item.`sum` AS USL_SUMV_USL,
            rbSpeciality.federalCode AS USL_PRVS,
            Person.regionalCode AS USL_CODE_MD,
            Event.execDate AS USL_DATE_IN,
            Event.execDate AS USL_DATE_OUT,
            Event.client_id AS PERS_ID_PAC,
            Client.firstName AS PERS_IM,
            Client.patrName AS PERS_OT,
            Client.lastName AS PERS_FAM,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            Client.birthPlace AS PERS_MR,
            rbDocumentType.regionalCode AS PERS_DOCTYPE,
            ClientDocument.serial AS PERS_DOCSER,
            ClientDocument.number AS PERS_DOCNUM,
            Client.SNILS AS PERS_SNILS,
            RegKLADR.OCATD AS PERS_OKATOG,
            LocKLADR.OCATD AS PERS_OKATOP,
            Account_Item.`sum` AS SUM_USL_SUMV_USL,
            AttachOrg.smoCode AS SLUCH_MASTER,
            rbSpeciality.usishCode AS USL_SPEC,
            Event.client_id AS PACIENT_ID_PAC,
            ClientPolicy.number AS PACIENT_NPOLIS,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            Insurer.miacCode AS PACIENT_SMO,
            age(Client.id,Event.execDate) AS clientAge
            FROM Account_Item
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN ClientAddress ClientRegAddress ON ClientRegAddress.client_id = Client.id AND
                      ClientRegAddress.id = (SELECT MAX(CRA.id)
                                         FROM   ClientAddress AS CRA
                                         WHERE  CRA.type = 0 AND CRA.client_id = Client.id AND CRA.deleted=0)
            LEFT JOIN ClientAddress ClientLocAddress ON ClientLocAddress.client_id = Client.id AND
                      ClientLocAddress.id = (SELECT MAX(CLA.id)
                                         FROM   ClientAddress AS CLA
                                         WHERE  CLA.type = 1 AND CLA.client_id = Client.id AND CLA.deleted=0)
            LEFT JOIN Address   RegAddress ON RegAddress.id = ClientRegAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN kladr.KLADR AS RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN Address   LocAddress ON LocAddress.id = ClientLocAddress.address_id
            LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
            LEFT JOIN kladr.KLADR AS LocKLADR ON LocKLADR.CODE = LocAddressHouse.KLADRCode
            LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                      AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                      AND Diagnostic.deleted = 0 )
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Account_Item.event_id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
            LEFT JOIN Organisation AS RelegateOrg
                ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN ClientAttach ON ClientAttach.id = getClientAttachIdForDate(Client.`id`, 0, Event.execDate)
            LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
                WHERE rs.master_id = rbItemService.id AND rs.speciality_id = Person.speciality_id)
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        """ % self.tableAccountItem['id'].inlist(self.idList)

        return self.db.query(stmt)


# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CAbstractExportPage2.__init__(self, parent, 'Export%s' % prefix)


    def saveExportResults(self):
        fileList = (self._parent.getXmlFileName(),
                    self._parent.getPersonalDataXmlFileName(),
                    self._parent.getRegionalDataXmlFileName())

        return self.moveFiles(fileList)

# ******************************************************************************

class XmlStreamWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'NPOLIS', 'SMO', 'SMO_OK', 'NOVOR')

    eventDateFields = ('DATE_1', 'DATE_2')

    eventFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO', 'EXTR',
        'LPU', 'LPU_1', 'PODR', 'PROFIL', )+  eventDateFields + ('DET',
        'NHISTORY',  'P_OTK', 'DS1', 'RSLT', 'ISHOD', 'PRVS', 'IDDOKT',
        'OS_SLUCH', 'IDSP', 'ED_COL', 'TARIF', 'SUMV')

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = ('IDSERV', 'LPU', 'PROFIL',
        'DET', 'DS', 'TARIF', 'SUMV_USL', 'PRVS', 'CODE_MD') + serviceDateFields

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        params['SLUCH_IDCASE'] = 0
        params['USL_LPU'] = params['lpuCode']
        params['SLUCH_LPU'] = u'510%s' % params['lpuCode']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', u'510%s' % params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', forceString(params['accNumber']))
        self.writeTextElement('DSCHET', settleDate.toString(Qt.ISODate))
        self.writeTextElement('PLAT', u'510%s' % params['payerCode'])
        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeTextElement('SUMMAP', '0.00')
        self.writeTextElement('SANK_MEK', '0.00')
        self.writeTextElement('SANK_MEE', '0.00')
        self.writeTextElement('SANK_EKMP', '0.00')
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('lastClientId'):
            if params['lastClientId']:
                self.writeEndElement() # SLUCH
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['rowNumber']))
            self.writeTextElement('PR_NOV', '0')
            self.writeClientInfo(record, params)

            params['rowNumber'] += 1
            params['lastClientId'] = clientId
            params['lastEventId'] = None

        self.writeEventInfo(record, params)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        sex = forceString(record.value('PERS_W'))
        birthDate = forceDate(record.value('PERS_DR'))
        age = forceInt(record.value('clientAge'))

        local_params = {
            'PACIENT_NOVOR':  '0' if age > 0 else  '%s%s0' % (sex[:1],
                birthDate.toString('ddMMyy')),
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, True)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        mkb = forceString(record.value('SLUCH_DS0'))

        specialCase = []
        multipleBirth = self._parent.getActionPropertyText(eventId,
           self._parent.actionTypeMultipleBirth, u'Признак')
        #«1» -  медицинская помощь, оказанная новорожденному
        #при  многоплодных родах.
        if multipleBirth:
            specialCase.append('1')

        if (not forceString(record.value('PERS_OT')) or
            not forceString(record.value('PERS_IM'))):
            specialCase.append('2')

        local_params = {
            'SLUCH_FOR_POM' : 3 if mkb in ('Z71.9', 'Z75.1') else 1,
            'SLUCH_OS_SLUCH': ''.join(specialCase)
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, True)

        if eventId != params.setdefault('lastEventId'):
            params['SLUCH_IDCASE'] += 1

            if params['lastEventId']:
                self.writeEndElement() # SLUCH

            self.writeGroup('SLUCH', self.eventFields, _record,
                            closeGroup=False, dateFields=self.eventDateFields)
            params['lastEventId'] = eventId


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params['lastEventId']:
            self.writeEndElement() # SLUCH
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


# ******************************************************************************

class PersonalDataWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'FAM', 'IM', 'OT', 'W', 'DR', 'MR', 'DOCTYPE',
        'DOCSER', 'DOCNUM', 'SNILS', 'OKATOG', 'OKATOP')

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        self.writeStartElement('PERS_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['personalDataFileName'][:-4])
        self.writeTextElement('FILENAME1', params['fileName'][:-4])
        self.writeEndElement() # ZGLV


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('persLastClientId'):
            local_params = {}
            _record = CExtendedRecord(record, local_params, True)
            self.writeClientInfo(_record)
            params['persLastClientId'] = clientId


    def writeClientInfo(self, record):
        u"""Пишет информацию о пациенте"""
        self.writeGroup('PERS', self.clientFields, record)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        self.writeEndElement() # PERS_LIST

# ******************************************************************************

class RegionalDataWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    eventFields = ('IDCASE', 'COUNT', 'MASTER', 'TOWN_HOSP')
    eventSumFields = ('SUMV', 'VID_FIN')
    serviceFields = ('IDSERV', 'SPEC')
    serviceSumFields = ('SUMV_USL', 'VID_FIN')

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        self.writeStartElement('REG_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['personalDataFileName'][:-4])
        self.writeTextElement('FILENAME1', params['fileName'][:-4])
        self.writeStartElement('SUMMA')
        self.writeTextElement('SUMMAV', u'%.2f' % params['accSum'])
        self.writeTextElement('VID_FIN', '1')
        self.writeEndElement() # SUMMA
        self.writeEndElement() # ZGLV


    def writeRecord(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))

        if eventId != params.setdefault('regionalLastEventId'):
            params['SUM_SUMV'] = params['mapEventIdToSum'].get(eventId)

        _record = CExtendedRecord(record, params, True)

        if eventId != params.setdefault('regionalLastEventId'):
            if params['regionalLastEventId']:
                self.writeEndElement() # SLUCH

            params['SLUCH_IDCASE'] += 1
            self.writeGroup('SLUCH', self.eventFields, _record,
                closeGroup=False)
            params['regionalLastEventId'] = eventId
            self.writeGroup('SUM', self.eventSumFields, _record)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params['regionalLastEventId']:
                self.writeEndElement() # SLUCH

        self.writeEndElement() # REG_LIST

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51EmergencyXml, u'17_ОМС-46',
                      'Kuznetcova_MSCH118.ini')
