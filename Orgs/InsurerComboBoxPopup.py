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
from PyQt4.QtCore import Qt, QEvent, pyqtSignature, SIGNAL

from library.Utils import addDotsEx, forceStringEx

from KLADR.KLADRModel import CKladrTreeModel
from Registry.PolicySerialEdit import CPolicySerialEdit


class CInsurerComboBoxPopupPolicySerialEdit(CPolicySerialEdit):
    def __init__(self, parent=None):
        CPolicySerialEdit.__init__(self, parent)

# WTF? циклические импорты?
from Ui_InsurerComboBoxPopup import Ui_InsurerComboBoxPopup

class CInsurerComboBoxPopup(QtGui.QFrame, Ui_InsurerComboBoxPopup):
    __pyqtSignals__ = ('insurerSelected(int)',
                      )
    insurerFilter = 'isInsurer = 1 and deleted = 0 AND isActive = 1'

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setupUi(self)
        self.model = parent.model()
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.tblInsurer.setModel(self.model)
        self.tblInsurer.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._areaFilter = ''
        self._areaList   = None
        self.regAddress  = None
        self._serialFilter = ''
        self._serial = ''
        self.cond = []
        self.table = QtGui.qApp.db.table('Organisation')
        model = CKladrTreeModel(None)
        model._rootItem._stmtCount = u'SELECT COUNT(CODE) FROM %s WHERE parent="%s" and CODE like "%%00000000"'
        model._rootItem._stmtQ = u'SELECT CODE, NAME, SOCR, STATUS FROM %s WHERE parent="%s" and CODE like "%%00000000"'
        model._rootItem._stmtCode = u'SELECT parent FROM %s WHERE CODE LIKE \'%s%%\' and CODE like "%%00000000" LIMIT 1'
        model.setAllSelectable(True)
        self.cmbArea._model = model
        self.cmbArea.setModel(model)
        self.cmbArea._popupView.treeModel = model
        self.cmbArea._popupView.treeView.setModel(model)
        self.setRegAdress()
        self.cmbArea.installEventFilter(self)
        self.edtInfis.installEventFilter(self)
        self.edtName.installEventFilter(self)
        self.edtINN.installEventFilter(self)
        self.edtPolisSerial.installEventFilter(self)
        self.isFirst = True


    def show(self):
        self.tblInsurer.setFocus()
        row = self.parent.currentIndex()
        if row >= 0:
            index = self.model.createIndex(row, 0)
        else:
            index = self.model.createIndex(0, 0)
        self.tblInsurer.setCurrentIndex(index)
        QtGui.QFrame.show(self)


    def selectItemByIndex(self, index):
        id = self.model.getId(index.row())
        id = id if id else 0
        self.emit(SIGNAL('insurerSelected(int)'), id)
        self.hide()

    @pyqtSignature('QModelIndex')
    def on_tblInsurer_clicked(self, index):
        self.selectItemByIndex(index)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    def on_buttonBox_reset(self):
        self.isFirst = True
        self._serialFilter = ''
        self._serial = ''
        self.chkArea.setChecked(False)
        self.cond = [self.insurerFilter]
        if self.regAddress:
            areaList = [QtGui.qApp.defaultKLADR()]
            regAddress = self.regAddress['KLADRCode']
            areaList.append(regAddress)
            self.setAreaFilter(areaList)
            self.cmbArea.setCode(regAddress)
        else:
