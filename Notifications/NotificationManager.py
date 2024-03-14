# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Управление оповещениями пациентов"""

import re
import os
import csv
import json
import requests
from urllib2 import HTTPError

from PyQt4 import QtGui
from PyQt4.QtCore import QDateTime, QDate

from library.PrintInfo import CInfoContext
from library.PrintTemplates import readUrl, compileAndExecTemplate, loadJson
from library.SendMailDialog import sendMailInt
from library.Utils import forceRef, forceString, forceInt, toVariant, forceStringEx, anyToUnicode

from Exchange.Utils import tbl
from Orgs.PersonInfo import CPersonInfo
from Orgs.Utils import COrgInfo, COrgStructureInfo, CActivityInfo
from Registry.Utils import CClientInfo
from Events.ActionInfo import CActionInfo


from Notifications.NotificationRule import (tblNotificationRule,
                                            CNotificationRule)

tblNotificationLog = 'Notification_Log'
kindCodeSMS = '1'
kindCodeEmail = '2'
kindCodeViber = '3'
kindCodeIPPhone = '33'
strSuccess = u'Успех'
strUnknownError = u'Неизвестный код ошибки'

class CNotificationManager(object):
    u"""Реализация управления оповещениями"""

    mapSmsErrorCode = {
        1 : u'Внутренняя ошибка.',
        2 : u'Ошибка парсинга.',
        3 : u'Ошибка авторизации.',
        4 : u'невалидное значение (режима вывода) mode',
        5 : u'невалидное значение (формата вывода) output',
        10 : u'Ошибка номера абонента',
        11 : u'Ошибка имени отправителя',
        12 : u'Ошибка текста сообщения',
        14 : u'Ошибка пользовательского messageId',
        15 : u'Недостаточно средств на балансе',
        16 : u'Ошибка отправки (не настроена маршрутизация)',
        18 : u'Сообщение с указанным userMessageId уже было',
        19 : u'Номер находится в «Чёрном списке»',
        20 : u'Превышено допустимое кол-во абонентов в запросе на множественную'
             u' отправку',
        25 : u'Неверный формат smsId',
        26 : u'Неверный формат userMessageId',
        27 : u'Не передано ни одного Id сообщения',
        28 : u'Нельзя передавать и smsId и userMessageId одновременно',
        29 : u'Сообщение с указанным Id не найдено',
        30 : u'Ошибка очередности каналов отправки order',
        34 : u'Ошибка таймаута («времени жизни») messengerModeTTL на Viber',
        35 : u'Неверный набор параметров для контента (текст, картинка, кнопка'
             u')',
        36 : u'Некорректный URL для картинки',
        37 : u'Некорректный URL для кнопки',
        38 : u'Некорректный маршрут',
        40 : u'Ошибка таймаута («времени жизни») smsTTL в SMS',
        44 : u'Не задан параметр options для поля типа enum',
        45 : u'Не знадано название поля',
        46 : u'Неверный тип поля',
        47 : u'Поле типа `link` должно называться `link`',
        48 : u'Поле типа `link` должно иметь значение по умолчанию (оно будет '
             u'подставлено в название кнопки при отправке через Viber)',
        50 : u'Такого шаблона не существует',
        51 : u'У вас нет доступа к данному шаблону',
        52 : u'Ошибка при проверке значений полей',
        53 : u'Не передано обязательное значение',
        54 : u'Неверный формат даты',
        55 : u'В базе не заданы возможные значения для поля типа enum',
        56 : u'Неверное значение для данного типа поля',
        57 : u'Неверное значение для поля типа link (невалидная ссылка)',
        59 : u'У данного пользователя нет ни одного шаблона',
        60 : u'Неверный формат id базы данных',
        61 : u'Имя базы не задано или содержит недопустимые символы',
        62 : u'Не передано ни одного подписчика для импорта',
        63 : u'Нет поля в данной базе абонентов',
    }


    def __init__(self):
        if hasattr(QtGui.qApp, 'db'):
            self._db = QtGui.qApp.db
            self._tblNotificationLog = tbl(tblNotificationLog)
            self._tblNotificationRule = tbl(tblNotificationRule)
            self._tblClientContact = tbl('ClientContact')
            self._tblClient = tbl('Client')
        prefs = QtGui.qApp.preferences.appPrefs if hasattr(QtGui.qApp,
                                                           'preferences') else {}
        self.__url = forceString(prefs.get('url', 'test'))
        self.__smsUser = forceString(prefs.get('smsLogin', 'test'))
        self.__smsPassword = forceString(prefs.get('smsPassword', 'test'))
        self.__smsSender = forceString(prefs.get('smsSender', 'SAMSON'))
        self.__viberSender = forceString(prefs.get('viberSender', 'SAMSON'))
        self.__apiKey = forceString(prefs.get('apiKey'))

        self._IPPhoneNotificationQuantity = 0
        self._IPPhoneResponsesQuantity = 0

    def notifyClient(self, clientInfoList, ruleId, msg=''):
        u"""Создает оповещения по списку пациентов по заданному правилу"""
        record = self._db.getRecord(self._tblNotificationRule, '*', ruleId)

        if record and clientInfoList:
            rule = CNotificationRule(record)
            noAddrClientList = []
            for (clientId, scheduleItem, schedule) in clientInfoList:
                recordClient = self._db.getRecord(self._tblClient,  'firstName, patrName, lastName', clientId)
                if rule.type == 1 and rule.condition == 3:
                    # text = rule.template
                    text = parseGroupQuizTemplate(rule.template, recordClient, msg=msg)
                else:
                    text = parseNotificationTemplate(rule.template,
                                                     clientId,
                                                     (scheduleItem, schedule),
                                                     msg=msg)

                if not text:
                    break

                for (_, kindId, contactTypeId) in rule.notificationKindList:
                    addrList = self.getClientContact(clientId, contactTypeId)
                    if not addrList:
                        lastName = unicode(forceString(recordClient.value('lastName')))
                        noAddrClientList.append(lastName)

                    for addr in addrList:
                        if rule.type == 1 and rule.condition == 3:
                            self.createNotificationLogRecord(
                                ruleId, kindId, text, addr, clientId, None, True)
                        else:
                            self.createNotificationLogRecord(
                            ruleId, kindId, text, addr, clientId)
            return noAddrClientList


    def notifyClientWithResearchInfo(self, ruleId, actionInfoList, msg=''):
        u"""Создает оповещения по списку пациентов по заданному правилу, относящемуся к результатам исследований"""
        record = self._db.getRecord(self._tblNotificationRule, '*', ruleId)
        
        if record and actionInfoList:
            rule = CNotificationRule(record)
            noAddrClientList = []
            if rule.condition == rule.ncdResearch: #TODO более точное условие или оформление условия не через числа
                for singleActionList in actionInfoList:
                    clientId, actionId, actionTypeId = singleActionList
                    recordClient = self._db.getRecord(self._tblClient,  'firstName, patrName, lastName', clientId)
                    text = parseResearchTemplate(rule.template, actionId, rule.actionType_id, clientId, msg=msg)
                    if not text:
                        QtGui.qApp.log(u'Ошибка в шаблоне: ', u'Шаблон пуст. Action_id={}'.format(actionId), fileName='notificationTool.log')
                        break
                    if u'NULL' in text:
                        QtGui.qApp.log(u'Ошибка в шаблоне: ', u'У одного из свойств действия в шаблоне отсутствует результат. Оповещение не создано. Action_id={}'.format(actionId), fileName='notificationTool.log')
                        break
                    for (kindCode, kindId, contactTypeId) in rule.notificationKindList:
                        addrList = self.getClientContact(clientId, contactTypeId)
                        if not addrList:
                            logId = self.createNotificationLogRecord(ruleId, kindId, text, '', clientId, actionId)
                            systemId = forceRef(self._db.translate('rbExternalSystem', 'code', 'SamsonExtNotification', 'id'))
                            self.writeActionConfirmation(logId, systemId, actionId)
                            lastName = unicode(forceString(recordClient.value('lastName')))
                            noAddrClientList.append(lastName)
                            continue

                        for addr in addrList:
                            logId = self.createNotificationLogRecord(
                                ruleId, kindId, text, addr, clientId, actionId)
                            systemId = forceRef(self._db.translate('rbExternalSystem', 'code', 'SamsonExtNotification', 'id'))
                            self.writeActionConfirmation(logId, systemId, actionId)
                            
                return noAddrClientList


    def writeActionConfirmation(self, logId, systemId, actionId):
        tableActionExport = self._db.table('Action_Export')
        record = tableActionExport.newRecord()
        record.setValue('master_id', toVariant(actionId))
        record.setValue('system_id', toVariant(systemId))
        record.setValue('externalId', toVariant(logId))
        record.setValue('dateTime', toVariant(QDateTime.currentDateTime()))
        return self._db.insertRecord(tableActionExport, record)


    def getClientContact(self, clientId, contactTypeId):
        u"""Возвращает список контактов пациента по типу, или пустой список"""
        result = []

        cond = [
            self._tblClientContact['client_id'].eq(clientId),
            self._tblClientContact['contactType_id'].eq(contactTypeId),
            self._tblClientContact['deleted'].eq(0)
        ]

        recordList = self._db.getRecordList(self._tblClientContact, 'contact',
                                            cond)

        for record in recordList:
            result.append(forceString(record.value(0)))

        return result


    def createNotificationLogRecord(self, ruleId, kindId, text, addr, clientId, actionId = None, isQuiz = None):
        u"""Создает запись в журнале оповещений, возвращает ее идентификатор"""
        record = self._tblNotificationLog.newRecord()
        record.setValue('createPerson_id', toVariant(QtGui.qApp.userId))
        record.setValue('createDatetime',
                        toVariant(QDateTime.currentDateTime()))
        record.setValue('rule_id', toVariant(ruleId))
        record.setValue('kind_id', toVariant(kindId))
        record.setValue('addr', toVariant(addr))
        record.setValue('text', toVariant(text))
        record.setValue('recipient', toVariant(clientId))
        #record.setValue('sendDatetime', toVariant(QDateTime.currentDateTime()))
        record.setValue('status', 0) if addr else record.setValue('status', 10)
        if not addr:
            record.setValue('lastErrorText', u'У пациента не задан контакт')
        if actionId:
            record.setValue('action_id', actionId)
        #if isQuiz and actionId:
            #record.setValue('lastErrorText', u'опрос onlineLPU')
            # record.setValue('status', 0)
            #record.setValue('action_id', actionId)
        # if isQuiz and not actionId:
            #record.setValue('lastErrorText', u'групповой опрос onlineLPU')
            # record.setValue('status', 0)
        return self._db.insertRecord(self._tblNotificationLog, record)


    def logNotification(self, logId, result, errorStr):
        u"""Записывает результат оповещения в журнал"""
        self._db.transaction()
        try:
            record = self._db.getRecord(self._tblNotificationLog, '*', logId)
            if result:
                record.setValue('status', toVariant(9))
                record.setValue('sendDatetime', toVariant(QDateTime.currentDateTime()))
            else:
                record.setValue('status', toVariant(10))
                record.setValue('lastErrorText', toVariant(errorStr))
            # record.setValue('lastErrorText', toVariant(
            #     strSuccess if result else errorStr))
            currentAttempt = forceInt(record.value('attempt')) + 1
            record.setValue('attempt', toVariant(currentAttempt))
            newLogId = self._db.updateRecord(self._tblNotificationLog, record)
            externalId = ''
            if result:
                if type(result) is tuple and len(result) == 2:
                    if isinstance(result[1], basestring):
                        externalId = result[1]
            if externalId:
                record = self._db.getRecord(self._tblNotificationLog, '*', newLogId)
                tableExport = self._db.table('Notification_Log_Export')
                newRecord = tableExport.newRecord()
                tableExternalSystem = 'rbExternalSystem'
                imobisSystemId = forceRef(self._db.translate('rbExternalSystem', 'code', 'Imobis', 'id'))
                newRecord.setValue('master_id', toVariant(record.value('id')))
                newRecord.setValue('masterDatetime', toVariant(record.value('modifyDatetime')))
                newRecord.setValue('system_id', toVariant(imobisSystemId))
                newRecord.setValue('success', toVariant(1))
                newRecord.setValue('datetime', toVariant(QDateTime.currentDateTime()))
                newRecord.setValue('externalId', toVariant(externalId))
                exportId = self._db.insertOrUpdate(tableExport, newRecord)
            self._db.commit()
        except:
            self._db.rollback()
            QtGui.qApp.logCurrentException()


    def confirmNotification(self, logId, result, errorStr):
        u"""Подтверждает оповещение сразу после успешной отправки"""
        record = self._db.getRecord(self._tblNotificationLog, '*', logId)
        record.setValue('status', toVariant(11))
        record.setValue('confirmationDatetime', toVariant(QDateTime.currentDateTime()))
        self._db.updateRecord(self._tblNotificationLog, record)
        self._writeConfirmation(logId)


    def sendNotification(self, notificationKindCode, text, addr, externalId, recipientId, path, smsConfig=None, attach=None):
        u"""Отправляет оповещение"""
        result = False
        errorStr = ''

        if notificationKindCode == kindCodeSMS:
            (result, errorStr) = self._sendSMSNotification(
                text, addr, externalId, smsConfig)
        elif notificationKindCode == kindCodeEmail:
            (result, errorStr) = sendEmailNotification(text, addr, attach)
        elif notificationKindCode == kindCodeViber:
            (result, errorStr) = self._sendViberNotification(text, addr,
                                                             externalId)
        elif notificationKindCode == kindCodeIPPhone:
            (result, errorStr) = self._sendIPPhoneNotification(text, addr, externalId, recipientId, path)
        else:
            errorStr = (u'Неподдерживаемый вид оповещения %s' %
                        notificationKindCode)

        return result, errorStr


    def _sendIPPhoneNotification(self, text, addr, externalId, recipientId, path):
        try:
            mode = 'wb' if not os.path.exists(path) else 'ab'
            with open(path, mode) as f:
                writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([externalId, recipientId, addr.encode('utf-8'), text.encode('utf-8')])
                f.close()
            self._IPPhoneNotificationQuantity += 1
            return (True, '')
        except Exception, e:
            QtGui.qApp.logCurrentException()
            return (False, anyToUnicode(e))


    def readDataAndUpdateIPPhoneNotification(self, filePath, basePath):
        path = basePath + '/' + filePath
        with open(path, 'rb') as f:
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if not row:
                    raise Exception(u'Пустое значение для обработки из файла .in. Возможно пустая строка в файле {}.'.format(path))
                self._db.transaction()
                try:
                    updatedLogId = self.writeDataToIPPhoneNotification(row)
                    if updatedLogId != int(row[0]):
                        raise Exception(u'Не найдена запись или найдена неверная запись id={} для обновления в файле {}'.format(updatedLogId, path))
                    self._db.commit()
                    self._IPPhoneResponsesQuantity +=1
                except Exception:
                    self._db.rollback()
                    f.close()
                    raise
            f.close()


    def writeDataToIPPhoneNotification(self, data):
        logId = data[0]
        status = data[1]
        if status == '1':
            result = u'Удалось дозвониться.'
            mappedStatus = 5
        elif status == '2':
            result = u'Удалось дозвониться и получить подтверждение.'
            mappedStatus = 6
        elif status == '3':
            result = u'Удалось дозвониться, но подтверждение не получено.'
            mappedStatus = 7
        elif status == '4':
            result = u'Не удалось дозвониться.'
            mappedStatus = 8
        else:
            raise Exception(u'Неизвестный статус ответа от IP телефонии %s' % status)
        
        tableNotificationLog = self._tblNotificationLog
        record = self._db.getRecord(tableNotificationLog, [tableNotificationLog['id'], tableNotificationLog['result'], tableNotificationLog['status']], logId)
        if record and record.value('result').toString() == '':
            record.setValue('result', result)
            record.setValue('status', mappedStatus)
            return self._db.updateRecord(tableNotificationLog, record)


    def _sendViberNotification(self, text, addr, externalId):
        result = False
        errorStr = ''
        url = 'https://api.hub.imobis.ru/v3/message/send'
        headers = ({'Authorization' : 'Token {0}'.format(self.__apiKey)}
                   if self.__apiKey else {})
        phone = filter(lambda ch: ch not in '+()-', addr)
        postData = [{
            'custom_id' : externalId,
            'channel': 'viber',
            'phone': phone,
            'sender': self.__viberSender,
            'text': text,
            'ttl': 30
        }, {
            'custom_id' : externalId,
            'channel': 'sms',
            'phone': phone,
            'sender': self.__smsSender,
            'text': text
        }]

        try:
            rval = readUrl(url, postData=postData, jsonData=True,
                           headers=headers)

            if rval.get('result', '') == 'ok':
                result = True
            else:
                errorStr = rval.get('error', {}).get('desc', strUnknownError)

        except HTTPError, error:
            eDict = loadJson(error.read())
            if isinstance(eDict, dict):
                errorStr = eDict.get('error', {}).get('desc', strUnknownError)
            else:
                errorStr = strUnknownError
        except IOError, error:
            QtGui.qApp.logCurrentException()
            errorStr = u'Произошла ошибка %s' % unicode(error)

        return (result, errorStr)


    def _sendSMSNotification(self, text, addr, externalId, config):
        u"""Отправляет СМС оповещение через Imobis по новому протоколу"""
        result = False
        errorStr = ''

        url = config['url']
        token = config['token']
        sender = config['sender']
        ttl = config['ttl']
        report = config['report']

        headers = { 'Content-type': 'application/json',
                    'Authorization': 'Token %s' % token
                  }

        postData = {
            'sender': sender,
            'phone':  filter(lambda ch: ch not in '+()-', addr),
            'text': text,
            'custom_Id': forceString(externalId),
            'ttl' : ttl if ttl else 172800,
            #'report': report
        }
        if report:
            postData['report'] = report

        try:
            response = requests.post(url, json=postData, headers=headers)
        except Exception, e:
            QtGui.qApp.logCurrentException()
            e = u'Произошла ошибка %s' % unicode(e)            
            try:
                response = requests.post(url, json=postData, headers=headers, verify = False)
            except Exception, e:
                QtGui.qApp.logCurrentException()
                e = u'Произошла ошибка %s' % unicode(e)
                return ('', e)
        statusCode = response.status_code
        content = response.content
        contentSerialized = json.loads(content)
        respHeaders = ''
        for k, v in response.headers.items():
            respHeaders = respHeaders + '%s: %s' % (k, v) + '\n'

        if statusCode == 200 and contentSerialized['result'] == 'success':
            result = (True, contentSerialized['id'])
        else:
            errorStr = u'Ошибка. Код статуса: %d, ответ: %s' % (statusCode, content)

        request = response.request
        reqBody = request.body
        reqHeaders = ''
        for k, v in request.headers.items():
            reqHeaders = reqHeaders + '%s: %s' % (k, v) + '\n'
        reqUrl = request.url
        reqMethod = request.method
        QtGui.qApp.log(u'Request Sms Send: \n', 'url: '+reqUrl+'\n'+'method: '+reqMethod+'\n'+'headers'+reqHeaders+'\n'+'body: '+reqBody+'\n', fileName='notificationTool.log')
        QtGui.qApp.log(u'Response Sms Send: \n', 'StatusCode: '+unicode(statusCode)+'\n'+'headers'+respHeaders+'\n'+'body: '+content+'\n', fileName='notificationTool.log')

        return (result, errorStr)


    def _getSMSConfirmation(self, externalId):
        u"""Получает код подтверждения для SMS"""
        result = False
        url = 'http://gate.imobis.ru/callback'

        getData = {
            'user': self.__smsUser,
            'password': self.__smsPassword,
            'userMessageId': externalId,
            'mode' : 'brief',
        }

        try:
            rval = forceString(readUrl(url, getData))

            if rval == 'DELIVRD':
                result = True

        except IOError:
            QtGui.qApp.logCurrentException()

        return result


    def _getSuccessfullLogRecords(self, ruleId, kindId):
        u"""Выдает список успешно отправленных уведомлений"""
        cond = [
            self._tblNotificationLog['rule_id'].eq(ruleId),
            self._tblNotificationLog['kind_id'].eq(kindId),
            self._tblNotificationLog['lastErrorText'].eq(''),
            self._tblNotificationLog['status'].eq(9),
            self._tblNotificationLog['confirmationDatetime'].isNull(),
            self._tblNotificationLog['sendDatetime'].dateGe(
                QDate.currentDate().addDays(-2)),
        ]

        return self._db.getIdList(self._tblNotificationLog, where=cond)


    def processNotificationConfirmation(self, rule):
        u"""Обработка подтверждений отправки, реализовано для SMS"""
        for (kindCode, kindId, _) in rule.notificationKindList:
            if kindCode == kindCodeSMS:
                idList = self._getSuccessfullLogRecords(rule.id, kindId)

                for _id in idList:
                    if self._getSMSConfirmation(_id):
                        self._writeConfirmation(_id)


    def _writeConfirmation(self, logId):
        u"""Устанавливает время подтверждения отправки"""
        record = self._db.getRecord(self._tblNotificationLog,
                                    'id, confirmationDatetime', logId)
        record.setValue('confirmationDatetime', toVariant(
            QDateTime.currentDateTime()))
        self._db.updateRecord(self._tblNotificationLog, record)



