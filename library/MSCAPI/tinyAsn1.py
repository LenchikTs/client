#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## ad hoc&dirty ASN.1/DER кодирование и декодирование.
##
## ограничения:
##  - поддержаны:
##    Asn1OctetString : OCTETSTRING,
##    Asn1BitString   : BITSTRING,
##    Asn1Oid         : OBJECT IDENTIFICATOR,
##    Asn1Sequence    : SEQUENCE (как список)
##    Asn1Structure   : SEQUENCE (как структура), по мотивам STRUCTURE из ctypes
##
##    ежели чего не хватает - добавляйте :)
##
##  - tag должен помещаться в 1 байт
##
## Да, я знаю про pyasn1 ( https://pypi.python.org/pypi/pyasn1 , http://snmplabs.com/pyasn1/ ,  http://snmplabs.com/pyasn1/ )
## но вижу некоторые препятствия для использования:
## - pyasn1 находится в разработке - скажем, находящая в репозитории alt linux версия не совместима
##   с опубликованной в PyPI, т.е. для использования pyasn1 придётся таскать с собой "свою" версию pyasn1.
##   самому патчить и пр., а я не хочу.
## - pyasn1 делает значительно больше чем мне нужно (BER/CER/DER) и имеет значительный объём (раз в 10 больше).
## - pyasn1 не показалась офигительно удобной. Мне нравится моё решение :)
##
## enjoy!
## прммеры использования в конце модуля.
##
## ещё читать:
##    https://ru.wikipedia.org/wiki/X.690
##    http://www.itu.int/ITU-T/studygroups/com17/languages/X.690-0207.pdf
##
#############################################################################

__all__ = ( 'Asn1Error', 'Asn1Base', 'Asn1BitString', 'Asn1OctetString', 'Asn1Oid', 'Asn1Sequence', 'Asn1Structure' )


class Asn1Error(Exception):
    pass


class EncBuffer:
    u'''Буфер для кодирования.
        Важная особенность реализации - запись должна производиться "с хвоста".
        Мотивирую такое решение тем, что длина префиксуюет содержание и сама имеет переменную длину
      '''
    UNIT = 128

    def __init__(self):
        self.__buffer = bytearray()
        self.__pos = 0 # последняя записанная позиция


    def __alloc(self, size):
        # добавляем в голову
        delta = size - self.__pos
        if delta>0:
            delta = ( delta + self.UNIT - 1) // self.UNIT * self.UNIT
            self.__buffer[:0] = bytearray(delta)
            self.__pos += delta


    def writeByte(self, byte):
        if self.__pos == 0:
            self.__alloc(self.UNIT)
        self.__pos -= 1
        self.__buffer[self.__pos] = byte


    def writeBytes(self, bytes):
        countBytes = len(bytes)
        if self.__pos < countBytes:
            self.__alloc(countBytes)
        self.__buffer[self.__pos - countBytes: self.__pos] = bytes
        self.__pos -= countBytes


    def anchor(self):
        return len(self.__buffer) - self.__pos


    def dist(self, anchor):
        return self.anchor() - anchor


    def data(self):
        return self.__buffer[self.__pos:]



class DecBuffer:
    def __init__(self, data):
        self.__buffer   = bytearray(data)
        self.__pos      = 0 # первая необработанная позиция
        self.__barrier  = len(self.__buffer)
        self.__barriers = []


    def isEmpty(self):
        return self.__pos == self.__barrier


    def peekByte(self):
        assert self.__pos < self.__barrier
        return self.__buffer[self.__pos]


    def readByte(self):
        assert self.__pos < self.__barrier
        result = self.__buffer[self.__pos]
        self.__pos += 1
        return result


    def readBytes(self, countBytes):
        if self.__pos+countBytes > self.__barrier:
            raise Asn1Error('no enough data to read')
        result = self.__buffer[self.__pos : self.__pos + countBytes]
        self.__pos += countBytes
        return result


    def readToBarrier(self):
        return self.readBytes(self.__barrier-self.__pos)


    def setBarrier(self, offset):
        self.__barriers.append(self.__barrier)
        self.__barrier = min(self.__barrier, self.__pos + offset)


    def restoreBarrier(self):
        self.__barrier = self.__barriers.pop()



class Unparsed:
    def __init__(self, value=None):
        self.value = value


    def __repr__(self):
        return 'Unparsed(h"%s")' % self.value.encode('hex') if self.value is not None else 'Unparsed()'


    def encodeToBuffer(self, encBuffer):
        assert isinstance(self.data, (bytearray, bytes))
        encBuffer.writeBytes( self.value )


    def decodeFromBuffer(self, decBuffer):
        self.value = bytes(decBuffer.readToBarrier())



