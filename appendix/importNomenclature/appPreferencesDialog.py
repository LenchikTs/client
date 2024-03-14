# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным ,обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Диалог настроек программы"""

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant, pyqtSignature, QDir

from Orgs.Orgs import selectOrganisation
from library.Utils import (forceBool, toVariant, forceString, forceInt,
                           forceStringEx, forceRef)

from Ui_appPreferencesDialog import Ui_appPreferencesDialog


class CAppPreferencesDialog(QtGui.QDialog, Ui_appPreferencesDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def props(self):
        result = {}
        result['logErrors'] = toVariant(self.chkLogErrors.isChecked())
        result['logSuccess'] = toVariant(self.chkLogSuccess.isChecked())
        result['createNomenclatureDuringImport'] = toVariant(
            self.chkCreateNomenclatureDuringImport.isChecked())
        result['autoImport'] = toVariant(self.chkAutoImport.isChecked())
        result['autoImportScanDir'] = toVariant(self.edtScanDir.text())
        result['autoImportScanPeriod'] = toVariant(self.edtScanPeriod.value())
        result['orgId'] = toVariant(self.cmbOrganisation.value())
        return result


    def setProps(self, props):
        self.chkLogErrors.setChecked(forceBool(props.get(
            'logErrors', QVariant())))
        self.chkLogSuccess.setChecked(forceBool(props.get(
            'logSuccess', QVariant())))
        self.chkCreateNomenclatureDuringImport.setChecked(forceBool(props.get(
            'createNomenclatureDuringImport', QVariant())))
        self.chkAutoImport.setChecked(forceBool(props.get('autoImport', False)))
        self.edtScanDir.setText(forceString(props.get('autoImportScanDir', '')))
        self.edtScanPeriod.setValue(forceInt(props.get(
            'autoImportScanPeriod', 100)))
        self.updateAutoImportControls(self.chkAutoImport.isChecked())
        self.cmbOrganisation.setValue(forceRef(props.get('orgId', None)))


    @pyqtSignature('bool')
    def on_chkAutoImport_clicked(self, checked):
        self.updateAutoImportControls(checked)


    @pyqtSignature('')
    def on_btnSelectScanDir_clicked(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self, u'Выберите директорий для отслеживания',
            forceStringEx(self.edtScanDir.text()),
            QtGui.QFileDialog.ShowDirsOnly)
        if forceString(path):
            self.edtScanDir.setText(QDir.toNativeSeparators(path))


    @pyqtSignature('')
    def on_btnSelectOrganisation_clicked(self):
        orgId = selectOrganisation(self, self.cmbOrganisation.value(), False)
        self.cmbOrganisation.updateModel()
        if orgId:
            self.cmbOrganisation.setValue(orgId)


    def updateAutoImportControls(self, val):
        for widget in (self.edtScanDir, self.lblScanDir, self.btnSelectScanDir,
                       self.lblScanPeriod, self.edtScanPeriod):
            widget.setEnabled(val)

# ******************************************************************************
