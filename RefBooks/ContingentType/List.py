# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QVariant, SIGNAL

from library.AgeSelector       import parseAgeSelector
from library.crbcombobox       import CRBComboBox
from library.InDocTable        import CInDocTableModel, CEnumInDocTableCol, CInDocTableCol, CIntInDocTableCol, CRBInDocTableCol
from library.interchange       import getLineEditValue, getSpinBoxValue, setLineEditValue, setSpinBoxValue
from library.ItemsListDialog   import CItemsListDialog, CItemEditorBaseDialog
from library.MES.MESComboBox   import CMESComboBox
from library.TableModel        import CNumCol, CTextCol
from library.Utils             import forceBool, forceInt, forceRef, forceString, toVariant

from Events.ActionTypeComboBox import CActionTypeTableCol
from RefBooks.Tables           import rbCode, rbName


from .Ui_RBContingentType import Ui_RBContingentTypeEditor

class CRBContingentTypeList(CItemsListDialog):
    class COperationCol(CTextCol):
        def format(self, values):
            return QVariant(CContingentTypeTranslator.formatOperationValue(forceInt(values[0]), forceInt(values[1]), forceInt(values[2])))

    def __init__(self, parent):
        priorityCol = CNumCol(u'Приоритет', ['priority'], 10)
        priorityCol.setToolTip(u'0-Выключено(не применяется)')
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode],                                    20),
            CTextCol(u'Наименование', [rbName],                                    40),
            priorityCol,
            CRBContingentTypeList.COperationCol(u'Операция',     ['contingentOperation', 'observedOperation', 'eventOrActionOperation'], 10)
            ], 'rbContingentType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы наблюдаемого контингента')
        self.actDuplicate = QtGui.QAction(u'Дублировать запись', self)
        self.actDuplicate.setObjectName('actDuplicate')
        self.connect(self.actDuplicate, SIGNAL('triggered()'), self.duplicateCurrentInternal)
        self.tblItems.createPopupMenu([self.actDuplicate])
        self.tblItems.addPopupDelRow()

    def duplicateCurrentInternal(self):
        currentItemId = self.tblItems.currentItemId()
        if currentItemId:
            db = QtGui.qApp.db
            tableContingentType = db.table('rbContingentType')
            tableContingentType_ActionType = db.table('rbContingentType_ActionType')
            tableContingentType_EventType = db.table('rbContingentType_EventType')
            tableContingentType_HealthGroup = db.table('rbContingentType_HealthGroup')
            tableContingentType_MES = db.table('rbContingentType_MES')
            tableContingentType_SexAge = db.table('rbContingentType_SexAge')
            tableContingentType_SocStatus = db.table('rbContingentType_SocStatus')
            tableContingentType_ContingentKind = db.table('rbContingentType_ContingentKind')
            tables = [tableContingentType_ActionType,
                            tableContingentType_EventType,
                            tableContingentType_HealthGroup,
                            tableContingentType_MES,
                            tableContingentType_SexAge,
                            tableContingentType_SocStatus,
                            tableContingentType_ContingentKind]
            db.transaction()
            try:
                recordContingentType = db.getRecord(tableContingentType, '*', currentItemId)
                recordContingentType.setNull('id')
                currentCode = forceString(recordContingentType.value('code'))
                currentName = forceString(recordContingentType.value('name'))
                recordContingentType.setValue('code', currentCode + '*')
                recordContingentType.setValue('name', currentName + u' (копия)')
                newItemId = db.insertRecord(tableContingentType, recordContingentType)
                for tableItem in tables:
                    records = db.getRecordList(
                        tableItem, '*',
                        tableItem['master_id'].eq(currentItemId))
                    for record in records:
                        record.setNull('id')
                        record.setValue('master_id', toVariant(newItemId))
                        db.insertRecord(tableItem, record)
                db.commit()
            except:
                db.rollback()
                QtGui.qApp.logCurrentException()
                raise
            self.renewListAndSetTo(newItemId)


    def getItemEditor(self):
        return CRBContingentTypeEditor(self)


#
# ##########################################################################
#


