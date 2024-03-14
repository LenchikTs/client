# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                    import QtGui
from PyQt4.QtCore             import Qt, pyqtSignature, QVariant, QModelIndex, QAbstractTableModel, SIGNAL, QRegExp, QDateTime

from library.DialogBase       import CDialogBase
from library.PreferencesMixin import CDialogPreferencesMixin
from library.SortFilterProxyTableModel import CSortFilterProxyTableModel
from Stock.Utils              import getExistsNomenclatureIdList
from library.Utils            import getPref, setPref, addDots, forceStringEx, forceInt, forceRef, toVariant

from library.ESKLP.Ui_SmnnGrlsLfNomenclatureExpenseEditorEx import Ui_SmnnGrlsLfNomenclatureExpenseEditorEx


class CSmnnGrlsLfNomenclatureExpenseEditorEx(CDialogBase, Ui_SmnnGrlsLfNomenclatureExpenseEditorEx, CDialogPreferencesMixin):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('', CSmnnTableModel(self))
        self.addModels('SmnnSortModel', CSortFilterProxyTableModel(self, self.model))
        self.model = self.modelSmnnSortModel.sourceModel()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblSmnn, self.modelSmnnSortModel, self.selectionModelSmnnSortModel)
        self.isType = 0
        self.UUID = None
        self._isOnlySmnnUUID = False
        self._smnnUUID = None
        self.lfFormId = None
        self.nomenclatureId = None
        self.nomenclatureIdList = []
        self.existsNomenclatureIdList = []
        self.financeId = None
        self.medicalAidKindId = None
        self.orgStructureId = None
        self.defaultOnlyExists = False
        self.setBegDate(None)
        self.setEndDate(None)
        self.tblSmnn.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CSmnnGrlsLfNomenclatureExpenseEditor', {})
        self.tblSmnn.loadPreferences(preferences)
        rX = QRegExp(u"[-?!,.А-Яа-яёЁA-Za-z\\d\\s]+")
        self.edtFindSmnnName.setValidator(QtGui.QRegExpValidator(rX, self))
        self.edtFindGrlsLfName.setValidator(QtGui.QRegExpValidator(rX, self))
        self.loadDialogPreferences()


    def closeEvent(self, event):
        preferences = self.tblSmnn.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CSmnnGrlsLfNomenclatureExpenseEditor', preferences)
        CDialogBase.closeEvent(self, event)


    def existsNomenclatureIdList(self, existsNomenclatureIdList):
        self.existsNomenclatureIdList = existsNomenclatureIdList


    def setFinanceId(self, value):
        self.financeId = value


    def setMedicalAidKindId(self, value):
        self.medicalAidKindId = value


    def getFinanceId(self):
        return self.financeId


    def getMedicalAidKindId(self):
        return self.medicalAidKindId


    def setOnlyExistsEnabled(self, value=True):
        self.chkOnlyExists.setEnabled(value)


    def setOnlyExists(self, value):
        self.defaultOnlyExists = value
        self.chkOnlyExists.setChecked(value)


    def setOnlySmnnUUID(self, value):
        self._isOnlySmnnUUID = value


    def setNomenclatureSmnnUUID(self, smnnUUID):
        self._smnnUUID = smnnUUID


    def setIsType(self, type):
        self.isType = type


    @pyqtSignature('QString')
    def on_edtFindSmnnName_textChanged(self, text):
        if text.isEmpty():
            self.modelSmnnSortModel.removeFilter('mnn')
        else:
            self.modelSmnnSortModel.setFilter('mnn', text, CSortFilterProxyTableModel.MatchContains)


    @pyqtSignature('QString')
    def on_edtFindGrlsLfName_textChanged(self, text):
        if text.isEmpty():
            self.modelSmnnSortModel.removeFilter('name')
        else:
            self.modelSmnnSortModel.setFilter('name', text, CSortFilterProxyTableModel.MatchContains)


    @pyqtSignature('bool')
    def on_chkOnlyExists_toggled(self, value):
        self.on_buttonBox_apply()


    def on_buttonBox_apply(self):
        QtGui.qApp.setWaitCursor()
        try:
            findSmnnName = forceStringEx(self.edtFindSmnnName.text())
            findGrlsLfName = forceStringEx(self.edtFindGrlsLfName.text())
            records = self.getUUIDList(findSmnnName, findGrlsLfName)
            self.setUUIDList(records, self.UUID)
        finally:
            QtGui.qApp.restoreOverrideCursor()


    def setUUID(self, UUID):
        self.UUID = UUID


    def setLfFormId(self, lfFormId):
        self.lfFormId = lfFormId


    def setNomenclatureId(self, nomenclatureId):
        self.nomenclatureId = nomenclatureId


    def setNomenclatureIdList(self, nomenclatureIdList):
        self.nomenclatureIdList = nomenclatureIdList


    def setUUIDList(self, records, posToId):
        self.tblSmnn.model().loadItems(records)
        self.tblSmnn.setFocus(Qt.OtherFocusReason)
        if not records:
            self.edtFindSmnnName.setFocus(Qt.OtherFocusReason)


    def setOrgStructureId(self, value):
        self.orgStructureId = value


    def getOrgStructureId(self):
        return self.orgStructureId


    def setBegDate(self, date):
        self.begDate = date


    def setEndDate(self, date):
        self.endDate = date


