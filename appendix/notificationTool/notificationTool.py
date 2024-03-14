#!/usr/bin/env python
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
u'''Внешняя утилита обработки оповещений'''

import requests
import logging
import json
import codecs
import locale
import os
import os.path
import shutil
import sys
import tempfile
import traceback
import io
from optparse import OptionParser

from PyQt4 import QtGui
from PyQt4.QtCore import (QCoreApplication, QDir, QDateTime, QDate, 
                          qInstallMsgHandler, QVariant, Qt, SIGNAL)

from datetime import datetime, timedelta
from Exchange.Utils import tbl
from Notifications.NotificationRule import tblNotificationRule
from Notifications.NotificationManager import (CNotificationRule,
                                               CNotificationManager,
                                               tblNotificationLog,
                                               parseNotificationTemplate,
                                               parseGroupQuizTemplate)
from RefBooks.Tables import rbNotificationKind
from Users.Rights import urSendExternalNotifications
from Users.UserInfo import CUserInfo

from library import database
from library.Preferences import CPreferences
from library.Utils import (forceString, toVariant, anyToUnicode, forceRef,
                           forceDateTime, forceInt, forceDate, forceTime)
from library.Attach.WebDAV import CWebDAVClient

try:
    from buildInfo import lastChangedRev  as gLastChangedRev, \
                          lastChangedDate as gLastChangedDate
except ImportError:
    gLastChangedRev = 'unknown'
    gLastChangedDate = 'unknown'

