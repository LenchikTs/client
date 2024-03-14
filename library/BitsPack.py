# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Упаковка данных в битовую строку,
## применяется при формировании штрих-кодов.
##
#############################################################################

from base64 import b64encode

class CBitsPack:
    def __init__(self, encoding='utf8'):
        self._bits = ''
        self.encoding = encoding


    def __len__(self):
        return len(self._bits)


    def packBool(self, val):
        self._bits += '1' if val else '0'


    def packInt(self, val, widthInBits):
        if isinstance(val, (int, long)):
            intVal = val
        else:
            try:
                intVal = long(val)
            except:
                intVal = 0
        self._bits += '{0:0{1}b}'.format(intVal, widthInBits)[-widthInBits:]


    def packString(self, val, widthInBytes=None, fillChar=' '):
        if isinstance(val, str):
            bytes = val
        elif isinstance(val, unicode):
            bytes = val.encode(self.encoding, 'ignore')
        else:
            bytes = unicode(val).encode(self.encoding, 'ignore')
        if widthInBytes:
            bytes = bytes.ljust(widthInBytes,fillChar) if len(bytes)<=widthInBytes else bytes[:widthInBytes]
        self._bits += ''.join( '{0:08b}'.format(ord(byte)) for byte in bytes )


    def pad(self, bound=8):
        self._bits += '0'*(-len(self._bits)%bound)


    def bits(self):
        return self._bits


    def bytes(self):
        assert len(self._bits) % 8 == 0
        return ''.join( chr(int(self._bits[i:i+8],2)) for i in xrange(0, len(self._bits),8) )


    def b64(self):
        return b64encode(self.bytes())


    def hex(self):
        assert len(self._bits) % 8 == 0
        return ''.join( '{0:02X}'.format((int(self._bits[i:i+8],2))) for i in xrange(0, len(self._bits),8) )