class Asn1Base(object):
    u'''Базовый класс для различных классов элементов
    '''

    # в наследниках обычно должен быть определён tag
    mapTagToItemClass = {}

    def __init__(self):
        self.tag = type(self).tag
        self.optional = False


    def encode(self):
        encBuffer = EncBuffer()
        self.encodeToBuffer(encBuffer)
        return bytes(encBuffer.data())


    @classmethod
    def decode(cls, data):
       decBuffer = DecBuffer(data)
       result = cls.decodeFromBuffer(decBuffer)
#       assert decBuffer.isEmpty()
       return result


    def encodeLenAndTag(self, encBuffer, itemLen):
        self.encodeLen(encBuffer, itemLen)
        encBuffer.writeByte(self.tag)


    @staticmethod
    def encodeLen(encBuffer, itemLen):
        if itemLen < 0:
            raise Asn1Error('itemLen must be non negative')
        if itemLen > 16777216: # 2**24
            raise Asn1Error('itemLen too big')

        if itemLen <= 127:
            encBuffer.writeByte(itemLen)
        else:
            cnt = 0
            while itemLen>0:
                itemLen, rest = divmod(itemLen, 256)
                encBuffer.writeByte(rest)
                cnt += 1

            assert cnt <= 127
            encBuffer.writeByte(0x80 + cnt)


    @classmethod
    def decodeFromBuffer(cls, decBuffer):
       tag = decBuffer.peekByte()
       itemClass = cls.mapTagToItemClass.get(tag, Unparsed)
       result = itemClass()
       result.decodeFromBuffer(decBuffer)
       return result


    def decodeTagAndLen(self, decBuffer):
        tag = decBuffer.readByte()
        assert tag == self.tag
        return self.decodeLen(decBuffer)


    @staticmethod
    def decodeLen(decBuffer):
        b = decBuffer.readByte()
        if b <= 127:
            return b
        cnt = b - 0x80
        if cnt <= 0:
            raise Asn1Error('can not decode itemLen')
        itemLen = 0
        while cnt>0:
            b = decBuffer.readByte()
            itemLen = itemLen*256 + b
            cnt -= 1
        return itemLen


class Asn1BitString(Asn1Base):
    tag = 0x03

    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, (bytearray, bytes)):
            value = (0, value)
        else:
            assert isinstance(value, tuple) and len(value) == 2 and 0<=value[0]<=7 and isinstance(value[1], (bytearray, bytes))
        self.value = value


    def __repr__(self):
        return 'Asn1BitString((%d, h"%s"))' % (self.value[0], self.value[1].encode('hex')) if self.value is not None else 'Asn1BitString()'


    def encodeToBuffer(self, encBuffer):
        assert isinstance(self.value, (tuple))
        assert isinstance(self.value[1], (bytearray, bytes))
        encBuffer.writeBytes( self.value[1] )
        encBuffer.writeByte( self.value[0] )
        self.encodeLenAndTag( encBuffer, 1+len(self.value[1]) )


    def decodeFromBuffer(self, decBuffer):
        dataLen = self.decodeTagAndLen(decBuffer)
        assert dataLen > 0
        skipBits = decBuffer.readByte()
        valBits  =  bytes(decBuffer.readBytes(dataLen-1))
        self.value = skipBits, valBits


class Asn1OctetString(Asn1Base):
    tag = 0x04

    def __init__(self, value=None):
        assert value is None or isinstance(value, (bytearray, bytes))
        self.value = value

    def __repr__(self):
        return 'Asn1OctetString(h"%s")' % self.value.encode('hex') if self.value is not None else 'Asn1OctetString()'


    def isEmpty(self):
        return self.value is None


    def encodeToBuffer(self, encBuffer):
        assert isinstance(self.value, (bytearray, bytes))
        encBuffer.writeBytes( self.value )
        self.encodeLenAndTag( encBuffer, len(self.value) )


    def decodeFromBuffer(self, decBuffer):
        dataLen = self.decodeTagAndLen(decBuffer)
        self.value = bytes( decBuffer.readBytes(dataLen)  )



class Asn1Oid(Asn1Base):
    tag = 0x06

    def __init__(self, value=None):
        self.value = value


    def __repr__(self):
        return 'Asn1Oid(%r)' % self.value


    def isEmpty(self):
        return self.value is None


    def encodeToBuffer(self, encBuffer):
        assert isinstance(self.value, bytes)

        anchor = encBuffer.anchor()
        sids = [ int(sid) for sid in self.value.split('.') ]
