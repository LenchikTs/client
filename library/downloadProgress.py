# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtGui import QDialog

from library.Ui_downloadProgress import Ui_DownloadProgress


class CDownloadProgress(QDialog, Ui_DownloadProgress):
    def __init__(self):
        super(CDownloadProgress, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.progressBarFile.setValue(0)

def DownloadProgress():
    dialog = CDownloadProgress()
    dialog.setModal(True)
    dialog.show()

    QtGui.qApp.processEvents()

    return dialog

def LoadSizeFormat(pos, size):
    fPos = float(pos)
    fSize = float(size)

    PosIzm = u"Б"
    SizeIzm = u"Б"

    if fPos / 1024 > 1:
        fPos = fPos / 1024
        PosIzm = u"КБ"

    if fPos / 1024 > 1:
        fPos = fPos / 1024
        PosIzm = u"МБ"

    if fSize / 1024 > 1:
        fSize = fSize / 1024
        SizeIzm = u"КБ"

    if fSize / 1024 > 1:
        fSize = fSize / 1024
        SizeIzm = u"МБ"

    pStr = u"{:.2f}".format(fPos)
    pStr = pStr + " " + PosIzm
    pStr = pStr + u" из "
    pStr = pStr + u"{:.2f}".format(fSize)
    pStr = pStr + u" " + SizeIzm

    return pStr
