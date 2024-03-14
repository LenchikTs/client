# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QModelIndex, QPersistentModelIndex


def isExpandable(modelIndex):
    return modelIndex.model().rowCount(modelIndex)>0


def isSelectable(modelIndex):
    flags = modelIndex.flags()
    return flags & Qt.ItemIsEnabled and flags & Qt.ItemIsSelectable


class CTreeComboBoxView(QtGui.QTreeView):
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.setUniformRowHeights(True)
        self.setRootIsDecorated(True)
        self.setItemsExpandable(True)
        #self.setSortingEnabled(True)
        self.setSelectionBehavior(QtGui.QTreeView.SelectRows)
        self.header().setVisible(False)
        self.setMinimumHeight(150)
#        self.connect(self, SIGNAL('expanded(QModelIndex)'), self.onExpanded)


    def expandAllFromIndex(self, index):
        blockSignals = self.blockSignals(True)
        try:
            rowCount = self.model().rowCount
            toExpand = [ index ]
            while toExpand:
                index = toExpand.pop()
                if index.isValid():
                    self.expand(index)
                    for i in xrange(rowCount(index)):
                        toExpand.append( index.child(i, 0) )
        finally:
            self.blockSignals(blockSignals)


    def expandUp(self, index):
        blockSignals = self.blockSignals(True)
        try:
            self.expandToDepth(0)
            if index and index.isValid():
                index = index.parent()
                while index and index.isValid():
                    self.expand(index)
                    index = index.parent()
        finally:
            self.blockSignals(blockSignals)


class CTreeComboBox(QtGui.QComboBox):
    __pyqtSignals__ = ('valueChanged()',
                      )
    # предполагается, что в наследниках этого класса
    # достаточно написать свою модель + сделать self.setModel
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self._view = CTreeComboBoxView()
        self._currentModelIndex = None
        self._selectedModelIndex = None
        self._expandAll = False
        self._expandDepth = 0
        self._preferredWidth = 0
        self._preferredHeight = 0
        self.setView(self._view)
#        self._view.installEventFilter(self)
#        self._view.viewport().installEventFilter(self)


    def setExpandAll(self, value):
        self._expandAll = value

    def expandToDepth(self, value):
        self._expandDepth = value

    def setPreferredWidth(self, value):
        self._preferredWidth = value


    def setPreferredHeight(self, value):
        self._preferredHeight = value


    def eventFilter(self, watched, event):
        # 1. Суета с MouseButtonPress/MouseButtonRelease обусловлена
        # желанием получить возможность открывать/закрывать узлы
        # дерева мышью. При этом механизм "skipNextHide" признан
        # не вполне подходящим, так как поведение оказывается
        # сильно отличающимся от обычного QComboBox
        # 2. Суета с KeyPress обусловлена особенностью реализации
        # поиска - в обычной реализации символы '-', '+' и '*'
        # сначала приводят к изменению дерева, а потом - ищутся как
        # обычные буквы.

        def conditionalShiftUp(view, index):
            if event.modifiers() & Qt.ShiftModifier:
                view.scrollTo(index, QtGui.QAbstractItemView.PositionAtTop)

        view = self._view

        if event.type() == QEvent.MouseButtonPress and watched == view.viewport():
            pos = event.pos()
            index = view.indexAt(pos)
            if index.isValid() and not view.visualRect(index).contains(pos):
                if isExpandable(index):
                    view.setExpanded(index, not view.isExpanded(index))
                    if view.isExpanded(index):
                        conditionalShiftUp(view, index)
            return True # filter out
        elif event.type() == QEvent.MouseButtonRelease and watched == view.viewport():
            pos = event.pos()
            index = view.indexAt(pos)
            if index.isValid() and view.visualRect(index).contains(pos) and isSelectable(index):
                self._selectedModelIndex = index
                self.hidePopup()
            return True
        if event.type() in [QEvent.KeyPress, QEvent.ShortcutOverride] and watched == view:
            key = event.key()
            index = view.currentIndex()
            if key == Qt.Key_Minus:
                view.collapse(index)
                return True
            elif key == Qt.Key_Plus:
                if isExpandable(index):
                    view.expand(index)
                    conditionalShiftUp(view, index)
                return True
            elif key == Qt.Key_Asterisk:
                if isExpandable(index):
                    view.expandAllFromIndex(index)
                    conditionalShiftUp(view, index)
                return True
            elif key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Select):
