# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights.setEnabled( reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import Qt, pyqtSignature

from library.InDocTable import CInDocTableCol
from library.interchange     import getCheckBoxValue, getLineEditValue, getRBComboBoxValue, setCheckBoxValue, setLineEditValue, setRBComboBoxValue
from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel      import CRefBookCol, CTextCol

from library.LineEditWithRegExpValidator import checkRegExp
from RefBooks.Tables                     import rbCode, rbDocumentType, rbDocumentTypeGroup, rbName
from .Descr                              import CDocumentTypeDescr
from .RegExpValidatorTest                import testRegExpValidator

from .Ui_RBDocumentTypeEditor import Ui_ItemEditorDialog


class CRBDocumentTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(    u'Код',              [rbCode], 20),
            CTextCol(    u'Федеральный код',  ['federalCode'], 20),
            CTextCol(    u'Региональный код', ['regionalCode'], 20),
            CTextCol(    u'Наименование',     [rbName], 40),
            CRefBookCol( u'Группа',       ['group_id'], rbDocumentTypeGroup, 30),

            ], rbDocumentType, [rbCode, rbName])
        self.setWindowTitleEx(u'Типы документов')

    def getItemEditor(self):
        return CRBDocumentTypeEditor(self)

#
# ##########################################################################
#

class CRBDocumentTypeEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbDocumentType')
        self.setWindowTitleEx(u'Тип документа')
        self.cmbGroup.setTable(rbDocumentTypeGroup, False)
        self.edtCode.setFocus(Qt.OtherFocusReason)
        self.fixPartSeparator()
        self.setupDirtyCather()


    def fixPartSeparator(self):
        if self.edtPartSeparator.text() == '':
            self.edtPartSeparator.setText(' ')


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(self.edtTitle, record, 'title')
        setLineEditValue(   self.edtFederalCode,    record, 'federalCode')
        setLineEditValue(   self.edtRegionalCode,   record, 'regionalCode')
        setRBComboBoxValue( self.cmbGroup,          record, 'group_id')
        setLineEditValue(self.edtLeftPartRegExp,    record, 'leftPartRegExp')
        setCheckBoxValue(self.chkHasRightPart,      record, 'hasRightPart')
        setLineEditValue(self.edtRightPartRegExp,   record, 'rightPartRegExp')
        setLineEditValue(self.edtPartSeparator,     record, 'partSeparator')
        setLineEditValue(self.edtNumberRegExp,      record, 'numberRegExp')
        setCheckBoxValue(self.chkCitizenship,       record, 'isCitizenship')
        self.fixPartSeparator()
        self.setIsDirty(False)


    def checkDataEntered(self):
        result = CItemEditorDialogWithIdentification.checkDataEntered(self)
        if result:
            if not checkRegExp(self.edtLeftPartRegExp.text()):
                result = self.checkInputMessage(u'правильное регулярное выражение', False, self.edtLeftPartRegExp)
        if result and self.chkHasRightPart.isChecked:
            if not checkRegExp(self.edtRightPartRegExp.text()):
                result = self.checkInputMessage(u'правильное регулярное выражение', False, self.edtRightPartRegExp)
        if result:
            if not checkRegExp(self.edtNumberRegExp.text()):
                result = self.checkInputMessage(u'правильное регулярное выражение', False, self.edtNumberRegExp)
        return result


    def getRecord(self):
        CDocumentTypeDescr.purge()

        self.fixPartSeparator()
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(self.edtTitle, record, 'title')
        getLineEditValue(   self.edtFederalCode,    record, 'federalCode')
        getLineEditValue(   self.edtRegionalCode,   record, 'regionalCode')
        getRBComboBoxValue( self.cmbGroup,          record, 'group_id')
        getLineEditValue(self.edtLeftPartRegExp,    record, 'leftPartRegExp')
        getCheckBoxValue(self.chkHasRightPart,      record, 'hasRightPart')
        getLineEditValue(self.edtRightPartRegExp,   record, 'rightPartRegExp')
        getLineEditValue(self.edtPartSeparator,     record, 'partSeparator')
        getLineEditValue(self.edtNumberRegExp,      record, 'numberRegExp')
        getCheckBoxValue(self.chkCitizenship,       record, 'isCitizenship')
        return record


    @pyqtSignature('')
    def on_btnTestLeftPart_clicked(self):
        testRegExpValidator(self.edtLeftPartRegExp.text())


    @pyqtSignature('')
    def on_btnTestRightPart_clicked(self):
        testRegExpValidator(self.edtRightPartRegExp.text())


    @pyqtSignature('')
    def on_btnTestNumber_clicked(self):
        testRegExpValidator(self.edtNumberRegExp.text())
