# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## диалог тестирования сканера
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QTimer

from library.Utils import exceptionToUnicode

from preferences.Ui_ScanTestDialog    import Ui_ScanTestDialog


class CScanTestDialog(QtGui.QDialog, Ui_ScanTestDialog):
    def __init__(self, parent, scanner):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.scanner = scanner
        self.scanner.timeout = 0.1

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'), self.checkScanner)
        self.timer.start(250)


    def checkScanner(self):
        data = None
        try:
            if self.scanner.inWaiting():
                data = self.scanner.readall()
        except Exception, e:
            QtGui.QMessageBox.information(self,
                                          u'Ошибка считывания со сканера',
                                          exceptionToUnicode(e),
                                          QtGui.QMessageBox.Close,
                                          QtGui.QMessageBox.Close)
            self.timer.stop()
        if data is not None:
            self.edtSample.appendPlainText(repr(data))

