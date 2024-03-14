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

from PyQt4            import QtGui
from PyQt4.QtCore     import Qt, pyqtSignature, SIGNAL

from Events.ActionProperty import CActionPropertyValueTypeRegistry
from Events.Action         import CAction

from library.AmountToWords import amountToWords
from library.Utils import forceInt, forceDouble, forceRef, forceString, forceStringEx, trim

from Ui_CorrectWidget import Ui_Form

class CCorrectWidget(QtGui.QWidget, Ui_Form):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self._cachePropertyTypes = {}
        self._cahceActionTypeIdToPropertyName = {}

        self._logWait      = False
        self._actionIdList = []
        self._actionList   = []
        self._propertyTypeIdListToDeliting = []
        self._propertyIdListToDeliting     = []

        self.connect(self.btnDataAnalysis, SIGNAL('clicked()'), self.on_btnDataAnalysis)
        self.connect(self.btnStart, SIGNAL('clicked()'), self.on_btnStart)
        self.connect(self.btnReset, SIGNAL('clicked()'), self.reset)

        self.setupTypeNameComboboxes()
        self._isStart = False
        self._progressBar.hide()
        self._isInProgress = False
        self._notReseted = False


    def startProgress(self, maxValue):
        self.resetProgress()
        self._progressBar.setMaximum(maxValue)
        self._progressBar.show()


    def stepProgress(self):
        self._progressBar.step()


    def resetProgress(self):
        self._progressBar.reset()
        self._progressBar.setValue(0)


    def stopProgress(self):
        self._progressBar.hide()
        self.resetProgress()

    def reset(self):
        if self._isInProgress:
            self.setBtnReset()
            self._notReseted = True
        else:
            self.edtLog.clear()
            self.clear()


    def clear(self):
        self._logWait      = False
        self._actionIdList = []
        self._actionList   = []
        self._propertyTypeIdListToDeliting = []
        self._propertyIdListToDeliting     = []
        self._isStart = False

        self.btnDataAnalysis.setEnabled(True)
        self.cmbSourceTypeName.setEnabled(True)
        self.cmbTargetTypeName.setEnabled(True)
        self.lblSourceTypeName.setEnabled(True)
        self.lblTargetTypeName.setEnabled(True)
        self.chkPropertyName.setEnabled(True)
        self.lblTargetPropertyName.setEnabled(True)
        self.edtSourcePropertyName.setEnabled(self.chkPropertyName.isChecked())
        self.edtTargetPropertyName.setEnabled(self.chkPropertyName.isChecked())
        self.chkDeleteSource.setEnabled(True)
        self.chkDeletingAutoStart.setEnabled(self.chkDeleteSource.isChecked())
        self.chkActionType.setEnabled(True)
        self.cmbActionType.setEnabled(self.chkActionType.isChecked())
        self.chkFullReport.setEnabled(True)

        self.btnStart.setText(u'Старт')
        self.btnStart.setEnabled(False)
        self._notReseted = False


    def setupTypeNameComboboxes(self):
        for name in CActionPropertyValueTypeRegistry.nameList:
            self.cmbSourceTypeName.addItem(name)
            self.cmbTargetTypeName.addItem(name)


    def addLogMessage(self, msg, wait=False):
        if self._logWait:
            self.edtLog.insertPlainText(msg)
        else:
            self.edtLog.append(msg)
        self._logWait = wait


    def availableDataAnalys(self):
        self.addLogMessage(u'Анализ данных: ', wait=True)
        db = QtGui.qApp.db
        tableAction                   = db.table('Action')
        tableActionType               = db.table('ActionType')
        tableActionPropertyTypeSource = db.table('ActionPropertyType').alias('ActionPropertyTypeSource')
        tableActionPropertyTypeTarget = db.table('ActionPropertyType').alias('ActionPropertyTypeTarget')
