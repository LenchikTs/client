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

from PyQt4              import QtGui
from PyQt4.QtCore       import Qt, QDate, QEvent, pyqtSignature, SIGNAL


from library.Utils      import forceInt, getPref, setPref

from library.TableModel import CTableModel, CDateCol, CRefBookCol, CTextCol

#from Accounting.Utils   import CContractFindTreeModel
#from Utils              import getOrganisationInfo


from Ui_PriceListComboBoxPopupEx import Ui_PriceListComboBoxPopupEx


class CPriceListComboBoxPopupEx(QtGui.QFrame, Ui_PriceListComboBoxPopupEx):
    __pyqtSignals__ = ('PriceListFindCodeSelected(int)',
                      )
    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.filter = {}
        self.tableModel = CPriceListTableModelEx(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblPriceListFind.setModel(self.tableModel)
        self.tblPriceListFind.setSelectionModel(self.tableSelectionModel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setShortcut(Qt.Key_Return)
        self.tblPriceListFind.installEventFilter(self)
        self.cmbFinance.setTable('rbFinance', True)
        self.date = None
        self.currentIdPriceList = None
        self.priceListOnly = False
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CPriceListComboBoxPopupEx', {})
        self.tblPriceListFind.loadPreferences(preferences)
        self.on_buttonBox_reset()


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent is not None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblPriceListFind.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CPriceListComboBoxPopupEx', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblPriceListFind:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblPriceListFind.currentIndex()
                self.tblPriceListFind.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    def on_buttonBox_reset(self):
        self.filter = {}
        self.cmbFinance.setValue(None)
        self.edtNumber.setText('')
        self.edtGrouping.setText('')
        self.edtResolution.setText('')
        self.setDate.setDate(QDate())
        self.begDate.setDate(QDate())
        self.endDate.setDate(QDate())
        self.setFilterPriceList()
        self.setPriceListCode(self.currentIdPriceList, self.priceListOnly)


    def setFilterPriceList(self):
        self.filter = {}
        self.filter['financeId']  = self.cmbFinance.value()
        self.filter['number']     = self.edtNumber.text()
        self.filter['grouping']   = self.edtGrouping.text()
        self.filter['resolution'] = self.edtResolution.text()
        self.filter['setDate']    = self.setDate.date()
        self.filter['begDate']    = self.begDate.date()
        self.filter['endDate']    = self.endDate.date()


    def on_buttonBox_apply(self, id=None):
        self.setFilterPriceList()
        self.setPriceListCode(self.currentIdPriceList, self.priceListOnly)
        self.tabWidget.setCurrentIndex(0)
        self.tblPriceListFind.setFocus(Qt.OtherFocusReason)


    def setPriceListIdList(self, idList, posToId):
        self.tblPriceListFind.setIdList(idList, posToId)
        if idList:
            self.tblPriceListFind.setFocus(Qt.OtherFocusReason)


    def getPriceListIdList(self, priceListOnly):
        db = QtGui.qApp.db
        tableContract = db.table('Contract')
        cond = [tableContract['deleted'].eq(0)]

        financeId  = self.filter.get('financeId', None   )
        number     = self.filter.get('number',    ''     )
        grouping   = self.filter.get('grouping',  ''     )
        resolution = self.filter.get('resolution',''     )
        setDate    = self.filter.get('setDate',   QDate())
        begDate    = self.filter.get('begDate',   QDate())
        endDate    = self.filter.get('endDate',   QDate())

        if financeId:
            cond.append(tableContract['finance_id'].eq(financeId))
        if number:
            cond.append(tableContract['number'].eq(number))
        if grouping:
            cond.append(tableContract['grouping'].eq(grouping))
        if resolution:
            cond.append(tableContract['resolution'].eq(resolution))
        if setDate:
            cond.append(tableContract['date'].eq(setDate))
        if begDate:
            cond.append(tableContract['begDate'].ge(begDate))
        if endDate:
            cond.append(tableContract['endDate'].le(endDate))
        if priceListOnly:
            priceListidList = db.getDistinctIdList(tableContract, tableContract['priceList_id'].name(), [tableContract['deleted'].eq(0), tableContract['priceList_id'].isNotNull()], u'finance_id, grouping, resolution, number, date')
            if priceListidList:
                cond.append(tableContract['id'].inlist(priceListidList))
                idList = db.getDistinctIdList(tableContract, tableContract['priceList_id'].name(), cond, u'finance_id, grouping, resolution, number, date')
            else:
                idList = []
        else:
            idList = db.getDistinctIdList(tableContract, tableContract['id'].name(), cond, u'finance_id, grouping, resolution, number, date')
        return idList


    def setDatePriceList(self, date):
        self.date = date
        self.setDate.setDate(self.date if self.date else QDate())


    def setCurrentIdPriceList(self, id):
        self.currentIdPriceList = id


    def setPriceListOnly(self, priceListOnly):
        self.priceListOnly = priceListOnly


    def setPriceListCode(self, id, priceListOnly):
        crIdList = self.getPriceListIdList(priceListOnly)
        self.setPriceListIdList(crIdList, id if id else None)


    def getCurrentPriceListCode(self):
        db = QtGui.qApp.db
        tableContract = db.table('Contract')
        id = self.tblPriceListFind.currentItemId()
        code = None
        if id:
            record = db.getRecordEx(tableContract, [tableContract['id']], [tableContract['deleted'].eq(0), tableContract['id'].eq(id)])
            if record:
                code = forceInt(record.value(0))
            return code
        return None


    def selectPriceListCode(self, id):
        self.currentIdPriceList = id
        self.emit(SIGNAL('PriceListFindCodeSelected(int)'), self.currentIdPriceList)
        self.close()


    @pyqtSignature('QModelIndex')
    def on_tblPriceListFind_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.tableModel.flags(index)):
                code = self.getCurrentPriceListCode()
                self.selectPriceListCode(code)


class CPriceListTableModelEx(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CRefBookCol(u'Источник финансирования', ['finance_id'], 'rbFinance', 30),
            CTextCol(   u'Группа',                  ['grouping'],    30            ),
            CTextCol(   u'Основание',               ['resolution'],  20            ),
            CTextCol(   u'Номер',                   ['number'],      20            ),
            CDateCol(   u'Дата',                    ['date'],        10            ),
            CDateCol(   u'Нач.дата',                ['begDate'],     10            ),
            CDateCol(   u'Кон.дата',                ['endDate'],     10            )
            ], 'Contract' )
        self.date = QDate.currentDate()


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable

