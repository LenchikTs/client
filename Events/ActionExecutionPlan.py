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

import datetime

import decimal


from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtCore import QTime, QDate, QDateTime

from library.Utils import forceDateTime, pyDate, forceInt, toVariant, forceDate, forceDouble



class ExecutionPlanException(Exception):
    pass


class CActionExecutionPlan(object):
    def __init__(self, action=None):
        self._action = action
        self._executionPlan = {}
        self._table = QtGui.qApp.db.table('Action_ExecutionPlan')


    def copy(self):
        result = {}
        for dk in self._executionPlan.keys():
            for tk in self._executionPlan[dk].keys():
                record = self._table.newRecord()
                source = self._executionPlan[dk][tk]

                for i in range(source.count()):
                    value = record.value(i)
                    fieldName = record.fieldName(i)
                    record.setValue(fieldName, value)

                result.setdefault(dk, {})[tk] = record

        ep = CActionExecutionPlan(self._action)
        ep._executionPlan = result
        return ep


    def set(self, executionPlan):
        if isinstance(executionPlan, CActionExecutionPlan):
            self._executionPlan = executionPlan._executionPlan
        else:
            self._executionPlan = executionPlan


    def bind(self, action):
        if self._action:
            raise ExecutionPlanException(
                u'Нельзя связывать с действием план выполнения который уже связан с действием. '
                u'Явно отвяжите план выполнения.'
            )

        self._action = action


    def unbind(self):
        self._action = None
        for timeDicts in self._executionPlan.values():
            for record in timeDicts.values():
                record.setValue('master_id', toVariant(None))


    def __nonzero__(self):
        return bool(self._executionPlan)


    def as_dict(self):
        return self._executionPlan

    # ##############################################################
    # Притворимся dict-ом, для обратной совместимости
    def get(self, key, *args):
        assert len(args) < 2
        default = args[0] if args else None
        return self._executionPlan.get(key, default)


    def setdefault(self, key, default):
        return self._executionPlan.setdefault(key, default)


    def pop(self, *args, **kwargs):
        return self._executionPlan.pop(*args, **kwargs)


    def __getitem__(self, item):
        return self._executionPlan[self._validateKey(item)]


    def __setitem__(self, key, value):
        self._executionPlan[self._validateKey(key)] = value


    def keys(self):
        return self._executionPlan.keys()


    def values(self):
        return self._executionPlan.values()


    def clear(self):
        self._executionPlan.clear()


    def update(self, executionPlan):
        if isinstance(executionPlan, CActionExecutionPlan):
            executionPlan = executionPlan.as_dict()
        self._executionPlan.update(executionPlan)


    def __iter__(self):
        return iter(self._executionPlan)


    def __contains__(self, key):
        return self._validateKey(key) in self._executionPlan


    def _validateKey(self, date):
        if isinstance(date, QDate):
            return date.toPyDate()
        return date

    # #################################################################

    def calcDosage(self):
        result = decimal.Decimal('0')
        for v in self._executionPlan.values():
            for r in v.values():
                result += decimal.Decimal(str(forceDouble(r.value('dosage'))))

        if result == decimal.Decimal('0'):
            return None
        return float(result)


    def load(self):
        actionId = self._action.getId()
        if not actionId:
            return

        db = QtGui.qApp.db
        stmt = db.selectStmt(self._table, '*', [self._table['master_id'].eq(actionId), self._table['deleted'].eq(0)])
        query = db.query(stmt)
        while query.next():
            executionPlanRecord = query.record()

            execDateTime = forceDateTime(executionPlanRecord.value('execDate'))
            execDate = pyDate(execDateTime.date())
            execTime = execDateTime.time()

            execTimeDict = self._executionPlan.setdefault(execDate, {})
            execTimeDict[execTime] = executionPlanRecord


    def _deleteUnbinded(self):
