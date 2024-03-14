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

u"""Экспорт реестра сведениями об оказанной медицинской помощи по
диспансеризации, медицинским осмотрам несовершеннолетних и
профилактических медицинским осмотрам взрослого населения.Тверь"""

import os.path
import shutil

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, Qt

from library.Utils     import (forceBool, forceRef,
    forceString, toVariant, forceStringEx, forceInt, forceDouble)
from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
    CAbstractExportPage1Xml, CAbstractExportPage2)

from Exchange.Ui_ExportR51HospitalPage1 import Ui_ExportPage1


def exportR69DD(widget, accountId, accountItemIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard('R69DD', widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportPage1(CAbstractExportPage1Xml, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    exportTypeDD1 = 0
    exportTypeDD2 = 1
    exportTypePO = 2
    exportTypeDSS = 3
    exportTypeDS = 4
    exportTypeMON = 5
    exportTypePMON = 6
    exportTypePerMON = 7

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self), ClientInfoXmlStreamWriter(self))
        CAbstractExportPage1Xml.__init__(self, parent, xmlWriter)
        CExportHelperMixin.__init__(self)

        self.prefix = prefix
        self.ignoreErrors = False

        self.cmbExportFormat.setVisible(False)
        self.lblExportFormat.setVisible(False)

        self.cmbExportType.clear()
        self.cmbExportType.addItem(u'ДД 1ый этап', self.exportTypeDD1)
        self.cmbExportType.addItem(u'ДД 2ой этап', self.exportTypeDD2)
        self.cmbExportType.addItem(u'Проф. осмотры', self.exportTypePO)
        self.cmbExportType.addItem(u'Дети-сироты стационар', self.exportTypeDSS)
        self.cmbExportType.addItem(u'Дети-сироты', self.exportTypeDS)
        self.cmbExportType.addItem(u'МО несовершеннолетних', self.exportTypeMON)
        self.cmbExportType.addItem(u'Предварительные МО несовершеннолетних',
                                   self.exportTypePMON)
        self.cmbExportType.addItem(u'Периодические МО несовершеннолетних',
                                   self.exportTypePerMON)

        self.lblPacketCounter = QtGui.QLabel(self)
        self.lblPacketCounter.setObjectName('lblPacketCounter')
        self.gridlayout.addWidget(self.lblPacketCounter, 2, 0, 1, 1)
        self.lblPacketCounter.setText(u'Номер пакета')

        self.edtPacketNumber = QtGui.QSpinBox(self)
        self.edtPacketNumber.setObjectName('edtPacketNumber')
        self.gridlayout.addWidget(self.edtPacketNumber, 2, 1, 1, 2)

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(forceBool(prefs.get('Export%sVerboseLog' % prefix, False)))
        self.chkIgnoreErrors.setChecked(forceBool(prefs.get('Export%sIgnoreErrors' % prefix, False)))
        self.edtPacketNumber.setValue(forceInt(prefs.get('Export%sPacketNumber' % prefix, 1)))


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.cmbExportType.setEnabled(not flag)
        self.lblExportType.setEnabled(not flag)

        if hasattr(self, 'lblPacketCounter'):
            self.lblPacketCounter.setEnabled(not flag)

        if hasattr(self, 'edtPacketNumber'):
            self.edtPacketNumber.setEnabled(not flag)


    def validatePage(self):
        QtGui.qApp.preferences.appPrefs['Export%sIgnoreErrors' % self.prefix] =\
            toVariant(self.chkIgnoreErrors.isChecked())
        QtGui.qApp.preferences.appPrefs['Export%sVerboseLog' % self.prefix] =\
            toVariant(self.chkVerboseLog.isChecked())
        QtGui.qApp.preferences.appPrefs['Export%sPacketNumber' % self.prefix] =\
            toVariant(self.edtPacketNumber.value()+1)
        return CAbstractExportPage1Xml.validatePage(self)

# ******************************************************************************

    def exportInt(self):
        tableOrganisation = self.db.table('Organisation')
        params = {}

        self.ignoreErrors = self.chkIgnoreErrors.isChecked()

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuOKPO'] = forceString(self.db.translate(
            tableOrganisation, 'id', lpuId, 'OKPO'))
        params['lpuCode'] = forceString(self.db.translate(
            tableOrganisation, 'id', lpuId, 'infisCode'))
        self.log(u'ЛПУ: ОКПО "%s", код инфис: "%s".' % (
            params['lpuOKPO'], params['lpuCode']))

        if not params['lpuCode']:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан код инфис', True)
            if not self.ignoreErrors:
                self.abort()
                return

        params.update(self.accountInfo())

        params['payerInfis'] = forceString(self.db.translate(
            tableOrganisation, 'id', params['payerId'], 'infisCode'))
        params['rowNumber'] = 0
        params['fileName'] = self._parent.getXmlFileName()
        params['clientInfofileName'] = self._parent.getXmlClientInfoFileName()
        params['mapEventIdToSum'] = self.getEventSum()

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)

        clientInfoFile = QFile(self._parent.getFullXmlClientInfoFileName())
        clientInfoFile.open(QFile.WriteOnly | QFile.Text)

        (eventInfoWriter, clientInfoWriter) = self.xmlWriter()
        eventInfoWriter.setDevice(outFile)
        clientInfoWriter.setDevice(clientInfoFile)

        self.setProcessParams(params)
        CAbstractExportPage1Xml.exportInt(self)