class CMyApp(QCoreApplication):
    u"""Класс приложения оповещений."""
    __pyqtSignals__ = ('dbConnectionChanged(bool)',
                       'currentUserIdChanged()',
                      )

    def __init__(self, _args, verbose, debugUrlLib2):
        QCoreApplication.__init__(self, _args)
        self.logDir = os.path.join(unicode(QDir.toNativeSeparators(
            QDir.homePath())), '.samson-vista')
        self.oldMsgHandler = qInstallMsgHandler(self.msgHandler)
        self.oldEexceptHook = sys.excepthook
        sys.excepthook = self.logException
        self.traceActive = True
        self.homeDir = None
        self.saveDir = None
        self.userId = None
        self.db = None
        self.preferences = CPreferences('notificationTool.ini')
        self.preferences.load()
        self.preferencesDir = self.preferences.getDir()
        self.presets = None
        self.notificationManager = None

        self._tblNotificationRule = None
        self._tblNotificationLog = None
        self._tblRbNotificationKind = None
        self._tblSheduleItem = None
        self._tblSheduleItemExport = None

        self.__verbose = verbose
        self.__statistics = {}
        self.__userRightCache = {}

        if debugUrlLib2:
            import urllib2
            handler = urllib2.HTTPSHandler(debuglevel=1)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)

    def doneTrace(self):
        self.traceActive = False
        qInstallMsgHandler(self.oldMsgHandler)
        sys.excepthook = self.oldEexceptHook


    def currentOrgId(self):
        return forceRef(QtGui.qApp.preferences.appPrefs.get('orgId',
                                                            QVariant()))


    def currentOrgStructureId(self):
        return forceRef(QtGui.qApp.preferences.appPrefs.get('orgStructureId',
                                                            QVariant()))


    def getHomeDir(self):
        if not self.homeDir:
            homeDir = os.path.expanduser('~')
            if homeDir == '~':
                homeDir = anyToUnicode(QDir.homePath())
            if isinstance(homeDir, str):
                homeDir = anyToUnicode(homeDir, locale.getpreferredencoding())
            self.homeDir = homeDir
        return self.homeDir


    def getTmpDir(self, suffix=''):
        return anyToUnicode(tempfile.mkdtemp('', 'samson_%s_'%suffix),
                            locale.getpreferredencoding())


    def getTemplateDir(self):
        result = forceString(self.preferences.appPrefs.get('templateDir', None))
        if not result:
            result = os.path.join(self.logDir, 'templates')
        return result


    def removeTmpDir(self, _dir):
        try:
            shutil.rmtree(_dir, False)
        except:
            self.logCurrentException()


    def highlightRedDate(self):
        return False


    def highlightInvalidDate(self):
        return True


    def setTemplateDir(self, path):
        self.preferences.appPrefs['templateDir'] = QVariant(path)


    def setPrinterName(self, name):
        self.preferences.appPrefs['printer'] = QVariant(name)


    def storePresetToAppPrefs(self, index, preset):
        presetDict = {
            'name':   toVariant(preset.name),
            'serial': toVariant(preset.serial),
            # регистр не сохраняется!
            'numcopies': toVariant(preset.numCopies),
            'date': toVariant(preset.date),
            'number': toVariant(preset.number),
            'resetnumber': toVariant(preset.resetNumber),
            'count': toVariant(preset.count),
            'context':toVariant(preset.context),
        }
        presetsDict = self.preferences.appPrefs.setdefault('presets', {})
        presetsDict[str(index)] = presetDict


    def setPresets(self, presets):
        self.presets = presets
        self.preferences.appPrefs['presets'] = {}
        for i, preset in enumerate(presets):
            self.storePresetToAppPrefs(i, preset)


    def log(self, title, message, stack=None, fileName='error.log'):
        try:
            if not os.path.exists(self.logDir):
                os.makedirs(self.logDir)
            logFile = os.path.join(self.logDir, fileName)
            timeString = unicode(QDateTime.currentDateTime().toString(
                Qt.SystemLocaleDate))
            logString = u'%s\n%s: %s(%s)\n' % (
                '='*72, timeString, title, message)
            if stack:
                try:
                    logString += ''.join(
                        traceback.format_list(stack)).decode('utf-8') + '\n'
                except:
                    logString += 'stack lost\n'
            _file = codecs.open(logFile, mode='a',
                                encoding=locale.getpreferredencoding())
            _file.write(logString)
            _file.close()
        except:
            pass


    def logException(self, exceptionType, exceptionValue, exceptionTraceback):
        title = repr(exceptionType)
        message = anyToUnicode(exceptionValue)
        self.log(title, message, traceback.extract_tb(exceptionTraceback))
        sys.__excepthook__(exceptionType, exceptionValue, exceptionTraceback)


    def logCurrentException(self):
        self.logException(*sys.exc_info())


    def msgHandler(self, type_, msg):
        if type_ == 0: # QtMsgType.QtDebugMsg:
            typeName = 'QtDebugMsg'
        elif type_ == 1: # QtMsgType.QtWarningMsg:
            typeName = 'QtWarningMsg'
        elif type_ == 2: # QtMsgType.QtCriticalMsg:
            typeName = 'QtCriticalMsg'
        elif type_ == 3: # QtFatalMsg
            typeName = 'QtFatalMsg'
        else:
            typeName = 'QtUnknownMsg'

        self.log(typeName, msg, traceback.extract_stack()[:-1])


    def openDatabase(self):
        self.db = None
        if self.preferences.logSQL:
            if not os.path.exists(self.logDir):
                os.makedirs(self.logDir)
            logFile = os.path.join(self.logDir, 'notificationTool.log')
            logging.basicConfig(filename=logFile, level=logging.DEBUG)
        self.db = database.connectDataBase(self.preferences.dbDriverName,
                                           self.preferences.dbServerName,
                                           self.preferences.dbServerPort,
                                           self.preferences.dbDatabaseName,
                                           self.preferences.dbUserName,
                                           self.preferences.dbPassword, 
                                           logger = logging.getLogger('DB') if self.preferences.logSQL else None)
        self.emit(SIGNAL('dbConnectionChanged(bool)'), True)


    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None
            self.emit(SIGNAL('dbConnectionChanged(bool)'), False)


    def notify(self, receiver, event):
        try:
            return QCoreApplication.notify(self, receiver, event)
        except Exception, e:
            if self.traceActive:
                self.logCurrentException()
                print u'Произошла ошибка %s' % anyToUnicode(e)
            return False
        except:
            return False


    def call(self, widget, func, params=()):
        try:
            return True, func(*params)
        except IOError, e:
            msg = ''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (
                    e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))

            print u'Произошла ошибка ввода-вывода %s' % msg
        except Exception, e:
            self.logCurrentException()
            print u'Произошла ошибка %s' % anyToUnicode(e)
        return False, None


    def defaultKLADR(self):
        return ''


    def provinceKLADR(self):
        return ''


    def processNotificationRulesGroupQuiz(self, systemId):
        u"""Обрабатывает все правила, касающиеся групповых опросов"""
        table = tbl(tblNotificationRule)
        cond = [table['class'].eq(CNotificationRule.ncInternal),
                table['deleted'].eq(0),
                table['type'].eq(1),
                table['condition'].eq(3)]
        recordList = self.db.getRecordList(table, where=cond,
                                           order=table['condition'].name())
        self.__statistics['rulesFound'] += len(recordList)
        self.__statistics['groupQuizesRules'] = len(recordList)
        self.__statistics['groupQuizesFound'] = 0
        self.__statistics['groupQuizesSent'] = 0
        self.__statistics['groupQuizesIgnored'] = 0

        for record in recordList:
            rule = CNotificationRule(record)
            self.processNotificationRuleGroupQuiz(rule, systemId)


    def processNotificationRuleGroupQuiz(self, rule, systemId):
        u"""Обрабатывает конкретное правило группового опроса"""
        tblNotificationLog = self._tblNotificationLog
        cols = [tblNotificationLog['id'],
                tblNotificationLog['recipient'],
                tblNotificationLog['text'],
                tblNotificationLog['addr'].alias('email'),
                tblNotificationLog['status'].alias('noteStatus'),
                tblNotificationLog['createDatetime']
            ]
        cond = self.db.joinAnd([tblNotificationLog['status'].eq(0),
                                tblNotificationLog['rule_id'].eq(rule.id)])
        notificationLogs = self.db.getRecordList(tblNotificationLog, cols = cols, where=cond)

        notifications = []
        for notificationLog in notificationLogs:
            note = {}
            note['id'] = int(notificationLog.value('id').toString())
            note['client_id'] = int(notificationLog.value('recipient').toString())
            note['text'] = unicode(notificationLog.value('text').toString())
            note['email'] = unicode(notificationLog.value('email').toString())
            note['createDatetime'] = forceDateTime(notificationLog.value('createDatetime'))
            if self.isNoteCancelled(note['createDatetime'], rule.expiration):
                self.markNote(note['id'], 4)
                continue
            else:
                notifications.append(note)

        self.__statistics['groupQuizesFound'] += len(notifications)
        self.__statistics['logRecordsFound'] += len(notifications)

        if notifications:
            notificationChunks = [notifications[i:i + 50] for i in xrange(0, len(notifications), 50)]
            for notificationChunk in notificationChunks:
                response = self.sendGroupQuizes(notificationChunk, rule.name, rule.id)
                if response['success']:
                    for note in notificationChunk:
                        if note['email'] in response['success']:
                            self.markNote(note['id'], 1)

                            self.__statistics['logRecordsProcessed'] += 1
                            self.__statistics['groupQuizesSent'] += 1
                if response['ignore']:
                    for note in notificationChunk:
                        if note['email'] in response['ignore']:
                            self.__statistics['groupQuizesIgnored'] += 1


        answers = self.getAnswers(rule.id)
        self.writeAnswersToNotes(answers)


    def writeAnswersToNotes(self, quizesWithCorrelatedAnswers):
        u"""Записывает полученные данные от onlineLPU о прочтении групповых опросов в БД и сообщает об этом порталу onlineLPU"""
        uuids = []
        for quizInfo in quizesWithCorrelatedAnswers:
            clientId, noteId = quizInfo['receiver']['ident'].split('-')
            #ruleId = quizInfo['idx']
            if quizInfo['status'] == 'read':
                idN = self.markNote(noteId, 2)
                if idN:
                    uuids.append(quizInfo['uuid'])
            else:
                continue 
        self.markRead(uuids)


    def sendGroupQuizes(self, notifications, name, rule_id):
        u"""Отправляет групповые опросы для данного правила на портал onlineLPU"""
            
        data = self.buildGroupQuizData(notifications, name, rule_id)

        response = requests.post("https://onlinelpu.ru/api", data=data)
        #result = json.loads(response.content)

        self.log(u'URL send group quizes onlineLPU: ', response.url + 
                                                          u'\nResponse code: ' + unicode(response.status_code) + 
                                                          u'\nResponse: ' + response.content.decode('utf-8'), 
                                                          fileName='notificationTool.log')
        print(response.url)
        print(response.status_code)
        print(response.content)

        return json.loads(response.content)


    def buildGroupQuizData(self, notifications, ruleName, rule_id):
        u"""Формирует строку параметров для отправки групповых опросов на портал onlineLPU"""
        data = {}
        data['method'] = 'onlinelpu/sqa/notice.create'
        data['auth[version]'] = '1.0'
        data['auth[client_id]'] = self.preferences.currentInfisCodeEncrypted
        data['auth[client]'] = 'samson.mis'

        data['params[idx]'] = rule_id
        data['params[header]'] = ruleName

        # data['params[receiver][0][email]'] = unicode(note['email'])
        # data['params[receiver][0][ident]'] = unicode(note['client_id']) + '-' + unicode(note['id'])

        i = 0
        for note in notifications:
            data['params[receiver][' + unicode(i) + '][email]'] = unicode(note['email'])
            data['params[receiver][' + unicode(i) + '][ident]'] = unicode(note['client_id']) + '-' + unicode(note['id'])
            data['params[receiver][' + unicode(i) + '][message]'] = unicode(note['text'])
            i = i + 1

        # data['params[message]'] = note['text']
        #data['params[validityPeriod]'] = '2020-10-30'

        return data


    def processNotificationRulesQuiz(self, systemId):
        u"""Обрабатывает все правила, касающиеся индивидуальных опросов"""
        table = tbl(tblNotificationRule)
        cond = [table['class'].eq(CNotificationRule.ncInternal),
                table['deleted'].eq(0),
                table['type'].eq(2),
                table['condition'].eq(3)]
        recordList = self.db.getRecordList(table, where=cond,
                                           order=table['condition'].name())
        self.__statistics['rulesFound'] += len(recordList)
        self.__statistics['quizesRules'] = len(recordList)
        self.__statistics['quizesFound'] = 0
        self.__statistics['quizesSent'] = 0
        self.__statistics['quizesIgnored'] = 0
        for record in recordList:
            rule = CNotificationRule(record)
            self.processNotificationRuleQuiz(rule, systemId)


    def processNotificationRuleQuiz(self, rule, systemId):
        u"""Обрабатывает конкретное правило индивидуального опроса"""
        actionTypeId = rule.actionType_id
        if actionTypeId == 0:
            return

        tableAction = self._tblAction
        tableEvent = self._tblEvent
        tableActionType = self._tblActionType
        table = self._tblAction
        table = table.innerJoin(self._tblActionType,
            self._tblActionType['id'].eq(table['actionType_id']))
        table = table.innerJoin(self._tblEvent,
            self._tblEvent['id'].eq(table['event_id']))
        table = table.leftJoin(self._tblActionExport,
            self._tblActionExport['master_id'].eq(table['id']))
        cols = [tableAction['id'].alias('action_id'),
                tableAction['event_id'],
                tableEvent['client_id'],
                tableActionType['id'].alias('actionType_id'),
                tableActionType['code'].alias('actionTypeCode'),
            ]
        cond = [table['status'].eq(5),
                table['deleted'].eq(0),
                table['actionType_id'].eq(actionTypeId),
                table['master_id'].isNull(),
                table['system_id'].isNull()]
        recordList = self.db.getRecordList(table, cols = cols, where=cond)
        #recordList = self.db.getRecordListGroupBy(table, cols = cols, where=cond, group=self._tblEvent['client_id'].name())
        quizesInfo = []
        for record in recordList:
            clientId = int(record.value('client_id').toString())
            eventId = int(record.value('event_id').toString())
            actionId = int(record.value('action_id').toString())
            quizesInfo.append({'client_id':clientId, 'event_id':eventId, 'action_id':actionId, 'email':[]})

        for (kindCode, kindId, contactTypeId) in rule.notificationKindList:
            if contactTypeId == 4:
                notificationLogs = []
                for quizInfo in quizesInfo:
                    form = self.getForm(actionTypeId, rule, quizInfo['client_id'])
                    addrList = self.notificationManager.getClientContact(quizInfo['client_id'], contactTypeId)
                    notificationLog = {}
                    for addr in addrList:
                        logId = self.notificationManager.createNotificationLogRecord(rule.id,
                                                                                     kindId,
                                                                                     form,
                                                                                     addr,
                                                                                     quizInfo['client_id'],
                                                                                     quizInfo['action_id'],
                                                                                     True)

                        if logId:
                            self.writeActionConfirmation(logId, systemId, quizInfo['action_id'])

        tblNotificationLog = self._tblNotificationLog
        cols = [tblNotificationLog['id'],
                tblNotificationLog['recipient'],
                tblNotificationLog['action_id'],
                tblNotificationLog['text'],
                tblNotificationLog['addr'].alias('email'),
                tblNotificationLog['status'].alias('noteStatus'),
                tblNotificationLog['createDatetime']
            ]
        cond = [tblNotificationLog['status'].eq(0),
                tblNotificationLog['action_id'].isNotNull(),
                tblNotificationLog['action_id'].ne(0),
                tblNotificationLog['rule_id'].eq(rule.id)]
        notificationLogs = self.db.getRecordList(tblNotificationLog, cols = cols, where=cond)

        notifications = []
        for notificationLog in notificationLogs:
            note = {}
            note['id'] = int(notificationLog.value('id').toString())
            note['client_id'] = int(notificationLog.value('recipient').toString())
            note['action_id'] = int(notificationLog.value('action_id').toString())
            note['form'] = unicode(notificationLog.value('text').toString())
            note['email'] = unicode(notificationLog.value('email').toString())
            note['createDatetime'] = forceDateTime(notificationLog.value('createDatetime'))

            if self.isNoteCancelled(note['createDatetime'], rule.expiration):
                self.db.transaction()
                try:
                    self.markNote(note['id'], 4)
                    self.markAction(note['action_id'], 3)
                    self.db.commit()
                except Exception, e:
                    QtGui.qApp.logCurrentException()
                    print('Error: %s' % anyToUnicode(e))
                    self.db.rollback()
                continue
            else:
                notifications.append(note)

        self.__statistics['logRecordsFound'] += len(notificationLogs)
        self.__statistics['quizesFound'] += len(notificationLogs)

        if notifications:
            notificationChunks = [notifications[i:i + 50] for i in xrange(0, len(notifications), 50)]
            for notificationChunk in notificationChunks:
                response = self.sendQuizes(notificationChunk, actionTypeId, rule.name)
                if response['success']:
                    for note in notificationChunk:
                        if note['email'] in response['success']:
                            self.db.transaction()
                            try:
                                self.markNote(note['id'], 1)
                                self.markNoteSendDate(note['id'])
                                self.markAction(note['action_id'], 1)

                                self.__statistics['logRecordsProcessed'] += 1
                                self.__statistics['quizesSent'] += 1
                                self.db.commit()
                            except Exception, e:
                                QtGui.qApp.logCurrentException()
                                print('Error: %s' % anyToUnicode(e))
                                self.db.rollback()
                if response['ignore']:
                    for note in notificationChunk:
                        if note['email'] in response['ignore']:
                            self.__statistics['quizesIgnored'] += 1

        answers = self.getAnswers(actionTypeId)

        self.writeAnswersToActions(answers)


    def isNoteCancelled(self, createDatetime, expiration):
        u"""Определяет, истек ли у опроса срок его отправки на onlineLPU"""
        if expiration == 0:
            expiration = 14
        now = QDateTime.currentDateTime()
        pyNow = now.toPyDateTime()
        pyCreateDatetime = createDatetime.toPyDateTime()
        expirationDatetime = pyCreateDatetime + timedelta(days = expiration)

        return True if expirationDatetime < pyNow else False


    def markAction(self, actionId, status, value=None):
        u"""Помечает действие в БД в соответствии с переданным статусом"""
        tableAction = self._tblAction
        record = self.db.getRecord(tableAction, [tableAction['status'], tableAction['id'], tableAction['note']], actionId)
        if value:
            note = forceString(record.value('note'))
            note = note + ' NotificationValues: ' + value
            record.setValue('note', note)
        if record:
            record.setValue('status', status)
            return self.db.updateRecord(tableAction, record)


    def markQuizNote(self, actionId, result, clientId, status):
        u"""Помечает уведомление об индивидуальном опросе(по actionId) в журнале оповещений в соответствии со статусом"""
        tableNotificationLog = self._tblNotificationLog
        record = self.db.getRecordEx(tableNotificationLog,
                                     [tableNotificationLog['status'], tableNotificationLog['id'], tableNotificationLog['result']],
                                     tableNotificationLog['action_id'].eq(actionId),
                                     tableNotificationLog['recipient'].eq(clientId))
        if record:
            record.setValue('status', status)
            resultJson = json.dumps(result, ensure_ascii=False)
            record.setValue('result', resultJson)
            return self.db.updateRecord(tableNotificationLog, record)


    def markNote(self, noteId, status):
        u"""Помечает уведомление в журнале оповещений соответствующим статусом"""
        tableNotificationLog = self._tblNotificationLog
        record = self.db.getRecord(tableNotificationLog, [tableNotificationLog['status'], tableNotificationLog['id']], noteId)
        if record:
            record.setValue('status', status)
            return self.db.updateRecord(tableNotificationLog, record)


    def markNoteSendDate(self, noteId):
        u"""Помечает уведомление в журнале оповещений датой отправки"""
        tableNotificationLog = self._tblNotificationLog
        record = self.db.getRecord(tableNotificationLog, [tableNotificationLog['sendDatetime'], tableNotificationLog['id']], noteId)
        if record:
            record.setValue('sendDatetime', toVariant(QDateTime.currentDateTime()))
            return self.db.updateRecord(tableNotificationLog, record)


    def sendQuizes(self, notifications, actionTypeId, ruleName):
        u"""Отправляет индивидуальные опросы для данного правила на портал onlineLPU"""
        data = self.buildData(notifications, actionTypeId, ruleName)

        response = requests.post("https://onlinelpu.ru/api", data=data)

        self.log(u'URL send individual quizes onlineLPU: ', response.url + 
                                                    u'\nResponse code: ' + unicode(response.status_code) + 
                                                    u'\nResponse: ' + response.content.decode('utf-8'), 
                                                    fileName='notificationTool.log')
        print(response.url)
        print(response.status_code)
        print(response.content)

        return json.loads(response.content)


    def getForm(self, actionTypeId, rule, clientId):
        u"""Фомрирует форму в соответствии с типом действия для отпарвки ее на портал onlineLPU"""
        result = None
        #tableAction = self._tblAction
        #tableEvent = self._tblEvent
        #tableActionPropertyType = self._tblActionPropertyType
        tableActionType = self._tblActionType
        table = self._tblActionPropertyType
        cond = [table['actionType_id'].eq(actionTypeId),
                table['deleted'].eq(0),
                ]
        cols = [table['id'].alias('questionTypeId'),
                table['name'].alias('questionName'),
                table['typeName'].alias('questionTypeName')
               ]
        table = table.innerJoin(tableActionType, tableActionType['id'].eq(table['actionType_id']))
        recordList = self.db.getRecordList(table, cols = cols, where=cond)
        questions = []
        form = unicode(rule.template)

        recordClient = self.db.getRecord(self._tblClient, 'firstName, patrName, lastName, birthDate', clientId)
        result = parseGroupQuizTemplate(form, recordClient)

        for record in recordList:
            question = {'id': unicode(record.value('questionTypeId').toString()),
                        'name': unicode(record.value('questionName').toString()),
                        'typeName': unicode(record.value('questionTypeName').toString())}
            questions.append(question)
            result = result + self.addField(result, question)
        result = result + u'; return builder; }'

        return result


    def buildData(self, notifications, actionTypeId, ruleName):
        u"""Формирует строку параметров для отправки индивидуальных опросов на портал onlineLPU"""
        data = {}
        data['method'] = 'onlinelpu/sqa/question.create'

        # data['params[form]'] = form
        data['params[idx]'] = actionTypeId
        data['params[header]'] = ruleName

        i = 0
        for note in notifications:
            data['params[receiver][' + unicode(i) + '][email]'] = unicode(note['email'])
            data['params[receiver][' + unicode(i) + '][quizId]'] = unicode(note['client_id']) + '-' + unicode(note['action_id'])
            data['params[receiver][' + unicode(i) + '][form]'] = unicode(note['form'])
            i = i + 1
        # data['params[values][0][k1]']: 'test1',
        #data['params[validityPeriod]'] = '2020-10-30'

        data['auth[version]'] = '1.0'
        data['auth[client_id]'] = self.preferences.currentInfisCodeEncrypted
        data['auth[client]'] = 'samson.mis'

        return data


    def addField(self, form, question):
        if question['typeName'] == 'String' or question['typeName'] == 'Double' or question['typeName'] == 'Integer':
            field = u".add('%s', TYPE.TextType, {label: '%s', required: true})" % (question['id'], question['name'])
        elif question['typeName'] == 'Boolean':
            field = u".add('%s', TYPE.CheckboxType, {label: '%s'})" % (question['id'], question['name'])
        elif question['typeName'] == 'Date':
            field = u".add('%s', TYPE.DateType, {label: '%s', required: true})" % (question['id'], question['name'])
        elif question['typeName'] == 'Time':
            field = u".add('%s', TYPE.TimeType, {label: '%s', required: true})" % (question['id'], question['name'])
