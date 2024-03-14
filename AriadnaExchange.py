#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler
from optparse import OptionParser

import requests
from collections import namedtuple

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QDir, QDate, QDateTime, QVariant

from Events.Action import CAction
from Events.ActionInfo import CActionInfo
from Events.Utils import getEventDiagnosis
from Exchange.AriadnaModels.BirthCertificate import BirthCertificate
from Exchange.AriadnaModels.Cellular import Cellular
from Exchange.AriadnaModels.Certificate import Certificate
from Exchange.AriadnaModels.Company import Company
from Exchange.AriadnaModels.Email import Email
from Exchange.AriadnaModels.InternationalPassport import InternationalPassport
from Exchange.AriadnaModels.Observation import Observation
from Exchange.AriadnaModels.OrderInfo import OrderInfo
from Exchange.AriadnaModels.Passport import Passport
from Exchange.AriadnaModels.Phone import Phone
from Exchange.AriadnaModels.Physician import Physician
from Exchange.AriadnaModels.Province import Province
from Exchange.AriadnaModels.Snils import Snils
from Registry.Utils import CClientInfo
from library import database
from library.Preferences import CPreferences
from library.PrintInfo import CInfoContext
from library.PrintTemplates import escape
from library.Utils import anyToUnicode, forceString, forceInt, forceRef, toVariant, quote, forceBool, unformatSNILS
import platform

_referral = namedtuple('referral', ('actionId', 'eventId', 'clientId', 'exportId'))
_service = namedtuple('service', ('testCode', 'serviceCode', 'serviceName'))


