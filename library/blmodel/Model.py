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

from threading import RLock


from PyQt4 import QtGui, QtSql

from library.blmodel.ModelAttribute import (
    CAttribute, CIntAttribute, CDateTimeAttribute, CRefAttribute, CBooleanAttribute
)
from library.blmodel.ModelRelationship import CRelationship, CManyRelationship
from library.blmodel.Query import CQuery


class CMetaData(object):
    def __init__(self, blFileds, blObjAttributes, relationShips, manyRelationShips):
        self.__set_attribute_value__('fieldNames', list(blFileds.keys()))
        self.__set_attribute_value__('attributes', list(blObjAttributes.keys()))
        self.__set_attribute_value__('relationShipNames', list(relationShips.keys()))
        self.__set_attribute_value__('manyRelationShipNames', list(manyRelationShips.keys()))

    def __set_attribute_value__(self, attrName, value):
        self.__dict__[attrName] = value

    def __setattr__(self, key, value):
        raise NotImplementedError()


class CDataRegister(object):
    def __init__(self):
        self._metaData = {}
        self._mapClasses = {}
        self._mapTables = {}
        self._lock = RLock()

    def set(self, cls, attributes_keys):
        # Так как инициализация мета данных происходит по требованию, данные могут подгружаться в разных потоках
        # а бизнес модели связываются через атрибуты внешних ключей и могут быть попытки паралельной
        # загрузки одной модели. Поэтому инициализация реализована под reentrant lock.

        assert cls.tableName not in self._metaData, \
            "Duplicate table %s defenition: mapper %s " % (cls.tableName, cls.__name__)
        assert cls.__name__ not in self._mapClasses, \
            "Duplicate mapper %s defenition: table %s " % (cls.__name__, cls.tableName)

        self._lock.acquire()
        try:
            blobjFields = {}
            blobjAttributes = {}
            relationShips = {}
            manyRelationShips = {}
            for attribute_key in attributes_keys:
                attr = cls.__dict__[attribute_key]
                if isinstance(attr, CAttribute):
                    blobjAttributes[attribute_key] = attr
                elif isinstance(attr, CRelationship):
                    relationShips[attribute_key] = attr
                elif isinstance(attr, CManyRelationship):
                    manyRelationShips[attribute_key] = attr

            for name, attr in blobjAttributes.items():
                attr._owner = cls
                if not attr._name:
                    attr._name = name
                blobjFields[attr._name] = attr

            meta = CMetaData(blobjFields, blobjAttributes, relationShips, manyRelationShips)

            self._metaData[cls.tableName] = meta
            self._mapTables[cls.tableName] = cls
            self._mapClasses[cls.__name__] = cls
            cls.__init_meta__()
        finally:
            self._lock.release()

    def getMeta(self, tableName):
        self._lock.acquire()
        try:
            return self._metaData[tableName]
        finally:
            self._lock.release()

    def getClassByTable(self, tableName):
        self._lock.acquire()
        try:
            return self._mapTables[tableName]
        finally:
            self._lock.release()

    def getClassByName(self, className):
        self._lock.acquire()
        try:
            return self._mapClasses[className]
        finally:
            self._lock.release()


class CModelMetaType(type):
    register = CDataRegister()

    def __new__(mcs, name, bases, attributes):
        _attributes = mcs.__propagateAttributes(bases)
        _attributes.update(attributes)

        cls = type.__new__(mcs, name, bases, _attributes)
        if cls.tableName is not None:
            mcs.register.set(cls, _attributes.keys())
        return cls

    @property
    def Table(cls):
        return QtGui.qApp.db.table(cls.tableName)

    @property
    def FieldsList(cls):
        return [
            '.'.join([cls.tableName, fieldName])
            for fieldName in CModelMetaType.register._metaData[cls.tableName].fieldNames
        ]

    @property
    def RelationShipList(cls):
        return CModelMetaType.register._metaData[cls.tableName].relationShipNames

    @property
    def ManyRelationShipList(cls):
        return CModelMetaType.register._metaData[cls.tableName].manyRelationShipNames

    @classmethod
    def __propagateAttributes(mcs, bases):
        attributes = {}
        for base in bases[::-1]:
            for k, v in base.__dict__.items():
                if isinstance(v, CAttribute):
                    attributes[k] = v.copy()
        return attributes