#        print repr(self.value), sids
        assert len(sids)>2
        assert 0<=sids[0]<=2
        assert 0<=sids[1]
        sids[1] += sids[0]*40
        del sids[0]

        for sid in reversed(sids):
            assert sid >= 0
            if sid <= 127:
                encBuffer.writeByte(sid)
            else:
                add = 0
                while sid > 0:
                    sid, rem = divmod(sid, 128)
                    encBuffer.writeByte(add + rem)
                    add = 128

        self.encodeLenAndTag( encBuffer, encBuffer.dist(anchor) )


    def decodeFromBuffer(self, decBuffer):
        dataLen = self.decodeTagAndLen(decBuffer)
        sids = []
        sid = 0
        while dataLen:
            sidByte = decBuffer.readByte()
            sid = sid*128 + (sidByte & 0x7F)
            if sidByte <= 127:
                if not sids:
                    sid1, sid2 = divmod(sid, 40)
                    if sid1>2:
                        sid2 = (sid1-2)*40 + sid2
                        sid1 = 2
                    sids.append(sid1)
                    sids.append(sid2)
                else:
                    sids.append(sid)
                sid = 0
            dataLen -= 1
        assert sid == 0 # последний sid разобран
        self.value = '.'.join('%d' % sid for sid in sids)


class Asn1Sequence(Asn1Base):
    tag = 0x30

    def __init__(self, value=None):
        self.value=value


    def __repr__(self):
        return 'Asn1Sequence([' + ', '.join( repr(item) for item in self.value ) + '])'


    def isEmpty(self):
        return self.value is None


    def encodeToBuffer(self, encBuffer):
        assert self.value is not None
        anchor = encBuffer.anchor()
        for item in reversed(self.value):
            item.encodeToBuffer(encBuffer)
        self.encodeLenAndTag( encBuffer, encBuffer.dist(anchor) )


    def decodeFromBuffer(self, decBuffer):
        dataLen = self.decodeTagAndLen(decBuffer)
        items = []
        decBuffer.setBarrier(dataLen)
        while not decBuffer.isEmpty():
            item = Asn1Base.decodeFromBuffer(decBuffer)
            items.append(item)
        decBuffer.restoreBarrier()
        self.value = items



class Asn1Structure(Asn1Base):
    tag = 0x30
    _fields_ = None


    def __init__(self):
        assert( self._fields_ )

        Asn1Base.__init__(self)
        Asn1Base.__setattr__(self, '_values_', None)
        Asn1Base.__setattr__(self, '_mapNameToValue_', None)
        self._buildValues()
#        self.value = self._values_


    def _buildValues(self):
        values = []
        mapNameToValue = {}
        for fieldDescr in self._fields_:
            fieldName = fieldDescr['name']
            fieldType = fieldDescr['type']
            contextSpecificTag = fieldDescr.get('context-specific-tag', None)
            optional  = fieldDescr.get('optional', False)
            v = fieldType()
            if contextSpecificTag is not None:
                assert 0<=contextSpecificTag<=30
                v.tag = (v.tag&0x20) | contextSpecificTag | 0xA0
            v.optional = optional
            mapNameToValue[fieldName] = v
            values.append(v)
        Asn1Base.__setattr__(self, '_values_', values)
        Asn1Base.__setattr__(self, '_mapNameToValue_', mapNameToValue)


    def __getattr__(self, name):
#        print '__getattr__(%r)' % name
        if name in self._mapNameToValue_:
            v = self._mapNameToValue_[name]
            if isinstance(v, Asn1Structure):
                return v
            else:
                return v.value
        else:
            print repr(type(self)), self._mapNameToValue_.keys(), self._fields_



    def __setattr__(self, name, value):
#        print '__setattr__(%r)=%r ' % (name, value)
        if name in ( 'tag', 'optional', 'value'):
            Asn1Base.__setattr__(self, name, value)
        else:
            v = self._mapNameToValue_[name]
            if isinstance(v, Asn1Structure):
                assert isinstance(value, Asn1Structure)
                assert value._fields_ == v._fields_
                idx = self._values_.index(v)
                self._mapNameToValue_[name] = value
                self._values_[idx] = value
            else:
                v.value = value


    def __repr__(self):
        return 'Asn1Sequence(' + ', '.join( '%s=%s' % ( self._fields_[i]['name'], repr(self._values_[i])) for i in range(len(self._fields_))) + ')'


    def isEmpty(self):
        return all( v.isEmpty() for v in self._values_ )


    def encodeToBuffer(self, encBuffer):
        anchor = encBuffer.anchor()
        for item in reversed(self._values_):
            if not item.optional or not item.isEmpty():
                item.encodeToBuffer(encBuffer)
        self.encodeLenAndTag( encBuffer, encBuffer.dist(anchor) )


    def decodeFromBuffer(self, decBuffer):
        dataLen = self.decodeTagAndLen(decBuffer)
        decBuffer.setBarrier(dataLen)
        i = 0
        while not decBuffer.isEmpty() and i < len(self._fields_):
            nextTag = decBuffer.peekByte()
            v = self._values_[i]
