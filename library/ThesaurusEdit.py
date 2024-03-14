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

import re

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, SIGNAL

from library.TreeModel       import CDBTreeItem, CDBTreeModel
from library.Utils           import forceString


PLACEHOLDER = r'(_+\w*_+)|(_+)|(\[\w*\])'

def cursorInPlaceholder(cursor):
    position = cursor.position()
    cursor.select(QtGui.QTextCursor.WordUnderCursor)
    selectedText = unicode(cursor.selectedText())
    bot = selectedText[:1]
    eot = selectedText[-1:]
    result = bot == '_' and eot == '_' or bot == '[' and eot == ']'
    if result:
        position = cursor.selectionStart()
        cursor.removeSelectedText()
    cursor.setPosition(position)
    return result


def moveCursorToEndOfWord(cursor):
    position = cursor.position()
    cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
    selectedText = unicode(cursor.selectedText()).rstrip()
    cursor.setPosition(position)
    if selectedText and not selectedText.isspace():
        cursor.movePosition(QtGui.QTextCursor.EndOfWord)


def separatorBeforeCursor(cursor):
    position = cursor.position()
    cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
    selectedText = unicode(cursor.selectedText()).rstrip()
    cursor.setPosition(position)
    lastChar = selectedText[-1:]
    return lastChar in ':,;.?!([{</|'


def removeUsedPrefix(cursor, text):
    if ':' in text:
        position = cursor.position()
        cursor.movePosition(QtGui.QTextCursor.StartOfBlock, QtGui.QTextCursor.KeepAnchor)
        selectedText = unicode(cursor.selectedText())
        cursor.setPosition(position)
        parts = text.split(':')
        for x in range(len(parts)-1,0,-1):
            prefix = ':'.join(parts[:x])
            if prefix in selectedText:
                return ':'.join(parts[x:])
    return text


def setCursorToNextPlaceholder(cursor, text, backward=False):
    position = cursor.position()
    if cursor.hasSelection():
        selection = cursor.selectionStart(), cursor.selectionEnd()
    else:
        selection = None
    placeholders = [(f.start(), f.end()) for f in re.finditer(PLACEHOLDER, text)]
    placeholderSelection = None
    if backward:
        for start, end in reversed(placeholders):
            if (start<=position<=end and (start, end) != selection) or position > start:
                placeholderSelection = start, end
                break
        if placeholderSelection is None and placeholders:
            placeholderSelection = placeholders[-1]
    else:
        for start, end in placeholders:
            if (start<=position<=end and (start, end) != selection) or position < start:
                placeholderSelection = start, end
                break
        if placeholderSelection is None and placeholders:
            placeholderSelection = placeholders[0]
    if placeholderSelection:
        start, end = placeholderSelection
        cursor.setPosition(start)
        cursor.setPosition(end, cursor.KeepAnchor)
    return bool(placeholderSelection)


# ##############################################


class CThesaurusTreeView(QtGui.QTreeView):
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.readOnly = False


    def setReadOnly(self, value=False):
        self.readOnly = value
        self.model().setReadOnly(self.readOnly)


    def isReadOnly(self):
        return self.readOnly


    def keyPressEvent(self, event):
        if self.model().isReadOnly():
            event.accept()
        elif event.key() == Qt.Key_Space:
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
        else:
            QtGui.QTreeView.keyPressEvent(self, event)


class CThesaurusEditor(QtGui.QWidget):
    __pyqtSignals__ = ('editingFinished()',
                       'commit()',
                      )
    def __init__(self, parent):
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

        self.treeView = CThesaurusTreeView(self.splitter)
        self.treeView.setObjectName('treeView')
        self.domain = u''


    def getThesaurus(self, propertyType):
        db = QtGui.qApp.db
        table = db.table('rbThesaurus')
        tableAPT = db.table('ActionPropertyType')
        if propertyType == 1:
            name = u'Объективность'
        elif propertyType == 2:
            name = u'Слизистая'
        record = db.getRecordEx(tableAPT, [tableAPT['valueDomain']], [tableAPT['deleted'].eq(0), tableAPT['name'].like(name), tableAPT['typeName'].like(u'Constructor')])
        if record:
            self.domain = forceString(record.value('valueDomain'))
        rootItemIdCandidates = db.getIdList(table, 'id', [table['group_id'].isNull(), table['code'].eq(self.domain)], 'id')
        # если в корне не нашлось, ищем в прочих.
        if not rootItemIdCandidates:
            rootItemIdCandidates = db.getIdList(table, 'id', table['code'].eq(self.domain), 'id')
        rootItemId = rootItemIdCandidates[0] if rootItemIdCandidates else None
        self.treeModel = CDBTreeModel(self, 'rbThesaurus', 'id', 'group_id', 'name', order='code')
        self.treeModel.setRootItem(CDBTreeItem(None, self.domain, rootItemId, self.treeModel))
        self.treeModel.setRootItemVisible(False)
        self.treeModel.setLeavesVisible(True)
        self.treeView.setModel(self.treeModel)
        self.treeView.header().setVisible(False)
        self.textEdit = QtGui.QTextEdit(self.splitter)
        self.textEdit.setObjectName('textEdit')
        self.textEdit.setFocusPolicy(Qt.StrongFocus)
        self.textEdit.setTabChangesFocus(True)
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        self.setFocusProxy(self.treeView)
        self.connect(self.treeView, SIGNAL('doubleClicked(QModelIndex)'), self.on_doubleClicked)
        self.textEdit.installEventFilter(self)
        self.treeView.installEventFilter(self)


    def eventFilter(self, widget, event):
        if self.treeView.model().isReadOnly():
            event.accept()
            return False
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
        self.setFocusProxy(self.textEdit if next else self.treeView)
        QtGui.QWidget.focusNextPrevChild(self, next)
        return True


    def setValue(self, value):
        v = forceString(value)
        self.textEdit.setPlainText(v)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)


    def value(self):
        return unicode(self.textEdit.toPlainText())


    def on_doubleClicked(self, index):
        if not self.treeView.isReadOnly():
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
            if cursor.hasSelection():
                pos = cursor.selectionStart()
                cursor.removeSelectedText()
                cursor.setPosition(pos)
            elif cursorInPlaceholder(cursor):
                pass
            elif not cursor.atBlockStart():
                moveCursorToEndOfWord(cursor)
                if separatorBeforeCursor(cursor):
                    cursor.insertText(' ')
                else:
                    cursor.insertText(', ')
            cursor.insertText(removeUsedPrefix(cursor, text))
            self.textEdit.setTextCursor(cursor)
