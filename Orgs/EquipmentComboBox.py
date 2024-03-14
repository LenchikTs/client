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
from PyQt4.QtCore import Qt, QDate, QVariant, pyqtSignature, SIGNAL

from library.crbcombobox import CRBComboBox
from library.TableModel  import CTableModel, CDateCol, CEnumCol, CRefBookCol, CTextCol
from library.Utils       import forceDate, forceInt, forceRef, forceStringEx, getPref, setPref


from Ui_EquipmentPopup   import Ui_EquipmentPopup

class CEquipmentPopupView(QtGui.QFrame, Ui_EquipmentPopup):
    __pyqtSignals__ = ('equipmentSelected(int)',
                      )
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.tableModel = CEquipmentTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblEquipment.setModel(self.tableModel)
        self.tblEquipment.setSelectionModel(self.tableSelectionModel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setShortcut(Qt.Key_Return)
        self.cmbEquipmentType.setTable('rbEquipmentType')
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CEquipmentPopupView', {})
        self.tblEquipment.loadPreferences(preferences)


    def closeEvent(self, event):
        preferences = self.tblEquipment.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CEquipmentPopupView', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def setEquipments(self):
        self.on_buttonBox_apply(None)


    def getEquipmentIdList(self):
        db = QtGui.qApp.db
        tableEquipment = db.table('rbEquipment')
        cond = []
        if self.chkName.isChecked():
            name = forceStringEx(self.edtName.text())
            if name:
                cond.append(tableEquipment['name'].contain(name))
        if self.chkReleaseDate.isChecked():
            cond.append(tableEquipment['releaseDate'].dateLe(self.edtReleaseDateTo.date()))
            cond.append(tableEquipment['releaseDate'].dateGe(self.edtReleaseDateFrom.date()))
        if self.chkEquipmentType.isChecked():
            equipmentTypeId = self.cmbEquipmentType.value()
            if equipmentTypeId:
                cond.append(tableEquipment['equipmentType_id'].eq(equipmentTypeId))
        if self.chkModel.isChecked():
            model = forceStringEx(self.edtModel.text())
            if model:
                cond.append(tableEquipment['model'].contain(model))
        if self.chkInventoryNumber.isChecked():
            inventoryNumber = forceStringEx(self.edtInventoryNumber.text())
            if inventoryNumber:
                cond.append(tableEquipment['inventoryNumber'].contain(inventoryNumber))
        if self.chkStatus.isChecked():
            cond.append(tableEquipment['status'].eq(self.cmbStatus.currentIndex()))
        idList = db.getIdList(tableEquipment, 'id', cond)
        return idList


    def on_buttonBox_apply(self, id = None):
        idList = self.getEquipmentIdList()
        self.setIdList(idList, id)


    def on_buttonBox_reset(self):
        self.chkName.setChecked(False)
        self.edtName.setEnabled(False)

        self.chkReleaseDate.setChecked(False)
        self.edtReleaseDateFrom.setEnabled(False)
        self.edtReleaseDateTo.setEnabled(False)

        self.chkEquipmentType.setChecked(False)
        self.cmbEquipmentType.setEnabled(False)

        self.chkModel.setChecked(False)
        self.edtModel.setEnabled(False)

        self.chkInventoryNumber.setChecked(False)
        self.edtInventoryNumber.setEnabled(False)

        self.chkStatus.setChecked(False)
        self.cmbStatus.setEnabled(False)


    def setIdList(self, idList, posToId=None):
        if bool(idList):
            self.tblEquipment.setIdList(idList, posToId)
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget.setTabEnabled(0, True)
            self.tblEquipment.setFocus(Qt.OtherFocusReason)
        else:
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(0, False)


    def emitEquipmentSelected(self, id):
        self.emit(SIGNAL('equipmentSelected(int)'), id)
        self.hide()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    @pyqtSignature('QModelIndex')
    def on_tblEquipment_doubleClicked(self, index):
        id = self.tblEquipment.itemId(index)
        if id:
            self.emitEquipmentSelected(id)


class CEquipmentComboBox(CRBComboBox):
    def __init__(self, parent):
        CRBComboBox.__init__(self, parent)
        self.popupView  = None
        self._tableName = 'rbEquipment'
        CRBComboBox.setTable(self, self._tableName)


    def showPopup(self):
        if not self.popupView:
            self.popupView = CEquipmentPopupView(self)
            self.connect(self.popupView, SIGNAL('equipmentSelected(int)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos2 = self.rect().topLeft()
        pos = self.mapToGlobal(pos)
        pos2 = self.mapToGlobal(pos2)
        size = self.popupView.sizeHint()
        width= max(size.width(), self.width())
        size.setWidth(width)
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self.popupView.move(pos)
        self.popupView.resize(size)
        self.popupView.setEquipments()
        self.popupView.show()


# ##########################################


class CWorkEnumCol(CEnumCol):
    def getForegroundColor(self, values):
        value = forceInt(values[0])
        if not value:
            return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()


class CEquipmentTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Код',                 ['code'], 20))
        self.addColumn(CTextCol(u'Наименование',        ['name'], 40))
        self.addColumn(CRefBookCol(u'Тип оборудования', ['equipmentType_id'], 'rbEquipmentType', 10, 2))
        self.addColumn(CTextCol(u'Инвентаризационный номер',          ['inventoryNumber'], 10))
        self.addColumn(CTextCol(u'Модель',          ['model'], 10))
        self.addColumn(CDateCol(u'Дата выпуска',        ['releaseDate'], 8))
        self.addColumn(CWorkEnumCol(u'Статус',          ['status'], [u'Не работает', u'работает'], 5))
        self.loadField('maintenancePeriod')
        self.loadField('maintenanceSingleInPeriod')
        self.loadField('startupDate')
        self.setTable('rbEquipment')
        self.mapBackGroundToId = {}


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.BackgroundRole:
            column = index.column()
            row    = index.row()
            (col, values) = self.getRecordValues(column, row)
            return self.getBackGroundByMaintenancePeriod(values[1])
        else:
            return CTableModel.data(self, index, role)
        return QVariant()


    def getBackGroundByMaintenancePeriod(self, record):
        equipmentId = forceRef(record.value('id'))
        backGround = self.getBackGround(equipmentId)
        if not backGround:
            valid = self.isValidMaintenancePeriod(record)
            if not valid:
                return QVariant()
            startupDate = forceDate(record.value('startupDate'))
            date = self.getLastEquipmentMaintenanceDate(equipmentId, startupDate)
            backGround = self.makeBackGround(date, record)
            self.mapBackGroundToId[equipmentId] = backGround
        return backGround


    def getBackGround(self, id):
        return self.mapBackGroundToId.get(id, None)


    def isValidMaintenancePeriod(self, record):
        maintenancePeriod = forceInt(record.value('maintenancePeriod'))
        maintenanceSingleInPeriod = forceInt(record.value('maintenanceSingleInPeriod'))
        bothEmpty = not (bool(maintenancePeriod) or bool(maintenanceSingleInPeriod))
        bothFull  = bool(maintenancePeriod) and bool(maintenanceSingleInPeriod)
        valid =  not (bothEmpty or bothFull)
        return valid


    def getLastEquipmentMaintenanceDate(self, equipmentId, startupDate):
        db = QtGui.qApp.db
        tableJournal = db.table('EquipmentMaintenanceJournal')
        cond = [tableJournal['master_id'].eq(equipmentId)]
        record = db.getRecordEx(tableJournal, 'MAX('+tableJournal['date'].name()+') AS maxDate', cond)
        if record:
            date = forceDate(record.value('maxDate'))
            if date:
                return date
        return startupDate


    def makeBackGround(self, date, record):
        backGround = QVariant()
        maintenancePeriod = forceInt(record.value('maintenancePeriod'))
        maintenanceSingleInPeriod = forceInt(record.value('maintenanceSingleInPeriod'))
        currentDate = QDate.currentDate()
        if maintenancePeriod and date:
            if date.addMonths(maintenancePeriod) < currentDate:
                backGround = QVariant(QtGui.QColor(125, 125, 125))
        elif maintenanceSingleInPeriod and date:
            checker = self.getCheckerMaintenanceSingleInPeriod(maintenanceSingleInPeriod)
            if checker:
                if not checker(date, currentDate):
                    backGround = QVariant(QtGui.QColor(125, 125, 125))
        return backGround


    def getCheckerMaintenanceSingleInPeriod(self, value):
        def checkWeek(date, currentDate):
            iWeekDay = currentDate.dayOfWeek()
            monday   = currentDate.addDays(Qt.Monday-iWeekDay)
            sunday   = currentDate.addDays(Qt.Sunday-iWeekDay)
            return  monday <= date <= sunday

        def checkMonth(date, currentDate):
            monthDays = currentDate.daysInMonth()
            iDay      = currentDate.day()
            firstDay  = currentDate.addDays(1-iDay)
            lastDay   = currentDate.addDays(monthDays-iDay)
            return firstDay <= date <= lastDay

        def checkQuarter(date, currentDate):
            iMonth     = currentDate.month()
            iQuarter   = ((iMonth-1)/3)+1
            iInQuarter = iMonth-((iQuarter-1)*3)
            firstMonth = currentDate.addMonths(1-iInQuarter)
            lastMonth  = currentDate.addMonths(3-iInQuarter)
            firstDate  = QDate(firstMonth.year(), firstMonth.month(), 1)
            lastDate   = QDate(lastMonth.year(), lastMonth.month(), lastMonth.daysInMonth())
            return firstDate <= date <= lastDate

        def checkHalfYear(date, currentDate):
            iMonth     = currentDate.month()
            iHalf      = ((iMonth-1)/6)+1
            iInHalf    = iMonth-((iHalf-1)*6)
            firstMonth = currentDate.addMonths(1-iInHalf)
            lastMonth  = currentDate.addMonths(6-iInHalf)
            firstDate  = QDate(firstMonth.year(), firstMonth.month(), 1)
            lastDate   = QDate(lastMonth.year(), lastMonth.month(), lastMonth.daysInMonth())
            return firstDate <= date <= lastDate

        def checkYear(date, currentDate):
            firstDate = QDate(currentDate.year(), 1, 1)
            lastDate  = QDate(currentDate.year(), 12, 31)
            return firstDate <= date <= lastDate

        funcs = {1:checkWeek,
                 2:checkMonth,
                 3:checkQuarter,
                 4:checkHalfYear,
                 5:checkYear,
                }

        return funcs.get(value, None)
