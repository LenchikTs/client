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
##
## Базовый класс цикла приёма/отравки сообщений согласно протокола
## ASTM E1381 (через последовательный порт сокет) либо файлового обмена
##
#############################################################################

import sys
import traceback
import threading
import time
import Queue
from   library.Utils import anyToUnicode


class CBaseMessage:
    def __init__(self, body):
        self.body = body

    def dismiss(self):
        pass


class CAbstractLoop(threading.Thread):
    #
    exceptionDelay = 1
    def __init__(self):
        threading.Thread.__init__(self)
        self.inputQueue  = Queue.Queue()
        self.outputQueue = Queue.Queue()
        self._continue   = threading.Event()
        self._stopped    = threading.Event()
        self._logLevel   = 0
        self.onMessageAccepted  = None # наверное, методически правильнее
        self.onMessageProcessed = None # накручивать сигналы/слоты. но я пока не хочу.
        self.onLog              = None
        self.onException        = None


    def setLogLevel(self, logLevel):
        self._logLevel = logLevel


    def send(self, message):
        self.outputQueue.put(message)


    def acceptInputMessage(self, message):
        if self.onMessageAccepted:
            self.onMessageAccepted(message)
        else:
            self.inputQueue.put(message)


    def get(self):
        try:
            return self.inputQueue.get_nowait()
        except Queue.Empty:
            return None
        except:
            raise


    def stop(self, timeout=None):
        self._continue.clear()
        self._stopped.wait(timeout)


    def run(self):
        self._continue.set()
        self._stopped.clear()
        while self._continue.isSet():
            try:
                self._mainLoop()
            except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                exceptionText = anyToUnicode('%s'%exceptionValue)
                exceptionStack = anyToUnicode(''.join(traceback.format_tb(exceptionTraceback)))
                if self.onException:
                    self.onException('%s:%s\n%s' % (self.getName(), exceptionText, exceptionStack))
                else:
                    print u'%s:%s\n%s' % (self.getName(), exceptionText, exceptionStack)
                    sys.stdout.flush()
                time.sleep(self.exceptionDelay)
        self._stopped.set()


    def log(self, level, text):
        # 1: work start/stop
        # 2: message exchange
        # 3: frame exchange
        # 4: byte exchange
        if level<=self._logLevel:
            if self.onLog:
                self.onLog(u'%s:%d: %s' % (self.getName(), level, text))
            else:
                print (u'%s:%d: %s' % (self.getName(), level, text)).encode(sys.stdout.encoding)
                sys.stdout.flush()


    def _mainLoop(self):
        raise NotImplementedError
