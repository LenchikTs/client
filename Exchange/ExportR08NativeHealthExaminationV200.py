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

u"""Экспорт реестра  в формате XML. Республика Калмыкия. ДД, (Д3) V200"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from library.Utils import (forceString, forceRef, toVariant, forceBool)
from Exchange.Order79Export import COrder79ExportWizard
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.ExportR08Hospital import (CR08PersonalDataWriter as
                                        PersonalDataWriter)
from Exchange.ExportR08NativeHealthExamination import (
    CR08ExportPage1, R08XmlStreamWriter, formatAccNumber)
from Exchange.ExportR47D3 import CExportPage2, getEventTypeCode

def exportR08NativeHealthExaminationV200(widget, accountId, accountItemIdList,
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
                                u'ПН2': 'DF', u'ОН3': 'DR', u'ДВ3': 'DP', u'ДС3': 'DS', u'ДС4': 'DU',}

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии V200'
        prefix = 'R08D3V200'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
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
        select += """, (SELECT MAX(ds.id) IS NOT NULL
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code = '9')
                  AND dc.event_id = Account_Item.event_id
                  AND rbDiseasePhases.code = 10
                  AND SUBSTR(ds.MKB,1,1) = 'C'
            ) AS SL_DS_ONK"""
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
        rbService.code AS NAZ_NAZ_USL,
        Action.endDate AS NAPR_DATE,
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

# ******************************************************************************

class XmlStreamWriter(R08XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    eventFields1 = (('SL_ID', 'LPU_1', 'NHISTORY')
                    + R08XmlStreamWriter.eventDateFields +
                    ('DS1', 'DS1_PR', 'DS_ONK', 'PR_D_N'))

    nazFields = ('NAZ_N', 'NAZ_R', 'NAZ_SP', 'NAZ_V', 'NAZ_USL', 'NAPR_DATE',
                 'NAPR_MO', 'NAZ_PMP', 'NAZ_PK')

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
                    _record = CExtendedRecord(diagRecord, local_params)
                    self.writeGroup('NAZ', self.nazFields, _record)

            _record = CExtendedRecord(record, local_params)
            self.writeGroup('SL', self.eventFields2, _record,
                            closeGroup=False, openGroup=False)
            self._lastEventId = eventId


if __name__ == '__main__':
    #pylint: disable=wrong-import-position
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position
    testAccountExport(exportR08NativeHealthExaminationV200, u'08002-ДВ1-17',
        'Balickiy_ONKD3.ini')