#            fd = self._fields_[i]
#            print repr(type(self)), i, fd, hex(v.tag)
            if nextTag == v.tag:
                v.decodeFromBuffer(decBuffer)
                i += 1
            elif v.optional:
                v.value = None
                i += 1
        while i < len(self._fields_):
            v = self._values_[i]
#            fd = self._fields_[i]
#            print fd
            if v.optional:
                v.value = None
                i += 1
            else:
               assert v.optional
        assert decBuffer.isEmpty()
        decBuffer.restoreBarrier()


    @classmethod
    def decode(cls, data):
       decBuffer = DecBuffer(data)
       result = cls()
       result.decodeFromBuffer(decBuffer)
       assert decBuffer.isEmpty()
       return result



for cls in ( Asn1Sequence, Asn1Oid, Asn1OctetString, Asn1BitString):
    Asn1Base.mapTagToItemClass[cls.tag] = cls



if __name__ == '__main__':

    for oidStr, oidEncoded in ( ('1.2.643.2.2.31.1', '06072A850302021F01'.decode('hex')),
                                ('1.2.643.2.2.19',   '06062A8503020213'.decode('hex')),
                                ('1.2.643.2.2.36.0', '06072A850302022400'.decode('hex')),
                                ('1.2.643.2.2.30.1', '06072A850302021E01'.decode('hex')),
                                ('2.999.0.0.1',      '06058837000001'.decode('hex')),
                              ):
        # print oidStr, oidEncoded.encode('hex')
        assert Asn1Oid(oidStr).encode() == oidEncoded
        assert isinstance( Asn1Base.decode(oidEncoded), Asn1Oid)
        # print Asn1Base.decode(oidEncoded).value, oidStr
        assert Asn1Base.decode(oidEncoded).value == oidStr
        # print 'oid test ok'


    for octetStr, Asn1OctetStringEncoded in ( ( '',       '0400'.decode('hex')),
                                          ( 'x',      '040178'.decode('hex')),
                                          ( 'x'*127,  ('047F' + '78'*127).decode('hex')),
                                          ( 'x'*128,  ('048180' + '78'*128).decode('hex')),
                                          ( 'x'*9999, ('0482270F' + '78'*9999).decode('hex')),
                                        ):

        #print bytes(Asn1OctetString(octetStr).encode()).encode('hex')
        #print Asn1OctetStringEncoded.encode('hex')
        assert bytes(Asn1OctetString(octetStr).encode()) == Asn1OctetStringEncoded
        assert isinstance( Asn1Base.decode(Asn1OctetStringEncoded), Asn1OctetString)
        assert Asn1Base.decode(Asn1OctetStringEncoded).value == octetStr
        #print 'octet string test ok'

    assert bytes(Asn1BitString((3, 'x')).encode()) == '03020378'.decode('hex')
    bs = Asn1Base.decode('03020378'.decode('hex'))
    assert isinstance(bs, Asn1BitString)
    assert bs.value == (3, 'x')

    assert bytes(Asn1Sequence( [ Asn1Oid('2.999.0.0.1'), Asn1OctetString('x') ] ).encode()) == '300a06058837000001040178'.decode('hex')
    s = Asn1Base.decode('300a06058837000001040178'.decode('hex'))
    assert isinstance(s, Asn1Sequence)
    assert len(s.value) == 2
    assert isinstance(s.value[0], Asn1Oid)
    assert s.value[0].value == '2.999.0.0.1'
    assert isinstance(s.value[1], Asn1OctetString)
    assert bytes(s.value[1].value) == 'x'

    class Gost28147_89_EncryptedKey( Asn1Structure ):
        _fields_ = ( { 'name': 'encryptedKey', 'type': Asn1OctetString },
                     { 'name': 'masKey',       'type': Asn1OctetString, 'context-specific-tag': 0, 'optional': True },
                     { 'name': 'macKey',       'type': Asn1OctetString }
                   )
    ek = Gost28147_89_EncryptedKey()
    ek.encryptedKey = 'x'
    ek.masKey       = 'y'
    ek.macKey       = 'z'
    assert bytes(ek.encode()) == '3009040178a0017904017a'.decode('hex')

    ek = Gost28147_89_EncryptedKey()
    ek.encryptedKey = 'x'
    ek.macKey       = 'z'
    assert bytes(ek.encode()) == '300604017804017a'.decode('hex')

    ek = Gost28147_89_EncryptedKey.decode( '3009040178a0017904017a'.decode('hex') )
    assert ek.encryptedKey == 'x'
    assert ek.masKey       == 'y'
    assert ek.macKey       == 'z'

    ek = Gost28147_89_EncryptedKey.decode( '300604017804017a'.decode('hex') )
    assert ek.encryptedKey == 'x'
    assert ek.masKey       == None
    assert ek.macKey       == 'z'

    print '-*- self-test passed -*-'