def sendEmailNotification(text, addr, attach):
    u"""Отправляет оповещение по электронной почте"""
    body = forceStringEx(QtGui.QTextDocument(text).toHtml('utf-8'))
    QtGui.qApp.log(u'Email body: \n', body + '\n', fileName='notificationTool.log')
    attachList = [attach] if attach else []
    (result, errorStr) = sendMailInt(addr, u'Оповещение', body, attachList)
    if result:
        QtGui.qApp.log(u'Email Send without errors: \n', 'No email errors from smtplib', fileName='notificationTool.log')
    else:
        QtGui.qApp.log(u'Email Send with errors: \n', errorStr, fileName='notificationTool.log')
    return (result, errorStr)


def parseNotificationTemplate(template, clientId, scheduleItem=None, msg=''):
    u"""Обрабатывает шаблон уведомления"""
    result = None

    try:
        context = CInfoContext()
        client = context.getInstance(CClientInfo, clientId)

        data = {
            'client': client,
            'message': msg,
            'currentOrganisation': context.getInstance(COrgInfo,
                                                       QtGui.qApp.currentOrgId()),
            'currentOrgStructure': context.getInstance(COrgStructureInfo,
                                                       QtGui.qApp.currentOrgStructureId()),
        }

        if isinstance(scheduleItem, tuple):
            (item, schedule) = scheduleItem

            if schedule:
                personId = schedule.personId
                person = context.getInstance(CPersonInfo, personId)
                data['office'] = schedule.office
                data['person'] = person
                activityId = schedule.activityId

                if activityId:
                    activity = context.getInstance(CActivityInfo, activityId)
                    data['activity'] = activity

            data['time'] = forceString(item.time) if item else '-'
        elif scheduleItem:
            personId = forceRef(scheduleItem.value('person_id'))
            person = context.getInstance(CPersonInfo, personId)
            data['office'] = forceString(scheduleItem.value('office'))
            data['person'] = person
            data['time'] = forceString(scheduleItem.value('time'))

        templateResult = compileAndExecTemplate('', template, data)
        # убираем escape-символы html:
        doc = QtGui.QTextDocument()
        doc.setHtml(templateResult.content)
        result = forceString(doc.toPlainText()).replace('\n', '\r\n')

    except Exception:
        QtGui.qApp.logCurrentException()

    return result


