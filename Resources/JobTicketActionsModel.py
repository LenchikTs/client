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
from PyQt4.QtCore import Qt, QVariant, SIGNAL

from library.TableModel           import CTableModel, CBoolCol, CDateTimeCol, CDesignationCol, CEnumCol, CRefBookCol, CSumCol, CTextCol
from library.Utils                import forceBool, forceDate, forceRef, forceString

from Events.ActionStatus          import CActionStatus
from Events.Utils                 import getIsRequiredCoordination


class CJobTicketActionsModel(CTableModel):
    mkbFieldType = 0
    morphologyMKBFieldType = 1

    class CMKBCol(CTextCol):
        _fieldType2fieldName = {0:'MKB',
                                1:'morphologyMKB'}
        def __init__(self, title, fieldType, defaultWidth):
            CTextCol.__init__(self, title, [self._fieldType2fieldName[fieldType]], defaultWidth)
            self._fieldType = fieldType
            self._cacheEventValue = {}


        def format(self, values):
            value = forceString(values[0])
            if not value:
                record = values[1]
                eventId = forceRef(record.value('event_id'))
                value = self._cacheEventValue.get(eventId, None)
                if value is None:
                    value = ''
                    db = QtGui.qApp.db
                    tableDiagnostic = db.table('Diagnostic')
                    tableDiagnosisType = db.table('rbDiagnosisType')

                    queryTable = tableDiagnostic.leftJoin(
                                              tableDiagnosisType,
                                              tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id']))
                    cond = [tableDiagnostic['deleted'].eq(0),
                            tableDiagnostic['event_id'].eq(eventId),
                            tableDiagnosisType['code'].inlist(['1', '2'])]
                    recordList = db.getRecordList(queryTable,
                                                  tableDiagnostic['diagnosis_id'].name(),
                                                  cond)
                    if recordList:
                        diagnosisId = forceRef(recordList[0].value('diagnosis_id'))
                        if diagnosisId:
                            value = forceString(db.translate('Diagnosis', 'id',
                                                             diagnosisId, self._fieldType2fieldName[self._fieldType]))
                    self._cacheEventValue[eventId] = value
            return QVariant(value)


    class CCheckCol(CBoolCol):
        def __init__(self, title, fields, defaultWidth):
            self._cache = {}
            CBoolCol.__init__(self, title, fields, defaultWidth)

        def resetCache(self):
            self._cache.clear()


        def checked(self, values):
            actionId = forceRef(values[0])
            return self._cache.get(actionId, CBoolCol.valUnchecked)

        def setChecked(self, actionId, value):
            self._cache[actionId] = value

        def getCheckedActionIdList(self):
            return [actionId for actionId, value in self._cache.items() if forceBool(value)]


    class CCheckColorCol(CBoolCol):
        def __init__(self, title, fields, defaultWidth):
            self._cache = {}
            CBoolCol.__init__(self, title, fields, defaultWidth)

        def getForegroundColor(self, values):
#            actionId = forceRef(values[0])
            actionTypeId = forceRef(values[1])
            coordDate = forceDate(values[2])
            isRequiredCoordination = getIsRequiredCoordination(actionTypeId)
            if isRequiredCoordination and not coordDate:
                return QVariant(QtGui.QColor(Qt.red))
            elif isRequiredCoordination and coordDate:
                return QVariant(QtGui.QColor(Qt.black))

        def resetCache(self):
            self._cache.clear()

        def checked(self, values):
            actionId = forceRef(values[0])
            actionTypeId = forceRef(values[1])
#            coordDate = forceDate(values[2])
            isRequiredCoordination = getIsRequiredCoordination(actionTypeId)
            return self._cache.get(actionId, CBoolCol.valChecked if isRequiredCoordination else CBoolCol.valUnchecked)

        def setChecked(self, actionId, value):
            self._cache[actionId] = value


    def __init__(self, parent, fromOperationDialog=False):
        self._parent = parent
        self._fromOperationDialog = fromOperationDialog
        self._checkCol = CJobTicketActionsModel.CCheckCol(u'Включить', ['id'], 6)
        self._checkCol2 = CJobTicketActionsModel.CCheckColorCol(u'Согласовано', ['id', 'actionType_id', 'coordDate'], 6)
        fields = [
                  self._checkCol,
                  CDesignationCol(u'Мероприятие',   ['actionType_id'], ('ActionType', 'name'),  20),
                  CJobTicketActionsModel.CMKBCol(u'МКБ', CJobTicketActionsModel.mkbFieldType, 8),
                  CEnumCol(u'Статус', ['status'], CActionStatus.names, 6),
                  CSumCol(u'Количество',            ['amount'], 10),
                  CDateTimeCol(   u'Назначено',     ['directionDate'], 20),
                  CDesignationCol(u'Назначил',      ['setPerson_id'],  ('vrbPersonWithSpeciality', 'name'), 20),
                  CDateTimeCol(   u'План',          ['plannedEndDate'], 20),
                  CDateTimeCol(   u'Выполнено',     ['endDate'], 20),
                  CDesignationCol(u'Ответственный', ['person_id'],     ('vrbPersonWithSpeciality', 'name'), 20),
                  CDesignationCol(u'Ассистент',     ['assistant_id'],  ('vrbPersonWithSpeciality', 'name'), 20), 
                  CDesignationCol(u'Особенности выполения', ['actionSpecification_id'], ('rbActionSpecification', 'name'), 20)
                 ]

        if fromOperationDialog:
            fields.insert(1, CBoolCol(u'Срочно', ['isUrgent'], 6))
            fields.insert(2, self._checkCol2)
            fields.insert(4, CRefBookCol(u'Тип финансирования', ['finance_id'], u'rbFinance', 8))
        if QtGui.qApp.defaultMorphologyMKBIsVisible():
            fields.insert(3, CJobTicketActionsModel.CMKBCol(u'Морфология МКБ',
                                                            CJobTicketActionsModel.morphologyMKBFieldType, 14))
        CTableModel.__init__(self, parent,  fields)
        self.loadField('*')
        self.setTable('Action', recordCacheCapacity=None)
        boldFont = QtGui.QFont()
        boldFont.setWeight(QtGui.QFont.Bold)
        self._qBoldFont = QVariant(boldFont)
        self._mkbColIndex = 5 if fromOperationDialog else 3


    def setAllChecked(self):
        for row in xrange(len(self.idList())):
            self.setData(self.index(row, 0), QVariant(Qt.Checked), role=Qt.CheckStateRole)

    def setCheckedById(self, actionId):
        idList = self.idList()
        if actionId in idList:
            self.setData(self.index(idList.index(actionId), 0), QVariant(Qt.Checked), role=Qt.CheckStateRole)


    def resetChecked(self):
        self._checkCol.resetCache()


    def getCheckedActionIdList(self):
        return list(set(self._checkCol.getCheckedActionIdList()) & set(self.idList()))


    def deleteRecord(self, table, itemId):
        CTableModel.deleteRecord(self, table, itemId)
        self._parent.removeCanDeletedId(itemId)


    def getActionTypeId(self, actionId):
        record = self.getRecordById(actionId)
        if record:
            return forceRef(record.value('actionType_id'))
        return None


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.FontRole:
            column = index.column()
            if column == self._mkbColIndex:
                row = index.row()
                (col, values) = self.getRecordValues(column, row)
                if not forceString(values[0]): # если МКБ не указано в Действии и мы смотри по событию.
                    return self._qBoldFont
            return QVariant()
        return CTableModel.data(self, index, role)


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        column = index.column()
        if role == Qt.CheckStateRole and column == 0:
            row = index.row()
            actionId = self._idList[row]
            value = CBoolCol.valChecked if forceBool(value) else CBoolCol.valUnchecked
            self._checkCol.setChecked(actionId, value)
            self.emitCellChanged(row, column)
            return True
        return False


    def flags(self, index=None):
        if index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return CTableModel.flags(self, index)


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)

