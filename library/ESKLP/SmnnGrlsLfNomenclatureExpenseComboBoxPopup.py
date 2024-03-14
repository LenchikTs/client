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


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, pyqtSignature, SIGNAL, QRegExp

from library.database   import CTableRecordCacheEx
from library.TableModel import CTableModel, CTextCol
from library.DialogBase import CConstructHelperMixin
from library.SortFilterProxyTableModel import CSortFilterProxyTableModel
from library.Utils      import getPref, setPref, addDots, forceStringEx, forceRef
from Stock.Utils        import getExistsNomenclatureIdList

from library.ESKLP.Ui_SmnnGrlsLfNomenclatureExpenseComboBoxPopup import Ui_SmnnGrlsLfNomenclatureExpenseComboBoxPopup

__all__ = [ 'CSmnnGrlsLfNomenclatureExpenseComboBoxPopup',
          ]


class CSmnnGrlsLfNomenclatureExpenseComboBoxPopup(QtGui.QFrame, Ui_SmnnGrlsLfNomenclatureExpenseComboBoxPopup, CConstructHelperMixin):
    __pyqtSignals__ = ('smnnUUIDSelected(QString)',
                       'smnnLfFormIdSelected(QString, int)'
                      )

    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.addModels('', CSmnnTableModel(self))
        self.addModels('SmnnSortModel', CSortFilterProxyTableModel(self, self.model))
        self.model = self.modelSmnnSortModel.sourceModel()
        self.setupUi(self)
        self.setModels(self.tblSmnn, self.modelSmnnSortModel, self.selectionModelSmnnSortModel)
        self.isType = 0
        self.UUID = None
        self._isOnlySmnnUUID = False
        self._smnnUUID = None
        self.lfFormId = None
        self.nomenclatureId = None
        self.nomenclatureIdList = []
        self.orgStructureId = None
        self.defaultOnlyExists = False
        self.tblSmnn.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CSmnnGrlsLfNomenclatureExpenseComboBoxPopup', {})
        self.tblSmnn.loadPreferences(preferences)
        rX = QRegExp(u"[-?!,.А-Яа-яёЁA-Za-z\\d\\s]+")
        self.edtFindName.setValidator(QtGui.QRegExpValidator(rX, self))


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblSmnn.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CSmnnGrlsLfNomenclatureExpenseComboBoxPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblSmnn:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblSmnn.currentIndex()
                self.tblSmnn.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


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


    def on_buttonBox_reset(self):
        self.edtFindName.setText('')
        self.chkOnlyExists.setChecked(self.defaultOnlyExists)


    def on_buttonBox_apply(self):
        QtGui.qApp.setWaitCursor()
        try:
            findName = forceStringEx(self.edtFindName.text())
            crIdList = self.getUUIDList(findName)
            self.setUUIDList(crIdList, self.UUID)
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


    def setUUIDList(self, idList, posToId):
        self.tblSmnn.setIdList(idList, posToId)
        self.tblSmnn.setFocus(Qt.OtherFocusReason)
        if not idList:
            self.edtFindName.setFocus(Qt.OtherFocusReason)


    def setOrgStructureId(self, value):
        self.orgStructureId = value


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
        cond = [tableLfForm['isESKLP'].eq(1)]
        findNomenclatureIdList = []
        order = u'esklp.Smnn.mnn, esklp.Smnn_GrlsLf.lf_name, esklp.Smnn_GrlsLf.dosage_name'
        if self.nomenclatureId:
            cond.append(tableNC['id'].eq(self.nomenclatureId))
            findNomenclatureIdList = [self.nomenclatureId]
        elif self.nomenclatureIdList:
            cond.append(tableNC['id'].inlist(self.nomenclatureIdList))
            findNomenclatureIdList = self.nomenclatureIdList
        if self.nomenclatureId or self.nomenclatureIdList:
            cond.append(tableLfForm['name'].eq(tableESKLP_Klp['lf_norm_name']))
            cond.append(tableLfForm['dosage'].eq(tableESKLP_Klp['dosage_norm_name']))
        if self.chkOnlyExists.isChecked():
            existsIdList = getExistsNomenclatureIdList(self.orgStructureId, nomenclatureIdList = findNomenclatureIdList)
            cond.append(tableNC['id'].inlist(existsIdList))
        if findName:
            cond.append(db.joinOr([tableEsklp_Smnn['code'].like(addDots(findName)), tableEsklp_Smnn['mnn'].like(addDots(findName)), tableEsklp_Smnn['form'].like(addDots(findName))]))
        idList = []
        records = db.getDistinctRecordList(queryTable, [tableEsklp_Smnn['UUID'], tableLfForm['id']], cond, order=order, limit=1000)
        for record in records:
            UUID = forceStringEx(record.value('UUID'))
            if UUID and UUID not in idList:
                idList.append(UUID)
        return idList


    def selectGrlsLfCode(self, UUID, lfFormId):
        self.lfFormId = lfFormId
        self.UUID = UUID
        self.emit(SIGNAL('smnnLfFormIdSelected(QString, int)'), self.UUID, self.lfFormId)
        self.close()

#
#    def selectSmnnCode(self, UUID):
#        self.UUID = UUID
#        self.emit(SIGNAL('smnnUUIDSelected(QString)'), self.UUID)
#        #self.close()


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


class CSmnnTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'МНН', ['mnn'], 30))
        self.addColumn(CTextCol(u'Форма выпуска', ['name'], 30))
        self.addColumn(CTextCol(u'Дозировка',  ['dosage'], 30))
        self.setTable('esklp.Smnn')


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable


    def setTable(self, tableName):
        db = QtGui.qApp.db
        tableEsklp_Smnn = db.table('esklp.Smnn')
        tableNC = db.table('rbNomenclature')
        tableESKLP_Klp = db.table('esklp.Klp')
        tableLfForm= db.table('rbLfForm')
        tableEsklp_SmnnGrlsLf = db.table('esklp.Smnn_GrlsLf')
        queryTable = tableNC.innerJoin(tableESKLP_Klp, tableESKLP_Klp['UUID'].eq(tableNC['esklpUUID']))
        queryTable = queryTable.innerJoin(tableEsklp_Smnn, tableEsklp_Smnn['id'].eq(tableESKLP_Klp['smnn_id']))
        queryTable = queryTable.innerJoin(tableEsklp_SmnnGrlsLf, tableEsklp_SmnnGrlsLf['master_id'].eq(tableEsklp_Smnn['id']))
        queryTable = queryTable.innerJoin(tableLfForm, db.joinAnd([tableLfForm['name'].eq(tableEsklp_SmnnGrlsLf['lf_name']),
        tableLfForm['dosage'].eq(tableEsklp_SmnnGrlsLf['dosage_name']), tableLfForm['name'].eq(tableESKLP_Klp['lf_norm_name']),
        tableLfForm['dosage'].eq(tableESKLP_Klp['dosage_norm_name'])]))
        loadFields = [u'''DISTINCT esklp.Smnn.code, esklp.Smnn.mnn, esklp.Smnn.form, esklp.Smnn.UUID, rbLfForm.id AS lfFormId, rbLfForm.name, rbLfForm.dosage''']
        self._table = queryTable
        self._recordsCache = CTableRecordCacheEx(db, self._table, loadFields, idFieldName = 'esklp.Smnn.UUID')

