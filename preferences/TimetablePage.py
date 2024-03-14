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
## Страница настройки - панель График
##
#############################################################################

from PyQt4 import QtGui

from library.Utils            import (
                                         forceBool,
                                         forceInt,
                                         toVariant,
                                     )

from Ui_TimetablePage import Ui_timetablePage


class CTimetablePage(Ui_timetablePage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbDoubleClickQueuePerson.setCurrentIndex(forceInt(props.get('doubleClickQueuePerson', 0)))
        self.chkAmbulanceUserCheckable.setChecked(forceBool(props.get('ambulanceUserCheckable', False)))
        self.chkSyncCheckableAndInvitiation.setChecked(forceBool(props.get('syncCheckableAndInvitiation', False)))
        self.cmbCombineTimetable.setCurrentIndex(forceInt(props.get('combineTimetable', 0)))


    def getProps(self, props):
        props['doubleClickQueuePerson'] = toVariant(self.cmbDoubleClickQueuePerson.currentIndex())
        props['ambulanceUserCheckable'] = toVariant(int(self.chkAmbulanceUserCheckable.isChecked()))
        props['syncCheckableAndInvitiation'] = toVariant(int(self.chkSyncCheckableAndInvitiation.isChecked()))
        props['combineTimetable']       = toVariant(self.cmbCombineTimetable.currentIndex())