#    def getUUIDList(self, findSmnnName, findGrlsLfName):
#        db = QtGui.qApp.db
#        tableLfForm= db.table('rbLfForm')
#        tableNC = db.table('rbNomenclature')
#        tableESKLP_Klp = db.table('esklp.Klp')
#        tableEsklp_SmnnGrlsLf = db.table('esklp.Smnn_GrlsLf')
#        tableEsklp_Smnn = db.table('esklp.Smnn')
##        queryTable = tableNC.innerJoin(tableESKLP_Klp, tableESKLP_Klp['UUID'].eq(tableNC['esklpUUID']))
##        queryTable = queryTable.innerJoin(tableEsklp_Smnn, tableEsklp_Smnn['id'].eq(tableESKLP_Klp['smnn_id']))
##        queryTable = queryTable.innerJoin(tableEsklp_SmnnGrlsLf, tableEsklp_SmnnGrlsLf['master_id'].eq(tableESKLP_Klp['smnn_id']))
##        queryTable = queryTable.innerJoin(tableLfForm, db.joinAnd([tableLfForm['name'].eq(tableEsklp_SmnnGrlsLf['lf_name']), tableLfForm['dosage'].eq(tableEsklp_SmnnGrlsLf['dosage_name'])]))
#
#        queryTable = tableEsklp_Smnn.innerJoin(tableEsklp_SmnnGrlsLf, tableEsklp_SmnnGrlsLf['master_id'].eq(tableEsklp_Smnn['id']))
#        queryTable = queryTable.innerJoin(tableESKLP_Klp, tableEsklp_Smnn['id'].eq(tableESKLP_Klp['smnn_id']))
#        queryTable = queryTable.leftJoin(tableNC, tableNC['esklpUUID'].eq(tableESKLP_Klp['UUID']))
#        queryTable = queryTable.leftJoin(tableLfForm, db.joinAnd([tableLfForm['name'].eq(tableEsklp_SmnnGrlsLf['lf_name']), tableLfForm['dosage'].eq(tableEsklp_SmnnGrlsLf['dosage_name']), tableLfForm['isESKLP'].eq(1), tableNC['lfForm_id'].eq(tableLfForm['id'])]))
#
#        cond = []
#        findNomenclatureIdList = []
#        order = u'esklp.Smnn.mnn, esklp.Smnn_GrlsLf.lf_name, esklp.Smnn_GrlsLf.dosage_name'
#        if self.nomenclatureId:
#            cond.append(tableNC['id'].eq(self.nomenclatureId))
#            findNomenclatureIdList = [self.nomenclatureId]
#        if self.nomenclatureIdList:
#            cond.append(tableNC['id'].inlist(self.nomenclatureIdList))
#            findNomenclatureIdList = self.nomenclatureIdList
#        if self.nomenclatureId or self.nomenclatureIdList:
#            cond.append(tableLfForm['name'].eq(tableESKLP_Klp['lf_norm_name']))
#            cond.append(tableLfForm['dosage'].eq(tableESKLP_Klp['dosage_norm_name']))
#        if self.chkOnlyExists.isChecked():
#            if QtGui.qApp.controlSMFinance() in (1, 2):
#                existsIdList = getExistsNomenclatureIdList(self.orgStructureId, self.getFinanceId(), self.getMedicalAidKindId(), nomenclatureIdList = findNomenclatureIdList)
#            else:
#                existsIdList = getExistsNomenclatureIdList(self.orgStructureId, nomenclatureIdList = findNomenclatureIdList)
#            cond.append(tableNC['id'].inlist(existsIdList))
##        else:
##            if QtGui.qApp.controlSMFinance() in (1, 2):
##                existsIdList = getExistsNomenclatureIdList(self.orgStructureId, self.getFinanceId(), self.getMedicalAidKindId(), otherHaving = [u'1'], nomenclatureIdList = findNomenclatureIdList)
##                cond.append(tableNC['id'].inlist(existsIdList))
#        if findSmnnName:
#            cond.append(db.joinOr([tableEsklp_Smnn['code'].like(addDots(findSmnnName)), tableEsklp_Smnn['mnn'].like(addDots(findSmnnName)), tableEsklp_Smnn['form'].like(addDots(findSmnnName))]))
#        if findGrlsLfName:
#            cond.append(db.joinOr([tableLfForm['name'].like(addDots(findGrlsLfName)), tableLfForm['dosage'].like(addDots(findGrlsLfName))]))
#        cols = [tableEsklp_Smnn['UUID'],
#                tableLfForm['id'].alias('lfFormId'),
#                tableEsklp_Smnn['mnn'],
#                tableLfForm['name'],
#                tableLfForm['dosage'],
#                tableESKLP_Klp['lf_norm_name'],
#                tableESKLP_Klp['dosage_norm_name'],
#                tableEsklp_SmnnGrlsLf['lf_name'],
#                tableEsklp_SmnnGrlsLf['dosage_name'],
#                tableLfForm['isESKLP'],
#                tableNC['id'].alias('nomenclatureId'),
#                tableNC['lfForm_id']
#                ]
#        records = db.getDistinctRecordList(queryTable, cols, cond, order=order, limit=1000)
#        #print db.selectDistinctStmt(queryTable, cols, cond, order=order, limit=1000)
#        return records


    def getUUIDList(self, findSmnnName, findGrlsLfName):
        db = QtGui.qApp.db
        tableLfForm= db.table('rbLfForm')
        tableNC = db.table('rbNomenclature')
        tableESKLP_Klp = db.table('esklp.Klp')
        tableEsklp_SmnnGrlsLf = db.table('esklp.Smnn_GrlsLf')
        tableEsklp_Smnn = db.table('esklp.Smnn')
        if self.nomenclatureId or self.nomenclatureIdList or self.chkOnlyExists.isChecked():
            queryTable = tableNC.innerJoin(tableESKLP_Klp, tableESKLP_Klp['UUID'].eq(tableNC['esklpUUID']))
            queryTable = queryTable.innerJoin(tableEsklp_Smnn, tableEsklp_Smnn['id'].eq(tableESKLP_Klp['smnn_id']))
            queryTable = queryTable.innerJoin(tableEsklp_SmnnGrlsLf, tableEsklp_SmnnGrlsLf['master_id'].eq(tableESKLP_Klp['smnn_id']))
            queryTable = queryTable.innerJoin(tableLfForm, db.joinAnd([tableLfForm['name'].eq(tableEsklp_SmnnGrlsLf['lf_name']), tableLfForm['dosage'].eq(tableEsklp_SmnnGrlsLf['dosage_name'])]))
            cond = [tableLfForm['isESKLP'].eq(1),
                    tableNC['lfForm_id'].eq(tableLfForm['id'])
                    ]
            cols = [tableEsklp_Smnn['UUID'],
                    tableLfForm['id'].alias('lfFormId'),
                    tableEsklp_Smnn['mnn'],
                    tableLfForm['name'],
                    tableLfForm['dosage']
                    ]
        else:
            queryTable = tableEsklp_Smnn.innerJoin(tableEsklp_SmnnGrlsLf, tableEsklp_SmnnGrlsLf['master_id'].eq(tableEsklp_Smnn['id']))
            queryTable = queryTable.leftJoin(tableLfForm, db.joinAnd([tableLfForm['name'].eq(tableEsklp_SmnnGrlsLf['lf_name']), tableLfForm['dosage'].eq(tableEsklp_SmnnGrlsLf['dosage_name']), tableLfForm['isESKLP'].eq(1)]))
            cond = []
            cols = [tableEsklp_Smnn['UUID'],
                    tableLfForm['id'].alias('lfFormId'),
                    tableEsklp_Smnn['mnn'],
                    tableEsklp_SmnnGrlsLf['id'].alias('smnnGrlsLfId'),
                    tableEsklp_SmnnGrlsLf['lf_name'].alias('name'),
                    tableEsklp_SmnnGrlsLf['dosage_name'].alias('dosage')
                    ]
        if self.begDate:
            cond.append(db.joinOr([tableEsklp_Smnn['date_end'].isNull(), tableEsklp_Smnn['date_end'].dateGe(self.begDate)]))
        if self.endDate:
            cond.append(db.joinOr([tableEsklp_Smnn['date_end'].isNull(), tableEsklp_Smnn['date_end'].dateLe(self.endDate)]))
        findNomenclatureIdList = []
        order = u'esklp.Smnn.mnn, esklp.Smnn_GrlsLf.lf_name, esklp.Smnn_GrlsLf.dosage_name'
        if self.nomenclatureId:
            cond.append(tableNC['id'].eq(self.nomenclatureId))
            findNomenclatureIdList = [self.nomenclatureId]
        if self.nomenclatureIdList:
            cond.append(tableNC['id'].inlist(self.nomenclatureIdList))
            findNomenclatureIdList = self.nomenclatureIdList
        if self.nomenclatureId or self.nomenclatureIdList:
            cond.append(tableLfForm['name'].eq(tableESKLP_Klp['lf_norm_name']))
            cond.append(tableLfForm['dosage'].eq(tableESKLP_Klp['dosage_norm_name']))
        if self.chkOnlyExists.isChecked():
            if QtGui.qApp.controlSMFinance() in (1, 2):
                existsIdList = getExistsNomenclatureIdList(self.orgStructureId, self.getFinanceId(), self.getMedicalAidKindId(), nomenclatureIdList = findNomenclatureIdList)
            else:
                existsIdList = getExistsNomenclatureIdList(self.orgStructureId, nomenclatureIdList = findNomenclatureIdList)
            cond.append(tableNC['id'].inlist(existsIdList))
        if findSmnnName:
            cond.append(db.joinOr([tableEsklp_Smnn['code'].like(addDots(findSmnnName)), tableEsklp_Smnn['mnn'].like(addDots(findSmnnName)), tableEsklp_Smnn['form'].like(addDots(findSmnnName))]))
        if findGrlsLfName:
            if self.nomenclatureId or self.nomenclatureIdList or self.chkOnlyExists.isChecked():
                cond.append(db.joinOr([tableLfForm['name'].like(addDots(findGrlsLfName)), tableLfForm['dosage'].like(addDots(findGrlsLfName))]))
            else:
                cond.append(db.joinOr([tableEsklp_SmnnGrlsLf['lf_name'].like(addDots(findGrlsLfName)), tableEsklp_SmnnGrlsLf['dosage_name'].like(addDots(findGrlsLfName))]))

        records = db.getDistinctRecordList(queryTable, cols, cond, order=order)
        #print db.selectDistinctStmt(queryTable, cols, cond, order=order, limit=1000)
        return records


    def selectGrlsLfCode(self, UUID, lfFormId):
        self.lfFormId = lfFormId
        self.UUID = UUID
        self.emit(SIGNAL('smnnLfFormIdSelected(QString, int)'), self.UUID, self.lfFormId)
        self.close()


    @pyqtSignature('QModelIndex')
    def on_tblSmnn_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.model.flags(index)):
                curIndex = self.tblSmnn.currentIndex()
                if curIndex.isValid():
                    sourceRow = self.modelSmnnSortModel.mapToSource(curIndex).row()
                    record = self.tblSmnn.model().getRecordByRow(sourceRow)
                    UUID = forceStringEx(record.value('UUID'))
                    lfFormId = forceRef(record.value('lfFormId'))
                    if not lfFormId:
                        if self.nomenclatureId or self.nomenclatureIdList or self.chkOnlyExists.isChecked():
                            pass
                        else:
                            db = QtGui.qApp.db
                            tableLfForm = db.table('rbLfForm')
                            codeMax = forceInt(db.getMax(tableLfForm, maxCol = tableLfForm['code'].cast(u'INT'), where = [tableLfForm['isESKLP'].eq(1)]))
                            newRecord = tableLfForm.newRecord()
                            newRecord.setValue('createDatetime', toVariant(QDateTime.currentDateTime()))
                            newRecord.setValue('createPerson_id', toVariant(QtGui.qApp.userId))
                            newRecord.setValue('modifyDatetime', toVariant(QDateTime.currentDateTime()))
                            newRecord.setValue('modifyPerson_id', toVariant(QtGui.qApp.userId))
                            newRecord.setValue('code', toVariant(codeMax+1)) #0015247:0067482:пункт2
                            newRecord.setValue('name', record.value('name'))
                            newRecord.setValue('dosage', record.value('dosage'))
                            newRecord.setValue('isESKLP', toVariant(1))
                            db.transaction()
                            try:
                                lfFormId = db.insertRecord(tableLfForm, newRecord)
                                db.commit()
                            except:
                                db.rollback()
                    self.selectGrlsLfCode(UUID, lfFormId)
        QtGui.QDialog.accept(self)


    def getValue(self):
        return self.UUID, self.lfFormId


    def saveData(self):
        return True


class CSmnnTableModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.headers = [u'МНН', u'Лекарственная форма', u'Дозировка']
        self.items = []


    def items(self):
        return self.items


    def columnCount(self, index = None):
        return len(self.headers)


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index = QModelIndex()):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headers[section])
        return QVariant()


    def getRecordByRow(self, row):
        if row >= 0 and row < len(self.items):
            return self.items[row]
        return None


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if 0 <= row < len(self.items):
                item = self.items[row]
                if item:
                    if column == 0:
                        return toVariant(item.value('mnn'))
                    elif column == 1:
                        return toVariant(item.value('name'))
                    elif column == 2:
                        return toVariant(item.value('dosage'))
        return QVariant()


    def loadItems(self, records):
        self.items = records
        self.reset()

