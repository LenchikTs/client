# coding=utf-8
############################################################################
#
# Copyright (C) 2023 SAMSON Group. All rights reserved.
#
############################################################################
#
# Это программа является свободным программным обеспечением.
# Вы можете использовать, распространять и/или модифицировать её согласно
# условиям GNU GPL версии 3 или любой более поздней версии.
#
############################################################################

from PyQt4                              import QtGui
from PyQt4.QtCore                       import Qt, QEvent, QVariant
from PyQt4.QtSql                        import QSqlRecord, QSqlField
from library.InDocTable                 import CRecordListModel, CInDocTableCol, CEnumInDocTableCol
from library.Utils                      import forceInt, forceRef, forceString, forceStringEx
from library.adjustPopup                import adjustPopupToWidget
from library.SortFilterProxyTableModel  import CSortFilterProxyTableModel
from Ui_ReleaseFormComboBox             import Ui_ReleaseComboBoxPopup


class CReleaseFormComboBoxPopup(QtGui.QFrame, Ui_ReleaseComboBoxPopup):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.setWindowFlags(Qt.Popup)
        self._parent = parent
        self._selected = False

        self.model = CRecordListModel(self)
        self.model.addCol(CInDocTableCol(u'Код', 'code', 40))
        self.model.addCol(CInDocTableCol(u'Наименование', 'name', 40))
        self.model.addCol(CInDocTableCol(u'Дозировка', 'dosage', 40))
        self.model.addCol(CEnumInDocTableCol(u'ЕСКЛП', 'isESKLP', 20, (u'Нет', u'Да')))
        self.model.addCol(CInDocTableCol(u'', 'displayColumn', 0))
        self.proxyModel = CSortFilterProxyTableModel(self, self.model)

        self.model.cols()[3].alignment = lambda: QVariant(Qt.AlignCenter)

        self.tableView.setModel(self.proxyModel)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        self.tableView.hideColumn(4)

        self.tableView.doubleClicked.connect(self.on_tableView_doubleClicked)
        self.buttonBox.clicked.connect(self.on_buttonBox_clicked)
        self.tableView.installEventFilter(self)


    def on_tableView_doubleClicked(self, index):
        sourceIndex = self.proxyModel.mapToSource(index)
        self._parent.setCurrentIndex(sourceIndex.row())
        self._parent.hidePopup()


    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Reset:
            self.edtName.setText('')
            self.edtDosage.setText('')
            self.chkOnlyESKLP.setChecked(False)
        elif buttonCode == QtGui.QDialogButtonBox.Apply:
            self.select()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
            event.accept()
            index = self.tableView.currentIndex()
            self.on_tableView_doubleClicked(index)
            return True
        return False


    def select(self, onlyOneItemId=None):
        name = forceStringEx(self.edtName.text())
        dosage = forceStringEx(self.edtDosage.text())
        onlyESKLP = self.chkOnlyESKLP.isChecked()

        if not self._selected:
            cols = 'id, code, name, dosage, isESKLP, CONCAT_WS(" ", name, dosage) AS displayColumn'
            if onlyOneItemId:
                self.model.setItems([QtGui.qApp.db.getRecord('rbLfForm', cols, onlyOneItemId)])
            else:
                self._selected = True
                recordList = QtGui.qApp.db.getRecordList('rbLfForm', cols, order='code')
                recordList.insert(0, self.getSpecialRecord())
                self.model.setItems(recordList)
            self.proxyModel.reset()

        self.proxyModel.clearFilters()
        if bool(name):
            self.proxyModel.setFilter('name', name, self.proxyModel.MatchContains)
        if bool(dosage):
            self.proxyModel.setFilter('dosage', dosage, self.proxyModel.MatchContains)
        if onlyESKLP:
            self.proxyModel.setFilter('isESKLP', True)
        self.tableView.hideColumn(4)


    def getSpecialRecord(self):
        record = QSqlRecord()
        record.append(QSqlField('id', QVariant.Int))
        record.append(QSqlField('code', QVariant.String))
        record.append(QSqlField('name', QVariant.String))
        record.append(QSqlField('dosage', QVariant.String))
        record.append(QSqlField('isESKLP', QVariant.Bool))
        record.append(QSqlField('displayColumn', QVariant.String))
        record.setValue('id', 0)
        record.setValue('code', '0')
        record.setValue('name', u'не задано')
        record.setValue('dosage', '')
        record.setValue('isESKLP', False)
        record.setValue('displayColumn', u'не задано')
        return record


class CReleaseFormComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self._popupView = CReleaseFormComboBoxPopup(self)
        self.readOnly = False
        self.preferredWidth = 100
        self.setModel(self._popupView.model)
        self.setModelColumn(4)


    def setReadOnly(self, value):
        self.readOnly = bool(value)


    def isReadOnly(self):
        return self.readOnly


    def value(self):
        row = self.currentIndex()
        try:
            itemId = forceRef(self.model().getRecordByRow(row).value('id'))
        except IndexError:
            itemId = None
        return itemId


    def setValue(self, itemId):
        if itemId:
            if not self._popupView._selected:
                self._popupView.select(itemId)
                self.setCurrentIndex(0)
            else:
                # очень плохо
                for row, item in enumerate(self.model().items()):
                    if forceInt(item.value('id')) == itemId:
                        self.setCurrentIndex(row)
                        break
        else:
            if not self._popupView._selected:
                self._popupView.model.setItems([self._popupView.getSpecialRecord()])
                self._popupView.proxyModel.reset()
            self.setCurrentIndex(0)


    def currentName(self):
        row = self.currentIndex()
        record = self.model().getRecordByRow(row)
        return forceString(record.value('name'))


    def currentDosage(self):
        row = self.currentIndex()
        record = self.model().getRecordByRow(row)
        return forceString(record.value('dosage'))


    def setTable(self, *args, **kwargs):
        # оставлено для совместимости с CRBComboBox
        pass


    def showPopup(self):
        if not self.isReadOnly():
            model = self._popupView.model
            proxyModel = self._popupView.proxyModel
            view = self._popupView.tableView
            totalItems = model.rowCount(None)
            if not self._popupView._selected and totalItems > 0:
                itemId = self.value()
                self._popupView.select()
                self.setValue(itemId)
            else:
                self._popupView.select()

            index = model.index(self.currentIndex(), 1)
            proxyIndex = proxyModel.mapFromSource(index)
            selectionModel = view.selectionModel()
            selectionModel.setCurrentIndex(proxyIndex, QtGui.QItemSelectionModel.ClearAndSelect)

            tblHeaderHeight = view.horizontalHeader().height()
            maxVisibleItems = self.maxVisibleItems()
            view.setFixedHeight( view.rowHeight(0)*maxVisibleItems + tblHeaderHeight )
            frame = view.parent()
            sizeHint = view.sizeHint()
            adjustPopupToWidget(self, frame, True, max(self.preferredWidth, sizeHint.width()), view.height()+2)
            frame.show()
            view.setFocus()
            scrollBar = view.horizontalScrollBar()
            scrollBar.setValue(0)


    def hidePopup(self):
        view = self._popupView.tableView
        frame = view.parent()
        frame.hide()
