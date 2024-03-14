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

from PyQt4              import QtGui
from PyQt4.QtCore       import Qt, pyqtSignature

from library.Utils        import getPref, setPref
from library.DialogBase   import CConstructHelperMixin
from Events.ActionPropertiesTable import CActionPropertiesTableModel
from Events.Utils         import inPlanOperatingDay

from Ui_OperatingAssistentsDialog import Ui_OperatingAssistentsDialog


class COperatingAssistentsDialog(QtGui.QDialog, CConstructHelperMixin, Ui_OperatingAssistentsDialog):
    def __init__(self,  parent, fieldName):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('APActionProperties', COperatingAssistentsPropertiesTableModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(fieldName)
        self.setModels(self.tblAPProps, self.modelAPActionProperties, self.selectionModelAPActionProperties)
        self.action = None
        self.fieldName = fieldName
        self.tblAPProps.setColumnHidden(0, True)
        self.tblAPProps.setColumnHidden(2, True)
        self.tblAPProps.setColumnHidden(3, True)
        self.tblAPProps.setColumnHidden(4, True)
        self.tblAPProps.resizeColumnsToContents()
        self.tblAPProps.resizeRowsToContents()
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'COperatingAssistentsDialog', {})
        self.tblAPProps.loadPreferences(preferences)


    def getAction(self):
        return self.action


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.action = self.modelAPActionProperties.action
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            preferences = self.tblAPProps.savePreferences()
            setPref(QtGui.qApp.preferences.windowPrefs, 'COperatingAssistentsDialog', preferences)
            self.close()


class COperatingAssistentsPropertiesTableModel(CActionPropertiesTableModel):
    def __init__(self, parent):
        CActionPropertiesTableModel.__init__(self, parent)


    def setAction(self, action, clientId, clientSex, clientAge, nameProperty, eventTypeId=None):
        self.action = action
        self.clientId = clientId
        self.eventTypeId = eventTypeId
        propertyTypeList = []
        if self.action:
            actionType = action.getType()
            for name, propertyType in actionType._propertiesByName.items():
                if propertyType.inPlanOperatingDay and nameProperty.lower() == inPlanOperatingDay[propertyType.inPlanOperatingDay].lower():
                    propertyTypeList.append(propertyType)
            propertyTypeList.sort(key=lambda x: (x.idx, x.name))
            self.propertyTypeList = [x for x in propertyTypeList if x.applicable(clientSex, clientAge) and self.visible(x)]
        else:
            self.propertyTypeList = []
        for propertyType in self.propertyTypeList:
            propertyType.shownUp(action, clientId)
        self.updateActionStatusTip()
        self.reset()

