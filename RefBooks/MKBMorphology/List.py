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

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialog
from library.TableModel      import CTextCol
from library.Utils           import forceString, forceStringEx, toVariant, trim

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBMKBMorphologyEditor import Ui_MKBMorphologyEditor


class CRBMKBMorphologyList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 8),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Группа', ['group'], 8),
            CTextCol(u'Нижняя граница МКБ', ['bottomMKBRange1'], 8),  # говно-то какое... а если было бы нужно три диапазона? а семь?
            CTextCol(u'Верхняя граница МКБ', ['topMKBRange1'], 8), 
            CTextCol(u'Нижняя граница МКБ', ['bottomMKBRange2'], 8), 
            CTextCol(u'Верхняя граница МКБ', ['topMKBRange2'], 8) 
            ], 'MKB_Morphology', [rbCode, rbName])
        self.setWindowTitleEx(u'Морфологии диагнозов МКБ')

    def getItemEditor(self):
        return CRBMKBMorphologyEditor(self)

#
# ##########################################################################
#

class CRBMKBMorphologyEditor(CItemEditorBaseDialog, Ui_MKBMorphologyEditor):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'MKB_Morphology')
        self.setupUi(self)
        self.cmbGroup.setTable('MKB_Morphology', addNone=True, filter='`group` IS NULL')
        self.setWindowTitleEx(u'Морфология диагноза МКБ')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, rbCode )
        setLineEditValue(self.edtName,                record, rbName )
        self.cmbGroup.setCode(forceString(record.value('group')))
        self.cmbDiagRangeFrom1.setText(forceString(record.value('bottomMKBRange1')))
        self.cmbDiagRangeTo1.setText(forceString(record.value('topMKBRange1')))
        self.cmbDiagRangeFrom2.setText(forceString(record.value('bottomMKBRange2')))
        self.cmbDiagRangeTo2.setText(forceString(record.value('topMKBRange2')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, rbCode )
        getLineEditValue(self.edtName,                record, rbName )
        record.setValue('group',           toVariant(forceStringEx(self.cmbGroup.code()) if forceStringEx(self.cmbGroup.code()) else None))
        record.setValue('bottomMKBRange1', toVariant(forceStringEx(self.cmbDiagRangeFrom1.text())))
        record.setValue('topMKBRange1',    toVariant(forceStringEx(self.cmbDiagRangeTo1.text())))
        record.setValue('bottomMKBRange2', toVariant(forceStringEx(self.cmbDiagRangeFrom2.text())))
        record.setValue('topMKBRange2',    toVariant(forceStringEx(self.cmbDiagRangeTo2.text())))
        return record


    def checkDataEntered(self):
        result = CItemEditorBaseDialog.checkDataEntered(self)
        result = result and self.checkCmbGroup()
        return result


    def badGroupCode(self):
        return self.checkValueMessage(u'Указан не подходящий код группы', False, self.cmbGroup)


    def checkCmbGroup(self):
        groupCode = self.cmbGroup.code()
        if bool(groupCode) and groupCode != '0':
            code = trim(self.edtCode.text())
            chkCode = code[1:4]
            try:
                iChkCode = int(chkCode)
                codeRange = groupCode.split('-')
                bCode = codeRange[0]
                if len(codeRange) == 2:
                    eCode = codeRange[1]
                else:
                    eCode = None
                if bool(eCode):
                    iBegCode = int(bCode[1:4])
                    iEndCode = int(eCode[1:4])
                    if iChkCode >= iBegCode and iChkCode <= iEndCode:
                        return True
                else:
                    iCode = int(bCode[1:4])
                    if iChkCode == iCode:
                        return True
                return self.badGroupCode()
            except:
                return self.badGroupCode()
        return True
