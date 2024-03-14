#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Скрипт обмена данными с лабораториями и ЛИС по протоколам ASTM и FHIR
##
#############################################################################

import codecs
import locale
import os.path
import sys
import traceback
import json
import logging
import httplib as http_client

from shutil import copyfile

from optparse import OptionParser

from PyQt4 import QtCore, QtGui

from library.database import connectDataBase
from library.Preferences import CPreferences
from library.Utils import forceInt, forceString, forceRef, forceBool, smartDict, setPref, quote, exceptionToUnicode
from library.ScriptLock import CScriptLock
from library.Attach.WebDAVInterface import CWebDAVInterface

from Exchange.Lab.AstmE1394.Message          import CMessage
from Exchange.Lab.AstmE1381.FileExchangeLoop import CFileExchangeLoop
from RefBooks.Equipment.Protocol             import CEquipmentProtocol
from RefBooks.Equipment.RoleInIntegration    import CEquipmentRoleInIntegration
from Registry.Utils                          import getClientInfo, selectAppropriateEpidCase
from TissueJournal.ProbeWorkListPage         import CProbeSaver, probeSent2LIS
from TissueJournal.LabInterface              import bundleProbes
from TissueJournal.LabInterfaceFHIR          import ( sendOrdersOverFHIR    as sendOrdersOverFHIR050,
                                                      pickupResultsOverFHIR as pickupResultsOverFHIR050,
                                                    )
from TissueJournal.LabInterfaceFHIR102       import ( sendOrdersOverFHIR    as sendOrdersOverFHIR102,
                                                      pickupResultsOverFHIR as pickupResultsOverFHIR102,
                                                      importOrdersOverFhir, CFHIRExchange

                                                    )
from TissueJournal.LabInterfaceASTM          import sendOrdersOverASTM
from TissueJournal.TissueJournalModels       import CSamplePreparationModel
from TissueJournal.ExportLocalLabResultsToUsish import exportLocalLabResultsToUsish, exportLabResultsToUsish, exportLocalLabResultsToUsishWithoutProbes
from TissueJournal.Utils                     import getEquipmentInterface


globalProcessedItemList = []
defaultDays = 14

def openDatabase(preferences, debug = None):
    return connectDataBase(preferences.dbDriverName,
                                 preferences.dbServerName,
                                 preferences.dbServerPort,
                                 preferences.dbDatabaseName,
                                 preferences.dbUserName,
                                 preferences.dbPassword,
                                 compressData = preferences.dbCompressData,
                                 logger = logging.getLogger('DB') if debug else None)


mapEquipmentIdToInterface = {}
def getEquipmentInterfaceCache(equipmentId):
    global mapEquipmentIdToInterface
    if equipmentId in mapEquipmentIdToInterface:
        return mapEquipmentIdToInterface[equipmentId]

    interface = getEquipmentInterface(equipmentId)
    mapEquipmentIdToInterface[equipmentId] = interface
    return interface


def testGetResult():
    testFhir()


def sendTests(probeIdList, probeSaver=None):
    global globalProcessedItemList
    mapClientIdToInfo = {}


    def getClientInfoCache(clientId):
        if clientId in mapClientIdToInfo:
            return mapClientIdToInfo[clientId]
        clientInfo = getClientInfo(clientId)
        mapClientIdToInfo[clientId] = clientInfo
        return clientInfo


    def convertProbeIdListToString(idList):
        return ', '.join( str(id) for id in idList )

    try:
        bundles = bundleProbes(probeIdList)
        for bundleKey, probeIdSubList in bundles.iteritems():
            equipmentId = bundleKey.equipmentId
            equipmentInterface = getEquipmentInterfaceCache(equipmentId)

            try:
                if equipmentInterface:
                    clientInfo = getClientInfoCache(bundleKey.clientId)
                    clientInfo.epidCase = selectAppropriateEpidCase(clientInfo, bundleKey.takenTissueJournalId)
                    if equipmentInterface.protocol == CEquipmentProtocol.astm:
                        ok = sendOrdersOverASTM(None,
                                           equipmentInterface,
                                           clientInfo,
                                           probeIdSubList,
                                           probeSaver)
                    elif equipmentInterface.protocol == CEquipmentProtocol.fhir050:
                        ok = sendOrdersOverFHIR050(None,
                                                   equipmentInterface,
                                                   clientInfo,
                                                   probeIdSubList,
                                                   probeSaver)
                    elif equipmentInterface.protocol == CEquipmentProtocol.fhir102:
                        ok = sendOrdersOverFHIR102(None,
                                                   equipmentInterface,
                                                   clientInfo,
                                                   probeIdSubList,
                                                   probeSaver)
                    else:
                        ok = True
                    if ok:
                        log('ok',
                            'probe(s) %s successfully sended'% convertProbeIdListToString(probeIdSubList),
                            level=2)
                        globalProcessedItemList.append(probeIdSubList)
            except Exception as e:
                log('error',
                    'sending probe(s) %s failed: %s' % (convertProbeIdListToString(probeIdSubList),
                                                        exceptionToUnicode(e)),
                    level=1)
                globalProcessedItemList.append(probeIdSubList)
                logCurrentException()
    except Exception as e:
        log('error', 'preparing data failed: %s'%unicode(e), level=1)
        logCurrentException()


