# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QVariant
import json

from ActionPropertyValueType import CActionPropertyValueType
from library.Utils import forceString


class CJSONActionPropertyValueType(CActionPropertyValueType):
    name                = 'JSON'
    variantType         = QVariant.String
    preferredHeight     = 64
    preferredHeightUnit = 0
    isHtml              = True
    isImage             = False


    class CPropEditor(QtGui.QTableWidget):
        __pyqtSignals__ = ('commit()',
                          )


        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QTableWidget.__init__(self, parent)
            self.setFocusPolicy(Qt.StrongFocus)
            self.horizontalHeader().setStretchLastSection(True)
            self.verticalHeader().setStretchLastSection(True)
            self._value = None


        def setValue(self, value):
            if forceString(value) == u'[]' or forceString(value) == u'':
                json_data = u'''[ 
                        {"Тест 1": "", "Тест 2": "", "Тест 3": ""}, 
                        {"Тест 1": "", "Тест 2": "", "Тест 3": ""}, 
                        {"Тест 1": "", "Тест 2": "", "Тест 3": ""} 
                    ]
                ''' .encode('utf-8')
                self._value = json.loads(json_data) 
            else:
                self._value = json.loads(forceString(value))
            self.setRowCount(len(self._value)) 
            self.setColumnCount(len(self._value[0])) 
 
            # Set the table headers 
            headers = list(self._value[0].keys()) 
            self.setHorizontalHeaderLabels(headers) 
 
            # Populate the table with data 
            for row_idx, row_data in enumerate(self._value): 
                for col_idx, value in enumerate(row_data.values()): 
                    item = QtGui.QTableWidgetItem(str(value)) 
                    self.setItem(row_idx, col_idx, item) 
 
            # Auto-resize columns to fit content 
            self.resizeColumnsToContents()


        def value(self):
            data = [] 
            for row_idx in range(self.rowCount()): 
                row_data = {} 
                for col_idx in range(self.columnCount()): 
                    item = self.item(row_idx, col_idx) 
                    if item is not None: 
                        row_data[forceString(self.horizontalHeaderItem(col_idx).text())] = forceString(item.text())
                data.append(row_data) 
            return json.dumps(data)



    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix + 'JSON'

    @staticmethod
    def convertDBValueToPyValue(value):
        if value.type() == QVariant.String:
            return value.toString()
        return None

    @staticmethod
    def convertQVariantToPyValue(value):
        if value.type() == QVariant.String:
            return value.toString()
        return None

    @staticmethod
    def convertPyValueToDBValue(value):
        if value:
            return QVariant(value)
        return None