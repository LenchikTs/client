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

from library.ESKLP.SmnnGrlsLfNomenclatureExpenseComboBoxPopup import CSmnnGrlsLfNomenclatureExpenseComboBoxPopup
from library.ROComboBox import CROComboBox
from library.Utils      import forceStringEx
from Users.Rights       import urEditChkOnlyExistsNomenclature


__all__ = [ 'CGrlsLfNomenclatureExpenseComboBox',
          ]

class CGrlsLfNomenclatureExpenseComboBox(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None, mainClientId = None, regAddressInfo = {}, logAddressInfo = {}, defaultAddressInfo = None):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup=None
        self.isType = 1
        self.lfFormId = None
        self.UUID = ''
        self.nomenclatureId = None
        self.nomenclatureIdList = []
        self.orgStructureId = None
        self._smnnUUID = None
        self.isOnlyExists = False
        self._isOnlySmnnUUID = False


    def showPopup(self):
        if not self._popup:
            self._popup = CSmnnGrlsLfNomenclatureExpenseComboBoxPopup(self)
            self.connect(self._popup, SIGNAL('smnnLfFormIdSelected(QString, int)'), self.setValue)
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
        self._popup.setIsType(self.isType)
        self._popup.setOnlySmnnUUID(self._isOnlySmnnUUID)
        self._popup.setOnlyExists(self.isOnlyExists)
        self._popup.setOrgStructureId(self.orgStructureId)
        self._popup.setLfFormId(self.lfFormId)
        self._popup.setNomenclatureId(self.nomenclatureId)
        self._popup.setNomenclatureIdList(self.nomenclatureIdList)
        self._popup.setNomenclatureSmnnUUID(self._smnnUUID)
        if not QtGui.qApp.userHasRight(urEditChkOnlyExistsNomenclature):
            self._popup.setOnlyExistsEnabled(False)
        self._popup.on_buttonBox_apply()


    def setOnlySmnnUUID(self, value):
        self._isOnlySmnnUUID = value


    def setOrgStructureId(self, value):
        self.orgStructureId = value


    def setNomenclatureId(self, nomenclatureId):
        self.nomenclatureId = nomenclatureId


    def setNomenclatureIdList(self, nomenclatureIdList):
        self.nomenclatureIdList = nomenclatureIdList


    def setNomenclatureSmnnUUID(self, smnnUUID):
        self._smnnUUID = smnnUUID


    def setOnlyExists(self, value):
        self.isOnlyExists = value


    def setValue(self, UUID, lfFormId):
        self.lfFormId = lfFormId
        self.UUID = UUID
        self.updateText()
        self.lineEdit().setCursorPosition(0)


    def value(self):
        return [self.UUID, self.lfFormId]


    def text(self):
        return self.lineEdit().text()


    def setText(self, text):
        self.lineEdit().setText(text)


    def updateText(self):
        result = u''
        db = QtGui.qApp.db
        table = db.table('rbLfForm')
        if self.lfFormId:
            record = db.getRecordEx(table, [table['name'], table['dosage']], [table['id'].eq(self.lfFormId), table['isESKLP'].eq(1)])
            if record:
                result = forceStringEx(record.value('name'))
                dosage = forceStringEx(record.value('dosage'))
                if dosage:
                    result += u' ' + dosage
        self.setEditText(result)


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            event.ignore()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            event.ignore()
        if key == Qt.Key_Delete or key == Qt.Key_Backspace:
            self.setValue('', None)
            event.accept()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)

