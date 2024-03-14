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
from PyQt4.QtCore import Qt, QDate, pyqtSignature, QVariant, QObject

from library.DialogBase    import CDialogBase
from library.crbcombobox   import CRBComboBox
from library.InDocTable    import CInDocTableModel, CIntInDocTableCol, CRBInDocTableCol
from library.Utils         import forceInt, forceRef, toVariant, forceStringEx, formatRecordsCount
from Quoting.QuotingDialog import CKLADROKATOInDocTableCol, COKATOInDocTableCol
from Quoting.Utils         import getValueFromRecords

from .Ui_RBPlanningHealthResortActivity import Ui_RBPlanningHealthResortActivity


class CPlanningHealthResortActivityModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'HealthResortActivityPlanning', 'id', 'regionCode', parent)
        self.addCol(CIntInDocTableCol(u'Год', 'planYear', 10, low=1900, high=2100).setReadOnly())
        self.addCol(CKLADROKATOInDocTableCol(u'Регион', 'regionCode', 20).setReadOnly())
        self.addCol(COKATOInDocTableCol(u'Район', 'districtCode', 25).setReadOnly())
        self.addCol(CRBInDocTableCol(u'Профиль', 'profile_id', 20, 'rbHospitalBedProfile', showFields = CRBComboBox.showName).setReadOnly())
        self.addCol(CIntInDocTableCol(u'1', 'plan1', 10,  high=100000).setToolTip(u'Январь План'))
        self.addCol(CIntInDocTableCol(u'2', 'plan2', 10,  high=100000).setToolTip(u'Февраль План'))
        self.addCol(CIntInDocTableCol(u'3', 'plan3', 10,  high=100000).setToolTip(u'Март План'))
        self.addCol(CIntInDocTableCol(u'4', 'plan4', 10,  high=100000).setToolTip(u'Апрель План'))
        self.addCol(CIntInDocTableCol(u'5', 'plan5', 10,  high=100000).setToolTip(u'Май План'))
        self.addCol(CIntInDocTableCol(u'6', 'plan6', 10,  high=100000).setToolTip(u'Июнь План'))
        self.addCol(CIntInDocTableCol(u'7', 'plan7', 10,  high=100000).setToolTip(u'Июль План'))
        self.addCol(CIntInDocTableCol(u'8', 'plan8', 10,  high=100000).setToolTip(u'Август План'))
        self.addCol(CIntInDocTableCol(u'9', 'plan9', 10,  high=100000).setToolTip(u'Сентябрь План'))
        self.addCol(CIntInDocTableCol(u'10', 'plan10', 10,  high=100000).setToolTip(u'Октябрь План'))
        self.addCol(CIntInDocTableCol(u'11', 'plan11', 10,  high=100000).setToolTip(u'Ноябрь План'))
        self.addCol(CIntInDocTableCol(u'12', 'plan12', 10,  high=100000).setToolTip(u'Декабрь План'))
        self.dirtyRows = []
        self.deletedRowsId = []
        self.setEnableAppendLine(False)


    def load(self, params):
        if self.dirtyRows:
            res = QtGui.QMessageBox.critical(None,
                        u'Внимание!',
                        u'Данные были изменены.\nСохранить данные?',
                        QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel,
                        QtGui.QMessageBox.Save)
            if res == QtGui.QMessageBox.Save:
                self.saveData()
        cond = []
        db = QtGui.qApp.db
        table = db.table('HealthResortActivityPlanning')
        year = params.get('year',  0)
        if year:
            cond.append(table['planYear'].eq(year))
        region = params.get('region',  0)
        if region:
            cond.append(table['regionCode'].eq(region))
        recordList = db.getRecordList(table, '*',  where=cond, order='planYear, regionCode, districtCode, idx')
        self.setItems(recordList)
        self.dirtyRows = []


    def setData(self, index, value, role=Qt.EditRole):
        if super(CPlanningHealthResortActivityModel, self).setData(index, value, role):
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
            self.dirtyRows = []
        except:
            return False
        return True


    def removeRow(self, row):
        if row >= 0 and row < len(self._items):
            record = self._items[row]
            self.deletedRowsId.append(forceInt(record.value(self._idFieldName)))
            if record in self.dirtyRows:
                self.dirtyRows.remove(record)
            super(CPlanningHealthResortActivityModel, self).removeRow(row)
            eventEditor = QObject.parent(self)
            if eventEditor:
                eventEditor.getRecordsCount()


    def addRecord(self, record):
        self.insertRecord(len(self._items), record)
        self.dirtyRows.append(record)


class CRBPlanningHealthResortActivity(CDialogBase, Ui_RBPlanningHealthResortActivity):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.addModels('Plan', CPlanningHealthResortActivityModel(self))
        self.setModels(self.tblPlan, self.modelPlan, self.selectionModelPlan)
        self.isFirstEntry = True
        self.tblPlan.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblPlan.addPopupSelectAllRow()
        self.tblPlan.addPopupClearSelectionRow()
        self.tblPlan.addPopupDelRow()
        self.setCurrentYear()
        props = QtGui.qApp.preferences.appPrefs
        kladrCode = forceStringEx(props.get('defaultKLADR', '7800000000000'))
        self.cmbRegion.setCurrentIndex(self.cmbRegion.getIndexByCode(kladrCode))
        self.onParamsChanged()
        self.isFirstEntry = False


    def fillDistricts(self):
