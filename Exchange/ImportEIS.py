# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import re

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDateTime, QFile, QTextStream, QTime, QVariant, pyqtSignature

from library.AgeSelector import convertAgeSelectorToAgeRange
from library.Utils import forceDate, forceInt, forceRef, forceString, getVal, nameCase, toVariant, trim

from Exchange.Cimport import CEISimport, Cimport, ns_list
from Exchange.Utils import EIS_close, findAndUpdateOrCreateRecord, getId, setEIS_db, tbl
from Orgs.Utils import CNet, getOrgStructureNetId
from Registry.Utils import getClientCompulsoryPolicy

from Exchange.Ui_ImportEIS import Ui_Dialog


def ImportEIS(widget):
    try:
        setEIS_db()
        dlg=CImportEIS(widget, QtGui.qApp.EIS_db)
        dlg.exec_()
    except:
        QtGui.qApp.logCurrentException()
        EIS_close()


class CFileLog(object):
    def __init__(self, parent, fileName=None, fnWithDate=False):
        assert isinstance(parent, QtGui.QWidget)
        self.logFile   = None
        self.logStream = None
        self.isTurnOn  = True
        self.addCurrentDateToFileName = fnWithDate
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


class CImportEIS(CEISimport, QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent, EIS_db):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setupAges()

        Cimport.__init__(self, self.logBrowser)
        self.progressBar.setFormat('%v')
        self.fileLog = CFileLog(self, fileName='importEIS.log', fnWithDate=False)
        self.EIS_db=EIS_db
        self.EP_NUMBER=''
        self.ID_HISTORY=''
        self.ID_PATIENT=''
        self.TOWN_KLADR={}
        self.OBL_TOWN_KLADR={}
        self.smo_id={}
        self.lpuCache={}
        self.mapeisDocumentTypeIdToDocTypeId = {}
        self.tableClientIdentification=tbl('ClientIdentification')
        self.tableClientAttach=tbl('ClientAttach')
        self.tableOrganisation=tbl('Organisation')
        self.ClientIdentification_EP_NUMBER=forceInt(QtGui.qApp.db.translate('rbAccountingSystem',  'code', '1', 'id'))
        self.ClientIdentification_ID_HISTORY=forceInt(QtGui.qApp.db.translate('rbAccountingSystem', 'code', '2', 'id'))
        self.ClientIdentification_ID_PATIENT=forceInt(QtGui.qApp.db.translate('rbAccountingSystem', 'code', '3', 'id'))
        self.attachTypeId=forceInt(QtGui.qApp.db.translate('rbAttachType', 'code', '078', 'id'))
        self.omsFinanceId=forceInt(QtGui.qApp.db.translate('rbFinance', 'name', u'ОМС', 'id'))
        self.identDate=None
        self.identBegDate = None
        tm=EIS_db.query('select * from TARIFF_MONTH')
        if tm.next():
            TARIFF_MONTH=tm.record()
            ID_TARIFF_MONTH=TARIFF_MONTH.value('ID_TARIFF_MONTH').toInt()[0]
            TARIFF_MONTH_BEG=forceDate(TARIFF_MONTH.value('TARIFF_MONTH_BEG'))
            TARIFF_MONTH_END=forceDate(TARIFF_MONTH.value('TARIFF_MONTH_END'))
            self.identDate=TARIFF_MONTH_END
            self.identBegDate = TARIFF_MONTH_BEG
            self.label_eis_mon.setText(
                    u'тарифный месяц ЕИС: '+str(ID_TARIFF_MONTH)+' ('+str(TARIFF_MONTH_BEG.toString(Qt.ISODate))+' - '+str(TARIFF_MONTH_END.toString(Qt.ISODate))+')')


    def setupAges(self):
        lowAge = 0
        highAge = 0

        netId = getOrgStructureNetId(QtGui.qApp.currentOrgStructureId())
        if netId:
            net = CNet(netId)
            if net.age:
                begAge, endAge = convertAgeSelectorToAgeRange(net.age)
                self.edtAgeFrom.setValue(begAge)
                self.edtAgeTo.setValue(endAge)



    def startImport(self):
        self.importMU=self.cmbPart.currentIndex() == 1
        self.importAttach=self.chkImportAttach.isChecked()
        if self.importAttach and not self.attachTypeId:
            if QtGui.QMessageBox.question( self,
                                       u'Внимание!',
                                       u'Не найден тип прикрепления ТФОМС. Добавить?',
                                       QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                       QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                tableAttachType=QtGui.qApp.db.table('rbAttachType')
                attachRecord = tableAttachType.newRecord()
                attachRecord.setValue('code', QVariant('078'))
                attachRecord.setValue('name', QVariant(u'ТФОМС'))
                attachRecord.setValue('regionalCode', QVariant('78'))
                attachRecord.setValue('temporary', QVariant(0))
                attachRecord.setValue('outcome', QVariant(0))
                attachRecord.setValue('finance_id', QVariant(self.omsFinanceId))
                self.attachTypeId = QtGui.qApp.db.insertRecord(tableAttachType, attachRecord)
                if not self.attachTypeId:
                    self.log.append(u'Ошибка записи типа прикрепления')
                    return
            else:
                self.log.append(u'Не найден тип прикрепления ТФОМС, код 078')
                return
        EIS_db=self.EIS_db
        if not EIS_db:
            return
        if self.chkLogImportRefuse.isChecked():
            self.fileLog.turnOn()
        else:
            self.fileLog.turnOff()

        QtGui.qApp.processEvents()
        TMONTH=forceInt(getVal(QtGui.qApp.preferences.appPrefs, 'TMONTH', 0))
        self.TMONTH=TMONTH
        cur_TMONTH=0
        onlyNew=self.chkOnlyNew.isChecked()
        today = QDate.currentDate()
        lowBirthdayStr=EIS_db.formatDate(today.addYears(-self.edtAgeTo.value()))
        highBirthdayStr=EIS_db.formatDate(today.addYears(-self.edtAgeFrom.value()))
        self.putSize(onlyNew, lowBirthdayStr, highBirthdayStr)
        smoFields=""", SMO.SMO_SHORT_NAME, SMO.SMO_LONG_NAME, SMO.INN, SMO.OKPO, SMO.ADDRESS, SMO.JUR_ADDRESS, SMO.CODE, SMO.KPP, SMO.IS_ACTIVE, SMO.REMARK, SMO.LIC_NUMBER, SMO.LIC_DATE_BEG, SMO.LIC_DATE_END, SMO.BANK, SMO.FILIAL, SMO.BIK, SMO.PC, SMO.PC2"""

        if self.importMU:
            stmt="""
SELECT
PATIENTS.ID_PATIENT, PATIENTS.ID_EIS_OMS AS ID_HISTORY, PATIENT_DATA.EP_NUMBER,
PATIENT_DATA.SURNAME, PATIENT_DATA.NAME, PATIENT_DATA.SECOND_NAME, PATIENT_DATA.BIRTHDAY, PATIENT_DATA.SEX,
PATIENT_DATA.ID_DOC_TYPE, PATIENT_DATA.SERIA_LEFT, PATIENT_DATA.SERIA_RIGHT, PATIENT_DATA.DOC_NUMBER,
PATIENT_DATA.ID_ADDRESS_REG AS ID_ADDRESS_REGISTRATION, PATIENT_DATA.ID_ADDRESS_LOC AS ID_ADDRESS_LOCATION,
PATIENT_DATA.SNILS,
PATIENT_POLIS.POLIS_SERIA, PATIENT_POLIS.POLIS_NUMBER, PATIENT_POLIS.ID_SMO, PATIENT_POLIS.SMO_NAME
"""+smoFields+"""
FROM
PATIENTS
LEFT JOIN PATIENT_DATA ON PATIENT_DATA.ID_PATIENT=PATIENTS.ID_PATIENT
LEFT JOIN PATIENT_POLIS ON PATIENT_POLIS.ID_PATIENT=PATIENTS.ID_PATIENT
LEFT JOIN SMO ON SMO.ID_SMO=PATIENT_POLIS.ID_SMO
            """
        else:
            stmt="""
SELECT
PEOPLE.ID_HISTORY, PEOPLE.EP_NUMBER,
PEOPLE.SURNAME, PEOPLE.NAME, PEOPLE.SECOND_NAME, PEOPLE.SEX, PEOPLE.BIRTHDAY,
PEOPLE.ID_SMO, PEOPLE.POLIS_SERIA, PEOPLE.POLIS_NUMBER, PEOPLE.POLIS_BEGIN_DATE, PEOPLE.POLIS_END_DATE,
PEOPLE.ID_DOC_TYPE, PEOPLE.SERIA_LEFT, PEOPLE.SERIA_RIGHT, PEOPLE.DOC_NUMBER,
PEOPLE.ID_ADDRESS_REGISTRATION, PEOPLE.ID_ADDRESS_LOCATION,
PEOPLE.TMONTH_BEGIN, PEOPLE.ID_HUMAN_TYPE, PEOPLE.ID_LPU
"""+smoFields+"""
FROM
PEOPLE
LEFT JOIN SMO ON SMO.ID_SMO=PEOPLE.ID_SMO
            """
        if self.importMU:
#            if onlyNew:
            stmt+="""
            WHERE NOT EXISTS (SELECT * FROM PEOPLE WHERE
            (PEOPLE.ID_HISTORY IS NOT NULL AND PEOPLE.ID_HISTORY=PATIENTS.ID_EIS_OMS) OR
            (PEOPLE.EP_NUMBER IS NOT NULL AND PEOPLE.EP_NUMBER=PATIENT_DATA.EP_NUMBER))
            AND PATIENT_DATA.BIRTHDAY BETWEEN %s AND %s""" % (lowBirthdayStr, highBirthdayStr)
        else:
            stmt+='WHERE PEOPLE.BIRTHDAY BETWEEN %s AND %s' % (lowBirthdayStr, highBirthdayStr)
            if onlyNew:
                stmt+=' AND PEOPLE.TMONTH_BEGIN>='+str(TMONTH)
#                stmt+=' AND EP_NUMBER=7801955122900256'
            stmt+=' ORDER BY PEOPLE.TMONTH_BEGIN'
        query = EIS_db.query(stmt)
        query.setForwardOnly(True)
        num=query.size()
        n=0
        self.num_added=0
        self.num_found=0
        self.num_fixed=0
        QtGui.qApp.db.transaction()
        try:
            while query.next():
                QtGui.qApp.processEvents()
                if self.abort:
                    break
                n+=1
                if self.num<=0:
                    self.labelNum.setText(u'всего записей в источнике: '+str(n))
                self.n=n

                if n % 50 == 0:
                    QtGui.qApp.db.commit()
                    TMONTH=max(TMONTH, cur_TMONTH)
                    QtGui.qApp.db.transaction()

                record = query.record()
                self.record=record

                if not self.importMU:
                    cur_TMONTH=record.value('TMONTH_BEGIN').toInt()[0]
                    self.label_cur_mon.setText(u'загруженный тарифный месяц: '+str(cur_TMONTH))

                clientId=self.processClientId()
                if clientId:
                    ID_ADDRESS_REGISTRATION=record.value('ID_ADDRESS_REGISTRATION')
                    clientAddressFields=self.getClientAddressFields(clientId, ID_ADDRESS_REGISTRATION)
                    if clientAddressFields:
                        findAndUpdateOrCreateRecord(self.tableClientAddress, clientAddressFields+[('type', 0)])
                    ID_ADDRESS_LOCATION=record.value('ID_ADDRESS_LOCATION')
                    if ID_ADDRESS_LOCATION!=ID_ADDRESS_REGISTRATION:
                        clientAddressFields=self.getClientAddressFields(clientId, ID_ADDRESS_LOCATION)
                    if clientAddressFields:
                        findAndUpdateOrCreateRecord(self.tableClientAddress, clientAddressFields+[('type', 1)])
                    if self.importAttach:
                        self.parceClientAttach(clientId, forceInt(record.value('ID_LPU')))

                self.progressBar.setValue(n)
                statusText = u'добавлено %d, найдено %d, исправлено %d' \
                    % (self.num_added, self.num_found, self.num_fixed)
                self.statusLabel.setText(statusText)
        finally:
            QtGui.qApp.db.commit()
            self.fileLog.close()
        if not self.importMU:
            TMONTH=max(TMONTH, cur_TMONTH)
            QtGui.qApp.preferences.appPrefs['TMONTH'] = toVariant(TMONTH)
        self.progressBar.setValue(n-1)



    def err2log(self, e, errorInfo=None):
        if self.log:
            s = ("; ID_PATIENT = "+self.ID_PATIENT) if self.importMU else ""
            errorMessage = u'запись '+str(self.n)+' (EP_NUMBER = '+self.EP_NUMBER+'; ID_HISTORY = '+str(self.ID_HISTORY)+s+'): '+e
            self.log.append(errorMessage)
            if errorInfo:
                self.fileLog.addErrorMessage(errorMessage+'\n'+errorInfo)


    def parceClientAttach(self, clientId, eisLpu):
        tableClient = self.db.table('Client')
        dead = forceDate(self.db.translate(tableClient, 'id', clientId, 'deathDate'))
        if dead and dead.isValid():
            return
        lpuId = self.findLPU(eisLpu)
        clientAttachRecord = None
        if lpuId:
            tableAttachType=QtGui.qApp.db.table('rbAttachType')
            table = self.tableClientAttach.leftJoin(tableAttachType, self.tableClientAttach['attachType_id'].eq(tableAttachType['id']))
            cond = [self.tableClientAttach['client_id'].eq(clientId),
                    self.tableClientAttach['deleted'].eq(0),
                    self.db.joinOr([self.tableClientAttach['endDate'].isNull(), self.tableClientAttach['endDate'].dateGe(self.identBegDate.addDays(-1))]),
                    tableAttachType['temporary'].eq(0),
                    tableAttachType['finance_id'].eq(self.omsFinanceId)
                   ]
            cols = [self.tableClientAttach['id'],
                    self.tableClientAttach['attachType_id'],
                    self.tableClientAttach['endDate'],
                    self.tableClientAttach['LPU_id']
                   ]
            records = self.db.getRecordList(table, cols, cond)
            for record in records:
                if forceInt(record.value('LPU_id')) == lpuId:
                    clientAttachRecord = record
                record.setValue('endDate', self.identBegDate.addDays(-1))
                self.db.updateRecord(self.tableClientAttach, record)
            if not clientAttachRecord:
                attachRecord = self.tableClientAttach.newRecord()
                attachRecord.setValue('client_id', QVariant(clientId))
                attachRecord.setValue('attachType_id', QVariant(self.attachTypeId))
                attachRecord.setValue('LPU_id', QVariant(lpuId))
                attachRecord.setValue('begDate', QVariant(self.identBegDate))
                attachRecord.setValue('endDate', QVariant(self.identDate))
                self.db.insertRecord(self.tableClientAttach, attachRecord)
            else:
                clientAttachRecord.setValue('attachType_id', QVariant(self.attachTypeId))
                clientAttachRecord.setValue('endDate', QVariant(self.identDate))
                self.db.updateRecord(self.tableClientAttach, clientAttachRecord)
        else:
            errorMessage = u'Не найдена организация для прикрепления'
            errorInfo = 'ID_LPU=%s' % eisLpu
            self.err2log(errorMessage, errorInfo)


    def findLPU(self, eisLPU):
        lpuId = self.lpuCache.get(eisLPU, None)
        if not lpuId:
            lpuId = forceInt(self.db.translate(self.tableOrganisation, 'tfomsExtCode', eisLPU, 'id'))
            self.lpuCache[eisLPU] = lpuId
        return lpuId


    def getClientIdentificationId(self, identifier, accountingSystemId):
        if not identifier:
            return None
        cond=[self.tableClientIdentification['identifier'].eq(identifier),
              self.tableClientIdentification['accountingSystem_id'].eq(accountingSystemId),
              self.tableClientIdentification['deleted'].eq(0),
             ]
        ident=self.db.getRecordEx(self.tableClientIdentification, '*', cond)
        if ident:
            clientId=ident.value('client_id').toInt()[0]
            if self.identDate and not self.importMU:
                ident.setValue('checkDate', toVariant(self.identDate))
                self.db.updateRecord(self.tableClientIdentification, ident)
            return clientId
        return None


    def getIdentClient(self, EP_NUMBER, ID_HISTORY=None, ID_PATIENT=None):
        id1=self.getClientIdentificationId(EP_NUMBER, self.ClientIdentification_EP_NUMBER)
        id2=self.getClientIdentificationId(ID_HISTORY, self.ClientIdentification_ID_HISTORY)
        id3=self.getClientIdentificationId(ID_PATIENT, self.ClientIdentification_ID_PATIENT)
        return (id1, id2, id3)


    def getInsurer(self):
        record=self.record
        ID_SMO=record.value('ID_SMO').toInt()[0]
        if not ID_SMO:
            return None
        insurerId=None
        org_id=self.smo_id.get(ID_SMO, -1)
        if org_id != -1:
            return org_id
        org_id=None
        SMO_SHORT_NAME=forceString(record.value('SMO_SHORT_NAME'))
        SMO_LONG_NAME=forceString(record.value('SMO_LONG_NAME'))
        insurerId=self.get_insurerId(SMO_SHORT_NAME)
        INN=forceString(record.value('INN'))
        CODE=forceString(record.value('CODE'))
        if not insurerId:
            OKPO=forceString(record.value('OKPO'))
            ADDRESS=forceString(record.value('ADDRESS'))
            JUR_ADDRESS=forceString(record.value('JUR_ADDRESS'))
            KPP=forceString(record.value('KPP'))
            if INN:
                insurerId=self.getOrganisationId(INN, 'shortName', SMO_SHORT_NAME)
                if not insurerId:
                    insurerId=self.getOrganisationId(INN, 'title', SMO_SHORT_NAME)
                if not insurerId:
                    insurerId=self.getOrganisationId(INN, 'shortName', SMO_LONG_NAME)
                if not insurerId:
                    insurerId=self.getOrganisationId(INN, 'fullName', SMO_LONG_NAME)
        if not insurerId and CODE:
            insurerId=forceInt(QtGui.qApp.db.translate('Organisation', 'infisCode', CODE, 'id'))

        if insurerId:
            IS_ACTIVE=forceString(record.value('IS_ACTIVE'))
            tblOrg=tbl('Organisation')
            cond=[tblOrg['id'].eq(toVariant(insurerId))]
            record=QtGui.qApp.db.getRecordEx(tblOrg, '*', where=cond)
            if IS_ACTIVE=='1':
                REMARK=forceString(record.value('REMARK'))
                LIC_NUMBER=forceString(record.value('LIC_NUMBER'))
                LIC_DATE_BEG=forceDate(record.value('LIC_DATE_BEG'))
                LIC_DATE_END=forceDate(record.value('LIC_DATE_END'))
                KPP=forceString(record.value('KPP'))
                notes=REMARK+u'; лиц. '+LIC_NUMBER+u', с '+forceString(LIC_DATE_BEG)+u' по '+forceString(LIC_DATE_END)
                record.setValue('notes', toVariant(notes))
                record.setValue('infisCode', toVariant(CODE))
                record.setValue('title', toVariant(SMO_SHORT_NAME))
                record.setValue('shortName', toVariant(SMO_SHORT_NAME))
                record.setValue('fullName', toVariant(SMO_LONG_NAME))
                record.setValue('INN', toVariant(INN))
                record.setValue('KPP', toVariant(KPP))
                BIK=forceString(record.value('BIK'))
                BANK=forceString(record.value('BANK'))
                FILIAL=forceString(record.value('FILIAL'))
                if FILIAL==u'-':
                    FILIAL=u''
                PC2=forceString(record.value('PC2'))
                tblBank=tbl('Bank')
                BankFields=[('BIK', BIK), ('branchName', FILIAL)]
                BankFields2=[('name', BANK), ('corrAccount', PC2), ('subAccount', '')]
                BankId=findAndUpdateOrCreateRecord(tblBank, BankFields, BankFields2)
                tblOrganisation_Account=tbl('Organisation_Account')
                Organisation_AccountFields=[
                    ('organisation_id', insurerId), ('bankName', BANK), ('name', PC2),
                    ('bank_id', BankId)]
                Organisation_AccountId=getId(tblOrganisation_Account, Organisation_AccountFields)
            else:
                record.setValue('notes', toVariant(u'не действует'))
            QtGui.qApp.db.updateRecord(tblOrg, record)


        self.smo_id[ID_SMO]=insurerId
        return insurerId


    def getClientAddressFields(self, clientId, ID_ADDRESS_RECORD):
        ID_ADDRESS = ("'"+forceString(ID_ADDRESS_RECORD)+"'") if self.importMU else ID_ADDRESS_RECORD.toInt()[0]
        EIS_db=self.EIS_db
        str1=""",
OBL_TOWN.OBL_TOWN_CODE, OBL_TOWN.OBL_TOWN_NAME, OBL_TOWN.OBL_TOWN_TYPE,
TOWN.TOWN_NAME, GEONIM_NAME.GEONIM_NAME, T_GEONIM.GEONIM_TYPE_NAME
        """
        str2="""
LEFT JOIN TOWN ON TOWN.ID_TOWN=PREFIX.ID_TOWN
LEFT JOIN GEONIM_NAME ON GEONIM_NAME.ID_GEONIM_NAME=PREFIX.ID_GEONIM_NAME
LEFT JOIN T_GEONIM ON T_GEONIM.ID_GEONIM_TYPE=PREFIX.ID_GEONIM_TYPE
        """
        if self.importMU:
            stmt="""
SELECT
PATIENT_ADDRESS.ADDRESS_TYPE, PATIENT_ADDRESS.FLAT, PATIENT_ADDRESS.UNSTRUCT_ADDRESS, PATIENT_ADDRESS.ID_OKATO_REGION AS REGION_CODE,
PATIENT_ADDRESS.HOUSE, PATIENT_ADDRESS.KORPUS
"""+str1+"""
FROM
PATIENT_ADDRESS
LEFT JOIN OBL_TOWN ON OBL_TOWN.ID_OBL_TOWN=PATIENT_ADDRESS.ID_OBL_TOWN
LEFT JOIN PREFIX ON PREFIX.ID_PREFIX=PATIENT_ADDRESS.ID_PREFIX
"""+str2+"""
WHERE
PATIENT_ADDRESS.ID_ADDRESS="""+unicode(ID_ADDRESS)
        else:
            stmt="""
SELECT
ADDRESSES.ADDRESS_TYPE, ADDRESSES.FLAT, ADDRESSES.UNSTRUCT_ADDRESS, ADDRESSES.REGION_CODE,
HOUSE.HOUSE, HOUSE.KORPUS
"""+str1+"""
FROM
ADDRESSES
LEFT JOIN HOUSE ON HOUSE.ID_HOUSE=ADDRESSES.ID_HOUSE
LEFT JOIN PREFIX ON PREFIX.ID_PREFIX=HOUSE.ID_PREFIX
LEFT JOIN OBL_TOWN ON OBL_TOWN.ID_OBL_TOWN=ADDRESSES.ID_OBL_TOWN
"""+str2+"""
WHERE
ADDRESSES.ID_ADDRESS_RECORD="""+str(ID_ADDRESS)
        query = EIS_db.query(stmt)
        query.setForwardOnly(True)
        if not query.next():
            return None
        record = query.record()
        UNSTRUCT_ADDRESS=forceString(record.value('UNSTRUCT_ADDRESS'))
        HOUSE=forceString(record.value('HOUSE'))
        FLAT=forceString(record.value('FLAT'))
#        if not HOUSE or not FLAT:
#            return None

        KLADRCode=None
        REGION_CODE=record.value('REGION_CODE').toInt()[0]
        if REGION_CODE==78:
            if UNSTRUCT_ADDRESS.startswith(u'г.Санкт-Петербург '):
                KLADRCode='7800000000000'
            else:
                TOWN_NAME=forceString(record.value('TOWN_NAME'))
                KLADRCode=self.getTOWN_KLADR(TOWN_NAME)
        elif REGION_CODE==47:
            OBL_TOWN_NAME=forceString(record.value('OBL_TOWN_NAME'))
            OBL_TOWN_TYPE=forceString(record.value('OBL_TOWN_TYPE'))
            KLADRCode=self.getOBL_TOWN_KLADR(OBL_TOWN_NAME, OBL_TOWN_TYPE)

        if KLADRCode:
            KLADRStreetCode=None
            GEONIM_NAME=getGEONIM_NAME(record.value('GEONIM_NAME'))
            GEONIM_TYPE_NAME=forceString(record.value('GEONIM_TYPE_NAME'))
            if GEONIM_TYPE_NAME==u'-':
                GEONIM_TYPE_NAME=u'ул.'
            if GEONIM_NAME and GEONIM_TYPE_NAME:
                street=GEONIM_NAME+' '+GEONIM_TYPE_NAME
                KLADRStreetCode=forceString(self.get_KLADRStreetCode(street, KLADRCode, None))
            if not KLADRStreetCode and UNSTRUCT_ADDRESS:
                street=get_street(UNSTRUCT_ADDRESS)
                if street:
                    KLADRStreetCode=forceString(self.get_KLADRStreetCode(street, KLADRCode, None))

            if KLADRStreetCode:
                KORPUS=forceString(record.value('KORPUS'))
                houseFields=[
                    ('KLADRCode', KLADRCode), ('KLADRStreetCode', KLADRStreetCode),
                    ('number', HOUSE)]
                if KORPUS:
                    houseFields.append(('corpus', KORPUS))
                houseId=getId(self.tableAddressHouse, houseFields)
                if houseId:
                    addressFields=[('house_id', houseId), ('flat', FLAT)]
                    addressId=getId(self.tableAddress, addressFields)
                    if addressId:
                        clientAddressFields=[('client_id', clientId), ('address_id', addressId)]
                        if UNSTRUCT_ADDRESS:
                            clientAddressFields.append(('freeInput', UNSTRUCT_ADDRESS))
                        return clientAddressFields

        if UNSTRUCT_ADDRESS:
            clientAddressFields=[('client_id', clientId), ('freeInput', UNSTRUCT_ADDRESS)]
            return clientAddressFields

        return None

    def getOBL_TOWN_KLADR(self, OBL_TOWN_NAME, OBL_TOWN_TYPE):
        if not OBL_TOWN_NAME or not OBL_TOWN_TYPE:
            return None
        key=(OBL_TOWN_NAME, OBL_TOWN_TYPE)
        KLADRCode=self.OBL_TOWN_KLADR.get(key, -1)
        if KLADRCode != -1:
            return KLADRCode
        KLADRCode=None
        SOCR=getOBL_TOWN_SOCR(OBL_TOWN_TYPE)
        if OBL_TOWN_NAME and SOCR:
            cond=[]
            cond.append(self.tableKLADR['parent'].like('47%'))
            cond.append(self.tableKLADR['NAME'].eq(toVariant(OBL_TOWN_NAME)))
            cond.append(self.tableKLADR['SOCR'].eq(toVariant(SOCR)))
            KLADRRecord=QtGui.qApp.db.getRecordEx(self.tableKLADR, 'CODE', where=cond)
            if KLADRRecord:
                KLADRCode=forceString(KLADRRecord.value('CODE'))
        self.OBL_TOWN_KLADR[key]=KLADRCode
        return KLADRCode

    def getTOWN_KLADR(self, TOWN_NAME):
        if not TOWN_NAME:
            return None
        KLADRCode=self.TOWN_KLADR.get(TOWN_NAME, -1)
        if KLADRCode != -1:
            return KLADRCode
        KLADRCode=None
        (NAME, SOCR)=(None, None)
        if TOWN_NAME.startswith(u'пос. '):
            NAME=TOWN_NAME[5:]
            SOCR=u'п'
        elif TOWN_NAME.startswith(u'п.'):
            NAME=TOWN_NAME[2:]
            SOCR=u'п'
        elif TOWN_NAME.startswith(u'г.'):
            NAME=TOWN_NAME[2:]
            SOCR=u'г'
        if NAME and SOCR:
            cond=[]
            cond.append(self.tableKLADR['parent'].like('78%'))
            cond.append(self.tableKLADR['NAME'].eq(toVariant(NAME)))
            cond.append(self.tableKLADR['SOCR'].eq(toVariant(SOCR)))
            KLADRRecord=QtGui.qApp.db.getRecordEx(self.tableKLADR, 'CODE', where=cond)
            if KLADRRecord:
                KLADRCode=forceString(KLADRRecord.value('CODE'))
        self.TOWN_KLADR[TOWN_NAME]=KLADRCode
        return KLADRCode


    def processClientId(self):
        record=self.record
        ID_HISTORY=record.value('ID_HISTORY').toInt()[0]
#        EP_NUMBER=forceString(record.value('EP_NUMBER'))
        EP_NUMBER=''
        ID_PATIENT=forceString(record.value('ID_PATIENT')) if self.importMU else ''

        self.EP_NUMBER=EP_NUMBER
        self.ID_HISTORY=ID_HISTORY
        self.ID_PATIENT=ID_PATIENT

        id1, id2, id3 = self.getIdentClient(EP_NUMBER, ID_HISTORY, ID_PATIENT)
        if id1 and id2 and id1!=id2:
            errorMessage = u'идентификаторы ID_HISTORY и EP_NUMBER указывают на разных пациентов'
            errorInfo = 'ID_HISTORY=%d, EP_NUMBER=%s'%(ID_HISTORY, EP_NUMBER)
            self.err2log(errorMessage, errorInfo)
            return None
        clientId = id2 if id2 else id1
        if self.importMU:
            if id1 and id3 and id1!=id3:
                errorMessage = u'идентификаторы ID_HISTORY и ID_PATIENT указывают на разных пациентов'
                errorInfo = 'ID_HISTORY=%d, ID_PATIENT=%s'%(ID_HISTORY, ID_PATIENT)
                self.err2log(errorMessage, errorInfo)
                return None
            if id2 and id3 and id2!=id3:
                errorMessage = u'идентификаторы EP_NUMBER и ID_PATIENT указывают на разных пациентов'
                errorInfo = 'EP_NUMBER=%s, ID_PATIENT=%s'%(EP_NUMBER, ID_PATIENT)
                self.err2log(errorMessage, errorInfo)
                return None
            if clientId:
                return None
            if id3:
                clientId=id3

        SURNAME=nameCase(forceString(record.value('SURNAME')))
        NAME=nameCase(forceString(record.value('NAME')))
        SECOND_NAME=nameCase(forceString(record.value('SECOND_NAME')))
        SEX=forceString(record.value('SEX')).upper()
        BIRTHDAY=forceDate(record.value('BIRTHDAY'))
        if not (SURNAME and NAME and SECOND_NAME and SEX and BIRTHDAY):
            return None
        sex=0
        if SEX == u'М':
            sex=1
        elif SEX == u'Ж':
            sex=2
        POLIS_SERIA=forceString(record.value('POLIS_SERIA'))
        POLIS_NUMBER=forceString(record.value('POLIS_NUMBER'))
        if self.importMU:
            POLIS_BEGIN_DATE=None
            POLIS_END_DATE=None
            ID_HUMAN_TYPE=6
        else:
            POLIS_BEGIN_DATE=forceDate(record.value('POLIS_BEGIN_DATE'))
            POLIS_END_DATE=forceDate(record.value('POLIS_END_DATE'))
            ID_HUMAN_TYPE=forceInt(record.value('ID_HUMAN_TYPE'))

        ID_DOC_TYPE = forceString(record.value('ID_DOC_TYPE'))
        documentTypeId=self.getDocumentTypeIdByEisId(ID_DOC_TYPE)
        if not documentTypeId:
            errorMessage = u'Невозможно подобрать тип документа'
            errorInfo = 'ID_DOC_TYPE=%s' % ID_DOC_TYPE
            self.err2log(errorMessage, errorInfo)
            return None

        SERIA_LEFT=forceString(record.value('SERIA_LEFT'))
        SERIA_RIGHT=forceString(record.value('SERIA_RIGHT'))
        SERIA=SERIA_LEFT+' '+SERIA_RIGHT
        DOC_NUMBER=forceString(record.value('DOC_NUMBER'))

        if clientId:
            self.num_found+=1
            Client=self.db.getRecord('Client', '*', clientId)
            lastName=forceString(Client.value('lastName'))
            firstName=forceString(Client.value('firstName'))
            patrName=forceString(Client.value('patrName'))
            if lastName!=SURNAME or firstName!=NAME or patrName!=SECOND_NAME:
                fix=False
                bad=False
                if lastName!=SURNAME and SURNAME:
                    if not lastName or numlat_re.search(lastName) is not None:
                        Client.setValue('lastName', toVariant(SURNAME))
                        fix=True
                    else:
                        bad=True
                if firstName!=NAME and NAME:
                    if not firstName or numlat_re.search(firstName) is not None:
                        Client.setValue('firstName', toVariant(NAME))
                        fix=True
                    else:
                        bad=True
                if patrName!=SECOND_NAME and SECOND_NAME:
                    if not patrName or numlat_re.search(patrName) is not None:
                        Client.setValue('patrName', toVariant(SECOND_NAME))
                        fix=True
                    else:
                        bad=True
#                if lastName!=SURNAME:
#                    Client.setValue('lastName', toVariant(SURNAME))
#                    fix=True
#                if firstName!=NAME:
#                    Client.setValue('firstName', toVariant(NAME))
#                    fix=True
#                if patrName!=SECOND_NAME:
#                    Client.setValue('patrName', toVariant(SECOND_NAME))
#                    fix=True

                if bad:
                    errorMessage = u'не совпадает ФИО'
                    errorInfo = u'lastName = %s, SURNAME = %s \nfirstName = %s, NAME = %s \npatrName=%s,  SECOND_NAME = %s' % (lastName, SURNAME, firstName, NAME, patrName, SECOND_NAME)
                    self.err2log(errorMessage, errorInfo)
                    return None
                elif fix:
                    self.num_fixed+=1
                    self.db.updateRecord(self.tableClient, Client)
            birthDate=Client.value('birthDate').toDate()
            if birthDate!=BIRTHDAY:
                errorMessage = u'не совпадает дата рождения'
#                errorInfo = u'birthDate = %s, BIRTHDAY = %s' %(forceString(birthDate), forceString(BIRTHDAY))
                self.err2log(errorMessage)
            ClientSex=Client.value('sex').toInt()[0]
            if ClientSex!=sex:
                errorMessage = u'не совпадает пол'
#                errorInfo = u'sex = %d, SEX = %d' %(ClientSex, sex)
                self.err2log(errorMessage)
            DocumentList=self.db.getRecordList(
                'ClientDocument', 'serial, number',
                'client_id=%d and documentType_id=%d' % (clientId, documentTypeId))
            if DocumentList:
                found=False
                dn = 1
                clientDocumentsStr = u''
                for Document in DocumentList:
                    serial=forceString(Document.value('serial'))
                    number=forceString(Document.value('number'))
                    clientDocumentsStr = clientDocumentsStr + '\nclientDocument %d\nserial = %s, number = %s' % (dn,serial,number)
                    dn += 1
                    if serial==SERIA and number==DOC_NUMBER:
                        found=True
                if not found:
                    errorMessage = u'не совпадает документ'
#                    errorInfo = clientDocumentsStr + '\nSERIA = %s, DOC_NUMBER = %s' % (SERIA, DOC_NUMBER)
                    self.err2log(errorMessage)
#                    return None
        else:
            client_ClientId=None
            if SURNAME and NAME and SECOND_NAME and sex and BIRTHDAY:
                cond=[]
                cond.append(self.tableClient['lastName'].eq(toVariant(SURNAME)))
                cond.append(self.tableClient['firstName'].eq(toVariant(NAME)))
                cond.append(self.tableClient['patrName'].eq(toVariant(SECOND_NAME)))
                cond.append(self.tableClient['sex'].eq(toVariant(sex)))
                cond.append(self.tableClient['birthDate'].eq(toVariant(BIRTHDAY)))
                client=QtGui.qApp.db.getRecordEx(self.tableClient, '*', where=cond)
                if client:
                    client_ClientId=client.value('client_id').toInt()[0]
            if POLIS_SERIA and POLIS_NUMBER:
                cond=[]
                cond.append(self.tableClientPolicy['serial'].eq(toVariant(POLIS_SERIA)))
                cond.append(self.tableClientPolicy['number'].eq(toVariant(POLIS_NUMBER)))
                clientPolicyList=QtGui.qApp.db.getRecordList(
                    self.tableClientPolicy, '*', where=cond)
                if clientPolicyList:
                    found=False
                    for clientPolicy in clientPolicyList:
                        Policy_ClientId=clientPolicy.value('client_id').toInt()[0]
                        if Policy_ClientId and Policy_ClientId==client_ClientId:
                            found=True
                    if not found and client_ClientId:
                        errorMessage = u'не совпадает полис'
                        errorInfo = u'\nНайденные полисы серии %s и номера %s не соотносятся с найденным клиентом id = %d' % (POLIS_SERIA, POLIS_NUMBER, client_ClientId)
                        self.err2log(errorMessage, errorInfo)
                        return None

            if SERIA_LEFT and SERIA_RIGHT and DOC_NUMBER:
                cond=[]
                cond.append(self.tableClientDocument['serial'].eq(toVariant(SERIA)))
                cond.append(self.tableClientDocument['number'].eq(toVariant(DOC_NUMBER)))
                clientDocumentList=QtGui.qApp.db.getRecordList(
                    self.tableClientDocument, '*', where=cond)
                if clientDocumentList:
                    found=True
                    for clientDocument in clientDocumentList:
                        Document_ClientId=clientDocument.value('client_id').toInt()[0]
                        if Document_ClientId and Document_ClientId==client_ClientId:
                            found=True
                    if not found and client_ClientId:
                        errorMessage = u'не совпадает документ'
                        errorInfo = u'\nНайденные документы серии %s и номера %s не соотносятся с найденным клиентом id = %d' % (SERIA, DOC_NUMBER, client_ClientId)
                        self.err2log(errorMessage, errorInfo)
                        return None

            if client_ClientId:
                if self.importMU:
                    return None
                self.num_found+=1
                clientId=client_ClientId
#                if self.importMU:
#                    return None
            else:
                self.num_added+=1
                clientFields=[
                    ('lastName', SURNAME), ('firstName', NAME), ('patrName', SECOND_NAME),
                    ('sex', sex), ('birthDate', BIRTHDAY)]
                clientId = getId(self.tableClient, clientFields)

            if clientId:
                if not self.importMU:
                    if EP_NUMBER:
                        ident_rec=self.tableClientIdentification.newRecord()
                        ident_rec.setValue('client_id', toVariant(clientId))
                        ident_rec.setValue('accountingSystem_id', toVariant(self.ClientIdentification_EP_NUMBER))
                        ident_rec.setValue('identifier', toVariant(EP_NUMBER))
                        if self.identDate:
                            ident_rec.setValue('checkDate', toVariant(self.identDate))
                        self.db.insertRecord(self.tableClientIdentification, ident_rec)

                    if ID_HISTORY:
                        ident_rec=self.tableClientIdentification.newRecord()
                        ident_rec.setValue('client_id', toVariant(clientId))
                        ident_rec.setValue(
                            'accountingSystem_id', toVariant(self.ClientIdentification_ID_HISTORY))
                        ident_rec.setValue('identifier', toVariant(ID_HISTORY))
                        if self.identDate:
                            ident_rec.setValue('checkDate', toVariant(self.identDate))
                        self.db.insertRecord(self.tableClientIdentification, ident_rec)

                if ID_PATIENT:
                    ident_rec=self.tableClientIdentification.newRecord()
                    ident_rec.setValue('client_id', toVariant(clientId))
                    ident_rec.setValue(
                        'accountingSystem_id', toVariant(self.ClientIdentification_ID_PATIENT))
                    ident_rec.setValue('identifier', toVariant(ID_PATIENT))
#                    if self.identDate:
#                        ident_rec.setValue('checkDate', toVariant(self.identDate))
                    self.db.insertRecord(self.tableClientIdentification, ident_rec)

        if clientId:
            insurerId=self.getInsurer()

            if POLIS_SERIA and POLIS_NUMBER:
                policyType_id=None
                if ID_HUMAN_TYPE==1:
                    policyType_id=2
                elif ID_HUMAN_TYPE==6:
                    policyType_id=1
                clientPolicyFields=[('client_id', clientId), ('serial', POLIS_SERIA), ('number', POLIS_NUMBER)]
                clientPolicyFields2=[
                    ('begDate', POLIS_BEGIN_DATE), ('endDate', POLIS_END_DATE),
                    ('insurer_id', insurerId), ('policyType_id', policyType_id)]
                currentPolicyRecord = getClientCompulsoryPolicy(clientId)
                currentPolicyId = forceRef(currentPolicyRecord.value('id')) if currentPolicyRecord else None
                findAndUpdateOrCreateRecord(self.tableClientPolicy, clientPolicyFields, clientPolicyFields2, currentPolicyId)

            clientDocumentId=None
            if documentTypeId and SERIA_LEFT and SERIA_RIGHT and DOC_NUMBER:
                documentFields=[
                    ('client_id', clientId), ('documentType_id', documentTypeId),
                    ('serial', SERIA), ('number', DOC_NUMBER)]
                getId(self.tableClientDocument, documentFields)

        return clientId

    def putSize(self, onlyNew, lowBirthdayStr, highBirthdayStr):
        self.labelNum.setText(u'подсчёт количества записей в источнике...')
        QtGui.qApp.processEvents()
        if self.importMU:
            size_stmt='SELECT COUNT(*) FROM PATIENTS'
#            if onlyNew:
            size_stmt+="""
            LEFT JOIN PATIENT_DATA ON PATIENT_DATA.ID_PATIENT=PATIENTS.ID_PATIENT
            WHERE NOT EXISTS (SELECT * FROM PEOPLE WHERE
            (PEOPLE.ID_HISTORY IS NOT NULL AND PEOPLE.ID_HISTORY=PATIENTS.ID_EIS_OMS) OR
            (PEOPLE.EP_NUMBER IS NOT NULL AND PEOPLE.EP_NUMBER=PATIENT_DATA.EP_NUMBER))
            AND PATIENT_DATA.BIRTHDAY BETWEEN %s AND %s""" % (lowBirthdayStr, highBirthdayStr)
        else:
            size_stmt='SELECT COUNT(*) FROM PEOPLE WHERE PEOPLE.BIRTHDAY BETWEEN %s AND %s' % (lowBirthdayStr, highBirthdayStr)
            if onlyNew:
                size_stmt+=' AND PEOPLE.TMONTH_BEGIN>='+str(self.TMONTH)
        q_size=self.EIS_db.query(size_stmt)
        if q_size.next():
            r_size=q_size.record()
            num=forceInt(r_size.value(0))
            self.num=num
        q_size.clear()
        if num>0:
            self.progressBar.setMaximum(num)
        else:
            self.progressBar.setMaximum(0)
        self.labelNum.setText(u'всего записей в источнике: '+str(num))
        QtGui.qApp.processEvents()


    def getDocumentTypeIdByEisId(self, eisDocumentTypeId):
        result = self.mapeisDocumentTypeIdToDocTypeId.get(eisDocumentTypeId, False)
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
            self.mapeisDocumentTypeIdToDocTypeId[eisDocumentTypeId] = result
        return result


    @pyqtSignature('int')
    def on_cmbPart_currentIndexChanged(self, index):
        if index == 0:
            self.chkImportAttach.setEnabled(True)
        else:
            self.chkImportAttach.setEnabled(False)
            self.chkImportAttach.setChecked(False)


def get_street(UNSTRUCT_ADDRESS):
    street=UNSTRUCT_ADDRESS
    if UNSTRUCT_ADDRESS.startswith(u'г.Санкт-Петербург '):
        return get_ul(UNSTRUCT_ADDRESS[18:])
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


badGEONIM_NAMEs={
    u'Большой В.О.':u'Большой ВО', u'Большой П.С.':u'Большой ПС',
    u'Малый В.О.':u'Малый ВО', u'Малый П.С.':u'Малый ПС'}


def getGEONIM_NAME(gn):
    GEONIM_NAME=trim(forceString(gn))
    if GEONIM_NAME and GEONIM_NAME[0].isdigit():
        gn=GEONIM_NAME.split()
        GEONIM_NAME=u' '.join(gn[1:]+gn[:1])
    GEONIM_NAME=badGEONIM_NAMEs.get(GEONIM_NAME, GEONIM_NAME)
    return GEONIM_NAME


OBL_TOWN_SOCR={u'г':u'г', u'Г':u'г', u'д':u'д', u'Д':u'д', u'п':u'п', u'П':u'п'}


def getOBL_TOWN_SOCR(OBL_TOWN_TYPE):
    return OBL_TOWN_SOCR.get(OBL_TOWN_TYPE, '')

ul_types=[
    u'ул.', u'наб.', u'ал.', u'б-р', u'дор.', u'дорожка', u'линия', u'пер.', u'пл.', u'пр.', u'пр-д', u'ш.', u'тупик', u'остров', u'парк', u'км', u'бск']


def get_ul(street):
    for ut in ul_types:
        pos=street.find(ut)
        if pos>0:
            return street[:pos+len(ut)]
    return None

numlat_re=re.compile('[0-9a-zA-Z]')
