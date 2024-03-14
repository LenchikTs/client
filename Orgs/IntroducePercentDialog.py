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
from PyQt4.QtCore import Qt, QAbstractTableModel, QVariant

from library.DialogBase import CDialogBase
from library.Utils import agreeNumberAndWord, forceDouble, forceRef, forceString, toVariant

from Ui_IntroducePercentDialog import Ui_IntroducePercentDialog


class CIntroducePercentDialog(CDialogBase, Ui_IntroducePercentDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
        self.setWindowTitle(u'Заполнение затрат')


    def preSetupUi(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.addModels('IntroducePercent', CIntroducePercentModel(self))


    def postSetupUi(self):
        self.setModels(self.tblIntroducePercent, self.modelIntroducePercent, self.selectionModelIntroducePercent)


    def saveData(self):
        total = sum( percent for (expenceId, percent) in self.modelIntroducePercent.getExpenceIdAndPercentList() )
        if total>100.001:
            QtGui.QMessageBox.critical(self, u'Ошибка!', u'Сумма процентов больше 100', QtGui.QMessageBox.Close)
            return False
        return True


    def prepare(self, cnt):
        self.modelIntroducePercent.loadData()
        self.lblSelectionRows.setText( agreeNumberAndWord(cnt, (u'Выделена %d строка', u'Выделенo %d строки', u'Выделенo %d строк')) % cnt )


    def selectExpencesAndPercents(self):
        if self.exec_():
            return self.modelIntroducePercent.getExpenceIdAndPercentList()
        else:
            return None


class CIntroducePercentModel(QAbstractTableModel):
    headerText = [u'Затрата', u'Процент']

    def __init__(self,  parent):
        QAbstractTableModel.__init__(self, parent)
#        self._cols = []
        self.items = []


    def columnCount(self, index = None):
        return 2


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index):
        column = index.column()
        if column == 0:
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return toVariant(item[column])
        return QVariant()


    def loadData(self):
        db = QtGui.qApp.db
        table = db.table('rbExpenseServiceItem')
        records = db.getRecordList(table, '*')
        for record in records:
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            id = forceRef(record.value('id'))
            item = [code + u'|' + name, 0.0, id]
            self.items.append(item)
        self.reset()


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        row = index.row()
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if column == 1:
               self.items[row][1] = forceDouble(value)
               #self.emitCellChanged(row, column)
               return True
        return False


    def getExpenceIdAndPercentList(self):
        return [ (item[2], item[1]) for item in self.items ]