class CAriadnaExchange(QtCore.QCoreApplication):

    iniFileName = '/root/.config/samson-vista/AriadnaExchange.ini'

    def __init__(self, args):
        parser = OptionParser(usage="usage: %prog [options]")
        parser.add_option('-r', '--result', dest='numberResult', help='', metavar='numberResult', default='')
        parser.add_option('-o', '--order', dest='numberOrder', help='', metavar='numberOrder', default='')
        parser.add_option('-a', '--applyresult', dest='applyResult', help='', metavar='applyResult', default='')
        parser.add_option('-c', '--config', dest='iniFile', help='custom .ini file name',
                          metavar='iniFile', default=CAriadnaExchange.iniFileName
                          )
        (options, _args) = parser.parse_args()
        parser.destroy()

        QtCore.QCoreApplication.__init__(self, args)
        self.options = options
        self.db = None
        self.preferences = None
        self.mainWindow = None
        self.userHasRight = lambda x: True
        self.userSpecialityId = None
        self.connectionName = 'AriadnaExchange'
        if self.options.iniFile:
            self.iniFileName = self.options.iniFile
        elif platform.system() != 'Windows':
            self.iniFileName = '/root/.config/samson-vista/AriadnaExchange.ini'
        else:
            self.iniFileName = None
        QtGui.qApp = self
        self.userId = 1
        self.font = lambda: None
        self.logLevel = 2
        self.mapVerifiers = {}
        self.mapUnits = {}
        self.mapTestFederalCodeToId = {}
        self.reloading = False
        self.updateJobTicketStatus = False
        self.resultCount = 40
        self.expirationDays = 7
        self.apikey = ''
        self.icmid = ''
        self.url = ''
        self.encoding = ''
        self.timeout = 60
        self.externalSystemId = None
        self.mapTestIdToServices = {}
        if platform.system() != 'Windows':
            self.logDir = '/var/log/AriadnaExchange'
        else:
            self.logDir = os.path.join(unicode(QDir().toNativeSeparators(QDir().homePath())), '.AriadnaExchange')
        self.initLogger()

    def openDatabase(self):
        self.db = None
        try:
            self.db = database.connectDataBase(self.preferences.dbDriverName,
                                               self.preferences.dbServerName,
                                               self.preferences.dbServerPort,
                                               self.preferences.dbDatabaseName,
                                               self.preferences.dbUserName,
                                               self.preferences.dbPassword,
                                               compressData=self.preferences.dbCompressData,
                                               connectionName=self.connectionName)
            database.registerDocumentTable('rbUnit')
        except Exception as e:
            self.log('error', anyToUnicode(e), 2)

    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None

    def getLogFilePath(self):
        if not os.path.exists(self.logDir):
            os.makedirs(self.logDir)
        dateString = unicode(fmtDateShort(QDate().currentDate()))
        return os.path.join(QtGui.qApp.logDir, '%s.log' % dateString)

    def initLogger(self):
        formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler = RotatingFileHandler(self.getLogFilePath(), maxBytes=1024*1024*50, backupCount=10, encoding='UTF-8')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        oldHandlers = list(logger.handlers)
        logger.addHandler(handler)
        for oldHandler in oldHandlers:
            logger.removeHandler(oldHandler)
        self.logger = logger

    def loadPreferences(self):
        QtGui.qApp.log(u'Путь к файлу конфигурации', self.iniFileName if self.iniFileName else 'AriadnaExchange.ini', level=1)
        self.preferences = CPreferences(self.iniFileName if self.iniFileName else 'AriadnaExchange.ini')
        self.preferences.load()
        self.apikey = forceString(self.preferences.appPrefs.get('apikey', None))
        self.icmid = forceString(self.preferences.appPrefs.get('icmid', None))
        self.url = forceString(self.preferences.appPrefs.get('url', None))
        self.encoding = forceString(self.preferences.appPrefs.get('encoding', 'UTF-8'))
        self.timeout = forceInt(self.preferences.appPrefs.get('timeout', 60))
        self.logDir = forceString(self.preferences.appPrefs.get('logDir', None))
        if not self.logDir:
            if platform.system() != 'Windows':
                self.logDir = '/var/log/AriadnaExchange'
            else:
                self.logDir = os.path.join(unicode(QDir().toNativeSeparators(QDir().homePath())), '.AriadnaExchange')
        self.logLevel = self.preferences.appPrefs.get('logLevel', 2)
        self.reloading = forceBool(self.preferences.appPrefs.get('reloading', False))
        self.updateJobTicketStatus = forceBool(self.preferences.appPrefs.get('updateJobTicketStatus', False))
        self.resultCount = forceInt(self.preferences.appPrefs.get('resultCount', 40))
        self.expirationDays = forceInt(self.preferences.appPrefs.get('expirationDays', 7))
        self.connectionName = forceString(self.preferences.appPrefs.get('connectionName', 'AriadnaExchange'))

    def currentOrgId(self):
        return forceRef(self.preferences.appPrefs.get('orgId', QVariant()))

    def log(self, title, message, level=2, stack=None):
        if level <= QtGui.qApp.logLevel:
            logString = u'%s: %s\n' % (title, message)
            if stack:
                try:
                    logString += anyToUnicode(''.join(traceback.format_list(stack))).decode('utf-8') + '\n'
                except:
                    logString += 'stack lost\n'
            self.logger.info(logString)

    def logException(self, exceptionType, exceptionValue, exceptionTraceback):
        title = repr(exceptionType)
        message = anyToUnicode(exceptionValue)
        self.log(title, message, 0, traceback.extract_tb(exceptionTraceback))
        sys.__excepthook__(exceptionType, exceptionValue, exceptionTraceback)

    def logCurrentException(self):
        self.logException(*sys.exc_info())

    def main(self):
        self.loadPreferences()
        if self.preferences:
            self.initLogger()
            self.openDatabase()
            if self.db:
                self.externalSystemId = forceRef(self.db.translate('rbExternalSystem', 'code', 'AriadnaLIS', 'id'))
                self.mappingTestToServices()
                self.db.query('CALL getAppLock_prepare()')
                if self.options.numberResult:
                    self.getResults(number=self.options.numberResult, count=self.resultCount)
                elif self.options.numberOrder:
                    if self.options.numberOrder != 'all':
                        referrals = []
                        referrals.append(self.getReferralByNumber(self.options.numberOrder))
                    else:
                        referrals = self.getReferrals()
                    for referral in referrals:
                        try:
                            self.sendOrders(referral)
                        except Exception:
                            self.logCurrentException()
                elif self.options.applyResult:
                    self.applyResults(self.options.applyResult)
                else:
                    self.getResults(count=self.resultCount)
                    referrals = self.getReferrals()
                    for referral in referrals:
                        try:
                            self.sendOrders(referral)
                        except Exception:
                            self.logCurrentException()
        self.closeDatabase()

    def mappingTestToServices(self):
        stmt = """SELECT t.id AS testId, st.baseServiceCode, st.testCode, st.serviceCode, st.serviceName
  FROM soc_mapTestToService st
  left JOIN rbTest t ON t.federalCode = st.testCode
  WHERE st.typeLIS = 0"""
        query = self.db.query(stmt)
        while query.next():
            record = query.record()
            testId = forceRef(record.value('testId'))
            testCode = forceString(record.value('testCode'))
            baseServiceCode = forceString(record.value('baseServiceCode'))
            serviceCode = forceString(record.value('serviceCode'))
            serviceName = forceString(record.value('serviceName'))
            self.mapTestIdToServices[(testId, baseServiceCode)] = _service(testCode, serviceCode, serviceName)

    def getReferrals(self):
        referrals = []
        stmt = u"""SELECT a.id as actionId, e.id AS eventId, e.client_id AS clientId, ae.id as exportId
FROM Action a
  left JOIN Event e on e.id = a.event_id
  LEFT JOIN ActionType at ON at.id= a.actionType_id
  left JOIN rbService s ON s.id = at.nomenclativeService_id
  left join Action_Export ae on ae.master_id = a.id and ae.system_id = {externalSystemId}
  WHERE at.flatCode LIKE '%ariadna%'
AND a.deleted = 0
and at.deleted = 0 
AND a.begDate >= NOW() - interval 5 DAY
AND a.begDate < CURDATE() + interval 1 DAY
AND a.status = 5
AND at.serviceType = 10
{reloading}
and e.deleted = 0
order by a.begDate desc
""".format(externalSystemId=self.externalSystemId,
           reloading='and ifnull(ae.success, 0) = 0' if not self.reloading else '')
        query = self.db.query(stmt)
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            eventId = forceRef(record.value('eventId'))
            clientId = forceRef(record.value('clientId'))
            exportId = forceRef(record.value('exportId'))
            referrals.append(_referral(actionId, eventId, clientId, exportId))
        return referrals

    def getReferralByNumber(self, number):
        referral = None
        if not number:
            return None
        stmt = u"""SELECT a.id as actionId, e.id AS eventId, e.client_id AS clientId, ae.id as exportId
FROM Action a
  left JOIN Event e on e.id = a.event_id
  LEFT JOIN ActionType at ON at.id= a.actionType_id
  left JOIN rbService s ON s.id = at.nomenclativeService_id
  left join Action_Export ae on ae.master_id = a.id and ae.system_id = {externalSystemId}
  left join ActionPropertyType apt on apt.actionType_id = at.id and apt.deleted = 0 and apt.name = 'Номер направления'
  left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt.id and ap.deleted = 0
  left join ActionProperty_String aps on aps.id = ap.id
  WHERE at.flatCode LIKE '%ariadna%'
AND a.deleted = 0
and at.deleted = 0 
AND at.serviceType = 10
and e.deleted = 0
and aps.value = '{number}'""".format(externalSystemId=self.externalSystemId, number=number)
        query = self.db.query(stmt)
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            eventId = forceRef(record.value('eventId'))
            clientId = forceRef(record.value('clientId'))
            exportId = forceRef(record.value('exportId'))
            referral = _referral(actionId, eventId, clientId, exportId)
        return referral

    def getHeaders(self):
        headers = {'Content-Type': 'application/json',
                   'ApiKey': self.apikey,
                   'icmid': self.icmid}
        return headers

    def sendOrders(self, referral):
        lockId = None
        response = None
        try:
            self.db.query('CALL getAppLock_(%s, %d, %d, %s, %s, @res)' % (quote('Event'), referral.eventId, 0, 1, quote('AriadnaExchange')))
            query = self.db.query('SELECT @res')

            if query.next():
                record = query.record()
                s = forceString(record.value(0)).split()
                if len(s) > 1:
                    isSuccess = int(s[0])
                    if isSuccess:
                        lockId = int(s[1])
                    else:
                        self.log(u'Выгрузка направления', u'Событие %i заблокировано' % referral.eventId, level=1)
            if lockId:
                context = CInfoContext()
                client = context.getInstance(CClientInfo, referral.clientId)
                observation = Observation()

                # заполняем данные пациента
                observation.patient.id = forceString(client.id)
                observation.patient.snils = client.SNILS
                if observation.patient.snils:
                    snils = Snils()
                    snils.number = unformatSNILS(client.SNILS)
                    observation.patient.identifications.append(snils)
                observation.patient.regCode = forceString(client.id)
                observation.patient.givenName = client.firstName
                observation.patient.familyName = client.lastName
                observation.patient.middleName = client.patrName

                if client.document and client.document.documentTypeRegionalCode in ['3', '9', '13', '14']:
                    identification = None
                    if client.document.documentTypeRegionalCode == '14':
                        identification = Passport()
                    elif client.document.documentTypeRegionalCode == '3':
                        identification = BirthCertificate()
                    elif client.document.documentTypeRegionalCode == '9':
                        identification = InternationalPassport()
                    elif client.document.documentTypeRegionalCode == '13':
                        identification = Certificate()
                    if client.document.documentTypeRegionalCode == '3':
                        identification.series = client.document.serial
                    else:
                        identification.series = client.document.serial.replace(' ', '').replace('-', '')
                    identification.number = client.document.number
                    if client.document.date.date:
                        try:
                            identification.issueDate = fmtDate(client.document.date.date)
                        except ValueError, e:
                            self.log('warning', '{0} client.document.date {1}'.format(client.id, anyToUnicode(e)), 2)
                    if client.document.origin:
                        identification.issuer = client.document.origin
                    observation.patient.identifications.append(identification)

                observation.patient.address = client.locAddress.__str__()  # адрес проживания
                observation.patient.province = Province()

                for contact in client.contacts:
                    if contact[0].lower() == 'e-mail':
                        observation.patient.email = ' '.join([contact[1], contact[2]])
                        email = Email()
                        email.email = contact[1]
                        observation.patient.telecom.append(email)
                    elif contact[0].lower() == u'домашний телефон':
                        phone = Phone()
                        phone.phone = contact[1]
                        observation.patient.telecom.append(phone)
                        if not observation.patient.phoneNumber:
                            observation.patient.phoneNumber = contact[1]
                    elif contact[0].lower() == u'мобильный телефон':
                        cellular = Cellular()
                        cellular.cellular = contact[1]
                        observation.patient.telecom.append(cellular)
                        observation.patient.phoneNumber = contact[1]

                observation.patient.gender = formatSex(client.sexCode)
                if client.birthDate.date:
                    observation.patient.birthDate = fmtDate(client.birthDate.date)
                observation.patient.workPlace = client.work.__str__()
                observation.patient.externalID = forceString(client.id)
                observation.patient.markID = ''
                observation.patient.mark = ''
                observation.patient.notes = ''
                if client.begDate.date:
                    observation.patient.regDate = fmtDate(client.begDate.date)
                if client.compulsoryPolicy and client.compulsoryPolicy.number:
                    observation.patient.insurance.policyID = ''
                    if client.compulsoryPolicy.serial:
                        observation.patient.insurance.policyCode = ' '.join(
                        [client.compulsoryPolicy.serial, client.compulsoryPolicy.number])
                    else:
                        observation.patient.insurance.policyCode = client.compulsoryPolicy.number
                    if client.compulsoryPolicy.kind:
                        observation.patient.insurance.statusID = client.compulsoryPolicy.kind.regionalCode
                        observation.patient.insurance.statusCode = client.compulsoryPolicy.kind.regionalCode
                        observation.patient.insurance.status = client.compulsoryPolicy.kind.name
                    if client.compulsoryPolicy.insurer:
                        observation.patient.insurance.company = Company()
                        observation.patient.insurance.company.id = forceString(client.compulsoryPolicy.insurer.id)
                        observation.patient.insurance.company.localName = client.compulsoryPolicy.insurer.shortName
                        observation.patient.insurance.company.fullName = client.compulsoryPolicy.insurer.fullName
                        observation.patient.insurance.company.code = client.compulsoryPolicy.insurer.tfomsCode
                        observation.patient.insurance.company.phone = client.compulsoryPolicy.insurer.phone
                        observation.patient.insurance.company.cellPhone = ''
                        observation.patient.insurance.company.email = ''
                        observation.patient.insurance.company.externalIdentification = []
                observation.patient.externalIdentification = []
                observation.patient.conditions = []

                action = CActionInfo(context, referral.actionId)

                observation.regDate = fmtDate(action.directionDate.date)
                observation.originalOrderIdentification.extId = forceString(action.id)
                observation.order.id = forceString(action[u'Номер направления'])
                observation.order.date = fmtDate(action.directionDate.date)
                observation.order.hisId = forceString(action.id)
                observation.order.medHistory = action.getEventInfo().externalId

                identifySpecimenTypes = action._action.getProperty(u'Биоматериал').getInfo(context).identify('urn:oid:1.2.643.5.1.13.13.11.1081')
                if identifySpecimenTypes:
                    observation.specimenTypes.id = forceString(action._action.getProperty(u'Биоматериал').getInfo(context).id)
                    observation.specimenTypes.name = action._action.getProperty(u'Биоматериал').getInfo(context).name
                    observation.specimenTypes.code = identifySpecimenTypes
                if action.isUrgent:
                    observation.cito = True
                diagnosis = getEventDiagnosis(referral.eventId)
                if diagnosis:
                    observation.diagnosis = diagnosis

                # заполняем услуги
                services = {}
                baseServiceCode = action.nomenclativeService.code if action.nomenclativeService else ''
                for prop in action._action.getProperties():
                    if prop._type.testId:
                        if not prop._type.isAssignable or (prop._type.isAssignable and prop._isAssigned):
                            service = self.mapTestIdToServices.get((prop._type.testId, baseServiceCode),
                                                                   (None, None, None))
                            if service[0]:
                                services[service.serviceCode] = service
                for key in services:
                    service = services[key]
                    order = OrderInfo()
                    order.service.id = service.testCode
                    order.service.name = service.serviceName
                    order.service.code = service.serviceCode
                    observation.orderInfo.append(order)

                if not observation.orderInfo and action.nomenclativeService:
                    order = OrderInfo()
                    order.service.id = forceString(action._actionType.id)
                    order.service.name = action.nomenclativeService.name
                    order.service.code = action.nomenclativeService.code
                    observation.orderInfo.append(order)

                if not observation.orderInfo:
                    self.log(u'В направлении отсутствуют коды услуг', observation.order.id, 2)
                    return

                person = action.setPerson

                observation.icmid = self.icmid
                observation.orderingInstitution.id = forceString(person.organisation.id)
                observation.orderingInstitution.localName = person.organisation.shortName
                observation.orderingInstitution.fullName = person.organisation.fullName
                if person:
                    observation.orderingInstitution.code = person.organisation.identify('urn:oid:1.2.643.2.69.1.1.1.64')

                observation.orderingInstitution.department = person.orgStructure.code
                if person:
                    observation.orderingInstitution.departmentCode = person.orgStructure.identifyInfoByCode('org.n3').value

                observation.orderingInstitution.phone = person.organisation.phone
                observation.orderingInstitution.icmid = self.icmid

                observation.orderingInstitution.physician = Physician()
                observation.orderingInstitution.physician.id = forceString(person.personId)
                observation.orderingInstitution.physician.regCode = forceString(person.personId)
                observation.orderingInstitution.physician.givenName = person.firstName
                observation.orderingInstitution.physician.familyName = person.lastName
                observation.orderingInstitution.physician.middleName = person.patrName

                headers = self.getHeaders()
                response = requests.post(self.url + '/orders', headers=headers, json=observation.as_json(), timeout=self.timeout)
                tableActionExport = self.db.table(u'Action_Export')
                actionExportRecord = tableActionExport.newRecord()
                actionExportRecord.setValue('id', toVariant(referral.exportId))
                actionExportRecord.setValue('master_id', toVariant(referral.actionId))
                actionExportRecord.setValue('system_id', toVariant(self.externalSystemId))
                actionExportRecord.setValue('dateTime', toVariant(QDateTime().currentDateTime()))
                actionExportRecord.setValue('note', toVariant(response.content.decode('utf-8')))
                if response.status_code == 200:
                    actionExportRecord.setValue('success', toVariant(1))
                    action = CAction(record=self.db.getRecord('Action', '*', referral.actionId))
                    action._record.setValue('status', toVariant(0))
                    action._record.setValue('note', toVariant(u'Заказ успешно выгружен в ЛИС {0}'.format(fmtDate(self.db.getCurrentDatetime()))))
                    action.save(idx=-1)
                else:
                    actionExportRecord.setValue('success', toVariant(0))
                self.db.insertOrUpdate(tableActionExport, actionExportRecord)

                self.log('response code', anyToUnicode(response.status_code), 2)
                self.log('Last sent', observation.as_json(), 2)
                self.log('Last received', anyToUnicode(response.content), 2)
        except Exception as e:
            self.log('error', anyToUnicode(e), 1)
        finally:
            if lockId:
                self.db.query('CALL ReleaseAppLock(%d)' % lockId)
        return response

    def getResults(self, order='desc', number=None, count=None):
        params = {}
        headers = self.getHeaders()
        referral = None

        if (not number or number == 'all') and count:
            params = {'count': forceString(count), 'order': order}
        if number and number != 'all':
            referral = self.getReferralByNumber(number)
            if not referral:
                self.log(u'Загрузка результата {0}'.format(number), u'Направление не найдено в БД', level=1)
                return
            url = self.url + '/results' + ('/{id}'.format(id=referral.actionId) if referral.actionId else '')
        else:
            url = self.url + '/results'
        response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
        jsonData = None
        self.log(u'Загрузка результатов response code', anyToUnicode(response.status_code), 2)
        self.log(u'Загрузка результатов response content', response.content.decode('utf-8'), 2)

        if response.status_code == 200:
            try:
                jsonData = response.json()
            except Exception as e:
                self.log('error', anyToUnicode(e), 2)
            if isinstance(jsonData, dict):
                self.saveResults(jsonData, referral)
            elif isinstance(jsonData, list):
                for result in jsonData:
                    self.saveResults(result, referral)

    def saveResults(self, jsonResult, referral):
        context = CInfoContext()
        observation = None
        lockId = None
        try:
            observation = Observation(jsondict=jsonResult)
            # hisId = forceRef(observation.order.hisId)
            if not referral:
                referral = self.getReferralByNumber(observation.order.id)
            if not referral:
                self.log(u'Загрузка результата {0}'.format(observation.order.id), u'Направление не найдено в БД', level=1)
                self.applyResults(observation.order.id)
                return
            if referral.actionId:
                self.db.query('CALL getAppLock_(%s, %d, %d, %s, %s, @res)' % (quote('Event'), referral.eventId, 0, 1, quote('AriadnaExchange')))
                query = self.db.query('SELECT @res')

                if query.next():
                    record = query.record()
                    s = forceString(record.value(0)).split()
                    if len(s) > 1:
                        isSuccess = int(s[0])
                        if isSuccess:
                            lockId = int(s[1])
                        else:
                            self.log(u'Загрузка результата {0}'.format(observation.order.id),
                                     u'Событие %i заблокировано' % referral.eventId, level=1)
                if lockId:
                    action = CAction(record=self.db.getRecord('Action', '*', referral.actionId))
                    if action and action.actionType() and 'ariadna' in action.actionType().flatCode:
                        finishDate = observation.observationDates.finish
                        verifier = None
                        verifierSNILS = None
                        hasErrors = False
                        hasCancelingTest = False
                        hasBacteria = False
                        testNotes = []
                        for rep in observation.reports:
                            for res in rep.results:
                                testCode = res.measurement.code
                                if res.bacteria:
                                    mapSIR = {1: 'S', 2: 'I', 3: 'R'}
                                    antibioticList = []
                                    hasBacteria = True
                                    if not finishDate:
                                        finishDate = rep.finishDate
                                    if not verifier:
                                        verifier = res.verifier
                                        verifierSNILS = res.verifier.code
                                        if res.verifierRef:
                                            for physician in observation.physicians:
                                                if res.verifierRef.ref == physician.uri:
                                                    for identification in physician.resource.identifications:
                                                        if identification.documentType == 'SNILS':
                                                            verifierSNILS = identification.number
                                    htmlText = u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><body><table>
                                    <tr><td style="font-size: 10pt;">Выделенные микроорганизмы:</td></tr>"""
                                    subTable = u'''<tr><td>
                                    <table border="1" style=" margin-top:0px; margin-bottom:0px; margin-left:30px; margin-right:0px;" width="70%" cellspacing="0" cellpadding="0">
                                    <tr><th>Антибиотикограмма **</th>'''
                                    # первый проход
                                    i = 0
                                    for bacteria in res.bacteria:
                                        i += 1
                                        if u'1,0E+' in bacteria.resultValue:
                                            value = '10<sup>' + ('%d' % forceInt(bacteria.resultValue.replace(u'1,0E+', ''))) + '</sup>   ' + bacteria.unit
                                        else:
                                            value = bacteria.resultValue
                                        htmlText += u'<tr><td style="font-size: 10pt;"><b>[{0}]</b> {1}<hr></td><td style="font-size: 10pt;">{2}<hr></td></tr>'.format(i, bacteria.name, value)
                                        if bacteria.antibiotics:
                                            subTable += u'<th colspan="2">[{0}] МПК</th>'.format(i)
                                            for antibiotic in bacteria.antibiotics:
                                                if antibiotic.code not in antibioticList:
                                                    antibioticList.append(antibiotic.code)

                                    htmlText += u'<tr></tr>'
                                    if antibioticList:
                                        htmlText += subTable + u"</tr>"

                                    # второй проход
                                    for antibioticCode in antibioticList:
                                        rowText = u"<tr><td>{0}</td>"
                                        antibioticName = None
                                        for bacteria in res.bacteria:
                                            if bacteria.antibiotics:
                                                tmp = u'<td colspan=2><table width=100%><tr><td align="left"></td><td align="right"></td></tr></table></td>'
                                            else:
                                                tmp = ''
                                            for antibiotic in bacteria.antibiotics:
                                                if antibioticCode == antibiotic.code:
                                                    if not antibioticName:
                                                        antibioticName = antibiotic.name
                                                    tmp = u'<td colspan=2><table width=100%><tr><td align="left">{0}</td><td align="right">{1}</td></tr></table></td>'.format(mapSIR.get(antibiotic.sir, ''), escape(antibiotic.mic))
                                                    break
                                            rowText += tmp
                                        htmlText += rowText.format(antibioticName) + u'</tr>'
                                    htmlText += u'</table></td></tr>'
                                    if antibioticList:
                                        htmlText += u'<tr><td align="center">** S - чувствителен, I - умеренно-устойчив, R - устойчив</td></tr>'
                                    htmlText += u'</table></body></html>'

                                    prop = action.getPropertyByShortName(u'results')
                                    if prop:
                                        prop.setValue(htmlText)
                                if res.notes:
                                    if hasBacteria:
                                        testNotes.append(u'{notes}'.format(notes=res.notes))
                                    else:
                                        testNotes.append(u'{name} - {notes}'.format(name=res.measurement.name, notes=res.notes))

                                if res.description:
                                    prop = action.getPropertyByShortName(u'conclusion')
                                    if prop:
                                        prop.setValue(res.description)

                                if testCode == '770700113':  # код теста для Обработки материала
                                    hasCancelingTest = True
                                    action._record.setValue('note', toVariant(u'Исследование отменено: {0}'.format(res.resultValue)))
                                    if not finishDate:
                                        finishDate = rep.finishDate
                                    if not verifier:
                                        verifier = res.verifier
                                        verifierSNILS = res.verifier.code
                                        if res.verifierRef:
                                            for physician in observation.physicians:
                                                if res.verifierRef.ref == physician.uri:
                                                    for identification in physician.resource.identifications:
                                                        if identification.documentType == 'SNILS':
                                                            verifierSNILS = identification.number
                                    continue
                                isTestFounding = False
                                try:
                                    testIds = self.getTestIds(testCode)
                                    for testId in testIds:
                                        if testId:
                                            prop = action.getPropertyByTest(testId)
                                            if prop:
                                                if res.resultValue:
                                                    prop.setValue(res.resultValue)
                                                elif res.protocol:
                                                    protocolText = u''
                                                    for item in res.protocol:
                                                        protocolText += item.measurName + ' ' + item.resultText + '; '
                                                    prop.setValue(protocolText.strip())
                                                if res.norm.text:
                                                    prop.setNorm(res.norm.text.replace('(', '').replace(')', ''))
                                                if res.unit:
                                                    prop.setUnitId(self.getUnitId(res.unit))
                                                if not finishDate:
                                                    finishDate = rep.finishDate
                                                if not verifier:
                                                    verifier = res.verifier
                                                    verifierSNILS = res.verifier.code
                                                    if res.verifierRef:
                                                        for physician in observation.physicians:
                                                            if res.verifierRef.ref == physician.uri:
                                                                for identification in physician.resource.identifications:
                                                                    if identification.documentType == 'SNILS':
                                                                        verifierSNILS = identification.number
                                                isTestFounding = True
                                                break
                                except:
                                    isTestFounding = False
                                finally:
                                    if not isTestFounding and not hasBacteria:
                                        self.log('error', u'Событие {0}. Направление: {1}. Отсутствует код теста {2}; name:{3}{4}{5}'.format(referral.eventId,
                                            observation.order.id, testCode, res.measurement.name,
                                            '; shortName: ' + res.measurement.shortName if res.measurement.shortName else '',
                                            '; srvdepCode: ' + res.srvdepCode if res.srvdepCode else ''), 2)
                                        hasErrors = True
                        if finishDate:
                            if hasCancelingTest:
                                action._record.setValue('status', toVariant(3))
                                action._record.setValue('endDate', toVariant(None))
                            else:
                                action._record.setValue('status', toVariant(2))
                                action._record.setValue('endDate', toVariant(unFmtDate(finishDate)))
                                action._record.setValue('note', toVariant(
                                    u'Результат загружен из ЛИС {0}'.format(fmtDate(self.db.getCurrentDatetime()))))
                            # Проставление статуса "Закончено" в номерке
                            if self.updateJobTicketStatus:
                                for prop in action._propertiesById.itervalues():
                                    if prop.type().isJobTicketValueType() and prop.getValue():
                                        recordJT = self.db.getRecord('Job_Ticket', '*', prop.getValue())
                                        if recordJT:
                                            recordJT.setValue('endDateTime', toVariant(unFmtDate(finishDate)))
                                            recordJT.setValue('status', toVariant(2))  # закончено
                                            self.db.updateRecord('Job_Ticket', recordJT)

                            if verifierSNILS and action.hasProperty(u'Лаборатория'):
                                verifierId = self.getVerifierId(action.getProperty(u'Лаборатория').getInfo(context).id, verifierSNILS)
                                if verifierId:
                                    action._record.setValue('person_id', toVariant(verifierId))
                            if testNotes:
                                prop = action.getPropertyByShortName(u'comments')
                                if prop:
                                    prop.setValue(u';'.join(testNotes))
                            action.save(idx=-1)
                            tableActionExport = self.db.table(u'Action_Export')
                            actionExportRecord = tableActionExport.newRecord()
                            actionExportRecord.setValue('id', toVariant(referral.exportId))
                            actionExportRecord.setValue('master_id', toVariant(referral.actionId))
                            actionExportRecord.setValue('system_id', toVariant(self.externalSystemId))
                            actionExportRecord.setValue('success', toVariant(1))
                            actionExportRecord.setValue('dateTime', toVariant(QDateTime().currentDateTime()))
                            actionExportRecord.setValue('note', toVariant(jsonResult))
                            self.db.insertOrUpdate(tableActionExport, actionExportRecord)
                            if observation.order.id:
                                if not hasErrors:
                                    self.log(u'Загрузка результата',
                                             u'Направление {0} успешно загружено. Событие {1}. Действие {2}'.format(
                                                                                                observation.order.id,
                                                                                                referral.eventId,
                                                                                                referral.actionId),
                                                                                            level=1)
                                    self.applyResults(observation.order.id)
                                else:
                                    self.applyOnExpiration(observation.order.id, observation.observationDates.finish)
        except Exception as e:
            self.log('error', anyToUnicode(e), 2)
            self.log('error', u'ошибка при загрузке результата {0}'.format(observation.order.id), 2)
            self.applyOnExpiration(observation.order.id, observation.observationDates.finish)
        finally:
            # снимаем блокировку
            if lockId:
                self.db.query('CALL ReleaseAppLock(%d)' % lockId)

    def getVerifierId(self, orgStructureId, snils):
        result = self.mapVerifiers.get((orgStructureId, snils), None)
        if not result and orgStructureId and snils:
            stmt = "select id from Person WHERE orgStructure_id = {0} AND snils = '{1}'".format(orgStructureId, snils)
            query = self.db.query(stmt)
            while query.next():
                record = query.record()
                result = forceRef(record.value('id'))
                self.mapVerifiers[(orgStructureId, snils)] = result
        return result

    def getUnitId(self, codeUnit):
        codeUnit = codeUnit.strip()
        result = None
        if codeUnit:
            result = self.mapUnits.get(codeUnit, None)
            if not result:
                stmt = u"select id from rbUnit WHERE code = '{0}' limit 1".format(codeUnit)
                query = self.db.query(stmt)
                while query.next():
                    record = query.record()
                    result = forceRef(record.value('id'))
                if not result:
                    tableUnit = self.db.table('rbUnit')
                    record_unit = tableUnit.newRecord()
                    record_unit.setValue('code', codeUnit)
                    record_unit.setValue('name', codeUnit)
                    result = self.db.insertOrUpdate(tableUnit, record_unit)
                self.mapUnits[codeUnit] = result
        return result

    def getTestIds(self, testCode):
        result = self.mapTestFederalCodeToId.get(testCode, [])
        if not result:
            stmt = u"select id from rbTest WHERE federalCode = '{0}'".format(testCode)
            query = self.db.query(stmt)
            while query.next():
                record = query.record()
                result.append(forceRef(record.value('id')))
            self.mapTestFederalCodeToId[testCode] = result
        return result

    def applyResults(self, orderId):
        headers = self.getHeaders()
        json_data = {'orderId': forceString(orderId), 'delivered': True}
        response = requests.post(self.url + '/results', headers=headers, json=json_data, timeout=self.timeout)
        self.log('applyResults response code', anyToUnicode(response.status_code), 2)
        self.log('applyResults  Last sent', json_data, 2)
        if response.status_code == 200:
            self.log('applyResults  response content', response.content.decode('utf-8'), 2)
        return response

    def applyOnExpiration(self, orderId, finishDate):
        # помечаем успешно полученными незагруженные результаты по сроку давности
        if finishDate and unFmtDate(finishDate) < QDateTime().currentDateTime().addDays(-self.expirationDays):
            try:
                self.log('expiration', u'Результат закрыт по сроку давности {0}'.format(orderId), 2)
                headers = self.getHeaders()
                json_data = {'orderId': forceString(orderId), 'delivered': True}
                response = requests.post(self.url + '/results', headers=headers, json=json_data, timeout=self.timeout)
                self.log('expiration response code', anyToUnicode(response.status_code), 2)
                self.log('expiration Last sent', json_data, 2)
                if response.status_code == 200:
                    self.log('expiration response content', response.content.decode('utf-8'), 2)
                return response
            except Exception as e:
                self.log('error', anyToUnicode(e), 2)


def formatSex(sex):
    sex = forceInt(sex)
    if sex == 1:
        return u'M'
    elif sex == 2:
        return u'F'
    else:
        return u'U'


def fmtDate(date):
    if isinstance(date, QDateTime):
        date = date.toPyDateTime()
    elif isinstance(date, QDate):
        date = date.toPyDate()
    if isinstance(date, datetime.datetime):
        if datetime.date(1981, 1, 1) <= date.date() <= datetime.date(1984, 12, 31):
            return date.strftime("%Y-%m-%dT01:%M:%S.%f")[:-3]
    elif isinstance(date, datetime.date):
        if datetime.date(1981, 1, 1) <= date <= datetime.date(1984, 12, 31):
            return date.strftime("%Y-%m-%dT01:%M:%S.%f")[:-3]
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]


def unFmtDate(date):
    return QDateTime().fromString(date[:-10] if len(date) == 29 else date[:-4], 'yyyy-MM-ddTHH:mm:ss')


def fmtDateShort(date):
    if isinstance(date, QDateTime):
        date = date.toPyDateTime()
    elif isinstance(date, QDate):
        date = date.toPyDate()
    return date.strftime("%Y-%m-%d")


if __name__ == '__main__':
    app = CAriadnaExchange(sys.argv)
    app.main()
