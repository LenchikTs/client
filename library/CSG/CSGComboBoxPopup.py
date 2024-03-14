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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDate, QEvent

from library.Utils import getPref, setPref
from library.TableModel import CTableModel, CTextCol

from Ui_CSGComboBoxPopup import Ui_CSGComboBoxPopup


__all__ = ('CCSGComboBoxPopup',
          )

TABLE_CSG = 'mes.CSG'
TABLE_CSG_MKB = 'mes.CSG_Diagnosis'

class CCSGComboBoxPopup(QtGui.QFrame, Ui_CSGComboBoxPopup):
    __pyqtSignals__ = ('CSGSelected(int)',
                      )

    def __init__(self, parent = None, eventEditor = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CCSGTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblCSG.setModel(self.tableModel)
        self.tblCSG.setSelectionModel(self.tableSelectionModel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setDefault(True)
#       к сожалению в данном случае setDefault обеспечивает рамочку вокруг кнопочки
#       но enter не работает...
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setShortcut(Qt.Key_Return)
        self.eventBegDate = None
        self.clientSex = 0
        self.clientBirthDate = None
        self.MKB = ''
        self.codeMask = None
        self.eventProfileId = None
        self.csgId = None
        self.eventEditor = eventEditor
        self.tblCSG.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CCSGComboBoxPopup', {})
        self.tblCSG.loadPreferences(preferences)
        self.on_buttonBox_reset()


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
        preferences = self.tblCSG.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CCSGComboBoxPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblCSG:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblCSG.currentIndex()
                self.tblCSG.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    def on_buttonBox_reset(self):
        parent = self.parentWidget()
        if parent.filterValues:
            self.chkSex.setChecked(parent.filterValues.get('sex', True))
            self.chkAge.setChecked(parent.filterValues.get('age', True))
            self.chkCsgServices.setChecked(parent.filterValues.get('csgServices', True))
            self.cmbMKB.setCurrentIndex(parent.filterValues.get('mkbCond', 2))
            self.cmbEventProfile.setCurrentIndex(parent.filterValues.get('isEventProfile', 1))
        else:
            self.chkSex.setChecked(True)
            self.chkAge.setChecked(True)
            self.chkCsgServices.setChecked(True)
            self.cmbMKB.setCurrentIndex(2)
            self.cmbEventProfile.setCurrentIndex(1)


    def on_buttonBox_apply(self):
        parent = self.parentWidget()
        useSex        = self.chkSex.isChecked()
        useAge        = self.chkAge.isChecked()
        useCsgServices = self.chkCsgServices.isChecked()
        mkbCond    = self.cmbMKB.currentIndex()
        isEventProfile = self.cmbEventProfile.currentIndex()
        parent.filterValues = {'age': useAge,
                               'sex': useSex,
                               'csgServices': useCsgServices,
                               'mkbCond': mkbCond,
                               'isEventProfile': isEventProfile}
        parent.model().dbdata.select(parent.filterValues)
        idList = parent.model().dbdata.idList
        self.setCSGIdList(idList)


    def setCSGIdList(self, idList):
        if idList:
            self.tblCSG.setIdList(idList, self.csgId)
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget.setTabEnabled(0, True)
            self.tblCSG.setFocus(Qt.OtherFocusReason)
        else:
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(0, False)
            self.chkSex.setFocus(Qt.OtherFocusReason)


    def setup(self, clientSex, clientBirthDate, MKB, csgId, eventBegDate, mesServiceTemplate, codeMask = None, eventProfileId = None):
        self.clientSex = clientSex
        self.clientBirthDate = clientBirthDate
        self.MKB = MKB
        self.csgId = csgId
        self.eventBegDate = eventBegDate
        self.codeMask = codeMask
        self.eventProfileId = eventProfileId
        self.mesServiceTemplate = mesServiceTemplate
        parent = self.parentWidget()
        idList = parent.model().dbdata.idList
        self.setCSGIdList(idList)


    @pyqtSignature('QModelIndex')
    def on_tblCSG_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.tableModel.flags(index)):
                csgId = self.tblCSG.currentItemId()
                self.csgd = csgId
                self.emit(SIGNAL('CSGSelected(int)'), csgId)
                self.close()


class CCSGTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Код',             ['code'],  20))
        self.addColumn(CTextCol(u'Наименование',    ['name'],  40))
        self.addColumn(CTextCol(u'Описание',        ['note'], 40))
        self.setTable(TABLE_CSG)
        self.date = QDate.currentDate()


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable
