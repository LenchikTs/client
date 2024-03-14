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

import re

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, QVariant, SIGNAL


from library.ThesaurusEdit import cursorInPlaceholder, moveCursorToEndOfWord, separatorBeforeCursor, removeUsedPrefix, setCursorToNextPlaceholder, PLACEHOLDER
from library.TreeModel     import CDBTreeModel, CDBTreeItem
from library.Utils         import forceString, trim

from ActionPropertyValueType           import CActionPropertyValueType
from ComplaintsActionPropertyValueType import CComplaintsActionPropertyValueType
from StringActionPropertyValueType     import CStringActionPropertyValueType
from library.SpellCheck                import CSpellCheckTextEdit


class CConstructorActionPropertyValueType(CActionPropertyValueType):
    name         = 'Constructor'
    preferredHeight = 10
    preferredHeightUnit = 1
    variantType  = QVariant.String
    expandingHeight = True

    class CPropEditor(QtGui.QWidget):
        __pyqtSignals__ = ('editingFinished()',
                           'commit()',
                          )


        def __init__(self, action, domain, parent, clientId, eventTypeId, isValueDomain=False):
            QtGui.QWidget.__init__(self, parent)
            self.gridlayout = QtGui.QGridLayout(self)
            self.gridlayout.setMargin(0)
            self.gridlayout.setSpacing(0)
            self.gridlayout.setObjectName('gridlayout')

            self.splitter = QtGui.QSplitter(self)
            self.splitter.setObjectName('splitter')
            self.splitter.setOrientation(Qt.Horizontal)
            self.splitter.setChildrenCollapsible(False)
            self.splitter.setAutoFillBackground(True)
            self.splitter.setFocusPolicy(Qt.ClickFocus)