def save(item, status=None):
    global globalProcessedItemList
    item.setValue('status', QtCore.QVariant(status))
    db = QtGui.qApp.db
    id = db.updateRecord('Probe', item)
    globalProcessedItemList.append(id)


def log(title, message, stack=None, level=2):
    app = QtGui.qApp
    if level<=app.logLevel:
        try:
            if not os.path.exists(app.logDir):
                os.makedirs(app.logDir)
            dateString = unicode(QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate))
            logFile = os.path.join(app.logDir, '%s.log'%dateString)
            timeString = unicode(QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.SystemLocaleDate))
            logString = u'%s: %s(%s)\n' % (timeString, title, message)
            if stack:
                try:
                    logString += ''.join(traceback.format_list(stack)).decode('utf-8') + '\n'
                except:
                    logString += 'stack lost\n'
            file = codecs.open(logFile, mode='a', encoding=locale.getpreferredencoding())
            file.write(logString)
            file.close()
        except:
            pass


def logException(exceptionType, exceptionValue, exceptionTraceback):
    title = repr(exceptionType)
    #message = anyToUnicode(exceptionValue)
    message = exceptionValue
    log(title, message, traceback.extract_tb(exceptionTraceback))
    sys.__excepthook__(exceptionType, exceptionValue, exceptionTraceback)


def logCurrentException():
    logException(*sys.exc_info())

def getOrgId(db):
    table = db.table('OrgStructure')
    record = db.getRecordEx(table, table['organisation_id'], order='id desc')
    if record:
        return forceRef(record.value(0))
    return None


