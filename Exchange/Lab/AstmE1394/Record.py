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
## Базовый класс записи протокола ASTM E-1394
##
#############################################################################


from PyQt4.QtCore import QDate, QDateTime, QTime


class EWrongRecordType(Exception):
    def __init__(self, classRecordType, stringRecordType):
        Exception.__init__(self, 'The record type from a string "%s" does not match with an expected record type "%s"' % (stringRecordType, classRecordType))


class CRecord(object):
# Базовый класс для представления записей ASTM.
#
# Принято решение в производных классах описывать структуру полей,
# a все данные хранить в некотором представлении напоминающем
# представление в MUMPS: списки списков и простых значений, для
# хранения отдельных значений используется строковое представление
# (возможно None для пустых значений). Это решение мотивировано
# желанием упростить добавление или изменение типов записей и их
# атрибутов. Существует альтернативное, и возможно, более
# производительное решение: каждый тип записи имеет своё описание
# как python class и в силу этого свою реализацию
# сериализации/десериализации. Меня "укачивает" при обсуждении
# подобной возможности. hl7 имеет подобную структуру записей, и
# поэтому есть надежда что что достижения в этой части ещё
# пригодятся.
#
#    Структура описывается следующим образом:
#    structure = { # имя            индекс   python -тип значения
#                   'fieldName' : ( (1,),    unicode),
#                   'd1'        : ( (2,),    int),
#                   'lastName'  : ( (3,0,0), unicode),
#                   'firstName' : ( (3,0,1), unicode),
#                   'patrName'  : ( (3,0,2), unicode),
#                }
    structure = {}

    def __init__(self):
        # _storage: это список списков
        object.__setattr__(self, '_storage', [])
        if hasattr(type(self), 'recordType'):
            self.__setattr__('recordType', type(self).recordType)


    @classmethod
    def getIndex(cls, attr):
        # получить индекс атрибута в self._storage
        # в силу принятого решения индекс оказывается вектором
        index = cls.structure[attr][0]
        return index if isinstance(index, (list, tuple)) else [index]


    @classmethod
    def getType(cls, attr):
        # получить python тип значения
        return cls.structure[attr][1]


    @classmethod
    def convertScalarAttrValueToString(cls, type_, value):
        if value is None:
            return value
        if type_ in (str, unicode):
            return value if isinstance(value, basestring) else unicode(value)
        elif type_ in (int, long, float):
            return str(value)
        elif type_ is QDate:
            return str(value.toString('yyyyMMdd'))
        elif type_ is QDateTime:
            return str(value.toString('yyyyMMddhhmmss'))
        elif type_ is QTime:
            return str(value.toString('hhmmss'))
        else:
            assert False, '"%s"unknown type of attribute' % repr(type_)


    @classmethod
    def convertAttrValueToString(cls, type_, value):
        if isinstance(value, (list, tuple)):
            return [cls.convertAttrValueToString(type_, x) for x in value]
        else:
            return cls.convertScalarAttrValueToString(type_, value)


    @classmethod
    def convertScalarStringToAttrValue(cls, type_, value):
        if type_ in (str, unicode) or value is None:
            return value
        elif type_ in (int, long, float):
            return type_(value) if value else None
        elif type_ is QDate:
            return QDate.fromString(value, 'yyyyMMdd')
        elif type_ is QDateTime:
            return QDateTime.fromString(value, 'yyyyMMddhhmmss')
        elif type_ is QTime:
            return QTime.fromString(value, 'hhmmss')
        else:
            assert False, '"%s"unknown type of attribute' % repr(type_)


    @classmethod
    def convertStringToAttrValue(cls, type_, stringOrList):
        if isinstance(stringOrList, (list, tuple)):
            return [cls.convertStringToAttrValue(type_, x) for x in stringOrList]
        else:
            return cls.convertScalarStringToAttrValue(type_, stringOrList)


    def __setattr__(self, name, value):
        index = self.getIndex(name)
        strValue = self.convertAttrValueToString(self.getType(name), value)
        setData(self._storage, index, strValue)


    def __getattr__(self, name):
        index = self.getIndex(name)
        strValue = flatValue(getData(self._storage, index))
        return self.convertStringToAttrValue(self.getType(name), strValue)


    def __getitem__(self, name):
        return self.__getattr__(name)


    def __setitem__(self, name, value):
        self.__setattr__(name, value)


    def asString(self, delimiters, encoding='utf8'):
        escape = lambda string: astmEscape(string.encode(encoding, 'replace'), delimiters)
        return convertStorageToString(self._storage, delimiters[:-1], escape)


    def setString(self, string, delimiters, encoding='utf8'):
        if hasattr(type(self), 'recordType') and type(self).recordType != string[:1]:
            raise EWrongRecordType(type(self).recordType, string[:1])
        unescape = lambda string: astmUnescape(string, delimiters).decode(encoding)
        object.__setattr__(self,
                           '_storage',
                           convertStringToStorage(string, delimiters[:-1], unescape)
                          )


# "механика" ##############################################################################
# есть стремление сделать эти методы статическими в классе, но
# необходимсть явно указывать имя класса в рекурсии удручает.

