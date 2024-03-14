# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
import codecs
import json
import locale
import os
import platform
import ssl
import sys
import time
import traceback
from datetime import datetime
from urllib2 import HTTPSHandler

import suds.transport.http
from PyQt4 import QtCore, QtSql, QtGui
from PyQt4.QtCore import QDateTime, QDate, QDir, Qt
from suds.client import Client
from suds.plugin import MessagePlugin
from suds.sax.text import Text

from Events.Action import CAction, CActionTypeCache
from library import database
from library.Preferences import CPreferences
from library.Utils import forceString, forceInt, forceDate, toVariant, forceRef, unformatSNILS, forceBool, forceDouble, forceDateTime, exceptionToUnicode, forceLong


class CMyApp(QtCore.QCoreApplication):

    def __init__(self, args):
        QtCore.QCoreApplication.__init__(self, args)
        self.db = None
        self.preferences = None
        QtGui.qApp.userId = None
        QtGui.qApp.userHasRight = lambda x: True
        QtGui.qApp.logLevel = 2
        if platform.system() != 'Windows':
            QtGui.qApp.logDir = '/var/log/downloadRecipeLLO'
        else:
            QtGui.qApp.logDir = os.path.join(unicode(QDir().toNativeSeparators(QDir().homePath())), '.downloadRecipeLLO')


    def openDatabase(self):
        try:
            self.db = database.connectDataBase(self.preferences.dbDriverName,
                                               self.preferences.dbServerName,
                                               self.preferences.dbServerPort,
                                               self.preferences.dbDatabaseName,
                                               self.preferences.dbUserName,
                                               self.preferences.dbPassword)
            QtGui.qApp.db = self.db
        except Exception as e:
            self.log(u'Ошибка подключения к базе данных!', exceptionToUnicode(e), 2, traceback.extract_stack()[:-1])


    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None
            if QtSql.QSqlDatabase.contains('qt_sql_default_connection'):
                QtSql.QSqlDatabase.removeDatabase('qt_sql_default_connection')


    def log(self, title, message, level, stack=None):
        app = QtGui.qApp
        if level <= app.logLevel:
            try:
                if not os.path.exists(app.logDir):
                    os.makedirs(app.logDir)
                dateString = unicode(QDate.currentDate().toString('yyyy-MM-dd'))
                logFile = os.path.join(app.logDir, '%s.log' % dateString)
                timeString = unicode(QDateTime.currentDateTime().toString(Qt.SystemLocaleDate))
                logString = u'%s\n%s: %s(%s)\n' % ('='*72, timeString, title, message)
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


    def download(self, downloadUrl, clientId):
        # timeStamp - временная метка, для получения только рецептов, у которых временная метка больше
        # в первом запросе равен 0, а далее берется из ответа сервиса и сохраняется в БД
        try:
            tableSocLLORecipe = self.db.table('soc_LLO_recipe')
            timeStamp = forceLong(self.db.getMax(tableSocLLORecipe, tableSocLLORecipe['timeStamp'], tableSocLLORecipe['clientId'].eq(clientId)))
            itsFirst = False if timeStamp else True
        except:
            timeStamp = 0
            tableSocLLORecipe = None
            itsFirst = True
        # timeStamp = 1019279843
        # список имен всех полей сервиса и подраздела saleItems
        fieldsNamesList, saleItemsList = self.getFieldsNames()
        # список имен полей на русском для дальнейшей записи в БД
        # fieldsNamesRusDict = self.getFieldsNamesRus(fieldsNamesList)

        if not clientId:
            self.log(u'Не задан clientId!', '', 2)
            return

        if downloadUrl:
            try:
                context = create_ssl_context(False)
                t = HTTPSTransport(context)
                plugin = PrunePlugin()
                downloadService = Client(downloadUrl, transport=t, plugins=[plugin])
                downloadService.set_options(port=u'DownloadServiceSoap12')
                downloadService.options.cache.clear()

                # получаем id типа действия "Льготный рецепт" и список всех типов действия вида "Льготный рецепт%"
                # actionTypeRecipe, allActionTypeIdList = self.getActionTypeId()
                # получаем id типа события "Выписка льготных рецептов"
                # eventTypeRecipe = self.getEventTypeId()

                while timeStamp or itsFirst:
                    # передаем код МО IDMU и timeStamp (начинается с 0, а далее получаем из ответа)
                    # получаем ответ от сервиса
                    query = {'SaledOnly': 0}
                    answer = downloadService.service.RecipesDataExport(clientId=clientId, timeStamp=timeStamp, query=query)
                    # query = {'Seria':'03-19-30', 'Number':'8850041'}
                    # answer = downloadService.service.RecipesDataExport(clientId=clientId, query=query)

                    # сохраняем в лог запрос-ответ сервиса
                    self.log('Last sent', plugin.last_sent.decode('utf-8'), 2)
                    self.log('Last received', plugin.last_received.decode('utf-8'), 2)

                    # для уменьшения времени обработки запросов рецепты передаются пачками по 500 штук
                    required_dict = Client.items(answer)
                    listRecipies = []
                    if required_dict is None:
                        return False
                    for required in required_dict:
                        listRecipies.append(required)
                    if timeStamp != listRecipies[0][1]:
                        timeStamp = listRecipies[0][1]
                        listAnswer = listRecipies[1][1][0]
                        # переводим содержимое ответа в словарь, прогоняя по именам полей сервиса
                        # сервис присылает на конкретного пациента только те поля, которые у него заполнены
                        # поэтому проверяем наличие полей, если поля в ответе нет,
                        # то в словарь записываем имя поля и значение None
                        # и не получаем ошибку при попытке обратится к несуществующему в ответе полю
                        fieldsDictList = self.getDictFromSoap(listFields=listAnswer,
                                                              fieldsNamesList=fieldsNamesList,
                                                              saleItemsList=saleItemsList)


                        for recipe in fieldsDictList:
                            now = toVariant(QDateTime.currentDateTime())
                            try:
                                # сохраняем(обновляем) данные рецепта в soc_LLO_recipe
                                recordSocLLORecipe = self.db.getRecordEx(tableSocLLORecipe, '*', [tableSocLLORecipe['Seria'].eq(recipe['Seria']),
                                                                                                  tableSocLLORecipe['Number'].eq(recipe['Number'])])
                                if not recordSocLLORecipe:
                                    recordSocLLORecipe = tableSocLLORecipe.newRecord()
                                    recordSocLLORecipe.setValue('createDatetime', now)
                                recordSocLLORecipe.setValue('modifyDatetime', now)
                                recordSocLLORecipe.setValue('timeStamp', timeStamp)
                                recordSocLLORecipe.setValue('clientId', clientId)
                                for fieldName in fieldsNamesList:
                                    try:
                                        if fieldName == 'SaleItems' and recipe[fieldName]:
                                            try:
                                                recordSocLLORecipe.setValue(fieldName, forceString(json.dumps(recipe[fieldName], ensure_ascii=False)))
                                            except Exception as e:
                                                self.log(u'Ошибка при формировании записи saleItems', exceptionToUnicode(e), 2, traceback.extract_stack()[:-1])
                                        else:
                                            recordSocLLORecipe.setValue(fieldName, recipe[fieldName])
                                    except Exception as e:
                                        self.log(u'Ошибка при формировании записи', exceptionToUnicode(e), 2, traceback.extract_stack()[:-1])

                                self.db.insertOrUpdate(tableSocLLORecipe, recordSocLLORecipe)

                                # рецепты с 2019 года добавляем в мероприятия
                                if forceDate(recordSocLLORecipe.value('IssueDate')) >= QDate(2019, 1, 1):
                                    actionId = None
                                    # ищем рецепт с такими же серией и номером
                                    stmt = u"""select a.id
                                    from Action a
                                    left join ActionType at on at.id = a.actionType_id
                                    left join ActionPropertyType apt on apt.name = 'Серия и номер бланка' AND apt.deleted = 0 AND apt.actionType_id = at.id
                                    left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt.id and ap.deleted = 0
                                    left join ActionProperty_String aps on aps.id = ap.id
                                    where a.deleted = 0 and aps.value = '{0} {1}'""".format(forceString(recordSocLLORecipe.value('Seria')), forceString(recordSocLLORecipe.value('Number')))
                                    query = self.db.query(stmt)
                                    if query.next():
                                        record = query.record()
                                        actionId = forceRef(record.value('id'))
                                    # не нашли - создаем новый
                                    if not actionId:
                                        stmt = u"select max(id) as id from Client where deleted = 0 and SNILS = '{0}'".format(unformatSNILS(recordSocLLORecipe.value('Snils')))
                                        query = self.db.query(stmt)
                                        patientId = None
                                        if query.next():
                                            record = query.record()
                                            patientId = forceRef(record.value('id'))
                                        if not patientId:
                                            stmt = u"""select max(id) as id from Client where deleted = 0
                                            and lastName = '{0}' and firstName = '{1}' and patrName = '{2}' and birthDate = {3}""".format(
                                                forceString(recordSocLLORecipe.value('PatientLastname')),
                                                forceString(recordSocLLORecipe.value('PatientFirstname')),
                                                forceString(recordSocLLORecipe.value('PatientMiddlename')),
                                                self.db.formatDate(forceDate(recordSocLLORecipe.value('PatientBirthday')))
                                            )
                                            query = self.db.query(stmt)
                                            if query.next():
                                                record = query.record()
                                                patientId = forceRef(record.value('id'))
                                        # ищем событие
                                        if patientId:
                                            stmt = u"""select max(e.id) as id, max(p.id) as personId
        from Event e
        left join EventType et on et.id = e.eventType_id
        left join rbMedicalAidType mat on mat.id = et.medicalAidType_id
        left JOIN Person p ON p.regionalCode = '{doctorCode}' OR p.lastName = '{doctorLastName}' AND p.firstName = '{doctorFirstName}' AND p.patrName = '{doctorPatrName}'
        where e.client_id = {clientId} and e.deleted = 0
            and mat.code NOT IN ('1', '2', '3', '7')
          AND e.setDate <= {issueDate} AND (e.execDate IS NULL OR e.execDate >= {issueDate})
          AND exists(SELECT NULL FROM Action a 
            left JOIN ActionType at ON at.id = a.actionType_id
          WHERE a.event_id = e.id AND a.deleted = 0 AND date(a.begDate) = {issueDate} AND at.code like 'B%'
          AND a.person_id = p.id)
                                            """.format(
                                                clientId=patientId,
                                                issueDate=self.db.formatDate(forceDate(recordSocLLORecipe.value('IssueDate'))),
                                                doctorCode=forceString(recordSocLLORecipe.value('PCod')).split(' ')[-1],
                                                doctorLastName=forceString(recordSocLLORecipe.value('DoctorLastname')),
                                                doctorFirstName=forceString(recordSocLLORecipe.value('DoctorFirstname')),
                                                doctorPatrName=forceString(recordSocLLORecipe.value('DoctorMiddlename'))
                                            )
                                            query = self.db.query(stmt)
                                            if query.next():
                                                record = query.record()
                                                eventId = forceRef(record.value('id'))
                                                personId = forceRef(record.value('personId'))
                                                # не нашли подходящего события, создаем связанное мероприятие
                                                if not eventId:
                                                    tableEventType = self.db.table('EventType')
                                                    recordEventType = self.db.getRecordEx(tableEventType,
                                                                                     [tableEventType['id']],
                                                                                     [tableEventType['context'].like(
                                                                                         u'relatedAction%'),
                                                                                      tableEventType['deleted'].eq(0)],
                                                                                     u'EventType.id')
                                                    eventTypeId = forceRef(recordEventType.value('id')) if recordEventType else None
                                                    tableEvent = self.db.table('Event')
                                                    recordEvent = self.db.getRecordEx(tableEvent, [tableEvent['id']],
                                                                                 [tableEvent['eventType_id'].eq(
                                                                                     eventTypeId),
                                                                                  tableEvent['deleted'].eq(0),
                                                                                  tableEvent['client_id'].eq(patientId),
                                                                                  tableEvent['setDate'].dateEq(forceDate(recordSocLLORecipe.value('IssueDate'))),
                                                                                  ], u'Event.id')
                                                    eventId = forceRef(recordEvent.value('id')) if recordEvent else None

                                                    recordEvent = tableEvent.newRecord()
                                                    recordEvent.setValue('createDatetime', toVariant(QDateTime.currentDateTime()))
                                                    recordEvent.setValue('modifyDatetime', toVariant(QDateTime.currentDateTime()))
                                                    recordEvent.setValue('setDate', toVariant(QDateTime.currentDateTime()))
                                                    recordEvent.setValue('eventType_id', toVariant(eventTypeId))
                                                    recordEvent.setValue('client_id', toVariant(patientId))
                                                    eventId = self.db.insertRecord(tableEvent, recordEvent)
                                                    stmt = u"""select max(id) as personId
                                                     from Person where regionalCode = '{doctorCode}' 
                                                        AND lastName = '{doctorLastName}' AND firstName = '{doctorFirstName}' AND patrName = '{doctorPatrName}'
                                                        AND deleted = 0""".format(doctorCode=forceString(recordSocLLORecipe.value('PCod')).split(' ')[-1],
                                                        doctorLastName=forceString(recordSocLLORecipe.value('DoctorLastname')),
                                                        doctorFirstName=forceString(recordSocLLORecipe.value('DoctorFirstname')),
                                                        doctorPatrName=forceString(recordSocLLORecipe.value('DoctorMiddlename')))
                                                    query = self.db.query(stmt)
                                                    if query.next():
                                                        personId = query.record().value('personId')
                                            actionType = CActionTypeCache.getByFlatCode('LLO_recipe')
                                            actionRecord = self.db.table('Action').newRecord()
                                            actionRecord.setValue('actionType_id', toVariant(actionType.id))
                                    else:
                                        actionRecord = QtGui.qApp.db.getRecord('Action', '*', actionId)
                                        QtGui.qApp.userId = forceRef(actionRecord.value('person_id'))
                                    newAction = CAction(record=actionRecord)

                                    # заполняем данные рецепта
                                    if not actionId:
                                        newAction._record.setValue('event_id', toVariant(eventId))
                                        newAction._record.setValue('setPerson_id', toVariant(personId))
                                        newAction._record.setValue('person_id', toVariant(personId))
                                        newAction._record.setValue('createDatetime', toVariant(QDateTime().currentDateTime()))

                                    newAction._record.setValue('modifyDatetime', toVariant(QDateTime().currentDateTime()))
                                    newAction._record.setValue('directionDate', toVariant(forceDate(recordSocLLORecipe.value('IssueDate'))))
                                    newAction._record.setValue('begDate', toVariant(forceDate(recordSocLLORecipe.value('IssueDate'))))
                                    newAction._record.setValue('endDate', toVariant(forceDate(recordSocLLORecipe.value('IssueDate'))))
                                    newAction._record.setValue('status', toVariant(2))
                                    newAction._record.setValue('amount', toVariant(1))
                                    newAction._record.setValue('finance_id', toVariant(1))
                                    newAction._record.setValue('MKB', toVariant(forceString(recordSocLLORecipe.value('Mkb'))))

                                    newAction[u'Серия и номер бланка'] = u' '.join([forceString(recordSocLLORecipe.value('Seria')), forceString(recordSocLLORecipe.value('Number'))])
                                    newAction[u'Источник финансирования'] = u'Федеральный' if forceInt(recordSocLLORecipe.value('SourceType')) == 1 else u'Региональный'
                                    newAction[u'Процент льготы'] = u'{0:.0%}'.format(forceDouble(recordSocLLORecipe.value('PayMode')))
                                    newAction[u'Код льготы'] = forceString(recordSocLLORecipe.value('PrivilegeCategory'))
                                    newAction[u'МНН/ТРН'] = u'ТРН' if forceBool(recordSocLLORecipe.value('IsTrn')) else u'МНН'

                                    # Наименование выписанного лекарственного средства, лекарственная форма, дозировка
                                    titleList = [forceString(recordSocLLORecipe.value('ProductName')), forceString(recordSocLLORecipe.value('CureformName'))]
                                    if forceString(recordSocLLORecipe.value('Dosage')):
                                        titleList.append(forceString(recordSocLLORecipe.value('Dosage')))
                                    newAction[u'Выписано'] = u', '.join(titleList)

                                    newAction[u'Единиц в упаковке'] = forceString(recordSocLLORecipe.value('PackageSize'))
                                    quant = forceDouble(recordSocLLORecipe.value('Quantity'))
                                    newAction[u'Количество упаковок'] = forceString(forceInt(quant) if quant.is_integer() else quant)
                                    newAction[u'Signa'] = forceString(recordSocLLORecipe.value('Signa'))
                                    newAction[u'Действителен в течение'] = dict([('15d', u'15 дней'), ('30d', u'30 дней'), ('90d', u'90 дней')])[forceString(recordSocLLORecipe.value('ValidPeriod'))]
                                    newAction[u'Протокол ВК'] = u'да' if forceBool(recordSocLLORecipe.value('IsVk')) else u'нет'
                                    newAction[u'Статус рецепта'] = dict([(u'PROVIDED', u'Отпущен (обеспечен)'),
                                                                   (u'SEND_TO_PAY', u'Рецепт входит в реестры'),
                                                                   (u'ACPT', u'Утвержден (нет отпуска)'),
                                                                   (u'ANNULLED', u'Аннулирован'),
                                                                   (u'DELAYED', u'На отсроченном обслуживании'),
                                                                   (u'DRUGSTORE', u'Зарегистрирован аптекой')])[forceString(recordSocLLORecipe.value('State'))]

                                    if forceString(recordSocLLORecipe.value('SaleItems')):
                                        saleItems = json.loads(forceString(recordSocLLORecipe.value('SaleItems')))
                                        if isinstance(saleItems, list):
                                            newAction[u'Отпущено'] = u'; '.join([u'{0}, кол-во {1} (цена {2})'.format(si['ProductName'], forceInt(si['Quantity']) if forceDouble(si['Quantity']).is_integer() else si['Quantity'],
                                                                                                                      forceString(si['Price'])) for si in saleItems])
                                        else:
                                            newAction[u'Отпущено'] = u'{0}, кол-во {1} (цена {2})'.format(saleItems['ProductName'],
                                                                                                          forceInt(saleItems['Quantity']) if forceDouble(saleItems['Quantity']).is_integer() else saleItems['Quantity'],
                                                                                                          saleItems['Price'])
                                    else:
                                        newAction[u'Отпущено'] = ''

                                    newAction[u'Дата отпуска'] = forceDate(recordSocLLORecipe.value('SaleDate')).toString('dd.MM.yyyy')
                                    newAction[u'Аптека'] = forceString(recordSocLLORecipe.value('AOName'))
                                    newAction[u'Примечание'] = u'Рецепт загружен из ПЦ ЛЛО {0}'.format(QDate().currentDate().toString('dd.MM.yyyy'))
                                    newAction.save(idx=-1)

                            except Exception as e:
                                self.log(u'Ошибка при записи в БД', exceptionToUnicode(e), 2, traceback.extract_stack()[:-1])

                        itsFirst = False
                    else:
                        break
                return False
            except Exception as e:
                self.log(u'Ошибка при установке соединения с сервисом download', exceptionToUnicode(e), 2, traceback.extract_stack()[:-1])
                return True
        else:
            self.log(u'Не задан URL сервиса!', '', 2)


    def getDictFromSoap(self, listFields, fieldsNamesList, saleItemsList):
        fieldsDictList = []
        for item in listFields:
            fieldsDict = dict.fromkeys(fieldsNamesList)
            for name in fieldsNamesList:
                # SaleItems - раздел с данными об отпуске в ответе сервиса
                if name == 'SaleItems' and hasattr(item, name):
                    saleItemsDict = []
                    for i, sale in enumerate(item[name]):
                        saleItemsDict.append(dict.fromkeys(saleItemsList))
                        for saleName in saleItemsList:
                            if hasattr(sale[1][0], saleName):
                                if isinstance(sale[1][0][saleName], Text):
                                    saleItemsDict[i][saleName] = forceString(unicode(sale[1][0][saleName]))
                                elif isinstance(sale[1][0][saleName], bool):
                                    saleItemsDict[i][saleName] = forceBool(sale[1][0][saleName])
                                elif isinstance(sale[1][0][saleName], datetime):
                                    saleItemsDict[i][saleName] = forceDateTime(sale[1][0][saleName])
                                else:
                                    saleItemsDict[i][saleName] = sale[1][0][saleName]
                    fieldsDict[name] = saleItemsDict
                else:
                    if hasattr(item, name):
                        if isinstance(item[name], Text):
                            fieldsDict[name] = forceString(unicode(item[name]))
                        elif isinstance(item[name], bool):
                            fieldsDict[name] = forceBool(item[name])
                        elif isinstance(item[name], datetime):
                            fieldsDict[name] = forceDateTime(item[name])
                        else:
                            fieldsDict[name] = item[name]
            fieldsDictList.append(fieldsDict)

        return fieldsDictList


    def getFieldsNames(self):
        fieldsNamesList = ['Seria', 'Number', 'State', 'ProgramCode', 'ProgramName', 'SourceType', 'Snils',
                          'PatientLastname', 'PatientFirstname', 'PatientMiddlename', 'PatientBirthday',
                          'PatientSex', 'PrivilegeCategory', 'Nosology', 'Mkb', 'ValidPeriod', 'IsVk',
                          'protocolNumber', 'ProtocolDate', 'IssueDate', 'MoOgrn', 'MoName', 'PCod',
                          'DoctorLastname', 'DoctorFirstname', 'DoctorMiddlename', 'IsTrn', 'ProductCode',
                          'ProductName', 'CureformCode', 'CureformName', 'Dosage', 'PackageSize', 'Quantity',
                          'Signa', 'IncomeDate', 'SaleDate', 'AOCode', 'AOName', 'PayMode',
                          'MCod', 'Nonresident', 'PatientAddress', 'SaledByFap',
                          'PrivilegeCategoryOriginal', 'SaleItems']
        saleItemsList = ['ProductCode', 'ProductName', 'Dosage', 'PackageSize', 'Quantity', 'Price',
                         'ContractNumber', 'ServiceNumber', 'ContractPrice']

        return fieldsNamesList, saleItemsList


    def main(self):
        self.preferences = CPreferences(u'/root/.config/samson-vista/downloadRecipeLLO.ini')
        self.preferences.load()

        app = QtGui.qApp
        # logDir = forceString(self.preferences.appPrefs.get('logDir', None))
        # if not logDir:
        #     logDir = '/var/log/downloadRecipeLLO'
        # app.logDir = logDir
        app.logLevel = self.preferences.appPrefs.get('logLevel', 2)

        self.openDatabase()
        if self.db:
            downloadUrl = str(forceString(self.preferences.appPrefs[u'downloadservice']))
            clientIdList = forceString(self.preferences.appPrefs[u'clientId'])
            for clientId in clientIdList.split(','):
                countTry = 1
                download = self.download(downloadUrl, str(clientId))
                while download and countTry < 4:
                    self.log(u'Попытка соединения с сервисом download {0} из 3'.format(countTry), '', 2)
                    time.sleep(60)
                    download = self.download(downloadUrl, str(clientId))
                    countTry += 1
            self.closeDatabase()


