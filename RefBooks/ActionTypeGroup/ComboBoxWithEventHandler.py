# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox


class CComboBoxWithKeyEventHandler(QComboBox):
    """QComboBox, реагирующий на нажатие Delete"""
    def __init__(self, parent=None):
        super(CComboBoxWithKeyEventHandler, self).__init__(parent)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            self.setCurrentIndex(0)
        else:
            QComboBox.keyPressEvent(self, event)
