# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDateTime

from library.InDocTable import CInDocTableModel, CRecordListModel, CDateInDocTableCol, CInDocTableCol
from library.TableView  import CTableView
from library.database   import decorateString
from library.Utils      import trim, forceRef, forceStringEx, forceString, forceInt, toVariant, getPref, setPref

__all__ = ( 'CIdentificationModel',
            'checkIdentification',
            'CAccountingSystemComboBox'
          )


class CIdentificationModel(CInDocTableModel):
    def __init__(self, parent, tableName, key):
        CInDocTableModel.__init__(self, tableName, 'id', 'master_id', parent)

        filter = u'''FIND_IN_SET(%s, REPLACE(domain, ' ', ''))>0 OR domain='' ''' % decorateString(key)
        self.addCol(CAccountingSystemInDocTableCol(u'Справочник', 'system_id', 40, filter=filter))
        self.addCol(CInDocTableCol(    u'Идентификатор', 'value',       30))
        self.addCol(CDateInDocTableCol(u'Дата подтверждения', 'checkDate', 20))
        self.addCol(CInDocTableCol(u'Примечание', 'note', 40))


    def identificationPresent(self, systemId, value):
        for item in self.items():
            if (     forceRef(item.value('system_id')) == systemId
                 and forceStringEx(item.value('value')) == value
               ):
                   return True
        return False


    def addIdentification(self, systemId, value):
        trimmedValue = trim(value)
        if self.identificationPresent(systemId, trimmedValue):
            return False
        item = self.getEmptyRecord()
        item.setValue('system_id', systemId)
        item.setValue('value', trimmedValue)
        item.setValue('checkDate', QDateTime.currentDateTime())
        self.addRecord(item)


def checkIdentification(dialog, tableWidget):
    model = tableWidget.model()
    for row, item in enumerate(model.items()):
        systemId = forceRef(item.value('system_id'))
        value    = forceStringEx(item.value('value'))
        if not (systemId or dialog.checkInputMessage(u'справочник',  False, tableWidget, row, 0)):
            return False
        if not (value or dialog.checkInputMessage(u'идентификатор', False, tableWidget, row, 1)):
            return False
    return True


class CAccountingSystemComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self._model = CRecordListModel(self)
        self._model.addCol(CInDocTableCol(u'Код', 'code', 20))
        self._model.addCol(CInDocTableCol(u'Наименование', 'name', 40))
        self._model.addCol(CInDocTableCol(u'urn', 'urn', 40))
        
        self._view = CTableView(None)
        self._view.setModel(self._model)
        self.setView(self._view)
        self.setModel(self._model)
        self.setModelColumn(1)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    
    
    def showPopup(self):
        width = self.parent().width()
        self.view().setMinimumWidth(width)
        self.view().setMaximumWidth(width)
        super(CAccountingSystemComboBox, self).showPopup()


    def value(self):
        row = self.currentIndex()
        return self._model.items()[row].value('id')


    def setValue(self, itemId):
        idList = [r.value('id') for r in self._model.items()]
        index = 0
        try:
            index = idList.index(itemId)
        except ValueError:
            index = 0
        self.setCurrentIndex(index)


    def setItems(self, recordList):
        self._model.setItems(recordList)



class CAccountingSystemInDocTableCol(CInDocTableCol):
    mapFilterToRecords = {}

    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.filter = params.get('filter', '')


    def _getItems(self):
        recordList = self.mapFilterToRecords.get(self.filter, None)
        if recordList is None:
            recordList = QtGui.qApp.db.getRecordList('rbAccountingSystem', 'id,code,name,urn', self.filter)
            self.mapFilterToRecords[self.filter] = recordList
        return recordList


    def toString(self, val, record):
        for item in self._getItems():
            if forceInt(item.value('id')) == forceInt(val):
                return forceString(item.value('name'))


    def toSortString(self, val, record):
        return forceString(self.toString(val, record)).lower()


    def getSortString(self, val, record):
        return toVariant(self.toSortString(val, record))


    def toStatusTip(self, val, record):
        return self.toString(val, record)


    def createEditor(self, parent):
        editor = CAccountingSystemComboBox(parent)
        recordList = self._getItems()
        editor.setItems(recordList)
        prefs = getPref(QtGui.qApp.preferences.windowPrefs, u'CAccountingSystemComboBox_view', {})
        editor._view.loadPreferences(prefs)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setValue(forceInt(value))


    def getEditorData(self, editor):
        data = toVariant(editor.value())
        prefs = editor._view.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, u'CAccountingSystemComboBox_view', prefs)
        return data