class CRBContingentTypeEditor(CItemEditorBaseDialog, Ui_RBContingentTypeEditor):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbContingentType')
        self.setupUi(self)

        self.addModels(u'SexAge',    CContingentTypeSexAgeModel(self))
        self.addModels(u'SocStatus', CContingentTypeSocStatusModel(self))
        self.addModels(u'ContingentKind', CContingentTypeContingentKindModel(self))
        self.addModels(u'EventType', CContingentTypeEventTypeModel(self))
        self.addModels(u'ActionType',CContingentTypeActionTypeModel(self))
        self.addModels(u'MES',       CContingentTypeMESModel(self))
        self.addModels(u'HealtGroup',CContingentTypeHealthGroupModel(self))

        self.setModels(self.tblSexAge,    self.modelSexAge,    self.selectionModelSexAge)
        self.setModels(self.tblSocStatus, self.modelSocStatus, self.selectionModelSocStatus)
        self.setModels(self.tblContingentKind, self.modelContingentKind, self.selectionModelContingentKind)
        self.setModels(self.tblEventType, self.modelEventType, self.selectionModelEventType)
        self.setModels(self.tblActionType,self.modelActionType,self.selectionModelActionType)
        self.setModels(self.tblMES,       self.modelMES,       self.selectionModelMES)
        self.setModels(self.tblHealtGroup,self.modelHealtGroup,self.selectionModelHealtGroup)

        self.tblSexAge.addPopupDelRow()
        self.tblSocStatus.addPopupDelRow()
        self.tblContingentKind.addPopupDelRow()
        self.tblEventType.addPopupDelRow()
        self.tblActionType.addPopupDelRow()
        self.tblMES.addPopupDelRow()
        self.tblHealtGroup.addPopupDelRow()

        self.setWindowTitleEx(u'Тип наблюдаемого контингента')


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,      record, 'code')
        setLineEditValue(self.edtName,      record, 'name')
        setSpinBoxValue(self.edtPriority,   record, 'priority')

        contingentOperationStorageValue = forceInt(record.value('contingentOperation'))
        self.cmbSASSOT.setCurrentIndex(CContingentTypeTranslator.formatSASSOTValue(contingentOperationStorageValue))
        observedOperationStorageValue = forceInt(record.value('observedOperation'))
        self.cmbETMOT.setCurrentIndex(CContingentTypeTranslator.formatETMOTValue(observedOperationStorageValue))
        eventOrActionOperationValue = forceInt(record.value('eventOrActionOperation'))
        self.cmbATOP.setCurrentIndex(CContingentTypeTranslator.formatATOPValue(eventOrActionOperationValue))

        itemId = self.itemId()

        self.modelSexAge.loadItems(itemId)
        self.modelSocStatus.loadItems(itemId)
        self.modelContingentKind.loadItems(itemId)
        self.modelEventType.loadItems(itemId)
        self.modelActionType.loadItems(itemId)
        self.modelMES.loadItems(itemId)
        self.modelHealtGroup.loadItems(itemId)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,      record, 'code')
        getLineEditValue(self.edtName,      record, 'name')
        getSpinBoxValue(self.edtPriority,   record, 'priority')
        contingentOperationStorageValue = CContingentTypeTranslator.formatStorageValue(self.cmbSASSOT.currentIndex())

        record.setValue('contingentOperation', QVariant(contingentOperationStorageValue))
        observedOperationStorageValue = CContingentTypeTranslator.formatStorageValue(self.cmbETMOT.currentIndex())
        record.setValue('observedOperation', QVariant(observedOperationStorageValue))
        eventOrActionOperationValue = CContingentTypeTranslator.formatStorageValue(self.cmbATOP.currentIndex())
        record.setValue('eventOrActionOperation', QVariant(eventOrActionOperationValue))
        return record

    def saveInternals(self, itemId):
        self.modelSexAge.saveItems(itemId)
        self.modelSocStatus.saveItems(itemId)
        self.modelContingentKind.saveItems(itemId)
        self.modelEventType.saveItems(itemId)
        self.modelActionType.saveItems(itemId)
        self.modelMES.saveItems(itemId)
        self.modelHealtGroup.saveItems(itemId)


# ####################################

class CContingentTypeSexAgeModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_SexAge', 'id', 'master_id', parent)
        self.addCol(CEnumInDocTableCol( u'Пол',              'sex',            5, ['', u'М', u'Ж']))
        self.addCol(CInDocTableCol(     u'Возраст',          'age',            12))
        self.addCol(CEnumInDocTableCol( u'Период контроля',  'controlPeriod',  15, [u'Текущая дата', u'Конец предыдущего года', u'Конец текущего года', u'В текущем году']))


class CContingentTypeSocStatusModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_SocStatus', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Соц.статус',          'socStatusType_id', 6,  'rbSocStatusType'))
        self.addCol(CEnumInDocTableCol( u'Период контроля',  'controlPeriod',    15, [u'Текущая дата', u'Конец предыдущего года', u'Конец текущего года']))


class CContingentTypeContingentKindModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_ContingentKind', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Вид контингента',    'contingentKind_id', 6,  'rbContingentKind'))
        self.addCol(CRBInDocTableCol(u'Специальность',      'speciality_id',     30, 'rbSpeciality', showFields=CRBComboBox.showNameAndCode, order='code'))
        self.addCol(CEnumInDocTableCol(u'Период контроля', 'controlPeriod',     15, [u'Текущая дата', u'Конец предыдущего года', u'Конец текущего года']))


# #######
class CFreePeriodModelMixin(object):
    def __init__(self):
        self.freePeriodCol = CIntInDocTableCol(u'Произвольный период', 'freePeriod', 6)
        self.addCol(self.freePeriodCol)
        self._freePeriodColIndex = self.getColIndex(u'freePeriod')


    def flags(self, index=None):
        if index and index.isValid():
            row = index.row()
            column = index.column()
            if column == self._freePeriodColIndex and  0 <= row < len(self._items):
                controlPeriod = forceBool(self._items[row].value('controlPeriod'))
                result = Qt.ItemIsSelectable
                if controlPeriod:
                    result |= Qt.ItemIsEditable | Qt.ItemIsEnabled
                return result

        return CInDocTableModel.flags(self, index)


class CContingentTypeEventTypeModel(CFreePeriodModelMixin, CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_EventType', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Тип события',         'eventType_id',  6,  'EventType'))
        self.addCol(CEnumInDocTableCol( u'Период контроля',  'controlPeriod', 15, [u'В текущем году', u'Произвольный период в днях', u'Произвольный период в неделях',  u'Произвольный период в месяцах', u'Произвольный период в годах']))

        CFreePeriodModelMixin.__init__(self)


