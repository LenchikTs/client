# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Путевка
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceInt, toVariant

from Ui_VoucherPage import Ui_VoucherPage

DefaultVoucherDuration = 0

class CVoucherPage(Ui_VoucherPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.edtVoucherDuration.setValue(forceInt(props.get('voucherDuration', DefaultVoucherDuration)))


    def getProps(self, props):
        props['voucherDuration'] = toVariant(self.edtVoucherDuration.value())

