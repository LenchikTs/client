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
from PyQt4.QtCore import Qt, QDate, QDateTime, QObject, pyqtSignature, SIGNAL

from library.interchange     import getLineEditValue, setLineEditValue
from library.DialogBase      import CDialogBase
from library.InDocTable      import CInDocTableModel, CRBInDocTableCol
from library.ItemsListDialog import CItemsListDialogEx, CItemEditorBaseDialog
from library.TableModel      import CTableModel, CTextCol

from library.Utils           import forceRef, forceString

from RefBooks.Tables         import rbCode, rbName

from Reports.ReportView      import CReportViewDialog
from Users.Rights            import urAdmin, urHBEditCurrentDateFeed

from .Ui_RBMenu import Ui_RBMenu

from .Ui_MenuDialog  import Ui_MenuDialog # WTF? эта форма одна на два класса? или она забыла переехать?
from .Ui_MenuContent import Ui_MenuContent # WTF?


class CRBMenu(CItemsListDialogEx):
    def __init__(self, parent):
        CItemsListDialogEx.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbMenu', [rbCode, rbName])
        self.setWindowTitleEx(u'Шаблоны питания')


    def getItemEditor(self):
        return CRBMenuEditor(self)


    def select(self, props={}):
        table = self.model.table()
        return QtGui.qApp.db.getIdList(table.name(), self.idFieldName, '', self.order)

#
# ##########################################################################
#

class CRBMenuEditor(CItemEditorBaseDialog, Ui_RBMenu):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbMenu')
        self.addModels('MenuContent', CMenuContent(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Шаблон питания')
        self.setModels(self.tblMenuContent, self.modelMenuContent, self.selectionModelMenuContent)
        self.setupDirtyCather()
        self.setPopupMenu()

    def setPopupMenu(self):
        self.tblMenuContent.addPopupDelRow()

    def delRow(self):
        pass


    def save(self):
        menu_id = CItemEditorBaseDialog.save(self)
        if menu_id:
            self.modelMenuContent.saveItems(menu_id)
        return menu_id


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, rbCode )
        setLineEditValue(self.edtName,                record, rbName )
        self.modelMenuContent.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, rbCode )
        getLineEditValue(self.edtName,                record, rbName )
        return record


    def checkDataEntered(self):
        if not CItemEditorBaseDialog.checkDataEntered(self):
            return False
        for row, record in enumerate(self.modelMenuContent.items()):
            if not self.checkMenuContentEntered(row, record):
                return False
        return True


    def checkMenuContentEntered(self, row, record):
        result = True
        result = result and (forceRef(record.value('mealTime_id')) or self.checkInputMessage(u'период питания', False, self.tblMenuContent, row, record.indexOf('mealTime_id')))
        result = result and (forceRef(record.value('diet_id')) or self.checkInputMessage(u'стол питания', False, self.tblMenuContent, row, record.indexOf('diet_id')))
        return result


class CMenuContent(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbMenu_Content', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Периоды питания', 'mealTime_id', 30, 'rbMealTime', addNone=False))
        self.addCol(CRBInDocTableCol(u'Столы питания', 'diet_id', 30, 'rbDiet', addNone=False))


