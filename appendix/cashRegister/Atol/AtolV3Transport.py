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
import threading
import weakref
from collections import deque

from AtolErrors import EAtolIOError

class CAtolV3Transport:

    # константы обмена:
    STX  = 0xFE
    ESC  = 0xFD
    TSTX = 0xEE
    TESC = 0xED

    # 
    asyncReadTimeout = 0.5  # таймаут ввода байта
    asyncQueueSize   = None # unlimited
    buffCommandRespTimeout = 0.5 # таймаут чтения ответа 

    minTransportId = 0
    maxTransportId = 0xDF


    def __init__(self, port):
        self.port = port
        self.__transportId = 0x76 # self.maxTransportId
        self.__asyncQueue = deque( maxlen=self.asyncQueueSize ) # очередь для сообщений об ошибках и полученных цепочек байтов
        self.__asyncThread = CAtolV3TransportReader(self)
        self.__asyncThread.start()


    def __del__(self):
        self.__asyncThread.terminate()
        self.__asyncThread.join(self.asyncReadTimeout)


    def writeToBuff(self, data):
        self.__transportId = self.__transportId+1 if self.__transportId < self.maxTransportId else self.minTransportId

        dataLen = len(data)
        crc = self.calcCRC( bytearray([self.__transportId]) + data )
        package = bytearray([ self.STX, dataLen & 0x7F, dataLen >> 7, self.__transportId])
        for byte in data:
            self.__addEscapedByte(package, byte)
        self.__addEscapedByte(package, crc)

        for rc in xrange(4):
            self.port.write(package)
            stopWaitTime = time.time() + self.buffCommandRespTimeout
            while time.time() < stopWaitTime:
                resp = self.read()
                if isinstance(resp, bytearray) and len(resp)>1 and resp[0] == self.__transportId:
                    return resp[1:]
        raise EAtolIOError(-1)


    def read(self):
        if len(self.__asyncQueue):
            item = self.__asyncQueue.popleft()
            if item == EAtolIOError.outOfSTX:      # получен не STX
#                print "READ: out of stx"
                pass
            elif item == EAtolIOError.readTimeout: # задержка при вооде очередного байта
#                print "READ: read timeout"
                pass
            elif item == EAtolIOError.badEscape:   # ошибка в ESC-последовательности
#                print "READ: bad escape sequence"
                pass
            elif item == EAtolIOError.badCRC:      # не совпала контрольная сумма
#                print "READ: CRC error"
                pass
            else:
