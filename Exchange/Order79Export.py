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

u"""Экспорт реестра  в по 79 приказу, общая часть"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, Qt, pyqtSignature, QTextCodec, QRegExp, QDate

from library.Utils import (forceBool, forceInt, toVariant, forceString,
                           forceRef, forceDate, formatSNILS)
from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
                             CAbstractExportPage1Xml, CAbstractExportPage2)
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Utils import compressFileInZip

# выводит в консоль имена невыгруженных полей
DEBUG = False

# ******************************************************************************

class COrder79ExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта счетов по 79 приказу"""

    def __init__(self, title, prefix, exportPage1, exportPage2, parent=None):
        self.prefix = prefix
        CAbstractExportWizard.__init__(self, parent, title)
        self.page1 = exportPage1(self, self.prefix)
        self.page2 = exportPage2(self, self.prefix)

        self.addPage(self.page1)
        self.addPage(self.page2)

        self.__xmlBaseFileName = None
        self.note = None
        self.startDate = None


    def clearCache(self):
        u"""Очищает кешированные значения переменных"""
        self.__xmlBaseFileName = None


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, self.prefix)


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""

        def getPrefix(infisCode, isInsurer):
            u"""Возвращает префиксы по коду инфис и признаку страховой"""
            result = ''

            if infisCode == '08':
                result = 'T'
            else:
                result = 'S' if isInsurer else 'M'

            return result

        if self.__xmlBaseFileName:
            result = self.__xmlBaseFileName
        else:
            tableOrganisation = self.db.table('Organisation')
            tableContract = self.db.table('Contract')
            info = self.info

            payerCode = forceString(self.db.translate(
                tableOrganisation, 'id', info['payerId'], 'infisCode'))
            payerIsInsurer = forceString(self.db.translate(
                tableOrganisation, 'id', info['payerId'], 'isInsurer'))
            recipientId = forceString(
                self.db.translate(tableContract, 'id', info['contractId'],
                                  'recipient_id'))
            recipientCode = forceString(
                self.db.translate(tableOrganisation, 'id',
                                  QtGui.qApp.currentOrgId(), 'miacCode'))
            recipientIsInsurer = forceBool(
                self.db.translate(tableOrganisation, 'id', recipientId,
                                  'isInsurer'))

            year = info['settleDate'].year() %100
            month = info['settleDate'].month()
            packetNumber = self.page1.edtPacketNumber.value()
            registryType = self.page1.cmbRegistryType.currentIndex()

            p_i = ''
            p_p = ''

            if registryType == COrder79ExportPage1.registryTypeFlk:
                p_i = 'M'
                p_p = 'T'
            elif registryType == COrder79ExportPage1.registryTypePayment:
                p_i = getPrefix(recipientCode, recipientIsInsurer)
                p_p = getPrefix(payerCode, payerIsInsurer)

            postfix = u'%02d%02d%d' % (year, month,
                                       packetNumber) if addPostfix else u''
            result = u'%s%s%s%s_%s.xml' % (
                p_i, recipientCode, p_p, '61', postfix)
            self.__xmlBaseFileName = result

        return result


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return u'H%s' % self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L%s' % self._getXmlBaseFileName(addPostfix)


    def getPersonalDataFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getPersonalDataXmlFileName())


    def getFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getXmlFileName())


    def getZipFileName(self):
        u"""Возвращает имя архива: первые 5 знаков из Organisation.infisCode
        +NN(месяц, например 06 - июнь) заархивировать в формате ZIP"""
        tableOrganisation = self.db.table('Organisation')
        code = forceString(
            self.db.translate(tableOrganisation, 'id',
                              QtGui.qApp.currentOrgId(), 'infisCode'))[:5]
        month = self.info['settleDate'].month()
        return u'%s%02d.zip' % (code, month)


    def getFullZipFileName(self):
        u"""Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getZipFileName())


    def setAccountNote(self):
        u"""Замещает примечание к счету на переменную NSCHET"""
        accountRecord = self.db.table('Account').newRecord(['id', 'note'])
        accountRecord.setValue('id', toVariant(self.accountId))
        accountRecord.setValue('note', toVariant(self.note))
        self.db.updateRecord('Account', accountRecord)


# ******************************************************************************

class COrder79ExportPage1(CAbstractExportPage1Xml, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    registryTypeFlk = 0
    registryTypePayment = 1

    def __init__(self, parent, prefix, xmlWriter):
        CAbstractExportPage1Xml.__init__(self, parent, xmlWriter)
        CExportHelperMixin.__init__(self)
        self.prefix = prefix

        self.exportedActionsList = None
        self.ignoreErrors = False

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(forceBool(prefs.get(
            'Export%sVerboseLog' % prefix, False)))
        self.chkIgnoreErrors.setChecked(forceBool(prefs.get(
            'Export%sIgnoreErrors' % prefix, False)))
        self.edtPacketNumber.setValue(forceInt(prefs.get(
            'Export%sPacketNumber' % prefix, 1)))


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
            'SUM_VID_FIN': '1',
            'SUM_USL_VID_FIN': '1',
            'SLUCH_TOWN_HOSP': '047',
            'SLUCH_P_OTK': '0',
            'PACIENT_SMO_OK': '47000',
        }
        params.update(self.processParams())

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuShortName'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'shortName'))
        params['lpuChief'] = self._getChiefName(lpuId)
        params['lpuAccountant'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'accountant'))
        params['lpuMiacCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'miacCode'))
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
            params['mapEventIdToFksgCode'] = self.getFksgCode()
            params['SLUCH_COUNT'] = params['accNumber']

            registryType = self.cmbRegistryType.currentIndex()
            params['NSCHET'] = self.nschet(registryType, params)
            self._parent.note = u'[NSCHET:%s]' % params['NSCHET']

        params['N_ZAP'] = 1
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getPersonalDataXmlFileName(False))
        params['visitExportedEventList'] = set()
        params['toggleFlag'] = 0
        params['doneVis'] = set()

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        CAbstractExportPage1Xml.exportInt(self)


    def getFksgCode(self):
        u"""Формирует словарь кодов КСГ по идентификатору события"""
        stmt = u"""SELECT Account_Item.event_id,
            GROUP_CONCAT(DISTINCT rbService.code SEPARATOR ';')
        FROM Account_Item
        LEFT JOIN rbService ON rbService.id = Account_Item.service_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id =
            Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL OR
                (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
            AND rbService.code NOT LIKE 'A%%'
            AND rbService.code NOT LIKE 'B%%'
            AND %s
        GROUP BY Account_Item.event_id""" % (
            self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            result[eventId] = forceString(record.value(1))

        return result


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
            payerCodePart = forceInt(params['payerCode'][-2:]) if (
                registryType == self.registryTypePayment) else 10
            result = u'%2d%02d%s' % (payerCodePart,
                                     params['settleDate'].month(),
                                     params['accNumber'][-1:])
            result = u'%s1' % result[:-1]

        return result


    @pyqtSignature('int')
    def on_edtPacketNumber_valueChanged(self, _):
        u"""Сбрасывает кэшированное имя файла вывода при изменении
            номера пакета"""
        self._parent.clearCache()


# ******************************************************************************

class COrder79ExportPage2(CAbstractExportPage2):
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
            self.wizard().setAccountNote()
        return success

# ******************************************************************************

class COrder79XmlStreamWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    # version = '2.1'

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'SMO', 'SMO_OGRN',
                    'SMO_OK', 'SMO_NAM', 'NOVOR', 'STAT_Z')

    eventDateFields1 = ('DATE_1', 'DATE_2')
    eventDateFields2 = ('NAPDAT',  )
    eventDateFields = eventDateFields1 + eventDateFields2

    eventFields = (('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'VID_HMP',
                    'METOD_HMP', 'TAL_D', 'TAL_P', 'NPR_MO', 'EXTR', 'PODR',
                    'LPU', 'PROFIL', 'DET', 'NHISTORY', 'P_PER')
                   + eventDateFields1 +
                   ('DS1', 'DS2', 'RSLT', 'ISHOD', 'PRVS',
                    'VERS_SPEC', 'IDDOKT', 'OS_SLUCH', 'IDSP', 'SUMV', 'OPLATA',
                    'NSVOD', 'KODLPU', 'PRNES', 'BOLDN', 'PCHAST', 'PRZAB',
                    'SHDZOS', 'NAPUCH', 'NOM_NAP')
                   + eventDateFields2 +
                   ('CODE_FKSG',  ))

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = (('IDSERV', 'IDMASTER', 'LPU', 'PODR', 'PROFIL', 'DET')
                     + serviceDateFields +
                     ('DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL',
                      'SL_KOEF', 'SK_KOEF', 'PRVS', 'CODE_MD', 'KODLPU', 'KSGA',
                      'KTLPU', 'PKUR', 'CODE_OPER'))

    serviceSubGroup = {
        'SL_KOEF' : {'fields': ('IDSL', 'Z_SL')}
    }

    mapEventOrderToForPom = {'1': '3', '6': '2', '2': '1'}
    mapSocStatusCode = {u'001': '1', u'с02': '2', u'003': '3', u'004': '4',
                        u'с05': '5', u'с07': '6', u'с06': '7', u'008': '8'}

    def __init__(self, parent, version='2.1'):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        self.setCodec(QTextCodec.codecForName('cp1251'))
        self.startDate = None
        self.version = version


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


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        raise NotImplementedError


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        raise NotImplementedError


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        sex = forceString(record.value('PERS_W'))
        birthDate = forceDate(record.value('PERS_DR'))
        socStatus = forceString(record.value('PACIENT_STAT_Z_raw'))
        execDate = forceDate(record.value('execDate'))
        isJustBorn = birthDate.daysTo(execDate) < 28
        isAnyBirthDoc = forceString(record.value('PERS_DOCSER')) or forceString(
            record.value('PERS_DOCNUM'))
        statZ = self.mapSocStatusCode.get(socStatus, '')

        local_params = {
            'PACIENT_NOVOR':  (('%s%s1' % (sex[:1], birthDate.toString('ddMMyy')
                                          )) if isJustBorn and not isAnyBirthDoc
                               else '0'),
            'PACIENT_STAT_Z': statZ,
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        raise NotImplementedError


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            self.writeEndElement() # SLUCH
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def writeElement(self, elementName, value=None):
        if value:
            if isinstance(value, QDate):
                self.writeTextElement(elementName, forceDate(value).toString(Qt.ISODate))
            else:
                self.writeTextElement(elementName, value)

# ******************************************************************************

class COrder79v3XmlStreamWriter(CAbstractExportXmlStreamWriter):
    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        self._lastCompleteEventId = None
        self._lastEventId = None
        self._lastRecord = None
        self._lastClientId = None


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        self._lastCompleteEventId = None
        self._lastEventId = None
        self._lastRecord = None
        self._lastClientId = None


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""

        if self._lastEventId:
            if self._lastRecord:
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                self._lastRecord,
                                closeGroup=True,
                                openGroup=False)
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        self.writeCompleteEvent(record, params)
        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))

        if lastEventId == self._lastCompleteEventId:
            return

        if self._lastEventId:
            self.writeEndElement() # SL
            self.writeGroup('Z_SL', self.completeEventFields2,
                            self._lastRecord,
                            closeGroup=True, openGroup=False)
            self._lastEventId = None

        lastEventId = forceRef(record.value('lastEventId'))
        self.writeGroup('Z_SL', self.completeEventFields1, record,
                        closeGroup=False,
                        dateFields=self.completeEventDateFields)
        self._lastCompleteEventId = forceRef(record.value('lastEventId'))
        self._lastRecord = record


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        pass


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        pass


    def writeTextElement(self, elementName, value=None):
        u"""Если тег в списке обязательных, выгружаем его пустым"""
        if value or (elementName in self.requiredFields):
            COrder79XmlStreamWriter.writeTextElement(self, elementName, value)

# ******************************************************************************

class COrder79PersonalDataWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    # version = '2.1'
    clientDateFields = ('DR', )
    clientFields = (('ID_PAC', 'FAM', 'IM', 'OT', 'W',)
                    + clientDateFields +
                    ('DOST', 'FAM_P', 'IM_P', 'OT_P', 'W_P', 'MR', 'DOCTYPE',
                     'DOCSER', 'DOCNUM', 'SNILS', 'OKATOG', 'OKATOP',
                     'ADRES', 'KLADR', 'DOM', 'KVART', 'KORP'))
    EVENT_EXEC_DATE_FIELD_NAME = 'SLUCH_DATE_2'

    def __init__(self, parent, version='2.1'):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        self.setCodec(QTextCodec.codecForName('cp1251'))
        self.version = version
        self._lastClientId = None


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        self.writeStartElement('PERS_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', self.version)
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['personalDataFileName'][:-4])
        self.writeTextElement('FILENAME1', params['fileName'][:-4])
        self.writeEndElement() # ZGLV
        self._lastClientId = None


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))

        if clientId != self._lastClientId:
            local_params = {}
            local_params.update(params)
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeClientInfo(_record, params)
            self._lastClientId = clientId


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        birthDate = forceDate(record.value('PERS_DR'))
        execDate = forceDate(record.value(self.EVENT_EXEC_DATE_FIELD_NAME))
        isJustBorn = birthDate.daysTo(execDate) < 28 and execDate.isValid()
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        nameProblems = []

        patrName = forceString(record.value('PERS_OT'))
        if not patrName or patrName.upper() == u'НЕТ':
            nameProblems.append('1')

        lastName = forceString(record.value('PERS_FAM'))
        if not lastName or lastName.upper() == u'НЕТ':
            nameProblems.append('2')

        firstName = forceString(record.value('PERS_IM'))
        if not firstName or firstName.upper() == u'НЕТ':
            nameProblems.append('3')

        local_params = {
            'PERS_DOST' : nameProblems if nameProblems else None,
        }

        hasBirthCert = forceString(record.value('PERS_DOCTYPE')) == '3'
        hasPolicy = forceString(record.value('PACIENT_NPOLIS')) != ''

        if isJustBorn and not (hasBirthCert or hasPolicy):
            info = self._parent.getClientRepresentativeInfo(clientId)
            local_params['PERS_FAM_P'] = info.get('lastName', '')
            local_params['PERS_IM_P'] = info.get('firstName', '')
            local_params['PERS_OT_P'] = info.get('patrName', '')
            local_params['PERS_W_P'] = info.get('sex', '')
            local_params['PERS_DR_P'] = info.get('birthDate', QDate())

        local_params.update(params)
        local_params['PERS_SNILS'] = formatSNILS(forceString(
            record.value('PERS_SNILS_raw')))
        _record = CExtendedRecord(record, local_params, DEBUG)

        self.writeGroup('PERS', self.clientFields, _record,
                        dateFields=self.clientDateFields)


    def writeElement(self, elementName, value=None):
        if value:
            self.writeTextElement(elementName, value)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        self.writeEndElement() # PERS_LIST