#                print 'key Enter/Return/Select'
                if isSelectable(index):
                    self._selectedModelIndex = view.currentIndex()
#                    print '[2]self._selectedModelIndex=', repr(self._selectedModelIndex)
                    self.hidePopup()
                return True
            elif key in (Qt.Key_Escape, Qt.Key_F4):
                self.hidePopup()
                return True
        return False


    def showPopup(self):
        # возня с installEventFilter/removeEventFilter
        # обусловлена тем, что при использовании Qt 4.6/4.7/4.8 и PyQt 4.9
        # в windows время от времени происходит segmentationFault.
        # Исследование показало, что это связано с установкой
        # view().viewport().installEventFilter(self)
        # в конструкторе. Поэтому я перенёс этот код в showPopup
        # и добавил removeEventFilter в hidePopup.
        # Так не падает.
        self.setRootModelIndex(QModelIndex())
        if self._expandAll:
            self._view.expandAll()
        else:
            if self._expandDepth:
                self._view.expandToDepth(self._expandDepth)
            else:
                self._view.expandUp(self.currentModelIndex())


        # устанавливаем ширину по максимальной длине элемента (переход на подуровень по ширине как 4 пробела + 3 пробела на скроллбар)
        items = ["    "*(level+1) + name + "   " for (name, level) in self.model().items()]
        itemLenghts = [self._view.fontMetrics().width(item) for item in items]
        preferredWidth = max(max(itemLenghts), self._preferredWidth, self._view.sizeHint().width())

        # на маленьком разрешениии, часть попапа пропадает за пределами экрана
        # ограничиваем его размер до ширины активного окна - 5%
        if preferredWidth > self.window().width():
            preferredWidth = self.window().width() - self.window().width() * 0.05
            #self._view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            #self._view.setTextElideMode(QtCore.Qt.ElideNone)
        if preferredWidth:
            if self.width() < preferredWidth:
                self._view.setFixedWidth(preferredWidth)
        if self._preferredHeight:
            self._view.setMinimumHeight(self._preferredHeight)
        self._view.installEventFilter(self)
        self._view.viewport().installEventFilter(self)
        self._selectedModelIndex = None
        QtGui.QComboBox.showPopup(self)
        scrollBar = self._view.horizontalScrollBar()
        scrollBar.setValue(0)


    def hidePopup(self):
        if self._view.isVisible():
            self._view.removeEventFilter(self)
            self._view.viewport().removeEventFilter(self)
        QtGui.QComboBox.hidePopup(self)
        if self._selectedModelIndex:
            self.setCurrentModelIndex(self._selectedModelIndex)
            self._selectedModelIndex = None


    def currentModelIndex(self):
        return QModelIndex(self._currentModelIndex) if self._currentModelIndex else QModelIndex()


    def setCurrentModelIndex(self, modelIndex):
        if modelIndex and modelIndex.isValid():
            if modelIndex != self._currentModelIndex:
                self._currentModelIndex = QPersistentModelIndex(modelIndex)
                self.setRootModelIndex(modelIndex.parent())
                self.setCurrentIndex(modelIndex.row())
                self.emitValueChanged()
        else:
            if self._currentModelIndex is not None:
                self._currentModelIndex = None
                self.setRootModelIndex(QModelIndex())
                self.setCurrentIndex(0)
                self.emitValueChanged()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.showPopup()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)


    def emitValueChanged(self):
        self.emit(SIGNAL('valueChanged()'))


class CTreeComboBoxGetIdSetIdMixin:
    def setValue(self, id):
        index = self._model.findItemId(id)
        if index:
            self.setCurrentModelIndex(index)


    def value(self):
        modelIndex = self.currentModelIndex()
        if modelIndex and modelIndex.isValid():
            return self._model.itemId(modelIndex)
        return None
