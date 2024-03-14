# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rlogMessageights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import re
import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime, QFile, QTextStream, QTime

from library.AgeSelector import convertAgeSelectorToAgeRange
from library.Utils import forceDate, forceInt, forceRef, forceString, forceStringEx, nameCase, toVariant, formatSex, parseSex, checkSNILS, unformatSNILS, formatSNILS

from Exchange.Cimport import Cimport, ns_list
from Exchange.Utils import EIS_close, setEIS_db
from Orgs.Utils import CNet, getOrgStructureNetId
from Registry.Utils import getAddress, getAddressId, getClientAddress, getClientCompulsoryPolicy, getClientDocument

from Exchange.Ui_ImportEISOMS_Clients import Ui_Dialog


def importClientsFromEisOms(widget):
    try:
        try:
            setEIS_db()
            if QtGui.qApp.EIS_db:
                dlg=CImportClientsFromEisOms(widget, QtGui.qApp.EIS_db)
                dlg.exec_()
        finally:
            QtGui.qApp.EIS_db.close()
            QtGui.qApp.EIS_db=None
    except:
        QtGui.qApp.logCurrentException()
        EIS_close()


class CImportClientsFromEisOms(Cimport, QtGui.QDialog, Ui_Dialog): #
    mapOblTownTypeToSocr = {u'Г' : u'г',
                            u'Д' : u'д',
                            u'Ж' : u'п/ст',
                            u'К' : u'кордон',
                            u'М' : u'м',
                            u'П' : u'п',
                            u'Р' : u'пгт',
                            u'С' : u'с',
                            u'Х' : u'х',
                           }

    def __init__(self, parent, EIS_db):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        Cimport.__init__(self, self.logBrowser)
        self.setupAges()

#        Cimport.__init__(self, self.logBrowser)
        self.progressBar.setFormat(u'%v из %m')
        self.fileLog = CFileLog(self, os.path.join(QtGui.qApp.getDocumentsDir(), 'importEIS.log'))
        self.EIS_db=EIS_db

        self.lblSourceTxt.setText(self.EIS_db.connectionId)
        self.badChars = re.compile('[0-9a-zA-Z]')

#        self.mapSpbTownToKladrCode = { u'г.Санкт-Петербург': '7800000000000',
#                                       ''                  : '7800000000000',
#                                     }
#        self.mapLoTownToKladrCode  = {}
#        self.mapEisLpuIdToOrgId={}
#        self.mapEisDocumentTypeIdToDocTypeId = {}

        self.setupEisTariffMonth()
        self.setLastLoadedTariffMonth(forceInt(QtGui.qApp.preferences.appPrefs.get('TMONTH', 0)))
        self.progressBar.setFormat('')
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)


    def setupAges(self):
        netId = getOrgStructureNetId(QtGui.qApp.currentOrgStructureId())
        if netId:
            net = CNet(netId)
            if net.age:
                begAge, endAge = convertAgeSelectorToAgeRange(net.age)
                self.edtAgeFrom.setValue(begAge)
                self.edtAgeTo.setValue(endAge)


    def setupEisTariffMonth(self):
        table = self.EIS_db.table('TARIFF_MONTH')
        tmonth = forceRef(self.EIS_db.getMax(table, 'ID_TARIFF_MONTH'))
        record = self.EIS_db.getRecordEx(table, '*', table['ID_TARIFF_MONTH'].eq(tmonth))
        if record:
            self.tmonthBegDate = forceDate(record.value('TARIFF_MONTH_BEG'))
            self.tmonthEndDate = forceDate(record.value('TARIFF_MONTH_END'))
            self.tmonth = tmonth
            self.lblEisTariffMonthTxt.setText( u'%d (%s - %s)' % (tmonth,
                                                                  forceString(self.tmonthBegDate),
                                                                  forceString(self.tmonthEndDate))
                                             )
        else:
            self.tmonthBegDate = None
            self.tmonthEndDate = None
            self.tmonth = None
            self.lblEisTariffMonthTxt.setText( u'тарифный месяц ЕИС не определён')


    def setLastLoadedTariffMonth(self, tmonth):
        self.lastLoadedTmonth = tmonth
        self.lblLastLoadedTariffMonthTxt.setText(str(self.lastLoadedTmonth))


    def startImport(self):
        self.importFromMu = self.rbMu.isChecked()
        onlyNew = self.chkOnlyNew.isChecked() and not self.importFromMu
        self.importAttach = self.chkImportAttach.isChecked() and not self.importFromMu
        if self.chkLogToFile.isChecked():
            self.fileLog.turnOn()
        else:
            self.fileLog.turnOff()

        if not self.setupImport():
            return

        QtGui.qApp.processEvents()

        today = QDate.currentDate()
        lowBirthdayStr=self.EIS_db.formatDate(today.addYears(-self.edtAgeTo.value()-1))
        highBirthdayStr=self.EIS_db.formatDate(today.addYears(-self.edtAgeFrom.value()).addDays(-1))
        self.setupCount(onlyNew, lowBirthdayStr, highBirthdayStr)

        if self.importFromMu:
            stmt='''
SELECT PATIENTS.ID_EIS_OMS AS ID_HISTORY, PATIENT_DATA.EP_NUMBER, PATIENTS.ID_HUMAN,
PATIENT_DATA.SURNAME, PATIENT_DATA.NAME, PATIENT_DATA.SECOND_NAME, PATIENT_DATA.SEX, PATIENT_DATA.BIRTHDAY,
PATIENT_DATA.SNILS,
PATIENT_POLIS.ID_SMO, PATIENT_POLIS.ID_SMO_REGION, PATIENT_POLIS.ID_POLIS_TYPE, PATIENT_POLIS.POLIS_SERIA, PATIENT_POLIS.POLIS_NUMBER, PATIENT_POLIS.POLIS_BEGIN_DATE, PATIENT_POLIS.POLIS_END_DATE,
PATIENT_DATA.ID_DOC_TYPE, PATIENT_DATA.SERIA_LEFT, PATIENT_DATA.SERIA_RIGHT, PATIENT_DATA.DOC_NUMBER, NULL AS ISSUE_DATE,
PATIENT_DATA.ID_ADDRESS_REG, PATIENT_DATA.ID_ADDRESS_LOC
FROM
PATIENTS
LEFT JOIN PATIENT_DATA ON PATIENT_DATA.ID_PATIENT=PATIENTS.ID_PATIENT
LEFT JOIN PATIENT_POLIS ON PATIENT_POLIS.ID_PATIENT=PATIENTS.ID_PATIENT
WHERE PATIENTS.IS_ACTIVE!='0'
  AND PATIENTS.ID_PATIENT IN (SELECT P1.ID_PATIENT FROM PATIENTS P1
                              WHERE P1.ID_EIS_OMS IS NULL
                                 OR P1.ID_EIS_OMS = 0
                                 OR P1.DATE_END = (SELECT MAX(P2.DATE_END)
                                                   FROM PATIENTS P2
                                                   WHERE P1.ID_EIS_OMS = P2.ID_EIS_OMS))
  AND NOT EXISTS (SELECT * FROM PEOPLE WHERE
           (PEOPLE.ID_HISTORY IS NOT NULL AND PEOPLE.ID_HISTORY=PATIENTS.ID_EIS_OMS) OR
           (PEOPLE.EP_NUMBER IS NOT NULL AND PEOPLE.EP_NUMBER=PATIENT_DATA.EP_NUMBER))
           AND PATIENT_DATA.BIRTHDAY BETWEEN %s AND %s''' % (lowBirthdayStr, highBirthdayStr)
        else:
            stmt='''
SELECT PEOPLE.ID_HISTORY, PEOPLE.EP_NUMBER, NULL AS ID_HUMAN,
PEOPLE.SURNAME, PEOPLE.NAME, PEOPLE.SECOND_NAME, PEOPLE.SEX, PEOPLE.BIRTHDAY,
PEOPLE.SS AS SNILS,
PEOPLE.ID_SMO, NULL AS ID_SMO_REGION, PEOPLE.ID_POLIS_TYPE, PEOPLE.POLIS_SERIA, PEOPLE.POLIS_NUMBER, PEOPLE.POLIS_BEGIN_DATE, PEOPLE.POLIS_END_DATE,
PEOPLE.ID_DOC_TYPE, PEOPLE.SERIA_LEFT, PEOPLE.SERIA_RIGHT, PEOPLE.DOC_NUMBER, PEOPLE.ISSUE_DATE,
PEOPLE.ID_ADDRESS_REGISTRATION, PEOPLE.ID_ADDRESS_LOCATION,
PEOPLE.TMONTH_BEGIN, PEOPLE.ID_HUMAN_TYPE, PEOPLE.ID_LPU
FROM
PEOPLE
WHERE PEOPLE.IS_ACTIVE!='0'
  AND PEOPLE.BIRTHDAY BETWEEN %s AND %s''' % (lowBirthdayStr, highBirthdayStr)
            if onlyNew:
                stmt+=' AND PEOPLE.TMONTH_BEGIN>%d' % self.lastLoadedTmonth
