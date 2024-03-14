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
from PyQt4.QtCore import Qt, QDate, QEvent, pyqtSignature, SIGNAL

from library.database   import CTableRecordCache
from library.TableModel import CTableModel, CDateCol, CEnumCol, CTextCol
from library.Utils      import forceDate, forceInt, forceString, getPref, setPref, addDots
from Registry.SimplifiedClientSearch import CSimplifiedClientSearch
from Users.Rights       import urRegTabNewWriteRegistry

from Ui_ClientRelationComboBoxPopup import Ui_ClientRelationComboBoxPopup

__all__ = [ 'CClientRelationComboBoxPopup',
          ]


class CClientRelationComboBoxPopup(QtGui.QFrame, Ui_ClientRelationComboBoxPopup):
    __pyqtSignals__ = ('relatedClientIdSelected(int)'
                      )

    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CClientRelationTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.edtBirthDate.setHighlightRedDate(False)
        self.tblClientRelation.setModel(self.tableModel)
        self.tblClientRelation.setSelectionModel(self.tableSelectionModel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setDefault(True)
#       к сожалению в данном случае setDefault обеспечивает рамочку вокруг кнопочки
#       но enter не работает...
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setShortcut(Qt.Key_Return)
        self.date = None
        self.code = None
        self.clientId = None
        self.regAddressInfo = {}
        self.logAddressInfo = {}
        self.defaultAddressInfo = None
        self.dialogInfo = {}
        self.tblClientRelation.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CClientRelationComboBoxPopup', {})
        self.tblClientRelation.loadPreferences(preferences)
        self.edtBirthDate.setDate(QDate())
        self.cmbDocType.setTable('rbDocumentType', True, 'group_id IN (SELECT id FROM rbDocumentTypeGroup WHERE code=\'1\')')
        self.btnRegistry.setEnabled(QtGui.qApp.userHasRight(urRegTabNewWriteRegistry))


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblClientRelation.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CClientRelationComboBoxPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblClientRelation:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblClientRelation.currentIndex()
                self.tblClientRelation.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


    def simplifiedClientSearch(self):
        ok, nameParts, date = CSimplifiedClientSearch(self).parseKey(unicode(self.edtKey.text()))
        if ok:
            widgets = (self.edtLastName,
                       self.edtFirstName,
                       self.edtPatrName,
                      )
            for part, edt in zip(nameParts, widgets):
                edt.setText(part)
            if date:
                self.edtBirthDate.setDate(date)


    @pyqtSignature('bool')
    def on_chkKey_toggled(self, checked):
        if checked:
            self.on_buttonBox_reset()


    @pyqtSignature('const QString &')
    def on_edtKey_textChanged(self, text):
        ok, nameParts, date = CSimplifiedClientSearch(self).parseKey(unicode(text))
        self.buttonBox.button(self.buttonBox.Apply).setEnabled(ok)


    @pyqtSignature('')
    def on_btnFillingFilter_clicked(self):
        clientId = self.clientId if self.clientId else QtGui.qApp.currentClientId()
        if clientId:
            db = QtGui.qApp.db
            tableClient = db.table('Client')
            record = db.getRecordEx(tableClient, [tableClient['lastName'], tableClient['firstName'], tableClient['patrName'], tableClient['birthDate']], [tableClient['deleted'].eq(0), tableClient['id'].eq(clientId)])
            if record:
                self.edtLastName.setText(forceString(record.value('lastName')))
                self.edtFirstName.setText(forceString(record.value('firstName')))
                self.edtPatrName.setText(forceString(record.value('patrName')))
                self.edtBirthDate.setDate(forceDate(record.value('birthDate')))


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    def on_buttonBox_reset(self):
        self.edtLastName.setText('')
        self.edtFirstName.setText('')
        self.edtPatrName.setText('')
        self.edtBirthDate.setDate(QDate())
        self.cmbDocType.setValue(None)
        self.edtLeftSerial.setText('')
        self.edtRightSerial.setText('')
        self.edtNumber.setText('')


    def on_buttonBox_apply(self):
        QtGui.qApp.setWaitCursor()
        try:
            if self.chkKey.isChecked():
                self.simplifiedClientSearch()
            lastName = forceString(self.edtLastName.text())
            firstName = forceString(self.edtFirstName.text())
            patrName = forceString(self.edtPatrName.text())
            birthDate = forceDate(self.edtBirthDate.date())
            docTypeId = self.cmbDocType.value()
            leftSerial = forceString(self.edtLeftSerial.text())
            rightSerial = forceString(self.edtRightSerial.text())
            number = forceString(self.edtNumber.text())
            serial = u''
            if leftSerial:
                serial = leftSerial
            if rightSerial:
                if serial != u'':
                    serial += u' ' + rightSerial
                else:
                    serial += rightSerial
            crIdList = self.getClientRelationIdList(lastName, firstName, patrName, birthDate, docTypeId, serial, number, self.code, self.clientId)
            self.setClientRelationIdList(crIdList, None)
        finally:
            QtGui.qApp.restoreOverrideCursor()
        if not crIdList and QtGui.qApp.userHasRight(urRegTabNewWriteRegistry):
            res = QtGui.QMessageBox.warning(self,
                                            u'Внимание',
                                            u'Пациент не обнаружен.\nХотите зарегистрировать пациента?',
                                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                            QtGui.QMessageBox.Ok)
            if res == QtGui.QMessageBox.Ok:
                self.editNewClient()


    @pyqtSignature('')
    def on_btnRegistry_clicked(self):
        self.editNewClient()


    def getParamsDialogFilter(self):
        self.dialogInfo = {}
        self.dialogInfo['lastName'] = forceString(self.edtLastName.text())
        self.dialogInfo['firstName'] = forceString(self.edtFirstName.text())
        self.dialogInfo['patrName'] = forceString(self.edtPatrName.text())
        self.dialogInfo['birthDate'] = forceDate(self.edtBirthDate.date())
        self.dialogInfo['docType'] = self.cmbDocType.value()
        self.dialogInfo['serialLeft'] = forceString(self.edtLeftSerial.text())
        self.dialogInfo['serialRight'] = forceString(self.edtRightSerial.text())
        self.dialogInfo['docNumber'] = forceString(self.edtNumber.text())


    def editNewClient(self):
        from Registry.ClientEditDialog  import CClientEditDialog
        if QtGui.qApp.userHasAnyRight([urRegTabNewWriteRegistry]):
            QtGui.qApp.setWaitCursor()
            try:
                dialog = CClientEditDialog(self)
                dialog.tabWidget.setTabEnabled(7, False)
                dialog.tabRelations.setEnabled(False)
                self.getParamsDialogFilter()
                if self.dialogInfo:
                    dialog.setClientDialogInfo(self.dialogInfo)
                if self.regAddressInfo or self.logAddressInfo:
                    dialog.btnCopyPrevAddress.setEnabled(True)
                    dialog.prevAddress = None
                    dialog.setParamsRegAddress(self.regAddressInfo)
                    dialog.setParamsLocAddress(self.logAddressInfo)
                if self.defaultAddressInfo:
                    dialog.setDefaultAddressInfo(self.defaultAddressInfo)
            finally:
                QtGui.qApp.restoreOverrideCursor()
            try:
                if dialog.exec_():
                    clientId = dialog.itemId()
                    self.selectClientRelationCode(clientId)
            finally:
                dialog.deleteLater()


    def setClientRelationIdList(self, idList, posToId):
        if idList:
            self.tblClientRelation.setIdList(idList, posToId)
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget.setTabEnabled(0, True)
            self.tblClientRelation.setFocus(Qt.OtherFocusReason)
        else:
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(0, False)
            self.edtLastName.setFocus(Qt.OtherFocusReason)


    def getClientRelationIdList(self, lastName, firstName, patrName, birthDate, docTypeId, serial, number, forceCode, clientId):
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableDocument = db.table('ClientDocument')
        tableAddress = db.table('ClientAddress')
        tableDocumentType = db.table('rbDocumentType')
        queryTable = tableClient.leftJoin(tableAddress, tableClient['id'].eq(tableAddress['client_id']))
        queryTable = queryTable.leftJoin(tableDocument, tableClient['id'].eq(tableDocument['client_id']))
        queryTable = queryTable.leftJoin(tableDocumentType, tableDocument['documentType_id'].eq(tableDocumentType['id']))
        cond = [tableClient['deleted'].eq(0)]
        if clientId:
           cond.append(tableClient['id'].ne(clientId))
        orderList = ['Client.lastName', 'Client.firstName', 'Client.patrName']
        if lastName:
            cond.append(tableClient['lastName'].like(addDots(lastName)))
        if firstName:
            cond.append(tableClient['firstName'].like(addDots(firstName)))
        if patrName:
            cond.append(tableClient['patrName'].like(addDots(patrName)))
        if birthDate:
            cond.append(tableClient['birthDate'].eq(birthDate))
        if self.parentWidget().sex in (1,2):
            cond.append(tableClient['sex'].eq(self.parentWidget().sex))
        if docTypeId:
            cond.append(tableDocument['documentType_id'].eq(docTypeId))
        if serial:
            cond.append(tableDocument['serial'].eq(serial))
        if number:
            cond.append(tableDocument['number'].eq(number))
        if docTypeId or serial or number:
            cond.append(tableDocument['deleted'].eq(0))
        cond.append(db.joinOr([tableAddress['id'].isNull(), tableAddress['deleted'].eq(0)]))
        orderStr = ', '.join([fieldName for fieldName in orderList])
        idList = db.getDistinctIdList(queryTable, tableClient['id'].name(),
                              where=cond,
                              order=orderStr,
                              limit=1000)
        return idList


    def setDate(self, date):
        self.tableModel.date = date


    def setClientRelationCode(self, code, clientId, regAddressInfo, logAddressInfo):
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        self.code = code
        self.clientId = clientId
        self.regAddressInfo = regAddressInfo
        self.logAddressInfo = logAddressInfo
        idList = []
        id = None
        if code:
            record = db.getRecordEx(tableClient, [tableClient['id']], [tableClient['deleted'].eq(0), tableClient['id'].eq(code)])
            if record:
                id = forceInt(record.value(0))
            if id:
                idList = [id]
        self.setClientRelationIdList(idList, id)


    def selectClientRelationCode(self, code):
        self.code = code
        self.emit(SIGNAL('relatedClientIdSelected(int)'), code)
        self.close()


    def getCurrentClientRelationCode(self):
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        id = self.tblClientRelation.currentItemId()
        code = None
        if id:
            record = db.getRecordEx(tableClient, [tableClient['id']], [tableClient['deleted'].eq(0), tableClient['id'].eq(id)])
            if record:
                code = forceInt(record.value(0))
            return code
        return None


    @pyqtSignature('QModelIndex')
    def on_tblClientRelation_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.tableModel.flags(index)):
                code = self.getCurrentClientRelationCode()
                self.selectClientRelationCode(code)


class CClientRelationTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Фамилия', ['lastName'], 30))
        self.addColumn(CTextCol(u'Имя', ['firstName'], 30))
        self.addColumn(CTextCol(u'Отчество', ['patrName'], 30))
        self.addColumn(CTextCol(u'Номер клиента', ['id'], 20))
        self.addColumn(CEnumCol(u'Пол', ['sex'], ['', u'М', u'Ж'], 10))
        self.addColumn(CDateCol(u'Дата рождения', ['birthDate'], 20, highlightRedDate=False))
        self.addColumn(CTextCol(u'Адрес регистрации', ['regAddress'], 20))
        self.addColumn(CTextCol(u'Адрес проживания', ['logAddress'], 20))
        self.addColumn(CTextCol(u'Тип документа', ['name'], 20))
        self.addColumn(CTextCol(u'Серия документа', ['serial'], 20))
        self.addColumn(CTextCol(u'Номер документа', ['number'], 20))
        self.addColumn(CTextCol(u'Документ выдан', ['origin'], 20))
        self.addColumn(CDateCol(u'Дата выдачи документа', ['date'], 20))
        self.setTable('Client')
        self.date = QDate.currentDate()


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        #row = index.row()
        #record = self.getRecordByRow(row)
        #enabled = True
        #if enabled:
        #    return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        #else:
        #    return Qt.ItemIsSelectable


    def setTable(self, tableName):
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableDocument = db.table('ClientDocument')
        tableAddress = db.table('ClientAddress')
        tableDocumentType = db.table('rbDocumentType')
        loadFields = []
        loadFields.append(u'''DISTINCT Client.id, Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.sex, ClientDocument.serial, ClientDocument.number, ClientDocument.date, ClientDocument.origin, rbDocumentType.name, IF(ClientAddress.type = 0, concat(_utf8'Адрес регистрации: ', ClientAddress.freeInput), _utf8'') AS regAddress, IF(ClientAddress.type = 1, concat(_utf8'Адрес проживания: ', ClientAddress.freeInput), _utf8'') AS logAddress''')
        queryTable = tableClient.leftJoin(tableAddress, tableClient['id'].eq(tableAddress['client_id']))
        queryTable = queryTable.leftJoin(tableDocument, tableClient['id'].eq(tableDocument['client_id']))
        queryTable = queryTable.leftJoin(tableDocumentType, tableDocument['documentType_id'].eq(tableDocumentType['id']))
        self._table = queryTable
        self._recordsCache = CTableRecordCache(db, self._table, loadFields)
