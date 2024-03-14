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
from PyQt4.QtCore import Qt, QVariant

from library.database                       import CTableRecordCache
from library.DialogBase                     import CDialogBase
from library.TableModel                     import CTableModel, CCol, CDateTimeCol, CEnumCol, CRefBookCol, CTextCol
from library.Utils                          import forceBool, forceRef, formatName, toVariant, forceString

from Timeline.Ui_ScheduleItemsHistoryDialog import Ui_ScheduleItemsHistoryDialog


class CScheduleItemsHistoryDialog(CDialogBase, Ui_ScheduleItemsHistoryDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('ScheduleItems', CScheduleItemsModel(self))

        self.setupUi(self)
        self.setModels(self.tblScheduleItems,  self.modelScheduleItems, self.selectionModelScheduleItems)


    def setPersonAndDate(self, personId, date):
        db = QtGui.qApp.db
        tableScheduleItem = db.table('Schedule_Item')
        tableSchedule = db.table('Schedule')
        table = tableScheduleItem.leftJoin(tableSchedule, tableSchedule['id'].eq(tableScheduleItem['master_id']))

        cond = [ tableSchedule['date'].eq(date),
                 tableSchedule['person_id'].eq(personId),
               ]

        idList = db.getIdList(table, idCol=tableScheduleItem['id'].name(), where=cond, order=tableScheduleItem['time'].name())
        self.tblScheduleItems.setIdList(idList)


class CClientCol(CCol):
    def __init__(self, title, fields, defaultWidth):
        CCol.__init__(self, title, fields, defaultWidth, 'l')
        db = QtGui.qApp.db
        self.clientCache = CTableRecordCache(db, 'Client', 'firstName, lastName, patrName, id')


    def getClientRecord(self, clientId):
        return self.clientCache.get(clientId) if clientId else None


    def format(self, values):
        clientId = forceRef(values[0])
        record = self.getClientRecord(clientId)
        if record:
            name  = formatName(record.value('lastName'),
                               record.value('firstName'),
                               record.value('patrName')) + u', (' + forceString(record.value('id')) + u')'
            return toVariant(name)
        else:
            return QVariant()


class CScheduleItemsModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent,  [
            CDateTimeCol(u'Время', ['time', 'master_id', 'deleted'], 10),
            CClientCol(u'Ф.И.О.', ['client_id'], 30),
            CEnumCol(u'Запись через',  ['recordClass'], [u'-', u'инфомат', u'Врач_АПУ', u'интернет', u'интернет', u'интернет', u'интернет', u'ЕПГУ'], 4, 'l'),
            CDateTimeCol(u'Дата и время записи', ['recordDatetime'], 10),
            CRefBookCol(u'Записал', ['recordPerson_id'], 'vrbPersonWithSpeciality', 20),
            CDateTimeCol(u'Дата и время изменения', ['modifyDatetime'], 10),
            CRefBookCol(u'Изменил', ['modifyPerson_id'], 'vrbPersonWithSpeciality', 20),
            CTextCol(u'Примечание', ['note'], 30),
            ], 'Schedule_Item' )
        # self.scheduleCache = CTableRecordCache(QtGui.qApp.db, 'Schedule', 'deleted')


    def data(self, index, role):
        if role == Qt.FontRole:
            column = index.column()
            if column == 0:
                row = index.row()
                id = self.idList()[row]
                if self.itemIsDeleted(id):
                    font = QtGui.QFont()
                    font.setStrikeOut(True)
                    return QVariant(font)
            return QVariant()
        else:
            return CTableModel.data(self, index, role)


    def itemIsDeleted(self, itemId):
        record = self.getRecordById(itemId)
        itemDeleted = forceBool(record.value('deleted'))
        return itemDeleted
