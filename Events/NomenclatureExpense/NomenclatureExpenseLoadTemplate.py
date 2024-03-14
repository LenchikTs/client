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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QVariant

from library.DialogBase         import CDialogBase
from library.Utils              import forceInt, forceRef, forceString, smartDict, trim, toVariant, forceDate
from Events.ActionsSelectorSelectedTable import CCheckedActionsModel
from Events.ActionsSelector     import CActionsModel, CActionTypeGroupsTemplatesModel, CActionTypesSelectionManager
from Events.NomenclatureExpense.QueriesStatements import getNomenclatureActionTypesIds
from Events.Utils               import getEventIncludeTooth
from Stock.Utils                 import getExistsNomenclatureAmount

from Events.NomenclatureExpense.Ui_NomenclatureExpenseLoadTemplate import Ui_LoadTemplateDialog

_TREE_TAB_INDEX = 0
_TEMPLATES_TAB_INDEX = 1

_RECIPE = 1
_DOSES  = 2
_SIGNA  = 3
_ACTIVESUBSTANCE = 4


class CNomenclatureExpenseLoadTemplate(CDialogBase, CActionTypesSelectionManager, Ui_LoadTemplateDialog):
    def __init__(self, parent, eventEditor, eventTypeId=None, _class=None):
        CDialogBase.__init__(self, parent)
        self.eventEditor = eventEditor
        self.existsActionTypesList = []
        self.addModels('ActionTypes', CActionsModel(self))
        self.addModels('SelectedActionTypes', CCheckedSelectedActionTypesModel(self,
                                                                   None,
                                                                   self.modelActionTypes,
                                                                   getEventIncludeTooth(eventTypeId),
                                                                   nomenclatureLS=True))
        self.addModels('Templates', CActionTypeGroupsTemplatesModel(self))
        self.setupUi(self)
        self.setModels(self.tblActionTypes, self.modelActionTypes, self.selectionModelActionTypes)
        self.setModels(self.tblSelectedActionTypes, self.modelSelectedActionTypes, self.selectionModelSelectedActionTypes)
        self.setModels(self.tblTemplates, self.modelTemplates, self.selectionModelTemplates)
        self.tblTemplates.addPopupDelRow()