#            self.treeView = QtGui.QTreeView(self.splitter)
            self.treeView = CComplaintsActionPropertyValueType.CTreeView(self.splitter)
            self.treeView.setObjectName('treeView')

            db = QtGui.qApp.db
            table = db.table('rbThesaurus')
            rootItemIdCandidates = db.getIdList(table, 'id', [table['group_id'].isNull(), table['code'].eq(domain)], 'id')
            # если в корне не нашлось, ищем в прочих.
            if not rootItemIdCandidates:
                rootItemIdCandidates = db.getIdList(table, 'id', table['code'].eq(domain), 'id')
            rootItemId = rootItemIdCandidates[0] if rootItemIdCandidates else None
            self.treeModel = CDBTreeModel(self, 'rbThesaurus', 'id', 'group_id', 'name', order='code')
            self.treeModel.setRootItem(CDBTreeItem(None, domain, rootItemId, self.treeModel))
            self.treeModel.setRootItemVisible(False)
            self.treeModel.setLeavesVisible(True)
            self.treeView.setModel(self.treeModel)
            self.treeView.header().setVisible(False)
            self.textEdit = CSpellCheckTextEdit(self.splitter)
            self.textEdit.setObjectName('textEdit')
            self.textEdit.setFocusPolicy(Qt.WheelFocus)
            self.textEdit.setTabChangesFocus(True)
            self.gridlayout.addWidget(self.splitter,0,0,1,1)
            self.actSelectAll = QtGui.QAction(self)
            self.actSelectAll.setShortcut(QtGui.QKeySequence.SelectAll)
            self.treeView.addAction(self.actSelectAll)
            self.actFindNextPlaceholder = QtGui.QAction(self)
            self.actFindNextPlaceholder.setShortcut('Alt+Y')
            self.treeView.addAction(self.actFindNextPlaceholder)
            self.textEdit.addAction(self.actFindNextPlaceholder)
            self.setFocusProxy(self.treeView)
            self.connect(self.treeView, SIGNAL('doubleClicked(QModelIndex)'), self.on_doubleClicked)
            self.connect(self.actSelectAll, SIGNAL('triggered()'), self.textEdit.selectAll)
            self.connect(self.actFindNextPlaceholder, SIGNAL('triggered()'), self.findNextPlaceholder)
            self.textEdit.installEventFilter(self)
            self.treeView.installEventFilter(self)
            self.previousBranchMainId = None
            self.isValueDomain = isValueDomain


        def eventFilter(self, widget, event):
            et = event.type()
            if et == QEvent.FocusOut:
                fw = QtGui.qApp.focusWidget()
                if not (fw and self.isAncestorOf(fw)):
                    self.emit(SIGNAL('editingFinished()'))
            elif et == QEvent.Hide and widget == self.textEdit:
                self.emit(SIGNAL('commit()'))
            return QtGui.QWidget.eventFilter(self, widget, event)


        def focusNextPrevChild(self, next):
            if self.treeView.hasFocus() and next:
                self.textEdit.setFocus(Qt.TabFocusReason)
                return True
            elif self.textEdit.hasFocus() and not next:
                self.treeView.setFocus(Qt.BacktabFocusReason)
                return True
            # self.emit(SIGNAL('commit()'))
            self.setFocusProxy(self.textEdit if next else self.treeView) # иначе что-то "проскакивает" мимо.
            QtGui.QWidget.focusNextPrevChild(self, next)
            return True


        def setValue(self, value):
            v = forceString(value)
            self.textEdit.setPlainText(v)
            self.textEdit.moveCursor(QtGui.QTextCursor.End)


        def value(self):
            return unicode(self.textEdit.toPlainText())


        def getCurrentBranchMainId(self, item):
            if item:
                tmpItem = None
                while item.parent() and item.parent().id():
                    tmpItem = item
                    item = item.parent()
                return item.id() if item.parent() else tmpItem.id() if tmpItem else None
            return None


        def on_doubleClicked(self, index):
            db = QtGui.qApp.db
            table = db.table('rbThesaurus')
            item = index.internalPointer()
            text = '%s'
            while item and item.id():
                template = forceString(db.translate(table, 'id', item.id(), 'template'))
                try:
                    text = text % template
                except:
                    break
                item = item.parent()
            try:
                text = text % ''
            except:
                pass
            cursor = self.textEdit.textCursor()
            keepPosition = False
            if cursor.hasSelection():
                pos = cursor.selectionStart()
                cursor.removeSelectedText()
                cursor.setPosition(pos)
                keepPosition = True
            elif cursorInPlaceholder(cursor):
                keepPosition = True
            elif not cursor.atBlockStart():
                moveCursorToEndOfWord(cursor)
                if separatorBeforeCursor(cursor):
                    cursor.insertText(' ')
                else:
                    cursor.insertText(', ')
            currentBranchMainId = self.getCurrentBranchMainId(index.internalPointer())
            setFromNewBranch = (self.previousBranchMainId and self.previousBranchMainId != currentBranchMainId)
            self.previousBranchMainId = currentBranchMainId
            if not keepPosition and setFromNewBranch and trim(self.textEdit.toPlainText()) != '':
                cursor.insertText('\n')
            pos = cursor.position
            text = removeUsedPrefix(cursor, text)
            pos = cursor.position()
            cursor.insertText(text)
            placeholder = re.search(PLACEHOLDER, text)
            if placeholder:
                cursor.setPosition(pos+placeholder.start())
                cursor.setPosition(pos+placeholder.end(), cursor.KeepAnchor)
            self.textEdit.setTextCursor(cursor)


        def findNextPlaceholder(self):
            cursor = self.textEdit.textCursor()
            if QtGui.qApp.focusWidget() != self.textEdit:
                self.textEdit.setFocus(Qt.OtherFocusReason)
                cursor.clearSelection()
            text = unicode(self.textEdit.toPlainText())
            if setCursorToNextPlaceholder(cursor, text):
                self.textEdit.setTextCursor(cursor)


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceString(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+CStringActionPropertyValueType.name

