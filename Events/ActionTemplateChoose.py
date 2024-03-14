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
from PyQt4.QtCore import Qt, QEvent, QModelIndex, QObject, QSize, SIGNAL, QVariant

from Events.Action import CActionTypeCache
from library.AgeSelector import checkAgeSelector, parseAgeSelector
from library.TreeModel import CDBTreeItem, CTreeModel
from library.Utils import forceInt, forceRef, forceString, forceStringEx, forceBool, toVariant

from RefBooks.ActionTemplate.List import deleteActionTemplateAndDescendants
from Users.Rights import urAdmin, urAccessRefBooks, urAccessRefAccount, urAccessRefAccountActionTemplate


class CActionTemplateTreeItem(CDBTreeItem):
    def __init__(self, parent, name, id, model, actionId, filter, isValidEx=True, typeDialog=0):
        CDBTreeItem.__init__(self, parent, name, id, model)
        self._actionId = actionId
        self._filter = filter
        self._isValidEx = isValidEx
        self.typeDialog = typeDialog
        self._selectable = actionId or not filter.removeEmptyNodes
        self._editable = True


    def flags(self):
        if self._isValidEx or not self._filter.removeEmptyNodes:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.NoItemFlags


    def isEmpty(self):
        if self._isValidEx:
            return False
        for child in self.items():
            if not child.isEmpty():
                return False
        return True

    def loadChildren(self):
        result = []
        records = self.model.cachedRecords.get(self._id, [])
        for record in records:
            age = forceString(record.value('age'))
            id = forceRef(record.value('id'))
            name = forceString(record.value('name'))
            actionId = forceRef(record.value('action_id'))
            isValidEx = forceBool(record.value('isValidEx'))
            if age and self._filter.clientAge:
                if isValidEx and not checkAgeSelector(parseAgeSelector(age), self._filter.clientAge):
                    isValidEx = isValidEx and False
                    # continue
            child = CActionTemplateTreeItem(self, name, id, self.model, actionId, self._filter, isValidEx, self.typeDialog)
            if isValidEx or not child.isEmpty() or not self._filter.removeEmptyNodes:
                result.append(child)
        return result
    
    def setData(self, column, value):
        if column == 0:
            newName = forceString(value)
            if self._name != newName:
                id = self.id()
                db = QtGui.qApp.db
                table = db.table('ActionTemplate')
                record = db.getRecord(table, 'id, name', id)
                record.setValue('name', toVariant(newName))
                db.updateRecord(table, record)
                self._name = newName
                return True
        return False


