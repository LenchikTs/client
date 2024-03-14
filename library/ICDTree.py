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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QAbstractItemModel, QModelIndex, QVariant

from library.abstract import abstract
from library.ICDUtils import MKBwithoutSubclassification
from library.TableModel import CTableModel, CTextCol
from library.Utils import addDotsEx, forceRef, forceString, forceStringEx, toVariant

from library.Ui_ICDTree import Ui_ICDTreePopup


u"""Выпадающая таблица с деревом для выбора кода МКБ"""


class CICDTreePopup(QtGui.QFrame, Ui_ICDTreePopup):
    __pyqtSignals__ = ('diagSelected(QString)',
                      )

    def __init__(self, parent=None, filter=u'', findfilter=u''):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
#        self.setAttribute(Qt.WA_AlwaysShowToolTips)
#        self.setWindowFlags(Qt.SubWindow)
        self.treeModel = CICDTreeModel(self, filter, findfilter)
        self.tableModel = CTableModel(self, [
                        CTextCol(u'Код',          ['DiagID'],   6),
                        CTextCol(u'Наименование', ['DiagName'], 40)],
                        'MKB')
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel,  self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.treeView.setModel(self.treeModel)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAllColumnsShowFocus(True)
        textWidth = self.treeView.fontMetrics().width('W00.000')
        self.treeView.setColumnWidth(0, self.treeView.indentation()*5+textWidth)
        self.tblSearchResult.setModel(self.tableModel)
        self.tblSearchResult.setSelectionModel(self.tableSelectionModel)
        self.treeView.setFocus()
        self.diag = None
        self.setLUDEnabled(False)
        self.clientId = None
        self.filter = filter
        self.findfilter = findfilter
        self.chkUseFindFilter.setChecked(bool(self.findfilter))
        self.findDiagId = None


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent is not None:
            opt = QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos()):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


#    def mouseReleaseEvent(self, event):
##        self.emit(SIGNAL('resetButton()'))
#        self.parent().mouseReleaseEvent(event)
#        pass


#    def eventFilter(self, obj, event):
#        if obj == self.treeView or obj == self.tblSearchResult:
#            if event.type() == QEvent.KeyPress:
#                if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
#                    pass
#            elif QEvent.ToolTip:
#                text = obj.toolTip()
#                if text:
#                    QToolTip.showText(event.globalPos(), 'sample', self)
#                return True
##        return QtGui.QFrame.eventFilter(self, obj, event)
#        return False


#    def event(self, event):
###        print event.type()
#        if event.type()==QEvent.ToolTip:
#           child = self.childAt(event.pos())
#           return child.event(event)
##           while child and child.objectName() == 'qt_scrollarea_viewport':
##                child = child.parentWidget()
##           if child:
##               return child()
##                text = child.toolTip()
##                if text:
##                    QToolTip.showText(event.globalPos(), text, self)
#        return QtGui.QFrame.event(self, event)


    def setCurrentDiag(self, diag):
        self.treeView.collapseAll()
        self.diag = forceString(diag)
        if self.diag or self.findDiagId:
            index = self.treeModel.findDiag(self.diag if self.diag else self.findDiagId)
            self.treeView.scrollTo(index)
            self.treeView.setCurrentIndex(index)
            self.treeView.setExpanded(index, True)


    def setLUDEnabled(self, value):
        self.chkLUD.setEnabled(value)


    def selectDiag(self, diag):
        self.diag = diag
        self.emit(SIGNAL('diagSelected(QString)'), diag)
        self.close()


    def getCurrentDiag(self):
        id = self.tblSearchResult.currentItemId()
        if id:
            diag = forceString(QtGui.qApp.db.translate('MKB', 'id', id, 'DiagID'))
            return diag
        return ''


    def setLUDChecked(self, isLUDSelected, clientId):
        if self.chkLUD.isEnabled():
            self.chkLUD.setChecked(isLUDSelected)
            self.clientId = clientId


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self,  index):
        if index == 0 and not self.findDiagId:
            diag = self.getCurrentDiag()
            self.setCurrentDiag(diag)
        elif index == 1:
            self.edtWords.setText(self.edtFindWord.text())


    @pyqtSignature('QModelIndex')
    def on_treeView_doubleClicked(self, index):
        flags = self.treeModel.flags(index)
        if flags & Qt.ItemIsSelectable:
            diag = forceString(self.treeModel.diag(index))
            self.selectDiag(diag)


    @pyqtSignature('')
    def on_btnSearch_clicked(self):
        db = QtGui.qApp.db
        words = forceStringEx(self.edtWords.text())
        table = self.tableModel.table()
        if self.chkLUD.isVisible() and self.chkLUD.isChecked() and self.clientId:
            tableDiagnosis = db.table('Diagnosis')
            stmt = db.selectDistinctStmt(tableDiagnosis, [tableDiagnosis['MKB']], [tableDiagnosis['client_id'].eq(self.clientId), tableDiagnosis['deleted'].eq(0)], tableDiagnosis['MKB'].name())
            query = db.query(stmt)
            MKBList = []
            while query.next():
                record = query.record()
                MKBList.append(forceStringEx(record.value('MKB')))
            cond = []
            if words:
                cond.append(table['DiagName'].like(addDotsEx(words)))
            if MKBList:
                cond.append(table['DiagID'].inlist(MKBList))
        else:
            cond = [table['DiagName'].like(addDotsEx(words))]
        idList = db.getIdList(table, 'id',
                                where=cond,
                                order='DiagID')
        self.tableModel.setIdList(idList)


    @pyqtSignature('QModelIndex')
    def on_tblSearchResult_doubleClicked(self, index):
        diag = self.getCurrentDiag()
        self.edtFindWord.setText('')
        self.findDiagId = None
        self.selectDiag(diag)


    @pyqtSignature('bool')
    def on_chkUseFindFilter_toggled(self, checked):
        self.treeModel.setFindFilter(self.findfilter if checked else u'')


    @pyqtSignature('QString')
    def on_edtFindWord_textChanged(self, text):
        self.findDiagId = None
        words = forceStringEx(text)
        table = self.tableModel.table()
        cond = [table['DiagName'].like(addDotsEx(words))]
        record = QtGui.qApp.db.getRecordEx(table, 'id',
                                where=cond,
                                order='DiagID')
        if record:
            id = forceRef(record.value('id'))
            if id:
                diag = forceString(QtGui.qApp.db.translate('MKB', 'id', id, 'DiagID'))
                self.setCurrentDiag(diag)
                self.findDiagId = diag


