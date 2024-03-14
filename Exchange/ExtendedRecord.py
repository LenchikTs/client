# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Гибрид QSqlRecord и словаря"""

from PyQt4.QtCore import QVariant

# ******************************************************************************

class CExtendedRecord(object):
    u"""Возвращает значения и QSqlRecord record, если они есть,
    иначе из указанного словаря params"""
    def __init__(self, record=None, params=None, debug=False):
        self._record = record
        self._params = params
        self._debug = debug

    def setRecord(self, record):
        u"""Установить новое значение поля record"""
        self._record = record


    def setParams(self, params):
        u"""Установить новое значение поля params"""
        self._params = params


    def value(self, name):
        u"""Возвращает поле по имени. Либо из записи, либо из словаря"""
        result = QVariant()

        if self._record and self._record.contains(name):
            result = self._record.value(name)
        elif self._params:
            if self._debug and not self._params.has_key(name):
                print('CExtendedRecord: unknown key "%s"' % name)

            result = self._params.get(name, QVariant())
        else:
            if self._debug:
                print('CExtendedRecord: unknown key "%s"' % name)

        return result


    def contains(self, field):
        result = False

        if self._record:
            result = self._record.contains(field)

        if self._params:
            result = result or self._params.has_key(field)

        return result


    def setValue(self, name, val):
        u'Сохраняет новое значение для поля'
        if self._record and self._record.contains(name):
            self._record.setValue(name, val)
        elif self._params:
            self._params[name] = val


    def isNull(self, field):
        result = True

        if self._record and self._record.contains(field):
            result = self._record.isNull(field)
        elif self._params:
            val = self._params.get(field)
            result = val is None or val == ''

        return result