def create_ssl_context(verify=True, cafile=None, capath=None):
    """Set up the SSL context.
    """
    # This is somewhat tricky to do it right and still keep it
    # compatible across various Python versions.

    try:
        # The easiest and most secure way.
        # Requires either Python 2.7.9 or 3.4 or newer.
        context = ssl.create_default_context(cafile=cafile, capath=capath)
        if not verify:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
    except AttributeError:
        # ssl.create_default_context() is not available.
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        except AttributeError:
            # We don't even have the SSLContext class.  This smells
            # Python 2.7.8 or 3.1 or older.  Bad luck.
            return None
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        if verify:
            context.verify_mode = ssl.CERT_REQUIRED
            if cafile or capath:
                context.load_verify_locations(cafile, capath)
            else:
                context.set_default_verify_paths()
        else:
            context.verify_mode = ssl.CERT_NONE
    return context


class HTTPSTransport(suds.transport.http.HttpTransport):
    """A modified HttpTransport using an explicit SSL context.
    """

    def __init__(self, context, **kwargs):
        """Initialize the HTTPSTransport instance.

        :param context: The SSL context to use.
        :type context: :class:`ssl.SSLContext`
        :param kwargs: keyword arguments.
        :see: :class:`suds.transport.http.HttpTransport` for the
            keyword arguments.
        """
        suds.transport.http.HttpTransport.__init__(self, **kwargs)
        self.ssl_context = context
        self.verify = (context and context.verify_mode != ssl.CERT_NONE)


    def u2handlers(self):
        """Get a collection of urllib handlers.
        """
        handlers = suds.transport.http.HttpTransport.u2handlers(self)
        if self.ssl_context:
            try:
                handlers.append(HTTPSHandler(context=self.ssl_context,
                                             check_hostname=self.verify))
            except TypeError:
                # Python 2.7.9 HTTPSHandler does not accept the
                # check_hostname keyword argument.
                #
                # Note that even older Python versions would also
                # croak on the context keyword argument.  But these
                # old versions do not have SSLContext either, so we
                # will not end up here in the first place.
                handlers.append(HTTPSHandler(context=self.ssl_context))
        return handlers


class PrunePlugin(MessagePlugin):
    last_sent = None
    last_received = None

    def marshalled(self, context):
        context.envelope = context.envelope.prune()

    def sending(self, context):
        self.last_sent = str(context.envelope)

    def received(self, context):
        self.last_received = str(context.reply)

if __name__ == '__main__':
    app = CMyApp(sys.argv)
    app.main()
