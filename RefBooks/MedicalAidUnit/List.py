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

from library.interchange                        import getLineEditValue, setLineEditValue

from library.ItemsListDialog                    import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel                         import CTextCol

from RefBooks.Tables                            import rbCode, rbName, rbMedicalAidUnit


from Ui_RBMedicalAidUnitEditor import Ui_ItemEditorDialog



class CRBMedicalAidUnitList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode],   8),
            CTextCol(u'Наименование', [rbName],   8),
            CTextCol(u'Описание',     ['descr'], 64),
#            CTextCol(u'Региональный код',     ['regionalCode'], 64),
#            CTextCol(u'Федеральный код',      ['federalCode'], 8),
            ], rbMedicalAidUnit, [rbCode, rbName])
        self.setWindowTitleEx(u'Единицы учета медицинской помощи')

    def getItemEditor(self):
        return CRBMedicalAidUnitEditor(self)


class CRBMedicalAidUnitEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbMedicalAidUnit)
        self.setWindowTitleEx(u'Единица учета медицинской помощи')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(self.edtDescr, record, 'descr')
        setLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        setLineEditValue(self.edtFederalCode, record, 'federalCode')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(self.edtDescr, record, 'descr')
        getLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        getLineEditValue(self.edtFederalCode, record, 'federalCode')
        return record