def main():
    parser = OptionParser(usage = "usage: %prog [options]")
    parser.add_option('-c', '--config',
                      dest='iniFile',
                      help='custom .ini file name',
                      metavar='iniFile',
                      default='/usr/local/labExchange/configs/autoLabExchange.ini'
                     )
    parser.add_option('-e', '--export',
                      action="store_true",
                      dest='export',
                      help='export data to configured destinations',
                      default=False
                     )
    parser.add_option('-a', '--astm',
                      action="store_true",
                      dest='importAstm',
                      help='import from astm',
                      default=False
                     )
    parser.add_option('-f', '--fhir',
                      action="store_true",
                      dest='importFhir',
                      help='import from fhir',
                      metavar='importFhir',
                      default=False
                     )
    parser.add_option('-o', '--orders',
                      action="store_true",
                      dest='importOrders',
                      help='import orders from fhir',
                      metavar='importOrders',
                      default=False
                     )
    parser.add_option('-l', '--exportLocalResults',
                      action="store_true",
                      dest='exportLocalResults',
                      help='export local results to usish',
                      metavar='exportLocalResults',
                      default=False
                     )
    parser.add_option('', '--exportLocalResultsWithoutProbes',
                      action="store_true",
                      dest='exportLocalResultsWithoutProbes',
                      help='export local results to usish. Not looking fro probes',
                      metavar='exportLocalResultsWithoutProbes',
                      default=False
                     )
    parser.add_option('-s', '--exportResults',
                      action="store_true",
                      dest='exportResults',
                      help='export results to usish',
                      metavar='exportResults',
                      default=False
                     )
    parser.add_option('-d', '--days',
                      dest='days',
                      type="int",
                      help='search probes for how much days?',
                      default='14'
                      )
    parser.add_option('-r', '--registrate',
                      action="store_true",
                      dest='registrateProbes',
                      help='registrate imported probes',
                      metavar='registrateProbes',
                      default=False
                     )
    parser.add_option('', '--registrateEquip',
                      dest='registrateProbesEquipment',
                      help='registrate imported probes',
                      metavar='registrateProbesEquipment',
                      default=None
                     )
    parser.add_option('', '--from',
                      dest='dateFrom',
                      help='beg date for probes pickup',
                      metavar='dateFrom'
                     )
    parser.add_option('', '--to',
                      dest='dateTo',
                      help='end date for probes pickup',
                      metavar='dateTo'
                     )
    parser.add_option('', '--debug',
                      action="store_true",
                      dest='debug',
                      help='print debug info',
                      default=False
                     )
    parser.add_option('', '--exportIbm',
                      dest='exportIbm',
                      help='provide ibm to reexport',
                      )
    parser.add_option('', '--exportEquipmentId',
                      dest='exportEquipmentId',
                      help='provide equipment id to export to',
                      )
    parser.add_option('', '--exportProtocolId',
                      dest='exportProtocolId',
                      help='provide protocol id to export. manual = 0, astm = 1, pacs = 2, fhir050 = 3, fhir102 = 4, samson  = 5',
                      )

    (options, args) = parser.parse_args()
    parser.destroy()

    app = QtGui.QApplication(sys.argv, False)
    app.logLevel = 2
    app.userHasRight = lambda x: True
    app.font = lambda : None
    QtGui.qApp = app
    preferences = CPreferences(options.iniFile)
    iniFileName = preferences.getSettings().fileName()
    if not os.path.exists(iniFileName):
        print("ini file (%s) not exists")%iniFileName
        app.quit()
    preferences.load()
    settings = preferences.getSettings()
    settings.beginGroup('astmImportSettings')
    preferences.astmImportSettings = {}
    for prop in settings.childKeys():
        preferences.astmImportSettings[unicode(prop)] = settings.value(prop, QtCore.QVariant())
    for group in settings.childGroups():
        setPref(preferences.astmImportSettings, unicode(group), preferences.loadProp(settings, group))
    settings.endGroup()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        http_client.HTTPConnection.debuglevel = 1
        f_handler = logging.FileHandler('file.log', encoding='utf8')
        f_format = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        requests_log.addHandler(f_handler)
        
    db = openDatabase(preferences, options.debug)
    app.db = db
    app.userId = 1
    app.debug = options.debug
    app.logLevel = forceInt(preferences.appPrefs.get('logLevel', 2))
    app.preferences = preferences
    logDir = forceString(preferences.appPrefs.get('logDir', None))
    if not logDir:
        logDir = os.path.join(unicode(QtCore.QDir.toNativeSeparators(QtCore.QDir.homePath())), '.labExchange')
    app.logDir = logDir
    app.importPDFDir = forceString(preferences.appPrefs.get('importPDFDir', None))
    app.webdavUrl = forceString(preferences.appPrefs.get('webdavUrl', None))
    app._currentOrgId = forceRef(preferences.appPrefs.get('currentOrgId', None))
    if not app._currentOrgId:
        app._currentOrgId = getOrgId(db)
    app.currentOrgId = lambda: app._currentOrgId
    app.financeCodeByActionType = forceRef(preferences.appPrefs.get('financeCodeByActionType', None))
    app.practitionerOrganisationOnly = forceBool(preferences.appPrefs.get('practitionerOrganisationOnly', False))
    app.controlSMFinance = lambda: 0
    app.currentOrgStructureId = lambda: None
    app.setJTR = lambda x: None
    app.unsetJTR = lambda x: None
    app.addJobTicketReservation = lambda x: x
    app.defaultKLADR = lambda: '2900000000000'
    app.provinceKLADR = lambda: '2900000000000'
    app.userOrgStructureId = None
    app.logCurrentException = logCurrentException
    app.log = log
    QtGui.qApp = app
    dateTo = QtCore.QDate.currentDate()
    dateFrom = dateTo.addDays(-1*defaultDays)
    if any([options.importFhir, options.registrateProbes, options.registrateProbesEquipment, options.importOrders, options.exportResults]):
        if options.dateTo:
            dateTo = QtCore.QDate.fromString(options.dateTo,  QtCore.Qt.ISODate)
            if not dateTo.isValid():
                log('fhir error', u'Неверно указана дата окончания: %s'%options.dateTo)
                return
            dateFrom = dateTo.addDays(-1*defaultDays)
        if options.days != defaultDays:
            try:
                dateFrom = dateTo.addDays((-1)*options.days)
            except Exception as e:
                log('fhir error',  unicode(e))
                return
        else:
            if options.dateFrom:
                dateFrom = QtCore.QDate.fromString(options.dateFrom, QtCore.Qt.ISODate)
                if not dateFrom.isValid():
                    log('import fhir',  u'Неверно указана дата начала: %s'%options.dateFrom)
                    return

    if options.export:
        try:
            lockfile = 'labExchange/export'+(options.exportProtocolId if options.exportProtocolId else '')
            with CScriptLock(lockfile, False):
                log('log', 'starting export', level=3)
                export(options.days, options.exportIbm, options.exportEquipmentId, options.exportProtocolId)
        except Exception as e:
            log('export', exceptionToUnicode(e), level=1)
    if options.importAstm:
        try:
            with CScriptLock('labExchange/importAstm', False):
                log('log', 'starting import astm', level=3)
                importAstm()
        except Exception as e:
            log('import astm', exceptionToUnicode(e), level=1)
    if options.importFhir:
        try:
            with CScriptLock('labExchange/importFhir', False):
                log('fhirLog', 'starting import fhir', level=3)
                importFhir(dateFrom, dateTo)
        except Exception as e:
            log('import fhir error', exceptionToUnicode(e), level=1)
    if options.importOrders:
        try:
            with CScriptLock('labExchange/importOrders', False):
                log('fhirLog', 'starting import orders', level=3)
                importOrders(dateFrom, dateTo)
        except Exception as e:
            log('import orders error', exceptionToUnicode(e), level=1)
    if options.registrateProbes:
        registrateProbes(dateFrom, dateTo)
    if options.registrateProbesEquipment:
        registrateProbes(dateFrom, dateTo, options.registrateProbesEquipment)
    if options.exportLocalResults:
        try:
            with CScriptLock('labExchange/exportLocalResults', False):
                log('log', 'starting export local results to usish', level=3)
                exportLocalLabResultsToUsish(dateFrom, dateTo, options.exportIbm)
        except Exception as e:
            log('export local results error', exceptionToUnicode(e), level=1)
    if options.exportLocalResultsWithoutProbes:
        try:
            with CScriptLock('labExchange/exportLocalResultsWithoutProbes', False):
                log('log', 'starting export local results to usish', level=3)
                exportLocalLabResultsToUsishWithoutProbes(options.days)
        except Exception as e:
            log('export local results error', exceptionToUnicode(e), level=1)
    if options.exportResults:
        try:
            with CScriptLock('labExchange/exportResults', False):
                log('log', 'starting export results to usish', level=3)
                exportLabResultsToUsish(dateFrom, dateTo)
        except Exception as e:
            log('export results error', exceptionToUnicode(e), level=1)
    if app.db:
        app.db.close()
    app.quit()


