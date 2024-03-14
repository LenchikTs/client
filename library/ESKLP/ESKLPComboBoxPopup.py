# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2024 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, pyqtSignature, SIGNAL, QDate

from library.database import CTableRecordCacheEx
from library.TableModel import CTableModel, CTextCol, CDesignationCol
from library.Utils import forceString, forceStringEx, setPref, getPref

from Ui_ESKLPComboBoxPopup import Ui_ESKLPComboBoxPopup

__all__ = ['CESKLPComboBoxPopup',
           ]


class CESKLPComboBoxPopup(QtGui.QFrame, Ui_ESKLPComboBoxPopup):
    __pyqtSignals__ = ('ESKLPUUIDSelected(QString)'
                       )

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CESKLPTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblESKLP.setModel(self.tableModel)
        self.tblESKLP.setSortingEnabled(True)
        self.tblESKLP.horizontalHeader().sortIndicatorChanged.connect(self.on_tblESKLP_sortIndicatorChanged)
        self.tblESKLP.setSelectionModel(self.tableSelectionModel)
        self.tblESKLP.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CESKLPComboBoxPopup', {})
        self.tblESKLP.loadPreferences(preferences)
        if not preferences:
            self.resizeESKLPHeader()
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setShortcut(Qt.Key_Return)
        self.UUID = None
        self.dialogInfo = {}
        self.on_buttonBox_reset()

    def resizeESKLPHeader(self):
        for column in range(self.tblESKLP.horizontalHeader().count()):
            text = self.tableModel.headerData(column, orientation=Qt.Horizontal, role=Qt.DisplayRole).toString()
            fm = QtGui.QFontMetrics(QtGui.QFont(text))
            width = fm.width(text)
            self.tblESKLP.horizontalHeader().resizeSection(column, width)

    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent is not None:
            opt = QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos()):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)

    def closeEvent(self, event):
        preferences = self.tblESKLP.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CESKLPComboBoxPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)

    def eventFilter(self, watched, event):
        if watched == self.tblESKLP:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblESKLP.currentIndex()
                self.tblESKLP.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)

    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()

    def on_buttonBox_reset(self):
        self.edtESKLPCode.clear()
        self.edtESKLPMnn_norm_name.clear()
        self.edtESKLPDosage_norm_name.clear()
        self.edtESKLPLf_norm_name.clear()
        self.edtESKLPTrade_name.clear()
        self.edtESKLPPack1_name.clear()
        self.edtESKLPPack2_name.clear()
        self.edtESKLPNum_reg.clear()
        self.edtESKLPManufacturer.clear()
        self.edtESKLP_GTIN.clear()
        self.chkESKLP_GTIN.setChecked(False)
        self.chkBegDateWithBeg.setChecked(False)
        self.chkBegDateWithEnd.setChecked(False)
        self.chkEndDateWithBeg.setChecked(False)
        self.chkEndDateWithEnd.setChecked(False)
        self.edtBegDate.setDate(QDate.currentDate())
        self.edtBegDate_2.setDate(QDate.currentDate())
        self.edtEndDate.setDate(QDate.currentDate())
        self.edtEndDate_2.setDate(QDate.currentDate())
        self.getParamsDialogFilter()

    def on_tblESKLP_sortIndicatorChanged(self, index, order):
        model = self.tblESKLP.model()
        model.headerSortingCol = {index: bool(order)}
        model.sortDataModel()

    def on_buttonBox_apply(self):
        self.setESKLPPopupUpdate(self.UUID)

    def checkParamsDialogFilter(self):
        if not self.dialogInfo.get('ESKLPCode', u''):
            if not self.dialogInfo.get('ESKLPMnn_norm_name', u''):
                if not self.dialogInfo.get('ESKLPDosage_norm_name', u''):
                    if not self.dialogInfo.get('ESKLPLf_norm_name', u''):
                        if not self.dialogInfo.get('ESKLPTrade_name', u''):
                            if not self.dialogInfo.get('ESKLPPack1_name', u''):
                                if not self.dialogInfo.get('ESKLPPack2_name', u''):
                                    if not self.dialogInfo.get('ESKLPNum_reg', u''):
                                        if not self.dialogInfo.get('ESKLPManufacturer', u''):
                                            if not self.dialogInfo.get('ESKLP_GTIN', u''):
                                                return False
        return True

    def getParamsDialogFilter(self):
        self.dialogInfo = {'ESKLPCode': forceStringEx(self.edtESKLPCode.text()),
                           'ESKLPMnn_norm_name': forceStringEx(self.edtESKLPMnn_norm_name.text()),
                           'ESKLPDosage_norm_name': forceStringEx(self.edtESKLPDosage_norm_name.text()),
                           'ESKLPLf_norm_name': forceStringEx(self.edtESKLPLf_norm_name.text()),
                           'ESKLPTrade_name': forceStringEx(self.edtESKLPTrade_name.text()),
                           'ESKLPPack1_name': forceStringEx(self.edtESKLPPack1_name.text()),
                           'ESKLPPack2_name': forceStringEx(self.edtESKLPPack2_name.text()),
                           'ESKLPNum_reg': forceStringEx(self.edtESKLPNum_reg.text()),
                           'ESKLPManufacturer': forceStringEx(self.edtESKLPManufacturer.text()),
                           'ESKLP_GTIN': forceStringEx(self.edtESKLP_GTIN.text()),
                           }

    def setESKLPIdList(self, idList, posToId):
        self.tblESKLP.setIdList(idList, posToId)
        if idList:
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget.setTabEnabled(0, True)
            self.tblESKLP.setFocus(Qt.OtherFocusReason)
        else:
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(0, False)
            self.edtESKLPCode.setFocus(Qt.OtherFocusReason)

    def getESKLPIdList(self):
        db = QtGui.qApp.db
        tableESKLP_Klp = db.table('esklp.Klp')
        tableESKLPManufacturer = db.table('esklp.Manufacturer')

        queryTable = tableESKLP_Klp

        ESKLPCode = self.dialogInfo.get('ESKLPCode', None)
        ESKLPMnn_norm_name = self.dialogInfo.get('ESKLPMnn_norm_name', None)
        ESKLPDosage_norm_name = self.dialogInfo.get('ESKLPDosage_norm_name', None)
        ESKLPLf_norm_name = self.dialogInfo.get('ESKLPLf_norm_name', None)
        ESKLPTrade_name = self.dialogInfo.get('ESKLPTrade_name', None)
        ESKLPPack1_name = self.dialogInfo.get('ESKLPPack1_name', None)
        ESKLPPack2_name = self.dialogInfo.get('ESKLPPack2_name', None)
        ESKLPNum_reg = self.dialogInfo.get('ESKLPNum_reg', None)
        ESKLPManufacturer = self.dialogInfo.get('ESKLPManufacturer', None)
        ESKLP_GTIN = self.dialogInfo.get('ESKLP_GTIN', None)

        cond = []
        orderList = u', '.join([fieldName for fieldName in [tableESKLP_Klp['trade_name'].name(), tableESKLP_Klp['mass_volume_name'].name()]])
        if not self.chkESKLP_GTIN.isChecked():
            if ESKLPCode:
                cond.append(tableESKLP_Klp['code'].contain(ESKLPCode))
            if ESKLPMnn_norm_name:
                cond.append(tableESKLP_Klp['mnn_norm_name'].contain(ESKLPMnn_norm_name))
            if ESKLPDosage_norm_name:
                cond.append(tableESKLP_Klp['dosage_norm_name'].contain(ESKLPDosage_norm_name))
            if ESKLPLf_norm_name:
                cond.append(tableESKLP_Klp['lf_norm_name'].contain(ESKLPLf_norm_name))
            if ESKLPTrade_name:
                cond.append(tableESKLP_Klp['trade_name'].contain(ESKLPTrade_name))
            if ESKLPPack1_name:
                cond.append(tableESKLP_Klp['pack1_name'].contain(ESKLPPack1_name))
            if ESKLPPack2_name:
                cond.append(tableESKLP_Klp['pack2_name'].contain(ESKLPPack2_name))
            if ESKLPNum_reg:
                cond.append(tableESKLP_Klp['num_reg'].contain(ESKLPNum_reg))
            if ESKLPManufacturer:
                queryTable = queryTable.leftJoin(tableESKLPManufacturer, tableESKLP_Klp['manufacturer_id'].eq(tableESKLPManufacturer['id']))
                cond.append(tableESKLPManufacturer['name'].contain(ESKLPManufacturer))
            dateCheckBox = any([
                self.chkBegDateWithBeg.isChecked(),
                self.chkBegDateWithEnd.isChecked(),
                self.chkEndDateWithBeg.isChecked(),
                self.chkEndDateWithEnd.isChecked(),
            ])
            if dateCheckBox:
                if self.chkBegDateWithBeg.isChecked():
                    cond.append(tableESKLP_Klp['date_start'].ge(self.edtBegDate.date()))
                if self.chkBegDateWithEnd.isChecked():
                    cond.append(tableESKLP_Klp['date_start'].le(self.edtBegDate_2.date()))
                if self.chkEndDateWithBeg.isChecked():
                    cond.append(tableESKLP_Klp['date_end'].ge(self.edtEndDate.date()))
                if self.chkEndDateWithEnd.isChecked():
                    cond.append(tableESKLP_Klp['date_end'].le(self.edtEndDate_2.date()))
            else:
                cond.append(db.joinOr([
                    tableESKLP_Klp['date_end'].isNull(),
                    tableESKLP_Klp['date_end'].ge(QDate.currentDate()),
                ]))

            idList = []
            records = db.getDistinctRecordList(queryTable, [tableESKLP_Klp['UUID']], cond, order=orderList, limit=1000)
            for record in records:
                UUID = forceStringEx(record.value('UUID'))
                if UUID and UUID not in idList:
                    idList.append(UUID)
        else:
            idList = []
            if ESKLP_GTIN:
                stmt = 'SELECT DISTINCT esklp.Klp.UUID ' \
                       'FROM esklp.Klp ' \
                       'LEFT JOIN esklp.MdlpPublicProductInformation ON esklp.MdlpPublicProductInformation.code = esklp.Klp.code ' \
                       'WHERE esklp.MdlpPublicProductInformation.gtin=%s' % self.edtESKLP_GTIN.text()
                query = QtGui.qApp.db.query(stmt)
                while query.next():
                    record = query.record()
                    idList.append(forceString(record.value('UUID')))
        return idList

    def setUUIDESKLPPopupUpdate(self, UUID):
        self.UUID = UUID
        self.setESKLPIdList([], self.UUID)

    def setESKLPPopupUpdate(self, UUID):
        QtGui.qApp.setWaitCursor()
        try:
            self.getParamsDialogFilter()
            crIdList = self.getESKLPIdList()
            self.setESKLPIdList(crIdList, UUID)
        finally:
            QtGui.qApp.restoreOverrideCursor()

    def selectESKLPUUID(self, UUID):
        self.UUID = UUID
        self.emit(SIGNAL('ESKLPUUIDSelected(QString)'), UUID)
        self.close()

    @pyqtSignature('QModelIndex')
    def on_tblESKLP_doubleClicked(self, index):
        if index.isValid():
            if Qt.ItemIsEnabled & self.tableModel.flags(index):
                UUID = self.tblESKLP.currentItemId()
                self.selectESKLPUUID(UUID)

    @pyqtSignature('bool')
    def on_chkESKLP_GTIN_toggled(self, checked):
        self.edtESKLPCode.setEnabled(not checked)
        self.edtESKLPMnn_norm_name.setEnabled(not checked)
        self.edtESKLPDosage_norm_name.setEnabled(not checked)
        self.edtESKLPLf_norm_name.setEnabled(not checked)
        self.edtESKLPTrade_name.setEnabled(not checked)
        self.edtESKLPPack1_name.setEnabled(not checked)
        self.edtESKLPPack2_name.setEnabled(not checked)
        self.edtESKLPNum_reg.setEnabled(not checked)
        self.edtESKLPManufacturer.setEnabled(not checked)
        self.chkBegDateWithBeg.setEnabled(not checked)
        self.chkBegDateWithEnd.setEnabled(not checked)
        self.chkEndDateWithBeg.setEnabled(not checked)
        self.chkEndDateWithEnd.setEnabled(not checked)
        self.edtBegDate.setEnabled(not checked)
        self.edtBegDate_2.setEnabled(not checked)
        self.edtEndDate.setEnabled(not checked)
        self.edtEndDate_2.setEnabled(not checked)
        if checked:
            self.edtESKLP_GTIN.setFocus()