class CActionTemplateRootTreeItem(CActionTemplateTreeItem):
    def __init__(self, model, filter, typeDialog=0):
        CActionTemplateTreeItem.__init__(self, None, u'-', None, model, None, filter, isValidEx=True, typeDialog=typeDialog)

    def loadChildren(self):
        result = []
        db = QtGui.qApp.db
        table = db.table('ActionTemplate')
        tableAction = db.table('Action')
        cols = [table['id'],
                table['name'],
                table['action_id'],
                table['age'],
                table['group_id']
                ]
        condSex = table['sex'].inlist([self._filter.clientSex, 0])
        condSpeciality = db.joinOr(
            [table['speciality_id'].eq(self._filter.specialityId), table['speciality_id'].isNull()])
        condOrgStructure = db.joinOr(
            [table['orgStructure_id'].eq(self._filter.orgStructureId), table['orgStructure_id'].isNull()])
        condSNILS = table['SNILS'].eq(self._filter.SNILS)
        condSNILSOr = db.joinOr([condSNILS, table['SNILS'].isNull()])
        condOwnerId = table['owner_id'].eq(self._filter.personId)
        condOwner = db.joinOr([condOwnerId, table['owner_id'].isNull()])
        condActionType = db.joinOr(
            [tableAction['actionType_id'].inlist(self._filter.actionTypeIdList), table['action_id'].isNull()])
        colsValidEx = []
        if self._filter.showTypeTemplate == 1:
            colsValidEx.append(table['owner_id'].eq(self._filter.personId))
        elif self._filter.showTypeTemplate == 2:
            if not self._filter.SNILS:
                colsValidEx.append(db.joinAnd([condOwnerId, table['SNILS'].isNull()]))
            else:
                colsValidEx.append(condSNILS)
        else:
            colsValidEx.append(condOwner)
            colsValidEx.append(condSNILSOr)
        if self._filter.actionTypeIdList:
            if self.typeDialog:
                colsValidEx.append(db.joinAnd([table['action_id'].isNotNull(), condActionType]))
            else:
                colsValidEx.append(condActionType)
        if self._filter.specialityId:
            colsValidEx.append(condSpeciality)
        if self._filter.orgStructureId:
            colsValidEx.append(condOrgStructure)
        if self._filter.clientSex:
            colsValidEx.append(condSex)
        cols.append(u'IF((%s), 1, 0) AS isValidEx' % (db.joinAnd(colsValidEx)))
        cond = [table['deleted'].eq(0),
                db.joinOr([condOwner, condSNILSOr])]
        if self._filter.actionTypeIdList:
            cond.append(condActionType)
        if self._filter.specialityId:
            cond.append(condSpeciality)
        if self._filter.orgStructureId:
            cond.append(condOrgStructure)
        if self._filter.clientSex:
            cond.append(condSex)
        queryTable = table.leftJoin(tableAction, db.joinAnd(
            [tableAction['id'].eq(table['action_id']), tableAction['deleted'].eq(0)]))
        query = db.query(db.selectStmt(queryTable, cols, where=cond, order=table['name'].name()))
        self.model.cachedRecords = dict()
        while query.next():
            record = query.record()
            groupId = forceRef(record.value('group_id'))
            if groupId is None:
                groupId = -1
            self.model.cachedRecords.setdefault(groupId, []).append(record)

        records = self.model.cachedRecords.get(-1, [])
        for record in records:
            age = forceString(record.value('age'))
            id = forceRef(record.value('id'))
            name = forceString(record.value('name'))
            actionId = forceRef(record.value('action_id'))
            isValidEx = forceBool(record.value('isValidEx'))
            if age and self._filter.clientAge:
                if isValidEx and not checkAgeSelector(parseAgeSelector(age), self._filter.clientAge):
                    isValidEx = isValidEx and False
                    # continue
            child = CActionTemplateTreeItem(self, name, id, self.model, actionId, self._filter, isValidEx, self.typeDialog)
            if isValidEx or not child.isEmpty() or not self._filter.removeEmptyNodes:
                result.append(child)
        return result


class CActionTemplateModel(CTreeModel):
    class CFilter:
        def __init__(self, actionTypeId, personId, orgStructureId, specialityId, SNILS, clientSex, clientAge, removeEmptyNodes, showTypeTemplate):
            db = QtGui.qApp.db
            if actionTypeId:
                actionTypeIdList = CActionTypeCache.getById(actionTypeId).getTestatorIdList()
                actionTypeIdList.append(actionTypeId)
                actionTypeIdList = db.getTheseAndParents('ActionType', 'group_id', actionTypeIdList)
            else:
                actionTypeIdList = []
            self.actionTypeIdList = actionTypeIdList
            self.personId = personId
            self.specialityId = specialityId
            self.SNILS = SNILS
            self.orgStructureId = orgStructureId
            self.clientSex = clientSex
            self.clientAge = clientAge
            self.showTypeTemplate = showTypeTemplate
            self.removeEmptyNodes = removeEmptyNodes

    def __init__(self, parent, actionTypeId, personId, orgStructureId, specialityId, SNILS, clientSex, clientAge, removeEmptyNodes=True, showTypeTemplate=0, typeDialog=0):
        CTreeModel.__init__(self, parent, CActionTemplateRootTreeItem(self, CActionTemplateModel.CFilter(actionTypeId, personId, orgStructureId, specialityId, SNILS, clientSex, clientAge, removeEmptyNodes, showTypeTemplate), typeDialog))
        self.rootItemVisible = False
        self.typeDialog = typeDialog
        self.cachedRecordsMap = {}


    def setFilter(self, actionTypeId, personId, orgStructureId, specialityId, SNILS, clientSex, clientAge, removeEmptyNodes=True, showTypeTemplate=0):
        self.getRootItem()._filter = CActionTemplateModel.CFilter(actionTypeId, personId, orgStructureId, specialityId, SNILS, clientSex, clientAge, removeEmptyNodes, showTypeTemplate)
        self.cachedRecordsMap = {}
        self.update()


    def filter(self):
        return self.getRootItem()._filter


    def update(self):
        self.getRootItem().removeChildren()
        # self.reset()


    def isEmpty(self):
        return self.getRootItem().isEmpty()


    def getShowTypeTemplate(self):
        return self.getRootItem()._filter.showTypeTemplate