def importOrders(dateFrom, dateTo):
    db = QtGui.qApp.db
    tableEquipment = db.table('rbEquipment')
    equipmentIdList = db.getIdList(tableEquipment,
                                   'id',
                                   [ tableEquipment['protocol'].eq(CEquipmentProtocol.fhir102),
                                     tableEquipment['roleInIntegration'].eq(CEquipmentRoleInIntegration.gateway),
                                     tableEquipment['status'].eq(1)
                                   ]
                                  )
    for equipmentId in equipmentIdList:
        equipmentInterface = getEquipmentInterfaceCache(equipmentId)
        importOrdersOverFhir(equipmentInterface, dateFrom, dateTo)


def importFhir(dateFrom, dateTo):
    db = QtGui.qApp.db
    tableEquipment = db.table('rbEquipment')
    tableProbe = db.table('Probe')
    tableTTJ = db.table('TakenTissueJournal')
    table = tableProbe.leftJoin(tableTTJ, tableTTJ['id'].eq(tableProbe['takenTissueJournal_id']))
    equipmentIdList = db.getIdList(tableEquipment,
                                   'id',
                                   [ tableEquipment['protocol'].inlist([CEquipmentProtocol.fhir050, CEquipmentProtocol.fhir102]),
                                     tableEquipment['roleInIntegration'].inlist([CEquipmentRoleInIntegration.external, CEquipmentRoleInIntegration.internal]),
                                     tableEquipment['status'].eq(1)
                                   ]
                                  )
    for equipmentId in equipmentIdList:
        log('import fhir', u'id оборудования: %i'%equipmentId, level=2)
        cond = [ tableProbe['status'].eq(6),
#                 tableEquipment['samplePreparationMode'].eq(1),
                 tableProbe['exportDatetime'].dateGe(dateFrom),
                 tableProbe['exportDatetime'].dateLe(dateTo),
                 tableProbe['equipment_id'].eq(equipmentId),
                 tableProbe['exportName'].ne(''),
                 tableTTJ['deleted'].eq(0)
               ]
        probeIdRecordList = db.getRecordList(table, 'Probe.*', where=cond, order='id')
        equipmentInterface = getEquipmentInterfaceCache(equipmentId)
        probeIdList = [forceRef(record.value('id')) for record in probeIdRecordList]
        if not probeIdList:
            log('import fhir', u'За указанный период нет проб', level=2)
            continue
        if len(probeIdList) > 20:
            log('import fhir', u'Запрос результатов по %i пробам с %s по %s'%(len(probeIdList),
                    db.formatDate(dateFrom),
                    db.formatDate(dateTo)), level=2)
        else:
            log('import fhir', u'Запрос результатов по пробам %s'%(', '.join([str(id) for id in probeIdList])), level=2)
        try:
            if equipmentInterface.protocol == CEquipmentProtocol.fhir050:
                setOfPrecessedOrderIds = pickupResultsOverFHIR050(None, equipmentInterface, [], probeIdRecordList)
            elif equipmentInterface.protocol == CEquipmentProtocol.fhir102:
                setOfPrecessedOrderIds = pickupResultsOverFHIR102(None, equipmentInterface, [], probeIdRecordList)
            else:
                assert False, u'invalid equipmentInterface.protocol for FHIR'
        except Exception as e:
            log('fhir error', exceptionToUnicode(e), level=1)
        else:
            cond = [tableProbe['equipment_id'].eq(equipmentId),
                tableProbe['exportName'].inlist(setOfPrecessedOrderIds),
                tableProbe['status'].eq(7)]
            receivedItemsList = db.getRecordList(tableProbe, '*', cond)
            if receivedItemsList:
                log('import fhir', u'Получены данные для %i проб'%len(receivedItemsList), level=2)
            else:
                log('import fhir', u'Сервер не вернул результатов', level=2)
    registrateProbes(dateFrom, dateTo)