#                stmt+=' AND EP_NUMBER=7801955122900256'
            stmt+=' ORDER BY PEOPLE.TMONTH_BEGIN'
        query = self.EIS_db.query(stmt)
        query.setForwardOnly(True)
        n=0
        self.num_added=0
        self.num_found=0
        self.num_fixed=0

        tmonth = 0
        if not onlyNew:
            self.setLastLoadedTariffMonth(0)

        try:
            while query.next():
                QtGui.qApp.processEvents()
                if self.abort:
                    break
                n+=1
                self.n=n

                record = query.record()
                QtGui.qApp.db.transaction()
                try:
                    self.processRecord(record)
                    QtGui.qApp.db.commit()
                except:
                    QtGui.qApp.db.rollback()
                    raise

                tmonth = forceInt(record.value('TMONTH_BEGIN'))
                if not self.importFromMu:
                    if tmonth-1>self.lastLoadedTmonth:
                        self.setLastLoadedTariffMonth(tmonth-1)
                self.progressBar.setValue(n)
                status = u'добавлено %d, найдено %d, исправлено %d' % (self.num_added, self.num_found, self.num_fixed)
                self.lblStatus.setText(status)

            if not self.importFromMu and tmonth:
                self.setLastLoadedTariffMonth(tmonth)

        finally:
            self.fileLog.close()
        if not self.importFromMu:
            QtGui.qApp.preferences.appPrefs['TMONTH'] = toVariant(self.lastLoadedTmonth)


    def setupImport(self):
        db = QtGui.qApp.db
        self.ClientIdentification_ID_HISTORY = forceRef(db.translate('rbAccountingSystem', 'code', '2', 'id'))
        self.ClientIdentification_ID_HUMAN   = forceRef(db.translate('rbAccountingSystem', 'code', '3', 'id'))
        self.omsFinanceId=forceInt(db.translate('rbFinance', 'name', u'ОМС', 'id'))
        self.attachTypeId=forceInt(db.translate('rbAttachType', 'code', '078', 'id'))
        self.defaultPolicyTypeId = forceRef(db.translate('rbPolicyType', 'code', '1', 'id'))
        self.mapEisPolicyTypeIdToKindId = {}
        for policyKind in (1, 2, 3):
            self.mapEisPolicyTypeIdToKindId[policyKind] = forceRef(db.translate('rbPolicyKind', 'regionalCode', str(policyKind), 'id'))

        if self.ClientIdentification_ID_HISTORY is None:
            self.log.append(u'Не найдена учётная система для ID_HISTORY код "2"')
            return False

        if self.ClientIdentification_ID_HUMAN is None:
            self.log.append(u'Не найдена учётная система для ID_HUMAN код "3"')
            return False

        if self.importAttach and not self.omsFinanceId:
            self.log.append(u'Не найден тип финансирования с наименованием "ОМС"')
            return False

        if self.importAttach and not self.attachTypeId:
            if QtGui.QMessageBox.question( self,
                                       u'Внимание!',
                                       u'Не найден тип прикрепления ТФОМС (код "078"). Добавить?',
                                       QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                       QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                tableAttachType = db.table('rbAttachType')
                attachRecord = tableAttachType.newRecord()
                attachRecord.setValue('code', '078')
                attachRecord.setValue('name', u'ТФОМС')
                attachRecord.setValue('regionalCode', '78')
                attachRecord.setValue('temporary', 0)
                attachRecord.setValue('outcome', 0)
                attachRecord.setValue('finance_id', self.omsFinanceId)
                self.attachTypeId = db.insertRecord(tableAttachType, attachRecord)
                if not self.attachTypeId:
                    self.log.append(u'Ошибка записи типа прикрепления')
                    return False
            else:
                self.log.append(u'Не найден тип прикрепления ТФОМС, код "078"')
                return False

        self.mapEisSmoIdToInsurerId = {}
        self.mapEisDocumentTypeIdToDocTypeId = {}
        self.mapSpbTownToKladrCode = { u'г.Санкт-Петербург': '7800000000000',
                                       ''                  : '7800000000000',
                                     }
        self.mapLoTownToKladrCode  = {
                                     }
        self.mapEisLpuIdToOrgId={}

        return True


    def setupCount(self, onlyNew, lowBirthdayStr, highBirthdayStr):
        if self.importFromMu:
            stmt='''SELECT COUNT(*) FROM PATIENTS
            LEFT JOIN PATIENT_DATA ON PATIENT_DATA.ID_PATIENT=PATIENTS.ID_PATIENT
            WHERE PATIENTS.IS_ACTIVE!='0'
            AND PATIENTS.ID_PATIENT IN (SELECT P1.ID_PATIENT FROM PATIENTS P1
                                        WHERE P1.ID_EIS_OMS IS NULL
                                           OR P1.ID_EIS_OMS = 0
                                           OR P1.DATE_END = (SELECT MAX(P2.DATE_END)
                                                             FROM PATIENTS P2
                                                             WHERE P1.ID_EIS_OMS = P2.ID_EIS_OMS))
            AND NOT EXISTS (SELECT * FROM PEOPLE WHERE
            (PEOPLE.ID_HISTORY IS NOT NULL AND PEOPLE.ID_HISTORY=PATIENTS.ID_EIS_OMS) OR
            (PEOPLE.EP_NUMBER IS NOT NULL AND PEOPLE.EP_NUMBER=PATIENT_DATA.EP_NUMBER))
            AND PATIENT_DATA.BIRTHDAY BETWEEN %s AND %s''' % (lowBirthdayStr, highBirthdayStr)
        else:
            stmt='''SELECT COUNT(*) FROM PEOPLE WHERE IS_ACTIVE!='0' AND BIRTHDAY BETWEEN %s AND %s''' % (lowBirthdayStr, highBirthdayStr)
            if onlyNew:
                stmt+=' AND PEOPLE.TMONTH_BEGIN>%d' % self.lastLoadedTmonth
        query=self.EIS_db.query(stmt)
        if query.next():
            record=query.record()
            num=forceInt(record.value(0))
        else:
            num = 0
        self.num=num
        self.progressBar.setFormat(u'%v из %m')
        if num>0:
            self.progressBar.setMaximum(num)
        else:
            self.progressBar.setMaximum(0)


# переделать!!!
    def logMessage(self, eisPatient, message, extMessage):
        parts = []
        if eisPatient.historyId:
            parts.append('%s=%s' % ( 'PATIENTS.ID_EIS_OMS' if self.importFromMu else 'PEOPLE.ID_HISTORY',
                                      self.eisPatient.historyId
                                   )
                        )
        if self.eisPatient.humanId:
            parts.append('PATIENTS.ID_HUMAN=%s' % self.eisPatient.humanId)
        idenification = '; '.join(parts)
        errorMessage = u'запись %d (%s): %s' % (self.n, idenification, message)
        self.logBrowser.append(errorMessage)
        if extMessage:
            self.fileLog.addErrorMessage(errorMessage+'\n'+extMessage)


    def processRecord(self, record):
        eisPatient = CEisPatient(self.importFromMu, record)
        self.eisPatient = eisPatient # временно, для диагностики

        failed, clientId = self.findClientByIdentifications(eisPatient)
        if failed:
            return

        if not clientId:
            failed, clientId = self.findClientByFields(eisPatient)
            if failed:
                return

        if clientId:
            if not self.verifyOrUpdateBaseFields(clientId, eisPatient):
                return
            self.num_found += 1
            self.updatePolicy(clientId, eisPatient)
            self.ensureDocument(clientId, eisPatient)
            self.ensureAddresses(clientId, eisPatient)
        else:
            self.num_added += 1
            clientId = self.createClient(eisPatient)
            self.updatePolicy(clientId, eisPatient)
            self.ensureDocument(clientId, eisPatient)
            self.ensureAddresses(clientId, eisPatient)

        if self.importAttach:
           self.setOrUpdateAttach(clientId, eisPatient)
        self.setOrUpdateIdentification(clientId, eisPatient)


    def findClientByIdentifications(self, eisPatient):
        # возвращает кортеж (отказ, clientId по идентификаторам)
        # отказ устанавливается в случае противоречивости в данных
        id2 = self.findClientIdByIdentification(self.ClientIdentification_ID_HISTORY, eisPatient.historyId)
        id3 = self.findClientIdByIdentification(self.ClientIdentification_ID_HUMAN, eisPatient.humanId)

        if id2 and id3 and id2!=id3:
            message    = u'идентификаторы ID_HISTORY и ID_HUMAN указывают на разных пациентов'
            extMessage = 'ID_HISTORY=%r, ID_HUMAN=%r'%(eisPatient.historyId, eisPatient.humanId)
            self.logMessage(eisPatient, message, extMessage)
            return True, None
        return False, id2 or id3


    def findClientIdByIdentification(self, accountingSystemId, identifier):
        # возвращает clientId по идентификатору либо None если не найдено
        if not identifier:
            return None

        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableClientIdentification = db.table('ClientIdentification')
        table = tableClientIdentification.innerJoin(tableClient, tableClient['id'].eq(tableClientIdentification['client_id']))
        cond=[tableClientIdentification['identifier'].eq(identifier),
              tableClientIdentification['accountingSystem_id'].eq(accountingSystemId),
              tableClientIdentification['deleted'].eq(0),
              tableClient['deleted'].eq(0)
             ]
        ident = db.getRecordEx(table, tableClient['id'], cond)
        if ident:
            clientId=forceRef(ident.value('id'))
            return clientId
        return None


    def findClientByFields(self, eisPatient):
        # возвращает кортеж (отказ, clientId по ФИО и др. полям)
        # отказ устанавливается в случае противоречивости в данных
        # например, неоднозначность результата
        # если ничего не найдено - нет отказа
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableClientPolicy = db.table('ClientPolicy')
        tableClientDocument = db.table('ClientDocument')

        cond = [ tableClient['lastName'].eq(eisPatient.lastName),
                 tableClient['firstName'].eq(eisPatient.firstName),
                 tableClient['patrName'].eq(eisPatient.patrName),
                 tableClient['birthDate'].eq(eisPatient.birthDate),
               ]

        idList = db.getIdList(tableClient, 'id', cond)
        if idList:
            idListByPolicy   = db.getDistinctIdList(tableClientPolicy,
                                            'client_id',
                                            [ tableClientPolicy['client_id'].inlist(idList),
                                              tableClientPolicy['number'].eq(eisPatient.policyNumber),
                                              tableClientPolicy['deleted'].eq(0),
                                            ]
                                           )
            idListByDocument = db.getDistinctIdList(tableClientDocument,
                                            'client_id',
                                            [ tableClientDocument['client_id'].inlist(idList),
                                              tableClientDocument['number'].eq(eisPatient.docNumber),
                                              tableClientDocument['deleted'].eq(0),
                                            ]
                                           )
            if idListByPolicy and idListByDocument:
                idList = list(set(idListByPolicy) & set(idListByDocument))
            else:
                idList = idListByPolicy or idListByDocument
            if not idList:
                return False, None
            if len(idList) == 1:
                return False, idList[0]
            else:
                message = u'неоднозначность поиска по основным реквизитам'
                extMessage = u'возможные претенденты Client.id=%r'%( idList, )
                self.logMessage(eisPatient, message, extMessage)
                return True, None
        return False, None


    def verifyOrUpdateBaseFields(self, clientId, eisPatient):
        # проверить отсутствие существенных расхождений, и в случае несущественных обновить поля в Client
        # возвращает успех проверки основных полей - т.е. отсутствие существенных расхождений
        db = QtGui.qApp.db
        record = db.getRecord('Client',
                              ['id', 'lastName', 'firstName', 'patrName', 'sex', 'birthDate', 'SNILS'],
                              clientId)
        lastName  = forceString(record.value('lastName'))
        firstName = forceString(record.value('firstName'))
        patrName  = forceString(record.value('patrName'))
        sex       = forceInt(record.value('sex'))
        birthDate = forceDate(record.value('birthDate'))
        snils     = forceString(record.value('SNILS'))

        fixed = False
        mismatch = []

        if eisPatient.lastName and lastName!=eisPatient.lastName:
            if not lastName or self.badChars.search(lastName) is not None:
                record.setValue('lastName', eisPatient.lastName)
                fixed = True
            else:
                mismatch.append(u'Фамилия: «%s», в ЕИС: «%s»'%(lastName, eisPatient.lastName))
        if eisPatient.firstName and firstName!=eisPatient.firstName:
            if not firstName or self.badChars.search(firstName) is not None:
                record.setValue('firstName', eisPatient.firstName)
                fixed = True
            else:
                mismatch.append(u'Имя: «%s», в ЕИС: «%s»'%(firstName, eisPatient.firstName))
        if eisPatient.patrName and patrName!=eisPatient.patrName:
            if not patrName or self.badChars.search(patrName) is not None:
                record.setValue('patrName', eisPatient.patrName)
                fixed = True
            else:
                mismatch.append(u'Отчество: «%s», в ЕИС: «%s»'%(patrName, eisPatient.patrName))
        if eisPatient.sex and sex!=eisPatient.sex:
            if not sex:
                record.setValue('sex', eisPatient.sex)
                fixed = True
            else:
                mismatch.append(u'Пол: «%s», в ЕИС: «%s»'%(formatSex(sex), formatSex(eisPatient.sex)))
        if eisPatient.birthDate and birthDate!=eisPatient.birthDate:
            if not birthDate:
                record.setValue('birthDate', eisPatient.birthDate)
                fixed = True
            else:
                mismatch.append(u'Д.Р.: «%s», в ЕИС: «%s»'%(forceString(birthDate), forceString(eisPatient.birthDate)))

        if mismatch:
            message = u'не совпадает основная информация'
            extMessage = u'Client.id=%d: %s'%( clientId, '; '.join(mismatch))
            self.logMessage(eisPatient, message, extMessage)
            return False

        if eisPatient.snils and eisPatient.snils != snils:
            if snils:
                message = u'не совпадает СНИЛС'
                extMessage = u'Client.id=%d: СНИЛС:«%s», в ЕИС: «%s» '%( clientId, formatSNILS(snils), formatSNILS(eisPatient.snils))
                self.logMessage(eisPatient, message, extMessage)
            else:
                record.setValue('SNILS', eisPatient.snils)
                fixed = True

        if fixed:
            self.num_fixed+=1
            db.updateRecord('Client', record)
        return True


    def createClient(self, eisPatient):
        # создать запись Client и заполнить основные поля
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        record = tableClient.newRecord()
        record.setValue('lastName',  eisPatient.lastName)
        record.setValue('firstName', eisPatient.firstName)
        record.setValue('patrName',  eisPatient.patrName)
        record.setValue('sex',       eisPatient.sex)
        record.setValue('birthDate', eisPatient.birthDate)
        record.setValue('SNILS',     eisPatient.snils)
        return db.insertRecord(tableClient, record)


    def updatePolicy(self, clientId, eisPatient):
        insurerId     = self.getInsurerId(eisPatient.smoId, eisPatient.regionalSmoId)
        policyKindId  = self.mapEisPolicyTypeIdToKindId.get(eisPatient.policyTypeId)

        currentPolicyRecord = getClientCompulsoryPolicy(clientId)
        db = QtGui.qApp.db
        tableClientPolicy = db.table('ClientPolicy')
        if (   currentPolicyRecord is None
            or insurerId    and insurerId != forceRef(currentPolicyRecord.value('insurer_id'))
            or policyKindId and policyKindId != forceRef(currentPolicyRecord.value('policyKind_id'))
            or eisPatient.policySerial != forceString(currentPolicyRecord.value('serial'))
            or eisPatient.policyNumber != forceString(currentPolicyRecord.value('number'))
           ):
            record = tableClientPolicy.newRecord()
            record.setValue('client_id', clientId)
            record.setValue('insurer_id', insurerId)
            record.setValue('policyType_id', self.defaultPolicyTypeId)
            record.setValue('policyKind_id', policyKindId)
            record.setValue('serial', eisPatient.policySerial)
            record.setValue('number', eisPatient.policyNumber)
            record.setValue('begDate',eisPatient.policyBegDate)
            record.setValue('endDate',eisPatient.policyEndDate)
            db.insertRecord(tableClientPolicy, record)
        elif (   eisPatient.policyBegDate and eisPatient.policyBegDate != forceDate(currentPolicyRecord.value('begDate'))
              or eisPatient.policyEndDate and eisPatient.policyEndDate != forceDate(currentPolicyRecord.value('endDate'))
             ):
            # оказалось, что currentPolicyRecord имеет поля, отсутствующие в ClientPolicy :(
            record = tableClientPolicy.newRecord(['id', 'begDate', 'endDate'])
            record.setValue('id', currentPolicyRecord.value('id'))
            record.setValue('begDate', eisPatient.policyBegDate)
            record.setValue('endDate', eisPatient.policyEndDate)
            db.updateRecord(tableClientPolicy, record)


    def getInsurerId(self, smoId, regionalSmoId):
        key = smoId, regionalSmoId
        insurerId = self.mapEisSmoIdToInsurerId.get(key, False)
        if insurerId is False:
            insurerId  = self.mapEisSmoIdToInsurerId[key] = self._getInsurerId(smoId, regionalSmoId)
        return insurerId


    def _getInsurerId(self, smoId, regionalSmoId):
        # получить наш id страховой компании
        if regionalSmoId:
            tableVmuSmoReg = self.EIS_db.table('VMU_SMO_REG')
            tableRfRegion  = self.EIS_db.table('RF_REGION')
            tableSmo = tableVmuSmoReg.innerJoin(tableRfRegion, tableRfRegion['REGION_CODE'].eq(tableVmuSmoReg['REGION_CODE']))
            record = self.EIS_db.getRecordEx(tableSmo,
                                             [ 'ID_SMO_REG',
                                               'SMOCOD AS FED_CODE',
                                               'SMOCOD AS CODE',
                                               'RF_REGION.KLADR_CODE_C AS REGION',
                                               'INN',
                                               'NULL AS KPP',
                                               'OGRN_SMO AS OGRN',
                                               'VMU_SMO_REG.OKATO',
                                               'SMO_LONG_NAME',
                                               'SMO_SHORT_NAME',
                                             ],
                                             tableVmuSmoReg['ID_SMO_REG'].eq(regionalSmoId)
                                            )
        elif smoId:
            tableSmo = self.EIS_db.table('SMO')
            record = self.EIS_db.getRecordEx(tableSmo,
                                             [ 'ID_SMO',
                                               'FED_CODE',
                                               'CODE',
                                               '78 AS REGION',
                                               'INN',
                                               'KPP',
                                               'NULL AS OGRN',
                                               'NULL AS OKATO',
                                               'SMO_LONG_NAME',
                                               'SMO_SHORT_NAME',
                                             ],
                                             self.EIS_db.joinAnd([tableSmo['ID_SMO'].eq(smoId),
                                                                  tableSmo['IS_ACTIVE'].ne('0'),
                                                                  tableSmo['IS_IN_CITY'].ne('0'),
                                                                  tableSmo['IS_CONFIRMED'].ne('0'),
                                                                 ])
                                            )
        else:
            record = None

        if record is None:
            return None

        federalCode = forceString(record.value('FED_CODE'))
        code        = forceString(record.value('CODE'))
        region      = '%02d' % forceInt(record.value('REGION'))
        inn         = forceString(record.value('INN'))
        kpp         = forceString(record.value('KPP'))
        ogrn        = forceString(record.value('OGRN'))
        okato       = forceString(record.value('OKATO'))

        # теперь можно:
        # 1) поискать страховую компанию по коду ФФОМС
        # 2) поискать страховую компанию по коду ИНФИС
        # 3) поискать страховую компанию по INN + KPP
        # 4) поискать страховую компанию по OGRN + OKATO
        # 5) поискать страховую компанию по наименованию?

        db = QtGui.qApp.db
        table = db.table('Organisation')
        commonCond = [ table['deleted'].eq(0), table['isInsurer'].ne(0) ]
        if region != '00':
            commonCond.append(db.joinOr([table['area'].like(region+'%'), table['area'].eq('')]))
        commonCond = db.joinAnd(commonCond)

        # 1) поискать страховую компанию по коду ФФОМС
        orgIdListSum = []
        orgIdList = db.getIdList(table,
                                 where=[ commonCond,
                                         table['smoCode'].eq(federalCode)
                                       ]
                                )
        if len(orgIdList) == 1:
            return orgIdList[0]
        orgIdListSum.extend(orgIdList)
        # 2) поискать страховую компанию по коду ИНФИС
        orgIdList = db.getIdList(table,
                                 where=[ commonCond,
                                         table['infisCode'].eq(code)
                                       ]
                                )
        if len(orgIdList) == 1:
            return orgIdList[0]
        orgIdListSum.extend(orgIdList)
        # 3) поискать страховую компанию по INN + KPP (наши,
        if inn and kpp:
            orgIdList = db.getIdList(table,
                                     where=[ commonCond,
                                             table['INN'].eq(inn),
                                             table['KPP'].eq(kpp),
                                           ]
                                    )
            if len(orgIdList) == 1:
                return orgIdList[0]
            orgIdListSum.extend(orgIdList)
        # 4) поискать страховую компанию по OGRN + OKATO
        if ogrn and okato:
            orgIdList = db.getIdList(table,
                                     where=[ commonCond,
                                             table['OGRN'].eq(ogrn),
                                             table['OKATO'].eq(okato),
                                           ]
                                    )
            if len(orgIdList) == 1:
                return orgIdList[0]
            orgIdListSum.extend(orgIdList)
        # 5) поискать страховую компанию по наименованию?

        if orgIdListSum:
            return orgIdListSum[0]

        # ещё можно добавить :)
        return None


    def ensureDocument(self, clientId, eisPatient):
        # установить тип документа, если ещё пока нет документа
        # если документ уже есть, то ничего делать не нужно - мы не верим источнику
        currentDocumentRecord = getClientDocument(clientId)
        if currentDocumentRecord is None:
            if eisPatient.docTypeId != 0 and eisPatient.docNumber != '':
                documentTypeId=self.getDocumentTypeIdByEisId(eisPatient.docTypeId)
                if not documentTypeId:
                    message = u'Невозможно подобрать тип документа'
                    extMessage = 'ID_DOC_TYPE=%s' % eisPatient.docTypeId
                    self.logMessage(eisPatient, message, extMessage)
                    return

                db = QtGui.qApp.db
                tableClientDocument = db.table('ClientDocument')
                record = tableClientDocument.newRecord()
                record.setValue('client_id', clientId)
                record.setValue('documentType_id', documentTypeId)
                record.setValue('serial', eisPatient.docSerialLeft + ' '+eisPatient.docSerialRight)
                record.setValue('number', eisPatient.docNumber)
                record.setValue('date',   eisPatient.docDate)
#                record.setValue('origin', eisPatient.docOrigin)
                db.insertRecord(tableClientDocument, record)
        else:
            # здесь можно добавить диагностику для случая несовпадения документа
            pass


    def ensureAddresses(self, clientId, eisPatient):
        if eisPatient.registrationAddressId:
            self.ensureAddress(clientId, eisPatient.registrationAddressId, 0)
        if eisPatient.locationAddressId:
            self.ensureAddress(clientId, eisPatient.locationAddressId,     1)


    def ensureAddress(self, clientId, eisAddressId, addressType):
        currAddress = self.getClientAddress(clientId, addressType)
        if currAddress is None or self.addressIsWeak(currAddress):
            # адреса нет, нужно добавить - либо существующий адрес "слабый"
            db = QtGui.qApp.db
            if self.importFromMu:
                stmt = self.getStmtForAddressFieldsFromMu(eisAddressId)
            else:
                stmt = self.getStmtForAddressFieldsFromRpf(eisAddressId)
            address = self.getAddressDescr(stmt)
            if address and not ( currAddress and self.addressIsWeak(address) ):
                addressId = getAddressId(address)
                tableClientAddress = db.table('ClientAddress')
                record = tableClientAddress.newRecord()
                record.setValue('client_id', clientId)
                record.setValue('type',      addressType)
                record.setValue('address_id',addressId)
                record.setValue('freeInput', address['freeInput'])
                db.insertRecord(tableClientAddress, record)
        else:
            # нужно диагностировать различие в адресе?
            pass


    def getClientAddress(self, clientId, addressType):
        clientAddress = getClientAddress(clientId, addressType)
        if clientAddress:
            return getAddress(forceRef(clientAddress.value('address_id')),
                              forceString(clientAddress.value('freeInput'))
                             )
        else:
            return None


    def addressIsWeak(self, address):
        if not address['KLADRCode']:
            return True
        if address['KLADRCode'].startswith('78') and not address['KLADRStreetCode']:
            return True
        return False


    def getStmtForAddressFieldsFromMu(self, eisAddressId):
        # сформировать запрос для получения адреса из МУ
        tablePatientAddress = self.EIS_db.table('PATIENT_ADDRESS')
        return u'''
SELECT PATIENT_ADDRESS.ID_ADDRESS,
       PATIENT_ADDRESS.ADDRESS_TYPE,
       RF_REGION.KLADR_CODE_C AS REGION,
       PATIENT_ADDRESS.KLADR_CODE,
       OBL_TOWN.OBL_TOWN_TYPE,
       OBL_TOWN.OBL_TOWN_CODE,
       OBL_TOWN.OBL_TOWN_NAME,
       TOWN.TOWN_NAME,
       COALESCE(T_GEONIM.GEONIM_TYPE_NAME, VMU_STREET_TYPE.STREET_TYPE_NAME) AS STREET_TYPE,
       COALESCE(GEONIM_NAME.GEONIM_NAME,PATIENT_ADDRESS.STREET) AS STREET,
       COALESCE(HOUSE.HOUSE, PATIENT_ADDRESS.HOUSE) AS HOUSE,
       COALESCE(HOUSE.KORPUS,PATIENT_ADDRESS.KORPUS) AS KORPUS,
       PATIENT_ADDRESS.FLAT,
       PATIENT_ADDRESS.UNSTRUCT_ADDRESS,
       PATIENT_ADDRESS.ID_PREFIX
FROM PATIENT_ADDRESS
LEFT JOIN RF_REGION       ON RF_REGION.REGION_CODE = PATIENT_ADDRESS.ID_OKATO_REGION
LEFT JOIN OBL_TOWN        ON OBL_TOWN.ID_OBL_TOWN=PATIENT_ADDRESS.ID_OBL_TOWN AND PATIENT_ADDRESS.ADDRESS_TYPE='о'
LEFT JOIN PREFIX          ON PREFIX.ID_PREFIX=PATIENT_ADDRESS.ID_PREFIX
LEFT JOIN TOWN            ON TOWN.ID_TOWN=PREFIX.ID_TOWN
LEFT JOIN GEONIM_NAME     ON GEONIM_NAME.ID_GEONIM_NAME=PREFIX.ID_GEONIM_NAME
LEFT JOIN T_GEONIM        ON T_GEONIM.ID_GEONIM_TYPE=PREFIX.ID_GEONIM_TYPE
LEFT JOIN HOUSE           ON HOUSE.ID_HOUSE = PATIENT_ADDRESS.ID_HOUSE
LEFT JOIN VMU_STREET_TYPE ON VMU_STREET_TYPE.ID_STREET_TYPE = PATIENT_ADDRESS.ID_STREET_TYPE
WHERE %s''' % tablePatientAddress['ID_ADDRESS'].eq(eisAddressId)


    def getStmtForAddressFieldsFromRpf(self, eisAddressId):
        # сформировать запрос для получения адреса из РПФ
        tableAddresses = self.EIS_db.table('ADDRESSES')
        return u'''
SELECT ADDRESSES.ID_ADDRESS_RECORD,
       ADDRESSES.ADDRESS_TYPE,
       RF_REGION.KLADR_CODE_C AS REGION,
       NULL AS KLADR_CODE,
       OBL_TOWN.OBL_TOWN_TYPE,
       OBL_TOWN.OBL_TOWN_CODE,
       OBL_TOWN.OBL_TOWN_NAME,
       TOWN.TOWN_NAME,
       T_GEONIM.GEONIM_TYPE_NAME AS STREET_TYPE,
       GEONIM_NAME.GEONIM_NAME AS STREET,
       HOUSE.HOUSE AS HOUSE,
       HOUSE.KORPUS AS KORPUS,
       ADDRESSES.FLAT,
       ADDRESSES.UNSTRUCT_ADDRESS,
       HOUSE.ID_PREFIX
FROM ADDRESSES
LEFT JOIN RF_REGION   ON RF_REGION.REGION_CODE = ADDRESSES.REGION_CODE
LEFT JOIN OBL_TOWN    ON OBL_TOWN.ID_OBL_TOWN=ADDRESSES.ID_OBL_TOWN AND ADDRESSES.ADDRESS_TYPE='о'
LEFT JOIN HOUSE       ON HOUSE.ID_HOUSE = ADDRESSES.ID_HOUSE
LEFT JOIN PREFIX      ON PREFIX.ID_PREFIX=HOUSE.ID_PREFIX
LEFT JOIN TOWN        ON TOWN.ID_TOWN=PREFIX.ID_TOWN
LEFT JOIN GEONIM_NAME ON GEONIM_NAME.ID_GEONIM_NAME=PREFIX.ID_GEONIM_NAME
LEFT JOIN T_GEONIM    ON T_GEONIM.ID_GEONIM_TYPE=PREFIX.ID_GEONIM_TYPE
WHERE %s''' % tableAddresses['ID_ADDRESS_RECORD'].eq(eisAddressId)


    def getAddressDescr(self, stmt):
        query = self.EIS_db.query(stmt)
        if not query.next():
            return None

        record=query.record()
#        addressType = forceString(record.value('ADDRESS_TYPE')).lower()
        freeInput   = forceStringEx(record.value('UNSTRUCT_ADDRESS'))
        region = forceString(record.value('REGION')).rjust(2, '0')
        if region == '00':
            region = ''
        kladrCode = forceString(record.value('KLADR_CODE'))
        if len(kladrCode) == 12:
            kladrCode = '0' + kladrCode
        if len(kladrCode) != 13:
            kladrCode = ''
        if not kladrCode:
            if region == '78':
                townName = forceString(record.value('TOWN_NAME'))
                kladrCode = self.getSpbKladrCode(townName)
            elif region == '47':
                oblTownType = forceString(record.value('OBL_TOWN_TYPE'))
                oblTownName =forceString(record.value('OBL_TOWN_NAME'))
                kladrCode = self.getLoKladrCode(oblTownType, oblTownName)
        kladrStreetCode = None
        number = corpus = flat = None
        if kladrCode:
            streetType = forceString(record.value('STREET_TYPE'))
            prefixId = forceRef(record.value('ID_PREFIX'))
            if streetType == '-':
                streetType = u'ул.'
            streetName = self.fixStreenName(forceStringEx(record.value('STREET')))
            if streetType and streetName:
                street = streetType + ' ' + streetName
                kladrStreetCode = self.get_KLADRStreetCode(street, kladrCode, None) #!!!! :(
            if not kladrStreetCode and freeInput:
                street = get_street(freeInput)
                if street:
                    kladrStreetCode = self.get_KLADRStreetCode(street, kladrCode, None)
            if not kladrStreetCode and prefixId:
                kladrStreetCode = self.getKLADRStreetCodeByPrefix(kladrCode, streetType, streetName, prefixId)

            if kladrStreetCode:
                number = forceString(record.value('HOUSE'))
                corpus = forceString(record.value('KORPUS'))
                flat   = forceString(record.value('FLAT'))
        return { 'KLADRCode'      : kladrCode,
                 'KLADRStreetCode': kladrStreetCode,
                 'number'         : number,
                 'corpus'         : corpus,
                 'flat'           : flat,
                 'freeInput'      : freeInput
               }



    def getSpbKladrCode(self, townName):
        # получить код КЛАДР для части Петербурга

        if townName.lower() in ('-', u'неизвестно'):
            townName = ''

        kladrCode =self.mapSpbTownToKladrCode.get(townName, None)
        if kladrCode is not None:
            return kladrCode

        kladrCode = ''
        socr = name = None

        if townName.startswith(u'пос.'):
            socr = u'п'
            name = townName[4:]
        elif townName.startswith(u'п.'):
            socr = u'п'
            name = townName[2:]
        elif townName.startswith(u'г.'):
            socr = u'г'
            name = townName[2:]
        if socr is not None:
            db = QtGui.qApp.db
            tableKLADR = db.table('kladr.KLADR')
            cond=[ tableKLADR['CODE'].like('78%'),
                   tableKLADR['SOCR'].eq(socr),
                   tableKLADR['NAME'].eq(name.strip()),
                 ]
            record = db.getRecordEx(tableKLADR, 'CODE', cond)
            if record:
                kladrCode = forceString(record.value('CODE'))

        self.mapSpbTownToKladrCode[townName]=kladrCode
        return kladrCode


    def getLoKladrCode(self, oblTownType, oblTownName):
        # Поучить код КЛАДР для населённого пункта Ленинградской области
        key = (oblTownType, oblTownName)
        kladrCode = self.mapLoTownToKladrCode.get(key, None)
        if kladrCode is not None:
            return kladrCode

        kladrCode=''
        socr = self.mapOblTownTypeToSocr.get(oblTownType.upper(), None)
        if socr and oblTownName:
            db = QtGui.qApp.db
            tableKLADR = db.table('kladr.KLADR')
            cond=[ tableKLADR['CODE'].like('47%'),
                   tableKLADR['SOCR'].eq(socr),
                   tableKLADR['NAME'].eq(oblTownName),
                 ]
            record = db.getRecordEx(tableKLADR, 'CODE', cond)
            if record:
                kladrCode = forceString(record.value('CODE'))
        self.mapLoTownToKladrCode[key]=kladrCode
        return kladrCode


    mapBadStreetNameToFixedOne = { u'Большой В.О.':u'Большой ВО',
                                   u'Большой П.С.':u'Большой ПС',
                                   u'Малый В.О.'  :u'Малый ВО',
                                   u'Малый П.С.'  :u'Малый ПС'
                                 }


    def fixStreenName(self, name):
        # в ЕИС ОМС некоторые улицы называются не так, как в КЛАДР
        # иногда это можно исправить
        if name and name[0].isdigit():
            parts = name.split()
            name = ' '.join(parts[1:] + parts[:1])
        return self.mapBadStreetNameToFixedOne.get(name, name)


    def getKLADRStreetCodeByPrefix(self, kladrCode, streetType, streetName, prefixId):
        db = QtGui.qApp.db
        tableStreet = db.table('kladr.STREET')
        cond=[ # tableStreet['NAME'].eq(streetName),
               # tableStreet['SOCR'].eq(streetType),
               tableStreet['CODE'].like(kladrCode[:11]+'%'),
               tableStreet['CODE'].like('%00'),
               tableStreet['eisPrefix'].eq(prefixId),
             ]

        list = db.getRecordList(tableStreet, where=cond)
        if list:
            return forceString(list[0].value('CODE'))
        return None


    def setOrUpdateAttach(self, clientId, eisPatient):
        db = QtGui.qApp.db
        deathDate = forceDate(db.translate('Client', 'id', clientId, 'deathDate'))
        if deathDate:
            return
        eisLpuId = eisPatient.lpuId
        lpuId = self.findLpu(eisLpuId)
        if lpuId:
            tableClientAttach = db.table('ClientAttach')
            tableAttachType   = db.table('rbAttachType')
            table = tableClientAttach.leftJoin(tableAttachType, tableClientAttach['attachType_id'].eq(tableAttachType['id']))
            cond = [tableClientAttach['client_id'].eq(clientId),
                    tableClientAttach['deleted'].eq(0),
                    db.joinOr([tableClientAttach['endDate'].isNull(),
                               tableClientAttach['endDate'].dateGe(self.tmonthBegDate.addDays(-1))
                              ]
                             ),
                    tableAttachType['temporary'].eq(0),
                    tableAttachType['finance_id'].eq(self.omsFinanceId)
                   ]
            cols = [tableClientAttach['id'],
                    tableClientAttach['attachType_id'],
                    tableClientAttach['endDate'],
                    tableClientAttach['LPU_id']
                   ]
            records = db.getRecordList(table, cols, cond, tableClientAttach['id'].name())
            for record in records[:-1]:
                record.setValue('endDate', self.tmonthBegDate.addDays(-1))
                db.updateRecord(tableClientAttach, record)
            if records:
                record = records[-1]
                if forceRef(record.value('LPU_id')) == lpuId:
                    record.setValue('endDate', None)
                    record.setValue('attachType_id', self.attachTypeId)
                    db.updateRecord(tableClientAttach, record)
                    return
                else:
                    record.setValue('endDate', self.tmonthBegDate.addDays(-1))
                    db.updateRecord(tableClientAttach, record)

            attachRecord = tableClientAttach.newRecord()
            attachRecord.setValue('client_id', clientId)
            attachRecord.setValue('attachType_id', self.attachTypeId)
            attachRecord.setValue('LPU_id', lpuId)
            attachRecord.setValue('begDate', self.tmonthBegDate)
            attachRecord.setValue('endDate', None)
            db.insertRecord(tableClientAttach, attachRecord)
        else:
            message = u'Не найдена организация для прикрепления'
            extMessage = 'ID_LPU=%s' % eisLpuId
            self.logMessage(eisPatient, message, extMessage)


    def findLpu(self, eisLpuId):
        orgId = self.mapEisLpuIdToOrgId.get(eisLpuId, False)
        if orgId is False:
            db = QtGui.qApp.db
            tableOrganisation = db.table('Organisation')
            orgIdList = db.getIdList(tableOrganisation,
                                     where=[ tableOrganisation['deleted'].eq(0),
                                             tableOrganisation['isMedical'].ne(0),
                                             tableOrganisation['tfomsExtCode'].eq(eisLpuId),
                                           ]
                                    )
            orgId = orgIdList[0] if orgIdList else None
            self.mapEisLpuIdToOrgId[eisLpuId] = orgId
        return orgId


    def setOrUpdateIdentification(self, clientId, eisPatient):
        db = QtGui.qApp.db
        tableClientIdentification = db.table('ClientIdentification')
        for accountingSystemId, identifier in [ (self.ClientIdentification_ID_HISTORY, eisPatient.historyId),
                                                (self.ClientIdentification_ID_HUMAN,   eisPatient.humanId)
                                              ]:
            if identifier:
                cond=[ tableClientIdentification['accountingSystem_id'].eq(accountingSystemId),
                       tableClientIdentification['deleted'].eq(0),
                       tableClientIdentification['client_id'].eq(clientId),
                     ]
                recordList = db.getRecordList(tableClientIdentification, '*', cond, 'id')
                if recordList:
                    for record in recordList[:-1]:
                        db.deleteRecord(tableClientIdentification, tableClientIdentification['id'].eq(record.value('id')))
                    record = recordList[-1]
                    record.setValue('checkDate', self.tmonthEndDate)
                    db.updateRecord(tableClientIdentification, record)
                else:
                    record = tableClientIdentification.newRecord()
                    record.setValue('client_id',  clientId)
                    record.setValue('accountingSystem_id', accountingSystemId)
                    record.setValue('identifier', identifier)
                    record.setValue('checkDate', self.tmonthEndDate)
                    db.insertRecord(tableClientIdentification, record)


################################################################################
# переделать:


    def getDocumentTypeIdByEisId(self, eisDocumentTypeId):
        result = self.mapEisDocumentTypeIdToDocTypeId.get(eisDocumentTypeId, False)
        if result is False:
            db = QtGui.qApp.db
            tableDocumentType = db.table('rbDocumentType')
            tableDocumentTypeGroup = db.table('rbDocumentTypeGroup')
            table = tableDocumentType.leftJoin(tableDocumentTypeGroup,
                                               tableDocumentTypeGroup['id'].eq(tableDocumentType['group_id']))
            cond  = [ tableDocumentType['regionalCode'].eq(eisDocumentTypeId),
                      tableDocumentTypeGroup['code'].eq('1'),  # удостоверения личности
                    ]
            record = db.getRecordEx(table,
                                    [tableDocumentType['id']],
                                    cond,
                                    tableDocumentType['code'].name()+' DESC'
                                   )
            result = forceInt(record.value(0)) if record else None
            self.mapEisDocumentTypeIdToDocTypeId[eisDocumentTypeId] = result
        return result


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        if self.importRun:
            self.abort=True
        else:
            self.close()


    @pyqtSignature('')
    def on_btnImport_clicked(self):
        self.btnImport.setEnabled(False)
        self.btnClose.setText(u'Прервать')
        self.abort=False
        self.importRun=True
        QtGui.qApp.call(self, self.startImport)
        self.progressBar.setFormat(u'прервано' if self.abort else u'готово')
        if self.progressBar.maximum() == 0:
            self.progressBar.setMaximum(1)
            self.progressBar.setValue(1)

        self.btnImport.setEnabled(True)
        self.btnClose.setText(u'Закрыть')
        self.abort=False
        self.importRun=False


def get_street(UNSTRUCT_ADDRESS):
    street=UNSTRUCT_ADDRESS
    if UNSTRUCT_ADDRESS.startswith(u'г.Санкт-Петербург'):
        return get_ul(UNSTRUCT_ADDRESS[17:].lstrip(' ,'))
    for (n, s) in ns_list:
        l=len(n)
        pos=street.find(u', '+n)
        if pos>=0:
            street=street[pos+2:]
            pos2=street.find(u',')
            if pos2>=0:
                street=street[:pos2].strip()
            return street
        pos=street.find(n+',')
        if pos>=0:
            street=street[:pos+l]
            pos2=street.rfind(u',')
            if pos2>=0:
                street=street[pos2:].strip()
            return street
    return None


ul_types=[
    u'ул.', u'наб.', u'ал.', u'б-р', u'дор.', u'дорожка', u'линия', u'пер.', u'пл.', u'пр.', u'пр-д', u'ш.', u'тупик', u'остров', u'парк', u'км', u'бск']


def get_ul(street):
    for ut in ul_types:
        pos=street.find(ut)
        if pos>0:
            return street[:pos+len(ut)]
    return None



#
# added ########################################################################
#

class CEisPatient:
    def __init__(self, importFromMu, record):
        self.historyId = forceString(record.value('ID_HISTORY')) # в PEOPLES
        self.humanId   = forceString(record.value('ID_HUMAN'))   # в PATIENTS

        self.lastName  = nameCase(forceStringEx(record.value('SURNAME')))
        self.firstName = nameCase(forceStringEx(record.value('NAME')))
        self.patrName  = nameCase(forceStringEx(record.value('SECOND_NAME')))
        if self.patrName == '-':
            self.patrName = ''
        self.sex       = parseSex(forceString(record.value('SEX')))
        self.birthDate = forceDate(record.value('BIRTHDAY'))
        self.snils     = unformatSNILS(forceString(record.value('SNILS')))
        if not checkSNILS(self.snils):
            self.snils = ''

        self.smoId         = forceRef(record.value('ID_SMO'))
        self.regionalSmoId = forceRef(record.value('ID_SMO_REGION'))
        self.policyTypeId  = forceRef(record.value('ID_POLIS_TYPE'))
        self.policySerial  = forceStringEx(record.value('POLIS_SERIA'))
        self.policyNumber  = forceStringEx(record.value('POLIS_NUMBER'))
        self.policyBegDate = forceDate(record.value('POLIS_BEGIN_DATE')) or None
        self.policyEndDate = forceDate(record.value('POLIS_END_DATE')) or None

        self.docTypeId     = forceInt(record.value('ID_DOC_TYPE'))
        self.docSerialLeft = forceStringEx(record.value('SERIA_LEFT'))
        self.docSerialRight= forceStringEx(record.value('SERIA_RIGHT'))
        self.docNumber     = forceStringEx(record.value('DOC_NUMBER'))
        self.docDate       = forceDate(record.value('ISSUE_DATE')) or None

        if importFromMu:
            self.registrationAddressId = forceString(record.value('ID_ADDRESS_REG'))
            self.locationAddressId     = forceString(record.value('ID_ADDRESS_LOC'))
        else:
            self.registrationAddressId = forceRef(record.value('ID_ADDRESS_REGISTRATION'))
            self.locationAddressId     = forceRef(record.value('ID_ADDRESS_LOCATION'))

        self.tmonth = forceInt(record.value('TMONTH_BEGIN'))
        self.humanTypeId = forceRef(record.value('ID_HUMAN_TYPE'))
        if self.humanTypeId is None:
            self.humanTypeId = 6
        self.lpuId = forceRef(record.value('ID_LPU'))


#
# ##############################################################################
#

class CFileLog(object):
    def __init__(self, parent, fileName=None, addCurrentDateToFileName=False):
        assert isinstance(parent, QtGui.QWidget)
        self.logFile   = None
        self.logStream = None
        self.isTurnOn  = True
        self.addCurrentDateToFileName = addCurrentDateToFileName
        self.parent = parent
        self.fileName  = None
        if fileName:
            self.setFile(fileName)


    def turnOn(self):
        self.isTurnOn = True


    def turnOff(self):
        self.isTurnOn = False


    def setFile(self, fileName):
        try:
            self.fileName = fileName
            if self.addCurrentDateToFileName:
                cdStr = forceString(QDate.currentDate())
                if fileName[-4:] == '.log':
                    fileName = fileName[:-4]
                fileName = fileName+'_'+cdStr+'.log'
            logFile = QFile(fileName)
            logFile.open(QFile.WriteOnly | QFile.Text)
        except:
            logFile = None
            self.logStream = None
            self.fileName  = None
            QtGui.QMessageBox.critical(self.parent,
                                 u'Внимание!',
                                 u'Не удалось открыть файл "%s" на запись'%fileName,
                                 QtGui.QMessageBox.Ok,
                                 QtGui.QMessageBox.Ok)
        self.logFile = logFile
        if bool(self.logFile):
            self.logStream = QTextStream(self.logFile)


    def getDatetimePart(self):
        if self.addCurrentDateToFileName:
            return unicode(QTime.currentTime().toString('hh:mm:ss'))
        return unicode(QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss'))


    def addMessage(self, msg):
        if self.isTurnOn and self.logStream:
            self.logStream << self.getDatetimePart() << '---'
            self.logStream << msg << '\n'
            self.logStream.flush()


    def addErrorMessage(self, msg):
        self.addMessage(msg)


    def close(self):
        self.logFile.close()
