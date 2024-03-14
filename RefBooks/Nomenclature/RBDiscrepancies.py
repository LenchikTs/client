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

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, pyqtSignature, Qt, SIGNAL
from PyQt4.QtGui import QCheckBox, QHBoxLayout, QWidget, QTableWidget

from library.DialogBase import CDialogBase
from library.PreferencesMixin import CDialogPreferencesMixin
from .Ui_RBDiscrepancies import Ui_RBDiscrepancies


class CRBDiscrepancies(CDialogBase, Ui_RBDiscrepancies, CDialogPreferencesMixin):
    def __init__(self, parent, listRBDiscrepancies, orderedList):
        CDialogBase.__init__(self, parent)
        self.addObject('mnuCheckItem', QtGui.QMenu(self))
        self.addObject('actCheckAll', QtGui.QAction(u'Выделить все', self))
        self.addObject('actUnCheckAll', QtGui.QAction(u'Снять все выделения', self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Расхождения между заполняемыми значениями')
        self.listRBDiscrepancies = listRBDiscrepancies
        self.orderedList = orderedList
        header = self.tblDiscrepancies.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)


        self.mnuCheckItem.addAction(self.actCheckAll)
        self.mnuCheckItem.addAction(self.actUnCheckAll)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL('customContextMenuRequested(QPoint)'), self.showMenu)
        self.outDict = self.fillTable()

    def showMenu(self, pos):
        if self.mnuCheckItem:
            self.mnuCheckItem.exec_(self.mapToGlobal(pos))

    def fillTable(self):
        nameField = None
        outDict = {}
        row = 0
        for order in self.orderedList:
            if order in self.listRBDiscrepancies.keys():
                key, value = order, self.listRBDiscrepancies[order]
                out = None
                check = None
                self.tblDiscrepancies.insertRow(row)
                for col, item in enumerate(value):
                    if not col:
                        nameField = item
                    if isinstance(item, bool):
                        cell_widget = QWidget()
                        check = QCheckBox()
                        check.setChecked(item)
                        lay_out = QHBoxLayout(cell_widget)
                        lay_out.addWidget(check)
                        check = check.isChecked()
                        lay_out.setAlignment(Qt.AlignCenter)
                        lay_out.setContentsMargins(0, 0, 0, 0)
                        cell_widget.setLayout(lay_out)
                        self.tblDiscrepancies.setCellWidget(row, col, cell_widget)
                    elif isinstance(item, QDate) and item.isValid():
                        out = item.toPyDate().strftime("%Y-%m-%d")
                        self.tblDiscrepancies.setItem(row, col, QtGui.QTableWidgetItem(out))
                    elif key == 'cmbNarcoticSubstance' and isinstance(item, int):
                        out = u'Да' if item == 1 else u'Нет'
                        self.tblDiscrepancies.setItem(row, col, QtGui.QTableWidgetItem(out))
                        out = item
                    elif isinstance(item, tuple):
                        out = item[0]
                        self.tblDiscrepancies.setItem(row, col, QtGui.QTableWidgetItem(item[1]))
                    elif item == 'Disabled':
                        cell_widget = QWidget()
                        check = QCheckBox()
                        check.setChecked(False)
                        check.setEnabled(False)
                        lay_out = QHBoxLayout(cell_widget)
                        lay_out.addWidget(check)
                        lay_out.setAlignment(Qt.AlignCenter)
                        lay_out.setContentsMargins(0, 0, 0, 0)
                        cell_widget.setLayout(lay_out)
                        self.tblDiscrepancies.setCellWidget(row, col, cell_widget)
                        check = False
                    else:
                        out = unicode(item)
                        self.tblDiscrepancies.setItem(row, col, QtGui.QTableWidgetItem(out))
                    outDict[key] = [nameField, out, check]
                row += 1
        return outDict

    @pyqtSignature('')
    def on_actCheckAll_triggered(self):
        for i in xrange(self.tblDiscrepancies.rowCount()):
            item = self.tblDiscrepancies.cellWidget(i, 3).children()[1]
            if item.isEnabled():
                item.setChecked(True)

    @pyqtSignature('')
    def on_actUnCheckAll_triggered(self):
        for i in xrange(self.tblDiscrepancies.rowCount()):
            item = self.tblDiscrepancies.cellWidget(i, 3).children()[1]
            if item.isEnabled():
                item.setChecked(False)

    def done(self, result):
        for key, value in self.outDict.items():
            for i in xrange(self.tblDiscrepancies.rowCount()):
                if value[0] == self.tblDiscrepancies.item(i, 0).text():
                    value[2] = self.tblDiscrepancies.cellWidget(i, 3).children()[1].isChecked()
                    self.outDict[key] = value
        self.saveDialogPreferences()
        QtGui.QDialog.done(self, result)

    def exec_(self):
        self.loadDialogPreferences()
        result = QtGui.QDialog.exec_(self)
        return result
