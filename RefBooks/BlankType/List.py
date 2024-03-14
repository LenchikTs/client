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
from PyQt4.QtCore import pyqtSignature


from library.interchange        import getComboBoxValue, getLineEditValue, getSpinBoxValue, setComboBoxValue, setLineEditValue, setSpinBoxValue
from library.ItemsListDialog    import CItemEditorBaseDialog
from library.TableModel         import CEnumCol, CIntCol, CTextCol

from library.Utils              import exceptionToUnicode, toVariant

from Blank.BlankItemsListDialog import CBlanksItemsListDialog
from RefBooks.Tables            import rbCode, rbName

from .Ui_RBBlanksEditor import Ui_ItemEditorDialog


class CBlankTypeList(CBlanksItemsListDialog):
    def __init__(self, parent):
        CBlanksItemsListDialog.__init__(self, parent, [
            CTextCol(u'код',                ['code'],  20),
            CTextCol(u'название',           ['name'],    20),
            CEnumCol(u'контроль серии',     ['checkingSerial'], [u'нет', u'мягко', u'жестко'], 20),
            CEnumCol(u'контроль номера',    ['checkingNumber'], [u'нет', u'мягко', u'жестко'], 20),
            CEnumCol(u'контроль количества',['checkingAmount'], [u'нет', u'мягко', u'жестко'], 20),
            CIntCol( u'Длина КС',           ['checkSumLen'], 20)
            ], 'rbTempInvalidDocument', 'rbBlankTempInvalids', 'ActionType', 'rbBlankActions', [])
        self.setWindowTitleEx(u'Типы бланков')
        self.treeItemsTempInvalid.expand(self.modelTree.index(0, 0))


    def setupUi(self, widget):
        CBlanksItemsListDialog.setupUi(self, widget)


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, widgetIndex):
        if widgetIndex == 0:
            self.treeItemsTempInvalid.expand(self.modelTree.index(0, 0))
        else:
            self.treeItemsOthers.expand(self.modelTree2.index(0, 0))


    def getItemEditor(self):
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 0:
            tableName = u'rbBlankTempInvalids'
            doctypeId = self.currentGroupId()
        else:
            tableName = u'rbBlankActions'
            doctypeId = self.currentGroupId()
        return CBlankTypeEditor(self, tableName, doctypeId)


class CBlankTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent, tableName, doctypeId):
        CItemEditorBaseDialog.__init__(self, parent, tableName)
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип бланка')
        self.setupDirtyCather()
        self.doctypeId = doctypeId


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, rbCode)
        setLineEditValue(self.edtName, record, rbName)
        setComboBoxValue(self.cmbCheckingSerial, record, 'checkingSerial')
        setComboBoxValue(self.cmbCheckingNumber, record, 'checkingNumber')
        setComboBoxValue(self.cmbCheckingAmount, record, 'checkingAmount')
        setComboBoxValue(self.cmbCheckingAmount, record, 'checkingAmount')
        setSpinBoxValue(self.edtCheckSumLen, record, 'checkSumLen')


    def getRecord(self):
        if not self.doctypeId:
            return None
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('doctype_id', toVariant(self.doctypeId))
        getLineEditValue(self.edtCode, record, rbCode)
        getLineEditValue(self.edtName, record, rbName)
        getComboBoxValue(self.cmbCheckingSerial, record, 'checkingSerial')
        getComboBoxValue(self.cmbCheckingNumber, record, 'checkingNumber')
        getComboBoxValue(self.cmbCheckingAmount, record, 'checkingAmount')
        getComboBoxValue(self.cmbCheckingAmount, record, 'checkingAmount')
        getSpinBoxValue(self.edtCheckSumLen, record, 'checkSumLen')
        return record


    def save(self):
        try:
            prevId = self.itemId()
            db = QtGui.qApp.db
            db.transaction()
            try:
                record = self.getRecord()
                if not record:
                    return True
                id = db.insertOrUpdate(db.table(self._tableName), record)
                self.saveInternals(id)
                db.commit()
            except:
                db.rollback()
                self.setItemId(prevId)
                raise
            self.setItemId(id)
            self.afterSave()
            return id
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)
            return None
