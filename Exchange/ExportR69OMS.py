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

u"""Экспорт реестра сведениями об оказанной медицинской помощи. Тверь"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, Qt

from library.Utils   import forceBool, forceRef, forceString, toVariant, forceInt
from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
    CAbstractExportPage1Xml, CAbstractExportPage2)

from Exchange.Ui_ExportR51HospitalPage1 import Ui_ExportPage1


def exportR69OMS(widget, accountId, accountItemIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard('R69OMS', widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта в ОМС Тверской области"""

    def __init__(self, prefix, parent=None):
        title = u'Мастер экспорта в ОМС Тверской области'
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

        lpuCode = forceString(self.db.translate(
            tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
        payerCode = forceString(self.db.translate(
            tableOrganisation, 'id', info['payerId'], 'infisCode'))
        year = info['settleDate'].year() %100
        month = info['settleDate'].month()
        packetNumber = self.page1.edtPacketNumber.value()

        result = u'HM%sS%s%02d%02d%d.xml' % (lpuCode, payerCode, year, month,
            packetNumber)
        return result


    def getFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getXmlFileName())

# ******************************************************************************

class CExportPage1(CAbstractExportPage1Xml, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        xmlWriter = XmlStreamWriter(self)
        CAbstractExportPage1Xml.__init__(self, parent, xmlWriter)
        CExportHelperMixin.__init__(self)

        self.prefix = prefix
        self.ignoreErrors = False

        self.cmbExportType.setVisible(False)
        self.cmbExportFormat.setVisible(False)
        self.lblExportType.setVisible(False)
        self.lblExportFormat.setVisible(False)

        self.lblPacketCounter = QtGui.QLabel(self)
        self.lblPacketCounter.setObjectName('lblPacketCounter')
        self.gridlayout.addWidget(self.lblPacketCounter, 1, 0, 1, 1)
        self.lblPacketCounter.setText(u'Номер пакета')

        self.edtPacketNumber = QtGui.QSpinBox(self)
        self.edtPacketNumber.setObjectName('edtPacketNumber')
        self.gridlayout.addWidget(self.edtPacketNumber, 1, 1, 1, 2)

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(forceBool(prefs.get('Export%sVerboseLog' % prefix, False)))
        self.chkIgnoreErrors.setChecked(forceBool(prefs.get('Export%sIgnoreErrors' % prefix, False)))
        self.edtPacketNumber.setValue(forceInt(prefs.get('Export%sPacketNumber' % prefix, 1)))


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)

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
        params['mapEventIdToSum'] = self.getEventSum()

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)

        self.setProcessParams(params)
        self.xmlWriter().setDevice(outFile)
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
                Insurer.shortName AS PACIENT_SMO_NAME,
                Client.birthWeight AS PACIENT_VNOV_D,
                EventType.regionalCode AS SLUCH_USL_OK,
                Event.order AS SLUCH_EXTR,
                IF (age(Client.id,Event.execDate) < 18, 1, 0) AS SLUCH_DET,
                Event.id AS SLUCH_NHISTORY,
                Event.setDate AS SLUCH_DATE_1,
                Event.execDate AS SLUCH_DATE_2,
                Diagnosis.MKB AS SLUCH_DS1,
                AccDiagnosis.MKB AS SLUCH_DS2,
                AccDiagnosis.MKB AS SLUCH_DS3,
                Client.birthWeight AS SLUCH_VNOV_M,
                EventResult.regionalCode AS SLUCH_RSLT,
                rbDiagnosticResult.regionalCode AS SLUCH_ISHOD,
                CuratorSpeciality.regionalCode AS SLUCH_PRVS,
                'V015' AS SLUCH_VERS_SPEC,
                Curator.regionalCode AS SLUCH_IDDOKT,
                rbMedicalAidUnit.code AS SLUCH_IDSP,
                Account_Item.amount AS SLUCH_ED_COL,
                IF (ServiceProfileMedicalAidProfile.id IS NOT NULL,
                    ServiceProfileMedicalAidProfile.code,
                        rbMedicalAidProfile.code) AS USL_PROFIL,
                IF (ServiceProfileMedicalAidProfile.id IS NOT NULL,
                    ServiceProfileMedicalAidProfile.regionalCode,
                        rbMedicalAidProfile.regionalCode) AS USL_PROFIL_T,
                IF (age(Client.id,Event.execDate) < 18, 1, 0) AS USL_DET,
                Event.setDate AS USL_DATE_IN,
                Event.execDate AS USL_DATE_OUT,
                Diagnosis.MKB AS USL_DS,
                rbService.infis AS USL_CODE_USL,
                IF (Account_Item.uet>0, Account_Item.uet,
                    Account_Item.amount) AS USL_KOL_USL,
                Account_Item.`sum` AS USL_SUMV_USL,
                IF(Event.execPerson_id IS NOT NULL, rbSpeciality.regionalCode,
                    SetSpeciality.regionalCode) AS USL_PRVS,
                IF(Event.execPerson_id IS NOT NULL, Person.regionalCode,
                    SetPerson.regionalCode) AS USL_CODE_MD
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN rbService ON rbService.id = Account_Item.service_id
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
            LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
             SELECT id FROM Diagnostic AS AD
             WHERE AD.event_id = Account_Item.event_id AND
                AD.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='9') AND
                AD.person_id = Event.execPerson_id AND
                AD.deleted = 0 LIMIT 1)
            LEFT JOIN Diagnosis AS AccDiagnosis ON
                AccDiagnosis.id = AccDiagnostic.diagnosis_id AND
                AccDiagnosis.deleted = 0
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
            LEFT JOIN rbPayRefuseType
                ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id =rbMedicalAidType.id
            LEFT JOIN Person AS Curator ON Curator.id = Event.curator_id
            LEFT JOIN rbSpeciality AS CuratorSpeciality ON Curator.speciality_id = CuratorSpeciality.id
            LEFT JOIN rbMedicalAidUnit ON Account_Item.unit_id = rbMedicalAidUnit.id
            LEFT JOIN Person ON Event.execPerson_id = Person.id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN Person AS SetPerson ON Event.setPerson_id = SetPerson.id
            LEFT JOIN rbSpeciality AS SetSpeciality ON SetPerson.speciality_id = SetSpeciality.id
            LEFT JOIN rbService_Profile
                ON rbService_Profile.master_id = rbService.id
                AND rbService_Profile.speciality_id = Person.speciality_id
            LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON
                ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
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

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CAbstractExportPage2.__init__(self, parent, 'Export%s' % prefix)


    def saveExportResults(self):
        fileList = [self._parent.getXmlFileName()]

        return self.moveFiles(fileList)

# ******************************************************************************

class XmlStreamWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
        'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR', 'VNOV_D')

    eventDateFields = ('DATE_1', 'DATE_2')

    eventFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM',
       'LPU', 'PROFIL_T', 'DET', 'NHISTORY', 'DS0', 'DS1', 'VNOV_M', 'RSLT',
       'ISHOD', 'PRVS', 'IDDOKT', 'IDSP', 'SUMV') + eventDateFields

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = ('IDSERV', 'LPU', 'PROFIL', 'PROFIL_T',
        'DET', 'DS', 'CODE_USL', 'KOL_USL',
        'SUMV_USL', 'PRVS', 'CODE_MD') + serviceDateFields

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла, абстрактный метод"""
        settleDate = params['settleDate']
        params['SLUCH_IDCASE'] = 0
        params['USL_LPU'] = params['lpuCode']
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


    def close(self):
        u"""Закрывает устройство при его наличии"""
        if self.device():
            self.device().close()
