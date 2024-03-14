# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2018-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature

from Events.ActionTypeComboBoxEx import CActionTypeFindInDocTableCol

from library.interchange     import ( getCheckBoxValue,
                                      getLineEditValue,
                                      getRadioButtonValue,
                                      setCheckBoxValue,
                                      setLineEditValue,
                                      setRadioButtonValue,
                                      setRBComboBoxValue,
                                    )
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol
from library.InDocTable      import ( CInDocTableModel,
                                      CInDocTableCol,
                                      CEnumInDocTableCol,
                                      CRBInDocTableCol,
                                    )
from library.crbcombobox     import CRBComboBox
from library.Utils           import forceInt

from RefBooks.Service.RBServiceComboBox import CRBServiceInDocTableCol


from .Ui_ExtraDataDefEditor import Ui_ItemEditorDialog


class CExtraDataDefList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Наименование', ['name'], 40),
            ], 'ExtraDataDef', ['name'])
        self.setWindowTitleEx(u'Шаблоны дополнительных данных обмена N3.УО')
        self.tblItems.createPopupMenu([self.actDuplicate, '-', self.actDelete])


    def preSetupUi(self):
        CItemsListDialog.preSetupUi(self)
        self.addObject('actDuplicate', QtGui.QAction(u'Дублировать', self))
        self.addObject('actDelete',    QtGui.QAction(u'Удалить', self))


    def copyInternals(self, newItemId, oldItemId):
        for tableName in ( 'ExtraDataDef_Download',
                           'ExtraDataDef_Element',
                           'ExtraDataDef_UploadActionType',
                           'ExtraDataDef_UploadCase',
                         ):
            self.copyDependedTableData(tableName,
                                       'master_id',
                                       newItemId,
                                       oldItemId
                                      )


    def getItemEditor(self):
        return CExtraDataDefEditor(self)


    @pyqtSignature('')
    def on_tblItems_popupMenuAboutToShow(self):
        currentItemId = self.currentItemId()
        self.actDuplicate.setEnabled(bool(currentItemId))
        self.actDelete.setEnabled(bool(currentItemId))


    @pyqtSignature('')
    def on_actDuplicate_triggered(self):
        self.duplicateCurrentRow()


    @pyqtSignature('')
    def on_actDelete_triggered(self):
        def deleteCurrentInternal():
            currentItemId = self.currentItemId()
            if currentItemId:
                row = self.tblItems.currentIndex().row()
                db = QtGui.qApp.db
                table = db.table('ExtraDataDef')
                db.deleteRecord(table, table['id'].eq(currentItemId))
                self.renewListAndSetTo()
                self.tblItems.setCurrentRow(row)
        QtGui.qApp.call(self, deleteCurrentInternal)


#
# ##########################################################################
#

class CExtraDataDefEditor(Ui_ItemEditorDialog, CItemEditorBaseDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'ExtraDataDef')
        self.addModels('UploadCases',       CUploadCasesModel(self))
        self.addModels('UploadActionTypes', CUploadActionTypesModel(self))
        self.addModels('Elements',          CElementsModel(self))
        self.addModels('DownloadElements',  CDownloadElementsModel(self))
        # Дизайнер позволяет добавить непустую группу, но не позволяет задать id кнопок :(
        # Так что проще самому создавать группу и наполнять её кнопками
        # Чем создавать группу в дизайнере и потом париться с назначением id-шек
        self.addObject('rbgSourceType', QtGui.QButtonGroup(self))
        self.addObject('rbgDestType',   QtGui.QButtonGroup(self))

        self.setupUi(self)
        self.setWindowTitleEx(u'Шаблон дополнительных данных обмена N3.УО')

        self.setModels(self.tblUploadCases, self.modelUploadCases, self.selectionModelUploadCases)
        self.tblUploadCases.addPopupDelRow()

        self.setModels(self.tblUploadActionTypes, self.modelUploadActionTypes, self.selectionModelUploadActionTypes)
        self.tblUploadActionTypes.addPopupDelRow()

        self.setModels(self.tblElements, self.modelElements, self.selectionModelElements)
        self.tblElements.addPopupDelRow()

        self.setModels(self.tblDownloadElements, self.modelDownloadElements, self.selectionModelDownloadElements)
        self.tblDownloadElements.addPopupDelRow()

        self.rbgSourceType.addButton(self.rbSourceIsDirection, 0)
        self.rbgSourceType.addButton(self.rbSourceIsActionFromSameEvent, 1)
        self.rbgSourceType.addButton(self.rbSourceIsAnyAction, 2)

        self.rbgDestType.addButton(self.rbDestIsDirection, 0)
        self.rbgDestType.addButton(self.rbDestIsSeparateAction, 1)

        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue( self.edtName,              record, 'name')
        setCheckBoxValue( self.chkUploadEnabled,     record, 'uploadEnabled')
        setRadioButtonValue(self.rbgSourceType,      record, 'sourceType')

        setRBComboBoxValue(self.cmbDestActionType,   record, 'destActionType_id')
        if self.cmbDestActionType.value():
            self.rbDestIsSeparateAction.setChecked(True)
        else:
            self.rbDestIsDirection.setChecked(True)

        self.modelUploadCases.loadItems(self.itemId())
        self.modelUploadActionTypes.loadItems(self.itemId())
        self.modelElements.loadItems(self.itemId())
        self.modelDownloadElements.loadItems(self.itemId())
        pass


    def checkDataEntered(self):
        return True


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue( self.edtName,              record, 'name')
        getCheckBoxValue( self.chkUploadEnabled,     record, 'uploadEnabled')
        getRadioButtonValue(self.rbgSourceType,      record, 'sourceType')

        record.setValue('destActionType_id',
                         self.cmbDestActionType.value() if self.rbDestIsSeparateAction.isChecked() else None
                       )

        return record


    def saveInternals(self, id):
        self.modelUploadCases.saveItems(id)
        self.modelUploadActionTypes.saveItems(id)
        self.modelElements.saveItems(id)
        self.modelDownloadElements.saveItems(id)


