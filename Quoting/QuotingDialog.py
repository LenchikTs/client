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
from PyQt4.QtCore import Qt, QDate, QObject, QString, QVariant, pyqtSignature, SIGNAL

from library.database          import addCondLike
from library.DialogBase        import CDialogBase
from library.InDocTable        import CInDocTableModel, CInDocTableCol, CIntInDocTableCol
from library.ItemsListDialog   import CItemEditorBaseDialog
from library.TableModel        import CTableModel, CDateCol, CDesignationCol, CEnumCol, CNumCol, CRefBookCol, CTextCol
from library.Utils             import addDots, forceDate, forceInt, forceRef, forceString, forceStringEx, formatRecordsCount, toVariant, nameCase

from KLADR.kladrComboxes       import CKLADRComboBox, CKladrOkatoComboBox
from KLADR.KLADRModel          import CKladrTreeModel, getOKATO
from Quoting.EventsListDialog  import CEventsList
from Quoting.Utils             import getValueFromRecords
from RefBooks.QuotaType.List   import CQuotaTypeTreeModel
from Registry.ClientEditDialog import CClientEditDialog
from Registry.RegistryWindow   import contactToLikeMask
from Registry.Utils            import getClientAddress, getAddress, findKLADRRegionRecordsInQuoting, findDistrictRecordsInQuoting
from Reports.ReportView        import CReportViewDialog
from Users.Rights              import urAdmin, urRegTabReadEvents, urRegTabReadRegistry, urRegTabWriteEvents, urRegTabWriteRegistry

from Quoting.Ui_QuotingDialog       import Ui_QuotingDialog
from Quoting.Ui_QuotingEditorDialog import Ui_QuotingEditorDialog