class CContingentTypeActionTypeModel(CFreePeriodModelMixin, CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_ActionType', 'id', 'master_id', parent)
        self.addCol(CActionTypeTableCol(u'Тип действия',   'actionType_id', 15, None, classesVisible=True))
        self.addCol(CEnumInDocTableCol( u'Период контроля',  'controlPeriod',  15, [u'В текущем году', u'Произвольный период в днях', u'Произвольный период в неделях',  u'Произвольный период в месяцах', u'Произвольный период в годах']))

        CFreePeriodModelMixin.__init__(self)


class CContingentTypeMESModel(CFreePeriodModelMixin, CInDocTableModel):

    class CMesCol(CRBInDocTableCol):
        def __init__(self):
            CRBInDocTableCol.__init__(self, u'МЭС', u'MES_id', 15, 'mes.MES', showFields=CRBComboBox.showCodeAndName)


        def createEditor(self, parent):
            editor = CMESComboBox(parent)
            return editor

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_MES', 'id', 'master_id', parent)
        self.addCol(CContingentTypeMESModel.CMesCol())
        self.addCol(CEnumInDocTableCol( u'Период контроля', 'controlPeriod', 15, [u'В текущем году', u'Произвольный период в днях', u'Произвольный период в неделях',  u'Произвольный период в месяцах', u'Произвольный период в годах']))

        CFreePeriodModelMixin.__init__(self)


class CContingentTypeHealthGroupModel(CFreePeriodModelMixin, CInDocTableModel):

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContingentType_HealthGroup', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'ГрЗд', 'healthGroup_id', 7, 'rbHealthGroup', addNone=True, showFields=CRBComboBox.showCode, preferredWidth=150)).setToolTip(u'Группа здоровья')
        self.addCol(CEnumInDocTableCol(u'Период контроля', 'controlPeriod', 15, [u'В текущем году', u'Произвольный период в днях', u'Произвольный период в неделях',  u'Произвольный период в месяцах', u'Произвольный период в годах']))

        CFreePeriodModelMixin.__init__(self)


# ###############################################################################################


class CContingentTypeTranslator(object):
    MSASSE    = 1  # маска что условие пола, возраста и соц статуса включено
    MSASSOTO  = 2  # маска что условие пола, возраста и соц статуса соединяется по ИЛИ (иначе И)
    METME     = 1  # маска что условие типа события и МЭС включено
    METMOTO   = 2  # маска что условие типа события и МЭС соединяется по ИЛИ (иначе И)
    METATE    = 1  # маска что условие типа события и типа действие включено
    METATOTO  = 2  # маска что условие типа события и типа действие соединяется по ИЛИ (иначе И)
    METHGE    = 1  # маска что условие типа события и Группа здоровья включено
    METHGOTO  = 2  # маска что условие типа события и Группа здоровья соединяется по ИЛИ (иначе И)

    d_OR_AND  = {0: u'И', 1: u'ИЛИ'}

    CTTName   = 'rbContingentType'
    CTSATName = 'rbContingentType_SexAge'
    CTSSTName = 'rbContingentType_SocStatus'
    CTCKTName = 'rbContingentType_ContingentKind'
    CTETTName = 'rbContingentType_EventType'
    CTATTName = 'rbContingentType_ActionType'
    CTMTName  = 'rbContingentType_MES'
    CTHGTName = 'rbContingentType_HealthGroup'


    @classmethod
    def formatOperationType(cls, operationValue):
        return cls.d_OR_AND[operationValue]

    @classmethod
    def formatHealthGroupOperationType(cls, value):
        return cls.formatOperationType(cls.isHealthGroupOperationType_OR(value))

    @classmethod
    def formatSexAgeSocStatusOperationType(cls, value):
        return cls.formatOperationType(cls.isSexAgeSocStatusOperationType_OR(value))

    @classmethod
    def formatEventTypeMESOperationType(cls, value):
        return cls.formatOperationType(cls.isEventTypeMESOperationType_OR(value))

    @classmethod
    def formatEventTypeActionTypeOperationType(cls, value):
        return cls.formatOperationType(cls.isEventTypeActionTypeOperationType_OR(value))

    @classmethod
    def formatCommonOperationType(cls):
        return ' | '

    @classmethod
    def isHealthGroupEnabled(cls, value):
        return value & cls.METHGE

    @classmethod
    def isHealthGroupOperationType_OR(cls, value):
        return (value & cls.METHGOTO) == cls.METHGOTO

    @classmethod
    def isSexAgeSocStatusEnabled(cls, value):
        return value & cls.MSASSE

    @classmethod
    def isSexAgeSocStatusOperationType_OR(cls, value):
        return (value & cls.MSASSOTO) == cls.MSASSOTO

    @classmethod
    def isEventTypeMESEnabled(cls, value):
        return value & cls.METME

    @classmethod
    def isEventTypeActionTypeEnabled(cls, value):
        return value & cls.METATE

    @classmethod
    def isEventTypeMESOperationType_OR(cls, value):
        return (value & cls.METMOTO) == cls.METMOTO

    @classmethod
    def isEventTypeActionTypeOperationType_OR(cls, value):
        return (value & cls.METATOTO) == cls.METATOTO

    @classmethod
    def getHealthGroup(cls, value):
        isHealthGroupEnabled = cls.isHealthGroupEnabled(value)
        if isHealthGroupEnabled:
            return u'Событие %s Группа здоровья' % cls.formatHealthGroupOperationType(value)
        return None

    @classmethod
    def getSexAgeSocStatus(cls, value):
        isSexAgeSocStatusEnabled = cls.isSexAgeSocStatusEnabled(value)
        if isSexAgeSocStatusEnabled:
            return u'ПВ %(val)s Соц.Статус %(val)s Вид контингента' % {'val': cls.formatSexAgeSocStatusOperationType(value)}
        return None

    @classmethod
    def getEventTypeMES(cls, value):
        isEventTypeMESEnabled = cls.isEventTypeMESEnabled(value)
        if isEventTypeMESEnabled:
            return u'Событие %s МЭС' % cls.formatEventTypeMESOperationType(value)
        return None


    @classmethod
    def getEventTypeActionType(cls, value):
        isEventTypeActionTypeEnabled = cls.isEventTypeActionTypeEnabled(value)
        if isEventTypeActionTypeEnabled:
            return u'Событие %s Действие' % cls.formatEventTypeActionTypeOperationType(value)
        return None


    @classmethod
    def formatOperationValue(cls, contingentOperation, observedOperation, eventOrActionOperation):
        sexAgeSocStatus = cls.getSexAgeSocStatus(contingentOperation)
        eventTypeMES = cls.getEventTypeMES(observedOperation)
        healthGroup = cls.getHealthGroup(observedOperation)
        eventTypeActionType = cls.getEventTypeActionType(eventOrActionOperation)
        if healthGroup and sexAgeSocStatus and eventTypeMES and eventTypeActionType:
            return u'(%s) %s (%s) %s (%s) %s (%s)' %(sexAgeSocStatus, cls.formatCommonOperationType(), eventTypeMES, cls.formatCommonOperationType(), healthGroup, cls.formatCommonOperationType(), eventTypeActionType)
        if sexAgeSocStatus:
            return sexAgeSocStatus
        elif eventTypeMES:
            return eventTypeMES
        elif healthGroup:
            return healthGroup
        elif eventTypeActionType:
            return eventTypeActionType
        else:
            return u''


    @classmethod
    def formatStorageValue(cls, cmbValue):
        return {0:0, 1:1, 2:3}[cmbValue]

    @classmethod
    def formatETHGOTOValue(cls, storageValue):
        if cls.isHealthGroupEnabled(storageValue):
            return cls.isHealthGroupOperationType_OR(storageValue)+1
        return 0

    @classmethod
    def formatSASSOTValue(cls, storageValue):
        if cls.isSexAgeSocStatusEnabled(storageValue):
            return cls.isSexAgeSocStatusOperationType_OR(storageValue)+1
        return 0

    @classmethod
    def formatETMOTValue(cls, storageValue):
        if cls.isEventTypeMESEnabled(storageValue):
            return cls.isEventTypeMESOperationType_OR(storageValue)+1
        return 0

    @classmethod
    def formatATOPValue(cls, storageValue):
        if cls.isEventTypeActionTypeEnabled(storageValue):
            return cls.isEventTypeActionTypeOperationType_OR(storageValue)+1
        return 0


# ######################################### #
# ##### format cond for client filter ##### #
# ######################################### #
    @classmethod
    def formatDate2Cond(cls, date):
        return forceString(date.toString('yyyy-MM-dd'))

    @classmethod
    def getCondRecordList(cls, tableName, contingentTypeId):
        db = QtGui.qApp.db
        table = db.table(tableName)
        return db.getRecordList(table, '*', table['master_id'].eq(contingentTypeId))

    @classmethod
    def getSASSControlDate(self, controlPeriod):
        currentDate = QDate.currentDate()
        controlEndDate = QDate()
        result = None
        if controlPeriod == 0:
            result = currentDate
        elif controlPeriod == 1:
            result = currentDate.addDays(-currentDate.dayOfYear())
        elif controlPeriod == 2:
            tmpDate = currentDate.addYears(1)
            result = tmpDate.addDays(-tmpDate.dayOfYear())
        elif controlPeriod == 3:
            tmpDate = currentDate.addYears(1)
            controlEndDate = tmpDate.addDays(-tmpDate.dayOfYear())
            result = controlEndDate.addDays(-controlEndDate.dayOfYear()+1)
        return controlEndDate, result

    @classmethod
    def getETMControlDates(cls, controlPeriod, freePeriod):
        controlBegDate = controlEndDate = None
        currentDate = QDate.currentDate()
        if controlPeriod == 0:
            tmpDate = currentDate.addYears(1)
            controlEndDate = tmpDate.addDays(-tmpDate.dayOfYear())
            controlBegDate = controlEndDate.addDays(-controlEndDate.dayOfYear()+1)
        elif controlPeriod == 1:
            controlEndDate = QDate(currentDate.year(), 12, 31)
            controlBegDate = controlEndDate.addDays(-(freePeriod-1))
        elif controlPeriod == 2:
            controlEndDate = QDate(currentDate.year(), 12, 31)
            controlBegDate = controlEndDate.addDays(-(7*freePeriod-1))
        elif controlPeriod == 3:
            controlEndDate = QDate(currentDate.year(), 12, 31)
            controlBegDate = controlEndDate.addMonths(-freePeriod).addDays(-1)
        elif controlPeriod == 4:
            controlEndDate = QDate(currentDate.year(), 12, 31)
            controlBegDate = controlEndDate.addYears(-freePeriod).addDays(-1)
        return controlBegDate, controlEndDate


    # изначально была идея использовать хранимую функцию `isSexAndAgeSuitable`
    # но она дает сильное торможение при наложении на всю таблицу Client
    @classmethod
    def getSexAgeCond(cls, contingentTypeId): # AgeSelectorUnits = u'днмг'
        def calcBirthDate(date, cnt, unit):
            if unit == 1: # дни
                date = date.addDays(-cnt)
            elif unit == 2: # недели
                date = date.addDays(-cnt*7)
            elif unit == 3: # месяцы
                date = date.addMonths(-cnt)
            else: # года
                date = date.addYears(-cnt)
            return date

        def getControlEndDate(date, unit):
            if unit == 1: # дни
                date = date.addDays(-1)
            elif unit == 2: # недели
                date = date.addDays(-7)
            elif unit == 3: # месяцы
                date = date.addMonths(-1)
            else: # года
                date = date.addYears(-1)
            return date

        result = []
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        recordList = cls.getCondRecordList(cls.CTSATName, contingentTypeId)
        if recordList:
            for record in recordList:
                controlPeriod = forceInt(record.value('controlPeriod'))
                sex           = forceInt(record.value('sex'))
                age           = forceString(record.value('age'))
                controlEndDate, controlDate = cls.getSASSControlDate(controlPeriod)
                begUnit, begCount, endUnit, endCount = parseAgeSelector(age)
                cond = []
                if sex:
                    cond.append(tableClient['sex'].eq(sex))
                if controlPeriod == 3:
                    if begCount:
                        cond.append(tableClient['birthDate'].dateLe(calcBirthDate(controlEndDate, begCount, begUnit)))
                    if endCount:
                        cond.append(tableClient['birthDate'].dateGe(calcBirthDate(controlDate, endCount, endUnit)))
                else:
                    controlEndDate = getControlEndDate(controlDate, endUnit)
                    if begCount:
                        cond.append(tableClient['birthDate'].dateLe(calcBirthDate(controlDate, begCount, begUnit)))
                    if endCount:
                        cond.append(tableClient['birthDate'].dateGt(calcBirthDate(controlEndDate, endCount, endUnit)))
                if cond:
                    result.append(db.joinAnd(cond))
        return result

    @classmethod
    def getContingentKindCond(cls, contingentTypeId):
        result = []
        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTCKTName, contingentTypeId)
        tableClientContingentKind = db.table('ClientContingentKind')
        if recordList:
            for record in recordList:
                controlPeriod = forceInt(record.value('controlPeriod'))
                controlEndDate, controlDate = cls.getSASSControlDate(controlPeriod)
                contingentKindId = forceRef(record.value('contingentKind_id'))
                specialityId = forceRef(record.value('speciality_id'))
                cond = [tableClientContingentKind['deleted'].eq(0),
                        tableClientContingentKind['contingentKind_id'].eq(contingentKindId),
                        db.joinOr([tableClientContingentKind['begDate'].dateLe(controlDate),
                                   tableClientContingentKind['begDate'].isNull()]),
                        db.joinOr([tableClientContingentKind['endDate'].dateGe(controlDate),
                                   tableClientContingentKind['endDate'].isNull()])
                        ]
                if specialityId:
                    cond.append(tableClientContingentKind['speciality_id'].eq(specialityId))
                result.append(db.joinAnd(cond))
        return result


    @classmethod
    def getSocStatusCond(cls, contingentTypeId):
        result = []
        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTSSTName, contingentTypeId)
        tableClientSocStatus = db.table('ClientSocStatus')
        if recordList:
            for record in recordList:
                controlPeriod = forceInt(record.value('controlPeriod'))
                controlEndDate, controlDate = cls.getSASSControlDate(controlPeriod)
                socStatusTypeId = forceRef(record.value('socStatusType_id'))
                cond = [tableClientSocStatus['deleted'].eq(0),
                        tableClientSocStatus['socStatusType_id'].eq(socStatusTypeId),
                        db.joinOr([tableClientSocStatus['begDate'].dateLe(controlDate),
                                   tableClientSocStatus['begDate'].isNull()]),
                        db.joinOr([tableClientSocStatus['endDate'].dateGe(controlDate),
                                   tableClientSocStatus['endDate'].isNull()])
                       ]
                result.append(db.joinAnd(cond))
        return result


    @classmethod
    def getEventTypeJoinCond(cls, contingentTypeId):
        result = []
        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTETTName, contingentTypeId)
