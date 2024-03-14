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

from PyQt4.QtCore import Qt, pyqtSignature

from library.DialogBase      import CDialogBase
from library.interchange     import getLineEditValue, getRBComboBoxValue, setLineEditValue, setRBComboBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CRefBookCol, CTextCol
from library.Utils           import forceStringEx

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBNomenclatureKindEditor import Ui_ItemEditorDialog
from .Ui_RBNomenclatureKindFilter import Ui_ItemFilterDialog


class CRBNomenclatureKindList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CRefBookCol(u'Класс',     ['class_id'], 'rbNomenclatureClass', 20),
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbNomenclatureKind', [rbCode, rbName],
            filterClass=CRBNomenclatureKindListFilter)
        self.setWindowTitleEx(u'Виды ЛСиИМН')


    def getItemEditor(self):
        return CRBNomenclatureKindEditor(self)


    def generateFilterByProps(self, props):
        cond = CItemsListDialog.generateFilterByProps(self, props)
        table = self.model.table()
        code = props.get('code', None)
        name = props.get('name', None)
        classId = props.get('classId', None)
        if code:
            cond.append(table['code'].like(code))
        if name:
            cond.append(table['name'].like(name))
        if classId:
            cond.append(table['class_id'].eq(classId))
        return cond

#
# ##########################################################################
#

class CRBNomenclatureKindListFilter(CDialogBase, Ui_ItemFilterDialog):
    def __init__(self,  parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Фильтр вида ЛСиИМН')
        self.cmbClass.setTable('rbNomenclatureClass', True)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == self.buttonBox.Reset:
            self.setProps({})


    def setProps(self, props):
        self.edtCode.setText(props.get('code', ''))
        self.edtName.setText(props.get('name', ''))
        self.cmbClass.setValue(props.get('classId', None))


    def props(self):
        code = forceStringEx(self.edtCode.text())
        name = forceStringEx(self.edtName.text())
        classId = self.cmbClass.value()

        result = {}
        if code:
            result['code'] = code
        if name:
            result['name'] = name
        if classId:
            result['classId'] = classId
        return result

#
# ##########################################################################
#

class CRBNomenclatureKindEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbNomenclatureKind')
        self.setupUi(self)
        self.setWindowTitleEx(u'Вид ЛСиИМН')
        self.cmbClass.setTable('rbNomenclatureClass', True)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,          record, 'code')
        setLineEditValue(   self.edtName,          record, 'name')
        setRBComboBoxValue( self.cmbClass,         record, 'class_id')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,          record, 'code')
        getLineEditValue(   self.edtName,          record, 'name')
        getRBComboBoxValue( self.cmbClass,         record, 'class_id')
        return record
