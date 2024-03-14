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
from PyQt4.QtCore import Qt, SIGNAL

from library.ESKLP.SmnnComboBoxPopupEx import CSmnnComboBoxPopupEx
from library.ROComboBox import CROComboBox
from library.Utils      import forceStringEx
from Users.Rights       import urEditChkOnlyExistsNomenclature


__all__ = [ 'CSmnnComboBoxEx',
          ]

class CSmnnComboBoxEx(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None, mainClientId = None, regAddressInfo = {}, logAddressInfo = {}, defaultAddressInfo = None):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup=None
        self.UUID = None
        self.nomenclatureId = None
        self.financeId = None
        self.nomenclatureIdList = []
        self.orgStructureId = None
        self.isOnlyExists = False


    def showPopup(self):
        if not self._popup:
            self._popup = CSmnnComboBoxPopupEx(self)
            self.connect(self._popup, SIGNAL('smnnUUIDSelected(QString)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos2 = self.rect().topLeft()
        pos = self.mapToGlobal(pos)
        pos2 = self.mapToGlobal(pos2)
        size = self._popup.sizeHint()
        width= max(size.width(), self.width())
        size.setWidth(width)
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()
        self._popup.setFinanceId(self.financeId)
        self._popup.setOnlyExists(self.isOnlyExists)
        self._popup.setOrgStructureId(self.orgStructureId)
        self._popup.setUUID(self.UUID)
        self._popup.setNomenclatureId(self.nomenclatureId)
        self._popup.setNomenclatureIdList(self.nomenclatureIdList)
        if not QtGui.qApp.userHasRight(urEditChkOnlyExistsNomenclature):
            self._popup.setOnlyExistsEnabled(False)
        self._popup.on_buttonBox_apply()


    def setOrgStructureId(self, value):
        self.orgStructureId = value


    def getOrgStructureId(self):
        return self.orgStructureId


    def setFinanceId(self, value):
        self.financeId = value


    def setOnlyExists(self, value):
        self.isOnlyExists = value


    def setNomenclatureIdList(self, nomenclatureIdList):
        self.nomenclatureIdList = nomenclatureIdList


    def setNomenclatureId(self, nomenclatureId):
        self.nomenclatureId = nomenclatureId
#        if self.nomenclatureId:
#            db = QtGui.qApp.db
#            tableEsklp_Smnn = db.table('esklp.Smnn')
#            tableNC = db.table('rbNomenclature')
#            tableESKLP_Klp = db.table('esklp.Klp')
#            cond = []
#            order = u'esklp.Smnn.code, esklp.Smnn.mnn, esklp.Smnn.form'
#            queryTable = tableNC.innerJoin(tableESKLP_Klp, tableESKLP_Klp['UUID'].eq(tableNC['esklpUUID']))
#            queryTable = queryTable.innerJoin(tableEsklp_Smnn, tableEsklp_Smnn['id'].eq(tableESKLP_Klp['smnn_id']))
#            cond.append(tableNC['id'].eq(self.nomenclatureId))
#            record = db.getRecordEx(queryTable, [tableEsklp_Smnn['UUID']], cond, order=order)
#            UUID = forceStringEx(record.value('UUID')) if record else None
#            self.setValue(UUID)


    def setValue(self, UUID):
        self.UUID = UUID
        self.updateText()
        self.lineEdit().setCursorPosition(0)


    def value(self):
        return self.UUID


    def text(self):
        return self.lineEdit().text()


    def setText(self, text):
        self.lineEdit().setText(text)


    def updateText(self):
        name = u''
        db = QtGui.qApp.db
        table = db.table('esklp.Smnn')
        if self.UUID:
            record = db.getRecordEx(table, [table['code'], table['mnn'], table['form']], [table['UUID'].eq(self.UUID)])
            if record:
                name = forceStringEx(record.value('mnn'))
#                mnn = forceStringEx(record.value('mnn'))
#                if mnn:
#                    name += u'-' + mnn
#                form = forceStringEx(record.value('form'))
#                if form:
#                    name += u', ' + form
        self.setEditText(name)


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            event.ignore()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            event.ignore()
        if key == Qt.Key_Delete or key == Qt.Key_Backspace:
            self.setValue(None)
            event.accept()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)

