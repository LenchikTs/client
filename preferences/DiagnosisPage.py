# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки - панель "ЛУД"
##
#############################################################################

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from library.Utils            import (
                                         forceInt,
                                         toVariant,
                                     )

from Ui_DiagnosisPage import Ui_DiagnosisPage


class CDiagnosisPage(Ui_DiagnosisPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.chkAnalyzeSurveillance.setCheckState(Qt.Checked) if QtGui.qApp.isDockDiagnosisAnalyzeSurveillance() else self.chkAnalyzeSurveillance.setCheckState(Qt.Unchecked)



    def getProps(self, props):
        props['dockDiagnosisAnalyzeSurveillance'] = toVariant(bool(self.chkAnalyzeSurveillance.checkState()))