class CQuotingDialog(CDialogBase, Ui_QuotingDialog):

    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.splitter_4.setChildrenCollapsible(False)

        self.listEditableWidgets = [
                                    self.btnEditQuota,
                                    self.btnProlongateQuota,
                                    self.btnNewQuota
                                    ]

        self.quotingId = None
        colsQuotaTypeLeaves = [
                               CEnumCol(u'Класс', ['class'],  [u'ВТМП', u'СМП', u'Родовой сертификат', u'Платные', u'ОМС', u'СКЛ'], 10),
#                               CQuotaTypeRefBookCol(u'Вид',   ['group_code'], 'QuotaType', 10),
                               CTextCol(   u'Код',            ['code'], 20),
                               CTextCol(   u'Наименование',   ['name'], 40)]
        colsQuoting         = [
                               CDateCol(u'Начало квотирования',    ['beginDate'], 20),
                               CDateCol(u'Окончание квотирования', ['endDate'], 20),
                               CRefBookCol(u'Наименование',        ['quotaType_id'], 'QuotaType', 255, 2),
                               CNumCol(u'Предел',                  ['limitation'], 8),
                               CNumCol(u'Использовано',            ['used'], 8),
                               CNumCol(u'Подтверждено',            ['confirmed'], 8),
                               CNumCol(u'В очереди',               ['inQueue'], 8)]

        colsPeopleList      = [
                               CDesignationCol(u'Фамилия',       ['master_id'],  ('Client', 'lastName'),   20),
                               CDesignationCol(u'Имя',           ['master_id'], ('Client', 'firstName'),  20),
                               CDesignationCol(u'Отчество',      ['master_id'],  ('Client', 'patrName'),  20),
                               CDesignationCol(u'Дата рождения', ['master_id'], ('Client', 'birthDate'),  20),
                               CDesignationCol(u'Вид квоты',     ['quotaType_id'], ('QuotaType', 'code'), 16),
                               CTextCol(u'Код МКБ',              ['MKB'], 8),
                               CNumCol(u'Этап',                  ['stage'], 2),
                               CEnumCol(u'Статус', ['status'],   [u'Отменено',
                                                                  u'Ожидание',
                                                                  u'Активный талон',
                                                                  u'Талон для заполнения',
                                                                  u'Заблокированный талон',
                                                                  u'Отказано',
                                                                  u'Необходимо согласовать дату обслуживания',
                                                                  u'Дата обслуживания на согласовании',
                                                                  u'Дата обслуживания согласована',
                                                                  u'Пролечен',
                                                                  u'Обслуживание отложено',
                                                                  u'Отказ пациента',
                                                                  u'Импортировано из ВТМП'], 40),
                               CDesignationCol(u'Подразделение', ['orgStructure_id'],  ('OrgStructure', 'name'),   128),
                               CTextCol(u'Номер талона',         ['quotaTicket'], 20),
                               CTextCol(u'Идентификатор',        ['identifier'], 20),
                               COKATOCol(u'Район',               ['districtCode'], 20),
                               CDesignationCol(u'ЛПУ направления',['org_id'],  ('Organisation', 'shortName'),   128),
                               ]

        self.quotaTypeOrder = ['class', 'group_code', 'code', 'name', 'id']
        self.quotingOrder   = ['beginDate', 'endDate']
        self.addModels('QuotaType', CQuotaTypeTreeModel(self, 'QuotaType', 'id', 'group_code', 'name', 'class', self.quotaTypeOrder))
        self.addModels('QuotaTypeLeaves', CTableModel(self, colsQuotaTypeLeaves, 'QuotaType'))
        self.addModels('Quoting', CTableModel(self, colsQuoting, 'Quoting'))
        self.addModels('Quoting_Region', CQuoting_RegionModel(self))
        self.addModels('Quoting_District', CQuoting_DistrictModel(self))
        self.addModels('PeopleList', CTableModel(self, colsPeopleList, 'Client_Quoting'))

        self.modelQuotaType.filterClassByExists(True)
        self.modelQuotaType.setLeavesVisible(False)

        self.setModels(self.treeQuotaType, self.modelQuotaType, self.selectionModelQuotaType)
        self.setModels(self.tblQuotaTypeLeaves, self.modelQuotaTypeLeaves, self.selectionModelQuotaTypeLeaves)
        self.setModels(self.tblQuoting, self.modelQuoting, self.selectionModelQuoting)
        self.setModels(self.tblQuoting_Region, self.modelQuoting_Region, self.selectionModelQuoting_Region)
        self.setModels(self.tblQuoting_District, self.modelQuoting_District, self.selectionModelQuoting_District)
        self.setModels(self.tblPeopleList, self.modelPeopleList, self.selectionModelPeopleList)

        #actions
        self.actRecountLimits    = QtGui.QAction(u'Пересчитать', self.tblQuoting)
        self.actEditClient       = QtGui.QAction(u'Открыть регистрационную карточку', self.tblPeopleList)
        self.actEditClientEvents = QtGui.QAction(u'Открыть события', self.tblPeopleList)
        self.tblQuoting.addPopupAction(self.actRecountLimits)
        self.tblPeopleList.addPopupAction(self.actEditClient)
        self.tblPeopleList.addPopupAction(self.actEditClientEvents)

        #connects
        self.connect(self.actRecountLimits, SIGNAL('triggered()'), self.recountLimitsAll)
        self.connect(self.actEditClient, SIGNAL('triggered()'), self.openClientCardFromAction)
        self.connect(self.actEditClientEvents, SIGNAL('triggered()'), self.openClientEventsFromAction)
        self.connect(self.tblPeopleList._popupMenu, SIGNAL('aboutToShow'), self.checkActionsRights)
        #smth
        model = CKladrTreeModel(None)
        model.setAllSelectable(True)
        self.cmbFilterAddressCity._model = model
        self.cmbFilterAddressCity.setModel(model)
        self.cmbFilterAddressCity._popupView.treeModel = model
        self.cmbFilterAddressCity._popupView.treeView.setModel(model)
        self.treeQuotaType.expand(self.modelQuotaType.index(0, 0))
        self.makeTables()
        self.lblInfo.setWordWrap(True)
        self.setWindowTitle(u'Квотирование')
        self.renewTblQuotingAndSetTo()
        self.clientKLADRCodeCache = {}
        self.clientOKATOCodeCache = {}
        self.regionValuseTmp      = {}
        self.districtValuseTmp    = {}
        for i in range(2, 6):
            self.tabWidgetLimitation.setTabEnabled(i, False)
        self.tabWidgetLimitation.setEnabled(False)
        self._isEditable = True
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.tblPeopleList.enableColsHide()
        self.tblPeopleList.enableColsMove()
        self.connect(self.selectionModelQuotaType,
                     SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
                     self.on_selectionModelQuotaType_currentChanged)
        self.connect(self.selectionModelQuotaTypeLeaves,
                     SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
                     self.on_selectionModelQuotaTypeLeaves_currentChanged)
        self.connect(self.selectionModelQuoting,
                     SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
                     self.on_selectionModelQuoting_currentChanged)
        self.connect(self.modelQuoting_Region,
                     SIGNAL('dataIsChanged()'), self.checkQuoting_RegionData)
        self.connect(self.modelQuoting_Region,
                     SIGNAL('dataChanged(QModelIndex, QModelIndex)'), self.saveTblQuoting_Region)
        self.connect(self.modelQuoting_Region,
                     SIGNAL('getMessage(QString)'), self.setLblInfoText)
        self.connect(self.modelQuoting_Region,
                     SIGNAL('regionAllRight()'), self.checkQuoting_RegionData)
        self.connect(self.modelQuoting_Region,
                     SIGNAL('recountQuotingRegionLimits()'), self.recountQuotingRegionLimitsByModelSignal)
        self.connect(self.modelQuoting_District,
                     SIGNAL('dataIsChanged()'), self.checkQuoting_DistrictData)
        self.connect(self.modelQuoting_District,
                     SIGNAL('dataChanged(QModelIndex, QModelIndex)'), self.saveTblQuoting_District)
        self.connect(self.modelQuoting_District,
                     SIGNAL('getMessage(QString)'), self.setLblInfoText)
        self.connect(self.modelQuoting_District,
                     SIGNAL('regionAllRight()'), self.checkQuoting_DistrictData)
        self.connect(self.modelQuoting_District,
                     SIGNAL('recountQuotingDistrictLimits()'), self.recountQuotingDistrictLimitsByModelSignal)


    @pyqtSignature('int')
    def on_tabWidgetLimitation_currentChanged(self, index):
        if index == 0:
            self.checkQuoting_RegionData()
        elif index == 1:
            self.checkQuoting_DistrictData()


    def setLblInfoText(self, val):
        self.lblInfo.setText(val)


    def exec_(self):
        self.setTableViewsSettings()
        return CDialogBase.exec_(self)


    def setEditable(self, val):
        self.modelQuoting_Region.setIsEditable(val)
        self._isEditable = val
        for obj in self.listEditableWidgets:
            obj.setEnabled(val)

    def isEditable(self):
        return self._isEditable

    def setTableViewsSettings(self):
        #разрешение редактирвоания через контекстное меню
        if self.isEditable():
            #Контекстное меню tblQuoting
            self.tblQuoting.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            self.actSelectAllRowQuoting = QtGui.QAction(u'Выделить все строки', self)
            self.tblQuoting.addPopupAction(self.actSelectAllRowQuoting)
            self.connect(self.actSelectAllRowQuoting, SIGNAL('triggered()'), self.selectAllRowQuoting)

            self.actClearSelectionRowQuoting = QtGui.QAction(u'Снять выделение', self)
            self.tblQuoting.addPopupAction(self.actClearSelectionRowQuoting)
            self.connect(self.actClearSelectionRowQuoting, SIGNAL('triggered()'), self.clearSelectionRowQuoting)

            self.actDelSelectedRowsQuoting = QtGui.QAction(u'Удалить выделенные строки', self)
            self.tblQuoting.addPopupAction(self.actDelSelectedRowsQuoting)
            self.connect(self.actDelSelectedRowsQuoting, SIGNAL('triggered()'), self.delSelectedRowsQuoting)

            #Контекстное меню tblQuoting_Region
            self.tblQuoting_Region.addPopupSelectAllRow()
            self.tblQuoting_Region.addPopupClearSelectionRow()
            self.actDelSelectedRowsQuoting_Region = QtGui.QAction(u'Удалить выделенные строки', self)
            self.tblQuoting_Region.popupMenu().addAction(self.actDelSelectedRowsQuoting_Region)
            self.connect(self.actDelSelectedRowsQuoting_Region, SIGNAL('triggered()'), self.delSelectedRowsQuoting_Region)

            self.actFillRegions = QtGui.QAction(u'Добавить регионы', self)
            self.tblQuoting_Region.popupMenu().addAction(self.actFillRegions)
            self.connect(self.actFillRegions, SIGNAL('triggered()'), self.fillRegionsIntoTblQuoting_Region)

            #Контекстное меню tblQuoting_District
            self.tblQuoting_District.addPopupSelectAllRow()
            self.tblQuoting_District.addPopupClearSelectionRow()
            self.actDelSelectedRowsQuoting_District = QtGui.QAction(u'Удалить выделенные строки', self)
            self.tblQuoting_District.popupMenu().addAction(self.actDelSelectedRowsQuoting_District)
            self.connect(self.actDelSelectedRowsQuoting_District, SIGNAL('triggered()'), self.delSelectedRowsQuoting_District)

            self.actFillDistricts = QtGui.QAction(u'Добавить районы', self)
            self.tblQuoting_District.popupMenu().addAction(self.actFillDistricts)
            self.connect(self.actFillDistricts, SIGNAL('triggered()'), self.fillDistrictsIntoTblQuoting_District)

            self.connect(self.tblQuoting_Region.popupMenu(), SIGNAL('aboutToShow()'), self.checkQuoting_RegionActionPosibility)
            self.connect(self.tblQuoting_District.popupMenu(), SIGNAL('aboutToShow()'), self.checkQuoting_DistrictActionPosibility)
            self.connect(self.tblQuoting.popupMenu(), SIGNAL('aboutToShow()'), self.checkQuotingActionPosibility)


    def selectAllRowQuoting(self):
        self.tblQuoting.selectAll()


    def clearSelectionRowQuoting(self):
        self.tblQuoting.clearSelection()


    def delSelectedRowsQuoting(self):
        db = QtGui.qApp.db
        selectedIdList = self.tblQuoting.selectedItemIdList()
        if QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                                    u'Вы уверены что хотите удалить выделенные строки?(количество строк: %d)'% len(selectedIdList),
                                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No
                                    ) == QtGui.QMessageBox.Yes:
            table = db.table('Quoting')
            for id in selectedIdList:
                record = db.getRecord(table, ['id','deleted'], id)
                record.setValue('deleted', QVariant(1))
                db.updateRecord(table, record)
        self.modelQuoting.setIdList(self.selectTblQuoting())


    def delSelectedRowsQuoting_Region(self):
        if QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                                    u'Вы уверены что хотите удалить выделенные строки?',
                                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No
                                    ) == QtGui.QMessageBox.Yes:
            selectedIdList = self.getSelectedIdListTblQuoting_Region()
            db = QtGui.qApp.db
            table = db.table('Quoting_Region')
            for id in selectedIdList:
                record = db.getRecord(table, ['id','deleted'], id)
                record.setValue('deleted', QVariant(1))
                db.updateRecord(table, record)
            quotingId = self.tblQuoting.currentItemId()
            if quotingId:
                self.loadTblQuoting_Region(quotingId)


    def getSelectedIdListTblQuoting_Region(self):
        resume = []
        rows = self.tblQuoting_Region.getSelectedRows()
        items = self.modelQuoting_Region.items()
        for row in rows:
            item = items[row]
            id = forceRef(item.value('id'))
            if id:
                resume.append(id)
            else:
                self.modelQuoting_Region.removeRow(row)
        return resume


    def delSelectedRowsQuoting_District(self):
        if QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                                    u'Вы уверены что хотите удалить выделенные строки?',
                                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No
                                    ) == QtGui.QMessageBox.Yes:
            selectedIdList = self.getSelectedIdListTblQuoting_District()
            db = QtGui.qApp.db
            table = db.table('Quoting_District')
            for id in selectedIdList:
                record = db.getRecord(table, ['id','deleted'], id)
                record.setValue('deleted', QVariant(1))
                db.updateRecord(table, record)
            quotingId = self.tblQuoting.currentItemId()
            if quotingId:
                self.loadTblQuoting_District(quotingId)


    def getSelectedIdListTblQuoting_District(self):
        resume = []
        rows = self.tblQuoting_District.getSelectedRows()
        items = self.modelQuoting_District.items()
        for row in rows:
            item = items[row]
            id = forceRef(item.value('id'))
            if id:
                resume.append(id)
            else:
                self.modelQuoting_District.removeRow(row)
        return resume


    def fillRegionsIntoTblQuoting_Region(self):
        quotingId = self.tblQuoting.currentItemId()
        if quotingId:
            db = QtGui.qApp.db
            items = self.loadRegionItems()
            existsItemsCode = getValueFromRecords(self.modelQuoting_Region.items(), 'region_code')
            for code in items:
                if code in existsItemsCode:
                    continue
                record = db.table('Quoting_Region').newRecord()
                record.setValue('region_code', QVariant(code))
                record.setValue('master_id', QVariant(quotingId))
                db.insertRecord('Quoting_Region', record)
            self.modelQuoting_Region.setResume(None)
            self.recountLimits(False)


    def loadRegionItems(self):
        return getValueFromRecords(QtGui.qApp.db.getRecordList(self.tableKLADR, 'CODE',
                                       'parent=\'\' AND RIGHT(CODE,2)=\'00\'',
                                       'NAME, SOCR, CODE'), 'CODE')


    def fillDistrictsIntoTblQuoting_District(self):
        quotingId = self.tblQuoting.currentItemId()
        if quotingId:
            db = QtGui.qApp.db
            items = self.loadDistrictItems()
            existsItemsCode = getValueFromRecords(self.modelQuoting_District.items(), 'district_code')
            for item in items:
                okatoCode = forceString(item.value('okatoCode'))
                kladrCode = forceString(item.value('kladrCode')) + '0'*11
                if okatoCode in existsItemsCode:
                    continue
                record = db.table('Quoting_District').newRecord()
                record.setValue('region_code', QVariant(kladrCode))
                record.setValue('district_code', QVariant(okatoCode))
                record.setValue('master_id', QVariant(quotingId))
                db.insertRecord('Quoting_District', record)
            self.modelQuoting_District.setResume(None)
            self.recountLimitDistricts(False)


    def loadDistrictItems(self):
        filterCode = forceString(QtGui.qApp.db.translate('kladr.KLADR', 'CODE', forceString(self.cmbQuotaKladr.itemData(self.cmbQuotaKladr.currentIndex())), 'OCATD'))[:2] if self.cmbQuotaKladr.currentIndex() else ''
        db = QtGui.qApp.db
        queryTable = 'kladr.KLADR INNER JOIN kladr.OKATO ON kladr.OKATO.P0=LEFT(kladr.KLADR.OCATD, 2)'
        return db.getRecordList(queryTable, 'DISTINCT kladr.OKATO.CODE AS okatoCode, LEFT(kladr.KLADR.CODE, 2) AS kladrCode',
                                       '%skladr.OKATO.P1 != \'\' AND kladr.OKATO.P2 = \'\'' % (('kladr.OKATO.P0=\'%s\' AND '%(filterCode)) if filterCode else ''),
                                       'kladr.OKATO.NAME, kladr.OKATO.P0, kladr.OKATO.infis, kladr.OKATO.CODE')


    def checkQuoting_RegionActionPosibility(self):
        self.checkActionPosibility([self.actDelSelectedRowsQuoting_Region],
                              self.tblQuoting_Region)


    def checkQuoting_DistrictActionPosibility(self):
        self.checkActionPosibility([self.actDelSelectedRowsQuoting_District],
                                    self.tblQuoting_District)


    def checkQuotingActionPosibility(self):
        self.checkActionPosibility([self.actDelSelectedRowsQuoting,
                                    self.actClearSelectionRowQuoting,
                                    self.actRecountLimits],
                                    self.tblQuoting)


    def checkActionPosibility(self, actions, table):
        if table == self.tblQuoting:
            b = bool(table.selectedItemIdList())
        elif table == self.tblQuoting_Region:
            b = bool(self.tblQuoting_Region.getSelectedRows())
        elif table == self.tblQuoting_District:
            b = bool(self.tblQuoting_District.getSelectedRows())
        for action in actions:
            action.setEnabled(b)


    def getQuotingRecordById(self, id):
        return QtGui.qApp.db.getRecord('Quoting', '*', id)


    def recountLimitsAll(self, clearItems=True):
        self.recountLimits(clearItems)
        self.recountLimitDistricts(clearItems)


    def recountLimits(self, clearItems=True):
        QtGui.qApp.setWaitCursor()
        self.clientKLADRCodeCache = {}
        self.clientOKATOCodeCache = {}
        idList = self.tblQuoting.selectedItemIdList()
        if idList:
            for id in idList:
                self.regionValuseTmp = {}
                record = self.getQuotingRecordById(id)
