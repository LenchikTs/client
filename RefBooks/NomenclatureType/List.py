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
from PyQt4.QtCore import Qt, pyqtSignature


from library.DialogBase      import CDialogBase
from library.interchange     import ( getRBComboBoxValue,
                                      setLineEditValue,
                                      getLineEditValue,
                                    )
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CRefBookCol
from library.Utils           import forceStringEx, forceRef

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBNomenclatureTypeEditor import Ui_ItemEditorDialog
from .Ui_RBNomenclatureTypeFilter import Ui_ItemFilterDialog


class CRBNomenclatureTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CRefBookCol(u'Вид',   ['kind_id'], 'rbNomenclatureKind', 20),
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbNomenclatureType', [rbCode, rbName],
            filterClass = CRBNomenclatureTypeListFilter

            )
        self.setWindowTitleEx(u'Типы ЛСиИМН')


    def getItemEditor(self):
        return CRBNomenclatureTypeEditor(self)


    def generateFilterByProps(self, props):
        db = QtGui.qApp.db
        cond = CItemsListDialog.generateFilterByProps(self, props)
        table = self.model.table()
        code = props.get('code', None)
        name = props.get('name', None)
        classId = props.get('classId', None)
        kindId = props.get('kindId', None)
        if code:
            cond.append(table['code'].like(code))
        if name:
            cond.append(table['name'].like(name))
        if kindId:
            cond.append(table['kind_id'].eq(kindId))
        elif classId:
            kindTable = db.table('rbNomenclatureKind')
            kindIdList = db.getIdList(kindTable,
                                      'id',
                                      kindTable['class_id'].eq(classId)
                                     )

            cond.append(table['kind_id'].inlist(kindIdList))
        return cond


#
# ##########################################################################
#

class CRBNomenclatureTypeListFilter(CDialogBase, Ui_ItemFilterDialog):
    def __init__(self,  parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Фильтр типа ЛСиИМН')
        self.cmbClass.setTable('rbNomenclatureClass', True)
        self.cmbKind.setTable('rbNomenclatureKind', True)


    @pyqtSignature('int')
    def on_cmbClass_currentIndexChanged(self, index):
        self.setKindFilter()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == self.buttonBox.Reset:
            self.setProps({})


    def setKindFilter(self):
        table = QtGui.qApp.db.table('rbNomenclatureKind')
        classId = self.cmbClass.value()
        if classId:
            self.cmbKind.setFilter(table['class_id'].eq(classId))
        else:
            self.cmbKind.setFilter('')


    def setProps(self, props):
        self.edtCode.setText(props.get('code', ''))
        self.edtName.setText(props.get('name', ''))
        self.cmbClass.setValue(props.get('classId', None))
        self.cmbKind.setValue(props.get('kindId', None))


    def props(self):
        code = forceStringEx(self.edtCode.text())
        name = forceStringEx(self.edtName.text())
        classId = self.cmbClass.value()
        kindId = self.cmbKind.value()
        result = {}
        if code:
            result['code'] = code
        if name:
            result['name'] = name
        if classId:
            result['classId'] = classId
        if kindId:
            result['kindId'] = kindId
        return result


#
# ##########################################################################
#

class CRBNomenclatureTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbNomenclatureType')
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип ЛСиИМН')
        self.cmbClass.setTable('rbNomenclatureClass', True)
        self.cmbKind.setTable('rbNomenclatureKind', True)
        self.setKindFilter()
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,          record, 'code')
        setLineEditValue(   self.edtName,          record, 'name')
        kindId = forceRef(record.value('kind_id'))
        classId = forceRef(QtGui.qApp.db.translate('rbNomenclatureKind',
                                                   'id',
                                                   kindId,
                                                   'class_id'))
        self.cmbClass.setValue(classId)
        self.cmbKind.setValue(kindId)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,          record, 'code')
        getLineEditValue(   self.edtName,          record, 'name')
        getRBComboBoxValue( self.cmbKind,          record, 'kind_id')
        return record


    def setKindFilter(self):
        table = QtGui.qApp.db.table('rbNomenclatureKind')
        classId = self.cmbClass.value()
        if classId:
            self.cmbKind.setFilter(table['class_id'].eq(classId))
        else:
            self.cmbKind.setFilter('')


    @pyqtSignature('int')
    def on_cmbClass_currentIndexChanged(self, index):
        self.setKindFilter()
