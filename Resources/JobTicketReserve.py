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
from PyQt4.QtCore import QObject, QTimer, SIGNAL

from library.Utils import forceBool

class CJobTicketReserveLevel:
    def __init__(self, key, prevLevel):
        self.key = key
        self.prevLevel = prevLevel
        self.reservedOnPrevLevels = prevLevel.getReservedOnAllLevels() if prevLevel else set([])
        self.reserved = set([])


    def add(self, jobTicketId):
        self.reserved.add(jobTicketId)


    def remove(self, jobTicketId):
        self.reserved.discard(jobTicketId)


    def getReservedOnAllLevels(self):
        return self.reserved | self.reservedOnPrevLevels


    def getUniqueReservedIdSet(self):
        return self.reserved - self.reservedOnPrevLevels


    def isAnythingReserved(self):
        return bool(self.reserved) or bool(self.reservedOnPrevLevels)


class CJobTicketReserveHolder(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.timerProlongReservation = QTimer(self) # 1 раз в минуту
        self.timerProlongReservation.setInterval(60000)
        self.currLevel = None
        self.connect(self.timerProlongReservation, SIGNAL('timeout()'), self.prolongReservation)


    def addLevel(self, key):
        self.currLevel = CJobTicketReserveLevel(key, self.currLevel)


    def delLevel(self, key, releaseReserve=True):
        assert self.currLevel is not None
        assert self.currLevel.key == key

        if releaseReserve:
            try:
                self.delAllJobTicketReservations()
            except:
                QtGui.qApp.logCurrentException()

        self.currLevel = self.currLevel.prevLevel
        if self.currLevel is None or not self.currLevel.isAnythingReserved():
            if self.timerProlongReservation.isActive():
                self.timerProlongReservation.stop()


    def addJobTicketReservation(self, jobTicketId):
        if self.currLevel:

            db = QtGui.qApp.db
            query = db.query('SELECT addJobTicketReservation(%d)' %jobTicketId)
            if query.next():
                result = forceBool(query.record().value(0))
            else:
                result = False
            if result:
                isAnythingReserved = self.currLevel.isAnythingReserved()
                if jobTicketId:
                    self.currLevel.add(jobTicketId)
                if not isAnythingReserved:
                    self.timerProlongReservation.start()
            return result
        return False


    def getReservedJobTickets(self):
        assert self.currLevel is not None
        return list(self.currLevel.getReservedOnAllLevels())


    def delJobTicketReservation(self, jobTicketId):
        if self.currLevel:
            db = QtGui.qApp.db
            query = db.query('SELECT delJobTicketReservation(%d)' % jobTicketId)
            if query.next():
                result = forceBool(query.record().value(0))
            else:
                result = False

            self.currLevel.remove(jobTicketId)

            if not self.currLevel.isAnythingReserved():
                self.timerProlongReservation.stop()
            return result
        return False


    def delAllJobTicketReservations(self):
        assert self.currLevel is not None

        getUniqueReservedIdSet = self.currLevel.getUniqueReservedIdSet()
        for jobTicketId in getUniqueReservedIdSet:
            self.delJobTicketReservation(jobTicketId)


    def prolongReservation(self):
        if self.currLevel is not None:
            db = QtGui.qApp.db
            reservedIdSet = self.currLevel.getReservedOnAllLevels()
            for jobTicketId in reservedIdSet:
                db.query('SELECT checkJobTicketReservation(%d)' % jobTicketId)

