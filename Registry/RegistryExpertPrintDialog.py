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

from PyQt4.QtCore       import pyqtSignature
from library.DialogBase import CDialogBase
from Ui_RegistryExpertPrintDialog import Ui_RegistryExpertPrintDialog


class CRegistryExpertPrintDialog(CDialogBase, Ui_RegistryExpertPrintDialog):
    __params = None  # Сохранять состояние чекбоксов

    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        if CRegistryExpertPrintDialog.__params is None:
            CRegistryExpertPrintDialog.__params = self.params()


    def setParams(self, params):
        params = CRegistryExpertPrintDialog.__params
        self.btnBegDatePermit.setChecked(params.get('begDatePermit', True))
        self.btnBegDateStationary.setChecked(params.get('begDateStationary', True))
        self.btnBreak.setChecked(params.get('break', True))
        self.btnBreakDate.setChecked(params.get('breakDate', True))
        self.btnDisability.setChecked(params.get('disability', True))
        self.btnEndDatePermit.setChecked(params.get('endDatePermit', True))
        self.btnEndDateStationary.setChecked(params.get('endDateStationary', True))
        self.btnNumberPermit.setChecked(params.get('numberPermit', True))
        self.btnResult.setChecked(params.get('result', True))
        self.btnResultDate.setChecked(params.get('resultDate', True))
        self.btnResultOtherwiseDate.setChecked(params.get('resultOtherwiseDate', True))
        self.btnIssueDate.setChecked(params.get('issueDate', True))


    def params(self):
        result = {}
        result['begDatePermit'] = self.btnBegDatePermit.isChecked()
        result['begDateStationary'] = self.btnBegDateStationary.isChecked()
        result['break'] = self.btnBreak.isChecked()
        result['breakDate'] = self.btnBreakDate.isChecked()
        result['disability'] = self.btnDisability.isChecked()
        result['endDatePermit'] = self.btnEndDatePermit.isChecked()
        result['endDateStationary'] = self.btnEndDateStationary.isChecked()
        result['numberPermit'] = self.btnNumberPermit.isChecked()
        result['result'] = self.btnResult.isChecked()
        result['resultDate'] = self.btnResultDate.isChecked()
        result['resultOtherwiseDate'] = self.btnResultOtherwiseDate.isChecked()
        result['issueDate'] = self.btnIssueDate.isChecked()
        CRegistryExpertPrintDialog.__params = result
        return result


    @pyqtSignature('')
    def on_btnSelectAll_clicked(self):
        pass