class CGTINCol(CTextCol):
    def __init__(self, title, fields, defaultWidth, alignment='l'):
        CTextCol.__init__(self, title, fields, defaultWidth, alignment)
        self._cache = {}

    def format(self, values):
        code = forceString(values[0])
        value = self._cache.get(code)
        if value is not None:
            return value
        db = QtGui.qApp.db
        tableMdlpProdInfo = db.table('esklp.MdlpPublicProductInformation')
        cols = [
            'GROUP_CONCAT(gtin SEPARATOR ", ") AS gtin'
        ]
        cond = [
            tableMdlpProdInfo['code'].eq(code),
        ]
        record = db.getRecordEx(tableMdlpProdInfo, cols, cond)
        value = forceString(record.value('gtin')) if record else u''
        self._cache[code] = value
        return value

    def invalidateRecordsCache(self):
        self._cache.clear()


class CESKLPTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Код', ['code'], 30).setToolTip(u'Код каталога для позиции КЛП'))
        self.addColumn(CTextCol(u'МНН', ['mnn_norm_name'], 30).setToolTip(u'Нормализованное описание (исходное) МНН'))
        self.addColumn(CTextCol(u'Дозировка', ['dosage_norm_name'], 30).setToolTip(u'Нормализованное описание (исходное) дозировки'))
        self.addColumn(CTextCol(u'Лекарственная форма', ['lf_norm_name'], 20).setToolTip(u'Нормализованное название (исходное) лекарственной формы'))
        self.addColumn(CTextCol(u'Торговое наименование', ['trade_name'], 10))
        self.addColumn(CTextCol(u'Кол-во ЛФ в Перв.уп.', ['pack1_num'], 10).setToolTip(u'Количество лекарственной формы в первичной упаковке'))
        self.addColumn(CTextCol(u'Название Перв.уп.', ['pack1_name'], 20).setToolTip(u'Название первичной упаковки'))
        self.addColumn(CTextCol(u'Кол-во Перв.уп. в Потр.уп.', ['pack2_num'], 10).setToolTip(u'Количество первичных упаковок в потребительской упаковке'))
        self.addColumn(CTextCol(u'Название Потр.уп.', ['pack2_name'], 20).setToolTip(u'Название потребительской упаковки'))
        self.addColumn(CTextCol(u'Номер РУ ЛП', ['num_reg'], 20).setToolTip(u'Номер регистрационного удостоверения лекарственного препарата'))
        self.addColumn(CDesignationCol(u'Производитель ЛП', ['manufacturer_id'], [('esklp.Manufacturer', 'name'),], 30).setToolTip(u'Название производителя лекарственного препарата'))
        self.addColumn(CTextCol(u'Дата начала', ['date_start'], 11).setToolTip(u'Дата начала действия записи'))
        self.addColumn(CTextCol(u'Дата окончания', ['date_end'], 11).setToolTip(u'Дата окончания действия записи'))
        self.addColumn(CGTINCol(u'GTIN', ['code'], 30).setToolTip(u'Global Trade Item Number'))
        self.setTable('esklp.Klp')

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setTable(self, tableName):
        db = QtGui.qApp.db
        tableESKLP_Klp = db.table('esklp.Klp')
        loadFields = [
            u'DISTINCT code, mnn_norm_name, dosage_norm_name, lf_norm_name, trade_name, pack1_num, pack1_name, '
            u'pack2_num, pack2_name, num_reg, manufacturer_id, date_start, date_end'
        ]
        self._table = tableESKLP_Klp
        self._recordsCache = CTableRecordCacheEx(db, self._table, loadFields, idFieldName='UUID')