#            self.setAreaFilter([QtGui.qApp.defaultKLADR(),
#                                self.cmbArea.code()])
            self.cmbArea.setCode(QtGui.qApp.defaultKLADR())
            self._areaFilter = ''
        self.updateFilter()
        self.edtInfis.clear()
        self.edtName.clear()
        self.edtINN.clear()
        self.edtOKATO.clear()
        self.edtPolisSerial.clear()


    def on_buttonBox_apply(self):
        self.isFirst = True
        table = self.table
        db = QtGui.qApp.db
        cond = []
        infisCode = forceStringEx(self.edtInfis.text())
        name      = forceStringEx(self.edtName.text())
        inn       = forceStringEx(self.edtINN.text())
        serial    = forceStringEx(self.edtPolisSerial.text())
        okato     = forceStringEx(self.edtOKATO.text())
        cond.append(self.insurerFilter) if self.chkCompulsoryPolisCompanyOnlyActive.isChecked() else cond.append('isInsurer = 1 and deleted = 0')
        if infisCode:
            cond.append(table['infisCode'].like(infisCode))
        if inn:
            cond.append(table['INN'].eq(inn))
        if okato:
            cond.append(table['OKATO'].eq(okato))
        if name:
            nameFilter = []
            dotedName = addDotsEx(name)
            nameFilter.append(table['shortName'].like(dotedName))
            nameFilter.append(table['fullName'].like(dotedName))
            nameFilter.append(table['title'].like(dotedName))
            cond.append(db.joinOr(nameFilter))
        if serial:
            serial = unicode(serial).upper()
            if self._serial != serial:
                self._serialFilter = self.constructSerialFilter(serial)
                self._serial = serial
        else:
            self._serialFilter = ''
            self._serial = ''
        self.cond = cond
        if self.chkArea.isChecked():
            areaList = [self.cmbArea.code()]
            self.setAreaFilter(areaList)
        else:
            self._areaFilter = ''
            self.updateFilter()
        self.model.update()


    def setRegAdress(self, regAddress=None):
        self.regAddress = regAddress
        if regAddress:
            self.cmbArea.setCode(regAddress['KLADRCode'])
        else:
            self.cmbArea.setCode(QtGui.qApp.defaultKLADR())


    def constructAreaFilter(self, areaList):
        if areaList:
            db = QtGui.qApp.db
            table = self.table
            return db.joinAnd([self.insurerFilter, table['area'].inlist(areaList+[''])])
        return None


    def setAreaFilter(self, areaList):
        l = set()
        for code in areaList:
            if code:
                l.add(code[:2].ljust(13, '0'))
                l.add(code[:5].ljust(13, '0'))
        areaList = list(l)
#        if self._areaList != areaList:
        self._areaFilter = self.constructAreaFilter(areaList)
        self._areaList = areaList
        self.updateFilter()


    def setSerialFilter(self, serial):
        self.isFirst = True
        serial = unicode(serial).upper()
        if self._serial != serial:
            innerSerial = forceStringEx(self.edtPolisSerial.text())
            if unicode(innerSerial).upper() != serial:
                self.edtPolisSerial.setText(serial)
            self._serialFilter = self.constructSerialFilter(serial)
            self._serial = serial
            self.updateFilter()


    def constructSerialFilter(self, serial):
        db = QtGui.qApp.db
        if serial:
            table = db.table('Organisation_PolicySerial')
            idlist1 = db.getIdList(table, 'organisation_id', table['serial'].eq(serial))
            table = db.table('Organisation')
#            idlist2 = db.getIdList(table, 'id', db.joinAnd([self.insurerFilter, 'NOT EXISTS (SELECT id FROM Organisation_PolicySerial WHERE Organisation_PolicySerial.organisation_id=Organisation.id)']))
            if idlist1:# or idlist2:
                return table['id'].inlist(idlist1)#+idlist2)
        return None


    def updateFilter(self):
        db = QtGui.qApp.db
        cond = self.cond
        if self._serialFilter:
            cond.append(self._serialFilter)
        if self._areaFilter:
            cond.append(self._areaFilter)
        currValue = self.parent.value()
        self.model.setFilter(db.joinAnd(cond))
        self.cond = []
        if self.model.rowCount() > 1:
            self.tabWidget.setCurrentIndex(0)
        self.parent.setValue(currValue)
        x = 0 if self.isFirst else 1
        if not self.parent.value() and self.model.rowCount()>x:
            self.parent.setCurrentIndex(x)
            self.tblInsurer.setCurrentIndex(self.model.createIndex(x, 0))


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_C, Qt.Key_G):
                if key == Qt.Key_C:
                    obj.keyPressEvent(event)
                self.keyPressEvent(event)
                return False
            if  key == Qt.Key_Tab:
                self.focusNextPrevChild(True)
                return True
        return False


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.tabWidget.currentIndex():
                self.on_buttonBox_apply()
            else:
                index = self.tblInsurer.selectedIndexes()
                if index:
                    self.selectItemByIndex(index[0])
        if (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C):
            self.tabWidget.setCurrentIndex(0)
        if (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_G):
            self.tabWidget.setCurrentIndex(1)
        QtGui.QFrame.keyPressEvent(self, event)
