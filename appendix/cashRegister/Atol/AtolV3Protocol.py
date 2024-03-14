# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


import time
from AtolErrors      import EAtolBufferError
from AtolV3Transport import CAtolV3Transport


class CAtolV3Protocol(CAtolV3Transport):
    # 
    asyncTransportId = 0xF0

    # Команды буфера
    bcAdd    = 0xC1
    bcAck    = 0xC2
    bcReq    = 0xC3
    bcAbort  = 0xC4
    bcAckAdd = 0xC5

    # Флаги задания
    tfNeedResult    = 1 # 0-й бит, настройка передачи результата задания (0 – результат не передается, 1 – результат передается);
    tfIgnoreError   = 2 # 1-й бит, настройка работы с ошибками (0 – не игнорировать, 1 – игнорировать);
    tfWaitAsyncData = 4 # 2-й бит, настройка ожидания выполнения задания (0 – сразу выполнять задание, 1 – ожидать выполнения задания сколь угодно долго, не препятствовать добавлению нового задания).

    # Статус задания
    tsPending     = 0xA1
    tsInProgress  = 0xA2
    tsResult      = 0xA3
    tsError       = 0xA4
    tsStopped     = 0xA5
    tsAsyncResult = 0xA6
    tsAsyncError  = 0xA7
    tsWaiting     = 0xA8

    # Ошибки, они тоже возвращаются как статус - поэтому их можно считать специальными статусами
    tsEOverflow      = EAtolBufferError.E_Overflow
    tsEAlreadyExists = EAtolBufferError.E_AlreadyExists
    tsENotFound      = EAtolBufferError.E_NotFound
    tsEIllegalValue  = EAtolBufferError.E_IllegalValue

    minTaskId = 0
    maxTaskId = 0xDF


    def __init__(self, port):
        CAtolV3Transport.__init__(self, port)
        self.__taskId = self.minTaskId
        self.__passwd = bytearray(b'\00\00')


    def setPasswd(self, passwd):
        assert isinstance(passwd, (bytearray, bytes, str)) and len(passwd) == 2
        self.__passwd = bytearray(passwd)


    def reset(self):
        bytes = bytearray( [ self.bcAbort ] )
        resp = self.writeToBuff(bytes)
        if resp[0] == self.tsResult:
            return None
        if resp[0] == self.tsInProgress:
            return resp[1]
        assert False, 'wrong answer for abort (%r)' % resp


    def _rep(self, title, ok, resp):
        print '%s: ok=%s, resp=%s, taskId=%02X' % ( title, ok, ' '.join(['%02X' % b for b in resp]), self.__taskId )


    def execCommand(self, command):
        resp = self.sendAdd(self.tfNeedResult|self.tfIgnoreError, command)
        status = resp[0] if resp else None
        if status == self.tsResult:
#            self._rep('execCommand(1)', True, resp[1:])
            return True, resp[1:]
        if status == self.tsError:
#            self._rep('execCommand(2)', False, resp[1:])
            return False, resp[1:]
        if status in(self.tsPending, self.tsInProgress, self.tsWaiting):
            t0 = time.time() + 10
            while time.time() < t0:
                time.sleep(0)
                raw = self.read()
                if isinstance(raw, bytearray) and len(raw)>2 and raw[0] == self.asyncTransportId and raw[1] in (self.tsAsyncResult, self.tsAsyncError) and raw[2] == self.__taskId:
                    resp = raw[1:]
                    status = resp[0] if resp else None
                    if status == self.tsAsyncResult:
#                        self._rep('execCommand(3)', True, resp[2:])
                        return True, resp[2:]
                    if status == self.tsAsyncError:
#                        self._rep('execCommand(4)', False, resp[2:])
                        return False, resp[2:]
            raise EAtolBufferError(EAtolBufferError.bufferTimeout)

        if status == self.tsStopped:
            raise EAtolBufferError(EAtolBufferError.bufferStopped)

        if status in ( self.tsEOverflow, self.tsEAlreadyExists, self.tsENotFound, self.tsEIllegalValue ):
            raise EAtolBufferError(status)

        print "Unkwown status in %r" % resp
        return None, None


#        while time.time() < t0:
#            time.sleep(0.1)
#            r = self.read()
#            if r:
#                print repr(r)
#        return resp


    def sendAdd(self, flags, command):
        self.__taskId = self.__taskId+1 if self.__taskId<self.maxTaskId else self.minTaskId
        bytes = bytearray( [ self.bcAdd, flags, self.__taskId ] ) + self.__passwd + command
        return self.writeToBuff(bytes)

