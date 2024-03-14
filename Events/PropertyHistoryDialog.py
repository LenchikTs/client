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
from PyQt4.QtCore import Qt, QVariant, pyqtSignature

from library.DialogBase  import CDialogBase
from library.InDocTable  import CInDocTableModel, CDateInDocTableCol, CEnumInDocTableCol, CInDocTableCol, CRBInDocTableCol
from library.Utils       import toVariant, forceDateTime, forceRef

from Events.ActionStatus import CActionStatus
from Registry.Utils      import getClientBanner
from Reports.ReportView  import CReportViewDialog
#from Reports.ReportBase  import CReportBase

from Events.Ui_PropertyHistoryDialog import Ui_PropertyHistoryDialog


class CPropertyHistoryDialog(CDialogBase, Ui_PropertyHistoryDialog):
    def __init__(self, clientId, actionPropertyList, parent):
        CDialogBase.__init__(self, parent)
        self.clientId = clientId
        self.actionPropertyList = actionPropertyList
        self.addModels('Values', CPropertyHistoryModel(clientId, actionPropertyList, self))
        self.addObject('btnPrint', QtGui.QPushButton(u'Печать', self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Журнал значения свойства')
        self.setModels(self.tblValues, self.modelValues, self.selectionModelValues)
        self.tblValues.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.modelValues.loadItems()

    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        format = QtGui.QTextCharFormat()
        format.setProperty(QtGui.QTextFormat.FontSizeIncrement, QVariant(2))
        format.setFontWeight(QtGui.QFont.Bold)
        cursor.setCharFormat(format)
        if len(self.actionPropertyList) == 1:
            title = u'Журнал значения свойства "' + self.actionPropertyList[0][0].type().name + '"'
        else:
            names = ['"'+actionProperty[0].type().name+'"' for actionProperty in self.actionPropertyList]
            title = u'Журнал значения свойств ' + ', '.join(names[:-1])+u' и '+names[-1]
        cursor.insertText(title)
        cursor.insertBlock()
        charFormat = QtGui.QTextCharFormat()
        cursor.setCharFormat(charFormat)
        cursor.insertText(u'пациент:')
        cursor.insertBlock()
        cursor.insertHtml(getClientBanner(self.clientId))
        self.tblValues.addContentToTextCursor(cursor)
        view = CReportViewDialog(self)
        view.setWindowTitle(u'Журнал значения свойства')
        view.setText(doc)
        view.exec_()


class CPropertyHistoryModel(CInDocTableModel):
    def __init__(self, clientId, actionPropertyList, parent):
        CInDocTableModel.__init__(self, 'ActionProperty', 'id', '', parent)
        self.clientId = clientId
        self.actionPropertyList = actionPropertyList
        self.addCol(CDateInDocTableCol(u'Начато',   'begDate', 10, canBeEmpty=True))
        self.addCol(CDateInDocTableCol(u'Окончено', 'endDate', 10, canBeEmpty=True))
        self.addCol(CEnumInDocTableCol(u'Состояние', 'status', 10, CActionStatus.names))

        for i, (actionProperty, showUnit, showNorm) in enumerate(self.actionPropertyList):
            seq = '_'+str(i+1)
            self.addCol(CActionPropertyValueTableCol(actionProperty.type().name, 'value'+seq, 30, actionProperty))
            if showUnit:
                self.addCol(CRBInDocTableCol(u'Ед.изм.', 'unit_id'+seq, 10, 'rbUnit'))
            if showNorm:
                self.addCol(CInDocTableCol(u'Норма', 'norm'+seq, 30))
        self.setEnableAppendLine(False)


    def addFieldToRecord(self, source, target):
        for fieldIndex in xrange(target.count()):
            fieldName = target.fieldName(fieldIndex)
            if source.indexOf(fieldName) == -1:
                source.append(target.field(fieldName))
                source.setValue(fieldName, QVariant(target.value(fieldName)))
        return source


    def loadItems(self):
        db = QtGui.qApp.db
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        recordDict = {}
        table = tableAction
        table = table.innerJoin(tableEvent,   tableEvent['id'].eq(tableAction['event_id']))
        for i, (actionProperty, showUnit, showNorm) in enumerate(self.actionPropertyList):
            cols = [tableAction['id'], tableAction['begDate'], tableAction['endDate'], tableAction['status']]
            cond = [tableEvent['client_id'].eq(self.clientId), tableEvent['deleted'].eq(0), tableAction['deleted'].eq(0)]
            seq = '_'+str(i+1)
            propertyType = actionProperty.type()
            tableActionProperty = db.table('ActionProperty').alias('AP'+seq)
            tableActionPropertyType  = db.table('ActionPropertyType').alias('APT'+seq)
            tableActionPropertyValue = db.table(propertyType.tableName).alias('APV'+seq)
            table = table.innerJoin(tableActionProperty, [tableActionProperty['action_id'].eq(tableAction['id']), tableActionProperty['deleted'].eq(0)])
            table = table.innerJoin(tableActionPropertyType, [tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']),
                                                              tableActionPropertyType['id'].eq(tableActionProperty['type_id']),
                                                              tableActionPropertyType['typeName'].eq(propertyType.typeName),
                                                              tableActionPropertyType['name'].eq(propertyType.name),
                                                              tableActionPropertyType['deleted'].eq(0)
                                                              ])
            table = table.innerJoin(tableActionPropertyValue, [tableActionPropertyValue['id'].eq(tableActionProperty['id']), db.joinOr([tableActionPropertyValue['value'].isNotNull(), tableActionPropertyValue['value'].ne('')])])
            cols.append(tableActionPropertyValue['value'].alias('value'+seq))
            if showUnit:
                cols.append(tableActionProperty['unit_id'].alias('unit_id'+seq))
            if showNorm:
                cols.append(tableActionProperty['norm'].alias('norm'+seq))
            cond.append(tableActionProperty['id'].isNotNull())

            order= [tableAction['endDate'].name()+' DESC',
                    tableAction['id'].name()
                   ]

            records = db.getRecordList(table, cols, cond, order)
            for record in records:
                actionId = forceRef(record.value('id'))
                actionLine = recordDict.get(actionId, None)
                recordDict[actionId] = self.addFieldToRecord(actionLine, record) if actionLine else record
        items = recordDict.values()
        items.sort(key=lambda x:forceDateTime(x.value('endDate')), reverse=True)
        self.setItems(items)


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return CInDocTableModel.data(self, index, role)
        elif role == Qt.TextAlignmentRole:
            return QVariant(Qt.AlignLeft|Qt.AlignTop)
        return QVariant()


class CActionPropertyValueTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, actionProperty):
        CInDocTableCol.__init__(self, title, fieldName, width)
        self.actionPropertyValueType = actionProperty.type().valueType
        self.cache = {}


    def toString(self, val, record):
        key = val.toPyObject() if val else None # т.к. hash(QVariant()) зависит от адреса QVariant-а и не зависит от значения
        if key in self.cache:
            return self.cache[key]
        else:
            result = toVariant(self.actionPropertyValueType.toText(val))
            self.cache[key] = result
            return result