#        tableClient = db.table('Client')
        if recordList:
            tableEvent  = db.table('Event').alias('ContingentEvent')
            for record in recordList:
                eventTypeId   = forceRef(record.value('eventType_id'))
                controlPeriod = forceInt(record.value('controlPeriod'))
                freePeriod    = forceInt(record.value('freePeriod'))
                controlBegDate, controlEndDate = cls.getETMControlDates(controlPeriod, freePeriod)

                cond = [tableEvent['deleted'].eq(0),
                        tableEvent['eventType_id'].eq(eventTypeId),
                        tableEvent['setDate'].dateLe(controlEndDate)]
                if controlBegDate:
                    cond.append(tableEvent['setDate'].dateGe(controlBegDate))

                result.append(db.joinAnd(cond))
#        else:
#            result.append('0')

        return result



    @classmethod
    def getEventTypeSubQueryJoinCond(cls, contingentTypeId):
        result = []

        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTETTName, contingentTypeId)
        if recordList:
            tableEvent  = db.table('Event').alias('CE')
            for record in recordList:
                eventTypeId   = forceRef(record.value('eventType_id'))
                controlPeriod = forceInt(record.value('controlPeriod'))
                freePeriod    = forceInt(record.value('freePeriod'))
                controlBegDate, controlEndDate = cls.getETMControlDates(controlPeriod, freePeriod)

                cond = [tableEvent['deleted'].eq(0),
                        tableEvent['eventType_id'].eq(eventTypeId),
                        tableEvent['setDate'].dateLe(controlEndDate)]
                if controlBegDate:
                    cond.append(tableEvent['setDate'].dateGe(controlBegDate))

                result.append(db.joinAnd(cond))