#        tableActionProperty           = db.table('ActionProperty')

        queryTable = tableActionType.innerJoin(tableActionPropertyTypeSource,
                                               tableActionPropertyTypeSource['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableActionPropertyTypeTarget,
                                               tableActionPropertyTypeTarget['actionType_id'].eq(tableActionType['id']))

        chkActionType = self.chkActionType.isChecked()
        actionTypeId = self.cmbActionType.value()
        chkPropertyTypeName = self.chkPropertyName.isChecked()
        sourcePropertyTypeName = forceStringEx(self.edtSourcePropertyName.text())
        targetPropertyTypeName = forceStringEx(self.edtTargetPropertyName.text())
        sourceType = forceString(self.cmbSourceTypeName.currentText())
        targetType = forceString(self.cmbTargetTypeName.currentText())

        cond = [
                tableActionType['deleted'].eq(0),
                tableActionPropertyTypeSource['typeName'].eq(sourceType),
                tableActionPropertyTypeTarget['typeName'].eq(targetType),
                tableActionPropertyTypeSource['deleted'].eq(0),
                tableActionPropertyTypeTarget['deleted'].eq(0)
               ]

        if chkActionType:
            cond.append(tableActionType['id'].eq(actionTypeId))

        if chkPropertyTypeName:
            cond.append(tableActionPropertyTypeSource['name'].eq(sourcePropertyTypeName))
            cond.append(tableActionPropertyTypeTarget['name'].eq(targetPropertyTypeName))
        else:
            cond.append(tableActionPropertyTypeSource['name'].eq(tableActionPropertyTypeTarget['name']))

        actionTypeIdList   = db.getIdList(queryTable, tableActionType['id'].name(), cond)

        cond = [tableAction['actionType_id'].inlist(actionTypeIdList),
                tableAction['deleted'].eq(0)]
        self._actionIdList = db.getIdList(tableAction, 'id', cond)

        return bool(self._actionIdList)


    def disabledByAnalys(self):
        self.btnDataAnalysis.setEnabled(False)
        self.cmbSourceTypeName.setEnabled(False)
        self.cmbTargetTypeName.setEnabled(False)
        self.lblSourceTypeName.setEnabled(False)
        self.lblTargetTypeName.setEnabled(False)
        self.chkPropertyName.setEnabled(False)
        self.lblTargetPropertyName.setEnabled(False)
        self.edtSourcePropertyName.setEnabled(False)
        self.edtTargetPropertyName.setEnabled(False)
        self.chkDeleteSource.setEnabled(False)
        self.chkDeletingAutoStart.setEnabled(False)
        self.chkActionType.setEnabled(False)
        self.cmbActionType.setEnabled(False)
        self.chkFullReport.setEnabled(False)


    def checkConditions(self):
        sourceType = forceString(self.cmbSourceTypeName.currentText())
        targetType = forceString(self.cmbTargetTypeName.currentText())
        if sourceType == targetType:
            QtGui.QMessageBox.information(self, u'Внимание!', u'Требуются разные типы свойств')
            return False
        return True


    def on_btnDataAnalysis(self):
        if not self.checkConditions():
            return
        QtGui.qApp.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        self._cachePropertyTypes.clear()
        self._cahceActionTypeIdToPropertyName.clear()
        self.disabledByAnalys()
        result = self.availableDataAnalys()
        self.addLogMessage(u'Найдено %s'%amountToWords(len(self._actionIdList),
                           ((u'действие', u'действия', u'действий', 'n'), None)))
        if result:
            self.btnStart.setEnabled(True)
        else:
            self.clear()
        QtGui.qApp.restoreOverrideCursor()
        if len(self._actionIdList)==0:
            QtGui.QMessageBox.warning( self,
                               u'Внимание!',
                               u'Для изменения типа данных необходима предварительная настройка Типа Действия. \
Проверьте, добавлено ли итоговое свойство в изменяемый Тип Действия (Справочники-Учёт-Типы Действий) \
с указанным в поле "Итоговое свойство" наименованием и соответствующим типом данных.',
                               QtGui.QMessageBox.Ok)


    def setBtnStop(self):
        self.btnReset.setText(u'Остановить')
        self._isInProgress = True


    def setBtnReset(self):
        self.btnReset.setText(u'Очистить')
        self._isInProgress = False


    def start(self):
        self._isStart = True

        self.btnStart.setEnabled(False)

        QtGui.qApp.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))

        chkPropertyTypeName = self.chkPropertyName.isChecked()
