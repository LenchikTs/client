# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from library.DialogBase import CConstructHelperMixin

from Ui_DispExchange import Ui_DispExchangeWindow


class CDispExchangeWindow(QtGui.QWidget, Ui_DispExchangeWindow, CConstructHelperMixin):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