#        else:
#            result.append('0')

        return result


    @classmethod
    def getActionTypeJoinCond(cls, contingentTypeId):
        result = []
        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTATTName, contingentTypeId)
#        tableClient = db.table('Client')

        if recordList:
            tableAction  = db.table('Action').alias('ContingentAction')
            for record in recordList:
                actionTypeId   = forceRef(record.value('actionType_id'))
                controlPeriod = forceInt(record.value('controlPeriod'))
                freePeriod    = forceInt(record.value('freePeriod'))
                controlBegDate, controlEndDate = cls.getETMControlDates(controlPeriod, freePeriod)

                cond = [tableAction['deleted'].eq(0),
                        tableAction['actionType_id'].eq(actionTypeId),
                        tableAction['begDate'].dateLe(controlEndDate)]
                if controlBegDate:
                    cond.append(tableAction['begDate'].dateGe(controlBegDate))

                result.append(db.joinAnd(cond))
#        else:
#            result.append('0')

        return result


    @classmethod
    def getActionTypeSubQueryJoinCond(cls, contingentTypeId):
        result = []
        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTATTName, contingentTypeId)
        if recordList:
            tableAction  = db.table('Action').alias('CA')
            for record in recordList:
                actionTypeId   = forceRef(record.value('actionType_id'))
                controlPeriod = forceInt(record.value('controlPeriod'))
                freePeriod    = forceInt(record.value('freePeriod'))
                controlBegDate, controlEndDate = cls.getETMControlDates(controlPeriod, freePeriod)

                cond = [tableAction['deleted'].eq(0),
                        tableAction['actionType_id'].eq(actionTypeId),
                        tableAction['begDate'].dateLe(controlEndDate)]
                if controlBegDate:
                    cond.append(tableAction['begDate'].dateGe(controlBegDate))

                result.append(db.joinAnd(cond))
