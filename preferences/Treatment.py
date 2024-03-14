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
## Страница настройки выбора ЛПУ, подразделения, региона
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceInt, toVariant

from Ui_Treatment import Ui_Treatment


class CTreatment(Ui_Treatment, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbShowOrgStructure.setCurrentIndex(forceInt(props.get('showOrgStructureForTreatment', 0)))


    def getProps(self, props):
        props['showOrgStructureForTreatment'] = toVariant(self.cmbShowOrgStructure.currentIndex())