#        sourcePropertyTypeName = forceStringEx(self.edtSourcePropertyName.text())
#        targetPropertyTypeName = forceStringEx(self.edtTargetPropertyName.text())

        self.addLogMessage(u'Обработка действий...')

        self.startProgress(len(self._actionIdList))

        self.setBtnStop()

        self._propertyTypeIdListToDeliting = []
        self._propertyIdListToDeliting     = []

        if chkPropertyTypeName:
            self._startEasyWay()
        else:
            self._startHardWay()

        self.btnStart.setText(u'Удалить свойства')
        self.btnStart.setEnabled(True)

        self.stopProgress()

        self.addLogMessage(u'Обработка действий окончена!')

        self.setBtnReset()

        QtGui.qApp.restoreOverrideCursor()

        if self.chkDeletingAutoStart.isChecked() and not self._notReseted:
            self.btnStart.emit(SIGNAL('clicked()'))


    def on_btnStart(self):
        if self._isStart:
            self.setBtnStop()
            self.saveResults()
            self.setBtnReset()
        else:
            self.start()
            if not self.chkDeleteSource.isChecked() or not self._propertyTypeIdListToDeliting:
                if not self._propertyTypeIdListToDeliting:
                    self.addLogMessage(u'\nНет свойств на удаление!')
                self.clear()


    def transformValue(self, key, value):
        return transform(key, value)


    def _startEasyWay(self):
#        db = QtGui.qApp.db

        sourcePropertyTypeName = forceStringEx(self.edtSourcePropertyName.text())
        targetPropertyTypeName = forceStringEx(self.edtTargetPropertyName.text())
        sourceType = forceString(self.cmbSourceTypeName.currentText())
        targetType = forceString(self.cmbTargetTypeName.currentText())

        fullReport = self.chkFullReport.isChecked()

        if sourcePropertyTypeName != targetPropertyTypeName:
            for actionId in self._actionIdList:
                QtGui.qApp.processEvents()

                if not self._isInProgress:
                    break

                self.stepProgress()

                sourcePropertyType = None
                sourceProperty     = None
                targetPropertyType = None
                targetProperty     = None
                action = CAction.getActionById(actionId)
                action._locked = False
#                self._actionList.append(action)
                actionType = action.getType()

                if fullReport:
                    msg = u'Действие \'%s\', id %d' % (actionType.name, actionId)
                    self.addLogMessage(msg)

                sourcePropertyType = actionType.getPropertyType(sourcePropertyTypeName)
                sourceProperty     = action.getPropertyById(sourcePropertyType.id)

                targetPropertyType = actionType.getPropertyType(targetPropertyTypeName)
                targetProperty     = action.getPropertyById(targetPropertyType.id)

                transformKey = (sourceType, targetType)
                value = self.transformValue(transformKey, sourceProperty.getValue())
                targetProperty.setValue(value)

                self._propertyTypeIdListToDeliting.append(sourcePropertyType.id)
                propertyTypeId = forceRef(sourceProperty.getRecord().value('id')) if sourceProperty.getRecord() else None
                if propertyTypeId:
                    self._propertyIdListToDeliting.append(propertyTypeId)
                action.save(idx=forceInt(action.getRecord().value('idx')))
        else:
            for actionId in self._actionIdList:
                QtGui.qApp.processEvents()

                if not self._isInProgress:
                    break

                self.stepProgress()

                sourcePropertyType = None
                sourceProperty     = None
                targetPropertyType = None
                targetProperty     = None
                action = CAction.getActionById(actionId)
                action._locked = False
