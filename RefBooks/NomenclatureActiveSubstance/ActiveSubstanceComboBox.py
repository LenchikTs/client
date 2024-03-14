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
from PyQt4.QtCore import SIGNAL

from RefBooks.NomenclatureActiveSubstance.ActiveSubstanceComboBoxPopup import CActiveSubstanceComboBoxPopup
from library.ROComboBox import CROComboBox
from library.Utils      import forceStringEx


__all__ = [ 'CActiveSubstanceComboBox',
          ]


class CActiveSubstanceComboBox(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None, mainClientId = None, regAddressInfo = {}, logAddressInfo = {}, defaultAddressInfo = None):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup=None
        self.activeSubstanceId = None
        self.nomenclatureId = None


    def showPopup(self):
        if not self._popup:
            self._popup = CActiveSubstanceComboBoxPopup(self)
            self.connect(self._popup, SIGNAL('activeSubstanceIdSelected(int)'), self.setValue)
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
        self._popup.setActiveSubstanceId(self.activeSubstanceId)
        self._popup.setNomenclatureId(self.nomenclatureId)
        self._popup.on_buttonBox_apply()


    def setNomenclatureId(self, nomenclatureId):
        self.nomenclatureId = nomenclatureId


    def setValue(self, activeSubstanceId):
        self.activeSubstanceId = activeSubstanceId
        self.updateText()


    def value(self):
        return self.activeSubstanceId


    def updateText(self):
        name = u''
        db = QtGui.qApp.db
        table = db.table('rbNomenclatureActiveSubstance')
        if self.activeSubstanceId:
            record = db.getRecordEx(table, [table['name'], table['mnnLatin']], [table['id'].eq(self.activeSubstanceId)])
            if record:
                name = forceStringEx(record.value('name'))
                if not name:
                    name = forceStringEx(record.value('mnnLatin'))
        self.setEditText(name)

