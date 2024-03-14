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
## Регистрационная карта пациента
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceBool, toVariant

from preferences.Ui_FormPage import Ui_FormPage


class CFormPage(Ui_FormPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.chkTempInvalid.setChecked(forceBool(props.get('showingFormTempInvalid', True)))


    def getProps(self, props):
        props['showingFormTempInvalid'] = toVariant(self.chkTempInvalid.isChecked())

