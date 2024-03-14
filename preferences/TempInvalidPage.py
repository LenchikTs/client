# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки - ввод документов ВУТ
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceString, toVariant, forceRef, forceBool

from Ui_TempInvalidPage import Ui_tempInvalidPage


class CTempInvalidPage(Ui_tempInvalidPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cmbTempInvalidDoctype.setTable('rbTempInvalidDocument', True, 'type=0')
        self.cmbTempInvalidReason.setTable('rbTempInvalidReason', True, 'type=0')
        self.cmbTempInvalidRegime.setTable('rbTempInvalidRegime', True, 'type=0')

    def setProps(self, props):
        self.cmbTempInvalidDoctype.setCode(forceString(props.get('tempInvalidDoctype', '')))
        self.cmbTempInvalidReason.setCode(forceString(props.get('tempInvalidReason', '')))
        self.cmbTempInvalidRegime.setValue(forceRef(props.get('tempInvalidRegime', None)))
        self.chkTempInvalidRequestFss.setChecked(forceBool(props.get('tempInvalidRequestFss', True)))

    def getProps(self, props):
        props['tempInvalidDoctype'] = toVariant(self.cmbTempInvalidDoctype.code())
        props['tempInvalidReason'] = toVariant(self.cmbTempInvalidReason.code())
        props['tempInvalidRegime'] = toVariant(self.cmbTempInvalidRegime.value())
        props['tempInvalidRequestFss'] = toVariant(self.chkTempInvalidRequestFss.isChecked())
