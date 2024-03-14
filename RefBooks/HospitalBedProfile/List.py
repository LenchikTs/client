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

from library.InDocTable import CInDocTableCol
from library.interchange     import getLineEditValue, getRBComboBoxValue, setLineEditValue, setRBComboBoxValue, setDateEditValue, getDateEditValue
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CRefBookCol, CTextCol, CDateCol
from library.Utils           import exceptionToUnicode, forceDate, forceRef, forceString

from .Ui_RBHospitalBedProfileEditor import Ui_ItemEditorDialog


class CRBHospitalBedProfileList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',              ['code'], 20),
#            CTextCol(u'Региональный код', ['regionalCode'], 20),
            CTextCol(u'Код ЕГИСЗ',        ['usishCode'], 20),
            CTextCol(u'Наименование',     ['name'], 40),
            CRefBookCol(u'Сервис ОМС',    ['service_id'], 'rbService', 10),
            CRefBookCol(u'Профиль медицинской помощи',   ['medicalAidProfile_id'], 'rbMedicalAidProfile', 10),
            CDateCol(   u'Дата закрытия', ['endDate'], 10),
            ], 'rbHospitalBedProfile', ['code', 'name', 'id'])
        self.setWindowTitleEx(u'Профили коек')


    def getItemEditor(self):
        return CRBHospitalBedProfileEditor(self)


class CRBHospitalBedProfileEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbHospitalBedProfile')
        self.setWindowTitleEx(u'Профиль койки')
        self.cmbService.setTable('rbService', True)
        self.cmbService.setCurrentIndex(0)
        self.cmbMedicalAidProfile.setTable('rbMedicalAidProfile', True)
        self.cmbMedicalAidProfile.setCurrentIndex(0)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(   self.edtCode,              record, 'code')
        setLineEditValue(   self.edtRegionalCode,      record, 'regionalCode')
        setLineEditValue(   self.edtName,              record, 'name')
        setRBComboBoxValue( self.cmbService,           record, 'service_id')
        setRBComboBoxValue( self.cmbMedicalAidProfile, record, 'medicalAidProfile_id')
        setLineEditValue(   self.edtEmsProfileCode,    record, 'emsProfileCode')
        setLineEditValue(   self.edtUsishCode,         record, 'usishCode')
        setLineEditValue(   self.edtTfomsCode,         record, 'tfomsCode')
        setDateEditValue(   self.edtEndDate,           record, 'endDate')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(   self.edtCode,              record, 'code')
        getLineEditValue(   self.edtRegionalCode,      record, 'regionalCode')
        getLineEditValue(   self.edtName,              record, 'name')
        getRBComboBoxValue( self.cmbService,           record, 'service_id')
        getRBComboBoxValue( self.cmbMedicalAidProfile, record, 'medicalAidProfile_id')
        getLineEditValue(   self.edtEmsProfileCode,    record, 'emsProfileCode')
        getLineEditValue(   self.edtUsishCode,         record, 'usishCode')
        getLineEditValue(   self.edtTfomsCode,         record, 'tfomsCode')
        getDateEditValue(   self.edtEndDate,           record, 'endDate')
        return record


    def checkEndDate(self, endDate, profileId):
        db = QtGui.qApp.db
        bedIdList = []
        orgStructureIdList = []
        orgStructureList = u''
        tableOS = db.table('OrgStructure')
        tableOSHB = db.table('OrgStructure_HospitalBed')
        queryTable = tableOS.innerJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
        cond = [tableOS['deleted'].eq(0),
                tableOSHB['profile_id'].eq(profileId),
                tableOSHB['endDate'].isNull()
                ]
        cols = [tableOS['id'].alias('orgStructureId'),
                tableOS['code'],
                tableOS['name'],
                tableOSHB['id'].alias('bedId')
                ]
        order = [tableOS['code'].name(),
                 tableOS['name'].name()
                ]
        records = db.getRecordList(queryTable, cols, cond, order)
        for record in records:
            bedId = forceRef(record.value('bedId'))
            if bedId and bedId not in bedIdList:
                bedIdList.append(bedId)
            orgStructureId = forceRef(record.value('orgStructureId'))
            if orgStructureId and orgStructureId not in orgStructureIdList:
                orgStructureIdList.append(orgStructureId)
                code = forceString(record.value('code'))
                name = forceString(record.value('name'))
                orgStructureList += code + u'-' + name + u'\n'
        if bedIdList:
            res = QtGui.QMessageBox.warning( self,
                                    u'Внимание!',
                                    u'''В подразделениях:\n %s присутствуют открытые койки с данным профилем. Закрыть койки?'''%(orgStructureList),
                                    QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                    QtGui.QMessageBox.Cancel)
            if res == QtGui.QMessageBox.Cancel:
                self.setFocusToWidget(self.edtEndDate)
                return False, []
        return True, bedIdList


    def checkDataEntered(self):
        result = True
        bedIdList = []
        endDate = self.edtEndDate.date()
        profileId = self.itemId()
        if endDate and profileId:
            result, bedIdList = self.checkEndDate(endDate, profileId)
        return result, bedIdList


    def saveData(self):
        result, bedIdList = self.checkDataEntered()
        return result and self.save(bedIdList)


    def save(self, bedIdList):
        try:
            prevId = self.itemId()
            db = QtGui.qApp.db
            db.transaction()
            try:
                record = self.getRecord()
                id = db.insertOrUpdate(db.table(self._tableName), record)
                self.saveInternals(id)
                endDate = forceDate(record.value('endDate'))
                if bedIdList and endDate:
                    tableOSHB = db.table('OrgStructure_HospitalBed')
                    db.updateRecords(tableOSHB.name(), tableOSHB['endDate'].eq(endDate), tableOSHB['id'].inlist(bedIdList))
                db.commit()
            except:
                db.rollback()
                self.setItemId(prevId)
                raise
            self.setItemId(id)
            self.afterSave()
            return id
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)
            return None

