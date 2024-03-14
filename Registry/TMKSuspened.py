# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from library.DialogBase import CConstructHelperMixin

from Ui_TMKSuspended import Ui_TMKWindow


class CTMKSuspenedWindow(QtGui.QWidget, Ui_TMKWindow, CConstructHelperMixin):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