class CUploadCasesModel(CInDocTableModel):
    directionTypeNameList = [u'Госпитализация',
                             u'Восстановительное лечение',
                             u'Обследование',
                             u'Консультация',
                             u'Исследование',
                            ]
#    dtHosp = 0
#    dt1 = 1

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ExtraDataDef_UploadCase', 'id', 'master_id', parent)
#        self.setEnableAppendLine(True)
        self.addCol(CEnumInDocTableCol(u'Тип направления',  'directionType', 10, self.directionTypeNameList))
        self.addCol(CRBInDocTableCol(u'Профиль койки',      'profile_id',    20, 'rbHospitalBedProfile', showFields = CRBComboBox.showName))
        self.addCol(CRBInDocTableCol(u'Специальность',      'speciality_id', 20, 'rbSpeciality', showFields = CRBComboBox.showName))
        self.addCol(CRBServiceInDocTableCol(u'Услуга',      'service_id',    20, 'rbService', showFields = CRBComboBox.showName))


#    def flags(self, index):
#        row = index.row()
#        column = index.column()
#        if column == 0:
#            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
#
#        if row<self.realRowCount():
#            sourceType = forceInt(self.value(row, 'sourceType'))
#            if sourceType != self.stProperty and column == 3:
#                return Qt.ItemIsSelectable
#            else:
#                return Qt.ItemIsSelectable | Qt.ItemIsEnabled
#        return Qt.ItemIsSelectable
#
#
#    def setData(self, index, value, role=Qt.EditRole):
#        result = CInDocTableModel.setData(self, index, value, role)
#        if result:
#            row = index.row()
#            column = index.column()
#            if column == 2:
#                sourceType = forceInt(self.value(row, 'sourceType'))
#                if sourceType != self.stProperty:
#                    self.setValue(row, 'sourcePropertyDescr', '')
#        return result



class CUploadActionTypesModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ExtraDataDef_UploadActionType', 'id', 'master_id', parent)
#        self.setEnableAppendLine(True)
        self.addCol(CActionTypeFindInDocTableCol(u'Тип действия', 'actionType_id', 100,  'ActionType',  None))


class CElementsModel(CInDocTableModel):
    sourceTypeNameList = [u'-',
                          u'Свойство',
                          u'Дата выполнения',
                          u'Примечание',
                         ]

    stNone     = 0
    stProperty = 1
    stDate     = 2
    stNote     = 3

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ExtraDataDef_Element', 'id', 'master_id', parent)
#        self.setEnableAppendLine(True)
        self.addCol(CInDocTableCol(u'Ключ ExtraData', 'name', 20))
        self.addCol(CInDocTableCol(u'Значение по умолчанию', 'defaultValue', 20))
        self.addCol(CEnumInDocTableCol(u'Тип источника', 'sourceType', 10, self.sourceTypeNameList))
        self.addCol(CInDocTableCol(u'Описание свойства', 'sourcePropertyDescr', 20))


    def cellReadOnly(self, index):
        if index.isValid():
            row = index.row()
            column = index.column()
            if column < 3:
                return False

            if row<self.realRowCount():
                sourceType = forceInt(self.value(row, 'sourceType'))
                if sourceType != self.stProperty and column == 3:
                    return True
                else:
                    return False
        return False


    def setData(self, index, value, role=Qt.EditRole):
        result = CInDocTableModel.setData(self, index, value, role)
        if result:
            row = index.row()
            column = index.column()
            if column == 2:
                sourceType = forceInt(self.value(row, 'sourceType'))
                if sourceType != self.stProperty:
                    self.setValue(row, 'sourcePropertyDescr', '')
        return result



class CDownloadElementsModel(CInDocTableModel):
    targetTypeNameList = [u'-',
                          u'Свойство',
                          u'Дата выполнения',
                          u'Примечание',
                         ]

    ttNone     = 0
    ttProperty = 1
    ttDate     = 2
    ttNote     = 3

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ExtraDataDef_Download', 'id', 'master_id', parent)
#        self.setEnableAppendLine(True)
        self.addCol(CEnumInDocTableCol(u'Тип получателя', 'targetType', 10, self.targetTypeNameList))
        self.addCol(CInDocTableCol(u'Описание свойства', 'targetPropertyDescr', 20))
        self.addCol(CInDocTableCol(u'Формат значения', 'formatValue', 20))


    def cellReadOnly(self, index):
        if index.isValid():
            row = index.row()
            column = index.column()
            if column == 0:
                return False

            if row<self.realRowCount():
                targetType = forceInt(self.value(row, 'targetType'))
                if (    targetType == self.ttProperty
                     or targetType == self.ttDate and column == 2
                     or targetType == self.ttNote and column == 2
                   ):
                    return False
                return True
        return False


    def setData(self, index, value, role=Qt.EditRole):
        result = CInDocTableModel.setData(self, index, value, role)
        if result:
            row = index.row()
            column = index.column()
            if column == 0:
                targetType = forceInt(self.value(row, 'targetType'))
                if targetType == self.ttNone:
                    self.setValue(row, 'formatValue', '')
                if targetType != self.ttProperty:
                    self.setValue(row, 'targetPropertyDescr', '')
        return result
