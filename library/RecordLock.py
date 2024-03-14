# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QObject, QTimer

from library.Utils import forceDateTime, forceRef, forceString, quote, forceInt


class CRecordLockMixin:
    def __init__(self):
        self._appLockIdList = []
        self._timerProlongLock = None


    def lock(self, tableName, id, propertyIndex=0, shorted=0):
        # shorted=0 - блокировка идёт как обычно, shorted=1 - блокируется только запись (id) в указанной таблице.
        if not id or QtGui.qApp.disableLock:
            return True
        while True:
            appLockId, message = self._tryLock(tableName, id, propertyIndex, shorted)
            if appLockId:
                return appLockId
            if not self._confirmLock(message):
                return False


    def tryLock(self, tableName, id, propertyIndex=0, shorted=0):
        if not id or QtGui.qApp.disableLock:
            return True, ''
        appLockId, message = self._tryLock(tableName, id, propertyIndex, shorted)
        return appLockId, message


    def lockList(self, tableName, idList, propertyIndex=0):
        for id in idList:
            self.lock(tableName, id, propertyIndex)


    def lockListEx(self, tableName, idList, propertyIndex = 0, shorted = 0):
        for id in idList:
            if not self.lock(tableName, id, propertyIndex, shorted):
                self.releaseLock()
                break


    def releaseLock(self, appLockId=None):
        # None: освободить все
        db = QtGui.qApp.db
        db.transaction()
        try:
            if appLockId:
                if appLockId in self._appLockIdList:
                    if db.name == 'postgres':
                        db.query('select ReleaseAppLock(%d)' % appLockId)
                    else:
                        db.query('CALL ReleaseAppLock(%d)' % appLockId)
                    self._appLockIdList.remove(appLockId)
            else:
                for appLockId in self._appLockIdList:
                    if db.name == 'postgres':
                        db.query('select ReleaseAppLock(%d)' % appLockId)
                    else:
                        db.query('CALL ReleaseAppLock(%d)' % appLockId)
                    self._appLockIdList = []
            if not self._appLockIdList and self._timerProlongLock is not None:
                self._timerProlongLock.stop()
            db.commit()
        except:
            db.rollback()
            raise


    def locked(self):
        return bool(self._appLockIdList)


    def _startTimer(self):
        if self._timerProlongLock is None:
            self._timerProlongLock = QTimer(self)
            QObject.connect(self._timerProlongLock, SIGNAL('timeout()'), self._prolongLocks)
            self._timerProlongLock.setInterval(60000)  # 1 раз в минуту
        if not self._timerProlongLock.isActive():
            self._timerProlongLock.start()


    def _tryLock(self, tableName, id, propertyIndex, shorted):
        u"""Однократная попытка установить блокировку и учёт блокировки"""
        ok, lockResult = QtGui.qApp.call(self, self._tryLockInt, (tableName, id, propertyIndex, shorted))
        if ok:
            isSuccess, appLockId, lockInfo = lockResult
        else:
            isSuccess, appLockId, lockInfo = False, None, None
        if isSuccess:
            self._appLockIdList.append(appLockId)
            self._startTimer()
            return appLockId, ''
        if lockInfo:
            message = u'Данные (id записи: %s) заблокированы %s\nпользователем %s\nс компьютера %s' % (
                forceRef(id), forceString(lockInfo[0]), lockInfo[1], lockInfo[2])
        else:
            message = u'Не удалось установить блокировку'
        return None, message


    def _tryLockInt(self, tableName, id, propertyIndex, shorted):
        u"""Однократная попытка установить блокировку"""
        isSuccess = False
        appLockId = None
        lockInfo = None
        db = QtGui.qApp.db
        personId = str(QtGui.qApp.userId) if QtGui.qApp.userId else 'NULL'

        # TODO Мне кажется, что корректнее было бы перенести реализацию в методы класса CDatabase и его наследников.
        # И обойтись тут без ветвления.
        id = forceInt(id)
        db.transaction()
        try:
            if db.name == 'postgres':
                query = db.query('select getAppLock(%s, %d, %d, %s, %s)' % (
                quote(tableName), id, propertyIndex, personId, quote(QtGui.qApp.hostName)))
            else:
                query = db.query('CALL getAppLockV2_(%s, %d, %d, %d, %s, %s, @res)' % (
                quote(tableName), id, propertyIndex, shorted, personId, quote(QtGui.qApp.hostName)))
                query = db.query('SELECT @res')
            if query.next():
                record = query.record()
                s = forceString(record.value(0)).split()
                if len(s) > 1:
                    isSuccess = int(s[0])
                    appLockId = int(s[1])
            if not isSuccess and appLockId:
                lockRecord = db.getRecord('AppLock', ['lockTime', 'person_id', 'addr'], appLockId)
                if lockRecord:
                    lockTime = forceDateTime(lockRecord.value('lockTime'))
                    personId = forceRef(lockRecord.value('person_id'))
                    personName = forceString(db.translate('vrbPersonWithSpecialityAndOrgStr', 'id', personId, "concat_ws(' ', code, name)")) if personId else u'аноним'
                    addr = forceString(lockRecord.value('addr'))
                    lockInfo = lockTime, personName, addr
            db.commit()
        except:
            db.rollback()
            raise
        return isSuccess, appLockId, lockInfo


    def _confirmLock(self, message):
        return QtGui.QMessageBox().critical(self,
                                            u'Ограничение совместного доступа к данным',
                                            message,
                                            QtGui.QMessageBox.Retry | QtGui.QMessageBox.Cancel,
                                            QtGui.QMessageBox.Retry
                                            ) == QtGui.QMessageBox.Retry


    def _prolongLocks(self):
        db = QtGui.qApp.db
        if QtGui.qApp.isBusyReconnect == 1:
            return
        db.transaction()
        try:
            for appLockId in self._appLockIdList:
                if db.name == 'postgres':
                    db.query('select ProlongAppLock(%d)' % appLockId)
                else:
                    db.query('CALL ProlongAppLock(%d)' % appLockId)
            db.commit()
        except:
            db.rollback()
            raise