#                allChildListId = self.getActualQuotaTypeListId([forceRef(record.value('quotaType_id'))])
#                actualChildListId = [chId for chId in allChildListId if chId not in idList]
                self.recountLimitsForRecord(record)
                self.recountRegionLimitsForRecord(record)
                self.modelQuoting.invalidateRecordsCache()
        else:
            id = None
        if clearItems:
            idListQR = self.modelQuoting_Region.itemIdList()
            if idListQR:
                db = QtGui.qApp.db
                table = db.table('Quoting_Region')
                db.markRecordsDeleted(table, [table['master_id'].inlist(idListQR)])
            self.modelQuoting_Region.loadItems(None)
            self.modelQuoting_Region.setResume(None)
        else:
            self.modelQuoting_Region.loadItems(id)
        self.checkQuoting_RegionData()
        QtGui.qApp.restoreOverrideCursor()


    def recountQuotingRegionLimitsByModelSignal(self):
        self.recountLimits(False)


    def recountRegionLimitsForRecord(self, record):
        db = QtGui.qApp.db
        for code in self.regionValuseTmp.keys():
            actualRecords = findKLADRRegionRecordsInQuoting(code, record)
            for actualRecord in actualRecords:
                used      = self.regionValuseTmp[code]['used']
                confirmed = self.regionValuseTmp[code]['confirmed']
                inQueue   = self.regionValuseTmp[code]['inQueue']
                actualRecord.setValue('used', QVariant(used))
                actualRecord.setValue('confirmed', QVariant(confirmed))
                actualRecord.setValue('inQueue', QVariant(inQueue))
                db.updateRecord('Quoting_Region', actualRecord)


    def recountLimitsForRecord(self, record):
        beginDate      = forceDate(record.value('beginDate'))
        endDate        = forceDate(record.value('endDate'))
        quotaTypeId    = forceInt(record.value('quotaType_id'))
#        dateTimeUnknow = '0000-00-00T00:00:00'
        db = QtGui.qApp.db
        table = db.table('Client_Quoting')
        cond = [table['dateRegistration'].le(endDate),
                table['deleted'].eq(0)]
        cond.append(db.joinOr([table['dateEnd'].ge(beginDate),
                    'Client_Quoting.`dateEnd`=\'0000-00-00T00:00:00\'']))
        cond.append(table['deleted'].eq(0))
        clientQuotingRecordList = self.getClientQuotingRecordList(table, cond, quotaTypeId)
        if not clientQuotingRecordList:
            allChildListId = self.getActualQuotaTypeListId([quotaTypeId])
