#!/usr/bin/env python
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
from PyQt4.QtCore import Qt, QDate, QTime, SIGNAL, QDateTime

from library.DialogBase        import CDialogBase
from library.TableModel        import CTableModel, CTextCol, CBoolCol, CCol
from library.Utils             import forceRef, forceBool, forceInt, toVariant
from Resources.JobTicketStatus import CJobTicketStatus

from Resources.Ui_CloseWorkForGroupDialog import Ui_CloseWorkForGroupDialog


class CCloseWorkForGroupDialog(CDialogBase, Ui_CloseWorkForGroupDialog):
    def __init__(self, parent, title, orgStructureId = None, idList=[]):
        CDialogBase.__init__(self, parent)
        self.addModels('ActionType', CCloseWorkForGroupModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblActionType, self.modelActionType, self.selectionModelActionType)
        self.setWindowTitleEx(title)
        self.cmbStatus.setValue(CJobTicketStatus.done)
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId() if QtGui.qApp.currentOrgStructureId() else orgStructureId)
        self.cmbPerson.setValue(QtGui.qApp.userId)
        self.edtExecDate.setDate(QDate.currentDate())
        self.edtExecTime.setTime(QTime.currentTime())
        self.modelActionType.setIdList(idList)
        if idList:
            self.tblActionType.selectRow(0)
            self.setCheckedIdList()


    def getStatus(self):
        return self.cmbStatus.value()


    def getOrgStructure(self):
        return self.cmbOrgStructure.value()


    def getPerson(self):
        return self.cmbPerson.value()


    def getDateTime(self):
        return QDateTime(self.edtExecDate.date(), self.edtExecTime.time())


    def getCheckedIdList(self):
        return self.modelActionType.getCheckedIdList()


    def setCheckedIdList(self):
        return self.modelActionType.setCheckedIdList()


    def selectItem(self):
        return self.exec_()


    def setCurrentItemId(self, itemId):
        self.tblActionType.setCurrentItemId(itemId)


    def currentItemId(self):
        return self.tblActionType.currentItemId()


class CCloseWorkForGroupModel(CTableModel):
    class CLocIncludeColumn(CBoolCol):
        def __init__(self, title, fields, defaultWidth, extraFields=[]):
            CBoolCol.__init__(self, title, fields, defaultWidth, 'l')
            self.extraFields = extraFields
            self.includeCaches = {}

        def format(self, values):
            return CCol.invalid

        def getIncludeCaches(self):
            return self.includeCaches

        def setIncludeCaches(self, includeCaches):
            self.includeCaches = includeCaches

        def checked(self, values):
            val = values[0]
            id  = forceRef(val)
            if id:
                include = self.includeCaches.get(id, 0)
                val = CBoolCol.valChecked if forceBool(include) else CBoolCol.valUnchecked
                self.includeCaches[id] = forceBool(val)
                return val
            else:
                return CCol.invalid

    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CCloseWorkForGroupModel.CLocIncludeColumn(u'Включить', ['id'], 5, ['include']),
            CTextCol(u'Код', ['code'],  20),
            CTextCol(u'Наименование действия', ['name'], 40),
            ], 'ActionType')


    def flags(self, index=None):
        result = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        if role == Qt.CheckStateRole:
            if column == 0:
                record = self.getRecordByRow(row)
                id = forceRef(record.value('id')) if record else None
                if id:
                    self._cols[column].includeCaches[id] = forceInt(value) == Qt.Checked
            self.emitDataChanged(row, column)
            return True
        return False


    def setCheckedIdList(self):
        for row, id in enumerate(self.idList()):
            self.setData(self.index(row, 0), toVariant(Qt.Checked), role=Qt.CheckStateRole)


    def getCheckedIdList(self):
        checkedIdList = []
        includeCaches = self._cols[0].getIncludeCaches()
        for id, include in includeCaches.items():
            if include and id and id not in checkedIdList:
                checkedIdList.append(id)
        return checkedIdList


    def emitDataChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


#class CCloseWorkForGroup(CCloseWorkForGroupDialog):
#    def __init__(self, parent, idList):
#        CActionTypeDialog.__init__(self, parent, [
#            CTextCol(u'Код', ['code'],  20),
#            CTextCol(u'Наименование действия', ['name'], 40),
#            CTextCol(u'"Плоский" код', ['flatCode'], 10)
#            ], 'ActionType', ['id'], False, None, idList)