def setData(storage, index, value):
    # поместить в хранилище по заданонму индексу указанное значение
    index, subIndex = index[0], index[1:]
    if len(storage)<=index:
        storage.extend(['']*(index-len(storage)+1))
    if not subIndex:
        storage[index] = value
    else:
        subStorage = storage[index]
        if not isinstance(subStorage, list):
            subStorage = list(subStorage) if isinstance(subStorage, tuple) else [subStorage]
            storage[index] = subStorage
        setData(subStorage, subIndex, value)


def getData(storage, index):
    # получить значение из хранилища по заданному индексу
    index, subIndex = index[0], index[1:]
    if len(storage)<=index:
        return None
    if not subIndex:
        return storage[index]
    else:
        subStorage = storage[index]
        if not isinstance(subStorage, (list, tuple)):
            subStorage = [subStorage]
        return getData(subStorage, subIndex)


def flatValue(value):
    # в принятом методе хранения данных нет принципиальной разницы между
    # 'val', ['val'] или [['val']]
    # это связано с тем, что когда мы видим в записи |val|
    # мы не можем сказать - val это просто значение атрибута,
    # первый и единственный элемент сложного атрибута
    # или первый и единственный экземпляр повторяемого значения
    # первого и единственного элемента сложного атрибута.
    flatten = value
    while isinstance(flatten, (list, tuple)):
        if len(flatten) == 1:
            flatten = flatten[0]
        else:
            return value
    return flatten


def convertStorageToString(storage, delimiters, escape):
    delimiter, subDelimiters = delimiters[:1], delimiters[1:]
    return delimiter.join( '' if part is None else
                           escape(part) if isinstance(part, basestring) else
                           convertStorageToString(part, subDelimiters, escape)
                           for part in storage
                         )


def convertStringToStorage(string, delimiters, unescape):
    delimiter, subDelimiters = delimiters[:1], delimiters[1:]
    result = string.split(delimiter)
    if subDelimiters:
        for i, part in enumerate(result):
            result[i] = flatValue(convertStringToStorage(part, subDelimiters, unescape))
    else:
        for i, part in enumerate(result):
            result[i] = unescape(part)
    return result


def astmEscape(string, delimiters, names='FSRE'):
    # delimiters это строка типа '|\\^&'
    # a names - это имена разделителей
    assert len(delimiters) == len(names) and len(delimiters) > 0 and names.find('E') >=0
    escape = delimiters[names.index('E')]

    def fltr(char):
        i = delimiters.find(char)
        if i >= 0:
            return '%s%s%s' % ( escape, names[i], escape)
        code = ord(char)
        if code<32 or code == 127: # or code == 255:
            return '%sX%02X%s' % ( escape, code, escape)
        return char
    return ''.join( fltr(char) for char in string )


def astmUnescape(string, delimiters, names='FSRE'):
    # delimiters это строка типа '|\\^&'
    # a names - это имена разделителей
    # эта реализация намеренно написана с избеганием выбрасывания исключений,
    # поскольку оператор скорее всего не сможет повлиять на источник данных непосредственно,
    # но есть надежда, что увидев «левые» символы догадается исправить.
    assert len(delimiters) == len(names) and len(delimiters) > 0 and names.find('E') >=0
    escape = delimiters[names.index('E')]

    result = ''
    pos = 0
    while True:
        start = string.find(escape, pos)
        stop  = string.find(escape, start+1) if start>=0 else -1
        if start<0 or stop<0:
            result += string[pos:]
            break
        result += string[pos:start]
        seq = string[start+1: stop]
        i = names.find(seq)
        if len(seq) == 1 and i>=0:
            result += delimiters[i]
        elif seq.startswith('X'):
            try:
                code = int(seq[1:], 16)
                result += chr(code)
            except:
                # ошибка. пусть будет как есть
                result += string[start:stop+1]
        elif seq == 'H': # &H& start highlighting text
            pass
        elif seq == 'N': # &N& normal text (end highlighting)
            pass
#        elif seq == '.br' #
#           result += '\n'
        else:
            # неизвестный код. пусть будет как есть
            result += string[start:stop+1]
        pos = stop+1
    return result



if __name__ == '__main__':
    class CTestRecord(CRecord):
        structure = {
                       'recordType': ( 0,       str),
                       'seqNo'     : ( 1,       int),
                       'greeting'  : ( 2,       unicode),
                       'age'       : ( 3,       int),
                       'lastName'  : ( (5,0,0), unicode),
                       'firstName' : ( (5,0,1), unicode),
                       'patrName'  : ( (5,0,2), unicode),
                    }
        recordType = 'T'

    r = CTestRecord()
    r.seqNo     = 1
    r.greeting  = 'hello'
    r.age       = 321
    r.lastName  = 'Ivanov'
    r.firstName = u'Ivan|\\^&:)'
#    r.patrName  = u'Иванович'
    r['patrName'] = u'Иванович'

    print r._storage
    print r.greeting, r.age, r.lastName, r.firstName, r.patrName
    s = r.asString('|\\^&', 'cp1251')
    print s

    r1 = CTestRecord()
    r1.setString(s, '|\\^&', 'cp1251')
    print r1.greeting, r1.age, r1.lastName, r1.firstName, r1.patrName
