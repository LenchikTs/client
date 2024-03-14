# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDateTime

from library.DialogBase           import CConstructHelperMixin
from library.database             import CTableRecordCache
from library.Utils                import forceRef
from Registry.Utils               import getRightEditTempInvalid, getClientMiniInfo
from Events.TempInvalidEditDialog import CTempInvalidCreateDialog, CTempInvalidEditDialog, titleList, getTempInvalidIdOpen
from Events.TempInvalidInfo       import CTempInvalidInfo
from Events.TempInvalid           import CTempInvalidPrivateModel

from F088.Ui_TempInvalidF088      import Ui_grpTempInvalid


class CTempInvalidF088(QtGui.QGroupBox, CConstructHelperMixin, Ui_grpTempInvalid):
    def __init__(self, parent=None):
        QtGui.QGroupBox.__init__(self, parent)
        self.eventEditor = None
        self.addObject('modelTempInvalidPrivate', CTempInvalidPrivateModel(self))
        self.setupUi(self)
        self.tblTempInvalidPrivate.setModel(self.modelTempInvalidPrivate)
#        self.addPopupEditTempInvalidPrivate()
#        self.connect(self.tblTempInvalidPrivate._popupMenu, SIGNAL('aboutToShow()'), self.on_popupMenuTempInvalidPrivate_aboutToShow)


    def on_popupMenuTempInvalidPrivate_aboutToShow(self):
        table = self.tblTempInvalidPrivate
        model = self.modelTempInvalidPrivate
        self.actEditTempInvalidPrivate.setEnabled(bool(self.popupMenuTempInvalidId(table, model)))


    def popupMenuTempInvalidId(self, table, model):
        table.on_popupMenu_aboutToShow()
        row = table.currentIndex().row()
        record = model._items[row] if 0 <= row < len(model._items) else None
        return forceRef(record.value('id')) if record else None


    def addPopupEditTempInvalidPrivate(self):
        if self.tblTempInvalidPrivate._popupMenu is None:
            self.tblTempInvalidPrivate.createPopupMenu()
        self.actEditTempInvalidPrivate = QtGui.QAction(u'Редактировать (F4)', self)
        self.actEditTempInvalidPrivate.setObjectName('actEditTempInvalidPrivate')
        self.tblTempInvalidPrivate._popupMenu.addAction(self.actEditTempInvalidPrivate)
        self.connect(self.actEditTempInvalidPrivate, SIGNAL('triggered()'), self.on_actEditTempInvalidPrivate_triggered)
        self.addObject('qshcEditTempInvalidPrivate', QtGui.QShortcut('F4', self.tblTempInvalidPrivate, self.on_actEditTempInvalidPrivate_triggered))
        self.qshcEditTempInvalidPrivate.setContext(Qt.WidgetShortcut)


    @pyqtSignature('')
    def on_actEditTempInvalidPrivate_triggered(self):
        currentItem = self.tblTempInvalidPrivate.currentItem()
        tempInvalidId = forceRef(currentItem.value('id')) if currentItem else None
        self.openTempInvalid(tempInvalidId)


    def protectFromEdit(self, isProtected):
        widgets = [self.tblTempInvalidPrivate.model()]
        for widget in widgets:
            widget.setReadOnly(isProtected)


    def destroy(self):
        self.tblTempInvalidPrivate.setModel(None)
        del self.modelTempInvalidPrivate


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor
        self.modelTempInvalidPrivate.setEventEditor(eventEditor)


    def setType(self, type_, docCode=None):
        self.type_ = type_
        self.docCode = docCode
        self.modelTempInvalidPrivate.setType(self.type_, self.docCode)


    def pickupTempInvalid(self):
        self.modelTempInvalidPrivate.loadItems(self.eventEditor.clientId)


#    @pyqtSignature('QModelIndex')
#    def on_tblTempInvalidPrivate_doubleClicked(self, index):
#        self.editTempInvalid(self.tblTempInvalidPrivate, 0)


    def openTempInvalid(self, tempInvalidId):
        if tempInvalidId and getRightEditTempInvalid(tempInvalidId):
            db = QtGui.qApp.db
            clientId = self.eventEditor.clientId
            clientCache = CTableRecordCache(db, db.forceTable('Client'), u'*', capacity=None)
            dialog = CTempInvalidEditDialog(self, clientCache)
            clientInfo = getClientMiniInfo(clientId)
            dialog.setWindowTitle(titleList[self.type_] + u': ' + clientInfo)
            dialog.setType(self.type_, self.docCode)
            dialog.load(tempInvalidId)
            try:
                if dialog.exec_():
                    self.modelTempInvalidPrivate.loadItems(clientId)
            finally:
                dialog.deleteLater()


    def editTempInvalid(self, table, type = 0):
        currentItem = table.currentItem()
        tempInvalidId = forceRef(currentItem.value('id')) if currentItem else None
        self.getEditorTempInvalid(tempInvalidId, type)


    def getEditorTempInvalid(self, tempInvalidId, type = 0):
        if tempInvalidId:
            self.openTempInvalid(tempInvalidId)
        else:
            openTempInvalidId = getTempInvalidIdOpen(self.eventEditor.clientId, self.type_, self.docCode)
            if openTempInvalidId:
                self.getEditorTempInvalid(openTempInvalidId, type)
            else:
                self.createTempInvalid(type)


    def newTempInvalid(self):
        tempInvalidId = getTempInvalidIdOpen(self.eventEditor.clientId, self.type_, self.docCode)
        self.getEditorTempInvalid(tempInvalidId)


    def createTempInvalid(self, type = 0):
        clientId = self.eventEditor.clientId
        if clientId:
            MKBList = self.eventEditor.getFinalDiagnosisMKB() if hasattr(self.eventEditor, 'getFinalDiagnosisMKB') else u''
            MKB = MKBList[0] if len(MKBList) > 1 else MKBList
            db = QtGui.qApp.db
            clientCache = CTableRecordCache(db, db.forceTable('Client'), u'*', capacity=None)
            dialog = CTempInvalidCreateDialog(self, clientId, clientCache)
            dialog.setType(self.type_, self.docCode)
            clientInfo = getClientMiniInfo(clientId)
            dialog.setWindowTitle(titleList[self.type_] + u': ' + clientInfo)
            if not QtGui.qApp.userSpecialityId:
                eventSetDateTime = self.eventEditor.eventSetDateTime
                execDate = (eventSetDateTime.date() if isinstance(eventSetDateTime, QDateTime) else eventSetDateTime) if (eventSetDateTime and eventSetDateTime.isValid()) else None
                execPersonId = self.eventEditor.getExecPersonId()
            else:
                execDate = None
                execPersonId = None
            dialog.createTempInvalidDocument(MKB, type = type, execDate = execDate, execPersonId = execPersonId)
            try:
                if dialog.exec_():
                   self.modelTempInvalidPrivate.loadItems(clientId)
            finally:
                dialog.deleteLater()


    def getTempInvalidInfo(self, context):
        result = context.getInstance(CTempInvalidInfo, None)
        if result._ok:
            return result
        result._loaded = True
        return result
