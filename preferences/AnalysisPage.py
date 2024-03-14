# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница выбора отчетов для руководителя
##
#############################################################################

from PyQt4              import QtGui, QtCore
from library.Utils      import forceString, forceRef, forceBool, toVariant
from library.database   import decorateString
from Users.Rights       import (urAccessSetupGlobalPreferencesWatching,
                                urAccessSetupGlobalPreferencesEdit,
                                urAdmin)


menuNameExceptions = (
    u'Отчеты для руководителя',
    u'Генератор отчётов',
)


class CTreeWidgetBase(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.setHeaderHidden(True)


    def findByObjectName(self, title, objectName):
        # рекурсивный поиск элемента в дереве по названию и objectName
        flags = QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive
        for foundItem in self.findItems(title, flags):
            if foundItem.objectName == objectName:
                return foundItem
        return None


    def addAllItemsFromMenu(self, checkedNames, reverseCheckState=False, groupCheckable=False):
        win = QtGui.qApp.mainWindow
        items = win.getMenuTree(win.mnuReports)
        self.addItemsFromMenu(items, self.invisibleRootItem(), checkedNames, reverseCheckState, groupCheckable)


    def addItemsFromMenu(self, items, parent, checkedNames, reverseCheckState=False, groupCheckable=False):
        for action, submenu in items.iteritems():
            text, objectName = action
            if text in menuNameExceptions:
                continue
            if submenu is None:
                item = CTreeWidgetItem(parent, text, objectName, isGroup=False)
                if reverseCheckState:
                    checked = objectName not in checkedNames
                else:
                    checked = objectName in checkedNames
                item.setCheckState(0, QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)
            else:
                item = CTreeWidgetItem(parent, text, objectName, isGroup=True)
                self.addItemsFromMenu(submenu, item, checkedNames, reverseCheckState, groupCheckable)
                if groupCheckable:
                    if reverseCheckState:
                        checked = objectName not in checkedNames
                    else:
                        checked = objectName in checkedNames
                    item.setCheckState(0, QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)


    def getChildsWithHierarchy(self, item=None):
        # получить список потомков, где каждая группа собрана в кортеж:
        # (потомок: CTreeWidgetItem, (потомок_потомка, ..., (..., ...)))
        if item is None:
            item = self.invisibleRootItem()
        result = []
        for i in xrange(item.childCount()):
            child = item.child(i)
            result.append((child, self.getChildsWithHierarchy(child)))
        return result


    def getChilds(self, item=None):
        # получить всех потомков одним списком
        result = []
        if item is None:
            item = self.invisibleRootItem()
        else:
            result.append(item)
        for i in xrange(item.childCount()):
            child = item.child(i)
            result.append(child)
            result.extend(self.getChilds(child))
        return result


class CReportsVisibleTree(CTreeWidgetBase):
    def __init__(self, parent=None):
        CTreeWidgetBase.__init__(self, parent)
        self.itemClicked.connect(self.on_itemClicked)


    def on_itemClicked(self, item, column):
        checkState = item.checkState(0)
        for i in xrange(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, checkState)
            self.on_itemClicked(child, column)


class CChiefTree(CTreeWidgetBase):
    def __init__(self, parent=None):
        CTreeWidgetBase.__init__(self, parent)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.menu = QtGui.QMenu(self)
        self.actCreate = self.menu.addAction(u'Создать групу')
        self.actRename = self.menu.addAction(u'Переименовать группу')
        self.actDelete = self.menu.addAction(u'Удалить группу')
        self.actCreate.triggered.connect(self.on_actCreate_triggered)
        self.actRename.triggered.connect(self.on_actRename_triggered)
        self.actDelete.triggered.connect(self.on_actDelete_triggered)


    def dropEvent(self, event):
        if self.dropIndicatorPosition() == QtGui.QAbstractItemView.OnItem:
            item = self.itemAt(event.pos())
            if not item.isGroup:
                event.setDropAction(QtCore.Qt.IgnoreAction)
        QtGui.QTreeWidget.dropEvent(self, event)


    def contextMenuEvent(self, event):
        item = self.currentItem()
        enabled = bool(item) and item.isGroup
        self.actRename.setEnabled(enabled)
        self.actDelete.setEnabled(enabled)
        self.menu.exec_(event.globalPos())


    def removeEmptyGroups(self):
        itemsToDelete = []
        it = QtGui.QTreeWidgetItemIterator(self)
        while it.value():
            item = it.value()
            if item.childCount() == 0 and item.isGroup:
                itemsToDelete.append(item)
            it += 1
        for item in itemsToDelete:
            parent = item.parent()
            if not parent:
                parent = self.invisibleRootItem()
            parent.removeChild(item)


    def addChiefItems(self, item, records, groupId):
        if item is None:
            item = self.invisibleRootItem()
        for record in records:
            itemId = forceRef(record.value('id'))
            parentId = forceRef(record.value('parent_id'))
            title = forceString(record.value('title'))
            objectName = forceString(record.value('objectName'))
            if parentId != groupId:
                continue
            newItem = CTreeWidgetItem(item, title.split('/')[-1], objectName)
            if objectName:
                item.addChild(newItem)
            else:
                self.addChiefItems(newItem, records, itemId)


    def on_actCreate_triggered(self):
        text, ok = QtGui.QInputDialog.getText(
            self, u'Создание группы', u'Наименование группы')
        if not ok:
            return
        # в группах, созданных пользователем, objectName должен быть пустым
        group = CTreeWidgetItem(None, text, '', True)
        self.invisibleRootItem().addChild(group)


    def on_actRename_triggered(self):
        item = self.currentItem()
        text, ok = QtGui.QInputDialog.getText(
            self, u'Переименование группы', u'Наименование группы', text=item.title)
        if not ok:
            return
        item.setText(0, text)


    def on_actDelete_triggered(self):
        item = self.currentItem()
        parent = item.parent()
        if not parent:
            parent = self.invisibleRootItem()
        parent.removeChild(item)


class CAnalysisPage(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName('analysisPage')
        self.setWindowTitle(u'Анализ')
        self.tree = CTreeWidgetBase(self)
        self.chiefTree = CChiefTree(self)
        self.reportsVisibleTree = CReportsVisibleTree(self)
        self.chkInheritGroups = QtGui.QCheckBox(u'Наследовать группы')

        tabReportsChief = QtGui.QWidget()
        splitter = QtGui.QSplitter()
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.chiefTree)
        layout = QtGui.QVBoxLayout(tabReportsChief)
        layout.addWidget(self.chkInheritGroups)
        layout.addWidget(splitter)

        tabWidget = QtGui.QTabWidget(self)
        tabWidget.addTab(tabReportsChief, u'Отчеты для руководителя')
        tabWidget.addTab(self.reportsVisibleTree, u'Настройка видимости отчетов')

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(tabWidget)

        tabWidget.setTabEnabled(1, QtGui.qApp.userHasAnyRight([
            urAccessSetupGlobalPreferencesWatching,
            urAccessSetupGlobalPreferencesEdit,
            urAdmin,
        ]))
        self.reportsVisibleTree.setEnabled(QtGui.qApp.userHasAnyRight([
            urAccessSetupGlobalPreferencesEdit,
            urAdmin,
        ]))
        self.tree.itemClicked.connect(self.on_tree_itemClicked)


    def on_tree_itemClicked(self, item, column):
        foundItem = self.chiefTree.findByObjectName(item.title, item.objectName)
        if item.checkState(0) == QtCore.Qt.Checked and not foundItem:
            newItem = CTreeWidgetItem(None, item.title, item.objectName)
            self.chiefTree.invisibleRootItem().addChild(newItem)
        if item.checkState(0) == QtCore.Qt.Unchecked and foundItem:
            parent = foundItem.parent()
            if not parent:
                parent = self.chiefTree.invisibleRootItem()
            parent.removeChild(foundItem)


    def makeReportChiefInsertValues(self, items, currentId=1, parentId=None):
        values = []
        for item, itemChilds in items:
            if self.chkInheritGroups.isChecked():
                i = self.tree.findByObjectName(item.title, item.objectName)
                if i is None:
                    title = decorateString(item.title)
                else:
                    title = decorateString(i.inheritedTitle)
            else:
                title = decorateString(item.title)
            objectName = decorateString(item.objectName)
            parent = parentId if parentId else 'NULL'
            values.append('(%s,%s,%s,%s)' % (currentId, parent, title, objectName))
            currentId += 1
            subValues = self.makeReportChiefInsertValues(itemChilds, currentId, currentId-1)
            values.extend(subValues)
            currentId += len(subValues)
        return values


    def makeReportsToHideInsertValues(self):
        objectNames = set()
        for item in self.reportsVisibleTree.getChilds():
            if item.checkState(0) == QtCore.Qt.Unchecked:
                if item.objectName:
                    objectNames.add(item.objectName)

        return ['(%d,%s)' % (i + 1, decorateString(name)) for i, name in enumerate(objectNames)]


    def getProps(self, props):
        # использую для сохранения отмеченных пунктов
        props['inheritGroups'] = toVariant(self.chkInheritGroups.isChecked())
        db = QtGui.qApp.db

        self.chiefTree.removeEmptyGroups()
        values = self.makeReportChiefInsertValues(self.chiefTree.getChildsWithHierarchy())
        db.query('DELETE FROM `ReportsChiefActions`')
        if values:
            stmt = 'INSERT INTO `ReportsChiefActions` VALUES ' + ','.join(values)
            db.query(stmt)

        values = self.makeReportsToHideInsertValues()
        # отображаем ранее скрытые отчеты перед очисткой таблицы ReportsToHide
        QtGui.qApp.mainWindow.setSelectedReportsVisible(True)
        db.query('DELETE FROM `ReportsToHide`')
        if values:
            stmt = 'INSERT INTO `ReportsToHide` VALUES ' + ','.join(values)
            db.query(stmt)


    def setProps(self, props):
        # использую для загрузки отмеченных пунктов
        self.chkInheritGroups.setChecked(forceBool(props.get('inheritGroups', False)))

        db = QtGui.qApp.db
        records = db.getRecordList('ReportsChiefActions')
        checkedNames = set()
        for record in records:
            checkedNames.add(forceString(record.value('objectName')))
        self.tree.addAllItemsFromMenu(checkedNames)
        self.chiefTree.addChiefItems(None, records, None)

        records = db.getRecordList('ReportsToHide')
        checkedNames = set()
        for record in records:
            checkedNames.add(forceString(record.value('objectName')))
        self.reportsVisibleTree.addAllItemsFromMenu(checkedNames, reverseCheckState=True, groupCheckable=True)



class CTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, title, objectName, isGroup=False):
        title = title.replace('&', '')
        QtGui.QTreeWidgetItem.__init__(self, parent, [title])
        self._objectName = objectName
        self._isGroup = isGroup

    @property
    def objectName(self):
        return self._objectName

    @property
    def isGroup(self):
        return self._isGroup or self.childCount() > 0

    @property
    def title(self):
        return forceString(self.text(0))

    @property
    def inheritedTitle(self):
        name = self.title
        parent = self.parent()
        while parent:
            name = parent.title + '/' + name
            parent = parent.parent()
        return name