#        ids = set()

        for timeDicts in self._executionPlan.values():
            for record in timeDicts.values():
                if record.value('master_id'):
                    record.setValue('master_id', toVariant(None))


    def save(self):
        if not self._action:
            return self._deleteUnbinded()

        actionId = self._action.getId()
        if not actionId:
            return False

        actionRecord = self._action.getRecord()

        db = QtGui.qApp.db

        executionPlanIds = set()
        if self._executionPlan:
            tableActionExecutionPlan = db.table('Action_ExecutionPlan')

            for execDate, execTimeDict in self._executionPlan.items():
                # Это значит что открывали планировщие назначений по F2 в окне выбора действия F9
                # И заплонировали по дням и по времени
                if execTimeDict:
                    for execTime, planRecord in execTimeDict.items():
                        executionPlanId = self._saveExecutionPlanRecord(actionId, planRecord)
                        executionPlanIds.add(executionPlanId)
                else:
                    # Планирование назначений не открывали, но на основе
                    # Action свойств duration и periodicity был сформирован план по дням.
                    for _ in range(forceInt(actionRecord.value('aliquoticity')) or 1):
                        planRecord = tableActionExecutionPlan.newRecord()
                        planRecord.setValue('execDate', toVariant(execDate))
                        executionPlanId = self._saveExecutionPlanRecord(actionId, planRecord)
                        executionPlanIds.add(executionPlanId)

        condToDelete = [
            self._table['master_id'].eq(actionId)
        ]
        if executionPlanIds:
            condToDelete.append(self._table['id'].notInlist(executionPlanIds))

        db.deleteRecord(self._table, condToDelete)


    def _saveExecutionPlanRecord(self, actionId, record):
        record.setValue('master_id', toVariant(actionId))
        executionPlanId = QtGui.qApp.db.insertOrUpdate(self._table, record)
        record.setValue('id', toVariant(executionPlanId))
        return executionPlanId


    def minExecutionPlanTime(self):
        minEPDate = self.minExecutionPlanDate()
        if not minEPDate:
            return None
        return self.minExecutionPlanTimeByDate(minEPDate)


    def minExecutionPlanTimeByDate(self, date):
        if not self._executionPlan or not date in self._executionPlan:
            return None

        timeKeys = self._executionPlan[date].keys()

        if not timeKeys:
            return None

        _timeKeys = []
        for timeKey in timeKeys:
            r = self._executionPlan[date][timeKey]
            _timeKeys.append((timeKey, forceInt(r.value('idx'))))

        timeKeys = sorted(_timeKeys)

        return timeKeys[0][0]


    def minExecutionPlanDateTime(self):
        date = self.minExecutionPlanDate()
        if date is None:
            return None

        time = self.minExecutionPlanTimeByDate(date)
        time = time.toPyTime() if isinstance(time, QtCore.QTime) else time
        if time is None:
            return None

        return datetime.datetime.combine(date, time)


    def minExecutionPlanDate(self):
        if not self._executionPlan:
            return None

        return min(self._executionPlan.keys())


    def getActualDosage(self):
        date = self.minExecutionPlanDate()
        if not date:
            return None

        time = self.minExecutionPlanTimeByDate(date)
        if not time:
            return None

        r = self._executionPlan[date][time]
        if not r:
            return None

        if not isinstance(r, QtSql.QSqlRecord):
            return None

        return forceDouble(r.value('dosage'))


    def addExecutionPlanByAction(self):
        if self._executionPlan is None:
            return

        if not self._executionPlan:
            return self.updateExecutionPlanByAction()

        date = self.minExecutionPlanDate()
        if not date:
            return

        record = self._action.getRecord()

        aliquoticity = forceInt(record.value('aliquoticity')) or 1
        periodicity = forceInt(record.value('periodicity')) or 0
        ep = self._executionPlan[date]

        plannedEndDate = forceDateTime(record.value('plannedEndDate'))
        datetime = forceDateTime(self.minExecutionPlanDateTime())
        execDate = datetime
        execDate.setTime(QTime(0, 0))

        for idx in range(aliquoticity - len(ep)):
            planRecord = self._table.newRecord()
            planRecord.setValue('execDate', toVariant(execDate))
            planRecord.setValue('idx', toVariant(execDate))

            v = forceDouble(self._action.findDosagePropertyValue() if self._action.findDosagePropertyValue() is not None else 0)
            planRecord.setValue('dosage', toVariant(v))

            self.getActualDosage()
            ep[date][QTime(0, 0)] = planRecord

        execDate = execDate.addDays(periodicity + 1)

        while execDate <= plannedEndDate:
            dateKey = execDate.toPyDateTime().date()
            self._executionPlan[dateKey] = {}

            for idx in xrange(aliquoticity):
                planRecord = self._table.newRecord()
                planRecord.setValue('idx', toVariant(idx))
                planRecord.setValue('execDate', toVariant(execDate))
                v = forceDouble(self._action.findDosagePropertyValue() if self._action.findDosagePropertyValue() is not None else 0)
                planRecord.setValue('dosage', toVariant(v))

                self._executionPlan[dateKey][QTime(0, 0)] = planRecord

            execDate = execDate.addDays(periodicity + 1)

        for dk in self._executionPlan.keys():
            if forceDate(dk) > plannedEndDate.date():
                del self._executionPlan[dk]


    def updateExecutionPlanByAction(self, forceDuration=False):
        record = self._action.getRecord()

        self._executionPlan.clear()
        # Длительность
        duration = forceInt(record.value('duration'))

        # periodicity - это интервал. Сколько полных дней между назначениями
        periodicity = forceInt(record.value('periodicity'))

        # кратность
        aliquoticity = forceInt(record.value('aliquoticity')) or 1

        if not (duration >= 1 or aliquoticity > 1 or forceDuration):
            return

        begDate = forceDate(record.value('begDate'))
        plannedEndDate = begDate.addDays(duration - 1)

        execDate = begDate
        while execDate <= plannedEndDate:
            dateKey = pyDate(execDate)
            self._executionPlan[dateKey] = {}

            for idx in xrange(aliquoticity):
                planRecord = self._table.newRecord()
                planRecord.setValue('idx', toVariant(idx))
                planRecord.setValue('execDate', toVariant(execDate))
                v = forceDouble(self._action.findDosagePropertyValue() if self._action.findDosagePropertyValue() is not None else 0)
                planRecord.setValue('dosage', toVariant(v))

                self._executionPlan[dateKey][QTime(0, 0)] = planRecord

            execDate = execDate.addDays(periodicity + 1)


    def getDataForNewExecutionPlanAction(self, dt):
        executionPlan = self._executionPlan
        executionPlanKeys = executionPlan.keys()
        executionPlanKeys.sort()
        executionPlanBegDate = executionPlan.get(dt.date(), {})
        if not executionPlanBegDate:
            for keyDate in executionPlanKeys:
                executionPlanTimes = executionPlan.get(keyDate, {})
                if not executionPlanTimes:
                    # Это значит что действие не было еще сохранено
                    # и не было планировок по конкретному времени
                    dt = QDateTime(QDate(keyDate), QTime(0, 0))
                    break
                else:
                    executionPlanTimeKeys = executionPlanTimes.keys()
                    executionPlanTimeKeys.sort()
                    dt = QDateTime(QDate(keyDate), executionPlanTimeKeys[0])
                    break
        else:
            executionPlanBegDateKeys = executionPlanBegDate.keys()
            executionPlanBegDateKeys.sort()
            begTime = executionPlanBegDateKeys[0]

            dt = QDateTime(executionPlanKeys[0], begTime)

        return dt


    def getExecutionPlanForNewAction(self):
        newExecutionPlan = {}
        executionPlan = self._executionPlan
        if not executionPlan:
            return newExecutionPlan

        tableActionExecutionPlan = QtGui.qApp.db.table('Action_ExecutionPlan')

        executionPlanKeys = executionPlan.keys()
        executionPlanKeys.sort()

        currentDayKey = executionPlanKeys[0]

        timeDict = executionPlan[currentDayKey]
        timeKeys = timeDict.keys()

        # Сортируем по аремени и по idx если время одинаковое
        _timeKeys = []
        for timeKey in timeKeys:
            r = timeDict[timeKey]
            _timeKeys.append((timeKey, forceInt(r.value('idx'))))

        timeKeys = sorted(_timeKeys)

        for timeAndIdx in timeKeys[1:]:
            time = timeAndIdx[0]
            newRecord = tableActionExecutionPlan.newRecord()
            record = executionPlan[currentDayKey][time]

            dosage = forceDouble(record.value('dosage'))
            idx = forceInt(record.value('idx'))

            newRecord.setValue('execDate', QDateTime(executionPlanKeys[0], time))
            newRecord.setValue('dosage', toVariant(dosage))
            newRecord.setValue('idx', toVariant(idx))

            newExecutionPlan.setdefault(currentDayKey, {})[time] = newRecord

        for executionPlanKey in executionPlanKeys[1:]:
            timeDict = executionPlan[executionPlanKey]
            timeKeys = timeDict.keys()
            timeKeys.sort()
            for time in timeKeys:
                newRecord = tableActionExecutionPlan.newRecord()
                newRecord.setValue('execDate', QDateTime(executionPlanKey, time))

                dosage = forceDouble(timeDict[time].value('dosage'))
                idx = forceInt(timeDict[time].value('idx'))
                newRecord.setValue('dosage', toVariant(dosage))
                newRecord.setValue('idx', toVariant(idx))

                newExecutionPlan.setdefault(executionPlanKey, {})[time] = newRecord

        return newExecutionPlan


    def defaultExecutionPlanCount(self):
        if self._action.getType().isNomenclatureExpense:
            return self.defaultExecutionPlanCountNE()
        record = self._action.getRecord()

        # Длительность
        duration = forceInt(record.value('duration'))

        # periodicity - это интервал. Сколько полных дней между назначениями
        periodicity = forceInt(record.value('periodicity'))

        # кратность
        aliquoticity = forceInt(record.value('aliquoticity')) or 1

        # Количество процедур
        quantity = forceInt(record.value('quantity'))

        if not (duration >= 1 or aliquoticity >= 1 or quantity >= 1):
            return 0

        begDate = forceDate(record.value('begDate'))
        plannedEndDate = begDate.addDays(duration - 1)
        count = 0
        execDate = begDate
        execQuantity = quantity
        if duration > 0:
            execAliquoticity = aliquoticity if aliquoticity > 0 else 1
            while execQuantity > 0:
                if execDate <= plannedEndDate:
                    for _ in xrange(execAliquoticity):
                        count += 1
                        execQuantity -= 1
                    execDate = execDate.addDays(periodicity + 1)
                else:
                    break
        elif duration == 0:
            count = execQuantity
        return count


    def defaultExecutionPlanCountNE(self):
        record = self._action.getRecord()

        # Длительность
        duration = forceInt(record.value('duration')) or 1

        # periodicity - это интервал. Сколько полных дней между назначениями
        periodicity = forceInt(record.value('periodicity'))

        # кратность
        aliquoticity = forceInt(record.value('aliquoticity')) or 1

        if not (duration > 1 or aliquoticity > 1):
            return 0

        begDate = forceDate(record.value('begDate'))
        plannedEndDate = begDate.addDays(duration - 1)

        count = 0

        execDate = begDate
        while execDate <= plannedEndDate:
            for _ in xrange(aliquoticity):
                count += 1

            execDate = execDate.addDays(periodicity + 1)

        return count