#            childrenTypesInQuoting       = self.getChildrenTypesInQuoting(beginDate, endDate, allChildListId)
            childrenTypesInClientQuoting = self.getChildrenTypesInClientQuoting(table, cond, allChildListId)
            used, confirmed, inQueue = self.getUsedConfirmedInQueueFromChildren(db, table, cond, quotaTypeId, childrenTypesInClientQuoting, record)#, childrenTypesInQuoting)
        else:
            used, confirmed, inQueue = self.getUsedConfirmedInQueueFromRecordList(clientQuotingRecordList, record)
        record.setValue('used', QVariant(used))
        record.setValue('confirmed', QVariant(confirmed))
        record.setValue('inQueue', QVariant(inQueue))
        db.updateRecord('Quoting', record)


    def getChildrenTypesInClientQuoting(self, table, cond, allChildListId):
        db = QtGui.qApp.db
        condTmp = list(cond)
        condTmp.append(table['quotaType_id'].inlist(allChildListId))
        return db.getIdList(table, 'quotaType_id', condTmp)


    def getChildrenTypesInQuoting(self, beginDate, endDate, allChildListId):
        db = QtGui.qApp.db
        tableQuoting = self.tableQuoting
        cond = [db.joinOr([db.joinAnd([tableQuoting['beginDate'].le(beginDate),
                                       tableQuoting['endDate'].ge(beginDate)]),
                           db.joinAnd([tableQuoting['beginDate'].le(endDate),
                                       tableQuoting['endDate'].ge(endDate)])])]
        cond.append(tableQuoting['deleted'].eq(0))
        cond.append(tableQuoting['quotaType_id'].inlist(allChildListId))
        return db.getIdList(tableQuoting, 'quotaType_id', cond)


    def recountLimitDistricts(self, clearItems=True):
        QtGui.qApp.setWaitCursor()
        self.clientKLADRCodeCache = {}
        self.clientOKATOCodeCache = {}
        idList = self.tblQuoting.selectedItemIdList()
        if idList:
            for id in idList:
                self.districtValuseTmp = {}
                record = self.getQuotingRecordById(id)
                self.recountLimitsForRecord(record)
                self.recountDistrictLimitsForRecord(record)
                self.modelQuoting.invalidateRecordsCache()
        else:
            id = None
        if clearItems:
            idListQD = self.modelQuoting_District.itemIdList()
            if idListQD:
                db = QtGui.qApp.db
                table = db.table('Quoting_District')
                db.markRecordsDeleted(table, [table['master_id'].inlist(idListQD)])
            self.modelQuoting_District.loadItems(None)
            self.modelQuoting_District.setResume(None)
        else:
            self.modelQuoting_District.loadItems(id)
        self.checkQuoting_DistrictData()
        QtGui.qApp.restoreOverrideCursor()


    def recountQuotingDistrictLimitsByModelSignal(self):
        self.recountLimitDistricts(False)


    def recountDistrictLimitsForRecord(self, record):
        db = QtGui.qApp.db
        for codes in self.districtValuseTmp.keys():
            actualRecords = findDistrictRecordsInQuoting(codes, record)
            for actualRecord in actualRecords:
                used      = self.districtValuseTmp[codes]['used']
                confirmed = self.districtValuseTmp[codes]['confirmed']
                inQueue   = self.districtValuseTmp[codes]['inQueue']
                actualRecord.setValue('used', QVariant(used))
                actualRecord.setValue('confirmed', QVariant(confirmed))
                actualRecord.setValue('inQueue', QVariant(inQueue))
                db.updateRecord('Quoting_District', actualRecord)


    def getClientQuotingRecordList(self, table, cond, quotaTypeId):
        condTmp = list(cond)
        condTmp.append(table['quotaType_id'].eq(quotaTypeId))
        return QtGui.qApp.db.getRecordList(table, '*', condTmp)


    def getUsedConfirmedInQueueFromRecordList(self, recordList, quotingRecord):
        used = confirmed = inQueue = 0
        for record in recordList:
            status = self.translateStatusToColumn(forceInt(record.value('status')))
            amount = forceInt(record.value('amount'))
            clientId = forceInt(record.value('master_id'))
            quotaKladrCode = forceString(record.value('regionCode'))
            quotaOKATOCode = forceString(record.value('districtCode'))
            if quotaKladrCode:
                clientKLADRCode = quotaKladrCode
            else:
                clientKLADRCode = self.clientKLADRCodeCache.get(clientId, None)
            if quotaOKATOCode:
                clientOKATOCode = quotaOKATOCode
            else:
                clientOKATOCode = self.clientOKATOCodeCache.get(clientId, None)
            if not clientKLADRCode:
                regAddressRecord = getClientAddress(clientId, 0)
                if regAddressRecord:
                    addressId = forceRef(regAddressRecord.value('address_id'))
                    regAddress = getAddress(addressId)
                    clientKLADRCode = regAddress.KLADRCode
                    self.clientKLADRCodeCache[clientId] = clientKLADRCode
                    if not clientOKATOCode:
                        KLADRStreetCode = regAddress.KLADRStreetCode
                        number = regAddress.number
                        clientOKATOCode = getOKATO(clientKLADRCode, KLADRStreetCode, number)
                    self.clientOKATOCodeCache[clientId] = (clientKLADRCode, clientOKATOCode)
            if clientKLADRCode:
                regionValuesTmp = self.regionValuseTmp.get(clientKLADRCode, None)
                if not regionValuesTmp:
                    regionValuesTmp = {'used':0, 'confirmed':0, 'inQueue':0}
                if clientOKATOCode:
                    districtValuseTmp = self.districtValuseTmp.get((clientKLADRCode, clientOKATOCode), None)
                    if not districtValuseTmp:
                        districtValuseTmp = {'used':0, 'confirmed':0, 'inQueue':0}
            if status == 'used':
                used += amount
            if status == 'confirmed':
                confirmed += amount
            if status == 'inQueue':
                inQueue += amount
            if clientKLADRCode and status:
                regionValuesTmp[status] += amount
                self.regionValuseTmp[clientKLADRCode] = regionValuesTmp
                if clientOKATOCode and status:
                    districtValuseTmp[status] += amount
                    self.districtValuseTmp[(clientKLADRCode, clientOKATOCode)] = districtValuseTmp
        return used, confirmed, inQueue


    def getUsedConfirmedInQueueFromChildren(self, db, table, cond, parentId, childrenTypesInClientQuoting, record):
        condTmp = list(cond)
        condTmp.append(table['quotaType_id'].inlist(childrenTypesInClientQuoting))
#        condTmp.append(table['quotaType_id'].notInlist(childrenTypesInQuoting))
        recordList = QtGui.qApp.db.getRecordList(table, '*', condTmp)
        return self.getUsedConfirmedInQueueFromRecordList(recordList, record)


    def translateStatusToColumn(self, status):
        if status == 9:
            return 'used'
        if status == 8:
            return 'confirmed'
        if status in (1, 2, 3, 4, 6, 7, 10, 12):
            return 'inQueue'
        return None


    def makeTables(self):
        db = QtGui.qApp.db
        self.tableQuoting   = db.table('Quoting')
        self.tableQuotaType = db.table('QuotaType')
        self.tableKLADR     = db.table('kladr.KLADR')
        self.tableOKATO     = db.table('kladr.OKATO')


    def selectQuotaTypeLeaves(self):
        db = QtGui.qApp.db
        table = self.modelQuotaTypeLeaves.table()
        cond = []
        groupId = self.currentGroupId()
        groupCond = db.translate(table, 'id', groupId, 'code')
        className = self.currentClass()
        cond = [ table['group_code'].eq(groupCond) ]
        cond.append(table['deleted'].eq(0))
        cond.append(table['class'].eq(className))
        list = db.getIdList(table.name(),
                           'id',
                           cond,
                           self.quotaTypeOrder)
        return list


    def getQuotaTypeListIdForTblQuoting(self):
        db = QtGui.qApp.db
        id = self.getActualQuotaTypeId()
        result = []
        actualIdList = [id] if id else []
        if actualIdList:
            while actualIdList:
                tmpActualIdList = []
                for id in actualIdList:
                    result.append(id)
                    group_code = db.translate(self.tableQuotaType, 'id', id, 'code')
                    tmpActualIdList.extend(db.getIdList(self.tableQuotaType, 'id', self.tableQuotaType['group_code'].eq(group_code)))
                actualIdList = tmpActualIdList
        else:
            _class = self.currentClass()
            if _class is not None:
                result = db.getIdList(self.tableQuotaType, 'id', self.tableQuotaType['class'].eq(_class))
        return result


    def selectTblQuoting(self):
        cond = []
        actualIdList = self.getQuotaTypeListIdForTblQuoting()
        if actualIdList:
            cond.append(self.tableQuoting['quotaType_id'].inlist(actualIdList))
        selectedDate = self.calendar.selectedDate().toPyDate()
        cond.append(self.tableQuoting['beginDate'].le(selectedDate))
        cond.append(self.tableQuoting['endDate'].ge(selectedDate))
        cond.append(self.tableQuoting['deleted'].eq(0))
        list = QtGui.qApp.db.getIdList(self.tableQuoting, 'id', cond, self.quotingOrder)
        return list


    def loadTblQuoting_Region(self, quotingId):
        self.modelQuoting_Region.loadItems(quotingId)
        self.checkQuoting_RegionData()


    def saveTblQuoting_Region(self):
        if self.quotingId:
            self.modelQuoting_Region.saveItems(self.quotingId)


    def checkQuoting_RegionData(self):
        resume   = self.modelQuoting_Region.resume()
        masterId = self.tblQuoting.currentItemId()
        db = QtGui.qApp.db
        if not resume:
            stmt = 'SELECT SUM(limitation) AS sumLimitation, SUM(used) AS sumUsed, SUM(confirmed) AS sumConfirmed, SUM(inQueue) AS sumInQueue FROM Quoting_Region WHERE deleted = 0 AND master_id = %d' % masterId
            query = db.query(stmt)
            resume = {}
            if query.first():
                record = query.record()
                limitation = forceInt(record.value('sumLimitation'))
                used       = forceInt(record.value('sumUsed'))
                confirmed  = forceInt(record.value('sumConfirmed'))
                inQueue    = forceInt(record.value('sumInQueue'))
                resume = {'limitation':limitation,
                          'used':used,
                          'confirmed':confirmed,
                          'inQueue':inQueue}
            self.modelQuoting_Region.setResume(resume)
        sum = resume['used']+resume['confirmed']+resume['inQueue']
        limitation = resume['limitation']
        masterQuotaLimit = forceInt(db.translate(self.tableQuoting, 'id', masterId, 'limitation'))
        addMasterLimitLessLimitation = masterQuotaLimit<limitation
        if  limitation < sum:
            msg = u'<FONT COLOR=#FF0000>Общий предел по регионам: %d</FONT> | Сумма составляющих: %d' % (limitation,sum)
        else:
            msg = u'Общий предел по регионам: %d' % limitation
        if addMasterLimitLessLimitation:
            msg += u' | <FONT COLOR=#FF0000>Предел данной квоты меньше чем по регионам: %d</FONT>' %masterQuotaLimit
        self.setLblInfoText(msg)


    def loadTblQuoting_District(self, quotingId):
        self.modelQuoting_District.loadItems(quotingId)
        self.checkQuoting_DistrictData()


    def saveTblQuoting_District(self):
        if self.quotingId:
            self.modelQuoting_District.saveItems(self.quotingId)


    def checkQuoting_DistrictData(self):
        resume   = self.modelQuoting_District.resume()
        masterId = self.tblQuoting.currentItemId()
        db = QtGui.qApp.db
        if not resume:
            stmt = 'SELECT SUM(limitation) AS sumLimitation, SUM(used) AS sumUsed, SUM(confirmed) AS sumConfirmed, SUM(inQueue) AS sumInQueue FROM Quoting_District WHERE deleted = 0 AND master_id = %d' % masterId
            query = db.query(stmt)
            resume = {}
            if query.first():
                record = query.record()
                limitation = forceInt(record.value('sumLimitation'))
                used       = forceInt(record.value('sumUsed'))
                confirmed  = forceInt(record.value('sumConfirmed'))
                inQueue    = forceInt(record.value('sumInQueue'))
                resume = {'limitation':limitation,
                          'used':used,
                          'confirmed':confirmed,
                          'inQueue':inQueue}
            self.modelQuoting_District.setResume(resume)
        sum = resume['used']+resume['confirmed']+resume['inQueue']
        limitation = resume['limitation']
        masterQuotaLimit = forceInt(db.translate(self.tableQuoting, 'id', masterId, 'limitation'))
        addMasterLimitLessLimitation = masterQuotaLimit<limitation
        if  limitation < sum:
            msg = u'<FONT COLOR=#FF0000>Общий предел по районам: %d</FONT> | Сумма составляющих: %d' % (limitation,sum)
        else:
            msg = u'Общий предел по районам: %d' % limitation
        if addMasterLimitLessLimitation:
            msg += u' | <FONT COLOR=#FF0000>Предел данной квоты меньше чем по районам: %d</FONT>' %masterQuotaLimit
        self.setLblInfoText(msg)


    def currentGroupId(self):
        return self.modelQuotaType.itemId(self.treeQuotaType.currentIndex())


    def currentClass(self):
        return self.modelQuotaType.itemClass(self.treeQuotaType.currentIndex())


    def renewTblQuotingAndSetTo(self, itemId=None):
        list = self.selectTblQuoting()
        self.modelQuoting.setIdList(list)
        if itemId and itemId in list:
            row = list.index(itemId)
            self.tblQuoting.setCurrentRow(row)
            self.setRegionsForQuoting(itemId)
        else:
            self.selectionModelQuoting.clear()
            self.setRegionsForQuoting(None)
            self.tblQuoting.setCurrentRow(0)



    def getActualQuotaTypeId(self):
        leavesId = self.tblQuotaTypeLeaves.currentItemId()
        if leavesId:
            return leavesId
        else:
            groupId  = self.currentGroupId()
            if groupId:
                return groupId
        return None


    def getActualQuotaTypeListId(self, idList='None'):
        db = QtGui.qApp.db
        if idList == 'None':
            id = self.getActualQuotaTypeId()
            idList = [id] if id else []
        if not idList:
            currentClass = self.currentClass()
            if currentClass is not None:
                return db.getIdList(self.tableQuotaType, 'id',
                                    self.tableQuotaType['class'].eq(currentClass))
            else:
                return []
        list = []
        for id in idList:
            group_code = db.translate(self.tableQuotaType, 'id', id, 'code')
            childIdList = db.getIdList(self.tableQuotaType, 'id',
                                       self.tableQuotaType['group_code'].eq(group_code))
            list += self.getActualQuotaTypeListId(childIdList) + childIdList
        return idList + list


    def setRegionsForQuoting(self, quotingId):
        if self.quotingId != quotingId:
            self.modelQuoting_Region.setResume(None)
            self.modelQuoting_District.setResume(None)
            self.quotingId = quotingId
            if quotingId:
                self.loadTblQuoting_Region(quotingId)
                self.loadTblQuoting_District(quotingId)
