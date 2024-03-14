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
from PyQt4.QtCore import Qt, QEvent, pyqtSignature, SIGNAL

from library.Utils import addDotsEx, forceStringEx

from Ui_OrgComboBoxPopupEx import Ui_OrgComboBoxPopupEx


class COrgComboBoxPopupEx(QtGui.QFrame, Ui_OrgComboBoxPopupEx):
    __pyqtSignals__ = ('itemSelected(int)',)

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setupUi(self)
        self.model = parent.model()
        self._parent = parent
        self.tblOrg.setModel(self.model)
        self.tblOrg.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.cond = []
        self.globalFilter = ''
        self.table = QtGui.qApp.db.table('Organisation')
        self.edtName.setFocus(Qt.ShortcutFocusReason)
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', addNone=True)
        self.cmbActive.setCurrentIndex(2)
        self.isFirst = True


    def setGlobalFilter(self, filter):
        self.globalFilter = filter


    def show(self):
        self.tblOrg.setFocus()
        row = self._parent.currentIndex()
        if row >= 0:
            index = self.model.createIndex(row, 0)
        else:
            index = self.model.createIndex(0, 0)
        self.tblOrg.setCurrentIndex(index)
        QtGui.QFrame.show(self)


    def selectItemByIndex(self, index):
        _id = self.model.getId(index.row())
        _id = _id if _id else 0
        self.emit(SIGNAL('itemSelected(int)'), _id)
        self.hide()


    @pyqtSignature('QModelIndex')
    def on_tblOrg_clicked(self, index):
        self.selectItemByIndex(index)


    def setIsMedicalOrg(self, isMedicalOrg):
        self.isMedicalOrg = isMedicalOrg


    def setIsMedical(self, isMedical):
        self.isMedical = isMedical
        self.cmbIsMedical.setCurrentIndex(self.isMedical)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    def on_buttonBox_reset(self):
        self.isFirst = True
        self.cond = []
        self.edtName.clear()
        self.edtINN.clear()
        self.edtOGRN.clear()
        self.edtOKATO.clear()
        self.updateFilter()


    def on_buttonBox_apply(self):
        self.isFirst = True
        table = self.table
        db = QtGui.qApp.db
        name = forceStringEx(self.edtName.text())
        inn = forceStringEx(self.edtINN.text())
        ogrn = forceStringEx(self.edtOGRN.text())
        okato = forceStringEx(self.edtOKATO.text())
        cond = ['deleted = 0']
        if name:
            nameFilter = []
            dotedName = addDotsEx(name)
            nameFilter.append(table['shortName'].like(dotedName))
            nameFilter.append(table['fullName'].like(dotedName))
            nameFilter.append(table['title'].like(dotedName))
            cond.append(db.joinOr(nameFilter))
        if inn:
            cond.append(table['INN'].eq(inn))
        if ogrn:
            cond.append(table['OGRN'].eq(ogrn))
        if okato:
            cond.append(table['OKATO'].eq(okato))
        tfomsCode = forceStringEx(self.edtTfomsCode.text())
        if tfomsCode:
            cond.append(table['infisCode'].eq(tfomsCode))
        okved = forceStringEx(self.edtOKVED.text())
        if okved:
            cond.append(table['OKVED'].like(okved))
        isInsurer = self.cmbIsInsurer.currentIndex()
        if isInsurer:
            cond.append(table['isInsurer'].eq(isInsurer - 1))
        isActive = self.cmbActive.currentIndex()
        if isActive:
            cond.append(table['isActive'].eq(isActive - 1))
        hospitalBedProfileId = self.cmbHospitalBedProfile.value()
        if hospitalBedProfileId:
            cond.append('EXISTS (SELECT 1 FROM Organisation_HospitalBedProfile WHERE master_id=Organisation.id and hospitalBedProfile_id=%d)' % hospitalBedProfileId)
        isMedical = self.cmbIsMedical.currentIndex()
        if isMedical:
            cond.append(table['isMedical'].eq(isMedical))
        self.cond = cond
        self.updateFilter()


    def updateFilter(self):
        db = QtGui.qApp.db
        currValue = self._parent.value()
        if self.globalFilter:
            self.cond.append(self.globalFilter)
        self.model.setFilter(db.joinAnd(self.cond))
        self.cond = []
        if self.model.rowCount() > 1:
            self.tabWidget.setCurrentIndex(0)
        self._parent.setValue(currValue)
        x = 0 if self.isFirst else 1
        if not self._parent.value() and self.model.rowCount() > x:
            self._parent.setCurrentIndex(x)
            self.tblOrg.setCurrentIndex(self.model.createIndex(x, 0))


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_C, Qt.Key_G):
                if key == Qt.Key_C:
                    obj.keyPressEvent(event)
                self.keyPressEvent(event)
                return False
            if key == Qt.Key_Tab:
                self.focusNextPrevChild(True)
                return True
        return False


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.tabWidget.currentIndex():
                self.on_buttonBox_apply()
            else:
                index = self.tblOrg.selectedIndexes()
                if index:
                    self.selectItemByIndex(index[0])
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.tabWidget.setCurrentIndex(0)
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_G:
            self.tabWidget.setCurrentIndex(1)
        QtGui.QFrame.keyPressEvent(self, event)