# ******************************************************************************

    def createQuery(self):
        tableAccountItem = self.db.table('Account_Item')

        stmt = """SELECT Event.client_id AS PACIENT_ID_PAC,
                ClientPolicy.serial AS PACIENT_SPOLIS,
                ClientPolicy.number AS PACIENT_NPOLIS,
                rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
                Insurer.OKATO AS PACIENT_ST_OKATO,
                Insurer.miacCode AS PACIENT_SMO,
                Insurer.OGRN AS PACIENT_SMO_OGRN,
                Insurer.OKATO AS PACIENT_SMO_OK,
                Insurer.shortName AS PACIENT_SMO_NAM,
                Event.id AS SLUCH_NHISTORY,
                Event.setDate AS SLUCH_DATE_1,
                Event.execDate AS SLUCH_DATE_2,
                Diagnosis.MKB AS SLUCH_DS1,
                EventResult.regionalCode AS SLUCH_RSLT_D,
                rbMedicalAidUnit.code AS SLUCH_IDSP,
                IF (ServiceProfileMedicalAidKind.id IS NOT NULL,
                    ServiceProfileMedicalAidKind.regionalCode,
                    IF (ServiceMedicalAidKind.id IS NOT NULL,
                        ServiceMedicalAidKind.regionalCode,
                            rbMedicalAidKind.regionalCode)) AS SLUCH_VIDPOM,
                '1' AS USL_SMODE,
                Event.setDate AS USL_DATE_IN,
                Event.execDate AS USL_DATE_OUT,
                Account_Item.`sum` AS USL_SUMV_USL,
                IF(Event.execPerson_id IS NOT NULL, rbSpeciality.regionalCode,
                    SetSpeciality.regionalCode) AS USL_PRVS,
                IF(Event.execPerson_id IS NOT NULL, Person.regionalCode,
                    SetPerson.regionalCode) AS USL_CODE_MD,
                Client.id AS PERS_ID_PAC,
                Client.lastName AS PERS_FAM,
                Client.firstName AS PERS_IM,
                Client.patrName AS PERS_OT,
                Client.sex AS PERS_W,
                Client.birthDate AS PERS_DR,
                Client.birthPlace AS PERS_MR,
                rbDocumentType.regionalCode AS PERS_DOCTYPE,
                ClientDocument.serial AS PERS_DOCSER,
                ClientDocument.number AS PERS_DOCNUM,
                Client.SNILS AS PERS_SNILS,
                RegKLADR.OCATD AS PERS_OKATOG,
                LocKLADR.OCATD AS PERS_OKATOP
            FROM Account_Item
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
                      ClientPolicy.id = (SELECT MAX(CP.id)
                                         FROM   ClientPolicy AS CP
                                         LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
                                         WHERE  CP.client_id = Client.id AND CP.deleted=0 AND CPT.code IN ('1','2'))
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                      AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('1', '2'))
                                      AND Diagnostic.person_id = Event.execPerson_id AND Diagnostic.deleted = 0)
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbPayRefuseType
                ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbMedicalAidUnit ON Account_Item.unit_id = rbMedicalAidUnit.id
            LEFT JOIN Person ON Event.execPerson_id = Person.id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN Person AS SetPerson ON Event.setPerson_id = SetPerson.id
            LEFT JOIN EventType ON Event.eventType_id  = EventType.id
            LEFT JOIN rbSpeciality AS SetSpeciality ON SetPerson.speciality_id = SetSpeciality.id
            LEFT JOIN rbService ON rbService.id = Account_Item.service_id
            LEFT JOIN rbService_Profile
                ON rbService_Profile.master_id = rbService.id
                AND rbService_Profile.speciality_id = Person.speciality_id
            LEFT JOIN rbMedicalAidKind AS ServiceProfileMedicalAidKind
                ON ServiceProfileMedicalAidKind.id = rbService_Profile.medicalAidKind_id
            LEFT JOIN rbMedicalAidKind AS ServiceMedicalAidKind
                ON ServiceMedicalAidKind.id = rbService.medicalAidKind_id
            LEFT JOIN rbMedicalAidKind
                ON rbMedicalAidKind.id = EventType.medicalAidKind_id
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
            LEFT JOIN Address   LocAddress ON LocAddress.id = ClientLocAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
            LEFT JOIN kladr.KLADR RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN kladr.KLADR LocKLADR ON LocKLADR.CODE = LocAddressHouse.KLADRCode
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
            ORDER BY Event.client_id, Event.id
        """ % tableAccountItem['id'].inlist(self.idList)
        query = self.db.query(stmt)
        return query


    def getEventSum(self):
        u"""возвращает общую стоимость услуг за событие"""

        stmt = """SELECT Account_Item.event_id,
            SUM(Account_Item.sum) AS totalPrice
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('event_id'))
            _sum = forceDouble(record.value('totalPrice'))
            result[eventId] = _sum

        return result

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CAbstractExportPage2.__init__(self, parent, 'Export%s' % prefix)


    def saveExportResults(self):
        fileList = [self._parent.getXmlFileName(),
                    self._parent.getXmlClientInfoFileName()]

        for src in fileList:
            srcFullName = os.path.join(forceStringEx(self.getTmpDir()),
                                                    os.path.basename(src))
            dst = os.path.join(forceStringEx(self.edtDir.text()),
                                                    os.path.basename(src))
            success, _ = QtGui.qApp.call(self, shutil.move,
                                              (srcFullName, dst))

            if not success:
                break

        return success

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта в ОМС Мурманской области (стационар)"""

    mapExportTypeToPrefix = {
        CExportPage1.exportTypeDD1: 'DP',
        CExportPage1.exportTypeDD2: 'DV',
        CExportPage1.exportTypePO: 'DO',
        CExportPage1.exportTypeDSS: 'DS',
        CExportPage1.exportTypeDS: 'DU',
        CExportPage1.exportTypeMON: 'DF',
        CExportPage1.exportTypePMON: 'DD',
        CExportPage1.exportTypePerMON: 'DR',
    }

    def __init__(self, prefix, parent=None):
        title = u'Мастер экспорта в ОМС Тверской области, ДД'
        CAbstractExportWizard.__init__(self, parent, title)
        self.prefix = prefix

        self.page1 = CExportPage1(self, prefix)
        self.page2 = CExportPage2(self, prefix)
        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, self.prefix)


    def getXmlFileName(self):
        u"""Возвращает имя файла для записи данных"""
        tableOrganisation = self.db.table('Organisation')
        info = self.info
        exportType = forceInt(self.page1.cmbExportType.itemData(
                           self.page1.cmbExportType.currentIndex()))
        prefix = self.mapExportTypeToPrefix.get(exportType, '')

        lpuCode = forceString(self.db.translate(
            tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
        payerCode = forceString(self.db.translate(
            tableOrganisation, 'id', info['payerId'], 'infisCode'))
        year = info['settleDate'].year() %100
        month = info['settleDate'].month()
        packetNumber = self.page1.edtPacketNumber.value()

        result = u'%s%sS%s%02d%02d%d.xml' % (prefix, lpuCode, payerCode, year,
            month, packetNumber)
        return result


    def getXmlClientInfoFileName(self):
        return u'L%s' % self.getXmlFileName()


    def getFullXmlClientInfoFileName(self):
        u"""Возвращает полное имя файла для записи сведений о пациентах.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getXmlClientInfoFileName())


    def getFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getXmlFileName())

# ******************************************************************************

class XmlStreamWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
        'SMO_OGRN', 'SMO_OK', 'SMO_NAM')

    eventDateFields = ('DATE_1', 'DATE_2')

    eventFields = ('IDCASE', 'VIDPOM',
       'LPU', 'NHISTORY', 'DS1', 'RSLT_D', 'IDSP',
        'SUMV') + eventDateFields

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = ('IDSERV', 'LPU', 'SMODE', 'LPU_D',
        'SUMV_USL', 'PRVS', 'CODE_MD') + serviceDateFields

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла, абстрактный метод"""
        settleDate = params['settleDate']
        params['SLUCH_IDCASE'] = 0
        params['USL_LPU'] = params['lpuCode']
        params['USL_LPU_D'] = params['lpuCode']
        params['SLUCH_LPU'] = params['lpuCode']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['fileName'])
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', forceString(params['accNumber']))
        self.writeTextElement('DSCHET', settleDate.toString(Qt.ISODate))
        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))

        if clientId != params.setdefault('lastClientId'):
            if params['lastClientId']:
                self.writeEndElement() # SLUCH
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['rowNumber']))
            self.writeTextElement('PR_NOV', '0')
            self.writeClientInfo(record)

            params['rowNumber'] += 1
            params['lastClientId'] = clientId
            params['lastEventId'] = None

        self.writeEventInfo(record, params)


    def writeClientInfo(self, record):
        u"""Пишет информацию о пациенте"""
        self.writeGroup('PACIENT', self.clientFields, record)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('SLUCH_NHISTORY'))

        if eventId != params.setdefault('lastEventId'):
            params['USL_IDSERV'] = 0
            params['SLUCH_SUMV'] = params['mapEventIdToSum'].get(eventId)

        local_params = {}
        local_params.update(params)

        _record = CExtendedRecord(record, local_params)

        if eventId != params.setdefault('lastEventId'):
            params['SLUCH_IDCASE'] += 1

            if params['lastEventId']:
                self.writeEndElement() # SLUCH

            self.writeGroup('SLUCH', self.eventFields, _record,
                            closeGroup=False, dateFields=self.eventDateFields)
            params['lastEventId'] = eventId
            params['USL_IDSERV'] = 0

        self.writeGroup('USL', self.serviceFields, _record,
                        dateFields=self.serviceDateFields)
        params['USL_IDSERV'] += 1


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params['lastEventId']:
            self.writeEndElement() # SLUCH
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST

