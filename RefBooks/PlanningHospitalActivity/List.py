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
#WTF? 
# - называется чёрти-как,
# - находтися чёрти-где
# - левая, неудобная структура

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, pyqtSignature

from library.DialogBase      import CDialogBase
from library.InDocTable      import CInDocTableModel, CIntInDocTableCol, CRBInDocTableCol
from library.Utils           import forceInt, toVariant

from .Ui_RBPlanningHospitalActivity import Ui_RBPlanningHospitalActivityDialog


class CPlanningHospitalActivityModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'OrgStructure_Planning', 'id', 'orgStructure_id', parent)
        self.addCol(CIntInDocTableCol(u'Год', 'year', 6, low=1900, high=2100).setReadOnly())
        self.addCol(CRBInDocTableCol(u'Подразделение', 'orgStructure_id',  20, 'OrgStructure', addNone=False).setReadOnly())
        self.addCol(CRBInDocTableCol(u'Профиль', 'profile_id',  20, 'rbHospitalBedProfile').setReadOnly())
        self.addCol(CIntInDocTableCol(u'1 п', 'plan1', 5,  high=100000).setToolTip(u'Январь План')) # вот говно-то...
        self.addCol(CIntInDocTableCol(u'1 к', 'bedDays1', 5,  high=100000).setToolTip(u'Январь Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'2 п', 'plan2', 5,  high=100000).setToolTip(u'Февраль План'))
        self.addCol(CIntInDocTableCol(u'2 к', 'bedDays2', 5,  high=100000).setToolTip(u'Февраль Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'3 п', 'plan3', 5,  high=100000).setToolTip(u'Март План'))
        self.addCol(CIntInDocTableCol(u'3 к', 'bedDays3', 5,  high=100000).setToolTip(u'Март Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'4 п', 'plan4', 5,  high=100000).setToolTip(u'Апрель План'))
        self.addCol(CIntInDocTableCol(u'4 к', 'bedDays4', 5,  high=100000).setToolTip(u'Апрель Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'5 п', 'plan5', 5,  high=100000).setToolTip(u'Май План'))
        self.addCol(CIntInDocTableCol(u'5 к', 'bedDays5', 5,  high=100000).setToolTip(u'Май Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'6 п', 'plan6', 5,  high=100000).setToolTip(u'Июнь План'))
        self.addCol(CIntInDocTableCol(u'6 к', 'bedDays6', 5,  high=100000).setToolTip(u'Июнь Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'7 п', 'plan7', 5,  high=100000).setToolTip(u'Июль План'))
        self.addCol(CIntInDocTableCol(u'7 к', 'bedDays7', 5,  high=100000).setToolTip(u'Июль Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'8 п', 'plan8', 5,  high=100000).setToolTip(u'Август План'))
        self.addCol(CIntInDocTableCol(u'8 к', 'bedDays8', 5,  high=100000).setToolTip(u'Август Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'9 п', 'plan9', 5,  high=100000).setToolTip(u'Сентябрь План'))
        self.addCol(CIntInDocTableCol(u'9 к', 'bedDays9', 5,  high=100000).setToolTip(u'Сентябрь Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'10 п', 'plan10', 5,  high=100000).setToolTip(u'Октябрь План'))
        self.addCol(CIntInDocTableCol(u'10 к', 'bedDays10', 5,  high=100000).setToolTip(u'Октябрь Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'11 п', 'plan11', 5,  high=100000).setToolTip(u'Ноябрь План'))
        self.addCol(CIntInDocTableCol(u'11 к', 'bedDays11', 5,  high=100000).setToolTip(u'Ноябрь Койко-Дни'))
        self.addCol(CIntInDocTableCol(u'12 п', 'plan12', 5,  high=100000).setToolTip(u'Декабрь План'))
        self.addCol(CIntInDocTableCol(u'12 к', 'bedDays12', 5,  high=100000).setToolTip(u'Декабрь Койко-Дни'))

        self.dirtyRows = []
        self.deletedRowsId = []
        self.setEnableAppendLine(False)


    def load(self, params):
        self.saveData()
        cond = []
        db = QtGui.qApp.db
        table = db.table('OrgStructure_Planning')
        dateYear = params.get('year',  QDate())
        year = dateYear.year() if dateYear else 0
        chkYear = params.get('chkYear', 0)
        orgStructureId = params.get('orgStructure', None)
        orgStructureIdList = params.get('orgStructureIdList', None)
        chkOrgStr = params.get('chkOrgStructure', 0)
        hospitalBedProfileId = params.get('hospitalBedProfileId', None)
        chkHospitalBedProfile = params.get('chkProfileBed', 0)
        if year and chkYear:
            cond.append(table['year'].eq(year))
        if orgStructureId and chkOrgStr:
            cond.append(table['orgStructure_id'].inlist(orgStructureIdList))
        if hospitalBedProfileId and chkHospitalBedProfile:
            cond.append(table['profile_id'].eq(hospitalBedProfileId))
        recordList = db.getRecordList(table, '*',  where=cond, order='year, orgStructure_id, profile_id')
        self.setItems(recordList)


    def setData(self, index, value, role=Qt.EditRole):
        if super(CPlanningHospitalActivityModel, self).setData(index, value, role):
            record = self._items[index.row()]
            if record not in self.dirtyRows:
                self.dirtyRows.append(record)


    def saveData(self):
        try:
            db = QtGui.qApp.db
            table = self._table
            idFieldName = self._idFieldName
            if self.dirtyRows:
                for record in self.dirtyRows:
                    if self._extColsPresent:
                        outRecord = self.removeExtCols(record)
                    else:
                        outRecord = record
                    id = db.insertOrUpdate(table, outRecord)
                    record.setValue(idFieldName, toVariant(id))
            if self.deletedRowsId:
                filter = [table[idFieldName].inlist(self.deletedRowsId)]
                db.deleteRecord(table, filter)
        except:
            return False
        return True


    def removeRow(self, row):
        if row >= 0 and row < len(self._items):
            record = self._items[row]
            self.deletedRowsId.append(forceInt(record.value(self._idFieldName)))
            if record in self.dirtyRows:
                self.dirtyRows.remove(record)
            super(CPlanningHospitalActivityModel, self).removeRow(row)

    def addRecord(self, record):
        self.insertRecord(len(self._items), record)
        self.dirtyRows.append(record)


class CRBPlanningHospitalActivityList(CDialogBase, Ui_RBPlanningHospitalActivityDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.addModels('', CPlanningHospitalActivityModel(parent))
        self.setModels(self.tblItems, self.model, self.selectionModel)
        self.prepareView()
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', addNone=True, order='code')
        self.setCurrentYear()
        self.onParamsChanged()


    def prepareView(self):
        self.tblItems.setTabLeftBorder(3)
        #self.actAddRows = QtGui.QAction(u'Заполнить отделения на указанный год', self)
        #self.actAddRows.setObjectName('actAddRows')
        #self.connect(self.actAddRows, SIGNAL('triggered()'), self.on_actAddRows)
        #self.tblItems.addPopupAction(self.actAddRows)
        self.tblItems.addPopupDelRow()


    def saveData(self):
        result =  self.model.saveData()
        if not result:
            QtGui.QMessageBox.critical(self,
                        u'Внимание!',
                        u'Ошибка при сохранении.',
                        QtGui.QMessageBox.Ok,
                        QtGui.QMessageBox.Ok)
        return result


    def onParamsChanged(self):
        params = {
            'chkYear' : self.chkYear.isChecked(),
            'chkOrgStructure' : self.chkOrgStructure.isChecked(),
            'chkProfileBed' : self.chkProfilBed.isChecked()
        }
        if self.chkYear.isChecked():
            params['year'] = self.edtYear.date()
        if  self.chkOrgStructure.isChecked():
            params['orgStructure'] = self.cmbOrgStructure.value()
            orgStructureIndex = self.cmbOrgStructure._model.index(self.cmbOrgStructure.currentIndex(), 0, self.cmbOrgStructure.rootModelIndex())
            params['orgStructureIdList'] = self.getOrgStructureIdList(orgStructureIndex)
        if self.chkProfilBed.isChecked():
            params['hospitalBedProfileId'] = self.cmbHospitalBedProfile.value()
        self.model.load(params)


    def setCurrentYear(self):
        currentDate = QDate.currentDate()
        if currentDate:
            self.edtYear.setDate(currentDate)
        else:
            self.edtYear.setDate(QDate())


    def getOrgStructureIdList(self, treeIndex):
        if treeIndex:
            treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
            return treeItem.getItemIdList() if treeItem else []
        else:
            return []


    @pyqtSignature('')
    def on_btnFill_clicked(self):
        year = self.edtYear.date()
        db = QtGui.qApp.db
        tableOS = db.table('OrgStructure')
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableHBP = db.table('rbHospitalBedProfile')

        table = tableOS.leftJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
        table = table.leftJoin(tableHBP, tableHBP['id'].eq(tableOSHB['profile_id']))
        cond = [
            tableOS['deleted'].eq(0),
            tableOSHB['id'].ne(0),
            db.joinOr([tableOSHB['endDate'].isNull(), tableOSHB['endDate'].dateGe(year)])
        ]
        cols = 'OrgStructure.id, rbHospitalBedProfile.id'
        group = 'rbHospitalBedProfile.id, OrgStructure.id'
        order = 'OrgStructure.name, rbHospitalBedProfile.name'
        recordList = db.getRecordListGroupBy(table, cols, cond, group, order)

        idList = []
        for record in self.model.items():
            orgId = forceInt(record.value('orgStructure_id'))
            profileId = forceInt(record.value('profile_id'))
            idList.append((orgId, profileId))

        for record in recordList:
            orgId = record.value(0)
            profileId = record.value(1)
            if (orgId, profileId) not in idList:
                newRecord = self.model.getEmptyRecord()
                newRecord.setValue('year', year.year())
                newRecord.setValue('orgStructure_id', record.value(0))
                newRecord.setValue('profile_id', record.value(1))
                self.model.addRecord(newRecord)


    @pyqtSignature('bool')
    def on_chkYear_toggled(self, checked):
        self.edtYear.setEnabled(checked)
        self.onParamsChanged()


    @pyqtSignature('bool')
    def on_chkOrgStructure_toggled(self, checked):
        self.cmbOrgStructure.setEnabled(checked)
        if not checked:
            self.chkProfilBed.setChecked(checked)
            self.cmbHospitalBedProfile.setEnabled(checked)
        self.onParamsChanged()


    @pyqtSignature('bool')
    def on_chkProfilBed_toggled(self, checked):
        self.cmbHospitalBedProfile.setEnabled(checked)
        self.onParamsChanged()


    @pyqtSignature('QDate')
    def on_edtYear_dateChanged(self, date):
        self.onParamsChanged()


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureIdList = []
        curOrgStructureId = self.cmbOrgStructure.value()
        if curOrgStructureId:
            orgStructureIndex = self.cmbOrgStructure._model.index(self.cmbOrgStructure.currentIndex(), 0, self.cmbOrgStructure.rootModelIndex())
            orgStructureIdList = self.getOrgStructureIdList(orgStructureIndex)
        if orgStructureIdList:
            db = QtGui.qApp.db
            table = db.table('vHospitalBed')
            profileBedIdList = db.getDistinctIdList(table, [table['profile_id']], [table['master_id'].inlist(orgStructureIdList)])
            selFilter = u'id IN (%s)'%(u', '.join(str(hospitalBedProfileId) for hospitalBedProfileId in profileBedIdList if hospitalBedProfileId))
        else:
            selFilter=''
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', addNone=True, filter=selFilter, order='code')
        self.onParamsChanged()
