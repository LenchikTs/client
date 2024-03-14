# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
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

from library.ESKLP.ESKLPComboBoxPopup import CESKLPComboBoxPopup
from library.ROComboBox import CROComboBox
from library.Utils import forceInt, forceStringEx, forceString

__all__ = ['CESKLPComboBox',
           ]


class CESKLPComboBox(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                       )

    def __init__(self, parent=None):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup = None
        self.UUID = None
        self.installEventFilter(self)

    def showPopup(self):
        if not self._popup:
            self._popup = CESKLPComboBoxPopup(self)
            self.connect(self._popup, SIGNAL('ESKLPUUIDSelected(QString)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width())
        pos.setX(max(min(pos.x(), screen.right() - size.width()), screen.left()))
        pos.setY(max(min(pos.y(), screen.bottom() - size.height()), screen.top()))
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.setUUIDESKLPPopupUpdate(self.UUID)
        self._popup.show()

    def setValue(self, UUID):
        self.UUID = UUID
        self.updateText()
        self.lineEdit().setCursorPosition(0)

    def value(self):
        return self.UUID

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

    def updateText(self):
        self.setEditText(self.ESKLPNameToText(self.UUID))

    def ESKLPNameToText(self, UUID):
        text = ''
        if UUID:
            db = QtGui.qApp.db
            tableESKLP_Klp = db.table('esklp.Klp')
            cols = [tableESKLP_Klp['mass_volume_num'],
                    tableESKLP_Klp['mass_volume_name'],
                    tableESKLP_Klp['trade_name'],
                    tableESKLP_Klp['lf_norm_name'],
                    tableESKLP_Klp['dosage_norm_name'],
                    tableESKLP_Klp['pack1_name'],
                    tableESKLP_Klp['pack1_num'],
                    tableESKLP_Klp['pack2_name'],
                    tableESKLP_Klp['pack2_num'],
                    ]
            cond = [tableESKLP_Klp['UUID'].eq(UUID)]
            record = db.getRecordEx(tableESKLP_Klp, cols, cond)
            if record:
                mass_volume_num = forceStringEx(record.value('mass_volume_num')).upper()
                mass_volume_name = forceStringEx(record.value('mass_volume_name')).upper()
                trade_name = forceStringEx(record.value('trade_name')).upper()
                lf_norm_name = forceStringEx(record.value('lf_norm_name')).upper()
                dosage_norm_name = forceStringEx(record.value('dosage_norm_name')).upper()
                pack1_name = forceStringEx(record.value('pack1_name')).upper()
                # pack1_num = forceStringEx(record.value('pack1_num')).upper()
                pack2_name = forceStringEx(record.value('pack2_name')).upper()
                pack2_num = forceStringEx(forceInt(record.value('pack2_num'))).upper()
                nameList = [trade_name, lf_norm_name + u' ' + dosage_norm_name]
                if mass_volume_name and mass_volume_num:
                    nameList.append(pack1_name + u' ' + mass_volume_num + u' ' + mass_volume_name)
                    nameList.append(pack2_name + u' №' + pack2_num)
                else:
                    nameList.append(pack2_name + u' №' + forceString(forceInt(record.value('pack1_num')) * forceInt(record.value('pack2_num'))).upper())
                text = ', '.join([field for field in nameList if field])
        else:
            text = ''
        return text