# ******************************************************************************

class ClientInfoXmlStreamWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись информации о пациентах в XML"""

    clientDateFields = ('DR', 'DR_P')

    clientFields = ('ID_PAC', 'FAM', 'IM', 'OT', 'W', 'FAM_P',
        'IM_P', 'OT_P', 'W_P', 'MR', 'DOCTYPE', 'DOCSER',
        'DOCNUM', 'SNILS', 'OKATOG', 'OKATOP') + clientDateFields


    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла, абстрактный метод"""
        settleDate = params['settleDate']
        params['SLUCH_IDCASE'] = 0
        params['USL_LPU'] = params['lpuCode']
        params['SLUCH_LPU'] = params['lpuCode']
        self.writeStartElement('PERS_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['clientInfofileName'])
        self.writeTextElement('FILENAME1', params['fileName'])
        self.writeEndElement() # ZGLV


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        self.writeEndElement() # PERS_LIST


    def writeClientInfo(self, record):
        u"""Пишет информацию о пациенте"""
        self.writeGroup('PERS', self.clientFields, record,
                        dateFields=self.clientDateFields)


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))

        if clientId not in params.setdefault('exportedClients', set()):
            representativeInfo = self._parent.getClientRepresentativeInfo(clientId)
            params['FAM_P'] = representativeInfo.get('lastName')
            params['IM_P'] = representativeInfo.get('firstName')
            params['OT_P'] = representativeInfo.get('patrName')
            params['W_P'] = representativeInfo.get('sex')
            params['DR_P'] = representativeInfo.get('birthDate')
            self.writeClientInfo(record)
            params['exportedClients'].add(clientId)