class CActionTemplateTreeView(QtGui.QTreeView):
    def __init__(self, parent):
        QtGui.QTreeView.__init__(self, parent)
        self.header().hide()
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setMinimumHeight(300)
        self.setMinimumWidth(600)
        self.connect(self, SIGNAL('expanded(QModelIndex)'), self.onExpanded)
        # self.connect(self, SIGNAL('collapsed(QModelIndex)'), self.onCollapsed)
        self.searchString = ''
        self.searchParent = None
        if self.itemsEditable():
            self.contextMenu = QtGui.QMenu(self)
            self.renameAction = self.contextMenu.addAction(u"Переименовать")
            self.renameAction.triggered.connect(self.onRenameTriggered)
            self.deleteAction = self.contextMenu.addAction(u"Удалить")
            self.deleteAction.triggered.connect(self.onDeleteTriggered)
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.onMenuRequested)
            self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    

    @staticmethod
    def itemsEditable():
        return QtGui.qApp.userHasAnyRight([urAdmin, urAccessRefBooks, urAccessRefAccount, urAccessRefAccountActionTemplate])


    def setModel(self, model):
        QtGui.QTreeView.setModel(self, model)

        pref = QtGui.qApp.preferences
        props = pref.appPrefs
        expand = forceInt(props.get('treeActionTemplateExpand',  QVariant()))
        if not expand:
            self.collapseAll()
        elif expand == 1:
            self.expandAll()
        else:
            expandLevel = forceInt(props.get('treeActionTemplateExpandLevel',  QVariant(1)))
            self.expandToDepth(expandLevel)


    def setRootIndex(self, index):
        pass


    def setRealRootIndex(self, index):
        QtGui.QTreeView.setRootIndex(self, index)
        # self.expandAll()


    def onMenuRequested(self, point):
        index = self.indexAt(point)
        if index.isValid():
            self.contextMenu.exec_(self.mapToGlobal(point))
    

    def onRenameTriggered(self):
        self.edit(self.currentIndex())


    def onDeleteTriggered(self):
        index = self.currentIndex()
        item = index.internalPointer()
        id = item.id()
        if id:
            parentItem = item.parent()
            success, deleted = QtGui.qApp.call(None, deleteActionTemplateAndDescendants, (None, id))
            if deleted:
                parentItem.update()

    def onExpanded(self, index):
        self.scrollTo(index, QtGui.QAbstractItemView.PositionAtTop)


    def keyPressEvent(self, event):
        if self.state() == QtGui.QAbstractItemView.NoState:
            if event.key() == Qt.Key_Left or event.key() == Qt.Key_Minus:
                current = self.currentIndex()
                if self.isExpanded(current) and self.model().rowCount(current):
                    self.collapse(current)
                else:
                    self.setCurrentIndex(current.parent())
                    current = self.currentIndex()
                    self.collapse(current)
                    self.scrollTo(current, QtGui.QAbstractItemView.PositionAtTop)
                event.accept()
                return
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                event.accept()
                self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
                return
        return QtGui.QTreeView.keyPressEvent(self, event)



