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
from PyQt4.QtCore import SIGNAL

from library.DialogBase import CDialogBase
from library.Utils import forceRef, forceInt, toVariant
from library.TableModel import CTableModel, CTextCol, CEnumCol, CDesignationCol, CRefBookCol
from library.crbcombobox import CRBComboBox

from Users.Rights import urCanDeleteForeignActionTypeGroup

from Ui_RBActionTypeGroupList import Ui_RBActionTypeGroupList


ACTION_TYPE_GROUP_APPOINTMENT = 0


class CRBActionTypeGroup(CDialogBase, Ui_RBActionTypeGroupList):
    _groupType = None

    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(u'Шаблоны назначения действий')
        self.addModels('ActionTypeGroups', CActionTypeGroupsModel(self, self._groupType))
        self.addModels('ActionTypeGroupItems', CActionTypeGroupItemsModel(self))

        self.setModels(self.tblActionTypeGroups, self.modelActionTypeGroups, self.selectionModelActionTypeGroups)
        self.setModels(
            self.tblActionTypeGroupItems, self.modelActionTypeGroupItems, self.selectionModelActionTypeGroupItems
        )

        self.tblActionTypeGroupItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.connect(
            self.selectionModelActionTypeGroups, SIGNAL('currentChanged(QModelIndex,QModelIndex)'),
            self.on_selectionModelActionTypeGroupsCurrentChanged
        )

        self._actATGDeleteRows = QtGui.QAction(u'Удалить запись', self)
        self._actATGDeleteRows.setObjectName('actATGDeleteRows')
        self.connect(self._actATGDeleteRows, SIGNAL('triggered()'), self.tblActionTypeGroups.removeSelectedRows)
        self.tblActionTypeGroups.addPopupAction(self._actATGDeleteRows)

        self.connect(self.tblActionTypeGroups.popupMenu(), SIGNAL('aboutToShow()'), self.on_atg_popupMenu_aboutToShow)

        self._actATGIDeleteRows = QtGui.QAction(u'Удалить выделенные записи', self)
        self._actATGIDeleteRows.setObjectName('actATGIDeleteRows')
        self.connect(self._actATGIDeleteRows, SIGNAL('triggered()'), self._atgi_removeSelectedRows)
        self.tblActionTypeGroupItems.addPopupAction(self._actATGIDeleteRows)

        self.connect(
            self.tblActionTypeGroupItems.popupMenu(), SIGNAL('aboutToShow()'), self.on_atgi_popupMenu_aboutToShow
        )

    def _atgi_removeSelectedRows(self):
        def deleteCurrentInternal():
            idList = self.tblActionTypeGroupItems.selectedItemIdList()
            res = QtGui.QMessageBox.question(
                self, u'Внимание!', u'Действительно удалить?',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No
            )
            if res != QtGui.QMessageBox.Yes:
                return

            db = QtGui.qApp.db
            table = db.table('ActionTypeGroup_Item')
            for itemId in idList:
                self.modelActionTypeGroupItems.deleteRecord(table, itemId)
            self.on_selectionModelActionTypeGroupsCurrentChanged(None, None)

        QtGui.qApp.call(self, deleteCurrentInternal)

    def on_selectionModelActionTypeGroupsCurrentChanged(self, current, previous):
        itemId = self.tblActionTypeGroups.currentItemId()
        if not itemId:
            self.tblActionTypeGroupItems.setIdList([])
            return

        db = QtGui.qApp.db
        table = db.table('ActionTypeGroup_Item')
        idList = db.getIdList(table, where=[table['master_id'].eq(itemId), table['deleted'].eq(0)])
        self.tblActionTypeGroupItems.setIdList(idList)

    def _userHasRigthToDelete(self):
        result = QtGui.qApp.userHasRight(urCanDeleteForeignActionTypeGroup)
        if not result:
            record = self.tblActionTypeGroups.currentItem()
            if record:
                createPersonId = forceRef(record.value('createPerson_id'))
                result = QtGui.qApp.userId == createPersonId
        return result

    def on_atg_popupMenu_aboutToShow(self):
        self._actATGDeleteRows.setEnabled(self._userHasRigthToDelete())

    def on_atgi_popupMenu_aboutToShow(self):
        rowsLen = len(self.tblActionTypeGroupItems.selectedItemIdList())
        enabled = self._userHasRigthToDelete() and bool(rowsLen)
        self._actATGIDeleteRows.setEnabled(enabled)
        if rowsLen > 1:
            self._actATGIDeleteRows.setText(u'Удалить выделенные записи')
        else:
            self._actATGIDeleteRows.setText(u'Удалить запись')

    def exec_(self):
        self.modelActionTypeGroups.loadData()
        return CDialogBase.exec_(self)


