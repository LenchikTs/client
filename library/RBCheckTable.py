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

from PyQt4               import QtGui
from PyQt4.QtCore        import Qt, QVariant, SIGNAL

from library.InDocTable  import CRecordListModel, CInDocTableCol, CInDocTableView
from library.Utils       import forceBool, forceRef



class CRBCheckTableModel(CRecordListModel):
    __pyqtSignals__ = ('itemCheckingChanged()',
                      )

    def __init__(self, parent, tableName, header, filter=''):
        CRecordListModel.__init__(self, parent)
        self.addCol(CInDocTableCol(u'Код', 'code', 10).setReadOnly().setSortable())
        self.addCol(CInDocTableCol(header, 'name', 30).setReadOnly().setSortable())
        self._checkedIdSet = set()
        self._filter    = filter
        self._tableName = tableName
        self.updateList()


    def _idSet(self):
        return set( ( forceRef(item.value('id')) for item in self.items()) )


    def updateList(self):
        items = QtGui.qApp.db.getRecordList(self._tableName,
                                           ('id','code','name'),
                                           self._filter,
                                           'code')
        self.setItems(items)
        self._checkedIdSet &= self._idSet()


    def setFilter(self, filter):
        if self._filter != filter:
            self._filter = filter
            self.updateList()


    def idList(self):
        return list(self._idSet())


    def getCheckedIdSet(self):
        return set(self._checkedIdSet)


    def getCheckedIdList(self):
        return list(self._checkedIdSet)


    def setCheckedIdList(self, checkedIdSet):
        newCheckedIdSet = set(checkedIdSet) & self._idSet()
        if self._checkedIdSet != newCheckedIdSet:
            self._checkedIdSet = newCheckedIdSet
            self.emitColumnChanged(0)
            self.emitItemCheckingChanged()


    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row    = index.row()
        if role == Qt.CheckStateRole and column == 0:
            itemId = forceRef(self.value(row,'id'))
            return QVariant( Qt.Checked if itemId in self._checkedIdSet else Qt.Unchecked )
        return CRecordListModel.data(self, index, role)


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        row    = index.row()
        if role == Qt.CheckStateRole and column == 0:
            row = index.row()
            itemId = forceRef(self.items()[row].value('id'))
            if forceBool(value):
                self._checkedIdSet.add(itemId)
            else:
                self._checkedIdSet.discard(itemId)
            self.emitCellChanged(row, column)
            self.emitItemCheckingChanged()
            return True
        return False


    def checkAll(self, value=True):
        bs = self.blockSignals(True)
        try:
            for row in xrange(self.rowCount()):
                self.setData(self.index(row, 0), value, Qt.CheckStateRole)
        finally:
            self.blockSignals(bs)

        self.emitColumnChanged(0)
        self.emitItemCheckingChanged()


    def uncheckAll(self):
        self.checkAll(value=False)


    def emitItemCheckingChanged(self):
        self.emit(SIGNAL('itemCheckingChanged()'))



# ####################################################################################

class CRBCheckTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.actCheckAll   = QtGui.QAction(u'Отметить всё', self)
        self.actUncheckAll = QtGui.QAction(u'Снять все отметки', self)
        self.createPopupMenu([self.actCheckAll, self.actUncheckAll])
        self.connect(self.actCheckAll,   SIGNAL('triggered()'), self.checkAll)
        self.connect(self.actUncheckAll, SIGNAL('triggered()'), self.uncheckAll)
        self.connect(self.popupMenu(), SIGNAL('aboutToShow()'), self.aboutToShowPopup)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)


    def currentItemId(self):
        model = self.model()
        if model:
            row = self.currentIndex().row()
            return forceRef(model.value(row, 'id'))


    def checkAll(self):
        model = self.model()
        if model:
            model.checkAll()


    def uncheckAll(self):
        model = self.model()
        if model:
            model.uncheckAll()


    def aboutToShowPopup(self):
        model = self.model()
        if model:
            checkedIdList = model.getCheckedIdList()
            rowCount      = model.rowCount()
            self.actCheckAll.setEnabled(len(checkedIdList)<rowCount)
            self.actUncheckAll.setEnabled(bool(checkedIdList))
        else:
            self.actCheckAll.setEnabled(False)
            self.actUncheckAll.setEnabled(False)
