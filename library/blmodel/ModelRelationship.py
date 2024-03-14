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

from library.blmodel.Query import CQuery

from library.CachedProperty import cached_property


class CBaseRelationship(object):
    def __init__(self, bl_model_class, fieldNameId, targetNameId=None):
        self.__bl_model_class = bl_model_class
        self._fieldNameId = fieldNameId
        self._targetNameId = targetNameId

    @cached_property
    def _bl_model_class(self):
        from library.blmodel.Model import CModelMetaType

        # Ленивая загрузка модели из кеша. Это если захочется сделать циклические связи
        if isinstance(self.__bl_model_class, basestring):
            bl_model_class = CModelMetaType.register.getClassByName(self.__bl_model_class)
            assert bl_model_class
        else:
            bl_model_class = self.__bl_model_class

        return bl_model_class

    @property
    def _key(self):
        return '.'.join([self._bl_model_class.tableName, self._fieldNameId])


class CRelationship(CBaseRelationship):
    def __get__(self, instance, owner):
        if not instance:
            return self

        if self._key in instance._relationShips.keys():
            return instance._relationShips[self._key]

        idValue = getattr(instance, self._fieldNameId)
        if not idValue:
            return None

        if self._targetNameId:
            db_name = getattr(self._bl_model_class, self._targetNameId).name
            cond = self._bl_model_class.Table[db_name].eq(idValue)
        else:
            idCol = self._bl_model_class.Table.idFieldName()
            cond = self._bl_model_class.Table[idCol].eq(idValue)

        record = QtGui.qApp.db.getRecordEx(self._bl_model_class.tableName, '*', where=cond)
        model = self._bl_model_class(record) if record else None
        instance._relationShips[self._key] = model
        return model

    def __set__(self, instance, value):
        if value is not None:
            assert isinstance(value, self._bl_model_class)

        instance._relationShips[self._key] = value
        if self._targetNameId:
            if value:
                setattr(value, self._targetNameId, getattr(instance, self._fieldNameId))
            setattr(instance, self._fieldNameId, getattr(instance, self._fieldNameId) if value else None)
        else:
            setattr(instance, self._fieldNameId, value.id if value else None)


class CManyRelationship(CBaseRelationship):
    def __get__(self, instance, owner):
        if not instance:
            return self

        if self._key in instance._manyRelationShips.keys():
            return instance._manyRelationShips[self._key]

        if instance.id:
            cond = getattr(self._bl_model_class, self._fieldNameId) == instance.id
            result = CQuery(self._bl_model_class, where=cond).getList()
        else:
            result = []

        instance._manyRelationShips[self._key] = result
        return result

    def __set__(self, instance, valueList):
        for value in valueList:
            assert isinstance(value, self._bl_model_class)

        instance._manyRelationShips[self._key] = valueList
        for value in valueList:
            setattr(value, self._fieldNameId, value.id if value else None)