class CActionTemplatePopup(QtGui.QFrame):
    __pyqtSignals__ = ('templateSelected(int)',
                       'closePopup()',
                      )

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.treeView=CActionTemplateTreeView(self)
        self.widgetLayout = QtGui.QVBoxLayout(self)
        self.widgetLayout.setMargin(0)
        self.widgetLayout.setSpacing(0)
        self.widgetLayout.addWidget(self.treeView)
        self.connect(self.treeView, SIGNAL('doubleClicked(QModelIndex)'), self.on_doubleClicked)
        self.setLayout(self.widgetLayout)
        self.treeView.setFocus()


    def on_doubleClicked(self, index):
        item = index.internalPointer()
        self.emit(SIGNAL('templateSelected(int)'), item.id())
        self.close()


    def mousePressEvent(self, event):
        p = self.parentWidget()
        if p is not None:
            rect = p.rect()
            rect.moveTo(p.mapToGlobal(rect.topLeft()))
            if rect.contains(event.globalPos()) or self.rect().contains(event.pos()):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event):
        # self.emit(SIGNAL('resetButton()'))
        self.parent().mouseReleaseEvent(event)
        pass


    # def event(self, event):
    #     if event.type() == QEvent.KeyPress:
    #         if event.key() == Qt.Key_Escape:
    #             self.dateChanged = False
    #     return QFrame.event(self, event)


    def hideEvent(self, event):
        self.emit(SIGNAL('closePopup()'))