#        db = QtGui.qApp.db
        cnt = 0
        year = self.edtYear.date().year()
#        region = forceStringEx(self.cmbRegion.itemData(self.cmbRegion.currentIndex()))
        districtItems = self.loadDistrictItems()
        hospitalBedProfileItems = self.loadHospitalBedProfileItems()
        existsItemsCode = getValueFromRecords(self.modelPlan.items(), 'districtCode')
        for item in districtItems:
            okatoCode = forceStringEx(item.value('okatoCode'))
            kladrCode = forceStringEx(item.value('kladrCode')) + '0'*11
            if okatoCode in existsItemsCode:
                continue
            hospitalBedProfileIdList = []
            for profileItem in hospitalBedProfileItems:
                hospitalBedProfileId = forceRef(profileItem.value('profile_id'))
                if hospitalBedProfileId and hospitalBedProfileId not in hospitalBedProfileIdList:
                    hospitalBedProfileIdList.append(hospitalBedProfileId)
                    newRecord = self.modelPlan.getEmptyRecord()
                    newRecord.setValue('idx', QVariant(cnt))
                    newRecord.setValue('planYear', year)
                    newRecord.setValue('regionCode', QVariant(kladrCode))
                    newRecord.setValue('districtCode', QVariant(okatoCode))
                    newRecord.setValue('profile_id', QVariant(hospitalBedProfileId))
                    newRecord.setValue('plan1', QVariant(0))
                    newRecord.setValue('plan2', QVariant(0))
                    newRecord.setValue('plan3', QVariant(0))
                    newRecord.setValue('plan4', QVariant(0))
                    newRecord.setValue('plan5', QVariant(0))
                    newRecord.setValue('plan6', QVariant(0))
                    newRecord.setValue('plan7', QVariant(0))
                    newRecord.setValue('plan8', QVariant(0))
                    newRecord.setValue('plan9', QVariant(0))
                    newRecord.setValue('plan10', QVariant(0))
                    newRecord.setValue('plan11', QVariant(0))
                    newRecord.setValue('plan12', QVariant(0))
                    self.modelPlan.addRecord(newRecord)
                    cnt += 1
        self.modelPlan.reset()
        self.getRecordsCount()


    def loadHospitalBedProfileItems(self):
        db = QtGui.qApp.db
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableHBP = db.table('rbHospitalBedProfile')
        queryTable = tableOSHB.innerJoin(tableHBP, tableHBP['id'].eq(tableOSHB['profile_id']))
        cols = [u'DISTINCT OrgStructure_HospitalBed.profile_id',
                tableHBP['code'],
                tableHBP['name']
               ]
        cond = [tableHBP['usishCode'].isNotNull()]
        return db.getRecordList(queryTable, cols, cond, [tableHBP['name'].name()])


    def loadDistrictItems(self):
        filterCode = forceStringEx(QtGui.qApp.db.translate('kladr.KLADR', 'CODE', forceStringEx(self.cmbRegion.itemData(self.cmbRegion.currentIndex())), 'OCATD'))[:2] if self.cmbRegion.currentIndex() else ''
        db = QtGui.qApp.db
        queryTable = 'kladr.KLADR INNER JOIN kladr.OKATO ON kladr.OKATO.P0=LEFT(kladr.KLADR.OCATD, 2)'
        return db.getRecordList(queryTable, 'DISTINCT kladr.OKATO.CODE AS okatoCode, LEFT(kladr.KLADR.CODE, 2) AS kladrCode',
                                       '%skladr.OKATO.P1 != \'\' AND kladr.OKATO.P2 = \'\'' % (('kladr.OKATO.P0=\'%s\' AND '%(filterCode)) if filterCode else ''),
                                       'kladr.OKATO.NAME, kladr.OKATO.P0, kladr.OKATO.infis, kladr.OKATO.CODE')


    def saveData(self):
        result =  self.modelPlan.saveData()
        if not result:
            QtGui.QMessageBox.critical(self,
                        u'Внимание!',
                        u'Ошибка при сохранении.',
                        QtGui.QMessageBox.Ok,
                        QtGui.QMessageBox.Ok)
        return result


    def onParamsChanged(self):
        params = {}
        params['year'] = self.edtYear.date().year()
        params['region'] = forceStringEx(self.cmbRegion.itemData(self.cmbRegion.currentIndex()))
        self.modelPlan.load(params)
        self.getRecordsCount()


    def getRecordsCount(self):
        if self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tabDistrict):
            self.lblCount.setText(formatRecordsCount(self.modelPlan.realRowCount()))
        else:
            self.lblCount.setText(formatRecordsCount(0))


    def setCurrentYear(self):
        currentDate = QDate.currentDate()
        if currentDate:
            self.edtYear.setDate(currentDate)
        else:
            self.edtYear.setDate(QDate())


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, widgetIndex):
        if widgetIndex == self.tabWidget.indexOf(self.tabDistrict):
            self.lblCount.setText(formatRecordsCount(self.modelPlan.realRowCount()))
        else:
            self.lblCount.setText(formatRecordsCount(0))


    @pyqtSignature('')
    def on_btnFillDistricts_clicked(self):
        self.fillDistricts()


    @pyqtSignature('QDate')
    def on_edtYear_dateChanged(self, date):
        if not self.isFirstEntry:
            self.onParamsChanged()


    @pyqtSignature('int')
    def on_cmbRegion_currentIndexChanged(self, index):
        if not self.isFirstEntry:
            self.onParamsChanged()