#                self._actionList.append(action)
                actionType = action.getType()

                if fullReport:
                    msg = u'Действие \'%s\', id %d' % (actionType.name, actionId)
                    self.addLogMessage(msg, wait=True)

                result = self._cachePropertyTypes.get(actionType.id, None)
                if result:
                    sourcePropertyType, targetPropertyType = result
                else:
                    propertyTypeList = actionType.getPropertiesById().values()
                    for propertyType in propertyTypeList:
                        if propertyType.name in (sourcePropertyTypeName, targetPropertyTypeName):
                            if not sourcePropertyType and propertyType.typeName == sourceType:
                                sourcePropertyType = propertyType
                            if not targetPropertyType and propertyType.typeName == targetType:
                                targetPropertyType = propertyType
                    self._cachePropertyTypes[actionType.id] = (sourcePropertyType, targetPropertyType)

                sourceProperty = action.getPropertyById(sourcePropertyType.id) if sourcePropertyType else None
                targetProperty = action.getPropertyById(targetPropertyType.id) if targetPropertyType else None

                if sourcePropertyType is None or sourcePropertyType is None:
                    if fullReport:
                        self.addLogMessage(u'Отсутствуют подходящие свойства')
                    continue
                if fullReport:
                    self.addLogMessage(u'Свойство \'%s\''%sourcePropertyTypeName)

                transformKey = (sourceType, targetType)
                value = self.transformValue(transformKey, sourceProperty.getValue())
                targetProperty.setValue(value)

                self._propertyTypeIdListToDeliting.append(sourcePropertyType.id)
                propertyTypeId = forceRef(sourceProperty.getRecord().value('id')) if sourceProperty.getRecord() else None
                if propertyTypeId:
                    self._propertyIdListToDeliting.append(propertyTypeId)
                action.save(idx=forceInt(action.getRecord().value('idx')))


    def saveResults(self):
        QtGui.qApp.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))

        db = QtGui.qApp.db

#        self.addLogMessage(u'Сохранение данных...')
#
#        self.startProgress(len(self._actionList))
#
#        for action in self._actionList:
#            if not self._isInProgress:
#                break
#            action.save(idx=forceInt(action.getRecord().value('idx')))
#            self.stepProgress()
#
#        self.stopProgress()

        tableActionPropertyType = db.table('ActionPropertyType')
        tableActionProperty     = db.table('ActionProperty')

        if self.chkDeleteSource.isChecked() and self._isInProgress:
            self.addLogMessage(u'Удаление свойств...')
            self.startProgress(len(self._propertyIdListToDeliting))

            for propertyId in self._propertyIdListToDeliting:
                if not self._isInProgress:
                    break
                QtGui.qApp.processEvents()
                db.deleteRecord(tableActionProperty, tableActionProperty['id'].eq(propertyId))
                self.stepProgress()

            self.stopProgress()

            self.addLogMessage(u'Удаление типов свойств...')
            self.startProgress(len(self._propertyTypeIdListToDeliting))

            for propertyTypeId in self._propertyTypeIdListToDeliting:
                if not self._isInProgress:
                    break
                QtGui.qApp.processEvents()
                db.deleteRecord(tableActionPropertyType, tableActionPropertyType['id'].eq(propertyTypeId))
                self.stepProgress()

            self.stopProgress()
        QtGui.qApp.restoreOverrideCursor()
        self.clear()
        self.addLogMessage(u'Сессия закончена')


    def _startHardWay(self):
        def getName(actionTypeId, propertyTypeList, sourceType, targetType):
            name = self._cahceActionTypeIdToPropertyName.get(actionTypeId, None)
            if name is None:
                sourceTypeNameList = []
                targetTypeNameList = []
                for propertyType in propertyTypeList:
                    if propertyType.typeName == sourceType:
                        sourceTypeNameList.append(propertyType.name)
                    if propertyType.typeName == targetType:
                        targetTypeNameList.append(propertyType.name)
                result = list(set(sourceTypeNameList) & set(targetTypeNameList))
                name = result[0] if result else ''
                self._cahceActionTypeIdToPropertyName[actionTypeId] = name
            return name

