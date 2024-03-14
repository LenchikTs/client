# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки соединения с ЕИС ОМС (СПб)
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QTimer

from Registry.IdentCard.EkpContactless  import CEkpContactless
from Registry.IdentCard.EkpContact      import CEkpContact

try:
    from library.SmartCard.SmartCardWatcher import CSmartCardWatcher
    gSmartCardAvailable = True
except:
    gSmartCardAvailable = False

from library.JsonRpc.client             import CJsonRpcClent
from library.SmartCard                  import hexDump
from library.Utils                      import (exceptionToUnicode,
                                                forceBool,
                                                forceString,
                                                toVariant,
                                               )

from Ui_EkpPage      import Ui_ekpPage
from Ui_ReaderLookup import Ui_readerLookup


class CEkpPage(Ui_ekpPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.edtIdentCardServiceUrl.setText(forceString(props.get('identCardServiceUrl', '')))
        self.chkEkpBarCodeEnabled.setChecked(forceBool(props.get('ekpBarCodeEnabled', True)))
        self.chkEkpContactlessEnabled.setChecked(forceBool(props.get('ekpContactlessEnabled', True)))
        self.chkEkpContactlessCheckATR.setChecked(forceBool(props.get('ekpContactlessCheckATR', True)))
        self.edtEkpContactlessReaders.setPlainText(forceString(props.get('ekpContactlessReaders', '')))
        self.chkEkpContactEnabled.setChecked(forceBool(props.get('ekpContactEnabled', True)))
        self.chkEkpContactCheckATR.setChecked(forceBool(props.get('ekpContactCheckATR', True)))
        self.edtEkpContactReaders.setPlainText(forceString(props.get('ekpContactReaders', '')))
        self.edtEkpContactLib.setText(forceString(props.get('ekpContactLib', '')))


    def getProps(self, props):
        props['identCardServiceUrl']   = toVariant(self.edtIdentCardServiceUrl.text())
        props['ekpBarCodeEnabled']     = toVariant(self.chkEkpBarCodeEnabled.isChecked())
        props['ekpContactlessEnabled'] = toVariant(self.chkEkpContactlessEnabled.isChecked())
        props['ekpContactlessCheckATR']= toVariant(self.chkEkpContactlessCheckATR.isChecked())
        props['ekpContactlessReaders'] = toVariant(self.edtEkpContactlessReaders.toPlainText())
        props['ekpContactEnabled']     = toVariant(self.chkEkpContactEnabled.isChecked())
        props['ekpContactCheckATR']    = toVariant(self.chkEkpContactCheckATR.isChecked())
        props['ekpContactReaders']     = toVariant(self.edtEkpContactReaders.toPlainText())
        props['ekpContactLib']         = toVariant(self.edtEkpContactLib.text())


    def updateWidgets(self):
        ekpEnabled = bool(self.edtIdentCardServiceUrl.text())
        cardWatcherAvailable = gSmartCardAvailable
        self.btnIdentCardServiceTest.setEnabled(ekpEnabled)
        self.lblEkpBarCodeEnabled.setEnabled(ekpEnabled)
        self.chkEkpBarCodeEnabled.setEnabled(ekpEnabled)

        self.lblEkpContactlessEnabled.setEnabled(ekpEnabled)
        self.chkEkpContactlessEnabled.setEnabled(ekpEnabled)
        ekpContactlessEnabled = ekpEnabled and self.chkEkpContactlessEnabled.isChecked()
        self.lblEkpContactlessCheckATR.setEnabled(ekpContactlessEnabled)
        self.chkEkpContactlessCheckATR.setEnabled(ekpContactlessEnabled)
        self.lblEkpContactlessReaders.setEnabled(ekpContactlessEnabled)
        self.edtEkpContactlessReaders.setEnabled(ekpContactlessEnabled)
        self.btnEkpContactlessReaderLookFor.setEnabled(ekpContactlessEnabled and cardWatcherAvailable)

        self.lblEkpContactEnabled.setEnabled(ekpEnabled)
        self.chkEkpContactEnabled.setEnabled(ekpEnabled)
        ekpContactEnabled = ekpEnabled and self.chkEkpContactEnabled.isChecked()
        self.lblEkpContactCheckATR.setEnabled(ekpContactEnabled)
        self.chkEkpContactCheckATR.setEnabled(ekpContactEnabled)
        self.lblEkpContactReaders.setEnabled(ekpContactEnabled)
        self.edtEkpContactReaders.setEnabled(ekpContactEnabled)
        self.btnEkpContactReaderLookFor.setEnabled(ekpContactEnabled and cardWatcherAvailable)
        self.lblEkpContactLib.setEnabled(ekpContactEnabled)
        self.edtEkpContactLib.setEnabled(ekpContactEnabled)


    def waitCardInReader(self, isConactless, widgetWithReaders):
        dlg = CReaderLookup(self)
        if isConactless:
            dlg.setInstruction(u'Поднесите карту к считывателю')
            dlg.setCardClass(CEkpContactless)
        else:
            dlg.setInstruction(u'Вставьте карту в считыватель')
            dlg.setCardClass(CEkpContact)
        if dlg.exec_():
            reader = dlg.getReader()
            if reader:
                widgetWithReaders.appendPlainText(reader)


    # #########################

    @pyqtSignature('QString')
    def on_edtIdentCardServiceUrl_textChanged(self, text):
        self.updateWidgets()


    @pyqtSignature('')
    def on_btnIdentCardServiceTest_clicked(self):
        serviceUrl = unicode(self.edtIdentCardServiceUrl.text())
        serviceUrl = serviceUrl.replace('${dbServerName}', QtGui.qApp.preferences.dbServerName)
        client = CJsonRpcClent(serviceUrl)
        try:
            client.call('search',
                        params={ 'identifierType': 'cardId',
                                 'identifier'    : '7800000000000007'
                               }
                       )
            QtGui.QMessageBox.information(self,
                                          u'Проверка подключения к сервису',
                                          u'Подключение успешно',
                                          QtGui.QMessageBox.Close,
                                          QtGui.QMessageBox.Close)

        except Exception as e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.information(self,
                                          u'Ошибка подключения к сервису',
                                          exceptionToUnicode(e),
                                          QtGui.QMessageBox.Close,
                                          QtGui.QMessageBox.Close)


    @pyqtSignature('bool')
    def on_chkEkpContactlessEnabled_toggled(self):
        self.updateWidgets()


    @pyqtSignature('')
    def on_btnEkpContactlessReaderLookFor_clicked(self):
        self.waitCardInReader(True,
                              self.edtEkpContactlessReaders
                             )


    @pyqtSignature('bool')
    def on_chkEkpContactEnabled_toggled(self):
        self.updateWidgets()


    @pyqtSignature('')
    def on_btnEkpContactReaderLookFor_clicked(self):
        self.waitCardInReader(False,
                              self.edtEkpContactReaders
                             )


class CReaderLookup(Ui_readerLookup, QtGui.QDialog):
    def __init__(self,  parent):
        QtGui.QDialog.__init__(self, parent)
        self.smartCardWatcher = CSmartCardWatcher() if gSmartCardAvailable else None
        self.smartCardTimer   = QTimer(self)
        self.smartCardTimer.setObjectName('smartCardTimer')
        self.setupUi(self)
        self.cardClass = None
        self.reader = None


    def checkSmartCard(self):
        self.smartCardWatcher.watch()


    def setInstruction(self, text):
        self.lblInstruction.setText(text)


    def setCardClass(self, cardClass):
        self.cardClass = cardClass


    def getReader(self):
        return self.reader


    def addSmartCardNotice(self, connection):
        self.pnlReader.setText(connection.getReader())
        atrHexDump = hexDump(connection.getATR(), ' ')
        if self.cardClass:
            if self.cardClass.atrIsSuitable(atrHexDump):
                conclusion = u'это знакомый ATR'
            else:
                conclusion = u'это незнакомый ATR'
        else:
            conclusion = u'проверка ATR не выполнялась'
        self.pnlAtr.setText('%s (%s)'%(atrHexDump, conclusion))
        self.reader = connection.getReader().strip()


    def exec_(self):
        try:
            if self.smartCardWatcher:
                self.smartCardWatcher.addSubscriber(self)
                self.smartCardTimer.start(250)
            return QtGui.QDialog.exec_(self)
        finally:
            if self.smartCardWatcher:
                self.smartCardTimer.stop()
                self.smartCardWatcher.removeSubscriber(self)


    @pyqtSignature('')
    def on_smartCardTimer_timeout(self):
        if self.smartCardWatcher:
            self.smartCardWatcher.watch()
