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

from PyQt4 import QtGui
from PyQt4.QtCore  import SIGNAL, pyqtSignature, QDate, QObject, QTimer

from library.Utils import forceBool, forceInt, forceRef, forceString

__all__ = [ 'CCounterController',
          ]


class CCounterTimer(QTimer):
    def __init__(self, counterValueCacheId, parent):
        QTimer.__init__(self, parent)
        self._counterValueCacheId = counterValueCacheId
        self.setInterval(240000)
        self.connect(self, SIGNAL('timeout()'), self.on_timout)


    def on_timout(self):
        self.emit(SIGNAL('counterTimerTimeout(int)'), self._counterValueCacheId)



class CCounterController(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.reservation = {}
        self.lastReservationId = None


    def getCounterValueCacheId(self, counterId, date):
        counterValueCacheId = getCounterValueCacheId(counterId, date)
        if counterValueCacheId:
            counterTimer = CCounterTimer(counterValueCacheId, self)
            self.connect(counterTimer, SIGNAL('counterTimerTimeout(int)'), self.on_counterTimerTimeout)
            counterTimer.start()
            self.reservation[counterValueCacheId] = counterTimer
            self.lastReservationId = counterValueCacheId
            return counterValueCacheId


    def getDocumentNumber(self, clientId, counterId, date=None):
        db = QtGui.qApp.db
        sequenceFlag = forceInt(db.translate('rbCounter', 'id', counterId, 'sequenceFlag'))
        if sequenceFlag:
            counterValueCacheId = self.getCounterValueCacheId(counterId, date)
            counterValue = forceInt(db.translate('rbCounter_Value_Cache', 'id', counterValueCacheId, 'value'))
        else:
            counterValue = getCounterValue(counterId, date)
        return getDocumentNumber(clientId, counterId, counterValue)


    def delCounterValueCacheReservation(self, id):
        QtGui.qApp.db.deleteRecord('rbCounter_Value_Cache', 'id=%d' % id)


    def delAllCounterValueIdReservation(self):
        for id in self.reservation.keys():
            self.delCounterValueCacheReservation(id)


    def resetCounterValueCacheReservation(self, id):
        db = QtGui.qApp.db
        query = db.query('SELECT resetCounterValueCacheReservation(%d)' % id)
        if query.next():
            result = forceBool(query.record().value(0))
        else:
            result = False

        try:
            timer = self.reservation.pop(id)
            timer.stop()
        except:
            pass

        return result


    def resetAllCounterValueIdReservation(self):
        for id in self.reservation.keys():
            self.resetCounterValueCacheReservation(id)


    @pyqtSignature('')
    def on_counterTimerTimeout(self, counterValueCacheId):
        if counterValueCacheId:
            QtGui.qApp.db.query('SELECT prolongateCounterValueCacheReservation(%d)' % counterValueCacheId)

# ##############################################################


def getCounterValueCacheId(counterId, date):
    db = QtGui.qApp.db
    while True:
        query = db.query('SELECT getCounterValueCacheId(%d, %s)' % (counterId, db.formatDate(date) if date else 'CURRENT_DATE'))
        if query.next():
            counterValueCacheId = forceRef(query.value(0))
            if counterValueCacheId:
                return counterValueCacheId


def getCounterValue(counterId, date):
    db = QtGui.qApp.db
    while True:
        query = db.query('SELECT getCounterValue(%d, %s)' % (counterId, db.formatDate(date) if date else 'CURRENT_DATE'))
        if query.next():
            result = forceRef(query.value(0))
            if result is not None:
                return result


def getDocumentNumber(clientId, counterId, counterValue):
    if counterValue:
        record = QtGui.qApp.db.getRecord('rbCounter', 'prefix, postfix, rbCounter.separator, format', counterId)
        format = forceString(record.value('format'))
        if format:
            return formatDocumentNumber2(format, counterValue, clientId)
        else:
            prefix = forceString(record.value('prefix'))
            postfix = forceString(record.value('postfix'))
            separator = forceString(record.value('separator'))
            return formatDocumentNumber(prefix, postfix, separator, counterValue, clientId)
    return u''


# example: formatDocumentNumber('date(yy:MM:dd);id(2)', 'id();str(GD23)', '--', 111, 4442) ### `postfix` like `prefix`
def formatDocumentNumber(prefix, postfix, separator, value, clientId):
    def getDatePrefix(val):
        val = val.replace('Y', 'y').replace('m', 'M').replace('D', 'd')
        if val.count('y') not in (0, 2, 4) or val.count('M') > 2 or val.count('d') > 2:
            return None
        s = QtGui.qApp.db.getCurrentDate().toString(val)
        if QDate.fromString(s, val).isValid():
            return unicode(s)
        return None

    def getIdPrefix(val):
        if not clientId:
            return None
        if val == '':
            return str(clientId)
        stmt = 'SELECT `identifier` FROM ClientIdentification JOIN rbAccountingSystem ON rbAccountingSystem.`id`=ClientIdentification.`accountingSystem_id` WHERE ClientIdentification.`client_id`=%d AND rbAccountingSystem.`code`=\'%s\'' % (clientId, val)
        query = QtGui.qApp.db.query(stmt)
        if query.first():
            return forceString(query.value(0))
        return None

    def getStrAddition(val):
        return val

    def getPre_Post_fixValue(ppValue):
        prefixTypes = {'date': getDatePrefix, 'id': getIdPrefix, 'str': getStrAddition}
        prefixList = ppValue.split(';')
        result = []
        for p in prefixList:
            for t in prefixTypes:
                f = p.find(t)
                if f == 0:
                    tl = len(t)
                    val = p[tl:]
                    if val.startswith('(') and val.endswith(')'):
                        val = prefixTypes[t](val.replace('(', '').replace(')', ''))
                        if val:
                            result.append(val)
        return result
    prefix  = getPre_Post_fixValue(prefix)  if prefix  else []
    postfix = getPre_Post_fixValue(postfix) if postfix else []
    return separator.join(prefix+['%d' % value]+postfix)


def formatDocumentNumber2Int(format, value, clientId, date=None):
    class CLocClientIdFmt:
        def __init__(self,  clientId):
            self.clientId = clientId

        def __getattr__(self, attr):
            return self.__getIdentifier(attr)

        def __format__(self,  fmt):
            return self.clientId.__format__(fmt)

        def __getIdentifier(self, code):
            if self.clientId:
                db = QtGui.qApp.db
                tableClientIdentification = db.table('ClientIdentification')
                tableAccountingSystem     = db.table('rbAccountingSystem')
                table = tableClientIdentification.innerJoin(tableAccountingSystem, tableAccountingSystem['id'].eq(tableClientIdentification['accountingSystem_id']))
                record = db.getRecordEx(table,
                                        'identifier',
                                        db.joinAnd([tableClientIdentification['client_id'].eq(self.clientId),
                                                    tableClientIdentification['deleted'].eq(0),
                                                    tableAccountingSystem['code'].eq(code)
                                                   ]
                                                  )
                                       )
                if record:
                    return forceString(record.value(0))
            return ''

    if not date:
        # date = QDate.currentDate()
        date = QtGui.qApp.db.getCurrentDate()
    year, month, day = date.getDate()
    params = { 'value'    : value,
               'day'      : day,
#               'dd'       : '%02d' % day,
               'month'    : month,
#               'mm'       : '%02d' % month,
               'year'     : year,
               'yy'       : '%02d' % (year % 100),
#               'doy'      : date.dayOfYear(),
               'clientId' : CLocClientIdFmt(clientId)
             }
    return format.format(**params)



def formatDocumentNumber2(format, value, clientId):
    try:
        return formatDocumentNumber2Int(format, value, clientId)
    except:
        QtGui.qApp.logCurrentException()
        return u'*ОШИБКА*'


def delCachedValues(counterId, value):
    db = QtGui.qApp.db
    query = db.query('''SELECT rbCounter_Value_Cache.id, rbCounter_Value_Cache.value FROM rbCounter_Value_Cache 
                                LEFT JOIN rbCounter_Value ON rbCounter_Value.id = rbCounter_Value_Cache.master_id 
                                LEFT JOIN rbCounter ON rbCounter.id = rbCounter_Value.master_id
                                WHERE rbCounter.id = %d AND rbCounter_Value_Cache.resTimestamp IS NULL'''%counterId)
    while query.next():
        cachedValueId = forceInt(query.value(0))
        cachedValue = forceInt(query.value(1))
        if cachedValue <= value:
            db.query('DELETE FROM rbCounter_Value_Cache WHERE id = %i'%cachedValueId)
