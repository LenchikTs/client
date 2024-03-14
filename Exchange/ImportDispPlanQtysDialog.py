# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import Exchange.AttachService as AttachService

from library.DialogBase import CConstructHelperMixin
from library.InDocTable import CRecordListModel, CInDocTableCol, CEnumInDocTableCol
from library.Utils import *

from Ui_ImportDispPlanQtysDialog import Ui_ImportDispPlanQtysDialog

monthNamePlanQtys = (u'весь год', u'январь', u'февраль', u'март', u'апрель', u'май', u'июнь', u'июль', u'август', u'сентябрь', u'октябрь', u'ноябрь', u'декабрь')

class CImportDispPlanQtysDialog(QtGui.QDialog, CConstructHelperMixin, Ui_ImportDispPlanQtysDialog):
    kindNames = {
        1: u'Диспансеризация раз в 3 года',
        2: u'Профилактический осмотр',
        3: u'Диспансеризация раз в 2 года',
        4: u'Диспансеризация ежегодная',
        5: u'Диспансеризация углубленная (1 группа)',
        6: u'Диспансеризация углубленная (2 группа)'
    }

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('PlanQtys', CPlanQtysModel(self))
        self.setupUi(self)
        self.setModels(self.tblPlanQtys, self.modelPlanQtys, self.selectionModelPlanQtys)
        self.cmbOrgStructure.setTable('OrgStructure')
        self.cmbOrgStructure.setFilter(u"""
            length(OrgStructure.bookkeeperCode) = 5
            and exists (
                select *
                from OrgStructure as Child1
                    left join OrgStructure as Child2 on Child2.parent_id = Child1.id
                    left join OrgStructure as Child3 on Child3.parent_id = Child2.id
                    left join OrgStructure as Child4 on Child4.parent_id = Child3.id
                    left join OrgStructure as Child5 on Child5.parent_id = Child4.id
                where Child1.parent_id = OrgStructure.id
                    and (Child1.areaType in (1, 2)
                        or Child2.areaType in (1, 2)
                        or Child3.areaType in (1, 2)
                        or Child4.areaType in (1, 2)
                        or Child5.areaType in (1, 2)
                    )
            )
            """
            )
        self.cmbOrgStructure.setNameField(u"concat(bookkeeperCode, ' - ', name)")
        self.cmbOrgStructure.setOrder(u"bookkeeperCode, name")
        for kind, name in self.kindNames.iteritems():
            self.cmbKind.addItem(name, kind)
        self.btnClose.setAutoDefault(False)
        self.loadPreferences()
        self.update()

    def loadPreferences(self):
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), {})
        self.sbYear.setValue(getPrefInt(preferences, 'year', QDate.currentDate().year()))
        self.cmbOrgStructure.setValue(getPrefInt(preferences, 'orgStructure_id', 0))
        self.cmbKind.setCurrentIndex(getPrefInt(preferences, 'kindIndex', 0))

    def savePreferences(self):
        preferences = {}
        setPref(preferences, 'year', QVariant(self.sbYear.value()))
        setPref(preferences, 'orgStructure_id', QVariant(self.cmbOrgStructure.value()))
        setPref(preferences, 'kindIndex', QVariant(self.cmbKind.currentIndex()))
        setPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), preferences)

    def disableControls(self, disabled = True):
        self.sbYear.setDisabled(disabled)
        self.btnClose.setDisabled(disabled)
        QtGui.qApp.processEvents()

    def enableControls(self):
        self.disableControls(False)
    
    def update(self):
        db = QtGui.qApp.db
        self.modelPlanQtys.saveItems()
        year = self.sbYear.value()
        codeMo = db.translate('OrgStructure', 'id', self.cmbOrgStructure.value(), 'bookkeeperCode')
        kind = forceInt(self.cmbKind.itemData(self.cmbKind.currentIndex()))
        self.disableControls()
        try:
            self.modelPlanQtys.loadItems(year, codeMo, kind)
        finally:
            self.enableControls()

    def done(self, result):
        self.savePreferences()
        self.modelPlanQtys.saveItems()
        QtGui.QDialog.done(self, result)
    
    def getFromService(self):
        db = QtGui.qApp.db
        year = forceInt(self.sbYear.value())
        message = u"Плановые объемы за %d год по всем видам осмотров будут перезаписаны данными ТФОМС!\nПродолжить?" % year
        result = QtGui.QMessageBox.question(
            self,
            u'Внимание!',
            message,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No)
        if result != QtGui.QMessageBox.Yes:
            return
        self.modelPlanQtys.saveItems()
        self.modelPlanQtys.clearItems()
        self.disableControls()
        try:
            AttachService.getEvPlanQtys(year)
        finally:
            self.update()
            self.enableControls()

    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.reject()

    @pyqtSignature('')
    def on_btnGetFromService_clicked(self):
        self.getFromService()
        
    @pyqtSignature('int')
    def on_sbYear_valueChanged(self, value):
        self.update()
        
    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        self.update()
        
    @pyqtSignature('int')
    def on_cmbKind_currentIndexChanged(self, index):
        self.update()


