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

from library.Utils        import toVariant, forceString, getPref, setPref
from library.DialogBase   import CDialogBase
from library.ICDUtils     import MKBwithoutSubclassification
from Events.ActionPropertiesTable import CActionPropertiesTableModel

from Ui_DiagnosisHospitalBedsDialog import Ui_DiagnosisHospitalBedsDialog


class CDiagnosisHospitalBedsDialog(CDialogBase, Ui_DiagnosisHospitalBedsDialog):
    def __init__(self,  parent):
        CDialogBase.__init__(self, parent)
        self.addModels('APActionProperties', CDiagnosisPropertiesTableModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblAPProps, self.modelAPActionProperties, self.selectionModelAPActionProperties)
        self.begDate = None
        self.tblAPProps.setColumnHidden(0, True)
        self.tblAPProps.setColumnHidden(2, True)
        self.tblAPProps.setColumnHidden(3, True)
        self.tblAPProps.setColumnHidden(4, True)
        self.tblAPProps.resizeColumnsToContents()
        self.tblAPProps.resizeRowsToContents()
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CDiagnosisHospitalBedsDialog', {})
        self.tblAPProps.loadPreferences(preferences)


    def setAPMKBBegDateFilter(self, begDate):
        self.begDate = begDate
        if self.begDate:
            self.cmbAPMKB.setFilter('''IF(MKB.endDate IS NOT NULL, MKB.endDate >= %s, 1)'''%(QtGui.qApp.db.formatDate(self.begDate)))
        else:
            self.cmbAPMKB.setFilter(u'')


    def setAPMKB(self, MKB):
        self.cmbAPMKB.setText(MKB)


    def getAPMKB(self):
        return self.cmbAPMKB.text()


    def checkActualMKB(self):
        result = True
        MKB = unicode(self.cmbAPMKB.text())
        if MKB:
            db = QtGui.qApp.db
            tableMKB = db.table('MKB')
            cond = [tableMKB['DiagID'].eq(MKBwithoutSubclassification(MKB))]
            cond.append(db.joinOr([tableMKB['endDate'].isNull(), tableMKB['endDate'].dateGe(self.begDate)] ))
            recordMKB = db.getRecordEx(tableMKB, [tableMKB['DiagID']], cond)
            result = result and (forceString(recordMKB.value('DiagID')) == MKBwithoutSubclassification(MKB) if recordMKB else False) or self.checkValueMessage(u'Диагноз %s не доступен для применения'%MKB, False, self.cmbAPMKB)
        return result


    @pyqtSignature('QString')
    def on_cmbAPMKB_textChanged(self, value):
        if value[-1:] == '.':
            value = value[:-1]
        diagName = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', value, 'DiagName'))
        if diagName:
            self.lblAPMKBText.setText(diagName)
        else:
            self.lblAPMKBText.clear()


    def saveData(self):
        return self.checkActualMKB() and self.save()


    def save(self):
        actionId = None
        if self.modelAPActionProperties.action:
            self.modelAPActionProperties.action.getRecord().setValue('MKB', toVariant(self.getAPMKB()))
            actionId = self.modelAPActionProperties.action.save(idx=-1)
        preferences = self.tblAPProps.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CDiagnosisHospitalBedsDialog', preferences)
        return actionId


class CDiagnosisPropertiesTableModel(CActionPropertiesTableModel):
    def __init__(self, parent):
        CActionPropertiesTableModel.__init__(self, parent)


    def setAction(self, action, clientId, clientSex, clientAge, namePropertis, eventTypeId=None):
        self.action = action
        self.clientId = clientId
        self.eventTypeId = eventTypeId
        propertyTypeList = []
        if self.action:
            actionType = action.getType()
            for name, propertyType in actionType._propertiesByName.items():
                if name.lower() in namePropertis:
                    propertyTypeList.append(propertyType)
            propertyTypeList.sort(key=lambda x: (x.idx, x.name))
            self.propertyTypeList = [x for x in propertyTypeList if x.applicable(clientSex, clientAge) and self.visible(x)]
        else:
            self.propertyTypeList = []
        for propertyType in self.propertyTypeList:
            propertyType.shownUp(action, clientId)
        self.updateActionStatusTip()
        self.reset()