#        else:
#            result.append('0')

        return result


    @classmethod
    def getEventStatusCond(cls, status):
        result = []

        db = QtGui.qApp.db

        tableEvent  = db.table('Event').alias('ContingentEvent')

        if status == 1:
            result.append(tableEvent['id'].isNull())
        else:
            result.append(tableEvent['id'].isNotNull())
        if status == 2:
            result.append(tableEvent['id'].isNotNull())
            result.append(tableEvent['execDate'].isNull())
        elif status == 3:
            result.append(tableEvent['execDate'].isNotNull())

        return result


    @classmethod
    def getActionStatusCond(cls, status):
        result = []

        db = QtGui.qApp.db

        tableAction  = db.table('Action').alias('ContingentAction')

        if status != 1:
            result.append(tableAction['id'].isNotNull())
        if status == 2:
            result.append(tableAction['endDate'].isNull())
        elif status == 3:
            result.append(tableAction['endDate'].isNotNull())

        return result


    @classmethod
    def getMESJoinCond(cls, contingentTypeId):
        result = []

        db = QtGui.qApp.db

        recordList = cls.getCondRecordList(cls.CTMTName, contingentTypeId)

        tableEvent  = db.table('Event').alias('ContingentEvent')

        if recordList:
            for record in recordList:
                MESId   = forceRef(record.value('MES_id'))
                controlPeriod = forceInt(record.value('controlPeriod'))
                freePeriod    = forceInt(record.value('freePeriod'))
                controlBegDate, controlEndDate = cls.getETMControlDates(controlPeriod, freePeriod)

                cond = [tableEvent['deleted'].eq(0),
                        tableEvent['MES_id'].eq(MESId),
                        tableEvent['setDate'].dateLe(controlEndDate)]

                if controlBegDate:
                    cond.append(tableEvent['setDate'].dateGe(controlBegDate))

                result.append(db.joinAnd(cond))
