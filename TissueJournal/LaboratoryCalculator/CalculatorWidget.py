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
from PyQt4.QtCore import pyqtSignature, SIGNAL, QMimeData, QString

from library.Utils import forceInt
from LaboratoryCalculatorTable import CLaboratoryCalculatorTableModel

from Ui_CalculatorWidget import Ui_CalculatorWidget

class CCalculatorWidget(QtGui.QWidget, Ui_CalculatorWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.createButtonGroup()
        self._model = CLaboratoryCalculatorTableModel(self)
        self.tableView.setModel(self._model)
        rounding = forceInt(QtGui.qApp.preferences.appPrefs.get('calculatorRounding', 0))
        self.edtRounding.setValue(rounding)
        self._model.setRounding(rounding)


    def rounding(self):
        return self.edtRounding.value()


    def createButtonGroup(self):
        self.buttonGroup = QtGui.QButtonGroup(self)
        self.buttonGroup.addButton(self.btnZero)
        self.buttonGroup.addButton(self.btnOne)
        self.buttonGroup.addButton(self.btnTwo)
        self.buttonGroup.addButton(self.btnThree)
        self.buttonGroup.addButton(self.btnFour)
        self.buttonGroup.addButton(self.btnFive)
        self.buttonGroup.addButton(self.btnSix)
        self.buttonGroup.addButton(self.btnSeven)
        self.buttonGroup.addButton(self.btnEight)
        self.buttonGroup.addButton(self.btnNine)
        self.buttonGroup.addButton(self.btnDiv)
        self.buttonGroup.addButton(self.btnMultiply)
        self.buttonGroup.addButton(self.btnMinus)
        self.buttonGroup.addButton(self.btnPlus)
        self.buttonGroup.addButton(self.btnEnter)
        self.buttonGroup.addButton(self.btnReset)
        self.buttonGroup.addButton(self.btnCancel)
        self.buttonGroup.addButton(self.btnResetAdditional)
        self.connect(self.buttonGroup, SIGNAL('buttonClicked(QAbstractButton*)'), self.on_buttonGroupClicked)


    def enabledKeys(self, keys):
        for btn in self.buttonGroup.buttons()[:-4]:
            btn.setEnabled(unicode(btn.text()) in keys)


    def resetButtons(self):
        additionalKeyList = self._model.additionalKeyList()
        for btn in self.buttonGroup.buttons()[:-4]:
            if unicode(btn.text()) not in additionalKeyList:
                btn.setEnabled(False)


    def clear(self):
        self.resetButtons()
        self._model.commands(['clear', 'reset'])
        self.edtLeukocytes.setValue(0)
        self.edtLeukocytes.setEnabled(True)
        self.lblLeukocytes.setEnabled(True)
        self.edtGG.setValue(0)
        self.edtGG.setEnabled(True)
        self.lblGG.setEnabled(True)
        self.edtEE.setValue(0)
        self.edtEE.setEnabled(True)
        self.lblEE.setEnabled(True)
        self.edtLeukocytes.setValue(0)


    def reset(self):
        self.resetButtons()
        self._model.command('resetData')


    def loadLastSetData(self):
        self._model.loadLastSetData()


    def load(self, data):
        self._model.load(data)


    def resetAdditional(self):
        additionalKeyList = self._model.additionalKeyList()
        for btn in self.buttonGroup.buttons()[:-4]:
            if unicode(btn.text()) in additionalKeyList:
                btn.setEnabled(False)
        self._model.resetAdditional()


    def on_buttonGroupClicked(self, button):
        btnText = unicode(button.text())
        if not self._model.done(btnText, self.edtRounding.value()):
            if btnText == 'E':
                self.sentData()
            elif btnText == '.':
                self.reset()
            elif btnText == u'Отменить':
                self.loadLastSetData()
#                self.sentData(minimized=False)
            elif btnText == u'Отменить назначения':
                self.resetAdditional()


    def sentData(self, minimized=True):
        data = self._model.formatData()
        mimeData = QMimeData()
        mimeData.setData(QtGui.qApp.outputMimeDataType,
                         QString(data).toUtf8())
        QtGui.qApp.clipboard().setMimeData(mimeData)
        if self._model.hasOuterItems() and minimized:
            QtGui.qApp.mainWindow.showMinimized()


    def addButton(self, btn, group, name):
        btn.setEnabled(True)
        self._model.addAdditionalRow(unicode(btn.text()), group, name)


    def availableGroupList(self):
        return self._model.availableGroupList()


    def recountCI(self, gg, ee):
        normEE = int(str(ee*100)[:3]) if ee else 0
        return gg*3/normEE if normEE else 0


    @pyqtSignature('int')
    def on_edtMaxGroupValue_valueChanged(self, value):
        self._model.setMaxGroupValue(value)


    @pyqtSignature('int')
    def on_edtRounding_valueChanged(self, value):
        self._model.setRounding(value)
        self._model.recountPercentValueForGroup(value)

    @pyqtSignature('double')
    def on_edtGG_valueChanged(self, value):
        self.edtCI.setValue(self.recountCI(value, self.edtEE.value()))

    @pyqtSignature('double')
    def on_edtEE_valueChanged(self, value):
        self.edtCI.setValue(self.recountCI(self.edtGG.value(), value))
