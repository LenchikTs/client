# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\RelatedEventAndActionListDialog.ui'
#
# Created: Fri Apr 19 14:57:49 2019
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_RelatedEventAndActionListDialog(object):
    def setupUi(self, RelatedEventAndActionListDialog):
        RelatedEventAndActionListDialog.setObjectName(_fromUtf8("RelatedEventAndActionListDialog"))
        RelatedEventAndActionListDialog.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(RelatedEventAndActionListDialog)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(RelatedEventAndActionListDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabActions = CRelatedActionListPage()
        self.tabActions.setObjectName(_fromUtf8("tabActions"))
        self.tabWidget.addTab(self.tabActions, _fromUtf8(""))
        self.tabEvents = CRelatedEventListPage()
        self.tabEvents.setObjectName(_fromUtf8("tabEvents"))
        self.tabWidget.addTab(self.tabEvents, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(RelatedEventAndActionListDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RelatedEventAndActionListDialog)

    def retranslateUi(self, RelatedEventAndActionListDialog):
        RelatedEventAndActionListDialog.setWindowTitle(_translate("RelatedEventAndActionListDialog", "Связанные события/мероприятия", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabActions), _translate("RelatedEventAndActionListDialog", "Мероприятия", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEvents), _translate("RelatedEventAndActionListDialog", "События", None))

from Events.RelatedEventListPage import CRelatedEventListPage
from Events.RelatedActionListPage import CRelatedActionListPage