class CMenuDialog(CDialogBase, Ui_MenuDialog):
    def __init__(self, parent, cols, tableName, order, forSelect=False, filterClass=None, financeId=None, clientId=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setup(cols, tableName, order, forSelect, filterClass, financeId, clientId)

    def getHBEditFeedRight(self):
        app = QtGui.qApp
        loggedIn = bool(app.db) and (app.demoMode or app.userId is not None)
        return app.userHasRight(urHBEditCurrentDateFeed) or (loggedIn and app.userHasRight(urAdmin))

    def setup(self, cols, tableName, order, forSelect=False, filterClass=None, financeId=None, clientId=None):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.forSelect = forSelect
        self.filterClass = filterClass
        self.financeId = financeId
        self.clientId = clientId
        self.props = {}
        self.order = order
        self.model = CTableModel(self, cols, tableName)
        idList = self.select(self.props)
        self.model.setIdList(idList)
        self.tblItems.setModel(self.model)
        self.cmbFinance.setTable('rbFinance')
        self.cmbFinance.setValue(self.financeId)
        self.edtFeaturesToEat.setText(u'')
        if self.getHBEditFeedRight():
            begDate = QDate.currentDate()
            self.edtBegDate.setDate(begDate)
            self.edtEndDate.setDate(begDate)
        else:
            begDate = QDateTime.currentDateTime().addSecs(-32400).date().addDays(1)
            self.edtBegDate.setDate(begDate)
            self.edtBegDate.setMinimumDate(begDate)
            self.edtEndDate.setDate(begDate)
            self.edtEndDate.setMinimumDate(begDate)
        if idList:
            self.tblItems.selectRow(0)
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.label.setText(u'всего: %d' % len(idList))

        QObject.connect(
            self.tblItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)


    def select(self, props):
        db = QtGui.qApp.db
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        tableRBMenu = db.table('rbMenu')
        tableRBDiet = db.table('rbDiet')
        tableRBMenuContent = db.table('rbMenu_Content')
        table = tableRBMenuContent.innerJoin(tableRBMenu, tableRBMenu['id'].eq(tableRBMenuContent['master_id']))
        table = table.innerJoin(tableRBDiet, tableRBDiet['id'].eq(tableRBMenuContent['diet_id']))
        cond = []
#        if begDate:
#            cond.append(db.joinOr([tableRBDiet['endDate'].isNull(), tableRBDiet['endDate'].ge(begDate)]))
#        if endDate:
#            cond.append(db.joinOr([tableRBDiet['begDate'].isNull(), tableRBDiet['begDate'].le(endDate)]))
        if begDate:
            cond.append(db.joinOr([tableRBDiet['begDate'].isNull(), tableRBDiet['begDate'].le(begDate)]))
        if endDate:
            cond.append(db.joinOr([tableRBDiet['endDate'].isNull(), tableRBDiet['endDate'].ge(endDate)]))
        date = begDate if begDate else (endDate if endDate else None)
        if self.clientId and date:
            cond.append(u'''(SELECT isSexAndAgeSuitable(0, (SELECT MAX(Client.birthDate) FROM Client WHERE Client.id = %s AND Client.deleted = 0), 0, rbDiet.age, %s))'''%(self.clientId, db.formatDate(date)))
        return QtGui.qApp.db.getDistinctIdList(table, 'rbMenu.id', cond, self.order)


    def selectItem(self):
        return self.exec_()


    def setCurrentItemId(self, itemId):
        self.tblItems.setCurrentItemId(itemId)


    def currentItemId(self):
        return self.tblItems.currentItemId()


    def renewListAndSetTo(self, itemId=None):
        idList = self.select(self.props)
        self.tblItems.setIdList(idList, itemId)
        self.label.setText(u'всего: %d' % len(idList))


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.renewListAndSetTo()


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.renewListAndSetTo()


    @pyqtSignature('QModelIndex')
    def on_tblItems_doubleClicked(self, index):
        self.selected = True
        self.close()


    @pyqtSignature('')
    def on_btnSelected_clicked(self):
        self.selected = True
        self.close()


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        itemId = self.currentItemId()
        if itemId:
            dialog = self.getItemEditor()
            try:
                dialog.load(itemId)
                if dialog.exec_():
                    itemId = dialog.itemId()
                    self.renewListAndSetTo(itemId)
            finally:
                dialog.deleteLater()


    def getReportHeader(self):
        return self.objectName()


    def getFilterAsText(self):
        return u''


    def contentToHTML(self):
        reportHeader=self.getReportHeader()
        self.tblItems.setReportHeader(reportHeader)
        reportDescription=self.getFilterAsText()
        self.tblItems.setReportDescription(reportDescription)
        return self.tblItems.contentToHTML()


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        html = self.contentToHTML()
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    def setSort(self, col):
        name=self.model.cols()[col].fields()[0]
        self.order = name
        header=self.tblItems.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(col, Qt.AscendingOrder)
        self.renewListAndSetTo(self.currentItemId())


class CGetRBMenu(CMenuDialog):
    def __init__(self, parent, financeId = None, clientId=None):
        CMenuDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbMenu', ['rbMenu.code', 'rbMenu.code'], False, None, financeId, clientId)
        self.setWindowTitleEx(u'Шаблоны питания')
        self.selected = False
        self.financeId = financeId
        self.clientId = clientId


    def getItemEditor(self):
        return CRBMenuContentView(self)


    def exec_(self):
        result = CMenuDialog.exec_(self)
        if self.selected:
            result = self.currentItemId()
        return result


class CRBMenuContentView(QtGui.QDialog, Ui_MenuContent):
    def __init__(self,  parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.tblMenuContent.setModel(CRBMenuContentViewModel(self))
        self.itemId = None


    def load(self, itemId):
        self.itemId = itemId
        if itemId:
            record = QtGui.qApp.db.getRecordEx('rbMenu', '*', 'id = %d'%(itemId))
            if record:
                self.edtCode.setText(forceString(record.value(rbCode)))
                self.edtName.setText(forceString(record.value(rbName)))
                self.tblMenuContent.model().loadItems(itemId)


class CRBMenuContentViewModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbMenu_Content', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Периоды питания', 'mealTime_id', 30, 'rbMealTime', addNone=False)).setReadOnly(True)
        self.addCol(CRBInDocTableCol(u'Столы питания', 'diet_id', 30, 'rbDiet', addNone=False)).setReadOnly(True)
