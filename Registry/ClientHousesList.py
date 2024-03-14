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

from PyQt4                   import QtGui
from PyQt4.QtCore            import QObject, Qt, SIGNAL

from library.abstract        import abstract
from library.DialogBase      import CConstructHelperMixin
from library.Utils           import forceInt, forceRef, forceString

from Ui_ClientHousesList     import Ui_ClientHousesList
from Registry.Utils          import getHousesList


class CClientHousesList():
    def __init__(self, parent,  streetCode = None, house = None, corp = None):
        self.parent = parent
        self.house = house
        self.corp = corp
        self.models = []
        self.checkFailedAt = []

        bases = QtGui.qApp.getGlobalPreference('22') # WTF?
        if bases:
            bases = bases.split(';')
            for base in bases:
                name = base.split(':')
                base = name[0]
                oper = forceInt(name[1]) if len(name) > 1 else 0
                if base == u'еис':
                    self.models.append(CEisHouses(parent, oper))
                if base == u'кладр':
                    self.models.append(CKladrHouses(parent, oper))

    def showHousesList(self, streetCode, house = None, corpus = None):
        house = house.strip()
        corpus = corpus.strip()
        dialog = CClientHousesListDialog(self.parent)
        for model in self.models:
            model.prepare(dialog)
            model.fillData(streetCode, house, corpus)
        for i in range(0, dialog.tabWidget.count()):
            if dialog.tabWidget.isTabEnabled(i):
                dialog.tabWidget.setCurrentIndex(i)
                break
        dialog.exec_()
        item = dialog.getResult()
        if item:
            house = item[0]
            corpus = item[1]
        for model in self.models:
            model.table = None
        dialog.deleteLater()
        return house, corpus

    def loadData(self, streetCode):
        for model in self.models:
            model.loadData(streetCode)

    def checkHouse(self, house, corp):
        result = 0
        self.checkFailedAt = []
        for model in self.models:
            row = model.getHouseRow(house, corp)
            result = result | 0 if row else model.checkRule
            if not row and model.checkRule:
                self.checkFailedAt.append(model.getName())
        return result

    def getCheckResult(self):
        return ','.join(self.checkFailedAt)


class CClientHousesListDialog(QtGui.QDialog, Ui_ClientHousesList, CConstructHelperMixin):
    def __init__(self,  parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.tabWidget.setTabEnabled(0, False)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.selectedItem = None
        QObject.connect(self.tblHousesList, SIGNAL("doubleClicked(QModelIndex)"), self.on_housesList_doubleClicked)

    def on_housesList_doubleClicked(self, index):
        widget = self.tabWidget.currentWidget()
        table = widget.focusWidget()
        self.selectedItem = table.selectedItems()
        self.close()

    def getResult(self):
        result = None
        if self.selectedItem:
            result = [forceString(self.selectedItem[0].text()),  forceString(self.selectedItem[1].text())]
        return result

    def getHouseListCheckResult(self):
        return ','.join(self.checkFailedAt)

    def selectRow(self, house, corp):
        for i in range(0, self.tabWidget.count()):
            tbl = self.tabWidget.widget(i)
            model = tbl.model()
            row = model.getHouseRow(house, corp)
            if row:
                tbl.selectRow(row)


class CHousesListModel():
    def __init__(self, parent):
        self.items = []
        self.streetCode = None
        self.table = None
        self.loaded = False


    def getHouseRow(self, house, corp):
        for i, item in enumerate(self.items):
            if house == item[0] and corp == item[1]:
                return i
        return None


    def getHousesListItemId(self, row):
        item = self.items[row]
        return forceRef(item.value('id'))


    def fillData(self, streetCode, selHouse = None, selCorp = None):
        if not self.loaded or self.streetCode != streetCode:
            self.loadData(streetCode, selHouse, selCorp)
        if self.table:
            self.table.setRowCount( len(self.items) )
            for i, item in enumerate(self.items):
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(item[0]))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(item[1]))
                if selHouse == item[0] and selCorp == item[1]:
                    self.table.selectRow(i)

    @abstract
    def loadData(self, streetCode, selHouse = None, selCorp = None):
        pass