#        else:
#            result.append('0')

        return result


    @classmethod
    def getHealtGroupJoinCond(cls, contingentTypeId):
        result = []
        db = QtGui.qApp.db
        recordList = cls.getCondRecordList(cls.CTHGTName, contingentTypeId)
        tableEvent      = db.table('Event').alias('ContingentEvent')

        if recordList:
            for record in recordList:
                healtGroupId  = forceRef(record.value('healthGroup_id'))
                controlPeriod = forceInt(record.value('controlPeriod'))
                freePeriod    = forceInt(record.value('freePeriod'))
                controlBegDate, controlEndDate = cls.getETMControlDates(controlPeriod, freePeriod)

                cond = [tableEvent['deleted'].eq(0),
                        tableEvent['setDate'].dateLe(controlEndDate)]
                if controlBegDate:
                    cond.append(tableEvent['setDate'].dateGe(controlBegDate))
                if healtGroupId:
                    cond.append('''EXISTS(SELECT Diagnosis.id
                                FROM Diagnostic INNER JOIN Diagnosis ON Diagnostic.diagnosis_id = Diagnosis.id
                                WHERE Diagnostic.event_id = ContingentEvent.id AND Diagnostic.healthGroup_id = %s
                                AND Diagnostic.diagnosisType_id = (SELECT rbDiagnosisType.id
                                FROM rbDiagnosisType WHERE rbDiagnosisType.code = 1 LIMIT 1)
                                AND Diagnostic.deleted = 0 AND Diagnosis.deleted = 0)'''%(healtGroupId))
                result.append(db.joinAnd(cond))

        return result

