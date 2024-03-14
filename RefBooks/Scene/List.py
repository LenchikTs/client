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

from PyQt4.QtCore import pyqtSignature

from library.interchange               import getComboBoxValue, getLineEditValue, setComboBoxValue, setLineEditValue
from library.ItemsListDialog           import CItemsListDialog, CItemEditorDialog
from library.TableModel                import CTextCol
from library.Utils                     import forceString, forceStringEx, toVariant

from RefBooks.Service.ServiceModifier  import createModifier, parseModifier, CServiceModifierCol, testRegExpServiceModifier
from RefBooks.Tables                   import rbCode, rbName, rbScene

from Ui_RBSceneEditor                  import Ui_ItemEditorDialog


class CRBSceneList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                     [rbCode], 10),
            CTextCol(u'Наименование',            [rbName], 30),
            CTextCol(u'Код ЕГИСЗ',               ['usishCode'], 10),
            CServiceModifierCol(u'Модификатор кода услуги', ['serviceModifier'],  30),
            ], rbScene, [rbCode, rbName])
        self.setWindowTitleEx(u'Места выполнения визита')

    def getItemEditor(self):
        return CRBSceneEditor(self)
#
# ##########################################################################
#

class CRBSceneEditor(Ui_ItemEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        from Timeline.Schedule import CSchedule

        CItemEditorDialog.__init__(self, parent, rbScene)
        self.setWindowTitleEx(u'Место выполнения визита')
        self.cmbAppointmentType.clear()
        self.cmbAppointmentType.addItems(CSchedule.atNames)
        self.rbNoModifyService.setChecked(True)
        self.setupDirtyCather()
        self.regExpTestStr  =''


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setLineEditValue(   self.edtUsishCode,                         record, 'usishCode')
        setComboBoxValue(   self.cmbAppointmentType,                   record, 'appointmentType')
        action, text = parseModifier(record.value('serviceModifier'))
        if action == 0:
            self.rbNoModifyService.setChecked(True)
        elif action == 1:
            self.rbRemoveService.setChecked(True)
        elif action == 2:
            self.rbReplaceService.setChecked(True)
            self.edtNewServiceName.setText(text)
        elif action == 3:
            self.rbModifyService.setChecked(True)
            self.edtNewServicePrefix.setText(text)
        elif action == 4:
            self.rbModifyByRegExp.setChecked(True)
            self.edtRegExp.setPlainText(text)
        else:
            self.rbNoModifyService.setChecked(True)
            self.edtNewServiceName.setText(text)
            self.edtNewServicePrefix.setText(text)


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getLineEditValue(   self.edtUsishCode,                         record, 'usishCode')
        getComboBoxValue(   self.cmbAppointmentType,                   record, 'appointmentType')
        action = 0
        text = u''
        if self.rbNoModifyService.isChecked():
            action = 0
        if self.rbRemoveService.isChecked():
            action = 1
        if self.rbReplaceService.isChecked():
            action = 2
            text = forceStringEx(self.edtNewServiceName.text())
        if self.rbModifyService.isChecked():
            action = 3
            text = forceStringEx(self.edtNewServicePrefix.text())
        if self.rbModifyByRegExp.isChecked():
            action = 4
            text = forceString(self.edtRegExp.toPlainText())
        record.setValue('serviceModifier', toVariant(createModifier(action, text)))
        return record


    @pyqtSignature('')
    def on_btnRegExpTest_clicked(self):
        self.regExpTestStr = testRegExpServiceModifier(self, self.edtRegExp.toPlainText(), self.regExpTestStr)