#                print "READ: data [%s]" % ' '.join('%02X' % b for b in item)
                return item
        return None


    def __addEscapedByte(self, package, byte):
        if byte == self.STX:
            package.append( self.ESC )
            package.append( self.TSTX )
        elif byte == self.ESC:
            package.append( self.ESC )
            package.append( self.TESC )
        else:
            package.append( byte )


    def dataArrived(self, data):
        self.__asyncQueue.append(data)

    def asyncError(self, asyncErrorCode):
        self.__asyncQueue.append(asyncErrorCode)

    crcTable = (
                0x00, 0x31, 0x62, 0x53, 0xc4, 0xf5, 0xa6, 0x97, 0xb9, 0x88, 0xdb, 0xea, 0x7d, 0x4c, 0x1f, 0x2e,
                0x43, 0x72, 0x21, 0x10, 0x87, 0xb6, 0xe5, 0xd4, 0xfa, 0xcb, 0x98, 0xa9, 0x3e, 0x0f, 0x5c, 0x6d,
                0x86, 0xb7, 0xe4, 0xd5, 0x42, 0x73, 0x20, 0x11, 0x3f, 0x0e, 0x5d, 0x6c, 0xfb, 0xca, 0x99, 0xa8,
                0xc5, 0xf4, 0xa7, 0x96, 0x01, 0x30, 0x63, 0x52, 0x7c, 0x4d, 0x1e, 0x2f, 0xb8, 0x89, 0xda, 0xeb,

                0x3d, 0x0c, 0x5f, 0x6e, 0xf9, 0xc8, 0x9b, 0xaa, 0x84, 0xb5, 0xe6, 0xd7, 0x40, 0x71, 0x22, 0x13,
                0x7e, 0x4f, 0x1c, 0x2d, 0xba, 0x8b, 0xd8, 0xe9, 0xc7, 0xf6, 0xa5, 0x94, 0x03, 0x32, 0x61, 0x50,
                0xbb, 0x8a, 0xd9, 0xe8, 0x7f, 0x4e, 0x1d, 0x2c, 0x02, 0x33, 0x60, 0x51, 0xc6, 0xf7, 0xa4, 0x95,
                0xf8, 0xc9, 0x9a, 0xab, 0x3c, 0x0d, 0x5e, 0x6f, 0x41, 0x70, 0x23, 0x12, 0x85, 0xb4, 0xe7, 0xd6,

                0x7a, 0x4b, 0x18, 0x29, 0xbe, 0x8f, 0xdc, 0xed, 0xc3, 0xf2, 0xa1, 0x90, 0x07, 0x36, 0x65, 0x54,
                0x39, 0x08, 0x5b, 0x6a, 0xfd, 0xcc, 0x9f, 0xae, 0x80, 0xb1, 0xe2, 0xd3, 0x44, 0x75, 0x26, 0x17,
                0xfc, 0xcd, 0x9e, 0xaf, 0x38, 0x09, 0x5a, 0x6b, 0x45, 0x74, 0x27, 0x16, 0x81, 0xb0, 0xe3, 0xd2,
                0xbf, 0x8e, 0xdd, 0xec, 0x7b, 0x4a, 0x19, 0x28, 0x06, 0x37, 0x64, 0x55, 0xc2, 0xf3, 0xa0, 0x91,

                0x47, 0x76, 0x25, 0x14, 0x83, 0xb2, 0xe1, 0xd0, 0xfe, 0xcf, 0x9c, 0xad, 0x3a, 0x0b, 0x58, 0x69,
                0x04, 0x35, 0x66, 0x57, 0xc0, 0xf1, 0xa2, 0x93, 0xbd, 0x8c, 0xdf, 0xee, 0x79, 0x48, 0x1b, 0x2a,
                0xc1, 0xf0, 0xa3, 0x92, 0x05, 0x34, 0x67, 0x56, 0x78, 0x49, 0x1a, 0x2b, 0xbc, 0x8d, 0xde, 0xef,
                0x82, 0xb3, 0xe0, 0xd1, 0x46, 0x77, 0x24, 0x15, 0x3b, 0x0a, 0x59, 0x68, 0xff, 0xce, 0x9d, 0xac,
               )

    @classmethod
    def calcCRC(cls, data):
        crc = 0xFF
        for byte in data:
            crc = cls.crcTable[ byte ^ crc ]
        return crc


class CAtolV3TransportReader(threading.Thread):
    def __init__(self, transport):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        transport.port.timeout = transport.asyncReadTimeout
        self.refToTransport = weakref.ref(transport)
        self.__termEvent  = threading.Event()


    def terminate(self):
        self.__termEvent.set()


    def run(self):
        buffer = bytearray()
        state = 0 # 0 - ожидание STX, 1-норм, 2-ожидание TESC или TSTS
        expectedLength = 0
        while not self.__termEvent.isSet():
            transport = self.refToTransport()
            if transport is None:
                break
            if transport.port.isOpen():
                try:
                    bytes = transport.port.read(size=1)
                except:
                    bytes = None

                if not bytes:
                    if state != 0:
                        buffer = bytearray()
                        state = 0
                        transport.asyncError(EAtolIOError.readTimeout)
                    continue # ничего нет - возвр. на цикл по вводу
                else:
                    byte = ord(bytes)
#                    print 'byte = %d (0x%02x)' % ( byte, byte )
                    if state == 0:
                        if byte == transport.STX:
                            state = 1
                        else:
                            transport.asyncError(EAtolIOError.outOfSTX)
                        continue
                    elif state == 1:
                        if byte == transport.ESC:
                            state = 2
                            continue
                    elif state == 2:
                        if byte == transport.TESC:
                            byte = transport.ESC
                            state = 1
                        elif byte == transport.TSTX:
                            byte = transport.STX
                            state = 1
                        else:
                            transport.asyncError(EAtolIOError.badEscape)
                            buffer = bytearray()
                            state = 0
                            continue
                    buffer.append(byte)
                    if len(buffer) == 2:
                        expectedLength = ( buffer[0]&0x7F | buffer[1]<<7 ) + 4 # len + id + crc
#                        print "expectedLength=", expectedLength

#                    print "expectedLength=", expectedLength, "buffer=", repr(buffer)

                    if len(buffer) >= 4 and len(buffer) == expectedLength:
                        dataBytes = buffer[2:-1]
                        crc = transport.calcCRC(dataBytes)
                        if crc == buffer[-1]:
                            transport.dataArrived(dataBytes)
                        else:
                            transport.asyncError(EAtolIOError.badCRC)
                        buffer = bytearray()
                        state = 0
            else:
                self.__termEvent.wait(transport.asyncReadTimeout)

