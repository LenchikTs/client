# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import QDate, pyqtSignature

from library.crbcombobox import CRBComboBox
from library.DialogBase import CDialogBase
from library.Utils import forceString, forceStringEx, formatNum1

from Accounting.Ui_PayStatusDialog import Ui_PayStatusDialog


class CPayStatusDialog(CDialogBase, Ui_PayStatusDialog):
    def __init__(self,  parent, financeId):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
#        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
#        self.setWindowTitleEx(u'Счет')
        self.cmbRefuseType.setTable('rbPayRefuseType',
                                    addNone=False,
                                    filter='finance_id=\'%s\'' % financeId)
        self.cmbRefuseType.setShowFields(CRBComboBox.showCodeAndName)
        self.setupDirtyCather()


    def setAccountItemsCount(self, count):
        self.setWindowTitle(u'Подтверждение оплаты по %s реестра'% formatNum1(count, (u'записи', u'записям', u'записям')))


    def setParams(self, params):
        self.edtDate.setDate(params.get('date', QDate()))
        self.edtNumber.setText(params.get('number', ''))
        if params.get('accepted', True):
            self.rbnAccepted.setChecked(True)
        else:
            if params.get('factPayedSum', 0):
                self.rbnFactPayed.setChecked(True)
                self.edtFactPayed.setValue(params.get('factPayedSum', 0))
            else:
                self.rbnRefused.setChecked(True)
        self.cmbRefuseType.setValue(params.get('refuseTypeId', None))
        self.edtNote.setText(params.get('note', ''))
        self.setIsDirty(False)


    def params(self):
        accepted  = self.rbnAccepted.isChecked()
        factPayed = self.rbnFactPayed.isChecked()
        result = {'date'     : self.edtDate.date(),
                  'number'   : forceString(self.edtNumber.text()),
                  'accepted' : accepted,
                  'factPayed': factPayed,
                  'factPayedSum': self.edtFactPayed.value() if factPayed else 0,
                  'refuseTypeId': None
                                  if (accepted or factPayed)
                                  else self.cmbRefuseType.value(),
                  'note'     : forceStringEx(self.edtNote.text()),
                 }
        return result


    def checkDataEntered(self):
        result = True
        date = self.edtDate.date()
        number = forceStringEx(self.edtNumber.text())
        accepted = self.rbnAccepted.isChecked()
        refuseTypeId = self.cmbRefuseType.value()
        if date or number or (not accepted and refuseTypeId):
            result = result and (date
                                 or self.checkInputMessage(u'дату', False, self.edtDate))
            result = result and (number
                                 or self.checkInputMessage(u'номер', False, self.edtNumber))
            if not accepted:
                result = result and (refuseTypeId
                                     or self.checkInputMessage(u'причину отказа', False, self.cmbRefuseType))
        return result


    @pyqtSignature('bool')
    def on_rbnAccepted_toggled(self, checked):
        self.cmbRefuseType.setEnabled( not self.rbnAccepted.isChecked() )
