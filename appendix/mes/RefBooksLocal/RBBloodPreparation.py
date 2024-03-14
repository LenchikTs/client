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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from library.Utils import *
from library.interchange import *
from library.ItemsListDialog import *

from ItemsListDialogEx import *

from Tables import *
from Ui_RBBloodPreparation import Ui_Dialog


class CRBBloodPreparationList(CItemsListDialogEx):
    def __init__(self, parent):
        CItemsListDialogEx.__init__(self, parent, [
            CTextCol(   u'Код',                  [rbCode], 10),
            CTextCol(   u'Наименование',         [rbName], 30),
            CRefBookCol(   u'Тип препарата',     ['type_id'], rbBloodPreparationType, 30),
            CNumCol(   u'Дозировка',         ['dosage'], 30),
            CNumCol(   u'Тариф',         ['tariff'], 30),
            ], rbBloodPreparation, [rbCode, rbName], uniqueCode=True)
        self.setWindowTitleEx(u'Препараты крови')

    def getItemEditor(self):
        return CRBBloodPreparationEditor(self)
#
# ##########################################################################
#

class CRBBloodPreparationEditor(CItemEditorDialogEx, Ui_Dialog):
    def __init__(self,  parent):
        CItemEditorDialogEx.__init__(self, parent, rbBloodPreparation)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Препарат крови')
        self.cmbType.setTable(rbBloodPreparationType)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,         record, 'code')
        setLineEditValue(   self.edtName,         record, 'name')
        setRBComboBoxValue(   self.cmbType,       record, 'type_id')
        setSpinBoxValue(   self.spinBox,       record, 'dosage')
        setLineEditValue(   self.edtTariff,      record, 'tariff')

    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,         record, 'code')
        getLineEditValue(   self.edtName,         record, 'name')
        getRBComboBoxValue(   self.cmbType,       record, 'type_id')
        getSpinBoxValue(   self.spinBox,       record, 'dosage')
        getLineEditValue(   self.edtTariff,      record, 'tariff')
        return record