class CActionTemplateSelectButton(QtGui.QPushButton):
    __pyqtSignals__ = ('templateSelected(int)',
                      )

    def __init__(self,  parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self._model = None


    def setModel(self, model):
        self._model = model
        self.setEnabled(not self._model.isEmpty())


class CActionTemplateChooseButton(QtGui.QPushButton):
    __pyqtSignals__ = ('templateSelected(int)',
                      )

    def __init__(self,  parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.popup = None
        # self.setMenu(QtGui.QMenu(self))
        # self.setMenu(CActionTemplateChooseMenu(self))
        self.connect(self, SIGNAL('pressed()'), self._popupPressed)
        self._model = None


    def setModel(self, model):
        self._model = model
        self._model.rowsRemoved.connect(self.modelRowsRemoved)
        self.setButtonEnabled()
    
    def modelRowsRemoved(self, parent, start, end):
        self.setButtonEnabled()

    def setButtonEnabled(self):
        self.setEnabled(not self._model.isEmpty())

    def initStyleOption(self, option):
        QtGui.QPushButton.initStyleOption(self, option)
        option.features |= QtGui.QStyleOptionButton.HasMenu

    def sizeHint(self):
        self.ensurePolished()
        w = 0
        h = 0
        opt = QtGui.QStyleOptionButton()
        self.initStyleOption(opt)

        if not opt.icon.isNull():
            ih = opt.iconSize.height()
            iw = opt.iconSize.width() + 4
            w += iw
            h = max(h, ih)

        if opt.features & QtGui.QStyleOptionButton.HasMenu:
            w += self.style().pixelMetric(QtGui.QStyle.PM_MenuButtonIndicator, opt, self)

        empty = opt.text.isEmpty()
        fm = self.fontMetrics()
        sz = fm.size(Qt.TextShowMnemonic, "XXXX" if empty else opt.text)
        if not empty or not w:
            w += sz.width()
        if not empty or not h:
            h = max(h, sz.height())
        result = self.style().sizeFromContents(QtGui.QStyle.CT_PushButton, opt, QSize(w, h), self).expandedTo(QtGui.qApp.globalStrut())
        return result


    def paintEvent(self, paintEvent):
        p = QtGui.QStylePainter(self)
        option = QtGui.QStyleOptionButton()
        self.initStyleOption(option)
        p.drawControl(QtGui.QStyle.CE_PushButton, option)


    def _popupPressed(self):
        self.setDown(True)
        if not self.popup:
            self.popup = CActionTemplatePopup(self)
            # m = CActionTemplateModel(self, None, None, None, None, 0, None, False)
        self.popup.treeView.setModel(self._model)
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self.popup.sizeHint()
        screen = QtGui.qApp.desktop().availableGeometry(pos)
        pos.setX(max(min(pos.x(), screen.right()-size.width()), screen.left()))
        pos.setY(max(min(pos.y(), screen.bottom()-size.height()), screen.top()))
        self.popup.move(pos)
        self.connect(self.popup, SIGNAL('templateSelected(int)'), self.on_templateSelected)
        self.connect(self.popup, SIGNAL('closePopup()'), self.on_closePopup)
        self.popup.show()

    def on_templateSelected(self, templateId):
        self.emit(SIGNAL('templateSelected(int)'), templateId)


    def on_closePopup(self):
        self.setDown(False)


# ##############################################################################


class CActionTemplateComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.setModelColumn(0)
        self._model = CActionTemplateModel(self, None, None, None, None, 0, None, False)
        self.setModel(self._model)
        self._popupView = CActionTemplateTreeView(self)
        self._popupView.setObjectName('popupView')
        self._popupView.setModel(self._model)
        self.setView(self._popupView)
        self._popupView.installEventFilter(self)
        self._popupView.viewport().installEventFilter(self)
        QObject.connect(self._popupView, SIGNAL('activated(QModelIndex)'), self.on_ItemActivated)
        QObject.connect(self._popupView, SIGNAL('entered(QModelIndex)'), self.setCurrentIndex)
        self.preferredWidth = 0

    def setPreferredWidth(self, preferredWidth):
        self.preferredWidth = preferredWidth


    def setFilter(self, actionTypeId, personId, specialityId, SNILS,  clientSex, clientAge, removeEmptyNodes=True, orgStructureId=None):
        self._model.setFilter(actionTypeId, personId, orgStructureId, specialityId, SNILS, clientSex, clientAge, removeEmptyNodes)


    def updateModel(self):
        self._model.update()


    def setValue(self, id):
        index = self._model.findItemId(id)
        self.setCurrentIndex(index)


    def value(self):
        modelIndex = self._model.index(self.currentIndex(), 0, self.rootModelIndex())
        if modelIndex.isValid():
            return self._model.itemId(modelIndex)
        return None


    def on_ItemActivated(self, index):
        if index.isValid():
            if (int(index.flags()) & Qt.ItemIsSelectable) != 0:
                self.hidePopup()
                self.emit(SIGNAL('itemSelected(QModelIndex)'), index)
            else:
                # print self.__popupView.isExpanded(index)
                self._popupView.setExpanded(index, not self._popupView.isExpanded(index))


    def showPopup(self):
        # self.__searchString = ''
        # modelIndex = self._model.index(self.currentIndex(), 0, self.rootModelIndex())

        self._popupView.setRealRootIndex(QModelIndex())
        self._popupView.expandAll()
        # preferredWidth = self._popupView.sizeHint().width()
        preferredWidth = max(self.preferredWidth if self.preferredWidth else 0, self._popupView.sizeHint().width())
        if preferredWidth:
            if self.width() < preferredWidth:
                self._popupView.setFixedWidth(preferredWidth)
        QtGui.QComboBox.showPopup(self)
        scrollBar = self._popupView.horizontalScrollBar()
        scrollBar.setValue(0)


    def setCurrentIndex(self, index):
        if not index:
            index = QModelIndex()
        if index:
            self.setRootModelIndex(index.parent())
            QtGui.QComboBox.setCurrentIndex(self, index.row())

        # self.emit(SIGNAL('codeSelected(QString)'), self._model.code(index))


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:  # and obj == self.__popupView:
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Select):
                index = self._popupView.currentIndex()
                if index.isValid() and (int(index.flags()) & Qt.ItemIsSelectable) != 0:
                    self.hidePopup()
                    self.setCurrentIndex(index)
                    self.emit(SIGNAL('itemSelected(QModelIndex)'), index)
                return True
            # print 'default for ',event.key()
            return False
        if event.type() == QEvent.MouseButtonRelease and obj == self._popupView.viewport():
            return True
        # return QtGui.QComboBox.eventFilter(self, obj, event)
        return False


# ##############################################################################
#
#
#class CActionTemplateCache(object):
#    def __init__(self, eventEditor, personEditor):
#        self.eventEditor = eventEditor
#        #personEditor должен иметь два метода:
#        # value - возвращает id врача
#        # currentPersonSpecialityId - возвращает id специальности текущего врача
#        self.personEditor = personEditor
#        self.data = {}
#
#
#    def reset(self, actionTypeId=None):
#        if actionTypeId:
#            del self.data[actionTypeId]
#        else:
#            self.data = {}
#
#
#    def getModel(self, actionTypeId):
#        personId, specialityId = self.__getPersonAndSpecialityId()
#        SNILS = self.__getSNILS()
#        actionLevel = self.data.setdefault(actionTypeId, {})
#        result = actionLevel.get(personId, None)
#        if result is None:
#            result = self.__createModel(actionTypeId, personId, specialityId, SNILS, QtGui.qApp.currentOrgStructureId())
#            actionLevel[personId] = result
#        return result
#
#
#    def __getPersonAndSpecialityId(self):
#        if QtGui.qApp.userSpecialityId:
#            return QtGui.qApp.userId, QtGui.qApp.userSpecialityId
#        if self.personEditor.currentPersonSpecialityId():
#            return self.personEditor.value(), self.personEditor.currentPersonSpecialityId()
#        return self.eventEditor.personId, self.eventEditor.personSpecialityId
#
#
#
#    def __getSNILS(self):
#        if QtGui.qApp.userId:
#            SNILS = forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('Person'), 'id', QtGui.qApp.userId, 'SNILS'))
#            return SNILS
#
#
#    def __createModel(self, actionTypeId, personId, specialityId, SNILS, orgStructureId):
#        result = CActionTemplateModel(self.eventEditor,
#                                      actionTypeId,
#                                      personId,
#                                      orgStructureId,
#                                      specialityId,
#                                      SNILS,
#                                      self.eventEditor.clientSex,
#                                      self.eventEditor.clientAge)
#        return result


# ##############################################################################


class CActionTemplateTreeModel(CActionTemplateModel):
    pass


class CActionTemplateCache(object):
    def __init__(self, eventEditor, personEditor):
        self.eventEditor = eventEditor
        self.personEditor = personEditor
        self.personSNILS = u''
        self.showTypeTemplate = 0
        self.data = {}


    def reset(self, actionTypeId=None):
        if actionTypeId:
            del self.data[actionTypeId]
        else:
            self.data = {}


    def getModel(self, actionTypeId):
        QtGui.qApp.setWaitCursor()
        try:
            personId, specialityId = self.__getPersonAndSpecialityId()
            SNILS, self.showTypeTemplate = self.__getSNILS(personId)
            actionLevel = self.data.setdefault(actionTypeId, {})
            result = actionLevel.get(personId, None)
            if result is None:
                result = self.__createModel(actionTypeId, personId, specialityId, SNILS, QtGui.qApp.currentOrgStructureId())
                actionLevel[personId] = result
        finally:
            QtGui.qApp.restoreOverrideCursor()
        return result


    def __getPersonAndSpecialityId(self):
        if QtGui.qApp.userSpecialityId:
            return QtGui.qApp.userId, QtGui.qApp.userSpecialityId
        if self.personEditor.currentPersonSpecialityId():
            return self.personEditor.value(), self.personEditor.currentPersonSpecialityId()
        return self.eventEditor.personId, self.eventEditor.personSpecialityId


    def setPersonSNILS(self, personSNILS):
        self.personSNILS = personSNILS


    def setShowTypeTemplate(self, showTypeTemplate):
        self.showTypeTemplate = showTypeTemplate


    def __getSNILS(self, personId):
        if personId:
            db = QtGui.qApp.db
            tablePerson = db.table('Person')
            record = db.getRecordEx(tablePerson, [tablePerson['showTypeTemplate'], tablePerson['SNILS']], [tablePerson['id'].eq(personId), tablePerson['deleted'].eq(0)])
            if record:
                personSNILS = forceStringEx(record.value('SNILS'))
                showTypeTemplate = forceInt(record.value('showTypeTemplate'))
                return personSNILS, showTypeTemplate
        return self.personSNILS, self.showTypeTemplate


    def __createModel(self, actionTypeId, personId, specialityId, SNILS, orgStructureId):
        result = CActionTemplateTreeModel(self.eventEditor,
                                      actionTypeId,
                                      personId,
                                      orgStructureId,
                                      specialityId,
                                      SNILS, 
                                      self.eventEditor.clientSex,
                                      self.eventEditor.clientAge,
                                      removeEmptyNodes=True,
                                      showTypeTemplate=self.showTypeTemplate,
                                      typeDialog=1)
        return result
