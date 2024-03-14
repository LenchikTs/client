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
from PyQt4.QtCore import Qt, pyqtSignature, QDate, SIGNAL

from library.HierarchicalItemsListDialog import CHierarchicalItemsListDialog
from library.Utils import unformatSNILS

from .Ui_ActionTemplateListDialog import Ui_ActionTemplateListDialog

class CActionTemplateListDialog(Ui_ActionTemplateListDialog, CHierarchicalItemsListDialog):
    def __init__(self, parent, cols, tableName, order, forSelect=False, filterClass=None, findClass=None):
        CHierarchicalItemsListDialog.__init__(self, parent, cols, tableName, order, forSelect, filterClass, findClass)
        self.tblItems.setSortingEnabled(True)
        self.model = self.tblItems.model()
        self.order = 'name ASC'
        self.connect(self.tblItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.sortByColumn)


    def sortByColumn(self, column):
        name = self.model.cols()[column].fields()[0]
        header = self.tblItems.horizontalHeader()
        header.setSortIndicatorShown(True)
        if self.order == name + ' ASC':
            asc = ' DESC'
            header.setSortIndicator(column, Qt.DescendingOrder)
        elif self.order == name + ' DESC':
            asc = ' ASC'
            header.setSortIndicator(column, Qt.AscendingOrder)
        else:
            asc = ' ASC'
            header.setSortIndicator(column, Qt.AscendingOrder)
        self.order = name + asc
        self.renewListAndSetToWithoutUpdate()


    def postSetupUi(self):
        self.setModels(self.treeItems,  self.modelTree,  self.selectionModelTree)
        self.setModels(self.tblItems,   self.modelTable, self.selectionModelTable)
        self.treeItems.header().hide()
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbActionType.setAllSelectable(True)
        self.btnSelect.setEnabled(self.forSelect)
        self.btnSelect.setVisible(self.forSelect)
        self.btnSelect.setDefault(self.forSelect)
        self.btnFilter.setEnabled(bool(self.filterClass))
        self.btnFilter.setVisible(bool(self.filterClass))
        self.btnFind.setEnabled(bool(self.findClass))
        self.btnFind.setVisible(bool(self.findClass))
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.edtBegCreateDate.blockSignals(True)
        self.edtBegCreateDate.setDate(QDate())
        self.edtBegCreateDate.blockSignals(False)
        self.edtEndCreateDate.blockSignals(True)
        self.edtEndCreateDate.setDate(QDate())
        self.edtEndCreateDate.blockSignals(False)
        # idList = self.select(self.props)
        # self.modelTable.setIdList(idList)
        # self.tblItems.selectRow(0)


    def renewListAndSetToWithoutUpdate(self, itemId=None):
        self.saveProps()
        if not itemId:
            itemId = self.tblItems.currentItemId()
        idList = self.select(self.props)
        self.tblItems.setIdList(idList, itemId)


    def setProps(self, props):
        self.props = props
        self.cmbActionType.setValue(props.get('actionTypeId', ''))
        self.cmbSpeciality.setValue(props.get('specialityId', None))
        self.cmbPerson.setValue(props.get('personId', None))
        self.edtSNILS.setText(props.get('snils', ''))
        self.cmbCreatePerson.setValue(props.get('createPersonId', None))
        self.edtBegCreateDate.setDate(props.get('begCreateDate', QDate()))
        self.edtEndCreateDate.setDate(props.get('endCreateDate', QDate()))


    def getProps(self):
        return self.props


    def saveProps(self):
        self.props['actionTypeId'] = self.cmbActionType.value()
        self.props['specialityId'] = self.cmbSpeciality.value()
        self.props['personId'] = self.cmbPerson.value()
        self.props['snils'] = self.edtSNILS.text()
        self.props['createPersonId'] = self.cmbCreatePerson.value()
        self.props['begCreateDate'] = self.edtBegCreateDate.date()
        self.props['endCreateDate'] = self.edtEndCreateDate.date()


    def select(self, props):
        db = QtGui.qApp.db
        if not self.props:
            table = self.modelTable.table()
            groupId = self.currentGroupId()
            return db.getIdList(table.name(),
                               'ActionTemplate.id',
                               table['group_id'].eq(groupId),
                               self.order)
        else:
            actionTypeId = props.get('actionTypeId', '')
            specialityId = props.get('specialityId', None)
            personId = props.get('personId', None)
            snils = unformatSNILS(props.get('snils', ''))
            createPersonId = props.get('createPersonId', None)
            begCreateDate = props.get('begCreateDate', QDate())
            endCreateDate = props.get('endCreateDate', QDate())
            tableActionTemplate = db.table('ActionTemplate')
            cond = [tableActionTemplate['deleted'].eq(0)]
            if createPersonId:
                cond.append(tableActionTemplate['createPerson_id'].eq(createPersonId))
            if begCreateDate:
                cond.append(tableActionTemplate['createDatetime'].dateGe(begCreateDate))
            if endCreateDate:
                cond.append(tableActionTemplate['createDatetime'].dateLe(endCreateDate))
            if snils:
                cond.append(tableActionTemplate['SNILS'].like(snils + '%'))
            groupId = self.currentGroupId()
            if groupId:
                cond.append(tableActionTemplate['group_id'].eq(groupId))
            queryTable = tableActionTemplate
            if actionTypeId or specialityId or personId:
                if actionTypeId:
                    tableAction = db.table('Action')
                    queryTable = queryTable.innerJoin(tableAction, tableAction['id'].eq(tableActionTemplate['action_id']))
                    cond.append(tableAction['actionType_id'].eq(actionTypeId))
                if specialityId:
                    cond.append(tableActionTemplate['speciality_id'].eq(specialityId))
                if personId:
                    cond.append(tableActionTemplate['owner_id'].eq(personId))
            return QtGui.qApp.db.getDistinctIdList(queryTable,
                               'ActionTemplate.id',
                               cond,
                               self.order)


    @pyqtSignature('int')
    def on_cmbActionType_currentIndexChanged(self, index):
        self.renewListAndSetToWithoutUpdate(None)

    @pyqtSignature('QString')
    def on_edtSNILS_textChanged(self, text):
        self.renewListAndSetToWithoutUpdate(None)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        if specialityId:
            self.cmbPerson.setValue(None)
        self.renewListAndSetToWithoutUpdate(None)


    @pyqtSignature('int')
    def on_cmbPerson_currentIndexChanged(self, index):
        personId = self.cmbPerson.value()
        if personId:
            self.cmbSpeciality.setValue(None)
        self.renewListAndSetToWithoutUpdate(None)


    @pyqtSignature('int')
    def on_cmbCreatePerson_currentIndexChanged(self, index):
        self.renewListAndSetToWithoutUpdate(None)


    @pyqtSignature('QDate')
    def on_edtBegCreateDate_dateChanged(self, date):
        self.renewListAndSetToWithoutUpdate(None)


    @pyqtSignature('QDate')
    def on_edtEndCreateDate_dateChanged(self, date):
        self.renewListAndSetToWithoutUpdate(None)