#                self.tblQuoting_Region.setEnabled(True)
                self.tabWidgetLimitation.setEnabled(True)
            else:
                self.modelQuoting_Region.reset()
                self.modelQuoting_District.reset()
#                self.tblQuoting_Region.setEnabled(False)
                self.tabWidgetLimitation.setEnabled(False)
                self.lblInfo.clear()


    def getEditor(self, props={}):
        editor = CQuotingEditorDialog(self)
        editor.setProps(props)
        return editor


    def addNewQuota(self, editor):
        try:
            if editor.exec_():
                beginDate = editor.edtBeginDate.date()
                endDate   = editor.edtEndDate.date()
                itemId    = editor.itemId()
                record = self.getQuotingRecordById(itemId)
                self.recountLimitsForRecord(record)
                self.renewTblQuotingAndDateAndSetTo(itemId,
                                             self.createCurrentCalendarDate(beginDate, endDate))
        finally:
            editor.deleteLater()


    def editQuota(self, editor):
        itemId = self.tblQuoting.currentItemId()
        if itemId:
            try:
                editor.load(itemId)
                if editor.exec_():
                    itemId = editor.itemId()
                    record = self.getQuotingRecordById(itemId)
                    self.recountLimitsForRecord(record)
                    self.renewTblQuotingAndSetTo(itemId)
            finally:
                editor.deleteLater()
        else:
            self.on_btnNewQuota_clicked()


    def createNewDates(self):
        currentDate = self.calendar.selectedDate()
        m = currentDate.month()
        y = currentDate.year()
        beginDate = QDate(y, m, 1)
        return beginDate, currentDate


    def createCurrentCalendarDate(self, beginDate, endDate):
        dDays = beginDate.daysTo(endDate)/2
        dY = dDays/365
        dM = dDays%365/30
        dD = dDays%365%30
        y = beginDate.year()+dY
        m = beginDate.month()+dM
        d = beginDate.day()+dD
        if m > 12:
            y += 1
            m = m - 12
        dLimit = QDate(y, m, 1).daysInMonth()
        if d > dLimit:
            m += 1
            d = d - dLimit
            if m > 12:
                y += 1
                m = m - 12
        return QDate(y, m, d)


    def renewTblQuotingAndDateAndSetTo(self, itemId=None, date=None):
        if date:
            self.calendar.setSelectedDate(date)
        self.renewTblQuotingAndSetTo(itemId)


    def setTblPeopleListId(self):
        def calcBirthDate(cnt):
            result = QDate.currentDate()
            return result.addYears(-cnt)

        def addAddressCond(cond, addrType, addrIdList):
            tableClientAddress = db.table('ClientAddress')
            subcond = [tableClientAddress['client_id'].eqEx('`Client`.`id`'),
                       tableClientAddress['id'].eqEx('(SELECT MAX(`id`) FROM `ClientAddress` AS `CA` WHERE `CA`.`client_id` = `Client`.`id` AND `CA`.`type`=%d)' % addrType)
                      ]
            if addrIdList is None:
                subcond.append(tableClientAddress['address_id'].isNull())
            else:
                subcond.append(tableClientAddress['address_id'].inlist(addrIdList))
            cond.append(db.existsStmt(tableClientAddress, subcond))

        selectedDate = self.calendar.selectedDate()
        quotaTypeIdList = self.getActualQuotaTypeListId()
        db = QtGui.qApp.db
        table = self.modelPeopleList.table()
        tableClient = db.table('Client')
        condBottomDate = [table['dateRegistration'].le(selectedDate),
                          '(Client_Quoting.`dateRegistration`=\'0000-00-00T00:00:00\')']
        condUpDate     = [table['dateEnd'].ge(selectedDate),
                          '(Client_Quoting.`dateEnd`=\'0000-00-00T00:00:00\')']
        cond = [table['deleted'].eq(0),
                db.joinOr(condBottomDate),
                db.joinOr(condUpDate)]
        if quotaTypeIdList:
            cond.append(table['quotaType_id'].inlist(quotaTypeIdList))
        if self.chkFilterStatus.isChecked():
            cond.append(table['status'].eq(self.cmbFilterStatus.currentIndex()))
        if self.chkFilterStage.isChecked():
            cond.append(table['stage'].eq(self.edtFilterStage.value()))
        if self.chkFilterOrgStructure.isChecked():
            cond.append(table['orgStructure_id'].eq(self.cmbFilterOrgStructure.value()))
        if self.chkFilterIdentifier.isChecked():
            addCondLike(cond, table['identifier'], addDots(forceStringEx(self.edtFilterIdentifier.text())))
        if self.chkFilterTicketNumber.isChecked():
            addCondLike(cond, table['quotaTicket'], addDots(forceStringEx(self.edtFilterTicketNumber.text())))
        if self.chkFilterRequest.isChecked():
            cond.append(table['request'].eq(self.cmbFilterRequest.currentIndex()))
        if self.chkFilterClientQuotaKladr.isChecked():
            code = forceString(self.cmbFilterClientQuotaKladr.itemData(self.cmbFilterClientQuotaKladr.currentIndex()))
            if code:
                cond.append(table['regionCode'].eq(code))
            else:
                cond.append(table['regionCode'].isNull())
        if self.chkFilterClientQuotaOKATO.isChecked():
            codeDistrict = forceString(self.cmbFilterClientQuotaDistrictKladr.value())
            if codeDistrict:
                cond.append(table['districtCode'].eq(codeDistrict))
            else:
                cond.append(table['districtCode'].isNull())
        if self.chkQuotaLPUDirection.isChecked():
            LPUDirectionId = forceRef(self.cmbQuotaLPUDirection.value())
            if LPUDirectionId:
                cond.append(table['org_id'].eq(LPUDirectionId))
            else:
                cond.append(table['org_id'].isNull())
        if self.chkFilterLastName.isChecked() or self.chkFilterFirstName.isChecked() or self.chkFilterPatrName.isChecked() or self.chkFilterBirthDay.isChecked() or self.chkFilterSex.isChecked() or self.chkFilterAge.isChecked() or self.chkFilterContact.isChecked() or self.chkFilterAddress.isChecked():
            table = db.leftJoin(table, 'Client', 'Client_Quoting.`master_id`=Client.`id`')
            if self.chkFilterLastName.isChecked():
                addCondLike(cond, tableClient['lastName'],  addDots(forceStringEx(self.edtFilterLastName.text())))
            if self.chkFilterFirstName.isChecked():
                addCondLike(cond, tableClient['firstName'],  addDots(forceStringEx(self.edtFilterFirstName.text())))
            if self.chkFilterPatrName.isChecked():
                addCondLike(cond, tableClient['patrName'],  addDots(forceStringEx(self.edtFilterPatrName.text())))
            if self.chkFilterBirthDay.isChecked():
                cond.append(tableClient['birthDate'].eq(self.edtFilterBirthDay.date()))
            if self.chkFilterSex.isChecked():
                index = self.cmbFilterSex.currentIndex()
                if index:
                    cond.append(tableClient['sex'].eq(index))
            if self.chkFilterAge.isChecked():
                lowAge  = self.edtFilterBegAge.value()
                highAge = self.edtFilterEndAge.value()+1
                cond.append(tableClient['birthDate'].le(calcBirthDate(lowAge)))
                cond.append(tableClient['birthDate'].ge(calcBirthDate(highAge)))
            if self.chkFilterContact.isChecked():
                tableContact = db.table('ClientContact')
                contact = forceStringEx(self.edtFilterContact.text())
                condContact = [tableContact['client_id'].eq(tableClient['id']),
                                   tableContact['deleted'].eq(0),
                                   tableContact['contact'].like(contactToLikeMask(contact))
                                  ]
                cond.append(db.existsStmt(tableContact, condContact))

            if self.chkFilterAddress.isChecked():
                addrType        = self.cmbFilterAddressType.currentIndex()
                KLADRCode       = self.cmbFilterAddressCity.code()
                KLADRStreetCode = self.cmbFilterAddressStreet.code()
                tableAddressHouse = db.table('AddressHouse')
                tableAddress = db.table('Address')
                condAddr = [ tableAddressHouse['KLADRCode'].eq(KLADRCode),
                             tableAddressHouse['KLADRStreetCode'].eq(KLADRStreetCode),
                           ]
                addrIdList = db.getIdList(tableAddress.leftJoin(tableAddressHouse, tableAddressHouse['id'].eq(tableAddress['house_id'])), tableAddress['id'].name(), condAddr)
                addAddressCond(cond, addrType, addrIdList)
        idList = db.getIdList(table, 'Client_Quoting.`id`', cond)
        self.lblPersonListCount.setText(formatRecordsCount(len(idList)))
        self.modelPeopleList.setIdList(idList)
        self.tblPeopleList.resizeColumnsToContents()


    @pyqtSignature('int')
    def on_cmbFilterClientQuotaKladr_currentIndexChanged(self, index):
        data = self.cmbFilterClientQuotaKladr.itemData(index)
        self.cmbFilterClientQuotaDistrictKladr.setKladrCode(data)


    def checkActionsRights(self):
        if QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]):
            self.actEditClient.setEnabled(True)
        else:
            self.actEditClient.setEnabled(False)
        if QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteEvents, urRegTabReadEvents]):
            self.actEditClientEvents.setEnabled(True)
        else:
            self.actEditClientEvents.setEnabled(False)


    def openClientCardFromAction(self):
        self.on_tblPeopleList_doubleClicked(None)


    def openClientEventsFromAction(self):
        quotingId = self.tblPeopleList.currentItemId()
        clientId = forceInt(QtGui.qApp.db.translate('Client_Quoting', 'id', quotingId, 'master_id'))
        dlg = CEventsList(self)
        dlg.setClientId(clientId)
        dlg.exec_()


    def on_buttonBox_reset(self):
        self.chkFilterLastName.setChecked(False)
        self.chkFilterFirstName.setChecked(False)
        self.chkFilterPatrName.setChecked(False)
        self.chkFilterBirthDay.setChecked(False)
        self.chkFilterSex.setChecked(False)
        self.chkFilterAge.setChecked(False)
        self.chkFilterContact.setChecked(False)
        self.chkFilterStatus.setChecked(False)
        self.chkFilterStage.setChecked(False)
        self.chkFilterOrgStructure.setChecked(False)
        self.chkFilterIdentifier.setChecked(False)
        self.chkFilterTicketNumber.setChecked(False)
        self.chkFilterRequest.setChecked(False)
        self.chkFilterAddress.setChecked(False)
        self.chkFilterClientQuotaKladr.setChecked(False)
        self.chkFilterClientQuotaOKATO.setChecked(False)
        self.chkQuotaLPUDirection.setChecked(False)

        self.edtFilterLastName.setEnabled(False)
        self.edtFilterFirstName.setEnabled(False)
        self.edtFilterPatrName.setEnabled(False)
        self.edtFilterBirthDay.setEnabled(False)
        self.cmbFilterSex.setEnabled(False)
        self.edtFilterBegAge.setEnabled(False)
        self.edtFilterEndAge.setEnabled(False)
        self.edtFilterContact.setEnabled(False)
        self.cmbFilterStatus.setEnabled(False)
        self.edtFilterStage.setEnabled(False)
        self.cmbFilterOrgStructure.setEnabled(False)
        self.edtFilterIdentifier.setEnabled(False)
        self.edtFilterTicketNumber.setEnabled(False)
        self.cmbFilterRequest.setEnabled(False)
        self.cmbFilterAddressType.setEnabled(False)
        self.cmbFilterAddressCity.setEnabled(False)
        self.cmbFilterAddressStreet.setEnabled(False)
        self.cmbFilterClientQuotaKladr.setEnabled(False)
        self.cmbFilterClientQuotaDistrictKladr.setEnabled(False)
        self.cmbQuotaLPUDirection.setEnabled(False)

        self.setTblPeopleListId()


    @pyqtSignature('int')
    def on_cmbFilterAddressCity_currentIndexChanged(self, index):
        code = self.cmbFilterAddressCity.code()
        self.cmbFilterAddressStreet.setCity(code)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.setTblPeopleListId()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    @pyqtSignature('int')
    def on_tabWidgetContent_currentChanged(self, index):
        widget = self.tabWidgetContent.widget(index)
        if widget == self.tabList:
            self.setTblPeopleListId()


    @pyqtSignature('QModelIndex')
    def on_tblPeopleList_doubleClicked(self, index):
        if QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]):
            quotingId = self.tblPeopleList.currentItemId()
            clientId = forceInt(QtGui.qApp.db.translate('Client_Quoting', 'id', quotingId, 'master_id'))
            if QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]):
                dialog = CClientEditDialog(self)
                try:
                    if clientId:
                        dialog.load(clientId)
                    if dialog.exec_():
                        clientId = dialog.itemId()
                finally:
                    dialog.deleteLater()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelQuotaType_currentChanged(self, current, previous):
        itemId = self.tblQuotaTypeLeaves.currentItemId()
        idList = self.selectQuotaTypeLeaves()
        self.modelQuotaTypeLeaves.setIdList(idList, itemId)
        #groupId = self.currentGroupId()
        self.modelQuotaType.update()
        self.renewTblQuotingAndSetTo()
