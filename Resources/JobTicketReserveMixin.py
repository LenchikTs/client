# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import *

from library.DialogBase         import CConstructHelperMixin
from library.Utils              import *
    

class CJobTicketReserveMixin(CConstructHelperMixin):
    def __init__(self):
        self.addObject('timerProlongReservation', QTimer(self)) # 1 раз в минуту
        self.timerProlongReservation.setInterval(60000)
        self.reservation = {} # список id резервируемых Job_Ticket

    def getMaxId(self, jobTicketId):
        db = QtGui.qApp.db
        stmt = 'SELECT MAX(`id`) FROM Job_Ticket WHERE Job_Ticket.`master_id` = (SELECT JT.`master_id` FROM Job_Ticket AS JT WHERE JT.`id` = %d)' %jobTicketId
        query = db.query(stmt)
        if query.next():
            return forceRef(query.value(0))
        else:
            return 0
        

    def addJobTicketReservation(self, jobTicketId, length=1):
        db = QtGui.qApp.db
        iteration = 0
        maxId = self.getMaxId(jobTicketId)
        result = False
        while iteration < length:
            resJobTicketId = jobTicketId+iteration
            if resJobTicketId > maxId:
                self.delJobTicketReservation(jobTicketId)
                result = False
                break
            query = db.query('SELECT addJobTicketReservation(%d)' %(resJobTicketId))
            if query.next():
                result = forceBool(query.record().value(0))
            else:
                result = False
            if result:
                if not self.reservation:
                    self.timerProlongReservation.start()
                jobTicketIdList = self.reservation.setdefault(jobTicketId, [])
                if not resJobTicketId in jobTicketIdList:
                    jobTicketIdList.append(resJobTicketId)
            else:
                self.delJobTicketReservation(jobTicketId)
                break
            iteration += 1
        return result


    def delJobTicketReservation(self, masterJobTicketId):
        db = QtGui.qApp.db
        for jobTicketId in self.reservation[masterJobTicketId]:
            query = db.query('SELECT delJobTicketReservation(%d)' % jobTicketId)

        try:
            del self.reservation[masterJobTicketId]
        except:
            pass

        if not self.reservation:
            self.timerProlongReservation.stop()

    def delAllJobTicketReservationsWithExcluding(self, excludingJTIdList):
        for jobTicketId in self.reservation.keys():
            if jobTicketId not in excludingJTIdList:
                self.delJobTicketReservation(jobTicketId)

    def delAllJobTicketReservations(self):
        for jobTicketId in self.reservation.keys():
            self.delJobTicketReservation(jobTicketId)


    def getReservedJobTickets(self):
        return self.reservation.keys()
    
    # должно выполняться из save CActionProperty. Так что в общем случае мы в транзакции.
    def makeJobTicketIdQueue(self, masterJobTicketId):
        if masterJobTicketId and masterJobTicketId in self.reservation.keys():
            stmtTemplate = 'UPDATE `Job_Ticket` SET `masterJobTicket_id`=%d WHERE `id`=%d'
            for jobTicketId in self.reservation[masterJobTicketId][1:]: # первый jobTicketId равен masterJobTicketId
                QtGui.qApp.db.query(stmtTemplate % (masterJobTicketId, jobTicketId))
            


    @pyqtSignature('')
    def on_timerProlongReservation_timeout(self):
        db = QtGui.qApp.db
        for jobTicketIdList in self.reservation.values():
            for jobTicketId in jobTicketIdList:
                db.query('SELECT checkJobTicketReservation(%d)' % jobTicketId)
            
