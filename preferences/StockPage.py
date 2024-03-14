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
## Страница настройки - Складской учет
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceBool, toVariant, forceInt
from Users.Rights  import urAccessPreferencesPermitOnlyParentStock, urAccessPreferencesAgreeRequirementsStock

from Ui_StockPage import Ui_stockPage


class CStockPage(Ui_stockPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.chkPermitRequisitionsOnlyParentStock.setEnabled(QtGui.qApp.userHasRight(urAccessPreferencesPermitOnlyParentStock))
        self.cmbAccordingRequirementsType.setEnabled(QtGui.qApp.userHasRight(urAccessPreferencesAgreeRequirementsStock))


    def setProps(self, props):
        self.chkShowMainStockRemainings.setChecked(forceBool(props.get('showMainStockRemainings', False)))
        self.chkPermitRequisitionsOnlyParentStock.setChecked(forceBool(props.get('isPermitRequisitionsOnlyParentStock', False)))
        self.chkShowOnlyCurrentAndDescendantsStock.setChecked(forceBool(props.get('isShowOnlyCurrentAndDescendantsStock', False)))
        self.cmbAccordingRequirementsType.setCurrentIndex(forceInt(props.get('accordingRequirementsStockType', 0)))
        self.chkShowOnlyLsInFilterNomenklature.setChecked(forceBool(props.get('isShowOnlyLsInFilterNomenklature', False)))


    def getProps(self, props):
        props['showMainStockRemainings'] = toVariant(int(self.chkShowMainStockRemainings.isChecked()))
        props['isPermitRequisitionsOnlyParentStock'] = toVariant(int(self.chkPermitRequisitionsOnlyParentStock.isChecked()))
        props['isShowOnlyCurrentAndDescendantsStock'] = toVariant(int(self.chkShowOnlyCurrentAndDescendantsStock.isChecked()))
        props['accordingRequirementsStockType'] = toVariant(self.cmbAccordingRequirementsType.currentIndex())
        props['isShowOnlyLsInFilterNomenklature'] = toVariant(self.chkShowOnlyLsInFilterNomenklature.isChecked())