#        self.tblSelectedActionTypes.addGetExecutionPlan()
#        self.tblSelectedActionTypes.addInsertSameAction()
        self.tblSelectedActionTypes.addSelectAllUrgentAction()
        self.tblSelectedActionTypes.addClearSelectionUrgentAction()
        self.tblSelectedActionTypes.enableColsHide()
        self.tblSelectedActionTypes.enableColsMove()
        self.orgStructureId = None
        self.classFirstUpdate = True
        self.selectedActionTypeIdList = []
        self.contractSum = 0
        self.sumDeposit = 0.0
        self.actionTypeClasses = []
        self.cmbClass.setCurrentIndex((_class + 1) if _class is not None else 0)
        self.actionsCacheByCode = {}
        self.actionsCodeCacheByName = {}
        self._sortActionType = smartDict(order='code, name', isAscending=False, column=0)
        self._sortTemplates = smartDict(order='ActionTypeGroup.code, ActionTypeGroup.name', isAscending=False, column=0)
        self.connect(self.modelSelectedActionTypes, SIGNAL('pricesAndSumsUpdated()'), self.on_pricesAndSumsUpdated)
        self.connect(self.tblActionTypes.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.on_sortActions)
        self.connect(self.tblTemplates.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.on_sortTemplates)
        self.setFocusToWidget(self.edtFindByCode)
        self.modelTemplates.setFilter(self.setActionTypeFilter())


    def setActionTypeNomenclatureIdList(self):
        db = QtGui.qApp.db
        table = db.table('ActionType')
        idList = getNomenclatureActionTypesIds()
        descendants = []
        for id in idList:
            descendants.extend(db.getDescendants(table, 'group_id', id))
        return db.getTheseAndParents(table, 'group_id', descendants)



    def setActionTypeFilter(self):
        idList = self.setActionTypeNomenclatureIdList()
        return u'ActionTypeGroup.id IN (SELECT ActionTypeGroup_Item.master_id FROM ActionTypeGroup_Item WHERE ActionTypeGroup_Item.deleted = 0 AND ActionTypeGroup_Item.actionType_id IN (%s))'%(u','.join(str(id) for id in idList if id))


    @pyqtSignature('int')
    def on_cmbClass_currentIndexChanged(self, index):
        self.actionTypeClasses = [index-1] if index else range(4)
        if not self.classFirstUpdate:
            self.updateTemplates()
        else:
            self.classFirstUpdate = False


    def exec_(self):
        self.updateTemplates()
        return CDialogBase.exec_(self)


    def updateTemplates(self):
        self.modelTemplates.loadData(self.actionTypeClasses[0] if len(self.actionTypeClasses) == 1 else None)
        self._updateActionTypesByTemplate()


    def _updateActionTypesByTemplate(self):
        templateId = self.tblTemplates.currentItemId()
        if not templateId:
            self.tblActionTypes.setIdList([])
            return
        idList = self.setActionTypeNomenclatureIdList()
        if not idList:
            self.tblActionTypes.setIdList([])
            return
        db = QtGui.qApp.db
        table = db.table('ActionTypeGroup_Item')
        idList = db.getDistinctIdList(
            table, 'actionType_id', where=[table['deleted'].eq(0), table['master_id'].eq(templateId), table['actionType_id'].inlist(idList)]
        )
        self.tblActionTypes.setIdList(idList)


    def getActionTypeItemsByTemplate(self, actionTypeId):
        templateId = self.tblTemplates.currentItemId()
        if not templateId:
            self.tblActionTypes.setIdList([])
            return None
        db = QtGui.qApp.db
        table = db.table('ActionTypeGroup_Item')
        return db.getRecordList(table, '*', [table['deleted'].eq(0), table['master_id'].eq(templateId), table['actionType_id'].eq(actionTypeId)], [table['id'].name()])


    def getPlanItemsByTemplate(self, templateItemId):
        db = QtGui.qApp.db
        tablePI = db.table('ActionTypeGroup_Plan_Item')
        tablePIN = db.table('ActionTypeGroup_Plan_Item_Nomenclature')
        queryTable = tablePI.innerJoin(tablePIN, tablePIN['master_id'].eq(tablePI['id']))
        cols = [tablePI['id'].alias('piId'),
                tablePI['master_id'].alias('piMasterId'),
                tablePI['idx'],
                tablePI['date_idx'],
                tablePI['time'],
                tablePIN['id'].alias('pinId'),
                tablePIN['master_id'].alias('pinMasterId'),
                tablePIN['nomenclature_id'],
                tablePIN['dosage'],
                ]
        cond = [tablePI['master_id'].eq(templateItemId)]
        return db.getRecordList(queryTable, cols, cond, [tablePI['idx'].name()])


    @pyqtSignature('const QModelIndex&,const QModelIndex&')
    def on_selectionModelTemplates_currentChanged(self, current, previous):
        isEnabled = False
        self._updateActionTypesByTemplate()
        templateId = self.tblTemplates.currentItemId()
        if templateId:
            db = QtGui.qApp.db
            table = db.table('ActionTypeGroup')
            record = db.getRecordEx(table, [table['createPerson_id']], [table['id'].eq(templateId), table['deleted'].eq(0)])
            createPersonId = forceRef(record.value('createPerson_id')) if record else None
            isEnabled = createPersonId and createPersonId == QtGui.qApp.userId
        self.btnUpdateTemplate.setEnabled(isEnabled)    
                

    def getMESqwt(self, actionTypeId):
        return None


    def getPrice(self, actionTypeId, contractId, financeId):
        return None


    def getClientId(self):
        return self.eventEditor.clientId
        
        
    def getMedicalAidKindId(self):
        return self.eventEditor.eventMedicalAidKindId
        
        
    def getFinanceId(self):
        return self.eventEditor.eventFinanceId
        
        
    def setOrgStructureId(self, value): 
        self.orgStructureId = value
      

    def insertActionIntoCheckedModel(self, actionTypeId, recipe=None, doses=None, signa=None, duration=None, periodicity=None, aliquoticity=None, offset=0, piRecords=None):
        row = self.modelSelectedActionTypes.add(actionTypeId, self.getMESqwt(actionTypeId), recipe=recipe, doses=doses, signa=signa, duration=duration, periodicity=periodicity, aliquoticity=aliquoticity, offset=offset, piRecords=piRecords)
        existQnt = getExistsNomenclatureAmount(recipe, financeId = self.getFinanceId(), medicalAidKindId = self.getMedicalAidKindId(), orgStructureId=self.orgStructureId)
        if existQnt <= 0:
            self.modelSelectedActionTypes.addExistQntRows(row)    


    def updatePresetValuesConditions(self, action):
        apm = action.executionPlanManager
        if not apm.currentItem:
            return
        firstItem = apm.currentItem
        action.updatePresetValuesConditions({
            'courseDate': firstItem.date,
            'courseTime': firstItem.time,
            'firstInCourse': True
        })


    def getSelectedActionList(self):
        result = []
        for actionTypeId in self.selectedActionTypeIdList:
            actions = self.modelSelectedActionTypes.getSelectedAction(actionTypeId)
            for action in actions:
                self.updatePresetValuesConditions(action)
                action.initPresetValues()
                if not action.deleteMark:
                    result.append(action)
        return result


    def getSelectedList(self):
        return self.getSelectedActionList()


    def setSelected(self, actionTypeId, value, resetMainModel=False):
        present = self.isSelected(actionTypeId)
        if value:
            if not present:
                self.selectedActionTypeIdList.append(actionTypeId)
                records = self.getActionTypeItemsByTemplate(actionTypeId)
                for record in records:
                    recipe = forceRef(record.value('nomenclature_id'))
                    doses = forceString(record.value('doses'))
                    signa = forceString(record.value('signa'))
                    duration = forceInt(record.value('duration'))
                    periodicity = forceInt(record.value('periodicity'))
                    aliquoticity = forceInt(record.value('aliquoticity'))
                    offset = forceInt(record.value('offset'))
                    templateItemId = forceRef(record.value('id'))
                    piRecords = self.getPlanItemsByTemplate(templateItemId) if templateItemId else None
                    self.insertActionIntoCheckedModel(actionTypeId, recipe, doses, signa, duration, periodicity, aliquoticity, offset=offset, piRecords=piRecords)
                self.updateSelectedCount()
                if resetMainModel:
                    self.modelActionTypes.emitDataChanged()
                return True
        else:
            if present:
                self.selectedActionTypeIdList.remove(actionTypeId)
                self.modelSelectedActionTypes.remove(actionTypeId)
                self.updateSelectedCount()
                if resetMainModel:
                    self.modelActionTypes.emitDataChanged()
                return True
        return False


    def on_pricesAndSumsUpdated(self):
        sum = self.modelSelectedActionTypes.getTotalSum()
        text = u'Назначить: %.2f' % sum if sum else u'Назначить'
        self.lblSelectedActionTypes.setText(text)
        payDeposit = 0.0
        if self.contractSum:
            self.sumDeposit = self.getSumDepositForContract()
            payDeposit = self.contractSum - (self.sumDeposit + sum)
            self.lblDeposit.setText(u'Остаток по депозиту = %s  '%forceString(payDeposit))
        if payDeposit < 0 and self.contractSum:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
            self.lblDeposit.setPalette(palette)
        elif self.contractSum:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
            self.lblDeposit.setPalette(palette)


    def on_sortActions(self, logicalIndex):
        header = self.tblActionTypes.horizontalHeader()
        if logicalIndex:
            self._sortActionType.order = 'code %s, name' if logicalIndex == 1 else 'name %s, code'
            if self._sortActionType.column == logicalIndex:
                self._sortActionType.isAscending = not self._sortActionType.isAscending
            else:
                self._sortActionType.column = logicalIndex
                self._sortActionType.isAscending = True
            header.setSortIndicatorShown(True)
            header.setSortIndicator(self._sortActionType.column, Qt.AscendingOrder if self._sortActionType.isAscending else Qt.DescendingOrder)
            if self._sortActionType.isAscending:
                self._sortActionType.order = self._sortActionType.order % 'ASC'
            else:
                self._sortActionType.order = self._sortActionType.order % 'DESC'
        else:
            if self._sortActionType.column != logicalIndex:
                header.setSortIndicatorShown(False)
                self._sortActionType.order = 'code, name'
                self._sortActionType.column = 0


    def on_sortTemplates(self, logicalIndex):
        header = self.tblTemplates.horizontalHeader()
        self._sortTemplates.order = 'ActionTypeGroup.name %s' if logicalIndex else 'ActionTypeGroup.code %s'
        if self._sortTemplates.column == logicalIndex:
            self._sortTemplates.isAscending = not self._sortTemplates.isAscending
        else:
            self._sortTemplates.column = logicalIndex
            self._sortTemplates.isAscending = True
        header.setSortIndicatorShown(True)
        header.setSortIndicator(self._sortTemplates.column, Qt.AscendingOrder if self._sortTemplates.isAscending else Qt.DescendingOrder)
        if self._sortTemplates.isAscending:
            self._sortTemplates.order = self._sortTemplates.order % 'ASC'
        else:
            self._sortTemplates.order = self._sortTemplates.order % 'DESC'
        self.modelTemplates.setTemplatesOrder(self._sortTemplates.order)


    def _updateActionTypesByTree(self, current):
        if current.isValid() and current.internalPointer():
            actionTypeId = current.internalPointer().id()
            _class = current.internalPointer().class_()
        else:
            actionTypeId = None
            _class = None
        self.setGroupId(actionTypeId, _class)
        text = trim(self.edtFindByCode.text())
        if text:
            self.on_edtFindByCode_textChanged(text)


    @pyqtSignature('QString')
    def on_edtFindByCode_textChanged(self, text):
        if text:
            row = self.findByCode(text)
            if row is not None:
                self.tblActionTypes.setCurrentRow(row)
            else:
                self.tblActionTypes.setCurrentRow(0)
        else:
            self.tblActionTypes.setCurrentRow(0)


    @pyqtSignature('const QModelIndex&,const QModelIndex&')
    def on_selectionModelActionTypeGroups_currentChanged(self, current, previous):
        self._updateActionTypesByTree(current)


    def setGroupId(self, groupId, _class=None):
        if not self.actionTypeClasses:
            return
        self.actionsCacheByCode.clear()
        self.actionsCodeCacheByName.clear()
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        cond = [tableActionType['deleted'].eq(0),
                tableActionType['showInForm'].ne(0),
                tableActionType['class'].inlist(self.actionTypeClasses)
               ]
        if groupId:
            groupIdList = db.getDescendants('ActionType', 'group_id', groupId)
            cond.append(tableActionType['group_id'].inlist(groupIdList))
        if _class is not None:
            cond.append(tableActionType['class'].eq(_class))
        cond.append('NOT EXISTS(SELECT id FROM ActionType AS at WHERE at.group_id = ActionType.id)')
        recordList = QtGui.qApp.db.getRecordListGroupBy(tableActionType, 'id, code, name', cond, 'code',  self._sortActionType.order)
        if recordList:
            idList = []
            for index, record in enumerate(recordList):
                id = forceRef(record.value('id'))
                code = forceString(record.value('code')).upper()
                name = forceString(record.value('name')).upper()
                idList.append(id)
                existCode = self.actionsCacheByCode.get(code, None)
                if existCode is None:
                    self.actionsCacheByCode[code] = index
                existName = self.actionsCodeCacheByName.get(name, None)
                if existName is None:
                    self.actionsCodeCacheByName[name] = code
        else:
            idList = []
        self.tblActionTypes.setIdList(idList)
        
        
    @pyqtSignature('')
    def on_btnUpdateTemplate_pressed(self):
        templateId = self.tblTemplates.currentItemId()
        if not templateId:
            return 
        class_ = self.actionTypeClasses[0] if len(self.actionTypeClasses) == 1 else None
        db = QtGui.qApp.db
        db.transaction()
        try:
            table = db.table('ActionTypeGroup_Item')
            items = self.tblSelectedActionTypes.model().items()
            mapActionTypeIdToPropertyValues = self.tblSelectedActionTypes.model()._mapActionTypeIdToPropertyValues
            idRowToAction = self.tblSelectedActionTypes.model()._idRowToAction
            recordTemplates = self.tblTemplates.model().getRecordById(templateId)
            isOffset = forceInt(recordTemplates.value('isOffset')) if recordTemplates else 0
            groupsList = self.tblSelectedActionTypes.model()._rowToAction.values()
            groupsList.sort(key=lambda x: forceDate(x.getRecord().value('begDate')))
            offsetDate = forceDate(groupsList[0].getRecord().value('begDate')) if len(groupsList) > 0 else None            
            rows = []
            db.deleteRecord(table, [table['master_id'].eq(templateId), table['deleted'].eq(0)])            
            for actionTypeId in self.selectedActionTypeIdList:
                for row, item in enumerate(items):
                    if row not in rows and actionTypeId == forceRef(item.value('actionType_id')):
                        newRecord = table.newRecord()
                        newRecord.setValue('master_id', templateId)
                        newRecord.setValue('actionType_id', actionTypeId)
                        fieldNameRecipe = item.fieldName(item.indexOf('recipe'))
                        fieldNameDoses = item.fieldName(item.indexOf('doses'))
                        fieldNameSigna = item.fieldName(item.indexOf('signa'))
                        fieldNameActiveSubstance = item.fieldName(item.indexOf('activeSubstance_id'))
                        action = idRowToAction[(actionTypeId, row)]
                        if action:
                            record = action.getRecord()
                            if record:
                                begDate = forceDate(record.value('begDate'))
                                values = mapActionTypeIdToPropertyValues.get(actionTypeId, None)
                                if values:
                                    if fieldNameRecipe == 'recipe' and forceString(fieldNameRecipe) in values.keys():
                                        value = values[forceString(fieldNameRecipe)]
                                        if u'propertyType' in value.keys():
                                            propertyType = value['propertyType']
                                            if propertyType.inActionsSelectionTable == _RECIPE:
                                                property = action.getPropertyById(propertyType.id)
                                                newRecord.setValue('nomenclature_id', toVariant(property.getValue()))
                                    if fieldNameDoses == 'doses' and forceString(fieldNameDoses) in values.keys():
                                        value = values[forceString(fieldNameDoses)]
                                        if u'propertyType' in value.keys():
                                            propertyType = value['propertyType']
                                            if propertyType.inActionsSelectionTable == _DOSES:
                                                property = action.getPropertyById(propertyType.id)
                                                newRecord.setValue('doses', toVariant(property.getText()))
                                    if fieldNameSigna == 'signa' and forceString(fieldNameSigna) in values.keys():
                                        value = values[forceString(fieldNameSigna)]
                                        if u'propertyType' in value.keys():
                                            propertyType = value['propertyType']
                                            if propertyType.inActionsSelectionTable == _SIGNA:
                                                property = action.getPropertyById(propertyType.id)
                                                newRecord.setValue('signa', toVariant(property.getValue()))
                                    if fieldNameActiveSubstance == 'activeSubstance_id' and forceString(fieldNameActiveSubstance) in values.keys():
                                        value = values[forceString(fieldNameActiveSubstance)]
                                        if u'propertyType' in value.keys():
                                            propertyType = value['propertyType']
                                            if propertyType.inActionsSelectionTable == _ACTIVESUBSTANCE:
                                                property = action.getPropertyById(propertyType.id)
                                                newRecord.setValue('activeSubstance_id', toVariant(property.getValue()))
                                newRecord.setValue('duration', toVariant(action.getDuration()))
                                newRecord.setValue('periodicity', toVariant(action.getPeriodicity()))
                                newRecord.setValue('aliquoticity', toVariant(action.getAliquoticity()))                            
                                offset = offsetDate.daysTo(begDate) if (isOffset and offsetDate) else 0
                                newRecord.setValue('offset', toVariant(offset))                                        
                                actionTypeGroupItemId = db.insertRecord(table, newRecord)
                                rows.append(row)
                                if actionTypeGroupItemId:
                                    items = action.getExecutionPlan().items
                                    if items:
                                        tablePI = db.table('ActionTypeGroup_Plan_Item')
                                        tablePINomenclature = db.table('ActionTypeGroup_Plan_Item_Nomenclature')
                                        for item in items:
                                            idx = item.idx
                                            time = item.time
                                            date = item.date
                                            dateIdx = (begDate.daysTo(item.date) + 1) if begDate != date else 1
                                            newRecordPI = tablePI.newRecord()
                                            newRecordPI.setValue('master_id', toVariant(actionTypeGroupItemId))
                                            newRecordPI.setValue('idx', toVariant(idx))
                                            newRecordPI.setValue('date_idx', toVariant(dateIdx))
                                            newRecordPI.setValue('time', toVariant(time))
                                            planItemId = db.insertRecord(tablePI, newRecordPI)
                                            if planItemId and item.nomenclature:
                                                doses = item.nomenclature.dosage
                                                nomenclatureId = item.nomenclature.nomenclatureId
                                                newRecordPIN = tablePINomenclature.newRecord()
                                                newRecordPIN.setValue('master_id', toVariant(planItemId))
                                                newRecordPIN.setValue('nomenclature_id', toVariant(nomenclatureId))
                                                newRecordPIN.setValue('dosage', toVariant(doses))
                                                db.insertRecord(tablePINomenclature, newRecordPIN)
            self.modelTemplates.reloadData(class_)
            self.tblTemplates.setCurrentItemId(templateId)
        except:
            db.rollback()
            raise
        else:
            db.commit()


    @pyqtSignature('')
    def on_btnFindTemplates_clicked(self):
        self.modelTemplates.setFindFilterText(unicode(self.edtFindTemplates.text()))
        self.modelTemplates.loadData(self.actionTypeClasses[0] if len(self.actionTypeClasses) == 1 else None)
        self._updateActionTypesByTemplate()
        
        
class CCheckedSelectedActionTypesModel(CCheckedActionsModel):
    def __init__(self, parent, existsActionsModel, actionTypesModel=None, includeTooth=False, nomenclatureLS=False):
        CCheckedActionsModel.__init__(self, parent, existsActionsModel, actionTypesModel, includeTooth, nomenclatureLS)
        self.existQntRows = []
        
        
    def addExistQntRows(self, row):
        if row >= 0 and row not in self.existQntRows:
            self.existQntRows.append(row) 
         
      
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.FontRole:
            row = index.row()
            record = self._items[row]
            actionTypeId = forceRef(record.value('actionType_id'))
            if row >= 0 and row in self.existQntRows:
                    result = QtGui.QFont()
                    result.setWeight(QtGui.QFont.DemiBold)
                    return QVariant(result)
            elif self._existsActionsModel and self._existsActionsModel.hasActionTypeId(actionTypeId):
                return self._qBoldFont                    
        return CCheckedActionsModel.data(self, index, role)
  