class CQuantityInDocTableCol(CInDocTableCol):
    def __init__(self, parent, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        validator = QtGui.QIntValidator(parent)
        validator.setBottom(0)
        self.setValidator(validator)

    def setEditorData(self, editor, value, record):
        if value.isNull():
            editor.setText(u'')
        else:
            editor.setText(forceString(value))
        editor.selectAll()

    def getEditorData(self, editor):
        if editor.text():
            return QVariant(int(editor.text()))
        else:
            return QVariant(QVariant.Int)


class CPlanQtysModel(CRecordListModel):
    def __init__(self, parent):
        CRecordListModel.__init__(self, parent)
        self.addCol(CEnumInDocTableCol(u'Месяц', 'mnth', 20, monthNamePlanQtys)).setReadOnly()
        self.addCol(CQuantityInDocTableCol(self, u'Плановый объем', 'quantity', 20))
        self.tablePlanQtys = QtGui.qApp.db.table('disp_PlanQtys')

    def loadItems(self, year, codeMo, kind):
        db = QtGui.qApp.db
        items = []
        self.prevQtyByMonth = {}
        if year and codeMo and kind:
            cond = [
                self.tablePlanQtys['year'].eq(year),
                self.tablePlanQtys['code_mo'].eq(codeMo),
                self.tablePlanQtys['kind'].eq(kind),
            ]
            records = db.getRecordList(table=self.tablePlanQtys, cols='*', where=cond)
            itemsByMonth = {}
            if kind in (5, 6):
                validMonthFrom = 0
                validMonthTo = 0
            else:
                validMonthFrom = 1
                validMonthTo = 12
            for record in records:
                mnth = forceInt(record.value('mnth'))
                if validMonthFrom <= mnth <= validMonthTo:
                    itemsByMonth[mnth] = record
                    self.prevQtyByMonth[mnth] = forceInt(record.value('quantity'))
            for mnth in xrange(validMonthFrom, validMonthTo + 1):
                if mnth not in itemsByMonth:
                    newRecord = self.tablePlanQtys.newRecord()
                    newRecord.setValue('year', year)
                    newRecord.setValue('code_mo', codeMo)
                    newRecord.setValue('kind', kind)
                    newRecord.setValue('mnth', mnth)
                    itemsByMonth[mnth] = newRecord
                    self.prevQtyByMonth[mnth] = None
                items.append(itemsByMonth[mnth])
        self.setItems(items)
    
    def saveItems(self):
        db = QtGui.qApp.db
        for record in self._items:
            id = forceRef(record.value('id'))
            mnth = forceInt(record.value('mnth'))
            quantity = None if record.isNull('quantity') else forceInt(record.value('quantity'))
            if quantity is not None and self.prevQtyByMonth[mnth] != quantity:
                db.insertOrUpdate(self.tablePlanQtys, record)
            elif quantity is None and id:
                db.deleteRecord(self.tablePlanQtys, self.tablePlanQtys['id'].eq(id))