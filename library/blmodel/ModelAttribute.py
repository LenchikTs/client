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
from PyQt4.QtCore import QVariant

from library.Utils import toVariant


class CBaseType(object):
    def toQVariantValue(self, value):
        if isinstance(value, QVariant):
            return value
        return toVariant(value)

    def fromQVariantValue(self, qvariantValue):
        raise NotImplementedError()


class CStringType(CBaseType):
    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return qvariantValue
        return unicode(qvariantValue.toString())


class CIntType(CBaseType):
    def __init__(self,  identifier=False):
        self._identifier = identifier

    def toQVariantValue(self, value):
        if isinstance(value, int):
            pass
        elif value is None and self._identifier:
            pass
        elif isinstance(value, QVariant):
            value = value.toInt()[0]
        else:
            raise ValueError()

        if not self._identifier:
            return CBaseType.toQVariantValue(self, value)

        return CBaseType.toQVariantValue(self, value or None)

    def fromQVariantValue(self, qvariantValue):
        if isinstance(qvariantValue, QVariant):
            result = qvariantValue.toInt()[0]
        elif isinstance(qvariantValue, int):
            result = qvariantValue
        elif qvariantValue is None and self._identifier:
            result = None
        else:
            raise ValueError()

        if not self._identifier:
            return result

        return result or None


class CBooleanType(CBaseType):
    def toQVariantValue(self, value):
        if isinstance(value, QVariant):
            value = value.toInt()[0]
        else:
            assert isinstance(value, (int, bool))

        value = int(bool(value))

        return toVariant(value)

    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return bool(qvariantValue)
        return bool(qvariantValue.toInt()[0])


class CDoubleType(CBaseType):
    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return qvariantValue
        return qvariantValue.toDouble()[0]


class CDateType(CBaseType):
    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return qvariantValue
        return qvariantValue.toDate()


class CTimeType(CBaseType):
    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return qvariantValue
        return qvariantValue.toTime()


class CDateTimeType(CBaseType):
    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return qvariantValue
        return qvariantValue.toDateTime()


class CRefType(CBaseType):
    def fromQVariantValue(self, qvariantValue):
        if not isinstance(qvariantValue, QVariant):
            return qvariantValue

        value, status = qvariantValue.toInt()
        if not (value and status):
            return None
        return value


class CClassAttribute(object):
    def __init__(self, attribute):
        self._attribute = attribute
        self._table = QtGui.qApp.db.table(attribute.owner.tableName)

    @property
    def attribute(self):
        return self._attribute

    @property
    def attributeType(self):
        return self._attribute.attributeType

    @property
    def name(self):
        return self._attribute.name

    @property
    def fullName(self):
        return self._table[self.name].name()

    def getValueFromRecord(self, record):
        qvariantValue = record.value(self.name)
        return self.attributeType.fromQVariantValue(qvariantValue)

    def _validateOther(self, other):
        if isinstance(other, CClassAttribute):
            other = self._table[other.name]
        return other

    def __eq__(self, other):
        return self._table[self.name].eq(self._validateOther(other))

    def __ne__(self, other):
        return self._table[self.name].ne(self._validateOther(other))

    def __ge__(self, other):
        return self._table[self.name].ge(self._validateOther(other))

    def __gt__(self, other):
        return self._table[self.name].gt(self._validateOther(other))

    def __le__(self, other):
        return self._table[self.name].le(self._validateOther(other))

    def __lt__(self, other):
        return self._table[self.name].lt(self._validateOther(other))

    def inlist(self, other):
        return self._table[self.name].inlist(self._validateOther(other))

    def notInlist(self, other):
        return self._table[self.name].notInlist(self._validateOther(other))