#        elif question['typeName'] == 'Double' or question['typeName'] == 'Integer':
#            field = u".add('%s', TYPE.TextType, {mask:'0*.00', label: '%s', required: true})" % (question['id'], question['name'])
        else:
            return ''

        return field


    def getAnswers(self, actionTypeId):
        u"""Отправка запроса на получение ответов от портала onlineLPU по групповым и индивидуальным опросам"""
        data = {}
        data['method'] = 'onlinelpu/sqa/get'
        data['params[idx]'] = actionTypeId
        # infisCode = self.preferences.currentInfisCodeEncrypted
        data['auth[version]'] = '1.0'
        data['auth[client_id]'] = self.preferences.currentInfisCodeEncrypted
        data['auth[client]'] = 'samson.mis'

        resp = requests.post("https://onlinelpu.ru/api", data=data)

        self.log(u'URL request answers from onlineLPU: ', resp.url + 
                                                          u'\nResponse code: ' + unicode(resp.status_code) + 
                                                          u'\nResponse: ' + resp.content.decode('utf-8'), 
                                                          fileName='notificationTool.log')
        print(resp.url)
        print(resp.status_code)
        print(resp.content)

        quizesWithCorrelatedAnswers = json.loads(resp.content)

        return quizesWithCorrelatedAnswers


    def writeAnswersToActions(self, quizesWithCorrelatedAnswers):
        u"""Записывает полученные данные от onlineLPU о прочтении индивидуальных опросов в БД и сообщает об этом порталу onlineLPU"""
        uuids = []
        for quizInfo in quizesWithCorrelatedAnswers:
            questions = []
            answers = quizInfo['values']
            for key, value in quizInfo['values'].iteritems():
                questions.append(key)
            clientId, actionId = quizInfo['receiver']['quizId'].split('-')
            courseActionRecordList = self.getCourseActionInfo(actionId, clientId)
            tableAction = self._tblAction
            table = tableAction
            if quizInfo['status'] != 'passed':
                self.db.transaction()
                try:
                    idA = self.markAction(actionId, 6)
                    idN = self.markQuizNote(actionId, None, clientId, 3)
                    if idA and idN:
                        uuids.append(quizInfo['uuid'])
                    self.db.commit()
                except Exception, e:
                    QtGui.qApp.logCurrentException()
                    print('Error: %s' % anyToUnicode(e))
                    self.db.rollback()
                if not courseActionRecordList:
                    continue
            table = table.innerJoin(self._tblEvent, self._tblEvent['id'].eq(table['event_id']))
            table = table.innerJoin(self._tblClient, self._tblClient['id'].eq(clientId))
            cols = [tableAction['id'], tableAction['status']]
            where = [tableAction['id'].eq(actionId), tableAction['deleted'].eq(0), self.db.joinOr([tableAction['status'].eq(1),
                                                                                                   tableAction['status'].eq(6)
                                                                                                  ]
                                                                                                 )
                    ]
            hasActionInDBrecord = self.db.getRecordEx(table, cols = cols, where = where)
            actionStatus = forceInt(hasActionInDBrecord.value('status')) if hasActionInDBrecord else None
            if actionStatus == 6 and not courseActionRecordList:
                continue
            if hasActionInDBrecord and questions:
                actionTypeId = quizInfo['idx']
                tableActionPropertyType = self._tblActionPropertyType
                actionPropertyTypes = self.db.getRecordList(tableActionPropertyType,
                                                            cols = [tableActionPropertyType['id'], tableActionPropertyType['typeName'], tableActionPropertyType['name']],
                                                            where = [tableActionPropertyType['actionType_id'].eq(actionTypeId)])
                self.db.transaction()
                try:
                    result = []
                    valueForNote = u''
                    for apt in actionPropertyTypes:
                        aptId = unicode(apt.value('id').toString())
                        aptType = unicode(apt.value('typeName').toString())
                        aptName = unicode(apt.value('name').toString())
                        if aptId in questions:
                            answerValue = answers[aptId]

                            recordAP = self._tblActionProperty.newRecord()
                            recordAP.setValue('deleted', 0)
                            recordAP.setValue('action_id', toVariant(actionId))
                            recordAP.setValue('type_id', toVariant(aptId))
                            apId = self.db.insertRecord(self._tblActionProperty, recordAP)

                            if aptType == 'String':
                                table = self._tblActionProperty_String
                                record = table.newRecord()
                                record.setValue('value', answerValue)
                            elif aptType == 'Integer':
                                table = self._tblActionProperty_Integer
                                record = table.newRecord()
                                try:
                                    answerNewValue = int(answerValue)
                                    record.setValue('value', answerNewValue)
                                    valueIsNull = False
                                except Exception, e:
                                    QtGui.qApp.logCurrentException()
                                    print('Error: %s' % anyToUnicode(e))
                                    valueIsNull = True
                                    valueForNote = valueForNote + ' ,  ' + answerValue if valueForNote else answerValue
                                    result.append({aptName:answerValue})
                                    continue
                            elif aptType == 'Double':
                                table = self._tblActionProperty_Double
                                record = table.newRecord()
                                try:
                                    answerNewValue = float(answerValue)
                                    record.setValue('value', answerNewValue)
                                    valueIsNull = False
                                except Exception, e:
                                    QtGui.qApp.logCurrentException()
                                    print('Error: %s' % anyToUnicode(e))
                                    valueIsNull = True
                                    valueForNote = valueForNote + ' ,  ' + answerValue if valueForNote else answerValue
                                    result.append({aptName:answerValue})
                                    continue
                            elif aptType == 'Date':
                                table = self._tblActionProperty_Date
                                record = table.newRecord()
                                record.setValue('value', answerValue)
                            elif aptType == 'Boolean':
                                table = self._tblActionProperty_Boolean
                                record = table.newRecord()
                                record.setValue('value', answerValue)
                            elif aptType == 'Time':
                                table = self._tblActionProperty_Time
                                record = table.newRecord()
                                record.setValue('value', answerValue)
                            elif aptType == 'Double':
                                table = self._tblActionProperty_Double
                                record = table.newRecord()
                                record.setValue('value', answerValue)
                            record.setValue('id', apId)
                            record.setValue('index', 0)
                            #record.setValue('value', answerValue)
                            self.db.insertRecord(table, record)
                            result.append({aptName:answerValue})
                            if courseActionRecordList:
                                self.checkNorm(apId, aptId, answerValue, actionId)
                    idA = self.markAction(actionId, 4, valueForNote) if valueIsNull else self.markAction(actionId, 2)
                    idN = self.markQuizNote(actionId, result, clientId, 2)
                    if courseActionRecordList:
                        self.handleCourseAction(actionId, courseActionRecordList)
                    self.db.commit()
                    if idA and idN:
                        uuids.append(quizInfo['uuid'])
                except Exception, e:
                    QtGui.qApp.logCurrentException()
                    print('Error: %s' % anyToUnicode(e))
                    self.db.rollback()
            elif hasActionInDBrecord:
                if courseActionRecordList:
                    self.db.transaction()
                    try:
                        self.handleCourseAction(actionId, courseActionRecordList)
                        self.db.commit()
                    except Exception, e:
                        QtGui.qApp.logCurrentException()
                        print('Error: %s' % anyToUnicode(e))
                        self.db.rollback()
        self.markRead(uuids)


    def markRead(self, uuids):
        u"""Отправляет запрос с информацией о полученных данных по групповым и индивидуальным опросам на портал onlineLPU"""
        if uuids:
            data = {}
            data['method'] = 'onlinelpu/sqa/mark.read'
            i = 0
            for uuid in uuids:
                data['params[uuid][' + unicode(i) + ']'] = uuid
                i = i + 1

            data['auth[version]'] = '1.0'
            data['auth[client_id]'] = self.preferences.currentInfisCodeEncrypted
            data['auth[client]'] = 'samson.mis'

            resp = requests.post("https://onlinelpu.ru/api", data=data)
            self.log(u'URL request statuses from onlineLPU: ', resp.url + 
                                                               u'\nResponse code: ' + unicode(resp.status_code) + 
                                                               u'\nResponse: ' + resp.content.decode('utf-8'), 
                                                               fileName='notificationTool.log')
            print(resp.url)
            print(resp.status_code)
            print(resp.content)


    def checkNorm(self, apId, aptId, value, actionId):
        u"""Проверяет, есть ли норма у пациента(индивидуальная) или у свойства типа действия(если нет индивидуальной). Записывает рассчитанную оценку"""
        result = None
        resultRecord = None
        clientNorm = None
        recordList = self.getNormData(apId, aptId, value)
        for record in recordList:
            resultRecord = record
            if forceRef(record.value('propertyTemplate_id')) == forceRef(record.value('clientTemplate_id')):
                #resultRecord = record
                clientNorm = forceString(resultRecord.value('clientNorm'))
                break
        if not resultRecord:
            self.log(u'Ошибка при получении данных по норме: ',
                u'Отсутствует указанный тип свойства id=%s у Action.id = %s' % (aptId, actionId), 
                fileName='notificationTool.log')
            print('No such ActionPropertyType.id=%s inside Action.id = %s' % (aptId, actionId))
            return None
        norm = clientNorm if clientNorm else forceString(resultRecord.value('propertyNorm'))
        if not norm:
            self.log(u'Ошибка при получении данных по норме: ',
                u'Отсутствует норма в типе свойства id=%s у Action.id = %s' % (aptId, actionId), 
                fileName='notificationTool.log')
            print('No such norm inside ActionPropertyType.id=%s, Action.id = %s' % (aptId, actionId))
            return None
        min, max = norm.split('-')
        try:
            value = float(value)
        except:
            self.log(u'Ошибка при получении данных по pзначению от onlineLPU: ',
                u'Невозможно привести значение к типу double id=%s у Action.id = %s' % (aptId, actionId), 
                fileName='notificationTool.log')
            print('Cannot convert value to double ActionPropertyType.id=%s inside Action.id = %s' % (aptId, actionId))
            return
        if float(min) <= float(value) <= float(max):
            result = 0
        elif float(value) < float(min):
            result = -1
        elif float(value) > float(max):
            result = 1
        if result is not None:
            table = self.db.table('ActionProperty')
            recordAP = self.db.getRecord(table, [table['id'], table['evaluation']], apId)
            recordAP.setValue('evaluation', result)
            self.db.updateRecord(table, recordAP)
        

    def getNormData(self, apId, aptId, value):
        u"""Возвращает информацию по нормам для данного типа свойства действия и для найденной по нему норме пациента"""
        tableActionPropertyType = self.db.table('ActionPropertyType')
        tableAction  = self.db.table('Action')
        tableActionProperty = self.db.table('ActionProperty')
        tableEvent = self.db.table('Event')
        tableClient = self.db.table('Client')
        tableClientNorm = self.db.table('Client_NormalParameters')
        table = tableActionProperty.innerJoin(tableAction, tableAction['id'].eq(tableActionProperty['action_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['id'].eq(tableActionProperty['type_id']))
        table = table.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        table = table.innerJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        table = table.leftJoin(tableClientNorm, self.db.joinAnd([tableClientNorm['client_id'].eq(tableClient['id']), 
                                                                 tableClientNorm['deleted'].eq(0)]
                                                               )
                               )
        cols = [tableActionPropertyType['norm'].alias('propertyNorm'), 
                tableActionProperty['evaluation'], 
                tableClientNorm['norm'].alias('clientNorm'), 
                tableActionPropertyType['template_id'].alias('propertyTemplate_id'), 
                tableClientNorm['template_id'].alias('clientTemplate_id'), 
               ]
        cond = [tableActionProperty['id'].eq(apId), 
                tableActionPropertyType['id'].eq(aptId), 
                tableActionPropertyType['deleted'].eq(0), 
                tableAction['deleted'].eq(0), 
                tableEvent['deleted'].eq(0), 
                tableClient['deleted'].eq(0)
               ]
        recordList = self.db.getRecordList(table, cols, cond)
        return recordList
    
    
    def getCourseActionInfo(self, actionId, clientId):
        u"""Получает информацию о курсовом назначении, если данное действие таковым является"""
        tableAction = self.db.table('Action')
        tableActionType = self.db.table('ActionType')
        tableActionExecutionPlan = self.db.table('ActionExecutionPlan')
        tableActionExecutionPlanItem = self.db.table('ActionExecutionPlan_Item')
        tableNotificationLog = self.db.table('Notification_Log')
        table = tableNotificationLog.innerJoin(tableAction, tableAction['id'].eq(tableNotificationLog['action_id']))
        table = table.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionExecutionPlanItem, tableActionExecutionPlanItem['action_id'].eq(tableAction['id']))
        table = table.innerJoin(tableActionExecutionPlan, tableActionExecutionPlan['id'].eq(tableActionExecutionPlanItem['master_id']))

        cols = [tableActionExecutionPlanItem['id'].alias('itemId'),
                tableActionExecutionPlan['id'].alias('planId'),
                tableActionType['id'].alias('actionTypeId'), 
                tableAction['event_id'].alias('eventId'), 
                tableAction['aliquoticity'].alias('actionAliquoticity')
               ]

        cond = [tableNotificationLog['recipient'].eq(clientId),
                tableNotificationLog['action_id'].eq(actionId),
                tableActionExecutionPlan['deleted'].eq(0), 
                tableAction['deleted'].eq(0), 
                tableActionType['deleted'].eq(0)
               ]
        return self.db.getRecordList(table, cols=cols, where=cond)


    def handleCourseAction(self, actionId, courseActionRecordList):
        u"""Выполняет необходимые действия по продолжению выполнения курсового назначения"""
        #if result:
        recordList = courseActionRecordList

        if len(recordList) > 1:
            print('Found more than 1 Notification for this CourseAction Action.id = %s' % actionId)
            self.log(u'Ошибка при получении данных от onlineLPU: ',
                u'Найдено больше одного оповещения по курсовому назначению Action.id = %s' % actionId, 
                fileName='notificationTool.log')
            return None

        for record in recordList:
            eventId = forceRef(record.value('eventId'))
            executionPlanId = forceRef(record.value('planId'))
            actionTypeId = forceRef(record.value('actionTypeId'))
            currentItemId = forceRef(record.value('itemId'))
            aliquoticity = forceInt(record.value('actionAliquoticity'))
            nextItemInfo = self.closeCurrentCourseItem(actionId, aliquoticity, executionPlanId)
            directionInfo = self.closeCurrentCourseAction(actionId)
            self.createNextCourse(currentItemId, actionTypeId, executionPlanId, eventId, aliquoticity, directionInfo, nextItemInfo)
            

    def closeCurrentCourseItem(self, actionId, aliquoticity, executionPlanId):
        u"""Закрывает текущий элемент плана курсового назначения. Возвращает порядковый номер, номер по кратности, дату и время выполнения"""
        tableItem = self.db.table('ActionExecutionPlan_Item')
        cond = [tableItem['action_id'].eq(actionId)]
        cols = [tableItem['executedDatetime'],
                tableItem['date'], 
                tableItem['time'],  
                tableItem['idx'], 
                tableItem['aliquoticityIdx'], 
                tableItem['id']
               ]
        record = self.db.getRecordEx(tableItem, cols, cond)
        nextIdx = forceInt(record.value('idx')) + 1
        currentAliquoticityIdx = forceInt(record.value('aliquoticityIdx'))
        dateIfNextDateIsNull = forceDate(record.value('date')).addDays(1)
        timeIfNextTimeIsNull = forceTime(record.value('time'))
        
        if nextIdx >= aliquoticity and aliquoticity > 1:
            cols = [tableItem['time'], 
                    tableItem['date'], 
                    tableItem['idx'], 
                    tableItem['aliquoticityIdx'], 
                    tableItem['id']
                   ]
            cond = [tableItem['master_id'].eq(executionPlanId), tableItem['idx'].eq(nextIdx - aliquoticity)]
            recordForTime = self.db.getRecordEx(tableItem, cols, cond)
            dateIfNextDateIsNull = forceDate(recordForTime.value('date')).addDays(1)
            timeIfNextTimeIsNull = forceTime(recordForTime.value('time'))
        if record:
            record.setValue('executedDatetime', toVariant(QDateTime.currentDateTime()))
            self.db.updateRecord(tableItem, record)
            return (nextIdx, currentAliquoticityIdx, dateIfNextDateIsNull, timeIfNextTimeIsNull)


    def closeCurrentCourseAction(self, actionId):
        u"""Закрывает текущее действие курсового назначения. Возвращает дату назначения, назначевшего врача"""
        tableAction = self.db.table('Action')
        cols = [tableAction['endDate'], 
                tableAction['directionDate'],
                tableAction['setPerson_id'],
                tableAction['person_id'],
                tableAction['status'], 
                tableAction['id']
               ]
        record = self.db.getRecord(tableAction, cols, actionId)
        setPersonId = forceRef(record.value('setPerson_id'))
        directionDate = forceDateTime(record.value('directionDate'))
        status = forceInt(record.value('status'))
        if record and status == 2:
            record.setValue('endDate', toVariant(QDateTime.currentDateTime()))
            record.setValue('person_id', toVariant(setPersonId))
            self.db.updateRecord(tableAction, record)
        return (setPersonId, directionDate)


    def createNextCourse(self, currentItemId, actionTypeId, executionPlanId, eventId, aliquoticity, directionInfo, nextItemInfo):
        u"""Создает следующее действие курсового назначения. Заполняет следующий элемент плана курсового назначения"""
        setPersonId, directionDate = directionInfo
        nextIdx, currentAliquoticityIdx, dateIfNextDateIsNull, timeIfNextTimeIsNull = nextItemInfo
        if not setPersonId:
            print('No setPerson_id in CourseAction inside eventId.id = %s' % eventId)
            self.log(u'Ошибка при создании следующего курсового назначния: ',
                u'Отсутствует назначивший врач в курсовом назначении eventId.id = %s' % eventId, 
                fileName='notificationTool.log')
            return None
        if not directionDate:
            print('No directionDate inside CourseAction eventId.id = %s' % eventId)
            self.log(u'Ошибка при создании следующего курсового назначния: ',
                u'Отсутствует дата назначения в курсовом назначении eventId.id = %s' % eventId, 
                fileName='notificationTool.log')
            return None
        if not nextIdx:
            print('No idx inside CourseActionItem eventId.id = %s' % eventId)
            self.log(u'Ошибка при создании следующего курсового назначния: ',
                u'Невозможно определить порядковый номер в курсовом назначении eventId.id = %s' % eventId, 
                fileName='notificationTool.log')
            return None
        if not dateIfNextDateIsNull:
            print('No date in previous CourseActionItem eventId.id = %s' % eventId)
            self.log(u'Ошибка при создании следующего курсового назначния: ',
                u'Отсутствует дата назначения в предыдущем курсовом назначении eventId.id = %s' % eventId, 
                fileName='notificationTool.log')
            return None
        if not timeIfNextTimeIsNull:
            print('No time in previous CourseActionItem eventId.id = %s' % eventId)
            self.log(u'Ошибка при создании следующего курсового назначния: ',
                u'Отсутствует время назначения в предыдущем курсовом назначении eventId.id = %s' % eventId, 
                fileName='notificationTool.log')
            return None
        tableItem = self.db.table('ActionExecutionPlan_Item')
        cond = [
                #tableItem['action_id'].eq(newActionId),
                tableItem['idx'].eq(nextIdx),
                tableItem['master_id'].eq(executionPlanId)
               ]
        cols = [tableItem['date'],
                tableItem['time'],
                tableItem['idx'], 
                tableItem['master_id'],
                tableItem['action_id'], 
                tableItem['id']
               ]
        recordItem = self.db.getRecordEx(tableItem, cols, cond)
        if not recordItem:
            print('Course has ended')
            self.log(u'Курсовое назначение закончено: ',
                u'В событии eventId.id = %s' % eventId, 
                fileName='notificationTool.log')
            return
        dateRecordValue = recordItem.value('date')
        date = forceDate(dateRecordValue).toString(Qt.ISODate)
        timeRecordValue = recordItem.value('time')
        timeValue = forceTime(timeRecordValue).toString(Qt.TextDate)
        if not date:
            date = dateIfNextDateIsNull.toString(Qt.ISODate)
        if not timeValue:
            timeValue = timeIfNextTimeIsNull.toString(Qt.TextDate)
        begDate = date + ' ' + timeValue

        tableAction = self.db.table('Action')
        newRecordAction = tableAction.newRecord()
        newRecordAction.setValue('actionType_id', actionTypeId)
        newRecordAction.setValue('begDate', toVariant(begDate))
        if forceDate(dateRecordValue).toString(Qt.ISODate):
            newRecordAction.setValue('plannedEndDate', toVariant(date))
        newRecordAction.setValue('directionDate', directionDate)
        newRecordAction.setValue('status', 5)
        newRecordAction.setValue('setPerson_id', setPersonId)
        newRecordAction.setValue('event_id', eventId)
        newRecordAction.setValue('idx', nextIdx)
        newRecordAction.setValue('aliquoticity', aliquoticity)
        newActionId = self.db.insertRecord(tableAction, newRecordAction)

        if recordItem and newActionId:
            recordItem.setValue('date', toVariant(date))
            recordItem.setValue('time', toVariant(timeValue))
            recordItem.setValue('idx', nextIdx)
            recordItem.setValue('master_id', executionPlanId)
            recordItem.setValue('action_id', toVariant(newActionId))
            return self.db.updateRecord(tableItem, recordItem)


    def processNotifications(self):
        self._tblNotificationRule = tbl(tblNotificationRule)
        self._tblNotificationLog = tbl(tblNotificationLog)
        self._tblRbNotificationKind = tbl(rbNotificationKind)
        self._tblSheduleItem = tbl('Schedule_Item')
        self._tblShedule = tbl('Schedule')
        self._tblSheduleItemExport = tbl('Schedule_Item_Export')
        self._tblEvent = tbl('Event')
        self._tblClient = tbl('Client')
        self._tblAction = tbl('Action')
        self._tblActionType = tbl('ActionType')
        self._tblActionProperty = tbl('ActionProperty')
        self._tblActionPropertyType = tbl('ActionPropertyType')
        self._tblActionExport = tbl('Action_Export')
        self._tblActionProperty_String = tbl('ActionProperty_String')
        self._tblActionProperty_Date = tbl('ActionProperty_Date')
        self._tblActionProperty_Boolean = tbl('ActionProperty_Boolean')
        self._tblActionProperty_Double = tbl('ActionProperty_Double')
        self._tblActionProperty_Integer = tbl('ActionProperty_Integer')
        self._tblActionProperty_Time = tbl('ActionProperty_Time')
        self.notificationManager = CNotificationManager()
        systemId = forceRef(self.db.translate(
            'rbExternalSystem', 'code', 'SamsonExtNotification', 'id'))
        if not systemId:
            raise Exception(u'Не указана внутренняя система оповещений в rbExternalSystem')
            
        self.__statistics['rulesFound'] = 0
        self.__statistics['logRecordsFound'] = 0
        self.__statistics['logRecordsProcessed'] = 0
        self.__statistics['iPPhoneNotifications'] = 0
        self.__statistics['iPPhoneResponses'] = 0

        # Для включения/отключения интеграции с onlineLPU создана настройка в notificationTool.ini
        if self.preferences.onlineLpuIsOn:
            self.processNotificationRulesQuiz(systemId)
            self.processNotificationRulesGroupQuiz(systemId)

        if not self.preferences.confirmInstantly:
            self.processSmsConfirmation()
        self.processNotificationRules(systemId)
        self.processNotificationLog(systemId)
        self.sendReseacrhNotificationsToEMK()
        self.importIPPhoneResponses()


    def processNotificationRules(self, systemId):
        table = tbl(tblNotificationRule)
        cond = [#table['class'].eq(CNotificationRule.ncExternal),
                table['deleted'].eq(0),
                #table['type'].ne(2),
                table['condition'].ne(3)]
        recordList = self.db.getRecordList(table, where=cond,
                                           order=table['condition'].name())

        self.__statistics['rulesFound'] += len(recordList)
        self.__statistics['schedulesItemsFound'] = 0
        self.__statistics['schedulesItemsProcessed'] = 0
        self.__statistics['schedulesItemsSkipped'] = 0

        for record in recordList:
            rule = CNotificationRule(record)
            self.processNotificationRule(rule, systemId)
            self.notificationManager.processNotificationConfirmation(rule)
        

    def processNotificationRule(self, rule, systemId):
        if rule.condition == CNotificationRule.ncdResearch and rule.ruleClass == CNotificationRule.ncExternal:
            currentDate = QDate.currentDate()
            days = self.preferences.daysForResearchConfirm
            period = 0-days if days else 0
            dateBefore = currentDate.addDays(period)
            dateBeforeString = dateBefore.toString(Qt.ISODate)
            tableAction = self.db.table('Action')
            tableEvent = self.db.table('Event')
            tableActionExport = self.db.table('Action_Export')
            table = tableAction.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
            table = table.leftJoin(tableActionExport, self.db.joinAnd([tableActionExport['master_id'].eq(tableAction['id']),
                                                                       tableActionExport['system_id'].eq(systemId)
                                                                      ]
                                                                     )
                                  )
            cond = [tableAction['actionType_id'].eq(rule.actionType_id),
                    tableActionExport['id'].isNull(),
                    tableAction['status'].eq(2), 
                    tableAction['deleted'].eq(0), 
                    tableAction['endDate'].dateGe(dateBeforeString)
                   ]
            cols = [tableAction['id'].alias('actionId'),
                    tableEvent['client_id'].alias('clientId'), 
                    tableAction['actionType_id'].alias('actionTypeId')
                   ]
            #order = 'Action.createDatetime DESC'
            #limit = 1
            recordList = self.db.getRecordList(table, cols, cond)
            clientIdList = []
            actionInfoList = []
            for record in recordList:
                clientId = forceRef(record.value('clientId'))
                clientIdList.append(clientId)
                actionInfoList.append([clientId, forceRef(record.value('actionId')), forceRef(record.value('actionTypeId'))])
            manager = CNotificationManager()
            noAddrClientList = manager.notifyClientWithResearchInfo(rule.id, actionInfoList, '')
            return noAddrClientList

        if rule.ruleClass == CNotificationRule.ncExternal and rule.condition != CNotificationRule.ncdResearch:
            currentDateTime = QDateTime.currentDateTime()
            date = currentDateTime.date()
            table = self._tblSheduleItem
            cond = [
                table['client_id'].isNotNull(),
            ]

            if rule.ignoreToday:
                cond.append(table['time'].ge(date.addDays(1)))
            else:
                cond.append(table['time'].gt(currentDateTime))

            table = table.leftJoin(
                self._tblSheduleItemExport,
                [self._tblSheduleItemExport['master_id'].eq(table['id']),
                 self.db.joinOr([
                     self._tblSheduleItemExport['system_id'].eq(systemId),
                     self._tblSheduleItemExport['system_id'].isNull()])
                ])
            table = table.leftJoin(self._tblShedule,
                                   [self._tblShedule['id'].eq(table['master_id']),
                                    self._tblShedule['appointmentType'].eq(
                                        rule.appointmentType)])

            table = table.leftJoin(
                self._tblNotificationLog,
                [self._tblNotificationLog['id'].eq(table['externalId']),
                 self.db.joinOr([
                     self._tblNotificationLog['rule_id'].eq(rule.id),
                     self._tblNotificationLog['rule_id'].isNull()])
                ])

            if rule.condition == CNotificationRule.ncdConfirmation:
                # recordDatetime < текущего времени не более чем на 30 минут
                lastHalfHour = currentDateTime.addSecs(30*60)
                cond.append(table['recordDatetime'].lt(lastHalfHour))
                cond.append(table['deleted'].eq(0))
            elif rule.condition == CNotificationRule.ncdNotification:
                cond.append(table['deleted'].eq(0))
                condPeriod = []

                if rule.multiplicity:
                    #recordDatetime попадает в период напоминания
                    periodList = zip(range(1, rule.multiplicity + 1),
                                     range(rule.multiplicity))

                    for (beg, end) in periodList:
                        begDateTime = 'ADDTIME(%s, \'%s:0:0\')' % (
                            table['time'], -beg*rule.term)
                        endDateTime = 'ADDTIME(%s, \'%s:0:0\')' % (
                            table['time'], -end*rule.term)
                        condPeriod.append('(NOW() BETWEEN %s AND %s)' % (
                            begDateTime, endDateTime))

                    if condPeriod:
                        cond.append(self.db.joinOr(condPeriod))

            elif rule.condition == CNotificationRule.ncdCancel:
                # recordDatetime < текущего времени не более чем на 60 минут
                # и deleted=1
                lastHour = currentDateTime.addSecs(60*60)
                cond.append(table['recordDatetime'].lt(lastHour))
                cond.append(table['deleted'].eq(1))

            cols = ('*, COUNT(%s) AS notificationCount' %
                    self._tblNotificationLog['id'])
            recordList = self.db.getRecordListGroupBy(
                table, cols, where=cond, group=self._tblSheduleItem['id'].name())
            self.__statistics['schedulesItemsFound'] += len(recordList)

            if not rule.condition != CNotificationRule.ncdNotification:
                cond.append(
                    self.db.joinOr([
                        self._tblSheduleItemExport['system_id'].ne(systemId),
                        self._tblSheduleItemExport['system_id'].isNull()
                    ]))

            for record in recordList:
                recordPersonId = forceRef(record.value('recordPerson_id'))

                if not recordPersonId:
                    recordPersonId = forceRef(record.value('modifyPerson_id'))

                if not recordPersonId:
                    recordPersonId = forceRef(record.value('createPerson_id'))

                notificationCount = forceInt(record.value('notificationCount'))
                # если число оповещений превышено,
                if ((rule.multiplicity and rule.multiplicity <= notificationCount)
                        or (not rule.multiplicity and notificationCount)):
                    self.report(u'Талон {id} число оповещений превышено'
                                .format(id=forceRef(record.value('id'))))
                    self.__statistics['schedulesItemsSkipped'] += 1
                    continue

                if rule.multiplicity > 1:
                    dateTime = forceDateTime(record.value('dateTime'))
                    time = forceDateTime(record.value('time'))

                    # если уже оповещали на текущем периоде
                    if self.isPeriodNotified(rule, notificationCount, dateTime,
                                             time):
                        self.report(u'Талон {id} уже оповещали в текущем периоде'
                                    .format(id=forceRef(record.value('id'))))
                        self.__statistics['schedulesItemsSkipped'] += 1
                        continue

                if self.userHasRightToNotify(recordPersonId):
                    self.processSheduleItem(record, rule, systemId)
                else:
                    self.report(u'Нет прав для отправки оповещения по талону `%d`'
                                u' у пользователя `%d`' %
                                (forceRef(record.value('id')),
                                 recordPersonId if recordPersonId else -1))



    def processSheduleItem(self, record, rule, systemId):
        self.report(u'Обработка правила %s' % rule.name)
        clientId = forceRef(record.value('client_id'))
        scheduleItemId = forceRef(record.value('id'))

        for (kindCode, kindId, contactTypeId) in rule.notificationKindList:
            addrList = self.notificationManager.getClientContact(
                clientId, contactTypeId)

            if addrList != []:
                text = parseNotificationTemplate(
                    rule.template, clientId, record)

                if not text:
                    msg = u'Ошибка обработки шаблона правила %s'  % rule.text
                    self.log(u'Ошибка', msg)
                    self.report(msg)
                    return

                for addr in addrList:
                    logId = (self.notificationManager.
                             createNotificationLogRecord(
                                 rule.id, kindId, text, addr, clientId))

                    if logId:
                        self.writeNotificationConfirmation(
                            logId, systemId, scheduleItemId)
                        self.__statistics['schedulesItemsProcessed'] += 1
            else:
                msg = (u'Ошибка: для пациента %d не задан контакт с кодом '
                       u'типа `%s`' % (clientId, kindCode))

                record = self._tblNotificationLog.newRecord()
                record.setValue('createPerson_id', toVariant(QtGui.qApp.userId))
                record.setValue('createDatetime',
                                toVariant(QDateTime.currentDateTime()))
                record.setValue('rule_id', toVariant(rule.id))
                record.setValue('kind_id', toVariant(kindId))
                record.setValue('recipient', toVariant(clientId))
                record.setValue('sendDatetime', toVariant(QDateTime.currentDateTime()))
                record.setValue('lastErrorText', toVariant(msg))
                QtGui.qApp.db.insertRecord(self._tblNotificationLog, record)
                self.log(u'Ошибка', msg)
                self.report(msg)


    def processSmsConfirmation(self):
        smsConfig = self.getSmsConfig()
        token = smsConfig['token']
        headers = { 'Content-type': 'application/json',
                    'Authorization': 'Token %s' % token
                  }
        postData = {}
        url = self.preferences.smsStatusUrl
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
                raise
        request = response.request
        reqBody = request.body
        reqHeaders = ''
        for k, v in request.headers.items():
            reqHeaders = reqHeaders + '%s: %s' % (k, v) + '\n'
        reqUrl = request.url
        reqMethod = request.method

        respHeaders = ''
        for k, v in response.headers.items():
            respHeaders = respHeaders + '%s: %s' % (k, v) + '\n'
        statusCode = response.status_code
        content = response.content
        contentSerialized = json.loads(content)
        self.log(u'Request Sms Status: \n', 'url: '+reqUrl+'\n'+'method: '+reqMethod+'\n'+'headers'+reqHeaders+'\n'+'body: '+reqBody+'\n', fileName='notificationTool.log')
        self.log(u'Response Sms Status: \n', 'StatusCode: '+unicode(statusCode)+'\n'+'headers'+respHeaders+'\n'+'body: '+content+'\n', fileName='notificationTool.log')

        if contentSerialized['data']:
            for notification in contentSerialized['data']:
                table = self._tblNotificationLog
                tableExport = self.db.table('Notification_Log_Export')
                table = table.leftJoin(tableExport, tableExport['master_id'].eq(table['id']))
                cond = [self._tblNotificationLog['lastErrorText'].eq(''),
                        self._tblNotificationLog['status'].eq('9'),
                        tableExport['externalId'].eq(notification['id'])
                       ]
                cols = [self._tblNotificationLog['id'],
                        self._tblNotificationLog['status'],
                        self._tblNotificationLog['confirmationDatetime'],
                        self._tblNotificationLog['lastErrorText']
                       ]

                record = self.db.getRecordEx(table, cols, where=cond)
                if notification['status'] == 'delivered' and record:
                    record.setValue('status', toVariant(11))
                    unixDatetime = notification['updated']
                    #datetimeConfirm = datetime.utcfromtimestamp(unixDatetime).strftime('%Y-%m-%d %H:%M:%S')
                    datetimeConfirm = datetime.fromtimestamp(unixDatetime).strftime('%Y-%m-%d %H:%M:%S')
                    record.setValue('confirmationDatetime', toVariant(datetimeConfirm))
                    self.db.updateRecord(self._tblNotificationLog, record)
                elif notification['status'] == 'error' and record:
                    record.setValue('status', toVariant(10))
                    record.setValue('lastErrorText', toVariant(notification['status']))
                    self.db.updateRecord(self._tblNotificationLog, record)
                else:
                    if record:
                        record.setValue('status', toVariant(10))
                        record.setValue('lastErrorText', toVariant(u'Неизвестный статус: '+notification['status']))
                        self.db.updateRecord(self._tblNotificationLog, record)


    def processNotificationLog(self, systemId):
        table = self._tblNotificationLog
        cond = [
            self._tblNotificationLog['lastErrorText'].eq(''),
            self._tblNotificationLog['status'].eq('0')
        ]

        table = table.leftJoin(
            self._tblNotificationRule,
            self._tblNotificationRule['id'].eq(
                self._tblNotificationLog['rule_id']))
        table = table.leftJoin(
            self._tblRbNotificationKind,
            self._tblRbNotificationKind['id'].eq(
                self._tblNotificationLog['kind_id']))

        recordList = self.db.getRecordList(
            table, where=cond, order=self._tblNotificationLog['rule_id'].name())
        self.__statistics['logRecordsFound'] += len(recordList)
        # self.__statistics['logRecordsProcessed'] = 0

        baseIPPhonePath = self.preferences.iPPhoneDataBasePath
        now = datetime.now()
        nowString = now.strftime("%Y-%m-%dT%H:%M")
        path = baseIPPhonePath + 'OUT/' + nowString + '.out'
        for record in recordList:
            logId = forceRef(record.value('id'))
            text = forceString(record.value('text'))
            addr = forceString(record.value('addr'))
            kindCode = forceString(record.value('code'))
            recipientId = forceRef(record.value('recipient'))
            smsConfig = self.getSmsConfig()
            actionId = forceRef(record.value('action_id'))
            isAttached = forceInt(record.value('attachedFileAttr'))
            attach = self.getFileAttach(actionId, isAttached)
            if isAttached and not attach:
                self.report(u'Ошибка отправки оповещения {id}: {errorStr}'.format(id=logId, errorStr='Нет файла для прикрепления'))
                continue
            (result, errorStr) = self.notificationManager.sendNotification(
                kindCode, text, addr, logId, recipientId, path, smsConfig, attach)
            self.notificationManager.logNotification(logId, result, errorStr)

            if result:
                if self.preferences.confirmInstantly:
                    self.notificationManager.confirmNotification(logId, result, errorStr)
                else:
                    if kindCode != '1': # код смс оповещения = 1
                        self.notificationManager.confirmNotification(logId, result, errorStr)
                if self.notificationManager._IPPhoneNotificationQuantity != 0:
                    self.__statistics['iPPhoneNotifications'] = self.notificationManager._IPPhoneNotificationQuantity
                self.__statistics['logRecordsProcessed'] += 1
            else:
                self.report(u'Ошибка отправки оповещения {id}: {errorStr}'
                            .format(id=logId, errorStr=errorStr))
        # Cоздать сигнальный файл с расширением .ok для IP телефонии
        if os.path.exists(path):
            okFilePath = path[:-4] + '.ok'
            with open(okFilePath, 'wb') as f:
                f.close()


    def getFileAttach(self, actionId, isAttached):
        if not actionId or not isAttached:
            return None
        try:
            tableAction = self.db.table('Action')
            tableActionFileAttach = self.db.table('Action_FileAttach')
            table = tableAction.innerJoin(tableActionFileAttach, tableActionFileAttach['master_id'].eq(tableAction['id']))
            cols = [tableActionFileAttach['path'].alias('fileAttachedPath'),
                    tableActionFileAttach['id'].alias('fileAttachId')
                   ]
            cond = [tableAction['id'].eq(actionId),
                    tableAction['deleted'].eq(0),
                    tableActionFileAttach['deleted'].eq(0),
                    tableActionFileAttach['respSignatureBytes'].isNotNull(),
                    tableActionFileAttach['respSigner_id'].isNotNull(),
                    tableActionFileAttach['orgSignatureBytes'].isNotNull(),
                    tableActionFileAttach['orgSigner_id'].isNotNull()
                   ]
            record = self.db.getRecordEx(table=table, cols=cols, where=cond, order='Action_FileAttach.id DESC')
            if record:
                filePath = forceString(record.value('fileAttachedPath'))
                fileName = os.path.basename(filePath)
                basePath = self.getWebDavUrl()
                baseUrl = basePath.replace('${dbServerName}', self.preferences.dbServerName)
                webDav = CWebDAVClient(baseUrl)
                stream = io.BytesIO()
                webDav.downloadStream(filePath, stream)
                return (stream, fileName)
        except Exception, e:
            QtGui.qApp.logCurrentException()
            print('Error: %s' % anyToUnicode(e))
            return None


    def getWebDavUrl(self):
        table = self.db.table('GlobalPreferences')
        cols = [table['value']]
        cond = [table['code'].eq('WebDav')]
        record = self.db.getRecordEx(table, cols, cond)
        return forceString(record.value('value'))


    def getSmsConfig(self):
        return {
                'url':    self.preferences.smsUrl,
                'token':  self.preferences.smsToken,
                'sender': self.preferences.smsSender,
                'ttl':    self.preferences.smsttl,
                'report': self.preferences.smsReport
               }


    def sendReseacrhNotificationsToEMK(self):
        recordList = self.findResearchNotifications()
        for record in recordList:
            self.db.transaction()
            try:
                notificationId = forceRef(record.value('notification_id'))
                actionTypeIdFromRule = forceRef(record.value('actionTypeIdFromRule'))
                eventId = forceRef(record.value('event_id'))
                personId = forceRef(record.value('setPerson_id'))
                directionDate = forceDate(record.value('directionDate'))
                obsDescr = forceString(record.value('obsDescr'))
                confirmationDatetime = forceDateTime(record.value('confirmationDateTime'))
                receivingActionTypeId = forceRef(record.value('receivingActionType_id'))
                recipient = forceRef(record.value('recipient'))

                tableAction = self.db.table('Action')
                tableEvent = self.db.table('Event')
                tableActionType = self.db.table('ActionType')
                tableActionPropertyForDate = self.db.table('ActionProperty').alias('APDate')
                tableActionPropertyForTime = self.db.table('ActionProperty').alias('APTime')
                tableActionPropertyTypeForDate = self.db.table('ActionPropertyType').alias('APTDate')
                tableActionPropertyTypeForTime = self.db.table('ActionPropertyType').alias('APTTime')
                tableActionPropertyDate = self.db.table('ActionProperty_Date')
                tableActionPropertyTime = self.db.table('ActionProperty_Time')

                table = tableAction.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
                table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
                table = table.leftJoin(tableActionPropertyTypeForDate,
                                    self.db.joinAnd([tableActionPropertyTypeForDate['actionType_id'].eq(tableActionType['id']),
                                                        tableActionPropertyTypeForDate['typeName'].eq('Date')
                                                    ]
                                                    )
                                      )
                table = table.leftJoin(tableActionPropertyTypeForTime,
                                    self.db.joinAnd([tableActionPropertyTypeForTime['actionType_id'].eq(tableActionType['id']),
                                                        tableActionPropertyTypeForTime['typeName'].eq('Time')
                                                    ]
                                                    )
                                      )
                table = table.leftJoin(tableActionPropertyForDate, 
                                    self.db.joinAnd([tableActionPropertyForDate['action_id'].eq(tableAction['id']),
                                                        tableActionPropertyForDate['type_id'].eq(tableActionPropertyTypeForDate['id'])
                                                    ]
                                                    )
                                      )
                table = table.leftJoin(tableActionPropertyForTime, 
                                    self.db.joinAnd([tableActionPropertyForTime['action_id'].eq(tableAction['id']),
                                                        tableActionPropertyForTime['type_id'].eq(tableActionPropertyTypeForTime['id'])
                                                    ]
                                                    )
                                      )
                table = table.leftJoin(tableActionPropertyDate, tableActionPropertyDate['id'].eq(tableActionPropertyForDate['id']))
                table = table.leftJoin(tableActionPropertyTime, tableActionPropertyTime['id'].eq(tableActionPropertyForTime['id']))

                cols = [#tableActionProperty['id'].alias('actionPropertyId'),
                        #tableActionPropertyDate['value'],
                        tableAction['id'].alias('receivingActionId'),
                        tableActionPropertyTypeForDate['id'].alias('APTdateId'),
                        tableActionPropertyTypeForTime['id'].alias('APTtimeId')
                       ]
                cond = [tableAction['event_id'].eq(eventId),
                        tableAction['deleted'].eq(0), 
                        tableEvent['client_id'].eq(recipient), 
                        self.db.joinAnd([tableActionPropertyTypeForDate['descr'].eq(obsDescr),
                                         tableActionPropertyTypeForTime['descr'].eq(obsDescr)
                                        ]
                                       ),
                        tableActionPropertyTime['value'].isNull(), 
                        tableActionPropertyDate['value'].isNull(), 
                        tableActionType['id'].eq(actionTypeIdFromRule)
                        #tableAction['person_id'].eq(personId), 
                        #tableAction['endDate'].dateEq(directionDate), 
                        #tableActionType['id'].ne(actionTypeIdFromRule)
                       ]

                actionRecordList = self.db.getRecordList(table, cols, cond, order='Action.id ASC', limit=1)
                actionRecord = actionRecordList[0] if actionRecordList else None
                if not actionRecord:
                    if receivingActionTypeId:
                        cond = cond[:-1]
                        cond.append(tableActionType['id'].eq(receivingActionTypeId))
                        actionRecordList = self.db.getRecordList(table, cols, cond, order='Action.id ASC', limit=1)
                        actionRecord = actionRecordList[0] if actionRecordList else None
                    else:
                        cond = cond[:-1]
                        cond.append(tableAction['person_id'].eq(personId))
                        cond.append(tableAction['endDate'].dateEq(directionDate))
                        actionRecordList = self.db.getRecordList(table, cols, cond, order='Action.id ASC', limit=1)
                        actionRecord = actionRecordList[0] if actionRecordList else None
                            
                if not actionRecord:
                    raise Exception(u'Не найдено действие для записи данных по оповещению id=%d' % notificationId)

                tableActionProperty = self.db.table('ActionProperty')
                newRecordAPDate = tableActionProperty.newRecord()
                newRecordAPDate.setValue('action_id', forceRef(actionRecord.value('receivingActionId')))
                newRecordAPDate.setValue('type_id', forceRef(actionRecord.value('APTdateId')))
                apDateId = self.db.insertOrUpdate(tableActionProperty, newRecordAPDate)

                newRecordAPDdate = tableActionPropertyDate.newRecord()
                newRecordAPDdate.setValue('id', apDateId)
                newRecordAPDdate.setValue('value', toVariant(confirmationDatetime.date()))
                self.db.insertRecord(tableActionPropertyDate, newRecordAPDdate)

                newRecordAPTime = tableActionProperty.newRecord()
                newRecordAPTime.setValue('action_id', forceRef(actionRecord.value('receivingActionId')))
                newRecordAPTime.setValue('type_id', forceRef(actionRecord.value('APTtimeId')))
                apTimeId = self.db.insertOrUpdate(tableActionProperty, newRecordAPTime)

                newRecordAPTtime = tableActionPropertyTime.newRecord()
                newRecordAPTtime.setValue('id', apTimeId)
                newRecordAPTtime.setValue('value', toVariant(confirmationDatetime.time()))
                self.db.insertRecord(tableActionPropertyTime, newRecordAPTtime)

                self.markNote(notificationId, 12)

                eventRecord = self.db.getRecord(tableEvent, ['modifyDatetime', 'id'], eventId)
                eventRecord.setValue('modifyDatetime', toVariant(QDateTime.currentDateTime()))
                self.db.updateRecord(tableEvent, eventRecord)
                self.db.commit()
            except Exception, e:
                self.db.rollback()
                QtGui.qApp.logCurrentException()
                print('Error: %s' % anyToUnicode(e))
                #raise


    def findResearchNotifications(self):
        table = self._tblNotificationLog
        tableAction = self.db.table('Action')
        tableEvent = self.db.table('Event')
        cond = [self._tblNotificationLog['confirmationDatetime'].isNotNull(),
                self._tblNotificationLog['confirmationDatetime'].ne(0),
                self._tblNotificationLog['status'].eq(11),
                self._tblNotificationRule['isTransmittable'].eq(1),
                #self._tblNotificationRule['receivingActionType_id'].isNotNull(),
                #self._tblNotificationRule['receivingActionType_id'].ne(0),
                self._tblNotificationRule['actionType_id'].ne(0),
                self._tblNotificationRule['actionType_id'].isNotNull(),
                self._tblNotificationRule['obsDescr'].ne(0),
                self._tblNotificationRule['obsDescr'].ne(''), 
                self._tblNotificationRule['obsDescr'].isNotNull()
               ]

        table = table.leftJoin(self._tblNotificationRule, 
                               self._tblNotificationRule['id'].eq(self._tblNotificationLog['rule_id'])
                              )
        table = table.leftJoin(self._tblRbNotificationKind,
                               self._tblRbNotificationKind['id'].eq(self._tblNotificationLog['kind_id'])
                              )
        table = table.leftJoin(tableAction,
                               tableAction['id'].eq(self._tblNotificationLog['action_id'])
                              )
        table = table.leftJoin(tableEvent,
                               tableEvent['id'].eq(tableAction['event_id'])
                              )
        cols = [tableAction['event_id'],
                tableAction['setPerson_id'], 
                tableAction['directionDate'], 
                self._tblNotificationLog['id'].alias('notification_id'),
                self._tblNotificationLog['action_id'],
                self._tblNotificationLog['recipient'],
                self._tblNotificationLog['confirmationDatetime'],
                self._tblNotificationRule['receivingActionType_id'],
                self._tblNotificationRule['actionType_id'].alias('actionTypeIdFromRule'),
                self._tblNotificationRule['obsDescr']
               ]

        recordList = self.db.getRecordList(table, cols=cols, where=cond, order=self._tblNotificationLog['rule_id'].name())
        return recordList


    def importIPPhoneResponses(self):
        baseIPPhonePath = self.preferences.iPPhoneDataBasePath + 'IN'
        files = os.listdir(baseIPPhonePath)
        dataFiles = []
        filesToDel = []
        for f in files:
            if f[-3:] == '.ok' and os.path.exists(baseIPPhonePath + '/' + f[:-3] + '.in'):
                fData = f[:-3] + '.in'
                dataFiles.append(fData)
                filesToDel.append(f)
                filesToDel.append(fData)
        for fd in dataFiles:
            self.notificationManager.readDataAndUpdateIPPhoneNotification(fd, baseIPPhonePath)
        for fdel in filesToDel:
            os.remove(baseIPPhonePath + '/' + fdel)
        if self.notificationManager._IPPhoneResponsesQuantity != 0:
            self.__statistics['iPPhoneResponses'] = self.notificationManager._IPPhoneResponsesQuantity


    def writeNotificationConfirmation(self, logId, systemId, scheduleItemId):
        record = self._tblSheduleItemExport.newRecord()
        record.setValue('master_id', toVariant(scheduleItemId))
        record.setValue('system_id', toVariant(systemId))
        record.setValue('externalId', toVariant(logId))
        record.setValue('dateTime', toVariant(QDateTime.currentDateTime()))
        return self.db.insertRecord(self._tblSheduleItemExport, record)


    def writeActionConfirmation(self, logId, systemId, actionId):
        record = self._tblActionExport.newRecord()
        record.setValue('master_id', toVariant(actionId))
        record.setValue('system_id', toVariant(systemId))
        record.setValue('externalId', toVariant(logId))
        record.setValue('dateTime', toVariant(QDateTime.currentDateTime()))
        return self.db.insertRecord(self._tblActionExport, record)


    def report(self, message, force=False):
        u"""Выводит сообщения в консоль"""

        if self.__verbose or force:
            print u'%s' % message


    def showStat(self):
        u"""Пишет статистику в журнал и в консоль"""
        stats = self.__statistics
        stats['logRecordsFailed'] = (stats['logRecordsFound'] -
                                     stats['logRecordsProcessed'])
        stats['scheduleItemsFailed'] = (stats['schedulesItemsFound'] -
                                        stats['schedulesItemsProcessed'] -
                                        stats['schedulesItemsSkipped'])

        msg = (u'Rules found {rulesFound},\n'
               u'Shedules items found {schedulesItemsFound},'
               u' processed {schedulesItemsProcessed}, '
               u' skipped {schedulesItemsSkipped}, '
               u' failed {scheduleItemsFailed}\n'
               u'iPPhoneNotifications sent {iPPhoneNotifications}, '
               u'iPPhoneNotifications read {iPPhoneResponses}\n'
            #    u'groupQuizesRules found {groupQuizesRules}, '
            #    u'groupQuizes found {groupQuizesFound}, '
            #    u'groupQuizes sent {groupQuizesSent}, '
            #    u'groupQuizes ignored {groupQuizesIgnored}\n'
            #    u'quizesRules found {quizesRules}, '
            #    u'quizes found {quizesFound}, '
            #    u'quizes sent {quizesSent}, '
            #    u'quizes ignored {quizesIgnored}\n'
               u'Log records found {logRecordsFound}, '
               u'processed {logRecordsProcessed}, '
               u'failed {logRecordsFailed}\n' .format(**stats))
        self.log(u'Statistics report', msg, fileName='notificationTool.log')
        self.report(msg)


    # !!! Затычка, чтобы можно было создавать экземпляр действия при формировании оповещения по шаблону через CActionInfo и compileAndExecTemplate.
    # !!! По правильному надо отнаследоваться от BaseApplication Class
    def userHasRight(self, right):
        return True

    def userHasRightToNotify(self, userId):
        result = self.__userRightCache.get(userId, -1)

        if result == -1:
            userInfo = CUserInfo(userId)
            result = userInfo.hasRight(urSendExternalNotifications)
            self.__userRightCache[userId] = result

        return result


    def isPeriodNotified(self, rule, periodNumber, notificationTime,
                         scheduleTime):
        result = False
        periodList = zip(range(1, rule.multiplicity + 1),
                         range(rule.multiplicity))

        if len(periodList) > periodNumber:
            (beg, end) = periodList[periodNumber]
            begTime = scheduleTime.addSecs(-beg*rule.term*60*60)
            endTime = scheduleTime.addSecs(-end*rule.term*60*60)
            result = ((begTime <= notificationTime) and
                      (endTime >= notificationTime))

        return result


# #############################################################

if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]')
    parser.add_option('--version',
                      dest='version',
                      help='print version and exit',
                      action='store_true',
                      default=False)
    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False,
                      help='verbose output')
    parser.add_option('-D', '--debug',
                      dest='debug',
                      help='print urllib debug output',
                      action='store_true',
                      default=False)
    (options, args) = parser.parse_args()

    if options.version:
        print u'{name} rev. {rev}, build {date}'.format(
            name=(sys.argv[0] if sys.argv else ''),
            rev=gLastChangedRev,
            date=gLastChangedDate)
    else:
        app = CMyApp(sys.argv, options.verbose, options.debug)
        QtGui.qApp = app

        try:
            app.openDatabase()
            app.processNotifications()
            app.showStat()
            app.preferences.save()
            app.closeDatabase()
            app.doneTrace()

        except Exception, e:
            if app.traceActive:
                app.logCurrentException()
                print 'Error top level: %s' % anyToUnicode(e)
                sys.exit(1)

        QtGui.qApp = None