class CRBActionTypeGroupAppointment(CRBActionTypeGroup):
    _groupType = ACTION_TYPE_GROUP_APPOINTMENT


class CActionTypeGroupsModel(CTableModel):
    class CLocEnumCol(CEnumCol):
        def format(self, values):
            val = values[0]
            if val.isNull():
                return self.invalid
            return CEnumCol.format(self, values)

    def __init__(self, parent, type_, show_class=True):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Код', ['code'], 20))
        self.addColumn(CTextCol(u'Наименование', ['name'], 20))
        if show_class:
            self.addColumn(
                self.CLocEnumCol(u'Класс', ['class'], [u'статус', u'диагностика', u'лечение', u'прочие мероприятия'], 10)
            )
        self.loadField('createPerson_id')
        self.setTable('ActionTypeGroup')
        self._loaded = False
        self._class = None
        self._type = type_

    def deleteRecord(self, table, itemId):
        QtGui.qApp.db.markRecordsDeleted(table, table[self.idFieldName].eq(itemId))
        QtGui.qApp.db.markRecordsDeleted('ActionTypeGroup_Item', 'ActionTypeGroup_Item.master_id=%d' % itemId)

    def loadData(self, class_=None):
        if self._loaded and class_ == self._class:
            return
        self.reloadData(class_)
        self._loaded = True

    def reloadData(self, class_=None):
        db = QtGui.qApp.db
        self._class = class_
        tablePerson = db.table('Person')

        queryTable = self._table.leftJoin(tablePerson, tablePerson['id'].eq(self._table['createPerson_id']))

        cond = [
            self._table['deleted'].eq(0),
            self._table['type'].eq(self._type),
            db.joinOr([
                self._table['availability'].eq(0),
                db.joinAnd([
                    self._table['availability'].eq(1),
                    self._table['id'].isNotNull(),
                    tablePerson['speciality_id'].eq(QtGui.qApp.userSpecialityId)
                ]),
                db.joinAnd([
                    self._table['availability'].eq(2),
                    tablePerson['id'].eq(QtGui.qApp.userId)
                ]),
            ])
        ]
        if class_ is not None:
            cond.append(self._table['class'].eq(class_))

        idList = db.getIdList(queryTable, 'ActionTypeGroup.id', cond, order='class')
        self.setIdList(idList)

class CActionTypeGroupItemsModel(CTableModel):
    class CClassEnum(CDesignationCol):
        class_name_list = [u'статус', u'диагностика', u'лечение', u'прочие мероприятия']
        def format(self, values):
            class_ = forceInt(CDesignationCol.format(self, values))
            return toVariant(self.class_name_list[class_])
    def __init__(self, parent):
        cols = [
            CRefBookCol(u'Код', ['actionType_id'], 'ActionType', 20, showFields=CRBComboBox.showCode),
            CRefBookCol(u'Наименование', ['actionType_id'], 'ActionType', 20, showFields=CRBComboBox.showName),
            self.CClassEnum(u'Код', ['actionType_id'], ('ActionType', 'class'), 20),
        ]
        CTableModel.__init__(self, parent, cols, 'ActionTypeGroup_Item')

    def deleteRecord(self, table, itemId):
        QtGui.qApp.db.markRecordsDeleted(table, table[self.idFieldName].eq(itemId))
