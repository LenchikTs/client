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

from PyQt4.QtCore       import pyqtSignature

from library.DialogBase import CDialogBase
from Orgs.Orgs          import selectOrganisation
from Orgs.OrgComboBox   import CPolyclinicComboBox

from Registry.Ui_ReferralEditDialog import Ui_ReferralEditDialog


class CReferral:
    def __init__(self):
        self.srcOrgId  = None
        self.srcPerson = ''
        self.srcSpecialityId = None
        self.srcNumber = ''
        self.srcDate   = None



def inputReferral(widget):
    dlg = CReferralEditDialog(widget)
    if dlg.exec_():
        return dlg.getReferral()
    return None


class CReferralEditDialog(Ui_ReferralEditDialog, CDialogBase):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbSrcSpeciality.setTable('rbSpeciality')
        self.setupDirtyCather()


#    def setRecord(self, record):
#        CItemEditorBaseDialog.setRecord(self,     record)
#        getRBComboBoxValue(self.cmbSrcOrg,        record, 'srcOrg_id')
#        setLineEditValue(  self.edtSrcPerson,     record, 'srcPerson')
#        getRBComboBoxValue(self.cmbSrcSpeciality, record, 'srcSpeciality_id')
#        setLineEditValue(  self.edtSrcNumber,     record, 'srcNumber')
#        setDateEditValue(  self.edtSrcDate,       record, 'srcDate')
#        self.setIsDirty(False)


    def setReferral(self, referral):
        self.cmbSrcOrg.setValue(referral.srcOrgId)
        self.edtSrcPerson.setText(referral.srcPerson)
        self.cmbSrcSpeciality.setValue(referral.srcSpecialityId)
        self.edtSrcNumber.setText(referral.srcNumber)
        self.edtSrcDate.setDate(referral.srcDate)
        self.setIsDirty(False)


    def saveData(self):
        return self.checkDataEntered()


    def checkDataEntered(self):
        result = True
        result = result and (self.cmbSrcOrg.value()   or self.checkInputMessage(u'ЛПУ',   False, self.cmbSrcOrg))
        result = result and (self.edtSrcPerson.text() or self.checkInputMessage(u'врача', True, self.edtSrcPerson))
        result = result and (self.cmbSrcSpeciality.value() or self.checkInputMessage(u'специальность врача', True, self.cmbSrcSpeciality))
        result = result and (self.edtSrcNumber.text() or self.checkInputMessage(u'номер', False, self.edtSrcNumber))
        result = result and (self.edtSrcDate.date()   or self.checkInputMessage(u'дату',  False, self.edtSrcNumber))
        return result


#    def getRecord(self):
#        record = CItemEditorBaseDialog.getRecord(self)
#        getRBComboBoxValue(self.cmbSrcOrg,        record, 'srcOrg_id')
#        getLineEditValue(  self.edtSrcPerson,     record, 'srcPerson')
#        getRBComboBoxValue(self.cmbSrcSpeciality, record, 'srcSpeciality_id')
#        getLineEditValue(  self.edtSrcNumber,     record, 'srcNumber')
#        getDateEditValue(  self.edtSrcDate,       record, 'srcDate')
#        return record



    def getReferral(self):
        result = CReferral()
        result.srcOrgId  = self.cmbSrcOrg.value()
        result.srcPerson = unicode(self.edtSrcPerson.text())
        result.srcSpecialityId = self.cmbSrcSpeciality.value()
        result.srcNumber = unicode(self.edtSrcNumber.text())
        result.srcDate   = self.edtSrcDate.date()
        return result


    @pyqtSignature('')
    def on_btnSelectSrcOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbSrcOrg.value(), False, filter=CPolyclinicComboBox.filter)
        self.cmbSrcOrg.updateModel()
        if orgId:
            self.cmbSrcOrg.setValue(orgId)