class CBaseTreeItem:
    subclasses = {}

    @staticmethod
    def loadSubclassItems(subclassId):
        result = []
        stmt   = 'SELECT code, name FROM %s WHERE master_id=%d ORDER BY code' % ('rbMKBSubclass_Item', subclassId, )
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            code   = forceString(record.value('code'))
            name   = forceString(record.value('name'))
            result.append( (code, name) )
        return result


    @staticmethod
    def getSubclassItems(subclassId):
        result = CBaseTreeItem.subclasses.get(subclassId, None)
        if result is None:
            result = CBaseTreeItem.loadSubclassItems(subclassId)
            CBaseTreeItem.subclasses[subclassId] = result
        return result


    def __init__(self, code, name, index, subclassId, parent=None, filter='', findFilter=''):
        self.parent = parent
        self.filter = filter
        self.findFilter = findFilter
        self.code = code
        self.name = name
        self.index = index
        self.subclassId = subclassId
        self.items = None
        self.itemsCount = None

#    def appendChild(self, item):
#        self.childItems.append(item)

    def child(self, row):
        if self.items is None:
            self.items = self.loadChilds()
            self.itemsCount = len(self.items)
        return self.items[row]


    @abstract
    def countChilds(self):
        pass


    def childCount(self):
        if self.itemsCount is None:
            self.itemsCount = self.countChilds()
        return self.itemsCount


    def columnCount(self):
        return 2


    def selectable(self):
        # if self.itemsCount:
        #     return False
        return True


    def data(self, column):
        if column == 0:
            return self.code
        if column == 1:
            return self.name
        return QVariant()


    def row(self):
        if self.parent:
            return self.parent.items.index(self)
        return 0


    def loadChilds(self):
        return []


    def findChildByCode(self, code):
        if self.items is None:
            self.items = self.loadChilds()
            self.itemsCount = len(self.items)
        for child in self.items:
            if child.code == code:
                return child
        return None


