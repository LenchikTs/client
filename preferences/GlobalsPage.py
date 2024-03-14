# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница с глобальными настройками
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, Qt

from library.TableModel       import CTableModel, CTextCol
from library.Utils import (
    forceString, forceInt,
)

from Ui_GlobalsPage import Ui_globalsPage
import re


class CGlobalsPage(Ui_globalsPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.modelGlobalPreferences = CGlobalPreferencesModel(self)
        self.selectionModelGlobalPreferences = QtGui.QItemSelectionModel(self.modelGlobalPreferences, self)
        self.tblGlobal.setModel(self.modelGlobalPreferences)
        self.tblGlobal.setSelectionModel(self.selectionModelGlobalPreferences)
        self.tblGlobal.setSortingEnabled(True)


    def setProps(self, props):
        self.refreshGlobalPreferences()


    def getProps(self, props):
        pass


    def refreshGlobalPreferences(self):
        self.modelGlobalPreferences.setIdList(QtGui.qApp.db.getIdList('GlobalPreferences'))


    @pyqtSignature('QModelIndex')
    def on_tblGlobal_doubleClicked(self, index):
        if QtGui.qApp.userHasAnyRight(['adm', 'setupGlobalPreferencesEdit']):
            item = self.tblGlobal.currentItem()
            currentValue = forceString(item.value('value'))
            note = forceString(item.value('note'))
            code = forceString(item.value('code'))
            if code == u'numberDecimalPlacesQnt':
                currentValue = forceInt(item.value('value'))
                newValue, ok = QtGui.QInputDialog.getInt(self,
                                                         u'Редактор',
                                                         u'Значение\n' + note,
                                                         value=currentValue, min=0, max=6, step=1)
            else:
                values = [y.replace("\"", '') for y in re.findall('\".*?\"', note)]
                if len(values) > 1:
                    if currentValue == u'жесткий':
                        currentValue.replace(u"е", u"ё")
                    ind = values.index(currentValue)
                    newValue, ok = QtGui.QInputDialog.getItem(self,
                                                              u'Редактор',
                                                              u'Значение\n' + note,
                                                              values,
                                                              ind,
                                                              False)
                else:
                    newValue, ok = QtGui.QInputDialog.getText(self,
                                                              u'Редактор',
                                                              u'Значение\n' + note,
                                                              QtGui.QLineEdit.Normal,
                                                              currentValue)
            if ok and unicode(newValue) != unicode(currentValue):
                item.setValue('value', newValue)
                QtGui.qApp.db.updateRecord('GlobalPreferences', item)
                self.refreshGlobalPreferences()


# ########################################################


class CGlobalPreferencesModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Код', ['code'], 10))
        self.addColumn(CTextCol(u'Наименование', ['name'], 18))
        self.addColumn(CTextCol(u'Значение', ['value'], 10))
        self.loadField('note')
        self.setTable('GlobalPreferences')
    
    
    def sort(self, col, order=Qt.AscendingOrder):
        reverse = order == Qt.DescendingOrder
        if self._idList:
            db = QtGui.qApp.db
            table = db.table('GlobalPreferences')
            colClass = self.cols()[col]
            colName = colClass.fields()[0]
            order = '{} {}'.format(colName, u'DESC' if order else u'ASC')
            self._idList = db.getIdList(table, order=order)
            self.reset()