#        if self.tblQuoting_Region.model():
#            self.tblQuoting_Region.setModel(None)
#            self.lblInfo.clear()
        self.setTblPeopleListId()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelQuotaTypeLeaves_currentChanged(self, current, previous):
        self.renewTblQuotingAndSetTo()
#        if self.tblQuoting_Region.model():
#            self.tblQuoting_Region.setModel(None)
#            self.lblInfo.clear()
        self.setTblPeopleListId()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelQuoting_currentChanged(self, current, previous):
        quotingId = self.tblQuoting.currentItemId()
        self.setRegionsForQuoting(quotingId)

    @pyqtSignature('')
    def on_calendar_selectionChanged(self):
        self.renewTblQuotingAndSetTo()
        self.setTblPeopleListId()


    @pyqtSignature('')
    def on_btnNewQuota_clicked(self):
        beginDate, endDate = self.createNewDates()
        props = {'cmbQuotaType' : True,
                 'quotaType_id' : self.getActualQuotaTypeId(),
                 'beginDate'    : beginDate,
                 'endDate'      : endDate}
        self.addNewQuota(self.getEditor(props))


    @pyqtSignature('')
    def on_btnProlongateQuota_clicked(self):
        self.editQuota(self.getEditor({'cmbQuotaType': False}))


    @pyqtSignature('')
    def on_btnEditQuota_clicked(self):
        self.editQuota(self.getEditor({'cmbQuotaType':True}))


    @pyqtSignature('QModelIndex')
    def on_tblQuoting_doubleClicked(self, index):
        self.editQuota(self.getEditor({'cmbQuotaType':True}))


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        reportHeader = u'Список квотников'
        self.tblPeopleList.setReportHeader(reportHeader)
        date = self.calendar.selectedDate().toString('dd.MM.yyyy')
        reportDescription = u'Актуально на дату: '+date
        self.tblPeopleList.setReportDescription(reportDescription)
        html = self.tblPeopleList.contentToHTML()
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()



