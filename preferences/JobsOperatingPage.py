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
## Страница настройки - всякая всячина
##
#############################################################################

from PyQt4 import QtGui

from library.Utils            import (
                                         forceBool,
                                         forceInt,
                                         toVariant,
                                     )

from Ui_JobsOperatingPage import Ui_jobsOperatingPage


class CJobsOperatingPage(Ui_jobsOperatingPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.chkJobTicketEndDateAskingIsRequired.setChecked(forceBool(props.get('jobTicketEndDateAskingIsRequired', True)))
        self.cmbJobsOperatingIdentifierScan.setCurrentIndex(forceInt(props.get('jobsOperatingIdentifierScan', 0)))


    def getProps(self, props):
        props['jobTicketEndDateAskingIsRequired'] = toVariant(int(self.chkJobTicketEndDateAskingIsRequired.isChecked()))
        props['jobsOperatingIdentifierScan'] = toVariant(self.cmbJobsOperatingIdentifierScan.currentIndex())

