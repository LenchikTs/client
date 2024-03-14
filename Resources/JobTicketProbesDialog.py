# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui
from PyQt4.QtCore import QVariant
from library.DialogBase import CDialogBase
from library.Utils import forceInt

from Ui_JobTicketProbesDialog import Ui_JobTicketProbesDialog

class CJobTicketProbesDialog(CDialogBase, Ui_JobTicketProbesDialog):
    def __init__(self, parent, probeModel=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self._probeModel = probeModel
        self.setModels(self.tblTreeProbe, self._probeModel)
        prefs=QtGui.qApp.preferences.appPrefs
        expand = forceInt(prefs.get('probesTreeExpand',  QVariant()))
        if expand == 1:
            self.tblTreeProbe.expandAll()
        elif expand == 2:
            expandLevel = forceInt(prefs.get('probesTreeExpandLevel',  QVariant(1)))
            self.tblTreeProbe.expandToDepth(expandLevel-1)
        elif self._probeModel.isCourseJobTicket:
            self.tblTreeProbe.expandToDepth(0)
        self.setWindowTitle(u'Пробы')