class CAttribute(object):
    def __init__(self, name=None, attributeTypeClass=None, validator=None):
        self._name = name
        self._validator = validator
        self._attributeType = self._initAttributeTypeCls(attributeTypeClass)
        self._owner = None
        self._events = {}

    def _initAttributeTypeCls(self, attributeTypeClass):
        return attributeTypeClass()

    def copy(self):
        cls = type(self)
        initKwargs = self._initKwargs()
        return cls(**initKwargs)

    def _initKwargs(self):
        return {
            'name': self._name,
            'attributeTypeClass': type(self._attributeType),
            'validator': self._validator
        }

    def __str__(self):
        return '.'.join([self._owner.tableName, self._name])

    def listen(self, event):
        def wrapper(slot):
            self._events.setdefault(event, []).append(slot.func_name)
            return slot
        return wrapper

    @property
    def attributeType(self):
        return self._attributeType

    @property
    def owner(self):
        return self._owner

    @property
    def name(self):
        return self._name

    def _call_slots(self, instance, event, *args, **kwargs):
        for slot_name in self._events.get(event, []):
            slot = getattr(instance, slot_name, None)
            if not slot:
                continue

            slot(*args, **kwargs)

    def __set__(self, instance, value):
        if self._validator and not self._validator.validate(value):
            raise ValueError(value)

        recordValue = instance.getAttributeFromRecord(self)

        self._call_slots(instance, 'before_set', recordValue, value)

        instance.setAttributeToRecord(self, value)

        self._call_slots(instance, 'after_set', value, recordValue)

    def __get__(self, instance, owner):
        if instance is None:
            # Дернули как аттрибут класса, вернем обертку над объектом аттрибута
            return CClassAttribute(self)

        return instance.getAttributeFromRecord(self)

    def setValueToRecord(self, record, value):
        qvariantValue = self._attributeType.toQVariantValue(value)
        record.setValue(self._name, qvariantValue)

    def getValueFromRecord(self, record):
        qvariantValue = record.value(self._name)
        return self._attributeType.fromQVariantValue(qvariantValue)


class CStringValidator(object):
    def __init__(self, length=None):
        self._length = length

    def validate(self, value):
        if self._length and value:
            return self._length >= len(value)
        return True


class CStringAttribute(CAttribute):
    def __init__(self, name=None, length=None):
        super(CStringAttribute, self).__init__(name, CStringType)
        if length:
            self._validator = CStringValidator(length=length)

    def _initKwargs(self):
        return {
            'name': self._name,
            'length': self._validator._length
        }


class CIntAttribute(CAttribute):
    def __init__(self, name=None, identifier=False):
        self._identifier = identifier
        super(CIntAttribute, self).__init__(name, CIntType)

    def _initAttributeTypeCls(self, attributeTypeClass):
        return attributeTypeClass(self._identifier)

    def _initKwargs(self):
        return {
            'name': self._name,
            'identifier': self._identifier
        }


class CBooleanAttribute(CAttribute):
    def __init__(self, name=None):
        super(CBooleanAttribute, self).__init__(name, CBooleanType)

    def _initKwargs(self):
        return {
            'name': self._name,
        }

class CDoubleAttribute(CAttribute):
    def __init__(self, name=None):
        super(CDoubleAttribute, self).__init__(name, CDoubleType)

    def _initKwargs(self):
        return {
            'name': self._name,
        }

class CDateAttribute(CAttribute):
    def __init__(self, name=None):
        super(CDateAttribute, self).__init__(name, CDateType)

    def _initKwargs(self):
        return {
            'name': self._name,
        }


class CTimeAttribute(CAttribute):
    def __init__(self, name=None):
        super(CTimeAttribute, self).__init__(name, CTimeType)

    def _initKwargs(self):
        return {
            'name': self._name,
        }


class CDateTimeAttribute(CAttribute):
    def __init__(self, name=None):
        super(CDateTimeAttribute, self).__init__(name, CDateTimeType)

    def _initKwargs(self):
        return {
            'name': self._name,
        }

class CRefAttribute(CAttribute):
    def __init__(self, name=None):
        super(CRefAttribute, self).__init__(name, CRefType)

    def _initKwargs(self):
        return {
            'name': self._name,
        }