def parseGroupQuizTemplate(template, record,  msg=''):
    u"""Обрабатывает шаблон группового опроса"""
    result = None
    firstName = unicode(forceString(record.value('firstName')))
    lastName = unicode(forceString(record.value('lastName')))
    patrName = unicode(forceString(record.value('patrName')))

    try:
        appeal = lastName + ' ' + firstName + ' ' + patrName
        #reg = r'\{\{[\s\S]*\}\}'
        reg = r'\{\{ fullName \}\}'
        templateFirstResult = re.sub(reg, appeal, template)
        regMessage = r'\{\{ message \}\}'
        result = re.sub(regMessage, msg, templateFirstResult)

    except Exception:
        QtGui.qApp.logCurrentException()

    return result


def parseResearchTemplate(template, actionId, actionTypeId, clientId, msg=''):
    u"""Обрабатывает шаблон оповещения по информированию о результатах исследования"""
    try:
        context = CInfoContext()
        client = context.getInstance(CClientInfo, clientId)
        data = {'client': client, 'message': msg}
        action = context.getInstance(CActionInfo, actionId)
        #action = context.getInstance(CCookedActionInfo, actionId)
        data['action'] = action
        newTemplate = compileAndExecTemplate('', template, data)
        # убираем escape-символы html:
        doc = QtGui.QTextDocument()
        doc.setHtml(newTemplate.content)
        result = forceString(doc.toPlainText()).replace('\n', '\r\n')
        return result
    except Exception:
        QtGui.qApp.logCurrentException()


if __name__ == '__main__':
    import urllib2
    handler= urllib2.HTTPSHandler(debuglevel=1)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    manager = CNotificationManager()
    (_result, erroText) = manager.sendNotification(kindCodeViber, 'test',
                                                  '+79000000000', 1)
    print u'result={0}, {1}'.format(_result, erroText)
