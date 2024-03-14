# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtSql
from PyQt4.QtCore import Qt, QVariant

from library.DialogBase import CDialogBase
from library.InDocTable import CRecordListModel, CDateTimeInDocTableCol, CIntInDocTableCol, CTimeInDocTableCol
from library.Utils      import forceInt, toVariant
from Resources.JobSchedule import getGapListForOrgStructure

from Resources.Ui_JobTicketsDialog import Ui_JobTicketsDialog


class CJobTicketsDialog(Ui_JobTicketsDialog, CDialogBase):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('JobTickets', CJobTicketsModel(self))
        self.addModels('Gaps', CGapsModel(self))
        self.setupUi(self)
        self.setModels(self.tblJobTickets,  self.modelJobTickets, self.selectionModelJobTickets)
        self.setModels(self.tblGaps,  self.modelGaps, self.selectionModelGaps)
#        self.timeDelegate = CTimeItemDelegate(self)
#        self.tblJobAmbNumbers.setItemDelegateForColumn(0, self.timeDelegate)
#        self.modelJobAmbNumbers.loadData(orgStructureId, jobTypeId, date)
#        self.modelJobOrgStructureGaps.loadData()

    def setJob(self, job):
        self.modelJobTickets.setItems(job.items)
        self.modelGaps.setOrgStructureId(job.orgStructureId)



    def saveData(self):
#        if not self.checkData(self.modelJobAmbNumbers, self.modelJobAmbNumbers.tableItems.changed, self.tblJobAmbNumbers):
#            return False
#        self.modelJobAmbNumbers.saveData()
        return True


#    def checkData(self, model, changed, widget):
#        if model.tableItems:
#            if changed:
#                timeRange = model.tableItems.timeRange
#                begTime, endTime = timeRange if timeRange else (None, None)
#            else:
#                if model.tableItems.record:
#                    begTime = forceTime(model.tableItems.record.value('begTime'))
#                    endTime = forceTime(model.tableItems.record.value('endTime'))
#                else:
#                    begTime, endTime = None, None
#            lenItems = len(model.items)
#            for row in xrange(lenItems):
#                itemTime = model.items[row][0]
#                if row > 0 and (row + 1) < lenItems:
#                    firstTime = model.items[row - 1][0]
#                    nextTime = model.items[row + 1][0]
#                else:
#                    firstTime = None
#                    nextTime = None
#                if not self.checkDataNumbers(begTime, endTime, itemTime, firstTime, nextTime, widget, row):
#                    return False
#        return True


#    def checkDataNumbers(self, begTime, endTime, date, firstTime, nextTime, widget, row, column=0):
#        result = True
#        if row > 0:
#            if firstTime:
#                result = result and (firstTime <= date or self.checkValueMessage(u'Время предыдущего номерка %s не должно быть позже времени следующего номерка %s' % (firstTime.toString('HH:mm'), date.toString('HH:mm')), False, widget, row, column))
#                result = result and (firstTime != date or self.checkValueMessage(u'Время предыдущего номерка %s не должно быть равно времени следующего номерка %s' % (firstTime.toString('HH:mm'), date.toString('HH:mm')), False, widget, row, column))
#            if nextTime:
#                result = result and (nextTime >= date or self.checkValueMessage(u'Время следующего номерка %s не должно быть меньше времени предыдущего номерка %s' % (nextTime.toString('HH:mm'), date.toString('HH:mm')), False, widget, row, column))
#                result = result and (nextTime != date or self.checkValueMessage(u'Время следующего номерка %s не должно быть равно времени предыдущего номерка %s' % (nextTime.toString('HH:mm'), date.toString('HH:mm')), False, widget, row, column))
#        else:
#            result = result and (begTime or self.checkValueMessage(u'Отсутствует время начала периода по плану %s' % (begTime.toString('HH:mm')), False, widget, row, column))
#            result = result and (begTime <= date or self.checkValueMessage(u'Время номерка %s не должно быть раньше начала периода по плану %s' % (date.toString('HH:mm'), begTime.toString('HH:mm')), False, widget, row, column))
#        result = result and (endTime or self.checkValueMessage(u'Отсутствует время конца периода по плану %s' % (endTime.toString('HH:mm')), False, widget, row, column))
#        result = result and (date <= endTime or self.checkValueMessage(u'Время номерка %s не должно быть позже конца периода по плану %s' % (date.toString('HH:mm'), endTime.toString('HH:mm')), False, widget, row, column))
#        result = result and (date != endTime or self.checkValueMessage(u'Время номерка %s не должно быть равно концу периода по плану %s' % (date.toString('HH:mm'), endTime.toString('HH:mm')), False, widget, row, column))
#        return result


class CJobTicketsModel(CRecordListModel):
    class CLocNumberColumn(CIntInDocTableCol):
        def __init__(self, title, fieldName, width, **params):
            CIntInDocTableCol.__init__(self, title, fieldName, width, **params)

        def toString(self, val, record):
            idx  = forceInt(val)
            return toVariant(idx+1)


    def __init__(self, parent):
        CRecordListModel.__init__(self, parent)
        self.addCol(CJobTicketsModel.CLocNumberColumn(u'Номер', 'idx', 10))
        self.addCol(CDateTimeInDocTableCol(u'Время', 'datetime', 10))


    def flags(self, index):
        row = index.row()
#        column = index.column()
        item = self.items()[row]
        if item.isUsed:
            return Qt.ItemIsSelectable
        else:
            return Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled


#    def emitCellChanged(self, row, column):
#        index = self.index(row, column)
#        self.emit(QtCore.SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


class CGapsModel(CRecordListModel):
    def __init__(self, parent):
        CRecordListModel.__init__(self, parent)
        self.addCol(CTimeInDocTableCol(u'Начало', 'begTime', 10)).setToolTip(u'Время начала перерыва').setSortable()
        self.addCol(CTimeInDocTableCol(u'Окончание', 'endTime', 10)).setToolTip(u'Время окончания перерыва').setSortable()

    def setOrgStructureId(self, orgStructureId):
        gapList = getGapListForOrgStructure(orgStructureId)
        items = []
        for gap in gapList:
            item = QtSql.QSqlRecord()
            item.append(QtSql.QSqlField('begTime', QVariant.Time))
            item.append(QtSql.QSqlField('endTime', QVariant.Time))
            item.setValue('begTime', gap[0])
            item.setValue('endTime', gap[1])
        self.setItems(items)



