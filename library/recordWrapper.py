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

from PyQt4.QtSql   import QSqlRecord

from library.abstract import abstract


def field(fieldName, variantToPyValue = None, pyValueToVariant = None):
    fieldName = intern(fieldName)
    if variantToPyValue:
        def getter(self):
            return variantToPyValue(self._getValueAsQVariant(fieldName))
    else:
        def getter(self):
            return self._getValueAsPyValue(fieldName)
    if pyValueToVariant:
        def setter(self, v):
            self._setValue(fieldName, pyValueToVariant(v))
    else:
        def setter(self, v):
            self._setValue(fieldName, v)
    return property(getter, setter)


class CSqlRecordWrapper(object):
    def __init__(self, record = None):
        self.setRecord(record or self.getEmptyRecord())
        self.isDirty = False


    def setRecord(self, record):
        self._record = record
        self._fieldIdx = {}
        for i in xrange(record.count()):
           self._fieldIdx[ intern(str(record.field(i).name())) ] = i

        self._recordSetValue = self._record.setValue
        self._recordValue    = self._record.value


    def getRecord(self):
        return self._record


    def clone(self):
        newRecord = QSqlRecord(self._record)
        newRecord.setNull('id')
        return type(self)(newRecord)


    def asDict(self):
        result = {}
        for fieldName, fieldIdx in self._fieldIdx.iteritems():
            v = self._recordValue(fieldIdx)
            result[fieldName] = None if v.isNull() else v.toPyObject()
        return result


    def setDict(self, d):
        for key, value in d.iteritems():
            if key in self._fieldIdx:
                self.setValue(key, value)


    @abstract
    def getEmptyRecord(self):
        pass


    # имитация поведения QSqlRecord
    def value(self, nameOrIndex):
        if isinstance(nameOrIndex, basestring):
            return self._recordValue(self._fieldIdx[nameOrIndex])
        else:
            return self._recordValue(nameOrIndex)


    def setValue(self, nameOrIndex, v):
        if isinstance(nameOrIndex, basestring):
            self._recordSetValue(self._fieldIdx[nameOrIndex], v)
        else:
            self._recordSetValue(nameOrIndex, v)
        self.isDirty = True


    def _getValueAsPyValue(self, fieldName):
        v = self._recordValue(self._fieldIdx[fieldName])
        return None if v.isNull() else v.toPyObject()


    def _getValueAsQVariant(self, fieldName):
        return self._recordValue(self._fieldIdx[fieldName])


    def _setValue(self, fieldName, v):
        self._recordSetValue(self._fieldIdx[fieldName], v)
        self.isDirty = True


    def __eq__(self, other):
        if isinstance(other, CSqlRecordWrapper):
            return self._record == other._record
        if other is None:
            return False
        return NotImplemented


    def __ne__(self, other):
        if isinstance(other, CSqlRecordWrapper):
            return self._record != other._record
        if other is None:
            return True
        return NotImplemented

    record = property(getRecord, setRecord)

# а ещё можно написать кеширующий вариант...