#        db = QtGui.qApp.db
        sourceType = forceString(self.cmbSourceTypeName.currentText())
        targetType = forceString(self.cmbTargetTypeName.currentText())
        fullReport = self.chkFullReport.isChecked()
        for actionId in self._actionIdList:
            QtGui.qApp.processEvents()
            if not self._isInProgress:
                break

            self.stepProgress()
            sourcePropertyType = None
            sourceProperty     = None
            targetPropertyType = None
            targetProperty     = None
            action = CAction.getActionById(actionId)
            action._locked = False
#            self._actionList.append(action)
            actionType = action.getType()

            if fullReport:
                msg = u'Действие \'%s\', id %d ---- ' % (actionType.name, actionId)
                self.addLogMessage(msg, wait=True)

            propertyTypeList = actionType.getPropertiesById().values()
            propertyTypeName = getName(actionType.id, propertyTypeList, sourceType, targetType)

            if not propertyTypeName:
                if fullReport:
                    self.addLogMessage(u'Отсутствуют подходящие свойства')
                continue
            if fullReport:
                self.addLogMessage(u'Свойство \'%s\''%propertyTypeName)

            result = self._cachePropertyTypes.get(actionType.id, None)
            if result:
                sourcePropertyType, targetPropertyType = result
            else:
                for propertyType in propertyTypeList:
                    if propertyType.name == propertyTypeName:
                        if not sourcePropertyType and propertyType.typeName == sourceType:
                            sourcePropertyType = propertyType

                        if not targetPropertyType and propertyType.typeName == targetType:
                            targetPropertyType = propertyType

                self._cachePropertyTypes[actionType.id] = (sourcePropertyType, targetPropertyType)

            sourceProperty = action.getPropertyById(sourcePropertyType.id) if sourcePropertyType else None
            targetProperty = action.getPropertyById(targetPropertyType.id) if targetPropertyType else None

            transformKey = (sourceType, targetType)
            value = self.transformValue(transformKey, sourceProperty.getValue())
            targetProperty.setValue(value)

            self._propertyTypeIdListToDeliting.append(sourcePropertyType.id)
            propertyTypeId = forceRef(sourceProperty.getRecord().value('id')) if sourceProperty.getRecord() else None
            if propertyTypeId:
                self._propertyIdListToDeliting.append(propertyTypeId)
            action.save(idx=forceInt(action.getRecord().value('idx')))


    @pyqtSignature('QString')
    def on_edtSourcePropertyName_textEdited(self, value):
        self.edtTargetPropertyName.setText(value)


# ################################################################


def transform(key, val):
    return TRANSFORMATION_MAP.get(key, nullTransormation)(val)


def nullTransormation(val):
    return val

# переделайте на регулярные выражения!
def str2int(val):
    if val:
        res = ''
        start = False
        for c in trim(val):
            if not start and c.isdigit():
                start = True
            if start:
                if c.isdigit():
                    res += c
                else:
                    break
        return forceInt(res) if res else None
    return None


# переделайте на регулярные выражения!
def str2double(val):
    if val:
        res = ''
        start = False
        for c in trim(val).replace(',', '.'):
            if not start and c.isdigit():
                start = True
            if start:
                if c.isdigit() or c == '.':
                    res += c
                else:
                    break

        return forceDouble(checkPoints(res)) if res else None
    return None


def checkPoints(val):
    return '.'.join(val.split('.')[-2:])

TRANSFORMATION_MAP = {
                      ('String', 'Int')             : str2int,
                      ('String', 'Double')          : str2double,
                      ('Int', 'String')             : forceString,
                      ('Double', 'String')          : forceString,
                      ('String', u'Доза облучения') : str2double,
                      (u'Доза облучения', 'String') : forceString
                     }
