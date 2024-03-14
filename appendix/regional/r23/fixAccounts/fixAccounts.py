#!/usr/bin/env python
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

import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot

from library import database
from library.Calendar import CCalendarInfo
from library.Preferences import CPreferences
from library.Utils import *

from Events.ActionStatus import CActionStatus
from preferences.connection import CConnectionDialog
from Users.Login import CLoginDialog
from Users.UserInfo import CUserInfo

from Ui_fixAccounts import Ui_MainWindow
from consts import CMainSelect, CEventSelect


class CMyApp(QtGui.QApplication):

    def __init__(self, args):
        QtGui.QApplication.__init__(self, args)
        self.connect(self, SIGNAL('lastWindowClosed()'), self.close)
        self.preferences = CPreferences('r23FixAccounts.ini')
        self.preferences.load()
        self.calendarInfo = CCalendarInfo(self)
        self.db = None
        self.userId = None
        self.isInTransaction = None

    def close(self):
        self.preferences.save()
        self.closeDatabase()

    def openDatabase(self):
        self.db = None
        self.db = database.connectDataBase(self.preferences.dbDriverName,
                                           self.preferences.dbServerName,
                                           self.preferences.dbServerPort,
                                           self.preferences.dbDatabaseName,
                                           self.preferences.dbUserName,
                                           self.preferences.dbPassword)
        self.calendarInfo.load()


    def closeDatabase(self):
        if self.db:
            if self.isInTransaction:
                self.isInTransaction = False
                self.db.rollback()
            self.db.close()
            self.db = None
            self.userId = None
            self.calendarInfo.clear()


    def highlightRedDate(self):
        pass

    def highlightInvalidDate(self):
        pass


class CMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.windowTitleOrigin = self.windowTitle()
        self.edtBeginDate.setFixedWidth(self.edtBeginDate.maximumWidth())
        self.edtEndDate.setFixedWidth(self.edtEndDate.maximumWidth())
        self.lwAccounts.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.btnRefresh.setEnabled(False)
        self.btnProcess.setEnabled(False)
        self.btnCancel.setEnabled(False)

    def closeEvent(self, event):
        if QtGui.qApp.isInTransaction:
            reply = QtGui.QMessageBox.question(self, u'Предупреждение',
                                               u'Вы действительно хотите выйти без сохранения?',
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    @pyqtSlot()
    def on_actLogin_triggered(self):
        try:
            QtGui.qApp.openDatabase()
            dlgLogin = CLoginDialog(self)
            dlgLogin.setLoginName(QtGui.qApp.preferences.appUserName)
            if dlgLogin.exec_():
                QtGui.qApp.preferences.appUserName = dlgLogin.loginName()
                QtGui.qApp.userId = dlgLogin.userId()
                userInfo = CUserInfo(dlgLogin.userId())
                self.setWindowTitle(u'%s: %s (%s)' % (self.windowTitleOrigin, userInfo.name(), userInfo.login()))
                self.btnRefresh.setEnabled(True)
                return
        except database.CDatabaseException, e:
            QtGui.QMessageBox.critical(
                self,
                u'Ошибка открытия базы данных',
                unicode(e),
                QtGui.QMessageBox.Close)
        except Exception, e:
            QtGui.QMessageBox.critical(
                self,
                u'Ошибка открытия базы данных',
                u'Невозможно установить соедиенение с базой данных\n' + unicode(e),
                QtGui.QMessageBox.Close)
        mainWindow.actLogout.activate(QtGui.QAction.Trigger)

    @pyqtSlot()
    def on_actLogout_triggered(self):
        self.setWindowTitle(self.windowTitleOrigin)
        self.btnRefresh.setEnabled(False)
        self.btnProcess.setEnabled(False)
        self.btnCancel.setEnabled(False)
        QtGui.qApp.closeDatabase()

    @pyqtSlot()
    def on_actConnection_triggered(self):
        preferences = QtGui.qApp.preferences
        dlgConnection = CConnectionDialog(self)
        dlgConnection.setDriverName(preferences.dbDriverName)
        dlgConnection.setServerName(preferences.dbServerName)
        dlgConnection.setServerPort(preferences.dbServerPort)
        dlgConnection.setDatabaseName(preferences.dbDatabaseName)
        dlgConnection.setUserName(preferences.dbUserName)
        dlgConnection.setPassword(preferences.dbPassword)
        if dlgConnection.exec_():
            preferences.dbDriverName = dlgConnection.driverName()
            preferences.dbServerName = dlgConnection.serverName()
            preferences.dbServerPort = dlgConnection.serverPort()
            preferences.dbDatabaseName = dlgConnection.databaseName()
            preferences.dbUserName = dlgConnection.userName()
            preferences.dbPassword = dlgConnection.password()
            preferences.save()

    @pyqtSlot()
    def on_lwAccounts_itemSelectionChanged(self):
        self.btnProcess.setEnabled(bool(self.lwAccounts.selectedIndexes()))

    @pyqtSlot()
    def on_btnRefresh_clicked(self):
        tableAccount = QtGui.qApp.db.table('Account')
        records = QtGui.qApp.db.getRecordList(tableAccount,
                                              'settleDate, number',
                                              [tableAccount['deleted'].eq(0),
                                               tableAccount['settleDate'].between(
                                                self.edtBeginDate.date(),
                                                self.edtEndDate.date())],
                                              'settleDate, number')
        self.lwAccounts.clear()
        self.lwAccounts.addItems(['%s - %s' % (forceString(record.value(0)), forceString(record.value(1)))
                                  for record in records])

    @pyqtSlot()
    def on_btnProcess_clicked(self):

        #   Применить
        if QtGui.qApp.isInTransaction:
            QtGui.qApp.isInTransaction = False
            try:
                QtGui.qApp.db.commit()
            except Exception, e:
                QtGui.QMessageBox.critical(
                    self,
                    u'Ошибка сохранения данных',
                    u'Не удалось сохранить данные\n%s' % unicode(e),
                    QtGui.QMessageBox.Close)
                QtGui.qApp.db.rollback()
            self.btnProcess.setText(u'Обработать')
            self.actConnection.setEnabled(True)
            self.actLogin.setEnabled(True)
            self.actLogout.setEnabled(True)
            self.btnRefresh.setEnabled(True)
            self.lwAccounts.setEnabled(True)
            self.btnProcess.setEnabled(True)
            self.btnCancel.setEnabled(False)
            return

        #   Обработать
        def processClientServices():
            log.outputAccountInfo(accountNumber, clientId, servicesWithInsert, servicesWithUpdate)
            tableEvent = QtGui.qApp.db.table('Event')
            tableAction = QtGui.qApp.db.table('Action')
            tableActionType = QtGui.qApp.db.table('ActionType')
            #   Обходим словарь услуг для вставки
            for eventId, services in servicesWithInsert.items():
                event = QtGui.qApp.db.getRecord(tableEvent, 'createDatetime,'
                                                            'createPerson_id,'
                                                            'setDate,'
                                                            'execDate,'
                                                            'execPerson_id', eventId)
                QtGui.qApp.processEvents()
                if not QtGui.qApp.isInTransaction:
                    return False
                for service in services:
                    actionType = QtGui.qApp.db.getRecordEx(tableActionType, 'id', tableActionType['code'].eq(service[0]))
                    action = tableAction.newRecord()
                    action.setValue('createDatetime', event.value(CEventSelect.createDatetime))
                    action.setValue('createPerson_id', event.value(CEventSelect.createPerson_id))
                    action.setValue('modifyDatetime', toVariant(QDateTime.currentDateTime()))
                    action.setValue('modifyPerson_id', toVariant(QtGui.qApp.userId))
                    action.setValue('actionType_id', actionType.value(0))
                    action.setValue('event_id', toVariant(eventId))
                    action.setValue('directionDate', event.value(CEventSelect.setDate))
                    action.setValue('status', toVariant(CActionStatus.finished))
                    action.setValue('setPerson_id', event.value(CEventSelect.execPerson_id))
                    action.setValue('begDate', event.value(CEventSelect.setDate))
                    action.setValue('plannedEndDate', event.value(CEventSelect.execDate))
                    action.setValue('endDate', event.value(CEventSelect.execDate))
                    action.setValue('note', toVariant(''))
                    action.setValue('person_id', event.value(CEventSelect.execPerson_id))
                    action.setValue('office', toVariant(''))
                    action.setValue('amount', toVariant(service[1]))
                    action.setValue('account', toVariant(0))
                    action.setValue('MKB', toVariant(''))
                    action.setValue('morphologyMKB', toVariant(''))
                    action.setValue('finance_id', toVariant(2)) # 2-ОМС
                    actionId = QtGui.qApp.db.insertRecord(tableAction, action)
                    log.outputInsertServiceInfo(eventId, actionId, service[0])
            #   Обходим словарь услуг для обновления
            for eventId, services in servicesWithUpdate.items():
                QtGui.qApp.processEvents()
                if not QtGui.qApp.isInTransaction:
                    return False
                for service in services:
                    actionType = QtGui.qApp.db.getRecordEx(tableActionType, 'id', tableActionType['code'].eq(service[0]))
                    action = QtGui.qApp.db.getRecordEx(tableAction, 'id, amount',
                                                       [tableAction['event_id'].eq(eventId),
                                                        tableAction['actionType_id'].eq(forceRef(actionType.value(0)))])
                    action.setValue('amount', toVariant(service[1]))
                    actionId = QtGui.qApp.db.updateRecord(tableAction, action)
                    log.outputUpdateServiceInfo(eventId, actionId, service[0])
            return True

        self.actConnection.setEnabled(False)
        self.actLogin.setEnabled(False)
        self.actLogout.setEnabled(False)
        self.btnRefresh.setEnabled(False)
        self.lwAccounts.setEnabled(False)
        self.btnProcess.setEnabled(False)
        self.btnCancel.setEnabled(True)
        log = CLog(self.tbLog)
        try:
            QtGui.qApp.db.transaction()
            QtGui.qApp.isInTransaction = True
            accounts = []
            #   Обходим выделенные элементы в listWidget
            for index in sorted(self.lwAccounts.selectedIndexes(), key = lambda key: key.row()):
                if not QtGui.qApp.isInTransaction:
                    break
                accountNumber = forceString(index.data())
                accountNumber = accountNumber[accountNumber.find(' - ') + 3:]
                services = QtGui.qApp.db.query(CMainSelect.value % accountNumber)
                if services.first():
                    accounts += [accountNumber]
                    clientId = forceRef(services.value(CMainSelect.clientId))
                    servicesWithInsert = {}
                    servicesWithUpdate = {}
                    #   Формируем словари услуг для вставки и обновления
                    while True:
                        isUpdate = forceInt(services.value(CMainSelect.isUpdate))
                        eventId = forceRef(services.value(CMainSelect.eventId))
                        if isUpdate == 0:
                            if not servicesWithInsert.get(eventId, None):
                                servicesWithInsert[eventId] = []
                            servicesWithInsert[eventId] += [(forceString(services.value(CMainSelect.code)),
                                                             forceInt(services.value(CMainSelect.neededCount)))]
                        elif isUpdate == 1:
                            if not servicesWithUpdate.get(eventId, None):
                                servicesWithUpdate[eventId] = []
                            servicesWithUpdate[eventId] += [(forceString(services.value(CMainSelect.code)),
                                                             forceInt(services.value(CMainSelect.neededCount)))]
                        if not services.next():
                            processClientServices()
                            break
                        elif clientId != services.value(CMainSelect.clientId):
                            if not processClientServices():
                                break
                            clientId = forceRef(services.value(CMainSelect.clientId))
                            servicesWithInsert = {}
                            servicesWithUpdate = {}
            if QtGui.qApp.isInTransaction:
                log.outputRedefinedAccounts(accounts)
        except Exception, e:
            QtGui.QMessageBox.critical(
                self,
                u'Ошибка получения данных',
                u'Не удалось получить данные реестра \'%s\'\n%s' % (accountNumber, unicode(e)),
                QtGui.QMessageBox.Close)
            QtGui.qApp.isInTransaction = False
            QtGui.qApp.db.rollback()
        self.btnProcess.setEnabled(True)
        if not accounts:
            QtGui.qApp.db.rollback()
            QtGui.qApp.isInTransaction = False
        if QtGui.qApp.isInTransaction:
            self.btnProcess.setText(u'Применить')
        else:
            self.actConnection.setEnabled(True)
            self.actLogin.setEnabled(True)
            self.actLogout.setEnabled(True)
            self.btnRefresh.setEnabled(True)
            self.lwAccounts.setEnabled(True)
            self.btnProcess.setEnabled(True)
            self.btnCancel.setEnabled(False)

    @pyqtSlot()
    def on_btnCancel_clicked(self):
        reply = QtGui.QMessageBox.question(self, u'Предупреждение',
                                           u'Вы действительно хотите отменить изменения?',
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtGui.qApp.isInTransaction = False
            try:
                QtGui.qApp.db.rollback()
            except:
                pass
            self.btnProcess.setText(u'Обработать')
            self.actConnection.setEnabled(True)
            self.actLogin.setEnabled(True)
            self.actLogout.setEnabled(True)
            self.btnRefresh.setEnabled(True)
            self.lwAccounts.setEnabled(True)
            self.btnProcess.setEnabled(True)
            self.btnCancel.setEnabled(False)

    @pyqtSlot()
    def on_actQuit_triggered(self):
        self.close()

class CLog:

    def __init__(self, textBrowser):
        self.textBrowser = textBrowser
        self.textBrowser.clear()

    def outputAccountInfo(self, accountNumber, clientId, servicesWithInsert, servicesWithUpdate):

        def getCount(services):
            result = 0
            for key, items in services.items():
                result += len(items)
            return result

        insertCount = getCount(servicesWithInsert)
        updateCount = getCount(servicesWithUpdate)
        self.textBrowser.append(u'<br><b>Номер счета: %s (Пациент: %s)</b>' % (accountNumber, clientId))
        if insertCount:
            self.textBrowser.append(u'<font color="red">Количество вставляемых: %s</font>' % insertCount)
        if updateCount:
            self.textBrowser.append(u'<font color="green">Количество обновляемых: %s</font>' % updateCount)

    def outputInsertServiceInfo(self, eventId, actionId, codeService):
        self.textBrowser.append(u'<font color="red">Вставлена усулуга %s: событие %s, действие %s</fonr>' %
                                (codeService, eventId, actionId))

    def outputUpdateServiceInfo(self, eventId, actionId, codeService):
        self.textBrowser.append(u'<font color="green">Обновлена усулуга %s: событие %s, действие %s</fonr>' %
                                (codeService, eventId, actionId))
    def outputRedefinedAccounts(self, accounts):
        if accounts:
            self.textBrowser.append(u'<br><b>Необходимо переформировать реестры:</b><br>%s' % ('<br>').join(accounts))
        else:
            self.textBrowser.append(u'<br><b>Выбранные реестры не требуется переформировывать')

if __name__ == '__main__':
    QtGui.qApp = CMyApp(sys.argv)
    mainWindow = CMainWindow()
    mainWindow.show()
    if QtGui.qApp.preferences.dbAutoLogin:
        mainWindow.actLogin.activate(QtGui.QAction.Trigger)
    sys.exit(QtGui.qApp.exec_())