# ##################################################333

class CQuotingEditorDialog(CItemEditorBaseDialog, Ui_QuotingEditorDialog):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'Quoting')
        self.setupUi(self)
        self.cmbQuotaType.setTable('QuotaType')
        self.setWindowTitle(u'Квота')


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.cmbQuotaType.setValue(forceInt(record.value('quotaType_id')))
        self.edtBeginDate.setDate(forceDate(record.value('beginDate')))
        self.edtEndDate.setDate(forceDate(record.value('endDate')))
        self.edtLimit.setValue(forceInt(record.value('limitation')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('quotaType_id', QVariant(self.cmbQuotaType.value()))
        record.setValue('beginDate', QVariant(self.edtBeginDate.date()))
        record.setValue('endDate', QVariant(self.edtEndDate.date()))
        record.setValue('limitation', QVariant(self.edtLimit.value()))
        return record


    def setProps(self, props):
        cmbQuotaType = props.get('cmbQuotaType', False)
        quotaTypeId  = props.get('quotaType_id', None)
        if quotaTypeId:
            self.cmbQuotaType.setValue(quotaTypeId)
        beginDate = props.get('beginDate', None)
        if beginDate:
            endDate   = props.get('endDate', None)
            self.edtBeginDate.setDate(beginDate)
            self.edtEndDate.setDate(endDate)
        self.cmbQuotaType.setEnabled(cmbQuotaType)


    def checkDataEntered(self):
        result      = True
        limit       = self.edtLimit.value()
        quotaTypeId = self.cmbQuotaType.value()
        result = result and (limit or self.checkInputMessage(u'предел больше нуля', True, self.edtLimit))
        result = result and (quotaTypeId or self.checkInputMessage(u'тип квоты', False, self.cmbQuotaType))
        if result:
            result = result and self.checkInputDates()
        if result:
            self.checkChildsQuotaLimitationIfExists()
            self.checkParentsQuotaLimitationIfExists()
        return result


    def getCommonCond(self):
        beginDate   = self.edtBeginDate.date()
        endDate     = self.edtEndDate.date()
        db = QtGui.qApp.db
        table = db.table('Quoting')
        cond = [db.joinOr([db.joinAnd([table['beginDate'].le(beginDate),
                                       table['endDate'].ge(beginDate)]),
                           db.joinAnd([table['beginDate'].le(endDate),
                                       table['endDate'].ge(endDate)])])]
        cond.append(table['deleted'].eq(0))
        return cond


    def checkInputDates(self):
        quotaTypeId = self.cmbQuotaType.value()
        db = QtGui.qApp.db
        table = db.table('Quoting')
        cond = self.getCommonCond()
        cond.append(table['quotaType_id'].eq(quotaTypeId))
        if self._id:
            cond.append(table['id'].ne(self._id))
        record = db.getRecordEx(table, '*', cond)
        if record:
            QtGui.QMessageBox.warning(self,
                                      u'Внимание!',
                                      u'Пересечение однотипных квот в данном периоде',
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
            return False
        return True


    def checkParentsQuotaLimitationIfExists(self):
        limitation = self.edtLimit.value()
        quotaTypeId = self.cmbQuotaType.value()
        cond = self.getCommonCond()
        parentsIdList = self.getPossibleParentsIdList(quotaTypeId)
        if parentsIdList:
            self.checkStructure(parentsIdList, limitation, cond)


    def getPossibleParentsIdList(self, quotaTypeId):
        db = QtGui.qApp.db
        code = forceString(db.translate('QuotaType', 'id', quotaTypeId, 'code'))
        retult = []
        dotIndex = None
        while True:
            dotIndex = code.rfind('.', 0, dotIndex)
            if dotIndex < 0:
                break
            parentId = forceRef(db.translate('QuotaType', 'code', code[:dotIndex], 'id'))
            if parentId:
                retult.append(parentId)
        return retult


    def checkStructure(self, parentsIdList, limitation, cond):
        isFirst = True
        db = QtGui.qApp.db
        table = db.table('Quoting')
        needToShowMessage = False
        for parentId in parentsIdList:
            parentCode = forceString(db.translate('QuotaType', 'id', parentId, 'code'))
            childIdList = db.getIdList('QuotaType', 'id', 'group_code=\'%s\''%parentCode)
            tmpCond = list(cond)
            tmpCond.append(table['quotaType_id'].inlist(childIdList))
            if self._id:
                tmpCond.append(table['id'].ne(self._id))
            stmt = db.selectStmt(table, 'SUM(limitation)', tmpCond)
            query = db.query(stmt)
            childsLimitation = 0
            if query.first():
                childsLimitation += forceInt(query.value(0))
                if isFirst:
                    childsLimitation += limitation
                isFirst = False
            tmpCond = list(cond)
            tmpCond.append(table['quotaType_id'].eq(parentId))
            parentLimitationRecord = db.getRecordEx(table, '*', tmpCond)
            if parentLimitationRecord:
                parentLimitation = forceInt(parentLimitationRecord.value('limitation'))
                if parentLimitation < childsLimitation:
                    parentLimitation += (childsLimitation-parentLimitation)
                    parentLimitationRecord.setValue('limitation', QVariant(parentLimitation))
                    db.updateRecord(table, parentLimitationRecord)
                    needToShowMessage = True
        if needToShowMessage:
            QtGui.QMessageBox.warning(self,
                                      u'Внимание!',
                                      u'Пределы руководящих квот скорректированы',
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)


    def checkChildsQuotaLimitationIfExists(self):
        db = QtGui.qApp.db
        table = db.table('Quoting')
        cond = self.getCommonCond()
        quotaTypeId = self.cmbQuotaType.value()
        code = forceString(db.translate('QuotaType', 'id', quotaTypeId, 'code'))
        childIdList = db.getIdList('QuotaType', 'id', 'group_code=\'%s\''%code)
        cond.append(table['quotaType_id'].inlist(childIdList))
        stmt = db.selectStmt(table, 'SUM(limitation)', cond)
        query = db.query(stmt)
        if query.first():
            childsLimitation = forceInt(query.value(0))
            value = self.edtLimit.value()
            if value < childsLimitation:
                QtGui.QMessageBox.warning(self,
                                          u'Внимание!',
                                          u'Заданый предел меньше суммы пределов подчиненных квот.\nПредел изменен на %d'%childsLimitation,
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
                self.edtLimit.setValue(childsLimitation)


# ################################
class CQuotingIntInDocTableCol(CIntInDocTableCol, QObject):
    __pyqtSignals__ = ('dataIsChanged(int,int,QString)',
                      )
    def __init__(self, title, fieldName, width, **params):
        CIntInDocTableCol.__init__(self, title, fieldName, width, **params)
        QObject.__init__(self)
        self.oldValue = 0


    def setEditorData(self, editor, value, record):
        val = forceInt(value)
        self.oldValue = val
        editor.setValue(val)
        editor.selectAll()


    def getEditorData(self, editor):
        val = editor.value()
        self.emit(SIGNAL('dataIsChanged(int,int,QString)'), val, self.oldValue, QString(self.fieldName()))
        return toVariant(val)


class CKLADRInDocTableCol(CInDocTableCol, QObject):
    __pyqtSignals__ = ('toCheckData(QString)',
                      )
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        QObject.__init__(self)
        self.editorModel = CKladrTreeModel(None)
        self.editorModel.setAllSelectable(True)
        self.codeIsValid = True
        self.currentCode = None


    def setCodeIsValid(self, val):
        self.codeIsValid = val


    def createEditor(self, parent):
        editor = CKLADRComboBox(parent)
        editor._model = self.editorModel
        editor.setModel(self.editorModel)
        editor._popupView.treeModel = self.editorModel
        editor._popupView.treeView.setModel(self.editorModel)
        return editor


    def setEditorData(self, editor, value, record):
        val = forceString(value)
        self.currentCode = val
        editor.setCode(val)


    def getEditorData(self, editor):
        val = QString(editor.code())
        self.emit(SIGNAL('toCheckData(QString)'), val)
        self.currentCode = None
        if self.codeIsValid:
            return toVariant(val)
        else:
            return QVariant()


    def toString(self, val, record):
        return QtGui.qApp.db.translate('kladr.KLADR', 'CODE', forceString(val), 'CONCAT(NAME,\' \', SOCR)')


class CKLADROKATOInDocTableCol(CKLADRInDocTableCol, QObject):
    __pyqtSignals__ = ('toCheckData(QString)',
                      )
    def __init__(self, title, fieldName, width, **params):
        CKLADRInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.currentCodeRegion = None
        self.currentCodeDistrict = None


    def setEditorData(self, editor, value, record):
        val = forceString(value)
        self.currentCodeRegion = val
        self.currentCodeDistrict = forceString(record.value('district_code'))
        editor.setCode(val)


    def getEditorData(self, editor):
        val = QString(forceString(editor.code()))
        self.emit(SIGNAL('toCheckData(QString)'), val)
        self.currentCodeRegion = None
        self.currentCodeDistrict = None
        if self.codeIsValid:
            return toVariant(val)
        else:
            return QVariant()


class COKATOCol(CTextCol):
    def __init__(self, title, fields, defaultWidth, alignment='l'):
        CTextCol.__init__(self, title, fields, defaultWidth, alignment)

    def format(self, values):
        return nameCase(forceString(QtGui.qApp.db.translate('kladr.OKATO', 'CODE', forceString(values[0].toString()), 'NAME')))


class COKATOInDocTableCol(CInDocTableCol, QObject):
    __pyqtSignals__ = ('toCheckData(QString)',
                      )
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        QObject.__init__(self)
        self.codeIsValid = True
        self.currentCodeRegion = None
        self.currentCodeDistrict = None


    def setCodeIsValid(self, val):
        self.codeIsValid = val


    def createEditor(self, parent):
        editor = CKladrOkatoComboBox(parent)
        return editor


    def setEditorData(self, editor, value, record):
        val = forceString(value)
        self.currentCodeDistrict = val
        self.currentCodeRegion = forceString(record.value('region_code'))
        editor.setValue(val)


    def getEditorData(self, editor):
        val = QString(forceString(editor.value()))
        self.emit(SIGNAL('toCheckData(QString)'), val)
        self.currentCodeDistrict = None
        self.currentCodeRegion = None
        if self.codeIsValid:
            return toVariant(val)
        else:
            return QVariant()


    def toString(self, val, record):
        return QtGui.qApp.db.translate('kladr.OKATO', 'CODE', forceString(val), 'NAME')


class CQuoting_RegionModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'Quoting_Region', 'id', 'master_id', parent)
        self.addCol(CKLADRInDocTableCol(u'Регион', 'region_code', 13))
        self.addCol(CQuotingIntInDocTableCol(u'Предел', 'limitation', 8, high=65535))
        self.addCol(CQuotingIntInDocTableCol(u'Использовано', 'used', 8, high=65535))
        self.addCol(CQuotingIntInDocTableCol(u'Подтверждено', 'confirmed', 8, high=65535))
        self.addCol(CQuotingIntInDocTableCol(u'В очереди', 'inQueue', 8, high=65535))
        self._isEditable = True
        self._resume = None
        self.connect(self.cols()[1], SIGNAL('dataIsChanged(int, int, QString)'), self.dataIsChanged)
        self.connect(self.cols()[0], SIGNAL('toCheckData(QString)'), self.toCheckRegionCode)


    def setResume(self, resume):
        self._resume = resume


    def resume(self):
        return self._resume


    def dataIsChanged(self, val, oldVal, fieldName):
        fieldName = forceString(fieldName)
        self._resume[fieldName] += (val-oldVal)
        self.emit(SIGNAL('dataIsChanged()'))


    def toCheckRegionCode(self, code):
        existsItemsCode = getValueFromRecords(self.items(), 'region_code')
        col = self.cols()[0]
        if code != col.currentCode and code in existsItemsCode:
            col.setCodeIsValid(False)
            region = forceString(QtGui.qApp.db.translate('kladr.KLADR', 'CODE', code, 'CONCAT(NAME,\' \', SOCR)'))
            msg = u'<FONT COLOR=#FF0000>Данный регион уже присутствует: %s</FONT>' % region
            self.emit(SIGNAL('getMessage(QString)'), QString(msg))
        else:
            col.setCodeIsValid(True)
            self.emit(SIGNAL('regionAllRight()'))


    def setIsEditable(self, val):
        self._isEditable = val


    def isEditable(self):
        return self._isEditable


    def flags(self, index):
        if self._isEditable:
            column = index.column()
            if column == 1:
                row    = index.row()
                reg = forceString(self.data(index.child(row, 0)))
                if reg:
                    return CInDocTableModel.flags(self, index)
            elif column == 0:
                return CInDocTableModel.flags(self, index)
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def setData(self, index, value, role=Qt.EditRole):
        resume = CInDocTableModel.setData(self, index, value, role)
        if resume:
            self.emit(SIGNAL('recountQuotingRegionLimits()'))
        return resume


class CQuoting_DistrictModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'Quoting_District', 'id', 'master_id', parent)
        self.addCol(CKLADROKATOInDocTableCol(u'Регион', 'region_code', 13))
        self.addCol(COKATOInDocTableCol(u'Район', 'district_code', 13))
        self.addCol(CQuotingIntInDocTableCol(u'Предел', 'limitation', 8, high=65535))
        self.addCol(CQuotingIntInDocTableCol(u'Использовано', 'used', 8, high=65535))
        self.addCol(CQuotingIntInDocTableCol(u'Подтверждено', 'confirmed', 8, high=65535))
        self.addCol(CQuotingIntInDocTableCol(u'В очереди', 'inQueue', 8, high=65535))
        self._isEditable = True
        self._resume = None
        self.connect(self.cols()[2], SIGNAL('dataIsChanged(int, int, QString)'), self.dataIsChanged)
        self.connect(self.cols()[0], SIGNAL('toCheckData(QString)'), self.toCheckRegionCode)
        self.connect(self.cols()[1], SIGNAL('toCheckData(QString)'), self.toCheckDistrictCode)


    def setResume(self, resume):
        self._resume = resume


    def resume(self):
        return self._resume


    def dataIsChanged(self, val, oldVal, fieldName):
        fieldName = forceString(fieldName)
        self._resume[fieldName] += (val-oldVal)
        self.emit(SIGNAL('dataIsChanged()'))


    def toCheckRegionCode(self, code):
        existsItemsCode = [ (forceString(rec.value('region_code')), forceString(rec.value('district_code'))) for rec in self.items() ]
        col = self.cols()[0]
        if code != col.currentCodeRegion and (code, col.currentCodeDistrict) in existsItemsCode:
            col.setCodeIsValid(False)
            region = forceString(QtGui.qApp.db.translate('kladr.KLADR', 'CODE', code, 'CONCAT(NAME,\' \', SOCR)'))
            district = forceString( QtGui.qApp.db.translate('kladr.OKATO', 'CODE', col.currentCodeDistrict, 'NAME'))
            msg = u'<FONT COLOR=#FF0000>Данный регион с этим районом уже присутствует: %s - %s</FONT>'%(region, district)
            self.emit(SIGNAL('getMessage(QString)'), QString(msg))
        else:
            col.setCodeIsValid(True)
            self.emit(SIGNAL('regionAllRight()'))


    def toCheckDistrictCode(self, code):
        existsItemsCode = [ (forceString(rec.value('region_code')), forceString(rec.value('district_code'))) for rec in self.items() ]
        col = self.cols()[1]
        if code != col.currentCodeDistrict and (col.currentCodeRegion, code) in existsItemsCode:
            col.setCodeIsValid(False)
            region = forceString(QtGui.qApp.db.translate('kladr.KLADR', 'CODE', col.currentCodeRegion, 'CONCAT(NAME,\' \', SOCR)'))
            district = forceString( QtGui.qApp.db.translate('kladr.OKATO', 'CODE', code, 'NAME'))
            msg = u'<FONT COLOR=#FF0000>Данный район с этим регионом уже присутствует: %s - %s</FONT>'%(district, region)
            self.emit(SIGNAL('getMessage(QString)'), QString(msg))
        else:
            col.setCodeIsValid(True)
            self.emit(SIGNAL('regionAllRight()'))


    def setIsEditable(self, val):
        self._isEditable = val


    def isEditable(self):
        return self._isEditable


    def flags(self, index):
        if self._isEditable:
            column = index.column()
            if column == 2:
                row    = index.row()
                reg = forceString(self.data(index.child(row, 0)))
                if reg:
                    return CInDocTableModel.flags(self, index)
            elif column in [0, 1]:
                return CInDocTableModel.flags(self, index)
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def setData(self, index, value, role=Qt.EditRole):
        resume = CInDocTableModel.setData(self, index, value, role)
        if resume:
            self.emit(SIGNAL('recountQuotingDistrictLimits()'))
        return resume
