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

from library.Utils import forceString


def _prepare_data_processor(model_class, fields):
    if not isinstance(model_class, (tuple, list)):
        if fields is None:
            fields = '*'
        return model_class, fields

    assert fields is None

    fields = []

    mc_helpers = {}

    for mc in model_class:
        fields_helpers = []
        for f in mc.FieldsList:
            field_as = "%s AS %s" % (f, f.replace('.', '_'))
            mc_attribute = f.split('.')[1]
            value_getter = lambda r: r.value(field_as)
            value_setter = lambda r, v: r.setValue(mc_attribute, v)
            fields.append(field_as)
            fields_helpers.append((value_getter, value_setter))
        mc_helpers[mc] = fields_helpers

    def process_record(record):
        result = []
        for mc in model_class:
            item = mc()
            newRecord = mc.getRecord()
            for value_getter, value_setter in mc_helpers[mc]:
                value_setter(newRecord, value_getter(record))
            result.append(item)
        return result

    return process_record, fields


class CQuery(object):
    def __init__(self, model_class, queryTable=None, fields=None, where='', order='', limit=None):
        self._process_record, self._fields = _prepare_data_processor(model_class, fields)
        self._queryTable = queryTable or model_class.Table
        self._where = where
        self._order = order
        self._limit = limit

    def orderBy(self, value):
        if not value:
            return self
        if not isinstance(self._order, (tuple, list)):
            order = [self._order] if self._order else []
        else:
            order = list(self._order)

        order.append(value)

        return CQuery(
            self._process_record, self._queryTable, self._fields, self._where, order, self._limit
        )

    def limit(self, limit):
        return CQuery(
            self._process_record, self._queryTable, self._fields, self._where, self._order, limit
        )

    def selectStmt(self):
        return QtGui.qApp.db.selectStmt(self._queryTable, self._fields, self._where, self._order, self._limit)

    def selectStmtGroupBy(self, group):
        return QtGui.qApp.db.selectStmtGroupBy(
            self._queryTable, self._fields, self._where, group, self._order, self._limit
        )

    def selectDistinctStmt(self):
        return QtGui.qApp.db.selectDistinctStmt(self._queryTable, self._fields, self._where, self._order, self._limit)

    def existsStmt(self):
        return QtGui.qApp.db.existsStmt(self._queryTable, self._where)

    def notExistsStmt(self, table, where):
        return QtGui.qApp.db.notExistsStmt(self._queryTable, self._where)

    def getSum(self):
        return QtGui.qApp.db.getSum(self._queryTable, self._fields, self._where)

    def getMax(self, maxCol='id'):
        return QtGui.qApp.db.getMax(self._queryTable, maxCol, self._where)

    def getMin(self, minCol='id'):
        return QtGui.qApp.db.getMin(self._queryTable, minCol, self._where)

    def getCount(self, countCol='1'):
        return QtGui.qApp.db.getCount(self._queryTable, countCol, self._where)

    def getDistinctCount(self, countCol='*'):
        return QtGui.qApp.db.getCount(self._queryTable, countCol, self._where)

    def getIdList(self, idCol='id'):
        return QtGui.qApp.db.getIdList(self._queryTable, idCol, self._where, self._order, self._limit)

    def getDistinctIdList(self, idCol=('id',)):
        return QtGui.qApp.db.getDistinctIdList(self._queryTable, idCol, self._where, self._order, self._limit)

    def getIdListGroupBy(self, idCol='id'):
        return QtGui.qApp.db.selectStmtGroupBy(self._queryTable, idCol, self._where, self._order, self._limit)

    def getRecordList(self):
        return QtGui.qApp.db.getRecordList(
            self._queryTable, self._fields, self._where, self._order, self._limit
        )

    def getRecordListGroupBy(self, group=''):
        return QtGui.qApp.db.getRecordListGroupBy(
            self._queryTable, self._fields, self._where, group, self._order, self._limit
        )

    def getList(self):
        return [self._process_record(r) for r in self.getRecordList()]

    def getFirst(self):
        result = self.limit(1).getList()
        if not result:
            return None
        return result[0]

    def getDistinctList(self):
        return self.getDistinctFieldValues(self._fields, self._process_record)

    def getDistinctStringValues(self, field):
        def formatter(record):
            return forceString(record.value(0))
        return self.getDistinctFieldValues(field, formatter)

    def getDistinctFieldValues(self, field, formatter):
        stmt = QtGui.qApp.db.selectDistinctStmt(self._queryTable, field, self._where, self._order, self._limit)
        query = QtGui.qApp.db.query(stmt)
        result = []
        while query.next():
            result.append(formatter(query.record()))
        return result

    @classmethod
    def save(cls, item):
        model = type(item)
        table = model.Table
        manyRelationShipList = model.ManyRelationShipList
        record = item.getRecord()
        result = QtGui.qApp.db.insertOrUpdate(table, record)

        for relationShipName in manyRelationShipList:
            key = getattr(model, relationShipName).key
            if key not in item._manyRelationShips:
                continue

            relationsList = getattr(item, relationShipName)
            if relationsList:
                idFieldName = getattr(model, relationShipName)._fieldNameId
                for relation in relationsList:
                    setattr(relation, idFieldName, result)
                    cls.save(relation)

        return result


    @classmethod
    def delete(cls, model, cond):
        if hasattr(model, 'deleted'):
            cls._mark_as_deleted(model, cond)
        else:
            cls._delete(model, cond)

    @staticmethod
    def _mark_as_deleted(model, cond):
        cond = QtGui.qApp.db.prepareWhere(cond)
        stmt = "UPDATE %s SET deleted = 1 %s" % (model.tableName, cond)
        query = QtGui.qApp.db.query(stmt)
        if query.first():
            record = query.record()
            return record.value(0).toInt()[0]
        else:
            return 0

    @staticmethod
    def _delete(model, cond):
        cond = QtGui.qApp.db.prepareWhere(cond)
        stmt = "DELETE FROM %s %s" % (model.tableName, cond)
        query = QtGui.qApp.db.query(stmt)
        if query.first():
            record = query.record()
            return record.value(0).toInt()[0]
        else:
            return 0
