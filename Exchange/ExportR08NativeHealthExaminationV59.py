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

u"""Экспорт реестра  в формате XML. Республика Калмыкия. ДД, (Д3) V59"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from library.Utils import (forceString, forceRef, toVariant, forceInt, forceBool)
from Exchange.Order79Export import COrder79ExportWizard
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.ExportR08Hospital import (CR08PersonalDataWriter as
                                        PersonalDataWriter)
from Exchange.ExportR08NativeHealthExamination import (
    CR08ExportPage1, R08XmlStreamWriter, formatAccNumber)
from Exchange.ExportR47D3 import CExportPage2, getEventTypeCode

def exportR08NativeHealthExaminationV59(widget, accountId, accountItemIdList,
                                        _):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Калмыкии"""

    mapPrefixToEventTypeCode = {u'ДВ1': 'DP', u'ДВ2': 'DV', u'ОПВ': 'DO',
                                u'ДС1': 'DS', u'ДС2': 'DU', u'ОН1': 'DF',
                                u'ОН2': 'DD', u'ОН3': 'DR'}

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии V59'
        prefix = 'R08D3V59'
        COrder79ExportWizard.__init__(self, title, prefix, CR08ExportPage1,
                                      CExportPage2, parent)

        self.page1.setXmlWriter((XmlStreamWriter(self.page1),
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

class CExportPage1(CR08ExportPage1):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CR08ExportPage1.__init__(self, parent, prefix)


    def prepareStmt(self, params):
        (select, tables, where, orderBy) = CR08ExportPage1.prepareStmt(
            self, params)
        select += """,
            rbDiseasePhases.code AS diseasePhaseCode
        """
        tables += """LEFT JOIN rbDiseasePhases ON
            rbDiseasePhases.id = Diagnostic.phase_id"""

        return (select, tables, where, orderBy)

# ******************************************************************************

class XmlStreamWriter(R08XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    eventFields1 = (('SL_ID', 'LPU_1', 'NHISTORY')
                    + R08XmlStreamWriter.eventDateFields +
                    ('DS1', 'DS1_PR', 'DS_ONK', 'PR_D_N'))


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

        eventSum = params['mapEventIdToSum'].get(eventId, '0')

        local_params = {
            'SL_SUMV': eventSum,
            'SL_TARIF': eventSum,
            'SL_SUM_M': params['mapEventIdToSum'].get(eventId, '')
        }

        diseasePhaseCode = forceInt(record.value('diseasePhaseCode'))
        mkb = forceString(record.value('SL_DS1'))

        if mkb[:1] == 'C' and diseasePhaseCode == 10:
            local_params['SL_DS_ONK'] = 1

        local_params.update(params)

        if eventId != params.setdefault('lastEventId'):
            params['USL_IDSERV'] = 0

            if params['lastEventId']:
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
                    _record = CExtendedRecord(diagRecord, local_params)
                    self.writeGroup('NAZ', self.nazFields, _record)

            _record = CExtendedRecord(record, local_params)
            self.writeGroup('SL', self.eventFields2, _record,
                            closeGroup=False, openGroup=False)
            params['lastEventId'] = eventId


if __name__ == '__main__':
    #pylint: disable=wrong-import-position
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position
    testAccountExport(exportR08NativeHealthExaminationV59, 730)