def importAstm():
    mapResult2Text = {CSamplePreparationModel.importResultFullResultField:u'! ОШИБКА: Все поля результат заняты, некуда импортировать',
                     CSamplePreparationModel.importResultCannotFindProbe:u'! ОШИБКА: Не удалось идентифицировать пробу',
                     CSamplePreparationModel.importResultOk:u'Импорт прошел успешно!',
                     CSamplePreparationModel.importResultValueIsEmpty:u'Импортируемое значение не задано',
                     CSamplePreparationModel.importResultCannotFindTest: u'ОШИБКА: Тест не найден',
                     CSamplePreparationModel.importResultExists: u'Предупреждение: повторное добавление'}
    def importAstmMessage(fileMessage, equipmentInterface):
        equipmentId = equipmentInterface.id
#        ownName = equipmentInterface.ownName
        message = CMessage()
        message.setRecords(fileMessage.body, fileMessage.encoding)
        #if message.header.receiverName == ownName:
        model = CSamplePreparationModel(None)
        model.importedItemsList = []
        model.receivedItemsList = []
        allOk = True
        log('import astm', u'Импорт результатов из %s'%fileMessage.dataFilePatch, level=1)
        for p in message.patients:
            for o in p.orders:
                orderComment = []
                for c in o.comments:
                    orderComment.append(c.textEx)
                orderComment = '\n'.join(orderComment)
                for r in o.results:
                    arg = {'clientId'          : p.patientId,
                           'laboratoryPatientId': p.laboratoryPatientId,
                           'clientId3'         : p.reservedPatientId,
                           'externalId'        : o.specimenId,
                           'specimenDescr'  : o.specimenDescr,
                           'testId_like_code'  : r.testId,
                           'testCode'          : r.assayCode,
                           'testName'          : r.assayName,
                           'value'             : r.value.replace(',', '.'),
                           'referenceRange'    : r.referenceRange,
                           'abnormalFlags'     : r.abnormalFlags,
                           'unit'              : r.unit,
                           'resultStatus'      : r.status,
                           'assistantCode'     : r.operator1,
                           'personCode'        : r.operator2,
                           'rewrite'           : True,
                           'onlyFromModel'     : False,
                           'filterEquipmentId' : None,
                           'equipmentId'       : equipmentId,
                           'dataFileName'      : fileMessage.dataFilePatch,
                           'resultOnFact'      : equipmentInterface.resultOnFact,
                           'resultType'        : r.resultType,
                           'instrumentSpecimenId' : o.instrumentSpecimenId,
                           'instrumentSpecimenIndex' : o.instrumentSpecimenIndex,
                           'orderComment' : orderComment}
                    result = model.setResult(arg)
                    if result == CSamplePreparationModel.importResultOk or result == CSamplePreparationModel.importResultExists:
                        log('import astm ok', u'%s: %s из задачи %s'%(r.testId or r.assayCode, mapResult2Text[result], fileMessage.dataFilePatch), level=2)
                        allOk = allOk and True
                    else:
                        log('import astm error', u'%s, %s: %s из задачи %s'%(r.testId or r.assayCode, r.assayName, mapResult2Text[result], fileMessage.dataFilePatch), level=1)
                        allOk = False
        model.applayItemWithoutImportValue()
        if allOk:
            saveDir = equipmentInterface.opts.get('autoSaveDirOk', None)
            if saveDir:
                if os.path.exists(saveDir):
                    copyfile(fileMessage.dataFilePatch, os.path.join(saveDir, os.path.basename(fileMessage.dataFilePatch)))
                else:
                    log('import astm error', u'Директория %s не существует'%saveDir)
            fileMessage.dismiss()
        else:
            saveDir = equipmentInterface.opts.get('autoSaveDirFail', None)
            if saveDir:
                if os.path.exists(saveDir):
                    copyfile(fileMessage.dataFilePatch, os.path.join(saveDir, os.path.basename(fileMessage.dataFilePatch)))
                    fileMessage.dismiss()
                else:
                    log('import astm error', u'Директория %s не существует'%saveDir)

    def boolOpt(value):
        return value in (1, '1')


    if QtGui.qApp.preferences.astmImportSettings:
        opts = {}
        for key, qval in QtGui.qApp.preferences.astmImportSettings.iteritems():
            val = qval.toInt()
            opts[key] = val[0] if val[1] else forceString(qval)
        equipmentInterface = smartDict(**{"id": None,  "resultOnFact":False})
        equipmentInterface.opts = smartDict(**opts)
        fileLoop = CFileExchangeLoop(opts)
        fileLoop.setLogLevel(QtGui.qApp.logLevel)
        fileLoop.onMessageAccepted = lambda message: importAstmMessage(message,  equipmentInterface)
        fileLoop.onLog = lambda message: log('log', message, level=QtGui.qApp.logLevel)
        try:
            fileLoop._GetMessages()
        except Exception:
            #log('error', unicode(e), 1)
            logCurrentException()
    else:
        db = QtGui.qApp.db
        tableEquipment = db.table('rbEquipment')
        cond = [tableEquipment['protocol'].eq(CEquipmentProtocol.astm),
                tableEquipment['roleInIntegration'].inlist([CEquipmentRoleInIntegration.external, CEquipmentRoleInIntegration.internal]),
                tableEquipment['status'].eq(1),
                tableEquipment['samplePreparationMode'].eq(1),
               ]
        equipmentIdList = db.getIdList(tableEquipment, 'id', where=cond)
        for equipmentId in equipmentIdList:
            equipmentInterface = getEquipmentInterfaceCache(equipmentId)
            opts = json.loads(equipmentInterface.address)
            opts['encoding'] = opts.get('encoding', 'utf-8')
            opts['inDir'] = opts.get('autoInDir', opts.get('inDir', ''))
            opts['processingId'] = opts.get('processingId', 'P')
            opts['extendedValues'] = boolOpt(opts.get('extendedValues', 0))
            opts['appendIbmIntoFileName'] = boolOpt(opts.get('appendIbmIntoFileName', 0))
            opts['uniTestId'] = boolOpt(opts.get('uniTestId', 1))
            opts['uniTestName'] = boolOpt(opts.get('uniTestName', 1))
            opts['testCode'] = boolOpt(opts.get('testCode', 1))
            equipmentInterface.opts = smartDict(**opts)
            fileLoop = CFileExchangeLoop(opts)
            fileLoop.setLogLevel(QtGui.qApp.logLevel)
            fileLoop.onMessageAccepted = lambda message: importAstmMessage(message,  equipmentInterface)
            fileLoop.onLog = lambda message: log('log', message, level=QtGui.qApp.logLevel)
            try:
                fileLoop._GetMessages()
            except Exception:
                #log('error', '%s'%unicode(e), 1)
                logCurrentException()
    registrateProbes()


