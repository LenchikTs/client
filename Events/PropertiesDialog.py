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

from PyQt4.QtCore import Qt

from library.DialogBase          import CDialogBase
from Events.PropertiesTableModel import CPropertiesTableModel
from Events.Utils                import setActionPropertiesColumnVisible

from Events.Ui_PropertiesDialog import Ui_PropertiesDialog

class CPropertiesDialog(CDialogBase, Ui_PropertiesDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('APActionProperties', CPropertiesTableModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(u'Внимание! В текущее Действие не скопированы Свойства!')
        self.setModels(self.tblAPProps, self.modelAPActionProperties, self.selectionModelAPActionProperties)
        self.action = None
        self.actionType = None


    def setProperties(self, action, propertyList, clientSex = None, clientAge = None):
        self.action = action
        self.actionType = self.action.getType()
        self.modelAPActionProperties.setProperties(self.action, propertyList, clientSex, clientAge)
        setActionPropertiesColumnVisible(self.actionType, self.tblAPProps)
        self.tblAPProps.resizeRowsToContents()
