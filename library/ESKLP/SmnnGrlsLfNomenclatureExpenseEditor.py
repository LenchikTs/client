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
from PyQt4.QtCore             import Qt, pyqtSignature, QVariant, QModelIndex, QAbstractTableModel, SIGNAL, QRegExp

from library.DialogBase       import CDialogBase
from library.PreferencesMixin import CDialogPreferencesMixin
from library.SortFilterProxyTableModel import CSortFilterProxyTableModel
from Stock.Utils              import getExistsNomenclatureIdList
from library.Utils            import getPref, setPref, addDots, forceStringEx, forceRef, toVariant

from library.ESKLP.Ui_SmnnGrlsLfNomenclatureExpenseEditor import Ui_SmnnGrlsLfNomenclatureExpenseEditor


class CSmnnGrlsLfNomenclatureExpenseEditor(CDialogBase, Ui_SmnnGrlsLfNomenclatureExpenseEditor, CDialogPreferencesMixin):
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
        self.tblSmnn.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CSmnnGrlsLfNomenclatureExpenseEditor', {})
        self.tblSmnn.loadPreferences(preferences)
        rX = QRegExp(u"[-?!,.А-Яа-яёЁA-Za-z\\d\\s]+")
        self.edtFindName.setValidator(QtGui.QRegExpValidator(rX, self))
        self.loadDialogPreferences()


    def closeEvent(self, event):
        preferences = self.tblSmnn.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CSmnnGrlsLfNomenclatureExpenseEditor', preferences)
        CDialogBase.closeEvent(self, event)


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
    def on_edtFindName_textChanged(self, text):
        if text.isEmpty():
            self.modelSmnnSortModel.removeFilter('mnn')
        else:
            self.modelSmnnSortModel.setFilter('mnn', text, CSortFilterProxyTableModel.MatchContains)


    @pyqtSignature('bool')
    def on_chkOnlyExists_toggled(self, value):
        self.on_buttonBox_apply()


    def on_buttonBox_apply(self):
        QtGui.qApp.setWaitCursor()
        try:
            findName = forceStringEx(self.edtFindName.text())
            records = self.getUUIDList(findName)
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


    def setUUIDList(self, records, posToId):
        self.tblSmnn.model().loadItems(records)
        self.tblSmnn.setFocus(Qt.OtherFocusReason)
        if not records:
            self.edtFindName.setFocus(Qt.OtherFocusReason)


    def setOrgStructureId(self, value):
        self.orgStructureId = value


    def getOrgStructureId(self):
        return self.orgStructureId


    def getUUIDList(self, findName):
        db = QtGui.qApp.db
        tableLfForm= db.table('rbLfForm')
        tableNC = db.table('rbNomenclature')
        tableESKLP_Klp = db.table('esklp.Klp')
        tableEsklp_SmnnGrlsLf = db.table('esklp.Smnn_GrlsLf')
        tableEsklp_Smnn = db.table('esklp.Smnn')
        queryTable = tableNC.innerJoin(tableESKLP_Klp, tableESKLP_Klp['UUID'].eq(tableNC['esklpUUID']))
        queryTable = queryTable.innerJoin(tableEsklp_Smnn, tableEsklp_Smnn['id'].eq(tableESKLP_Klp['smnn_id']))
        queryTable = queryTable.innerJoin(tableEsklp_SmnnGrlsLf, tableEsklp_SmnnGrlsLf['master_id'].eq(tableESKLP_Klp['smnn_id']))
        queryTable = queryTable.innerJoin(tableLfForm, db.joinAnd([tableLfForm['name'].eq(tableEsklp_SmnnGrlsLf['lf_name']), tableLfForm['dosage'].eq(tableEsklp_SmnnGrlsLf['dosage_name'])]))
        cond = [tableLfForm['isESKLP'].eq(1),
                tableNC['lfForm_id'].eq(tableLfForm['id'])]
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
#        else:
#            if QtGui.qApp.controlSMFinance() in (1, 2):
#                existsIdList = getExistsNomenclatureIdList(self.orgStructureId, self.getFinanceId(), self.getMedicalAidKindId(), otherHaving = [u'1'], nomenclatureIdList = findNomenclatureIdList)
#                cond.append(tableNC['id'].inlist(existsIdList))
        if findName:
            cond.append(db.joinOr([tableEsklp_Smnn['code'].like(addDots(findName)), tableEsklp_Smnn['mnn'].like(addDots(findName)), tableEsklp_Smnn['form'].like(addDots(findName))]))
        cols = [tableEsklp_Smnn['UUID'],
                tableLfForm['id'].alias('lfFormId'),
                tableEsklp_Smnn['mnn'],
                tableLfForm['name'],
                tableLfForm['dosage']
                ]
        records = db.getDistinctRecordList(queryTable, cols, cond, order=order, limit=1000)
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
                    UUID = forceStringEx(self.tblSmnn.model().getRecordByRow(sourceRow).value('UUID'))
                    lfFormId = forceRef(self.tblSmnn.model().getRecordByRow(sourceRow).value('lfFormId'))
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