class CICDRootTreeItem(CBaseTreeItem):
    def __init__(self, filter='', findFilter=''):
        CBaseTreeItem.__init__(self, '', '', 0, None, parent=None, filter=filter, findFilter=findFilter)
        self.findFilter = findFilter


    def selectable(self):
        return False


    def countChilds(self):
        result = 0
        stmtFilter = u''
        if self.filter or self.findFilter:
            findFilter = (self.findFilter[0]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
            stmtFilter = ('WHERE %s'%(u' AND '.join(filter for filter in [self.filter, findFilter] if filter)))
        stmt   = 'SELECT COUNT(DISTINCT ClassID) FROM MKB %s'%(stmtFilter)
        query = QtGui.qApp.db.query(stmt)
        if query.next():
            record = query.record()
            result = record.value(0).toInt()[0]
        return result


    def loadChilds(self):
        result = []
        stmtFilter = u''
        if self.filter or self.findFilter:
            findFilter = (self.findFilter[0]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
            stmtFilter = ('WHERE %s'%(u' AND '.join(filter for filter in [self.filter, findFilter] if filter)))
        stmt   = 'SELECT DISTINCT ClassID, ClassName FROM MKB %s ORDER BY ClassID'%(stmtFilter)
        query = QtGui.qApp.db.query(stmt)
        i = 0
        while query.next():
            record = query.record()
            code   = forceString(record.value('ClassID'))
            name   = forceString(record.value('ClassName'))
            result.append( CICDClassTreeItem(code, name, i, None, self, self.filter, self.findFilter) )
            i += 1
        return result


    def findChild(self, classId, blockId, diagId, diag):
        child = self.findChildByCode(classId)
        if child:
            return child.findChild(blockId, diagId, diag)
        else:
            return self


    def findDiag(self, diag):
        normDiag = MKBwithoutSubclassification(diag)
        db = QtGui.qApp.db
        table = db.table('MKB')
        cond = [table['DiagID'].eq(normDiag)]
        if self.filter:
            cond.append(self.filter)
        if self.findFilter:
            findFilter = (self.findFilter[1]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
            if findFilter:
                cond.append(findFilter)
        record = db.getRecordEx(table, ['ClassID, BlockID'], cond)
        if not record:
            normDiag = diag[:3]
            record = db.getRecordEx(table, 'ClassID, BlockID', table['DiagID'].eq(normDiag))
        if not record:
            record = db.getRecordEx(table, 'ClassID, BlockID', table['DiagID'].like(normDiag+'%'))
        if record:
            classId = forceString(record.value('ClassID'))
            blockId = forceString(record.value('BlockID'))
            diagId  = normDiag
            return self.findChild(classId, blockId, diagId, diag)
        return self


class CICDClassTreeItem(CBaseTreeItem):
    def countChilds(self):
        result = 0
        findFilter = (self.findFilter[0]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
        stmt   = 'SELECT COUNT(DISTINCT BlockID) FROM %s WHERE ClassID = \'%s\' %s %s' %('MKB', self.code, (' AND %s'% self.filter) if self.filter else '', (' AND %s'% findFilter) if findFilter else '')
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            result = record.value(0).toInt()[0]
        return result


    def selectable(self):
        return False


    def loadChilds(self):
        result = []
        findFilter = (self.findFilter[0]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
        stmt   = 'SELECT DISTINCT BlockID, BlockName FROM %s WHERE ClassID = \'%s\' %s %s ORDER BY BlockID' %('MKB', self.code, (' AND %s'% self.filter) if self.filter else '', (' AND %s'% findFilter) if findFilter else '')
        query = QtGui.qApp.db.query(stmt)
        i = 0
        while query.next():
            record = query.record()
            code   = forceString(record.value('BlockID'))
            name   = forceString(record.value('BlockName'))
            result.append( CICDBlockTreeItem(code, name, i, None, self, self.filter, self.findFilter) )
            i += 1
        return result


    def findChild(self, blockId, diagId, diag):
        child = self.findChildByCode(blockId)
        if child:
            return child.findChild(diagId, diag)
        else:
            return self


class CICDBlockTreeItem(CBaseTreeItem):
    def countChilds(self):
        result = 0
        findFilter = (self.findFilter[0]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
        stmt   = 'SELECT COUNT(DiagID) FROM %s WHERE BlockID = \'%s\' AND DiagID LIKE \'___\' %s %s ORDER BY DiagID' %('MKB', self.code, (' AND %s'% self.filter) if self.filter else '', (' AND %s'% findFilter) if findFilter else '')
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            result = record.value(0).toInt()[0]
        return result


    def selectable(self):
        return False


    def loadChilds(self):
        result = []
        findFilter = (self.findFilter[0]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
        stmt   = 'SELECT DiagID, DiagName, MKBSubclass_id FROM %s WHERE BlockID = \'%s\' AND DiagID LIKE \'___\' %s %s ORDER BY DiagID' %('MKB', self.code, (' AND %s'% self.filter) if self.filter else '', (' AND %s'% findFilter) if findFilter else '')
        query = QtGui.qApp.db.query(stmt)
        i = 0
        while query.next():
            record = query.record()
            code   = forceString(record.value('DiagID'))
            name   = forceString(record.value('DiagName'))
            subclassId = forceRef(record.value('MKBSubclass_id'))
            result.append( CICDDiagTreeItem(code, name, i, subclassId, self, self.filter, self.findFilter) )
            i += 1
        return result


    def findChild(self, diagId, diag):
        child = self.findChildByCode(diagId[:3])
        if child:
            return child.findChild(diagId, diag)
        else:
            return self


class CICDDiagTreeItem(CBaseTreeItem):
    def countChilds(self):
        result = 0
        findFilter = (self.findFilter[1]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
        stmt   = 'SELECT COUNT(DiagID) FROM %s WHERE DiagID LIKE \'%s.%%\' %s %s ORDER BY DiagID' %('MKB', self.code, (' AND %s'% self.filter) if self.filter else '', (' AND %s'% findFilter) if findFilter else '')
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            result = record.value(0).toInt()[0]

        if self.subclassId:
            result += len(self.getSubclassItems(self.subclassId))
        return result


    def loadChilds(self):
        result = []
        i = 0
        if self.subclassId:
            for code, name in self.getSubclassItems(self.subclassId):
                result.append( CICDDiagSubclassTreeItem(self.code + '. '+ code, ' -/- '+name, i, None, self, self.filter, self.findFilter) )
                i += 1
        findFilter = (self.findFilter[1]) if self.findFilter and isinstance(self.findFilter, tuple) else self.findFilter
        stmt   = 'SELECT DiagID, DiagName, MKBSubclass_id FROM %s WHERE DiagID LIKE \'%s.%%\' %s %s ORDER BY DiagID' %('MKB', self.code, (' AND %s'% self.filter) if self.filter else '', (' AND %s'% findFilter) if findFilter else '')
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            code   = forceString(record.value('DiagID'))
            name   = forceString(record.value('DiagName'))
            subclassId = forceRef(record.value('MKBSubclass_id'))
            result.append( CICDDiagExTreeItem(code, name, i, subclassId, self, self.filter, self.findFilter) )
            i += 1
        return result


    def findChild(self, diagId, diag):
        child = self.findChildByCode(diagId)
        if child:
            return child.findChild(diag)
        elif self.subclassId:
            child = self.findChildByCode(diag)
            if child:
                return child
        return self


class CICDDiagExTreeItem(CBaseTreeItem):

    def countChilds(self):
        if self.subclassId:
            return len(self.getSubclassItems(self.subclassId))
        else:
            return 0


    def loadChilds(self):
        result = []
        i = 0
        if self.subclassId:
            for code, name in self.getSubclassItems(self.subclassId):
                result.append( CICDDiagSubclassTreeItem(self.code + code, ' -/- '+name, i, None, self, self.filter, self.findFilter) )
                i += 1
        return result


    def findChild(self, diag):
        if self.subclassId:
            child = self.findChildByCode(diag)
            if child:
                return child
        return self


class CICDDiagSubclassTreeItem(CBaseTreeItem):
    def countChilds(self):
        return 0


    def loadChilds(self):
        return []


class CICDTreeModel(QAbstractItemModel):
    chCode = QVariant(u'Код')
    chName = QVariant(u'Наименование')

    def __init__(self, parent=None, filter = '', findFilter=None):
        QAbstractItemModel.__init__(self, parent)
        self.filter = filter
        self.findFilter = findFilter
        self._rootItem = CICDRootTreeItem(self.filter)


    def setFindFilter(self, findFilter=None):
        self.findFilter = findFilter
        if self._rootItem:
            self._rootItem = CICDRootTreeItem(self.filter, self.findFilter)
            self.reset()


    def setFilter(self, filter=None):
        if self.filter != filter:
            self.filter = filter
            if self._rootItem:
                self._rootItem = CICDRootTreeItem(self.filter, self.findFilter)
                self.reset()


    def getRootItem(self):
        return self._rootItem


    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.getRootItem().columnCount()


    def data(self, index, role):
        if role == Qt.ToolTipRole:
            pass
        if index.isValid():
            column = index.column()
            if role == Qt.DisplayRole or (column == 1 and role == Qt.ToolTipRole):
                item = index.internalPointer()
                return toVariant(item.data(column))
        return QVariant()


    def diag(self, index):
        if index.isValid():
            item = index.internalPointer()
            return item.data(0)
        return ''


    def flags(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item.selectable():
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled


    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return self.chCode
            if section == 1:
                return self.chName
        return QVariant()


    def index(self, row, column, parent):
        if not parent.isValid():
            parentItem = self.getRootItem()
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()


    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent

        if parentItem == self.getRootItem() or parentItem is None:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)


    def rowCount(self, parent):
        if not parent.isValid():
            parentItem = self.getRootItem()
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()


    def findDiag(self, code):
        item = self.getRootItem().findDiag(code)
        return self.createIndex(item.index, 0, item)
