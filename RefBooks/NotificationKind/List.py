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
u"""Справочник 'Виды оповещений'"""

from PyQt4.QtCore import pyqtSignature

from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel import CTextCol
from library.Utils import toVariant, forceInt, forceString, forceStringEx

from RefBooks.Tables import rbCode, rbName, rbNotificationKind, rbContactType
from .Ui_RBNotificationKind import Ui_NotificationKindEditorDialog


class CRBNotificationKindList(CItemsListDialog):
    u"""Список видов оповещений"""
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код', [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbNotificationKind, [rbCode, rbName])
        self.setWindowTitleEx(u'Виды оповещений')


    def getItemEditor(self):
        u"""Возвращает диалог редактировния вида оповещения"""
        return CRBNotificationKindEditor(self)


class CRBNotificationKindEditor(CItemEditorBaseDialog, Ui_NotificationKindEditorDialog):
    u"""Диалог редактирования вида оповещения"""
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, rbNotificationKind)
        self.setupUi(self)
        self.cmbContactType.setTable(rbContactType)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.edtCode.setText(forceString(record.value('code')))
        self.edtName.setText(forceString(record.value('name')))
        self.cmbContactType.setCurrentIndex(forceInt(
            record.value('contactType_id')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('code', toVariant(forceStringEx(self.edtCode.text())))
        record.setValue('name', toVariant(forceStringEx(self.edtName.text())))
        record.setValue('contactType_id', toVariant(
            forceInt(self.cmbContactType.currentIndex())))
        return record


    @pyqtSignature('QString')
    def on_edtCode_textEdited(self, text):
        self.setIsDirty()


    @pyqtSignature('QString')
    def on_edtName_textEdited(self, text):
        self.setIsDirty()


    @pyqtSignature('int')
    def on_cmbContactType_currentIndexChanged(self, _):
        self.setIsDirty()
