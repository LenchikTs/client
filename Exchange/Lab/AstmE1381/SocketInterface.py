#! /usr/bin/env python
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
## Интерфейс приёма/отравки сообщений согласно протокола
## ASTM E1381 через сокет (представлены "клиентский" и "серверный" вариант)
##
#############################################################################


import time
import socket

from AbstractInterface import CAbstractInterface

def getSocketInterface(opts, isServer):
    return (CServerSocketInterface if isServer else CClientSocketInterface)(opts)


class CClientSocketInterface(CAbstractInterface):
    def __init__(self, opts):
        CAbstractInterface.__init__(self)
        self.host = opts.get('address', '')
        self.port = opts.get('port', 1025)
        self.socket = None


    def prepareForWork(self):
        if self.socket is None:
            self.open()
        return bool(self.socket)


    def open(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((self.host, self.port))
        self.socket = s


    def close(self):
        if self.socket is not None:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None


    def read(self, timeout):
        if self.socket:
            self.socket.settimeout(timeout)
            try:
                return self.socket.recv(1)
            except socket.timeout:
                return ''
            except:
                self.close()
                raise
        else:
            return ''


    def write(self, buff):
        if self.socket:
            self.socket.settimeout(1)
            try:
                self.socket.sendall(buff)
            except:
                self.close()
                raise



class CServerSocketInterface(CClientSocketInterface):
    def __init__(self, opts):
        CClientSocketInterface.__init__(self, opts)
        self.ctrlSocket = None


    def open(self):
        if self.ctrlSocket:
            try:
                self.ctrlSocket.fileno()
            except:
                self.ctrlSocket = None
        if self.ctrlSocket is None:
            try:
                self.ctrlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.ctrlSocket.bind((self.host, self.port))
                self.ctrlSocket.listen(1)
                self.ctrlSocket.settimeout(0)
            except:
                self.ctrlSocket = None
                return
        if self.ctrlSocket:
            try:
                self.socket, addr = self.ctrlSocket.accept()
            except:
                self.socket = None


    def close(self):
        CClientSocketInterface.close(self)
        if self.ctrlSocket:
            try:
                self.ctrlSocket.close()
            except:
                pass
            self.ctrlSocket = None



if __name__ == '__main__':
    from AbstractLoop  import CBaseMessage
    from AstmE1381Loop import CAstmE1381Loop
    

    def testSingleSocketSendMessage(host, port, isServer=False):
        print '-'*60
        print 'testSingleSocketSendMessage'
        opts = {'host':host, 'port':port}
        interface = getSocketInterface(opts, isServer)

        try:
            f = file('samples/order-small.ord','r')
#            f = file('samples/order-average.ord','r')
#            f = file('samples/order-big.ord','r')
            messageBody = [ s.replace('\r','').replace('\n','') for s in f ]
            f.close()
        except:
            messageBody = ['1','2','3','4']

        loop = CAstmE1381Loop(interface, interface)
        loop.setName('i/o loop')
#        l.setLogLevel(9)
        loop.start()
        try:
            loop.send(CBaseMessage(messageBody))
            for i in range(60):
                print 'write',i
                if loop.outputQueue.empty():
                    break
                time.sleep(1)
        finally:
            loop.stop()



    def testSingleSocketGetMessage(host, port, isServer=False):
        print '-'*60
        print 'testSingleSocketGetMessage'
        opts = {'host':host, 'port':port}
        interface = getSocketInterface(opts, isServer)

        loop = CAstmE1381Loop(interface, interface)
        loop.setName('i/o loop')
        loop.setLogLevel(9)
        loop.start()
        try:
            for i in range(60):
                print 'read', i
                message = loop.get()
                if message:
                    print repr(message.body)
                    message.dismiss()
                time.sleep(1)
        finally:
            loop.stop()

#    testSingleSocketSendMessage('192.168.56.101', 4001, False)
#    testSingleSocketGetMessage('192.168.56.101', 4001, False)
#    testSingleSocketSendMessage('192.168.56.1', 4001, True)
    testSingleSocketGetMessage('192.168.56.1', 4001, True)