class CBLObjectState(object):
    __slots__ = ('_blobject', '_dirty', '_attributeStates')
    
    def __init__(self, blobject):
        self._blobject = blobject
        self._dirty = False
        self._attributeStates = {}

    @property
    def dirty(self):
        return self._dirty

    def setDirty(self, attribute):
        self._dirty = True
        self._attributeStates[attribute.name] = True


class CBaseModel(object):
    """
        Базовый объект бизнес логики.
    """

    __metaclass__ = CModelMetaType

    __blobjectmeta__ = None
    __origin__ = None
    __originRecord__ = None

    tableName = None

    def __init__(self, record=None):
        self._table = self.getTable()
        self._record = record or self._newRecord()
        self._state = CBLObjectState(self)
        self._relationShips = {}
        self._manyRelationShips = {}

    def getOrigin(self):
        return self.__origin__ or self

    def makeCopy(self, new=False):
        return self.copyFrom(self, new=new)

    def mergeIntoOrigin(self):
        assert self.__origin__
        self.__origin__._updateByRecord(self._record)

    @classmethod
    def copyFrom(cls, item, new=False):
        return cls._copyFrom(item, new)

    @classmethod
    def _copyFrom(cls, item, new=False):
        assert isinstance(item, cls)

        newRecord = cls.Table.newRecord()
        record = item.getRecord()

        for i in range(record.count()):
            fieldName = record.fieldName(i)
            newRecord.setValue(fieldName, record.value(fieldName))

        newItem = cls(newRecord)
        if not new:
            newItem.__originRecord__ = record
            newItem.__origin__ = item
        return newItem


    @classmethod
    def query(cls, queryTable, fields='*', cond=None, limit=None):
        return CQuery(cls, queryTable, fields, cond, limit)

    @classmethod
    def getTable(cls):
        return QtGui.qApp.db.table(cls.tableName)

    @property
    def _dirty(self):
        return self._state.dirty

    def getRecord(self):
        if self._record is None:
            self._record = self._newRecord()
        return self._record

    def _newRecord(self):
        return self._table.newRecord()

    def setAttributeToRecord(self, attribute, value):
        dirty = attribute.getValueFromRecord(self.getRecord()) != attribute.attributeType.fromQVariantValue(value)
        attribute.setValueToRecord(self.getRecord(), value)
        if dirty:
            self._state.setDirty(attribute)

    def getAttributeFromRecord(self, attribute):
        return attribute.getValueFromRecord(self.getRecord())

    def update(self, data):
        if isinstance(data, QtSql.QSqlRecord):
            self._updateByRecord(data)
        elif isinstance(data, dict):
            self._updateByDict(data)
        else:
            raise ValueError('data must be QSqlRecord or dict type')
        return self

    @classmethod
    def _getValueFromRecord(cls, fieldName, record):
        return getattr(cls, fieldName).getValueFromRecord(record)

    def _updateByRecord(self, record):
        for attributeName in self.getMeta().attributes:
            fieldValue = self._getValueFromRecord(attributeName, record)
            setattr(self, attributeName, fieldValue)

    def _updateByDict(self, data):
        fieldNames = self.getMeta().fieldNames
        for attrName, attrValue in data.items():
            if not attrName in fieldNames:
                continue
            setattr(self, attrName, attrValue)

    # QSqlRecord back capability
    def value(self, indexOrName):
        return self._record.value(indexOrName)

    def setValue(self, indexOrName, value):
        if isinstance(indexOrName, int):
            fieldName = unicode(self._record.fieldName(indexOrName))
        else:
            fieldName = indexOrName

        attribute = getattr(self, fieldName)
        assert isinstance(attribute, CAttribute)

        self.setAttributeToRecord(attribute, value)

    @classmethod
    def __init_meta__(cls):
        if cls.__blobjectmeta__ is None:
            cls.__blobjectmeta__ = CModel.register.getMeta(cls.tableName)

    @classmethod
    def getMeta(cls):
        assert cls.__blobjectmeta__, 'bl object meta did not initialized'
        return cls.__blobjectmeta__

    @classmethod
    def get(cls, recordId):
        meta = cls.getMeta()
        record = QtGui.qApp.db.getRecord(cls.tableName, meta.fieldNames, recordId)
        if record:
            return cls().update(record)
        return None


class CModel(CBaseModel):
    id = CIntAttribute(identifier=True)


class CDocumentModel(CModel):
    createDatetime = CDateTimeAttribute()
    createPerson_id = CRefAttribute()
    modifyDatetime = CDateTimeAttribute()
    modifyPerson_id = CRefAttribute()
    deleted = CBooleanAttribute()
