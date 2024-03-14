# -*- coding: utf-8 -*-
# iiro: Incoming Invoice - Reverse Order
# Заголовок будет потом,
# сейчас это "превью"

# Средство для отображения обмена с МДЛП.
# ну как обмена - просто показ выполняемых шагов, реальные байты никому не нужны.
# 
#with CLogger(parentWidget, 'title') as logger:
#    logger.setAutoClose(setAutoClose.cmIfOf)
#    ...
#    logger.addText('message')
#    ...
#    logger.addText('another message')


from PyQt4.QtCore import pyqtSignature, QEventLoop
from PyQt4 import QtGui

from library.Utils import exceptionToUnicode

from Ui_Logger import Ui_Logger


class ELoggerClosed(Exception):
    pass


class CLogger(QtGui.QDialog, Ui_Logger):
    cmAlways = 0 # 
    cmNewer  = 1
    cmIfOk   = 2

    def __init__(self, parent, title):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.setModal(True)
        self._closeMode = self.cmIfOk
        self._inProgress = False
        self._closeRequired = False


    def setAutoClose(self, closeMode):
        self._closeMode = closeMode


    def closeEvent(self, event):
#        print 'closeEvent(self, event)', self._inProgress, self._closeRequired
        if self.interrupt():
            event.ignore()
        else:
            event.accept()


    def setWork(self):
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self._inProgress = True
        self.repaint()


    def setDone(self):
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self._inProgress = False
        self.repaint()


    def interrupt(self):
        if self._inProgress:
            self.setDone()
            self._closeRequired = True
            return True
        else:
            return False


    def _append(self, text):
        self.textBrowser.append(text)


    def append(self, text):
        if self._closeRequired:
            raise ELoggerClosed
        self._append(text)
        self.repaint() # иначе строка отоброжается с задержкой
        QtGui.qApp.processEvents()


    def __enter__(self):
        self.setWork()
        self.show()
        self.repaint()
        for cnt in xrange(5):
            # эта "магия" для того, чтобы окно успело прорисоваться...
            QtGui.qApp.flush()
            QtGui.qApp.processEvents(QEventLoop.ExcludeUserInputEvents)
            if not QtGui.qApp.hasPendingEvents():
                break
        return self


    def __exit__(self, exceptionType, exceptionValue, exceptionTraceback):
        ok = exceptionType is None or exceptionType == ELoggerClosed
        if not ok:
            self._append( exceptionToUnicode(exceptionValue) )
        self.setDone()
        if (    self._closeMode == self.cmAlways
             or ( self._closeMode == self.cmIfOk and ok )
           ):
            self.close()
        return ok


    def reject(self):
        if self.interrupt():
            pass
        else:
            QtGui.QDialog.reject(self)


    @pyqtSignature('')
    def on_buttonBox_rejected(self):
        self.reject()