def registrateProbes(dateFrom = None, dateTo = None, equipmentId = 0):
    db = QtGui.qApp.db
    model = CSamplePreparationModel(None)
    model.receivedItemsList = []
    lockCache = {}
    loggedExtId = {}

    tableProbe = db.table('Probe')
    tableTTJ = db.table('TakenTissueJournal')
    cond = [tableProbe['status'].eq(7), tableProbe['modifyDatetime'].ge('date_sub(current_date(), interval 1 month)')]
    if equipmentId:
        cond.append(tableProbe['equipment_id'].eq(equipmentId))
    if dateFrom:
        cond.append(tableProbe['importDatetime'].dateGe(dateFrom))
    if dateTo:
        cond.append(tableProbe['importDatetime'].dateLe(dateTo))
    recordList = db.getRecordList(tableProbe, '*', cond)
    if len(recordList) > 0:
        db.query('CALL getAppLock_prepare()')
    else:
        log('registrate', u'Нечего регистрировать', level=3)
    exportNameMap = {}
    i = 0
    for item in recordList:
        externalId = forceString(item.value('externalId'))
        exportName = forceString(item.value('exportName'))
        if externalId not in loggedExtId:
            log('registrate', u'Регистрация %s'%externalId, level=3)
            loggedExtId[externalId] = 1
        id = forceRef(item.value('id'))
        tissueJournalId = forceRef(item.value('takenTissueJournal_id'))
        parent_id = forceRef(db.translate(tableTTJ, 'id', tissueJournalId, 'parent_id'))
        if parent_id:
            tissueJournalId = parent_id
        lockId = lockCache.get(tissueJournalId, None)
        if lockId is None:
            tableAction = db.table('Action')
            actionIdList = db.getDistinctIdList(tableAction, tableAction['id'], [tableAction['takenTissueJournal_id'].eq(tissueJournalId)])
            eventIdList = db.getDistinctIdList(tableAction, tableAction['event_id'], [tableAction['takenTissueJournal_id'].eq(tissueJournalId)])
            for eventId in eventIdList:
                query = db.query('CALL getAppLock_(%s, %d, %d, %s, %s, @res)' % (quote('Event'), eventId, 0, 1, quote('autoexport')))
                query = db.query('SELECT @res')
                if query.next():
                    record = query.record()
                    s = forceString(record.value(0)).split()
                    isSuccess = False
                    if len(s)>1:
                        isSuccess = int(s[0])
                        if isSuccess:
                            lockId = int(s[1])
                            lockIdList = lockCache.setdefault(tissueJournalId, [])
                            lockIdList.append(lockId)
                            if exportName:
                                exportNameIdList = exportNameMap.setdefault(exportName, [])
                                exportNameIdList.extend(actionIdList)
                        else:
                            lockCache[tissueJournalId] = False
                            externalId = forceString(item.value('externalId'))
                            log('registrate', u'Событие %i заблокировано'%eventId, level=1)
        if lockId:
            model.addRecord(item)
            model._checkedRowsList.append(i)
            model._mapIdToCheckedResults[id] = [True, forceInt(item.value('resultIndex')), i]
            i += 1
    try:
        model.registrateProbe(True)
        importFiles(exportNameMap)
    except Exception as e:
        log('registrate error', unicode(e), level=3)
    finally:
        for tjId, appLockIdList in lockCache.iteritems():
            if type(appLockIdList) is list:
                for appLockId in appLockIdList:
                    db.query('CALL ReleaseAppLock(%d)' % appLockId)

