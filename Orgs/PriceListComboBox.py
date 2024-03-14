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
from PyQt4.QtCore import Qt, QDate, SIGNAL

from library.Utils            import forceString
from PriceListComboBoxPopup   import CPriceListComboBoxPopup
from PriceListComboBoxPopupEx import CPriceListComboBoxPopupEx


__all__ = ['CPriceListComboBox',
           'CPriceListComboBoxEx'
          ]


class CPriceListComboBox(QtGui.QComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup = None
        self.code = None
        self.date = QDate.currentDate()
        self.priceListOnly = False


    def showPopup(self):
        if not self._popup:
            self._popup = CPriceListComboBoxPopup(self)
            self.connect(self._popup,SIGNAL('PriceListCodeSelected(int)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos2 = self.rect().topLeft()
        pos = self.mapToGlobal(pos)
        pos2 = self.mapToGlobal(pos2)
        size = self._popup.sizeHint()
        width = max(size.width(), self.width())
        size.setWidth(width)
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()
        self._popup.setDate(self.date)
        self._popup.setPriceListCode(self.code, self.priceListOnly)


    def setPriceListOnly(self, priceListOnly):
        self.priceListOnly = priceListOnly


    def setDate(self, date):
        self.date = date


    def setValue(self, code):
        self.code = code
        self.updateText()


    def value(self):
        return self.code


    def updateText(self):
        self.setEditText(codeToTextPriceList(self.code))


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            self.setValue(None)
            event.accept()
        elif key == Qt.Key_Backspace: # BS
            self.setValue(None)
            event.accept()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)


def codeToTextPriceList(contractId):
    text = ''
    if contractId:
        db = QtGui.qApp.db
        tableContract = db.table('Contract')
        tableRBFinance = db.table('rbFinance')
        cols = [tableRBFinance['code'],
                tableRBFinance['name'],
                tableContract['grouping'],
                tableContract['resolution'],
                tableContract['number'],
                tableContract['date'],
                tableContract['begDate'],
                tableContract['endDate']
                ]
        cond = [tableContract['id'].eq(contractId),
                tableContract['deleted'].eq(0)
               ]
        table = tableContract.leftJoin(tableRBFinance, tableRBFinance['id'].eq(tableContract['finance_id']))
        record = db.getRecordEx(table, cols, cond)
        if record:
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            grouping = forceString(record.value('grouping'))
            resolution = forceString(record.value('resolution'))
            number = forceString(record.value('number'))
            date = forceString(record.value('date'))
            begDate = forceString(record.value('begDate'))
            endDate = forceString(record.value('endDate'))
            text = ', '.join([field for field in (code + u'-' + name, u'Группа ' + grouping, u'Основание ' + resolution, u'Номер ' + number, date, begDate + u'-' + endDate) if field])
    else:
        text = ''
    return text


class CPriceListComboBoxEx(CPriceListComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None):
        CPriceListComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup = None
        self.code = None
        self.date = QDate.currentDate()
        self.priceListOnly = False


    def showPopup(self):
        if not self._popup:
            self._popup = CPriceListComboBoxPopupEx(self)
            self.connect(self._popup, SIGNAL('PriceListFindCodeSelected(int)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width())
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()
        self._popup.setPriceListOnly(self.priceListOnly)
        self._popup.setDatePriceList(self.date)
        self._popup.setCurrentIdPriceList(self.code)
        self._popup.setPriceListCode(self.code, self.priceListOnly)

