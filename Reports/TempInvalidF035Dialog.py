# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore       import pyqtSignature

from library.Utils      import forceString, trim
from library.DialogBase import CDialogBase

from Reports.Ui_TempInvalidF035Setup import Ui_TempInvalidF035Dialog


class CTempInvalidF035Dialog(CDialogBase, Ui_TempInvalidF035Dialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        flatCode = [u'inspection_disability%', u'inspection_case%']
        self.cmbFilterExpertExpertiseTypeMC.clearValue()
        self.cmbFilterExpertExpertiseTypeMC.clear()
        self.cmbFilterExpertExpertiseTypeMC.setTable('ActionType', False, filter="(flatCode LIKE '%s') OR (flatCode LIKE '%s')"%(flatCode[0], flatCode[1]))
        self.cmbFilterExpertSpecialityMC.setTable('rbSpeciality', True)
        self.cmbFilterExpertExpertiseCharacterMC.setTable('rbMedicalBoardExpertiseCharacter', False, filter='class = 0')


    @pyqtSignature('int')
    def on_cmbFilterExpertExpertiseCharacterMC_currentIndexChanged(self, index):
        self.cmbFilterExpertExpertiseKindMC.setTable('rbMedicalBoardExpertiseKind', False, filter='expertiseCharacter_id=%s'%(self.cmbFilterExpertExpertiseCharacterMC.value()))
        self.cmbFilterExpertExpertiseObjectMC.setTable('rbMedicalBoardExpertiseObject', False, filter='expertiseCharacter_id=%s'%(self.cmbFilterExpertExpertiseCharacterMC.value()))
        self.cmbFilterExpertExpertiseArgumentMC.setTable('rbMedicalBoardExpertiseArgument', False, filter='expertiseCharacter_id=%s'%(self.cmbFilterExpertExpertiseCharacterMC.value()))


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.chkFilterExpertExpertiseTypeMC.setChecked(params.get('expertiseTypeChk', False))
        self.chkFilterExpertSetPersonMC.setChecked(params.get('setPersonChk', False))
        self.chkFilterExpertOrgStructMC.setChecked(params.get('expertOrgStructureChk', False))
        self.chkFilterExecDateMC.setChecked(params.get('execDateChk', False))
        self.chkFilterExpertSpecialityMC.setChecked(params.get('expertSpecialityChk', False))
        self.chkFilterExpertMKBMC.setChecked(params.get('MKBChk', False))
        self.chkFilterExpertClosedMC.setChecked(params.get('actionStatusChk', False))
        self.chkFilterExpertExpertiseCharacterMC.setChecked(params.get('expertiseCharacterChk', False))
        self.chkFilterExpertExpertiseKindMC.setChecked(params.get('expertiseKindChk', False))
        self.ghkFilterExpertExpertiseObjectMC.setChecked(params.get('expertiseObjectChk', False))
        self.chkFilterExpertExpertiseArgumentMC.setChecked(params.get('expertiseArgumentChk', False))
        self.chkExpertIdMC.setChecked(params.get('expertChk', False))
        expertiseTypeIdList, expertiseTypeMCCurrentText = params.get('expertiseTypeId', ([], u''))
        self.cmbFilterExpertExpertiseTypeMC.setValue(expertiseTypeIdList)
        self.cmbFilterExpertSetPersonMC.setValue(params.get('setPersonId', None))
        self.cmbFilterExpertOrgStructMC.setValue(params.get('expertOrgStructureId', None))
        self.edtFilterBegExecDateMC.setDate(params.get('begExecDate', None))
        self.edtFilterEndExecDateMC.setDate(params.get('endExecDate', None))
        self.cmbFilterExpertSpecialityMC.setValue(params.get('expertSpecialityId', None))
        self.edtFilterExpertBegMKBMC.setText(params.get('begMKB', u''))
        self.edtFilterExpertEndMKBMC.setText(params.get('endMKB', u''))
        self.cmbFilterExpertClosedMC.setValue(params.get('actionStatus', 0))
        self.cmbFilterExpertExpertiseCharacterMC.setValue(params.get('expertiseCharacterId', None))
        characterMCIndex = self.cmbFilterExpertExpertiseCharacterMC.currentIndex()
        if characterMCIndex >= 0:
            self.on_cmbFilterExpertExpertiseCharacterMC_currentIndexChanged(characterMCIndex)
            self.cmbFilterExpertExpertiseKindMC.setValue(params.get('expertiseKindId', None))
            self.cmbFilterExpertExpertiseObjectMC.setValue(params.get('expertiseObjectId', None))
            self.cmbFilterExpertExpertiseArgumentMC.setValue(params.get('expertiseArgumentId', None))
        self.cmbExpertIdMC.setValue(params.get('expertId', None))
        self.edtCntUser.setValue(params.get('cntUser', 1))
        self.chkRegAddress.setChecked(params.get('isRegAddress', 1))
        self.chkNumberPolicy.setChecked(params.get('isNumberPolicy', 0))
        self.chkClientId.setChecked(params.get('isClientId', 0))


    def params(self):
        result = {}
        if self.chkFilterExpertExpertiseTypeMC.isChecked():
            expertiseTypeIdList = []
            expertiseTypeStr = self.cmbFilterExpertExpertiseTypeMC.value().split(',')
            for expertiseType in expertiseTypeStr:
                expertiseTypeId = trim(expertiseType)
                if expertiseTypeId and expertiseTypeId not in expertiseTypeIdList:
                    expertiseTypeIdList.append(expertiseTypeId)
            result['expertiseTypeId'] = (expertiseTypeIdList, forceString(self.cmbFilterExpertExpertiseTypeMC.currentText()))
            result['expertiseTypeChk'] = self.chkFilterExpertExpertiseTypeMC.isChecked()
        if self.chkFilterExpertSetPersonMC.isChecked():
            result['setPersonId'] = self.cmbFilterExpertSetPersonMC.value()
            result['setPersonChk'] = self.chkFilterExpertSetPersonMC.isChecked()
        if self.chkFilterExpertOrgStructMC.isChecked():
            result['expertOrgStructureId'] = self.cmbFilterExpertOrgStructMC.value()
            result['expertOrgStructureChk'] = self.chkFilterExpertOrgStructMC.isChecked()
        if self.chkFilterExecDateMC.isChecked():
            result['begExecDate'] = self.edtFilterBegExecDateMC.date()
            result['endExecDate'] = self.edtFilterEndExecDateMC.date()
            result['execDateChk'] = self.chkFilterExecDateMC.isChecked()
        if self.chkFilterExpertSpecialityMC.isChecked():
            result['expertSpecialityId'] = self.cmbFilterExpertSpecialityMC.value()
            result['expertSpecialityChk'] = self.chkFilterExpertSpecialityMC.isChecked()
        if self.chkFilterExpertMKBMC.isChecked():
            result['begMKB'] = unicode(self.edtFilterExpertBegMKBMC.text())
            result['endMKB'] = unicode(self.edtFilterExpertEndMKBMC.text())
            result['MKBChk'] = self.chkFilterExpertMKBMC.isChecked()
        if self.chkFilterExpertClosedMC.isChecked():
            result['actionStatus'] = self.cmbFilterExpertClosedMC.value()
            result['actionStatusChk'] = self.chkFilterExpertClosedMC.isChecked()
        if self.chkFilterExpertExpertiseCharacterMC.isChecked():
            result['expertiseCharacterId'] = self.cmbFilterExpertExpertiseCharacterMC.value()
            result['expertiseCharacterChk'] = self.chkFilterExpertExpertiseCharacterMC.isChecked()
        characterMCIndex = self.cmbFilterExpertExpertiseCharacterMC.currentIndex()
        if characterMCIndex >= 0:
            if self.chkFilterExpertExpertiseKindMC.isChecked():
                result['expertiseKindId'] = self.cmbFilterExpertExpertiseKindMC.value()
                result['expertiseKindChk'] = self.chkFilterExpertExpertiseKindMC.isChecked()
            if self.ghkFilterExpertExpertiseObjectMC.isChecked():
                result['expertiseObjectId'] = self.cmbFilterExpertExpertiseObjectMC.value()
                result['expertiseObjectChk'] = self.ghkFilterExpertExpertiseObjectMC.isChecked()
            if self.chkFilterExpertExpertiseArgumentMC.isChecked():
                result['expertiseArgumentId'] = self.cmbFilterExpertExpertiseArgumentMC.value()
                result['expertiseArgumentChk'] = self.chkFilterExpertExpertiseArgumentMC.isChecked()
        if self.chkExpertIdMC.isChecked():
            result['expertId'] = self.cmbExpertIdMC.value()
            result['expertChk'] = self.chkExpertIdMC.isChecked()
        result['cntUser'] = self.edtCntUser.value()
        result['isRegAddress'] = self.chkRegAddress.isChecked()
        result['isNumberPolicy'] = self.chkNumberPolicy.isChecked()
        result['isClientId'] = self.chkClientId.isChecked()
        return result