def importFiles(orderIdMap):
    pdfDir = QtGui.qApp.importPDFDir
    db = QtGui.qApp.db
    tbl = db.table('Action_FileAttach')
    if pdfDir:
        webdav = CWebDAVInterface()
        webdav.setWebDAVUrl(QtGui.qApp.webdavUrl)
        for root, dirs, files in os.walk(pdfDir):
            orderId = os.path.basename(root)
            actionIdList = orderIdMap.get(orderId, None)
            if actionIdList:
                fileItems = webdav.uploadFiles([os.path.join(root, fileName) for fileName in files])
                webdav.saveFiles(fileItems)
                for file in fileItems:
                    for actionId in actionIdList:
                        QtGui.qApp.log('pdf',
                                       u'Регистрируется pdf для действия %i' % actionId,
                                       level=3)
                        attachRecord = tbl.newRecord()
                        attachRecord.setValue('createDatetime', QtCore.QDateTime.currentDateTime())
                        attachRecord.setValue('master_id', actionId)
                        attachRecord.setValue('path', file.getPath())
                        db.insertRecord(tbl, attachRecord)
                for name in files:
                    os.remove(os.path.join(root, name))
                if not dirs:
                    os.rmdir(root)


def export(days = defaultDays, exportIbm = None, exportEquipmentId = None, exportProtocolId = None):
    try:
        global globalProcessedItemList
        db = QtGui.qApp.db
        tableProbe = db.table('Probe')
        tableEquipment = db.table('rbEquipment')
        tableTTJ = db.table('TakenTissueJournal')
        table = tableProbe.leftJoin(tableEquipment, tableProbe['equipment_id'].eq(tableEquipment['id']))
        table = table.leftJoin(tableTTJ, tableTTJ['id'].eq(tableProbe['takenTissueJournal_id']))
        if exportIbm:
            cond = [tableProbe['externalId'].eq(exportIbm),
                   tableEquipment['samplePreparationMode'].eq(1),
                   tableTTJ['deleted'].eq(0)
                   ]
        else:
            cond = [tableProbe['status'].eq(1),
                   'Probe.takenTissueJournal_id in (select takenTissueJournal_id from Probe as P where P.status=1)',
                   tableEquipment['samplePreparationMode'].eq(1),
                   tableProbe['createDatetime'].dateGe(QtCore.QDate.currentDate().addDays(days*(-1))),
                   tableTTJ['deleted'].eq(0)
                   ]
            if exportEquipmentId:
                cond.append(tableEquipment['id'].eq(exportEquipmentId))
            elif exportProtocolId:
                cond.append(tableEquipment['protocol'].eq(exportProtocolId))
        #cond.append(tableProbe['createDatetime'].dateEq(QtCore.QDate.currentDate()))
        recordList = db.getRecordList(table, 'Probe.*', where=cond, order='Probe.id')
        log('log', 'found %d ready to export probes'%len(recordList), level=3)
        idList = []
        externalIdList = {}
        for record in recordList:
            id = forceInt(record.value('id'))
            idList.append(id)
            externalIdList[id] = forceString(record.value('externalId'))
        probeSaver = CProbeSaver({'status':probeSent2LIS},
                                     recordList,
                                     save)
        sendTests(idList, probeSaver=probeSaver)
        #for id in idList:
        #    if id not in globalProcessedItemList:
        #        log('warning', 'probe (%i,%s) was not processed'%(id, externalIdList[id]), level=1)
    except Exception as e:
        log('error', '%s'%unicode(e), level=1)
        logCurrentException()


if __name__ == '__main__':
    main()
