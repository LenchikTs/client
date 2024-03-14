# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки картотеки
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceInt, toVariant, forceBool

from Ui_RegistryPage import Ui_registryPage


class CRegistryPage(Ui_registryPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbDoubleClickQueueClient.setCurrentIndex(forceInt(props.get('doubleClickQueueClient', 0)))
        self.cmbOnSingleClientInSearchResult.setCurrentIndex(forceInt(props.get('onSingleClientInSearchResult', 0)))
        self.edtClientsLimit.setValue(forceInt(props.get('clientsLimit', 10000)))
        self.chkExternalNotificationAuto.setChecked(forceBool(props.get('externalNotificationAuto', False)))
        self.chkExternalNotificationOnlyAttach.setChecked(forceBool(props.get('externalNotificationOnlyAttach', False)))


    def getProps(self, props):
        props['doubleClickQueueClient'] = toVariant(self.cmbDoubleClickQueueClient.currentIndex())
        props['onSingleClientInSearchResult'] = toVariant(self.cmbOnSingleClientInSearchResult.currentIndex())
        props['clientsLimit'] = toVariant(self.edtClientsLimit.value())
        props['externalNotificationAuto'] = toVariant(self.chkExternalNotificationAuto.isChecked())
        props['externalNotificationOnlyAttach'] = toVariant(self.chkExternalNotificationOnlyAttach.isChecked())
