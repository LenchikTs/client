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

u"""Экспорт реестра  в формате XML. Забайкальский край. ДД, (Д3) V173"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, pyqtSignature

from library.Utils import (forceString, forceRef, toVariant, forceBool, forceDate)
from Exchange.Order79Export import COrder79ExportWizard
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.ExportR08Hospital import CR08PersonalDataWriter
from Exchange.ExportR08NativeHealthExaminationV173 import (
    CR08ExportPage1, R08XmlStreamWriter, formatAccNumber)
from Exchange.ExportR08NativeHealthExaminationV173 import (CExportPage2,
    getEventTypeCode)

def exportR80NativeHealthExaminationV173(widget, accountId, accountItemIdList,
                                        _=None):
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
        title = u'Мастер экспорта реестра услуг для Забайкальского края Д3 v173'
        prefix = 'R80D3V173'
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
                payerCode = '75'
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
        self.chkReexposed.setEnabled(True)
        self.edtReexposedAccountNumber = QtGui.QLineEdit(self)
        self.lblReexposedAccountNumber = QtGui.QLabel(u'Номер исправляемого счёта', self)
        self.reexposedAccountNumberLayout = QtGui.QHBoxLayout(self)
        self.reexposedAccountNumberLayout.addWidget(self.lblReexposedAccountNumber)
        self.reexposedAccountNumberLayout.addWidget(self.edtReexposedAccountNumber)
        self.verticalLayout.addLayout(self.reexposedAccountNumberLayout)
        self.lblReexposedAccountNumber.setEnabled(self.chkReexposed.isChecked())
        self.edtReexposedAccountNumber.setEnabled(self.chkReexposed.isChecked())


    @pyqtSignature('bool')
    def on_chkReexposed_toggled(self, checked):
        self.lblReexposedAccountNumber.setEnabled(checked)
        self.edtReexposedAccountNumber.setEnabled(checked)


    def prepareStmt(self, params):
        (select, tables, where, orderBy) = CR08ExportPage1.prepareStmt(
            self, params)
        select = u"""Account_Item.event_id AS eventId,
            Account_Item.service_id AS serviceId,
            Event.client_id AS clientId,
            Action.id AS actionId,
            Visit.id AS visitId,
            Event.execDate,
            LastEvent.id AS lastEventId,

            Account_Item.event_id AS Z_SL_IDCASE,
            IF('{isReexposed}',Account_Item.event_id,'') AS Z_SL_FIRST_IDCASE,
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

            '1' AS MR_USL_N_MR_N,
            ActionPersonSpeciality.regionalCode AS MR_USL_N_PRVS,
            ActionPerson.regionalCode AS MR_USL_N_CODE_MD,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            IF(rbPolicyKind.code = '3', '', ClientPolicy.serial) AS PACIENT_SPOLIS,
            IF(rbPolicyKind.code = '3', '', ClientPolicy.number) AS PACIENT_NPOLIS,
            IF(rbPolicyKind.code = '3', ClientPolicy.number, '') AS PACIENT_ENP,
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
            ActionOrgSruct.parent_id AS actionParentOrgStructureId, (SELECT MAX(ds.id) IS NOT NULL
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
            rbPolicyKind.code AS policyKindCode""".format(isReexposed=params['isReexposed'])
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
                rbSpeciality.federalCode,'') AS NAZ_NAZ_IDDOKT,
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
        params['reexposedAccountNumber'] = self._getAccountInfoByNumber(
            forceString(self.edtReexposedAccountNumber.text()))
        self.setProcessParams(params)
        CR08ExportPage1.exportInt(self)


    def _getAccountInfoByNumber(self, number):
        table = self._db.table('Account')
        record = self.db.getRecordEx(table, ['id', 'settleDate'], table['number'].eq(number))
        if record:
            return forceString(record.value(0)), forceDate(record.value(1))
        return None

# ******************************************************************************

class CXmlStreamWriter(R08XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""
    completeEventFields1 = (('IDCASE', 'FIRST_IDCASE', 'VIDPOM', 'LPU', 'VBR')
                            + R08XmlStreamWriter.completeEventDateFields +
                            ('P_OTK', 'RSLT_D', 'OS_SLUCH'))

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO',
                    'SMO', 'SMO_NAM', 'NOVOR')
    eventFields1 = (('SL_ID', 'LPU_1', 'NHISTORY')
                    + R08XmlStreamWriter.eventDateFields +
                    ('DS1', 'DS1_PR', 'DS_ONK', 'PR_D_N'))

    nazFields = ('NAZ_N', 'NAZ_R', 'NAZ_IDDOKT', 'NAZ_V', 'NAZ_USL', 'NAPR_DATE',
                 'NAPR_MO', 'NAZ_PMP', 'NAZ_PK')
    nazDateFields = ('NAPR_DATE')

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'LPU', 'LPU_1')
                     + serviceDateFields +
                     ('P_OTK', 'CODE_USL',  'TARIF', 'SUMV_USL', 'MR_USL_N'))
    serviceSubGroup = {
        'MR_USL_N':{
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    def __init__(self, parent):
        R08XmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params.get('settleDate', QDate())
        date = params.get('accDate', QDate())
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
        if params.get('reexposedAccountNumber'):
            _id, settleDate = params['reexposedAccountNumber']
            self.writeStartElement('REF')
            self.writeTextElement('CODE', _id)
            self.writeTextElement('FIRST_YEAR', forceString(settleDate.year()))
            self.writeTextElement('FIRST_MONTH', forceString(settleDate.month()))
            self.writeEndElement()
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


    def writeService(self, record, params):
        params.setdefault('exportedActions', set()).add(
            forceString(record.value('actionId')))
        params['USL_IDSERV'] += 1
        record = CExtendedRecord(record, params)
        self.writeGroup('USL', self.serviceFields, record,
                        subGroup=self.serviceSubGroup,
                        dateFields=self.serviceDateFields)


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


if __name__ == '__main__':
    #pylint: disable=wrong-import-position
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position
    testAccountExport(exportR80NativeHealthExaminationV173,
                      accNum=u'5-6',
                      configFileName=u'lokosova_ononskayaCRB_06032023.ini')
