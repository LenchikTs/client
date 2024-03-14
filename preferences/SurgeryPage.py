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
from PyQt4.QtCore import pyqtSignature

from library.Utils import forceRef, toVariant, forceInt

from Ui_SurgeryPage import Ui_SurgeryPage


class CSurgeryPage(Ui_SurgeryPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbRestrictFormationSurgeryPage.setCurrentIndex(forceInt(props.get('surgeryPageRestrictFormation', 0)))
        self.cmbOrgStructure.setValue(forceRef(props.get('surgeryPageOrgStructureId', None)))


    def getProps(self, props):
        props['surgeryPageRestrictFormation'] = toVariant(self.cmbRestrictFormationSurgeryPage.currentIndex())
        props['surgeryPageOrgStructureId'] = toVariant(self.cmbOrgStructure.value())


    @pyqtSignature('int')
    def on_cmbRestrictFormationSurgeryPage_currentIndexChanged(self, index):
        self.cmbOrgStructure.setEnabled(index == 4)