class CKladrHouses(CHousesListModel):
    def __init__(self, parent, oper):
        CHousesListModel.__init__(self, parent)
        self.loaded = False
        self.items = []
        self.streetCode = None
        self.checkRule = oper

    def loadData(self, streetCode, selHouse = None, selCorp = None):
        if streetCode:
            self.items = []
            db = QtGui.qApp.db
            table = db.table('kladr.DOMA')
            cols = [table['NAME'],
                    table['KORP'],
                    table['CODE'],
                    table['flatHouseList']
                    ]
            records = db.getRecordList(table, cols, [table['CODE'].like(streetCode[:15] + '____')], 'kladr.DOMA.NAME, kladr.DOMA.KORP ')
            numberList = getHousesList(records)
            numberListKeys = numberList.keys()
            numberListKeys.sort()
            for number in numberListKeys:
                number = unicode(number)
                korpList = numberList.get(number, [])
                if korpList:
                    for corp in korpList:
                        item = [number, corp]
                        self.items.append(item)
            self.loaded = True
            self.streetCode = streetCode

    def prepare(self, dialog):
        dialog.tabWidget.setTabEnabled(0, True)
        self.table = dialog.tblHousesList

    def getName(self):
        return u'КЛАДР'


class CEisHouses(CHousesListModel):
    def __init__(self, parent, oper):
        CHousesListModel.__init__(self, parent)
        self.loaded = False
        self.checkRule = oper

    def prepare(self, dialog):
        dialog.eisTab = QtGui.QWidget()
        dialog.eisTab.setObjectName('eisTab')
        dialog.verticalLayout2 = QtGui.QVBoxLayout(dialog.eisTab) # WFT?
        dialog.verticalLayout2.setObjectName('verticalLayout2')
        dialog.tblEisHousesList = QtGui.QTableWidget(dialog.eisTab)
        dialog.tblEisHousesList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        dialog.tblEisHousesList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        dialog.tblEisHousesList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        dialog.tblEisHousesList.setObjectName('tblEisHousesList')
        dialog.tblEisHousesList.setColumnCount(2)
        dialog.tblEisHousesList.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        dialog.tblEisHousesList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        dialog.tblEisHousesList.setHorizontalHeaderItem(1, item)
        dialog.tblEisHousesList.horizontalHeader().setStretchLastSection(True)
        dialog.tblEisHousesList.verticalHeader().setVisible(False)
        dialog.tblEisHousesList.verticalHeader().setDefaultSectionSize(20)
        dialog.verticalLayout2.addWidget(dialog.tblEisHousesList)
        dialog.tabWidget.addTab(dialog.tblEisHousesList, u'ЕИС')
        item = dialog.tblEisHousesList.horizontalHeaderItem(0)
        item.setText(u'Дом')
        item = dialog.tblEisHousesList.horizontalHeaderItem(1)
        item.setText(u'Корпус')
        self.table = dialog.tblEisHousesList
        QObject.connect(dialog.tblEisHousesList, SIGNAL('doubleClicked(QModelIndex)'), dialog.on_housesList_doubleClicked)


    def loadData(self, streetCode, selHouse = None, selCorp = None):
        if streetCode:
            db = QtGui.qApp.db
            self.items = []
            tableStreet = db.table('kladr.STREET')
            tableEisHouse = db.table('kladr.eisHouse')
            streetRecord = db.getRecordEx(tableStreet, 'eisPrefix', tableStreet['CODE'].eq(streetCode))
            if streetRecord:
                eisPrefix = forceInt(streetRecord.value(0))
                cols = [tableEisHouse['HOUSE'], tableEisHouse['KORPUS']]
                houseRecords = db.getRecordList(tableEisHouse, cols, tableEisHouse['ID_PREFIX'].eq(eisPrefix))
                for record in houseRecords:
                    house = forceString(record.value('HOUSE')).strip()
                    corp = forceString(record.value('KORPUS')).strip()
                    item = [house, corp]
                    self.items.append(item)
            self.loaded = True
            self.streetCode = streetCode


    def getName(self):
        return u'ЕИС'
