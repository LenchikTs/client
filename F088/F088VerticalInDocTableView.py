# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QVariant, QSize, QString, SIGNAL, QEvent, QObject

from library.InDocTable import CInDocTableView, CLocItemDelegate
from library.Utils      import forceString

updateEditorHeight = 4
updateRowHeight = 1

class CVerticalHeaderView(QtGui.QHeaderView):
    def __init__(self, orientation, parent=None):
        QtGui.QHeaderView.__init__(self, orientation, parent)


    def sectionSizeFromContents(self, logicalIndex):
        model = self.model()
        if model:
            orientation = self.orientation()
            opt = QtGui.QStyleOptionHeader()
            self.initStyleOption(opt)
            var = model.headerData(logicalIndex, orientation, Qt.FontRole)
            if var and var.isValid() and var.type() == QVariant.Font:
                fnt = var.toPyObject()
            else:
                fnt = self.font()
            opt.fontMetrics = QtGui.QFontMetrics(fnt)
            sizeText = QSize(0,4)
            opt.text = model.headerData(logicalIndex, orientation, Qt.DisplayRole).toString()
            sizeText = self.style().sizeFromContents(QtGui.QStyle.CT_HeaderSection, opt, sizeText, self)
            sizeFiller = QSize(0,4)
            opt.text = QString('x'*CF088VerticalInDocTableView.titleWidth)
            sizeFiller = self.style().sizeFromContents(QtGui.QStyle.CT_HeaderSection, opt, sizeFiller, self)
            return QSize(min(sizeText.width(), sizeFiller.width()),
                         max(sizeText.height(), sizeFiller.height())
                        )
        else:
            return QtGui.QHeaderView.sectionSizeFromContents(self, logicalIndex)


class CLocVerticalItemDelegate(CLocItemDelegate):
    def __init__(self, parent, lineHeight):
        CLocItemDelegate.__init__(self, parent)
        self.lineHeight = lineHeight


    def createEditor(self, parent, option, index):
        editor = QtGui.QTextEdit(parent)
        editor.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        editor.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        editor.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.connect(editor, SIGNAL('commit()'), self.emitCommitData)
        self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
        self.editor = editor
        self.row = index.row()
        self.rowcount = index.model().rowCount(None)
        self.column = index.column()
        return editor


    def editorEvent(self, event, model, option, index):
        return QtGui.QItemDelegate.editorEvent(self, event, model, option, index)


    def eventFilter(self, editor, event):
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter) and isinstance(editor, QtGui.QTextEdit):
                return False
        return QtGui.QItemDelegate.eventFilter(self, editor, event)


    def updateEditorGeometry(self, editor, option, index):
        QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index)
        index.model().afterUpdateEditorGeometry(editor, index)
        if isinstance(editor, QtGui.QTextEdit):
            height = editor.height()
            if editor.height() <= ((3*self.lineHeight/2 + 1))*2:
                height = 2*editor.height()
            editor.resize(editor.width(), height)


    def sizeHint(self, option, index):
        model = index.model()
        row = index.row()
        heightRow = self.lineHeight
        result = QSize(10, self.lineHeight*updateRowHeight)
        if row >= 0 and row < len(model._items):
            record = model._items[row]
            heightMaxRow = self.getHeightMaxRow(record)
            preferredHeight = min(heightMaxRow, updateEditorHeight)*heightRow
            result = QSize(10, preferredHeight if preferredHeight else self.lineHeight*updateRowHeight)
        return result


    def getHeightMaxRow(self, record):
        heightMaxRow = 0
        parentWidget = QObject.parent(self)
        freeInput = forceString(record.value('freeInput'))
        if freeInput:
            freeInputStr = QString(freeInput)
            freeInputList = freeInputStr.split(u'\n')
            heightMaxRow = len(freeInputList)
            if parentWidget:
                colWidth = parentWidget.columnWidth(parentWidget.columnHint)*1.0
            else:
                colWidth = 256.0
                fm = QtGui.QFontMetrics(QtGui.QFont())
            for freeInputPar in freeInputList:
                lenPx = 0.0
                lenFreeInput = len(freeInputPar)-1
                if parentWidget:
                    for i in range(lenFreeInput):
                        lenPx += parentWidget.fontMetrics().width(QString(freeInputPar).at(i))
                else:
                    for i in range(lenFreeInput):
                        lenPx += fm.width(QString(freeInputPar).at(i))
                cnt = round(lenPx/(colWidth if colWidth else 1.0))
                propertyLine = cnt if cnt > 0 else 0
                heightMaxRow += propertyLine
        return heightMaxRow


class CF088VerticalInDocTableView(CInDocTableView):
    titleWidth = 0
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.parent = parent
        self.columnHint = 2
        h = self.fontMetrics().height()
        self._verticalHeader = CVerticalHeaderView(Qt.Vertical, self)
        self.setVerticalHeader(self._verticalHeader)
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.setWordWrap(True)
        self.verticalItemDelegate = CLocVerticalItemDelegate(self, h)
        self.setItemDelegateForColumn(self.columnHint, self.verticalItemDelegate)


    def sizeHintForRow(self, row):
        model = self.model()
        if model:
            index = model.index(row, self.columnHint)
            return self.verticalItemDelegate.sizeHint(None, index).height()*1+1
        return -1


class CF088_30_1VerticalInDocTableView(CInDocTableView):
    titleWidth = 0
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.parent = parent
        self.columnHint = 2
        h = self.fontMetrics().height()
        self._verticalHeader = CVerticalHeaderView(Qt.Vertical, self)
        self.setVerticalHeader(self._verticalHeader)
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.setWordWrap(True)
        self.verticalHeader().setStretchLastSection(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.verticalItemDelegate = CLocVerticalItemDelegate(self, h)
        self.setItemDelegateForColumn(self.columnHint, self.verticalItemDelegate)


    def sizeHintForRow(self, row):
        model = self.model()
        if model:
            index = model.index(row, self.columnHint)
            return self.verticalItemDelegate.sizeHint(None, index).height()*1+1
        return -1

